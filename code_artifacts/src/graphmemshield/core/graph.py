from __future__ import annotations

from collections import defaultdict, deque
from typing import Iterable, Protocol

from graphmemshield.core.types import MemoryEdge, MemoryNode, RetrievalResult


class RetrievalGuard(Protocol):
    def allow_edge(self, edge: MemoryEdge, requester_session_id: str) -> bool:
        ...

    def record_exposure(self, edge: MemoryEdge, requester_session_id: str) -> None:
        ...


class DynamicMemoryGraph:
    """Small in-memory KG store for repeatable privacy experiments."""

    def __init__(self) -> None:
        self._nodes: dict[str, MemoryNode] = {}
        self._edges: dict[str, MemoryEdge] = {}
        self._adjacency: dict[str, set[str]] = defaultdict(set)

    @property
    def nodes(self) -> tuple[MemoryNode, ...]:
        return tuple(self._nodes.values())

    @property
    def edges(self) -> tuple[MemoryEdge, ...]:
        return tuple(self._edges.values())

    def get_node(self, node_id: str) -> MemoryNode | None:
        return self._nodes.get(node_id)

    def get_edge(self, edge_id: str) -> MemoryEdge | None:
        return self._edges.get(edge_id)

    def add_node(self, node: MemoryNode) -> None:
        self._nodes[node.node_id] = node

    def add_edge(self, edge: MemoryEdge) -> None:
        if edge.source_id not in self._nodes:
            self.add_node(MemoryNode(node_id=edge.source_id, label=edge.source_id))
        if edge.target_id not in self._nodes:
            self.add_node(MemoryNode(node_id=edge.target_id, label=edge.target_id))

        self._edges[edge.edge_id] = edge
        self._adjacency[edge.source_id].add(edge.edge_id)
        self._adjacency[edge.target_id].add(edge.edge_id)

    def retrieve(
        self,
        query: str,
        requester_session_id: str,
        *,
        max_hops: int = 1,
        guard: RetrievalGuard | None = None,
    ) -> RetrievalResult:
        """Retrieve matching graph edges and optionally expand by k-hop topology."""

        terms = _normalize_terms(query)
        seed_edge_ids = {
            edge.edge_id
            for edge in self._edges.values()
            if _edge_matches(edge, self._nodes, terms)
            and _guard_allows(edge, requester_session_id, guard)
        }
        selected_edge_ids = self._expand_edges(
            seed_edge_ids,
            max_hops=max_hops,
            requester_session_id=requester_session_id,
            guard=guard,
        )

        visible_edges: list[MemoryEdge] = []
        node_ids: set[str] = set()
        for edge_id in sorted(selected_edge_ids):
            edge = self._edges[edge_id]
            if not _guard_allows(edge, requester_session_id, guard):
                continue
            visible_edges.append(edge)
            node_ids.add(edge.source_id)
            node_ids.add(edge.target_id)
            if guard is not None:
                guard.record_exposure(edge, requester_session_id)

        nodes = tuple(self._nodes[node_id] for node_id in sorted(node_ids))
        return RetrievalResult(
            query=query,
            requester_session_id=requester_session_id,
            edges=tuple(visible_edges),
            nodes=nodes,
        )

    def edges_by_session(self, session_id: str) -> tuple[MemoryEdge, ...]:
        return tuple(
            edge for edge in self._edges.values() if edge.owner_session_id == session_id
        )

    def _expand_edges(
        self,
        seed_edge_ids: Iterable[str],
        *,
        max_hops: int,
        requester_session_id: str,
        guard: RetrievalGuard | None,
    ) -> set[str]:
        if max_hops <= 0:
            return set(seed_edge_ids)

        selected: set[str] = set(seed_edge_ids)
        queue: deque[tuple[str, int]] = deque()
        for edge_id in seed_edge_ids:
            edge = self._edges[edge_id]
            queue.append((edge.source_id, 0))
            queue.append((edge.target_id, 0))

        visited_nodes: set[tuple[str, int]] = set()
        while queue:
            node_id, depth = queue.popleft()
            if (node_id, depth) in visited_nodes:
                continue
            visited_nodes.add((node_id, depth))
            if depth >= max_hops:
                continue

            for edge_id in self._adjacency.get(node_id, set()):
                edge = self._edges[edge_id]
                if not _guard_allows(edge, requester_session_id, guard):
                    continue
                selected.add(edge_id)
                neighbor = edge.target_id if edge.source_id == node_id else edge.source_id
                queue.append((neighbor, depth + 1))

        return selected


def _normalize_terms(query: str) -> tuple[str, ...]:
    return tuple(term for term in query.lower().replace("_", " ").split() if term)


def _edge_matches(
    edge: MemoryEdge, nodes: dict[str, MemoryNode], terms: tuple[str, ...]
) -> bool:
    if not terms:
        return False

    source = nodes.get(edge.source_id)
    target = nodes.get(edge.target_id)
    haystack = " ".join(
        [
            edge.relation,
            edge.source_id,
            edge.target_id,
            source.label if source else "",
            target.label if target else "",
            edge.sensitivity,
        ]
    ).lower()
    return any(term in haystack for term in terms)


def _guard_allows(
    edge: MemoryEdge,
    requester_session_id: str,
    guard: RetrievalGuard | None,
) -> bool:
    return guard is None or guard.allow_edge(edge, requester_session_id)
