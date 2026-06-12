# Frozen-V5 Paired Sign Tests

Updated: 2026-06-11

## Scope

This no-spend audit adds exact paired sign tests to the frozen-v5 script
gap table. For each model, dataset, and comparison, it counts only
discordant item pairs: rows where reviewed Banglish wins over the
baseline script, and rows where the baseline script wins over reviewed
Banglish. The exact two-sided p-value is a binomial sign test over those
discordant pairs.

- Machine-readable summary: `results/analysis/v5_paired_sign_tests.csv`
- Source failure table: `results/analysis/validation200_v5_cross_script_failure_patterns_items.csv`

These tests complement the bootstrap intervals. They are not a replacement
for effect sizes, and they remain paired behavioral tests over a controlled
benchmark.

## Banglish Versus Bangla

| Model | Dataset | Bangla | Reviewed Banglish | Delta | Banglish gains | Banglish losses | Discordant | Exact p |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | `all` | 54/200 | 41/200 | -6.5 pts | 15 | 28 | 43 | 0.0660 |
| Qwen2.5-3B | `benqa` | 49/144 | 41/144 | -5.6 pts | 15 | 23 | 38 | 0.2559 |
| Qwen2.5-3B | `banglamath` | 5/56 | 0/56 | -8.9 pts | 0 | 5 | 5 | 0.0625 |
| Qwen2.5-7B 8-bit | `all` | 65/200 | 47/200 | -9.0 pts | 19 | 37 | 56 | 0.0222 |
| Qwen2.5-7B 8-bit | `benqa` | 60/144 | 47/144 | -9.0 pts | 19 | 32 | 51 | 0.0919 |
| Qwen2.5-7B 8-bit | `banglamath` | 5/56 | 0/56 | -8.9 pts | 0 | 5 | 5 | 0.0625 |
| Qwen3-4B | `all` | 80/200 | 49/200 | -15.5 pts | 8 | 39 | 47 | <0.0001 |
| Qwen3-4B | `benqa` | 76/144 | 47/144 | -20.1 pts | 8 | 37 | 45 | <0.0001 |
| Qwen3-4B | `banglamath` | 4/56 | 2/56 | -3.6 pts | 0 | 2 | 2 | 0.5000 |

## Banglish Versus English

| Model | Dataset | English | Reviewed Banglish | Delta | Banglish gains | Banglish losses | Discordant | Exact p |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | `all` | 71/200 | 41/200 | -15.0 pts | 15 | 45 | 60 | 0.0001 |
| Qwen2.5-3B | `benqa` | 66/144 | 41/144 | -17.4 pts | 15 | 40 | 55 | 0.0010 |
| Qwen2.5-3B | `banglamath` | 5/56 | 0/56 | -8.9 pts | 0 | 5 | 5 | 0.0625 |
| Qwen2.5-7B 8-bit | `all` | 94/200 | 47/200 | -23.5 pts | 13 | 60 | 73 | <0.0001 |
| Qwen2.5-7B 8-bit | `benqa` | 86/144 | 47/144 | -27.1 pts | 13 | 52 | 65 | <0.0001 |
| Qwen2.5-7B 8-bit | `banglamath` | 8/56 | 0/56 | -14.3 pts | 0 | 8 | 8 | 0.0078 |
| Qwen3-4B | `all` | 88/200 | 49/200 | -19.5 pts | 13 | 52 | 65 | <0.0001 |
| Qwen3-4B | `benqa` | 82/144 | 47/144 | -24.3 pts | 13 | 48 | 61 | <0.0001 |
| Qwen3-4B | `banglamath` | 6/56 | 2/56 | -7.1 pts | 0 | 4 | 4 | 0.1250 |

## Interpretation

- Qwen2.5-7B 8-bit has 19 Banglish-over-Bangla
  gains versus 37 losses on all-200
  (two-sided exact p=0.0222).
  Qwen3-4B has 8 gains versus
  39 losses (p<0.0001).
- Qwen2.5-3B is again the weakest all-200 row: 15
  gains versus 28 losses,
  p=0.0660. Keep the existing
  CI-reaches-zero qualification.
- Qwen3-4B BEnQA remains strongly asymmetric: 8
  gains versus 37 losses,
  p<0.0001.
- Banglish-versus-English asymmetry is exact-test strong on all-200 for
  all three thesis-facing Qwen rows: Qwen2.5-3B p=0.0001; Qwen2.5-7B 8-bit p<0.0001; Qwen3-4B p<0.0001.

## Artifacts

- Builder: `scripts/analyze_v5_paired_sign_tests.py`
- Summary table: `results/analysis/v5_paired_sign_tests.csv`
