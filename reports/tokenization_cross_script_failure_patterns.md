# Tokenization vs Cross-Script Failure Patterns

Updated: 2026-06-11

## Purpose

This report joins the frozen-v5 cross-script failure taxonomy with
validation-200 v5 tokenizer metrics. The mechanism question is narrow:

> Are reviewed-Banglish failures that are recoverable under Bangla or
> English simply the long/token-heavy Banglish prompts?

The answer remains no under the frozen-v5 evidence.

## Artifacts

- Builder: `scripts/build_v5_tokenization_failure_patterns.py`
- Joined item table: `results/analysis/validation200_v5_cross_script_token_patterns_items.csv`
- Summary table: `results/analysis/validation200_v5_cross_script_token_patterns_summary.csv`
- Source taxonomy: `results/analysis/validation200_v5_cross_script_failure_patterns_items.csv`
- Source tokenization audit: `results/tokenization/validation200_v5/audit.csv`
- Source tokenization summary: `results/tokenization/validation200_v5/summary.csv`

## Tokenization Summary

The three thesis-facing Qwen tokenizers produce identical item-level
token counts for 600 frozen-v5 item/variant pairs
(0 mismatches across tokenizers).

Tokenizers audited:
- `Qwen/Qwen2.5-3B-Instruct`
- `Qwen/Qwen2.5-7B-Instruct`
- `Qwen/Qwen3-4B-Instruct-2507`

Mean HF tokens per word:

| Dataset | Bangla | Reviewed Banglish | English |
| --- | ---: | ---: | ---: |
| BEnQA | 4.0242 | 2.4942 | 1.9545 |
| BanglaMATH | 4.6285 | 2.1114 | 1.4080 |

## Recoverable Banglish Misses

Rows where `banglish_wrong_other_correct=True` are items where reviewed
Banglish is wrong but at least one other script variant is correct.

| Model | Dataset | Recoverable? | n | Mean Bangla tokens | Mean Banglish tokens | Banglish/Bangla token ratio | Banglish tokens/word |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | BanglaMATH | no | 49 | 121.8 | 54.3 | 0.461 | 2.127 |
| Qwen2.5-3B | BanglaMATH | yes | 7 | 65.0 | 31.1 | 0.487 | 2.000 |
| Qwen2.5-3B | BEnQA | no | 93 | 129.2 | 82.1 | 0.657 | 2.533 |
| Qwen2.5-3B | BEnQA | yes | 51 | 123.5 | 71.0 | 0.600 | 2.423 |
| Qwen2.5-7B 8-bit | BanglaMATH | no | 46 | 124.6 | 55.4 | 0.460 | 2.134 |
| Qwen2.5-7B 8-bit | BanglaMATH | yes | 10 | 69.1 | 33.1 | 0.486 | 2.010 |
| Qwen2.5-7B 8-bit | BEnQA | no | 86 | 130.0 | 82.2 | 0.658 | 2.561 |
| Qwen2.5-7B 8-bit | BEnQA | yes | 58 | 123.0 | 72.1 | 0.605 | 2.395 |
| Qwen3-4B | BanglaMATH | no | 52 | 119.0 | 53.2 | 0.462 | 2.117 |
| Qwen3-4B | BanglaMATH | yes | 4 | 58.5 | 28.5 | 0.498 | 2.033 |
| Qwen3-4B | BEnQA | no | 89 | 130.2 | 83.5 | 0.666 | 2.552 |
| Qwen3-4B | BEnQA | yes | 55 | 122.3 | 69.4 | 0.589 | 2.401 |

Interpretation:

- Recoverable reviewed-Banglish misses are not longer in Banglish token
  count.
- In BEnQA, recoverable misses are shorter on average than other rows for
  all three thesis-facing Qwen models.
- BanglaMATH recoverable groups are small, so they are descriptive only.

## Strongest Script-Specific Pattern

For `bangla_english_correct_banglish_wrong`, both Bangla and English are
correct while reviewed Banglish is wrong.

| Model | Dataset | n | Mean Bangla tokens | Mean Banglish tokens | Banglish/Bangla token ratio | Banglish tokens/word |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | BanglaMATH | 3 | 55.0 | 27.3 | 0.510 | 2.000 |
| Qwen2.5-3B | BEnQA | 12 | 126.5 | 69.0 | 0.566 | 2.435 |
| Qwen2.5-7B 8-bit | BanglaMATH | 3 | 55.0 | 27.3 | 0.510 | 2.000 |
| Qwen2.5-7B 8-bit | BEnQA | 26 | 113.4 | 68.3 | 0.626 | 2.360 |
| Qwen3-4B | BanglaMATH | 2 | 45.5 | 24.0 | 0.535 | 2.000 |
| Qwen3-4B | BEnQA | 30 | 126.5 | 72.1 | 0.593 | 2.401 |

These are the cleanest script-specific failures, and they are still
token-cheaper in reviewed Banglish than native Bangla.

## Thesis-Safe Claim

Use:

> Token count does not explain the cross-script Banglish failures. The
> script-specific reviewed-Banglish misses are not the longest Banglish
> prompts; many are token-cheaper than the corresponding native Bangla
> prompts and shorter than non-recoverable items.

Avoid:

- Claiming tokenization has no role at all.
- Claiming this proves an internal mechanism.
- Treating small BanglaMATH pattern groups as standalone statistical
  evidence.

## Implication

The failure is more consistent with representation, lexical grounding,
training distribution, or script-conditioned task interpretation than
with a simple context-budget or token-length bottleneck.
