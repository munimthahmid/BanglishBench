# Real Banglish Distribution Comparison

Updated: 2026-05-31

## Purpose

This report separates two roles:

- Validation-200 v5 is the controlled script-equivalence benchmark.
- BanglaTLit is real Romanized Bangla evidence for natural spelling variation
  and normalization difficulty.

The comparison should support the thesis limitations and motivation sections,
not replace the controlled QA/math result.

## Distribution Summary

| Source | Rows | Mean chars | Mean words | Mean Latin ratio | Digit row share | Mixed Latin/Bengali share |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| BanglaTLit test | 2500 | 56.9 | 10.7 | 0.927 | 0.183 | 0.025 |
| BanglaTLit val | 1500 | 56.4 | 10.6 | 0.927 | 0.179 | 0.024 |
| Validation-200 v5 content-only Banglish | 200 | 86.2 | 14.2 | 0.902 | 0.545 | 0.000 |
| Validation-200 v5 raw Banglish | 200 | 159.5 | 31.5 | 0.834 | 0.695 | 0.000 |

Interpretation:

- Validation-200 is longer and much more number-heavy than BanglaTLit, even
  after removing answer instructions and MCQ options.
- BanglaTLit has a small but real script-mixing rate; validation-200 clean
  Banglish is intentionally Latin-only.
- These differences are useful: they show why the thesis should call
  validation-200 controlled clean Banglish, not natural Banglish.

## Spelling Variation Audit

A simple token-alignment pass over BanglaTLit val+test found:

| Metric | Value |
| --- | ---: |
| Total rows | 4000 |
| Token-aligned rows under simple tokenization | 2754 |
| Token-aligned row share | 0.6885 |
| Aligned token pairs | 24418 |
| Unique Bangla tokens in aligned rows | 4281 |
| Bangla tokens with 2+ observed Latin variants, min count 3 | 825 |
| Bangla tokens with 2+ repeated Latin variants, min count 3 | 299 |

Illustrative repeated variants:

| Bangla token | Total | Repeated Latin variants |
| --- | ---: | --- |
| ভাই | 594 | vai:467; vi:33; bhai:29; vhai:14; bai:14; vay:8 |
| কিভাবে | 138 | kivabe:109; kibabe:7; kivaba:3; kibave:3; kivave:2 |
| এখন | 94 | akhon:36; ekhon:18; akon:8; akn:7; akhn:6 |
| প্লিজ | 279 | plz:192; please:35; pls:21; plzz:13 |
| কোন | 83 | kono:31; kon:23; kuno:5; kun:5; kno:3 |
| কিছু | 75 | kichu:27; kisu:20; kicu:12; kiso:4 |
| থ্যাংকস | 132 | thanks:76; tnx:41; thnx:5; tnxx:2 |

The token-alignment method is heuristic. One-off variants can be misalignments,
so thesis examples should prefer repeated variants and avoid claiming exact
variant counts as a gold linguistic measurement.

## Thesis Use

Use this section to make three concrete points:

1. Real Banglish has substantial spelling variation, including vowel choices,
   abbreviation, consonant alternation, and English/code-mixed spellings.
2. Our current clean Banglish benchmark is deliberately controlled and cannot
   stand alone as a naturalness claim.
3. A stronger final benchmark should include human-reviewed Banglish v5 and,
   if time allows, a small real-style perturbation layer informed by BanglaTLit.

## Artifacts

- `scripts/compare_banglish_distributions.py`
- `scripts/analyze_banglatlit_spelling_variation.py`
- `results/analysis/banglatlit_vs_validation200_v5_banglish_distribution_summary.csv`
- `results/analysis/banglatlit_vs_validation200_v5_banglish_distribution_items.csv`
- `results/analysis/banglatlit_vs_validation200_v5_banglish_top_words.csv`
- `results/analysis/banglatlit_spelling_variation_summary.csv`
- `results/analysis/banglatlit_spelling_variation_tokens.csv`
