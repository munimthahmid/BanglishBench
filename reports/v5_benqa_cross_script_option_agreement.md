# Frozen-V5 BEnQA Cross-Script Option-Agreement Audit

Updated: 2026-06-11

## Scope

This no-spend audit asks what reviewed Banglish does when the same
model's Bangla and English BEnQA predictions agree on an option label.
The strongest slice is where Bangla and English are both correct and
agree on the same non-D option. It uses only the frozen-v5 BEnQA
choice-bias item table.

- Item table: `results/analysis/v5_benqa_cross_script_option_agreement_items.csv`
- Summary table: `results/analysis/v5_benqa_cross_script_option_agreement_summary.csv`

## Headline

- When Qwen3-4B Bangla and English are both correct and agree on the same non-D option, reviewed Banglish still switches to wrong D on 23/36 rows (63.9%).
- The corresponding Qwen2.5 wrong-D rates are 2/23 and 7/44.
- In the broader Qwen3 Bangla-English non-D agreement slice, reviewed Banglish predicts D on 30/47 rows.
- Across all Qwen3 rows where Bangla and English agree, reviewed Banglish predicts D on 72/92 rows.
- When Bangla and English are both correct and agree on D, Qwen3 reviewed Banglish keeps D on 23/25 rows.

## Summary

| Model | Scope | N | Banglish correct | Banglish D | Wrong D | Same as agreement | Switches |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | All BEnQA rows | 144 | 41 | 39 | 25 | 43 | 26 |
| Qwen2.5-3B | Bangla and English agree | 69 | 24 | 20 | 13 | 43 | 26 |
| Qwen2.5-3B | Bangla and English agree on non-D | 47 | 14 | 4 | 4 | 27 | 20 |
| Qwen2.5-3B | Bangla and English agree on D | 22 | 10 | 16 | 9 | 16 | 6 |
| Qwen2.5-3B | Bangla and English are correct and agree | 30 | 18 | 9 | 2 | 18 | 12 |
| Qwen2.5-3B | Bangla and English are correct and agree on non-D | 23 | 11 | 2 | 2 | 11 | 12 |
| Qwen2.5-3B | Bangla and English are correct and agree on D | 7 | 7 | 7 | 0 | 7 | 0 |
| Qwen2.5-7B 8-bit | All BEnQA rows | 144 | 47 | 25 | 17 | 43 | 40 |
| Qwen2.5-7B 8-bit | Bangla and English agree | 85 | 28 | 14 | 10 | 43 | 40 |
| Qwen2.5-7B 8-bit | Bangla and English agree on non-D | 76 | 24 | 9 | 8 | 38 | 36 |
| Qwen2.5-7B 8-bit | Bangla and English agree on D | 9 | 4 | 5 | 2 | 5 | 4 |
| Qwen2.5-7B 8-bit | Bangla and English are correct and agree | 49 | 23 | 10 | 7 | 23 | 24 |
| Qwen2.5-7B 8-bit | Bangla and English are correct and agree on non-D | 44 | 20 | 7 | 7 | 20 | 22 |
| Qwen2.5-7B 8-bit | Bangla and English are correct and agree on D | 5 | 3 | 3 | 0 | 3 | 2 |
| Qwen3-4B | All BEnQA rows | 144 | 47 | 111 | 77 | 53 | 39 |
| Qwen3-4B | Bangla and English agree | 92 | 35 | 72 | 46 | 53 | 39 |
| Qwen3-4B | Bangla and English agree on non-D | 47 | 12 | 30 | 27 | 11 | 36 |
| Qwen3-4B | Bangla and English agree on D | 45 | 23 | 42 | 19 | 42 | 3 |
| Qwen3-4B | Bangla and English are correct and agree | 61 | 31 | 46 | 23 | 31 | 30 |
| Qwen3-4B | Bangla and English are correct and agree on non-D | 36 | 8 | 23 | 23 | 8 | 28 |
| Qwen3-4B | Bangla and English are correct and agree on D | 25 | 23 | 23 | 0 | 23 | 2 |

## Interpretation

- This is a stricter version of the option-switching audit: it requires
  both alternate scripts to agree before inspecting the reviewed-Banglish
  answer.
- Qwen3's D-attractor survives this agreement filter, including the slice
  where both Bangla and English are correct on the same non-D answer.
- The result remains behavioral evidence and uses benchmark-provided
  alternate-script views, so it is diagnostic rather than deployable.

## Artifacts

- Builder: `scripts/analyze_v5_benqa_cross_script_option_agreement.py`
- Item table: `results/analysis/v5_benqa_cross_script_option_agreement_items.csv`
- Summary table: `results/analysis/v5_benqa_cross_script_option_agreement_summary.csv`
