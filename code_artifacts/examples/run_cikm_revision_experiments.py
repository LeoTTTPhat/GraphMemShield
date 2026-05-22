import csv
import json
import os
import random
import sys
import time
from math import ceil
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graphmemshield import (  # noqa: E402
    CompositionReport,
    CrossSessionProbe,
    EdgeAdmissionPolicy,
    FixedUniverseRandomizedResponseAdmission,
    FullGraphReleasePrivacyReport,
    GraphMemGuard,
    GraphMemGuardPolicy,
    SessionGraphLink,
    TemporalPathInfer,
    randomized_response_privacy_loss,
    randomized_response_probabilities,
)
from graphmemshield.core.graph import DynamicMemoryGraph  # noqa: E402
from graphmemshield.core.types import MemoryEdge  # noqa: E402
from graphmemshield.adapters.sqlite_property_graph import (  # noqa: E402
    SQLitePropertyGraphAdapter,
)
from graphmemshield.adapters.kuzu_property_graph import KuzuPropertyGraphAdapter  # noqa: E402
from graphmemshield.datasets.dialogue import dialogue_records_to_graph  # noqa: E402
from graphmemshield.datasets.enterprise import (  # noqa: E402
    build_enterprise_health_finance_records,
)
from graphmemshield.evaluation.blackbox import (  # noqa: E402
    EvidenceDumpResponseGenerator,
    LocalAbstractiveResponseGenerator,
    OpenAIChatResponseGenerator,
    ResponseLeakageScorer,
    SemanticResponseLeakageScorer,
    TemplateResponseGenerator,
)
from graphmemshield.evaluation.metrics import (  # noqa: E402
    pairwise_ordering_accuracy,
)
from graphmemshield.evaluation.utility_evaluator import UtilityEvaluator  # noqa: E402
from graphmemshield.evaluation.statistics import ci95  # noqa: E402


OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")


def main() -> None:
    records = build_enterprise_health_finance_records()
    graph = dialogue_records_to_graph(records)
    rows: list[dict[str, Any]] = []
    rows.extend(_dataset_rows(records, graph))
    rows.extend(_backend_rows(graph))
    rows.extend(_kuzu_backend_rows(graph))
    rows.extend(_bounded_sharing_rows(graph))
    rows.extend(_multihop_rows(graph))
    rows.extend(_hybrid_pipeline_rows(graph))
    rows.extend(_provenance_error_rows(graph))
    rows.extend(_strong_generator_rows(graph))
    rows.extend(_utility_quality_rows(graph))
    rows.extend(_multiseed_bounded_sharing_rows())
    rows.extend(_adaptive_probe_rows(graph))
    rows.extend(_blackbox_rows(graph))
    rows.extend(_semantic_response_rows(graph))
    rows.extend(_session_link_rows(graph))
    rows.extend(_temporal_hidden_rows(graph))
    rows.extend(_fixed_universe_dp_rows(graph))
    rows.extend(_privacy_accounting_rows())
    rows.extend(_full_graph_privacy_rows(graph))

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    _write_json(rows, "tifs_revision_results.json")
    _write_csv(rows, "tifs_revision_results.csv")
    _write_markdown(rows, "tifs_revision_results.md")
    print(f"tifs revision rows: {len(rows)}")


def _dataset_rows(records, graph) -> list[dict[str, Any]]:
    return [
        _row("enterprise_health_finance", "dataset", "records", len(records)),
        _row("enterprise_health_finance", "dataset", "users", len({r.user_id for r in records})),
        _row("enterprise_health_finance", "dataset", "sessions", len({r.session_id for r in records})),
        _row("enterprise_health_finance", "dataset", "nodes", len(graph.nodes)),
        _row("enterprise_health_finance", "dataset", "edges", len(graph.edges)),
    ]


def _backend_rows(graph) -> list[dict[str, Any]]:
    path = os.path.join(OUTPUT_DIR, "enterprise_property_graph.sqlite")
    adapter = SQLitePropertyGraphAdapter(path)
    adapter.write_graph(graph)
    loaded = adapter.read_graph()
    summary = adapter.summary()
    probe = CrossSessionProbe(loaded).run(
        attacker_session_id="ehf-user-001-session-1",
        victim_session_id="ehf-user-000-session-1",
        probe_queries=("arrhythmia", "CloudVendor", "Project-A", "Sydney"),
        max_hops=1,
    )
    return [
        _row("sqlite_property_graph", "backend", "nodes", summary["nodes"]),
        _row("sqlite_property_graph", "backend", "edges", summary["edges"]),
        _row("sqlite_property_graph", "backend", "sessions", summary["sessions"]),
        _row("sqlite_property_graph", "cross_session_probe", "leaked_edges", probe.leaked_edge_count),
    ]


