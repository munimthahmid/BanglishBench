# Frozen-V5 Consensus Stability Audit

Updated: 2026-06-11

## Scope

This no-spend audit stress-tests the item-consensus result by recomputing
model-item accuracy for every non-empty subset of the three
thesis-facing Qwen rows. The two-model rows are the leave-one-model-out
test: if every pair still shows a reviewed-Banglish deficit, the
consensus result is not carried by one model.

- Item table: `results/analysis/v5_consensus_stability_items.csv`
- Summary table: `results/analysis/v5_consensus_stability_summary.csv`

Bootstrap intervals resample validation items as paired clusters within
each model subset.

## Leave-One-Model-Out Result

| Model subset | Bangla | Reviewed Banglish | English | Banglish-Bangla | Banglish-English |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B + Qwen2.5-7B | 119/400 (29.8%) | 88/400 (22.0%) | 165/400 (41.2%) | -7.8 pts [-13.0, -2.5] | -19.2 pts [-25.8, -13.0] |
| Qwen2.5-3B + Qwen3-4B | 134/400 (33.5%) | 90/400 (22.5%) | 159/400 (39.8%) | -11.0 pts [-15.5, -6.5] | -17.2 pts [-23.2, -11.5] |
| Qwen2.5-7B + Qwen3-4B | 145/400 (36.2%) | 96/400 (24.0%) | 182/400 (45.5%) | -12.2 pts [-17.2, -7.2] | -21.5 pts [-28.0, -15.2] |

## Dataset Stress Test

| Dataset | Two-model subsets negative vs Bangla and English | Strong alternate, low Banglish range | Banglish beats alternate range |
| --- | --- | ---: | ---: |
| all | yes | 52-61 | 7-13 |
| benqa | yes | 48-57 | 7-13 |
| banglamath | yes | 4-4 | 0-0 |

## Interpretation

- The all-model consensus result is 137/600
  reviewed-Banglish successes versus 199/600
  Bangla and 253/600 English.
- All three leave-one-model-out pairs keep reviewed Banglish below both
  Bangla and English on the all-200 slice: yes.
- The same pairwise negative ordering holds on BEnQA, the clearest
  competent dataset slice: yes.
- BanglaMATH pair rows are also negative, but the absolute accuracy is
  low across scripts; keep BanglaMATH framed as a hard stress test.
- This is still Qwen-family stability, not independent family
  replication. Use it to answer the narrower criticism that the
  consensus audit is driven by one Qwen row.

## Artifacts

- Builder: `scripts/analyze_v5_consensus_stability.py`
- Item table: `results/analysis/v5_consensus_stability_items.csv`
- Summary table: `results/analysis/v5_consensus_stability_summary.csv`
