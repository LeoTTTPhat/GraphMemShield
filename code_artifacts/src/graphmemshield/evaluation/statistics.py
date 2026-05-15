from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class ConfidenceInterval:
    mean: float
    std: float
    n: int
    ci95_low: float
    ci95_high: float


def ci95(values: list[float]) -> ConfidenceInterval:
    n = len(values)
    if n == 0:
        return ConfidenceInterval(0.0, 0.0, 0, 0.0, 0.0)
    mean = sum(values) / n
    if n == 1:
        return ConfidenceInterval(mean, 0.0, n, mean, mean)
    variance = sum((value - mean) ** 2 for value in values) / (n - 1)
    std = sqrt(variance)
    half_width = 1.96 * std / sqrt(n)
    return ConfidenceInterval(mean, std, n, mean - half_width, mean + half_width)
