# Generated-View Preservation Audit v2

Updated: 2026-05-31

## Purpose

This audit tightens the rewrite-quality checks needed before any deployable
generated-view consistency routing experiment. It extends
`scripts/analyze_rewrite_outputs.py` beyond the earlier option/digit/formula
counts.

## New Checks

The audit now records:

- normalized digit sequence preservation, not only digit count,
- line-count preservation,
- extra answer markers such as `Answer:` or `Final answer:`,
- existing option-label preservation,
- formula preservation expanded to standalone scientific tokens such as `Au`
  and `Cu`, annotated units such as `gL^{-1}`, and LaTeX commands including
  subscript/superscript payloads such as `\theta_{ice}`.

Digit sequence comparison normalizes Bengali numerals to Arabic digits before
comparison.

The expanded token gate was applied to the locked 36-item dev50 BEnQA MCQ
generated-view smoke. It exposed scientific-token corruption on 17/36 raw
deterministic rows for both tested generators. A later formula-expression gate
also checks ASCII/operator expressions such as algebraic tokens, not only
chemistry-style symbols and LaTeX.

The protected-v2 structural wrapper protected numbers, scientific/math tokens,
and nested LaTeX identifiers in addition to option prefixes and answer-format
lines, but reviewed-v5 protected-v2 outputs still fail 16/36 hard gates because
formula/operator expressions are corrupted. The protected-v3 wrapper masks the
same formula-like expressions used by the auditor; both reviewed-v5
deterministic protected-v3 smokes pass 0/36 hard failures after regeneration.

The prior protected-v1 files used by the historical Qwen answer audits are kept
for provenance. Under the tightened gate they fail on 9/36
`phonetic-bangla` rows and 10/36 `bnbphoneticparser` rows. Reviewed-v5
protected-v2 files received Qwen answer audits but are gate-blocked; protected
v3 is the current formal candidate. Its answer audits are complete and remain
dev-only: preservation is fixed, but generated-BN gains are small and
uncertain.

The protected `fms-byte/banglish_to_bangla` MBART line-segment dry run also
fails 15/36 formula-expression hard gates and leaves genuine Latin residue on
7/36 rows. Its privileged native-reference mean CER is 0.1855, compared with
0.0906 for deterministic protected `phonetic-bangla`.

## Qwen2.5-7B Self-Normalization Preservation

Inputs:

- `results/runs/qwen25_7b_8bit_validation200_v4_dev50_selfnorm_v2/results/runs/qwen25_7b_8bit_validation200_v4_dev50_selfnorm.jsonl`
- `results/runs/qwen25_7b_8bit_validation200_v4_test150_selfnorm/results/runs/qwen25_7b_8bit_validation200_v4_test150_selfnorm.jsonl`

Summary:

| Dataset | n | Options not preserved | Digit sequence changed | Formulas changed | Line count changed | Extra answer markers |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| BanglaMATH | 56 | 0 | 6 | 0 | 56 | 0 |
| BEnQA | 144 | 10 | 25 | 5 | 64 | 21 |

## Qwen3-4B Self-Normalization Preservation

Input:

- `results/runs/qwen3_4b_validation200_v3_selfnorm/results/runs/qwen3_4b_validation200_v3_selfnorm.jsonl`

Summary:

| Dataset | n | Options not preserved | Digit sequence changed | Formulas changed | Line count changed | Extra answer markers |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| BanglaMATH | 56 | 0 | 1 | 0 | 56 | 0 |
| BEnQA | 144 | 3 | 14 | 1 | 108 | 5 |

## Interpretation

These checks explain why generated-view routing needs strict preservation gates:

- Even when option labels are preserved, the generated text can change numbers
  or leak an answer marker.
- BEnQA is more vulnerable than BanglaMATH to option, digit, formula, and answer
  leakage errors.
- Line-count preservation is very strict and will over-flag harmless line
  wrapping, but it is still useful as a warning feature for generated MCQ views.

For the first deployable consistency route, a generated alternate view should be
rejected if option labels change, digit sequence changes, formulas change, or an
extra answer marker appears. Line-count mismatch should be logged and inspected
before being used as a hard rejection rule.

## Artifacts

- Script:
  `scripts/analyze_rewrite_outputs.py`
- Qwen2.5-7B item audit:
  `results/analysis/qwen25_7b_8bit_validation200_v4_selfnorm_preservation_v2_items.csv`
- Qwen2.5-7B summary:
  `results/analysis/qwen25_7b_8bit_validation200_v4_selfnorm_preservation_v2_summary.csv`
- Qwen3-4B item audit:
  `results/analysis/qwen3_validation200_v3_selfnorm_preservation_v2_items.csv`
- Qwen3-4B summary:
  `results/analysis/qwen3_validation200_v3_selfnorm_preservation_v2_summary.csv`
