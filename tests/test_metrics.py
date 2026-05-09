import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graphmemshield.evaluation import (
    pairwise_ordering_accuracy,
    reciprocal_rank,
    set_precision_recall_f1,
    top_k_hit,
)


def test_top_k_and_reciprocal_rank_metrics():
    ranked = ("a", "b", "c")

    assert top_k_hit(ranked, "b", k=2)
    assert not top_k_hit(ranked, "c", k=2)
    assert reciprocal_rank(ranked, "b") == 0.5
    assert reciprocal_rank(ranked, "missing") == 0.0


def test_set_precision_recall_f1():
    precision, recall, f1 = set_precision_recall_f1(
        ("a", "b", "x"),
        ("a", "b", "c"),
    )

    assert round(precision, 4) == 0.6667
    assert round(recall, 4) == 0.6667
    assert round(f1, 4) == 0.6667


def test_pairwise_ordering_accuracy():
    assert pairwise_ordering_accuracy(("a", "b", "c"), ("a", "b", "c")) == 1.0
    assert pairwise_ordering_accuracy(("c", "b", "a"), ("a", "b", "c")) == 0.0
