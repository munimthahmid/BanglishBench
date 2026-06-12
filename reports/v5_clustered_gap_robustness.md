# Frozen-V5 Clustered Gap Robustness

Updated: 2026-06-11

## Scope

This no-spend robustness check recomputes the paired script gaps with a
cluster bootstrap instead of an item bootstrap. The resampling unit is a
curriculum stratum: BEnQA subject for BEnQA rows and BanglaMATH grade for
BanglaMATH rows. It checks whether the release-facing gap depends on
treating neighboring items inside the same subject/grade as independent.

- Source item table: `results/analysis/v5_banglish_fragility_items.csv`
- Cluster rows: `results/analysis/v5_clustered_gap_clusters.csv`
- Summary rows: `results/analysis/v5_clustered_gap_summary.csv`

BanglaMATH has only three grade clusters, so its cluster intervals are
coarse and should remain descriptive. The all-200 rows use 16 clusters
(13 BEnQA subjects plus 3 BanglaMATH grades).

## Banglish Minus Bangla

| Model | Dataset | Clusters | Bangla | Reviewed Banglish | Delta | Cluster 95% CI | Gains | Losses |
| --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| Qwen2.5-3B | `all` | 16 | 54/200 | 41/200 | -6.5 pts | [-13.9, +1.1] | 15 | 28 |
| Qwen2.5-3B | `benqa` | 13 | 49/144 | 41/144 | -5.6 pts | [-15.8, +4.2] | 15 | 23 |
| Qwen2.5-3B | `banglamath` | 3 | 5/56 | 0/56 | -8.9 pts | [-15.0, 0.0] | 0 | 5 |
| Qwen2.5-7B 8-bit | `all` | 16 | 65/200 | 47/200 | -9.0 pts | [-15.1, -3.1] | 19 | 37 |
| Qwen2.5-7B 8-bit | `benqa` | 13 | 60/144 | 47/144 | -9.0 pts | [-16.8, -1.4] | 19 | 32 |
| Qwen2.5-7B 8-bit | `banglamath` | 3 | 5/56 | 0/56 | -8.9 pts | [-15.0, 0.0] | 0 | 5 |
| Qwen3-4B | `all` | 16 | 80/200 | 49/200 | -15.5 pts | [-23.6, -8.4] | 8 | 39 |
| Qwen3-4B | `benqa` | 13 | 76/144 | 47/144 | -20.1 pts | [-28.5, -11.2] | 8 | 37 |
| Qwen3-4B | `banglamath` | 3 | 4/56 | 2/56 | -3.6 pts | [-10.0, 0.0] | 0 | 2 |

## Banglish Minus English

| Model | Dataset | Clusters | English | Reviewed Banglish | Delta | Cluster 95% CI | Gains | Losses |
| --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| Qwen2.5-3B | `all` | 16 | 71/200 | 41/200 | -15.0 pts | [-23.2, -7.0] | 15 | 45 |
| Qwen2.5-3B | `benqa` | 13 | 66/144 | 41/144 | -17.4 pts | [-27.3, -7.0] | 15 | 40 |
| Qwen2.5-3B | `banglamath` | 3 | 5/56 | 0/56 | -8.9 pts | [-20.0, 0.0] | 0 | 5 |
| Qwen2.5-7B 8-bit | `all` | 16 | 94/200 | 47/200 | -23.5 pts | [-33.3, -14.4] | 13 | 60 |
| Qwen2.5-7B 8-bit | `benqa` | 13 | 86/144 | 47/144 | -27.1 pts | [-38.6, -16.0] | 13 | 52 |
| Qwen2.5-7B 8-bit | `banglamath` | 3 | 8/56 | 0/56 | -14.3 pts | [-30.0, -5.0] | 0 | 8 |
| Qwen3-4B | `all` | 16 | 88/200 | 49/200 | -19.5 pts | [-29.0, -10.8] | 13 | 52 |
| Qwen3-4B | `benqa` | 13 | 82/144 | 47/144 | -24.3 pts | [-34.3, -12.6] | 13 | 48 |
| Qwen3-4B | `banglamath` | 3 | 6/56 | 2/56 | -7.1 pts | [-15.0, 0.0] | 0 | 4 |

## Interpretation

- The all-200 cluster bootstrap keeps Qwen2.5-7B 8-bit negative
  (-9.0 pts, CI [-15.1, -3.1])
  and Qwen3-4B negative (-15.5 pts, CI
  [-23.6, -8.4]).
- Qwen2.5-3B remains directionally negative on all-200
  (-6.5 pts), but its cluster
  interval reaches zero [-13.9,
  +1.1], matching the existing
  caution that the 3B all-200 result is weakest.
- On BEnQA, Qwen3-4B remains clearly negative under subject-cluster
  resampling (-20.1 pts, CI
  [-28.5, -11.2]).
  The Qwen2.5 BEnQA rows also remain negative; Qwen2.5-3B reaches
  zero (CI [-15.8,
  +4.2]), while Qwen2.5-7B
  stays below zero (CI [-16.8,
  -1.4]).
- BanglaMATH cluster intervals are intentionally treated as descriptive
  because there are only three grade clusters and the slice is
  low-accuracy across scripts.

## Artifacts

- Builder: `scripts/analyze_v5_clustered_gap_robustness.py`
- Cluster rows: `results/analysis/v5_clustered_gap_clusters.csv`
- Summary rows: `results/analysis/v5_clustered_gap_summary.csv`
