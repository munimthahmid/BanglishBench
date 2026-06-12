# Guarded Generated-EN Answer Audit Slice: Dev50 BEnQA MCQ

Updated: 2026-06-11

## Purpose

This slice joins a locked dev item subset with generated alternate views
so the standard evaluator can answer Banglish and generated views under
the same parser.

Status label: `reviewed_v5_qwen3_guarded_generated_en_dev_audit`

## Artifacts

- Source items: `data/slices/validation_200_v5.jsonl`
- Output JSONL: `data/generated_views/validation200_v5_dev50_benqa_mcq_guarded_generated_en_answer_audit.jsonl`
- `generated_en_qwen3_guarded` source: `results/generated_views/qwen3_4b_selftranslate_guarded_v5_dev50_benqa_mcq_generated_en.jsonl`

## Counts

- Rows: 36
- `benqa`: 36

| Subject | Rows |
| --- | ---: |
| `unknown` | 36 |

## Suggested Dev-Only Variants

- `banglish_clean`
- `generated_en_qwen3_guarded`

Do not run test150 from this slice. If a generated-view variant
helps on dev, first inspect item-level outputs and preservation-gate
status, then decide whether a full agreement-routing protocol is
ready.
