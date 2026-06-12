# DeepSeek V4 Flash BEnQA Extension Full851 Result

Updated: 2026-06-05

## Purpose

This run evaluates DeepSeek V4 Flash on the full 851-row pass-only BEnQA
extension. It is the non-Qwen API-family scale replication for the silver
BEnQA extension: the validation-200 v5 gold core remains human-reviewed, while
this extension tests whether the reviewed-Banglish deficit survives at larger
scale under a cheap hosted frontier-family model.

## Input And Output

- Model: `deepseek-v4-flash`
- Provider mode: OpenAI-compatible chat completions, thinking disabled
- Input manifest:
  `data/api_audit/deepseek_v4_flash_benqa_ext_full851_requests.jsonl`
- Source items: `data/slices/benqa_extended_1000_v1_ai_pass.jsonl`
- Rows: 851 BEnQA extension items
- Variants: Bangla, reviewed Banglish, English
- Evaluation requests: 2,553
- Raw output: `results/api_audit/deepseek_v4_flash_benqa_ext_full851_raw.jsonl`
- Imported rows:
  `results/analysis/deepseek_v4_flash_benqa_ext_full851_imported.jsonl`
- Summary: `results/analysis/deepseek_v4_flash_benqa_ext_full851_summary.csv`
- Paired-gap analysis:
  `reports/deepseek_v4_flash_benqa_ext_full851_paired_gap_analysis.md`
- Recoverable examples:
  `reports/deepseek_v4_flash_benqa_ext_full851_recoverable_examples.md`

## Operational Result

The full extension run passed the scale gate.

- Result rows: 2,553/2,553.
- Unique request IDs: 2,553/2,553.
- Finish reasons: STOP=2,553.
- Parsed-empty rows: 0/2,553.
- Runtime/parser failure pattern: none observed.
- Approximate text-token cost at checked 2026-06-05 DeepSeek V4 Flash pricing:
  $0.0371.

## Accuracy Snapshot

| Variant | Correct | Total | Accuracy | Parsed empty |
| --- | ---: | ---: | ---: | ---: |
| Bangla | 665 | 851 | 78.14% | 0 |
| Reviewed Banglish | 376 | 851 | 44.18% | 0 |
| English | 697 | 851 | 81.90% | 0 |

Paired bootstrap gaps from
`reports/deepseek_v4_flash_benqa_ext_full851_paired_gap_analysis.md`:

| Gap | Delta | 95% bootstrap CI |
| --- | ---: | --- |
| Reviewed Banglish - Bangla | -33.96 pts | [-37.84, -30.08] |
| Reviewed Banglish - English | -37.72 pts | [-41.36, -33.96] |
| English - Bangla | +3.76 pts | [+1.29, +6.35] |

## Recoverable Misses

The full extension has 380 recoverable reviewed-Banglish misses where reviewed
Banglish is wrong but Bangla or English is correct on the same item.

- Bangla and English both recover: 301.
- English-only recovery: 51.
- Bangla-only recovery: 28.
- Examples: `reports/deepseek_v4_flash_benqa_ext_full851_recoverable_examples.md`

## Interpretation

This is the cleanest low-cost API scale replication so far. DeepSeek V4 Flash
is much stronger than Qwen2.5-3B in absolute BEnQA extension accuracy, but the
reviewed-Banglish deficit is also much larger:

English > Bangla > reviewed Banglish.

The result strengthens the thesis because it separates two claims that could
otherwise be conflated:

- The BEnQA extension scale result is not only a Qwen-local artifact.
- Higher absolute model accuracy does not guarantee script robustness for
  reviewed Banglish.

Use this as the only API full851 scale add-on. Do not run full851 for Claude,
Groq, Gemini, or GPT by default; validation-200 is sufficient for the
cross-family frontier panel, and DeepSeek already answers the cheap non-Qwen
scale-replication question.
