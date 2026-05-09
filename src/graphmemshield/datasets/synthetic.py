from __future__ import annotations

from graphmemshield.core.graph import DynamicMemoryGraph
from graphmemshield.core.types import MemoryEdge, MemoryNode


def build_synthetic_multisession_graph() -> DynamicMemoryGraph:
    """Build a tiny graph with repeated user motifs for deterministic tests."""

    graph = DynamicMemoryGraph()
    for node_id, label in [
        ("alice", "Alice"),
        ("alice-alt", "A. Nguyen"),
        ("bob", "Bob"),
        ("clinic", "Heart Clinic"),
        ("condition", "arrhythmia"),
        ("gym", "Gym"),
        ("laptop", "Laptop"),
        ("invoice", "Invoice"),
    ]:
        graph.add_node(MemoryNode(node_id=node_id, label=label))

    edges = [
        MemoryEdge(
            edge_id="alice-s1-e1",
            source_id="alice",
            relation="visited",
            target_id="clinic",
            owner_session_id="alice-session-1",
            source_user_id="alice-user",
            turn_id="t1",
            sensitivity="medical",
            created_at=1.0,
        ),
        MemoryEdge(
            edge_id="alice-s1-e2",
            source_id="clinic",
            relation="diagnosed",
            target_id="condition",
            owner_session_id="alice-session-1",
            source_user_id="alice-user",
            turn_id="t2",
            sensitivity="medical",
            created_at=2.0,
        ),
        MemoryEdge(
            edge_id="alice-s2-e1",
            source_id="alice-alt",
            relation="visited",
            target_id="clinic",
            owner_session_id="alice-session-2",
            source_user_id="alice-user",
            turn_id="t1",
            sensitivity="medical",
            created_at=3.0,
        ),
        MemoryEdge(
            edge_id="alice-s2-e2",
            source_id="clinic",
            relation="diagnosed",
            target_id="condition",
            owner_session_id="alice-session-2",
            source_user_id="alice-user",
            turn_id="t2",
            sensitivity="medical",
            created_at=4.0,
        ),
        MemoryEdge(
            edge_id="bob-s1-e1",
            source_id="bob",
            relation="visited",
            target_id="gym",
            owner_session_id="bob-session-1",
            source_user_id="bob-user",
            turn_id="t1",
            sensitivity="normal",
            created_at=5.0,
        ),
        MemoryEdge(
            edge_id="bob-s1-e2",
            source_id="bob",
            relation="purchased",
            target_id="laptop",
            owner_session_id="bob-session-1",
            source_user_id="bob-user",
            turn_id="t2",
            sensitivity="financial",
            created_at=6.0,
        ),
        MemoryEdge(
            edge_id="bob-s1-e3",
            source_id="laptop",
            relation="has_record",
            target_id="invoice",
            owner_session_id="bob-session-1",
            source_user_id="bob-user",
            turn_id="t3",
            sensitivity="financial",
            created_at=7.0,
        ),
    ]
    for edge in edges:
        graph.add_edge(edge)
    return graph
