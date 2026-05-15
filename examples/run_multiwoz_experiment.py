import csv
import json
import os
import sys
import urllib.request
import zipfile
from dataclasses import asdict
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graphmemshield import CrossSessionProbe, GraphMemGuard, GraphMemGuardPolicy  # noqa: E402
from graphmemshield.datasets.dialogue import dialogue_records_to_graph  # noqa: E402
from graphmemshield.datasets.public_ingest import load_multiwoz_dialogues  # noqa: E402
from graphmemshield.evaluation.blackbox import (  # noqa: E402
    ResponseLeakageScorer,
    TemplateResponseGenerator,
)
from graphmemshield.evaluation.utility_evaluator import UtilityEvaluator  # noqa: E402


OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MULTIWOZ_URL = "https://raw.githubusercontent.com/budzianowski/multiwoz/master/data/MultiWOZ_2.1.zip"


def main() -> None:
    max_dialogues = int(os.environ.get("GRAPHMEMSHIELD_MULTIWOZ_DIALOGUES", "1000"))
    source_path = _ensure_multiwoz_data()
    records = load_multiwoz_dialogues(source_path, max_dialogues=max_dialogues)
    graph = dialogue_records_to_graph(records)
    DATA_DIR.mkdir(exist_ok=True)
    sample_path = DATA_DIR / "multiwoz_2_1_sample.jsonl"
    _write_records(records, sample_path)

    rows = []
    rows.extend(_dataset_rows(records, graph, max_dialogues))
    rows.extend(_leakage_rows(graph))
    rows.extend(_blackbox_rows(graph))
    OUTPUT_DIR.mkdir(exist_ok=True)
    _write_json(rows, "multiwoz_results.json")
    _write_csv(rows, "multiwoz_results.csv")
    _write_markdown(rows, "multiwoz_results.md")
    print(f"multiwoz rows: {len(rows)}")
    print(f"sample jsonl: {sample_path}")


def _ensure_multiwoz_data() -> Path:
    env_path = os.environ.get("GRAPHMEMSHIELD_MULTIWOZ_DATA")
    if env_path:
        return Path(env_path)
    tmp_dir = Path("/tmp/graphmemshield_multiwoz")
    tmp_dir.mkdir(exist_ok=True)
    data_path = tmp_dir / "data.json"
    if data_path.exists():
        return data_path
    zip_path = tmp_dir / "MultiWOZ_2.1.zip"
    if not zip_path.exists():
        urllib.request.urlretrieve(MULTIWOZ_URL, zip_path)
    with zipfile.ZipFile(zip_path) as archive:
        data_path.write_bytes(archive.read("MultiWOZ_2.1/data.json"))
    return data_path


def _dataset_rows(records, graph, max_dialogues: int) -> list[dict[str, Any]]:
    return [
        _row("multiwoz_2_1", "dataset", "max_dialogues", max_dialogues),
        _row("multiwoz_2_1", "dataset", "records", len(records)),
        _row("multiwoz_2_1", "dataset", "users", len({record.user_id for record in records})),
        _row("multiwoz_2_1", "dataset", "sessions", len({record.session_id for record in records})),
        _row("multiwoz_2_1", "dataset", "nodes", len(graph.nodes)),
        _row("multiwoz_2_1", "dataset", "edges", len(graph.edges)),
    ]


def _leakage_rows(graph) -> list[dict[str, Any]]:
    sessions = sorted({edge.owner_session_id for edge in graph.edges})
    victim = sessions[0]
    attacker = sessions[1] if len(sessions) > 1 else "multiwoz-attacker"
    queries = _queries_for_victim(graph, victim)
    baseline = CrossSessionProbe(graph).run(
        attacker_session_id=attacker,
        victim_session_id=victim,
        probe_queries=queries,
        max_hops=1,
    )
    rows = [
        _row("baseline", "cross_session_probe", "queries", len(queries)),
        _row("baseline", "cross_session_probe", "leaked_edges", baseline.leaked_edge_count),
        _row("baseline", "cross_session_probe", "leakage_events", baseline.leakage_event_count),
    ]
    evaluator = UtilityEvaluator(graph)
    for budget in (0, 1, 2, 5):
        guard = GraphMemGuard(
            GraphMemGuardPolicy(
                allow_cross_session=True,
                max_cross_session_edges_per_pair=budget,
                blocked_sensitivity_labels=frozenset({"medical", "financial", "secret"}),
            )
        )
        report = CrossSessionProbe(graph).run(
            attacker_session_id=attacker,
            victim_session_id=victim,
            probe_queries=queries,
            max_hops=1,
            guard=guard,
        )
        utility = evaluator.evaluate(
            query=" ".join(queries),
            requester_session_id=attacker,
            guard=guard,
            max_hops=1,
        )
        rows.extend(
            [
                _row(f"budget_{budget}", "bounded_sharing", "leaked_edges", report.leaked_edge_count),
                _row(f"budget_{budget}", "bounded_sharing", "utility_retention", round(utility.utility_retention_rate, 4)),
            ]
        )
    return rows


