# Frozen-V5 BEnQA Subject Option-Bias Audit

Updated: 2026-06-11

## Scope

This no-spend audit checks whether the Qwen3 reviewed-Banglish BEnQA
D-attractor is broad across subjects or concentrated in one subject
cluster. It joins the frozen-v5 answer-format rows with BEnQA subject
metadata from the validation slice.

- Item-level output: `results/analysis/v5_benqa_subject_option_bias_items.csv`
- Subject summary: `results/analysis/v5_benqa_subject_option_bias_summary.csv`

## Headline

- Qwen3-4B reviewed Banglish has majority-D predictions in 12/13 BEnQA subjects.
- The same check gives 1/13 for Qwen2.5-3B and 0/13 for Qwen2.5-7B 8-bit reviewed Banglish.
- Qwen3-4B Bangla and English have majority-D predictions in 7/13 and 3/13 subjects, so the reviewed-Banglish collapse is much broader than its native-script rows.
- No subject has gold-D share above 45.5%; the subject-level D-attractor is not a single gold-label distribution artifact.

## Qwen3 Reviewed-Banglish By Subject

| Subject | N | Correct | Pred A | Pred B | Pred C | Pred D | Gold D | Majority | Entropy | TVD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| Biology | 12 | 3/12 | 0 | 0 | 1 | 11 | 2 | D (91.7%) | 0.21 | 0.75 |
| Biology-I | 11 | 3/11 | 0 | 1 | 1 | 9 | 2 | D (81.8%) | 0.43 | 0.64 |
| Biology-II | 11 | 1/11 | 0 | 0 | 1 | 10 | 1 | D (90.9%) | 0.22 | 0.82 |
| Chemistry | 11 | 4/11 | 1 | 0 | 0 | 10 | 5 | D (90.9%) | 0.22 | 0.45 |
| Chemistry-I | 11 | 5/11 | 0 | 0 | 1 | 10 | 5 | D (90.9%) | 0.22 | 0.45 |
| Chemistry-II | 11 | 2/11 | 0 | 0 | 4 | 7 | 1 | D (63.6%) | 0.47 | 0.55 |
| Math | 11 | 2/11 | 0 | 0 | 1 | 9 | 3 | D (81.8%) | 0.23 | 0.59 |
| Math-I | 11 | 4/11 | 0 | 2 | 1 | 7 | 2 | D (63.6%) | 0.58 | 0.50 |
| Math-II | 11 | 8/11 | 0 | 0 | 3 | 7 | 5 | D (63.6%) | 0.44 | 0.23 |
| Physics | 11 | 6/11 | 1 | 3 | 2 | 5 | 5 | D (45.5%) | 0.90 | 0.09 |
| Physics-I | 11 | 4/11 | 0 | 0 | 2 | 9 | 3 | D (81.8%) | 0.34 | 0.55 |
| Physics-II | 11 | 2/11 | 0 | 0 | 1 | 10 | 3 | D (90.9%) | 0.22 | 0.64 |
| Science | 11 | 3/11 | 1 | 1 | 2 | 7 | 2 | D (63.6%) | 0.75 | 0.45 |

## Qwen2.5 Reviewed-Banglish Subject Check

| Model | Majority-D subjects | Highest subject D share | Mean subject entropy |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 1/13 | 54.5% | 0.85 |
| Qwen2.5-7B 8-bit | 0/13 | 45.5% | 0.88 |
| Qwen3-4B | 12/13 | 91.7% | 0.40 |

## Interpretation

- Qwen3's reviewed-Banglish D-attractor is broad across BEnQA subjects, not
  just a single-subject artifact.
- Qwen2.5 rows remain useful contrast cases: they still lose accuracy under
  reviewed Banglish, but their subject-level option distributions do not
  collapse to D.
- This is behavioral evidence about answer selection, not a mechanism claim.
  It should be cited beside the choice-bias, distractor-transition, and
  label-balance audits.

## Reproducibility

- Builder: `scripts/analyze_v5_benqa_subject_option_bias.py`
- Item rows: 1296
- Subject summary rows: 117
