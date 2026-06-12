# Kaggle GPU Feasibility Notes

Updated: 2026-05-29

## Purpose

This note tracks which model/runtime combinations are feasible on the Kaggle GPU
sessions used for Script Matters. It prevents repeated spending on known-bad
stacks.

## Current GPU Reality

Kaggle has repeatedly assigned Tesla P100-PCIE-16GB GPUs with compute capability
6.0. This strongly shapes model choices:

- bitsandbytes 4-bit is not usable on P100/sm_60 in our stack.
- 8-bit can work for some 7B models, but depends heavily on the
  Transformers/bitsandbytes/Torch combination.
- Qwen3 larger models are harder than Qwen2.5 because current Transformers
  support pulls in newer bitsandbytes behavior that fails on P100.

## Feasible Or Completed

| Model | Mode | Status | Notes |
| --- | --- | --- | --- |
| Qwen2.5-0.5B | fp16 | complete | Useful only as weak/noisy scaling point. |
| Qwen2.5-1.5B | fp16 | complete | Feasible on P100. |
| Qwen2.5-3B | fp16 | complete | Main economical Qwen2.5 baseline/mitigation model. |
| Qwen3-1.7B | fp16, no-thinking | complete | Feasible; thinking must be disabled for answer-only evaluation. |
| Qwen3-4B-Instruct-2507 | fp16 | complete | Strongest P100-compatible Qwen3 baseline so far. |
| Qwen2.5-7B-Instruct | 8-bit | complete | Feasible with `transformers==4.43.4`, `accelerate==0.33.0`, `bitsandbytes==0.43.3`. |
| Phi-3.5-mini | fp16 | complete | Useful non-Qwen breadth point. |
| Indic-Gemma-2B Navarasa | fp16 | diagnostic | Feasible and parseable with Alpaca wrapper, but pilot20 was around chance. |

## Blocked Or Diagnostic

| Model | Mode | Status | Cause |
| --- | --- | --- | --- |
| Qwen3-8B | 4-bit | blocked | Guarded out on P100 because 4-bit bitsandbytes is not supported. |
| Qwen3-8B | 8-bit | blocked | Shim fixes `set_submodule`; current bitsandbytes fails with `cublasLt`; older bitsandbytes is rejected by current Transformers. |
| Phi-4-mini | fp16 | blocked | Transformers/Torch compatibility issue around `SlidingWindowCache`. |
| BanglaLLM/Bangla-s1k-qwen-2.5-3B-Instruct | fp16 | diagnostic | Outputs remain degenerate under current prompt/template. |
| TituLM Llama-3.2-3B v2.0 | fp16 | diagnostic | Current prompt yields unrelated prose/zero-score pilot. |

## Latest Pilot Result

| Model | Mode | Status | Notes |
| --- | --- | --- | --- |
| Mistral-7B-Instruct-v0.3 | 8-bit | diagnostic | Pilot20 completed with Bangla 3/20, Banglish 4/20, English 4/20, but was slow at about 30 seconds per generation. Do not run full dev/test unless this family becomes a specific priority. |
| Indic-Gemma-2B Navarasa | fp16 | diagnostic | Pilot20 completed with Bangla 4/20, Banglish 3/20, English 5/20, parsed-empty 0. Do not run dev50 now. |

## Post-v5 Compute Budget

Current budget report:

- `reports/post_v5_compute_budget.md`
- `results/analysis/post_v5_compute_budget.csv`

Under the working assumption of four Kaggle accounts with 30 GPU-hours each,
the required post-v5 clean-Banglish reruns are not compute-limited:

- Required Qwen2.5-3B plus Qwen3-4B reruns, conservative: 0.89 GPU-hours.
- Required plus conditional Qwen2.5-7B 8-bit rerun, conservative: 1.51
  GPU-hours.

The active blocker is therefore not GPU-hour availability. The blocker is the
manual v5 review/freeze/readiness path.

## Decision Rules

- Do not launch post-v5 jobs while `reports/post_v5_kaggle_job_plan.md` is
  `not_ready`.
- Do not retry Qwen3-8B on P100 without a materially different backend plan.
- Do not run 4-bit jobs unless Kaggle assigns T4/L4/A100.
- Use pilot20 before any new 7B-class full dev/test run.
- Prefer full dev50/test150 only after model loading, answer format, and runtime
  are proven on pilot20.
- Keep Qwen2.5-7B as the main successful 7B P100 scaling point.
