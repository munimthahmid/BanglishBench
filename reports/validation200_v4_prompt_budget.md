# Prompt Budget Estimate

Updated: 2026-05-28

## Inputs

- Input slice: `data/slices/validation_200_v4.jsonl`
- Summary CSV: `results/analysis/validation200_v4_prompt_budget_summary.csv`

Approximate tokens use `ceil(characters / 4)`. This is a budget heuristic,
not provider-specific tokenization.

## Summary

| Group | Calls | Total approx tokens | Mean | Max |
| --- | ---: | ---: | ---: | ---: |
| `overall` | 600 | 36489 | 60.8 | 132 |
| `dataset=banglamath` | 168 | 9132 | 54.4 | 122 |
| `dataset=banglamath;variant=bangla` | 56 | 2974 | 53.1 | 110 |
| `dataset=banglamath;variant=banglish_clean` | 56 | 3140 | 56.1 | 122 |
| `dataset=banglamath;variant=english` | 56 | 3018 | 53.9 | 93 |
| `dataset=benqa` | 432 | 27357 | 63.3 | 132 |
| `dataset=benqa;variant=bangla` | 144 | 8820 | 61.2 | 124 |
| `dataset=benqa;variant=banglish_clean` | 144 | 9074 | 63.0 | 127 |
| `dataset=benqa;variant=english` | 144 | 9463 | 65.7 | 132 |
| `variant=bangla` | 200 | 11794 | 59.0 | 124 |
| `variant=banglish_clean` | 200 | 12214 | 61.1 | 127 |
| `variant=english` | 200 | 12481 | 62.4 | 132 |
