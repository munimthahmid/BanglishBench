# Qwen3-1.7B Dev50 No-Thinking Probe

Updated: 2026-05-28 13:52 +0600

This report documents the Qwen3-1.7B dev50 probe and the evaluator fix needed
for Qwen3-style thinking models.

## Default Run Was Diagnostic Only

Default Qwen3-1.7B dev50 output was dominated by truncated `<think>` traces.
That made it an evaluator/protocol failure rather than a fair task baseline.

| Mode | Bangla | Banglish | English | Parsed Empty |
| --- | ---: | ---: | ---: | ---: |
| Default thinking | 1/50 | 0/50 | 1/50 | 29, 35, 35 |

Artifact:

- `results/runs/qwen3_1_7b_validation200_v4_dev50/`

## Pipeline Fix

Added `--disable-thinking` support to:

- `scripts/run_eval_kaggle.py`
- `scripts/prepare_kaggle_model_run.py`

The runner now passes `enable_thinking=False` to tokenizer chat templates when
supported. If the tokenizer does not accept that argument, it falls back to
appending `/no_think`.

## Corrected Dev50 Result

Run:

- Model: `Qwen/Qwen3-1.7B`
- Kernel: `munimthahmid/qwen3-1-7b-nothink-validation200-v4-dev50`
- Slice: `data/slices/validation_200_v4_dev50.jsonl`
- Prompt mode: baseline
- Max new tokens: 128
- `--disable-thinking`: enabled

Overall:

| Variant | Correct | Accuracy | Parsed Empty |
| --- | ---: | ---: | ---: |
| Bangla | 11/50 | 0.22 | 7 |
| Clean Banglish | 11/50 | 0.22 | 3 |
| English | 20/50 | 0.40 | 6 |

By dataset:

| Dataset | Bangla | Banglish | English |
| --- | ---: | ---: | ---: |
| BEnQA | 10/36 | 11/36 | 18/36 |
| BanglaMATH | 1/14 | 0/14 | 2/14 |

## Interpretation

- The no-thinking setting converts Qwen3-1.7B from unusable to informative.
- On dev50, Qwen3-1.7B is tied between Bangla and Banglish, while English is
  substantially higher.
- This resembles the Phi-3.5-mini pattern more than Qwen3-4B: English competence
  is useful, but the Banglish-below-Bangla ordering is not visible on dev.
- Because the dev result is non-degenerate and fills a Qwen3 scaling gap, a
  held-out test150 run is justified.

## Artifacts

- `results/runs/qwen3_1_7b_nothink_validation200_v4_dev50/results/runs/qwen3_1_7b_nothink_validation200_v4_dev50.jsonl`
- `results/runs/qwen3_1_7b_nothink_validation200_v4_dev50/summary_by_variant_reparsed_rescored.csv`
- `results/runs/qwen3_1_7b_nothink_validation200_v4_dev50/summary_by_dataset_variant_reparsed_rescored.csv`
