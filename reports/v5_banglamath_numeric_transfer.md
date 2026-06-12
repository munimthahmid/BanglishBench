# Frozen-V5 BanglaMATH Numeric Transfer Audit

Updated: 2026-06-11

## Scope

This no-spend audit checks whether BanglaMATH numeric-answer evidence
transfers from Bangla or English into reviewed Banglish. It joins the
numeric-signature sensitivity audit with response-style metadata and
uses only frozen-v5 thesis-facing Qwen outputs.

- Item table: `results/analysis/v5_banglamath_numeric_transfer_items.csv`
- Summary table: `results/analysis/v5_banglamath_numeric_transfer_summary.csv`

## Headline

- Qwen3-4B has at least one alternate script with the full raw numeric signature on 24/56 BanglaMATH items, but reviewed Banglish retains the signature on only 8/24 and is correct on 2/24.
- Qwen2.5 rows show even weaker Banglish numeric transfer: 1/12 retained for 3B and 4/24 retained for 7B.
- When both Bangla and English have the full raw numeric signature, Qwen3 reviewed Banglish retains it on 8/19 items; Qwen2.5 rows retain 1/8 and 4/12.
- In Qwen3's alternate-raw-signature slice, reviewed Banglish emits meta/uncertainty language on 9/24 and wrong no-number outputs on 4/24.

## Model Summary

| Model | Alt raw signature | Both alt raw | Banglish raw signature | Retains alt raw | Banglish correct in alt-raw slice | Meta in alt-raw slice | No-number wrong in alt-raw slice |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 12/56 | 8/56 | 1/56 | 1/12 | 0/12 | 0/12 | 0/12 |
| Qwen2.5-7B 8-bit | 24/56 | 12/56 | 5/56 | 4/24 | 0/24 | 0/24 | 0/24 |
| Qwen3-4B | 24/56 | 19/56 | 10/56 | 8/24 | 2/24 | 9/24 | 4/24 |

## Interpretation

- BanglaMATH is a low-accuracy stress test, but alternate scripts often
  contain the gold numeric values that reviewed Banglish drops.
- This supports the thesis framing that many Banglish failures are
  script-conditioned transfer failures rather than impossible items.
- Numeric signatures are optimistic and can credit intermediate reasoning
  numbers, so this should be cited as behavioral transfer evidence, not
  as final-answer accuracy.
