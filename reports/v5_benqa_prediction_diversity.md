# Frozen-V5 BEnQA Prediction-Diversity Audit

Updated: 2026-06-11

## Scope

This no-spend audit summarizes whether BEnQA MCQ option predictions retain
normal label diversity or collapse toward one label. It reuses the frozen-v5
choice-bias and subject option-bias summaries, so it adds no new model
inference and no manual review.

- Summary table: `results/analysis/v5_benqa_prediction_diversity_summary.csv`

## Headline

- Gold labels are close to balanced: A=29, B=35, C=41, D=39; normalized entropy 0.994 and 3.97 effective options.
- Qwen3-4B reviewed Banglish collapses to D: predictions are A=3, B=7, C=20, D=111; normalized entropy 0.502 and 2.01 effective options.
- The same Qwen3 row has 3.52 effective options in Bangla and 3.69 in English; reviewed Banglish loses 1.51 effective options versus Bangla.
- Qwen2.5 reviewed Banglish retains high diversity: 3.75 and 3.77 effective options for the 3B and 7B rows.
- Subject rollup shows Qwen3 reviewed Banglish majority-D in 12/13 subjects with mean subject entropy 0.402, versus 0.799 Bangla and 0.807 English.

## Variant Distribution

| Model | Variant | Correct | Pred A | Pred B | Pred C | Pred D | Entropy | Effective options | D excess vs gold | TVD vs gold |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | Bangla | 49/144 | 23 | 45 | 31 | 45 | 0.97 | 3.86 | 4.2% | 0.11 |
| Qwen2.5-3B | Reviewed Banglish | 41/144 | 22 | 56 | 27 | 39 | 0.95 | 3.75 | 0.0% | 0.15 |
| Qwen2.5-3B | English | 66/144 | 28 | 43 | 29 | 44 | 0.98 | 3.91 | 3.5% | 0.09 |
| Qwen2.5-7B 8-bit | Bangla | 60/144 | 36 | 45 | 45 | 18 | 0.96 | 3.79 | -14.6% | 0.15 |
| Qwen2.5-7B 8-bit | Reviewed Banglish | 47/144 | 33 | 57 | 27 | 25 | 0.96 | 3.77 | -9.7% | 0.19 |
| Qwen2.5-7B 8-bit | English | 86/144 | 35 | 47 | 35 | 27 | 0.99 | 3.92 | -8.3% | 0.12 |
| Qwen3-4B | Bangla | 76/144 | 20 | 24 | 29 | 67 | 0.91 | 3.52 | 19.4% | 0.21 |
| Qwen3-4B | Reviewed Banglish | 47/144 | 3 | 7 | 20 | 111 | 0.50 | 2.01 | 50.0% | 0.51 |
| Qwen3-4B | English | 82/144 | 22 | 25 | 31 | 58 | 0.94 | 3.69 | 13.2% | 0.16 |

## Subject Rollup

| Model | Variant | Majority-D subjects | Mean subject entropy | Max subject D share |
| --- | --- | ---: | ---: | ---: |
| Qwen2.5-3B | Bangla | 2/13 | 0.84 | 54.5% |
| Qwen2.5-3B | Reviewed Banglish | 1/13 | 0.85 | 54.5% |
| Qwen2.5-3B | English | 1/13 | 0.88 | 54.5% |
| Qwen2.5-7B 8-bit | Bangla | 0/13 | 0.82 | 27.3% |
| Qwen2.5-7B 8-bit | Reviewed Banglish | 0/13 | 0.88 | 45.5% |
| Qwen2.5-7B 8-bit | English | 0/13 | 0.89 | 36.4% |
| Qwen3-4B | Bangla | 7/13 | 0.80 | 63.6% |
| Qwen3-4B | Reviewed Banglish | 12/13 | 0.40 | 91.7% |
| Qwen3-4B | English | 3/13 | 0.81 | 63.6% |

## Interpretation

- Qwen3's reviewed-Banglish BEnQA behavior is not just lower accuracy; it
  is a sharp reduction in prediction diversity relative to gold labels and
  to the same model's Bangla/English rows.
- Qwen2.5 rows preserve near-normal option diversity, so the Qwen3 collapse
  is a model-specific failure mode rather than an unavoidable property of
  Latin-script Banglish prompts.
- This is behavioral evidence only. It supports the failure analysis but
  does not identify an internal model mechanism.

## Artifacts

- Builder: `scripts/analyze_v5_benqa_prediction_diversity.py`
- Summary table: `results/analysis/v5_benqa_prediction_diversity_summary.csv`
