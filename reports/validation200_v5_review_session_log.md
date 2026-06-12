# Validation-200 v5 Review Session Log

Updated: 2026-05-29

## Purpose

Use this file to record each human-review session for
`data/slices/validation_200_v5_review_queue.csv`.

The CSV queue remains the source of truth for row labels and corrected
Banglish. This log is the audit trail for who reviewed which batch, what checks
were run afterward, and which rows still need attention.

Do not paste credentials, API keys, PEM contents, or paid-provider responses
into this file.

## Read-Only Session Preview

Before editing a batch, preview the exact row set:

```bash
python3 scripts/review_validation200_v5_queue.py --session 1 --dry-run
```

For a reusable CSV preview:

```bash
python3 scripts/review_validation200_v5_queue.py \
  --session 1 \
  --export-matches results/analysis/validation200_v5_review_session_01_preview.csv
```

Current preview artifact:

- `results/analysis/validation200_v5_review_session_01_preview.csv`

Current generated session plan:

- `reports/validation200_v5_review_session_plan.md`
- `results/analysis/validation200_v5_review_session_plan.csv`

## Session Table

| Date | Reviewer | Batch command | Preview artifact | Rows opened | ok | minor_edit | major_edit | bad | Pending before | Pending after | Validation result | Notes |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 2026-05-29 | Codex AI-assisted review | full queue first-pass plus conservative manual overrides | `reports/validation200_v5_substitution_review_playbook.md` | 140 | 0 | 126 | 11 | 3 | 140 | 0 | `errors=0 warnings=0 pending=0`; full checks passed | Applied obvious repeated Banglish normalizations, user preference `shotokora->shotkora`, fixed partial first-row entry, and marked three source/option-corruption rows bad. |

Bad-row notes:

- `benqa_10th-Physics_0130`: source question mismatches listed statements.
- `benqa_12th-Chemistry-I_0286`: answer options appear date-corrupted.
- `benqa_12th-Physics-II_0131`: option formula appears malformed.

Freeze outcome:

- Default all-200 policy used; `bad` rows are kept and flagged, not dropped.
- Frozen slice: `data/slices/validation_200_v5.jsonl`
- Review audit: `results/analysis/validation200_v5_banglish_review_audit.csv`
- Artifact audit: `results/analysis/validation200_v5_banglish_artifact_summary.csv`
- Artifact examples: `results/analysis/validation200_v5_banglish_artifact_examples.csv`

## After-Session Checks

Run these after every partial session:

```bash
python3 scripts/summarize_v5_review_progress.py
python3 scripts/validate_banglish_review_queue.py
python3 scripts/check_post_v5_rerun_readiness.py
```

When all rows are labeled, run the stricter completion gate:

```bash
python3 scripts/validate_banglish_review_queue.py --require-complete
python3 scripts/check_post_v5_rerun_readiness.py
```

Record the pending count and validation result in the session table before
freezing v5 or scheduling any Kaggle reruns.
