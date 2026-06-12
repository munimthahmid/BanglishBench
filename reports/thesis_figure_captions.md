# Thesis Figure Captions

Updated: 2026-05-30

## Purpose

This file stores thesis-ready caption drafts for the current figures.

## F1: Main Script Gap

Artifact: `reports/figures/main_script_gap.svg`

Draft caption:

Frozen validation-200 v5 accuracy by script for the main Qwen-family models.
Banglish uses reviewed Romanized Bangla prompts while Bangla and English use
parallel native or translated prompts. Qwen2.5-7B 8-bit and Qwen3-4B retain
negative all-200 paired Banglish-minus-Bangla intervals. Qwen2.5-3B retains a
point deficit, but its reviewed all-200 interval reaches zero; its historical
and strict-197 checks remain negative.

Presentation note:

- Keep numerator/denominator and paired intervals in the surrounding table,
  not only percent labels.

## F2: Self-Normalization Delta

Artifact: `reports/figures/selfnorm_delta.svg`

Draft caption:

Effect of model self-normalization before answering Banglish prompts.
Self-normalization improves Qwen2.5-3B on validation-200, is flat for the
Qwen2.5-7B 8-bit run, and sharply hurts Qwen3-4B. The result shows that
prompt-only normalization is not a stable mitigation across model families.

Post-v5 note:

- Caption must say whether the figure uses full200, dev50, or test150.
- Do not present answer-signal routing in the same caption unless the figure is
  explicitly marked exploratory.

## F3: Cross-Script Recovery

Artifact: `reports/figures/cross_script_recovery.svg`

Draft caption:

Frozen-v5 reviewed Banglish accuracy compared with a privileged Bangla+English
agreement route and an any-script oracle. Cross-script agreement recovers a
meaningful share of the Banglish failures, especially for Qwen2.5-7B and
Qwen3-4B, while the oracle shows additional headroom. Because the route uses
benchmark-provided alternate script views, it is diagnostic evidence rather
than deployable accuracy. The Qwen2.5-3B route point gain remains positive, but
its reviewed-v5 interval crosses zero.

Post-v5 note:

- Keep the word "privileged" in the caption unless generated alternate-script
  views are used under a locked post-v5 protocol.

## Planned F4: v5 Review Impact

Source artifacts:

- `reports/validation200_v5_review_impact_ranking.md`
- `reports/validation200_v5_review_impact_substitutions.md`
- `reports/validation200_v5_review_metadata_summary.md`

Draft caption:

Human-review workload for validation-200 v5, grouped by impact tier and repeated
Banglish substitution pattern. The review queue concentrates on rows where both
main models are wrong under current Banglish and where alternate scripts suggest
recoverable answers, prioritizing edits most likely to affect the thesis-facing
script-gap estimate.

Post-v5 note:

- Add final counts for accepted, rejected, and bad rows after review.
- If bad rows are retained in the denominator, say so explicitly.

## Planned F5: Generated-View Funnel

Source artifacts:

- `reports/generated_view_preservation_audit_v2.md`
- `reports/generated_view_prompt_set_dev50_benqa_mcq.md`
- `reports/qwen3_4b_generated_bn_answer_audit_dev50.md`
- `reports/qwen25_3b_generated_bn_answer_audit_dev50.md`

Draft caption:

Generated alternate-script views require both structural preservation and answer
audits. Raw deterministic generators fail MCQ preservation gates, while
protected generators pass the gates but produce model- and generator-dependent
answer effects on dev BEnQA items. The deployable mitigation route therefore
remains future work rather than a locked thesis result.

Post-v5 note:

- Keep this as a diagnostic figure unless generated-view test results are run
  under the preregistered post-v5 protocol.
