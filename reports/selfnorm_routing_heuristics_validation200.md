# Self-Normalization Routing Heuristics

Updated: 2026-05-28

## Purpose

The oracle routing analysis showed that baseline and self-normalized answers are
partly complementary. This report tests whether simple rewrite-quality features
can route between them without access to labels.

## Artifacts

- `scripts/evaluate_selfnorm_routing_heuristics.py`
- `results/analysis/qwen25_validation200_v3_selfnorm_routing_heuristics.csv`
- `results/analysis/qwen3_validation200_v3_selfnorm_routing_heuristics.csv`

## Results

| Heuristic | Qwen2.5 Correct | Qwen3 Correct |
| --- | ---: | ---: |
| Always baseline | 38/200 | 46/200 |
| Always self-normalize | 51/200 | 21/200 |
| Selfnorm if options preserved | 51/200 | 22/200 |
| Selfnorm if digits/formulas preserved | 49/200 | 26/200 |
| Selfnorm if all structure preserved | 50/200 | 27/200 |
| Selfnorm if Bengali ratio >= 0.5 | 46/200 | 40/200 |
| Selfnorm if structure preserved and Bengali ratio >= 0.3 | 50/200 | 32/200 |
| Selfnorm only for BanglaMATH | 43/200 | 49/200 |
| Selfnorm only for BEnQA | 46/200 | 18/200 |

## Interpretation

Simple surface-quality routing is not enough.

For Qwen2.5, these rules do not improve over always self-normalizing. They can
avoid some rewrites, but they also skip enough useful rewrites that accuracy
stays the same or drops slightly.

For Qwen3, every tested rule still underperforms the direct Banglish baseline.
Even when rewrites preserve options, digits, and formulas, the normalized path
often changes the model's decision behavior in harmful ways.

The task-aware rule is the first simple exception: for Qwen3, using
self-normalization only on BanglaMATH improves 46/200 to 49/200, because the
normalization path helps arithmetic but badly damages BEnQA. This is a small
gain, not a full solution.

The next routing attempt should use stronger signals:

- Answer agreement between direct and normalized paths.
- Model confidence or log-probability margin where available.
- Consistency across Bangla, Banglish, and normalized Bangla variants.
- A small learned router trained only on development data, after the benchmark
  split is finalized.

## Answer Agreement Check

Direct Banglish and self-normalized parsed answers agree on a minority of items:

| Model | Agreement Group | Items | Direct Correct | Selfnorm Correct |
| --- | --- | ---: | ---: | ---: |
| Qwen2.5-3B | Parsed answers agree | 64 | 24 | 24 |
| Qwen2.5-3B | Parsed answers differ | 136 | 14 | 27 |
| Qwen3-4B | Parsed answers agree | 33 | 8 | 8 |
| Qwen3-4B | Parsed answers differ | 167 | 38 | 13 |

Agreement alone is not enough as an accuracy signal. When the two paths agree,
they can still be jointly wrong. When they disagree, the better choice is
model-dependent: self-normalization is better for Qwen2.5 disagreements, while
the direct baseline is better for Qwen3 disagreements.
