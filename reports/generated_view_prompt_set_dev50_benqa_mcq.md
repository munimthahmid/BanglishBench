# Generated-View Prompt Set: Dev50 BEnQA MCQ

Updated: 2026-05-28

## Purpose

This prompt set prepares the first deployable consistency-routing
experiment without launching a generator yet. It creates locked prompts
for generated Bengali and generated English alternate views from
Banglish-only inputs.

## Artifacts

- Input slice: `data/slices/validation_200_v4_dev50.jsonl`
- Output JSONL: `data/generated_views/validation200_v4_dev50_benqa_mcq_generation_prompts.jsonl`

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

Expected generator-output JSONL schema:

- `id`
- `target_view`
- one text field such as `generated_text`, `output_text`, `output`, or
  `raw_output`

Audit generated outputs with:

```bash
python3 scripts/audit_generated_view_outputs.py \
  --outputs path/to/generated_view_outputs.jsonl \
  --items-output results/analysis/generated_view_output_audit_items.csv \
  --summary-output results/analysis/generated_view_output_audit_summary.csv \
  --report-output reports/generated_view_output_audit.md
```

Do not tune on test150 until generator prompts and routing are fixed
on dev50.

## Deterministic Smoke Result

`phonetic-bangla==1.0.0` was tested only for the `generated_bn` rows:

- Output JSONL:
  `results/generated_views/phonetic_bangla_dev50_benqa_mcq_generated_bn.jsonl`
- Audit report:
  `reports/phonetic_bangla_generated_bn_dev50_benqa_mcq_audit.md`
- Result: 36/36 hard preservation failures. All rows corrupt option labels; the
  tightened scientific-token gate also catches formula/token corruption on
  17/36 rows.

Decision: do not use `phonetic-bangla` for answer routing.

`bnbphoneticparser==0.1.5` was tested on the same `generated_bn` rows:

- Output JSONL:
  `results/generated_views/bnbphoneticparser_dev50_benqa_mcq_generated_bn.jsonl`
- Audit report:
  `reports/bnbphoneticparser_generated_bn_dev50_benqa_mcq_audit.md`
- Result: 36/36 hard preservation failures. All rows corrupt option labels; the
  tightened scientific-token gate also catches formula/token corruption on
  17/36 rows.

Decision: do not use `bnbphoneticparser` for answer routing.

## Protected Deterministic Smoke Result

A structural-mask wrapper was then tested. It protects option prefixes, the
answer-format line, numbers, standalone scientific tokens, annotated units,
math tokens, and LaTeX commands including subscript/superscript payloads before
deterministic transliteration, then restores them before auditing.

Historical protected-v1 `phonetic-bangla==1.0.0`:

- Output JSONL:
  `results/generated_views/phonetic_bangla_protected_dev50_benqa_mcq_generated_bn.jsonl`
- Audit report:
  `reports/phonetic_bangla_protected_generated_bn_dev50_benqa_mcq_audit.md`
- Result under the tightened gate: 9/36 scientific-token failures.

Historical protected-v1 `bnbphoneticparser==0.1.5`:

- Output JSONL:
  `results/generated_views/bnbphoneticparser_protected_dev50_benqa_mcq_generated_bn.jsonl`
- Audit report:
  `reports/bnbphoneticparser_protected_generated_bn_dev50_benqa_mcq_audit.md`
- Result under the tightened gate: 10/36 scientific-token failures.

Expanded protected-v2 files:

- `results/generated_views/phonetic_bangla_protected_v2_dev50_benqa_mcq_generated_bn.jsonl`
- `results/generated_views/bnbphoneticparser_protected_v2_dev50_benqa_mcq_generated_bn.jsonl`
- Result after the tightened formula-expression gate: both fail 16/36 hard
  gates. These are no longer route-ready candidates.

Reviewed-v5 formulaish protected-v3 files:

- `results/generated_views/phonetic_bangla_protected_v3_v5_dev50_benqa_mcq_generated_bn.jsonl`
- `results/generated_views/bnbphoneticparser_protected_v3_v5_dev50_benqa_mcq_generated_bn.jsonl`
- Result: both pass with 0/36 hard failures and 0/36 lexical warnings.

Decision: protected-v3 deterministic generated-Bengali views are the first
deterministic candidates to pass the tightened formula-expression gate, but
their completed dev answer audits still show only weak gains. Existing
protected-v1 and protected-v2 Qwen answer audits are diagnostics and are not
validated mitigation claims.
