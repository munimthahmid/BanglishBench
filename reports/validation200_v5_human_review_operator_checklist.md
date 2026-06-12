# Validation-200 v5 Human Review Operator Checklist

Updated: 2026-05-29

## Review File

Use:

- `data/slices/validation_200_v5_review_queue.csv`

This is the main worksheet. It includes:

- Bangla source text,
- English source text,
- current v4 Banglish,
- auto-suggested Banglish,
- model correctness flags,
- blank human-review fields.

For easiest high-impact review, start with the calibration set, then move to the
impact-ordered read-only packet index:

- `reports/validation200_v5_review_calibration_set.md`
- `reports/validation200_v5_review_packets_impact_order/README.md`

For CSV-order reading, use the original packet index:

- `reports/validation200_v5_review_packets/README.md`

For effort and repeated-substitution planning, use:

- `reports/validation200_v5_review_effort_summary.md`
- `reports/validation200_v5_review_impact_ranking.md`
- `reports/validation200_v5_review_impact_substitutions.md`
- `reports/validation200_v5_substitution_review_playbook.md`
- `reports/validation200_v5_review_session_plan.md`
- `reports/validation200_v5_review_session_packets/README.md`
- `reports/validation200_v5_review_session_log.md`

Optional terminal helper:

```bash
python3 scripts/review_validation200_v5_queue.py --session 1 --dry-run
python3 scripts/review_validation200_v5_queue.py --session 1
```

For repeated-substitution batches:

```bash
python3 scripts/review_validation200_v5_queue.py --substitution konoti:konti --dry-run
python3 scripts/review_validation200_v5_queue.py --substitution konoti:konti
```

Track progress after each review session:

```bash
python3 scripts/plan_v5_review_sessions.py
python3 scripts/summarize_v5_review_progress.py
```

Current progress report:

- `reports/validation200_v5_review_progress.md`
- `results/analysis/validation200_v5_review_progress_summary.csv`
- `results/analysis/validation200_v5_review_session_plan.csv`

The current pending-row coverage estimate shows that reviewing substitution
groups in this order reaches all 140 pending rows by the first ten groups:
`kot->koto`, `konoti->konti`, `ekoti->ekti`, `kshetrofol->khetrofol`,
`doirghy->doirgho`, `prosth->prostho`, `ayotakar->ayotokar`,
`korote->korte`, `achhe->ache`, and `thakole->thakle`.

Fill the CSV worksheet, not the packet Markdown files.

## Fields To Fill

Fill only these columns:

- `reviewed_banglish`
- `quality_label`
- `review_notes`

Allowed `quality_label` values:

- `ok`: current Banglish is acceptable.
- `minor_edit`: small replacement needed; fill `reviewed_banglish`.
- `major_edit`: substantial replacement needed; fill `reviewed_banglish`.
- `bad`: item should not be trusted for the human-reviewed clean-Banglish
  subset; leave `reviewed_banglish` blank and add a short `review_notes`
  reason.

Leave `reviewed_banglish` blank when `quality_label` is `ok`.

## Review Rule

For each row, compare:

- `bangla`,
- `english`,
- `current_banglish_clean`,
- `auto_suggested_banglish_clean`.

Accept the current Banglish only if it preserves the same task, numbers,
options, formulas, units, and answer format. The auto-suggested field is only a
candidate; do not copy it blindly.

## Priority Order

Recommended order:

1. Review `reports/validation200_v5_review_calibration_set.md` to establish
   consistent treatment of repeated patterns.
2. Open `reports/validation200_v5_review_session_plan.md`.
3. Run session 1 with `python3 scripts/review_validation200_v5_queue.py --session 1`.
4. Use `reports/validation200_v5_review_packets_impact_order/README.md` for
   additional context when a row is hard.
5. Use `reports/validation200_v5_review_impact_substitutions.md` to batch-check
   repeated substitutions.
6. Use `reports/validation200_v5_substitution_review_playbook.md` for example
   context and terminal-helper shortcuts.

The original priority buckets are:

1. `both_wrong_multi_edit`
2. `both_wrong_single_edit`
3. `qwen25_wrong_multi_edit`
4. `qwen3_wrong_multi_edit`
5. `lower_priority`

The impact ranking refines these buckets with held-out split, cross-script
recoverability, agreement-route signal, and replacement burden.

## Quick Consistency Checks

Before marking a row `ok` or accepting a replacement:

- MCQ option labels A-D must remain present and ordered.
- Digits must match the source task.
- Formulas and units must not be changed.
- The reviewed Banglish must not include the answer unless the original prompt
  already includes it as part of the item.
- Keep the answer-format line unchanged.

## Validate Before Freezing

During review, check progress with:

```bash
python3 scripts/validate_banglish_review_queue.py
```

Before freezing v5, require a complete queue and zero blocking issues:

```bash
python3 scripts/validate_banglish_review_queue.py --require-complete
```

Validation artifacts:

- `reports/validation200_v5_review_validation.md`
- `results/analysis/validation200_v5_review_validation_issues.csv`

## Freeze Command After Review

After review is filled, create v5 with:

```bash
python3 scripts/apply_banglish_review.py \
  --input data/slices/validation_200_v4.jsonl \
  --review data/slices/validation_200_v5_review_queue.csv \
  --output data/slices/validation_200_v5.jsonl \
  --audit-output results/analysis/validation200_v5_banglish_review_audit.csv \
  --quality-status human_reviewed_banglish_v5
```

Then audit artifacts:

```bash
python3 scripts/audit_banglish_artifacts.py \
  data/slices/validation_200_v5.jsonl \
  --summary-output results/analysis/validation200_v5_banglish_artifact_summary.csv \
  --examples-output results/analysis/validation200_v5_banglish_artifact_examples.csv
```

Rows labeled `bad` are kept and flagged by default. If the final thesis policy
is a strict reviewed subset, add `--drop-bad` to the freeze command and report
the reduced denominator explicitly.

## Rerun Policy

If v5 changes only a small number of rows, first rerun clean Banglish only for:

- Qwen2.5-3B,
- Qwen3-4B,
- Qwen2.5-7B 8-bit only if changes affect many Qwen disagreement items.

Do not rerun Bangla or English baselines unless non-Banglish fields changed.
