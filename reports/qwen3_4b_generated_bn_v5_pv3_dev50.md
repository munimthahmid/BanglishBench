# Qwen/Qwen3-4B-Instruct-2507 Generated-BN Answer Audit: Dev50 BEnQA MCQ

Updated: 2026-05-31

## Inputs

- Eval inputs: `results/runs/qwen3_4b_generated_bn_v5_pv3_dev50/results/runs/qwen3_4b_generated_bn_v5_pv3_dev50.jsonl`
- Item slice: `data/generated_views/validation200_v5_dev50_benqa_mcq_protected_v3_generated_bn_answer_audit.jsonl`
- Summary CSV: `results/analysis/qwen3_4b_generated_bn_v5_pv3_dev50_summary.csv`
- Item compare CSV: `results/analysis/qwen3_4b_generated_bn_v5_pv3_dev50_item_compare.csv`

## Provenance

This report analyzes reviewed-v5 formulaish protected-v3 deterministic generated-Bengali dev candidates under the tightened preservation gate. It is dev-only evidence and not a held-out mitigation claim.

## Accuracy

| Variant | n | Correct | Accuracy | Parsed empty |
| --- | ---: | ---: | ---: | ---: |
| `banglish_clean` | 36 | 15 | 0.417 | 2 |
| `generated_bn_bnb_protected_v3` | 36 | 17 | 0.472 | 1 |
| `generated_bn_phonetic_protected_v3` | 36 | 14 | 0.389 | 1 |

## Pairwise Changes vs `banglish_clean`

| Generated variant | Gains | Losses | Same correct | Same wrong |
| --- | ---: | ---: | ---: | ---: |
| `generated_bn_phonetic_protected_v3` | 3 | 4 | 11 | 18 |
| `generated_bn_bnb_protected_v3` | 4 | 2 | 13 | 17 |

## Gate-Eligible Pairwise Changes

| Generated variant | Gate hard fails | Eligible n | Baseline correct | Generated correct | Gains | Losses | Same correct | Same wrong |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `generated_bn_phonetic_protected_v3` | 0 | 36 | 15 | 14 | 3 | 4 | 11 | 18 |
| `generated_bn_bnb_protected_v3` | 0 | 36 | 15 | 17 | 4 | 2 | 13 | 17 |

## Paired Bootstrap vs Banglish

Intervals are right-minus-left accuracy deltas in percentage points over the
36 paired dev items.

| Generated variant | Delta | 95% CI | Direction p |
| --- | ---: | ---: | ---: |
| `generated_bn_phonetic_protected_v3` | -2.8 pts | [-16.7, +11.1] | 0.4284 |
| `generated_bn_bnb_protected_v3` | +5.6 pts | [-8.3, +19.4] | 0.2704 |

## Example Gains

- `benqa_12th-Biology-II_0179` `generated_bn_phonetic_protected_v3` gold=A baseline=D generated=A
- `benqa_12th-Biology-II_0325` `generated_bn_bnb_protected_v3` gold=A baseline=C generated=A
- `benqa_12th-Biology-I_0039` `generated_bn_bnb_protected_v3` gold=C baseline=B generated=C
- `benqa_12th-Math-I_0088` `generated_bn_phonetic_protected_v3` gold=C baseline=D generated=C
- `benqa_8th-Math_0085` `generated_bn_phonetic_protected_v3` gold=C baseline=D generated=C
- `benqa_8th-Math_0085` `generated_bn_bnb_protected_v3` gold=C baseline=D generated=C
- `benqa_8th-Science_0153` `generated_bn_bnb_protected_v3` gold=C baseline=D generated=C

## Example Losses

- `benqa_10th-Biology_0143` `generated_bn_phonetic_protected_v3` gold=C baseline=C generated=D
- `benqa_10th-Biology_0143` `generated_bn_bnb_protected_v3` gold=C baseline=C generated=D
- `benqa_10th-Physics_0045` `generated_bn_phonetic_protected_v3` gold=A baseline=A generated=B
- `benqa_10th-Physics_0296` `generated_bn_phonetic_protected_v3` gold=D baseline=D generated=B
- `benqa_12th-Chemistry-II_0305` `generated_bn_phonetic_protected_v3` gold=D baseline=D generated=C
- `benqa_12th-Chemistry-II_0305` `generated_bn_bnb_protected_v3` gold=D baseline=D generated=C

## Decision Rule

This is a dev-only diagnostic. It can justify dropping or inspecting
a generated-BN path, but it must not be promoted to a held-out
mitigation claim. A deployable route requires preservation-gate
eligibility, a locked generated-English view, and a held-out test
protocol.

Current decision: do not launch test150 from generated-BN alone. Protected-v3
fixes deterministic preservation, but the answer effect is still a weak
Qwen3/BNB dev lead with a wide interval. A later guarded generated-English
agreement route is still only +1 item on dev, so this remains below the
held-out launch bar.
