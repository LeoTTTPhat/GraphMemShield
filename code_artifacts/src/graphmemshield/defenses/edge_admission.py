from __future__ import annotations

import random
from dataclasses import dataclass
from math import exp
from typing import Iterable

from graphmemshield.core.graph import DynamicMemoryGraph
from graphmemshield.core.types import MemoryEdge


@dataclass(frozen=True)
class EdgeAdmissionPolicy:
    """Seeded write-time edge admission policy for utility/leakage sweeps."""

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
    """One-sided sensitive-edge suppression heuristic.

    This class intentionally does not claim edge differential privacy. It only
    randomizes whether present sensitive edges are retained; absent edges are not
    randomized over a public universe, so outputs containing a present edge can
    have zero probability under an adjacent graph where that edge is absent.
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


class FixedUniverseRandomizedResponseAdmission:
    """Edge-DP randomized response over a fixed candidate edge universe."""

    def __init__(
        self,
        policy: EdgeAdmissionPolicy,
        *,
        candidate_edges: Iterable[MemoryEdge],
    ) -> None:
        self.policy = policy
        self.candidate_edges = tuple(candidate_edges)
        self._rng = random.Random(self.policy.seed)

    @property
    def absent_edge_emit_probability(self) -> float:
        return 1.0 / (1.0 + exp(max(self.policy.epsilon, 0.0)))

    def filter_graph(self, graph: DynamicMemoryGraph) -> DynamicMemoryGraph:
        """Release a graph with randomized sensitive edge presence bits.

        For each protected candidate edge, present bits are emitted with
        e^epsilon/(1+e^epsilon), while absent bits are emitted with
        1/(1+e^epsilon). This is standard randomized response over a fixed
        edge universe and gives epsilon-DP for each protected edge bit.
        """

        present = {edge.edge_id: edge for edge in graph.edges}
        candidate_ids = {edge.edge_id for edge in self.candidate_edges}
        released = DynamicMemoryGraph()
        for node in graph.nodes:
            released.add_node(node)

        for edge in graph.edges:
            if edge.edge_id in candidate_ids and _is_protected(edge, self.policy):
                continue
            released.add_edge(edge)

        for candidate in self.candidate_edges:
            if not _is_protected(candidate, self.policy):
                if candidate.edge_id in present:
                    released.add_edge(candidate)
                continue

            is_present = candidate.edge_id in present
            emit_probability = (
                self.policy.sensitive_keep_probability
                if is_present
                else self.absent_edge_emit_probability
            )
            if self._rng.random() <= emit_probability:
                edge = present.get(candidate.edge_id, candidate)
                if not is_present:
                    edge = _synthetic_edge(edge)
                released.add_edge(edge)
        return released


def _is_protected(edge: MemoryEdge, policy: EdgeAdmissionPolicy) -> bool:
    return edge.sensitivity in policy.protected_sensitivity_labels


def _synthetic_edge(edge: MemoryEdge) -> MemoryEdge:
    metadata = dict(edge.metadata)
    metadata["dp_synthetic"] = True
    return MemoryEdge(
        edge_id=f"dp-synthetic:{edge.edge_id}",
        source_id=edge.source_id,
        relation=edge.relation,
        target_id=edge.target_id,
        owner_session_id=edge.owner_session_id,
        source_user_id=edge.source_user_id,
        turn_id=edge.turn_id,
        sensitivity=edge.sensitivity,
        created_at=edge.created_at,
        metadata=metadata,
    )
