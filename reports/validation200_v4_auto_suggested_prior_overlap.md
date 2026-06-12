# Auto-Suggested Banglish Candidate: Prior Outcome Overlap

Updated: 2026-05-28

## Purpose

This analysis checks where the automatic Banglish spelling suggestions fall relative to the already completed validation-200 v3-to-v4 Banglish sensitivity results. It helps interpret the currently running auto-suggested GPU sensitivity jobs.

## Inputs

- Qwen2.5 v3-v4 compare: `results/analysis/qwen25_validation200_v3_vs_v4_banglish_items_reparsed.csv`
- Qwen3 v3-v4 compare: `results/analysis/qwen3_validation200_v3_vs_v4_banglish_items_reparsed.csv`
- Summary CSV: `results/analysis/validation200_v4_auto_suggested_prior_overlap_summary.csv`

## Candidate Coverage

- Items with any auto-suggested text change: 140/200
- Items with clean-field change: 140/200
- Items with noisy-field change: 138/200

## Existing v4 Outcomes by Candidate Bucket

| Model | Bucket | n | v3 correct | v4 correct | v4-v3 | v4 wrong |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | auto_changed | 140 | 26 | 26 | 0 | 114 |
| Qwen2.5-3B | auto_unchanged | 60 | 12 | 13 | 1 | 47 |
| Qwen2.5-3B | all | 200 | 38 | 39 | 1 | 161 |
| Qwen3-4B | auto_changed | 140 | 33 | 33 | 0 | 107 |
| Qwen3-4B | auto_unchanged | 60 | 13 | 14 | 1 | 46 |
| Qwen3-4B | all | 200 | 46 | 47 | 1 | 153 |

## Interpretation Before New GPU Results

- Qwen2.5-3B: among the 140 auto-changed items, v4 already gets 26/140 correct and leaves 114 wrong; among the 60 unchanged items, v4 gets 13/60 correct.
- Qwen3-4B: among the 140 auto-changed items, v4 already gets 33/140 correct and leaves 107 wrong; among the 60 unchanged items, v4 gets 14/60 correct.
- The auto-suggested run therefore has room to improve many currently wrong changed items, but it can also create losses. The paired result after the Kaggle runs finish is the decisive check.
