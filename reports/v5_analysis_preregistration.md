# Validation-200 v5 Analysis Preregistration

Updated: 2026-05-28

## Purpose

This note locks the analysis plan for validation-200 v5 before the human review
is complete. It is meant to prevent accidental overfitting after seeing v5
model outputs.

## Current State At Preregistration Time

- v5 review queue: `data/slices/validation_200_v5_review_queue.csv`
- Queue size: 140 rows.
- Current review status: 140 pending rows.
- Structural validator: 0 errors, 0 warnings.
- v5 frozen slice does not exist yet.
- No post-v5 model runs have been launched.

## Primary Question

After human-reviewed Banglish cleanup, do the main competent open models still
perform worse on Latin-script Banglish than on native Bangla and English for the
same validation-200 items?

## Primary Models

| Model | Role | Run after v5? |
| --- | --- | --- |
| Qwen2.5-3B-Instruct | Main Qwen2.5 evidence anchor | Yes, Banglish-only. |
| Qwen3-4B-Instruct-2507 | Strongest current P100-compatible open baseline | Yes, Banglish-only. |

Secondary model:

- Qwen2.5-7B-Instruct 8-bit only if v5 materially affects many held-out or
  main-table rows, or if the 7B row becomes necessary for the thesis main table.

## Primary Comparisons

For each primary model:

1. v5 Banglish vs existing native Bangla baseline.
2. v5 Banglish vs existing English baseline.
3. v5 Banglish vs v4 Banglish as a dataset-quality sensitivity check.

The existing Bangla and English baselines may be reused because v5 is designed
to modify only Banglish text and review metadata. If any non-Banglish item
field, item id, gold answer, or answer-format instruction changes, this
preregistration is invalid and Bangla/English rerun policy must be revisited.

## Primary Denominator Policy

Default policy:

- Keep all 200 rows.
- Rows labeled `bad` remain in the frozen JSONL with
  `quality_status=human_review_bad_banglish`.
- Report the count of `bad` rows.

Strict-subset policy:

- Use `scripts/apply_banglish_review.py --drop-bad` only if the thesis
  explicitly decides before reruns that `bad` rows should be excluded.
- If strict-subset policy is chosen, all main v5 tables must clearly state the
  reduced denominator and cannot be mixed with all-200 tables.

## Statistics

Primary unit:

- Paired item id.

Primary metric:

- Accuracy difference in percentage points.

Uncertainty:

- Paired bootstrap over item ids using 10,000 resamples.
- Report 2.5th and 97.5th percentile intervals.

Required outputs:

- Overall full-slice accuracy.
- BEnQA and BanglaMATH split accuracy.
- Dev50/test150 split accuracy for transparency.
- Paired bootstrap intervals for Banglish-minus-Bangla and
  Banglish-minus-English.
- Item-level v4-v5 flips and whether each flip is in dev50 or test150.

## Decision Rules

If v5 changes fewer than 10 model-relevant rows:

- Treat v5 as a quality/sensitivity audit.
- Keep v3/v4 as historical anchors and report v5 as supporting robustness
  evidence.

If v5 materially changes Qwen2.5-3B or Qwen3-4B Banglish accuracy:

- Promote v5 as the final Banglish benchmark slice.
- Recompute thesis tables, evidence matrix, dashboard, and abstract numbers.

If the v5 Banglish gap disappears for a primary model:

- Report that result directly.
- Do not replace it with a secondary model or alternate metric.
- Analyze item flips to determine whether the original gap was romanizer-driven
  for that model.

If the gap remains for both primary models:

- State the main claim as human-review-robust for the primary open baselines.
- Keep model-family caveats: do not claim every model shows Banglish below
  Bangla.

## What Is Not Allowed After Seeing v5 Outputs

- Do not change the primary models.
- Do not add new prompt variants to rescue a weak v5 result.
- Do not rerun Bangla/English unless v5 accidentally changes non-Banglish
  fields.
- Do not select a generated-view routing rule on test150.
- Do not run paid API full triad before open-model v5 tables are locked.

## Allowed Secondary Analyses

- Qwen2.5-7B 8-bit Banglish-only rerun if the decision condition above is met.
- Paid API 10-item smoke and full triad after v5/open-model tables are locked,
  following `reports/final_api_audit_cost_plan.md`.
- Qualitative flip examples for v4-v5 wins/losses.
- Subject/domain breakdowns as descriptive support, not separate primary
  hypotheses.

## Required Commands

Before reruns:

```bash
python3 scripts/validate_banglish_review_queue.py --require-complete
python3 scripts/apply_banglish_review.py \
  --input data/slices/validation_200_v4.jsonl \
  --review data/slices/validation_200_v5_review_queue.csv \
  --output data/slices/validation_200_v5.jsonl \
  --audit-output results/analysis/validation200_v5_banglish_review_audit.csv \
  --quality-status human_reviewed_banglish_v5
python3 scripts/audit_banglish_artifacts.py \
  data/slices/validation_200_v5.jsonl \
  --summary-output results/analysis/validation200_v5_banglish_artifact_summary.csv \
  --examples-output results/analysis/validation200_v5_banglish_artifact_examples.csv
```

After reruns:

```bash
python3 scripts/analyze_banglish_variant_sensitivity.py \
  --baseline-results path/to/v4_banglish.jsonl \
  --candidate-results path/to/v5_banglish.jsonl \
  --model Qwen/Qwen2.5-3B-Instruct \
  --model-label Qwen2.5-3B \
  --baseline-name v4 \
  --candidate-name v5 \
  --output-prefix results/analysis/qwen25_validation200_v5_vs_v4_banglish

python3 scripts/build_thesis_tables.py
python3 scripts/build_artifact_manifest.py
```

## Reports To Update After v5

- `reports/thesis_results_dashboard.md`
- `reports/evidence_matrix.md`
- `reports/current_research_state.md`
- `reports/thesis_abstract_and_contributions_draft.md`
- `reports/thesis_writeup_blueprint.md`
- `reports/threats_to_validity.md`
- `reports/dataset_card_validation200.md`
- `research_log.md`
- `results/experiment_log.md`
