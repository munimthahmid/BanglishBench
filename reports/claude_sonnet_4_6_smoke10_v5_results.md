# Claude Sonnet 4.6 Smoke10 Results

Updated: 2026-06-05

## Scope

This is a 10-item / 30-request smoke gate for Claude Sonnet 4.6 on frozen validation-200 v5 prompts. It checks parser behavior, endpoint compatibility, token/cost behavior, and answer-only compliance before any full validation-200 run.

- Raw API responses: `results/api_audit/claude_sonnet_4_6_smoke10_v5_raw.jsonl`
- Imported strict rows: `results/analysis/claude_sonnet_4_6_smoke10_v5_imported.jsonl`
- Item audit CSV: `results/analysis/claude_sonnet_4_6_smoke10_v5_items.csv`
- Summary CSV: `results/analysis/claude_sonnet_4_6_smoke10_v5_summary.csv`
- Paired gap CSV: `results/analysis/claude_sonnet_4_6_smoke10_v5_paired_gaps.csv`
- Recoverability CSV: `results/analysis/claude_sonnet_4_6_smoke10_v5_recoverability_items.csv`
- Gemini comparison CSV: `results/analysis/claude_sonnet_4_6_smoke10_v5_gemini_comparison.csv`

## Headline

- Strict accuracy on this evaluation scope is 9/10 (90.0%) Bangla, 5/10 (50.0%) reviewed Banglish, and 8/10 (80.0%) English.
- Secondary parser/unit sensitivity is 9/10 (90.0%) Bangla, 5/10 (50.0%) reviewed Banglish, and 9/10 (90.0%) English.
- Against Gemini on the matched Banglish requests, Claude Sonnet 4.6 strict delta is -20.0 points; secondary delta is -50.0 points.

## Accuracy

| Dataset | Score | Bangla | Reviewed Banglish | English |
| --- | --- | ---: | ---: | ---: |
| All | Strict | 9/10 (90.0%) | 5/10 (50.0%) | 8/10 (80.0%) |
| All | Secondary | 9/10 (90.0%) | 5/10 (50.0%) | 9/10 (90.0%) |
| BEnQA | Strict | 6/6 (100.0%) | 3/6 (50.0%) | 5/6 (83.3%) |
| BEnQA | Secondary | 6/6 (100.0%) | 3/6 (50.0%) | 5/6 (83.3%) |
| BanglaMATH | Strict | 3/4 (75.0%) | 2/4 (50.0%) | 3/4 (75.0%) |
| BanglaMATH | Secondary | 3/4 (75.0%) | 2/4 (50.0%) | 4/4 (100.0%) |

## Paired Script Gaps

| Score | Dataset | Comparison | Delta | Left-only | Right-only | p |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| strict | All | Banglish - Bangla | -40.0 | 4 | 0 | 0.125 |
| strict | All | Banglish - English | -30.0 | 4 | 1 | 0.375 |
| strict | BanglaMATH | Banglish - Bangla | -25.0 | 1 | 0 | 1.0 |
| strict | BanglaMATH | Banglish - English | -25.0 | 1 | 0 | 1.0 |
| secondary | All | Banglish - Bangla | -40.0 | 4 | 0 | 0.125 |
| secondary | All | Banglish - English | -40.0 | 5 | 1 | 0.21875 |
| secondary | BanglaMATH | Banglish - Bangla | -25.0 | 1 | 0 | 1.0 |
| secondary | BanglaMATH | Banglish - English | -50.0 | 2 | 0 | 0.5 |

## Same-Slice Model Comparison

| Model | Score | Bangla | Reviewed Banglish | English | Banglish-Bangla |
| --- | --- | ---: | ---: | ---: | ---: |
| Gemini 3.5 Flash | strict | 10/10 | 7/10 | 9/10 | -30.0 pts |
| Gemini 3.5 Flash | secondary | 10/10 | 10/10 | 10/10 | +0.0 pts |
| Claude Sonnet 4.6 | strict | 9/10 | 5/10 | 8/10 | -40.0 pts |
| Claude Sonnet 4.6 | secondary | 9/10 | 5/10 | 9/10 | -40.0 pts |

## Matched Gemini Delta

| Score | Variant | Delta | Model-only | Gemini-only | p |
| --- | --- | ---: | ---: | ---: | ---: |
| strict | Bangla | -10.0 | 0 | 1 | 1.0 |
| strict | Reviewed Banglish | -20.0 | 1 | 3 | 0.625 |
| strict | English | -10.0 | 0 | 1 | 1.0 |
| secondary | Bangla | -10.0 | 0 | 1 | 1.0 |
| secondary | Reviewed Banglish | -50.0 | 0 | 5 | 0.0625 |
| secondary | English | -10.0 | 0 | 1 | 1.0 |

## Format And Cost Signals

- Finish reasons: MAX_TOKENS=4, STOP=26.
- Key usage by environment variable name: ANTHROPIC_API_KEY=30.
- Recoverable non-strict rows: 1 total (short_extended_unit=1).
- Reported input tokens: 3314.
- Reported output tokens: 1027.
- Reported reasoning tokens: 0.
- Approximate Claude Sonnet 4.6 pricing checked 2026-06-05 text-token cost: $0.0253.
- Total API wall time summed across requests: 71.2s.

| Variant | Parsed empty | MAX_TOKENS | Long >120 chars | Mean output tokens |
| --- | ---: | ---: | ---: | ---: |
| Bangla | 0 | 1 | 1 | 37 |
| Reviewed Banglish | 1 | 3 | 4 | 57.1 |
| English | 0 | 0 | 0 | 8.6 |
