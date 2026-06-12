# Qwen/Qwen2.5-3B-Instruct Generated-BN Answer Audit: Dev50 BEnQA MCQ

Updated: 2026-05-28

## Inputs

- Eval inputs: `results/runs/qwen25_3b_generated_bn_answer_audit_dev50/results/runs/qwen25_3b_generated_bn_answer_audit_dev50.jsonl`
- Item slice: `data/generated_views/validation200_v4_dev50_benqa_mcq_protected_generated_bn_answer_audit.jsonl`
- Summary CSV: `results/analysis/qwen25_3b_generated_bn_answer_audit_dev50_summary.csv`
- Item compare CSV: `results/analysis/qwen25_3b_generated_bn_answer_audit_dev50_item_compare.csv`
- Bootstrap CSVs:
  - `results/analysis/qwen25_3b_generated_bn_answer_audit_phonetic_vs_banglish_bootstrap.csv`
  - `results/analysis/qwen25_3b_generated_bn_answer_audit_bnb_vs_banglish_bootstrap.csv`

## Provenance

This report analyzes the historical protected-v1 deterministic files. They
predate the tightened scientific-token gate and must not be presented as answer
audits of the expanded-v2 candidates.

## Accuracy

| Variant | n | Correct | Accuracy | Parsed empty |
| --- | ---: | ---: | ---: | ---: |
| `banglish_clean` | 36 | 8 | 0.222 | 0 |
| `generated_bn_bnb_protected` | 36 | 7 | 0.194 | 0 |
| `generated_bn_phonetic_protected` | 36 | 14 | 0.389 | 0 |

## Pairwise Changes vs Banglish

| Generated variant | Gains | Losses | Same correct | Same wrong |
| --- | ---: | ---: | ---: | ---: |
| `generated_bn_phonetic_protected` | 8 | 2 | 6 | 20 |
| `generated_bn_bnb_protected` | 3 | 4 | 4 | 25 |

## Paired Bootstrap vs Banglish

Intervals are right-minus-left accuracy deltas in percentage points over the
36 paired dev items.

| Generated variant | Delta | 95% CI | Direction p |
| --- | ---: | ---: | ---: |
| `generated_bn_phonetic_protected` | +16.7 pts | [0.0, +33.3] | 0.0303 |
| `generated_bn_bnb_protected` | -2.8 pts | [-16.7, +11.1] | 0.4249 |

## Example Gains

- `benqa_10th-Biology_0057` `generated_bn_phonetic_protected` gold=C baseline=D generated=C
- `benqa_10th-Chemistry_0280` `generated_bn_phonetic_protected` gold=A baseline=D generated=A
- `benqa_10th-Math-II_0367` `generated_bn_phonetic_protected` gold=C baseline=B generated=C
- `benqa_10th-Physics_0045` `generated_bn_phonetic_protected` gold=A baseline=B generated=A
- `benqa_12th-Biology-II_0119` `generated_bn_phonetic_protected` gold=C baseline=B generated=C
- `benqa_12th-Biology-I_0218` `generated_bn_phonetic_protected` gold=B baseline=D generated=B
- `benqa_12th-Biology-I_0218` `generated_bn_bnb_protected` gold=B baseline=D generated=B
- `benqa_12th-Math-I_0202` `generated_bn_phonetic_protected` gold=B baseline=D generated=B

## Example Losses

- `benqa_10th-Chemistry_0374` `generated_bn_phonetic_protected` gold=B baseline=B generated=D
- `benqa_10th-Physics_0055` `generated_bn_bnb_protected` gold=D baseline=D generated=B
- `benqa_12th-Chemistry-II_0240` `generated_bn_phonetic_protected` gold=B baseline=B generated=A
- `benqa_12th-Chemistry-II_0240` `generated_bn_bnb_protected` gold=B baseline=B generated=C
- `benqa_12th-Math-II_0230` `generated_bn_bnb_protected` gold=D baseline=D generated=B
- `benqa_12th-Math-II_0234` `generated_bn_bnb_protected` gold=A baseline=A generated=B

## Decision Rule

This is a dev-only diagnostic. It can justify dropping or inspecting a
historical generated-BN path, but it must not be promoted to a held-out
mitigation claim. Reviewed-v5 protected-v2 candidates have since received
separate answer audits but fail the tightened formula-expression gate on 16/36
rows. Protected-v3 candidates repair that gate and need their own answer audit
plus a locked generated-English view before any test150 protocol.
