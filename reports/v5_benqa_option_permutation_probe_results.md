# Frozen-V5 BEnQA Option-Permutation Results

Updated: 2026-06-11

## Scope

This controlled dev-only audit rotates the semantic option content across
labels A/B/C/D for 36 reviewed-v5 BEnQA MCQs. It asks whether model
predictions follow the option content or remain attached to label D.

- Probe items: `data/slices/validation200_v5_dev50_benqa_option_permutations.jsonl`
- Item analysis: `results/analysis/v5_benqa_option_permutation_probe_items.csv`
- Summary analysis: `results/analysis/v5_benqa_option_permutation_probe_summary.csv`
- `Qwen3-4B` output: `results/runs/qwen3_4b_v5_benqa_option_permutation_dev50/results/runs/qwen3_4b_v5_benqa_option_permutation_dev50.jsonl`
- `Qwen2.5-3B` output: `results/runs/qwen25_3b_v5_benqa_option_permutation_dev50/results/runs/qwen25_3b_v5_benqa_option_permutation_dev50.jsonl`

## Headline

| Model | Identity D predictions | Rotated rows from identity-D items | Remain label D | Follow original D content | Semantic match vs identity | Exact semantic-equivariant items |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 11/36 | 33 | 10 (30.3%) | 15 (45.5%) | 39/108 | 4/36 |
| Qwen3-4B | 26/36 | 78 | 60 (76.9%) | 9 (11.5%) | 19/108 | 2/36 |

Identity wrong-D subset:

| Model | Identity wrong-D items | Rotated rows | Remain label D | Follow original D content |
| --- | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 7 | 21 | 5 (23.8%) | 12 (57.1%) |
| Qwen3-4B | 15 | 45 | 35 (77.8%) | 6 (13.3%) |

## Rotation Breakdown

| Model | Shift | Correct | Pred D | Wrong D | Selected original-D content |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 0 | 9/36 | 11/36 | 7/36 | 11/36 |
| Qwen2.5-3B | 1 | 7/36 | 7/36 | 5/36 | 11/36 |
| Qwen2.5-3B | 2 | 5/36 | 11/36 | 10/36 | 13/36 |
| Qwen2.5-3B | 3 | 11/36 | 9/36 | 9/36 | 8/36 |
| Qwen3-4B | 0 | 15/36 | 26/36 | 15/36 | 26/36 |
| Qwen3-4B | 1 | 11/36 | 22/36 | 15/36 | 1/36 |
| Qwen3-4B | 2 | 7/36 | 29/36 | 24/36 | 2/36 |
| Qwen3-4B | 3 | 10/36 | 28/36 | 20/36 | 6/36 |

## Interpretation

- Label-D persistence after content rotation is behavioral evidence for
  a positional D-attractor.
- Original-D-content persistence after rotation is behavioral evidence
  for semantic distractor tracking.
- This is a controlled dev-only audit. It strengthens mechanism
  discussion but does not prove an internal causal mechanism or support
  a held-out mitigation claim.
