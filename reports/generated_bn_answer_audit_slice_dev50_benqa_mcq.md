# Generated-BN Answer Audit Slice: Dev50 BEnQA MCQ

Updated: 2026-05-28

## Purpose

This historical slice records the protected-v1 deterministic generated-Bengali
views used by the completed dev-only answer audits. The files predate the
tightened scientific-token gate and are not route-ready expanded-v2 candidates.
It does not launch any GPU run.

## Artifacts

- Source items: `data/slices/validation_200_v4_dev50.jsonl`
- Output JSONL: `data/generated_views/validation200_v4_dev50_benqa_mcq_protected_generated_bn_answer_audit.jsonl`
- `generated_bn_phonetic_protected` source: `results/generated_views/phonetic_bangla_protected_dev50_benqa_mcq_generated_bn.jsonl`
- `generated_bn_bnb_protected` source: `results/generated_views/bnbphoneticparser_protected_dev50_benqa_mcq_generated_bn.jsonl`

## Counts

- Rows: 36
- `benqa`: 36

| Subject | Rows |
| --- | ---: |
| `unknown` | 36 |

## Suggested Dev-Only Variants

- `banglish_clean`
- `generated_bn_phonetic_protected`
- `generated_bn_bnb_protected`

Dry-run prompt validation passed for the first item with:

```bash
python3 scripts/run_eval_kaggle.py \
  --input data/generated_views/validation200_v4_dev50_benqa_mcq_protected_generated_bn_answer_audit.jsonl \
  --output /tmp/generated_bn_answer_audit_dry_run.jsonl \
  --model dry-run-model \
  --dry-run \
  --limit 1 \
  --variants banglish_clean generated_bn_phonetic_protected generated_bn_bnb_protected \
  --max-new-tokens 64
```

Do not run test150 from this slice. If a generated-BN variant helps on
dev, first inspect item-level outputs and decide whether a generated
English view is needed for the full agreement-routing protocol.
