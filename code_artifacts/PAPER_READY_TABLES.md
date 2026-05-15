# GraphMemShield Paper-Ready Tables

These tables summarize the current runnable artifact results in a compact format suitable for a draft paper. Values are generated from the current files under `Ideas/GraphMemShield/output`.

## Table 1: Implemented Evaluation Systems

| System | Dataset | Execution Mode | Records | Users | Sessions | Nodes | Edges |
|---|---|---:|---:|---:|---:|---:|---:|
| In-memory simulator | synthetic_multisession | local Python | n/a | 20 | 60 | 134 | 159 |
| PrivacyGuard Docker | seed_records | Docker + Mongo + Cloud API | 3 | 2 | 3 | 15 | 15 |
| PrivacyGuard Docker | sample_dialogues | Docker + Mongo + Cloud API | 12 | 6 | 12 | 36 | 48 |

## Table 2: Cross-Session Leakage and Defense

| System | Dataset | Condition | Query Budget | Leaked Edges | Leakage Reduction |
|---|---|---|---:|---:|---:|
| In-memory simulator | synthetic_multisession | baseline | n/a | 3 | n/a |
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

| System | Dataset | Epsilon | Sensitive Keep Probability | Victim Leaked Edges Mean | Victim Leaked Edges Std | Utility Retention Mean |
|---|---|---:|---:|---:|---:|---:|
| In-memory simulator | synthetic_multisession | 0.1 | 0.5250 | 1.0000 | 0.9826 | 1.0000 |
| In-memory simulator | synthetic_multisession | 1.0 | 0.7311 | 1.7667 | 1.1943 | 1.0000 |
| In-memory simulator | synthetic_multisession | 3.0 | 0.9526 | 2.7333 | 0.6397 | 1.0000 |

Interpretation: this is a seeded proxy for write-time edge admission, not a differentially private mechanism.

## Table 7: Current Artifact Coverage

| Component | Status | Evidence |
|---|---|---|
| Synthetic attack suite | implemented | `synthetic_experiments.*` |
| Docker-backed system experiment | implemented | `privacyguard_docker_experiment.*` |
| Batch Docker experiment | implemented | `privacyguard_batch_results.*` |
| Aggregate report | implemented | `aggregate_results.*` |
| Unit tests | passing | 41 pytest cases passing in the local verification environment |
| Release hygiene | implemented | `.gitignore`, `LICENSE`, `CITATION.cff`, `pyproject.toml`, CI workflow template |
| Public-format ingestion | implemented | MultiWOZ 2.1 upstream run plus Enron maildir loader with tests |
| Black-box response scoring | implemented | deterministic response-level scorer in `tifs_revision_results.*` |
| Fixed-universe DP release/accounting | implemented baseline | randomized response over 160 candidate protected edges with single-release, full-graph scope, and basic composition accounting |

## Table 8: TIFS Revision Experiments

| Component | Metric | Value |
|---|---:|---:|
| Enterprise/health/finance benchmark | Records | 576 |
| Enterprise/health/finance benchmark | Users | 48 |
| Enterprise/health/finance benchmark | Sessions | 192 |
| Enterprise/health/finance benchmark | Edges | 2304 |
| SQLite property graph | Roundtrip edges | 2304 |
| Kuzu property graph | Roundtrip edges | 2304 |
| Adaptive probe, budget 6 | Fixed leaked edges | 9 |
| Adaptive probe, budget 6 | Adaptive leaked edges | 12 |
| Black-box response baseline | Leaked victim edges | 12 |
| Black-box local abstractive baseline | Leaked victim edges | 9 |
| Black-box response bounded `b=0` | Leaked victim edges | 0 |
| Black-box response bounded `b=5` | Leaked victim edges | 3 |
| Bounded sharing `b=10` | Utility retention | 0.6141 |
| Multi-seed bounded `b=10` | Utility mean / 95% CI | 0.6050 / [0.5939, 0.6160] |
| Timestamp-hidden temporal inference | Pairwise accuracy range | 0.6057-0.7155 |
| Fixed-universe randomized response | Candidate protected edges | 160 |

Interpretation: these results address the reviewer-requested larger realistic benchmark, public-format ingestion, Kuzu/property-graph roundtrip, adaptive probing, multi-seed confidence intervals, black-box response scoring, stronger attack baselines, bounded-sharing emphasis, and fixed-universe DP mechanism.

## Table 9: MultiWOZ External Corpus Run

| Metric | Value |
|---|---:|
| Dialogue cap | 1000 |
| Records | 6613 |
| Users/dialogues | 955 |
| Sessions | 955 |
| Nodes | 2708 |
| Edges | 36408 |
| Baseline leaked edges | 67 |
| Baseline leakage events | 536 |
| Bounded `b=0` leaked edges | 0 |
| Bounded `b=5` leaked edges | 5 |
| Black-box baseline leaked edges | 67 |

Interpretation: this is an end-to-end run on public MultiWOZ 2.1 data downloaded from the upstream repository and capped at 1,000 dialogues for artifact size.

