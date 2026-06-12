# DeepSeek V4 Flash Smoke10 Results

Updated: 2026-06-05

## Scope

This is a 10-item / 30-request smoke gate for DeepSeek V4 Flash non-thinking on frozen validation-200 v5 prompts. It checks parser behavior, endpoint compatibility, and token/cost behavior before any full validation-200 run.

- Raw API responses: `results/api_audit/deepseek_v4_flash_smoke10_v5_raw.jsonl`
- Imported strict rows: `results/analysis/deepseek_v4_flash_smoke10_v5_imported.jsonl`
- Item audit CSV: `results/analysis/deepseek_v4_flash_smoke10_v5_items.csv`
- Summary CSV: `results/analysis/deepseek_v4_flash_smoke10_v5_summary.csv`
- Paired gap CSV: `results/analysis/deepseek_v4_flash_smoke10_v5_paired_gaps.csv`
- Recoverability CSV: `results/analysis/deepseek_v4_flash_smoke10_v5_recoverability_items.csv`
- Gemini comparison CSV: `results/analysis/deepseek_v4_flash_smoke10_v5_gemini_comparison.csv`

## Headline

- Strict accuracy on this evaluation scope is 10/10 (100.0%) Bangla, 7/10 (70.0%) reviewed Banglish, and 9/10 (90.0%) English.
- Secondary parser/unit sensitivity is 10/10 (100.0%) Bangla, 8/10 (80.0%) reviewed Banglish, and 10/10 (100.0%) English.
- Against Gemini on the matched Banglish requests, DeepSeek V4 Flash strict delta is +0.0 points; secondary delta is -20.0 points.

## Accuracy

| Dataset | Score | Bangla | Reviewed Banglish | English |
| --- | --- | ---: | ---: | ---: |
| All | Strict | 10/10 (100.0%) | 7/10 (70.0%) | 9/10 (90.0%) |
| All | Secondary | 10/10 (100.0%) | 8/10 (80.0%) | 10/10 (100.0%) |
| BEnQA | Strict | 6/6 (100.0%) | 5/6 (83.3%) | 6/6 (100.0%) |
| BEnQA | Secondary | 6/6 (100.0%) | 5/6 (83.3%) | 6/6 (100.0%) |
| BanglaMATH | Strict | 4/4 (100.0%) | 2/4 (50.0%) | 3/4 (75.0%) |
| BanglaMATH | Secondary | 4/4 (100.0%) | 3/4 (75.0%) | 4/4 (100.0%) |

## Paired Script Gaps

| Score | Dataset | Comparison | Delta | Left-only | Right-only | p |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| strict | All | Banglish - Bangla | -30.0 | 3 | 0 | 0.25 |
| strict | All | Banglish - English | -20.0 | 3 | 1 | 0.625 |
| strict | BanglaMATH | Banglish - Bangla | -50.0 | 2 | 0 | 0.5 |
| strict | BanglaMATH | Banglish - English | -25.0 | 2 | 1 | 1.0 |
| secondary | All | Banglish - Bangla | -20.0 | 2 | 0 | 0.5 |
| secondary | All | Banglish - English | -20.0 | 2 | 0 | 0.5 |
| secondary | BanglaMATH | Banglish - Bangla | -25.0 | 1 | 0 | 1.0 |
| secondary | BanglaMATH | Banglish - English | -25.0 | 1 | 0 | 1.0 |

## Same-Slice Model Comparison

| Model | Score | Bangla | Reviewed Banglish | English | Banglish-Bangla |
| --- | --- | ---: | ---: | ---: | ---: |
| Gemini 3.5 Flash | strict | 10/10 | 7/10 | 9/10 | -30.0 pts |
| Gemini 3.5 Flash | secondary | 10/10 | 10/10 | 10/10 | +0.0 pts |
| DeepSeek V4 Flash | strict | 10/10 | 7/10 | 9/10 | -30.0 pts |
| DeepSeek V4 Flash | secondary | 10/10 | 8/10 | 10/10 | -20.0 pts |

## Matched Gemini Delta

| Score | Variant | Delta | Model-only | Gemini-only | p |
| --- | --- | ---: | ---: | ---: | ---: |
| strict | Bangla | +0.0 | 0 | 0 |  |
| strict | Reviewed Banglish | +0.0 | 2 | 2 | 1.0 |
| strict | English | +0.0 | 0 | 0 |  |
| secondary | Bangla | +0.0 | 0 | 0 |  |
| secondary | Reviewed Banglish | -20.0 | 0 | 2 | 0.5 |
| secondary | English | +0.0 | 0 | 0 |  |

## Format And Cost Signals

- Finish reasons: STOP=30.
- Key usage by environment variable name: DEEPSEEK_API_KEY=30.
- Recoverable non-strict rows: 2 total (short_extended_unit=1, short_numeric_only=1).
- Reported input tokens: 2585.
- Reported output tokens: 60.
- Reported reasoning tokens: 0.
- Approximate DeepSeek V4 Flash non-thinking pricing checked 2026-06-05 text-token cost: $0.0004.
- Total API wall time summed across requests: 36.1s.

| Variant | Parsed empty | MAX_TOKENS | Long >120 chars | Mean output tokens |
| --- | ---: | ---: | ---: | ---: |
| Bangla | 0 | 0 | 0 | 2.4 |
| Reviewed Banglish | 0 | 0 | 0 | 1.8 |
| English | 0 | 0 | 0 | 1.8 |
