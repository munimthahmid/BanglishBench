# Frozen-V5 Composition Sensitivity

Updated: 2026-06-11

## Scope

This no-spend audit checks whether the reviewed-Banglish deficit is only
a byproduct of number-heavy or formula-heavy educational rows. It reuses
the frozen-v5 item-level correctness table and reports paired bootstrap
intervals inside simpler composition subsets.

- Item membership table: `results/analysis/v5_composition_sensitivity_items.csv`
- Summary table: `results/analysis/v5_composition_sensitivity_summary.csv`

This does not turn the benchmark into natural Banglish. It is a
composition stress test for the controlled educational slice.

## Digit And Formula Stress Test

| Filter | n | Model | Bangla | Reviewed Banglish | English | Banglish-Bangla | Banglish-English |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| all | 200 | Qwen2.5-3B | 54/200 (27.0%) | 41/200 (20.5%) | 71/200 (35.5%) | -6.5 pts [-12.5, 0.0] | -15.0 pts [-22.0, -7.5] |
| all | 200 | Qwen2.5-7B | 65/200 (32.5%) | 47/200 (23.5%) | 94/200 (47.0%) | -9.0 pts [-16.5, -2.0] | -23.5 pts [-31.0, -16.0] |
| all | 200 | Qwen3-4B | 80/200 (40.0%) | 49/200 (24.5%) | 88/200 (44.0%) | -15.5 pts [-22.0, -9.0] | -19.5 pts [-26.5, -12.0] |
| no_digits | 61 | Qwen2.5-3B | 22/61 (36.1%) | 14/61 (23.0%) | 33/61 (54.1%) | -13.1 pts [-26.2, 0.0] | -31.1 pts [-45.9, -16.4] |
| no_digits | 61 | Qwen2.5-7B | 29/61 (47.5%) | 19/61 (31.1%) | 42/61 (68.9%) | -16.4 pts [-32.8, -1.6] | -37.7 pts [-52.5, -22.9] |
| no_digits | 61 | Qwen3-4B | 34/61 (55.7%) | 14/61 (23.0%) | 38/61 (62.3%) | -32.8 pts [-45.9, -19.7] | -39.3 pts [-55.7, -22.9] |
| no_formula_operator | 107 | Qwen2.5-3B | 24/107 (22.4%) | 9/107 (8.4%) | 36/107 (33.6%) | -14.0 pts [-21.5, -6.5] | -25.2 pts [-34.6, -16.8] |
| no_formula_operator | 107 | Qwen2.5-7B | 30/107 (28.0%) | 18/107 (16.8%) | 48/107 (44.9%) | -11.2 pts [-20.6, -1.9] | -28.0 pts [-38.3, -18.7] |
| no_formula_operator | 107 | Qwen3-4B | 33/107 (30.8%) | 15/107 (14.0%) | 39/107 (36.4%) | -16.8 pts [-25.2, -8.4] | -22.4 pts [-31.8, -13.1] |
| no_digits_no_formula | 39 | Qwen2.5-3B | 13/39 (33.3%) | 7/39 (17.9%) | 22/39 (56.4%) | -15.4 pts [-33.3, 0.0] | -38.5 pts [-56.4, -23.1] |
| no_digits_no_formula | 39 | Qwen2.5-7B | 19/39 (48.7%) | 13/39 (33.3%) | 30/39 (76.9%) | -15.4 pts [-33.3, +2.6] | -43.6 pts [-61.5, -25.6] |
| no_digits_no_formula | 39 | Qwen3-4B | 22/39 (56.4%) | 11/39 (28.2%) | 27/39 (69.2%) | -28.2 pts [-46.2, -10.3] | -41.0 pts [-59.0, -23.1] |
| benqa_no_digits | 60 | Qwen2.5-3B | 22/60 (36.7%) | 14/60 (23.3%) | 33/60 (55.0%) | -13.3 pts [-26.7, 0.0] | -31.7 pts [-46.7, -16.7] |
| benqa_no_digits | 60 | Qwen2.5-7B | 29/60 (48.3%) | 19/60 (31.7%) | 42/60 (70.0%) | -16.7 pts [-31.7, -1.7] | -38.3 pts [-53.3, -23.3] |
| benqa_no_digits | 60 | Qwen3-4B | 34/60 (56.7%) | 14/60 (23.3%) | 38/60 (63.3%) | -33.3 pts [-46.7, -20.0] | -40.0 pts [-55.0, -23.3] |
| benqa_no_digits_no_formula | 38 | Qwen2.5-3B | 13/38 (34.2%) | 7/38 (18.4%) | 22/38 (57.9%) | -15.8 pts [-34.2, 0.0] | -39.5 pts [-55.3, -21.1] |
| benqa_no_digits_no_formula | 38 | Qwen2.5-7B | 19/38 (50.0%) | 13/38 (34.2%) | 30/38 (78.9%) | -15.8 pts [-34.2, +2.6] | -44.7 pts [-63.2, -26.3] |
| benqa_no_digits_no_formula | 38 | Qwen3-4B | 22/38 (57.9%) | 11/38 (28.9%) | 27/38 (71.1%) | -28.9 pts [-47.4, -10.5] | -42.1 pts [-60.5, -23.7] |

## Interpretation

- The no-digit subset has 61 rows. All three thesis-facing Qwen rows
  keep reviewed Banglish below both Bangla and English there; the
  Banglish-minus-Bangla range is -32.8 to -13.1 pts.
- The no-formula/operator subset has 107 rows and also keeps the
  Banglish-minus-Bangla gap negative for all three Qwen rows.
- The stricter no-digit/no-formula BEnQA subset has 38 rows. It is small,
  but every Qwen row still shows reviewed Banglish below Bangla and
  English.
- The shorter-half subset has 101 rows. Its Banglish-minus-Bangla range is
  -16.0 to -10.0 pts.
- These results do not remove the real-Banglish naturalness limitation;
  they show the main signal is not solely a numeric/formula artifact.

## Caveats

- The simplest subsets are smaller, so confidence intervals widen.
- BanglaMATH is mostly numeric; no-digit composition checks are therefore
  essentially BEnQA checks.
- The benchmark remains controlled educational Banglish, not a sample of
  naturally occurring social/media Banglish.

## Artifacts

- Builder: `scripts/analyze_v5_composition_sensitivity.py`
- Item membership table: `results/analysis/v5_composition_sensitivity_items.csv`
- Summary table: `results/analysis/v5_composition_sensitivity_summary.csv`
