# Frozen-V5 BEnQA Distractor-Transition Audit

Updated: 2026-06-11

## Scope

This no-spend audit extends the BEnQA choice-bias analysis by asking
what reviewed Banglish predicts when it is wrong even though Bangla or
English is correct. It uses only the frozen-v5 BEnQA MCQ rows and the
three thesis-facing Qwen models.

- Per-model item table: `results/analysis/v5_benqa_distractor_transition_items.csv`
- Cross-model item table: `results/analysis/v5_benqa_distractor_transition_item_consensus.csv`
- Summary table: `results/analysis/v5_benqa_distractor_transition_summary.csv`

## Headline

- Recoverable reviewed-Banglish BEnQA misses are almost always valid distractor choices: 162/164 valid, with 2 invalid choices.
- Qwen2.5 rows do not collapse to one distractor label: their most common recoverable wrong option is B, but it accounts for 21/51 and 19/58 recoverable misses.
- Qwen3-4B has a much sharper script-conditioned distractor mode: D is selected on 44/55 recoverable reviewed-Banglish misses.
- Cross-model convergence is nontrivial: 50 items have at least two valid recoverable Banglish misses, and 27 of them share the same wrong option across at least two models.
- 17 items have all three models making valid recoverable Banglish misses; 5 choose the same wrong option across all three models.

## Recoverable Misses By Model

| Model | Recoverable misses | Valid distractors | Invalid | Top wrong option | Pred A | Pred B | Pred C | Pred D |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 51 | 51 | 0 | B (21) | 10 | 21 | 8 | 12 |
| Qwen2.5-7B 8-bit | 58 | 56 | 2 | B (19) | 13 | 19 | 10 | 14 |
| Qwen3-4B | 55 | 55 | 0 | D (44) | 2 | 1 | 8 | 44 |

## Gold-To-Wrong Transitions

| Model | Gold | Recoverable misses | Pred A | Pred B | Pred C | Pred D | Invalid | Top wrong option |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Qwen2.5-3B | A | 14 | 0 | 7 | 3 | 4 | 0 | B (7) |
| Qwen2.5-3B | B | 12 | 5 | 0 | 4 | 3 | 0 | A (5) |
| Qwen2.5-3B | C | 14 | 2 | 7 | 0 | 5 | 0 | B (7) |
| Qwen2.5-3B | D | 11 | 3 | 7 | 1 | 0 | 0 | B (7) |
| Qwen2.5-7B 8-bit | A | 13 | 0 | 8 | 1 | 4 | 0 | B (8) |
| Qwen2.5-7B 8-bit | B | 13 | 5 | 0 | 4 | 4 | 0 | A (5) |
| Qwen2.5-7B 8-bit | C | 19 | 4 | 7 | 0 | 6 | 2 | B (7) |
| Qwen2.5-7B 8-bit | D | 13 | 4 | 4 | 5 | 0 | 0 | C (5) |
| Qwen3-4B | A | 14 | 0 | 0 | 4 | 10 | 0 | D (10) |
| Qwen3-4B | B | 17 | 0 | 0 | 2 | 15 | 0 | D (15) |
| Qwen3-4B | C | 20 | 1 | 0 | 0 | 19 | 0 | D (19) |
| Qwen3-4B | D | 4 | 1 | 1 | 2 | 0 | 0 | C (2) |

## Cross-Model Wrong-Option Convergence

| Bucket | Items | Repeated wrong option | All-three same wrong option |
| --- | ---: | ---: | ---: |
| `any_model_recoverable_valid` | 95/144 | 27 | 5 |
| `two_plus_models_recoverable_valid` | 50/144 | 27 | 5 |
| `three_models_recoverable_valid` | 17/144 | 12 | 5 |

## Interpretation

The BEnQA script gap is not mainly an MCQ parser artifact. When reviewed
Banglish loses items that Bangla or English can answer, it usually still
emits a valid option label. For Qwen2.5 models the wrong choices remain
distributed, so the gap cannot be reduced to a single label prior. For
Qwen3-4B, the reviewed-Banglish row has a sharp D-attractor failure mode,
which is itself a script-conditioned behavior.

The cross-model convergence counts show that some BEnQA items pull more
than one model toward the same wrong distractor under Banglish. Treat this
as behavioral evidence of script-conditioned distractor attraction, not as
a causal mechanism for internal representations.

## Reproducibility

- Builder: `scripts/analyze_v5_benqa_distractor_transition.py`
- Per-model item rows: 432
- Cross-model item rows: 144
- Summary rows: 20
