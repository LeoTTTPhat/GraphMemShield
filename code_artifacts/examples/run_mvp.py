import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graphmemshield import (  # noqa: E402
    CrossSessionProbe,
    DynamicMemoryGraph,
    GraphMemGuard,
    GraphMemGuardPolicy,
    MemoryEdge,
    MemoryNode,
    SessionGraphLink,
    TemporalPathInfer,
    build_synthetic_multisession_graph,
)
from graphmemshield.evaluation import leakage_reduction, top_k_hit  # noqa: E402


def build_demo_graph() -> DynamicMemoryGraph:
    graph = DynamicMemoryGraph()
    graph.add_node(MemoryNode("alice", "Alice", owner_session_id="victim-session"))
    graph.add_node(MemoryNode("clinic", "Cardiology Clinic"))
    graph.add_node(MemoryNode("condition", "arrhythmia"))
    graph.add_node(MemoryNode("bob", "Bob", owner_session_id="attacker-session"))

    graph.add_edge(
        MemoryEdge(
            edge_id="e1",
            source_id="alice",
            relation="visited",
            target_id="clinic",
            owner_session_id="victim-session",
            source_user_id="victim-user",
            sensitivity="medical",
        )
    )
    graph.add_edge(
        MemoryEdge(
            edge_id="e2",
            source_id="clinic",
            relation="treats",
            target_id="condition",
            owner_session_id="victim-session",
            source_user_id="victim-user",
            sensitivity="medical",
        )
    )
    graph.add_edge(
        MemoryEdge(
            edge_id="e3",
            source_id="bob",
            relation="asked_about",
            target_id="clinic",
            owner_session_id="attacker-session",
            source_user_id="attacker-user",
            sensitivity="normal",
        )
    )
    return graph


def main() -> None:
    graph = build_demo_graph()
    probe = CrossSessionProbe(graph)
    queries = ["clinic", "arrhythmia", "visited cardiology"]

    baseline = probe.run(
        attacker_session_id="attacker-session",
        victim_session_id="victim-session",
        probe_queries=queries,
        max_hops=1,
    )

    guard = GraphMemGuard(GraphMemGuardPolicy())
    defended = probe.run(
        attacker_session_id="attacker-session",
        victim_session_id="victim-session",
        probe_queries=queries,
        max_hops=1,
        guard=guard,
    )

    print("GraphMemShield MVP")
    print(f"baseline leaked edges: {baseline.leaked_edge_ids}")
    print(f"defended leaked edges: {defended.leaked_edge_ids}")
    print(
        "leakage reduction: "
        f"{leakage_reduction(baseline.leaked_edge_count, defended.leaked_edge_count):.2f}"
    )

    synthetic = build_synthetic_multisession_graph()
    link_report = SessionGraphLink(synthetic).rank(
        query_session_id="alice-session-1",
        candidate_session_ids=("alice-session-2", "bob-session-1"),
    )
    ranked_ids = tuple(candidate.session_id for candidate in link_report.candidates)
    temporal_report = TemporalPathInfer(synthetic).infer(
        query="arrhythmia",
        requester_session_id="attacker-session",
        max_hops=1,
    )
    print(f"session-link top candidate: {link_report.top_session_id}")
    print(f"session-link top-1 hit: {top_k_hit(ranked_ids, 'alice-session-2', k=1)}")
    print(f"temporal path edges: {temporal_report.inferred_edge_ids}")


if __name__ == "__main__":
    main()
