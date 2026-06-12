# Prompt Budget Estimate

Updated: 2026-06-04

## Inputs

- Input slice: `data/slices/validation_200_v5.jsonl`
- Summary CSV: `results/analysis/openai_gpt55_validation200_v5_cap1024_prompt_budget_summary.csv`

Approximate tokens use `ceil(characters / 4)`. This is a budget heuristic,
not provider-specific tokenization.

## Summary

| Group | Calls | Total approx tokens | Mean | Max |
| --- | ---: | ---: | ---: | ---: |
| `overall` | 600 | 36471 | 60.8 | 132 |
| `dataset=banglamath` | 168 | 9127 | 54.3 | 122 |
| `dataset=banglamath;variant=bangla` | 56 | 2974 | 53.1 | 110 |
| `dataset=banglamath;variant=banglish_clean` | 56 | 3135 | 56.0 | 122 |
| `dataset=banglamath;variant=english` | 56 | 3018 | 53.9 | 93 |
| `dataset=benqa` | 432 | 27344 | 63.3 | 132 |
| `dataset=benqa;variant=bangla` | 144 | 8820 | 61.2 | 124 |
| `dataset=benqa;variant=banglish_clean` | 144 | 9061 | 62.9 | 127 |
| `dataset=benqa;variant=english` | 144 | 9463 | 65.7 | 132 |
| `variant=bangla` | 200 | 11794 | 59.0 | 124 |
| `variant=banglish_clean` | 200 | 12196 | 61.0 | 127 |
| `variant=english` | 200 | 12481 | 62.4 | 132 |
