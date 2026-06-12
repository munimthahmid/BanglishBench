# Post-v5 Rerun Protocol

Updated: 2026-05-28

## Purpose

This protocol locks what to run after the validation-200 v5 human review is
complete. The goal is to measure the effect of human-reviewed Banglish without
rerunning stable Bangla/English baselines unnecessarily.

## Preconditions

Do not launch any post-v5 GPU run until all checks pass:

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

Required freeze artifacts:

- `data/slices/validation_200_v5.jsonl`
- `results/analysis/validation200_v5_banglish_review_audit.csv`
- `results/analysis/validation200_v5_banglish_artifact_summary.csv`
- `results/analysis/validation200_v5_banglish_artifact_examples.csv`

## Minimal GPU Reruns

| Priority | Model | Variant | Slice | Reason |
| ---: | --- | --- | --- | --- |
| 1 | Qwen2.5-3B-Instruct | `banglish_clean` only | validation-200 v5 full200 | Main Qwen2.5 evidence anchor; cheap enough to rerun. |
| 2 | Qwen3-4B-Instruct-2507 | `banglish_clean` only | validation-200 v5 full200 | Main Qwen3 evidence anchor; strongest current script gap. |
| 3 | Qwen2.5-7B-Instruct 8-bit | `banglish_clean` only | validation-200 v5 full200 or test150 | Only if v5 changes many held-out/test rows or if 7B remains a thesis main table row. |

Do not rerun Bangla or English unless source fields, gold answers, item ids, or
answer-format lines changed. The v5 process is supposed to change only
`banglish_clean`, `quality_status`, and review metadata.

## Kaggle Packaging Commands

After `data/slices/validation_200_v5.jsonl` exists, prepare the first two runs
with the generic Kaggle packager:

```bash
python3 scripts/prepare_kaggle_model_run.py \
  --account 1 \
  --model Qwen/Qwen2.5-3B-Instruct \
  --dataset-slug validation-200-v5-assets \
  --dataset-title "Validation 200 v5 assets" \
  --items-path data/slices/validation_200_v5.jsonl \
  --assets-job-name validation_200_v5_assets_account1 \
  --job-name qwen25_3b_validation200_v5_banglish \
  --kernel-slug qwen25-3b-validation200-v5-banglish \
  --title "Qwen2.5 3B validation-200 v5 Banglish" \
  --output-name qwen2_5_3b_validation200_v5_banglish \
  --limit 0 \
  --variants banglish_clean \
  --max-new-tokens 128

python3 scripts/prepare_kaggle_model_run.py \
  --account 1 \
  --model Qwen/Qwen3-4B-Instruct-2507 \
  --dataset-slug validation-200-v5-assets \
  --dataset-title "Validation 200 v5 assets" \
  --items-path data/slices/validation_200_v5.jsonl \
  --assets-job-name validation_200_v5_assets_account1 \
  --job-name qwen3_4b_validation200_v5_banglish \
  --kernel-slug qwen3-4b-validation200-v5-banglish \
  --title "Qwen3 4B validation-200 v5 Banglish" \
  --output-name qwen3_4b_validation200_v5_banglish \
  --limit 0 \
  --variants banglish_clean \
  --max-new-tokens 128 \
  --disable-thinking
```

Use the printed `datasets create` or `datasets version` command first, then the
printed `kernels push` command. Reuse the same v5 assets dataset for both
kernels.

The generated, readiness-gated job plan is:

- `reports/post_v5_kaggle_job_plan.md`
- `results/analysis/post_v5_kaggle_job_plan.csv`

## Analysis After Reruns

For each rerun:

1. Reparse/rescore outputs with the same answer parser used for v3/v4.
2. Summarize full200, dev50, and test150 accuracy for `banglish_clean`.
3. Compare v5 Banglish to v4 Banglish item-by-item.
4. Recompute Banglish-minus-Bangla and Banglish-minus-English paired bootstrap
   intervals using existing Bangla/English baselines.
5. Update thesis tables only after all main reruns are complete.

Expected analysis artifacts:

- `results/analysis/*validation200_v5_banglish_summary*.csv`
- `results/analysis/*validation200_v5_vs_v4_banglish_items*.csv`
- `results/analysis/*validation200_v5_banglish_minus_bangla_bootstrap.csv`
- `results/analysis/*validation200_v5_banglish_minus_english_bootstrap.csv`
- `reports/v5_banglish_sensitivity_validation200.md`
- `results/tables/thesis_tables.md`

Reusable analyzer:

```bash
python3 scripts/analyze_banglish_variant_sensitivity.py \
  --baseline-results path/to/v4_banglish.jsonl \
  --candidate-results path/to/v5_banglish.jsonl \
  --model Qwen/Qwen2.5-3B-Instruct \
  --model-label Qwen2.5-3B \
  --baseline-name v4 \
  --candidate-name v5 \
  --output-prefix results/analysis/qwen25_validation200_v5_vs_v4_banglish
```

## Decision Rules

If v5 changes fewer than 10 model-relevant rows:

- Report v5 as a quality/sensitivity audit.
- Keep v3/v4 main script-gap results as the historical anchor, with v5 as a
  robustness check.

If v5 materially changes the main Qwen2.5 or Qwen3 Banglish accuracy:

- Promote v5 as the final Banglish benchmark slice.
- Keep v4 only as an audit trail.
- Recompute the main evidence matrix and thesis tables from v5.

If v5 marks rows as `bad`:

- Report the number of excluded/untrusted rows.
- Decide whether final tables use all 200 rows with `bad` flagged, or a
  strict human-reviewed subset. Do not mix those policies silently.
- The default freeze command keeps `bad` rows flagged. Use
  `scripts/apply_banglish_review.py --drop-bad` only if the thesis explicitly
  switches to a strict subset policy.

## Compute Policy

- No generated-view test150 jobs before v5 reruns.
- No paid API calls before v5 reruns and thesis tables are locked.
- No new model-family pilots unless the v5 result undermines the current main
  conclusion and a targeted contrast is needed.
