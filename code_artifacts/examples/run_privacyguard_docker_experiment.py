import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graphmemshield import CrossSessionProbe, GraphMemGuard, GraphMemGuardPolicy  # noqa: E402
from graphmemshield.adapters import (  # noqa: E402
    PrivacyGuardClient,
    PrivacyGuardGraphBuilder,
    build_seed_documents,
)
from graphmemshield.evaluation import leakage_reduction  # noqa: E402


SEED_USER_IDS = ("graphmem-alice", "graphmem-bob")


def seed_mongo() -> None:
    docs = build_seed_documents()
    script = (
        "db.userData.deleteMany({userId: {$in: "
        + json.dumps(list(SEED_USER_IDS))
        + "}});"
        + "db.userData.insertMany("
        + json.dumps(docs)
        + ");"
    )
    subprocess.run(
        ["docker", "exec", "zkp-mongodb", "mongosh", "privacyguard", "--quiet", "--eval", script],
        check=True,
        text=True,
        capture_output=True,
    )


def main() -> None:
    seed_mongo()
    client = PrivacyGuardClient()
    health = client.health()
    records_by_user = {
        user_id: client.fetch_user_data(user_id)
        for user_id in SEED_USER_IDS
    }
    graph = PrivacyGuardGraphBuilder().build(records_by_user)

    probe = CrossSessionProbe(graph)
    baseline = probe.run(
        attacker_session_id="attacker-session",
        victim_session_id="alice-session-1",
        probe_queries=["Heart Clinic", "arrhythmia", "Melbourne"],
        max_hops=1,
    )
    defended = probe.run(
        attacker_session_id="attacker-session",
        victim_session_id="alice-session-1",
        probe_queries=["Heart Clinic", "arrhythmia", "Melbourne"],
        max_hops=1,
        guard=GraphMemGuard(GraphMemGuardPolicy()),
    )

    output = {
        "health": health,
        "record_counts": {user_id: len(records) for user_id, records in records_by_user.items()},
        "graph": {
            "node_count": len(graph.nodes),
            "edge_count": len(graph.edges),
        },
        "baseline": {
            "leaked_edge_count": baseline.leaked_edge_count,
            "leakage_event_count": baseline.leakage_event_count,
            "leaked_edge_ids": baseline.leaked_edge_ids,
            "leakage_rate": baseline.leakage_rate,
            "event_leakage_rate": baseline.event_leakage_rate,
            "per_query_leak_rate": baseline.per_query_leak_rate,
        },
        "defended": {
            "leaked_edge_count": defended.leaked_edge_count,
            "leakage_event_count": defended.leakage_event_count,
            "leaked_edge_ids": defended.leaked_edge_ids,
            "leakage_reduction": leakage_reduction(
                baseline.leaked_edge_count,
                defended.leaked_edge_count,
            ),
            "framing": "strict provenance/session isolation",
        },
    }

    output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "privacyguard_docker_experiment.json")
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=2)
    report_path = os.path.join(output_dir, "privacyguard_docker_experiment.md")
    with open(report_path, "w", encoding="utf-8") as handle:
        handle.write(render_report(output))

    print(json.dumps(output, indent=2))
    print(f"wrote: {output_path}")
    print(f"wrote: {report_path}")


def render_report(output: dict) -> str:
    lines = [
        "# GraphMemShield PrivacyGuard Docker Experiment",
        "",
        "This experiment seeds de-identified records into the running PrivacyGuard MongoDB",
        "mock, fetches them through the Cloud API, maps them into a GraphMemShield",
        "memory graph, and evaluates cross-session leakage.",
        "",
        "## System Health",
        "",
        f"- Edge: `{output['health']['edge']['status']}`",
        f"- Fog: `{output['health']['fog']['status']}`",
        f"- Cloud: `{output['health']['cloud']['status']}`",
        f"- Mongo state: `{output['health']['cloud'].get('mongoState')}`",
        "",
        "## Data and Graph",
        "",
        f"- Records: `{output['record_counts']}`",
        f"- Nodes: `{output['graph']['node_count']}`",
        f"- Edges: `{output['graph']['edge_count']}`",
        "",
        "## Leakage Results",
        "",
        f"- Baseline leaked edges: `{output['baseline']['leaked_edge_count']}`",
        f"- Baseline leakage events: `{output['baseline']['leakage_event_count']}`",
        f"- Baseline leakage rate: `{output['baseline']['leakage_rate']}`",
        f"- Baseline event leakage rate: `{output['baseline']['event_leakage_rate']}`",
        f"- Defended leaked edges: `{output['defended']['leaked_edge_count']}`",
        f"- Leakage reduction: `{output['defended']['leakage_reduction']}`",
        f"- Defense framing: `{output['defended']['framing']}`",
        "",
        "## Manual Follow-up",
        "",
        "- Replace seed records with public datasets or approved real records.",
        "- Avoid storing raw personal identifiers in seed data; use de-identified IDs.",
        "- Add API-level write flow through `/api/validate-and-prove` and `/api/store` when proof material is available.",
        "- Add repeated query budgets and multiple attacker sessions.",
    ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
