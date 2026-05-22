from __future__ import annotations

from dataclasses import dataclass, field

from graphmemshield.core.types import MemoryEdge


@dataclass(frozen=True)
class GraphMemGuardPolicy:
    """Retrieval-time policy for provenance-aware graph memory isolation."""

    allow_cross_session: bool = False
    max_cross_session_edges_per_pair: int = 0
    budget_scope: str = "requester_owner"
    blocked_sensitivity_labels: frozenset[str] = field(
        default_factory=lambda: frozenset({"secret", "medical", "financial"})
    )


class GraphMemGuard:
    """Blocks or budgets graph edges before they enter the context."""

    def __init__(self, policy: GraphMemGuardPolicy | None = None) -> None:
        self.policy = policy or GraphMemGuardPolicy()
        self._admitted_edges: dict[tuple[str, str], set[str]] = {}

    def allow_edge(self, edge: MemoryEdge, requester_session_id: str) -> bool:
        if edge.owner_session_id == requester_session_id:
            return True

        if edge.sensitivity in self.policy.blocked_sensitivity_labels:
            return False

        if not self.policy.allow_cross_session:
            return False

        key = self._budget_key(requester_session_id, edge.owner_session_id)
        admitted = self._admitted_edges.get(key, set())
        return (
            edge.edge_id in admitted
            or len(admitted) < self.policy.max_cross_session_edges_per_pair
        )

    def record_exposure(self, edge: MemoryEdge, requester_session_id: str) -> None:
        if edge.owner_session_id == requester_session_id:
            return
        key = self._budget_key(requester_session_id, edge.owner_session_id)
        self._admitted_edges.setdefault(key, set()).add(edge.edge_id)

    def exposure_count(self, requester_session_id: str, victim_session_id: str) -> int:
        key = self._budget_key(requester_session_id, victim_session_id)
        return len(self._admitted_edges.get(key, set()))

    def _budget_key(self, requester_session_id: str, owner_session_id: str) -> tuple[str, str]:
        if self.policy.budget_scope == "owner":
            return ("*", owner_session_id)
        return (requester_session_id, owner_session_id)