def _kuzu_backend_rows(graph) -> list[dict[str, Any]]:
    if not KuzuPropertyGraphAdapter.available():
        return [
            _row("kuzu_property_graph", "backend", "available", False),
            _row("kuzu_property_graph", "backend", "status", "kuzu package unavailable"),
        ]
    path = os.path.join(OUTPUT_DIR, "enterprise_kuzu_graph")
    adapter = KuzuPropertyGraphAdapter(path)
    write_start = time.perf_counter()
    adapter.write_graph(graph)
    write_seconds = time.perf_counter() - write_start
    read_start = time.perf_counter()
    loaded = adapter.read_graph()
    read_seconds = time.perf_counter() - read_start
    summary = adapter.summary()
    latency_rows = _latency_rows(loaded)
    probe = CrossSessionProbe(loaded).run(
        attacker_session_id="ehf-user-001-session-1",
        victim_session_id="ehf-user-000-session-1",
        probe_queries=("arrhythmia", "CloudVendor", "Project-A", "Sydney"),
        max_hops=1,
    )
    return [
        _row("kuzu_property_graph", "backend", "available", True),
        _row("kuzu_property_graph", "backend", "nodes", summary["nodes"]),
        _row("kuzu_property_graph", "backend", "edges", summary["edges"]),
        _row("kuzu_property_graph", "backend", "write_seconds", round(write_seconds, 4)),
        _row("kuzu_property_graph", "backend", "read_seconds", round(read_seconds, 4)),
        _row("kuzu_property_graph", "cross_session_probe", "leaked_edges", probe.leaked_edge_count),
    ] + latency_rows


def _latency_rows(graph) -> list[dict[str, Any]]:
    queries = ("arrhythmia", "CloudVendor", "Project-A", "Sydney", "hotel") * 20
    strict_guard = GraphMemGuard(GraphMemGuardPolicy())
    bounded_guard = GraphMemGuard(
        GraphMemGuardPolicy(
            allow_cross_session=True,
            max_cross_session_edges_per_pair=5,
            blocked_sensitivity_labels=frozenset({"medical", "financial", "secret"}),
        )
    )

    baseline = _mean_retrieval_ms(graph, queries, None)
    strict = _mean_retrieval_ms(graph, queries, strict_guard)
    bounded = _mean_retrieval_ms(graph, queries, bounded_guard)
    return [
        _row("kuzu_property_graph", "latency", "queries", len(queries)),
        _row("kuzu_property_graph", "latency", "baseline_ms", round(baseline, 4)),
        _row("kuzu_property_graph", "latency", "strict_guard_ms", round(strict, 4)),
        _row("kuzu_property_graph", "latency", "bounded_guard_ms", round(bounded, 4)),
        _row("kuzu_property_graph", "latency", "strict_overhead_pct", round(_overhead(strict, baseline), 4)),
        _row("kuzu_property_graph", "latency", "bounded_overhead_pct", round(_overhead(bounded, baseline), 4)),
    ]


def _mean_retrieval_ms(graph, queries, guard) -> float:
    start = time.perf_counter()
    for query in queries:
        graph.retrieve(query, "ehf-user-001-session-1", max_hops=1, guard=guard)
    elapsed = time.perf_counter() - start
    return 1000.0 * elapsed / len(queries)


def _overhead(value: float, baseline: float) -> float:
    return 100.0 * (value - baseline) / baseline if baseline else 0.0


def _bounded_sharing_rows(graph) -> list[dict[str, Any]]:
    probe = CrossSessionProbe(graph)
    evaluator = UtilityEvaluator(graph)
    rows: list[dict[str, Any]] = []
    queries = ("arrhythmia", "CloudVendor", "Project-A", "Sydney")
    for budget in (0, 1, 2, 5, 10):
        guard = GraphMemGuard(
            GraphMemGuardPolicy(
                allow_cross_session=True,
                max_cross_session_edges_per_pair=budget,
                blocked_sensitivity_labels=frozenset({"medical", "financial", "secret"}),
            )
        )
        report = probe.run(
            attacker_session_id="ehf-user-001-session-1",
            victim_session_id="ehf-user-000-session-1",
            probe_queries=queries,
            max_hops=1,
            guard=guard,
        )
        utility = evaluator.evaluate(
            query="Sydney Hotel CloudVendor",
            requester_session_id="ehf-user-001-session-1",
            guard=guard,
            max_hops=1,
        )
        rows.extend(
            [
                _row(f"budget_{budget}", "bounded_sharing", "leaked_edges", report.leaked_edge_count),
                _row(f"budget_{budget}", "bounded_sharing", "leakage_events", report.leakage_event_count),
                _row(f"budget_{budget}", "bounded_sharing", "utility_retention", round(utility.utility_retention_rate, 4)),
            ]
        )
    return rows


