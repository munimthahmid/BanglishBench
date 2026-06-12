# Open-Model Next Experiment Plan

Updated: 2026-05-28

The next GPU run should improve model-family breadth without spending a full
validation budget blindly. The current best choice is a dev-only probe of
`microsoft/Phi-4-mini-instruct` on validation-200 v4 dev50.

## Candidate Review

| Candidate | Why Consider It | Risk | Decision |
| --- | --- | --- | --- |
| `microsoft/Phi-4-mini-instruct` | 3.8B dense instruction model, MIT license, strong compact reasoning target, non-Qwen family. Hugging Face model card: <https://huggingface.co/microsoft/Phi-4-mini-instruct> | Supported-language list does not visibly include Bengali, so Bangla/Banglish may be weak. | Run dev50 all-script probe. |
| `microsoft/Phi-3.5-mini-instruct` | 3.8B predecessor with stable Transformers support. Hugging Face model card: <https://huggingface.co/microsoft/Phi-3.5-mini-instruct> | Older and language list also does not include Bengali. | Keep as fallback if Phi-4-mini fails. |
| `CohereLabs/aya-expanse-8b` | Multilingual research model with 8B parameters. Hugging Face model card: <https://huggingface.co/CohereLabs/aya-expanse-8b> | 8B is heavier for Kaggle; model card lists 23 supported languages but not Bengali; non-commercial license. | Defer. |
| `sarvamai/sarvam-1` | Indic model explicitly optimized for Bengali among 10 Indic languages. Hugging Face model card: <https://huggingface.co/sarvamai/sarvam-1> | Base text-completion model, not instruction-tuned; likely unfair in our direct QA prompt. | Do not use as direct QA baseline. |

## Run Specification

Purpose:

- Test whether the clean Banglish gap appears outside the Qwen family.
- Follow the dev/test discipline: run dev50 first, inspect competence, and only
  run test150 if the dev result is informative.

Initial run:

- Model: `microsoft/Phi-4-mini-instruct`
- Slice: `data/slices/validation_200_v4_dev50.jsonl`
- Variants: `bangla`, `banglish_clean`, `english`
- Prompt mode: `baseline`
- Max new tokens: 128
- Quantization: none initially, because the model is 3.8B and Qwen3-4B already
  ran without 4-bit in the same pipeline.
- Expected generations: 150

Success criteria for test150:

- If English accuracy is above roughly 30 percent and at least one Bangla or
  Banglish script is non-trivial, run the unchanged baseline on test150.
- If Bangla and Banglish are both near zero while English is usable, keep the run
  as a negative model-family probe and do not spend test GPU.
- If the job fails due model-loading issues, try `microsoft/Phi-3.5-mini-instruct`
  as the fallback dev50 probe.

## Planned Artifacts

- Kaggle asset dataset: `validation-200-v4-dev50-assets`
- Kaggle kernel: `phi4-mini-validation200-v4-dev50`
- Local run directory after download:
  `results/runs/phi4_mini_validation200_v4_dev50/`
- Summary:
  `results/runs/phi4_mini_validation200_v4_dev50/summary_by_variant_reparsed_rescored.csv`
- Report:
  `reports/phi4_mini_dev50_probe.md`

## Execution Update

Phi-4-mini was submitted as planned but failed before evaluation rows were
produced on the Kaggle P100 stack:

- Kernel: `munimthahmid/phi4-mini-validation200-v4-dev50`
- Local log: `results/runs/phi4_mini_validation200_v4_dev50/phi4-mini-validation200-v4-dev50.log`
- Error: `ImportError: cannot import name 'SlidingWindowCache' from
  'transformers.cache_utils'`

This repeats the earlier Phi-4-mini pilot blocker. The fallback run is now:

- Model: `microsoft/Phi-3.5-mini-instruct`
- Kaggle asset dataset: `validation-200-v4-dev50-phi35-assets`
- Kaggle kernel: `phi35-mini-validation200-v4-dev50`
- Local run directory after download:
  `results/runs/phi35_mini_validation200_v4_dev50/`
- Fallback asset requirements pin `transformers==4.43.4` and
  `accelerate==0.33.0`.

Fallback dev50 result:

- Report: `reports/phi35_mini_dev50_probe.md`
- Phi-3.5-mini dev50 scored Bangla 5/50, Banglish 7/50, English 19/50.
- Because the result is informative and non-degenerate, the unchanged test150
  run was submitted:
  - Kernel: `munimthahmid3/phi35-mini-validation200-v4-test150`
  - Expected output directory:
    `results/runs/phi35_mini_validation200_v4_test150/`

Fallback test150 completed:

- Report: `reports/phi35_mini_validation200_v4.md`
- Test150: Bangla 33/150, Banglish 33/150, English 61/150.
- Full200: Bangla 38/200, Banglish 40/200, English 80/200.
- Conclusion: no Banglish-below-Bangla gap for Phi-3.5-mini, but a large
  Banglish-vs-English gap remains.

## Current Follow-Up Result

Qwen2.5-7B-Instruct completed on validation-200 v4 with bitsandbytes 8-bit
loading:

- Dev kernel: `munimthahmid/qwen25-7b-8bit-validation200-v4-dev50`
- Test kernel: `munimthahmid3/qwen25-7b-8bit-validation200-v4-test150`
- Slice: `data/slices/validation_200_v4.jsonl` via dev50/test150.
- Variants: Bangla, clean Banglish, English.
- Prompt mode: baseline.
- Max new tokens: 128.
- Quantization: bitsandbytes 8-bit.
- Report: `reports/qwen25_7b_8bit_validation200_v4.md`

Result:

- Full200: Bangla 65/200, clean Banglish 48/200, English 94/200.
- Banglish minus Bangla: -8.5 points, CI [-15.5, -1.5].
- Banglish minus English: -23 points, CI [-30.5, -15.5].

Operational note:

- The first dev attempt failed with latest Transformers on the Torch 2.4.1 P100
  stack.
- The successful package pins were `transformers==4.43.4`,
  `accelerate==0.33.0`, and `bitsandbytes==0.43.3`.

## Latest Feasibility Update

Qwen3-8B and Mistral-7B were checked before spending another full dev/test run:

- `Qwen/Qwen3-8B` 8-bit pilot20 is blocked on Kaggle P100. A compatibility shim
  fixes the missing `set_submodule` method, but generation fails with a
  bitsandbytes `cublasLt` error; pinning older bitsandbytes is rejected by the
  current Transformers 8-bit loader.
- `mistralai/Mistral-7B-Instruct-v0.3` 8-bit pilot20 completes, but is weak and
  slow: Bangla 3/20, Banglish 4/20, English 4/20, around 30 seconds per
  generation.

Current active pilot:

- Model: `Telugu-LLM-Labs/Indic-gemma-2b-finetuned-sft-Navarasa-2.0`
- Kernel: `munimthahmid3/indic-gemma2b-v4-dev50-p20`
- Rationale: small Bengali-tagged Indic Gemma instruction model; cheap
  model-family breadth probe.
- Prompt wrapper: `alpaca`, matching the model card's `### Instruction`,
  `### Input`, `### Response` format.
- Decision rule: if pilot20 shows non-degenerate answer-only behavior and at
  least one script above chance, run dev50. Otherwise keep it as a negative
  compatibility/model-family probe.

Result:

- Report: `reports/indic_gemma2b_pilot20_validation200_v4.md`
- Pilot20 completed with no parsed-empty failures.
- Accuracy was too low to scale: Bangla 4/20, Banglish 3/20, English 5/20.
- Decision: keep as diagnostic only; do not launch dev50.
