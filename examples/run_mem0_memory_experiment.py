import csv
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graphmemshield.adapters.mem0_memory import Mem0MemoryAdapter  # noqa: E402
from graphmemshield.datasets.dialogue import dialogue_records_to_graph  # noqa: E402
from graphmemshield.datasets.enterprise import build_enterprise_health_finance_records  # noqa: E402
from graphmemshield.defenses.guard import GraphMemGuard, GraphMemGuardPolicy  # noqa: E402
from graphmemshield.evaluation.blackbox import EvidenceDumpResponseGenerator, ResponseLeakageScorer  # noqa: E402


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output"


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        rows = [_row("mem0", "dataset", "status", "skipped_missing_openai_api_key")]
        _write_all(rows)
        print(f"mem0 memory rows: {len(rows)}")
        return

    records = build_enterprise_health_finance_records()
    graph = dialogue_records_to_graph(records)
    victim = "ehf-user-000-session-1"
    attacker = "ehf-user-001-session-1"
    indexed_edges = _edge_sample(graph, victim, attacker)
    storage_dir = OUTPUT_DIR / "mem0_memory_index"
    shutil.rmtree(storage_dir, ignore_errors=True)
    adapter = Mem0MemoryAdapter(graph=graph, storage_dir=storage_dir)
    adapter.load_edges(indexed_edges)

    rows: list[dict[str, Any]] = [
        _row("mem0", "dataset", "framework", "Mem0"),
        _row("mem0", "dataset", "framework_available", Mem0MemoryAdapter.available()),
        _row("mem0", "dataset", "indexed_edges", len(indexed_edges)),
        _row("mem0", "dataset", "victim_indexed_edges", len([e for e in indexed_edges if e.owner_session_id == victim])),
    ]
    rows.extend(_policy_rows(adapter, graph, victim, attacker))
    _write_all(rows)
    print(f"mem0 memory rows: {len(rows)}")


def _edge_sample(graph, victim: str, attacker: str):
    victim_edges = list(graph.edges_by_session(victim))[:16]
    attacker_edges = list(graph.edges_by_session(attacker))[:16]
    bridge_edges = [
        edge
        for edge in graph.edges
        if edge.owner_session_id not in {victim, attacker}
        and any(term in edge.target_id.lower() for term in ("clinic", "vendor", "payroll", "hotel"))
    ][:16]
    return victim_edges + attacker_edges + bridge_edges


def _policy_rows(adapter: Mem0MemoryAdapter, graph, victim: str, attacker: str) -> list[dict[str, Any]]:
    scorer = ResponseLeakageScorer()
    victim_edges = graph.edges_by_session(victim)
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
        result = adapter.search(
            query="arrhythmia clinic confidential settlement payroll",
            requester_session_id=attacker,
            top_k=24,
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
                _row(condition, "mem0_end_to_end", "retrieved_edges", result.edge_count),
                _row(condition, "mem0_end_to_end", "leaked_edges", leaked_edges),
                _row(condition, "mem0_end_to_end", "response_leaked_edges", leakage.leaked_edge_count),
                _row(condition, "mem0_end_to_end", "response_leaked_terms", leakage.leaked_secret_term_count),
                _row(condition, "mem0_end_to_end", "qa_accuracy", 1.0 if result.edge_count else 0.0),
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
        "system": "mem0_agent_memory",
        "dataset": "enterprise_health_finance",
        "experiment": experiment,
        "condition": condition,
        "metric": metric,
        "value": value,
    }


def _write_all(rows: list[dict[str, Any]]) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    _write_json(rows, "mem0_memory_trace.json")
    _write_csv(rows, "mem0_memory_trace.csv")
    _write_markdown(rows, "mem0_memory_trace.md")


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
        "# Mem0 Agent-Memory Integration",
        "",
        "This run uses the real `mem0ai` package with local Qdrant storage and OpenAI embeddings.",
        "It indexes a bounded enterprise edge sample to keep the reproducible run small.",
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
