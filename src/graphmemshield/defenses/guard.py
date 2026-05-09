from __future__ import annotations

from dataclasses import dataclass, field

from graphmemshield.core.types import MemoryEdge


@dataclass(frozen=True)
class GraphMemGuardPolicy:
    """Retrieval-time policy for provenance-aware graph memory isolation."""

    allow_cross_session: bool = False
    max_cross_session_edges_per_pair: int = 0
    blocked_sensitivity_labels: frozenset[str] = field(
        default_factory=lambda: frozenset({"secret", "medical", "financial"})
    )


class GraphMemGuard:
    """Blocks or budgets graph edges before they enter the context."""

    def __init__(self, policy: GraphMemGuardPolicy | None = None) -> None:
        self.policy = policy or GraphMemGuardPolicy()
        self._exposure_counts: dict[tuple[str, str], int] = {}

    def allow_edge(self, edge: MemoryEdge, requester_session_id: str) -> bool:
        if edge.owner_session_id == requester_session_id:
            return True

        if edge.sensitivity in self.policy.blocked_sensitivity_labels:
            return False

        if not self.policy.allow_cross_session:
            return False

        pair = (requester_session_id, edge.owner_session_id)
        current = self._exposure_counts.get(pair, 0)
        return current < self.policy.max_cross_session_edges_per_pair

    def record_exposure(self, edge: MemoryEdge, requester_session_id: str) -> None:
        if edge.owner_session_id == requester_session_id:
            return
        pair = (requester_session_id, edge.owner_session_id)
        self._exposure_counts[pair] = self._exposure_counts.get(pair, 0) + 1

    def exposure_count(self, requester_session_id: str, victim_session_id: str) -> int:
        return self._exposure_counts.get((requester_session_id, victim_session_id), 0)
