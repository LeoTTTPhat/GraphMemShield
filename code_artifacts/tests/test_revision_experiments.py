import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graphmemshield.adapters.sqlite_property_graph import SQLitePropertyGraphAdapter
from graphmemshield.adapters.kuzu_property_graph import KuzuPropertyGraphAdapter
from graphmemshield.datasets.dialogue import dialogue_records_to_graph
from graphmemshield.datasets.enterprise import build_enterprise_health_finance_records
from graphmemshield.evaluation.blackbox import (
    EvidenceDumpResponseGenerator,
    LocalAbstractiveResponseGenerator,
    ResponseLeakageScorer,
    SemanticResponseLeakageScorer,
    TemplateResponseGenerator,
)
from graphmemshield.defenses.privacy_accounting import (
    CompositionReport,
    FullGraphReleasePrivacyReport,
    randomized_response_privacy_loss,
)
from graphmemshield.datasets.public_ingest import load_enron_maildir, load_multiwoz_dialogues
from graphmemshield.evaluation.statistics import ci95
from graphmemshield import CrossSessionProbe, GraphMemGuard, GraphMemGuardPolicy
from graphmemshield.core.graph import DynamicMemoryGraph
from graphmemshield.core.types import MemoryEdge


def test_enterprise_generator_builds_larger_graph():
    records = build_enterprise_health_finance_records(
        num_users=4, sessions_per_user=2, turns_per_session=2
    )
    graph = dialogue_records_to_graph(records)

    assert len(records) == 16
    assert len(graph.edges) == 64


def test_sqlite_property_graph_round_trips(tmp_path):
    graph = dialogue_records_to_graph(
        build_enterprise_health_finance_records(
            num_users=2, sessions_per_user=1, turns_per_session=1
        )
    )
    adapter = SQLitePropertyGraphAdapter(tmp_path / "graph.sqlite")
    adapter.write_graph(graph)
    loaded = adapter.read_graph()

    assert len(loaded.nodes) == len(graph.nodes)
    assert len(loaded.edges) == len(graph.edges)


def test_kuzu_property_graph_round_trips_when_available(tmp_path):
    if not KuzuPropertyGraphAdapter.available():
        return
    graph = dialogue_records_to_graph(
        build_enterprise_health_finance_records(
            num_users=2, sessions_per_user=1, turns_per_session=1
        )
    )
    adapter = KuzuPropertyGraphAdapter(tmp_path / "kuzu_graph")
    adapter.write_graph(graph)
    loaded = adapter.read_graph()

    assert len(loaded.nodes) == len(graph.nodes)
    assert len(loaded.edges) == len(graph.edges)


def test_blackbox_response_leakage_scorer_detects_victim_terms():
    graph = dialogue_records_to_graph(
        build_enterprise_health_finance_records(
            num_users=2, sessions_per_user=1, turns_per_session=1
        )
    )
    victim_edges = graph.edges_by_session("ehf-user-000-session-1")
    secret_term = next(
        token
        for edge in victim_edges
        if edge.sensitivity != "normal"
        for token in edge.target_id.replace("-", " ").split()
        if len(token) >= 4
    )
    result = graph.retrieve(secret_term, "attacker", max_hops=1)
    response = TemplateResponseGenerator().generate(result)

    report = ResponseLeakageScorer().score(
        response_text=response,
        victim_edges=victim_edges,
        secret_terms=(secret_term,),
    )

    assert report.leaked_secret_term_count >= 1


def test_local_abstractive_generator_returns_response_text():
    graph = dialogue_records_to_graph(
        build_enterprise_health_finance_records(
            num_users=2, sessions_per_user=1, turns_per_session=1
        )
    )
    result = graph.retrieve("clinic", "attacker", max_hops=1)

    assert LocalAbstractiveResponseGenerator().generate(result)


def test_multiwoz_ingestion_accepts_common_json_shape(tmp_path):
    path = tmp_path / "multiwoz.json"
    path.write_text(
        '{"dlg-1": {"log": [{"text": "book hotel", "metadata": {"hotel": {"semi": {"area": "north", "pricerange": "cheap"}, "book": {}}}}]}}',
        encoding="utf-8",
    )

    records = load_multiwoz_dialogues(path)

    assert len(records) == 1
    assert len(records[0].relations) == 2


def test_enron_ingestion_accepts_maildir_message(tmp_path):
    message = tmp_path / "msg1"
    message.write_text(
        "From: alice@example.com\nTo: bob@example.com\nSubject: Confidential settlement\nDate: Mon, 1 Jan 2001 00:00:00 -0000\n\nBody",
        encoding="utf-8",
    )

    records = load_enron_maildir(tmp_path)

    assert len(records) == 1
    assert any(relation.sensitivity == "secret" for relation in records[0].relations)


def test_ci95_reports_mean_and_interval():
    report = ci95([1.0, 2.0, 3.0])

    assert report.n == 3
    assert report.ci95_low < report.mean < report.ci95_high


def test_multihop_retrieval_expands_at_least_one_hop():
    graph = dialogue_records_to_graph(
        build_enterprise_health_finance_records(
            num_users=4, sessions_per_user=2, turns_per_session=2
        )
    )
    one_hop = CrossSessionProbe(graph).run(
        attacker_session_id="ehf-user-001-session-1",
        victim_session_id="ehf-user-000-session-1",
        probe_queries=("arrhythmia", "CloudVendor"),
        max_hops=1,
    )
    two_hop = CrossSessionProbe(graph).run(
        attacker_session_id="ehf-user-001-session-1",
        victim_session_id="ehf-user-000-session-1",
        probe_queries=("arrhythmia", "CloudVendor"),
        max_hops=2,
    )

    assert two_hop.unique_retrieved_edge_count >= one_hop.unique_retrieved_edge_count


