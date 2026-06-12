# BEnQA Extension Publication Strategy

Updated: 2026-06-05

## Position

The thesis should not replace the frozen `validation_200_v5` gold core. The
stronger publication framing is:

- `validation_200_v5`: 200-item deeply audited gold core for the main paired
  Bangla/Banglish/English claim.
- `benqa_extended_1000_v1_ai_reviewed`: 1,000-item BEnQA-only silver extension
  for scale and robustness checks.
- `benqa_extended_1000_v1_ai_pass`: 851-item conservative pass-only subset for
  cleaner large-scale evaluation.

This directly addresses the "only 200 items" weakness without weakening the
gold-core controls.

## Built Artifacts

- Extended raw slice: `data/slices/benqa_extended_1000_v1.jsonl`
- Extended manifest: `data/slices/benqa_extended_1000_v1.manifest.json`
- AI-assisted reviewed slice: `data/slices/benqa_extended_1000_v1_ai_reviewed.jsonl`
- Conservative pass-only slice: `data/slices/benqa_extended_1000_v1_ai_pass.jsonl`
- Review queue: `results/analysis/benqa_extended_1000_v1_ai_review_queue.csv`
- Construction report: `reports/benqa_extended_1000_v1.md`
- AI-assisted review report: `reports/benqa_extended_1000_v1_ai_review.md`
- Evaluation subset report: `reports/benqa_extension_eval_subsets.md`
- Kaggle smoke launch report: `reports/benqa_extension_kaggle_smoke_launch.md`
- Qwen2.5-3B smoke result report: `reports/qwen25_3b_benqa_ext_smoke26.md`
- Qwen2.5-3B smoke paired-gap analysis:
  `reports/qwen25_3b_benqa_ext_smoke26_paired_gap_analysis.md`
- Kaggle pilot launch report: `reports/benqa_extension_kaggle_pilot130_launch.md`
- Qwen2.5-3B pilot result report: `reports/qwen25_3b_benqa_ext_pilot130.md`
- Qwen2.5-3B pilot paired-gap analysis:
  `reports/qwen25_3b_benqa_ext_pilot130_paired_gap_analysis.md`
- Qwen2.5-3B pilot recoverable examples:
  `reports/qwen25_3b_benqa_ext_pilot130_recoverable_examples.md`
- Qwen2.5-3B full extension launch report:
  `reports/benqa_extension_kaggle_full851_launch.md`
- Qwen2.5-3B full extension result report:
  `reports/qwen25_3b_benqa_ext_full851.md`
- Qwen2.5-3B full extension paired-gap analysis:
  `reports/qwen25_3b_benqa_ext_full851_paired_gap_analysis.md`
- Qwen2.5-3B full extension recoverable examples:
  `reports/qwen25_3b_benqa_ext_full851_recoverable_examples.md`
- DeepSeek V4 Flash full extension result report:
  `reports/deepseek_v4_flash_benqa_ext_full851.md`
- DeepSeek V4 Flash full extension paired-gap analysis:
  `reports/deepseek_v4_flash_benqa_ext_full851_paired_gap_analysis.md`
- DeepSeek V4 Flash full extension recoverable examples:
  `reports/deepseek_v4_flash_benqa_ext_full851_recoverable_examples.md`
- Gold-core/extension alignment report:
  `reports/benqa_gold_core_extension_alignment.md`
- Builder: `scripts/build_benqa_extended_slice.py`
- Reviewer/triage script: `scripts/review_benqa_extended_slice.py`
- Subset builder: `scripts/build_benqa_extension_eval_subsets.py`
- Extension result paired-gap analyzer:
  `scripts/analyze_benqa_extension_scale_result.py`

## Construction Summary

- Upstream BEnQA rows seen: 5,087.
- Frozen-core BEnQA rows excluded: 144.
- Candidate pool after required-field filtering: 4,939.
- Selected extension rows: 1,000.
- Sampling: deterministic round-robin over BEnQA subject files.
- Per-subject coverage: 12 subject files with 77 rows each and one subject file
  with 76 rows.

## Review Summary

The extension has transparent AI-assisted review, not human review.

- Rows reviewed: 1,000.
- Pass rows: 851.
- Warning-only rows: 149.
- Structural failures: 0.
- Total warnings: 165.

The most common warnings are upstream Bangla-English digit mismatches and
formula-like token mismatches. These should be treated as a warning sensitivity,
not as silent quality-controlled rows.

