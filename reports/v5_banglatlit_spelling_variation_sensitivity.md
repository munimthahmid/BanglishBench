# V5 BanglaTLit Spelling-Variation Sensitivity

Updated: 2026-06-11

## Inputs And Outputs

- Frozen-v5 slice: `data/slices/validation_200_v5.jsonl`
- Fragility/correctness items: `results/analysis/v5_banglish_fragility_items.csv`
- BanglaTLit spelling-variation tokens: `results/analysis/banglatlit_spelling_variation_tokens.csv`
- BanglaTLit spelling-variation summary: `results/analysis/banglatlit_spelling_variation_summary.csv`
- Main dataset intervals for all-item rows: `results/analysis/v5_dataset_gap_intervals.csv`
- Per-model item output: `results/analysis/v5_banglatlit_spelling_variation_sensitivity_items.csv`
- Per-model summary output: `results/analysis/v5_banglatlit_spelling_variation_sensitivity_summary.csv`

## Headline

- The BanglaTLit alignment contributes 24418 aligned token pairs from 2754 token-aligned rows and identifies 299 Bangla tokens with at least two repeated Latin variants.
- This audit scores each frozen-v5 content Banglish item by exposure to
  those repeated-variant Latin spellings.
- In the highest spelling-variation-exposure all-200 quartile, reviewed Banglish remains below both Bangla and English for every thesis-facing Qwen row.
- The below-Bangla-and-English direction holds in all but the lowest all-200 exposure quartile, where Qwen2.5-3B ties Bangla at 16/50.
- This is descriptive naturalness evidence, not a causal spelling-variation
  mechanism.

### All Frozen-V5 Items

| Model | n | Mean exposure | Bangla | Banglish | English | Banglish-Bangla | Banglish-English | Fragile items |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: |
| Qwen2.5-3B | 200 | 0.4563 | 54/200 | 41/200 | 71/200 | -6.5 pts [-12.5, 0.0] | -15.0 pts [-22.0, -7.5] | 58 |
| Qwen2.5-7B | 200 | 0.4563 | 65/200 | 47/200 | 94/200 | -9.0 pts [-16.0, -2.0] | -23.5 pts [-31.0, -15.5] | 68 |
| Qwen3-4B | 200 | 0.4563 | 80/200 | 49/200 | 88/200 | -15.5 pts [-22.0, -9.0] | -19.5 pts [-27.0, -12.0] | 59 |

### Highest Spelling-Variation Exposure Quartile

| Model | n | Mean exposure | Bangla | Banglish | English | Banglish-Bangla | Banglish-English | Fragile items |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: |
| Qwen2.5-3B | 50 | 1.0044 | 9/50 | 7/50 | 18/50 | -4.0 pts [-16.0, +6.0] | -22.0 pts [-36.0, -8.0] | 15 |
| Qwen2.5-7B | 50 | 1.0044 | 14/50 | 10/50 | 26/50 | -8.0 pts [-22.0, +6.0] | -32.0 pts [-50.0, -14.0] | 24 |
| Qwen3-4B | 50 | 1.0044 | 24/50 | 15/50 | 27/50 | -18.0 pts [-32.0, -6.0] | -24.0 pts [-38.0, -12.0] | 15 |

### Highest BEnQA Spelling-Variation Exposure Quartile

| Model | n | Mean exposure | Bangla | Banglish | English | Banglish-Bangla | Banglish-English | Fragile items |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: |
| Qwen2.5-3B | 36 | 1.0507 | 8/36 | 7/36 | 16/36 | -2.8 pts [-16.7, +11.1] | -25.0 pts [-41.7, -8.3] | 13 |
| Qwen2.5-7B | 36 | 1.0507 | 13/36 | 10/36 | 22/36 | -8.3 pts [-27.8, +11.1] | -33.3 pts [-55.6, -11.1] | 20 |
| Qwen3-4B | 36 | 1.0507 | 21/36 | 13/36 | 24/36 | -22.2 pts [-38.9, -5.6] | -30.6 pts [-47.2, -13.9] | 14 |

## All-200 Variation-Exposure Direction Check

| Exposure bucket | Model | n | Mean exposure | Bangla | Banglish | English | Direction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `q1` | Qwen2.5-3B | 50 | 0.038 | 16 | 16 | 18 | mixed |
| `q1` | Qwen2.5-7B | 50 | 0.038 | 22 | 17 | 25 | below Bangla and English |
| `q1` | Qwen3-4B | 50 | 0.038 | 23 | 13 | 24 | below Bangla and English |
| `q2` | Qwen2.5-3B | 50 | 0.2831 | 13 | 9 | 17 | below Bangla and English |
| `q2` | Qwen2.5-7B | 50 | 0.2831 | 15 | 9 | 21 | below Bangla and English |
| `q2` | Qwen3-4B | 50 | 0.2831 | 16 | 9 | 16 | below Bangla and English |
| `q3` | Qwen2.5-3B | 50 | 0.4997 | 16 | 9 | 18 | below Bangla and English |
| `q3` | Qwen2.5-7B | 50 | 0.4997 | 14 | 11 | 22 | below Bangla and English |
| `q3` | Qwen3-4B | 50 | 0.4997 | 17 | 12 | 21 | below Bangla and English |
| `q4` | Qwen2.5-3B | 50 | 1.0044 | 9 | 7 | 18 | below Bangla and English |
| `q4` | Qwen2.5-7B | 50 | 1.0044 | 14 | 10 | 26 | below Bangla and English |
| `q4` | Qwen3-4B | 50 | 1.0044 | 24 | 15 | 27 | below Bangla and English |

## Interpretation

BanglaTLit shows that natural Romanized Bangla has many repeated spelling
variants. The frozen-v5 benchmark is still controlled educational
Banglish, but high exposure to BanglaTLit repeated-variant spellings
does not remove the reviewed-Banglish deficit. The lowest-exposure
bucket is mixed for Qwen2.5-3B, so this audit should be cited as
limitations/robustness evidence rather than a monotonic feature effect.

## Reproducibility

- Builder: `scripts/analyze_v5_banglatlit_spelling_variation_sensitivity.py`
- Per-model item rows: 600
- Summary rows: 45
- Exposure metric: for each content token that appears as a repeated
  BanglaTLit Latin variant, add `max_repeated_variants - 1`, divided by
  content token count.
- Bootstrap: paired item resampling within each model/bucket, 5,000 samples.
