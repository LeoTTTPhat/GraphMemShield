import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from graphmemshield.evaluation import (
    render_markdown_report,
    run_synthetic_experiments,
)


def test_synthetic_experiments_cover_all_baseline_attacks():
    records = run_synthetic_experiments()
    experiment_names = {record.experiment for record in records}

    assert "cross_session_probe" in experiment_names
    assert "session_graph_link" in experiment_names
    assert "temporal_path_infer" in experiment_names
    assert "budget_curve" in experiment_names
    assert "edge_admission" in experiment_names


def test_synthetic_experiments_include_strict_guard_reduction():
    records = run_synthetic_experiments()
    lookup = {
        (record.experiment, record.condition, record.metric): record.value
        for record in records
    }

    assert lookup[("cross_session_probe", "baseline", "leaked_edge_count")] > 0
    assert lookup[("cross_session_probe", "strict_guard", "leaked_edge_count")] == 0
    assert lookup[("cross_session_probe", "strict_guard", "leakage_reduction")] == 1.0


def test_markdown_report_lists_manual_follow_up():
    report = render_markdown_report(run_synthetic_experiments())

    assert "Manual Follow-up Required" in report
    assert "Connect retrieval to Neo4j" in report
