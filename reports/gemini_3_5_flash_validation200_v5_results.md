# Gemini 3.5 Flash Validation-200 V5 Results

Updated: 2026-06-04

## Scope

This report adds the first frontier/API model row to the frozen validation-200 v5
Bangla/Banglish/English audit. The primary metric uses the same strict parser as
the open-model runs. A secondary sensitivity is reported separately for parser
and unit-normalization recoveries; it does not replace the strict benchmark.

- Raw API responses: `results/api_audit/gemini_3_5_flash_validation200_v5_raw.jsonl`
- Imported strict rows: `results/analysis/gemini_3_5_flash_validation200_v5_imported.jsonl`
- Item audit CSV: `results/analysis/gemini_3_5_flash_validation200_v5_items.csv`
- Summary CSV: `results/analysis/gemini_3_5_flash_validation200_v5_summary.csv`
- Paired gap CSV: `results/analysis/gemini_3_5_flash_validation200_v5_paired_gaps.csv`
- Recoverability CSV: `results/analysis/gemini_3_5_flash_validation200_v5_recoverability_items.csv`
- Qwen comparison CSV: `results/analysis/gemini_3_5_flash_validation200_v5_qwen_comparison.csv`

## Headline

- Strict all-200 accuracy is 163/200 (81.5%) Bangla, 136/200 (68.0%) reviewed Banglish, and 144/200 (72.0%) English.
- The strict all-200 Banglish gap is -13.5 points versus Bangla and -4.0 points
  versus English. The Bangla comparison is significant by the exact paired
  discordance test; the English comparison is smaller.
- BEnQA remains strong but still not equal: 133/144 (92.4%) Bangla, 124/144 (86.1%) Banglish, and 129/144 (89.6%) English.
- BanglaMATH is the key protocol finding. Strict scoring gives 30/56 (53.6%) Bangla, 12/56 (21.4%) Banglish, and 15/56 (26.8%) English; after the
  secondary numeric/unit sensitivity this becomes 36/56 (64.3%) Bangla, 34/56 (60.7%) Banglish, and 35/56 (62.5%) English.
- Interpretation: the frontier model mostly reduces semantic Banglish failure,
  especially on math, but the code-mixed setting still creates response-format
  and normalization instability. That is a stronger thesis claim than just
  adding a benchmark row.

## Strict Accuracy

| Dataset | Bangla | Reviewed Banglish | English |
| --- | ---: | ---: | ---: |
| All | 163/200 (81.5%) | 136/200 (68.0%) | 144/200 (72.0%) |
| BEnQA | 133/144 (92.4%) | 124/144 (86.1%) | 129/144 (89.6%) |
| BanglaMATH | 30/56 (53.6%) | 12/56 (21.4%) | 15/56 (26.8%) |

## Secondary Parser/Unit Sensitivity

| Dataset | Bangla | Reviewed Banglish | English | Strict-to-secondary gains |
| --- | ---: | ---: | ---: | --- |
| All | 170/200 (85.0%) | 161/200 (80.5%) | 165/200 (82.5%) | Bangla +7, Reviewed Banglish +25, English +21 |
| BEnQA | 134/144 (93.1%) | 127/144 (88.2%) | 130/144 (90.3%) | Bangla +1, Reviewed Banglish +3, English +1 |
| BanglaMATH | 36/56 (64.3%) | 34/56 (60.7%) | 35/56 (62.5%) | Bangla +6, Reviewed Banglish +22, English +20 |

## Paired Script Gaps

Right minus left, matched by item id. The p-value is an exact binomial test on
discordant pairs.

| Score | Dataset | Comparison | Delta | Left-only | Right-only | p |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| strict | All | Banglish - Bangla | -13.5 | 31 | 4 | 3e-06 |
| strict | All | Banglish - English | -4.0 | 17 | 9 | 0.168638 |
| strict | BanglaMATH | Banglish - Bangla | -32.1 | 18 | 0 | 8e-06 |
| strict | BanglaMATH | Banglish - English | -5.4 | 5 | 2 | 0.453125 |
| secondary | All | Banglish - Bangla | -4.5 | 14 | 5 | 0.063568 |
| secondary | All | Banglish - English | -2.0 | 12 | 8 | 0.503445 |

## Format And Cost Signals

- Finish reasons: MAX_TOKENS=10, STOP=590.
- Key usage by environment variable name: GEMINI_API_KEY=577, GEMINI_API_KEY2=11, GEMINI_API_KEY3=12.
- Recoverable non-strict rows: 53 total (choice_markdown_recovery=5, short_extended_unit=12, short_numeric_only=36).

| Variant | Parsed empty | MAX_TOKENS | Long >120 chars | Mean output tokens |
| --- | ---: | ---: | ---: | ---: |
| Bangla | 1 | 2 | 33 | 47.2 |
| Reviewed Banglish | 3 | 3 | 49 | 70.8 |
| English | 2 | 5 | 49 | 68.0 |

## Open-Model Comparison

| Model | Score | Bangla | Reviewed Banglish | English | Banglish-Bangla |
| --- | --- | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | strict | 54/200 | 41/200 | 71/200 | -6.5 pts |
| Qwen2.5-7B 8-bit | strict | 65/200 | 47/200 | 94/200 | -9.0 pts |
| Qwen3-4B | strict | 80/200 | 49/200 | 88/200 | -15.5 pts |
| Gemini 3.5 Flash | strict | 163/200 | 136/200 | 144/200 | -13.5 pts |
| Gemini 3.5 Flash | secondary | 170/200 | 161/200 | 165/200 | -4.5 pts |

## Use In Thesis

This should be framed as a bounded frontier-model audit, not as the final SOTA
sweep. It justifies the next paid runs because it shows exactly where extra
models matter: whether the Gemini pattern generalizes across frontier systems,
and whether Banglish robustness is now mostly semantic or mostly protocol-level
format compliance.
