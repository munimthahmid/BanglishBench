# V5 English-Warning Sensitivity Audit

Updated: 2026-06-11

## Inputs

- Source parity items: `results/analysis/v5_source_variant_structural_parity_items.csv`
- Recoverability items: `results/analysis/v5_recoverability_source_items.csv`
- Main dataset intervals for all-item rows: `results/analysis/v5_dataset_gap_intervals.csv`
- Item sensitivity CSV: `results/analysis/v5_english_warning_sensitivity_items.csv`
- Summary CSV: `results/analysis/v5_english_warning_sensitivity_summary.csv`

## Headline

- The source-parity audit flags 39/200 items with an English-side structural warning; bangla-vs-reviewed-Banglish remains 0/200 primary hard fails.
- On the 161 English-structurally-clean items, reviewed Banglish stays below both Bangla and English for all three thesis-facing Qwen rows.
- Recoverable Banglish misses also persist on the clean-English subset, so English-backed diagnostics are not driven only by the warning rows.

English warning codes on Bangla-vs-English comparisons: digits=23, formulas=23

## All-Items Versus English-Clean Subset

| Model | Group | n | Bangla | Banglish | English | Banglish-Bangla | Banglish-English | Recoverable misses | English recoveries | Both alternates |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- | ---: | ---: | ---: |
| Qwen2.5-3B | All frozen-v5 items | 200 | 54/200 (27.0%) | 41/200 (20.5%) | 71/200 (35.5%) | -6.5 pts [-12.5, 0.0] | -15.0 pts [-22.0, -7.5] | 58 | 45 | 15 |
| Qwen2.5-3B | No English structural warning | 161 | 45/161 (28.0%) | 31/161 (19.2%) | 60/161 (37.3%) | -8.7 pts [-15.5, -1.2] | -18.0 pts [-26.1, -9.9] | 50 | 40 | 14 |
| Qwen2.5-3B | English structural warning | 39 | 9/39 (23.1%) | 10/39 (25.6%) | 11/39 (28.2%) | +2.6 pts [-12.8, +17.9] | -2.6 pts [-17.9, +12.8] | 8 | 5 | 1 |
| Qwen2.5-7B 8-bit | All frozen-v5 items | 200 | 65/200 (32.5%) | 47/200 (23.5%) | 94/200 (47.0%) | -9.0 pts [-16.5, -2.0] | -23.5 pts [-31.0, -16.0] | 68 | 60 | 29 |
| Qwen2.5-7B 8-bit | No English structural warning | 161 | 55/161 (34.2%) | 38/161 (23.6%) | 80/161 (49.7%) | -10.6 pts [-18.6, -2.5] | -26.1 pts [-34.8, -17.4] | 58 | 52 | 26 |
| Qwen2.5-7B 8-bit | English structural warning | 39 | 10/39 (25.6%) | 9/39 (23.1%) | 14/39 (35.9%) | -2.6 pts [-17.9, +12.8] | -12.8 pts [-28.2, +2.6] | 10 | 8 | 3 |
| Qwen3-4B | All frozen-v5 items | 200 | 80/200 (40.0%) | 49/200 (24.5%) | 88/200 (44.0%) | -15.5 pts [-22.0, -9.0] | -19.5 pts [-27.0, -12.0] | 59 | 52 | 32 |
| Qwen3-4B | No English structural warning | 161 | 64/161 (39.8%) | 36/161 (22.4%) | 73/161 (45.3%) | -17.4 pts [-24.8, -9.9] | -23.0 pts [-31.1, -14.9] | 51 | 45 | 28 |
| Qwen3-4B | English structural warning | 39 | 16/39 (41.0%) | 13/39 (33.3%) | 15/39 (38.5%) | -7.7 pts [-20.5, +5.1] | -5.1 pts [-23.1, +12.8] | 8 | 7 | 4 |

## Interpretation

This audit does not repair or discard English rows. Instead, it asks
whether the thesis diagnostics that use English views disappear when
items with English-side structural warnings are separated. They do not:
the clean-English subset keeps the same direction for Bangla-vs-Banglish
and Banglish-vs-English, and it still contains many recoverable Banglish
misses. The English-warning rows should remain caveated as upstream
translation/structure risks, while the primary Bangla-vs-reviewed-Banglish
source pair remains structurally clean.
