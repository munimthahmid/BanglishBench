# V5 Difficulty-Conditioned Script Gap

Updated: 2026-06-11

This no-spend audit asks whether the reviewed-Banglish deficit is
concentrated only in globally hard items. It reuses the frozen-v5
three-model item-consensus table and buckets each item by how many Qwen
rows answer the same item correctly in English, native Bangla, or the
best non-Banglish alternate script.

## Inputs And Outputs

- Input item consensus: `results/analysis/v5_item_consensus_items.csv`
- Item-level output: `results/analysis/v5_difficulty_conditioned_gap_items.csv`
- Summary table: `results/analysis/v5_difficulty_conditioned_gap_summary.csv`

## Headline

- The Banglish deficit grows, rather than disappears, on items with
  stronger alternate-script consensus.
- In the all-200 English-consensus=3 bucket, reviewed Banglish has 50/147 correct model-item slots versus Bangla 92/147 (-28.6 pts, CI [-38.8,-18.4]).
- In the all-200 English-consensus=2 bucket, reviewed Banglish has 36/108 versus Bangla 49/108 (-12.0 pts, CI [-22.2,-1.8]).
- On BEnQA items with English consensus=3, reviewed Banglish has 50/138 versus Bangla 84/138 (-24.6 pts, CI [-34.8,-15.2]).
- In the all-200 best-alternate-consensus=3 bucket, reviewed Banglish has 60/162 versus Bangla 107/162 (-29.0 pts, CI [-38.3,-19.8]).

## English-Consensus Buckets

The bucket value is the number of thesis-facing Qwen rows that answer the
English version correctly. This avoids using Banglish itself to define
the difficulty bucket.

### All 200 Items

| Bucket | Items | Bangla slots | Reviewed Banglish slots | English slots | Banglish - Bangla |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 81 | 30/243 (12.3%) | 26/243 (10.7%) | 0/243 (0.0%) | -1.7 pts, CI [-5.8,+2.9] |
| 1 | 34 | 28/102 (27.5%) | 25/102 (24.5%) | 34/102 (33.3%) | -2.9 pts, CI [-11.8,+5.9] |
| 2 | 36 | 49/108 (45.4%) | 36/108 (33.3%) | 72/108 (66.7%) | -12.0 pts, CI [-22.2,-1.8] |
| 3 | 49 | 92/147 (62.6%) | 50/147 (34.0%) | 147/147 (100.0%) | -28.6 pts, CI [-38.8,-18.4] |

### BEnQA Only

| Bucket | Items | Bangla slots | Reviewed Banglish slots | English slots | Banglish - Bangla |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 35 | 26/105 (24.8%) | 26/105 (24.8%) | 0/105 (0.0%) | 0.0 pts, CI [-9.5,+9.5] |
| 1 | 30 | 27/90 (30.0%) | 24/90 (26.7%) | 30/90 (33.3%) | -3.3 pts, CI [-13.3,+6.7] |
| 2 | 33 | 48/99 (48.5%) | 35/99 (35.4%) | 66/99 (66.7%) | -13.1 pts, CI [-24.2,-2.0] |
| 3 | 46 | 84/138 (60.9%) | 50/138 (36.2%) | 138/138 (100.0%) | -24.6 pts, CI [-34.8,-15.2] |

## Best Alternate-Script Buckets

Here the bucket is the larger of the native-Bangla and English model
correct counts. This is a headroom view: it asks how Banglish behaves
when at least one trusted non-Banglish script shows that the item is
answerable for the same Qwen family.

### All 200 Items

| Bucket | Items | Bangla slots | Reviewed Banglish slots | English slots | Banglish - Bangla |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 59 | 0/177 (0.0%) | 6/177 (3.4%) | 0/177 (0.0%) | +3.4 pts, CI [+0.6,+6.8] |
| 1 | 43 | 30/129 (23.3%) | 26/129 (20.2%) | 28/129 (21.7%) | -3.1 pts, CI [-10.1,+3.9] |
| 2 | 44 | 62/132 (47.0%) | 45/132 (34.1%) | 71/132 (53.8%) | -12.9 pts, CI [-22.7,-3.8] |
| 3 | 54 | 107/162 (66.0%) | 60/162 (37.0%) | 154/162 (95.1%) | -29.0 pts, CI [-38.3,-19.8] |

## Interpretation

- The near-zero low-consensus buckets are not good evidence for or against
  a script gap because they contain many all-script-hard rows.
- The stronger diagnostic rows are the high-consensus buckets. There, the
  same item is answerable by multiple Qwen rows in English or native
  Bangla, yet reviewed Banglish loses many of those model-item successes.
- This supports the thesis wording that the Banglish weakness is not just
  ordinary item difficulty or a different mix of easy and hard questions.
- This remains Qwen-family behavioral evidence. It is not an independent
  model-family replication and does not prove an internal mechanism.

## Reproducibility

- Builder: `scripts/analyze_v5_difficulty_conditioned_gap.py`
- Input rows: 200
- Summary rows: 36
- Bootstrap: item-cluster resampling within each bucket, 5,000 samples.
