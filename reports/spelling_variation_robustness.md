# Banglish Spelling-Variation Robustness

Updated: 2026-06-11

Each of 100 BEnQA items is evaluated under 5 spellings (canonical reviewed
Banglish plus 4 seeded phonetic respellings that preserve digits, formulae,
option labels, and the answer line). A flip means the model's correctness
is not constant across spellings of the same item.

- Summary: `results/analysis/spelling_variation_summary.csv`
- Builder: `scripts/analyze_spelling_variation.py`

| Model | Items | Acc % | Items with flip | Flip rate | All-correct | All-wrong | Mean swing |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 100 | 31.2 | 17 | 17.0% | 23 | 60 | 0.17 |
| Qwen3-4B | 100 | 29.0 | 6 | 6.0% | 26 | 68 | 0.06 |

## Per-spelling accuracy

| Model | spell0 | spell1 | spell2 | spell3 | spell4 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 31.0% | 28.0% | 29.0% | 34.0% | 34.0% |
| Qwen3-4B | 28.0% | 28.0% | 31.0% | 28.0% | 30.0% |
