# Frozen-V5 BEnQA Order-Confound Audit

Updated: 2026-06-11

## Scope

This no-spend audit checks whether the Qwen3-4B reviewed-Banglish BEnQA
D-attractor can be reduced to item order, BEnQA-only order, or output
run position. It joins the frozen-v5 item order, reviewed-Banglish
answer-format run-line metadata, and the BEnQA choice-bias item table.

- Item table: `results/analysis/v5_benqa_order_confound_items.csv`
- Summary table: `results/analysis/v5_benqa_order_confound_summary.csv`

## Headline

- By reviewed-Banglish output-line quartile, Qwen3-4B predicts D on 26/36, 31/36, 28/36, 26/36 rows; every quartile is at least 26/36 (72.2%).
- Wrong-D counts by the same quartiles are 20/36, 19/36, 19/36, 19/36; the first and last quartiles are 20/36 and 19/36.
- Qwen3-4B has D on 111/144 rows overall with 23 separate D-runs; its longest contiguous D-run is 13 rows.
- The two Qwen2.5 reviewed-Banglish rows have much lower D totals and shorter D-runs: 39/144 with longest run 3, and 25/144 with longest run 2.

## Run-Line Quartiles

| Model | Q1 D | Q2 D | Q3 D | Q4 D | Q1 wrong D | Q4 wrong D | Longest D-run |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 10/36 | 11/36 | 12/36 | 6/36 | 9/36 | 6/36 | 3 |
| Qwen2.5-7B 8-bit | 8/36 | 6/36 | 9/36 | 2/36 | 6/36 | 2/36 | 2 |
| Qwen3-4B | 26/36 | 31/36 | 28/36 | 26/36 | 20/36 | 19/36 | 13 |

## Interpretation

- Qwen3's reviewed-Banglish D-attractor is visible from the first
  output-line quartile and remains visible in the last, so it is not
  a simple late-run degradation or a single terminal corruption block.
- The repeated D-runs are longer for Qwen3 than for Qwen2.5, but they
  are distributed across the run rather than confined to one segment.
- This audit addresses an execution/order confound. It remains behavioral
  evidence over fixed outputs and does not identify an internal mechanism.

## Artifacts

- Builder: `scripts/analyze_v5_benqa_order_confound.py`
- Item table: `results/analysis/v5_benqa_order_confound_items.csv`
- Summary table: `results/analysis/v5_benqa_order_confound_summary.csv`
