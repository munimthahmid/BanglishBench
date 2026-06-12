# Bangla-Specialized Model Pilots

Updated: 2026-05-28

## Purpose

Bangla-specialized open models are attractive for this thesis because they test
whether Bangla-focused tuning improves native Bangla, Latin-script Banglish, or
both. The current evidence is diagnostic, not yet a clean model-family result.

## Existing BanglaLLM Run: Invalid As Baseline

Model:

- `BanglaLLM/Bangla-s1k-qwen-2.5-3B-Instruct`

Run:

- Slice: validation-100 v3.
- Variants: Bangla, clean Banglish, English.
- Max new tokens: 64.
- Output directory:
  `results/runs/banglallm_qwen2_5_3b_validation100_v3/`

Summary:

| Variant | Correct | Parsed empty |
| --- | ---: | ---: |
| Bangla | 0/100 | 60 |
| Clean Banglish | 0/100 | 58 |
| English | 3/100 | 51 |

Reason not to cite as a normal baseline:

- Outputs frequently begin with `think` traces and do not follow the answer-only
  protocol.
- BEnQA parsing is mostly empty; BanglaMATH parsing often captured `think`
  rather than a final answer.
- The result measures runtime/prompt incompatibility more than model knowledge.

## Existing TituLM Pilot: Negative Diagnostic

Model:

- `hishab/titulm-llama-3.2-3b-v2.0`

Run:

- Slice: validation-100 v3 pilot20.
- Variants: Bangla, clean Banglish, English.
- Output directory:
  `results/runs/titulm_3b_validation100_v3_pilot20/`

Summary:

| Dataset | Bangla | Clean Banglish | English |
| --- | ---: | ---: | ---: |
| BEnQA pilot12 | 0/12 | 0/12 | 0/12 |
| BanglaMATH pilot8 | 0/8 | 0/8 | 0/8 |

Reason not to scale now:

- Example outputs are generic Bengali prose unrelated to the prompt.
- The model did not produce parseable answer-only behavior on the pilot.

## BanglaLLM No-Thinking Dev50 Retry

The useful next diagnostic was a small BanglaLLM no-thinking dev50 rerun:

- Kernel:
  `munimthahmid/banglallm-qwen25-3b-nothink-validation200-v4-dev50`
- Slice: `data/slices/validation_200_v4_dev50.jsonl`
- Variants: Bangla, clean Banglish, English.
- Max new tokens: 128.
- Runtime flag: `--disable-thinking`.
- Output directory:
  `results/runs/banglallm_qwen25_3b_nothink_validation200_v4_dev50/`

Result:

| Variant | Correct | Parsed empty |
| --- | ---: | ---: |
| Bangla | 0/50 | 36 |
| Clean Banglish | 1/50 | 34 |
| English | 3/50 | 29 |

All 150 raw outputs started with a `think` prefix despite the
`--disable-thinking` run flag.

Dataset split:

| Dataset | Bangla | Clean Banglish | English |
| --- | ---: | ---: | ---: |
| BEnQA dev36 | 0/36 | 1/36 | 3/36 |
| BanglaMATH dev14 | 0/14 | 0/14 | 0/14 |

Interpretation:

- `--disable-thinking` did not make this checkpoint comply with the answer-only
  protocol; outputs still frequently start with `think`.
- The dev result is degenerate relative to base Qwen2.5-3B and Qwen2.5-7B.
- Do not spend test150 GPU on this model under the current prompt/runtime.

Decision rule:

- Abandon BanglaLLM as a direct answer-only baseline for now.
- Reconsider only if we build a model-specific prompt/template fix and validate
  it on dev50 first.

## Thesis Use

These pilots support an operational caution: Bangla-specialized model labels are
not enough. A model must also satisfy the same answer-only protocol before it is
useful for script-gap measurement.
