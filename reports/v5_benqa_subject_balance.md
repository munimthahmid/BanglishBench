# Frozen-V5 BEnQA Subject-Macro Balance

Updated: 2026-06-11

## Scope

This no-spend audit asks whether the BEnQA part of the frozen-v5 gap
depends on subject-size weighting. It computes each subject's script
accuracy, then averages the 13 BEnQA subjects equally. Bootstrap
intervals resample subjects, not individual items.

- Source failure table: `results/analysis/validation200_v5_cross_script_failure_patterns_items.csv`
- Per-subject table: `results/analysis/v5_benqa_subject_balance_subjects.csv`
- Summary table: `results/analysis/v5_benqa_subject_balance_summary.csv`
- Bootstrap iterations: 10000

## Subject-Macro Summary

| Model | Comparison | Micro delta | Subject-macro delta | Subject-macro CI | Negative subjects | Gains/Losses |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | Banglish - Bangla | -5.6 pts | -5.3 pts | [-15.2, +4.2] pts | 7/13 | 15/23 |
| Qwen2.5-3B | Banglish - English | -17.4 pts | -17.3 pts | [-27.3, -6.8] pts | 9/13 | 15/40 |
| Qwen2.5-7B 8-bit | Banglish - Bangla | -9.0 pts | -9.2 pts | [-16.8, -1.6] pts | 8/13 | 19/32 |
| Qwen2.5-7B 8-bit | Banglish - English | -27.1 pts | -27.1 pts | [-38.5, -16.1] pts | 11/13 | 13/52 |
| Qwen3-4B | Banglish - Bangla | -20.1 pts | -20.2 pts | [-28.6, -11.2] pts | 12/13 | 8/37 |
| Qwen3-4B | Banglish - English | -24.3 pts | -24.4 pts | [-34.3, -13.0] pts | 12/13 | 13/48 |

## Per-Subject Accuracy

