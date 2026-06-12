# Validation-200 v5 Review Session Plan

Updated: 2026-06-11

Pending rows at planning time: `0`.
Session size target: `20` rows.
Planned row slots: `0`.
Unique row ids in plan: `0`.
Duplicate planned row ids: `0`.

This plan is generated from the current pending queue and impact ranking.
Each command uses the terminal helper's default behavior of skipping
already reviewed rows, so repeated substitution sessions can be rerun
after prior sessions are saved.

## Session Commands

| Session | Substitution | Planned new rows | Tier-1 rows | Test rows | Preview command | Review command |
| ---: | --- | ---: | ---: | ---: | --- | --- |

## Exact Row Ids

## After Each Session

1. Update `reports/validation200_v5_review_session_log.md`.
2. Run `python3 scripts/summarize_v5_review_progress.py`.
3. Run `python3 scripts/validate_banglish_review_queue.py`.
4. Run `python3 scripts/check_post_v5_rerun_readiness.py`.
