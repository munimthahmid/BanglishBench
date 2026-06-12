# V5 Flagged-Bad Denominator Policy Sensitivity

Updated: 2026-06-11

## Purpose

The preregistered main policy keeps all 200 frozen validation rows and flags
three source-quality problems. This report separately excludes those rows to
verify that the denominator choice does not drive the reviewed-v5 conclusion.

- Summary CSV: `results/analysis/v5_bad_row_policy_sensitivity.csv`
- Flagged-item CSV: `results/analysis/v5_bad_row_policy_items.csv`

## Flagged Rows

| ID | Dataset | Review note |
| --- | --- | --- |
| `benqa_10th-Physics_0130` | benqa | source question mismatches listed statements |
| `benqa_12th-Chemistry-I_0286` | benqa | answer options appear date-corrupted |
| `benqa_12th-Physics-II_0131` | benqa | option formula appears malformed |

## Strict-197 Results

| Model | Comparison | Left | Right | Delta | 95% CI | Gains | Losses |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: |
| Qwen2.5-3B | `v5_minus_v4_banglish` | 37/197 | 39/197 | +1.0 pts | [-1.0, +3.0] | 3 | 1 |
| Qwen2.5-3B | `v5_banglish_minus_bangla` | 53/197 | 39/197 | -7.1 pts | [-13.2, -1.0] | 14 | 28 |
| Qwen2.5-3B | `v5_banglish_minus_english` | 71/197 | 39/197 | -16.2 pts | [-23.4, -9.1] | 13 | 45 |
| Qwen3-4B | `v5_minus_v4_banglish` | 46/197 | 48/197 | +1.0 pts | [0.0, +2.5] | 2 | 0 |
| Qwen3-4B | `v5_banglish_minus_bangla` | 79/197 | 48/197 | -15.7 pts | [-22.3, -9.6] | 8 | 39 |
| Qwen3-4B | `v5_banglish_minus_english` | 87/197 | 48/197 | -19.8 pts | [-27.4, -12.2] | 13 | 52 |
| Qwen2.5-7B 8-bit | `v5_minus_v4_banglish` | 47/197 | 46/197 | -0.5 pts | [-3.5, +2.5] | 4 | 5 |
| Qwen2.5-7B 8-bit | `v5_banglish_minus_bangla` | 65/197 | 46/197 | -9.6 pts | [-16.8, -2.5] | 18 | 37 |
| Qwen2.5-7B 8-bit | `v5_banglish_minus_english` | 93/197 | 46/197 | -23.9 pts | [-31.5, -15.7] | 13 | 60 |

## Interpretation

- The all-200 frozen policy remains the primary thesis denominator.
- The strict-197 view is a separately reported sensitivity analysis.
- Reviewed cleanup remains small under strict exclusion.
- Reviewed Banglish remains below native Bangla and English for all three
  thesis-facing Qwen rows under strict exclusion.