| Model | Subject | n | Bangla | Reviewed Banglish | English | Banglish-Bangla |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | `Biology` | 12 | 5/12 (41.7%) | 0/12 (0.0%) | 3/12 (25.0%) | -41.7 pts |
| Qwen2.5-3B | `Biology-I` | 11 | 3/11 (27.3%) | 2/11 (18.2%) | 7/11 (63.6%) | -9.1 pts |
| Qwen2.5-3B | `Biology-II` | 11 | 3/11 (27.3%) | 4/11 (36.4%) | 6/11 (54.5%) | +9.1 pts |
| Qwen2.5-3B | `Chemistry` | 11 | 3/11 (27.3%) | 4/11 (36.4%) | 7/11 (63.6%) | +9.1 pts |
| Qwen2.5-3B | `Chemistry-I` | 11 | 4/11 (36.4%) | 2/11 (18.2%) | 5/11 (45.5%) | -18.2 pts |
| Qwen2.5-3B | `Chemistry-II` | 11 | 2/11 (18.2%) | 5/11 (45.5%) | 6/11 (54.5%) | +27.3 pts |
| Qwen2.5-3B | `Math` | 11 | 5/11 (45.5%) | 3/11 (27.3%) | 8/11 (72.7%) | -18.2 pts |
| Qwen2.5-3B | `Math-I` | 11 | 3/11 (27.3%) | 3/11 (27.3%) | 2/11 (18.2%) | 0.0 pts |
| Qwen2.5-3B | `Math-II` | 11 | 6/11 (54.5%) | 5/11 (45.5%) | 3/11 (27.3%) | -9.1 pts |
| Qwen2.5-3B | `Physics` | 11 | 5/11 (45.5%) | 4/11 (36.4%) | 7/11 (63.6%) | -9.1 pts |
| Qwen2.5-3B | `Physics-I` | 11 | 4/11 (36.4%) | 5/11 (45.5%) | 5/11 (45.5%) | +9.1 pts |
| Qwen2.5-3B | `Physics-II` | 11 | 2/11 (18.2%) | 3/11 (27.3%) | 3/11 (27.3%) | +9.1 pts |
| Qwen2.5-3B | `Science` | 11 | 4/11 (36.4%) | 1/11 (9.1%) | 4/11 (36.4%) | -27.3 pts |
| Qwen2.5-7B 8-bit | `Biology` | 12 | 5/12 (41.7%) | 6/12 (50.0%) | 9/12 (75.0%) | +8.3 pts |
| Qwen2.5-7B 8-bit | `Biology-I` | 11 | 6/11 (54.5%) | 2/11 (18.2%) | 8/11 (72.7%) | -36.4 pts |
| Qwen2.5-7B 8-bit | `Biology-II` | 11 | 6/11 (54.5%) | 5/11 (45.5%) | 6/11 (54.5%) | -9.1 pts |
| Qwen2.5-7B 8-bit | `Chemistry` | 11 | 3/11 (27.3%) | 1/11 (9.1%) | 6/11 (54.5%) | -18.2 pts |
| Qwen2.5-7B 8-bit | `Chemistry-I` | 11 | 5/11 (45.5%) | 2/11 (18.2%) | 7/11 (63.6%) | -27.3 pts |
| Qwen2.5-7B 8-bit | `Chemistry-II` | 11 | 5/11 (45.5%) | 4/11 (36.4%) | 9/11 (81.8%) | -9.1 pts |
| Qwen2.5-7B 8-bit | `Math` | 11 | 5/11 (45.5%) | 2/11 (18.2%) | 9/11 (81.8%) | -27.3 pts |
| Qwen2.5-7B 8-bit | `Math-I` | 11 | 5/11 (45.5%) | 6/11 (54.5%) | 6/11 (54.5%) | +9.1 pts |
| Qwen2.5-7B 8-bit | `Math-II` | 11 | 2/11 (18.2%) | 2/11 (18.2%) | 2/11 (18.2%) | 0.0 pts |
| Qwen2.5-7B 8-bit | `Physics` | 11 | 4/11 (36.4%) | 5/11 (45.5%) | 8/11 (72.7%) | +9.1 pts |
| Qwen2.5-7B 8-bit | `Physics-I` | 11 | 6/11 (54.5%) | 5/11 (45.5%) | 6/11 (54.5%) | -9.1 pts |
| Qwen2.5-7B 8-bit | `Physics-II` | 11 | 3/11 (27.3%) | 2/11 (18.2%) | 4/11 (36.4%) | -9.1 pts |
| Qwen2.5-7B 8-bit | `Science` | 11 | 5/11 (45.5%) | 5/11 (45.5%) | 6/11 (54.5%) | 0.0 pts |
| Qwen3-4B | `Biology` | 12 | 5/12 (41.7%) | 3/12 (25.0%) | 4/12 (33.3%) | -16.7 pts |
| Qwen3-4B | `Biology-I` | 11 | 6/11 (54.5%) | 3/11 (27.3%) | 6/11 (54.5%) | -27.3 pts |
| Qwen3-4B | `Biology-II` | 11 | 6/11 (54.5%) | 1/11 (9.1%) | 4/11 (36.4%) | -45.5 pts |
| Qwen3-4B | `Chemistry` | 11 | 7/11 (63.6%) | 4/11 (36.4%) | 8/11 (72.7%) | -27.3 pts |
| Qwen3-4B | `Chemistry-I` | 11 | 7/11 (63.6%) | 5/11 (45.5%) | 9/11 (81.8%) | -18.2 pts |
| Qwen3-4B | `Chemistry-II` | 11 | 7/11 (63.6%) | 2/11 (18.2%) | 8/11 (72.7%) | -45.5 pts |
| Qwen3-4B | `Math` | 11 | 5/11 (45.5%) | 2/11 (18.2%) | 6/11 (54.5%) | -27.3 pts |
| Qwen3-4B | `Math-I` | 11 | 5/11 (45.5%) | 4/11 (36.4%) | 5/11 (45.5%) | -9.1 pts |
| Qwen3-4B | `Math-II` | 11 | 6/11 (54.5%) | 8/11 (72.7%) | 5/11 (45.5%) | +18.2 pts |
| Qwen3-4B | `Physics` | 11 | 8/11 (72.7%) | 6/11 (54.5%) | 9/11 (81.8%) | -18.2 pts |
| Qwen3-4B | `Physics-I` | 11 | 6/11 (54.5%) | 4/11 (36.4%) | 6/11 (54.5%) | -18.2 pts |
| Qwen3-4B | `Physics-II` | 11 | 3/11 (27.3%) | 2/11 (18.2%) | 4/11 (36.4%) | -9.1 pts |
| Qwen3-4B | `Science` | 11 | 5/11 (45.5%) | 3/11 (27.3%) | 8/11 (72.7%) | -18.2 pts |

## Interpretation

- Equal-weighting BEnQA subjects keeps reviewed Banglish below Bangla
  for all three thesis-facing Qwen rows.
- Qwen3-4B remains the clearest subject-balanced BEnQA case:
  -20.2 pts, CI
  [-28.6, -11.2].
- Qwen2.5-7B 8-bit is directionally negative under subject balancing
  (-9.2 pts), while Qwen2.5-3B
  remains the weaker row (-5.3 pts).
- This complements the leave-one-subject check: BEnQA is not only
  negative after dropping subjects, but also negative when subjects
  are given equal macro weight.
