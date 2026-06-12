# Qwen2.5-3B BEnQA Extension Pilot130 Result

Updated: 2026-06-05

## Purpose

This run scales the BEnQA extension smoke from 26 rows to 130 pass-only
extension rows. It tests whether the BEnQA scale-extension path is operationally
clean and whether the cross-script direction is worth evaluating on the full
851-row pass-only extension.

## Input And Output

- Model: `Qwen/Qwen2.5-3B-Instruct`
- Input: `data/slices/benqa_extended_1000_v1_ai_pass_pilot130.jsonl`
- Rows: 130 BEnQA extension items
- Variants: Bangla, reviewed Banglish, English
- Evaluation requests: 390
- Output:
  `results/runs/qwen25_3b_benqa_ext_pilot130/results/runs/qwen25_3b_benqa_ext_pilot130.jsonl`
- Summary: `results/analysis/qwen25_3b_benqa_ext_pilot130_summary.csv`
- Paired-gap analysis: `reports/qwen25_3b_benqa_ext_pilot130_paired_gap_analysis.md`
- Recoverable examples:
  `reports/qwen25_3b_benqa_ext_pilot130_recoverable_examples.md`
- Kaggle kernel: `munimthahmid/qwen2-5-3b-benqa-extension-pilot130`

## Operational Result

The pilot passed the scale gate.

- Result rows: 390/390.
- Parsed-empty rows: 0/390.
- Runtime failure pattern: none observed in the collected output/log tail.
- Log:
  `results/runs/qwen25_3b_benqa_ext_pilot130/qwen2-5-3b-benqa-extension-pilot130.log`

## Accuracy Snapshot

| Variant | Correct | Total | Accuracy | Parsed empty |
| --- | ---: | ---: | ---: | ---: |
| Bangla | 53 | 130 | 40.77% | 0 |
| Reviewed Banglish | 42 | 130 | 32.31% | 0 |
| English | 71 | 130 | 54.62% | 0 |

Paired bootstrap gaps from
`reports/qwen25_3b_benqa_ext_pilot130_paired_gap_analysis.md`:

| Gap | Delta | 95% bootstrap CI |
| --- | ---: | --- |
| Reviewed Banglish - Bangla | -8.46 pts | [-16.92, 0.00] |
| Reviewed Banglish - English | -22.31 pts | [-33.08, -11.54] |
| English - Bangla | +13.85 pts | [+3.85, +23.85] |

## Interpretation

The pilot strengthens the dataset-size hardening story. On a new 130-row BEnQA
extension subset outside the frozen validation-200 gold core, the same model
again shows reviewed Banglish below English and directionally below Bangla.

The Banglish-vs-Bangla confidence interval touches zero on the 130-row pilot,
so this should not be written as a final scale claim yet. The operational result
is clean and the direction is useful enough to run the full 851-row pass-only
extension for the same model.

Qualitative support: the pilot has 49 recoverable reviewed-Banglish misses
where Banglish is wrong but Bangla or English is correct on the same item. Of
those, 17 are recovered by both Bangla and English, 26 by English only, and 6 by
Bangla only. See
`reports/qwen25_3b_benqa_ext_pilot130_recoverable_examples.md`.

## Decision

Launch `Qwen/Qwen2.5-3B-Instruct` on
`data/slices/benqa_extended_1000_v1_ai_pass.jsonl`.

Do not add more model families or paid frontier APIs to the extension until the
full Qwen2.5-3B extension result is collected and analyzed.
