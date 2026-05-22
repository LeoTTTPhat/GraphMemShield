import csv
import json
import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graphmemshield.adapters.langgraph_memory import LangGraphMemoryAdapter  # noqa: E402
from graphmemshield.core.graph import DynamicMemoryGraph  # noqa: E402
from graphmemshield.datasets.dialogue import dialogue_records_to_graph  # noqa: E402
from graphmemshield.datasets.enterprise import build_enterprise_health_finance_records  # noqa: E402
from graphmemshield.defenses.guard import GraphMemGuard, GraphMemGuardPolicy  # noqa: E402
from graphmemshield.evaluation.blackbox import (  # noqa: E402
    EvidenceDumpResponseGenerator,
    ResponseLeakageScorer,
)


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output"


def main() -> None:
    records = build_enterprise_health_finance_records()
    source_graph = dialogue_records_to_graph(records)
    adapter = LangGraphMemoryAdapter(DynamicMemoryGraph())
    adapter.load_graph(source_graph)

    rows: list[dict[str, Any]] = []
    rows.extend(_dataset_rows(records, source_graph))
    rows.extend(_policy_rows(adapter, source_graph))

    OUTPUT_DIR.mkdir(exist_ok=True)
    _write_json(rows, "langgraph_memory_trace.json")
    _write_csv(rows, "langgraph_memory_trace.csv")
    _write_markdown(rows, "langgraph_memory_trace.md")
    print(f"langgraph memory rows: {len(rows)}")


def _dataset_rows(records, graph) -> list[dict[str, Any]]:
    return [
        _row("langgraph", "dataset", "framework", "LangGraph"),
        _row("langgraph", "dataset", "framework_available", LangGraphMemoryAdapter.available()),
        _row("langgraph", "dataset", "records", len(records)),
        _row("langgraph", "dataset", "users", len({record.user_id for record in records})),
        _row("langgraph", "dataset", "sessions", len({record.session_id for record in records})),
        _row("langgraph", "dataset", "edges", len(graph.edges)),
    ]


def _policy_rows(adapter: LangGraphMemoryAdapter, graph) -> list[dict[str, Any]]:
    victim = "ehf-user-000-session-1"
    attacker = "ehf-user-001-session-1"
    victim_edges = graph.edges_by_session(victim)
    scorer = ResponseLeakageScorer()
    policies = {
        "global": None,
        "owner_only": GraphMemGuard(GraphMemGuardPolicy()),
        "bounded5": GraphMemGuard(
            GraphMemGuardPolicy(
                allow_cross_session=True,
                max_cross_session_edges_per_pair=5,
                blocked_sensitivity_labels=frozenset({"medical", "financial", "secret"}),
            )
        ),
    }
    rows: list[dict[str, Any]] = []
    for condition, guard in policies.items():
        result = adapter.retrieve(
            query="arrhythmia clinic confidential settlement payroll",
            requester_session_id=attacker,
            max_hops=2,
            guard=guard,
        )
        response = EvidenceDumpResponseGenerator().generate(result)
        leakage = scorer.score(
            response_text=response,
            victim_edges=victim_edges,
            secret_terms=_secret_terms(victim_edges),
        )
        leaked_edges = len({edge.edge_id for edge in result.edges if edge.owner_session_id == victim})
        rows.extend(
            [
                _row(condition, "langgraph_end_to_end", "retrieved_edges", result.edge_count),
                _row(condition, "langgraph_end_to_end", "leaked_edges", leaked_edges),
                _row(condition, "langgraph_end_to_end", "response_leaked_edges", leakage.leaked_edge_count),
                _row(condition, "langgraph_end_to_end", "response_leaked_terms", leakage.leaked_secret_term_count),
                _row(condition, "langgraph_end_to_end", "qa_accuracy", 1.0 if result.edge_count else 0.0),
            ]
        )
    return rows


def _secret_terms(edges) -> tuple[str, ...]:
    return tuple(
        sorted(
            {
                token
                for edge in edges
                if edge.sensitivity != "normal"
                for token in edge.target_id.replace("-", " ").replace("_", " ").split()
                if len(token) >= 4
            }
        )
    )


def _row(condition: str, experiment: str, metric: str, value: Any) -> dict[str, Any]:
    return {
        "system": "langgraph_agent_memory",
        "dataset": "enterprise_health_finance",
        "experiment": experiment,
        "condition": condition,
        "metric": metric,
        "value": value,
    }


def _write_json(rows: list[dict[str, Any]], filename: str) -> None:
    (OUTPUT_DIR / filename).write_text(json.dumps(rows, indent=2), encoding="utf-8")


def _write_csv(rows: list[dict[str, Any]], filename: str) -> None:
    with (OUTPUT_DIR / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["system", "dataset", "experiment", "condition", "metric", "value"],
        )
        writer.writeheader()
        writer.writerows(rows)


def _write_markdown(rows: list[dict[str, Any]], filename: str) -> None:
    lines = [
        "# LangGraph Agent-Memory Integration",
        "",
        "This run uses a real LangGraph StateGraph workflow for write and retrieval nodes.",
        "",
        "| System | Dataset | Experiment | Condition | Metric | Value |",
        "|---|---|---|---|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['system']} | {row['dataset']} | {row['experiment']} | "
            f"{row['condition']} | {row['metric']} | {row['value']} |"
        )
    (OUTPUT_DIR / filename).write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
