# McNemar Exact Tests for Script Gaps

Updated: 2026-06-11

Paired binary outcomes per item under two prompt scripts form the
textbook McNemar setting. For each model we report the discordant-pair
counts (b = baseline-script-only correct, c = Banglish-only correct),
the exact two-sided McNemar p-value, the conditional odds ratio b/c
(Haldane-corrected, 95% CI), and Holm-adjusted p-values across models
within each panel/scoring family.

- Machine-readable summary: `results/analysis/mcnemar_script_gaps.csv`
- Builder: `scripts/analyze_mcnemar_script_gaps.py`

## Validation-200 v5 Qwen triad (strict) — Banglish vs Bangla

| Model | Bangla | Banglish | Delta | b (losses) | c (gains) | OR [95% CI] | Exact p | Holm p |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| Qwen2.5-3B | 54/200 | 41/200 | -6.50 pts | 28 | 15 | 1.839 [0.991, 3.413] | 0.0660 | 0.0660 |
| Qwen2.5-7B 8-bit | 65/200 | 47/200 | -9.00 pts | 37 | 19 | 1.923 [1.113, 3.324] | 0.0222 | 0.0445 |
| Qwen3-4B | 80/200 | 49/200 | -15.50 pts | 39 | 8 | 4.647 [2.215, 9.751] | <0.0001 | <0.0001 |

## Validation-200 v5 Qwen triad (strict) — Banglish vs English

| Model | English | Banglish | Delta | b (losses) | c (gains) | OR [95% CI] | Exact p | Holm p |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| Qwen2.5-3B | 71/200 | 41/200 | -15.00 pts | 45 | 15 | 2.935 [1.649, 5.224] | 0.0001 | 0.0001 |
| Qwen2.5-7B 8-bit | 94/200 | 47/200 | -23.50 pts | 60 | 13 | 4.481 [2.484, 8.084] | <0.0001 | <0.0001 |
| Qwen3-4B | 88/200 | 49/200 | -19.50 pts | 52 | 13 | 3.889 [2.138, 7.073] | <0.0001 | <0.0001 |

## Validation-200 v5 API panel (strict) — Banglish vs Bangla

| Model | Bangla | Banglish | Delta | b (losses) | c (gains) | OR [95% CI] | Exact p | Holm p |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| Gemini 3.5 Flash | 163/200 | 136/200 | -13.50 pts | 31 | 4 | 7.0 [2.607, 18.796] | <0.0001 | <0.0001 |
| GPT-5.5 low | 172/200 | 169/200 | -1.50 pts | 6 | 3 | 1.857 [0.506, 6.811] | 0.5078 | 0.5078 |
| Claude Sonnet 4.6 | 162/200 | 130/200 | -16.00 pts | 39 | 7 | 5.267 [2.413, 11.497] | <0.0001 | <0.0001 |
| DeepSeek V4 Flash | 143/200 | 82/200 | -30.50 pts | 68 | 7 | 9.133 [4.298, 19.41] | <0.0001 | <0.0001 |
| Groq Llama 3.3 70B | 90/200 | 48/200 | -21.00 pts | 56 | 14 | 3.897 [2.188, 6.939] | <0.0001 | <0.0001 |

## Validation-200 v5 API panel (strict) — Banglish vs English

| Model | English | Banglish | Delta | b (losses) | c (gains) | OR [95% CI] | Exact p | Holm p |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| Gemini 3.5 Flash | 144/200 | 136/200 | -4.00 pts | 17 | 9 | 1.842 [0.836, 4.058] | 0.1686 | 0.1686 |
| GPT-5.5 low | 154/200 | 169/200 | +7.50 pts | 6 | 21 | 0.302 [0.126, 0.727] | 0.0059 | 0.0178 |
| Claude Sonnet 4.6 | 153/200 | 130/200 | -11.50 pts | 44 | 21 | 2.07 [1.237, 3.463] | 0.0059 | 0.0178 |
| DeepSeek V4 Flash | 132/200 | 82/200 | -25.00 pts | 59 | 9 | 6.263 [3.158, 12.422] | <0.0001 | <0.0001 |
| Groq Llama 3.3 70B | 102/200 | 48/200 | -27.00 pts | 69 | 15 | 4.484 [2.586, 7.776] | <0.0001 | <0.0001 |

## Validation-200 v5 API panel (secondary) — Banglish vs Bangla

