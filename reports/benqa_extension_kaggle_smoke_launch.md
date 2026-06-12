# BEnQA Extension Kaggle Smoke Launch

Updated: 2026-06-05

## Purpose

This smoke run tests whether the new BEnQA extension pass-only slice works with
the existing Kaggle open-model evaluation pipeline before launching larger
extension evaluations.

## Input

- Source full pass-only slice: `data/slices/benqa_extended_1000_v1_ai_pass.jsonl`
- Smoke subset: `data/slices/benqa_extended_1000_v1_ai_pass_smoke26.jsonl`
- Subset report: `reports/benqa_extension_eval_subsets.md`
- Rows: 26
- Evaluation requests: 78 = 26 rows x Bangla, reviewed Banglish, English

## Local Checks

Local dry-run prompt rendering succeeded for the first two smoke items across
Bangla, Banglish, and English:

```bash
python3 scripts/run_eval_kaggle.py \
  --input data/slices/benqa_extended_1000_v1_ai_pass_smoke26.jsonl \
  --output /tmp/benqa_ext_smoke_dry_run.jsonl \
  --model Qwen/Qwen2.5-3B-Instruct \
  --variants bangla banglish_clean english \
  --limit 2 \
  --dry-run
```

## Kaggle Assets

- Dataset folder: `kaggle_jobs/benqa_ext_smoke26_assets_account1`
- Kernel folder: `kaggle_jobs/qwen25_3b_benqa_ext_smoke26`
- Kaggle dataset: `munimthahmid/script-matters-benqa-ext-smoke26-assets`
- Kaggle kernel: `munimthahmid/qwen2-5-3b-benqa-extension-smoke26`
- Expected output file: `results/runs/qwen25_3b_benqa_ext_smoke26.jsonl`

## Launch Commands Used

```bash
python3 scripts/prepare_kaggle_model_run.py \
  --account 1 \
  --model Qwen/Qwen2.5-3B-Instruct \
  --dataset-slug script-matters-benqa-ext-smoke26-assets \
  --dataset-title 'Script Matters BEnQA Extension Smoke26 Assets' \
  --items-path data/slices/benqa_extended_1000_v1_ai_pass_smoke26.jsonl \
  --assets-job-name benqa_ext_smoke26_assets_account1 \
  --job-name qwen25_3b_benqa_ext_smoke26 \
  --kernel-slug qwen25-3b-benqa-ext-smoke26 \
  --title 'Qwen2.5-3B BEnQA Extension Smoke26' \
  --output-name qwen25_3b_benqa_ext_smoke26 \
  --limit 0 \
  --variants bangla banglish_clean english \
  --max-new-tokens 64 \
  --temperature 0.0
```

```bash
python3 scripts/kaggle_with_account.py --account 1 -- \
  datasets create -p kaggle_jobs/benqa_ext_smoke26_assets_account1 --dir-mode zip
```

```bash
python3 scripts/kaggle_with_account.py --account 1 -- \
  kernels push -p kaggle_jobs/qwen25_3b_benqa_ext_smoke26
```

## Current Status

The dataset upload, kernel push, output collection, and summary all succeeded.
Kaggle's status endpoint returned a transient 500 for the new private kernel,
but the kernel appears in `kernels list --mine` as:

- `munimthahmid/qwen2-5-3b-benqa-extension-smoke26`

Collected output:

- Result file:
  `results/runs/qwen25_3b_benqa_ext_smoke26/results/runs/qwen25_3b_benqa_ext_smoke26.jsonl`
- Log:
  `results/runs/qwen25_3b_benqa_ext_smoke26/qwen2-5-3b-benqa-extension-smoke26.log`
- Summary:
  `results/analysis/qwen25_3b_benqa_ext_smoke26_summary.csv`
- Result report:
  `reports/qwen25_3b_benqa_ext_smoke26.md`

Operational gate:

- Result rows: 78/78.
- Parsed-empty rows: 0/78.
- Runtime/parser failure pattern: none observed.

Accuracy snapshot:

| Variant | Correct | Total | Accuracy |
| --- | ---: | ---: | ---: |
| Bangla | 8 | 26 | 30.77% |
| Reviewed Banglish | 11 | 26 | 42.31% |
| English | 20 | 26 | 76.92% |

## Follow-Up Commands

Check status:

```bash
python3 scripts/kaggle_with_account.py --account 1 -- \
  kernels status munimthahmid/qwen2-5-3b-benqa-extension-smoke26
```

Download output:

```bash
python3 scripts/kaggle_with_account.py --account 1 -- \
  kernels output munimthahmid/qwen2-5-3b-benqa-extension-smoke26 \
  -p results/runs/qwen25_3b_benqa_ext_smoke26
```

Summary command used:

```bash
python3 scripts/summarize_outputs.py \
  results/runs/qwen25_3b_benqa_ext_smoke26 \
  --output results/analysis/qwen25_3b_benqa_ext_smoke26_summary.csv \
  --rescore
```

## Decision Rule

The smoke run has 78/78 rows, 0 parsed-empty rows, and no runtime/parser failure
pattern. Launch Qwen2.5-3B on
`data/slices/benqa_extended_1000_v1_ai_pass_pilot130.jsonl`.

Do not launch the 851-row full pass-only extension until the 130-row pilot
passes.
