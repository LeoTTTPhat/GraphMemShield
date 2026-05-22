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
| graphmemshield | enterprise_health_finance | dataset | enterprise_health_finance | records | 576 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dataset | enterprise_health_finance | users | 48 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dataset | enterprise_health_finance | sessions | 192 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dataset | enterprise_health_finance | nodes | 162 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dataset | enterprise_health_finance | edges | 2304 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | backend | sqlite_property_graph | nodes | 162 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | backend | sqlite_property_graph | edges | 2304 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | backend | sqlite_property_graph | sessions | 192 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | cross_session_probe | sqlite_property_graph | leaked_edges | 9 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | backend | kuzu_property_graph | available | False | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | backend | kuzu_property_graph | status | kuzu package unavailable | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_0 | leaked_edges | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_0 | leakage_events | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_0 | utility_retention | 0.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_1 | leaked_edges | 1 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_1 | leakage_events | 1 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_1 | utility_retention | 0.1925 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_2 | leaked_edges | 2 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_2 | leakage_events | 2 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_2 | utility_retention | 0.3819 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_5 | leaked_edges | 3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_5 | leakage_events | 3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_5 | utility_retention | 0.6667 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_10 | leaked_edges | 3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_10 | leakage_events | 3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing | budget_10 | utility_retention | 0.9048 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_1 | baseline_leaked_edges | 9 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_1 | baseline_retrieved_edges | 1956 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_1 | bounded_b5_leaked_edges | 3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_1 | bounded_b5_retrieved_edges | 488 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_2 | baseline_leaked_edges | 12 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_2 | baseline_retrieved_edges | 2304 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_2 | bounded_b5_leaked_edges | 3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_2 | bounded_b5_retrieved_edges | 774 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_3 | baseline_leaked_edges | 12 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_3 | baseline_retrieved_edges | 2304 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_3 | bounded_b5_leaked_edges | 3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | multihop_probe | hop_3 | bounded_b5_retrieved_edges | 777 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | baseline | query_count | 6 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | baseline | retrieval_leaked_edges | 12 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | baseline | response_leaked_edges | 6 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | baseline | response_leaked_terms | 8 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | baseline | pipeline_ms | 37.4496 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | strict_guard | query_count | 2 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | strict_guard | retrieval_leaked_edges | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | strict_guard | response_leaked_edges | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | strict_guard | response_leaked_terms | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | strict_guard | pipeline_ms | 2.6485 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | bounded_b5 | query_count | 6 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | bounded_b5 | retrieval_leaked_edges | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | bounded_b5 | response_leaked_edges | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | bounded_b5 | response_leaked_terms | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | hybrid_pipeline | bounded_b5 | pipeline_ms | 11.5624 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.00 | corrupted_sensitive_edges | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.00 | retrieval_leaked_edges | 3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.00 | response_leaked_edges | 3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.00 | response_leaked_terms | 2 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.10 | corrupted_sensitive_edges | 1 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.10 | retrieval_leaked_edges | 4 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.10 | response_leaked_edges | 3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.10 | response_leaked_terms | 4 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.25 | corrupted_sensitive_edges | 3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.25 | retrieval_leaked_edges | 5 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.25 | response_leaked_edges | 6 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.25 | response_leaked_terms | 6 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.50 | corrupted_sensitive_edges | 5 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.50 | retrieval_leaked_edges | 5 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.50 | response_leaked_edges | 6 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | provenance_error_robustness | sensitivity_error_0.50 | response_leaked_terms | 6 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_template | adaptive_queries | 8 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_template | retrieval_leaked_edges | 12 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_template | response_leaked_edges | 6 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_template | response_leaked_terms | 8 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_local_abstractive | adaptive_queries | 8 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_local_abstractive | retrieval_leaked_edges | 12 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_local_abstractive | response_leaked_edges | 6 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_local_abstractive | response_leaked_terms | 8 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_evidence_dump | adaptive_queries | 8 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_evidence_dump | retrieval_leaked_edges | 12 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_evidence_dump | response_leaked_edges | 6 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | baseline_evidence_dump | response_leaked_terms | 8 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_template | adaptive_queries | 8 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_template | retrieval_leaked_edges | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_template | response_leaked_edges | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_template | response_leaked_terms | 2 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_local_abstractive | adaptive_queries | 8 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_local_abstractive | retrieval_leaked_edges | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_local_abstractive | response_leaked_edges | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_local_abstractive | response_leaked_terms | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_evidence_dump | adaptive_queries | 8 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_evidence_dump | retrieval_leaked_edges | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_evidence_dump | response_leaked_edges | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | strong_generator | bounded_b5_evidence_dump | response_leaked_terms | 2 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | sydney_hotel_cloudvendor | baseline_relevant_edges | 1152 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | sydney_hotel_cloudvendor | defended_relevant_edges | 768 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | sydney_hotel_cloudvendor | precision | 1.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | sydney_hotel_cloudvendor | recall | 0.6667 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | sydney_hotel_cloudvendor | f1 | 0.8 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | diabetes_clinic_appointment | baseline_relevant_edges | 1152 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | diabetes_clinic_appointment | defended_relevant_edges | 528 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | diabetes_clinic_appointment | precision | 1.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | diabetes_clinic_appointment | recall | 0.4583 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | diabetes_clinic_appointment | f1 | 0.6286 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | payrollbank_vendor | baseline_relevant_edges | 1152 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | payrollbank_vendor | defended_relevant_edges | 144 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | payrollbank_vendor | precision | 1.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | payrollbank_vendor | recall | 0.125 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | payrollbank_vendor | f1 | 0.2222 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | project-a_vendor | baseline_relevant_edges | 1152 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | project-a_vendor | defended_relevant_edges | 144 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | project-a_vendor | precision | 1.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | project-a_vendor | recall | 0.125 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | utility_quality | project-a_vendor | f1 | 0.2222 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_0 | leaked_edges_mean | 0.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_0 | leaked_edges_ci95_low | 0.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_0 | leaked_edges_ci95_high | 0.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_0 | utility_mean | 0.0011 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_0 | utility_ci95_low | 0.0004 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_0 | utility_ci95_high | 0.0018 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_1 | leaked_edges_mean | 1.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_1 | leaked_edges_ci95_low | 1.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_1 | leaked_edges_ci95_high | 1.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_1 | utility_mean | 0.1925 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_1 | utility_ci95_low | 0.1925 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_1 | utility_ci95_high | 0.1925 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_2 | leaked_edges_mean | 2.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_2 | leaked_edges_ci95_low | 2.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_2 | leaked_edges_ci95_high | 2.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_2 | utility_mean | 0.3819 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_2 | utility_ci95_low | 0.3819 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_2 | utility_ci95_high | 0.3819 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_5 | leaked_edges_mean | 3.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_5 | leaked_edges_ci95_low | 3.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_5 | leaked_edges_ci95_high | 3.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_5 | utility_mean | 0.6667 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_5 | utility_ci95_low | 0.6667 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_5 | utility_ci95_high | 0.6667 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_10 | leaked_edges_mean | 3.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_10 | leaked_edges_ci95_low | 3.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_10 | leaked_edges_ci95_high | 3.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_10 | utility_mean | 0.9048 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_10 | utility_ci95_low | 0.9048 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | bounded_sharing_multiseed | budget_10 | utility_ci95_high | 0.9048 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | adaptive_probe | fixed_budget_6 | leaked_edges | 9 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | adaptive_probe | fixed_budget_6 | query_count | 6 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | adaptive_probe | adaptive_budget_6 | leaked_edges | 12 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | adaptive_probe | adaptive_budget_6 | query_count | 6 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | llm_adaptive_probe | openai | status | skipped_ModuleNotFoundError | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | baseline_template | response_chars | 59468 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | baseline_template | leaked_edges | 6 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | baseline_template | leaked_secret_terms | 8 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | baseline_local_abstractive | response_chars | 244 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | baseline_local_abstractive | leaked_edges | 3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | baseline_local_abstractive | leaked_secret_terms | 6 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b0_template | response_chars | 29 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b0_template | leaked_edges | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b0_template | leaked_secret_terms | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b0_local_abstractive | response_chars | 59 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b0_local_abstractive | leaked_edges | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b0_local_abstractive | leaked_secret_terms | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b5_template | response_chars | 12772 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b5_template | leaked_edges | 3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b5_template | leaked_secret_terms | 2 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b5_local_abstractive | response_chars | 157 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b5_local_abstractive | leaked_edges | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | bounded_b5_local_abstractive | leaked_secret_terms | 0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | blackbox_response | openai | status | skipped_RuntimeError | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | semantic_response_leakage | baseline | lexical_edges | 6 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | semantic_response_leakage | baseline | semantic_edges | 6 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | semantic_response_leakage | baseline | lexical_terms | 8 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | semantic_response_leakage | baseline | semantic_terms | 8 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | semantic_response_leakage | bounded_b5 | lexical_edges | 3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | semantic_response_leakage | bounded_b5 | semantic_edges | 3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | semantic_response_leakage | bounded_b5 | lexical_terms | 2 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | semantic_response_leakage | bounded_b5 | semantic_terms | 2 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | cosine | evaluated_users | 24 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | cosine | top1_accuracy | 0.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | cosine | top3_accuracy | 0.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | cosine | mrr | 0.0165 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | wl_kernel | evaluated_users | 24 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | wl_kernel | top1_accuracy | 0.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | wl_kernel | top3_accuracy | 0.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | wl_kernel | mrr | 0.0137 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | graph_edit | evaluated_users | 24 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | graph_edit | top1_accuracy | 0.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | graph_edit | top3_accuracy | 0.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | graph_edit | mrr | 0.015 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | embedding | evaluated_users | 24 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | embedding | top1_accuracy | 0.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | embedding | top3_accuracy | 0.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | embedding | mrr | 0.0191 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | learned_logreg | evaluated_users | 24 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | learned_logreg | top1_accuracy | 1.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | learned_logreg | top3_accuracy | 1.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | session_link | learned_logreg | mrr | 1.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | global | retrieved_edges | 2304 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | global | leaked_edges | 12 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | global | response_leaked_edges | 6 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | global | response_leaked_terms | 8 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | global | qa_accuracy | 1.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | graphmemguard_bounded5 | retrieved_edges | 681 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | graphmemguard_bounded5 | leaked_edges | 3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | graphmemguard_bounded5 | response_leaked_edges | 3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | graphmemguard_bounded5 | response_leaked_terms | 2 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | graphmemguard_bounded5 | qa_accuracy | 0.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | posthoc_response_redaction | retrieved_edges | 2304 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | posthoc_response_redaction | leaked_edges | 12 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | posthoc_response_redaction | response_leaked_edges | 3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | posthoc_response_redaction | response_leaked_terms | 6 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | posthoc_response_redaction | qa_accuracy | 1.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | local_dp_suppression_eps0.5 | retrieved_edges | 1838 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | local_dp_suppression_eps0.5 | leaked_edges | 9 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | local_dp_suppression_eps0.5 | response_leaked_edges | 4 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | local_dp_suppression_eps0.5 | response_leaked_terms | 8 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | local_dp_suppression_eps0.5 | qa_accuracy | 1.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | fixed_universe_rr_eps0.5 | retrieved_edges | 2271 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | fixed_universe_rr_eps0.5 | leaked_edges | 13 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | fixed_universe_rr_eps0.5 | response_leaked_edges | 5 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | fixed_universe_rr_eps0.5 | response_leaked_terms | 10 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | fixed_universe_rr_eps0.5 | qa_accuracy | 1.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | local_dp_suppression_eps1.0 | retrieved_edges | 1980 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | local_dp_suppression_eps1.0 | leaked_edges | 10 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | local_dp_suppression_eps1.0 | response_leaked_edges | 5 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | local_dp_suppression_eps1.0 | response_leaked_terms | 8 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | local_dp_suppression_eps1.0 | qa_accuracy | 1.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | fixed_universe_rr_eps1.0 | retrieved_edges | 2282 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | fixed_universe_rr_eps1.0 | leaked_edges | 11 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | fixed_universe_rr_eps1.0 | response_leaked_edges | 5 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | fixed_universe_rr_eps1.0 | response_leaked_terms | 9 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | fixed_universe_rr_eps1.0 | qa_accuracy | 1.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | local_dp_suppression_eps2.0 | retrieved_edges | 2164 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | local_dp_suppression_eps2.0 | leaked_edges | 10 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | local_dp_suppression_eps2.0 | response_leaked_edges | 5 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | local_dp_suppression_eps2.0 | response_leaked_terms | 8 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | local_dp_suppression_eps2.0 | qa_accuracy | 1.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | fixed_universe_rr_eps2.0 | retrieved_edges | 2292 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | fixed_universe_rr_eps2.0 | leaked_edges | 10 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | fixed_universe_rr_eps2.0 | response_leaked_edges | 5 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | fixed_universe_rr_eps2.0 | response_leaked_terms | 8 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | frontier_privacy_baselines | fixed_universe_rr_eps2.0 | qa_accuracy | 1.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D2_eps0.5 | accuracy_mean | 0.1512 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D2_eps0.5 | accuracy_ci95_low | 0.1253 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D2_eps0.5 | accuracy_ci95_high | 0.177 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D2_eps0.5 | cross_session_accuracy_mean | 0.0833 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D2_eps0.5 | cross_session_accuracy_ci95_low | -0.0045 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D2_eps0.5 | cross_session_accuracy_ci95_high | 0.1711 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D2_eps0.5 | leaked_edges_mean | 2.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D2_eps0.5 | leaked_edges_ci95_low | 2.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D2_eps0.5 | leaked_edges_ci95_high | 2.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D2_eps0.5 | mean_margin | 0.5372 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D2_eps2.0 | accuracy_mean | 0.1744 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D2_eps2.0 | accuracy_ci95_low | 0.1555 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D2_eps2.0 | accuracy_ci95_high | 0.1933 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D2_eps2.0 | cross_session_accuracy_mean | 0.2 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D2_eps2.0 | cross_session_accuracy_ci95_low | 0.1185 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D2_eps2.0 | cross_session_accuracy_ci95_high | 0.2815 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D2_eps2.0 | leaked_edges_mean | 2.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D2_eps2.0 | leaked_edges_ci95_low | 2.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D2_eps2.0 | leaked_edges_ci95_high | 2.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D2_eps2.0 | mean_margin | 0.5372 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D4_eps1.0 | accuracy_mean | 0.1512 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D4_eps1.0 | accuracy_ci95_low | 0.1297 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D4_eps1.0 | accuracy_ci95_high | 0.1727 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D4_eps1.0 | cross_session_accuracy_mean | 0.1 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D4_eps1.0 | cross_session_accuracy_ci95_low | 0.0129 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D4_eps1.0 | cross_session_accuracy_ci95_high | 0.1871 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D4_eps1.0 | leaked_edges_mean | 4.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D4_eps1.0 | leaked_edges_ci95_low | 4.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D4_eps1.0 | leaked_edges_ci95_high | 4.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D4_eps1.0 | mean_margin | 0.7814 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D4_eps4.0 | accuracy_mean | 0.1733 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D4_eps4.0 | accuracy_ci95_low | 0.1428 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D4_eps4.0 | accuracy_ci95_high | 0.2037 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D4_eps4.0 | cross_session_accuracy_mean | 0.1167 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D4_eps4.0 | cross_session_accuracy_ci95_low | 0.0316 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D4_eps4.0 | cross_session_accuracy_ci95_high | 0.2017 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D4_eps4.0 | leaked_edges_mean | 4.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D4_eps4.0 | leaked_edges_ci95_low | 4.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D4_eps4.0 | leaked_edges_ci95_high | 4.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D4_eps4.0 | mean_margin | 0.7814 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D8_eps2.0 | accuracy_mean | 0.1791 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D8_eps2.0 | accuracy_ci95_low | 0.1548 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D8_eps2.0 | accuracy_ci95_high | 0.2034 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D8_eps2.0 | cross_session_accuracy_mean | 0.2167 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D8_eps2.0 | cross_session_accuracy_ci95_low | 0.1187 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D8_eps2.0 | cross_session_accuracy_ci95_high | 0.3147 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D8_eps2.0 | leaked_edges_mean | 5.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D8_eps2.0 | leaked_edges_ci95_low | 5.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D8_eps2.0 | leaked_edges_ci95_high | 5.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D8_eps2.0 | mean_margin | 1.243 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D8_deterministic_ceiling | accuracy_mean | 0.6128 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D8_deterministic_ceiling | accuracy_ci95_low | 0.5757 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D8_deterministic_ceiling | accuracy_ci95_high | 0.6499 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D8_deterministic_ceiling | cross_session_accuracy_mean | 0.6333 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D8_deterministic_ceiling | cross_session_accuracy_ci95_low | 0.568 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D8_deterministic_ceiling | cross_session_accuracy_ci95_high | 0.6987 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | dp_graphqa | D8_deterministic_ceiling | leaked_edges_mean | 3.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_utility_frontier | enterprise_graphqa | cross_session_questions | 40 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_utility_frontier | enterprise_graphqa | fitted_reuse_factor_rho | 9.3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_utility_frontier | enterprise_graphqa | max_gap_to_lower_bound | 1.0568 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_utility_frontier | enterprise_graphqa | mean_gap_to_lower_bound | 1.0034 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | rho_structural_proxy | enterprise_graphqa | bridge_degree_proxy | 9.1 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | rho_structural_proxy | enterprise_graphqa | fitted_reuse_factor_rho | 9.3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | rho_structural_proxy | enterprise_graphqa | multiplicative_gap | 1.022 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | rho_structural_proxy | public_http_trace | bridge_degree_proxy | 12.7 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | rho_structural_proxy | public_http_trace | fitted_reuse_factor_rho | 13.1 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | rho_structural_proxy | public_http_trace | multiplicative_gap | 1.0315 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | rho_structural_proxy | internal_rag_trace | bridge_degree_proxy | 8.4 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | rho_structural_proxy | internal_rag_trace | fitted_reuse_factor_rho | 8.8 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | rho_structural_proxy | internal_rag_trace | multiplicative_gap | 1.0476 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | rho_structural_proxy | langgraph_adapter | bridge_degree_proxy | 9.1 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | rho_structural_proxy | langgraph_adapter | fitted_reuse_factor_rho | 9.3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | rho_structural_proxy | langgraph_adapter | multiplicative_gap | 1.022 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | rho_structural_proxy | mem0_sample | bridge_degree_proxy | 3.8 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | rho_structural_proxy | mem0_sample | fitted_reuse_factor_rho | 4.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | rho_structural_proxy | mem0_sample | multiplicative_gap | 1.0526 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | rho_structural_proxy | enron_style_graph | bridge_degree_proxy | 6.2 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | rho_structural_proxy | enron_style_graph | fitted_reuse_factor_rho | 6.6 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | rho_structural_proxy | enron_style_graph | multiplicative_gap | 1.0645 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | continual_release_accounting | T100 | linear_expected_abs_error | 100.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | continual_release_accounting | T100 | binary_tree_expected_abs_error | 18.5203 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | continual_release_accounting | T100 | error_reduction_factor | 5.3995 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | continual_release_accounting | T1000 | linear_expected_abs_error | 1000.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | continual_release_accounting | T1000 | binary_tree_expected_abs_error | 31.6228 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | continual_release_accounting | T1000 | error_reduction_factor | 31.6228 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | continual_release_accounting | T10000 | linear_expected_abs_error | 10000.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | continual_release_accounting | T10000 | binary_tree_expected_abs_error | 52.3832 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | continual_release_accounting | T10000 | error_reduction_factor | 190.9009 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | learned_link_privacy_curve | structural_embedding_baseline | top1_accuracy | 0.042 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | learned_link_privacy_curve | structural_embedding_baseline | top3_accuracy | 0.125 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | learned_link_privacy_curve | structural_embedding_baseline | mrr | 0.166 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | learned_link_privacy_curve | enterprise_to_public_http_transfer | top1_accuracy | 0.09 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | learned_link_privacy_curve | enterprise_to_public_http_transfer | top3_accuracy | 0.18 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | learned_link_privacy_curve | enterprise_to_public_http_transfer | mrr | 0.136 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | learned_link_privacy_curve | enterprise_to_internal_rag_transfer | top1_accuracy | 0.11 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | learned_link_privacy_curve | enterprise_to_internal_rag_transfer | top3_accuracy | 0.22 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | learned_link_privacy_curve | enterprise_to_internal_rag_transfer | mrr | 0.158 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | learned_link_privacy_curve | enterprise_to_enron_transfer | top1_accuracy | 0.08 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | learned_link_privacy_curve | enterprise_to_enron_transfer | top3_accuracy | 0.17 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | learned_link_privacy_curve | enterprise_to_enron_transfer | mrr | 0.128 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | certified_radius | neighbor_shadow | certified_flip_radius | 2 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | certified_radius | neighbor_shadow | first_sensitive_exposure_flips | 3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | certified_radius | neighbor_shadow | leakage_at_or_below_radius | 3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | certified_radius | neighbor_shadow | leakage_after_breakpoint | 4 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | temporal_hidden | arrhythmia | pairwise_ordering_accuracy | 0.7155 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | temporal_hidden | CloudVendor | pairwise_ordering_accuracy | 0.6436 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | temporal_hidden | Project-A | pairwise_ordering_accuracy | 0.6057 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | temporal_hidden | Sydney | pairwise_ordering_accuracy | 0.6546 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_0.5 | candidate_edges | 160 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_0.5 | released_edges | 2280 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_0.5 | synthetic_absent_edges | 16 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_0.5 | per_edge_epsilon | 0.5 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_1.0 | candidate_edges | 160 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_1.0 | released_edges | 2288 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_1.0 | synthetic_absent_edges | 10 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_1.0 | per_edge_epsilon | 1.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_2.0 | candidate_edges | 160 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_2.0 | released_edges | 2294 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_2.0 | synthetic_absent_edges | 3 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | fixed_universe_dp | epsilon_2.0 | per_edge_epsilon | 2.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_0.5 | present_emit_probability | 0.622459 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_0.5 | absent_emit_probability | 0.377541 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_0.5 | single_release_privacy_loss | 0.5 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_0.5_releases_1 | basic_composed_epsilon | 0.5 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_0.5_releases_5 | basic_composed_epsilon | 2.5 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_0.5_releases_10 | basic_composed_epsilon | 5.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_1.0 | present_emit_probability | 0.731059 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_1.0 | absent_emit_probability | 0.268941 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_1.0 | single_release_privacy_loss | 1.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_1.0_releases_1 | basic_composed_epsilon | 1.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_1.0_releases_5 | basic_composed_epsilon | 5.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_1.0_releases_10 | basic_composed_epsilon | 10.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_2.0 | present_emit_probability | 0.880797 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_2.0 | absent_emit_probability | 0.119203 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_2.0 | single_release_privacy_loss | 2.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_2.0_releases_1 | basic_composed_epsilon | 2.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_2.0_releases_5 | basic_composed_epsilon | 10.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | privacy_accounting | epsilon_2.0_releases_10 | basic_composed_epsilon | 20.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_0.5_releases_1 | guarantee_scope | protected_candidate_edges_only | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_0.5_releases_1 | has_full_graph_dp | False | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_0.5_releases_1 | protected_release_epsilon | 576.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_0.5_releases_1 | guarantee_scope | full_graph_over_candidate_universe | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_0.5_releases_1 | has_full_graph_dp | True | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_0.5_releases_1 | protected_release_epsilon | 1152.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_0.5_releases_5 | guarantee_scope | protected_candidate_edges_only | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_0.5_releases_5 | has_full_graph_dp | False | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_0.5_releases_5 | protected_release_epsilon | 2880.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_0.5_releases_5 | guarantee_scope | full_graph_over_candidate_universe | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_0.5_releases_5 | has_full_graph_dp | True | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_0.5_releases_5 | protected_release_epsilon | 5760.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_1.0_releases_1 | guarantee_scope | protected_candidate_edges_only | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_1.0_releases_1 | has_full_graph_dp | False | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_1.0_releases_1 | protected_release_epsilon | 1152.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_1.0_releases_1 | guarantee_scope | full_graph_over_candidate_universe | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_1.0_releases_1 | has_full_graph_dp | True | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_1.0_releases_1 | protected_release_epsilon | 2304.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_1.0_releases_5 | guarantee_scope | protected_candidate_edges_only | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_1.0_releases_5 | has_full_graph_dp | False | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | scoped_epsilon_1.0_releases_5 | protected_release_epsilon | 5760.0 | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_1.0_releases_5 | guarantee_scope | full_graph_over_candidate_universe | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_1.0_releases_5 | has_full_graph_dp | True | CIKM revision experiment. |
| graphmemshield | enterprise_health_finance | full_graph_privacy | full_epsilon_1.0_releases_5 | protected_release_epsilon | 11520.0 | CIKM revision experiment. |
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
| langgraph_agent_memory | enterprise_health_finance | dataset | langgraph | framework | LangGraph | Real LangGraph StateGraph memory workflow over the enterprise sensitive graph. |
| langgraph_agent_memory | enterprise_health_finance | dataset | langgraph | framework_available | True | Real LangGraph StateGraph memory workflow over the enterprise sensitive graph. |
| langgraph_agent_memory | enterprise_health_finance | dataset | langgraph | records | 576 | Real LangGraph StateGraph memory workflow over the enterprise sensitive graph. |
| langgraph_agent_memory | enterprise_health_finance | dataset | langgraph | users | 48 | Real LangGraph StateGraph memory workflow over the enterprise sensitive graph. |
| langgraph_agent_memory | enterprise_health_finance | dataset | langgraph | sessions | 192 | Real LangGraph StateGraph memory workflow over the enterprise sensitive graph. |
| langgraph_agent_memory | enterprise_health_finance | dataset | langgraph | edges | 2304 | Real LangGraph StateGraph memory workflow over the enterprise sensitive graph. |
| langgraph_agent_memory | enterprise_health_finance | langgraph_end_to_end | global | retrieved_edges | 2304 | Real LangGraph StateGraph memory workflow over the enterprise sensitive graph. |
| langgraph_agent_memory | enterprise_health_finance | langgraph_end_to_end | global | leaked_edges | 12 | Real LangGraph StateGraph memory workflow over the enterprise sensitive graph. |
| langgraph_agent_memory | enterprise_health_finance | langgraph_end_to_end | global | response_leaked_edges | 6 | Real LangGraph StateGraph memory workflow over the enterprise sensitive graph. |
| langgraph_agent_memory | enterprise_health_finance | langgraph_end_to_end | global | response_leaked_terms | 8 | Real LangGraph StateGraph memory workflow over the enterprise sensitive graph. |
| langgraph_agent_memory | enterprise_health_finance | langgraph_end_to_end | global | qa_accuracy | 1.0 | Real LangGraph StateGraph memory workflow over the enterprise sensitive graph. |
| langgraph_agent_memory | enterprise_health_finance | langgraph_end_to_end | owner_only | retrieved_edges | 0 | Real LangGraph StateGraph memory workflow over the enterprise sensitive graph. |
| langgraph_agent_memory | enterprise_health_finance | langgraph_end_to_end | owner_only | leaked_edges | 0 | Real LangGraph StateGraph memory workflow over the enterprise sensitive graph. |
| langgraph_agent_memory | enterprise_health_finance | langgraph_end_to_end | owner_only | response_leaked_edges | 0 | Real LangGraph StateGraph memory workflow over the enterprise sensitive graph. |
| langgraph_agent_memory | enterprise_health_finance | langgraph_end_to_end | owner_only | response_leaked_terms | 0 | Real LangGraph StateGraph memory workflow over the enterprise sensitive graph. |
| langgraph_agent_memory | enterprise_health_finance | langgraph_end_to_end | owner_only | qa_accuracy | 0.0 | Real LangGraph StateGraph memory workflow over the enterprise sensitive graph. |
| langgraph_agent_memory | enterprise_health_finance | langgraph_end_to_end | bounded5 | retrieved_edges | 681 | Real LangGraph StateGraph memory workflow over the enterprise sensitive graph. |
| langgraph_agent_memory | enterprise_health_finance | langgraph_end_to_end | bounded5 | leaked_edges | 3 | Real LangGraph StateGraph memory workflow over the enterprise sensitive graph. |
| langgraph_agent_memory | enterprise_health_finance | langgraph_end_to_end | bounded5 | response_leaked_edges | 3 | Real LangGraph StateGraph memory workflow over the enterprise sensitive graph. |
| langgraph_agent_memory | enterprise_health_finance | langgraph_end_to_end | bounded5 | response_leaked_terms | 2 | Real LangGraph StateGraph memory workflow over the enterprise sensitive graph. |
| langgraph_agent_memory | enterprise_health_finance | langgraph_end_to_end | bounded5 | qa_accuracy | 1.0 | Real LangGraph StateGraph memory workflow over the enterprise sensitive graph. |
| mem0_agent_memory | enterprise_health_finance | dataset | mem0 | framework | Mem0 | Real Mem0 memory integration with local Qdrant storage and OpenAI embeddings. |
| mem0_agent_memory | enterprise_health_finance | dataset | mem0 | framework_available | True | Real Mem0 memory integration with local Qdrant storage and OpenAI embeddings. |
| mem0_agent_memory | enterprise_health_finance | dataset | mem0 | indexed_edges | 40 | Real Mem0 memory integration with local Qdrant storage and OpenAI embeddings. |
| mem0_agent_memory | enterprise_health_finance | dataset | mem0 | victim_indexed_edges | 12 | Real Mem0 memory integration with local Qdrant storage and OpenAI embeddings. |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | global | retrieved_edges | 24 | Real Mem0 memory integration with local Qdrant storage and OpenAI embeddings. |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | global | leaked_edges | 10 | Real Mem0 memory integration with local Qdrant storage and OpenAI embeddings. |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | global | response_leaked_edges | 6 | Real Mem0 memory integration with local Qdrant storage and OpenAI embeddings. |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | global | response_leaked_terms | 8 | Real Mem0 memory integration with local Qdrant storage and OpenAI embeddings. |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | global | qa_accuracy | 1.0 | Real Mem0 memory integration with local Qdrant storage and OpenAI embeddings. |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | owner_only | retrieved_edges | 7 | Real Mem0 memory integration with local Qdrant storage and OpenAI embeddings. |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | owner_only | leaked_edges | 0 | Real Mem0 memory integration with local Qdrant storage and OpenAI embeddings. |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | owner_only | response_leaked_edges | 0 | Real Mem0 memory integration with local Qdrant storage and OpenAI embeddings. |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | owner_only | response_leaked_terms | 0 | Real Mem0 memory integration with local Qdrant storage and OpenAI embeddings. |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | owner_only | qa_accuracy | 1.0 | Real Mem0 memory integration with local Qdrant storage and OpenAI embeddings. |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | bounded5 | retrieved_edges | 10 | Real Mem0 memory integration with local Qdrant storage and OpenAI embeddings. |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | bounded5 | leaked_edges | 3 | Real Mem0 memory integration with local Qdrant storage and OpenAI embeddings. |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | bounded5 | response_leaked_edges | 3 | Real Mem0 memory integration with local Qdrant storage and OpenAI embeddings. |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | bounded5 | response_leaked_terms | 2 | Real Mem0 memory integration with local Qdrant storage and OpenAI embeddings. |
| mem0_agent_memory | enterprise_health_finance | mem0_end_to_end | bounded5 | qa_accuracy | 1.0 | Real Mem0 memory integration with local Qdrant storage and OpenAI embeddings. |
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
- Reproduce the public HTTP trace with `examples/run_deployed_graphrag_trace.py`.
- Reproduce the LangGraph memory integration with `examples/run_langgraph_memory_experiment.py`.
- Reproduce the Mem0 memory integration with `examples/run_mem0_memory_experiment.py` when `OPENAI_API_KEY` is configured.
- Reproduce the approved internal HTTP trace by converting the TraceKG export, setting `GRAPHMEMSHIELD_PRODUCTION_GRAPHRAG_JSONL`, and running `examples/run_deployed_graphrag_trace.py`.
- Run `examples/run_enron_experiment.py` against a full approved Enron maildir by setting `GRAPHMEMSHIELD_ENRON_MAILDIR`.
- Connect the property-graph adapter to a live Neo4j deployment for system-level latency and policy tests.
