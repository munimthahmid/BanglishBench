# Cross-Script Answer Agreement on Validation-200

Updated: 2026-05-28

Historical report. For the frozen-v5 reviewed-Banglish refresh, use
`reports/cross_script_diagnostics_validation200_v5.md`.

## Purpose

This analysis asks whether parsed-answer agreement across Bangla, clean
Banglish, and English can explain or recover Banglish failures.

This is not a deployable router because it uses the benchmark's parallel Bangla
and English versions. Its value is diagnostic: if the same model gives one
answer under Banglish but an agreed answer under Bangla and English, then the
Banglish failure is likely script-specific rather than an impossible item.

## Setup

Inputs:

- Qwen2.5-3B validation-200 v3 baseline.
- Qwen3-4B validation-200 v3 baseline.
- Qwen2.5-7B 8-bit validation-200 v4 baseline, combined from dev50 and test150.

Rules:

- Normalize parsed MCQ answers by option letter.
- Normalize short answers with the existing evaluator's compact answer
  normalization.
- `majority_vote`: use the answer if any two scripts agree; otherwise keep the
  clean Banglish answer.
- `bangla_english_agreement_route`: use the agreed Bangla/English answer when
  Bangla and English agree; otherwise keep the clean Banglish answer.

On these outputs, `majority_vote` and `bangla_english_agreement_route` have the
same totals because Banglish-matching pairs keep the Banglish answer, while the
only accuracy-changing pair is Bangla+English agreement against Banglish.

## Route-Level Result

| Model | Banglish baseline | Agreement route | Delta | 95% CI | Oracle |
| --- | ---: | ---: | ---: | --- | ---: |
| Qwen2.5-3B | 38/200 | 47/200 | +4.5 pts | [0.0, +9.0] | 99/200 |
| Qwen2.5-7B 8-bit | 48/200 | 71/200 | +11.5 pts | [+6.5, +17.0] | 114/200 |
| Qwen3-4B | 46/200 | 76/200 | +15.0 pts | [+9.5, +21.0] | 108/200 |

The agreement route recovers a meaningful subset of the oracle gain, especially
for Qwen3-4B and Qwen2.5-7B. This supports a future mitigation direction:
generate or retrieve alternate-script views, then trust Bangla/English agreement
when the Banglish answer diverges.

## Key Agreement Buckets

All-model overall buckets:

| Model | Bucket | n | Banglish correct | Agreement route correct | Oracle correct | Banglish wrong, other correct |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | Bangla+English agree, Banglish differs | 33 | 6 | 15 | 21 | 15 |
| Qwen2.5-7B 8-bit | Bangla+English agree, Banglish differs | 43 | 4 | 25 | 29 | 25 |
| Qwen3-4B | Bangla+English agree, Banglish differs | 51 | 4 | 34 | 38 | 34 |
| Qwen2.5-3B | All three different | 77 | 1 | 1 | 28 | 27 |
| Qwen2.5-7B 8-bit | All three different | 66 | 3 | 3 | 29 | 26 |
| Qwen3-4B | All three different | 49 | 1 | 1 | 10 | 9 |

Two patterns matter:

- When Bangla and English agree but Banglish differs, Banglish is usually wrong
  and the agreed answer often recovers accuracy.
- When all three scripts disagree, there is still large oracle headroom for
  Qwen2.5 models, but simple answer agreement cannot choose the right script.

## Interpretation

This result strengthens the mechanism story:

- The model often has access to the correct answer under another script.
- Banglish failures are not only low model competence; they can be inconsistent
  answer selection induced by script.
- Cross-script consistency is a concrete signal for future mitigation, but it
  needs a deployable way to obtain alternate-script views without using gold
  benchmark translations.

Thesis-safe framing:

- Use this as diagnostic and mitigation-design evidence.
- Do not present it as a fair deployed accuracy number.
- Pair it with the oracle and failure-taxonomy reports to argue that many
  Banglish misses are recoverable in principle.

## Artifacts

- Script:
  `scripts/analyze_cross_script_answer_agreement.py`
- Example exporter:
  `scripts/export_cross_script_agreement_examples.py`
- Qualitative examples:
  `reports/cross_script_answer_agreement_examples.md`
- Item output:
  `results/analysis/validation200_cross_script_answer_agreement_items.csv`
- Bucket summary:
  `results/analysis/validation200_cross_script_answer_agreement_buckets.csv`
- Route summary:
  `results/analysis/validation200_cross_script_answer_agreement_routes.csv`