def _multihop_rows(graph) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    probe = CrossSessionProbe(graph)
    queries = ("arrhythmia", "CloudVendor", "Project-A", "Sydney")
    for hops in (1, 2, 3):
        baseline = probe.run(
            attacker_session_id="ehf-user-001-session-1",
            victim_session_id="ehf-user-000-session-1",
            probe_queries=queries,
            max_hops=hops,
        )
        guard = GraphMemGuard(
            GraphMemGuardPolicy(
                allow_cross_session=True,
                max_cross_session_edges_per_pair=5,
                blocked_sensitivity_labels=frozenset({"medical", "financial", "secret"}),
            )
        )
        bounded = probe.run(
            attacker_session_id="ehf-user-001-session-1",
            victim_session_id="ehf-user-000-session-1",
            probe_queries=queries,
            max_hops=hops,
            guard=guard,
        )
        rows.extend(
            [
                _row(f"hop_{hops}", "multihop_probe", "baseline_leaked_edges", baseline.leaked_edge_count),
                _row(f"hop_{hops}", "multihop_probe", "baseline_retrieved_edges", baseline.unique_retrieved_edge_count),
                _row(f"hop_{hops}", "multihop_probe", "bounded_b5_leaked_edges", bounded.leaked_edge_count),
                _row(f"hop_{hops}", "multihop_probe", "bounded_b5_retrieved_edges", bounded.unique_retrieved_edge_count),
            ]
        )
    return rows


def _hybrid_pipeline_rows(graph) -> list[dict[str, Any]]:
    """Evaluate backend -> adaptive retrieval -> guard -> response scoring."""

    path = os.path.join(OUTPUT_DIR, "hybrid_pipeline.sqlite")
    adapter = SQLitePropertyGraphAdapter(path)
    adapter.write_graph(graph)
    backend_graph = adapter.read_graph()
    scorer = ResponseLeakageScorer()
    generator = LocalAbstractiveResponseGenerator()
    victim_session = "ehf-user-000-session-1"
    victim_edges = backend_graph.edges_by_session(victim_session)
    secret_terms = tuple(
        sorted(
            {
                token
                for edge in victim_edges
                if edge.sensitivity != "normal"
                for token in edge.target_id.replace("-", " ").split()
                if len(token) >= 4
            }
        )
    )
    rows: list[dict[str, Any]] = []
    for condition, guard in (
        ("baseline", None),
        ("strict_guard", GraphMemGuard(GraphMemGuardPolicy())),
        (
            "bounded_b5",
            GraphMemGuard(
                GraphMemGuardPolicy(
                    allow_cross_session=True,
                    max_cross_session_edges_per_pair=5,
                    blocked_sensitivity_labels=frozenset({"medical", "financial", "secret"}),
                )
            ),
        ),
    ):
        start = time.perf_counter()
        probe_report = CrossSessionProbe(backend_graph).run_adaptive(
            attacker_session_id="ehf-user-001-session-1",
            victim_session_id=victim_session,
            seed_queries=("arrhythmia", "CloudVendor"),
            query_budget=6,
            max_hops=2,
            guard=guard,
        )
        response_text = "\n".join(generator.generate(result) for result in probe_report.results)
        response_report = scorer.score(
            response_text=response_text,
            victim_edges=victim_edges,
            secret_terms=secret_terms,
        )
        elapsed_ms = 1000.0 * (time.perf_counter() - start)
        rows.extend(
            [
                _row(condition, "hybrid_pipeline", "query_count", probe_report.query_count),
                _row(condition, "hybrid_pipeline", "retrieval_leaked_edges", probe_report.leaked_edge_count),
                _row(condition, "hybrid_pipeline", "response_leaked_edges", response_report.leaked_edge_count),
                _row(condition, "hybrid_pipeline", "response_leaked_terms", response_report.leaked_secret_term_count),
                _row(condition, "hybrid_pipeline", "pipeline_ms", round(elapsed_ms, 4)),
            ]
        )
    return rows


