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
    records.extend(_run_dataset_summary_experiment())
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
            "- Add graph edit distance and learned-embedding baselines for SessionGraphLink.",
            "- Replace timestamp sorting in TemporalPathInfer with beam-search path likelihood when retrieved contexts are noisy.",
            "- Replace one-sided edge suppression with a formal DP mechanism over a public candidate edge universe.",
            "- Add privacy accounting and repeated-composition analysis for any future write-time DP release mechanism.",
        ]
    )
    return "\n".join(lines) + "\n"


from graphmemshield.datasets.synthetic import build_large_synthetic_graph
from graphmemshield.evaluation.utility_evaluator import UtilityEvaluator
import statistics


def _run_dataset_summary_experiment() -> list[ExperimentRecord]:
    graph = build_large_synthetic_graph(num_users=20, sessions_per_user=3, seed=42)
    session_ids = {edge.owner_session_id for edge in graph.edges}
    user_ids = {edge.source_user_id for edge in graph.edges}
    return [
        _record("dataset_summary", "large_synthetic", "users", len(user_ids)),
        _record("dataset_summary", "large_synthetic", "sessions", len(session_ids)),
        _record("dataset_summary", "large_synthetic", "nodes", len(graph.nodes)),
        _record("dataset_summary", "large_synthetic", "edges", len(graph.edges)),
    ]


def _run_cross_session_probe_experiment() -> list[ExperimentRecord]:
    graph = build_large_synthetic_graph(num_users=20, sessions_per_user=3, seed=42)
    probe = CrossSessionProbe(graph)
    queries = ["arrhythmia", "laptop", "hotel"]

    baseline = probe.run(
        attacker_session_id="user_1_session_1",
        victim_session_id="session_0_0",
        probe_queries=queries,
        max_hops=1,
    )
    strict = probe.run(
        attacker_session_id="user_1_session_1",
        victim_session_id="session_0_0",
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
        _record("cross_session_probe", "strict_guard", "leaked_edge_count", strict.leaked_edge_count),
        _record(
            "cross_session_probe",
            "strict_guard",
            "leakage_reduction",
            leakage_reduction(baseline.leaked_edge_count, strict.leaked_edge_count),
        ),
    ]


def _run_session_link_experiment() -> list[ExperimentRecord]:
    graph = build_large_synthetic_graph(num_users=20, sessions_per_user=3, seed=42)
    report = SessionGraphLink(graph).rank(
        query_session_id="session_0_0",
        candidate_session_ids=[f"session_{u}_{s}" for u in range(20) for s in range(3)],
        include_semantic_labels=False,
    )
    ranked_ids = tuple(candidate.session_id for candidate in report.candidates)
    top_score = report.candidates[0].score if report.candidates else 0.0

    return [
        _record("session_graph_link", "structure_only", "top_1_hit", top_k_hit(ranked_ids, "session_0_1", k=1) or top_k_hit(ranked_ids, "session_0_2", k=1)),
        _record("session_graph_link", "structure_only", "top_score", round(top_score, 4)),
    ]


def _run_temporal_path_experiment() -> list[ExperimentRecord]:
    graph = build_large_synthetic_graph(num_users=20, sessions_per_user=3, seed=42)
    report = TemporalPathInfer(graph).infer(
        query="arrhythmia",
        requester_session_id="attacker-session",
        max_hops=1,
    )
    
    return [
        _record("temporal_path_infer", "baseline", "inferred_edge_count", len(report.inferred_edge_ids)),
    ]


def _run_budget_curve_experiment() -> list[ExperimentRecord]:
    graph = build_large_synthetic_graph(num_users=20, sessions_per_user=3, seed=42)
    probe = CrossSessionProbe(graph)
    evaluator = UtilityEvaluator(graph)
    records: list[ExperimentRecord] = []

    for budget in (0, 1, 2, 5):
        guard = GraphMemGuard(
            GraphMemGuardPolicy(
                allow_cross_session=True,
                max_cross_session_edges_per_pair=budget,
                blocked_sensitivity_labels=frozenset({"medical", "financial", "secret"}),
            )
        )
        report = probe.run(
            attacker_session_id="attacker",
            victim_session_id="session_0_0",
            probe_queries=["hotel", "laptop"],
            max_hops=1,
            guard=guard,
        )
        utility = evaluator.evaluate(
            query="hotel laptop",
            requester_session_id="attacker",
            defended_graph=graph,
            guard=guard,
            max_hops=1,
        )
        records.append(
            _record(
                "budget_curve",
                f"budget_{budget}",
                "victim_leaked_edges",
                report.leaked_edge_count,
            )
        )
        records.append(
            _record(
                "budget_curve",
                f"budget_{budget}",
                "utility_retention_rate",
                round(utility.utility_retention_rate, 4),
            )
        )

    return records


def _run_edge_admission_experiment() -> list[ExperimentRecord]:
    source_graph = build_large_synthetic_graph(num_users=20, sessions_per_user=3, seed=42)
    records: list[ExperimentRecord] = []

    for epsilon in (0.1, 1.0, 3.0):
        leaked_edges_runs = []
        utility_runs = []
        
        for run_idx in range(30):
            admission = RandomizedEdgeAdmission(
                EdgeAdmissionPolicy(epsilon=epsilon, seed=run_idx)
            )
            admitted_graph = admission.filter_graph(source_graph)
            probe = CrossSessionProbe(admitted_graph)
            report = probe.run(
                attacker_session_id="attacker-session",
                victim_session_id="session_0_0",
                probe_queries=["arrhythmia", "laptop"],
                max_hops=1,
            )
            leaked_edges_runs.append(report.leaked_edge_count)
            
            evaluator = UtilityEvaluator(source_graph)
            utility = evaluator.evaluate(
                query="hotel laptop",
                requester_session_id="attacker",
                defended_graph=admitted_graph,
                max_hops=1,
            )
            utility_runs.append(utility.utility_retention_rate)
            
        mean_leakage = statistics.mean(leaked_edges_runs)
        std_leakage = statistics.stdev(leaked_edges_runs) if len(leaked_edges_runs) > 1 else 0.0
        
        mean_utility = statistics.mean(utility_runs)
        std_utility = statistics.stdev(utility_runs) if len(utility_runs) > 1 else 0.0

        records.extend(
            [
                _record(
                    "edge_admission",
                    f"epsilon_{epsilon}",
                    "victim_leaked_edges_mean",
                    round(mean_leakage, 4),
                ),
                _record(
                    "edge_admission",
                    f"epsilon_{epsilon}",
                    "victim_leaked_edges_std",
                    round(std_leakage, 4),
                ),
                _record(
                    "edge_admission",
                    f"epsilon_{epsilon}",
                    "utility_retention_mean",
                    round(mean_utility, 4),
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
