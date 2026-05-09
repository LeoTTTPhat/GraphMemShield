from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from graphmemshield import (
    CrossSessionProbe,
    EdgeAdmissionPolicy,
    GraphMemGuard,
    GraphMemGuardPolicy,
    RandomizedEdgeAdmission,
    SessionGraphLink,
    TemporalPathInfer,
    build_synthetic_multisession_graph,
)
from graphmemshield.evaluation.metrics import (
    leakage_reduction,
    ordering_accuracy,
    top_k_hit,
)


@dataclass(frozen=True)
class ExperimentRecord:
    experiment: str
    condition: str
    metric: str
    value: float | int | str | bool
    notes: str = ""


def run_synthetic_experiments() -> list[ExperimentRecord]:
    """Run all experiments that do not require external datasets or calls."""

    records: list[ExperimentRecord] = []
    records.extend(_run_cross_session_probe_experiment())
    records.extend(_run_session_link_experiment())
    records.extend(_run_temporal_path_experiment())
    records.extend(_run_budget_curve_experiment())
    records.extend(_run_edge_admission_experiment())
    return records


def write_experiment_outputs(
    records: list[ExperimentRecord], output_dir: str | Path
) -> dict[str, str]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "synthetic_experiments.json"
    csv_path = output_path / "synthetic_experiments.csv"
    md_path = output_path / "synthetic_experiments.md"

    payload = [asdict(record) for record in records]
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=["experiment", "condition", "metric", "value", "notes"],
        )
        writer.writeheader()
        writer.writerows(payload)

    md_path.write_text(render_markdown_report(records), encoding="utf-8")
    return {
        "json": str(json_path),
        "csv": str(csv_path),
        "markdown": str(md_path),
    }


def render_markdown_report(records: list[ExperimentRecord]) -> str:
    lines = [
        "# GraphMemShield Synthetic Experiment Report",
        "",
        "This report covers experiments that run without external datasets, APIs,",
        "GPU resources, or production graph-memory systems.",
        "",
        "| Experiment | Condition | Metric | Value | Notes |",
        "|---|---|---:|---:|---|",
    ]
    for record in records:
        lines.append(
            "| "
            f"{record.experiment} | {record.condition} | {record.metric} | "
            f"{record.value} | {record.notes} |"
        )
    lines.extend(
        [
            "",
            "## Manual Follow-up Required",
            "",
            "- Replace the synthetic graph with PersonaChat, MultiWOZ, Enron, and controlled health/finance dialogue ingestion.",
            "- Connect retrieval to Neo4j or another property-graph backend-backed graph memory.",
            "- Add response-level scoring for black-box CrossSessionProbe.",
            "- Replace heuristic SessionGraphLink with WL-kernel or graph edit distance baselines.",
            "- Replace timestamp sorting in TemporalPathInfer with beam-search path likelihood when retrieved contexts are noisy.",
            "- Replace seeded edge-admission proxy with a formal DP mechanism after adjacency granularity is finalized.",
            "- Add privacy accounting and repeated-composition analysis for write-time defenses.",
        ]
    )
    return "\n".join(lines) + "\n"


def _run_cross_session_probe_experiment() -> list[ExperimentRecord]:
    graph = build_synthetic_multisession_graph()
    probe = CrossSessionProbe(graph)
    queries = ["clinic", "arrhythmia", "diagnosed"]

    baseline = probe.run(
        attacker_session_id="attacker-session",
        victim_session_id="alice-session-1",
        probe_queries=queries,
        max_hops=1,
    )
    strict = probe.run(
        attacker_session_id="attacker-session",
        victim_session_id="alice-session-1",
        probe_queries=queries,
        max_hops=1,
        guard=GraphMemGuard(GraphMemGuardPolicy()),
    )

    return [
        _record("cross_session_probe", "baseline", "leaked_edge_count", baseline.leaked_edge_count),
        _record(
            "cross_session_probe",
            "baseline",
            "unique_leaked_edge_count",
            baseline.unique_leaked_edge_count,
        ),
        _record(
            "cross_session_probe",
            "baseline",
            "leakage_event_count",
            baseline.leakage_event_count,
        ),
        _record("cross_session_probe", "baseline", "leakage_rate", round(baseline.leakage_rate, 4)),
        _record(
            "cross_session_probe",
            "baseline",
            "event_leakage_rate",
            round(baseline.event_leakage_rate, 4),
        ),
        _record(
            "cross_session_probe",
            "baseline",
            "per_query_leak_rate",
            round(baseline.per_query_leak_rate, 4),
        ),
        _record("cross_session_probe", "strict_guard", "leaked_edge_count", strict.leaked_edge_count),
        _record(
            "cross_session_probe",
            "strict_guard",
            "leakage_event_count",
            strict.leakage_event_count,
        ),
        _record(
            "cross_session_probe",
            "strict_guard",
            "leakage_reduction",
            leakage_reduction(baseline.leaked_edge_count, strict.leaked_edge_count),
        ),
    ]