def _provenance_error_rows(graph) -> list[dict[str, Any]]:
    """Stress-test guard behavior when sensitivity provenance is wrong."""

    rows: list[dict[str, Any]] = []
    victim_session = "ehf-user-000-session-1"
    attacker_session = "ehf-user-001-session-1"
    queries = ("arrhythmia", "CloudVendor", "Project-A", "Sydney")
    guard_policy = GraphMemGuardPolicy(
        allow_cross_session=True,
        max_cross_session_edges_per_pair=5,
        blocked_sensitivity_labels=frozenset({"medical", "financial", "secret"}),
    )
    for error_rate in (0.0, 0.1, 0.25, 0.5):
        corrupted, corrupted_edges = _graph_with_sensitivity_provenance_errors(
            graph,
            victim_session_id=victim_session,
            error_rate=error_rate,
            seed=2026,
        )
        report = CrossSessionProbe(corrupted).run(
            attacker_session_id=attacker_session,
            victim_session_id=victim_session,
            probe_queries=queries,
            max_hops=2,
            guard=GraphMemGuard(guard_policy),
        )
        response_text = "\n".join(
            EvidenceDumpResponseGenerator().generate(result)
            for result in report.results
        )
        response_report = ResponseLeakageScorer().score(
            response_text=response_text,
            victim_edges=corrupted.edges_by_session(victim_session),
            secret_terms=_secret_terms(corrupted, victim_session),
        )
        condition = f"sensitivity_error_{error_rate:.2f}"
        rows.extend(
            [
                _row(condition, "provenance_error_robustness", "corrupted_sensitive_edges", corrupted_edges),
                _row(condition, "provenance_error_robustness", "retrieval_leaked_edges", report.leaked_edge_count),
                _row(condition, "provenance_error_robustness", "response_leaked_edges", response_report.leaked_edge_count),
                _row(condition, "provenance_error_robustness", "response_leaked_terms", response_report.leaked_secret_term_count),
            ]
        )
    return rows


def _strong_generator_rows(graph) -> list[dict[str, Any]]:
    """Compare benign generators with an evidence-dump adversarial generator."""

    rows: list[dict[str, Any]] = []
    scorer = ResponseLeakageScorer()
    victim_session = "ehf-user-000-session-1"
    victim_edges = graph.edges_by_session(victim_session)
    secret_terms = _secret_terms(graph, victim_session)
    generators = (
        ("template", TemplateResponseGenerator()),
        ("local_abstractive", LocalAbstractiveResponseGenerator()),
        ("evidence_dump", EvidenceDumpResponseGenerator()),
    )
    for condition, guard in (
        ("baseline", None),
        (
            "bounded_b5",
            GraphMemGuard(
                GraphMemGuardPolicy(
                    allow_cross_session=True,
                    max_cross_session_edges_per_pair=5,
                    blocked_sensitivity_labels=frozenset({"medical", "financial", "secret"}),
                )
            ),
        ),
    ):
        report = CrossSessionProbe(graph).run_adaptive(
            attacker_session_id="ehf-user-001-session-1",
            victim_session_id=victim_session,
            seed_queries=("arrhythmia", "CloudVendor"),
            query_budget=8,
            max_hops=2,
            guard=guard,
        )
        for generator_name, generator in generators:
            response = "\n".join(generator.generate(result) for result in report.results)
            response_report = scorer.score(
                response_text=response,
                victim_edges=victim_edges,
                secret_terms=secret_terms,
            )
            row_condition = f"{condition}_{generator_name}"
            rows.extend(
                [
                    _row(row_condition, "strong_generator", "adaptive_queries", report.query_count),
                    _row(row_condition, "strong_generator", "retrieval_leaked_edges", report.leaked_edge_count),
                    _row(row_condition, "strong_generator", "response_leaked_edges", response_report.leaked_edge_count),
                    _row(row_condition, "strong_generator", "response_leaked_terms", response_report.leaked_secret_term_count),
                ]
            )
    return rows


def _utility_quality_rows(graph) -> list[dict[str, Any]]:
    """Measure utility with relevance precision/recall/F1, not just retention."""

    rows: list[dict[str, Any]] = []
    guard = GraphMemGuard(
        GraphMemGuardPolicy(
            allow_cross_session=True,
            max_cross_session_edges_per_pair=5,
            blocked_sensitivity_labels=frozenset({"medical", "financial", "secret"}),
        )
    )
    queries = (
        "Sydney Hotel CloudVendor",
        "diabetes clinic appointment",
        "payrollbank vendor",
        "Project-A vendor",
    )
    for query in queries:
        baseline = graph.retrieve(query, "ehf-user-001-session-1", max_hops=2)
        defended = graph.retrieve(query, "ehf-user-001-session-1", max_hops=2, guard=guard)
        report = _utility_quality_report(baseline, defended)
        condition = query.replace(" ", "_").lower()
        rows.extend(
            [
                _row(condition, "utility_quality", "baseline_relevant_edges", report["baseline_relevant_edges"]),
                _row(condition, "utility_quality", "defended_relevant_edges", report["defended_relevant_edges"]),
                _row(condition, "utility_quality", "precision", report["precision"]),
                _row(condition, "utility_quality", "recall", report["recall"]),
                _row(condition, "utility_quality", "f1", report["f1"]),
            ]
        )
    return rows


