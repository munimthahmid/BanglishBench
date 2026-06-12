# Tokenization Audit: Validation 200

Updated: 2026-05-31

## Artifacts

- `results/tokenization/validation200_v3/audit.csv`
- `results/tokenization/validation200_v3/summary.csv`
- `results/tokenization/validation200_v4/audit.csv`
- `results/tokenization/validation200_v4/summary.csv`
- `results/tokenization/validation200_v5/audit.csv`
- `results/tokenization/validation200_v5/summary.csv`

Tokenizers:

- `Qwen/Qwen2.5-3B-Instruct`
- `Qwen/Qwen2.5-7B-Instruct`
- `Qwen/Qwen3-4B-Instruct-2507`

The three thesis-facing Qwen tokenizers give the same item-level counts on the
frozen-v5 slice. The frozen-v5 audit was generated with a tokenizer-only
Transformers stack via `uv`; the checked downstream reports use the saved CSV
artifacts and do not reload tokenizers during the normal local check bundle.

## v5 Summary

Mean HF tokens per word:

| Dataset | Bangla | Reviewed Banglish | English |
| --- | ---: | ---: | ---: |
| BEnQA | 4.0242 | 2.4942 | 1.9545 |
| BanglaMATH | 4.6285 | 2.1114 | 1.4080 |

For provenance, v4 clean-Banglish tokens per word were 2.4869 on BEnQA and
2.0850 on BanglaMATH. The reviewed-v5 edits barely change aggregate token cost.

## Interpretation

Reviewed Banglish is substantially cheaper than native Bangla under the Qwen
tokenizers:

- BEnQA reviewed Banglish uses about 38% fewer tokens per word than Bangla.
- BanglaMATH reviewed Banglish uses about 54% fewer tokens per word than Bangla.

Despite that, validation-200 accuracy is lower for Banglish than Bangla:

- Qwen2.5-3B frozen-v5: Bangla 54/200, reviewed Banglish 41/200.
- Qwen2.5-7B 8-bit frozen-v5: Bangla 65/200, reviewed Banglish 47/200.
- Qwen3-4B frozen-v5: Bangla 80/200, reviewed Banglish 49/200.

This strengthens the mechanism argument: the Banglish gap is not a simple
token-budget problem. The model sees fewer tokens, but those tokens are less
useful for the downstream task.

Reviewed-v5 cleanup barely changes tokenization aggregates, which matches the
accuracy sensitivity result: review improves text quality but does not
materially alter the script-gap finding.

## Item-Level Accuracy Relationship

Historical item-level accuracy relationship artifacts:

- `results/analysis/validation200_v3_token_accuracy_items_qwen_tokenizer_reparsed.csv`
- `results/analysis/validation200_v3_token_accuracy_summary_qwen_tokenizer_reparsed.csv`

For BEnQA clean Banglish under the historical v3 join:

| Model | Accuracy | Mean Tokens Correct | Mean Tokens Wrong | Corr Correct vs Tokens |
| --- | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 38/144 | 87.9737 | 74.5755 | +0.2061 |
| Qwen3-4B | 45/144 | 79.3333 | 77.5556 | +0.0288 |

For BEnQA native Bangla:

| Model | Accuracy | Corr Correct vs Tokens |
| --- | ---: | ---: |
| Qwen2.5-3B | 49/144 | +0.0538 |
| Qwen3-4B | 76/144 | -0.0658 |

Interpretation:

- Within BEnQA clean Banglish, wrong answers are not simply the longer-token
  prompts. Qwen2.5 actually has higher mean token counts among correct Banglish
  items, and Qwen3's relationship is near zero.
- This historical item-level relationship is now secondary to the frozen-v5
  failure-pattern join below.

## Cross-Script Failure Pattern Join

Frozen-v5 follow-up report:

- `reports/tokenization_cross_script_failure_patterns.md`
- `results/analysis/validation200_v5_cross_script_token_patterns_items.csv`
- `results/analysis/validation200_v5_cross_script_token_patterns_summary.csv`

This joins v5 tokenization metrics with the frozen-v5 cross-script failure
taxonomy. The main finding is that recoverable reviewed-Banglish misses are not
the long/token-heavy Banglish items. For BEnQA, recoverable Banglish misses are
shorter on average than non-recoverable/other items for Qwen2.5-3B,
Qwen2.5-7B, and Qwen3-4B. The strongest script-specific pattern,
`bangla_english_correct_banglish_wrong`, remains token-cheaper in reviewed
Banglish than in native Bangla.
