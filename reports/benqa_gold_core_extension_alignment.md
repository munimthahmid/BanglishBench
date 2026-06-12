# BEnQA Gold-Core And Extension Alignment

Updated: 2026-06-05

## Purpose

This note checks whether the new BEnQA extension points in the same direction
as the frozen validation-200 v5 BEnQA gold core. The goal is to make the
scale-extension argument explicit: validation-200 v5 remains the human-reviewed
gold core, while the BEnQA extension tests whether that pattern survives outside
the frozen core.

## Compared Evidence

- Gold core: BEnQA subset of `validation_200_v5`, Qwen2.5-3B.
- Extension pilot: `data/slices/benqa_extended_1000_v1_ai_pass_pilot130.jsonl`,
  Qwen2.5-3B.
- Full extension: `data/slices/benqa_extended_1000_v1_ai_pass.jsonl`,
  Qwen2.5-3B.
- Full extension API replication: `data/slices/benqa_extended_1000_v1_ai_pass.jsonl`,
  DeepSeek V4 Flash.
- Pilot report: `reports/qwen25_3b_benqa_ext_pilot130.md`.
- Pilot paired-gap report:
  `reports/qwen25_3b_benqa_ext_pilot130_paired_gap_analysis.md`.
- Full report: `reports/qwen25_3b_benqa_ext_full851.md`.
- Full paired-gap report:
  `reports/qwen25_3b_benqa_ext_full851_paired_gap_analysis.md`.
- DeepSeek full report: `reports/deepseek_v4_flash_benqa_ext_full851.md`.
- DeepSeek full paired-gap report:
  `reports/deepseek_v4_flash_benqa_ext_full851_paired_gap_analysis.md`.

## Accuracy Alignment

| Slice | Bangla | Reviewed Banglish | English | Ordering |
| --- | ---: | ---: | ---: | --- |
| BEnQA gold core | 49/144 = 34.03% | 38/144 = 26.39% | 66/144 = 45.83% | English > Bangla > Banglish |
| BEnQA extension pilot | 53/130 = 40.77% | 42/130 = 32.31% | 71/130 = 54.62% | English > Bangla > Banglish |
| BEnQA extension full, Qwen2.5-3B | 291/851 = 34.20% | 248/851 = 29.14% | 437/851 = 51.35% | English > Bangla > Banglish |
| BEnQA extension full, DeepSeek V4 Flash | 665/851 = 78.14% | 376/851 = 44.18% | 697/851 = 81.90% | English > Bangla > Banglish |

## Gap Alignment

| Gap | BEnQA gold core | BEnQA extension pilot |
| --- | ---: | ---: |
| Reviewed Banglish - Bangla | -7.64 pts | -8.46 pts |
| Reviewed Banglish - English | -19.44 pts | -22.31 pts |
| English - Bangla | +11.81 pts | +13.85 pts |

Full-extension paired gaps:

| Gap | BEnQA extension full | 95% bootstrap CI |
| --- | ---: | --- |
| Reviewed Banglish - Bangla | -5.05 pts | [-8.46, -1.65] |
| Reviewed Banglish - English | -22.21 pts | [-26.20, -18.10] |
| English - Bangla | +17.16 pts | [+13.28, +20.92] |

DeepSeek full-extension paired gaps:

| Gap | BEnQA extension full | 95% bootstrap CI |
| --- | ---: | --- |
| Reviewed Banglish - Bangla | -33.96 pts | [-37.84, -30.08] |
| Reviewed Banglish - English | -37.72 pts | [-41.36, -33.96] |
| English - Bangla | +3.76 pts | [+1.29, +6.35] |

## Interpretation

The extension does not merely run without parser failures; it reproduces the
same BEnQA ordering for Qwen2.5-3B and DeepSeek V4 Flash:

- English remains highest.
- Native Bangla remains in the middle.
- Reviewed Banglish remains lowest.

Both full-extension runs give fully negative paired confidence intervals for
reviewed Banglish against Bangla and English. This is an important thesis
result because it supports the claim that the validation-200 BEnQA pattern is
not an artifact of only 144 gold-core BEnQA rows or a single local Qwen model.

## Claim Boundary

Safe current claim:

"An 851-row pass-only BEnQA extension outside the frozen gold core reproduces
the same English > Bangla > reviewed Banglish ordering for Qwen2.5-3B and
DeepSeek V4 Flash, with paired reviewed-Banglish deficits against both Bangla
and English."

Do not yet claim:

- The extension has the same review standard as validation-200 v5.
- The scale result generalizes to all model families.

The extension is still silver-scale evidence because it is AI-assisted reviewed,
not human-reviewed.
