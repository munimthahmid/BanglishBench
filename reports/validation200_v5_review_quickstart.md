# Validation-200 v5 Review Quickstart

Updated: 2026-05-29

## Goal

Fill the human-review fields in:

- `data/slices/validation_200_v5_review_queue.csv`

Do not edit the Markdown packets as the source of truth.

## First 5 Minutes

Read these two files first:

1. `data/slices/banglish_review_guidelines.md`
2. `reports/validation200_v5_review_calibration_set.md`

Then check current progress:

```bash
python3 scripts/summarize_v5_review_progress.py
python3 scripts/export_v5_review_resume_card.py
```

Fastest restart artifact:

- `reports/validation200_v5_review_resume_card.md`

## Preview A Batch

Use read-only modes before editing the queue:

```bash
python3 scripts/review_validation200_v5_queue.py --session 1 --dry-run
python3 scripts/review_validation200_v5_queue.py --session 1 --list-ids
```

To export a reusable session preview:

```bash
python3 scripts/review_validation200_v5_queue.py \
  --session 1 \
  --export-matches results/analysis/validation200_v5_review_session_01_preview.csv
```

Record each session in:

- `reports/validation200_v5_review_session_log.md`

For a generated session-by-session plan:

```bash
python3 scripts/plan_v5_review_sessions.py
```

Plan artifacts:

- `reports/validation200_v5_review_session_plan.md`
- `results/analysis/validation200_v5_review_session_plan.csv`
- `reports/validation200_v5_review_session_packets/README.md`
- `reports/validation200_v5_review_resume_card.md`
- `results/analysis/validation200_v5_review_resume_card.csv`

## Recommended Review Order

Use the substitution batches below. They cover all 140 pending rows because the
same rows often contain several repeated spelling edits.

```bash
python3 scripts/review_validation200_v5_queue.py --substitution kot:koto
python3 scripts/review_validation200_v5_queue.py --substitution konoti:konti
python3 scripts/review_validation200_v5_queue.py --substitution ekoti:ekti
python3 scripts/review_validation200_v5_queue.py --substitution kshetrofol:khetrofol
python3 scripts/review_validation200_v5_queue.py --substitution doirghy:doirgho
python3 scripts/review_validation200_v5_queue.py --substitution prosth:prostho
python3 scripts/review_validation200_v5_queue.py --substitution ayotakar:ayotokar
python3 scripts/review_validation200_v5_queue.py --substitution korote:korte
python3 scripts/review_validation200_v5_queue.py --substitution achhe:ache
python3 scripts/review_validation200_v5_queue.py --substitution thakole:thakle
```

The helper skips already reviewed rows unless `--all` is passed, so overlap
between batches is safe.

## Labels

Use exactly one of:

- `ok`: current Banglish is acceptable; leave `reviewed_banglish` blank.
- `minor_edit`: small replacement needed; fill the full corrected prompt in
  `reviewed_banglish`.
- `major_edit`: larger rewrite needed; fill the full corrected prompt in
  `reviewed_banglish`.
- `bad`: source or Banglish is too ambiguous to trust; leave
  `reviewed_banglish` blank and add a short reason in `review_notes`.

## During Review

Compare all four fields:

- `bangla`
- `english`
- `current_banglish_clean`
- `auto_suggested_banglish_clean`

The auto-suggested text is only a candidate. Accept it only if it preserves the
same task, options, numbers, formulas, units, and answer instruction.

## After Each Session

Run:

```bash
python3 scripts/plan_v5_review_sessions.py
python3 scripts/export_v5_review_session_packets.py
python3 scripts/summarize_v5_review_progress.py
python3 scripts/export_v5_review_resume_card.py
python3 scripts/validate_banglish_review_queue.py
python3 scripts/check_post_v5_rerun_readiness.py
```

Only when all rows are filled, run:

```bash
python3 scripts/validate_banglish_review_queue.py --require-complete
```

## Freeze Gate

Do not freeze v5 or launch Kaggle reruns until:

- `python3 scripts/validate_banglish_review_queue.py --require-complete` passes.
- `python3 scripts/check_post_v5_rerun_readiness.py` reports `ready`.
