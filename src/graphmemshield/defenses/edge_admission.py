from __future__ import annotations

import random
from dataclasses import dataclass
from math import exp

from graphmemshield.core.graph import DynamicMemoryGraph
from graphmemshield.core.types import MemoryEdge


@dataclass(frozen=True)
class EdgeAdmissionPolicy:
    """Write-time edge admission policy based on Differential Privacy (Randomized Response)."""

    epsilon: float
    protected_sensitivity_labels: frozenset[str] = frozenset(
        {"secret", "medical", "financial"}
    )
    seed: int | None = None

    @property
    def sensitive_keep_probability(self) -> float:
        """Probability to keep a sensitive edge based on epsilon."""
        if self.epsilon <= 0:
            return 0.5
        return exp(self.epsilon) / (1.0 + exp(self.epsilon))


class RandomizedEdgeAdmission:
    """Formal epsilon-edge Differential Privacy mechanism via Randomized Response.
    
    Adjacency definition: Two memory graphs G and G' are adjacent if they differ 
    by exactly one sensitive edge. For a sensitive edge, the mechanism admits it
    with probability p = exp(epsilon) / (1 + exp(epsilon)) and suppresses it with 
    probability 1 - p. This satisfies epsilon-edge-DP.
    """

    def __init__(self, policy: EdgeAdmissionPolicy) -> None:
        self.policy = policy
        self._rng = random.Random(self.policy.seed)

    def admit(self, edge: MemoryEdge) -> bool:
        """Decide whether to admit an edge."""
        if edge.sensitivity not in self.policy.protected_sensitivity_labels:
            return True
        return self._rng.random() <= self.policy.sensitive_keep_probability

    def filter_graph(self, graph: DynamicMemoryGraph) -> DynamicMemoryGraph:
        """Filter the entire graph based on the DP mechanism."""
        admitted = DynamicMemoryGraph()
        for node in graph.nodes:
            admitted.add_node(node)
        for edge in graph.edges:
            if self.admit(edge):
                admitted.add_edge(edge)
        return admitted
