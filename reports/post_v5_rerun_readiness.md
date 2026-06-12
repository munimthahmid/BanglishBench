# Post-v5 Rerun Readiness

Updated: 2026-06-11

This report checks whether validation-200 v5 is ready for the minimal
post-review clean-Banglish Kaggle reruns.

Overall status: `ready`

## Review Queue

| Label | Rows |
| --- | ---: |
| `total` | 140 |
| `pending` | 0 |
| `ok` | 0 |
| `minor_edit` | 126 |
| `major_edit` | 11 |
| `bad` | 3 |
| `invalid_label` | 0 |
| `missing_replacement` | 0 |
| `unexpected_replacement` | 0 |
| `bad_without_review_notes` | 0 |

## Gates

| Gate | Status | Detail |
| --- | --- | --- |
| `review_queue_complete` | `pass` | `pending=0 total=140` |
| `review_queue_labels_valid` | `pass` | `issues=0` |
| `freeze_artifact_exists` | `pass` | `data/slices/validation_200_v5.jsonl` |
| `freeze_artifact_exists` | `pass` | `results/analysis/validation200_v5_banglish_review_audit.csv` |
| `freeze_artifact_exists` | `pass` | `results/analysis/validation200_v5_banglish_artifact_summary.csv` |
| `freeze_artifact_exists` | `pass` | `results/analysis/validation200_v5_banglish_artifact_examples.csv` |
| `protocol_artifact_exists` | `pass` | `reports/v5_analysis_preregistration.md` |
| `protocol_artifact_exists` | `pass` | `reports/post_v5_rerun_protocol.md` |
| `protocol_artifact_exists` | `pass` | `reports/reproducibility_release_checklist.md` |
| `protocol_artifact_exists` | `pass` | `reports/validation200_v5_review_session_log.md` |
| `protocol_artifact_exists` | `pass` | `reports/validation200_v5_review_session_plan.md` |
| `protocol_artifact_exists` | `pass` | `results/analysis/validation200_v5_review_session_plan.csv` |

## Decision

Post-v5 reruns may be packaged according to `reports/post_v5_rerun_protocol.md`.
