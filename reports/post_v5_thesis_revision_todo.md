# Post-v5 Thesis Revision Todo

Updated: 2026-05-31

## Purpose

This is the exact revision path after human review freezes validation-200 v5.
It keeps the thesis draft, result tables, figures, and release artifacts in sync.

## Execution Status

| Gate | Status | Evidence |
| --- | --- | --- |
| Gate 0: human review | complete | 140/140 reviewed; v5 frozen with 126 minor edits, 11 major edits, and 3 flagged bad rows. |
| Gate 1: required reruns | complete | Qwen2.5-3B and Qwen3-4B v5 Banglish reruns analyzed. |
| Gate 1: optional 7B rerun | complete | Pinned retry: v4 48/200 -> v5 47/200, -0.5 points, CI [-3.5, +2.5]. |
| Gate 2: analysis refresh | complete | Sensitivity tables, strict-197 flagged-bad policy analysis, figures, manifest, and local-reference checks regenerated. |
| Gate 3: chapter updates | complete | Core stale v5 language and optional 7B result refreshed; final prose scan passed on 2026-05-30. |
| Gate 4: paid API decision | no-spend ready; paid calls not authorized | Re-check current provider pricing and run only the 10-item smoke if approved. Provider-neutral requests, importer, manifest integrity, and importer round-trip checks are prepared under `reports/paid_api_audit_execution_runbook.md`, `reports/api_audit_manifest_integrity_check.md`, and `reports/api_audit_import_roundtrip_check.md`. |
| Gate 5: release checks | pass | `python3 scripts/run_research_checks.py` passed on 2026-05-31. |

## Gate 0: Human Review Must Finish

Do not run post-v5 model jobs until:

1. `data/slices/validation_200_v5_review_queue.csv` has no pending rows.
2. `python3 scripts/validate_banglish_review_queue.py --require-complete`
   passes.
3. `reports/v5_analysis_preregistration.md` is unchanged after review starts,
   except for clearly logged structural corrections.
4. `scripts/apply_banglish_review.py` has produced the frozen v5 slice.

## Gate 1: Minimal Post-v5 Reruns

Primary reruns:

1. Qwen2.5-3B clean Banglish on full validation-200 v5.
2. Qwen3-4B clean Banglish on full validation-200 v5.

Conditional rerun:

3. Qwen2.5-7B 8-bit clean Banglish only if enough reviewed rows affect the
   main table, test split, or cross-script-recovery examples.

Avoid reruns:

- Do not rerun Bangla or English unless their fields changed.
- Do not run paid API audits until open-model tables are locked.

## Gate 2: Analysis Refresh

After downloading post-v5 results:

1. Run `scripts/analyze_banglish_variant_sensitivity.py` for v4-vs-v5 paired
   accuracy and item flips.
2. Recompute paired bootstrap intervals for the clean-Banglish delta.
3. Rebuild thesis tables with `python3 scripts/build_thesis_tables.py`.
4. Rebuild figures with `python3 scripts/build_thesis_figures.py`.
5. Re-export qualitative examples if any selected thesis example changed.
6. Rebuild the artifact manifest with
   `python3 scripts/build_artifact_manifest.py`.
7. Run `python3 scripts/check_local_artifact_refs.py`.

## Gate 3: Chapter Updates

| Chapter | Required Update |
| --- | --- |
| Chapter 1 | Replace provisional v4/v3 language with final v5 status and final contribution wording. |
| Chapter 2 | Add final citation formatting; no new literature claims unless sourced. |
| Chapter 3 | Replace review-plan language with completed v5 review counts, bad-row policy, and freeze hash/manifest references. |
| Chapter 4 | Update main script-gap table, confidence intervals, and any v5 sensitivity paragraph. |
| Chapter 5 | Update model-breadth discussion only if Qwen2.5-7B is rerun or v5 materially changes scaling interpretation. |
| Chapter 6 | Refresh qualitative examples and agreement-route numbers if affected by v5 wording. |
| Chapter 7 | Keep mechanism claims cautious; update tokenization/failure joins only if v5 text changes enough to matter. |
| Chapter 8 | Update mitigation tables and make generated-view status explicit: diagnostic unless held-out v5 tests exist. |
| Chapter 9 | Replace "pending review" limitations with final dataset-quality and compute limitations. |
| Chapter 10 | Update final numbers and remove stale future-tense phrasing. |

## Gate 4: Final API Audit Decision

Run the paid API audit only after Gates 0-3 pass.

Minimum path:

1. Build `data/slices/api_audit_smoke_10_v5.jsonl` against frozen v5.
2. Re-run `scripts/estimate_prompt_budget.py`.
3. Run `scripts/check_api_audit_manifest.py` and require 0 issues.
4. Run `scripts/check_api_audit_import_roundtrip.py` and require 0 issues.
5. Run 10-item smoke across chosen paid models.
6. Inspect parser failures and cost.
7. Run full validation-200 only if the smoke is clean and the budget remains
   acceptable.

## Gate 5: Release Checks

Before thesis submission or public release:

1. `python3 -m py_compile scripts/*.py`
2. `python3 scripts/check_local_artifact_refs.py`
3. `python3 scripts/build_artifact_manifest.py`
4. Secret scan for Kaggle keys, PEM contents, and API tokens.
5. Recompile thesis draft with `python3 scripts/compile_thesis_draft.py`.
6. Confirm `reports/reproducibility_release_checklist.md` has no open
   thesis-blocking item.
