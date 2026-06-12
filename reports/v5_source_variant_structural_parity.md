# V5 Source-Variant Structural Parity Audit

Updated: 2026-06-11

## Inputs

- Frozen v5 slice: `data/slices/validation_200_v5.jsonl`
- Item audit CSV: `results/analysis/v5_source_variant_structural_parity_items.csv`
- Summary CSV: `results/analysis/v5_source_variant_structural_parity_summary.csv`

## Headline

- Bangla vs reviewed Banglish has 0/200 structural mismatches and 0 primary hard-fail rows across option labels, digit sequences, formula-like tokens, and answer instructions.
- Bangla vs English has 39/200 diagnostic warnings; these are retained as source-translation caveats, not as the main paired claim.
- Reviewed Banglish vs English has 39/200 diagnostic warnings.

## Summary

| Comparison | Role | Dataset | Task type | n | Mismatch | Options | Digits | Formulas | Instruction |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| bangla_vs_banglish | primary | all | all | 200 | 0 | 0 | 0 | 0 | 0 |
| bangla_vs_banglish | primary | banglamath | all | 56 | 0 | 0 | 0 | 0 | 0 |
| bangla_vs_banglish | primary | banglamath | short_answer | 56 | 0 | 0 | 0 | 0 | 0 |
| bangla_vs_banglish | primary | benqa | all | 144 | 0 | 0 | 0 | 0 | 0 |
| bangla_vs_banglish | primary | benqa | mcq | 144 | 0 | 0 | 0 | 0 | 0 |
| bangla_vs_english | diagnostic | all | all | 200 | 39 | 0 | 23 | 23 | 0 |
| bangla_vs_english | diagnostic | banglamath | all | 56 | 12 | 0 | 12 | 3 | 0 |
| bangla_vs_english | diagnostic | banglamath | short_answer | 56 | 12 | 0 | 12 | 3 | 0 |
| bangla_vs_english | diagnostic | benqa | all | 144 | 27 | 0 | 11 | 20 | 0 |
| bangla_vs_english | diagnostic | benqa | mcq | 144 | 27 | 0 | 11 | 20 | 0 |
| banglish_vs_english | diagnostic | all | all | 200 | 39 | 0 | 23 | 23 | 0 |
| banglish_vs_english | diagnostic | banglamath | all | 56 | 12 | 0 | 12 | 3 | 0 |
| banglish_vs_english | diagnostic | banglamath | short_answer | 56 | 12 | 0 | 12 | 3 | 0 |
| banglish_vs_english | diagnostic | benqa | all | 144 | 27 | 0 | 11 | 20 | 0 |
| banglish_vs_english | diagnostic | benqa | mcq | 144 | 27 | 0 | 11 | 20 | 0 |

## Primary Pair Hard Fails

None. This supports using Bangla vs reviewed Banglish as the
primary paired comparison without a structural source-mismatch
exclusion rule.

## First Diagnostic Warnings

- `benqa_10th-Chemistry_0111` `bangla_vs_english` codes=digits formulas left_digits=`1 2 2 2 2 2 1 3 5 13` right_digits=`1 2 2 2 2 1 1 3 5 13`
- `benqa_10th-Chemistry_0111` `banglish_vs_english` codes=digits formulas left_digits=`1 2 2 2 2 2 1 3 5 13` right_digits=`1 2 2 2 2 1 1 3 5 13`
- `benqa_12th-Chemistry-II_0054` `bangla_vs_english` codes=formulas left_digits=`2 2` right_digits=`2 2`
- `benqa_12th-Chemistry-II_0054` `banglish_vs_english` codes=formulas left_digits=`2 2` right_digits=`2 2`
- `benqa_10th-Math-II_0139` `bangla_vs_english` codes=formulas left_digits=`1 2 1 10 1 30 10 1 1010 1 1100 1 11000 1 10010` right_digits=`1 2 1 10 1 30 10 1 1010 1 1100 1 11000 1 10010`
- `benqa_10th-Math-II_0139` `banglish_vs_english` codes=formulas left_digits=`1 2 1 10 1 30 10 1 1010 1 1100 1 11000 1 10010` right_digits=`1 2 1 10 1 30 10 1 1010 1 1100 1 11000 1 10010`
- `benqa_12th-Physics-I_0289` `bangla_vs_english` codes=formulas left_digits=`30 90 300 436 636` right_digits=`30 90 300 436 636`
- `benqa_12th-Physics-I_0289` `banglish_vs_english` codes=formulas left_digits=`30 90 300 436 636` right_digits=`30 90 300 436 636`
- `banglamath_0557` `bangla_vs_english` codes=digits formulas left_digits=`120 31 4` right_digits=`120 3`
- `banglamath_0557` `banglish_vs_english` codes=digits formulas left_digits=`120 31 4` right_digits=`120 3`
- `banglamath_0542` `bangla_vs_english` codes=digits left_digits=`25 44 24` right_digits=`44 24 25`
- `banglamath_0542` `banglish_vs_english` codes=digits left_digits=`25 44 24` right_digits=`44 24 25`
- `benqa_12th-Chemistry-II_0294` `bangla_vs_english` codes=formulas left_digits=`2 2 2 3` right_digits=`2 2 2 3`
- `benqa_12th-Chemistry-II_0294` `banglish_vs_english` codes=formulas left_digits=`2 2 2 3` right_digits=`2 2 2 3`
- `benqa_12th-Math-II_0230` `bangla_vs_english` codes=digits left_digits=`5 9 5 4 45 14 14` right_digits=`9 5 5 4 45 14 14`
- `benqa_12th-Math-II_0230` `banglish_vs_english` codes=digits left_digits=`5 9 5 4 45 14 14` right_digits=`9 5 5 4 45 14 14`
- `benqa_12th-Physics-I_0214` `bangla_vs_english` codes=formulas left_digits=`0 27 273 300 546` right_digits=`0 27 273 300 546`
- `benqa_12th-Physics-I_0214` `banglish_vs_english` codes=formulas left_digits=`0 27 273 300 546` right_digits=`0 27 273 300 546`
- `banglamath_1698` `bangla_vs_english` codes=digits formulas left_digits=`6 12 1` right_digits=`30 6 12`
- `banglamath_1698` `banglish_vs_english` codes=digits formulas left_digits=`6 12 1` right_digits=`30 6 12`

## Interpretation

The strict preservation gate is applied to the Bangla-vs-reviewed-Banglish
source pair because that pair carries the main script-robustness claim.
English is still valuable privileged diagnostic evidence, but the source
English field can contain upstream translation differences; structural
warnings in English comparisons should be cited as caveats rather than
used to discard the primary Bangla-vs-Banglish result.
