# v4 Banglish Sensitivity: Validation 200

Updated: 2026-05-28

## Purpose

v4 keeps the same item ids as validation-200 v3 but regenerates Banglish with
conservative artifact cleanup. The goal is to check whether text-quality fixes
change the measured Banglish accuracy.

## Qwen2.5-3B

Artifacts:

- `results/runs/qwen2_5_3b_validation200_v4_banglish/`
- `results/analysis/qwen25_validation200_v3_vs_v4_banglish_items_reparsed.csv`
- `results/analysis/qwen25_validation200_v3_vs_v4_banglish_summary_reparsed.csv`
- `results/analysis/qwen25_validation200_v4_minus_v3_banglish_bootstrap.csv`

Accuracy:

| Slice | Overall | BEnQA | BanglaMATH |
| --- | ---: | ---: | ---: |
| v3 Banglish | 38/200 | 38/144 | 0/56 |
| v4 Banglish | 39/200 | 39/144 | 0/56 |

Paired result:

- v4 minus v3: +0.5 points.
- 95% CI: [0, +1.5].
- Item flips: 1 BEnQA gain, 0 losses.

Gain inspection:

- `benqa_10th-Chemistry_0374`: v4 removes the `oja` artifact from answer
  options such as `ojalokohol`, and the model changes from `C` to the correct
  option `B`.

Interpretation:

- v4 cleanup improves a clear artifact without materially changing Qwen2.5's
  Banglish accuracy.
- The v3 Qwen2.5 script-gap conclusion is robust to this cleanup pass.

## Qwen3-4B

Artifacts:

- `results/runs/qwen3_4b_validation200_v4_banglish/`
- `results/analysis/qwen3_validation200_v3_vs_v4_banglish_items_reparsed.csv`
- `results/analysis/qwen3_validation200_v3_vs_v4_banglish_summary_reparsed.csv`
- `results/analysis/qwen3_validation200_v4_minus_v3_banglish_bootstrap.csv`

Accuracy:

| Slice | Overall | BEnQA | BanglaMATH |
| --- | ---: | ---: | ---: |
| v3 Banglish | 46/200 | 45/144 | 1/56 |
| v4 Banglish | 47/200 | 46/144 | 1/56 |

Paired result:

- v4 minus v3: +0.5 points.
- 95% CI: [-1.0, +2.5].
- Item flips: 2 BEnQA gains, 1 BEnQA loss.

Interpretation:

- v4 cleanup also does not materially change Qwen3's Banglish accuracy.
- The v3 Qwen3 script-gap conclusion is robust to this cleanup pass.

## Combined Takeaway

| Model | v3 Banglish | v4 Banglish | v4 - v3 |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 38/200 | 39/200 | +0.5 points |
| Qwen3-4B | 46/200 | 47/200 | +0.5 points |

The v4 cleanup is valuable for dataset quality but does not erase or materially
change the measured Banglish weakness. For thesis-facing results, v3 remains a
valid completed baseline, and v4 is a cleaner release candidate.
