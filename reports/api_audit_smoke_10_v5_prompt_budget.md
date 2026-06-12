# Prompt Budget Estimate

Updated: 2026-06-11

## Inputs

- Input slice: `data/slices/api_audit_smoke_10_v5.jsonl`
- Summary CSV: `results/analysis/api_audit_smoke_10_v5_prompt_budget_summary.csv`

Approximate tokens use `ceil(characters / 4)`. This is a budget heuristic,
not provider-specific tokenization.

## Summary

| Group | Calls | Total approx tokens | Mean | Max |
| --- | ---: | ---: | ---: | ---: |
| `overall` | 30 | 1736 | 57.9 | 97 |
| `dataset=banglamath` | 12 | 516 | 43.0 | 49 |
| `dataset=banglamath;variant=bangla` | 4 | 165 | 41.2 | 45 |
| `dataset=banglamath;variant=banglish_clean` | 4 | 170 | 42.5 | 46 |
| `dataset=banglamath;variant=english` | 4 | 181 | 45.2 | 49 |
| `dataset=benqa` | 18 | 1220 | 67.8 | 97 |
| `dataset=benqa;variant=bangla` | 6 | 396 | 66.0 | 91 |
| `dataset=benqa;variant=banglish_clean` | 6 | 409 | 68.2 | 97 |
| `dataset=benqa;variant=english` | 6 | 415 | 69.2 | 93 |
| `variant=bangla` | 10 | 561 | 56.1 | 91 |
| `variant=banglish_clean` | 10 | 579 | 57.9 | 97 |
| `variant=english` | 10 | 596 | 59.6 | 93 |
