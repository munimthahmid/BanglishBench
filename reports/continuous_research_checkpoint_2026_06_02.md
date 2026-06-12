# Continuous Research Checkpoint: 2026-06-02

## Current State

The frozen validation-200 v5 benchmark remains locked. No manual review, paid
API call, or new Kaggle job was launched in this continuation. Recent work
added no-spend BEnQA prediction-diversity, cross-script agreement,
cross-model Banglish-agreement, order-confound, and review-label option-bias
audits that make the Qwen3 reviewed-Banglish option collapse easier to cite.
This continuation also added a length/token confound audit for the same
D-attractor and an option-coverage confound audit for the lexical-familiarity
alternative, then added a BanglaMATH numeric-transfer audit for the short-answer
side of the failure analysis and a BEnQA multi-confound residual audit for the
option-collapse story.

## BEnQA Prediction-Diversity Audit

Artifacts:

- `scripts/analyze_v5_benqa_prediction_diversity.py`
- `reports/v5_benqa_prediction_diversity.md`
- `results/analysis/v5_benqa_prediction_diversity_summary.csv`

Key result:

- Gold BEnQA labels are close to balanced: A=29, B=35, C=41, D=39; normalized
  entropy 0.994 and 3.97 effective options.
- Qwen3-4B reviewed Banglish predicts A=3, B=7, C=20, D=111, dropping to 0.502
  normalized entropy and 2.01 effective options.
- The same Qwen3 row has 3.52 effective options in Bangla and 3.69 in English.
- Qwen2.5 reviewed Banglish retains high diversity: 3.75 and 3.77 effective
  options for the 3B and 7B rows.
- Subject rollup keeps the same story: Qwen3 reviewed Banglish is majority-D
  in 12/13 subjects with mean subject entropy 0.402, versus 0.799 Bangla and
  0.807 English.

Interpretation: the Qwen3 reviewed-Banglish BEnQA failure is not just lower
accuracy or a majority-label count. It is a measurable prediction-diversity
collapse relative to gold labels, Qwen3's other scripts, and Qwen2.5 reviewed
Banglish. This remains behavioral evidence, not an internal causal mechanism.

## BEnQA Cross-Script Option Agreement

Artifacts:

- `scripts/analyze_v5_benqa_cross_script_option_agreement.py`
- `reports/v5_benqa_cross_script_option_agreement.md`
- `results/analysis/v5_benqa_cross_script_option_agreement_items.csv`
- `results/analysis/v5_benqa_cross_script_option_agreement_summary.csv`

Key result:

- When Qwen3 Bangla and English are both correct and agree on the same non-D
  option, reviewed Banglish still switches to wrong D on 23/36 rows.
- The corresponding Qwen2.5 wrong-D rates are 2/23 and 7/44.
- In the broader Qwen3 Bangla-English non-D agreement slice, reviewed Banglish
  predicts D on 30/47 rows.

Interpretation: the D-attractor survives a stricter agreement filter where both
alternate-script views support the same non-D answer. This is still privileged
diagnostic evidence, not deployable mitigation.

## BEnQA Cross-Model Banglish Agreement

Artifacts:

- `scripts/analyze_v5_benqa_cross_model_banglish_agreement.py`
- `reports/v5_benqa_cross_model_banglish_agreement.md`
- `results/analysis/v5_benqa_cross_model_banglish_agreement_items.csv`
- `results/analysis/v5_benqa_cross_model_banglish_agreement_summary.csv`

Key result:

- The two Qwen2.5 rows agree on a reviewed-Banglish option in 61/144 BEnQA
  items, including 42 non-D agreements.
- When both Qwen2.5 rows agree on non-D reviewed Banglish, Qwen3 predicts D on
  26/42 rows and wrong D on 18/42.
- In the stricter both-correct non-D slice, Qwen3 is wrong-D on 8/15 rows and
  matches the Qwen2.5 agreement on 4/15 rows.

Interpretation: this holds the script fixed and shows the Qwen3 D-attractor
persists even where the same reviewed-Banglish item supports Qwen2.5 non-D
agreement. The strict slice is small, so use it as corroborating evidence.

## BEnQA Order Confound

Artifacts:

- `scripts/analyze_v5_benqa_order_confound.py`
- `reports/v5_benqa_order_confound.md`
- `results/analysis/v5_benqa_order_confound_items.csv`
- `results/analysis/v5_benqa_order_confound_summary.csv`

Key result:

- By reviewed-Banglish output-line quartile, Qwen3 predicts D on 26/36,
  31/36, 28/36, and 26/36 rows.
- Wrong-D counts by the same quartiles are 20/36, 19/36, 19/36, and 19/36.
- Qwen3 has 23 separate D-runs and a longest contiguous D-run of 13, while
  Qwen2.5 rows have longest D-runs of 3 and 2.

Interpretation: the D-attractor is present from the first run quartile through
the last, so it is not a simple late-run degradation or single terminal output
corruption.

## BEnQA Review-Label Option Bias

Artifacts:

- `scripts/analyze_v5_benqa_review_label_option_bias.py`
- `reports/v5_benqa_review_label_option_bias.md`
- `results/analysis/v5_benqa_review_label_option_bias_items.csv`
- `results/analysis/v5_benqa_review_label_option_bias_summary.csv`

Key result:

