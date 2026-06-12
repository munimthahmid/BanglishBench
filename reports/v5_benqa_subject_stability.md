# Frozen-V5 BEnQA Subject Stability

Updated: 2026-06-11

## Scope

This no-spend report checks whether the BEnQA portion of the frozen-v5
Banglish-minus-Bangla gap is an artifact of a single subject stratum.
For each thesis-facing Qwen row, it recomputes the BEnQA paired count
after dropping one subject at a time.

- Machine-readable summary: `results/analysis/v5_benqa_subject_stability.csv`
- Source failure table: `results/analysis/validation200_v5_cross_script_failure_patterns_items.csv`

## Summary

| Model | All BEnQA Delta | Leave-One-Subject Delta Range | Negative Drops | Closest To Zero | Strongest Drop |
| --- | ---: | ---: | ---: | --- | --- |
| Qwen2.5-3B | -5.6 pts (41/144 vs 49/144) | [-8.3, -2.3] pts | 13/13 | drop `Biology`: -2.3 pts | drop `Chemistry-II`: -8.3 pts |
| Qwen2.5-7B 8-bit | -9.0 pts (47/144 vs 60/144) | [-10.6, -6.8] pts | 13/13 | drop `Biology-I`: -6.8 pts | drop `Biology`: -10.6 pts |
| Qwen3-4B | -20.1 pts (47/144 vs 76/144) | [-23.3, -18.0] pts | 13/13 | drop `Biology-II`: -18.0 pts | drop `Math-II`: -23.3 pts |

## Leave-One-Subject Rows

| Model | Dropped Subject | Remaining n | Bangla | Reviewed Banglish | Delta | Gains | Losses |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | `Biology` | 132 | 44/132 | 41/132 | -2.3 pts | 15 | 18 |
| Qwen2.5-3B | `Biology-I` | 133 | 46/133 | 39/133 | -5.3 pts | 15 | 22 |
| Qwen2.5-3B | `Biology-II` | 133 | 46/133 | 37/133 | -6.8 pts | 13 | 22 |
| Qwen2.5-3B | `Chemistry` | 133 | 46/133 | 37/133 | -6.8 pts | 14 | 23 |
| Qwen2.5-3B | `Chemistry-I` | 133 | 45/133 | 39/133 | -4.5 pts | 15 | 21 |
| Qwen2.5-3B | `Chemistry-II` | 133 | 47/133 | 36/133 | -8.3 pts | 10 | 21 |
| Qwen2.5-3B | `Math` | 133 | 44/133 | 38/133 | -4.5 pts | 14 | 20 |
| Qwen2.5-3B | `Math-I` | 133 | 46/133 | 38/133 | -6.0 pts | 14 | 22 |
| Qwen2.5-3B | `Math-II` | 133 | 43/133 | 36/133 | -5.3 pts | 15 | 22 |
| Qwen2.5-3B | `Physics` | 133 | 44/133 | 37/133 | -5.3 pts | 14 | 21 |
| Qwen2.5-3B | `Physics-I` | 133 | 45/133 | 36/133 | -6.8 pts | 13 | 22 |
| Qwen2.5-3B | `Physics-II` | 133 | 47/133 | 38/133 | -6.8 pts | 13 | 22 |
| Qwen2.5-3B | `Science` | 133 | 45/133 | 40/133 | -3.8 pts | 15 | 20 |
| Qwen2.5-7B 8-bit | `Biology` | 132 | 55/132 | 41/132 | -10.6 pts | 17 | 31 |
| Qwen2.5-7B 8-bit | `Biology-I` | 133 | 54/133 | 45/133 | -6.8 pts | 17 | 26 |
| Qwen2.5-7B 8-bit | `Biology-II` | 133 | 54/133 | 42/133 | -9.0 pts | 17 | 29 |
| Qwen2.5-7B 8-bit | `Chemistry` | 133 | 57/133 | 46/133 | -8.3 pts | 18 | 29 |
| Qwen2.5-7B 8-bit | `Chemistry-I` | 133 | 55/133 | 45/133 | -7.5 pts | 19 | 29 |
| Qwen2.5-7B 8-bit | `Chemistry-II` | 133 | 55/133 | 43/133 | -9.0 pts | 17 | 29 |
| Qwen2.5-7B 8-bit | `Math` | 133 | 55/133 | 45/133 | -7.5 pts | 19 | 29 |
| Qwen2.5-7B 8-bit | `Math-I` | 133 | 55/133 | 41/133 | -10.5 pts | 17 | 31 |
| Qwen2.5-7B 8-bit | `Math-II` | 133 | 58/133 | 45/133 | -9.8 pts | 18 | 31 |
| Qwen2.5-7B 8-bit | `Physics` | 133 | 56/133 | 42/133 | -10.5 pts | 17 | 31 |
| Qwen2.5-7B 8-bit | `Physics-I` | 133 | 54/133 | 42/133 | -9.0 pts | 17 | 29 |
| Qwen2.5-7B 8-bit | `Physics-II` | 133 | 57/133 | 45/133 | -9.0 pts | 18 | 30 |
| Qwen2.5-7B 8-bit | `Science` | 133 | 55/133 | 42/133 | -9.8 pts | 17 | 30 |
| Qwen3-4B | `Biology` | 132 | 71/132 | 44/132 | -20.5 pts | 6 | 33 |
| Qwen3-4B | `Biology-I` | 133 | 70/133 | 44/133 | -19.5 pts | 8 | 34 |
| Qwen3-4B | `Biology-II` | 133 | 70/133 | 46/133 | -18.0 pts | 8 | 32 |
| Qwen3-4B | `Chemistry` | 133 | 69/133 | 43/133 | -19.5 pts | 8 | 34 |
| Qwen3-4B | `Chemistry-I` | 133 | 69/133 | 42/133 | -20.3 pts | 7 | 34 |
| Qwen3-4B | `Chemistry-II` | 133 | 69/133 | 45/133 | -18.0 pts | 7 | 31 |
| Qwen3-4B | `Math` | 133 | 71/133 | 45/133 | -19.5 pts | 8 | 34 |
| Qwen3-4B | `Math-I` | 133 | 71/133 | 43/133 | -21.1 pts | 8 | 36 |
| Qwen3-4B | `Math-II` | 133 | 70/133 | 39/133 | -23.3 pts | 6 | 37 |
| Qwen3-4B | `Physics` | 133 | 68/133 | 41/133 | -20.3 pts | 7 | 34 |
| Qwen3-4B | `Physics-I` | 133 | 70/133 | 43/133 | -20.3 pts | 8 | 35 |
| Qwen3-4B | `Physics-II` | 133 | 73/133 | 45/133 | -21.1 pts | 8 | 36 |
| Qwen3-4B | `Science` | 133 | 71/133 | 44/133 | -20.3 pts | 7 | 34 |

## Interpretation

- Dropping any one BEnQA subject keeps the reviewed-Banglish-minus-Bangla
  gap negative for all three thesis-facing Qwen rows.
- Qwen3-4B remains the strongest BEnQA case: its leave-one-subject gaps
  range from -23.3 to -18.0 points.
- The Qwen2.5 rows are smaller and should still be described as
  directionally negative at the dataset level, but they are not driven
  by only one subject bucket.

Thesis-safe phrasing:

> Within BEnQA, the reviewed-v5 Banglish deficit is not a single-subject
> artifact: every leave-one-subject recomputation remains negative for
> the three thesis-facing Qwen rows.
