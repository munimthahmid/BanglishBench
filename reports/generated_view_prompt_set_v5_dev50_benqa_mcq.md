# Generated-View Prompt Set: Dev50 BEnQA MCQ

Updated: 2026-06-11

## Purpose

This prompt set prepares the first deployable consistency-routing
experiment without launching a generator yet. It creates locked prompts
for generated Bengali and generated English alternate views from
Banglish-only inputs.

## Artifacts

- Input slice: `data/slices/validation_200_v5.jsonl`
- ID filter source: `data/slices/validation_200_v4_dev50.jsonl`
- Output JSONL: `data/generated_views/validation200_v5_dev50_benqa_mcq_generation_prompts.jsonl`

## Filter

- Dataset: `benqa`
- Answer type: `choice`
- Unique items: 36
- Generation prompts: 72
- `generated_bn`: 36
- `generated_en`: 36

## Use

Run a generator over `generation_prompt`, write its output beside the
same `id` and `target_view`, then apply the preservation gates from
`reports/generated_view_preservation_audit_v2.md` before answering
generated views.

Do not tune on test150 until generator prompts and routing are fixed
on dev50.