def _run_session_link_experiment() -> list[ExperimentRecord]:
    graph = build_synthetic_multisession_graph()
    report = SessionGraphLink(graph).rank(
        query_session_id="alice-session-1",
        candidate_session_ids=("alice-session-2", "bob-session-1"),
        include_semantic_labels=False,
    )
    ranked_ids = tuple(candidate.session_id for candidate in report.candidates)
    top_score = report.candidates[0].score if report.candidates else 0.0

    return [
        _record("session_graph_link", "structure_only", "top_1_hit", top_k_hit(ranked_ids, "alice-session-2", k=1)),
        _record("session_graph_link", "structure_only", "top_candidate", report.top_session_id or ""),
        _record("session_graph_link", "structure_only", "top_score", round(top_score, 4)),
    ]


def _run_temporal_path_experiment() -> list[ExperimentRecord]:
    graph = build_synthetic_multisession_graph()
    report = TemporalPathInfer(graph).infer(
        query="arrhythmia",
        requester_session_id="attacker-session",
        max_hops=1,
    )
    expected_prefix = ("alice-s1-e1", "alice-s1-e2")
    accuracy = ordering_accuracy(report.inferred_edge_ids[:2], expected_prefix)

    guarded = TemporalPathInfer(graph).infer(
        query="arrhythmia",
        requester_session_id="attacker-session",
        max_hops=1,
        guard=GraphMemGuard(GraphMemGuardPolicy()),
    )
    return [
        _record("temporal_path_infer", "baseline", "prefix_ordering_accuracy", accuracy),
        _record("temporal_path_infer", "baseline", "inferred_edge_count", len(report.inferred_edge_ids)),
        _record("temporal_path_infer", "strict_guard", "inferred_edge_count", len(guarded.inferred_edge_ids)),
    ]


def _run_budget_curve_experiment() -> list[ExperimentRecord]:
    graph = build_synthetic_multisession_graph()
    probe = CrossSessionProbe(graph)
    records: list[ExperimentRecord] = []

    for budget in (0, 1, 2):
        guard = GraphMemGuard(
            GraphMemGuardPolicy(
                allow_cross_session=True,
                max_cross_session_edges_per_pair=budget,
                blocked_sensitivity_labels=frozenset({"medical"}),
            )
        )
        report = probe.run(
            attacker_session_id="attacker-session",
            victim_session_id="bob-session-1",
            probe_queries=["gym", "visited"],
            max_hops=1,
            guard=guard,
        )
        records.append(
            _record(
                "budget_curve",
                f"budget_{budget}",
                "bob_session_leaked_edges",
                report.leaked_edge_count,
                notes="Medical edges remain blocked; normal cross-session edges follow budget.",
            )
        )

    return records


def _run_edge_admission_experiment() -> list[ExperimentRecord]:
    source_graph = build_synthetic_multisession_graph()
    records: list[ExperimentRecord] = []

    for epsilon in (0.1, 1.0, 3.0):
        admission = RandomizedEdgeAdmission(
            EdgeAdmissionPolicy(epsilon=epsilon, seed="synthetic-edge-admission")
        )
        admitted_graph = admission.filter_graph(source_graph)
        probe = CrossSessionProbe(admitted_graph)
        report = probe.run(
            attacker_session_id="attacker-session",
            victim_session_id="alice-session-1",
            probe_queries=["clinic", "arrhythmia", "diagnosed"],
            max_hops=1,
        )
        sensitive_edges = [
            edge
            for edge in admitted_graph.edges
            if edge.sensitivity in {"medical", "financial"}
        ]
        records.extend(
            [
                _record(
                    "edge_admission",
                    f"epsilon_{epsilon}",
                    "sensitive_keep_probability",
                    round(admission.policy.sensitive_keep_probability, 4),
                ),
                _record(
                    "edge_admission",
                    f"epsilon_{epsilon}",
                    "admitted_sensitive_edges",
                    len(sensitive_edges),
                    notes="Seeded proxy; not a complete DP accounting result.",
                ),
                _record(
                    "edge_admission",
                    f"epsilon_{epsilon}",
                    "victim_leaked_edges",
                    report.leaked_edge_count,
                    notes="Leakage after write-time edge admission.",
                ),
            ]
        )

    return records


def _record(
    experiment: str,
    condition: str,
    metric: str,
    value: float | int | str | bool,
    notes: str = "",
) -> ExperimentRecord:
    return ExperimentRecord(
        experiment=experiment,
        condition=condition,
        metric=metric,
        value=value,
        notes=notes,
    )
