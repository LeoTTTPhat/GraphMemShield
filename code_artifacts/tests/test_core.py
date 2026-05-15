import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graphmemshield import (
    CrossSessionProbe,
    DynamicMemoryGraph,
    GraphMemGuard,
    GraphMemGuardPolicy,
    MemoryEdge,
    MemoryNode,
)
from graphmemshield.evaluation import leakage_reduction


def build_graph() -> DynamicMemoryGraph:
    graph = DynamicMemoryGraph()
    graph.add_node(MemoryNode("alice", "Alice", owner_session_id="victim"))
    graph.add_node(MemoryNode("clinic", "Heart Clinic"))
    graph.add_node(MemoryNode("condition", "arrhythmia"))
    graph.add_node(MemoryNode("mallory", "Mallory", owner_session_id="attacker"))
    graph.add_edge(
        MemoryEdge(
            edge_id="victim-edge",
            source_id="alice",
            relation="visited",
            target_id="clinic",
            owner_session_id="victim",
            sensitivity="medical",
        )
    )
    graph.add_edge(
        MemoryEdge(
            edge_id="attacker-edge",
            source_id="mallory",
            relation="asked_about",
            target_id="clinic",
            owner_session_id="attacker",
            sensitivity="normal",
        )
    )
    return graph


def test_retrieval_reports_cross_session_edges_without_guard():
    graph = build_graph()
    result = graph.retrieve("clinic", requester_session_id="attacker", max_hops=1)

    assert result.edge_count == 2
    assert result.cross_session_edge_count == 1
    assert result.cross_session_edges[0].edge_id == "victim-edge"


def test_graphmemguard_blocks_sensitive_cross_session_edges():
    graph = build_graph()
    guard = GraphMemGuard(GraphMemGuardPolicy())
    result = graph.retrieve(
        "clinic", requester_session_id="attacker", max_hops=1, guard=guard
    )

    assert result.edge_count == 1
    assert result.edges[0].edge_id == "attacker-edge"
    assert result.cross_session_edge_count == 0


def test_cross_session_probe_measures_leakage_reduction():
    graph = build_graph()
    probe = CrossSessionProbe(graph)
    baseline = probe.run(
        attacker_session_id="attacker",
        victim_session_id="victim",
        probe_queries=["clinic"],
    )
    defended = probe.run(
        attacker_session_id="attacker",
        victim_session_id="victim",
        probe_queries=["clinic"],
        guard=GraphMemGuard(GraphMemGuardPolicy()),
    )

    assert baseline.leaked_edge_count == 1
    assert defended.leaked_edge_count == 0
    assert leakage_reduction(baseline.leaked_edge_count, defended.leaked_edge_count) == 1.0


def test_guard_can_budget_non_sensitive_cross_session_edges():
    graph = DynamicMemoryGraph()
    graph.add_edge(
        MemoryEdge(
            edge_id="shared-edge",
            source_id="topic",
            relation="related_to",
            target_id="public-fact",
            owner_session_id="victim",
            sensitivity="normal",
        )
    )
    guard = GraphMemGuard(
        GraphMemGuardPolicy(
            allow_cross_session=True,
            max_cross_session_edges_per_pair=1,
            blocked_sensitivity_labels=frozenset({"medical"}),
        )
    )

    first = graph.retrieve("topic", requester_session_id="attacker", guard=guard)
    second = graph.retrieve("topic", requester_session_id="attacker", guard=guard)

    assert first.edge_count == 1
    assert second.edge_count == 0
    assert guard.exposure_count("attacker", "victim") == 1


def test_guard_blocks_sensitive_bridge_during_expansion():
    graph = DynamicMemoryGraph()
    graph.add_edge(
        MemoryEdge(
            edge_id="victim-bridge",
            source_id="secret-condition",
            relation="connects_to",
            target_id="shared-clinic",
            owner_session_id="victim",
            sensitivity="medical",
        )
    )
    graph.add_edge(
        MemoryEdge(
            edge_id="public-neighbor",
            source_id="shared-clinic",
            relation="located_in",
            target_id="public-city",
            owner_session_id="public",
            sensitivity="normal",
        )
    )

    guarded = graph.retrieve(
        "secret-condition",
        requester_session_id="attacker",
        max_hops=2,
        guard=GraphMemGuard(GraphMemGuardPolicy()),
    )

    assert guarded.edge_count == 0
