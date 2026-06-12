# V5 BanglaTLit Model-Coverage Sensitivity

Updated: 2026-06-11

## Inputs And Outputs

- Lexical coverage items: `results/analysis/v5_banglatlit_lexical_coverage_items.csv`
- Fragility/correctness items: `results/analysis/v5_banglish_fragility_items.csv`
- Main dataset intervals for all-item rows: `results/analysis/v5_dataset_gap_intervals.csv`
- Per-model item output: `results/analysis/v5_banglatlit_model_coverage_sensitivity_items.csv`
- Per-model summary output: `results/analysis/v5_banglatlit_model_coverage_sensitivity_summary.csv`

## Headline

- This audit expands the BanglaTLit lexical-coverage result from a
  Qwen-family aggregate to separate rows for Qwen2.5-3B, Qwen2.5-7B,
  and Qwen3-4B.
- In the highest-coverage all-200 quartile, reviewed Banglish remains below both Bangla and English for every thesis-facing Qwen row.
- The same below-Bangla-and-English direction holds in every all-200 coverage quartile for every thesis-facing Qwen row.
- This weakens a model-specific explanation that only rare or low-coverage
  Banglish vocabulary drives the frozen-v5 gap.

### All Frozen-V5 Items

| Model | n | Mean coverage | Bangla | Banglish | English | Banglish-Bangla | Banglish-English | Fragile items |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: |
| Qwen2.5-3B | 200 | 36.8% | 54/200 | 41/200 | 71/200 | -6.5 pts [-12.5, 0.0] | -15.0 pts [-22.0, -7.5] | 58 |
| Qwen2.5-7B | 200 | 36.8% | 65/200 | 47/200 | 94/200 | -9.0 pts [-16.0, -2.0] | -23.5 pts [-31.0, -15.5] | 68 |
| Qwen3-4B | 200 | 36.8% | 80/200 | 49/200 | 88/200 | -15.5 pts [-22.0, -9.0] | -19.5 pts [-27.0, -12.0] | 59 |

### Highest-Coverage All-200 Quartile

| Model | n | Mean coverage | Bangla | Banglish | English | Banglish-Bangla | Banglish-English | Fragile items |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: |
| Qwen2.5-3B | 50 | 63.0% | 10/50 | 8/50 | 16/50 | -4.0 pts [-14.0, +6.0] | -16.0 pts [-28.0, -6.0] | 10 |
| Qwen2.5-7B | 50 | 63.0% | 15/50 | 8/50 | 21/50 | -14.0 pts [-26.0, -4.0] | -26.0 pts [-40.0, -12.0] | 17 |
| Qwen3-4B | 50 | 63.0% | 15/50 | 12/50 | 21/50 | -6.0 pts [-18.0, +6.0] | -18.0 pts [-32.0, -4.0] | 12 |

### Highest-Coverage BEnQA Quartile

| Model | n | Mean coverage | Bangla | Banglish | English | Banglish-Bangla | Banglish-English | Fragile items |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: |
| Qwen2.5-3B | 36 | 52.5% | 11/36 | 9/36 | 17/36 | -5.6 pts [-19.4, +11.1] | -22.2 pts [-38.9, -5.6] | 13 |
| Qwen2.5-7B | 36 | 52.5% | 16/36 | 10/36 | 21/36 | -16.7 pts [-30.6, -2.8] | -30.6 pts [-50.0, -11.1] | 14 |
| Qwen3-4B | 36 | 52.5% | 20/36 | 17/36 | 24/36 | -8.3 pts [-25.0, +8.3] | -19.4 pts [-38.9, 0.0] | 13 |

## All-200 Quartile Direction Check

| Coverage bucket | Model | n | Bangla | Banglish | English | Direction |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `q1` | Qwen2.5-3B | 50 | 14 | 10 | 16 | below Bangla and English |
| `q1` | Qwen2.5-7B | 50 | 19 | 13 | 25 | below Bangla and English |
| `q1` | Qwen3-4B | 50 | 19 | 8 | 23 | below Bangla and English |
| `q2` | Qwen2.5-3B | 50 | 17 | 16 | 19 | below Bangla and English |
| `q2` | Qwen2.5-7B | 50 | 20 | 16 | 25 | below Bangla and English |
| `q2` | Qwen3-4B | 50 | 23 | 12 | 21 | below Bangla and English |
| `q3` | Qwen2.5-3B | 50 | 13 | 7 | 20 | below Bangla and English |
| `q3` | Qwen2.5-7B | 50 | 11 | 10 | 23 | below Bangla and English |
| `q3` | Qwen3-4B | 50 | 23 | 17 | 23 | below Bangla and English |
| `q4` | Qwen2.5-3B | 50 | 10 | 8 | 16 | below Bangla and English |
| `q4` | Qwen2.5-7B | 50 | 15 | 8 | 21 | below Bangla and English |
| `q4` | Qwen3-4B | 50 | 15 | 12 | 21 | below Bangla and English |

## Interpretation

The existing lexical-coverage audit already shows that frozen-v5 Banglish
is not a natural-chat benchmark. This per-model sensitivity adds a
narrower robustness check: even among items whose content tokens overlap
most with BanglaTLit, each thesis-facing Qwen row still performs worse
on reviewed Banglish than on Bangla or English. Coverage buckets are
descriptive; they should not be presented as a causal lexical mechanism.

## Reproducibility

- Builder: `scripts/analyze_v5_banglatlit_model_coverage_sensitivity.py`
- Per-model item rows: 600
- Summary rows: 45
- Quartiles reuse exact-token BanglaTLit coverage from
  `reports/v5_banglatlit_lexical_coverage.md`.
- Bootstrap: paired item resampling within each model/bucket, 5,000 samples.
