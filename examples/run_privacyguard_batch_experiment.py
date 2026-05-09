import csv
import json
import os
import subprocess
import sys
from collections import defaultdict
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graphmemshield import (  # noqa: E402
    CrossSessionProbe,
    GraphMemGuard,
    GraphMemGuardPolicy,
    SessionGraphLink,
    TemporalPathInfer,
)
from graphmemshield.adapters import PrivacyGuardClient, PrivacyGuardGraphBuilder  # noqa: E402
from graphmemshield.datasets import (  # noqa: E402
    dialogue_records_to_privacyguard_docs,
    load_dialogue_jsonl,
    session_ids,
    user_ids,
)
from graphmemshield.evaluation import (  # noqa: E402
    leakage_reduction,
    ordering_accuracy,
    pairwise_ordering_accuracy,
    reciprocal_rank,
    set_precision_recall_f1,
    top_k_hit,
)


DATASET_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "sample_dialogues.jsonl"
)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
ATTACKER_SESSION_ID = "external-attacker-session"


def seed_mongo(docs: list[dict[str, Any]], seeded_user_ids: tuple[str, ...]) -> None:
    docs_json = json.dumps(docs).replace("\\", "\\\\").replace("'", "\\'")
    users_json = json.dumps(list(seeded_user_ids))
    script = (
        f"const docs = EJSON.parse('{docs_json}');"
        f"db.userData.deleteMany({{userId: {{$in: {users_json}}}}});"
        "db.userData.insertMany(docs);"
    )
    subprocess.run(
        ["docker", "exec", "zkp-mongodb", "mongosh", "privacyguard", "--quiet", "--eval", script],
        check=True,
        text=True,
        capture_output=True,
    )


def run_batch() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    records = load_dialogue_jsonl(DATASET_PATH)
    seeded_user_ids = user_ids(records)
    seed_mongo(dialogue_records_to_privacyguard_docs(records), seeded_user_ids)

    client = PrivacyGuardClient()
    health = client.health()
    records_by_user = {
        user_id: client.fetch_user_data(user_id, limit=200)
        for user_id in seeded_user_ids
    }
    graph = PrivacyGuardGraphBuilder().build(records_by_user)
    all_session_ids = session_ids(records)

    rows: list[dict[str, Any]] = []
    rows.extend(_cross_session_rows(graph, records))
    rows.extend(_query_budget_rows(graph, records))
    rows.extend(_session_link_rows(graph, records, all_session_ids))
    rows.extend(_temporal_rows(graph, records))

    summary = {
        "system": "privacyguard-docker",
        "dataset": "sample_dialogues",
        "health": health,
        "input_records": len(records),
        "fetched_records": sum(len(items) for items in records_by_user.values()),
        "user_count": len(seeded_user_ids),
        "session_count": len(all_session_ids),
        "node_count": len(graph.nodes),
        "edge_count": len(graph.edges),
    }
    return rows, summary


