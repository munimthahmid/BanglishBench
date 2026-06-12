# Frozen-V5 BEnQA Length/Token Confound Audit

Updated: 2026-06-11

## Scope

This no-spend audit checks whether Qwen3-4B's reviewed-Banglish BEnQA
D-attractor can be reduced to prompt length or tokenization burden. It
joins frozen-v5 BEnQA choice-bias rows with the reviewed-Banglish
tokenization audit. The audited tokenizer is the Qwen3-4B tokenizer;
prior tokenization checks showed the thesis-facing Qwen tokenizers have
identical counts on frozen-v5 item/variant pairs.

- Item table: `results/analysis/v5_benqa_length_token_confound_items.csv`
- Summary table: `results/analysis/v5_benqa_length_token_confound_summary.csv`

## Headline

- Across reviewed-Banglish HF-token quartiles, Qwen3-4B predicts D on 32/36, 26/36, 27/36, 26/36 rows; every quartile is at least 26/36 (72.2%).
- Wrong-D counts by the same token quartiles are 26/36, 17/36, 15/36, 19/36; the shortest-token quartile is 26/36.
- By character-length quartile, Qwen3-4B still predicts D on 31/36 shortest rows and 29/36 longest rows.
- By token-density quartile, Qwen3-4B predicts D on 33/36 lowest-density rows and 22/36 highest-density rows.
- Qwen2.5 rows remain much lower in the shortest and longest HF-token quartiles: 5/36 and 1/36 in Q1; 14/36 and 9/36 in Q4.

## HF-Token Quartiles

| Model | Q1 D | Q2 D | Q3 D | Q4 D | Q1 wrong D | Q4 wrong D |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 5/36 | 8/36 | 12/36 | 14/36 | 3/36 | 9/36 |
| Qwen2.5-7B 8-bit | 1/36 | 5/36 | 10/36 | 9/36 | 0/36 | 6/36 |
| Qwen3-4B | 32/36 | 26/36 | 27/36 | 26/36 | 26/36 | 19/36 |

## Interpretation

- The Qwen3 D-attractor is strongest in the shortest reviewed-Banglish
  HF-token quartile, so it is not a simple long-prompt or token-heavy
  failure mode.
- Character length, word count, and token-density quartiles all keep the
  Qwen3 D pattern visible, while Qwen2.5 rows remain far less D-heavy.
- This complements the broader tokenization audit: reviewed Banglish is
  token-cheaper than Bangla overall, and the option collapse is not
  concentrated in token-heavy BEnQA rows.

## Artifacts

- Builder: `scripts/analyze_v5_benqa_length_token_confound.py`
- Item table: `results/analysis/v5_benqa_length_token_confound_items.csv`
- Summary table: `results/analysis/v5_benqa_length_token_confound_summary.csv`
