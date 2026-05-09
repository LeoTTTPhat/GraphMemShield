# GraphMemShield

GraphMemShield is a research prototype for auditing cross-session privacy leakage in dynamic knowledge-graph memory systems. It provides a small graph-memory simulator, attack baselines, defense baselines, reproducible benchmark fixtures, and report generators.

The project is intended as a source artifact and synthetic/de-identified benchmark scaffold. It is not a production security product.

## Features

- Dynamic graph-memory model with nodes, edges, owner sessions, source users, timestamps, provenance metadata, and sensitivity labels.
- `CrossSessionProbe` for measuring whether victim-owned graph memory appears in another session's retrieval results.
- `SessionGraphLink` for linking anonymized sessions via graph-structure features.
- `TemporalPathInfer` timestamp/provenance exposure baseline.
- `GraphMemGuard` for provenance-filtered retrieval and bounded cross-session exposure.
- `RandomizedEdgeAdmission` seeded proxy for write-time sensitive-edge admission experiments.
- JSONL dialogue ingestion for multi-user, multi-session benchmark data.
- PrivacyGuard Docker adapter for de-identified MongoDB-backed read-path experiments.
- JSON, CSV, and Markdown report generation.

## Installation

Clone the repository:

```bash
git clone https://github.com/SonHaXuan/GraphMemShield.git
cd GraphMemShield
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the package in editable mode with test dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Run Tests

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests -q
```

Expected local verification result for this snapshot:

```text
22 passed
```

The `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` prefix prevents unrelated globally installed pytest plugins from affecting the artifact.

## Run Local Experiments

Run the basic MVP:

```bash
python examples/run_mvp.py
```

Run all in-memory synthetic experiments:

```bash
python examples/run_experiments.py
```

Expected outputs:

- `output/synthetic_experiments.json`
- `output/synthetic_experiments.csv`
- `output/synthetic_experiments.md`

## Run Docker-Backed Experiments

The Docker-backed scripts expect a running PrivacyGuard-style mock stack:

- edge service on `localhost:3001`
- fog service on `localhost:3002`
- cloud service on `localhost:3003`
- MongoDB on `localhost:27017`

Check health endpoints:

```bash
curl -sS http://localhost:3001/api/health
curl -sS http://localhost:3002/api/health
curl -sS http://localhost:3003/api/health
```

Run the single de-identified seed-record experiment:

```bash
python examples/run_privacyguard_docker_experiment.py
```

Run the batch de-identified JSONL experiment:

```bash
python examples/run_privacyguard_batch_experiment.py
```

These scripts seed controlled de-identified benchmark records into MongoDB, fetch them through the cloud API, convert them into a GraphMemShield memory graph, and evaluate leakage.

## Generate Aggregate Results

```bash
python examples/generate_aggregate_report.py
```

Expected outputs:

- `output/aggregate_results.json`
- `output/aggregate_results.csv`
- `output/aggregate_results.md`

Expected aggregate row count for this snapshot: `62`.

## Important Caveats

- The included datasets are synthetic/de-identified benchmark fixtures.
- Docker-backed experiments are read-path experiments with controlled MongoDB seeding.
- `GraphMemGuard` strict isolation results should be interpreted as provenance/session isolation baselines.
- `TemporalPathInfer` measures timestamp/provenance exposure, not hidden temporal-order inference.
- `RandomizedEdgeAdmission` is a seeded proxy, not a formal differentially private mechanism.
- Larger public datasets, production graph backends, response-level leakage scoring, and stronger graph-matching baselines are future work.

## Documentation

- `EXPERIMENT_MANIFEST.md`: implemented experiments and reproduction commands.
- `PAPER_READY_TABLES.md`: compact result tables.
- `LIMITATIONS_AND_NEXT_STEPS.md`: artifact limitations and next steps.
- `REPRODUCIBILITY.md`: full reproduction guide.
- `RELEASE_CHECKLIST.md`: source artifact release checklist.

## License

MIT. See `LICENSE`.
