# BEnQA Extension Kaggle Full851 Launch

Updated: 2026-06-05

## Purpose

This run evaluates Qwen2.5-3B on the full 851-row pass-only BEnQA extension.
It is the main no-paid-compute scale check for the thesis dataset-size
hardening argument.

## Input

- Source pass-only slice: `data/slices/benqa_extended_1000_v1_ai_pass.jsonl`
- Rows: 851
- Evaluation requests: 2,553 = 851 rows x Bangla, reviewed Banglish, English
- Smoke report: `reports/qwen25_3b_benqa_ext_smoke26.md`
- Pilot report: `reports/qwen25_3b_benqa_ext_pilot130.md`

## Precondition

The staged gates passed before this launch:

- Smoke26: 78/78 rows, 0 parsed-empty rows, no runtime/parser failure pattern.
- Pilot130: 390/390 rows, 0 parsed-empty rows, no runtime/parser failure
  pattern.
- Pilot130 accuracy: 53/130 Bangla, 42/130 reviewed Banglish, 71/130 English.
- Pilot130 paired gaps: -8.46 pts reviewed Banglish minus Bangla and
  -22.31 pts reviewed Banglish minus English.

## Kaggle Assets

- Dataset folder: `kaggle_jobs/benqa_ext_full851_assets_account1`
- Kernel folder: `kaggle_jobs/qwen25_3b_benqa_ext_full851`
- Kaggle dataset: `munimthahmid/script-matters-benqa-ext-full851-assets`
- Kaggle kernel: `munimthahmid/qwen2-5-3b-benqa-extension-full851`
- Expected output file:
  `results/runs/qwen25_3b_benqa_ext_full851/results/runs/qwen25_3b_benqa_ext_full851.jsonl`

## Launch Commands Used

```bash
python3 scripts/prepare_kaggle_model_run.py \
  --account 1 \
  --model Qwen/Qwen2.5-3B-Instruct \
  --dataset-slug script-matters-benqa-ext-full851-assets \
  --dataset-title 'Script Matters BEnQA Extension Full851 Assets' \
  --items-path data/slices/benqa_extended_1000_v1_ai_pass.jsonl \
  --assets-job-name benqa_ext_full851_assets_account1 \
  --job-name qwen25_3b_benqa_ext_full851 \
  --kernel-slug qwen2-5-3b-benqa-extension-full851 \
  --title 'Qwen2.5-3B BEnQA Extension Full851' \
  --output-name qwen25_3b_benqa_ext_full851 \
  --limit 0 \
  --variants bangla banglish_clean english \
  --max-new-tokens 64 \
  --temperature 0.0
```

```bash
python3 scripts/kaggle_with_account.py --account 1 -- \
  datasets create -p kaggle_jobs/benqa_ext_full851_assets_account1 --dir-mode zip
```

```bash
python3 scripts/kaggle_with_account.py --account 1 -- \
  kernels push -p kaggle_jobs/qwen25_3b_benqa_ext_full851
```

## Current Status

The full assets dataset was created successfully, kernel version 1 was pushed
successfully, output was collected, and summary/paired-gap analysis completed.

- Dataset URL:
  `https://www.kaggle.com/datasets/munimthahmid/script-matters-benqa-ext-full851-assets`
- Kernel URL:
  `https://www.kaggle.com/code/munimthahmid/qwen2-5-3b-benqa-extension-full851`

Collected output:

- Result file:
  `results/runs/qwen25_3b_benqa_ext_full851/results/runs/qwen25_3b_benqa_ext_full851.jsonl`
- Log:
  `results/runs/qwen25_3b_benqa_ext_full851/qwen2-5-3b-benqa-extension-full851.log`
- Summary:
  `results/analysis/qwen25_3b_benqa_ext_full851_summary.csv`
- Paired-gap report:
  `reports/qwen25_3b_benqa_ext_full851_paired_gap_analysis.md`
- Recoverable examples:
  `reports/qwen25_3b_benqa_ext_full851_recoverable_examples.md`
- Result report:
  `reports/qwen25_3b_benqa_ext_full851.md`

Operational gate:

- Result rows: 2,553/2,553.
- Parsed-empty rows: 0/2,553.
- Runtime/parser failure pattern: none observed.

Accuracy snapshot:

| Variant | Correct | Total | Accuracy |
| --- | ---: | ---: | ---: |
| Bangla | 291 | 851 | 34.20% |
| Reviewed Banglish | 248 | 851 | 29.14% |
| English | 437 | 851 | 51.35% |

## Follow-Up Commands

Check status:

```bash
python3 scripts/kaggle_with_account.py --account 1 -- \
  kernels status munimthahmid/qwen2-5-3b-benqa-extension-full851
```

Download output:

```bash
python3 scripts/kaggle_with_account.py --account 1 -- \
  kernels output munimthahmid/qwen2-5-3b-benqa-extension-full851 \
  -p results/runs/qwen25_3b_benqa_ext_full851 --force
```

Summary command used:

```bash
python3 scripts/summarize_outputs.py \
  results/runs/qwen25_3b_benqa_ext_full851 \
  --output results/analysis/qwen25_3b_benqa_ext_full851_summary.csv \
  --rescore
```

Paired-gap command used:

```bash
python3 scripts/analyze_benqa_extension_scale_result.py \
  --input results/runs/qwen25_3b_benqa_ext_full851/results/runs/qwen25_3b_benqa_ext_full851.jsonl \
  --output-summary results/analysis/qwen25_3b_benqa_ext_full851_paired_gaps.csv \
  --output-items results/analysis/qwen25_3b_benqa_ext_full851_item_matrix.csv \
  --report reports/qwen25_3b_benqa_ext_full851_paired_gap_analysis.md \
  --title 'Qwen2.5-3B BEnQA Extension Full851 Paired Gap Analysis'
```

## Decision Rule

The full run has 2,553/2,553 rows, 0 parsed-empty rows, and negative paired
Banglish gaps:

- Reviewed Banglish - Bangla: -5.05 pts, CI [-8.46, -1.65].
- Reviewed Banglish - English: -22.21 pts, CI [-26.20, -18.10].

The thesis can now claim that the human-reviewed 200-item gold-core BEnQA
result is supported by a much larger AI-assisted silver BEnQA extension.

Do not launch additional extension models until this full run is collected and
the claim boundary is updated.