- Qwen3 predicts D on 39/51 unreviewed BEnQA rows, with wrong D on 28/51;
  gold D appears on 13/51.
- Qwen3 predicts D on 69/90 reviewed nonbad rows.
- Qwen2.5 rows are much lower: 10/51 and 7/51 D predictions in the unreviewed
  bucket, and 28/90 and 17/90 in the reviewed nonbad bucket.

Interpretation: the D-attractor is not confined to rows selected for v5
Banglish review or manual edits. Major-edit and bad buckets remain too small
for standalone claims.

## BEnQA Length/Token Confound

Artifacts:

- `scripts/analyze_v5_benqa_length_token_confound.py`
- `reports/v5_benqa_length_token_confound.md`
- `results/analysis/v5_benqa_length_token_confound_items.csv`
- `results/analysis/v5_benqa_length_token_confound_summary.csv`

Key result:

- The audit joins 432 frozen-v5 BEnQA choice rows with reviewed-Banglish
  tokenization features and exports 48 quartile summary rows.
- By reviewed-Banglish HF-token quartile, Qwen3 predicts D on 32/36, 26/36,
  27/36, and 26/36 rows; wrong-D counts are 26/36, 17/36, 15/36, and 19/36.
- By character-length quartile, Qwen3 still predicts D on 31/36 shortest rows
  and 29/36 longest rows.
- Qwen2.5 rows remain much lower in shortest/longest HF-token quartiles:
  5/36 and 14/36 for 3B, 1/36 and 9/36 for 7B.

Interpretation: the Qwen3 reviewed-Banglish BEnQA D-attractor is not a simple
long-prompt or token-burden artifact. This remains a behavioral confound audit,
not an internal mechanism claim.

## BEnQA Option-Coverage Confound

Artifacts:

- `scripts/analyze_v5_benqa_option_coverage_confound.py`
- `reports/v5_benqa_option_coverage_confound.md`
- `results/analysis/v5_benqa_option_coverage_confound_items.csv`
- `results/analysis/v5_benqa_option_coverage_confound_summary.csv`

Key result:

- The audit joins 432 frozen-v5 BEnQA choice rows with per-option exact
  BanglaTLit lexical coverage and exports 21 summary rows.
- On 101 BEnQA items where all four answer options have identical exact
  coverage, Qwen3 predicts D on 76/101 rows and wrong D on 52/101.
- Qwen2.5 rows in the same tied-coverage bucket predict D on only 14/101 and
  8/101 rows.
- When at least one option has higher exact coverage than D, Qwen3 still
  predicts D on 31/35 rows and wrong D on 23/35.

Interpretation: option lexical familiarity is not sufficient to explain the
Qwen3 D-attractor. This is exact-overlap behavioral evidence, not a causal
mechanism claim.

## BEnQA Multi-Confound Residual

Artifacts:

- `scripts/analyze_v5_benqa_multiconfound_residual.py`
- `reports/v5_benqa_multiconfound_residual.md`
- `results/analysis/v5_benqa_multiconfound_residual_items.csv`
- `results/analysis/v5_benqa_multiconfound_residual_summary.csv`

Key result:

- The audit joins 432 BEnQA choice rows with option length/content, exact
  option coverage, semantic-cue, and option-switch rows; it exports 36 summary
  rows.
- In the primary residual scope, Qwen3 is wrong-D on 19/24 rows; Qwen2.5 rows
  are 4/24 and 1/24.
- In the tied-coverage residual scope, Qwen3 is wrong-D on 16/20 rows; Qwen2.5
  rows are 4/20 and 1/20.
- Correct non-D Bangla/English answers in the primary residual scope still
  become wrong reviewed-Banglish D for Qwen3 on 11/13 and 11/14 rows.

Interpretation: the D-attractor survives several local confound controls at
once, but the residual slice is small and should support the failure-mode
argument rather than replace the all-200 paired result.

## BanglaMATH Numeric Transfer Audit

Artifacts:

- `scripts/analyze_v5_banglamath_numeric_transfer.py`
- `reports/v5_banglamath_numeric_transfer.md`
- `results/analysis/v5_banglamath_numeric_transfer_items.csv`
- `results/analysis/v5_banglamath_numeric_transfer_summary.csv`

Key result:

- The audit exports 168 model-item rows and 3 model summaries.
- Qwen3 has an alternate-script raw numeric signature on 24/56 BanglaMATH items,
  but reviewed Banglish retains it on only 8/24 and is correct on 2/24.
- Qwen2.5 retention is 1/12 for 3B and 4/24 for 7B.
- In Qwen3's alternate-signature slice, reviewed Banglish has 9/24
  meta/uncertainty outputs and 4/24 wrong no-number outputs.

Interpretation: numeric evidence visible in Bangla or English does not reliably
transfer into reviewed Banglish. Numeric signatures remain optimistic behavioral
evidence because they can credit values in reasoning, not only final answers.

## QA Snapshot

- Full local QA rerun completed on 2026-06-02 after the multi-confound audit.
- Dashboard: 61 rows, 0 blocked, 0 failing.
- Research log compactness: 65 checks, 0 issues; `research_log.md` is 269
  lines / 15.0 KB.
- Secret hygiene: 901 files checked, 0 suspicious findings.
- Local artifact references: 4,051 checked, 0 unexpected missing, 19 expected
  future references.
- Reproducibility manifest: 899 non-secret artifacts.
