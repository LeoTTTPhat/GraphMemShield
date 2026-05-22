import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graphmemshield.adapters.langgraph_memory import LangGraphMemoryAdapter
from graphmemshield.core.graph import DynamicMemoryGraph
from graphmemshield.defenses.guard import GraphMemGuard, GraphMemGuardPolicy
from graphmemshield.datasets.synthetic import build_synthetic_multisession_graph


@pytest.mark.skipif(not LangGraphMemoryAdapter.available(), reason="langgraph not installed")
def test_langgraph_memory_adapter_retrieves_through_guard():
    source = build_synthetic_multisession_graph()
    adapter = LangGraphMemoryAdapter(DynamicMemoryGraph())
    adapter.load_graph(source)

    baseline = adapter.retrieve(
        query="arrhythmia",
        requester_session_id="attacker-session",
        max_hops=1,
    )
    guarded = adapter.retrieve(
        query="arrhythmia",
        requester_session_id="attacker-session",
        max_hops=1,
        guard=GraphMemGuard(GraphMemGuardPolicy()),
    )

    assert baseline.cross_session_edge_count > 0
    assert guarded.cross_session_edge_count == 0
