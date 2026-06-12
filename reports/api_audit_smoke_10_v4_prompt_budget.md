# Prompt Budget Estimate

Updated: 2026-05-28

## Inputs

- Input slice: `data/slices/api_audit_smoke_10_v4.jsonl`
- Summary CSV: `results/analysis/api_audit_smoke_10_v4_prompt_budget_summary.csv`

Approximate tokens use `ceil(characters / 4)`. This is a budget heuristic,
not provider-specific tokenization.

## Summary

| Group | Calls | Total approx tokens | Mean | Max |
| --- | ---: | ---: | ---: | ---: |
| `overall` | 30 | 1741 | 58.0 | 97 |
| `dataset=banglamath` | 12 | 518 | 43.2 | 49 |
| `dataset=banglamath;variant=bangla` | 4 | 165 | 41.2 | 45 |
| `dataset=banglamath;variant=banglish_clean` | 4 | 172 | 43.0 | 47 |
| `dataset=banglamath;variant=english` | 4 | 181 | 45.2 | 49 |
| `dataset=benqa` | 18 | 1223 | 67.9 | 97 |
| `dataset=benqa;variant=bangla` | 6 | 396 | 66.0 | 91 |
| `dataset=benqa;variant=banglish_clean` | 6 | 412 | 68.7 | 97 |
| `dataset=benqa;variant=english` | 6 | 415 | 69.2 | 93 |
| `variant=bangla` | 10 | 561 | 56.1 | 91 |
| `variant=banglish_clean` | 10 | 584 | 58.4 | 97 |
| `variant=english` | 10 | 596 | 59.6 | 93 |
