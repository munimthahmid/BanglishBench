# Qwen2.5-3B Guarded Generated-EN Answer Audit: Dev50 BEnQA MCQ

Updated: 2026-05-31

## Inputs

- Eval inputs: `results/runs/qwen25_3b_guarded_generated_en_v5_dev50/results/runs/qwen25_3b_guarded_generated_en_v5_dev50.jsonl`
- Item slice: `data/generated_views/validation200_v5_dev50_benqa_mcq_guarded_generated_en_answer_audit.jsonl`
- Summary CSV: `results/analysis/qwen25_3b_guarded_generated_en_v5_dev50_summary.csv`
- Item compare CSV: `results/analysis/qwen25_3b_guarded_generated_en_v5_dev50_item_compare.csv`

## Provenance

This report analyzes the reviewed-v5 guarded generated-English diagnostic. The repair restores source option/answer lines and falls back to Banglish when preservation would fail, so it is a conservative dev-only generated-view diagnostic rather than a pure English-translation result.

## Accuracy

| Variant | n | Correct | Accuracy | Parsed empty |
| --- | ---: | ---: | ---: | ---: |
| `banglish_clean` | 36 | 9 | 0.250 | 0 |
| `generated_en_qwen3_guarded` | 36 | 11 | 0.306 | 0 |

## Pairwise Changes vs `banglish_clean`

| Generated variant | Gains | Losses | Same correct | Same wrong |
| --- | ---: | ---: | ---: | ---: |
| `generated_en_qwen3_guarded` | 4 | 2 | 7 | 23 |

## Gate-Eligible Pairwise Changes

| Generated variant | Gate hard fails | Eligible n | Baseline correct | Generated correct | Gains | Losses | Same correct | Same wrong |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `generated_en_qwen3_guarded` | 0 | 36 | 9 | 11 | 4 | 2 | 7 | 23 |

## Example Gains

- `benqa_12th-Biology-II_0179` `generated_en_qwen3_guarded` gold=A baseline=B generated=A
- `benqa_12th-Biology-II_0325` `generated_en_qwen3_guarded` gold=A baseline=B generated=A
- `benqa_12th-Chemistry-I_0190` `generated_en_qwen3_guarded` gold=B baseline=C generated=B
- `benqa_8th-Math_0031` `generated_en_qwen3_guarded` gold=D baseline=B generated=D

## Example Losses

- `benqa_12th-Physics-II_0131` `generated_en_qwen3_guarded` gold=B baseline=B generated=D
- `benqa_12th-Physics-I_0106` `generated_en_qwen3_guarded` gold=D baseline=D generated=C

## Decision Rule

This is a dev-only diagnostic. It can justify dropping or inspecting
a generated-view path, but it must not be promoted to a held-out
mitigation claim. A deployable route requires preservation-gate
eligibility, a locked agreement route, and a held-out test
protocol.
