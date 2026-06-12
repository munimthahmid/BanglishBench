# Frozen-v5 BEnQA Multi-Confound Residual Audit

Updated: 2026-06-11

This audit joins the frozen-v5 BEnQA choice-bias rows with option
position/length, exact BanglaTLit option coverage, simple semantic-cue
flags, and alternate-script option-switch rows. It asks whether the Qwen3
reviewed-Banglish D-attractor remains after several local explanations
are removed at the same time.

Machine-readable outputs:

- Item rows: `results/analysis/v5_benqa_multiconfound_residual_items.csv`
- Summary rows: `results/analysis/v5_benqa_multiconfound_residual_summary.csv`

## Key Result

- Primary residual scope: gold is not D, D is not the longest option, and
  D has no simple composite/numeric/all-none-both cue.
- In that 24-item scope, Qwen3 predicts wrong D on 19/24 rows (79.2%).
- The two Qwen2.5 rows are much lower: 4/24 and 1/24.
- In the stricter tied-coverage residual scope, Qwen3 is wrong-D on 16/20 rows, while Qwen2.5 rows are 4/20 and 1/20.
- The D-not-highest-coverage residual is tiny at n=3; Qwen3 is wrong-D on 2/3,
  so use it only as a stress slice, not as a standalone estimate.

## Alternate-Script Support

Restricting to rows where the same model's Bangla or English answer is
already correct and non-D preserves the residual failure mode:

| Model | Bangla correct non-D -> wrong D | English correct non-D -> wrong D |
| --- | ---: | ---: |
| Qwen2.5-3B | 1/7 | 1/13 |
| Qwen2.5-7B 8-bit | 1/14 | 0/17 |
| Qwen3-4B | 11/13 | 11/14 |

## Interpretation

The Qwen3 D-attractor is not just a single local confound such as gold-label
imbalance, a long D option, a simple semantic cue, or exact option-coverage
ties considered separately. The residual scope is smaller than the full
BEnQA set, so it should be used as a targeted failure-mode audit rather than
a replacement for the main all-200 paired result.

## Summary Table

| Section | Scope | Model | Baseline | n | D/wrong-D or switch count | Subjects |
| --- | --- | --- | --- | ---: | ---: | ---: |
| choice_scope | non_gold_D | Qwen2.5-3B |  | 105 | 25/105 | 13 |
| choice_scope | non_gold_D_D_not_longest | Qwen2.5-3B |  | 36 | 4/36 | 13 |
| choice_scope | non_gold_D_D_no_semantic_cue | Qwen2.5-3B |  | 37 | 7/37 | 9 |
| choice_scope | residual_primary | Qwen2.5-3B |  | 24 | 4/24 | 9 |
| choice_scope | residual_tied_coverage | Qwen2.5-3B |  | 20 | 4/20 | 9 |
| choice_scope | residual_D_not_highest_coverage | Qwen2.5-3B |  | 3 | 0/3 | 3 |
| switch_scope | baseline_correct_non_D | Qwen2.5-3B | Bangla | 35 | 6/35 | 13 |
| switch_scope | baseline_correct_non_D_residual_primary | Qwen2.5-3B | Bangla | 7 | 1/7 | 4 |
| switch_scope | baseline_correct_non_D_residual_tied_coverage | Qwen2.5-3B | Bangla | 7 | 1/7 | 4 |
| switch_scope | baseline_correct_non_D | Qwen2.5-3B | English | 48 | 8/48 | 13 |
| switch_scope | baseline_correct_non_D_residual_primary | Qwen2.5-3B | English | 13 | 1/13 | 8 |
| switch_scope | baseline_correct_non_D_residual_tied_coverage | Qwen2.5-3B | English | 12 | 1/12 | 8 |
| choice_scope | non_gold_D | Qwen2.5-7B 8-bit |  | 105 | 17/105 | 13 |
| choice_scope | non_gold_D_D_not_longest | Qwen2.5-7B 8-bit |  | 36 | 3/36 | 13 |
| choice_scope | non_gold_D_D_no_semantic_cue | Qwen2.5-7B 8-bit |  | 37 | 3/37 | 9 |
| choice_scope | residual_primary | Qwen2.5-7B 8-bit |  | 24 | 1/24 | 9 |
| choice_scope | residual_tied_coverage | Qwen2.5-7B 8-bit |  | 20 | 1/20 | 9 |
| choice_scope | residual_D_not_highest_coverage | Qwen2.5-7B 8-bit |  | 3 | 0/3 | 3 |
| switch_scope | baseline_correct_non_D | Qwen2.5-7B 8-bit | Bangla | 54 | 10/54 | 13 |
| switch_scope | baseline_correct_non_D_residual_primary | Qwen2.5-7B 8-bit | Bangla | 14 | 1/14 | 7 |
| switch_scope | baseline_correct_non_D_residual_tied_coverage | Qwen2.5-7B 8-bit | Bangla | 11 | 1/11 | 7 |
| switch_scope | baseline_correct_non_D | Qwen2.5-7B 8-bit | English | 69 | 11/69 | 13 |
| switch_scope | baseline_correct_non_D_residual_primary | Qwen2.5-7B 8-bit | English | 17 | 0/17 | 8 |
| switch_scope | baseline_correct_non_D_residual_tied_coverage | Qwen2.5-7B 8-bit | English | 14 | 0/14 | 8 |
| choice_scope | non_gold_D | Qwen3-4B |  | 105 | 77/105 | 13 |
| choice_scope | non_gold_D_D_not_longest | Qwen3-4B |  | 36 | 22/36 | 13 |
| choice_scope | non_gold_D_D_no_semantic_cue | Qwen3-4B |  | 37 | 30/37 | 9 |
| choice_scope | residual_primary | Qwen3-4B |  | 24 | 19/24 | 9 |
| choice_scope | residual_tied_coverage | Qwen3-4B |  | 20 | 16/20 | 9 |
| choice_scope | residual_D_not_highest_coverage | Qwen3-4B |  | 3 | 2/3 | 3 |
| switch_scope | baseline_correct_non_D | Qwen3-4B | Bangla | 44 | 30/44 | 13 |
| switch_scope | baseline_correct_non_D_residual_primary | Qwen3-4B | Bangla | 13 | 11/13 | 7 |
| switch_scope | baseline_correct_non_D_residual_tied_coverage | Qwen3-4B | Bangla | 10 | 9/10 | 7 |
| switch_scope | baseline_correct_non_D | Qwen3-4B | English | 54 | 37/54 | 13 |
| switch_scope | baseline_correct_non_D_residual_primary | Qwen3-4B | English | 14 | 11/14 | 7 |
| switch_scope | baseline_correct_non_D_residual_tied_coverage | Qwen3-4B | English | 11 | 9/11 | 6 |