def _multiseed_bounded_sharing_rows() -> list[dict[str, Any]]:
    rows = []
    for budget in (0, 1, 2, 5, 10):
        leak_values: list[float] = []
        utility_values: list[float] = []
        for seed in range(10):
            records = build_enterprise_health_finance_records(seed=2026 + seed)
            graph = dialogue_records_to_graph(records)
            probe = CrossSessionProbe(graph)
            evaluator = UtilityEvaluator(graph)
            guard = GraphMemGuard(
                GraphMemGuardPolicy(
                    allow_cross_session=True,
                    max_cross_session_edges_per_pair=budget,
                    blocked_sensitivity_labels=frozenset({"medical", "financial", "secret"}),
                )
            )
            report = probe.run(
                attacker_session_id="ehf-user-001-session-1",
                victim_session_id="ehf-user-000-session-1",
                probe_queries=("arrhythmia", "CloudVendor", "Project-A", "Sydney"),
                max_hops=1,
                guard=guard,
            )
            utility = evaluator.evaluate(
                query="Sydney Hotel CloudVendor",
                requester_session_id="ehf-user-001-session-1",
                guard=guard,
                max_hops=1,
            )
            leak_values.append(float(report.leaked_edge_count))
            utility_values.append(float(utility.utility_retention_rate))
        leak_ci = ci95(leak_values)
        utility_ci = ci95(utility_values)
        rows.extend(
            [
                _row(f"budget_{budget}", "bounded_sharing_multiseed", "leaked_edges_mean", round(leak_ci.mean, 4)),
                _row(f"budget_{budget}", "bounded_sharing_multiseed", "leaked_edges_ci95_low", round(leak_ci.ci95_low, 4)),
                _row(f"budget_{budget}", "bounded_sharing_multiseed", "leaked_edges_ci95_high", round(leak_ci.ci95_high, 4)),
                _row(f"budget_{budget}", "bounded_sharing_multiseed", "utility_mean", round(utility_ci.mean, 4)),
                _row(f"budget_{budget}", "bounded_sharing_multiseed", "utility_ci95_low", round(utility_ci.ci95_low, 4)),
                _row(f"budget_{budget}", "bounded_sharing_multiseed", "utility_ci95_high", round(utility_ci.ci95_high, 4)),
            ]
        )
    return rows


def _adaptive_probe_rows(graph) -> list[dict[str, Any]]:
    probe = CrossSessionProbe(graph)
    fixed = probe.run(
        attacker_session_id="ehf-user-001-session-1",
        victim_session_id="ehf-user-000-session-1",
        probe_queries=("arrhythmia", "CloudVendor", "Project-A", "Sydney", "clinic", "hotel"),
        max_hops=1,
    )
    adaptive = probe.run_adaptive(
        attacker_session_id="ehf-user-001-session-1",
        victim_session_id="ehf-user-000-session-1",
        seed_queries=("arrhythmia", "CloudVendor"),
        query_budget=6,
        max_hops=1,
    )
    return [
        _row("fixed_budget_6", "adaptive_probe", "leaked_edges", fixed.leaked_edge_count),
        _row("fixed_budget_6", "adaptive_probe", "query_count", fixed.query_count),
        _row("adaptive_budget_6", "adaptive_probe", "leaked_edges", adaptive.leaked_edge_count),
        _row("adaptive_budget_6", "adaptive_probe", "query_count", adaptive.query_count),
    ]


def _blackbox_rows(graph) -> list[dict[str, Any]]:
    scorer = ResponseLeakageScorer()
    victim_session = "ehf-user-000-session-1"
    victim_edges = graph.edges_by_session(victim_session)
    secret_terms = tuple(
        sorted(
            {
                token
                for edge in victim_edges
                if edge.sensitivity != "normal"
                for token in edge.target_id.replace("-", " ").split()
                if len(token) >= 4
            }
        )
    )
    rows = []
    generators = (
        ("template", TemplateResponseGenerator()),
        ("local_abstractive", LocalAbstractiveResponseGenerator()),
    )
    for condition, guard in (
        ("baseline", None),
        ("bounded_b0", GraphMemGuard(GraphMemGuardPolicy(allow_cross_session=True, max_cross_session_edges_per_pair=0))),
        (
            "bounded_b5",
            GraphMemGuard(
                GraphMemGuardPolicy(
                    allow_cross_session=True,
                    max_cross_session_edges_per_pair=5,
                    blocked_sensitivity_labels=frozenset({"medical", "financial", "secret"}),
                )
            ),
        ),
    ):
        result = graph.retrieve(
            "arrhythmia clinic",
            "ehf-user-001-session-1",
            max_hops=1,
            guard=guard,
        )
        for generator_name, generator in generators:
            response = generator.generate(result)
            report = scorer.score(
                response_text=response,
                victim_edges=victim_edges,
                secret_terms=secret_terms,
            )
            row_condition = f"{condition}_{generator_name}"
            rows.extend(
                [
                    _row(row_condition, "blackbox_response", "response_chars", len(response)),
                    _row(row_condition, "blackbox_response", "leaked_edges", report.leaked_edge_count),
                    _row(row_condition, "blackbox_response", "leaked_secret_terms", report.leaked_secret_term_count),
                ]
            )
    rows.extend(_optional_openai_rows(graph, victim_edges, secret_terms, scorer))
    return rows


