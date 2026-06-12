# Frozen-V5 Item Consensus Audit

Updated: 2026-06-11

## Scope

This no-spend audit treats each validation item as a paired unit and
counts how many of the three thesis-facing Qwen rows answer each script
view correctly. It asks whether reviewed Banglish failures persist even
when Bangla or English has cross-model support on the same item.

- Item-level table: `results/analysis/v5_item_consensus_items.csv`
- Summary table: `results/analysis/v5_item_consensus_summary.csv`

Bootstrap intervals below resample validation items, keeping the three
model outcomes for an item together. They are descriptive robustness
intervals for cross-model consensus, not a new independent model family.

## Cross-Model Script Totals

| Dataset | Bangla model-item successes | Reviewed Banglish | English | Banglish-Bangla delta | Banglish-English delta |
| --- | ---: | ---: | ---: | ---: | ---: |
| all | 199/600 (33.2%) | 137/600 (22.8%) | 253/600 (42.2%) | -10.3 pts [-14.7, -6.3] | -19.3 pts [-25.0, -13.7] |
| benqa | 185/432 (42.8%) | 135/432 (31.2%) | 234/432 (54.2%) | -11.6 pts [-17.1, -6.2] | -22.9 pts [-30.3, -15.7] |
| banglamath | 14/168 (8.3%) | 2/168 (1.2%) | 19/168 (11.3%) | -7.1 pts [-13.7, -2.4] | -10.1 pts [-17.9, -4.2] |

## Consensus Distribution

| Script | 0 models correct | 1 model | 2 models | 3 models |
| --- | ---: | ---: | ---: | ---: |
| Bangla | 80 | 60 | 41 | 19 |
| Reviewed Banglish | 109 | 56 | 24 | 11 |
| English | 81 | 34 | 36 | 49 |

## Recoverability Pressure

| Dataset | All-script hard | Banglish zero, alternate works | Banglish zero, strong alternate | Strong alternate, <=1 Banglish model | Banglish beats alternates |
| --- | ---: | ---: | ---: | ---: | ---: |
| all | 54/200 | 55/200 | 35/200 | 67/200 | 12/200 |
| benqa | 12/144 | 43/144 | 30/144 | 61/144 | 12/144 |
| banglamath | 42/56 | 12/56 | 5/56 | 6/56 | 0/56 |

## Interpretation

- Across 600 paired model-item slots, reviewed Banglish trails Bangla by -10.3 points (item-bootstrap CI [-14.7, -6.3]) and English by -19.3 points (CI [-25.0, -13.7]).
- BEnQA carries the cleanest recoverability signal: 61/144
  items have at least two-model support in Bangla or English while
  reviewed Banglish has at most one correct model; only 12/144 BEnQA items are all-script hard.
- BanglaMATH remains a stress-test slice: 42/56 items are
  all-script hard across the three Qwen rows, so its low Banglish score
  should be interpreted with that difficulty caveat.
- Banglish is not uniformly worse: it beats both alternate scripts on
  12/200 items. Keep this as counterevidence against
  overclaiming, while the dominant consensus pattern remains negative.

## Artifacts

- Builder: `scripts/analyze_v5_item_consensus.py`
- Item table: `results/analysis/v5_item_consensus_items.csv`
- Summary table: `results/analysis/v5_item_consensus_summary.csv`
