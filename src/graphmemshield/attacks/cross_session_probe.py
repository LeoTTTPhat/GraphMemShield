from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from graphmemshield.core.graph import DynamicMemoryGraph, RetrievalGuard
from graphmemshield.core.types import MemoryEdge, RetrievalResult


@dataclass(frozen=True)
class ProbeReport:
    attacker_session_id: str
    victim_session_id: str
    query_count: int
    retrieved_edge_count: int
    unique_retrieved_edge_count: int
    leaked_edge_count: int
    unique_leaked_edge_count: int
    leakage_event_count: int
    leaked_edge_ids: tuple[str, ...]
    leakage_rate: float
    event_leakage_rate: float
    per_query_leak_rate: float
    results: tuple[RetrievalResult, ...]


class CrossSessionProbe:
    """Measures whether victim-owned graph memory leaks into attacker retrieval."""

    def __init__(self, graph: DynamicMemoryGraph) -> None:
        self.graph = graph

    def run(
        self,
        *,
        attacker_session_id: str,
        victim_session_id: str,
        probe_queries: Iterable[str],
        max_hops: int = 1,
        guard: RetrievalGuard | None = None,
    ) -> ProbeReport:
        results = tuple(
            self.graph.retrieve(
                query,
                attacker_session_id,
                max_hops=max_hops,
                guard=guard,
            )
            for query in probe_queries
        )
        leaked_edges = _unique_edges(
            edge
            for result in results
            for edge in result.edges
            if edge.owner_session_id == victim_session_id
        )
        all_retrieved_edges = tuple(edge for result in results for edge in result.edges)
        unique_retrieved_edges = _unique_edges(all_retrieved_edges)
        leakage_event_count = sum(
            1
            for result in results
            for edge in result.edges
            if edge.owner_session_id == victim_session_id
        )
        queries_with_leak = sum(
            1
            for result in results
            if any(edge.owner_session_id == victim_session_id for edge in result.edges)
        )
        retrieved_edge_count = sum(result.edge_count for result in results)
        leakage_rate = (
            len(leaked_edges) / len(unique_retrieved_edges)
            if unique_retrieved_edges
            else 0.0
        )
        event_leakage_rate = (
            leakage_event_count / retrieved_edge_count if retrieved_edge_count else 0.0
        )
        per_query_leak_rate = (
            queries_with_leak / len(results) if results else 0.0
        )
        return ProbeReport(
            attacker_session_id=attacker_session_id,
            victim_session_id=victim_session_id,
            query_count=len(results),
            retrieved_edge_count=retrieved_edge_count,
            unique_retrieved_edge_count=len(unique_retrieved_edges),
            leaked_edge_count=len(leaked_edges),
            unique_leaked_edge_count=len(leaked_edges),
            leakage_event_count=leakage_event_count,
            leaked_edge_ids=tuple(edge.edge_id for edge in leaked_edges),
            leakage_rate=leakage_rate,
            event_leakage_rate=event_leakage_rate,
            per_query_leak_rate=per_query_leak_rate,
            results=results,
        )


def _unique_edges(edges: Iterable[MemoryEdge]) -> tuple[MemoryEdge, ...]:
    seen: set[str] = set()
    unique: list[MemoryEdge] = []
    for edge in edges:
        if edge.edge_id in seen:
            continue
        seen.add(edge.edge_id)
        unique.append(edge)
    return tuple(unique)
