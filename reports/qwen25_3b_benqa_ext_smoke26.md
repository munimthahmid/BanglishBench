# Qwen2.5-3B BEnQA Extension Smoke26 Result

Updated: 2026-06-05

## Purpose

This run checks whether the BEnQA extension pass-only slice works with the
existing Kaggle open-model pipeline before scaling to the 130-row pilot and
eventually the 851-row pass-only extension.

## Input And Output

- Model: `Qwen/Qwen2.5-3B-Instruct`
- Input: `data/slices/benqa_extended_1000_v1_ai_pass_smoke26.jsonl`
- Rows: 26 BEnQA extension items
- Variants: Bangla, reviewed Banglish, English
- Evaluation requests: 78
- Output: `results/runs/qwen25_3b_benqa_ext_smoke26/results/runs/qwen25_3b_benqa_ext_smoke26.jsonl`
- Summary: `results/analysis/qwen25_3b_benqa_ext_smoke26_summary.csv`
- Paired-gap analysis: `reports/qwen25_3b_benqa_ext_smoke26_paired_gap_analysis.md`
- Kaggle kernel: `munimthahmid/qwen2-5-3b-benqa-extension-smoke26`

## Operational Result

The smoke passed the launch gate.

- Result rows: 78/78.
- Parsed-empty rows: 0/78.
- Runtime failure pattern: none observed in the collected output/log tail.
- Log: `results/runs/qwen25_3b_benqa_ext_smoke26/qwen2-5-3b-benqa-extension-smoke26.log`

## Accuracy Snapshot

| Variant | Correct | Total | Accuracy | Parsed empty |
| --- | ---: | ---: | ---: | ---: |
| Bangla | 8 | 26 | 30.77% | 0 |
| Reviewed Banglish | 11 | 26 | 42.31% | 0 |
| English | 20 | 26 | 76.92% | 0 |

Paired item patterns over the 26 smoke items:

| Bangla | Reviewed Banglish | English | Items |
| --- | --- | --- | ---: |
| wrong | wrong | correct | 9 |
| wrong | correct | correct | 5 |
| correct | wrong | correct | 3 |
| correct | correct | correct | 3 |
| wrong | wrong | wrong | 2 |
| wrong | correct | wrong | 2 |
| correct | wrong | wrong | 1 |
| correct | correct | wrong | 1 |

Paired bootstrap gaps from
`reports/qwen25_3b_benqa_ext_smoke26_paired_gap_analysis.md`:

| Gap | Delta | 95% bootstrap CI |
| --- | ---: | --- |
| Reviewed Banglish - Bangla | +11.54 pts | [-11.54, +34.62] |
| Reviewed Banglish - English | -34.62 pts | [-57.69, -7.69] |
| English - Bangla | +46.15 pts | [+23.08, +69.23] |

## Interpretation

This is a parser/runtime smoke, not a thesis-level accuracy estimate. The
important result is that the extension data, prompt rendering, answer parser,
and Kaggle collection path all worked cleanly.

The tiny accuracy pattern is nevertheless worth scaling: English is much higher
than both Bengali-script conditions, and reviewed Banglish is not behaving like
a parser-broken variant. Because the smoke has only 26 items, the next valid
step is the 130-row pilot rather than a substantive claim.

## Decision

Launch `Qwen/Qwen2.5-3B-Instruct` on
`data/slices/benqa_extended_1000_v1_ai_pass_pilot130.jsonl`.

Do not launch the full 851-row extension until the pilot also has complete
outputs and no parser/runtime failure pattern.
