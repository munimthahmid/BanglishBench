# Validation-200 v5 Review Validation

Updated: 2026-06-11

## Inputs

- Review queue: `data/slices/validation_200_v5_review_queue.csv`
- Source slice: `data/slices/validation_200_v4.jsonl`
- Issue CSV: `results/analysis/validation200_v5_review_validation_issues.csv`
- Require complete: `False`

## Progress

- Rows: 140
- Reviewed rows: 140
- Pending rows: 0
- Rows with replacement text: 137

| Quality label | Rows |
| --- | ---: |
| `minor_edit` | 126 |
| `major_edit` | 11 |
| `bad` | 3 |

## Issue Counts

| Severity | Issues |
| --- | ---: |
| `error` | 0 |
| `warning` | 0 |
| `pending` | 0 |

| Code | Issues |
| --- | ---: |

## Freeze Rule

Run the freeze only after this validator has zero `error` rows and
zero `pending` rows under `--require-complete`. Warnings should be
read before freezing; line-count warnings can be acceptable when the
answer-format line and semantic content are preserved.