def _semantic_response_rows(graph) -> list[dict[str, Any]]:
    lexical_scorer = ResponseLeakageScorer()
    semantic_scorer = SemanticResponseLeakageScorer()
    victim_session = "ehf-user-000-session-1"
    victim_edges = graph.edges_by_session(victim_session)
    secret_terms = _secret_terms(graph, victim_session)
    rows: list[dict[str, Any]] = []
    for condition, guard in (
        ("baseline", None),
        (
            "bounded_b5",
            GraphMemGuard(
                GraphMemGuardPolicy(
                    allow_cross_session=True,
                    max_cross_session_edges_per_pair=5,
                    blocked_sensitivity_labels=frozenset({"medical", "financial", "secret"}),
                )
            ),
        ),
    ):
        result = graph.retrieve(
            "arrhythmia clinic confidential settlement payroll",
            "ehf-user-001-session-1",
            max_hops=2,
            guard=guard,
        )
        response = EvidenceDumpResponseGenerator().generate(result)
        lexical = lexical_scorer.score(
            response_text=response,
            victim_edges=victim_edges,
            secret_terms=secret_terms,
        )
        semantic = semantic_scorer.score(
            response_text=response,
            victim_edges=victim_edges,
            secret_terms=secret_terms,
        )
        rows.extend(
            [
                _row(condition, "semantic_response_leakage", "lexical_edges", lexical.leaked_edge_count),
                _row(condition, "semantic_response_leakage", "semantic_edges", semantic.semantic_edge_count),
                _row(condition, "semantic_response_leakage", "lexical_terms", lexical.leaked_secret_term_count),
                _row(condition, "semantic_response_leakage", "semantic_terms", semantic.semantic_secret_term_count),
            ]
        )
    return rows


def _optional_openai_rows(graph, victim_edges, secret_terms, scorer) -> list[dict[str, Any]]:
    if not os.environ.get("OPENAI_API_KEY"):
        return [_row("openai", "blackbox_response", "status", "skipped_missing_openai_api_key")]
    try:
        result = graph.retrieve("arrhythmia clinic", "ehf-user-001-session-1", max_hops=1)
        response = OpenAIChatResponseGenerator().generate(result)
        report = scorer.score(
            response_text=response,
            victim_edges=victim_edges,
            secret_terms=secret_terms,
        )
    except Exception as exc:
        return [_row("openai", "blackbox_response", "status", f"skipped_{type(exc).__name__}")]
    return [
        _row("baseline_openai", "blackbox_response", "response_chars", len(response)),
        _row("baseline_openai", "blackbox_response", "leaked_edges", report.leaked_edge_count),
        _row("baseline_openai", "blackbox_response", "leaked_secret_terms", report.leaked_secret_term_count),
    ]


def _session_link_rows(graph) -> list[dict[str, Any]]:
    linker = SessionGraphLink(graph)
    all_sessions = sorted({edge.owner_session_id for edge in graph.edges})
    users = sorted({edge.source_user_id for edge in graph.edges if edge.source_user_id})
    rows = []
    for method in ("cosine", "wl_kernel", "graph_edit", "embedding"):
        evaluated = 0
        top1 = 0
        top3 = 0
        rr_total = 0.0
        for user in users[:24]:
            sessions = sorted(session for session in all_sessions if session.startswith(user))
            if len(sessions) < 2:
                continue
            expected_sessions = set(sessions[1:])
            report = linker.rank(
                query_session_id=sessions[0],
                candidate_session_ids=all_sessions,
                include_semantic_labels=(method == "embedding"),
                method=method,
            )
            ranked = tuple(candidate.session_id for candidate in report.candidates)
            first_hit_rank = next(
                (index + 1 for index, session in enumerate(ranked) if session in expected_sessions),
                0,
            )
            evaluated += 1
            top1 += int(any(session in expected_sessions for session in ranked[:1]))
            top3 += int(any(session in expected_sessions for session in ranked[:3]))
            rr_total += 1.0 / first_hit_rank if first_hit_rank else 0.0
        rows.extend(
            [
                _row(method, "session_link", "evaluated_users", evaluated),
                _row(method, "session_link", "top1_accuracy", round(top1 / evaluated, 4) if evaluated else 0.0),
                _row(method, "session_link", "top3_accuracy", round(top3 / evaluated, 4) if evaluated else 0.0),
                _row(method, "session_link", "mrr", round(rr_total / evaluated, 4) if evaluated else 0.0),
            ]
        )
    return rows


