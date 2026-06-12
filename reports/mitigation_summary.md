# Mitigation Summary

Updated: 2026-05-28

## Validation v3 Clean Banglish

| Model | Baseline | Aware Prompt | Few-Shot | Self-Normalize | English Pivot | External Normalizer |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 18/100 | 22/100 on v2 | 17/100 on v2 | 26/100 | 2/100 | 19/100 |
| Qwen3-4B | 18/100 | 16/100 on v2 | 17/100 on v2 | 11/100 | 16/100 | 15/100 |

Notes:

- Prompt-only mitigation is weak and inconsistent.
- Self-normalization is the only clearly positive signal so far, and only for
  Qwen2.5 on validation v3.
- Same-model English pivot is consistently bad or weak.
- The current specialist external normalizer is not sufficient; it preserves
  option labels but changes many digit counts and leaves substantial Latin text.

## Validation 200 v3 Clean Banglish

| Model | Baseline | Self-Normalize | Delta |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 38/200 | 51/200 | +13 correct / +6.5 points |
| Qwen3-4B | 46/200 | 21/200 | -25 correct / -12.5 points |

Qwen2.5 paired bootstrap:

- Self-normalize minus baseline: +6.5 points.
- 95% CI: approximately [+0.5, +13].

Qwen3 paired bootstrap:

- Self-normalize minus baseline: -12.5 points.
- 95% CI: approximately [-19.5, -5.5].

Qwen2.5 rewrite quality:

- BEnQA options not preserved in 19/144 items.
- BEnQA digit counts changed in 28/144 items.
- BEnQA formulas changed in 9/144 items.
- BanglaMATH digit counts changed in 14/56 items.

Interpretation:

- The Qwen2.5 self-normalization gain survives the larger validation-200 slice.
- The Qwen3 self-normalization degradation also survives the larger slice.
- It remains brittle enough that the thesis should present it as a promising
  model-dependent mitigation direction, not a solved normalization layer.

## MGSM Clean Banglish

| Model | Baseline 128 Tokens | Self-Normalize | English Pivot |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 0/50 | 0/50 | not run |
| Qwen3-4B | 5/50 | 0/50 | 2/50 |

Notes:

- Qwen2.5 validation self-normalization does not transfer to MGSM.
- Qwen3 self-normalization also does not transfer to MGSM: 5/50 -> 0/50,
  paired delta -10 points with CI approximately [-20, -2].
- Qwen3 English-pivot self-translation also fails on MGSM.
- Arithmetic is especially sensitive to rewrite/translation damage in numbers,
  units, and quantities.

## Working Interpretation

The failure is not solved by asking the same model to "try harder". Same-model
rewriting can help in a model-dependent way, but it frequently damages task
structure. The stronger thesis claim is that Banglish robustness needs a
reliable script-normalization layer or direct model adaptation, with explicit
preservation checks for options, digits, formulas, and named entities.

## Next Mitigation Candidates

1. Human-reviewed Banglish subset: measure how much rule-based romanization
   artifacts affect the current gap.
2. Better external normalization: test only if a model preserves digits,
   formulas, and option structure on a small dry run.
3. Script-consistency self-check: ask the model to answer Bangla and Banglish
   variants and flag disagreements, using it as uncertainty routing rather than
   direct accuracy recovery.
4. Lightweight adaptation: only after the benchmark is fixed and the open-model
   baseline story is stable.
