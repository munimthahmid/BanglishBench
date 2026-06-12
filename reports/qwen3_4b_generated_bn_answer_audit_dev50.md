# Qwen3-4B Generated-BN Answer Audit: Dev50 BEnQA MCQ

Updated: 2026-05-28

## Inputs

- Eval inputs: `results/runs/qwen3_4b_generated_bn_answer_audit_dev50/results/runs/qwen3_4b_generated_bn_answer_audit_dev50.jsonl`
- Item slice: `data/generated_views/validation200_v4_dev50_benqa_mcq_protected_generated_bn_answer_audit.jsonl`
- Summary CSV: `results/analysis/qwen3_4b_generated_bn_answer_audit_dev50_summary.csv`
- Item compare CSV: `results/analysis/qwen3_4b_generated_bn_answer_audit_dev50_item_compare.csv`
- Bootstrap CSVs:
  - `results/analysis/qwen3_4b_generated_bn_answer_audit_bnb_vs_banglish_bootstrap.csv`
  - `results/analysis/qwen3_4b_generated_bn_answer_audit_phonetic_vs_banglish_bootstrap.csv`

## Provenance

This report analyzes the historical protected-v1 deterministic files. They
predate the tightened scientific-token gate and must not be presented as answer
audits of the expanded-v2 candidates.

## Accuracy

| Variant | n | Correct | Accuracy | Parsed empty |
| --- | ---: | ---: | ---: | ---: |
| `banglish_clean` | 36 | 15 | 0.417 | 2 |
| `generated_bn_bnb_protected` | 36 | 17 | 0.472 | 0 |
| `generated_bn_phonetic_protected` | 36 | 11 | 0.306 | 0 |

## Pairwise Changes vs Banglish

| Generated variant | Gains | Losses | Same correct | Same wrong |
| --- | ---: | ---: | ---: | ---: |
| `generated_bn_phonetic_protected` | 2 | 6 | 9 | 19 |
| `generated_bn_bnb_protected` | 4 | 2 | 13 | 17 |

## Paired Bootstrap vs Banglish

Intervals are right-minus-left accuracy deltas in percentage points over the
36 paired dev items.

| Generated variant | Delta | 95% CI | Direction p |
| --- | ---: | ---: | ---: |
| `generated_bn_bnb_protected` | +5.6 pts | [-8.3, +19.4] | 0.2603 |
| `generated_bn_phonetic_protected` | -11.1 pts | [-25.0, +2.8] | 0.1000 |

## Example Gains

- `benqa_12th-Chemistry-II_0240` `generated_bn_bnb_protected` gold=B baseline=C generated=B
- `benqa_12th-Math-II_0234` `generated_bn_bnb_protected` gold=A baseline= generated=A
- `benqa_12th-Math-I_0088` `generated_bn_phonetic_protected` gold=C baseline=D generated=C
- `benqa_8th-Math_0085` `generated_bn_phonetic_protected` gold=C baseline=D generated=C
- `benqa_8th-Math_0085` `generated_bn_bnb_protected` gold=C baseline=D generated=C
- `benqa_8th-Science_0153` `generated_bn_bnb_protected` gold=C baseline=D generated=C

## Example Losses

- `benqa_10th-Biology_0143` `generated_bn_phonetic_protected` gold=C baseline=C generated=D
- `benqa_10th-Biology_0143` `generated_bn_bnb_protected` gold=C baseline=C generated=D
- `benqa_10th-Physics_0045` `generated_bn_phonetic_protected` gold=A baseline=A generated=B
- `benqa_10th-Physics_0296` `generated_bn_phonetic_protected` gold=D baseline=D generated=B
- `benqa_12th-Chemistry-I_0140` `generated_bn_phonetic_protected` gold=D baseline=D generated=C
- `benqa_12th-Chemistry-I_0140` `generated_bn_bnb_protected` gold=D baseline=D generated=C
- `benqa_12th-Math-I_0120` `generated_bn_phonetic_protected` gold=D baseline=D generated=C
- `benqa_12th-Math-I_0202` `generated_bn_phonetic_protected` gold=B baseline=B generated=D

## Decision Rule

This is a dev-only diagnostic. It can justify dropping or inspecting a
historical generated-BN path, but it must not be promoted to a held-out
mitigation claim. Reviewed-v5 protected-v2 candidates have since received
separate answer audits but fail the tightened formula-expression gate on 16/36
rows. Protected-v3 candidates repair that gate and need their own answer audit
plus a locked generated-English view before any test150 protocol.
