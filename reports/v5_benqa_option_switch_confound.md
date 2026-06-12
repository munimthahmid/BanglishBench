# Frozen-V5 BEnQA Option-Switch Confound Audit

Updated: 2026-06-11

## Scope

This no-spend audit joins the BEnQA option-switching rows with the
option position/content features. It asks whether Qwen3's reviewed-
Banglish non-D-to-D switches persist after controlling for D being the
longest option and for gold-D rows.

- Joined item table: `results/analysis/v5_benqa_option_switch_confound_items.csv`
- Summary table: `results/analysis/v5_benqa_option_switch_confound_summary.csv`

## Headline

- When the alternate-script prediction is correct, non-D, and D is not the longest option, Qwen3 still switches to a wrong reviewed-Banglish D on 11/19 Bangla rows and 12/21 English rows.
- In the broader non-D, gold-not-D, D-not-longest scope, Qwen3 switches to D on 13/25 Bangla rows and 15/26 English rows.
- The corresponding correct-non-D and D-not-longest Bangla-side counts for Qwen2.5 are only 1/13 and 2/22.

## Strict Scope Summary

| Model | Baseline | Non-D/gold-not-D/D-not-longest: switched to D | Correct non-D/D-not-longest: wrong D |
| --- | --- | ---: | ---: |
| Qwen2.5-3B | Bangla | 3/29 (10.3%) | 1/13 (7.7%) |
| Qwen2.5-3B | English | 2/28 (7.1%) | 1/19 (5.3%) |
| Qwen2.5-7B 8-bit | Bangla | 2/33 (6.1%) | 2/22 (9.1%) |
| Qwen2.5-7B 8-bit | English | 2/33 (6.1%) | 1/25 (4.0%) |
| Qwen3-4B | Bangla | 13/25 (52.0%) | 11/19 (57.9%) |
| Qwen3-4B | English | 15/26 (57.7%) | 12/21 (57.1%) |

## Interpretation

- D being a long option is a real BEnQA confound, but it does not remove
  the Qwen3 switching result: many Qwen3 non-D alternate-script choices
  still become reviewed-Banglish D when D is not longest.
- Excluding gold-D rows also preserves the pattern, so the switch is not
  merely a route to the correct gold-D label.
- Treat this as a confound audit for the Qwen3 BEnQA failure mode, not as
  a causal internal-mechanism claim.

## Reproducibility

- Builder: `scripts/analyze_v5_benqa_option_switch_confound.py`
- Joined item rows: 864
- Summary rows: 36
