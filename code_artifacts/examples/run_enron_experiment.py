import csv
import json
import os
import shutil
import sys
from email.message import EmailMessage
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graphmemshield import CrossSessionProbe, GraphMemGuard, GraphMemGuardPolicy  # noqa: E402
from graphmemshield.datasets.dialogue import dialogue_records_to_graph  # noqa: E402
from graphmemshield.datasets.public_ingest import load_enron_maildir  # noqa: E402
from graphmemshield.evaluation.blackbox import (  # noqa: E402
    EvidenceDumpResponseGenerator,
    ResponseLeakageScorer,
    SemanticResponseLeakageScorer,
    TemplateResponseGenerator,
)
from graphmemshield.evaluation.utility_evaluator import UtilityEvaluator  # noqa: E402


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output"
DATA_DIR = ROOT / "data"


def main() -> None:
    max_messages = int(os.environ.get("GRAPHMEMSHIELD_ENRON_MESSAGES", "160"))
    source = _ensure_enron_source(max_messages)
    records = load_enron_maildir(source, max_messages=max_messages)
    graph = dialogue_records_to_graph(records)
    rows: list[dict[str, Any]] = []
    rows.extend(_dataset_rows(records, graph, source))
    rows.extend(_leakage_rows(graph))
    rows.extend(_response_rows(graph))

    OUTPUT_DIR.mkdir(exist_ok=True)
    _write_json(rows, "enron_results.json")
    _write_csv(rows, "enron_results.csv")
    _write_markdown(rows, "enron_results.md")
    print(f"enron rows: {len(rows)}")
    print(f"source: {source}")


def _ensure_enron_source(max_messages: int) -> Path:
    env_path = os.environ.get("GRAPHMEMSHIELD_ENRON_MAILDIR")
    if env_path:
        return Path(env_path)
    fixture_dir = DATA_DIR / "enron_style_maildir"
    if fixture_dir.exists():
        shutil.rmtree(fixture_dir)
    _write_enron_style_fixture(fixture_dir, max_messages)
    return fixture_dir


def _write_enron_style_fixture(root: Path, max_messages: int) -> None:
    senders = (
        "alice.legal@enron.example",
        "bob.trading@enron.example",
        "carol.hr@enron.example",
        "dave.risk@enron.example",
        "erin.finance@enron.example",
        "frank.ops@enron.example",
    )
    recipients = (
        "legal-team@enron.example",
        "trading-desk@enron.example",
        "hr-confidential@enron.example",
        "risk-committee@enron.example",
        "finance-review@enron.example",
        "ops-center@enron.example",
    )
    subjects = (
        "Confidential settlement discussion",
        "Daily power trading schedule",
        "Salary review packet",
        "Investigation document hold",
        "Quarterly finance forecast",
        "Pipeline outage update",
        "Legal privilege review",
        "Counterparty exposure report",
    )
    root.mkdir(parents=True, exist_ok=True)
    for index in range(max_messages):
        sender = senders[index % len(senders)]
        to = recipients[(index + 1) % len(recipients)]
        cc = recipients[(index + 3) % len(recipients)] if index % 4 == 0 else ""
        sender_slug = sender.split("@", 1)[0].replace(".", "-")
        subject = f"{subjects[index % len(subjects)]} {sender_slug} thread-{index // len(senders)}"
        message = EmailMessage()
        message["From"] = sender
        message["To"] = to
        if cc:
            message["Cc"] = cc
        message["Subject"] = subject
        message["Date"] = f"Mon, {(index % 28) + 1} Jan 2001 10:{index % 60:02d}:00 -0000"
        message.set_content(
            "This fixture preserves Enron-style enterprise communication "
            "structure without containing real personal email content."
        )
        sender_dir = root / sender.split("@", 1)[0] / "sent"
        sender_dir.mkdir(parents=True, exist_ok=True)
        (sender_dir / f"{index:05d}.eml").write_text(message.as_string(), encoding="utf-8")


def _dataset_rows(records, graph, source: Path) -> list[dict[str, Any]]:
    return [
        _row("enron_maildir", "dataset", "source_mode", "user_maildir" if os.environ.get("GRAPHMEMSHIELD_ENRON_MAILDIR") else "enron_style_fixture"),
        _row("enron_maildir", "dataset", "source_path", str(source)),
        _row("enron_maildir", "dataset", "records", len(records)),
        _row("enron_maildir", "dataset", "users", len({record.user_id for record in records})),
        _row("enron_maildir", "dataset", "sessions", len({record.session_id for record in records})),
        _row("enron_maildir", "dataset", "nodes", len(graph.nodes)),
        _row("enron_maildir", "dataset", "edges", len(graph.edges)),
    ]


