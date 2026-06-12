# GPT-5.5 low cap1024 Validation-200 V5 Results

Updated: 2026-06-04

## Scope

This is the full frozen validation-200 v5 frontier-model audit: 200 items x Bangla, reviewed Banglish, and English.
It uses the same strict parser as the open-model and Gemini runs, with secondary parser/unit sensitivity reported separately.

- Raw API responses: `results/api_audit/openai_gpt55_low_validation200_v5_cap1024_raw.jsonl`
- Imported strict rows: `results/analysis/openai_gpt55_low_validation200_v5_cap1024_imported.jsonl`
- Item audit CSV: `results/analysis/openai_gpt55_low_validation200_v5_cap1024_items.csv`
- Summary CSV: `results/analysis/openai_gpt55_low_validation200_v5_cap1024_summary.csv`
- Paired gap CSV: `results/analysis/openai_gpt55_low_validation200_v5_cap1024_paired_gaps.csv`
- Recoverability CSV: `results/analysis/openai_gpt55_low_validation200_v5_cap1024_recoverability_items.csv`
- Gemini comparison CSV: `results/analysis/openai_gpt55_low_validation200_v5_cap1024_gemini_comparison.csv`

## Headline

- Strict accuracy on this evaluation scope is 172/200 (86.0%) Bangla, 169/200 (84.5%) reviewed Banglish, and 154/200 (77.0%) English.
- Secondary parser/unit sensitivity is 173/200 (86.5%) Bangla, 174/200 (87.0%) reviewed Banglish, and 168/200 (84.0%) English.
- Against Gemini on the matched Banglish requests, GPT-5.5 low cap1024 strict delta is +16.5 points; secondary delta is +6.5 points.

## Accuracy

| Dataset | Score | Bangla | Reviewed Banglish | English |
| --- | --- | ---: | ---: | ---: |
| All | Strict | 172/200 (86.0%) | 169/200 (84.5%) | 154/200 (77.0%) |
| All | Secondary | 173/200 (86.5%) | 174/200 (87.0%) | 168/200 (84.0%) |
| BEnQA | Strict | 134/144 (93.1%) | 134/144 (93.1%) | 131/144 (91.0%) |
| BEnQA | Secondary | 134/144 (93.1%) | 134/144 (93.1%) | 131/144 (91.0%) |
| BanglaMATH | Strict | 38/56 (67.9%) | 35/56 (62.5%) | 23/56 (41.1%) |
| BanglaMATH | Secondary | 39/56 (69.6%) | 40/56 (71.4%) | 37/56 (66.1%) |

## Paired Script Gaps

| Score | Dataset | Comparison | Delta | Left-only | Right-only | p |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| strict | All | Banglish - Bangla | -1.5 | 6 | 3 | 0.507812 |
| strict | All | Banglish - English | +7.5 | 6 | 21 | 0.005925 |
| strict | BanglaMATH | Banglish - Bangla | -5.4 | 4 | 1 | 0.375 |
| strict | BanglaMATH | Banglish - English | +21.4 | 1 | 13 | 0.001831 |
| secondary | All | Banglish - Bangla | +0.5 | 2 | 3 | 1.0 |
| secondary | All | Banglish - English | +3.0 | 5 | 11 | 0.210114 |
| secondary | BanglaMATH | Banglish - Bangla | +1.8 | 0 | 1 | 1.0 |
| secondary | BanglaMATH | Banglish - English | +5.4 | 0 | 3 | 0.25 |

## Same-Slice Model Comparison

| Model | Score | Bangla | Reviewed Banglish | English | Banglish-Bangla |
| --- | --- | ---: | ---: | ---: | ---: |
| Gemini 3.5 Flash | strict | 163/200 | 136/200 | 144/200 | -13.5 pts |
| Gemini 3.5 Flash | secondary | 170/200 | 161/200 | 165/200 | -4.5 pts |
| GPT-5.5 low cap1024 | strict | 172/200 | 169/200 | 154/200 | -1.5 pts |
| GPT-5.5 low cap1024 | secondary | 173/200 | 174/200 | 168/200 | +0.5 pts |

## Matched Gemini Delta

| Score | Variant | Delta | Model-only | Gemini-only | p |
| --- | --- | ---: | ---: | ---: | ---: |
| strict | Bangla | +4.5 | 14 | 5 | 0.063568 |
| strict | Reviewed Banglish | +16.5 | 37 | 4 | 1.03e-07 |
| strict | English | +5.0 | 15 | 5 | 0.041389 |
| secondary | Bangla | +1.5 | 8 | 5 | 0.581055 |
| secondary | Reviewed Banglish | +6.5 | 16 | 3 | 0.004425 |
| secondary | English | +1.5 | 8 | 5 | 0.581055 |

## Format And Cost Signals

- Finish reasons: STOP=600.
- Key usage by environment variable name: OPENAI_API_KEY=600.
- Recoverable non-strict rows: 20 total (short_extended_unit=8, short_numeric_only=12).
- Reported input tokens: 59852.
- Reported output tokens: 59270.
- Reported reasoning tokens: 53632.
- Approximate standard GPT-5.5 text-token cost: $2.0774.
- Total API wall time summed across requests: 2581.5s.

| Variant | Parsed empty | MAX_TOKENS | Long >120 chars | Mean output tokens |
| --- | ---: | ---: | ---: | ---: |
| Bangla | 0 | 0 | 2 | 93.4 |
| Reviewed Banglish | 0 | 0 | 2 | 113.0 |
| English | 0 | 0 | 2 | 90.0 |
