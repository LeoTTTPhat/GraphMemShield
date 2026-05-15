# GraphMemShield Synthetic Experiment Report

This report covers experiments that run without external datasets, APIs,
GPU resources, or production graph-memory systems.

| Experiment | Condition | Metric | Value | Notes |
|---|---|---:|---:|---|
| dataset_summary | large_synthetic | users | 20 |  |
| dataset_summary | large_synthetic | sessions | 60 |  |
| dataset_summary | large_synthetic | nodes | 134 |  |
| dataset_summary | large_synthetic | edges | 159 |  |
| cross_session_probe | baseline | leaked_edge_count | 3 |  |
| cross_session_probe | baseline | unique_leaked_edge_count | 3 |  |
| cross_session_probe | baseline | leakage_event_count | 3 |  |
| cross_session_probe | baseline | leakage_rate | 0.0323 |  |
| cross_session_probe | strict_guard | leaked_edge_count | 0 |  |
| cross_session_probe | strict_guard | leakage_reduction | 1.0 |  |
| session_graph_link | structure_only | top_1_hit | True |  |
| session_graph_link | structure_only | top_score | 1.0 |  |
| temporal_path_infer | baseline | inferred_edge_count | 23 |  |
| budget_curve | budget_0 | victim_leaked_edges | 0 |  |
| budget_curve | budget_0 | utility_retention_rate | 0.0 |  |
| budget_curve | budget_1 | victim_leaked_edges | 0 |  |
| budget_curve | budget_1 | utility_retention_rate | 0.0 |  |
| budget_curve | budget_2 | victim_leaked_edges | 0 |  |
| budget_curve | budget_2 | utility_retention_rate | 0.0 |  |
| budget_curve | budget_5 | victim_leaked_edges | 0 |  |
| budget_curve | budget_5 | utility_retention_rate | 1.0 |  |
| edge_admission | epsilon_0.1 | victim_leaked_edges_mean | 1 |  |
| edge_admission | epsilon_0.1 | victim_leaked_edges_std | 0.9826 |  |
| edge_admission | epsilon_0.1 | utility_retention_mean | 1.0 |  |
| edge_admission | epsilon_1.0 | victim_leaked_edges_mean | 1.7667 |  |
| edge_admission | epsilon_1.0 | victim_leaked_edges_std | 1.1943 |  |
| edge_admission | epsilon_1.0 | utility_retention_mean | 1.0 |  |
| edge_admission | epsilon_3.0 | victim_leaked_edges_mean | 2.7333 |  |
| edge_admission | epsilon_3.0 | victim_leaked_edges_std | 0.6397 |  |
| edge_admission | epsilon_3.0 | utility_retention_mean | 1.0 |  |

## Manual Follow-up Required

- Replace the synthetic graph with PersonaChat, MultiWOZ, Enron, and controlled health/finance dialogue ingestion.
- Connect retrieval to Neo4j or another property-graph backend-backed graph memory.
- Add response-level scoring for black-box CrossSessionProbe.
- Add graph edit distance and learned-embedding baselines for SessionGraphLink.
- Replace timestamp sorting in TemporalPathInfer with beam-search path likelihood when retrieved contexts are noisy.
- Replace one-sided edge suppression with a formal DP mechanism over a public candidate edge universe.
- Add privacy accounting and repeated-composition analysis for any future write-time DP release mechanism.
