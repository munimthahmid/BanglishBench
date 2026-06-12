# Frozen-V5 Dataset-Level Script-Gap Intervals

Updated: 2026-06-11

## Scope

This no-spend report adds paired bootstrap intervals to the Chapter 4
dataset-level split. It uses the frozen-v5 cross-script failure table,
so Bangla and English are the unchanged controlled outputs and Banglish
is the reviewed-v5 rerun.

- Machine-readable summary: `results/analysis/v5_dataset_gap_intervals.csv`
- Source failure table: `results/analysis/validation200_v5_cross_script_failure_patterns_items.csv`

## Banglish Minus Bangla

| Model | Dataset | Bangla | Reviewed Banglish | Delta | 95% CI | Gains | Losses |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: |
| Qwen2.5-3B | `all` | 54/200 | 41/200 | -6.5 pts | [-12.5, 0.0] | 15 | 28 |
| Qwen2.5-3B | `benqa` | 49/144 | 41/144 | -5.6 pts | [-13.9, +2.8] | 15 | 23 |
| Qwen2.5-3B | `banglamath` | 5/56 | 0/56 | -8.9 pts | [-17.9, -1.8] | 0 | 5 |
| Qwen2.5-7B 8-bit | `all` | 65/200 | 47/200 | -9.0 pts | [-16.5, -2.0] | 19 | 37 |
| Qwen2.5-7B 8-bit | `benqa` | 60/144 | 47/144 | -9.0 pts | [-18.8, +0.7] | 19 | 32 |
| Qwen2.5-7B 8-bit | `banglamath` | 5/56 | 0/56 | -8.9 pts | [-16.1, -1.8] | 0 | 5 |
| Qwen3-4B | `all` | 80/200 | 49/200 | -15.5 pts | [-22.0, -9.0] | 8 | 39 |
| Qwen3-4B | `benqa` | 76/144 | 47/144 | -20.1 pts | [-28.5, -11.8] | 8 | 37 |
| Qwen3-4B | `banglamath` | 4/56 | 2/56 | -3.6 pts | [-8.9, 0.0] | 0 | 2 |

## Banglish Minus English

| Model | Dataset | English | Reviewed Banglish | Delta | 95% CI | Gains | Losses |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: |
| Qwen2.5-3B | `all` | 71/200 | 41/200 | -15.0 pts | [-22.0, -7.5] | 15 | 45 |
| Qwen2.5-3B | `benqa` | 66/144 | 41/144 | -17.4 pts | [-27.1, -7.6] | 15 | 40 |
| Qwen2.5-3B | `banglamath` | 5/56 | 0/56 | -8.9 pts | [-17.9, -1.8] | 0 | 5 |
| Qwen2.5-7B 8-bit | `all` | 94/200 | 47/200 | -23.5 pts | [-31.0, -16.0] | 13 | 60 |
| Qwen2.5-7B 8-bit | `benqa` | 86/144 | 47/144 | -27.1 pts | [-37.5, -17.4] | 13 | 52 |
| Qwen2.5-7B 8-bit | `banglamath` | 8/56 | 0/56 | -14.3 pts | [-23.2, -5.4] | 0 | 8 |
| Qwen3-4B | `all` | 88/200 | 49/200 | -19.5 pts | [-27.0, -12.0] | 13 | 52 |
| Qwen3-4B | `benqa` | 82/144 | 47/144 | -24.3 pts | [-34.0, -14.6] | 13 | 48 |
| Qwen3-4B | `banglamath` | 6/56 | 2/56 | -7.1 pts | [-14.3, -1.8] | 0 | 4 |

## Interpretation

- BEnQA is the clearest dataset-level source of the reviewed-v5
  Banglish-below-Bangla signal: Qwen3-4B has a clearly negative paired
  interval, while Qwen2.5-3B and Qwen2.5-7B 8-bit are directionally
  negative but their BEnQA intervals reach zero.
- BanglaMATH remains a low-accuracy stress test. Its Banglish-Bangla
  deltas are negative or near zero, but the intervals are wide and the
  models answer very few BanglaMATH items correctly in any script.
- Banglish is below English in BEnQA for all three thesis-facing Qwen
  rows. BanglaMATH again has wide, low-accuracy intervals.

Thesis-safe phrasing:

> The release-facing script gap is clearest on BEnQA, where the models
> have enough task competence for paired script differences to be
> meaningful. BanglaMATH should remain a hard stress test rather than
> the basis for fine-grained dataset-level claims.
