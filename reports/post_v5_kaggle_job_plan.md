# Post-v5 Kaggle Job Plan

Updated: 2026-06-11

Readiness status: `ready`

Compute budget companion: `reports/post_v5_compute_budget.md`

The required v5 review and freeze gates pass. Prepare jobs in priority order.

## Planned Jobs

| Priority | Run id | Model | Variant | Quantization | Status | Condition |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | `qwen25_3b_validation200_v5_banglish` | `Qwen/Qwen2.5-3B-Instruct` | `banglish_clean` | `none` | `ready_to_prepare` | `required_after_readiness` |
| 2 | `qwen3_4b_validation200_v5_banglish` | `Qwen/Qwen3-4B-Instruct-2507` | `banglish_clean` | `none` | `ready_to_prepare` | `required_after_readiness` |
| 3 | `qwen25_7b_8bit_validation200_v5_banglish` | `Qwen/Qwen2.5-7B-Instruct` | `banglish_clean` | `8-bit` | `conditional_manual_decision` | `conditional_if_v5_changes_main_table_or_7b_remains_primary` |

## Packaging Commands

### 1. `qwen25_3b_validation200_v5_banglish`

Status: `ready_to_prepare`

```bash
python3 scripts/prepare_kaggle_model_run.py --account 1 --model Qwen/Qwen2.5-3B-Instruct --dataset-slug validation-200-v5-assets --dataset-title "Validation 200 v5 assets" --items-path data/slices/validation_200_v5.jsonl --assets-job-name validation_200_v5_assets_account1 --job-name qwen25_3b_validation200_v5_banglish --kernel-slug qwen25-3b-validation200-v5-banglish --title "Qwen2.5 3B validation-200 v5 Banglish" --output-name qwen2_5_3b_validation200_v5_banglish --limit 0 --variants banglish_clean --max-new-tokens 128
```

### 2. `qwen3_4b_validation200_v5_banglish`

Status: `ready_to_prepare`

```bash
python3 scripts/prepare_kaggle_model_run.py --account 1 --model Qwen/Qwen3-4B-Instruct-2507 --dataset-slug validation-200-v5-assets --dataset-title "Validation 200 v5 assets" --items-path data/slices/validation_200_v5.jsonl --assets-job-name validation_200_v5_assets_account1 --job-name qwen3_4b_validation200_v5_banglish --kernel-slug qwen3-4b-validation200-v5-banglish --title "Qwen3 4B validation-200 v5 Banglish" --output-name qwen3_4b_validation200_v5_banglish --limit 0 --variants banglish_clean --max-new-tokens 128 --disable-thinking
```

### 3. `qwen25_7b_8bit_validation200_v5_banglish`

Status: `conditional_manual_decision`

```bash
python3 scripts/prepare_kaggle_model_run.py --account 1 --model Qwen/Qwen2.5-7B-Instruct --dataset-slug validation-200-v5-assets --dataset-title "Validation 200 v5 assets" --items-path data/slices/validation_200_v5.jsonl --assets-job-name validation_200_v5_assets_account1 --job-name qwen25_7b_8bit_validation200_v5_banglish --kernel-slug qwen25-7b-8bit-validation200-v5-banglish --title "Qwen2.5 7B 8-bit validation-200 v5 Banglish" --output-name qwen2_5_7b_8bit_validation200_v5_banglish --limit 0 --variants banglish_clean --max-new-tokens 128 --load-in-8bit
```

## Launch Rule

Only run a packaging command after:

1. `python3 scripts/validate_banglish_review_queue.py --require-complete` passes.
2. `scripts/apply_banglish_review.py` creates `data/slices/validation_200_v5.jsonl`.
3. `scripts/audit_banglish_artifacts.py` creates the v5 artifact audit files.
4. `python3 scripts/check_post_v5_rerun_readiness.py` reports `ready`.
