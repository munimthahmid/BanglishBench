# Claude Sonnet 4.6 Validation-200 v5 Results

Updated: 2026-06-05

## Scope

This is a full validation-200 v5 Anthropic frontier API audit for Claude Sonnet 4.6 with a 1024 output-token cap. It uses the frozen provider-neutral prompt manifest, the same strict parser as open-model runs, and secondary parser/unit sensitivity for recoverable noncanonical answers.

- Raw API responses: `results/api_audit/claude_sonnet_4_6_validation200_v5_cap1024_raw.jsonl`
- Imported strict rows: `results/analysis/claude_sonnet_4_6_validation200_v5_cap1024_imported.jsonl`
- Item audit CSV: `results/analysis/claude_sonnet_4_6_validation200_v5_cap1024_items.csv`
- Summary CSV: `results/analysis/claude_sonnet_4_6_validation200_v5_cap1024_summary.csv`
- Paired gap CSV: `results/analysis/claude_sonnet_4_6_validation200_v5_cap1024_paired_gaps.csv`
- Recoverability CSV: `results/analysis/claude_sonnet_4_6_validation200_v5_cap1024_recoverability_items.csv`
- Gemini comparison CSV: `results/analysis/claude_sonnet_4_6_validation200_v5_cap1024_gemini_comparison.csv`

## Headline

- Strict accuracy on this evaluation scope is 162/200 (81.0%) Bangla, 130/200 (65.0%) reviewed Banglish, and 153/200 (76.5%) English.
- Secondary parser/unit sensitivity is 167/200 (83.5%) Bangla, 133/200 (66.5%) reviewed Banglish, and 166/200 (83.0%) English.
- Against Gemini on the matched Banglish requests, Claude Sonnet 4.6 strict delta is -3.0 points; secondary delta is -14.0 points.

## Accuracy

| Dataset | Score | Bangla | Reviewed Banglish | English |
| --- | --- | ---: | ---: | ---: |
| All | Strict | 162/200 (81.0%) | 130/200 (65.0%) | 153/200 (76.5%) |
| All | Secondary | 167/200 (83.5%) | 133/200 (66.5%) | 166/200 (83.0%) |
| BEnQA | Strict | 128/144 (88.9%) | 96/144 (66.7%) | 130/144 (90.3%) |
| BEnQA | Secondary | 129/144 (89.6%) | 96/144 (66.7%) | 131/144 (91.0%) |
| BanglaMATH | Strict | 34/56 (60.7%) | 34/56 (60.7%) | 23/56 (41.1%) |
| BanglaMATH | Secondary | 38/56 (67.9%) | 37/56 (66.1%) | 35/56 (62.5%) |

## Paired Script Gaps

| Score | Dataset | Comparison | Delta | Left-only | Right-only | p |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| strict | All | Banglish - Bangla | -16.0 | 39 | 7 | 2e-06 |
| strict | All | Banglish - English | -11.5 | 44 | 21 | 0.005918 |
| strict | BanglaMATH | Banglish - Bangla | +0.0 | 3 | 3 | 1.0 |
| strict | BanglaMATH | Banglish - English | +19.6 | 2 | 13 | 0.007385 |
| secondary | All | Banglish - Bangla | -17.0 | 40 | 6 | 3.1e-07 |
| secondary | All | Banglish - English | -16.5 | 46 | 13 | 1.9e-05 |
| secondary | BanglaMATH | Banglish - Bangla | -1.8 | 3 | 2 | 1.0 |
| secondary | BanglaMATH | Banglish - English | +3.6 | 3 | 5 | 0.726562 |

## Same-Slice Model Comparison

| Model | Score | Bangla | Reviewed Banglish | English | Banglish-Bangla |
| --- | --- | ---: | ---: | ---: | ---: |
| Gemini 3.5 Flash | strict | 163/200 | 136/200 | 144/200 | -13.5 pts |
| Gemini 3.5 Flash | secondary | 170/200 | 161/200 | 165/200 | -4.5 pts |
| Claude Sonnet 4.6 | strict | 162/200 | 130/200 | 153/200 | -16.0 pts |
| Claude Sonnet 4.6 | secondary | 167/200 | 133/200 | 166/200 | -17.0 pts |

## Matched Gemini Delta

| Score | Variant | Delta | Model-only | Gemini-only | p |
| --- | --- | ---: | ---: | ---: | ---: |
| strict | Bangla | -0.5 | 12 | 13 | 1.0 |
| strict | Reviewed Banglish | -3.0 | 34 | 40 | 0.561381 |
| strict | English | +4.5 | 15 | 6 | 0.078354 |
| secondary | Bangla | -1.5 | 7 | 10 | 0.629059 |
| secondary | Reviewed Banglish | -14.0 | 12 | 40 | 0.000128 |
| secondary | English | +0.5 | 8 | 7 | 1.0 |

## Format And Cost Signals

- Finish reasons: MAX_TOKENS=2, STOP=598.
- Key usage by environment variable name: ANTHROPIC_API_KEY=600.
- Recoverable non-strict rows: 21 total (choice_markdown_recovery=2, short_extended_unit=9, short_numeric_only=10).
- Reported input tokens: 70903.
- Reported output tokens: 51324.
- Reported reasoning tokens: 0.
- Approximate Claude Sonnet 4.6 pricing checked 2026-06-05 text-token cost: $0.9826.
- Total API wall time summed across requests: 1862.0s.

| Variant | Parsed empty | MAX_TOKENS | Long >120 chars | Mean output tokens |
| --- | ---: | ---: | ---: | ---: |
| Bangla | 1 | 1 | 69 | 94.6 |
| Reviewed Banglish | 1 | 0 | 88 | 101.1 |
| English | 1 | 1 | 46 | 60.9 |
