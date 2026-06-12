# Validation-200 v5 Review Metadata Summary

Updated: 2026-05-28

## Inputs

- Summary CSV: `results/analysis/validation200_v5_review_metadata_summary.csv`

## Dataset And Split

| Key | Rows | Tier-1 | Test rows | Mean score | Mean repl |
| --- | ---: | ---: | ---: | ---: | ---: |
| `benqa | test` | 73 | 29 | 73 | 112.1 | 1.33 |
| `banglamath | test` | 36 | 10 | 36 | 130.4 | 2.64 |
| `benqa | dev` | 20 | 4 | 0 | 91.3 | 1.2 |
| `banglamath | dev` | 11 | 0 | 0 | 122.5 | 3.0 |

## Impact Tier

| Key | Rows | Tier-1 | Test rows | Mean score | Mean repl |
| --- | ---: | ---: | ---: | ---: | ---: |
| `tier_2_high` | 52 | 0 | 40 | 126.3 | 2.04 |
| `tier_1_review_first` | 43 | 43 | 39 | 152.4 | 2.14 |
| `tier_4_low` | 39 | 0 | 28 | 58.3 | 1.05 |
| `tier_3_medium` | 6 | 0 | 2 | 110.3 | 1.67 |

## Priority Bucket

| Key | Rows | Tier-1 | Test rows | Mean score | Mean repl |
| --- | ---: | ---: | ---: | ---: | ---: |
| `both_wrong_single_edit` | 55 | 27 | 47 | 136.7 | 1.0 |
| `both_wrong_multi_edit` | 40 | 16 | 30 | 139.3 | 3.38 |
| `lower_priority` | 39 | 0 | 28 | 58.3 | 1.05 |
| `qwen25_wrong_multi_edit` | 4 | 0 | 2 | 109.0 | 2.0 |
| `qwen3_wrong_multi_edit` | 2 | 0 | 2 | 126.0 | 5.0 |

## Top Domains

| Key | Rows | Tier-1 | Test rows | Mean score | Mean repl |
| --- | ---: | ---: | ---: | ---: | ---: |
| `math` | 55 | 16 | 41 | 130.9 | 2.71 |
| `physics-ii` | 9 | 4 | 7 | 119.1 | 1.33 |
| `chemistry-i` | 8 | 2 | 7 | 100.9 | 1.12 |
| `math-ii` | 8 | 0 | 6 | 71.4 | 1.12 |
| `physics` | 8 | 1 | 6 | 83.1 | 1.25 |
| `biology` | 7 | 4 | 5 | 128.9 | 1.0 |
| `biology-ii` | 7 | 3 | 7 | 109.0 | 1.14 |
| `chemistry` | 7 | 2 | 5 | 105.1 | 1.0 |
| `chemistry-ii` | 7 | 3 | 6 | 111.6 | 1.14 |
| `math-i` | 7 | 0 | 5 | 86.1 | 1.14 |
| `science` | 7 | 4 | 6 | 123.9 | 1.14 |
| `physics-i` | 6 | 1 | 5 | 93.3 | 1.33 |
| `biology-i` | 4 | 3 | 3 | 131.8 | 1.5 |

## Top Subjects

| Key | Rows | Tier-1 | Test rows | Mean score | Mean repl |
| --- | ---: | ---: | ---: | ---: | ---: |
| `blank` | 47 | 10 | 36 | 128.5 | 2.72 |
| `Physics-II` | 9 | 4 | 7 | 119.1 | 1.33 |
| `Chemistry-I` | 8 | 2 | 7 | 100.9 | 1.12 |
| `Math` | 8 | 6 | 5 | 144.8 | 2.62 |
| `Math-II` | 8 | 0 | 6 | 71.4 | 1.12 |
| `Physics` | 8 | 1 | 6 | 83.1 | 1.25 |
| `Biology` | 7 | 4 | 5 | 128.9 | 1.0 |
| `Biology-II` | 7 | 3 | 7 | 109.0 | 1.14 |
| `Chemistry` | 7 | 2 | 5 | 105.1 | 1.0 |
| `Chemistry-II` | 7 | 3 | 6 | 111.6 | 1.14 |
| `Math-I` | 7 | 0 | 5 | 86.1 | 1.14 |
| `Science` | 7 | 4 | 6 | 123.9 | 1.14 |
| `Physics-I` | 6 | 1 | 5 | 93.3 | 1.33 |
| `Biology-I` | 4 | 3 | 3 | 131.8 | 1.5 |

## Grades

| Key | Rows | Tier-1 | Test rows | Mean score | Mean repl |
| --- | ---: | ---: | ---: | ---: | ---: |
| `12th` | 49 | 16 | 40 | 105.2 | 1.22 |
| `10th` | 33 | 11 | 25 | 104.1 | 1.12 |
| `seven` | 18 | 6 | 13 | 135.1 | 4.17 |
| `six` | 18 | 2 | 14 | 127.1 | 1.72 |
| `8th` | 11 | 6 | 8 | 129.3 | 2.18 |
| `Eight` | 11 | 2 | 9 | 120.3 | 2.0 |
