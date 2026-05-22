import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graphmemshield import (
    CrossSessionProbe,
    GraphMemGuard,
    GraphMemGuardPolicy,
    LearnedSessionGraphLink,
    SessionGraphLink,
    TemporalPathInfer,
    build_synthetic_multisession_graph,
)
from graphmemshield.evaluation import ordering_accuracy, top_k_hit


def test_session_graph_link_ranks_same_user_session_first_structure_only():
    graph = build_synthetic_multisession_graph()
    linker = SessionGraphLink(graph)

    report = linker.rank(
        query_session_id="alice-session-1",
        candidate_session_ids=("alice-session-2", "bob-session-1"),
        include_semantic_labels=False,
    )

    ranked_ids = tuple(candidate.session_id for candidate in report.candidates)
    assert report.top_session_id == "alice-session-2"
    assert top_k_hit(ranked_ids, "alice-session-2", k=1)
    assert report.candidates[0].score > report.candidates[1].score


def test_session_graph_link_supports_stronger_similarity_methods():
    graph = build_synthetic_multisession_graph()
    linker = SessionGraphLink(graph)

    for method in ("wl_kernel", "graph_edit", "embedding"):
        report = linker.rank(
            query_session_id="alice-session-1",
            candidate_session_ids=("alice-session-2", "bob-session-1"),
            include_semantic_labels=(method == "embedding"),
            method=method,
        )
        assert report.candidates
        assert 0.0 <= report.candidates[0].score <= 1.0


def test_learned_session_graph_link_trains_and_ranks():
    graph = build_synthetic_multisession_graph()
    linker = LearnedSessionGraphLink(graph, include_semantic_labels=True).fit()

    report = linker.rank(
        query_session_id="alice-session-1",
        candidate_session_ids=("alice-session-2", "bob-session-1"),
    )

    assert report.candidates
    assert report.top_session_id == "alice-session-2"
    assert 0.0 <= report.candidates[0].score <= 1.0


def test_temporal_path_infer_orders_retrieved_edges_by_write_time():
    graph = build_synthetic_multisession_graph()
    infer = TemporalPathInfer(graph)

    report = infer.infer(
        query="arrhythmia",
        requester_session_id="attacker-session",
        max_hops=1,
    )

    assert report.inferred_edge_ids[:2] == ("alice-s1-e1", "alice-s1-e2")
    assert ordering_accuracy(
        report.inferred_edge_ids[:2], ("alice-s1-e1", "alice-s1-e2")
    ) == 1.0


def test_temporal_path_infer_respects_graphmemguard():
    graph = build_synthetic_multisession_graph()
    infer = TemporalPathInfer(graph)
    guard = GraphMemGuard(GraphMemGuardPolicy())

    report = infer.infer(
        query="arrhythmia",
        requester_session_id="attacker-session",
        max_hops=1,
        guard=guard,
    )

    assert report.inferred_edge_ids == ()


def test_temporal_path_infer_without_timestamps_returns_retrieved_edges():
    graph = build_synthetic_multisession_graph()
    infer = TemporalPathInfer(graph)

    report = infer.infer_without_timestamps(
        query="arrhythmia",
        requester_session_id="attacker-session",
        max_hops=1,
    )

    assert set(report.inferred_edge_ids) == {"alice-s1-e1", "alice-s1-e2", "alice-s2-e1", "alice-s2-e2"}


def test_cross_session_probe_reports_event_and_unique_rates():
    graph = build_synthetic_multisession_graph()
    probe = CrossSessionProbe(graph)

    report = probe.run(
        attacker_session_id="attacker-session",
        victim_session_id="alice-session-1",
        probe_queries=["arrhythmia", "arrhythmia"],
        max_hops=1,
    )

    assert report.unique_leaked_edge_count == report.leaked_edge_count
    assert report.leakage_event_count >= report.unique_leaked_edge_count
    assert 0.0 <= report.event_leakage_rate <= 1.0
    assert report.per_query_leak_rate == 1.0


def test_adaptive_cross_session_probe_expands_from_observed_edges():
    graph = build_synthetic_multisession_graph()
    probe = CrossSessionProbe(graph)

    report = probe.run_adaptive(
        attacker_session_id="attacker-session",
        victim_session_id="alice-session-1",
        seed_queries=("clinic",),
        query_budget=3,
        max_hops=1,
    )

    assert report.query_count <= 3
    assert report.leaked_edge_count >= 1
