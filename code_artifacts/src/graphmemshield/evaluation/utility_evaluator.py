from __future__ import annotations

from dataclasses import dataclass

from graphmemshield.core.graph import DynamicMemoryGraph, RetrievalGuard
from graphmemshield.core.types import MemoryEdge


@dataclass(frozen=True)
class UtilityReport:
    query: str
    requester_session_id: str
    baseline_non_sensitive_edges: int
    defended_non_sensitive_edges: int
    utility_retention_rate: float


class UtilityEvaluator:
    def __init__(self, baseline_graph: DynamicMemoryGraph) -> None:
        self.baseline_graph = baseline_graph

    def evaluate(
        self,
        *,
        query: str,
        requester_session_id: str,
        defended_graph: DynamicMemoryGraph | None = None,
        guard: RetrievalGuard | None = None,
        max_hops: int = 1,
    ) -> UtilityReport:
        graph_to_query = defended_graph if defended_graph else self.baseline_graph
        
        baseline_result = self.baseline_graph.retrieve(
            query, requester_session_id, max_hops=max_hops, guard=None
        )
        
        defended_result = graph_to_query.retrieve(
            query, requester_session_id, max_hops=max_hops, guard=guard
        )
        
        base_non_sens = len([e for e in baseline_result.edges if e.sensitivity == "normal"])
        defended_non_sens = len([e for e in defended_result.edges if e.sensitivity == "normal"])
        
        retention = defended_non_sens / base_non_sens if base_non_sens > 0 else 1.0
        
        return UtilityReport(
            query=query,
            requester_session_id=requester_session_id,
            baseline_non_sensitive_edges=base_non_sens,
            defended_non_sensitive_edges=defended_non_sens,
            utility_retention_rate=retention
        )