| Model | Bangla | Banglish | Delta | b (losses) | c (gains) | OR [95% CI] | Exact p | Holm p |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| Gemini 3.5 Flash | 170/200 | 161/200 | -4.50 pts | 14 | 5 | 2.636 [0.988, 7.035] | 0.0636 | 0.1271 |
| GPT-5.5 low | 173/200 | 174/200 | +0.50 pts | 2 | 3 | 0.714 [0.141, 3.62] | 1.0000 | 1.0000 |
| Claude Sonnet 4.6 | 167/200 | 133/200 | -17.00 pts | 40 | 6 | 6.231 [2.722, 14.263] | <0.0001 | <0.0001 |
| DeepSeek V4 Flash | 152/200 | 96/200 | -28.00 pts | 63 | 7 | 8.467 [3.972, 18.046] | <0.0001 | <0.0001 |
| Groq Llama 3.3 70B | 92/200 | 56/200 | -18.00 pts | 52 | 16 | 3.182 [1.83, 5.532] | <0.0001 | <0.0001 |

## Validation-200 v5 API panel (secondary) — Banglish vs English

| Model | English | Banglish | Delta | b (losses) | c (gains) | OR [95% CI] | Exact p | Holm p |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| Gemini 3.5 Flash | 165/200 | 161/200 | -2.00 pts | 12 | 8 | 1.471 [0.615, 3.515] | 0.5034 | 0.5034 |
| GPT-5.5 low | 168/200 | 174/200 | +3.00 pts | 5 | 11 | 0.478 [0.173, 1.321] | 0.2101 | 0.4202 |
| Claude Sonnet 4.6 | 166/200 | 133/200 | -16.50 pts | 46 | 13 | 3.444 [1.879, 6.314] | <0.0001 | <0.0001 |
| DeepSeek V4 Flash | 148/200 | 96/200 | -26.00 pts | 59 | 7 | 7.933 [3.712, 16.954] | <0.0001 | <0.0001 |
| Groq Llama 3.3 70B | 111/200 | 56/200 | -27.50 pts | 70 | 15 | 4.548 [2.625, 7.882] | <0.0001 | <0.0001 |

## BEnQA human-gold 974 extension (strict) — Banglish vs Bangla

| Model | Bangla | Banglish | Delta | b (losses) | c (gains) | OR [95% CI] | Exact p | Holm p |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| Qwen2.5-3B | 323/974 | 285/974 | -3.90 pts | 153 | 115 | 1.329 [1.044, 1.692] | 0.0236 | 0.0236 |
| Gemini 3.5 Flash | 743/974 | 633/974 | -11.29 pts | 131 | 21 | 6.116 [3.877, 9.65] | <0.0001 | <0.0001 |
| GPT-5.5 none | 820/974 | 699/974 | -12.42 pts | 159 | 38 | 4.143 [2.914, 5.89] | <0.0001 | <0.0001 |
| Claude Sonnet 4.6 | 764/974 | 524/974 | -24.64 pts | 281 | 41 | 6.783 [4.897, 9.397] | <0.0001 | <0.0001 |
| DeepSeek V4 Flash | 756/974 | 438/974 | -32.65 pts | 361 | 43 | 8.31 [6.068, 11.382] | <0.0001 | <0.0001 |
| Groq Llama 3.3 70B | 547/974 | 333/974 | -21.97 pts | 302 | 88 | 3.418 [2.697, 4.332] | <0.0001 | <0.0001 |

## BEnQA human-gold 974 extension (strict) — Banglish vs English

| Model | English | Banglish | Delta | b (losses) | c (gains) | OR [95% CI] | Exact p | Holm p |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| Qwen2.5-3B | 490/974 | 285/974 | -21.05 pts | 296 | 91 | 3.24 [2.563, 4.096] | <0.0001 | <0.0001 |
| Gemini 3.5 Flash | 680/974 | 633/974 | -4.83 pts | 115 | 68 | 1.686 [1.25, 2.274] | 0.0006 | 0.0006 |
| GPT-5.5 none | 825/974 | 699/974 | -12.94 pts | 179 | 53 | 3.355 [2.472, 4.553] | <0.0001 | <0.0001 |
| Claude Sonnet 4.6 | 771/974 | 524/974 | -25.36 pts | 296 | 49 | 5.99 [4.433, 8.093] | <0.0001 | <0.0001 |
| DeepSeek V4 Flash | 791/974 | 438/974 | -36.24 pts | 392 | 39 | 9.937 [7.164, 13.783] | <0.0001 | <0.0001 |
| Groq Llama 3.3 70B | 622/974 | 333/974 | -29.67 pts | 355 | 66 | 5.346 [4.114, 6.946] | <0.0001 | <0.0001 |
