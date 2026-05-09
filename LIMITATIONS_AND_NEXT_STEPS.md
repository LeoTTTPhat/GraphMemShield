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
   - Current batch dataset has 12 records, 6 users, and 12 sessions.
   - This is enough to verify the pipeline, not enough for final journal claims.

2. **The Docker system is a mock deployment**
   - The experiment uses a real running Docker stack and Cloud API reads.
   - It does not yet exercise the full `/api/validate-and-prove` to `/api/store` encrypted proof flow.
   - Data is seeded directly into MongoDB for controlled benchmarking.
   - Current wording should therefore say "Docker-backed read-path experiment", not full end-to-end PrivacyGuard validation.

3. **Graph extraction is controlled**
   - The JSONL dataset already contains ground-truth relations.
   - A production system would need entity/relation extraction from raw conversations.

4. **SessionGraphLink is still heuristic**
   - Current features include relation counts, relation bigrams, sensitivity bigrams, co-occurrence features, degree histograms, and optional semantic labels.
   - A stronger paper version should add WL-kernel, graph edit distance approximation, or learned graph embeddings.

5. **TemporalPathInfer is still timestamp-based**
   - Current inference sorts retrieved edges by `created_at`.
   - Current accuracy measures timestamp/provenance exposure, not hidden-order inference capability.
   - A stronger paper version should add beam search over relation paths and response-likelihood scoring.

6. **CrossSessionProbe is retrieval-level**
   - Current experiments measure graph-edge exposure.
   - Black-box response scoring requires a real system response endpoint.

7. **RandomizedEdgeAdmission is not a complete DP proof**
   - It is a seeded proxy for write-time edge admission.
   - It should not be described as a differentially private mechanism in source release or paper claims.
   - Formal DP accounting requires a finalized adjacency definition and composition analysis.

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

1. Add a larger public dataset ingestion path.
2. Add a real graph backend adapter.
3. Add response-level leakage scoring.
4. Add stronger session-linking baselines.
5. Add formal privacy accounting for write-time defenses.
6. Convert the proposal into a paper outline with threat model, method, experiments, results, limitations, and ethics sections.
