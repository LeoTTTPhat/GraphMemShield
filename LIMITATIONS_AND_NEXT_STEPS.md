# GraphMemShield Limitations and Next Steps

This document separates what the current artifact demonstrates from what still requires larger datasets, production system integrations, or formal privacy analysis.

## What Is Implemented

- A runnable Python package, `graphmemshield`.
- In-memory graph-memory simulator with session/user provenance.
- Three baseline attacks:
  - `CrossSessionProbe`
  - `SessionGraphLink`
  - `TemporalPathInfer`
- Two defense mechanisms:
  - `GraphMemGuard` for retrieval-time provenance filtering and exposure budgeting.
  - `RandomizedEdgeAdmission` as a seeded write-time edge-admission proxy.
- JSONL dialogue ingestion with entities, relations, sensitivity labels, user IDs, session IDs, and turn IDs.
- Docker-backed PrivacyGuard integration using MongoDB seeding and Cloud API reads.
- Paper-shaped JSON, CSV, and Markdown outputs.

## What The Current Results Mean

The current results show that the proposed auditing pipeline can detect cross-session leakage in both a local simulator and a running Docker-backed mock system. The PrivacyGuard batch experiment is stronger than a toy unit test because data is seeded into MongoDB, retrieved through the Cloud API, mapped into a memory graph, and evaluated by the GraphMemShield attacks.

The results should be described as **de-identified benchmark experiments**, not experiments on raw personal data. The current sample records are realistic but manually constructed.

## Main Limitations

1. **Dataset scale is small**
   - Current Docker batch dataset has 12 records, 6 users, and 12 sessions.
   - The CIKM revision benchmark has 576 records, 48 users, 192 sessions, and 2304 edges, but it is deterministic/de-identified rather than an externally hosted public corpus.
   - MultiWOZ and Enron-format loaders are implemented; full public-corpus runs require evaluator-supplied licensed data files.

2. **The Docker system is a mock deployment**
   - The experiment uses a real running Docker stack and Cloud API reads.
   - It does not yet exercise the full `/api/validate-and-prove` to `/api/store` encrypted proof flow.
   - Data is seeded directly into MongoDB for controlled benchmarking.
   - Current wording should therefore say "Docker-backed read-path experiment", not full end-to-end PrivacyGuard validation.

3. **Graph extraction is controlled**
   - The JSONL dataset already contains ground-truth relations.
   - A production system would need entity/relation extraction from raw conversations.

4. **SessionGraphLink is still heuristic**
   - Current features include relation counts, relation bigrams, sensitivity bigrams, co-occurrence features, degree histograms, 1-WL hashes, a graph-edit proxy, hashed embeddings, and optional semantic labels.
   - A stronger paper version should add learned graph encoders trained on larger public traces.

5. **TemporalPathInfer is still heuristic**
   - Current inference sorts retrieved edges by `created_at`.
   - A timestamp-hidden relation-priority/path-continuity baseline is implemented, but it is not a learned hidden-order attacker.
   - A stronger paper version should add beam search over relation paths and response-likelihood scoring.

6. **Black-box response scoring is deterministic**
   - The CIKM revision experiments add response-level leakage scoring using deterministic template and local abstractive generators.
   - OpenAI-backed response generation is implemented as an optional path and is skipped when `OPENAI_API_KEY` is not configured.
   - A production system should additionally score real model responses from deployed graph-backed applications.

7. **RandomizedEdgeAdmission is not differentially private**
   - It is a seeded proxy for write-time edge admission.
   - It should not be described as a differentially private mechanism in source release or paper claims.
   - Under edge-event adjacency, one-sided suppression gives positive probability to outputs containing a present sensitive edge and zero probability to the same output when that edge is absent.
   - `FixedUniverseRandomizedResponseAdmission` is implemented separately for candidate-universe DP experiments over present and absent candidates.
   - Advanced composition and privacy-budget management remain future work.

8. **Strict guard results are isolation-baseline results**
   - Default `GraphMemGuardPolicy` uses `allow_cross_session=False`.
   - The 48 to 0 leakage result demonstrates that strict provenance/session isolation eliminates measured leakage on the sample data.
   - It should not be presented as strong standalone evidence of a novel defense.

## Next Steps Before External Artifact Evaluation

1. Freeze the current artifact as the baseline implementation.
2. Have another reviewer review code correctness, experiment validity, and documentation clarity.
3. Have another reviewer check whether paper tables match generated JSON/CSV outputs.
4. Have another reviewer propose the next integration target: Neo4j or another property-graph backend.

## Next Steps After Review

1. Replace or supplement the deterministic enterprise/health/finance benchmark with externally approved public traces.
2. Connect the property-graph adapter to a live Neo4j deployment for latency and policy-regression experiments; Kuzu is covered locally when installed.
3. Score real model responses from a deployed graph-backed application or from OpenAI with an approved API key.
4. Add learned graph encoders for session-linking baselines.
5. Add advanced composition and privacy-budget management for fixed-universe DP releases.
