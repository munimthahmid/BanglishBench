# Qwen/Qwen2.5-3B-Instruct Generated-BN Answer Audit: Dev50 BEnQA MCQ

Updated: 2026-05-31

## Inputs

- Eval inputs: `results/runs/qwen25_3b_generated_bn_v5_pv3_dev50/results/runs/qwen25_3b_generated_bn_v5_pv3_dev50.jsonl`
- Item slice: `data/generated_views/validation200_v5_dev50_benqa_mcq_protected_v3_generated_bn_answer_audit.jsonl`
- Summary CSV: `results/analysis/qwen25_3b_generated_bn_v5_pv3_dev50_summary.csv`
- Item compare CSV: `results/analysis/qwen25_3b_generated_bn_v5_pv3_dev50_item_compare.csv`

## Provenance

This report analyzes reviewed-v5 formulaish protected-v3 deterministic generated-Bengali dev candidates under the tightened preservation gate. It is dev-only evidence and not a held-out mitigation claim.

## Accuracy

| Variant | n | Correct | Accuracy | Parsed empty |
| --- | ---: | ---: | ---: | ---: |
| `banglish_clean` | 36 | 9 | 0.250 | 0 |
| `generated_bn_bnb_protected_v3` | 36 | 9 | 0.250 | 0 |
| `generated_bn_phonetic_protected_v3` | 36 | 10 | 0.278 | 0 |

## Pairwise Changes vs `banglish_clean`

| Generated variant | Gains | Losses | Same correct | Same wrong |
| --- | ---: | ---: | ---: | ---: |
| `generated_bn_phonetic_protected_v3` | 6 | 5 | 4 | 21 |
| `generated_bn_bnb_protected_v3` | 6 | 6 | 3 | 21 |

## Gate-Eligible Pairwise Changes

| Generated variant | Gate hard fails | Eligible n | Baseline correct | Generated correct | Gains | Losses | Same correct | Same wrong |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `generated_bn_phonetic_protected_v3` | 0 | 36 | 9 | 10 | 6 | 5 | 4 | 21 |
| `generated_bn_bnb_protected_v3` | 0 | 36 | 9 | 9 | 6 | 6 | 3 | 21 |

## Paired Bootstrap vs Banglish

Intervals are right-minus-left accuracy deltas in percentage points over the
36 paired dev items.

| Generated variant | Delta | 95% CI | Direction p |
| --- | ---: | ---: | ---: |
| `generated_bn_phonetic_protected_v3` | +2.8 pts | [-13.9, +19.4] | 0.4350 |
| `generated_bn_bnb_protected_v3` | +0.0 pts | [-19.4, +19.4] | 0.5553 |

## Example Gains

- `benqa_10th-Biology_0057` `generated_bn_phonetic_protected_v3` gold=C baseline=D generated=C
- `benqa_10th-Biology_0057` `generated_bn_bnb_protected_v3` gold=C baseline=D generated=C
- `benqa_10th-Math_0032` `generated_bn_phonetic_protected_v3` gold=B baseline=A generated=B
- `benqa_10th-Math_0032` `generated_bn_bnb_protected_v3` gold=B baseline=A generated=B
- `benqa_12th-Biology-II_0119` `generated_bn_phonetic_protected_v3` gold=C baseline=B generated=C
- `benqa_12th-Biology-I_0218` `generated_bn_phonetic_protected_v3` gold=B baseline=D generated=B
- `benqa_12th-Biology-I_0218` `generated_bn_bnb_protected_v3` gold=B baseline=D generated=B
- `benqa_12th-Math-I_0202` `generated_bn_phonetic_protected_v3` gold=B baseline=D generated=B

## Example Losses

- `benqa_10th-Chemistry_0374` `generated_bn_phonetic_protected_v3` gold=B baseline=B generated=D
- `benqa_10th-Physics_0055` `generated_bn_bnb_protected_v3` gold=D baseline=D generated=B
- `benqa_12th-Chemistry-II_0054` `generated_bn_phonetic_protected_v3` gold=A baseline=A generated=D
- `benqa_12th-Chemistry-II_0054` `generated_bn_bnb_protected_v3` gold=A baseline=A generated=D
- `benqa_12th-Chemistry-II_0240` `generated_bn_phonetic_protected_v3` gold=B baseline=B generated=A
- `benqa_12th-Chemistry-II_0240` `generated_bn_bnb_protected_v3` gold=B baseline=B generated=A
- `benqa_12th-Math-II_0230` `generated_bn_bnb_protected_v3` gold=D baseline=D generated=B
- `benqa_12th-Physics-II_0131` `generated_bn_phonetic_protected_v3` gold=B baseline=B generated=A

## Decision Rule

This is a dev-only diagnostic. It can justify dropping or inspecting
a generated-BN path, but it must not be promoted to a held-out
mitigation claim. A deployable route requires preservation-gate
eligibility, a locked generated-English view, and a held-out test
protocol.

Current decision: do not launch test150 from generated-BN alone. Protected-v3
fixes deterministic preservation, but Qwen2.5-3B is flat to +1 item with wide
uncertainty. A later guarded generated-English agreement route is negative
on dev, so this remains below the held-out launch bar.
