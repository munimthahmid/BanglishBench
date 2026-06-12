# Qwen/Qwen3-4B-Instruct-2507 Generated-BN Answer Audit: Dev50 BEnQA MCQ

Updated: 2026-05-31

## Inputs

- Eval inputs: `results/runs/qwen3_4b_generated_bn_v5_pv2_dev50`
- Item slice: `data/generated_views/validation200_v5_dev50_benqa_mcq_protected_v2_generated_bn_answer_audit.jsonl`
- Summary CSV: `results/analysis/qwen3_4b_generated_bn_v5_pv2_dev50_summary.csv`
- Item compare CSV: `results/analysis/qwen3_4b_generated_bn_v5_pv2_dev50_item_compare.csv`

## Provenance

This report analyzes reviewed-v5 protected-v2 deterministic generated-Bengali dev candidates under the tightened formula-preservation gate. It is dev-only evidence and not a held-out mitigation claim.

## Accuracy

| Variant | n | Correct | Accuracy | Parsed empty |
| --- | ---: | ---: | ---: | ---: |
| `banglish_clean` | 36 | 15 | 0.417 | 2 |
| `generated_bn_bnb_protected_v2` | 36 | 16 | 0.444 | 1 |
| `generated_bn_phonetic_protected_v2` | 36 | 13 | 0.361 | 0 |

## Pairwise Changes vs `banglish_clean`

| Generated variant | Gains | Losses | Same correct | Same wrong |
| --- | ---: | ---: | ---: | ---: |
| `generated_bn_phonetic_protected_v2` | 2 | 4 | 11 | 19 |
| `generated_bn_bnb_protected_v2` | 3 | 2 | 13 | 18 |

## Gate-Eligible Pairwise Changes

| Generated variant | Gate hard fails | Eligible n | Baseline correct | Generated correct | Gains | Losses | Same correct | Same wrong |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `generated_bn_phonetic_protected_v2` | 16 | 20 | 10 | 9 | 2 | 3 | 7 | 8 |
| `generated_bn_bnb_protected_v2` | 16 | 20 | 10 | 11 | 2 | 1 | 9 | 8 |

## Example Gains

- `benqa_12th-Biology-II_0179` `generated_bn_phonetic_protected_v2` gold=A baseline=D generated=A
- `benqa_12th-Chemistry-II_0240` `generated_bn_bnb_protected_v2` gold=B baseline=C generated=B
- `benqa_8th-Math_0085` `generated_bn_phonetic_protected_v2` gold=C baseline=D generated=C
- `benqa_8th-Math_0085` `generated_bn_bnb_protected_v2` gold=C baseline=D generated=C
- `benqa_8th-Science_0153` `generated_bn_bnb_protected_v2` gold=C baseline=D generated=C

## Example Losses

- `benqa_10th-Biology_0143` `generated_bn_phonetic_protected_v2` gold=C baseline=C generated=D
- `benqa_10th-Biology_0143` `generated_bn_bnb_protected_v2` gold=C baseline=C generated=D
- `benqa_10th-Physics_0045` `generated_bn_phonetic_protected_v2` gold=A baseline=A generated=B
- `benqa_10th-Physics_0296` `generated_bn_phonetic_protected_v2` gold=D baseline=D generated=B
- `benqa_12th-Chemistry-I_0140` `generated_bn_bnb_protected_v2` gold=D baseline=D generated=C
- `benqa_12th-Math-I_0120` `generated_bn_phonetic_protected_v2` gold=D baseline=D generated=C

## Decision Rule

This is a dev-only diagnostic. It can justify dropping or inspecting
a generated-BN path, but it must not be promoted to a held-out
mitigation claim. A deployable route requires preservation-gate
eligibility, a locked generated-English view, and a held-out test
protocol.
