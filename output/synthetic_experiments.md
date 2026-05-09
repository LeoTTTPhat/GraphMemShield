# GraphMemShield Synthetic Experiment Report

This report covers experiments that run without external datasets, APIs,
GPU resources, or production graph-memory systems.

| Experiment | Condition | Metric | Value | Notes |
|---|---|---:|---:|---|
| cross_session_probe | baseline | leaked_edge_count | 2 |  |
| cross_session_probe | baseline | unique_leaked_edge_count | 2 |  |
| cross_session_probe | baseline | leakage_event_count | 6 |  |
| cross_session_probe | baseline | leakage_rate | 0.5 |  |
| cross_session_probe | baseline | event_leakage_rate | 0.5 |  |
| cross_session_probe | baseline | per_query_leak_rate | 1.0 |  |
| cross_session_probe | strict_guard | leaked_edge_count | 0 |  |
| cross_session_probe | strict_guard | leakage_event_count | 0 |  |
| cross_session_probe | strict_guard | leakage_reduction | 1.0 |  |
| session_graph_link | structure_only | top_1_hit | True |  |
| session_graph_link | structure_only | top_candidate | alice-session-2 |  |
| session_graph_link | structure_only | top_score | 1.0 |  |
| temporal_path_infer | baseline | prefix_ordering_accuracy | 1.0 |  |
| temporal_path_infer | baseline | inferred_edge_count | 4 |  |
| temporal_path_infer | strict_guard | inferred_edge_count | 0 |  |
| budget_curve | budget_0 | bob_session_leaked_edges | 0 | Medical edges remain blocked; normal cross-session edges follow budget. |
| budget_curve | budget_1 | bob_session_leaked_edges | 1 | Medical edges remain blocked; normal cross-session edges follow budget. |
| budget_curve | budget_2 | bob_session_leaked_edges | 2 | Medical edges remain blocked; normal cross-session edges follow budget. |
| edge_admission | epsilon_0.1 | sensitive_keep_probability | 0.525 |  |
| edge_admission | epsilon_0.1 | admitted_sensitive_edges | 3 | Seeded proxy; not a complete DP accounting result. |
| edge_admission | epsilon_0.1 | victim_leaked_edges | 1 | Leakage after write-time edge admission. |
| edge_admission | epsilon_1.0 | sensitive_keep_probability | 0.7311 |  |
| edge_admission | epsilon_1.0 | admitted_sensitive_edges | 3 | Seeded proxy; not a complete DP accounting result. |
| edge_admission | epsilon_1.0 | victim_leaked_edges | 1 | Leakage after write-time edge admission. |
| edge_admission | epsilon_3.0 | sensitive_keep_probability | 0.9526 |  |
| edge_admission | epsilon_3.0 | admitted_sensitive_edges | 5 | Seeded proxy; not a complete DP accounting result. |
| edge_admission | epsilon_3.0 | victim_leaked_edges | 2 | Leakage after write-time edge admission. |

## Manual Follow-up Required

- Replace the synthetic graph with PersonaChat, MultiWOZ, Enron, and controlled health/finance dialogue ingestion.
- Connect retrieval to Neo4j or another property-graph backend-backed graph memory.
- Add response-level scoring for black-box CrossSessionProbe.
- Replace heuristic SessionGraphLink with WL-kernel or graph edit distance baselines.
- Replace timestamp sorting in TemporalPathInfer with beam-search path likelihood when retrieved contexts are noisy.
- Replace seeded edge-admission proxy with a formal DP mechanism after adjacency granularity is finalized.
- Add privacy accounting and repeated-composition analysis for write-time defenses.