def write_outputs(rows: list[dict[str, Any]], summary: dict[str, Any]) -> dict[str, str]:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    json_path = os.path.join(OUTPUT_DIR, "privacyguard_batch_results.json")
    csv_path = os.path.join(OUTPUT_DIR, "privacyguard_batch_results.csv")
    md_path = os.path.join(OUTPUT_DIR, "privacyguard_batch_results.md")

    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump({"summary": summary, "results": rows}, handle, indent=2)

    with open(csv_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "system",
                "dataset",
                "attack",
                "condition",
                "metric",
                "value",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    with open(md_path, "w", encoding="utf-8") as handle:
        handle.write(render_markdown(rows, summary))

    return {"json": json_path, "csv": csv_path, "markdown": md_path}


def _cross_session_rows(graph, records) -> list[dict[str, Any]]:
    probe = CrossSessionProbe(graph)
    baseline_leaks = 0
    defended_leaks = 0
    query_count = 0
    for record in records:
        queries = [str(value) for value in record.entities.values()]
        baseline = probe.run(
            attacker_session_id=ATTACKER_SESSION_ID,
            victim_session_id=record.session_id,
            probe_queries=queries,
            max_hops=1,
        )
        defended = probe.run(
            attacker_session_id=ATTACKER_SESSION_ID,
            victim_session_id=record.session_id,
            probe_queries=queries,
            max_hops=1,
            guard=GraphMemGuard(GraphMemGuardPolicy()),
        )
        baseline_leaks += baseline.leaked_edge_count
        defended_leaks += defended.leaked_edge_count
        query_count += len(queries)

    return [
        _row("CrossSessionProbe", "baseline", "total_leaked_edges", baseline_leaks),
        _row("CrossSessionProbe", "strict_guard", "total_leaked_edges", defended_leaks),
        _row(
            "CrossSessionProbe",
            "strict_guard",
            "leakage_reduction",
            leakage_reduction(baseline_leaks, defended_leaks),
        ),
        _row("CrossSessionProbe", "baseline", "query_count", query_count),
        _row(
            "CrossSessionProbe",
            "strict_guard",
            "defense_framing",
            "strict_provenance_session_isolation",
            "Default GraphMemGuard blocks cross-session retrieval before graph expansion.",
        ),
    ]


def _query_budget_rows(graph, records) -> list[dict[str, Any]]:
    probe = CrossSessionProbe(graph)
    rows: list[dict[str, Any]] = []
    for budget in (1, 2, 4, "all"):
        total_leaks = 0
        total_queries = 0
        total_events = 0
        for record in records:
            queries = [str(value) for value in record.entities.values()]
            if budget != "all":
                queries = queries[: int(budget)]
            baseline = probe.run(
                attacker_session_id=ATTACKER_SESSION_ID,
                victim_session_id=record.session_id,
                probe_queries=queries,
                max_hops=1,
            )
            total_leaks += baseline.leaked_edge_count
            total_queries += len(queries)
            total_events += baseline.leakage_event_count
        rows.append(
            _row(
                "CrossSessionProbe",
                f"query_budget_{budget}",
                "total_leaked_edges",
                total_leaks,
            )
        )
        rows.append(
            _row(
                "CrossSessionProbe",
                f"query_budget_{budget}",
                "query_count",
                total_queries,
            )
        )
        rows.append(
            _row(
                "CrossSessionProbe",
                f"query_budget_{budget}",
                "leakage_event_count",
                total_events,
            )
        )
    return rows


def _session_link_rows(graph, records, all_session_ids) -> list[dict[str, Any]]:
    sessions_by_user: dict[str, list[str]] = defaultdict(list)
    for record in records:
        sessions_by_user[record.user_id].append(record.session_id)

    rows: list[dict[str, Any]] = []
    for include_semantic in (False, True):
        condition = "semantic_labels" if include_semantic else "structure_only"
        evaluated, top1_hits, top3_hits, rr_total = _evaluate_session_link(
            graph,
            sessions_by_user,
            all_session_ids,
            include_semantic_labels=include_semantic,
        )
        rows.extend(
            [
                _row("SessionGraphLink", condition, "evaluated_users", evaluated),
                _row(
                    "SessionGraphLink",
                    condition,
                    "top1_accuracy",
                    top1_hits / evaluated if evaluated else 0.0,
                ),
                _row(
                    "SessionGraphLink",
                    condition,
                    "top3_accuracy",
                    top3_hits / evaluated if evaluated else 0.0,
                ),
                _row(
                    "SessionGraphLink",
                    condition,
                    "mean_reciprocal_rank",
                    rr_total / evaluated if evaluated else 0.0,
                ),
            ]
        )
    return rows


def _temporal_rows(graph, records) -> list[dict[str, Any]]:
    infer = TemporalPathInfer(graph)
    ordering_scores: list[float] = []
    pairwise_scores: list[float] = []
    precision_scores: list[float] = []
    recall_scores: list[float] = []
    f1_scores: list[float] = []
    for record in records:
        if not record.entities:
            continue
        query = str(next(iter(record.entities.values())))
        report = infer.infer(
            query=query,
            requester_session_id=ATTACKER_SESSION_ID,
            max_hops=1,
        )
        expected = tuple(
            edge.edge_id
            for edge in sorted(
                graph.edges_by_session(record.session_id),
                key=lambda edge: (edge.created_at, edge.edge_id),
            )
        )
        if expected:
            predicted_prefix = report.inferred_edge_ids[: len(expected)]
            ordering_scores.append(ordering_accuracy(predicted_prefix, expected))
            pairwise_scores.append(
                pairwise_ordering_accuracy(report.inferred_edge_ids, expected)
            )
            precision, recall, f1 = set_precision_recall_f1(
                report.inferred_edge_ids,
                expected,
            )
            precision_scores.append(precision)
            recall_scores.append(recall)
            f1_scores.append(f1)

    evaluated = len(ordering_scores)
    return [
        _row("TemporalPathInfer", "timestamp_order", "evaluated_sessions", evaluated),
        _row(
            "TemporalPathInfer",
            "timestamp_order",
            "average_ordering_accuracy",
            _average(ordering_scores),
        ),
        _row(
            "TemporalPathInfer",
            "timestamp_order",
            "pairwise_ordering_accuracy",
            _average(pairwise_scores),
        ),
        _row("TemporalPathInfer", "timestamp_order", "edge_precision", _average(precision_scores)),
        _row("TemporalPathInfer", "timestamp_order", "edge_recall", _average(recall_scores)),
        _row("TemporalPathInfer", "timestamp_order", "edge_f1", _average(f1_scores)),
    ]


def _evaluate_session_link(
    graph,
    sessions_by_user: dict[str, list[str]],
    all_session_ids,
    *,
    include_semantic_labels: bool,
) -> tuple[int, int, int, float]:
    linker = SessionGraphLink(graph)
    evaluated = 0
    top1_hits = 0
    top3_hits = 0
    rr_total = 0.0
    for user_sessions in sessions_by_user.values():
        unique_sessions = sorted(set(user_sessions))
        if len(unique_sessions) < 2:
            continue
        query_session = unique_sessions[0]
        expected_session = unique_sessions[1]
        report = linker.rank(
            query_session_id=query_session,
            candidate_session_ids=all_session_ids,
            include_semantic_labels=include_semantic_labels,
        )
        ranked_ids = tuple(candidate.session_id for candidate in report.candidates)
        evaluated += 1
        top1_hits += int(top_k_hit(ranked_ids, expected_session, k=1))
        top3_hits += int(top_k_hit(ranked_ids, expected_session, k=3))
        rr_total += reciprocal_rank(ranked_ids, expected_session)
    return evaluated, top1_hits, top3_hits, rr_total


def _average(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _row(attack: str, condition: str, metric: str, value: Any, notes: str = "") -> dict[str, Any]:
    return {
        "system": "privacyguard-docker",
        "dataset": "sample_dialogues",
        "attack": attack,
        "condition": condition,
        "metric": metric,
        "value": value,
        "notes": notes,
    }


def render_markdown(rows: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        "# GraphMemShield PrivacyGuard Batch Results",
        "",
        "## Summary",
        "",
        f"- System: `{summary['system']}`",
        f"- Dataset: `{summary['dataset']}`",
        f"- Input records: `{summary['input_records']}`",
        f"- Fetched records: `{summary['fetched_records']}`",
        f"- Users: `{summary['user_count']}`",
        f"- Sessions: `{summary['session_count']}`",
        f"- Nodes: `{summary['node_count']}`",
        f"- Edges: `{summary['edge_count']}`",
        "",
        "## Results",
        "",
        "| System | Dataset | Attack | Condition | Metric | Value | Notes |",
        "|---|---|---|---|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row['system']} | {row['dataset']} | {row['attack']} | "
            f"{row['condition']} | {row['metric']} | {row['value']} | "
            f"{row['notes']} |"
        )
    lines.extend(
        [
            "",
            "## Manual Follow-up",
            "",
            "- Replace sample JSONL with approved public datasets or larger de-identified exports.",
            "- Add response-level scoring after a real system response endpoint is available.",
            "- Add multiple attacker sessions and repeated query-budget curves.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    rows, summary = run_batch()
    paths = write_outputs(rows, summary)
    print(json.dumps({"summary": summary, "results": rows}, indent=2))
    print(f"json: {paths['json']}")
    print(f"csv: {paths['csv']}")
    print(f"markdown: {paths['markdown']}")


if __name__ == "__main__":
    main()
