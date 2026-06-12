# Qwen3-8B 8-bit Pilot20 Failure

Updated: 2026-05-28

## Purpose

This pilot tested whether `Qwen/Qwen3-8B` could run as a stronger Qwen3 scaling
point on Kaggle P100 using bitsandbytes 8-bit quantization and thinking disabled.

## Setup

- Model: `Qwen/Qwen3-8B`
- Slice: first 20 items from `data/slices/validation_200_v4_dev50.jsonl`
- Variants: Bangla, clean Banglish, English
- Prompt mode: baseline
- Thinking mode: disabled
- Max new tokens: 128
- GPU assigned by Kaggle: Tesla P100-PCIE-16GB, compute capability 6.0

## Attempts

| Attempt | Kernel | Result |
| --- | --- | --- |
| v1 | `munimthahmid/qwen3-8b-8bit-v4-dev50-p20` | Failed before rows: latest Transformers called `Qwen3ForCausalLM.set_submodule`, missing from the P100-compatible `torch==2.4.1` build. |
| v2 | `munimthahmid/qwen3-8b-8bit-v4-dev50-p20` | Compatibility shim fixed loading; all weights loaded, then first generation failed in bitsandbytes with `RuntimeError: cublasLt ran into an error`. |
| pinned bnb | `munimthahmid/qwen3-8b-8bit-v4-p20-bnb043` | Failed before loading because current Transformers requires `bitsandbytes>=0.46.1` for 8-bit quantization. |

No evaluation rows were produced.

## Decision

Do not spend full dev50 or test150 GPU on Qwen3-8B 8-bit under the current
Kaggle P100 stack. The model is not ruled out scientifically; it is blocked by
the available GPU/backend combination.

Useful follow-up only if compute changes:

- Retry on T4/L4/A100 with a current Torch + bitsandbytes stack.
- Or use an API/open-weight endpoint where Qwen3-8B can run without P100
  bitsandbytes constraints.

## Code Change Kept

`scripts/run_eval_kaggle.py` now includes a small compatibility shim that defines
`torch.nn.Module.set_submodule` when a quantized load needs it and the installed
Torch version does not provide it. This is useful for future P100 8-bit probes,
but it is not sufficient for Qwen3-8B generation on P100.

## Artifacts

- v1/v2 log directory:
  `results/runs/qwen3_8b_8bit_validation200_v4_dev50_pilot20/`
- v2 log/output directory:
  `results/runs/qwen3_8b_8bit_validation200_v4_dev50_pilot20_v2/`
- pinned-bitsandbytes log directory:
  `results/runs/qwen3_8b_8bit_validation200_v4_dev50_pilot20_bnb043/`
- Prepared job folders:
  `kaggle_jobs/qwen3_8b_8bit_validation200_v4_dev50_pilot20/`
  and `kaggle_jobs/qwen3_8b_8bit_v4_p20_bnb043/`
