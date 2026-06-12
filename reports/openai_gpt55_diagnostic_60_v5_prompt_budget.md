# Prompt Budget Estimate

Updated: 2026-06-04

## Inputs

- Input slice: `data/slices/openai_gpt55_diagnostic_60_v5.jsonl`
- Summary CSV: `results/analysis/openai_gpt55_diagnostic_60_v5_prompt_budget_summary.csv`

Approximate tokens use `ceil(characters / 4)`. This is a budget heuristic,
not provider-specific tokenization.

## Summary

| Group | Calls | Total approx tokens | Mean | Max |
| --- | ---: | ---: | ---: | ---: |
| `overall` | 180 | 9469 | 52.6 | 92 |
| `dataset=banglamath` | 120 | 5970 | 49.8 | 65 |
| `dataset=banglamath;variant=bangla` | 40 | 1927 | 48.2 | 62 |
| `dataset=banglamath;variant=banglish_clean` | 40 | 2019 | 50.5 | 65 |
| `dataset=banglamath;variant=english` | 40 | 2024 | 50.6 | 62 |
| `dataset=benqa` | 60 | 3499 | 58.3 | 92 |
| `dataset=benqa;variant=bangla` | 20 | 1133 | 56.6 | 91 |
| `dataset=benqa;variant=banglish_clean` | 20 | 1158 | 57.9 | 90 |
| `dataset=benqa;variant=english` | 20 | 1208 | 60.4 | 92 |
| `variant=bangla` | 60 | 3060 | 51.0 | 91 |
| `variant=banglish_clean` | 60 | 3177 | 53.0 | 90 |
| `variant=english` | 60 | 3232 | 53.9 | 92 |
