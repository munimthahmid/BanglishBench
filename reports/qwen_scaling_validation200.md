# Qwen Scaling: Validation-200

Updated: 2026-05-28

## Purpose

This report compares Qwen-family models on validation-200 to see whether the
Banglish gap changes with model scale. Most rows use the same validation-200 v3
slice. The Qwen2.5-7B and Qwen3-1.7B no-thinking rows use the matching v4 split
after romanizer cleanup, because those runs were added after the v4 protocol was
introduced.

## Completed Reference Points

| Model | Bangla | Clean Banglish | English |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B-Instruct | 54/200 | 38/200 | 71/200 |
| Qwen3-4B-Instruct-2507 | 80/200 | 46/200 | 88/200 |

## Completed Scaling Results

| Model | Bangla | Clean Banglish | English |
| --- | ---: | ---: | ---: |
| Qwen2.5-0.5B-Instruct | 40/200 | 44/200 | 40/200 |
| Qwen2.5-1.5B-Instruct | 46/200 | 38/200 | 72/200 |
| Qwen2.5-3B-Instruct | 54/200 | 38/200 | 71/200 |
| Qwen2.5-7B-Instruct 8-bit | 65/200 | 48/200 | 94/200 |
| Qwen3-1.7B no-thinking | 34/200 | 36/200 | 61/200 |
| Qwen3-4B-Instruct-2507 | 80/200 | 46/200 | 88/200 |

## Dataset Split

| Model | Dataset | Bangla | Clean Banglish | English |
| --- | --- | ---: | ---: | ---: |
| Qwen2.5-0.5B | BEnQA | 40/144 | 43/144 | 37/144 |
| Qwen2.5-0.5B | BanglaMATH | 0/56 | 1/56 | 3/56 |
| Qwen2.5-1.5B | BEnQA | 44/144 | 38/144 | 67/144 |
| Qwen2.5-1.5B | BanglaMATH | 2/56 | 0/56 | 5/56 |
| Qwen2.5-3B | BEnQA | 49/144 | 38/144 | 66/144 |
| Qwen2.5-3B | BanglaMATH | 5/56 | 0/56 | 5/56 |
| Qwen2.5-7B 8-bit | BEnQA | 60/144 | 48/144 | 86/144 |
| Qwen2.5-7B 8-bit | BanglaMATH | 5/56 | 0/56 | 8/56 |
| Qwen3-1.7B no-thinking | BEnQA | 30/144 | 36/144 | 56/144 |
| Qwen3-1.7B no-thinking | BanglaMATH | 4/56 | 0/56 | 5/56 |
| Qwen3-4B | BEnQA | 76/144 | 45/144 | 82/144 |
| Qwen3-4B | BanglaMATH | 4/56 | 1/56 | 6/56 |

## Paired Deltas For Smaller Models

| Model | Comparison | Delta | 95% CI |
| --- | --- | ---: | --- |
| Qwen2.5-0.5B | Banglish - Bangla | +2.0 points | [-2.5, +7.0] |
| Qwen2.5-0.5B | Banglish - English | +2.0 points | [-3.0, +7.5] |
| Qwen2.5-1.5B | Banglish - Bangla | -4.0 points | [-10.0, +2.0] |
| Qwen2.5-1.5B | Banglish - English | -17.0 points | [-24.5, -9.5] |
| Qwen2.5-7B 8-bit | Banglish - Bangla | -8.5 points | [-15.5, -1.5] |
| Qwen2.5-7B 8-bit | Banglish - English | -23.0 points | [-30.5, -15.5] |
| Qwen3-1.7B no-thinking | Banglish - Bangla | +1.0 point | [-6.0, +7.5] |
| Qwen3-1.7B no-thinking | Banglish - English | -12.5 points | [-20.0, -5.0] |

## Interpretation

The 0.5B model is too weak/noisy to show the same clean script hierarchy; its
scores are clustered around 20-22% overall and the intervals overlap zero.

The 1.5B model already shows a strong Banglish-vs-English drop, but the
Banglish-vs-Bangla interval still crosses zero. Qwen3-1.7B no-thinking has the
same shape: English is clearly stronger than Banglish, but Bangla and Banglish
are not separated. The Qwen2.5-3B, Qwen2.5-7B, and Qwen3-4B results are more
thesis-relevant because they have enough Bangla/English capability for the
Banglish weakness to become a clearer differential effect.

This supports a useful framing: script gaps become most meaningful once the
model has enough task competence in at least one non-Banglish script condition.

For the broader cross-family synthesis, see
`reports/model_family_scaling_synthesis_validation200.md`.
