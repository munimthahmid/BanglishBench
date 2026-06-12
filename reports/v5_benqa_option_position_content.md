# Frozen-V5 BEnQA Option Position/Content Audit

Updated: 2026-06-11

## Scope

This no-spend audit checks whether the Qwen3 reviewed-Banglish BEnQA
D-attractor can be reduced to option text features, especially D often
being the longest option. It uses reviewed-Banglish option text from the
frozen-v5 slice and reviewed-Banglish predictions from the choice-bias audit.

- Item-level output: `results/analysis/v5_benqa_option_position_content_items.csv`
- Summary table: `results/analysis/v5_benqa_option_position_content_summary.csv`

## Headline

- D is tied for longest option on 98/144 BEnQA items, while gold D appears on 39/144 items.
- Qwen3-4B still predicts D on 30/46 items where D is not the longest option.
- The corresponding non-longest-D counts are 9/46 for Qwen2.5-3B and 5/46 for Qwen2.5-7B 8-bit.
- Qwen3-4B predicts a longest option on 97/144 rows, so option length/content contributes to behavior, but it does not fully explain the D-position collapse.

## Summary

| Model | Correct | Pred D | Pred D when D longest | Pred D when D not longest | Pred longest option | Pred composite option |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 41/144 | 39/144 | 30/98 (30.6%) | 9/46 (19.6%) | 82/144 | 25/144 |
| Qwen2.5-7B 8-bit | 47/144 | 25/144 | 20/98 (20.4%) | 5/46 (10.9%) | 82/144 | 24/144 |
| Qwen3-4B | 47/144 | 111/144 | 81/98 (82.7%) | 30/46 (65.2%) | 97/144 | 25/144 |

## Item Feature Summary

- Gold option is among the longest options on 76/144 items.
- D is tied for longest on 98/144 items, but only 29/98 of those have gold D.
- D is composite on 25/144 items; composite markers are balanced enough that D-only composition is not the sole explanation.

Weighted longest-label counts:

| A | B | C | D |
| ---: | ---: | ---: | ---: |
| 24.25 | 27.58 | 28.58 | 63.58 |

## Interpretation

- BEnQA option text length partly explains why D is tempting: D is often one
  of the longest options.
- Qwen3's reviewed-Banglish D-attractor remains visible when D is not the
  longest option, and it is far stronger than the same slice for Qwen2.5.
- Use this as a confound check beside the choice-bias, subject-option,
  distractor-transition, and label-balance audits.

## Reproducibility

- Builder: `scripts/analyze_v5_benqa_option_position_content.py`
- Item rows: 432
- Summary rows: 4
