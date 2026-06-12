# GPT-5.5 low cap1024 Diagnostic Results

Updated: 2026-06-04

## Scope

This is a targeted frontier-model diagnostic slice, not the final full SOTA
audit. It uses the same strict parser as the open-model and Gemini runs,
with secondary parser/unit sensitivity reported separately.

- Raw API responses: `results/api_audit/openai_gpt55_low_diagnostic_60_v5_cap1024_raw.jsonl`
- Imported strict rows: `results/analysis/openai_gpt55_low_diagnostic_60_v5_cap1024_imported.jsonl`
- Item audit CSV: `results/analysis/openai_gpt55_low_diagnostic_60_v5_cap1024_items.csv`
- Summary CSV: `results/analysis/openai_gpt55_low_diagnostic_60_v5_cap1024_summary.csv`
- Paired gap CSV: `results/analysis/openai_gpt55_low_diagnostic_60_v5_cap1024_paired_gaps.csv`
- Recoverability CSV: `results/analysis/openai_gpt55_low_diagnostic_60_v5_cap1024_recoverability_items.csv`
- Gemini comparison CSV: `results/analysis/openai_gpt55_low_diagnostic_60_v5_cap1024_gemini_comparison.csv`

## Headline

- Strict accuracy on the diagnostic slice is 44/60 (73.3%) Bangla, 42/60 (70.0%) reviewed Banglish, and 30/60 (50.0%) English.
- Secondary parser/unit sensitivity is 45/60 (75.0%) Bangla, 48/60 (80.0%) reviewed Banglish, and 44/60 (73.3%) English.
- Against Gemini on the same selected Banglish requests, GPT-5.5 low cap1024 strict delta is +60.0 points; secondary delta is +28.3 points.

## Accuracy

| Dataset | Score | Bangla | Reviewed Banglish | English |
| --- | --- | ---: | ---: | ---: |
| All | Strict | 44/60 (73.3%) | 42/60 (70.0%) | 30/60 (50.0%) |
| All | Secondary | 45/60 (75.0%) | 48/60 (80.0%) | 44/60 (73.3%) |
| BEnQA | Strict | 12/20 (60.0%) | 14/20 (70.0%) | 13/20 (65.0%) |
| BEnQA | Secondary | 12/20 (60.0%) | 14/20 (70.0%) | 13/20 (65.0%) |
| BanglaMATH | Strict | 32/40 (80.0%) | 28/40 (70.0%) | 17/40 (42.5%) |
| BanglaMATH | Secondary | 33/40 (82.5%) | 34/40 (85.0%) | 31/40 (77.5%) |

## Paired Script Gaps

| Score | Dataset | Comparison | Delta | Left-only | Right-only | p |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| strict | All | Banglish - Bangla | -3.3 | 5 | 3 | 0.726562 |
| strict | All | Banglish - English | +20.0 | 3 | 15 | 0.007538 |
| strict | BanglaMATH | Banglish - Bangla | -10.0 | 5 | 1 | 0.21875 |
| strict | BanglaMATH | Banglish - English | +27.5 | 0 | 11 | 0.000977 |
| secondary | All | Banglish - Bangla | +5.0 | 0 | 3 | 0.25 |
| secondary | All | Banglish - English | +6.7 | 3 | 7 | 0.34375 |
| secondary | BanglaMATH | Banglish - Bangla | +2.5 | 0 | 1 | 1.0 |
| secondary | BanglaMATH | Banglish - English | +7.5 | 0 | 3 | 0.25 |

## Same-Slice Model Comparison

| Model | Score | Bangla | Reviewed Banglish | English | Banglish-Bangla |
| --- | --- | ---: | ---: | ---: | ---: |
| Gemini 3.5 Flash | strict | 37/60 | 6/60 | 23/60 | -51.7 pts |
| Gemini 3.5 Flash | secondary | 43/60 | 31/60 | 42/60 | -20.0 pts |
| GPT-5.5 low cap1024 | strict | 44/60 | 42/60 | 30/60 | -3.3 pts |
| GPT-5.5 low cap1024 | secondary | 45/60 | 48/60 | 44/60 | +5.0 pts |

## Matched Gemini Delta

| Score | Variant | Delta | Model-only | Gemini-only | p |
| --- | --- | ---: | ---: | ---: | ---: |
| strict | Bangla | +11.7 | 11 | 4 | 0.118469 |
| strict | Reviewed Banglish | +60.0 | 36 | 0 | 2.91e-11 |
| strict | English | +11.7 | 9 | 2 | 0.06543 |
| secondary | Bangla | +3.3 | 6 | 4 | 0.753906 |
| secondary | Reviewed Banglish | +28.3 | 17 | 0 | 1.5e-05 |
| secondary | English | +3.3 | 4 | 2 | 0.6875 |

## Format And Cost Signals

- Finish reasons: STOP=180.
- Key usage by environment variable name: OPENAI_API_KEY=180.
- Recoverable non-strict rows: 21 total (short_extended_unit=8, short_numeric_only=13).
- Reported input tokens: 14566.
- Reported output tokens: 18844.
- Reported reasoning tokens: 17207.
- Approximate standard GPT-5.5 text-token cost: $0.6381.
- Total API wall time summed across requests: 769.7s.

| Variant | Parsed empty | MAX_TOKENS | Long >120 chars | Mean output tokens |
| --- | ---: | ---: | ---: | ---: |
| Bangla | 0 | 0 | 0 | 107.0 |
| Reviewed Banglish | 0 | 0 | 0 | 117.8 |
| English | 0 | 0 | 0 | 89.3 |
