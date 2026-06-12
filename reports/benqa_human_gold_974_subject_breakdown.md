# BEnQA Human-Gold 974 Per-Subject Script Gap

Updated: 2026-06-11

Macro-subject breakdown of the 974-row extension triads. The gap
column is reviewed-Banglish accuracy minus Bangla accuracy in points;
the p-value is a within-subject McNemar exact test.

- Machine-readable summary: `results/analysis/benqa_human_gold_974_subject_breakdown.csv`
- Builder: `scripts/analyze_extension_subject_breakdown.py`

## Qwen2.5-3B

| Subject | n | Bangla | Banglish | English | Gap (pts) | b | c | Exact p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Biology | 229 | 28.38% | 25.33% | 52.84% | -3.06 | 36 | 29 | 0.4570 |
| Chemistry | 221 | 31.22% | 25.79% | 44.8% | -5.43 | 38 | 26 | 0.1686 |
| Physics | 226 | 34.96% | 28.32% | 60.18% | -6.64 | 39 | 24 | 0.0769 |
| Math | 223 | 39.01% | 36.32% | 41.7% | -2.69 | 30 | 24 | 0.4966 |
| Science | 75 | 30.67% | 33.33% | 54.67% | +2.67 | 10 | 12 | 0.8318 |

## Gemini 3.5 Flash

| Subject | n | Bangla | Banglish | English | Gap (pts) | b | c | Exact p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Biology | 229 | 90.83% | 77.73% | 80.35% | -13.10 | 34 | 4 | 0.0000 |
| Chemistry | 221 | 85.52% | 71.04% | 74.66% | -14.48 | 34 | 2 | 0.0000 |
| Physics | 226 | 77.43% | 67.26% | 73.89% | -10.18 | 29 | 6 | 0.0001 |
| Math | 223 | 46.64% | 35.87% | 44.84% | -10.76 | 30 | 6 | 0.0001 |
| Science | 75 | 89.33% | 88.0% | 85.33% | -1.33 | 4 | 3 | 1.0000 |

## GPT-5.5 none

| Subject | n | Bangla | Banglish | English | Gap (pts) | b | c | Exact p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Biology | 229 | 82.53% | 64.63% | 85.15% | -17.90 | 51 | 10 | 0.0000 |
| Chemistry | 221 | 88.69% | 73.76% | 87.33% | -14.93 | 36 | 3 | 0.0000 |
| Physics | 226 | 87.17% | 73.89% | 87.61% | -13.27 | 36 | 6 | 0.0000 |
| Math | 223 | 76.68% | 73.09% | 78.48% | -3.59 | 25 | 17 | 0.2800 |
| Science | 75 | 89.33% | 77.33% | 85.33% | -12.00 | 11 | 2 | 0.0225 |

## Claude Sonnet 4.6

| Subject | n | Bangla | Banglish | English | Gap (pts) | b | c | Exact p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Biology | 229 | 80.79% | 47.6% | 78.17% | -33.19 | 84 | 8 | 0.0000 |
| Chemistry | 221 | 79.64% | 53.85% | 79.19% | -25.79 | 66 | 9 | 0.0000 |
| Physics | 226 | 79.2% | 49.12% | 81.42% | -30.09 | 75 | 7 | 0.0000 |
| Math | 223 | 71.75% | 65.47% | 75.34% | -6.28 | 28 | 14 | 0.0436 |
| Science | 75 | 85.33% | 52.0% | 86.67% | -33.33 | 28 | 3 | 0.0000 |

## DeepSeek V4 Flash

| Subject | n | Bangla | Banglish | English | Gap (pts) | b | c | Exact p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Biology | 229 | 72.93% | 34.93% | 80.35% | -37.99 | 99 | 12 | 0.0000 |
| Chemistry | 221 | 81.9% | 42.53% | 81.9% | -39.37 | 98 | 11 | 0.0000 |
| Physics | 226 | 80.97% | 43.81% | 82.74% | -37.17 | 90 | 6 | 0.0000 |
| Math | 223 | 74.89% | 61.43% | 79.82% | -13.45 | 39 | 9 | 0.0000 |
| Science | 75 | 77.33% | 37.33% | 81.33% | -40.00 | 35 | 5 | 0.0000 |

## Groq Llama 3.3 70B

| Subject | n | Bangla | Banglish | English | Gap (pts) | b | c | Exact p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Biology | 229 | 58.95% | 32.75% | 65.94% | -26.20 | 81 | 21 | 0.0000 |
| Chemistry | 221 | 56.11% | 32.13% | 64.25% | -23.98 | 74 | 21 | 0.0000 |
| Physics | 226 | 57.52% | 33.19% | 65.93% | -24.34 | 77 | 22 | 0.0000 |
| Math | 223 | 51.57% | 41.7% | 57.4% | -9.87 | 39 | 17 | 0.0046 |
| Science | 75 | 57.33% | 25.33% | 69.33% | -32.00 | 31 | 7 | 0.0001 |
