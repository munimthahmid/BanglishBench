# Groq Llama 3.3 70B Smoke10 Results

Updated: 2026-06-05

## Scope

This is a 10-item / 30-request smoke gate for Groq-hosted Llama 3.3 70B Versatile on frozen validation-200 v5 prompts. It checks parser behavior, endpoint compatibility, and token/cost behavior before the full validation-200 run.

- Raw API responses: `results/api_audit/groq_llama33_70b_smoke10_v5_raw.jsonl`
- Imported strict rows: `results/analysis/groq_llama33_70b_smoke10_v5_imported.jsonl`
- Item audit CSV: `results/analysis/groq_llama33_70b_smoke10_v5_items.csv`
- Summary CSV: `results/analysis/groq_llama33_70b_smoke10_v5_summary.csv`
- Paired gap CSV: `results/analysis/groq_llama33_70b_smoke10_v5_paired_gaps.csv`
- Recoverability CSV: `results/analysis/groq_llama33_70b_smoke10_v5_recoverability_items.csv`
- Gemini comparison CSV: `results/analysis/groq_llama33_70b_smoke10_v5_gemini_comparison.csv`

## Headline

- Strict accuracy on this evaluation scope is 7/10 (70.0%) Bangla, 1/10 (10.0%) reviewed Banglish, and 7/10 (70.0%) English.
- Secondary parser/unit sensitivity is 7/10 (70.0%) Bangla, 2/10 (20.0%) reviewed Banglish, and 9/10 (90.0%) English.
- Against Gemini on the matched Banglish requests, Groq Llama 3.3 70B Versatile strict delta is -60.0 points; secondary delta is -80.0 points.

## Accuracy

| Dataset | Score | Bangla | Reviewed Banglish | English |
| --- | --- | ---: | ---: | ---: |
| All | Strict | 7/10 (70.0%) | 1/10 (10.0%) | 7/10 (70.0%) |
| All | Secondary | 7/10 (70.0%) | 2/10 (20.0%) | 9/10 (90.0%) |
| BEnQA | Strict | 4/6 (66.7%) | 1/6 (16.7%) | 6/6 (100.0%) |
| BEnQA | Secondary | 4/6 (66.7%) | 1/6 (16.7%) | 6/6 (100.0%) |
| BanglaMATH | Strict | 3/4 (75.0%) | 0/4 (0.0%) | 1/4 (25.0%) |
| BanglaMATH | Secondary | 3/4 (75.0%) | 1/4 (25.0%) | 3/4 (75.0%) |

## Paired Script Gaps

| Score | Dataset | Comparison | Delta | Left-only | Right-only | p |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| strict | All | Banglish - Bangla | -60.0 | 7 | 1 | 0.070312 |
| strict | All | Banglish - English | -60.0 | 6 | 0 | 0.03125 |
| strict | BanglaMATH | Banglish - Bangla | -75.0 | 3 | 0 | 0.25 |
| strict | BanglaMATH | Banglish - English | -25.0 | 1 | 0 | 1.0 |
| secondary | All | Banglish - Bangla | -50.0 | 6 | 1 | 0.125 |
| secondary | All | Banglish - English | -70.0 | 7 | 0 | 0.015625 |
| secondary | BanglaMATH | Banglish - Bangla | -50.0 | 2 | 0 | 0.5 |
| secondary | BanglaMATH | Banglish - English | -50.0 | 2 | 0 | 0.5 |

## Same-Slice Model Comparison

| Model | Score | Bangla | Reviewed Banglish | English | Banglish-Bangla |
| --- | --- | ---: | ---: | ---: | ---: |
| Gemini 3.5 Flash | strict | 10/10 | 7/10 | 9/10 | -30.0 pts |
| Gemini 3.5 Flash | secondary | 10/10 | 10/10 | 10/10 | +0.0 pts |
| Groq Llama 3.3 70B Versatile | strict | 7/10 | 1/10 | 7/10 | -60.0 pts |
| Groq Llama 3.3 70B Versatile | secondary | 7/10 | 2/10 | 9/10 | -50.0 pts |

## Matched Gemini Delta

| Score | Variant | Delta | Model-only | Gemini-only | p |
| --- | --- | ---: | ---: | ---: | ---: |
| strict | Bangla | -30.0 | 0 | 3 | 0.25 |
| strict | Reviewed Banglish | -60.0 | 0 | 6 | 0.03125 |
| strict | English | -20.0 | 0 | 2 | 0.5 |
| secondary | Bangla | -30.0 | 0 | 3 | 0.25 |
| secondary | Reviewed Banglish | -80.0 | 0 | 8 | 0.007812 |
| secondary | English | -10.0 | 0 | 1 | 1.0 |

## Format And Cost Signals

- Finish reasons: STOP=30.
- Key usage by environment variable name: GROQ_API_KEY=30.
- Recoverable non-strict rows: 3 total (short_extended_unit=1, short_numeric_only=2).
- Reported input tokens: 4100.
- Reported output tokens: 86.
- Reported reasoning tokens: 0.
- Approximate Groq Llama 3.3 70B pricing checked 2026-06-05 text-token cost: $0.0025.
- Total API wall time summed across requests: 13.1s.

| Variant | Parsed empty | MAX_TOKENS | Long >120 chars | Mean output tokens |
| --- | ---: | ---: | ---: | ---: |
| Bangla | 0 | 0 | 0 | 3.9 |
| Reviewed Banglish | 0 | 0 | 0 | 2.3 |
| English | 0 | 0 | 0 | 2.4 |
