# Noisy Banglish: Validation 200 v3

Updated: 2026-05-28

## Purpose

This run checks whether deterministic noisy Banglish makes the already observed
clean-Banglish gap worse on the larger 200-item validation slice.

## Qwen2.5-3B

Artifacts:

- `results/runs/qwen2_5_3b_validation200_v3_noisy/`
- `results/analysis/qwen25_validation200_v3_clean_vs_noisy_items_reparsed.csv`
- `results/analysis/qwen25_validation200_v3_clean_vs_noisy_summary_reparsed.csv`
- `results/analysis/qwen25_validation200_v3_noisy_minus_clean_bootstrap.csv`

Accuracy:

| Variant | Overall | BEnQA | BanglaMATH |
| --- | ---: | ---: | ---: |
| Clean Banglish | 38/200 | 38/144 | 0/56 |
| Noisy Banglish | 41/200 | 41/144 | 0/56 |

Paired result:

- Noisy minus clean: +1.5 points.
- 95% CI: [0, +3.5].
- Item flips: 3 BEnQA gains, 0 losses.

Gain inspection:

- `benqa_10th-Biology_0149`: noisy changes `bhesel` to `vesel`, likely making
  the biology term easier.
- `benqa_12th-Biology-II_0287`: noisy changes `ongsh` to `ongs`, but the gain
  may be sampling/format sensitivity because the key technical term remains
  awkward.
- `benqa_8th-Science_0042`: noisy changes `ksharok` to `ksarok`; this may make
  the option less formal but not necessarily more natural.

Interpretation:

- Qwen2.5 does not show evidence of additional sensitivity to this deterministic
  noise generator on validation-200.
- The small positive shift should not be overinterpreted as real-world noisy
  Banglish robustness. It may partly reflect the noise rules replacing formal
  transliteration with simpler Latin spellings.

## Qwen3-4B

Artifacts:

- `results/runs/qwen3_4b_validation200_v3_noisy/`
- `results/analysis/qwen3_validation200_v3_clean_vs_noisy_items_reparsed.csv`
- `results/analysis/qwen3_validation200_v3_clean_vs_noisy_summary_reparsed.csv`
- `results/analysis/qwen3_validation200_v3_noisy_minus_clean_bootstrap.csv`

Accuracy:

| Variant | Overall | BEnQA | BanglaMATH |
| --- | ---: | ---: | ---: |
| Clean Banglish | 46/200 | 45/144 | 1/56 |
| Noisy Banglish | 46/200 | 45/144 | 1/56 |

Paired result:

- Noisy minus clean: 0 points.
- 95% CI: [-1.5, +1.5].
- Item flips: 1 BEnQA gain, 1 BEnQA loss.

Interpretation:

- Qwen3 also shows no meaningful clean-vs-noisy difference under this
  deterministic noise generator.

## Combined Takeaway

| Model | Clean Banglish | Noisy Banglish | Noisy - Clean |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 38/200 | 41/200 | +1.5 points |
| Qwen3-4B | 46/200 | 46/200 | 0 points |

The larger validation-200 result suggests that the main benchmark phenomenon is
not sensitivity to the current synthetic noise rules. The primary gap is already
present in clean Latin-script Banglish.
