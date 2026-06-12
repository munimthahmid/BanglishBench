# GPT-5.5 Diagnostic Slice

Updated: 2026-06-04

## Purpose

This slice targets the frontier-model question raised by the Gemini audit:
whether reviewed Banglish failures persist because of semantic understanding
or because the code-mixed setting destabilizes answer format and unit
normalization. It is not the final full SOTA run.

## Artifacts

- Source items: `data/slices/validation_200_v5.jsonl`
- Gemini item audit: `results/analysis/gemini_3_5_flash_validation200_v5_items.csv`
- Diagnostic slice: `data/slices/openai_gpt55_diagnostic_60_v5.jsonl`
- Items: 60
- Planned API calls with 3 variants: 180

## Dataset Counts

| Dataset | Items |
| --- | ---: |
| `banglamath` | 40 |
| `benqa` | 20 |

## Selection Buckets

| Bucket | Items |
| --- | ---: |
| `all_strict_correct_control` | 6 |
| `bangla_correct_banglish_wrong` | 31 |
| `banglish_recoverable` | 8 |
| `banglish_unrecovered_wrong` | 8 |
| `benqa_banglish_wrong` | 7 |

## Item IDs

banglamath_0182, banglamath_0183, banglamath_0185, banglamath_0227, banglamath_0231, banglamath_0232, banglamath_0233, banglamath_0234, banglamath_0518, banglamath_0519, banglamath_0521, banglamath_0539, banglamath_0540, banglamath_0542, banglamath_0552, banglamath_0557, banglamath_0558, banglamath_1694, benqa_10th-Biology_0090, benqa_10th-Biology_0188, benqa_10th-Chemistry_0111, benqa_10th-Math_0186, benqa_12th-Biology-II_0122, benqa_12th-Biology-I_0039, benqa_12th-Biology-I_0056, benqa_12th-Chemistry-II_0067, benqa_12th-Chemistry-II_0228, benqa_12th-Physics-II_0219, benqa_8th-Science_0086, benqa_8th-Science_0098, benqa_8th-Science_0159, banglamath_0184, banglamath_0187, banglamath_0188, banglamath_0189, banglamath_0226, banglamath_0553, banglamath_1698, banglamath_1703, benqa_10th-Biology_0128, benqa_10th-Chemistry_0280, benqa_10th-Math-II_0062, benqa_12th-Chemistry-I_0286, benqa_12th-Physics-I_0253, benqa_12th-Physics-I_0256, benqa_8th-Science_0127, banglamath_0181, banglamath_0186, banglamath_0522, banglamath_0531, banglamath_0532, banglamath_0533, banglamath_0538, banglamath_0541, banglamath_0228, banglamath_0229, banglamath_0230, banglamath_0237, banglamath_0526, banglamath_0549
