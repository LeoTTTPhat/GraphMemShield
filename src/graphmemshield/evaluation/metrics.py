from __future__ import annotations


def leakage_reduction(baseline_leaks: int, defended_leaks: int) -> float:
    """Return relative leakage reduction in [0, 1] when baseline has leaks."""

    if baseline_leaks <= 0:
        return 0.0
    reduction = (baseline_leaks - defended_leaks) / baseline_leaks
    return max(0.0, min(1.0, reduction))


def top_k_hit(ranked_ids: tuple[str, ...], expected_id: str, *, k: int) -> bool:
    return expected_id in ranked_ids[:k]


def reciprocal_rank(ranked_ids: tuple[str, ...], expected_id: str) -> float:
    try:
        return 1.0 / (ranked_ids.index(expected_id) + 1)
    except ValueError:
        return 0.0


def ordering_accuracy(
    inferred_ids: tuple[str, ...], expected_ids: tuple[str, ...]
) -> float:
    if not expected_ids:
        return 0.0
    aligned = zip(inferred_ids, expected_ids)
    correct = sum(1 for inferred, expected in aligned if inferred == expected)
    return correct / len(expected_ids)


def set_precision_recall_f1(
    predicted_ids: tuple[str, ...], expected_ids: tuple[str, ...]
) -> tuple[float, float, float]:
    predicted = set(predicted_ids)
    expected = set(expected_ids)
    if not predicted and not expected:
        return 1.0, 1.0, 1.0
    if not predicted:
        return 0.0, 0.0, 0.0
    true_positive = len(predicted.intersection(expected))
    precision = true_positive / len(predicted)
    recall = true_positive / len(expected) if expected else 0.0
    if precision + recall == 0.0:
        return precision, recall, 0.0
    return precision, recall, 2 * precision * recall / (precision + recall)


def pairwise_ordering_accuracy(
    inferred_ids: tuple[str, ...], expected_ids: tuple[str, ...]
) -> float:
    expected_pairs = _ordered_pairs(expected_ids)
    if not expected_pairs:
        return 0.0

    inferred_positions = {edge_id: index for index, edge_id in enumerate(inferred_ids)}
    correct = 0
    comparable = 0
    for left, right in expected_pairs:
        if left not in inferred_positions or right not in inferred_positions:
            continue
        comparable += 1
        if inferred_positions[left] < inferred_positions[right]:
            correct += 1
    return correct / comparable if comparable else 0.0


def _ordered_pairs(ids: tuple[str, ...]) -> tuple[tuple[str, str], ...]:
    pairs: list[tuple[str, str]] = []
    for left_index, left in enumerate(ids):
        for right in ids[left_index + 1 :]:
            pairs.append((left, right))
    return tuple(pairs)
