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

    def infer_without_timestamps(
        self,
        *,
        query: str,
        requester_session_id: str,
        max_hops: int = 1,
        guard: RetrievalGuard | None = None,
    ) -> TemporalPathReport:
        """Infer a plausible write order after removing timestamp access."""

        result = self.graph.retrieve(
            query,
            requester_session_id,
            max_hops=max_hops,
            guard=guard,
        )
        query_terms = tuple(term for term in query.lower().replace("_", " ").split() if term)
        ordered_edges = tuple(
            sorted(
                result.edges,
                key=lambda edge: (
                    _relation_priority(edge.relation),
                    _query_overlap(edge, query_terms),
                    edge.owner_session_id,
                    edge.turn_id or "",
                    edge.edge_id,
                ),
            )
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


def _relation_priority(relation: str) -> int:
    relation = relation.lower()
    priorities = (
        ("visited", "booked", "submitted", "purchased", "works_on"),
        ("has", "takes", "member", "travels"),
        ("diagnosed", "managed", "billed", "located", "for_client"),
    )
    for index, group in enumerate(priorities):
        if any(token in relation for token in group):
            return index
    return len(priorities)


def _query_overlap(edge: MemoryEdge, terms: tuple[str, ...]) -> int:
    haystack = f"{edge.source_id} {edge.relation} {edge.target_id} {edge.sensitivity}".lower()
    return -sum(1 for term in terms if term in haystack)