def _blackbox_rows(graph) -> list[dict[str, Any]]:
    sessions = sorted({edge.owner_session_id for edge in graph.edges})
    victim = sessions[0]
    attacker = sessions[1] if len(sessions) > 1 else "multiwoz-attacker"
    query = " ".join(_queries_for_victim(graph, victim)[:3])
    victim_edges = graph.edges_by_session(victim)
    scorer = ResponseLeakageScorer()
    rows = []
    for condition, guard in (
        ("baseline", None),
        ("budget_0", GraphMemGuard(GraphMemGuardPolicy(allow_cross_session=True, max_cross_session_edges_per_pair=0))),
        (
            "budget_5",
            GraphMemGuard(
                GraphMemGuardPolicy(
                    allow_cross_session=True,
                    max_cross_session_edges_per_pair=5,
                    blocked_sensitivity_labels=frozenset({"medical", "financial", "secret"}),
                )
            ),
        ),
    ):
        result = graph.retrieve(query, attacker, max_hops=1, guard=guard)
        response = TemplateResponseGenerator().generate(result)
        report = scorer.score(
            response_text=response,
            victim_edges=victim_edges,
            secret_terms=tuple(_queries_for_victim(graph, victim)),
        )
        rows.extend(
            [
                _row(condition, "blackbox_response", "response_chars", len(response)),
                _row(condition, "blackbox_response", "leaked_edges", report.leaked_edge_count),
                _row(condition, "blackbox_response", "leaked_terms", report.leaked_secret_term_count),
            ]
        )
    return rows


def _queries_for_victim(graph, victim: str) -> tuple[str, ...]:
    terms = []
    for edge in graph.edges_by_session(victim):
        for raw in (edge.target_id, edge.relation):
            for term in raw.replace("-", " ").split():
                if len(term) >= 4 and term not in terms:
                    terms.append(term)
    return tuple(terms[:8] or ("hotel", "restaurant"))


def _write_records(records, path: Path) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            payload = asdict(record)
            payload["relations"] = [asdict(relation) for relation in record.relations]
            handle.write(json.dumps(payload, sort_keys=True) + "\n")


def _row(condition: str, experiment: str, metric: str, value: Any) -> dict[str, Any]:
    return {
        "system": "graphmemshield",
        "dataset": "multiwoz_2_1",
        "experiment": experiment,
        "condition": condition,
        "metric": metric,
        "value": value,
    }


def _write_json(rows: list[dict[str, Any]], filename: str) -> None:
    with (OUTPUT_DIR / filename).open("w", encoding="utf-8") as handle:
        json.dump(rows, handle, indent=2)


def _write_csv(rows: list[dict[str, Any]], filename: str) -> None:
    with (OUTPUT_DIR / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["system", "dataset", "experiment", "condition", "metric", "value"])
        writer.writeheader()
        writer.writerows(rows)


def _write_markdown(rows: list[dict[str, Any]], filename: str) -> None:
    lines = [
        "# MultiWOZ 2.1 External Corpus Experiment",
        "",
        "| System | Dataset | Experiment | Condition | Metric | Value |",
        "|---|---|---|---|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['system']} | {row['dataset']} | {row['experiment']} | "
            f"{row['condition']} | {row['metric']} | {row['value']} |"
        )
    with (OUTPUT_DIR / filename).open("w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
