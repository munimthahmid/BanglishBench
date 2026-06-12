# Validation-200 v5 Review Effort Summary

Updated: 2026-05-28

## Inputs

- Review queue: `data/slices/validation_200_v5_review_queue.csv`
- Substitution CSV: `results/analysis/validation200_v5_review_queue_substitutions.csv`

## Review Progress

- Rows: 140
- Reviewed rows: 0
- Pending rows: 140

## Dataset Counts

| Dataset | Rows |
| --- | ---: |
| `benqa` | 93 |
| `banglamath` | 47 |

## Priority Counts

| Priority bucket | Rows |
| --- | ---: |
| `both_wrong_single_edit` | 55 |
| `both_wrong_multi_edit` | 40 |
| `lower_priority` | 39 |
| `qwen25_wrong_multi_edit` | 4 |
| `qwen3_wrong_multi_edit` | 2 |

## Replacement Count Histogram

| Replacement count | Rows |
| --- | ---: |
| 8 | 3 |
| 7 | 2 |
| 6 | 1 |
| 5 | 3 |
| 4 | 6 |
| 3 | 8 |
| 2 | 25 |
| 1 | 92 |

## Top Suggested Substitutions

| Substitution | Occurrences |
| --- | ---: |
| `kot` -> `koto` | 72 |
| `konoti` -> `konti` | 57 |
| `ekoti` -> `ekti` | 40 |
| `kshetrofol` -> `khetrofol` | 14 |
| `doirghy` -> `doirgho` | 13 |
| `korote` -> `korte` | 10 |
| `prosth` -> `prostho` | 9 |
| `ayotakar` -> `ayotokar` | 7 |
| `achhe` -> `ache` | 6 |
| `thakole` -> `thakle` | 5 |
| `penyaj` -> `peyaj` | 5 |
| `kshetre` -> `khetre` | 5 |
| `choora` -> `chowra` | 4 |
| `uchchota` -> `ucchota` | 2 |

## Review Strategy

Start with the repeated math-artifact substitutions because they cover
many high-priority rows. Do not bulk-accept them blindly: still compare
Bangla, English, current Banglish, and auto-suggested Banglish for each
row before setting `quality_label`.
