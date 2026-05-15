# GraphMemShield Aggregate Results

This table aggregates all currently runnable experiments.

| System | Dataset | Attack | Condition | Metric | Value | Notes |
|---|---|---|---|---:|---:|---|
| in_memory_simulator | synthetic_multisession | dataset_summary | large_synthetic | users | 20 |  |
| in_memory_simulator | synthetic_multisession | dataset_summary | large_synthetic | sessions | 60 |  |
| in_memory_simulator | synthetic_multisession | dataset_summary | large_synthetic | nodes | 134 |  |
| in_memory_simulator | synthetic_multisession | dataset_summary | large_synthetic | edges | 159 |  |
| in_memory_simulator | synthetic_multisession | cross_session_probe | baseline | leaked_edge_count | 3 |  |
| in_memory_simulator | synthetic_multisession | cross_session_probe | baseline | unique_leaked_edge_count | 3 |  |
| in_memory_simulator | synthetic_multisession | cross_session_probe | baseline | leakage_event_count | 3 |  |
| in_memory_simulator | synthetic_multisession | cross_session_probe | baseline | leakage_rate | 0.0323 |  |
| in_memory_simulator | synthetic_multisession | cross_session_probe | strict_guard | leaked_edge_count | 0 |  |
| in_memory_simulator | synthetic_multisession | cross_session_probe | strict_guard | leakage_reduction | 1.0 |  |
| in_memory_simulator | synthetic_multisession | session_graph_link | structure_only | top_1_hit | True |  |
| in_memory_simulator | synthetic_multisession | session_graph_link | structure_only | top_score | 1.0 |  |
| in_memory_simulator | synthetic_multisession | temporal_path_infer | baseline | inferred_edge_count | 23 |  |
| in_memory_simulator | synthetic_multisession | budget_curve | budget_0 | victim_leaked_edges | 0 |  |
| in_memory_simulator | synthetic_multisession | budget_curve | budget_0 | utility_retention_rate | 0.0 |  |
| in_memory_simulator | synthetic_multisession | budget_curve | budget_1 | victim_leaked_edges | 0 |  |
| in_memory_simulator | synthetic_multisession | budget_curve | budget_1 | utility_retention_rate | 0.0 |  |
| in_memory_simulator | synthetic_multisession | budget_curve | budget_2 | victim_leaked_edges | 0 |  |
| in_memory_simulator | synthetic_multisession | budget_curve | budget_2 | utility_retention_rate | 0.0 |  |
| in_memory_simulator | synthetic_multisession | budget_curve | budget_5 | victim_leaked_edges | 0 |  |
| in_memory_simulator | synthetic_multisession | budget_curve | budget_5 | utility_retention_rate | 1.0 |  |
| in_memory_simulator | synthetic_multisession | edge_admission | epsilon_0.1 | victim_leaked_edges_mean | 1 |  |
| in_memory_simulator | synthetic_multisession | edge_admission | epsilon_0.1 | victim_leaked_edges_std | 0.9826 |  |
| in_memory_simulator | synthetic_multisession | edge_admission | epsilon_0.1 | utility_retention_mean | 1.0 |  |
| in_memory_simulator | synthetic_multisession | edge_admission | epsilon_1.0 | victim_leaked_edges_mean | 1.7667 |  |
| in_memory_simulator | synthetic_multisession | edge_admission | epsilon_1.0 | victim_leaked_edges_std | 1.1943 |  |
| in_memory_simulator | synthetic_multisession | edge_admission | epsilon_1.0 | utility_retention_mean | 1.0 |  |
| in_memory_simulator | synthetic_multisession | edge_admission | epsilon_3.0 | victim_leaked_edges_mean | 2.7333 |  |
| in_memory_simulator | synthetic_multisession | edge_admission | epsilon_3.0 | victim_leaked_edges_std | 0.6397 |  |
| in_memory_simulator | synthetic_multisession | edge_admission | epsilon_3.0 | utility_retention_mean | 1.0 |  |
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
| graphmemshield | enterprise_health_finance | dataset | enterprise_health_finance | records | 576 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | dataset | enterprise_health_finance | users | 48 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | dataset | enterprise_health_finance | sessions | 192 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | dataset | enterprise_health_finance | nodes | 162 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | dataset | enterprise_health_finance | edges | 2304 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | backend | sqlite_property_graph | nodes | 162 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | backend | sqlite_property_graph | edges | 2304 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | backend | sqlite_property_graph | sessions | 192 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | cross_session_probe | sqlite_property_graph | leaked_edges | 9 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | backend | kuzu_property_graph | available | True | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | backend | kuzu_property_graph | nodes | 162 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | backend | kuzu_property_graph | edges | 2304 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | backend | kuzu_property_graph | write_seconds | 27.4829 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | backend | kuzu_property_graph | read_seconds | 0.0615 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | cross_session_probe | kuzu_property_graph | leaked_edges | 9 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | latency | kuzu_property_graph | queries | 100 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | latency | kuzu_property_graph | baseline_ms | 1.9513 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | latency | kuzu_property_graph | strict_guard_ms | 1.3446 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | latency | kuzu_property_graph | bounded_guard_ms | 1.3084 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | latency | kuzu_property_graph | strict_overhead_pct | -31.0944 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | latency | kuzu_property_graph | bounded_overhead_pct | -32.9481 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_0 | leaked_edges | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_0 | leakage_events | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_0 | utility_retention | 0.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_1 | leaked_edges | 1 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_1 | leakage_events | 1 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_1 | utility_retention | 0.0456 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_2 | leaked_edges | 2 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_2 | leakage_events | 2 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_2 | utility_retention | 0.0913 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_5 | leaked_edges | 3 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_5 | leakage_events | 3 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_5 | utility_retention | 0.374 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_10 | leaked_edges | 3 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_10 | leakage_events | 3 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_10 | utility_retention | 0.6141 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_1 | baseline_leaked_edges | 9 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_1 | baseline_retrieved_edges | 1956 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_1 | bounded_b5_leaked_edges | 3 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_1 | bounded_b5_retrieved_edges | 488 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_2 | baseline_leaked_edges | 12 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_2 | baseline_retrieved_edges | 2304 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_2 | bounded_b5_leaked_edges | 3 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_2 | bounded_b5_retrieved_edges | 774 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_3 | baseline_leaked_edges | 12 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_3 | baseline_retrieved_edges | 2304 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_3 | bounded_b5_leaked_edges | 3 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_3 | bounded_b5_retrieved_edges | 776 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | baseline | query_count | 6 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | baseline | retrieval_leaked_edges | 12 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | baseline | response_leaked_edges | 6 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | baseline | response_leaked_terms | 8 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | baseline | pipeline_ms | 39.6663 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | strict_guard | query_count | 2 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | strict_guard | retrieval_leaked_edges | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | strict_guard | response_leaked_edges | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | strict_guard | response_leaked_terms | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | strict_guard | pipeline_ms | 2.7263 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | bounded_b5 | query_count | 6 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | bounded_b5 | retrieval_leaked_edges | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | bounded_b5 | response_leaked_edges | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | bounded_b5 | response_leaked_terms | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | bounded_b5 | pipeline_ms | 10.7421 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.00 | corrupted_sensitive_edges | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.00 | retrieval_leaked_edges | 3 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.00 | response_leaked_edges | 3 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.00 | response_leaked_terms | 2 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.10 | corrupted_sensitive_edges | 1 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.10 | retrieval_leaked_edges | 4 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.10 | response_leaked_edges | 3 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.10 | response_leaked_terms | 4 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.25 | corrupted_sensitive_edges | 3 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.25 | retrieval_leaked_edges | 5 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.25 | response_leaked_edges | 6 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.25 | response_leaked_terms | 6 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.50 | corrupted_sensitive_edges | 5 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.50 | retrieval_leaked_edges | 5 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.50 | response_leaked_edges | 6 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.50 | response_leaked_terms | 6 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_template | adaptive_queries | 8 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_template | retrieval_leaked_edges | 12 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_template | response_leaked_edges | 6 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_template | response_leaked_terms | 8 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_local_abstractive | adaptive_queries | 8 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_local_abstractive | retrieval_leaked_edges | 12 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_local_abstractive | response_leaked_edges | 6 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_local_abstractive | response_leaked_terms | 8 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_evidence_dump | adaptive_queries | 8 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_evidence_dump | retrieval_leaked_edges | 12 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_evidence_dump | response_leaked_edges | 6 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_evidence_dump | response_leaked_terms | 8 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_template | adaptive_queries | 8 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_template | retrieval_leaked_edges | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_template | response_leaked_edges | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_template | response_leaked_terms | 2 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_local_abstractive | adaptive_queries | 8 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_local_abstractive | retrieval_leaked_edges | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_local_abstractive | response_leaked_edges | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_local_abstractive | response_leaked_terms | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_evidence_dump | adaptive_queries | 8 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_evidence_dump | retrieval_leaked_edges | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_evidence_dump | response_leaked_edges | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_evidence_dump | response_leaked_terms | 2 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | sydney_hotel_cloudvendor | baseline_relevant_edges | 1152 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | sydney_hotel_cloudvendor | defended_relevant_edges | 768 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | sydney_hotel_cloudvendor | precision | 1.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | sydney_hotel_cloudvendor | recall | 0.6667 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | sydney_hotel_cloudvendor | f1 | 0.8 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | diabetes_clinic_appointment | baseline_relevant_edges | 1152 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | diabetes_clinic_appointment | defended_relevant_edges | 96 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | diabetes_clinic_appointment | precision | 1.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | diabetes_clinic_appointment | recall | 0.0833 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | diabetes_clinic_appointment | f1 | 0.1538 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | payrollbank_vendor | baseline_relevant_edges | 1152 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | payrollbank_vendor | defended_relevant_edges | 97 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | payrollbank_vendor | precision | 1.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | payrollbank_vendor | recall | 0.0842 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | payrollbank_vendor | f1 | 0.1553 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | project-a_vendor | baseline_relevant_edges | 1152 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | project-a_vendor | defended_relevant_edges | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | project-a_vendor | precision | 1.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | project-a_vendor | recall | 0.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | project-a_vendor | f1 | 0.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_0 | leaked_edges_mean | 0.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_0 | leaked_edges_ci95_low | 0.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_0 | leaked_edges_ci95_high | 0.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_0 | utility_mean | 0.0011 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_0 | utility_ci95_low | 0.0004 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_0 | utility_ci95_high | 0.0018 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_1 | leaked_edges_mean | 1.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_1 | leaked_edges_ci95_low | 1.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_1 | leaked_edges_ci95_high | 1.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_1 | utility_mean | 0.0473 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_1 | utility_ci95_low | 0.0454 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_1 | utility_ci95_high | 0.0493 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_2 | leaked_edges_mean | 2.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_2 | leaked_edges_ci95_low | 2.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_2 | leaked_edges_ci95_high | 2.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_2 | utility_mean | 0.0936 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_2 | utility_ci95_low | 0.0901 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_2 | utility_ci95_high | 0.097 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_5 | leaked_edges_mean | 3.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_5 | leaked_edges_ci95_low | 3.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_5 | leaked_edges_ci95_high | 3.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_5 | utility_mean | 0.3776 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_5 | utility_ci95_low | 0.3711 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_5 | utility_ci95_high | 0.3841 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_10 | leaked_edges_mean | 3.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_10 | leaked_edges_ci95_low | 3.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_10 | leaked_edges_ci95_high | 3.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_10 | utility_mean | 0.605 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_10 | utility_ci95_low | 0.5939 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_10 | utility_ci95_high | 0.616 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | adaptive_probe | fixed_budget_6 | leaked_edges | 9 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | adaptive_probe | fixed_budget_6 | query_count | 6 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | adaptive_probe | adaptive_budget_6 | leaked_edges | 12 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | adaptive_probe | adaptive_budget_6 | query_count | 6 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | baseline_template | response_chars | 59468 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | baseline_template | leaked_edges | 6 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | baseline_template | leaked_secret_terms | 8 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | baseline_local_abstractive | response_chars | 244 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | baseline_local_abstractive | leaked_edges | 3 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | baseline_local_abstractive | leaked_secret_terms | 6 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b0_template | response_chars | 29 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b0_template | leaked_edges | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b0_template | leaked_secret_terms | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b0_local_abstractive | response_chars | 59 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b0_local_abstractive | leaked_edges | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b0_local_abstractive | leaked_secret_terms | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b5_template | response_chars | 12772 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b5_template | leaked_edges | 3 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b5_template | leaked_secret_terms | 2 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b5_local_abstractive | response_chars | 157 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b5_local_abstractive | leaked_edges | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b5_local_abstractive | leaked_secret_terms | 0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | openai | status | skipped_missing_openai_api_key | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | semantic_response_leakage | baseline | lexical_edges | 6 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | semantic_response_leakage | baseline | semantic_edges | 6 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | semantic_response_leakage | baseline | lexical_terms | 8 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | semantic_response_leakage | baseline | semantic_terms | 8 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | semantic_response_leakage | bounded_b5 | lexical_edges | 3 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | semantic_response_leakage | bounded_b5 | semantic_edges | 3 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | semantic_response_leakage | bounded_b5 | lexical_terms | 2 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | semantic_response_leakage | bounded_b5 | semantic_terms | 2 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | cosine | evaluated_users | 24 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | cosine | top1_accuracy | 0.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | cosine | top3_accuracy | 0.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | cosine | mrr | 0.0165 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | wl_kernel | evaluated_users | 24 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | wl_kernel | top1_accuracy | 0.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | wl_kernel | top3_accuracy | 0.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | wl_kernel | mrr | 0.0137 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | graph_edit | evaluated_users | 24 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | graph_edit | top1_accuracy | 0.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | graph_edit | top3_accuracy | 0.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | graph_edit | mrr | 0.015 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | embedding | evaluated_users | 24 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | embedding | top1_accuracy | 0.0417 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | embedding | top3_accuracy | 0.125 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | embedding | mrr | 0.1663 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | temporal_hidden | arrhythmia | pairwise_ordering_accuracy | 0.7155 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | temporal_hidden | CloudVendor | pairwise_ordering_accuracy | 0.6436 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | temporal_hidden | Project-A | pairwise_ordering_accuracy | 0.6057 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | temporal_hidden | Sydney | pairwise_ordering_accuracy | 0.6546 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_0.5 | candidate_edges | 160 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_0.5 | released_edges | 2280 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_0.5 | synthetic_absent_edges | 16 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_0.5 | per_edge_epsilon | 0.5 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_1.0 | candidate_edges | 160 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_1.0 | released_edges | 2288 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_1.0 | synthetic_absent_edges | 10 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_1.0 | per_edge_epsilon | 1.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_2.0 | candidate_edges | 160 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_2.0 | released_edges | 2294 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_2.0 | synthetic_absent_edges | 3 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_2.0 | per_edge_epsilon | 2.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_0.5 | present_emit_probability | 0.622459 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_0.5 | absent_emit_probability | 0.377541 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_0.5 | single_release_privacy_loss | 0.5 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_0.5_releases_1 | basic_composed_epsilon | 0.5 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_0.5_releases_5 | basic_composed_epsilon | 2.5 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_0.5_releases_10 | basic_composed_epsilon | 5.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_1.0 | present_emit_probability | 0.731059 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_1.0 | absent_emit_probability | 0.268941 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_1.0 | single_release_privacy_loss | 1.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_1.0_releases_1 | basic_composed_epsilon | 1.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_1.0_releases_5 | basic_composed_epsilon | 5.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_1.0_releases_10 | basic_composed_epsilon | 10.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_2.0 | present_emit_probability | 0.880797 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_2.0 | absent_emit_probability | 0.119203 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_2.0 | single_release_privacy_loss | 2.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_2.0_releases_1 | basic_composed_epsilon | 2.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_2.0_releases_5 | basic_composed_epsilon | 10.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_2.0_releases_10 | basic_composed_epsilon | 20.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_0.5_releases_1 | guarantee_scope | protected_candidate_edges_only | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_0.5_releases_1 | has_full_graph_dp | False | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_0.5_releases_1 | protected_release_epsilon | 576.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_0.5_releases_1 | guarantee_scope | full_graph_over_candidate_universe | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_0.5_releases_1 | has_full_graph_dp | True | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_0.5_releases_1 | protected_release_epsilon | 1152.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_0.5_releases_5 | guarantee_scope | protected_candidate_edges_only | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_0.5_releases_5 | has_full_graph_dp | False | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_0.5_releases_5 | protected_release_epsilon | 2880.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_0.5_releases_5 | guarantee_scope | full_graph_over_candidate_universe | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_0.5_releases_5 | has_full_graph_dp | True | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_0.5_releases_5 | protected_release_epsilon | 5760.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_1.0_releases_1 | guarantee_scope | protected_candidate_edges_only | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_1.0_releases_1 | has_full_graph_dp | False | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_1.0_releases_1 | protected_release_epsilon | 1152.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_1.0_releases_1 | guarantee_scope | full_graph_over_candidate_universe | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_1.0_releases_1 | has_full_graph_dp | True | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_1.0_releases_1 | protected_release_epsilon | 2304.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_1.0_releases_5 | guarantee_scope | protected_candidate_edges_only | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_1.0_releases_5 | has_full_graph_dp | False | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_1.0_releases_5 | protected_release_epsilon | 5760.0 | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_1.0_releases_5 | guarantee_scope | full_graph_over_candidate_universe | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_1.0_releases_5 | has_full_graph_dp | True | TIFS revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_1.0_releases_5 | protected_release_epsilon | 11520.0 | TIFS revision experiment. |
| graphmemshield | multiwoz_2_1 | dataset | multiwoz_2_1 | max_dialogues | 1000 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | dataset | multiwoz_2_1 | records | 6613 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | dataset | multiwoz_2_1 | users | 955 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | dataset | multiwoz_2_1 | sessions | 955 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | dataset | multiwoz_2_1 | nodes | 2708 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | dataset | multiwoz_2_1 | edges | 36408 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | cross_session_probe | baseline | queries | 8 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | cross_session_probe | baseline | leaked_edges | 67 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | cross_session_probe | baseline | leakage_events | 536 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | bounded_sharing | budget_0 | leaked_edges | 0 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | bounded_sharing | budget_0 | utility_retention | 0.0015 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | bounded_sharing | budget_1 | leaked_edges | 1 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | bounded_sharing | budget_1 | utility_retention | 0.0015 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | bounded_sharing | budget_2 | leaked_edges | 2 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | bounded_sharing | budget_2 | utility_retention | 0.0015 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | bounded_sharing | budget_5 | leaked_edges | 5 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | bounded_sharing | budget_5 | utility_retention | 0.0016 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | blackbox_response | baseline | response_chars | 1003929 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | blackbox_response | baseline | leaked_edges | 67 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | blackbox_response | baseline | leaked_terms | 5 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | blackbox_response | budget_0 | response_chars | 1890 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | blackbox_response | budget_0 | leaked_edges | 32 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | blackbox_response | budget_0 | leaked_terms | 2 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | blackbox_response | budget_5 | response_chars | 118618 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | blackbox_response | budget_5 | leaked_edges | 58 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | multiwoz_2_1 | blackbox_response | budget_5 | leaked_terms | 4 | External MultiWOZ 2.1 corpus run. |
| graphmemshield | enron_communication_graph | dataset | enron_maildir | source_mode | enron_style_fixture | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | dataset | enron_maildir | source_path | /Users/phatttt/Documents/Claude/Projects/GraphMemShield/data/enron_style_maildir | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | dataset | enron_maildir | records | 160 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | dataset | enron_maildir | users | 6 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | dataset | enron_maildir | sessions | 160 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | dataset | enron_maildir | nodes | 179 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | dataset | enron_maildir | edges | 447 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | communication_graph_probe | baseline | queries | 8 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | communication_graph_probe | baseline | leaked_edges | 3 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | communication_graph_probe | baseline | leakage_events | 24 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | communication_graph_probe | budget_0 | leaked_edges | 0 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | communication_graph_probe | budget_0 | utility_retention | 0.0083 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | communication_graph_probe | budget_1 | leaked_edges | 1 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | communication_graph_probe | budget_1 | utility_retention | 0.0083 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | communication_graph_probe | budget_2 | leaked_edges | 2 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | communication_graph_probe | budget_2 | utility_retention | 0.0083 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | communication_graph_probe | budget_5 | leaked_edges | 2 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | communication_graph_probe | budget_5 | utility_retention | 0.0083 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | baseline_template | lexical_edges | 2 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | baseline_template | semantic_edges | 2 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | baseline_template | lexical_terms | 5 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | baseline_template | semantic_terms | 5 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | baseline_evidence_dump | lexical_edges | 2 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | baseline_evidence_dump | semantic_edges | 2 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | baseline_evidence_dump | lexical_terms | 5 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | baseline_evidence_dump | semantic_terms | 5 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | budget_0_template | lexical_edges | 0 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | budget_0_template | semantic_edges | 0 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | budget_0_template | lexical_terms | 0 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | budget_0_template | semantic_terms | 0 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | budget_0_evidence_dump | lexical_edges | 0 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | budget_0_evidence_dump | semantic_edges | 0 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | budget_0_evidence_dump | lexical_terms | 0 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | budget_0_evidence_dump | semantic_terms | 0 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | budget_5_template | lexical_edges | 2 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | budget_5_template | semantic_edges | 2 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | budget_5_template | lexical_terms | 5 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | budget_5_template | semantic_terms | 5 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | budget_5_evidence_dump | lexical_edges | 2 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | budget_5_evidence_dump | semantic_edges | 2 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | budget_5_evidence_dump | lexical_terms | 5 | Enron maildir or Enron-style communication graph run. |
| graphmemshield | enron_communication_graph | semantic_response_leakage | budget_5_evidence_dump | semantic_terms | 5 | Enron maildir or Enron-style communication graph run. |

## Remaining Manual Work

- Replace de-identified sample data with additional approved public datasets where licensing permits.
- Run `examples/run_enron_experiment.py` against a full approved Enron maildir by setting `GRAPHMEMSHIELD_ENRON_MAILDIR`.
- Connect the property-graph adapter to a live Neo4j deployment for system-level latency and policy tests.
