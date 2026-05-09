# GraphMemShield Paper-Ready Tables

These tables summarize the current runnable artifact results in a compact format suitable for a draft paper. Values are generated from the current files under `Ideas/GraphMemShield/output`.

## Table 1: Implemented Evaluation Systems

| System | Dataset | Execution Mode | Records | Users | Sessions | Nodes | Edges |
|---|---|---:|---:|---:|---:|---:|---:|
| In-memory simulator | synthetic_multisession | local Python | n/a | n/a | n/a | synthetic | synthetic |
| PrivacyGuard Docker | seed_records | Docker + Mongo + Cloud API | 3 | 2 | 3 | 15 | 15 |
| PrivacyGuard Docker | sample_dialogues | Docker + Mongo + Cloud API | 12 | 6 | 12 | 36 | 48 |

## Table 2: Cross-Session Leakage and Defense

| System | Dataset | Condition | Query Budget | Leaked Edges | Leakage Reduction |
|---|---|---|---:|---:|---:|
| In-memory simulator | synthetic_multisession | baseline | n/a | 2 | n/a |
| In-memory simulator | synthetic_multisession | strict_guard | n/a | 0 | 1.0 |
| PrivacyGuard Docker | seed_records | baseline | n/a | 5 | n/a |
| PrivacyGuard Docker | seed_records | strict_guard | n/a | 0 | 1.0 |
| PrivacyGuard Docker | sample_dialogues | baseline | all | 48 | n/a |
| PrivacyGuard Docker | sample_dialogues | strict_guard | all | 0 | 1.0 |

Note: `strict_guard` means strict provenance/session isolation. It blocks cross-session retrieval before graph expansion, so the result should be interpreted as an isolation baseline, not proof of a novel privacy mechanism.

## Table 3: Query-Budget Curve

| System | Dataset | Attack | Budget | Query Count | Unique Leaked Edges | Leakage Events |
|---|---|---|---:|---:|---:|---:|
| PrivacyGuard Docker | sample_dialogues | CrossSessionProbe | 1 | 12 | 48 | 48 |
| PrivacyGuard Docker | sample_dialogues | CrossSessionProbe | 2 | 24 | 48 | 88 |
| PrivacyGuard Docker | sample_dialogues | CrossSessionProbe | 4 | 48 | 48 | 132 |
| PrivacyGuard Docker | sample_dialogues | CrossSessionProbe | all | 48 | 48 | 132 |

Interpretation: one entity-level query per session is already sufficient to expose all victim-owned edges in the current de-identified sample graph under the baseline retrieval policy.

## Table 4: Session Linking

| System | Dataset | Feature Condition | Evaluated Users | Top-1 Accuracy | Top-3 Accuracy | MRR |
|---|---|---|---:|---:|---:|---:|
| PrivacyGuard Docker | sample_dialogues | structure_only | 6 | 0.3333 | 1.0 | 0.6111 |
| PrivacyGuard Docker | sample_dialogues | semantic_labels | 6 | 0.3333 | 1.0 | 0.6667 |

Interpretation: structure-only matching is weak at top-1 on this small dataset, but the correct linked session appears within the top 3 for all evaluated users. Semantic labels improve MRR but do not change top-1 accuracy.

## Table 5: Temporal Path Exposure Baseline

| System | Dataset | Condition | Evaluated Sessions | Prefix Ordering Accuracy | Pairwise Ordering Accuracy | Edge Precision | Edge Recall | Edge F1 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| PrivacyGuard Docker | sample_dialogues | timestamp_order | 12 | 0.5 | 1.0 | 0.4925 | 1.0 | 0.6563 |

Interpretation: this is a timestamp/provenance exposure baseline. It measures whether retrieved edges preserve write-time metadata, not whether a model can infer hidden temporal order.

## Table 6: Edge Admission Proxy

| System | Dataset | Epsilon | Sensitive Keep Probability | Admitted Sensitive Edges | Victim Leaked Edges |
|---|---|---:|---:|---:|---:|
| In-memory simulator | synthetic_multisession | 0.1 | 0.5250 | 3 | 1 |
| In-memory simulator | synthetic_multisession | 1.0 | 0.7311 | 3 | 1 |
| In-memory simulator | synthetic_multisession | 3.0 | 0.9526 | 5 | 2 |

Interpretation: this is a seeded proxy for write-time edge admission, not a complete formal differentially private mechanism.

## Table 7: Current Artifact Coverage

| Component | Status | Evidence |
|---|---|---|
| Synthetic attack suite | implemented | `synthetic_experiments.*` |
| Docker-backed system experiment | implemented | `privacyguard_docker_experiment.*` |
| Batch Docker experiment | implemented | `privacyguard_batch_results.*` |
| Aggregate report | implemented | `aggregate_results.*` |
| Unit tests | passing | 22 pytest cases passing in the local verification environment |
| Release hygiene | implemented | `.gitignore`, `LICENSE`, `CITATION.cff`, `pyproject.toml`, CI workflow template |
| Public large-dataset ingestion | pending | requires PersonaChat/MultiWOZ/Enron or approved export |
| Real response scoring | pending | requires system response endpoint |
| Formal DP accounting | pending | requires finalized adjacency definition |
