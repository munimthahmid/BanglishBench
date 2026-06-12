# Frozen-V5 BEnQA Option-Switching Audit

Updated: 2026-06-11

## Scope

This no-spend audit asks whether reviewed-Banglish BEnQA choices are
a stable reuse of the model's Bangla/English option labels or a
script-conditioned switch pattern. It uses the frozen-v5 BEnQA
choice-bias item table for the three thesis-facing Qwen rows.

- Item table: `results/analysis/v5_benqa_option_switching_items.csv`
- Summary table: `results/analysis/v5_benqa_option_switching_summary.csv`

## Headline

- Qwen3-4B switches valid non-D Bangla predictions to D in reviewed Banglish on 47/73 rows (64.4%).
- The same Qwen3 non-D-to-D switch from English is 55/78 rows (70.5%).
- Qwen2.5 rows are far less D-attracted from Bangla: 14/99 for Qwen2.5-3B and 17/126 for Qwen2.5-7B 8-bit.
- Among correct non-D alternate-script predictions, Qwen3 changes to a wrong D on 30/44 Bangla rows and 37/54 English rows.

## Summary

| Model | Baseline | Same valid option | Valid switches | Non-D->D | D->non-D | Net D shift | Correct non-D->wrong D |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | Bangla | 70/144 | 74/144 | 14/99 | 20/45 | -6 | 6/35 |
| Qwen2.5-3B | English | 63/144 | 81/144 | 16/100 | 21/44 | -5 | 8/48 |
| Qwen2.5-7B 8-bit | Bangla | 63/142 | 79/142 | 17/126 | 10/18 | +7 | 10/54 |
| Qwen2.5-7B 8-bit | English | 57/142 | 85/142 | 18/117 | 20/27 | -2 | 11/69 |
| Qwen3-4B | Bangla | 79/139 | 60/139 | 47/73 | 4/67 | +43 | 30/44 |
| Qwen3-4B | English | 66/136 | 70/136 | 55/78 | 6/58 | +49 | 37/54 |

## Interpretation

- Qwen3 reviewed Banglish does not merely preserve its alternate-script
  choice labels. It sharply converts many non-D Bangla/English choices
  into D while rarely moving D back to another option.
- The Qwen2.5 rows switch options too, but their non-D-to-D rates and
  net D shifts are much smaller. This supports treating the Qwen3
  D-attractor as a script-conditioned failure mode rather than a
  generic BEnQA transition pattern.
- Use this audit beside the choice-bias, option-position/content,
  distractor-transition, and label-balance checks.

## Reproducibility

- Builder: `scripts/analyze_v5_benqa_option_switching.py`
- Item rows: 864
- Summary rows: 36
