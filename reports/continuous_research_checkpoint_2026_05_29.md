# Continuous Research Checkpoint: 2026-05-29

## Current State

The project is still gated on validation-200 v5 human review.

Current review queue:

- Source: `data/slices/validation_200_v5_review_queue.csv`
- Total rows: 140
- Pending rows: 140
- Structural validation: 0 errors, 0 warnings

Post-v5 rerun readiness:

- Report: `reports/post_v5_rerun_readiness.md`
- Status: `not_ready`
- Intended blockers: pending human-review rows and missing frozen v5 artifacts.

No Kaggle GPU job should be launched yet.

## Exact Next Action

Start the first generated review session:

```bash
python3 scripts/review_validation200_v5_queue.py --session 1 --dry-run
python3 scripts/review_validation200_v5_queue.py --session 1
```

Read-only context packet:

- `reports/validation200_v5_review_session_packets/session_01.md`

After the session:

```bash
python3 scripts/plan_v5_review_sessions.py
python3 scripts/summarize_v5_review_progress.py
python3 scripts/validate_banglish_review_queue.py
python3 scripts/check_post_v5_rerun_readiness.py
```

Then record counts and notes in:

- `reports/validation200_v5_review_session_log.md`

## What Changed In This Work Block

Review helper:

- `scripts/review_validation200_v5_queue.py`
- Added `--list-ids`, `--dry-run`, `--export-matches`, and exact
  `--session N` support.
- Added a bad-row guard requiring `review_notes` before saving a `bad` label.

Review planning:

- `scripts/plan_v5_review_sessions.py`
- `reports/validation200_v5_review_session_plan.md`
- `results/analysis/validation200_v5_review_session_plan.csv`
- Current plan: 12 sessions, 140 unique pending ids, 0 duplicate planned ids.

Review packets:

- `scripts/export_v5_review_session_packets.py`
- `reports/validation200_v5_review_session_packets/README.md`
- `reports/validation200_v5_review_session_packets/session_01.md` through
  `session_12.md`

Review resume card:

- `scripts/export_v5_review_resume_card.py`
- `reports/validation200_v5_review_resume_card.md`
- `results/analysis/validation200_v5_review_resume_card.csv`
- Current next session: 1 (`kot->koto`), 20 pending rows.

Review audit/logging:

- `reports/validation200_v5_review_session_log.md`
- `reports/validation200_v5_review_quickstart.md`
- `reports/validation200_v5_human_review_operator_checklist.md`
- `data/slices/banglish_review_guidelines.md`

Rerun gates:

- `scripts/check_post_v5_rerun_readiness.py`
- `reports/post_v5_rerun_readiness.md`
- `scripts/build_post_v5_kaggle_job_plan.py`
- `reports/post_v5_kaggle_job_plan.md`
- `results/analysis/post_v5_kaggle_job_plan.csv`
- `scripts/build_post_v5_compute_budget.py`
- `reports/post_v5_compute_budget.md`
- `results/analysis/post_v5_compute_budget.csv`
- Current conservative required post-v5 budget: 0.89 GPU-hours; required plus
  conditional 7B rerun: 1.51 GPU-hours under the 120 GPU-hour Kaggle-account
  assumption.

QA:

- `scripts/run_research_checks.py`
- `scripts/build_thesis_tables.py`
- `scripts/check_thesis_tables.py`
- `scripts/build_thesis_figures.py`
- `scripts/check_thesis_figures.py`
- `scripts/build_current_research_status_dashboard.py`
- `scripts/build_v5_next_session_brief.py`
- `scripts/check_v5_review_packet_integrity.py`
- `scripts/check_literature_corpus.py`
- `scripts/check_citation_readiness.py`
- `scripts/check_secret_hygiene.py`
- `scripts/check_local_artifact_refs.py`
- `scripts/build_artifact_manifest.py`
- Current full check result: passed.
- v5 review packet integrity check: 78 checks, 0 issues.
- Thesis table integrity check: 50 checks, 0 issues.
- Thesis figure integrity check: 25 checks, 0 issues.
- Literature corpus check: 33 complete citation-backed sources, 0 issues.
- Citation readiness check: 33 expected keys complete, 0 issues.
- Secret hygiene check: 596 non-secret files checked, 0 suspicious findings.
- Local reference check: 3,295 checked, 0 unexpected missing, 67 expected
  future/planned.
- Artifact manifest: 594 non-secret local thesis artifacts.
- Current status dashboard: `reports/current_research_status_dashboard.md`
- Next session brief: `reports/validation200_v5_next_session_brief.md`

Literature framing:

- `literature/notes/benchmark_gap_matrix.md`
- `literature/notes/citation_key_map.md`
- `literature/references_seed.bib`
- `reports/literature_corpus_check.md`
- Added 2026 landscape notes for newer Bangla/Bengali and adjacent romanized
  South Asian benchmark work.
- Added bibliography entries and citation keys for BanglaVerse, Bengali-Loop,
  BanglaGuard, BanglaMedQA, the Romanized Nepali LLM benchmark, BanglaT5,
  BanglaByT5, TituLLMs, and TigerLLM.

## Launch Rules

Do not run `scripts/prepare_kaggle_model_run.py` for v5 until all are true:

1. `python3 scripts/validate_banglish_review_queue.py --require-complete`
   passes.
2. `scripts/apply_banglish_review.py` creates
   `data/slices/validation_200_v5.jsonl`.
3. `scripts/audit_banglish_artifacts.py` creates the v5 audit files.
4. `python3 scripts/check_post_v5_rerun_readiness.py` reports `ready`.

When ready, use:

- `reports/post_v5_kaggle_job_plan.md`

Required first jobs:

- `qwen25_3b_validation200_v5_banglish`
- `qwen3_4b_validation200_v5_banglish`

Conditional only after decision:

- `qwen25_7b_8bit_validation200_v5_banglish`
