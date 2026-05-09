from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from typing import Any


@dataclass(frozen=True)
class MemoryNode:
    """Entity node stored by a dynamic application memory graph."""

    node_id: str
    label: str
    node_type: str = "entity"
    owner_session_id: str | None = None
    source_user_id: str | None = None
    created_at: float = field(default_factory=time)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class MemoryEdge:
    """Provenance-aware relation extracted from one memory write."""

    edge_id: str
    source_id: str
    relation: str
    target_id: str
    owner_session_id: str
    source_user_id: str | None = None
    turn_id: str | None = None
    sensitivity: str = "normal"
    created_at: float = field(default_factory=time)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RetrievalResult:
    """Graph retrieval output with enough metadata to audit leakage."""

    query: str
    requester_session_id: str
    edges: tuple[MemoryEdge, ...]
    nodes: tuple[MemoryNode, ...]

    @property
    def cross_session_edges(self) -> tuple[MemoryEdge, ...]:
        return tuple(
            edge
            for edge in self.edges
            if edge.owner_session_id != self.requester_session_id
        )

    @property
    def edge_count(self) -> int:
        return len(self.edges)

    @property
    def cross_session_edge_count(self) -> int:
        return len(self.cross_session_edges)
