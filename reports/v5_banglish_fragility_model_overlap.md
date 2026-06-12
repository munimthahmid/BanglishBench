# Frozen-V5 Fragility Model-Overlap Analysis

Updated: 2026-06-11

## Scope

This no-spend analysis separates one-model Banglish fragility from
fragility shared across the three thesis-facing Qwen rows. A fragility
event means reviewed Banglish is wrong while Bangla or English is correct
for the same model and item.

- Item-level overlap: `results/analysis/v5_banglish_fragility_model_overlap_items.csv`
- Machine-readable summary: `results/analysis/v5_banglish_fragility_model_overlap_summary.csv`
- Source: `results/analysis/v5_banglish_fragility_items.csv`

## Overall Overlap

- Items with at least one fragile model: 108/200 (54.0%)
- Exactly one fragile model: 52/200 (26.0%)
- Exactly two fragile models: 35/200 (17.5%)
- All three models fragile: 21/200 (10.5%)
- Shared fragility among any-fragile items: 56/108 (51.9%)
- Strict all-three Bangla+English-correct/Banglish-wrong items: 5/200 (2.5%)

## Model Totals

| Model | Fragile items | Strict items | Unique fragile items |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 58/200 | 15/200 | 14/58 |
| Qwen2.5-7B 8-bit | 68/200 | 29/200 | 22/68 |
| Qwen3-4B | 59/200 | 32/200 | 16/59 |

## Pairwise Overlap

| Model pair | Shared fragile items | Union | Jaccard | Shared strict items | Strict union | Strict Jaccard |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B + Qwen2.5-7B 8-bit | 34 | 92 | 0.370 | 7 | 37 | 0.189 |
| Qwen2.5-3B + Qwen3-4B | 31 | 86 | 0.360 | 7 | 40 | 0.175 |
| Qwen2.5-7B 8-bit + Qwen3-4B | 33 | 94 | 0.351 | 13 | 48 | 0.271 |

## Dataset Buckets

| Dataset | No model | Exactly one | Exactly two | All three | Shared two or more |
| --- | ---: | ---: | ---: | ---: | ---: |
| banglamath | 43 | 8 | 2 | 3 | 5/56 |
| benqa | 49 | 44 | 33 | 18 | 51/144 |

## Highest Shared-Fragility Dataset-Domains

This table separates BanglaMATH and BEnQA rows before ranking domains.

| Dataset:domain | Shared-fragile items | Items | Any fragile / all three |
| --- | ---: | ---: | --- |
| benqa:biology-i | 6 | 11 | any_fragile=10; all_three=3 |
| benqa:chemistry-ii | 6 | 11 | any_fragile=9; all_three=1 |
| benqa:math | 6 | 11 | any_fragile=9; all_three=3 |
| benqa:biology-ii | 5 | 11 | any_fragile=9; all_three=2 |
| benqa:chemistry | 5 | 11 | any_fragile=6; all_three=2 |
| benqa:chemistry-i | 5 | 11 | any_fragile=7; all_three=2 |
| benqa:biology | 5 | 12 | any_fragile=10; all_three=2 |
| banglamath:math | 5 | 56 | any_fragile=13; all_three=3 |

Merged-domain view for continuity:

| Domain | Shared-fragile items | Items | Any fragile / all three |
| --- | ---: | ---: | --- |
| math | 11 | 67 | any_fragile=22; all_three=6 |
| biology-i | 6 | 11 | any_fragile=10; all_three=3 |
| chemistry-ii | 6 | 11 | any_fragile=9; all_three=1 |
| biology-ii | 5 | 11 | any_fragile=9; all_three=2 |
| chemistry | 5 | 11 | any_fragile=6; all_three=2 |
| chemistry-i | 5 | 11 | any_fragile=7; all_three=2 |
| biology | 5 | 12 | any_fragile=10; all_three=2 |
| science | 4 | 11 | any_fragile=8; all_three=2 |

## Interpretation

- Shared fragility is common enough to treat Banglish fragility as more
  than isolated model noise: over half of any-fragile items affect at
  least two thesis-facing Qwen rows.
- Model-specific fragility still matters: 52 items affect exactly one
  model, so item-level examples should avoid implying every failure is
  universal across the Qwen family.
- Strict all-three failures are rarer, but the five such items are the
  cleanest shared script-specific failures because Bangla and English
  both succeed for every thesis-facing Qwen row.
- The overlap analysis is descriptive failure analysis, not a causal
  feature attribution or deployable routing rule.