def _temporal_hidden_rows(graph) -> list[dict[str, Any]]:
    infer = TemporalPathInfer(graph)
    rows = []
    for query in ("arrhythmia", "CloudVendor", "Project-A", "Sydney"):
        timestamp_report = infer.infer(
            query=query,
            requester_session_id="ehf-user-001-session-1",
            max_hops=1,
        )
        hidden_report = infer.infer_without_timestamps(
            query=query,
            requester_session_id="ehf-user-001-session-1",
            max_hops=1,
        )
        expected = timestamp_report.inferred_edge_ids
        rows.append(
            _row(
                query,
                "temporal_hidden",
                "pairwise_ordering_accuracy",
                round(pairwise_ordering_accuracy(hidden_report.inferred_edge_ids, expected), 4),
            )
        )
    return rows


def _fixed_universe_dp_rows(graph) -> list[dict[str, Any]]:
    present_candidates = tuple(edge for edge in graph.edges if edge.sensitivity != "normal")[:120]
    absent_candidates = tuple(
        MemoryEdge(
            edge_id=f"absent-candidate-{index}",
            source_id=edge.source_id,
            relation=edge.relation,
            target_id=f"absent-{edge.target_id}",
            owner_session_id=edge.owner_session_id,
            source_user_id=edge.source_user_id,
            turn_id=edge.turn_id,
            sensitivity=edge.sensitivity,
            created_at=edge.created_at,
        )
        for index, edge in enumerate(present_candidates[:40])
    )
    candidate_edges = present_candidates + absent_candidates
    rows = []
    for epsilon in (0.5, 1.0, 2.0):
        mechanism = FixedUniverseRandomizedResponseAdmission(
            EdgeAdmissionPolicy(epsilon=epsilon, seed=123),
            candidate_edges=candidate_edges,
        )
        released = mechanism.filter_graph(graph)
        synthetic_edges = sum(1 for edge in released.edges if edge.metadata.get("dp_synthetic"))
        rows.extend(
            [
                _row(f"epsilon_{epsilon}", "fixed_universe_dp", "candidate_edges", len(candidate_edges)),
                _row(f"epsilon_{epsilon}", "fixed_universe_dp", "released_edges", len(released.edges)),
                _row(f"epsilon_{epsilon}", "fixed_universe_dp", "synthetic_absent_edges", synthetic_edges),
                _row(f"epsilon_{epsilon}", "fixed_universe_dp", "per_edge_epsilon", epsilon),
            ]
        )
    return rows


def _privacy_accounting_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for epsilon in (0.5, 1.0, 2.0):
        present_probability, absent_probability = randomized_response_probabilities(epsilon)
        privacy_loss = randomized_response_privacy_loss(epsilon)
        rows.extend(
            [
                _row(f"epsilon_{epsilon}", "privacy_accounting", "present_emit_probability", round(present_probability, 6)),
                _row(f"epsilon_{epsilon}", "privacy_accounting", "absent_emit_probability", round(absent_probability, 6)),
                _row(f"epsilon_{epsilon}", "privacy_accounting", "single_release_privacy_loss", round(privacy_loss, 6)),
            ]
        )
        for releases in (1, 5, 10):
            report = CompositionReport(per_release_epsilon=epsilon, release_count=releases)
            rows.append(
                _row(
                    f"epsilon_{epsilon}_releases_{releases}",
                    "privacy_accounting",
                    "basic_composed_epsilon",
                    round(report.composed_epsilon, 6),
                )
            )
    return rows


