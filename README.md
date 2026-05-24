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
git clone https://github.com/LeoTTTPhat/GraphMemShield.git
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
41 passed
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

Run the larger CIKM revision benchmark:

```bash
python examples/generate_enterprise_benchmark.py
python examples/run_langgraph_memory_experiment.py
python examples/run_mem0_memory_experiment.py
python examples/run_cikm_revision_experiments.py
```

This adds a 576-record enterprise/health/finance benchmark, real LangGraph and Mem0 memory-framework workflows, a persistent SQLite property-graph roundtrip, black-box response leakage scoring, bounded-sharing curves, cross-domain session-link transfer diagnostics, OpenAI-backed adaptive probing when configured, timestamp-hidden temporal inference, fixed-universe randomized response, and frontier-style privacy baseline comparisons.

Run the external MultiWOZ corpus experiment:

```bash
python examples/run_multiwoz_experiment.py
```

By default this downloads MultiWOZ 2.1 into `/tmp`, caps the run at 1,000 dialogues, and writes only the derived sample/results into the repo.

Run the deployed-style agent-memory / GraphRAG trace experiment:

```bash
python examples/run_deployed_graphrag_trace.py
```

By default this starts a live local HTTP retrieval service over a persistent SQLite graph built from the MultiWOZ-derived trace. To run an approved production GraphRAG trace with the same service boundary, set `GRAPHMEMSHIELD_PRODUCTION_GRAPHRAG_JSONL=/path/to/trace.jsonl` using the GraphMemShield dialogue JSONL schema. The required JSONL fields are `user_id`, `session_id`, `turn_id`, `timestamp`, `domain`, `text`, `entities`, and `relations`; each relation contains `source`, `relation`, `target`, and optional `sensitivity`. Runs with this environment variable are labeled `user_supplied_production_jsonl` and set `approved_internal_deployment_trace=True` in the output.

For the paper snapshot, the public proxy run is archived as `output/public_multiwoz_http_trace.*`, and the approved internal OpenAI-RAG run is archived as `output/internal_tracekg_rag_openai_trace.*`. The internal run uses a de-identified 60-task, 300-event TraceKG RAG export converted through the same JSONL schema.

Run the Enron maildir / Enron-style communication graph experiment:

```bash
python examples/run_enron_experiment.py
```

Set `GRAPHMEMSHIELD_ENRON_MAILDIR=/path/to/maildir` to use an approved local Enron maildir. Without that variable, the script generates a reproducible Enron-style communication fixture for artifact testing.

## Generate Aggregate Results

```bash
python examples/generate_aggregate_report.py
```

Expected outputs:

- `output/aggregate_results.json`
- `output/aggregate_results.csv`
- `output/aggregate_results.md`

Expected aggregate row count for this snapshot: `575`.

## Important Caveats

- The included datasets are synthetic/de-identified benchmark fixtures.
- Docker-backed experiments are read-path experiments with controlled MongoDB seeding.
- `GraphMemGuard` strict isolation results should be interpreted as provenance/session isolation baselines.
- `TemporalPathInfer` includes both timestamp exposure and a timestamp-hidden heuristic baseline.
- `RandomizedEdgeAdmission` is a seeded one-sided suppression proxy, not a differentially private mechanism.
- Fixed-universe randomized response is implemented separately for per-edge DP experiments over a public candidate edge universe.
- The LangGraph experiment uses an actual `langgraph` workflow around write/retrieve memory nodes; install `graphmemshield[frameworks]` or `langgraph>=1.2.0`.
- The Mem0 experiment uses the real `mem0ai` package with local Qdrant storage and OpenAI embeddings; it indexes a bounded edge sample to keep the reproducible run small.
- The learned session-link audit uses supervised graph-pair features and deliberately excludes direct user-id features; high accuracy is evidence that the benchmark graph has linkable structural signatures.
- MultiWOZ runs from the upstream public zip by default; Enron-format loaders are included for user-provided licensed maildir files.
- The deployed-style GraphRAG trace uses a local HTTP service and SQLite backend; it is a deployment-surface test, not evidence that an external production service was probed unless `GRAPHMEMSHIELD_PRODUCTION_GRAPHRAG_JSONL` points to an approved production export.
- Kuzu backend experiments run when `graphmemshield[backends]` is installed; live Neo4j latency/policy experiments remain future integration work.
- OpenAI response generation and adaptive probe planning run when `graphmemshield[llm]` and `OPENAI_API_KEY` are configured; otherwise the experiment records skipped LLM conditions.

## Documentation

The following detailed documentation files are available in the `code_artifacts/` directory:

- `code_artifacts/EXPERIMENT_MANIFEST.md`: implemented experiments and reproduction commands.
- `code_artifacts/PAPER_READY_TABLES.md`: compact result tables.
- `code_artifacts/REPRODUCIBILITY.md`: full reproduction guide.
- `code_artifacts/RELEASE_CHECKLIST.md`: source artifact release checklist.
- `code_artifacts/CODE_ARTIFACTS_MANIFEST.md`: manifest of the code artifact.

## License

This project is licensed under the MIT License.