## Table 9b: Enron-Style Communication Graph

| Metric | Value |
|---|---:|
| Source mode | enron_style_fixture |
| Records/messages | 160 |
| Users | 6 |
| Sessions/threads | 160 |
| Nodes | 179 |
| Edges | 447 |
| Baseline leaked edges | 3 |
| Baseline leakage events | 24 |
| Bounded `b=0` leaked edges | 0 |
| Bounded `b=5` leaked edges | 2 |
| Semantic baseline leaked edges | 2 |
| Semantic `b=0` leaked edges | 0 |

Interpretation: the runner ingests an approved local Enron maildir when `GRAPHMEMSHIELD_ENRON_MAILDIR` is set; otherwise it generates a reproducible Enron-style communication fixture that stresses sender-recipient-subject graph structure without real email content.

## Table 10: Kuzu Performance

| Metric | Value |
|---|---:|
| Write time (s) | 23.1402 |
| Read time (s) | 0.0555 |
| Retrieval queries | 100 |
| Baseline retrieval (ms/query) | 2.4278 |
| Strict guard retrieval (ms/query) | 1.4189 |
| Bounded guard retrieval (ms/query) | 1.4100 |

Interpretation: guard-enabled retrieval is faster in this workload because blocked provenance/sensitivity edges reduce the expansion frontier.

## Table 11: Threat-to-Metric Mapping

| Threat | Attack / Evaluation | Metric | Defense |
|---|---|---|---|
| Cross-session edge exposure | CrossSessionProbe / adaptive probe | leaked edges, leakage events | GraphMemGuard budget |
| Response-level leakage | black-box scorer | leaked response edges/terms | bounded sharing, sensitivity block |
| Session re-identification | SessionGraphLink | Top-k, MRR | provenance minimization |
| Temporal inference | TemporalPathInfer | pairwise order accuracy | timestamp stripping |
| Write-time edge presence | fixed-universe randomized response | released/synthetic candidate edges | per-edge DP over candidate universe |

## Table 12: Multi-Hop and Hybrid Pipeline

| Experiment | Condition | Metric | Value |
|---|---|---:|---:|
| Multi-hop probe | hop 1 | baseline leaked edges | 9 |
| Multi-hop probe | hop 2 | baseline leaked edges | 12 |
| Multi-hop probe | hop 3 | baseline leaked edges | 12 |
| Multi-hop probe | hop 1 | bounded `b=5` leaked edges | 3 |
| Multi-hop probe | hop 2 | bounded `b=5` leaked edges | 3 |
| Multi-hop probe | hop 3 | bounded `b=5` leaked edges | 3 |
| Hybrid pipeline | baseline | response leaked edges | 12 |
| Hybrid pipeline | baseline | response leaked terms | 8 |
| Hybrid pipeline | strict guard | response leaked edges | 0 |
| Hybrid pipeline | bounded `b=5` | response leaked edges | 0 |

Interpretation: multi-hop expansion increases unguarded leakage by hop 2, but the bounded policy caps leakage across hop depths. The hybrid backend-adaptive-retrieval-response pipeline blocks final-response leakage under strict and bounded settings.

## Table 13: Robustness, Strong Generators, Utility, and Privacy Accounting

| Experiment | Condition | Metric | Value |
|---|---|---:|---:|
| Provenance error robustness | sensitivity error 0.00 | response leaked edges | 3 |
| Provenance error robustness | sensitivity error 0.10 | response leaked edges | 6 |
| Provenance error robustness | sensitivity error 0.25 | response leaked edges | 9 |
| Provenance error robustness | sensitivity error 0.50 | response leaked edges | 12 |
| Strong generator | baseline evidence dump | response leaked edges | 12 |
| Strong generator | bounded `b=5` evidence dump | response leaked edges | 3 |
| Strong generator | bounded `b=5` local abstractive | response leaked edges | 0 |
| Utility quality | Sydney/Hotel/CloudVendor | precision / recall / F1 | 1.0000 / 0.6667 / 0.8000 |
| Utility quality | Project-A/vendor | precision / recall / F1 | 1.0000 / 0.0000 / 0.0000 |
| Privacy accounting | epsilon 1.0 | single-release privacy loss | 1.0000 |
| Privacy accounting | epsilon 1.0, 10 releases | composed epsilon | 10.0000 |
| Full graph privacy | scoped epsilon 1.0, one release | full-graph DP? | false |
| Full graph privacy | full universe epsilon 1.0, one release | composed epsilon | 2304.0000 |
| Semantic response leakage | enterprise baseline | semantic leaked edges | 12 |
| Semantic response leakage | enterprise bounded `b=5` | semantic leaked edges | 3 |

Interpretation: bounded sharing depends on correct sensitivity provenance; systematic sensitivity downgrading can re-open response leakage even when the guard is active. Strong evidence-dump generation confirms the residual worst case, while tighter utility metrics show high precision but query-dependent recall loss. The fixed-universe randomized-response mechanism now includes explicit single-release, full-graph scope, and basic composition accounting.