def _full_graph_privacy_rows(graph) -> list[dict[str, Any]]:
    protected_candidates = sum(1 for edge in graph.edges if edge.sensitivity != "normal")
    unprotected_edges = sum(1 for edge in graph.edges if edge.sensitivity == "normal")
    rows: list[dict[str, Any]] = []
    for epsilon in (0.5, 1.0):
        for releases in (1, 5):
            scoped = FullGraphReleasePrivacyReport(
                per_edge_epsilon=epsilon,
                protected_candidate_edges=protected_candidates,
                unprotected_released_edges=unprotected_edges,
                release_count=releases,
            )
            full = FullGraphReleasePrivacyReport(
                per_edge_epsilon=epsilon,
                protected_candidate_edges=len(graph.edges),
                unprotected_released_edges=0,
                release_count=releases,
            )
            rows.extend(
                [
                    _row(f"scoped_epsilon_{epsilon}_releases_{releases}", "full_graph_privacy", "guarantee_scope", scoped.guarantee_scope),
                    _row(f"scoped_epsilon_{epsilon}_releases_{releases}", "full_graph_privacy", "has_full_graph_dp", scoped.has_full_graph_dp),
                    _row(f"scoped_epsilon_{epsilon}_releases_{releases}", "full_graph_privacy", "protected_release_epsilon", round(scoped.protected_release_epsilon, 4)),
                    _row(f"full_epsilon_{epsilon}_releases_{releases}", "full_graph_privacy", "guarantee_scope", full.guarantee_scope),
                    _row(f"full_epsilon_{epsilon}_releases_{releases}", "full_graph_privacy", "has_full_graph_dp", full.has_full_graph_dp),
                    _row(f"full_epsilon_{epsilon}_releases_{releases}", "full_graph_privacy", "protected_release_epsilon", round(full.protected_release_epsilon, 4)),
                ]
            )
    return rows


def _graph_with_sensitivity_provenance_errors(
    graph,
    *,
    victim_session_id: str,
    error_rate: float,
    seed: int,
) -> tuple[DynamicMemoryGraph, int]:
    rng = random.Random(seed)
    sensitive_victim_edges = [
        edge
        for edge in graph.edges
        if edge.owner_session_id == victim_session_id and edge.sensitivity != "normal"
    ]
    corrupt_count = ceil(len(sensitive_victim_edges) * error_rate) if error_rate else 0
    corrupt_ids = {
        edge.edge_id
        for edge in rng.sample(sensitive_victim_edges, min(corrupt_count, len(sensitive_victim_edges)))
    }
    corrupted = DynamicMemoryGraph()
    for node in graph.nodes:
        corrupted.add_node(node)
    for edge in graph.edges:
        if edge.edge_id in corrupt_ids:
            metadata = dict(edge.metadata)
            metadata["provenance_error"] = "sensitivity_downgraded"
            edge = MemoryEdge(
                edge_id=edge.edge_id,
                source_id=edge.source_id,
                relation=edge.relation,
                target_id=edge.target_id,
                owner_session_id=edge.owner_session_id,
                source_user_id=edge.source_user_id,
                turn_id=edge.turn_id,
                sensitivity="normal",
                created_at=edge.created_at,
                metadata=metadata,
            )
        corrupted.add_edge(edge)
    return corrupted, len(corrupt_ids)


def _secret_terms(graph, victim_session: str) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                token
                for edge in graph.edges_by_session(victim_session)
                if edge.sensitivity != "normal"
                for token in edge.target_id.replace("-", " ").split()
                if len(token) >= 4
            }
        )
    )


def _utility_quality_report(baseline, defended) -> dict[str, Any]:
    baseline_relevant = {
        edge.edge_id for edge in baseline.edges if edge.sensitivity == "normal"
    }
    defended_relevant = {
        edge.edge_id for edge in defended.edges if edge.sensitivity == "normal"
    }
    true_positive = len(baseline_relevant & defended_relevant)
    precision = true_positive / len(defended_relevant) if defended_relevant else 1.0
    recall = true_positive / len(baseline_relevant) if baseline_relevant else 1.0
    f1 = 2.0 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "baseline_relevant_edges": len(baseline_relevant),
        "defended_relevant_edges": len(defended_relevant),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
    }


def _row(condition: str, experiment: str, metric: str, value: Any) -> dict[str, Any]:
    return {
        "system": "graphmemshield",
        "dataset": "enterprise_health_finance",
        "experiment": experiment,
        "condition": condition,
        "metric": metric,
        "value": value,
    }


def _write_json(rows: list[dict[str, Any]], filename: str) -> None:
    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as handle:
        json.dump(rows, handle, indent=2)


def _write_csv(rows: list[dict[str, Any]], filename: str) -> None:
    with open(os.path.join(OUTPUT_DIR, filename), "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["system", "dataset", "experiment", "condition", "metric", "value"])
        writer.writeheader()
        writer.writerows(rows)


def _write_markdown(rows: list[dict[str, Any]], filename: str) -> None:
    lines = [
        "# TIFS Revision Experiments",
        "",
        "| System | Dataset | Experiment | Condition | Metric | Value |",
        "|---|---|---|---|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['system']} | {row['dataset']} | {row['experiment']} | "
            f"{row['condition']} | {row['metric']} | {row['value']} |"
        )
    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
