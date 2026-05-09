# GraphMemShield Aggregate Results

This table aggregates all currently runnable experiments.

| System | Dataset | Attack | Condition | Metric | Value | Notes |
|---|---|---|---|---:|---:|---|
| in_memory_simulator | synthetic_multisession | cross_session_probe | baseline | leaked_edge_count | 2 |  |
| in_memory_simulator | synthetic_multisession | cross_session_probe | baseline | unique_leaked_edge_count | 2 |  |
| in_memory_simulator | synthetic_multisession | cross_session_probe | baseline | leakage_event_count | 6 |  |
| in_memory_simulator | synthetic_multisession | cross_session_probe | baseline | leakage_rate | 0.5 |  |
| in_memory_simulator | synthetic_multisession | cross_session_probe | baseline | event_leakage_rate | 0.5 |  |
| in_memory_simulator | synthetic_multisession | cross_session_probe | baseline | per_query_leak_rate | 1.0 |  |
| in_memory_simulator | synthetic_multisession | cross_session_probe | strict_guard | leaked_edge_count | 0 |  |
| in_memory_simulator | synthetic_multisession | cross_session_probe | strict_guard | leakage_event_count | 0 |  |
| in_memory_simulator | synthetic_multisession | cross_session_probe | strict_guard | leakage_reduction | 1.0 |  |
| in_memory_simulator | synthetic_multisession | session_graph_link | structure_only | top_1_hit | True |  |
| in_memory_simulator | synthetic_multisession | session_graph_link | structure_only | top_candidate | alice-session-2 |  |
| in_memory_simulator | synthetic_multisession | session_graph_link | structure_only | top_score | 1.0 |  |
| in_memory_simulator | synthetic_multisession | temporal_path_infer | baseline | prefix_ordering_accuracy | 1.0 |  |
| in_memory_simulator | synthetic_multisession | temporal_path_infer | baseline | inferred_edge_count | 4 |  |
| in_memory_simulator | synthetic_multisession | temporal_path_infer | strict_guard | inferred_edge_count | 0 |  |
| in_memory_simulator | synthetic_multisession | budget_curve | budget_0 | bob_session_leaked_edges | 0 | Medical edges remain blocked; normal cross-session edges follow budget. |
| in_memory_simulator | synthetic_multisession | budget_curve | budget_1 | bob_session_leaked_edges | 1 | Medical edges remain blocked; normal cross-session edges follow budget. |
| in_memory_simulator | synthetic_multisession | budget_curve | budget_2 | bob_session_leaked_edges | 2 | Medical edges remain blocked; normal cross-session edges follow budget. |
| in_memory_simulator | synthetic_multisession | edge_admission | epsilon_0.1 | sensitive_keep_probability | 0.525 |  |
| in_memory_simulator | synthetic_multisession | edge_admission | epsilon_0.1 | admitted_sensitive_edges | 3 | Seeded proxy; not a complete DP accounting result. |
| in_memory_simulator | synthetic_multisession | edge_admission | epsilon_0.1 | victim_leaked_edges | 1 | Leakage after write-time edge admission. |
| in_memory_simulator | synthetic_multisession | edge_admission | epsilon_1.0 | sensitive_keep_probability | 0.7311 |  |
| in_memory_simulator | synthetic_multisession | edge_admission | epsilon_1.0 | admitted_sensitive_edges | 3 | Seeded proxy; not a complete DP accounting result. |
| in_memory_simulator | synthetic_multisession | edge_admission | epsilon_1.0 | victim_leaked_edges | 1 | Leakage after write-time edge admission. |
| in_memory_simulator | synthetic_multisession | edge_admission | epsilon_3.0 | sensitive_keep_probability | 0.9526 |  |
| in_memory_simulator | synthetic_multisession | edge_admission | epsilon_3.0 | admitted_sensitive_edges | 5 | Seeded proxy; not a complete DP accounting result. |
| in_memory_simulator | synthetic_multisession | edge_admission | epsilon_3.0 | victim_leaked_edges | 2 | Leakage after write-time edge admission. |
| privacyguard-docker | seed_records | CrossSessionProbe | baseline | leaked_edge_count | 5 |  |
| privacyguard-docker | seed_records | CrossSessionProbe | baseline | leakage_event_count | 15 |  |
| privacyguard-docker | seed_records | CrossSessionProbe | strict_guard | leaked_edge_count | 0 |  |
| privacyguard-docker | seed_records | CrossSessionProbe | strict_guard | leakage_reduction | 1.0 | Strict provenance/session isolation blocks cross-session retrieval. |
| privacyguard-docker | sample_dialogues | CrossSessionProbe | baseline | total_leaked_edges | 48 |  |
| privacyguard-docker | sample_dialogues | CrossSessionProbe | strict_guard | total_leaked_edges | 0 |  |
| privacyguard-docker | sample_dialogues | CrossSessionProbe | strict_guard | leakage_reduction | 1.0 |  |
| privacyguard-docker | sample_dialogues | CrossSessionProbe | baseline | query_count | 48 |  |
| privacyguard-docker | sample_dialogues | CrossSessionProbe | strict_guard | defense_framing | strict_provenance_session_isolation | Default GraphMemGuard blocks cross-session retrieval before graph expansion. |
| privacyguard-docker | sample_dialogues | CrossSessionProbe | query_budget_1 | total_leaked_edges | 48 |  |
| privacyguard-docker | sample_dialogues | CrossSessionProbe | query_budget_1 | query_count | 12 |  |
| privacyguard-docker | sample_dialogues | CrossSessionProbe | query_budget_1 | leakage_event_count | 48 |  |
| privacyguard-docker | sample_dialogues | CrossSessionProbe | query_budget_2 | total_leaked_edges | 48 |  |
| privacyguard-docker | sample_dialogues | CrossSessionProbe | query_budget_2 | query_count | 24 |  |
| privacyguard-docker | sample_dialogues | CrossSessionProbe | query_budget_2 | leakage_event_count | 88 |  |
| privacyguard-docker | sample_dialogues | CrossSessionProbe | query_budget_4 | total_leaked_edges | 48 |  |
| privacyguard-docker | sample_dialogues | CrossSessionProbe | query_budget_4 | query_count | 48 |  |
| privacyguard-docker | sample_dialogues | CrossSessionProbe | query_budget_4 | leakage_event_count | 132 |  |
| privacyguard-docker | sample_dialogues | CrossSessionProbe | query_budget_all | total_leaked_edges | 48 |  |
| privacyguard-docker | sample_dialogues | CrossSessionProbe | query_budget_all | query_count | 48 |  |
| privacyguard-docker | sample_dialogues | CrossSessionProbe | query_budget_all | leakage_event_count | 132 |  |
| privacyguard-docker | sample_dialogues | SessionGraphLink | structure_only | evaluated_users | 6 |  |
| privacyguard-docker | sample_dialogues | SessionGraphLink | structure_only | top1_accuracy | 0.3333333333333333 |  |
| privacyguard-docker | sample_dialogues | SessionGraphLink | structure_only | top3_accuracy | 1.0 |  |
| privacyguard-docker | sample_dialogues | SessionGraphLink | structure_only | mean_reciprocal_rank | 0.611111111111111 |  |
| privacyguard-docker | sample_dialogues | SessionGraphLink | semantic_labels | evaluated_users | 6 |  |
| privacyguard-docker | sample_dialogues | SessionGraphLink | semantic_labels | top1_accuracy | 0.3333333333333333 |  |
| privacyguard-docker | sample_dialogues | SessionGraphLink | semantic_labels | top3_accuracy | 1.0 |  |
| privacyguard-docker | sample_dialogues | SessionGraphLink | semantic_labels | mean_reciprocal_rank | 0.6666666666666666 |  |
| privacyguard-docker | sample_dialogues | TemporalPathInfer | timestamp_order | evaluated_sessions | 12 |  |
| privacyguard-docker | sample_dialogues | TemporalPathInfer | timestamp_order | average_ordering_accuracy | 0.5 |  |
| privacyguard-docker | sample_dialogues | TemporalPathInfer | timestamp_order | pairwise_ordering_accuracy | 1.0 |  |
| privacyguard-docker | sample_dialogues | TemporalPathInfer | timestamp_order | edge_precision | 0.4924603174603175 |  |
| privacyguard-docker | sample_dialogues | TemporalPathInfer | timestamp_order | edge_recall | 1.0 |  |
| privacyguard-docker | sample_dialogues | TemporalPathInfer | timestamp_order | edge_f1 | 0.6562998405103669 |  |

## Remaining Manual Work

- Replace de-identified sample data with approved public datasets.
- Add real system response endpoints for black-box scoring.
- Add production graph backend adapters such as Neo4j or another property-graph store.
