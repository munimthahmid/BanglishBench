# Frozen-V5 BEnQA Cross-Model Banglish-Agreement Audit

Updated: 2026-06-11

## Scope

This no-spend audit asks how Qwen3-4B behaves on reviewed Banglish
BEnQA items where the two Qwen2.5 thesis rows agree on the same
reviewed-Banglish option. Unlike the cross-script agreement audit,
this holds the script fixed and varies only the model row.

- Item table: `results/analysis/v5_benqa_cross_model_banglish_agreement_items.csv`
- Summary table: `results/analysis/v5_benqa_cross_model_banglish_agreement_summary.csv`

## Headline

- The two Qwen2.5 rows agree on a reviewed-Banglish option in 61/144 BEnQA items; 42 of those agreements are non-D.
- When the Qwen2.5 rows agree on a non-D reviewed-Banglish option, Qwen3-4B predicts D on 26/42 rows (61.9%) and wrong D on 18/42 rows.
- In the stricter slice where both Qwen2.5 rows are correct and agree on the same non-D option, Qwen3-4B is wrong-D on 8/15 rows and matches the Qwen2.5 agreement on 4/15 rows.
- When both Qwen2.5 rows are correct and agree on D, Qwen3-4B also predicts D on 7/7 rows.

## Summary

| Scope | N | Qwen3 correct | Qwen3 D | Qwen3 wrong D | Same as Qwen2.5 agreement | Switches from agreement | Qwen3 invalid |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| All BEnQA rows | 144 | 47 | 111 | 77 | 28 | 33 | 3 |
| Both Qwen2.5 Banglish predictions are valid | 142 | 47 | 109 | 75 | 28 | 33 | 3 |
| Qwen2.5 models agree on Banglish | 61 | 22 | 44 | 29 | 28 | 33 | 0 |
| Qwen2.5 models agree on non-D Banglish | 42 | 14 | 26 | 18 | 10 | 32 | 0 |
| Qwen2.5 models agree on D Banglish | 19 | 8 | 18 | 11 | 18 | 1 | 0 |
| Qwen2.5 models are correct and agree | 22 | 11 | 15 | 8 | 11 | 11 | 0 |
| Qwen2.5 models are correct and agree on non-D | 15 | 4 | 8 | 8 | 4 | 11 | 0 |
| Qwen2.5 models are correct and agree on D | 7 | 7 | 7 | 0 | 7 | 0 | 0 |

## Interpretation

- The result isolates a model-specific reviewed-Banglish failure mode:
  the same Banglish items can support non-D agreement for both Qwen2.5
  rows while Qwen3 still falls into D.
- The strict correct-non-D slice is small, so use it as corroborating
  evidence beside the larger cross-script option-agreement and
  option-switching audits.
- This remains behavioral evidence over fixed outputs; it does not claim
  an internal mechanism or a deployable mitigation.

## Artifacts

- Builder: `scripts/analyze_v5_benqa_cross_model_banglish_agreement.py`
- Item table: `results/analysis/v5_benqa_cross_model_banglish_agreement_items.csv`
- Summary table: `results/analysis/v5_benqa_cross_model_banglish_agreement_summary.csv`
