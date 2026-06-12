# Cross-Script Oracle: Validation 200 v3

Updated: 2026-05-28

Historical report. For the frozen-v5 reviewed-Banglish refresh, use
`reports/cross_script_diagnostics_validation200_v5.md`.

## Purpose

This is an upper-bound analysis across native Bangla, clean Banglish, and
English. It asks: for how many items does the model get at least one script
variant correct?

This is not a deployable result because final systems will not always have
trusted parallel English or Bangla rewrites. It estimates how much item-level
knowledge is present somewhere across scripts.

## Artifacts

- `scripts/oracle_union_variants.py`
- `results/analysis/qwen25_validation200_v3_cross_script_oracle_union.csv`
- `results/analysis/qwen3_validation200_v3_cross_script_oracle_union.csv`
- `reports/cross_script_failure_taxonomy_validation200.md`

## Overall

| Model | Bangla | Banglish | English | Oracle Any-Script |
| --- | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 54/200 | 38/200 | 71/200 | 99/200 |
| Qwen3-4B | 80/200 | 46/200 | 88/200 | 108/200 |

## BEnQA

| Model | Bangla | Banglish | English | Oracle Any-Script | All Scripts Correct |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 49/144 | 38/144 | 66/144 | 92/144 | 17/144 |
| Qwen3-4B | 76/144 | 45/144 | 82/144 | 102/144 | 29/144 |

## BanglaMATH

| Model | Bangla | Banglish | English | Oracle Any-Script | All Scripts Correct |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 5/56 | 0/56 | 5/56 | 7/56 | 0/56 |
| Qwen3-4B | 4/56 | 1/56 | 6/56 | 6/56 | 1/56 |

## Interpretation

The BEnQA oracle gap is large. Qwen3 gets 102/144 BEnQA items correct in at
least one script, but only 45/144 in Banglish. This means many failures are not
because the model cannot solve the underlying item at all; the answer is
available under another script condition.

This supports the thesis framing that script choice changes access to latent
task knowledge. It also motivates future cross-script consistency or routing
methods, while keeping oracle results clearly separated from deployable
accuracy.

## Failure Taxonomy Addendum

The item-level taxonomy strengthens the oracle interpretation. Qwen3-4B has
35/200 validation items where Bangla and English are both correct but clean
Banglish is wrong; 32 of those are BEnQA items. More broadly, Qwen3-4B has
62/200 Banglish misses that are correct under Bangla or English. Qwen2.5-3B has
a similar broad recoverability count, 61/200.

See `reports/cross_script_failure_taxonomy_validation200.md` for the full
pattern table and example packet.
