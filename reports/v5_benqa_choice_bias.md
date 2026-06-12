# Frozen-V5 BEnQA Choice-Bias Audit

Updated: 2026-06-11

## Scope

This no-spend audit checks whether BEnQA MCQ losses are caused by
malformed option outputs or by a script-conditioned option-label bias.
It uses the frozen-v5 answer-format audit rows for the 144 BEnQA MCQs
and the three thesis-facing Qwen models.

- Item table: `results/analysis/v5_benqa_choice_bias_items.csv`
- Summary table: `results/analysis/v5_benqa_choice_bias_summary.csv`

The gold BEnQA option distribution is not collapsed: A=29, B=35, C=41,
and D=39.

## Option Distribution

| Model | Variant | Correct | Invalid | Pred A | Pred B | Pred C | Pred D | Majority | Entropy | TVD vs gold |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | Bangla | 49/144 | 0 | 23 | 45 | 31 | 45 | B (31.2%) | 0.97 | 0.11 |
| Qwen2.5-3B | Reviewed Banglish | 41/144 | 0 | 22 | 56 | 27 | 39 | B (38.9%) | 0.95 | 0.15 |
| Qwen2.5-3B | English | 66/144 | 0 | 28 | 43 | 29 | 44 | D (30.6%) | 0.98 | 0.09 |
| Qwen2.5-7B 8-bit | Bangla | 60/144 | 0 | 36 | 45 | 45 | 18 | B (31.2%) | 0.96 | 0.15 |
| Qwen2.5-7B 8-bit | Reviewed Banglish | 47/144 | 2 | 33 | 57 | 27 | 25 | B (39.6%) | 0.96 | 0.19 |
| Qwen2.5-7B 8-bit | English | 86/144 | 0 | 35 | 47 | 35 | 27 | B (32.6%) | 0.99 | 0.12 |
| Qwen3-4B | Bangla | 76/144 | 4 | 20 | 24 | 29 | 67 | D (46.5%) | 0.91 | 0.21 |
| Qwen3-4B | Reviewed Banglish | 47/144 | 3 | 3 | 7 | 20 | 111 | D (77.1%) | 0.50 | 0.51 |
| Qwen3-4B | English | 82/144 | 8 | 22 | 25 | 31 | 58 | D (40.3%) | 0.94 | 0.16 |

## Banglish Agreement With Other Scripts

| Model | Pair | Both valid | Same option | Different option | Left correct/right wrong | Right correct/left wrong |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | Bangla vs Reviewed Banglish | 144 | 70 | 74 | 23 | 15 |
| Qwen2.5-3B | English vs Reviewed Banglish | 144 | 63 | 81 | 40 | 15 |
| Qwen2.5-7B 8-bit | Bangla vs Reviewed Banglish | 142 | 63 | 79 | 30 | 19 |
| Qwen2.5-7B 8-bit | English vs Reviewed Banglish | 142 | 57 | 85 | 50 | 13 |
| Qwen3-4B | Bangla vs Reviewed Banglish | 139 | 79 | 60 | 37 | 8 |
| Qwen3-4B | English vs Reviewed Banglish | 136 | 66 | 70 | 48 | 11 |

## Interpretation

- MCQ format failure is not the main explanation: Qwen2.5-3B has no
  invalid BEnQA choices, Qwen2.5-7B has two invalid reviewed-Banglish
  choices, and Qwen3 has three invalid reviewed-Banglish choices.
- Qwen2.5 rows do not collapse to one Banglish option label. Their
  reviewed-Banglish majority shares are 38.9%
  for Qwen2.5-3B and 39.6%
  for Qwen2.5-7B.
- Qwen3-4B does show a real script-conditioned choice bias: reviewed
  Banglish predicts D on 111/144 rows (77.1%), while gold D appears on
  39/144 rows.
- The Qwen3 Banglish row scores 47/144, only 8 items above an always-D
  baseline, while Qwen3 Bangla and English score 76/144 and 82/144.
- Treat option-label bias as a discovered failure mode for Qwen3
  Banglish, not as a reason to dismiss the gap: Qwen2.5 gaps remain
  without one-label collapse, and Qwen3's collapse is itself
  script-conditioned behavior.

## Artifacts

- Builder: `scripts/analyze_v5_benqa_choice_bias.py`
- Item table: `results/analysis/v5_benqa_choice_bias_items.csv`
- Summary table: `results/analysis/v5_benqa_choice_bias_summary.csv`
