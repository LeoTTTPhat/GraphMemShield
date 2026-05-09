from __future__ import annotations

import hashlib
from dataclasses import dataclass
from math import exp

from graphmemshield.core.graph import DynamicMemoryGraph
from graphmemshield.core.types import MemoryEdge


@dataclass(frozen=True)
class EdgeAdmissionPolicy:
    """Seeded write-time edge admission policy for sensitivity experiments."""

    epsilon: float
    protected_sensitivity_labels: frozenset[str] = frozenset(
        {"secret", "medical", "financial"}
    )
    seed: str = "graphmemshield"

    @property
    def sensitive_keep_probability(self) -> float:
        if self.epsilon <= 0:
            return 0.5
        return exp(self.epsilon) / (1.0 + exp(self.epsilon))


class RandomizedEdgeAdmission:
    """Deterministic proxy for edge-admission experiments.

    This class is not a formal differentially private mechanism. It exists to
    stress-test write-time edge suppression until adjacency definitions,
    accounting, and composition proofs are added.
    """

    def __init__(self, policy: EdgeAdmissionPolicy) -> None:
        self.policy = policy

    def admit(self, edge: MemoryEdge) -> bool:
        if edge.sensitivity not in self.policy.protected_sensitivity_labels:
            return True
        return self._score(edge.edge_id) <= self.policy.sensitive_keep_probability

    def filter_graph(self, graph: DynamicMemoryGraph) -> DynamicMemoryGraph:
        admitted = DynamicMemoryGraph()
        for node in graph.nodes:
            admitted.add_node(node)
        for edge in graph.edges:
            if self.admit(edge):
                admitted.add_edge(edge)
        return admitted

    def _score(self, edge_id: str) -> float:
        digest = hashlib.sha256(f"{self.policy.seed}:{edge_id}".encode()).digest()
        value = int.from_bytes(digest[:8], "big")
        return value / float(2**64 - 1)