def _leakage_rows(graph) -> list[dict[str, Any]]:
    victim, attacker = _victim_attacker(graph)
    queries = _queries_for_victim(graph, victim)
    baseline = CrossSessionProbe(graph).run(
        attacker_session_id=attacker,
        victim_session_id=victim,
        probe_queries=queries,
        max_hops=2,
    )
    rows = [
        _row("baseline", "communication_graph_probe", "queries", len(queries)),
        _row("baseline", "communication_graph_probe", "leaked_edges", baseline.leaked_edge_count),
        _row("baseline", "communication_graph_probe", "leakage_events", baseline.leakage_event_count),
    ]
    evaluator = UtilityEvaluator(graph)
    for budget in (0, 1, 2, 5):
        guard = GraphMemGuard(
            GraphMemGuardPolicy(
                allow_cross_session=True,
                max_cross_session_edges_per_pair=budget,
                blocked_sensitivity_labels=frozenset({"secret", "medical", "financial"}),
            )
        )
        report = CrossSessionProbe(graph).run(
            attacker_session_id=attacker,
            victim_session_id=victim,
            probe_queries=queries,
            max_hops=2,
            guard=guard,
        )
        utility = evaluator.evaluate(
            query=" ".join(queries),
            requester_session_id=attacker,
            guard=guard,
            max_hops=2,
        )
        rows.extend(
            [
                _row(f"budget_{budget}", "communication_graph_probe", "leaked_edges", report.leaked_edge_count),
                _row(f"budget_{budget}", "communication_graph_probe", "utility_retention", round(utility.utility_retention_rate, 4)),
            ]
        )
    return rows


def _response_rows(graph) -> list[dict[str, Any]]:
    victim, attacker = _victim_attacker(graph)
    query = " ".join(_queries_for_victim(graph, victim)[:4])
    victim_edges = graph.edges_by_session(victim)
    secret_terms = _secret_terms(victim_edges)
    lexical = ResponseLeakageScorer()
    semantic = SemanticResponseLeakageScorer()
    rows: list[dict[str, Any]] = []
    for condition, guard in (
        ("baseline", None),
        ("budget_0", GraphMemGuard(GraphMemGuardPolicy(allow_cross_session=True, max_cross_session_edges_per_pair=0))),
        (
            "budget_5",
            GraphMemGuard(
                GraphMemGuardPolicy(
                    allow_cross_session=True,
                    max_cross_session_edges_per_pair=5,
                    blocked_sensitivity_labels=frozenset({"secret", "medical", "financial"}),
                )
            ),
        ),
    ):
        result = graph.retrieve(query, attacker, max_hops=2, guard=guard)
        for generator_name, generator in (
            ("template", TemplateResponseGenerator()),
            ("evidence_dump", EvidenceDumpResponseGenerator()),
        ):
            response = generator.generate(result)
            lexical_report = lexical.score(
                response_text=response,
                victim_edges=victim_edges,
                secret_terms=secret_terms,
            )
            semantic_report = semantic.score(
                response_text=response,
                victim_edges=victim_edges,
                secret_terms=secret_terms,
            )
            row_condition = f"{condition}_{generator_name}"
            rows.extend(
                [
                    _row(row_condition, "semantic_response_leakage", "lexical_edges", lexical_report.leaked_edge_count),
                    _row(row_condition, "semantic_response_leakage", "semantic_edges", semantic_report.semantic_edge_count),
                    _row(row_condition, "semantic_response_leakage", "lexical_terms", lexical_report.leaked_secret_term_count),
                    _row(row_condition, "semantic_response_leakage", "semantic_terms", semantic_report.semantic_secret_term_count),
                ]
            )
    return rows


def _victim_attacker(graph) -> tuple[str, str]:
    sessions = sorted({edge.owner_session_id for edge in graph.edges})
    victim = sessions[0]
    victim_users = {edge.source_user_id for edge in graph.edges_by_session(victim)}
    for session in sessions[1:]:
        users = {edge.source_user_id for edge in graph.edges_by_session(session)}
        if users.isdisjoint(victim_users):
            return victim, session
    return victim, sessions[1] if len(sessions) > 1 else "enron-attacker"


def _queries_for_victim(graph, victim: str) -> tuple[str, ...]:
    terms = []
    for edge in graph.edges_by_session(victim):
        for raw in (edge.source_id, edge.relation, edge.target_id):
            for term in raw.replace(":", " ").replace("-", " ").replace("_", " ").split():
                if len(term) >= 4 and term not in terms:
                    terms.append(term)
    return tuple(terms[:8] or ("confidential", "settlement", "trading"))


def _secret_terms(edges) -> tuple[str, ...]:
    terms = []
    for edge in edges:
        if edge.sensitivity == "normal":
            continue
        raws = (edge.source_id,) if edge.relation == "has_sensitivity" else (edge.relation, edge.target_id)
        for raw in raws:
            for term in raw.replace(":", " ").replace("-", " ").replace("_", " ").split():
                if len(term) >= 4 and term not in {"subject", "thread", "enron", "example"} and term not in terms:
                    terms.append(term)
    return tuple(terms[:12])


def _row(condition: str, experiment: str, metric: str, value: Any) -> dict[str, Any]:
    return {
        "system": "graphmemshield",
        "dataset": "enron_communication_graph",
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
        "# Enron-Style Communication Graph Experiment",
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
