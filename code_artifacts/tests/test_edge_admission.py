import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graphmemshield import (
    EdgeAdmissionPolicy,
    FixedUniverseRandomizedResponseAdmission,
    RandomizedEdgeAdmission,
    build_synthetic_multisession_graph,
)
from graphmemshield.core.types import MemoryEdge


def test_sensitive_keep_probability_increases_with_epsilon():
    low = EdgeAdmissionPolicy(epsilon=0.1).sensitive_keep_probability
    high = EdgeAdmissionPolicy(epsilon=3.0).sensitive_keep_probability

    assert 0.5 < low < high < 1.0


def test_randomized_edge_admission_is_deterministic_for_seed():
    graph = build_synthetic_multisession_graph()
    first = RandomizedEdgeAdmission(
        EdgeAdmissionPolicy(epsilon=1.0, seed="fixed")
    ).filter_graph(graph)
    second = RandomizedEdgeAdmission(
        EdgeAdmissionPolicy(epsilon=1.0, seed="fixed")
    ).filter_graph(graph)

    assert tuple(edge.edge_id for edge in first.edges) == tuple(
        edge.edge_id for edge in second.edges
    )


def test_fixed_universe_randomized_response_can_emit_absent_edges():
    graph = build_synthetic_multisession_graph()
    absent = MemoryEdge(
        edge_id="absent-medical-edge",
        source_id="alice",
        relation="has_condition",
        target_id="condition",
        owner_session_id="alice-session-1",
        source_user_id="alice-user",
        sensitivity="medical",
    )
    released = FixedUniverseRandomizedResponseAdmission(
        EdgeAdmissionPolicy(epsilon=0.1, seed=1),
        candidate_edges=(absent,),
    ).filter_graph(graph)

    assert any(edge.metadata.get("dp_synthetic") for edge in released.edges)
