# Real Banglish Layer Plan

Updated: 2026-05-31

## Purpose

The current core benchmark uses controlled, rule-based clean Banglish. A strong
thesis should add at least a small real-Banglish layer, but it must not confuse
real Romanized Bangla corpora with task-equivalent QA/math benchmark items.

## Local Resource Check

BanglaTLit is available locally:

- `literature/code/BanglaTLit/data/BanglaTLiT_val.csv`: 1,500 rows plus header.
- `literature/code/BanglaTLit/data/BanglaTLiT_test.csv`: 2,500 rows plus header.
- Columns: `id`, `text_transliterated`, `text_bengali`.

The BanglaTLit README describes:

- 42,705 paired Romanized Bangla and Bangla-script back-transliteration samples.
- 245,727 Romanized Bangla pretraining samples.

## What BanglaTLit Can Support

Use it for:

- Real Banglish spelling variation analysis.
- Comparing our rule-based clean Banglish against naturally written Romanized
  Bangla.
- Evaluating Banglish-to-Bangla normalization quality.
- Building examples of real user-style Romanized Bangla for prompts or human
  discussion.

Do not use it as:

- A direct QA/math benchmark.
- Evidence that our controlled Banglish items are natural.
- A Bangla-to-Banglish generator for arbitrary benchmark questions.

## Proposed Thesis Use

Add a short real-Banglish chapter section:

1. Sample 200-500 BanglaTLit rows from local val/test.
2. Compute spelling and tokenization statistics:
   - words per row,
   - Latin/Bengali/code-mixed character ratios,
   - digit and punctuation preservation,
   - common spelling variants.
3. Compare those distributions against validation-200 clean Banglish.
4. Use the comparison to state how synthetic clean Banglish differs from real
   Banglish.

Optional, only if time allows:

- Evaluate a normalizer on BanglaTLit back-transliteration accuracy.
- Use a small manually selected real-Banglish MCQ-style subset if labels can be
  constructed without changing semantics.

## Initial Distribution Comparison

Artifacts:

- `reports/real_banglish_distribution_comparison.md`
- `scripts/compare_banglish_distributions.py`
- `scripts/analyze_banglatlit_spelling_variation.py`
- `results/analysis/banglatlit_vs_validation200_v5_banglish_distribution_items.csv`
- `results/analysis/banglatlit_vs_validation200_v5_banglish_distribution_summary.csv`
- `results/analysis/banglatlit_vs_validation200_v5_banglish_top_words.csv`
- `results/analysis/banglatlit_spelling_variation_summary.csv`
- `results/analysis/banglatlit_spelling_variation_tokens.csv`

Summary:

| Source | Rows | Mean chars | Mean words | Mean Latin ratio | Digit row share | Mixed Latin/Bengali share |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| BanglaTLit test | 2500 | 56.9 | 10.7 | 0.927 | 0.183 | 0.025 |
| BanglaTLit val | 1500 | 56.4 | 10.6 | 0.927 | 0.179 | 0.024 |
| Validation-200 v5 content-only Banglish | 200 | 86.2 | 14.2 | 0.902 | 0.545 | 0.000 |
| Validation-200 v5 raw Banglish | 200 | 159.5 | 31.5 | 0.834 | 0.695 | 0.000 |

Interpretation:

- Validation-200 Banglish is longer and much more number-heavy than BanglaTLit,
  even after stripping answer instructions and MCQ option lines.
- BanglaTLit contains small but real script mixing, while validation-200 clean
  Banglish is intentionally Latin-only.
- This supports a clean thesis distinction: validation-200 is a controlled
  script-equivalence benchmark, while BanglaTLit is a real Romanized Bangla
  distribution comparison.
- A simple token-alignment audit over 4,000 BanglaTLit val+test rows found 2,754
  token-aligned rows and 299 Bangla tokens with at least two repeated Latin
  variants, under a minimum token count of three. This is heuristic but gives
  concrete examples of real spelling variation such as `vai`/`bhai`,
  `kivabe`/`kibhabe`, and `plz`/`please`.

## Other Candidate Resources

- BanglishRev: useful for real e-commerce review distribution and code-mixing,
  but not currently downloaded locally.
- BnSentMix: useful for sentiment/code-mixed classification, but it would expand
  the thesis beyond controlled QA/math.
- BAN-TH or MixSarc: use only if licensing and content handling are clear.

## Decision

For the thesis core, prioritize human-reviewed validation-200 v5 first. Use
BanglaTLit as a distributional comparison and normalization resource, not as a
replacement for controlled script-equivalent evaluation.
