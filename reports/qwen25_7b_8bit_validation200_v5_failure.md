# Qwen2.5-7B 8-bit Validation-200 v5 Latest-Stack Failure

Updated: 2026-05-29

## Summary

The optional Qwen2.5-7B 8-bit clean-Banglish v5 rerun was launched after the
required Qwen2.5-3B and Qwen3-4B v5 reruns. The Kaggle kernel failed before
writing any evaluation rows.

## Artifacts

- Kernel: `munimthahmid/qwen2-5-7b-8-bit-validation-200-v5-banglish`
- Log: `results/runs/qwen25_7b_8bit_validation200_v5_banglish/qwen2-5-7b-8-bit-validation-200-v5-banglish.log`
- Output: `results/runs/qwen25_7b_8bit_validation200_v5_banglish/results/runs/qwen2_5_7b_8bit_validation200_v5_banglish.jsonl`

## Failure

- Output rows: 0.
- Kernel status: error.
- Failure point: first generation call.
- Backend error: `RuntimeError: cublasLt ran into an error!`
- Stack location: `bitsandbytes.int8_linear_matmul`.

This matches the known Kaggle P100/latest-stack 8-bit failure mode. Earlier
successful Qwen2.5-7B 8-bit validation-200 v4 runs used a pinned stack:

- `transformers==4.43.4`
- `accelerate==0.33.0`
- `bitsandbytes==0.43.3`

## Decision

The required post-v5 reruns are already complete and show only small changes
from v4 to v5:

- Qwen2.5-3B: 39/200 -> 41/200.
- Qwen3-4B: 47/200 -> 49/200.

Therefore this optional 7B v5 attempt is recorded as blocked, not as missing
primary evidence.

## Resolved Pinned Retry

The pinned-stack retry completed on 2026-05-30:

- Kernel:
  `munimthahmid/qwen2-5-7b-8-bit-validation-200-v5-banglish-pinned`
- Analysis:
  `results/analysis/qwen25_7b_8bit_validation200_v5_vs_v4_banglish.md`
- Result: v4 48/200 -> v5 47/200, -0.5 points, CI [-3.5, +2.5].

The latest-stack failure remains useful as an environment-reproducibility
note; the pinned result is the thesis-facing sensitivity row.
