# Frozen-V5 Recoverability Source Decomposition

Updated: 2026-06-11

## Scope

This no-spend audit decomposes every thesis-facing Qwen model-item slot
by which script views are correct on the same frozen-v5 item. It turns
the cross-script oracle into a source attribution table: native Bangla
only, English only, both alternate scripts, or no script view correct.

- Input failure rows: `results/analysis/validation200_v5_cross_script_failure_patterns_items.csv`
- Item table: `results/analysis/v5_recoverability_source_items.csv`
- Summary table: `results/analysis/v5_recoverability_source_summary.csv`

Counts are descriptive and paired by item/model. They do not define a
deployable route because Bangla and English views are benchmark-provided.

## Overall Source Decomposition

| Dataset | Banglish wrong | Recoverable by Bangla/English | All-script hard | Bangla-only recovery | English-only recovery | Both alternates | Banglish-only success |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all | 463/600 (77.2%) | 185/600 (30.8%) | 278/600 (46.3%) | 28/600 (4.7%) | 81/600 (13.5%) | 76/600 (12.7%) | 20/600 (3.3%) |
| benqa | 297/432 (68.8%) | 164/432 (38.0%) | 133/432 (30.8%) | 24/432 (5.6%) | 72/432 (16.7%) | 68/432 (15.7%) | 20/432 (4.6%) |
| banglamath | 166/168 (98.8%) | 21/168 (12.5%) | 145/168 (86.3%) | 4/168 (2.4%) | 9/168 (5.4%) | 8/168 (4.8%) | 0/168 (0.0%) |

## By Model

| Model | Banglish correct | Banglish wrong | Recoverable miss | All-script hard | Bangla-only | English-only | Both alternates | Banglish-only success |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 41/200 (20.5%) | 159/200 (79.5%) | 58/200 (29.0%) | 101/200 (50.5%) | 13/200 (6.5%) | 30/200 (15.0%) | 15/200 (7.5%) | 7/200 (3.5%) |
| Qwen2.5-7B 8-bit | 47/200 (23.5%) | 153/200 (76.5%) | 68/200 (34.0%) | 85/200 (42.5%) | 8/200 (4.0%) | 31/200 (15.5%) | 29/200 (14.5%) | 8/200 (4.0%) |
| Qwen3-4B | 49/200 (24.5%) | 151/200 (75.5%) | 59/200 (29.5%) | 92/200 (46.0%) | 7/200 (3.5%) | 20/200 (10.0%) | 32/200 (16.0%) | 5/200 (2.5%) |

## Miss-Conditioned Shares

| Dataset | Recoverable share of Banglish misses | All-script-hard share | Native Bangla participates | English participates |
| --- | ---: | ---: | ---: | ---: |
| all | 185/463 (40.0%) | 278/463 (60.0%) | 104/463 (22.5%) | 157/463 (33.9%) |
| benqa | 164/297 (55.2%) | 133/297 (44.8%) | 92/297 (31.0%) | 140/297 (47.1%) |
| banglamath | 21/166 (12.7%) | 145/166 (87.3%) | 12/166 (7.2%) | 17/166 (10.2%) |

## Interpretation

- Across 600 model-item slots, reviewed Banglish is wrong in
  463/600 slots. Of those misses, 185/463
  (40.0%) are recoverable by native
  Bangla or English, while 278/463
  (60.0%) are all-script hard.
- Recovery is not just an English-only effect: native Bangla participates
  in 104/185 recoverable misses, English
  participates in 157/185, and
  76/185 are recovered by both alternate scripts.
- English-only recovery is still the largest single source
  (81/185), followed by both-alternate
  recovery (76/185) and Bangla-only recovery
  (28/185).
- Banglish-only success exists on 20/600 slots. Keep that
  counterevidence in the limitations: the result is a robust aggregate
  gap, not a claim that Banglish is always worse item by item.
- BEnQA contains most recoverable misses, while BanglaMATH is dominated by
  all-script-hard rows; that supports using BanglaMATH as a stress-test
  slice rather than the cleanest source-attribution stratum.

## Artifacts

- Builder: `scripts/analyze_v5_recoverability_sources.py`
- Item table: `results/analysis/v5_recoverability_source_items.csv`
- Summary table: `results/analysis/v5_recoverability_source_summary.csv`
