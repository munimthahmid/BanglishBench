# Frozen-V5 BEnQA Gold-Label Balance Sensitivity

Updated: 2026-06-11

## Scope

This no-spend audit checks whether the BEnQA MCQ script gap is an
artifact of gold option-label distribution or Qwen3's reviewed-Banglish
over-selection of option D. It reports micro accuracy, gold-label
balanced accuracy (mean of A/B/C/D stratum accuracies), and a non-D
stress slice. Bootstrap intervals resample paired items, stratified by
gold label for the balanced metric.

- Source choice-bias items: `results/analysis/v5_benqa_choice_bias_items.csv`
- By-label table: `results/analysis/v5_benqa_label_balance_by_label.csv`
- Summary table: `results/analysis/v5_benqa_label_balance_summary.csv`
- Bootstrap iterations: 10000

Gold label counts: A=29, B=35, C=41, D=39.

## Label-Balanced Accuracy

| Model | Bangla | Reviewed Banglish | English | Banglish-Bangla | Banglish-English |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 33.2% | 27.9% | 46.2% | -5.3 pts [-13.9, +3.4] | -18.3 pts [-27.8, -8.8] |
| Qwen2.5-7B 8-bit | 42.5% | 33.3% | 60.6% | -9.2 pts [-18.4, +0.4] | -27.3 pts [-37.1, -17.0] |
| Qwen3-4B | 52.0% | 30.3% | 55.8% | -21.7 pts [-29.6, -13.7] | -25.5 pts [-34.6, -16.5] |

## Non-D Stress Slice

This removes gold-D items, where a D-heavy predictor can score by chance
or bias. Qwen3 reviewed Banglish becomes much weaker, which confirms
that option-D over-selection is a failure mode rather than an
explanation away from the script effect.

| Model | n | Bangla | Reviewed Banglish | English | Banglish-Bangla | Banglish-English |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 105 | 35/105 (33.3%) | 27/105 (25.7%) | 48/105 (45.7%) | -7.6 pts [-18.1, +3.8] | -20.0 pts [-31.4, -8.6] |
| Qwen2.5-7B 8-bit | 105 | 54/105 (51.4%) | 39/105 (37.1%) | 69/105 (65.7%) | -14.3 pts [-26.7, -1.9] | -28.6 pts [-40.0, -17.1] |
| Qwen3-4B | 105 | 44/105 (41.9%) | 13/105 (12.4%) | 54/105 (51.4%) | -29.5 pts [-40.0, -19.1] | -39.1 pts [-49.5, -28.6] |

## Gold-D Slice

| Model | Bangla | Reviewed Banglish | English | Banglish-Bangla |
| --- | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 14/39 (35.9%) | 14/39 (35.9%) | 18/39 (46.2%) | 0.0 pts [-10.3, +10.3] |
| Qwen2.5-7B 8-bit | 6/39 (15.4%) | 8/39 (20.5%) | 17/39 (43.6%) | +5.1 pts [-7.7, +17.9] |
| Qwen3-4B | 32/39 (82.0%) | 34/39 (87.2%) | 28/39 (71.8%) | +5.1 pts [-7.7, +17.9] |

## Per-Label Accuracy

| Model | Gold | Bangla | Reviewed Banglish | English |
| --- | --- | ---: | ---: | ---: |
| Qwen2.5-3B | A | 6/29 (20.7%) | 4/29 (13.8%) | 14/29 (48.3%) |
| Qwen2.5-3B | B | 13/35 (37.1%) | 14/35 (40.0%) | 18/35 (51.4%) |
| Qwen2.5-3B | C | 16/41 (39.0%) | 9/41 (21.9%) | 16/41 (39.0%) |
| Qwen2.5-3B | D | 14/39 (35.9%) | 14/39 (35.9%) | 18/39 (46.2%) |
| Qwen2.5-7B 8-bit | A | 17/29 (58.6%) | 10/29 (34.5%) | 20/29 (69.0%) |
| Qwen2.5-7B 8-bit | B | 14/35 (40.0%) | 18/35 (51.4%) | 25/35 (71.4%) |
| Qwen2.5-7B 8-bit | C | 23/41 (56.1%) | 11/41 (26.8%) | 24/41 (58.5%) |
| Qwen2.5-7B 8-bit | D | 6/39 (15.4%) | 8/39 (20.5%) | 17/39 (43.6%) |
| Qwen3-4B | A | 13/29 (44.8%) | 1/29 (3.5%) | 12/29 (41.4%) |
| Qwen3-4B | B | 13/35 (37.1%) | 3/35 (8.6%) | 18/35 (51.4%) |
| Qwen3-4B | C | 18/41 (43.9%) | 9/41 (21.9%) | 24/41 (58.5%) |
| Qwen3-4B | D | 32/39 (82.0%) | 34/39 (87.2%) | 28/39 (71.8%) |

## Interpretation

- Gold-label balancing keeps reviewed Banglish below Bangla and English
  for all three thesis-facing Qwen rows.
- Qwen3-4B is not helped by balancing: reviewed Banglish is
  -21.7 pts below Bangla
  on the balanced metric and -29.5 pts
  below Bangla after removing gold-D items.
- Qwen2.5-7B 8-bit remains negative after label balancing
  (-9.2 pts vs Bangla).
  Qwen2.5-3B remains the qualified row
  (-5.3 pts vs Bangla),
  matching the main-table and paired-sign-test caveat.
- Treat Qwen3 option-D over-selection as a script-conditioned failure
  mode, not as a confound that removes the BEnQA gap.

## Thesis-Safe Claim

Use this as a sensitivity check: the BEnQA reviewed-Banglish deficit
survives gold-label balancing and a non-D stress slice, while Qwen3's
D-heavy behavior is reported as a discovered failure mode.
