# GraphMemShield Reproducibility Guide

This guide reproduces the current GraphMemShield artifact from the repository root.

## 1. Verify Python Tests

Run:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest Ideas/GraphMemShield/tests -q
```

Expected result:

```text
22 passed
```

The `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` prefix avoids unrelated globally installed pytest plugins from affecting this project.

## 2. Run In-Memory Synthetic Experiments

Run:

```bash
python3 Ideas/GraphMemShield/examples/run_experiments.py
```

Expected outputs:

- `Ideas/GraphMemShield/output/synthetic_experiments.json`
- `Ideas/GraphMemShield/output/synthetic_experiments.csv`
- `Ideas/GraphMemShield/output/synthetic_experiments.md`

Expected key results:

- baseline cross-session leaked edges: 2
- strict guard leaked edges: 0
- strict guard leakage reduction: 1.0

## 3. Verify PrivacyGuard Docker Services

Required containers:

```text
zkp-edge
zkp-fog
zkp-cloud
zkp-mongodb
```

Health endpoints:

```bash
curl -sS http://localhost:3001/api/health
curl -sS http://localhost:3002/api/health
curl -sS http://localhost:3003/api/health
```

Expected status: `ok` for edge, fog, and cloud. Cloud should report `mongoState: 1`.

## 4. Run Single Docker Experiment

Run:

```bash
python3 Ideas/GraphMemShield/examples/run_privacyguard_docker_experiment.py
```

What it does:

1. Seeds de-identified records into `privacyguard.userData`.
2. Fetches records through the Cloud API.
3. Converts fetched records into a GraphMemShield memory graph.
4. Runs `CrossSessionProbe` with and without `GraphMemGuard`.

Scope: this is a Docker-backed Cloud API read-path experiment. It does not exercise the full encrypted proof write path.

Expected outputs:

- `Ideas/GraphMemShield/output/privacyguard_docker_experiment.json`
- `Ideas/GraphMemShield/output/privacyguard_docker_experiment.md`

Expected key results:

- records: 3
- nodes: 15
- edges: 15
- baseline leaked edges: 5
- defended leaked edges: 0
- leakage reduction: 1.0

## 5. Run Batch Docker Experiment

Run:

```bash
python3 Ideas/GraphMemShield/examples/run_privacyguard_batch_experiment.py
```

Input dataset:

- `Ideas/GraphMemShield/data/sample_dialogues.jsonl`

Expected outputs:

- `Ideas/GraphMemShield/output/privacyguard_batch_results.json`
- `Ideas/GraphMemShield/output/privacyguard_batch_results.csv`
- `Ideas/GraphMemShield/output/privacyguard_batch_results.md`

Expected key results:

- input records: 12
- fetched records: 12
- users: 6
- sessions: 12
- nodes: 36
- edges: 48
- baseline leaked edges: 48
- strict guard leaked edges: 0
- leakage reduction: 1.0
- SessionGraphLink top-3 accuracy: 1.0
- TemporalPathInfer edge recall: 1.0

## 6. Generate Aggregate Report

Run:

```bash
python3 Ideas/GraphMemShield/examples/generate_aggregate_report.py
```

Expected outputs:

- `Ideas/GraphMemShield/output/aggregate_results.json`
- `Ideas/GraphMemShield/output/aggregate_results.csv`
- `Ideas/GraphMemShield/output/aggregate_results.md`

Expected result count:

```text
aggregate rows: 62
```

## 7. Validate Output Structure

Run:

```bash
python3 - <<'PY'
import json
from pathlib import Path
batch = json.loads(Path('Ideas/GraphMemShield/output/privacyguard_batch_results.json').read_text())['results']
agg = json.loads(Path('Ideas/GraphMemShield/output/aggregate_results.json').read_text())
checks = {
    'session_topk_mrr': all(any(r['attack']=='SessionGraphLink' and r['metric']==m for r in batch) for m in ['top1_accuracy','top3_accuracy','mean_reciprocal_rank']),
    'temporal_metrics': all(any(r['attack']=='TemporalPathInfer' and r['metric']==m for r in batch) for m in ['edge_precision','edge_recall','edge_f1','pairwise_ordering_accuracy']),
    'query_budget_curves': all(any(r['attack']=='CrossSessionProbe' and r['condition']==f'query_budget_{b}' for r in batch) for b in ['1','2','4','all']),
    'aggregate_report_rows': len(agg),
}
print(json.dumps(checks, indent=2))
assert checks['session_topk_mrr']
assert checks['temporal_metrics']
assert checks['query_budget_curves']
assert checks['aggregate_report_rows'] >= 50
PY
```

Expected output:

```json
{
  "session_topk_mrr": true,
  "temporal_metrics": true,
  "query_budget_curves": true,
  "aggregate_report_rows": 62
}
```

## 8. Reproducibility Notes

- Docker experiments intentionally seed de-identified benchmark records directly into MongoDB for controlled evaluation.
- Strict guard results should be interpreted as provenance/session isolation baselines.
- The temporal-path baseline measures timestamp/provenance exposure.
- Edge admission is a seeded proxy and should not be described as formal DP.
- The current artifact does not require GPUs or external APIs.
- The current sample data is not raw personal data.
- Generated `output/*.json`, `output/*.csv`, and `output/*.md` files are part of the experiment artifact.
