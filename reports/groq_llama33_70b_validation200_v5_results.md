# Groq Llama 3.3 70B Validation-200 v5 Results

Updated: 2026-06-05

## Scope

This is a full validation-200 v5 frontier/hosted-open API audit for Groq-hosted Llama 3.3 70B Versatile. It uses the frozen provider-neutral prompt manifest, the same strict parser as open-model runs, and secondary parser/unit sensitivity for recoverable noncanonical answers.

- Raw API responses: `results/api_audit/groq_llama33_70b_validation200_v5_raw.jsonl`
- Imported strict rows: `results/analysis/groq_llama33_70b_validation200_v5_imported.jsonl`
- Item audit CSV: `results/analysis/groq_llama33_70b_validation200_v5_items.csv`
- Summary CSV: `results/analysis/groq_llama33_70b_validation200_v5_summary.csv`
- Paired gap CSV: `results/analysis/groq_llama33_70b_validation200_v5_paired_gaps.csv`
- Recoverability CSV: `results/analysis/groq_llama33_70b_validation200_v5_recoverability_items.csv`
- Gemini comparison CSV: `results/analysis/groq_llama33_70b_validation200_v5_gemini_comparison.csv`

## Headline

- Strict accuracy on this evaluation scope is 90/200 (45.0%) Bangla, 48/200 (24.0%) reviewed Banglish, and 102/200 (51.0%) English.
- Secondary parser/unit sensitivity is 92/200 (46.0%) Bangla, 56/200 (28.0%) reviewed Banglish, and 111/200 (55.5%) English.
- Against Gemini on the matched Banglish requests, Groq Llama 3.3 70B Versatile strict delta is -44.0 points; secondary delta is -52.5 points.

## Accuracy

| Dataset | Score | Bangla | Reviewed Banglish | English |
| --- | --- | ---: | ---: | ---: |
| All | Strict | 90/200 (45.0%) | 48/200 (24.0%) | 102/200 (51.0%) |
| All | Secondary | 92/200 (46.0%) | 56/200 (28.0%) | 111/200 (55.5%) |
| BEnQA | Strict | 72/144 (50.0%) | 48/144 (33.3%) | 88/144 (61.1%) |
| BEnQA | Secondary | 72/144 (50.0%) | 48/144 (33.3%) | 88/144 (61.1%) |
| BanglaMATH | Strict | 18/56 (32.1%) | 0/56 (0.0%) | 14/56 (25.0%) |
| BanglaMATH | Secondary | 20/56 (35.7%) | 8/56 (14.3%) | 23/56 (41.1%) |

## Paired Script Gaps

| Score | Dataset | Comparison | Delta | Left-only | Right-only | p |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| strict | All | Banglish - Bangla | -21.0 | 56 | 14 | 4.3e-07 |
| strict | All | Banglish - English | -27.0 | 69 | 15 | 1.94e-09 |
| strict | BanglaMATH | Banglish - Bangla | -32.1 | 18 | 0 | 8e-06 |
| strict | BanglaMATH | Banglish - English | -25.0 | 14 | 0 | 0.000122 |
| secondary | All | Banglish - Bangla | -18.0 | 52 | 16 | 1.4e-05 |
| secondary | All | Banglish - English | -27.5 | 70 | 15 | 1.17e-09 |
| secondary | BanglaMATH | Banglish - Bangla | -21.4 | 14 | 2 | 0.004181 |
| secondary | BanglaMATH | Banglish - English | -26.8 | 15 | 0 | 6.1e-05 |

## Same-Slice Model Comparison

| Model | Score | Bangla | Reviewed Banglish | English | Banglish-Bangla |
| --- | --- | ---: | ---: | ---: | ---: |
| Gemini 3.5 Flash | strict | 163/200 | 136/200 | 144/200 | -13.5 pts |
| Gemini 3.5 Flash | secondary | 170/200 | 161/200 | 165/200 | -4.5 pts |
| Groq Llama 3.3 70B Versatile | strict | 90/200 | 48/200 | 102/200 | -21.0 pts |
| Groq Llama 3.3 70B Versatile | secondary | 92/200 | 56/200 | 111/200 | -18.0 pts |

## Matched Gemini Delta

| Score | Variant | Delta | Model-only | Gemini-only | p |
| --- | --- | ---: | ---: | ---: | ---: |
| strict | Bangla | -36.5 | 4 | 77 | 2.91e-16 |
| strict | Reviewed Banglish | -44.0 | 6 | 94 | 1.91e-15 |
| strict | English | -21.0 | 6 | 48 | 3.26e-09 |
| secondary | Bangla | -39.0 | 3 | 81 | 5.14e-16 |
| secondary | Reviewed Banglish | -52.5 | 3 | 108 | 1.24e-15 |
| secondary | English | -27.0 | 2 | 56 | 1.19e-14 |

## Format And Cost Signals

- Finish reasons: MAX_TOKENS=24, STOP=576.
- Key usage by environment variable name: GROQ_API_KEY=600.
- Recoverable non-strict rows: 19 total (short_extended_unit=3, short_numeric_only=16).
- Reported input tokens: 88321.
- Reported output tokens: 7361.
- Reported reasoning tokens: 0.
- Approximate Groq Llama 3.3 70B pricing checked 2026-06-05 text-token cost: $0.0579.
- Total API wall time summed across requests: 341.2s.

| Variant | Parsed empty | MAX_TOKENS | Long >120 chars | Mean output tokens |
| --- | ---: | ---: | ---: | ---: |
| Bangla | 0 | 12 | 1 | 16.5 |
| Reviewed Banglish | 0 | 1 | 2 | 5.1 |
| English | 1 | 11 | 22 | 15.3 |
