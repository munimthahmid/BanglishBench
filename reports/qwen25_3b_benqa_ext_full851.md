# Qwen2.5-3B BEnQA Extension Full851 Result

Updated: 2026-06-05

## Purpose

This run evaluates Qwen2.5-3B on the full 851-row pass-only BEnQA extension.
It is the main silver-scale result supporting the dataset-size hardening claim:
the human-reviewed validation-200 v5 gold core is now backed by a much larger
AI-assisted BEnQA extension.

## Input And Output

- Model: `Qwen/Qwen2.5-3B-Instruct`
- Input: `data/slices/benqa_extended_1000_v1_ai_pass.jsonl`
- Rows: 851 BEnQA extension items
- Variants: Bangla, reviewed Banglish, English
- Evaluation requests: 2,553
- Output:
  `results/runs/qwen25_3b_benqa_ext_full851/results/runs/qwen25_3b_benqa_ext_full851.jsonl`
- Summary: `results/analysis/qwen25_3b_benqa_ext_full851_summary.csv`
- Paired-gap analysis: `reports/qwen25_3b_benqa_ext_full851_paired_gap_analysis.md`
- Recoverable examples:
  `reports/qwen25_3b_benqa_ext_full851_recoverable_examples.md`
- Kaggle kernel: `munimthahmid/qwen2-5-3b-benqa-extension-full851`

## Operational Result

The full extension run passed the scale gate.

- Result rows: 2,553/2,553.
- Parsed-empty rows: 0/2,553.
- Runtime failure pattern: none observed in the collected output/log tail.
- Log:
  `results/runs/qwen25_3b_benqa_ext_full851/qwen2-5-3b-benqa-extension-full851.log`

## Accuracy Snapshot

| Variant | Correct | Total | Accuracy | Parsed empty |
| --- | ---: | ---: | ---: | ---: |
| Bangla | 291 | 851 | 34.20% | 0 |
| Reviewed Banglish | 248 | 851 | 29.14% | 0 |
| English | 437 | 851 | 51.35% | 0 |

Paired bootstrap gaps from
`reports/qwen25_3b_benqa_ext_full851_paired_gap_analysis.md`:

| Gap | Delta | 95% bootstrap CI |
| --- | ---: | --- |
| Reviewed Banglish - Bangla | -5.05 pts | [-8.46, -1.65] |
| Reviewed Banglish - English | -22.21 pts | [-26.20, -18.10] |
| English - Bangla | +17.16 pts | [+13.28, +20.92] |

## Recoverable Misses

The full extension has 311 recoverable reviewed-Banglish misses where reviewed
Banglish is wrong but Bangla or English is correct on the same item.

- Bangla and English both recover: 96.
- English-only recovery: 175.
- Bangla-only recovery: 40.
- Examples: `reports/qwen25_3b_benqa_ext_full851_recoverable_examples.md`

## Interpretation

This is a meaningful thesis upgrade. The full extension is outside the frozen
validation-200 v5 gold core, yet it reproduces the same ordering for Qwen2.5-3B:

English > Bangla > reviewed Banglish.

Unlike the 130-row pilot, the full extension gives a Banglish-vs-Bangla
confidence interval that is fully below zero. The extension still remains a
silver layer because its review is AI-assisted structural triage, not human
review. The correct framing is therefore:

"The human-reviewed validation-200 v5 gold core is supported by an 851-row
AI-assisted BEnQA pass-only extension, where Qwen2.5-3B again shows a paired
reviewed-Banglish deficit against both Bangla and English."

## Decision

Use this as the dataset-size hardening result. Do not launch more extension
models until the thesis write-up integrates this result and decides whether an
additional model family would materially change the claim.
