# BEnQA Extension Evaluation Subsets

Updated: 2026-06-05

## Purpose

These subsets turn the BEnQA extension into evaluation-ready units. The
gold-core validation-200 result remains the primary thesis claim; these
subsets are for scale-checking that BEnQA behavior beyond the gold core
points in the same direction.

## Files

- Source pass-only slice: `data/slices/benqa_extended_1000_v1_ai_pass.jsonl`
- Smoke subset: `data/slices/benqa_extended_1000_v1_ai_pass_smoke26.jsonl`
- Pilot subset: `data/slices/benqa_extended_1000_v1_ai_pass_pilot130.jsonl`
- Full pass-only slice: `data/slices/benqa_extended_1000_v1_ai_pass.jsonl`

## Subset Sizes

| Subset | Rows | Triad requests | Purpose |
| --- | ---: | ---: | --- |
| Smoke | 26 | 78 | Parser/prompt/runtime smoke. |
| Pilot | 130 | 390 | First open-model scale check. |
| Full pass-only | 851 | 2553 | Conservative extension evaluation. |

## Smoke Subject Balance

| Subject | Rows |
| --- | ---: |
| Biology | 2 |
| Biology-I | 2 |
| Biology-II | 2 |
| Chemistry | 2 |
| Chemistry-I | 2 |
| Chemistry-II | 2 |
| Math | 2 |
| Math-I | 2 |
| Math-II | 2 |
| Physics | 2 |
| Physics-I | 2 |
| Physics-II | 2 |
| Science | 2 |

## Recommended Launch Order

1. Run dry-run prompt rendering locally on the smoke subset.
2. Run one Qwen2.5-3B Kaggle smoke on the smoke subset.
3. If parser/runtime is clean, run Qwen2.5-3B on the 130-row pilot.
4. Only then decide whether to run all three Qwen rows on the full
   851-row pass-only extension.

Do not spend frontier API budget on the full extension unless a specific
paper-review question requires it.
