# BEnQA Extension Kaggle Pilot130 Launch

Updated: 2026-06-05

## Purpose

This pilot scales the clean 26-row BEnQA extension smoke to 130 pass-only
extension rows. It is the first substantive open-model scale check for the
silver BEnQA extension, but it is still a gate before the full 851-row pass-only
extension.

## Input

- Source full pass-only slice: `data/slices/benqa_extended_1000_v1_ai_pass.jsonl`
- Pilot subset: `data/slices/benqa_extended_1000_v1_ai_pass_pilot130.jsonl`
- Subset report: `reports/benqa_extension_eval_subsets.md`
- Rows: 130
- Evaluation requests: 390 = 130 rows x Bangla, reviewed Banglish, English

## Precondition

The 26-row smoke passed:

- Result rows: 78/78.
- Parsed-empty rows: 0/78.
- Runtime/parser failure pattern: none observed.
- Smoke report: `reports/qwen25_3b_benqa_ext_smoke26.md`

## Kaggle Assets

- Dataset folder: `kaggle_jobs/benqa_ext_pilot130_assets_account1`
- Kernel folder: `kaggle_jobs/qwen25_3b_benqa_ext_pilot130`
- Kaggle dataset: `munimthahmid/script-matters-benqa-ext-pilot130-assets`
- Kaggle kernel: `munimthahmid/qwen2-5-3b-benqa-extension-pilot130`
- Expected output file:
  `results/runs/qwen25_3b_benqa_ext_pilot130/results/runs/qwen25_3b_benqa_ext_pilot130.jsonl`

## Launch Commands Used

```bash
python3 scripts/prepare_kaggle_model_run.py \
  --account 1 \
  --model Qwen/Qwen2.5-3B-Instruct \
  --dataset-slug script-matters-benqa-ext-pilot130-assets \
  --dataset-title 'Script Matters BEnQA Extension Pilot130 Assets' \
  --items-path data/slices/benqa_extended_1000_v1_ai_pass_pilot130.jsonl \
  --assets-job-name benqa_ext_pilot130_assets_account1 \
  --job-name qwen25_3b_benqa_ext_pilot130 \
  --kernel-slug qwen2-5-3b-benqa-extension-pilot130 \
  --title 'Qwen2.5-3B BEnQA Extension Pilot130' \
  --output-name qwen25_3b_benqa_ext_pilot130 \
  --limit 0 \
  --variants bangla banglish_clean english \
  --max-new-tokens 64 \
  --temperature 0.0
```

```bash
python3 scripts/kaggle_with_account.py --account 1 -- \
  datasets create -p kaggle_jobs/benqa_ext_pilot130_assets_account1 --dir-mode zip
```

```bash
python3 scripts/kaggle_with_account.py --account 1 -- \
  kernels push -p kaggle_jobs/qwen25_3b_benqa_ext_pilot130
```

## Current Status

The pilot assets dataset was created successfully, kernel version 1 was pushed
successfully, output was collected, and summary/paired-gap analysis completed.

- Dataset URL:
  `https://www.kaggle.com/datasets/munimthahmid/script-matters-benqa-ext-pilot130-assets`
- Kernel URL:
  `https://www.kaggle.com/code/munimthahmid/qwen2-5-3b-benqa-extension-pilot130`

Collected output:

- Result file:
  `results/runs/qwen25_3b_benqa_ext_pilot130/results/runs/qwen25_3b_benqa_ext_pilot130.jsonl`
- Log:
  `results/runs/qwen25_3b_benqa_ext_pilot130/qwen2-5-3b-benqa-extension-pilot130.log`
- Summary:
  `results/analysis/qwen25_3b_benqa_ext_pilot130_summary.csv`
- Paired-gap report:
  `reports/qwen25_3b_benqa_ext_pilot130_paired_gap_analysis.md`
- Result report:
  `reports/qwen25_3b_benqa_ext_pilot130.md`

Operational gate:

- Result rows: 390/390.
- Parsed-empty rows: 0/390.
- Runtime/parser failure pattern: none observed.

Accuracy snapshot:

| Variant | Correct | Total | Accuracy |
| --- | ---: | ---: | ---: |
| Bangla | 53 | 130 | 40.77% |
| Reviewed Banglish | 42 | 130 | 32.31% |
| English | 71 | 130 | 54.62% |

## Follow-Up Commands

Check status:

```bash
python3 scripts/kaggle_with_account.py --account 1 -- \
  kernels status munimthahmid/qwen2-5-3b-benqa-extension-pilot130
```

Download output:

```bash
python3 scripts/kaggle_with_account.py --account 1 -- \
  kernels output munimthahmid/qwen2-5-3b-benqa-extension-pilot130 \
  -p results/runs/qwen25_3b_benqa_ext_pilot130 --force
```

Summary command used:

```bash
python3 scripts/summarize_outputs.py \
  results/runs/qwen25_3b_benqa_ext_pilot130 \
  --output results/analysis/qwen25_3b_benqa_ext_pilot130_summary.csv \
  --rescore
```

## Decision Rule

The pilot run has 390/390 rows, 0 parsed-empty rows, and no runtime/parser
failure pattern. The paired result is directionally useful enough to run the
full 851-row pass-only extension for Qwen2.5-3B.

Do not run frontier APIs on the extension unless the open-model scale result
creates a specific paper-review question.
