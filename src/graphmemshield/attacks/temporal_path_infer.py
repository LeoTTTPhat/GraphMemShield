from __future__ import annotations

from dataclasses import dataclass

from graphmemshield.core.graph import DynamicMemoryGraph, RetrievalGuard
from graphmemshield.core.types import MemoryEdge


@dataclass(frozen=True)
class TemporalPathReport:
    query: str
    requester_session_id: str
    inferred_edge_ids: tuple[str, ...]
    inferred_turn_ids: tuple[str, ...]
    edges: tuple[MemoryEdge, ...]


class TemporalPathInfer:
    """Orders retrieved graph edges by observable write-time metadata.

    This baseline measures timestamp/provenance exposure rather than model-based
    inference capability. Stronger variants should infer paths when timestamps
    are hidden or noisy.
    """

    def __init__(self, graph: DynamicMemoryGraph) -> None:
        self.graph = graph

    def infer(
        self,
        *,
        query: str,
        requester_session_id: str,
        max_hops: int = 1,
        guard: RetrievalGuard | None = None,
    ) -> TemporalPathReport:
        result = self.graph.retrieve(
            query,
            requester_session_id,
            max_hops=max_hops,
            guard=guard,
        )
        ordered_edges = tuple(
            sorted(result.edges, key=lambda edge: (edge.created_at, edge.edge_id))
        )
        turn_ids = tuple(
            edge.turn_id for edge in ordered_edges if edge.turn_id is not None
        )
        return TemporalPathReport(
            query=query,
            requester_session_id=requester_session_id,
            inferred_edge_ids=tuple(edge.edge_id for edge in ordered_edges),
            inferred_turn_ids=turn_ids,
            edges=ordered_edges,
        )
