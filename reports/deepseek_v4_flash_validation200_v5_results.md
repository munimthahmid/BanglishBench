# DeepSeek V4 Flash Validation-200 v5 Results

Updated: 2026-06-05

## Scope

This is a full validation-200 v5 frontier API audit for DeepSeek V4 Flash in non-thinking mode. It uses the frozen provider-neutral prompt manifest, the same strict parser as open-model runs, and secondary parser/unit sensitivity for recoverable noncanonical answers.

- Raw API responses: `results/api_audit/deepseek_v4_flash_validation200_v5_raw.jsonl`
- Imported strict rows: `results/analysis/deepseek_v4_flash_validation200_v5_imported.jsonl`
- Item audit CSV: `results/analysis/deepseek_v4_flash_validation200_v5_items.csv`
- Summary CSV: `results/analysis/deepseek_v4_flash_validation200_v5_summary.csv`
- Paired gap CSV: `results/analysis/deepseek_v4_flash_validation200_v5_paired_gaps.csv`
- Recoverability CSV: `results/analysis/deepseek_v4_flash_validation200_v5_recoverability_items.csv`
- Gemini comparison CSV: `results/analysis/deepseek_v4_flash_validation200_v5_gemini_comparison.csv`

## Headline

- Strict accuracy on this evaluation scope is 143/200 (71.5%) Bangla, 82/200 (41.0%) reviewed Banglish, and 132/200 (66.0%) English.
- Secondary parser/unit sensitivity is 152/200 (76.0%) Bangla, 96/200 (48.0%) reviewed Banglish, and 148/200 (74.0%) English.
- Against Gemini on the matched Banglish requests, DeepSeek V4 Flash strict delta is -27.0 points; secondary delta is -32.5 points.

## Accuracy

| Dataset | Score | Bangla | Reviewed Banglish | English |
| --- | --- | ---: | ---: | ---: |
| All | Strict | 143/200 (71.5%) | 82/200 (41.0%) | 132/200 (66.0%) |
| All | Secondary | 152/200 (76.0%) | 96/200 (48.0%) | 148/200 (74.0%) |
| BEnQA | Strict | 114/144 (79.2%) | 73/144 (50.7%) | 117/144 (81.2%) |
| BEnQA | Secondary | 114/144 (79.2%) | 73/144 (50.7%) | 117/144 (81.2%) |
| BanglaMATH | Strict | 29/56 (51.8%) | 9/56 (16.1%) | 15/56 (26.8%) |
| BanglaMATH | Secondary | 38/56 (67.9%) | 23/56 (41.1%) | 31/56 (55.4%) |

## Paired Script Gaps

| Score | Dataset | Comparison | Delta | Left-only | Right-only | p |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| strict | All | Banglish - Bangla | -30.5 | 68 | 7 | 1.17e-13 |
| strict | All | Banglish - English | -25.0 | 59 | 9 | 3.91e-10 |
| strict | BanglaMATH | Banglish - Bangla | -35.7 | 21 | 1 | 1.1e-05 |
| strict | BanglaMATH | Banglish - English | -10.7 | 11 | 5 | 0.210114 |
| secondary | All | Banglish - Bangla | -28.0 | 63 | 7 | 2.28e-12 |
| secondary | All | Banglish - English | -26.0 | 59 | 7 | 2.38e-11 |
| secondary | BanglaMATH | Banglish - Bangla | -26.8 | 16 | 1 | 0.000275 |
| secondary | BanglaMATH | Banglish - English | -14.3 | 11 | 3 | 0.057373 |

## Same-Slice Model Comparison

| Model | Score | Bangla | Reviewed Banglish | English | Banglish-Bangla |
| --- | --- | ---: | ---: | ---: | ---: |
| Gemini 3.5 Flash | strict | 163/200 | 136/200 | 144/200 | -13.5 pts |
| Gemini 3.5 Flash | secondary | 170/200 | 161/200 | 165/200 | -4.5 pts |
| DeepSeek V4 Flash | strict | 143/200 | 82/200 | 132/200 | -30.5 pts |
| DeepSeek V4 Flash | secondary | 152/200 | 96/200 | 148/200 | -28.0 pts |

## Matched Gemini Delta

| Score | Variant | Delta | Model-only | Gemini-only | p |
| --- | --- | ---: | ---: | ---: | ---: |
| strict | Bangla | -10.0 | 8 | 28 | 0.001193 |
| strict | Reviewed Banglish | -27.0 | 11 | 65 | 1.81e-10 |
| strict | English | -6.0 | 7 | 19 | 0.028959 |
| secondary | Bangla | -9.0 | 7 | 25 | 0.002102 |
| secondary | Reviewed Banglish | -32.5 | 6 | 71 | 3.42e-15 |
| secondary | English | -8.5 | 4 | 21 | 0.000911 |

## Format And Cost Signals

- Finish reasons: MAX_TOKENS=11, STOP=589.
- Key usage by environment variable name: DEEPSEEK_API_KEY=600.
- Recoverable non-strict rows: 39 total (short_extended_unit=5, short_numeric_only=34).
- Reported input tokens: 57285.
- Reported output tokens: 3169.
- Reported reasoning tokens: 0.
- Approximate DeepSeek V4 Flash non-thinking pricing checked 2026-06-05 text-token cost: $0.0089.
- Total API wall time summed across requests: 730.3s.

| Variant | Parsed empty | MAX_TOKENS | Long >120 chars | Mean output tokens |
| --- | ---: | ---: | ---: | ---: |
| Bangla | 0 | 3 | 3 | 4.8 |
| Reviewed Banglish | 0 | 6 | 11 | 7.3 |
| English | 0 | 2 | 3 | 3.7 |
