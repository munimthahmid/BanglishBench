# Qwen3-1.7B No-Thinking Validation-200 v4

Updated: 2026-05-28 13:52 +0600

This report summarizes Qwen3-1.7B after disabling Qwen3 thinking mode. The
default-thinking run is treated as diagnostic only because it produced mostly
truncated `<think>` outputs.

## Runs

Diagnostic default-thinking dev50:

- Kernel: `munimthahmid/qwen3-1-7b-validation200-v4-dev50`
- Result: Bangla 1/50, Banglish 0/50, English 1/50
- Problem: truncated thinking traces, high parsed-empty rate

Corrected no-thinking dev50:

- Kernel: `munimthahmid/qwen3-1-7b-nothink-validation200-v4-dev50`
- Output: `results/runs/qwen3_1_7b_nothink_validation200_v4_dev50/results/runs/qwen3_1_7b_nothink_validation200_v4_dev50.jsonl`

Corrected no-thinking test150:

- Kernel: `munimthahmid3/qwen3-1-7b-nothink-validation200-v4-test150`
- Output: `results/runs/qwen3_1_7b_nothink_validation200_v4_test150/results/runs/qwen3_1_7b_nothink_validation200_v4_test150.jsonl`

## Results

Split results:

| Split | Bangla | Banglish | English |
| --- | ---: | ---: | ---: |
| Dev50 | 11/50 | 11/50 | 20/50 |
| Test150 | 23/150 | 25/150 | 41/150 |
| Full200 | 34/200 | 36/200 | 61/200 |

By dataset, full200:

| Dataset | Bangla | Banglish | English |
| --- | ---: | ---: | ---: |
| BEnQA | 30/144 | 36/144 | 56/144 |
| BanglaMATH | 4/56 | 0/56 | 5/56 |

## Paired Bootstrap

| Comparison | Delta | 95% CI |
| --- | ---: | ---: |
| Banglish - Bangla | +1 point | [-6, +7.5] |
| Banglish - English | -12.5 points | [-20, -5] |

Artifacts:

- `results/analysis/qwen3_1_7b_nothink_validation200_v4_banglish_minus_bangla_bootstrap.csv`
- `results/analysis/qwen3_1_7b_nothink_validation200_v4_banglish_minus_english_bootstrap.csv`

## Interpretation

- Qwen3-1.7B no-thinking is informative but substantially weaker than Qwen3-4B.
- It does not show a Banglish-below-Bangla gap on validation-200 v4.
- It does show a clear Banglish-vs-English gap.
- This strengthens the scaling interpretation: the robust Banglish-below-Bangla
  effect appears after enough Bangla/task competence, not merely from belonging
  to the Qwen3 family.
- BEnQA carries all clean Banglish signal for this model; BanglaMATH remains too
  hard, with Banglish at 0/56.

## Pipeline Lesson

For Qwen3-family models that default to thinking traces, use
`--disable-thinking` in this evaluation protocol. Otherwise the model may spend
the 128-token budget on hidden/reasoning text and fail to emit a parseable final
answer.

## Generated Artifacts

- `results/runs/qwen3_1_7b_nothink_validation200_v4_dev50/summary_by_variant_reparsed_rescored.csv`
- `results/runs/qwen3_1_7b_nothink_validation200_v4_dev50/summary_by_dataset_variant_reparsed_rescored.csv`
- `results/runs/qwen3_1_7b_nothink_validation200_v4_test150/summary_by_variant_reparsed_rescored.csv`
- `results/runs/qwen3_1_7b_nothink_validation200_v4_test150/summary_by_dataset_variant_reparsed_rescored.csv`
- `results/runs/qwen3_1_7b_nothink_validation200_v4_full200_by_variant_reparsed_rescored.csv`
- `results/runs/qwen3_1_7b_nothink_validation200_v4_full200_by_dataset_variant_reparsed_rescored.csv`
- `results/analysis/qwen3_1_7b_nothink_validation200_v4_devtest_by_split_variant_reparsed_rescored.csv`
- `results/analysis/qwen3_1_7b_nothink_validation200_v4_devtest_by_split_dataset_variant_reparsed_rescored.csv`
