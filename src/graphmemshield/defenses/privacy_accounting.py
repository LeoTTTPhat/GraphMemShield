from __future__ import annotations

from dataclasses import dataclass
from math import exp, log


@dataclass(frozen=True)
class CompositionReport:
    """Basic sequential composition for repeated edge-DP releases."""

    per_release_epsilon: float
    release_count: int

    @property
    def composed_epsilon(self) -> float:
        return self.per_release_epsilon * self.release_count


@dataclass(frozen=True)
class FullGraphReleasePrivacyReport:
    """Scope accounting for full-graph releases over a candidate universe."""

    per_edge_epsilon: float
    protected_candidate_edges: int
    unprotected_released_edges: int
    release_count: int = 1

    @property
    def protected_release_epsilon(self) -> float:
        return self.per_edge_epsilon * self.protected_candidate_edges * self.release_count

    @property
    def has_full_graph_dp(self) -> bool:
        return self.unprotected_released_edges == 0

    @property
    def guarantee_scope(self) -> str:
        if self.has_full_graph_dp:
            return "full_graph_over_candidate_universe"
        return "protected_candidate_edges_only"


def randomized_response_probabilities(epsilon: float) -> tuple[float, float]:
    """Return present/absent emit probabilities for fixed-universe RR."""

    bounded_epsilon = max(epsilon, 0.0)
    present = exp(bounded_epsilon) / (1.0 + exp(bounded_epsilon))
    absent = 1.0 / (1.0 + exp(bounded_epsilon))
    return present, absent


def randomized_response_privacy_loss(epsilon: float) -> float:
    """Worst-case single-bit privacy loss for fixed-universe RR."""

    present, absent = randomized_response_probabilities(epsilon)
    emit_loss = abs(log(present / absent))
    suppress_loss = abs(log((1.0 - present) / (1.0 - absent)))
    return max(emit_loss, suppress_loss)