def test_hybrid_pipeline_components_work_together():
    graph = dialogue_records_to_graph(
        build_enterprise_health_finance_records(
            num_users=4, sessions_per_user=2, turns_per_session=2
        )
    )
    guard = GraphMemGuard(
        GraphMemGuardPolicy(
            allow_cross_session=True,
            max_cross_session_edges_per_pair=2,
            blocked_sensitivity_labels=frozenset({"medical", "financial", "secret"}),
        )
    )
    probe_report = CrossSessionProbe(graph).run_adaptive(
        attacker_session_id="ehf-user-001-session-1",
        victim_session_id="ehf-user-000-session-1",
        seed_queries=("arrhythmia",),
        query_budget=3,
        max_hops=2,
        guard=guard,
    )
    response = "\n".join(
        LocalAbstractiveResponseGenerator().generate(result)
        for result in probe_report.results
    )
    victim_edges = graph.edges_by_session("ehf-user-000-session-1")
    report = ResponseLeakageScorer().score(
        response_text=response,
        victim_edges=victim_edges,
        secret_terms=("arrhythmia",),
    )

    assert probe_report.query_count <= 3
    assert report.leaked_edge_count <= len(victim_edges)


def test_sensitivity_provenance_error_increases_bounded_exposure():
    graph = dialogue_records_to_graph(
        build_enterprise_health_finance_records(
            num_users=4, sessions_per_user=2, turns_per_session=2
        )
    )
    victim_session = "ehf-user-000-session-1"
    corrupted = DynamicMemoryGraph()
    corrupted_one = False
    for node in graph.nodes:
        corrupted.add_node(node)
    for edge in graph.edges:
        if (
            not corrupted_one
            and edge.owner_session_id == victim_session
            and edge.sensitivity != "normal"
            and "diabetes" in edge.target_id
        ):
            edge = MemoryEdge(
                edge_id=edge.edge_id,
                source_id=edge.source_id,
                relation=edge.relation,
                target_id=edge.target_id,
                owner_session_id=edge.owner_session_id,
                source_user_id=edge.source_user_id,
                turn_id=edge.turn_id,
                sensitivity="normal",
                created_at=edge.created_at,
                metadata={"provenance_error": "sensitivity_downgraded"},
            )
            corrupted_one = True
        corrupted.add_edge(edge)

    guard = GraphMemGuard(
        GraphMemGuardPolicy(
            allow_cross_session=True,
            max_cross_session_edges_per_pair=5,
            blocked_sensitivity_labels=frozenset({"medical", "financial", "secret"}),
        )
    )
    report = CrossSessionProbe(corrupted).run(
        attacker_session_id="ehf-user-001-session-1",
        victim_session_id=victim_session,
        probe_queries=("diabetes",),
        max_hops=2,
        guard=guard,
    )

    assert corrupted_one
    assert report.leaked_edge_count >= 1


def test_evidence_dump_generator_is_scored_as_blackbox_leakage():
    graph = dialogue_records_to_graph(
        build_enterprise_health_finance_records(
            num_users=2, sessions_per_user=1, turns_per_session=1
        )
    )
    result = graph.retrieve("diabetes", "ehf-user-001-session-1", max_hops=1)
    response = EvidenceDumpResponseGenerator().generate(result)
    victim_edges = graph.edges_by_session("ehf-user-000-session-1")
    report = ResponseLeakageScorer().score(
        response_text=response,
        victim_edges=victim_edges,
        secret_terms=("diabetes",),
    )

    assert report.leaked_edge_count >= 1


def test_privacy_accounting_matches_randomized_response_epsilon():
    assert round(randomized_response_privacy_loss(1.0), 6) == 1.0
    assert CompositionReport(per_release_epsilon=0.5, release_count=10).composed_epsilon == 5.0


def test_semantic_response_scorer_detects_alias_leakage():
    graph = dialogue_records_to_graph(
        build_enterprise_health_finance_records(
            num_users=2, sessions_per_user=1, turns_per_session=1
        )
    )
    victim_edges = graph.edges_by_session("ehf-user-000-session-1")
    response = "The private health topic involved a clinic and condition."
    report = SemanticResponseLeakageScorer(similarity_threshold=0.2).score(
        response_text=response,
        victim_edges=victim_edges,
        secret_terms=("medical",),
    )

    assert report.semantic_edge_count >= report.leaked_edge_count


def test_full_graph_privacy_scope_flags_unprotected_release():
    scoped = FullGraphReleasePrivacyReport(
        per_edge_epsilon=1.0,
        protected_candidate_edges=10,
        unprotected_released_edges=2,
        release_count=3,
    )
    full = FullGraphReleasePrivacyReport(
        per_edge_epsilon=1.0,
        protected_candidate_edges=12,
        unprotected_released_edges=0,
        release_count=3,
    )

    assert scoped.guarantee_scope == "protected_candidate_edges_only"
    assert not scoped.has_full_graph_dp
    assert scoped.protected_release_epsilon == 30.0
    assert full.guarantee_scope == "full_graph_over_candidate_universe"
