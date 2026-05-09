import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graphmemshield.adapters import PrivacyGuardGraphBuilder, build_seed_documents
from graphmemshield.adapters.privacyguard import _timestamp_to_float


def test_privacyguard_seed_documents_build_graph_edges():
    docs = build_seed_documents()
    records_by_user = {
        "graphmem-alice": [doc for doc in docs if doc["userId"] == "graphmem-alice"],
        "graphmem-bob": [doc for doc in docs if doc["userId"] == "graphmem-bob"],
    }

    graph = PrivacyGuardGraphBuilder().build(records_by_user)

    assert len(graph.nodes) > 0
    assert len(graph.edges) > 0
    assert graph.edges_by_session("alice-session-1")
    assert any(edge.relation == "has_condition" for edge in graph.edges)
    assert any(edge.sensitivity == "medical" for edge in graph.edges)


def test_privacyguard_timestamp_parser_accepts_ejson_date_dict():
    parsed = _timestamp_to_float({"$date": "2026-05-09T02:00:00.000Z"}, 7)

    assert parsed == 20260509020000.0


def test_privacyguard_timestamp_parser_accepts_plain_date_dict():
    parsed = _timestamp_to_float({"date": "2026-05-09T02:00:00.000Z"}, 7)

    assert parsed == 20260509020000.0
