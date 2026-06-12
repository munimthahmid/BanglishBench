# Generated-BN Answer Audit Slice: Dev50 BEnQA MCQ

Updated: 2026-06-11

## Purpose

This slice joins a locked dev50 BEnQA MCQ item subset with generated
Bengali candidate views so the standard evaluator can answer Banglish
and generated views under the same parser.

Status label: `reviewed_v5_protected_v3_formulaish_deterministic_generated_bn_dev_audit`

## Artifacts

- Source items: `data/slices/validation_200_v5.jsonl`
- Output JSONL: `data/generated_views/validation200_v5_dev50_benqa_mcq_protected_v3_generated_bn_answer_audit.jsonl`
- `generated_bn_phonetic_protected_v3` source: `results/generated_views/phonetic_bangla_protected_v3_v5_dev50_benqa_mcq_generated_bn.jsonl`
- `generated_bn_bnb_protected_v3` source: `results/generated_views/bnbphoneticparser_protected_v3_v5_dev50_benqa_mcq_generated_bn.jsonl`

## Counts

- Rows: 36
- `benqa`: 36

| Subject | Rows |
| --- | ---: |
| `unknown` | 36 |

## Suggested Dev-Only Variants

- `banglish_clean`
- `generated_bn_phonetic_protected_v3`
- `generated_bn_bnb_protected_v3`

Do not run test150 from this slice. If a generated-BN variant helps on
dev, first inspect item-level outputs and decide whether a generated
English view is needed for the full agreement-routing protocol.
