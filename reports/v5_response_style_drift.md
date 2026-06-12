# Frozen-V5 Response-Style Drift Audit

Updated: 2026-06-11

## Scope

This no-spend audit checks raw model responses, not just parsed correctness.
It asks whether reviewed Banglish changes response style: verbosity,
script of the output, and meta/uncertainty language such as `cannot`,
`unclear`, or `appears`. It uses the same thesis-facing frozen-v5 Qwen
rows as the main table.

- Item-level output: `results/analysis/v5_response_style_drift_items.csv`
- Summary table: `results/analysis/v5_response_style_drift_summary.csv`

This is behavioral failure analysis. It is not a causal mechanism, and it
does not replace correctness, parser, or answer-format audits.

## Headline

- Qwen3-4B BanglaMATH reviewed Banglish has 15/56
  meta/uncertainty outputs, versus 0/56
  for Bangla and 1/56 for English.
- Qwen3-4B is verbose on BanglaMATH across scripts, but reviewed Banglish
  is the clearest meta-confusion case: mean raw length 238.9
  chars and 39/56 outputs over 120 chars.
- Qwen2.5 rows do not show the same BanglaMATH meta pattern:
  Qwen2.5-3B reviewed Banglish has 1/56
  meta outputs and Qwen2.5-7B has 0/56.
- Therefore response-style drift is a model-specific failure mode, not a
  complete explanation of the Banglish gap.

## BanglaMATH Response Style

| Model | Variant | Correct | Meta/uncertainty | Wrong meta | Long >120 chars | Mean raw chars | Bengali output | Latin output | Mixed output |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | Bangla | 5/56 | 0/56 | 0/51 | 2/56 | 15.5 | 9 | 15 | 0 |
| Qwen2.5-3B | Reviewed Banglish | 0/56 | 1/56 | 1/56 | 3/56 | 29.6 | 0 | 25 | 0 |
| Qwen2.5-3B | English | 5/56 | 0/56 | 0/51 | 4/56 | 35.0 | 0 | 34 | 0 |
| Qwen2.5-7B 8-bit | Bangla | 5/56 | 0/56 | 0/51 | 1/56 | 12.3 | 18 | 5 | 2 |
| Qwen2.5-7B 8-bit | Reviewed Banglish | 0/56 | 0/56 | 0/56 | 0/56 | 7.4 | 1 | 7 | 0 |
| Qwen2.5-7B 8-bit | English | 8/56 | 1/56 | 1/48 | 1/56 | 17.3 | 0 | 24 | 0 |
| Qwen3-4B | Bangla | 4/56 | 0/56 | 0/52 | 42/56 | 132.2 | 52 | 16 | 13 |
| Qwen3-4B | Reviewed Banglish | 2/56 | 15/56 | 15/54 | 39/56 | 238.9 | 6 | 50 | 4 |
| Qwen3-4B | English | 6/56 | 1/56 | 1/50 | 48/56 | 274.2 | 0 | 54 | 0 |

## All-200 Summary

| Model | Variant | Correct | Meta/uncertainty | Long >120 chars | Mean raw chars |
| --- | --- | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | Bangla | 54/200 | 0/200 | 2/200 | 5.0 |
| Qwen2.5-3B | Reviewed Banglish | 41/200 | 1/200 | 3/200 | 9.0 |
| Qwen2.5-3B | English | 71/200 | 0/200 | 4/200 | 10.5 |
| Qwen2.5-7B 8-bit | Bangla | 65/200 | 0/200 | 1/200 | 4.2 |
| Qwen2.5-7B 8-bit | Reviewed Banglish | 47/200 | 0/200 | 2/200 | 7.1 |
| Qwen2.5-7B 8-bit | English | 94/200 | 1/200 | 1/200 | 5.6 |
| Qwen3-4B | Bangla | 80/200 | 0/200 | 48/200 | 46.2 |
| Qwen3-4B | Reviewed Banglish | 49/200 | 15/200 | 42/200 | 72.2 |
| Qwen3-4B | English | 88/200 | 1/200 | 62/200 | 102.7 |

## Qwen3 BanglaMATH Banglish Meta Examples

| Item | Gold | Parsed | Raw excerpt |
| --- | --- | --- | --- |
| `banglamath_0182` | `৬০০ টাকা` | `cannot be derived.` | The given text appears to be in a mix of Bengali and possibly a typo or miscommunication. It seems to be trying to express a calculation or comparison involving "keji chaler" (p... |
| `banglamath_0227` | `৭.৫ কিমি` | `.` | The question appears to be in a mix of Bengali and English, and it seems to be asking about a sequence or pattern involving "bondhur durotto" (likely meaning "bondhur" or "pair"... |
| `banglamath_0553` | `১১২৫টি` | `The given statement is in Bengali and...` | The given statement is in Bengali and appears to be a question or statement about agricultural land and the number of ploughs (pathor) required. However, the sentence is grammat... |
| `banglamath_0542` | `৩৪০০ টাকা` | `2. Cost per square mile = 25 taka` | The question appears to be in a mix of Bengali and English, and it seems to be asking for the cost of a certain area (likely a rectangular plot) at a rate of 25 taka per square... |
| `banglamath_0230` | `20%` | `.` | The question "25 taka 125 takar shotkora koto" appears to be in a mix of Bengali and possibly a typo or misphrasing. "Taka" is the currency unit in Bangladesh, and "takar" might... |

## Interpretation

- BEnQA MCQ outputs are mostly one-letter answers, so response-style drift is
  not the main BEnQA parser explanation; choice-bias and distractor audits
  are the better BEnQA failure-analysis sources.
- BanglaMATH has low accuracy across scripts, but Qwen3 reviewed Banglish
  often elicits meta/uncertainty prose instead of a direct short answer.
- This supports the broader robustness framing: script choice can alter not
  only correctness but also answer behavior. Because Qwen2.5 does not show
  the same meta pattern, keep the claim model-specific.

## Reproducibility

- Builder: `scripts/analyze_v5_response_style_drift.py`
- Item rows: 1800
- Summary rows: 27
- Meta/uncertainty detection is regex-based and intentionally conservative.
