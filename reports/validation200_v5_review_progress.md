# Validation-200 v5 Review Progress

Updated: 2026-06-11

This report summarizes manual-review progress for
`data/slices/validation_200_v5_review_queue.csv`.

## Overall Status

| Value | Rows |
| --- | ---: |
| `minor_edit` | 126 |
| `major_edit` | 11 |
| `bad` | 3 |

## By Impact Tier

| Group | Total | Pending | ok | minor_edit | major_edit | bad |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `tier_2_high` | 52 | 0 | 0 | 47 | 4 | 1 |
| `tier_1_review_first` | 43 | 0 | 0 | 37 | 6 | 0 |
| `tier_4_low` | 39 | 0 | 0 | 37 | 0 | 2 |
| `tier_3_medium` | 6 | 0 | 0 | 5 | 1 | 0 |

## By Split

| Group | Total | Pending | ok | minor_edit | major_edit | bad |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `test` | 109 | 0 | 0 | 99 | 8 | 2 |
| `dev` | 31 | 0 | 0 | 27 | 3 | 1 |

## By Priority Bucket

| Group | Total | Pending | ok | minor_edit | major_edit | bad |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `both_wrong_single_edit` | 55 | 0 | 0 | 53 | 1 | 1 |
| `both_wrong_multi_edit` | 40 | 0 | 0 | 31 | 9 | 0 |
| `lower_priority` | 39 | 0 | 0 | 37 | 0 | 2 |
| `qwen25_wrong_multi_edit` | 4 | 0 | 0 | 4 | 0 | 0 |
| `qwen3_wrong_multi_edit` | 2 | 0 | 0 | 1 | 1 | 0 |

## Top Pending Substitutions

| Substitution | Pending rows | Helper command |
| --- | ---: | --- |

## Top Substitution Batch Coverage

Rows overlap across substitutions. This table estimates unique pending-row
coverage if the top substitutions are reviewed in the listed order.

| Order | Substitution | Matching rows | New rows | Cumulative rows |
| ---: | --- | ---: | ---: | ---: |

## Next Command

```bash
python3 scripts/validate_banglish_review_queue.py --require-complete
```
