# DeepSeek V4 Flash Smoke3 Results

Updated: 2026-06-05

## Scope

This is a 3-request endpoint smoke on the first validation smoke item only. It verifies API compatibility before the 30-request smoke and is not a population estimate.

- Raw API responses: `results/api_audit/deepseek_v4_flash_smoke3_v5_raw.jsonl`
- Imported strict rows: `results/analysis/deepseek_v4_flash_smoke3_v5_imported.jsonl`
- Item audit CSV: `results/analysis/deepseek_v4_flash_smoke3_v5_items.csv`
- Summary CSV: `results/analysis/deepseek_v4_flash_smoke3_v5_summary.csv`
- Paired gap CSV: `results/analysis/deepseek_v4_flash_smoke3_v5_paired_gaps.csv`
- Recoverability CSV: `results/analysis/deepseek_v4_flash_smoke3_v5_recoverability_items.csv`
- Gemini comparison CSV: `results/analysis/deepseek_v4_flash_smoke3_v5_gemini_comparison.csv`

## Headline

- Strict accuracy on this evaluation scope is 1/1 (100.0%) Bangla, 1/1 (100.0%) reviewed Banglish, and 1/1 (100.0%) English.
- Secondary parser/unit sensitivity is 1/1 (100.0%) Bangla, 1/1 (100.0%) reviewed Banglish, and 1/1 (100.0%) English.
- Against Gemini on the matched Banglish requests, DeepSeek V4 Flash strict delta is +0.0 points; secondary delta is +0.0 points.

## Accuracy

| Dataset | Score | Bangla | Reviewed Banglish | English |
| --- | --- | ---: | ---: | ---: |
| All | Strict | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| All | Secondary | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| BEnQA | Strict | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |
| BEnQA | Secondary | 1/1 (100.0%) | 1/1 (100.0%) | 1/1 (100.0%) |

## Paired Script Gaps

| Score | Dataset | Comparison | Delta | Left-only | Right-only | p |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| strict | All | Banglish - Bangla | +0.0 | 0 | 0 |  |
| strict | All | Banglish - English | +0.0 | 0 | 0 |  |
| strict | BanglaMATH | Banglish - Bangla | +0.0 | 0 | 0 |  |
| strict | BanglaMATH | Banglish - English | +0.0 | 0 | 0 |  |
| secondary | All | Banglish - Bangla | +0.0 | 0 | 0 |  |
| secondary | All | Banglish - English | +0.0 | 0 | 0 |  |
| secondary | BanglaMATH | Banglish - Bangla | +0.0 | 0 | 0 |  |
| secondary | BanglaMATH | Banglish - English | +0.0 | 0 | 0 |  |

## Same-Slice Model Comparison

| Model | Score | Bangla | Reviewed Banglish | English | Banglish-Bangla |
| --- | --- | ---: | ---: | ---: | ---: |
| Gemini 3.5 Flash | strict | 1/1 | 1/1 | 1/1 | +0.0 pts |
| Gemini 3.5 Flash | secondary | 1/1 | 1/1 | 1/1 | +0.0 pts |
| DeepSeek V4 Flash | strict | 1/1 | 1/1 | 1/1 | +0.0 pts |
| DeepSeek V4 Flash | secondary | 1/1 | 1/1 | 1/1 | +0.0 pts |

## Matched Gemini Delta

| Score | Variant | Delta | Model-only | Gemini-only | p |
| --- | --- | ---: | ---: | ---: | ---: |
| strict | Bangla | +0.0 | 0 | 0 |  |
| strict | Reviewed Banglish | +0.0 | 0 | 0 |  |
| strict | English | +0.0 | 0 | 0 |  |
| secondary | Bangla | +0.0 | 0 | 0 |  |
| secondary | Reviewed Banglish | +0.0 | 0 | 0 |  |
| secondary | English | +0.0 | 0 | 0 |  |

## Format And Cost Signals

- Finish reasons: STOP=3.
- Key usage by environment variable name: DEEPSEEK_API_KEY=3.
- Recoverable non-strict rows: 0 total ().
- Reported input tokens: 235.
- Reported output tokens: 3.
- Reported reasoning tokens: 0.
- Approximate DeepSeek V4 Flash non-thinking pricing checked 2026-06-05 text-token cost: $0.0000.
- Total API wall time summed across requests: 4.6s.

| Variant | Parsed empty | MAX_TOKENS | Long >120 chars | Mean output tokens |
| --- | ---: | ---: | ---: | ---: |
| Bangla | 0 | 0 | 0 | 1 |
| Reviewed Banglish | 0 | 0 | 0 | 1 |
| English | 0 | 0 | 0 | 1 |
