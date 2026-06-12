# Cross-Script Failure Taxonomy: Validation-200 v3

Updated: 2026-05-28

Historical report. For the frozen-v5 reviewed-Banglish refresh, use
`reports/cross_script_diagnostics_validation200_v5.md`.

## Purpose

The cross-script oracle shows that many items are answerable in at least one
script. This report makes that more concrete by classifying each item by its
correctness pattern across native Bangla, clean Banglish, and English for the
two main validation-200 runs.

## Artifacts

- `scripts/analyze_cross_script_failure_patterns.py`
- `scripts/export_gap_report.py`
- `results/analysis/validation200_v3_cross_script_failure_patterns_items.csv`
- `results/analysis/validation200_v3_cross_script_failure_patterns_summary.csv`
- `reports/cross_script_failure_examples_qwen3_validation200.md`

## Pattern Definitions

- `all_correct`: Bangla, Banglish, and English are all correct.
- `all_wrong`: all three scripts are wrong.
- `bangla_english_correct_banglish_wrong`: strongest script-access pattern;
  the same model answers Bangla and English but misses Banglish.
- `banglish_wrong_other_correct`: broader recoverability count; Banglish is
  wrong, but Bangla or English is correct.

## Main Counts

| Model | Dataset | All correct | All wrong | Bangla+English correct, Banglish wrong | Banglish wrong, other correct |
| --- | --- | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | All | 17/200 | 101/200 | 16/200 | 61/200 |
| Qwen2.5-3B | BEnQA | 17/144 | 52/144 | 13/144 | 54/144 |
| Qwen2.5-3B | BanglaMATH | 0/56 | 49/56 | 3/56 | 7/56 |
| Qwen3-4B | All | 30/200 | 92/200 | 35/200 | 62/200 |
| Qwen3-4B | BEnQA | 29/144 | 42/144 | 32/144 | 57/144 |
| Qwen3-4B | BanglaMATH | 1/56 | 50/56 | 3/56 | 5/56 |

## Interpretation

The strongest item-level evidence is Qwen3-4B on BEnQA. It has 32/144 items
where Bangla and English are both correct but clean Banglish is wrong. This is
hard to explain as ordinary item difficulty, because the same model has access
to the answer under both non-Banglish scripts.

The broader recoverability count is also stable across both main models:
Qwen2.5-3B has 61/200 Banglish misses that are correct under Bangla or English,
and Qwen3-4B has 62/200. On BEnQA, these become 54/144 and 57/144 respectively.

BanglaMATH remains mostly all-wrong, so it is less useful for fine-grained
failure taxonomy at the current model scale. Its value is as a hard transfer
stress test, not as the clearest source of the script-access evidence.

## Example Packet

`reports/cross_script_failure_examples_qwen3_validation200.md` exports eight
Qwen3-4B examples from the strongest pattern. The first examples include simple
math cases where Bangla and English yield the correct final answer but Banglish
does not, plus BEnQA MCQs with the same pattern.

## Thesis Use

Use this taxonomy to support a stronger mechanistic framing:

> Many Banglish failures are not just hard questions. For a substantial subset,
> the same model answers the same item correctly in Bangla and/or English, but
> fails when the Bangla content is written in Latin-script Banglish.

This remains behavioral evidence, not a claim about the model's internal
mechanism.
