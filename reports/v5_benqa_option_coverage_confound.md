# Frozen-V5 BEnQA Option-Coverage Confound Audit

Updated: 2026-06-11

## Scope

This no-spend audit checks whether Qwen3-4B's reviewed-Banglish BEnQA
D-attractor can be reduced to choosing the most lexically familiar
answer option. It reuses the exact BanglaTLit vocabulary and tokenizer
from the BEnQA option-lexical coverage audit, computes per-option
coverage for A/B/C/D, and joins those features to frozen-v5 choice-bias
rows.

- Item table: `results/analysis/v5_benqa_option_coverage_confound_items.csv`
- Summary table: `results/analysis/v5_benqa_option_coverage_confound_summary.csv`

## Headline

- On rows where all four options have identical exact BanglaTLit coverage, Qwen3-4B still predicts D on 76/101 rows (75.2%) and wrong D on 52/101.
- The corresponding Qwen2.5 D counts in the same tied-coverage bucket are 14/101 and 8/101.
- When at least one option has higher exact coverage than D, Qwen3-4B still predicts D on 31/35 rows and wrong D on 23/35.
- Qwen2.5 rows in that not-highest-D bucket predict D on 22/35 and 15/35 rows.
- Only three items have D as a strictly highest-coverage option; Qwen3 predicts D on 1/3 of them.

## Bucket Summary

| Model | Bucket | Rows | Gold D | Pred D | Wrong D | Correct | Mean D coverage |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | overall | 144 | 39 | 39 | 25 | 41 | 0.1868 |
| Qwen2.5-7B 8-bit | overall | 144 | 39 | 25 | 17 | 47 | 0.1868 |
| Qwen3-4B | overall | 144 | 39 | 111 | 77 | 47 | 0.1868 |
| Qwen2.5-3B | all_options_same_coverage | 101 | 27 | 14 | 10 | 24 | 0.0792 |
| Qwen2.5-7B 8-bit | all_options_same_coverage | 101 | 27 | 8 | 7 | 32 | 0.0792 |
| Qwen3-4B | all_options_same_coverage | 101 | 27 | 76 | 52 | 35 | 0.0792 |
| Qwen2.5-3B | d_among_highest_coverage | 109 | 30 | 17 | 10 | 30 | 0.1321 |
| Qwen2.5-7B 8-bit | d_among_highest_coverage | 109 | 30 | 10 | 7 | 37 | 0.1321 |
| Qwen3-4B | d_among_highest_coverage | 109 | 30 | 80 | 54 | 38 | 0.1321 |
| Qwen2.5-3B | d_not_highest_coverage | 35 | 9 | 22 | 15 | 11 | 0.3571 |
| Qwen2.5-7B 8-bit | d_not_highest_coverage | 35 | 9 | 15 | 10 | 10 | 0.3571 |
| Qwen3-4B | d_not_highest_coverage | 35 | 9 | 31 | 23 | 9 | 0.3571 |
| Qwen2.5-3B | d_among_lowest_coverage | 111 | 29 | 14 | 10 | 25 | 0.0721 |
| Qwen2.5-7B 8-bit | d_among_lowest_coverage | 111 | 29 | 8 | 7 | 34 | 0.0721 |
| Qwen3-4B | d_among_lowest_coverage | 111 | 29 | 83 | 58 | 36 | 0.0721 |
| Qwen2.5-3B | d_not_lowest_coverage | 33 | 10 | 25 | 15 | 16 | 0.5727 |
| Qwen2.5-7B 8-bit | d_not_lowest_coverage | 33 | 10 | 17 | 10 | 13 | 0.5727 |
| Qwen3-4B | d_not_lowest_coverage | 33 | 10 | 28 | 19 | 11 | 0.5727 |
| Qwen2.5-3B | d_strict_highest_coverage | 3 | 1 | 1 | 0 | 3 | 1.0 |
| Qwen2.5-7B 8-bit | d_strict_highest_coverage | 3 | 1 | 1 | 0 | 3 | 1.0 |
| Qwen3-4B | d_strict_highest_coverage | 3 | 1 | 1 | 0 | 2 | 1.0 |

## Interpretation

- Exact BanglaTLit option coverage is too tie-heavy to explain the D-attractor
  as a simple highest-coverage-option heuristic.
- The strongest slice is the 101-item tied-coverage bucket: option lexical
  familiarity supplies no A/B/C/D distinction, but Qwen3 still collapses
  toward D while Qwen2.5 does not.
- This remains behavioral evidence over exact lexical overlap. It does not
  identify the internal mechanism behind the Qwen3 failure mode.