## Recommended Use

For thesis:

- Keep the main claim anchored in `validation_200_v5`.
- Use the 851-row pass-only extension to show that the BEnQA part of the result
  can scale beyond the 200-item gold core.
- Use the full 1,000-row reviewed extension only with warning-status sensitivity.

For publication:

- Present the dataset as a two-tier benchmark: gold paired core plus silver
  BEnQA scale extension.
- Report all quality-status categories.
- Never call the extension human-reviewed unless a separate human review is
  actually completed and logged.

## Evaluation Plan

Priority order:

1. Run one cheap parser/prompt smoke on the 851-pass subset.
2. Evaluate one open model on Bangla/Banglish/English for the 851-pass subset.
3. If the direction matches the gold core, evaluate the other open Qwen rows.
4. Use frontier APIs only on a stratified subset unless the writing needs a
   specific cross-family replication claim.

This keeps the thesis publishable without exploding compute/API cost.

Current evaluation status:

- Smoke subset built: `data/slices/benqa_extended_1000_v1_ai_pass_smoke26.jsonl`
  with 26 rows and 78 triad requests.
- Pilot subset built: `data/slices/benqa_extended_1000_v1_ai_pass_pilot130.jsonl`
  with 130 rows and 390 triad requests.
- Qwen2.5-3B smoke kernel pushed to Kaggle:
  `munimthahmid/qwen2-5-3b-benqa-extension-smoke26`.
- Qwen2.5-3B smoke output collected cleanly: 78/78 rows, 0 parsed-empty rows,
  and no runtime/parser failure pattern. Accuracy on the 26-item smoke is
  8/26 Bangla, 11/26 reviewed Banglish, and 20/26 English.
- Qwen2.5-3B pilot130 output collected cleanly: 390/390 rows, 0 parsed-empty
  rows, and no runtime/parser failure pattern. Accuracy on the 130-item pilot
  is 53/130 Bangla, 42/130 reviewed Banglish, and 71/130 English.
- Pilot paired gaps are -8.46 pts reviewed Banglish minus Bangla, -22.31 pts
  reviewed Banglish minus English, and +13.85 pts English minus Bangla.
- The BEnQA extension pilot aligns with the validation-200 v5 BEnQA gold-core
  pattern for Qwen2.5-3B: both show English > Bangla > reviewed Banglish, with
  similar gap magnitudes.
- The pilot has 49 recoverable reviewed-Banglish misses where Banglish is wrong
  but Bangla or English is correct on the same item.
- Qwen2.5-3B full 851-row pass-only extension output collected cleanly:
  2,553/2,553 rows, 0 parsed-empty rows, and no runtime/parser failure pattern.
  Accuracy is 291/851 Bangla, 248/851 reviewed Banglish, and 437/851 English.
- Full-extension paired gaps are -5.05 pts reviewed Banglish minus Bangla
  with CI [-8.46, -1.65], -22.21 pts reviewed Banglish minus English with
  CI [-26.20, -18.10], and +17.16 pts English minus Bangla with CI
  [+13.28, +20.92].
- The full extension exports 311 recoverable reviewed-Banglish misses where
  Banglish is wrong but Bangla or English is correct on the same item.
- DeepSeek V4 Flash full 851-row pass-only extension output collected cleanly:
  2,553/2,553 rows, STOP=2,553, 0 parsed-empty rows. Accuracy is 665/851
  Bangla, 376/851 reviewed Banglish, and 697/851 English.
- DeepSeek full-extension paired gaps are -33.96 pts reviewed Banglish minus
  Bangla with CI [-37.84, -30.08], -37.72 pts reviewed Banglish minus English
  with CI [-41.36, -33.96], and +3.76 pts English minus Bangla with CI
  [+1.29, +6.35].
- DeepSeek full851 exports 380 recoverable reviewed-Banglish misses.
- Next step: integrate the Qwen and DeepSeek scale results into the thesis
  write-up; do not add more extension models by default.

## Claim Boundary

Safe claim:

"The deeply audited 200-item gold core is supported by a larger 851-item
AI-triaged BEnQA pass subset, showing that the controlled BEnQA script-robustness
signal can be scaled beyond the original gold core."

Avoid:

- "The 1,000-row extension is human-reviewed."
- "The extension has the same quality level as validation-200 v5."
- "The extension solves natural Banglish coverage."
