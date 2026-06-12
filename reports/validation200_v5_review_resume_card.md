# Validation-200 v5 Review Resume Card

Updated: 2026-06-11

This card is generated from the authoritative review queue and session
plan. It is meant to be the quickest restart point after an interruption.

Machine-readable session status: `results/analysis/validation200_v5_review_resume_card.csv`.

## Overall

| Metric | Rows |
| --- | ---: |
| Total review rows | 140 |
| Reviewed rows | 140 |
| Pending rows | 0 |

## Label Counts

| Label | Rows |
| --- | ---: |
| `pending` | 0 |
| `ok` | 0 |
| `minor_edit` | 126 |
| `major_edit` | 11 |
| `bad` | 3 |

## Next Session

All planned sessions are reviewed. Move to the completion gate:

```bash
python3 scripts/validate_banglish_review_queue.py --require-complete
```

## After Each Session

```bash
python3 scripts/plan_v5_review_sessions.py
python3 scripts/export_v5_review_session_packets.py
python3 scripts/summarize_v5_review_progress.py
python3 scripts/export_v5_review_resume_card.py
python3 scripts/validate_banglish_review_queue.py
python3 scripts/check_post_v5_rerun_readiness.py
```

Record the session outcome in
`reports/validation200_v5_review_session_log.md` before freezing v5.

## Session Status

| Session | Substitution | Total | Reviewed | Pending |
| ---: | --- | ---: | ---: | ---: |
