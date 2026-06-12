# Frozen-V5 Cross-Script Transfer Retention

Updated: 2026-06-11

## Scope

This no-spend diagnostic asks a conditional robustness question: when a
model answers an item correctly in Bangla or English, how often does the
same model retain correctness in reviewed Banglish? It complements the
oracle/recoverability tables by reporting retention rates over items the
model has already demonstrated it can solve in another script.

- Source failure table: `results/analysis/validation200_v5_cross_script_failure_patterns_items.csv`
- Item flags: `results/analysis/v5_cross_script_transfer_items.csv`
- Summary table: `results/analysis/v5_cross_script_transfer_summary.csv`

Wilson intervals are reported for conditional proportions. These are
behavioral diagnostics, not causal mechanism estimates.

## All-200 Transfer Retention

| Model | If Bangla Correct | If English Correct | If Bangla or English Correct | If Both Correct |
| --- | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 26/54 (48.1%, CI [35.4%, 61.2%]) | 26/71 (36.6%, CI [26.4%, 48.2%]) | 34/92 (37.0%, CI [27.8%, 47.2%]) | 18/33 (54.5%, CI [38.0%, 70.2%]) |
| Qwen2.5-7B 8-bit | 28/65 (43.1%, CI [31.8%, 55.2%]) | 34/94 (36.2%, CI [27.2%, 46.2%]) | 39/107 (36.4%, CI [28.0%, 45.9%]) | 23/52 (44.2%, CI [31.6%, 57.7%]) |
| Qwen3-4B | 41/80 (51.2%, CI [40.5%, 61.9%]) | 36/88 (40.9%, CI [31.2%, 51.3%]) | 44/103 (42.7%, CI [33.6%, 52.4%]) | 33/65 (50.8%, CI [38.9%, 62.5%]) |

## BEnQA Transfer Retention

| Model | If Bangla Correct | If English Correct | If Bangla or English Correct | If Both Correct |
| --- | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 26/49 (53.1%, CI [39.4%, 66.3%]) | 26/66 (39.4%, CI [28.5%, 51.4%]) | 34/85 (40.0%, CI [30.2%, 50.6%]) | 18/30 (60.0%, CI [42.3%, 75.4%]) |
| Qwen2.5-7B 8-bit | 28/60 (46.7%, CI [34.6%, 59.1%]) | 34/86 (39.5%, CI [29.9%, 50.1%]) | 39/97 (40.2%, CI [31.0%, 50.2%]) | 23/49 (46.9%, CI [33.7%, 60.6%]) |
| Qwen3-4B | 39/76 (51.3%, CI [40.3%, 62.2%]) | 34/82 (41.5%, CI [31.4%, 52.3%]) | 42/97 (43.3%, CI [33.9%, 53.2%]) | 31/61 (50.8%, CI [38.6%, 62.9%]) |

## BanglaMATH Stress-Test Retention

| Model | If Bangla or English Correct | If Both Correct |
| --- | ---: | ---: |
| Qwen2.5-3B | 0/7 (0.0%, CI [0.0%, 35.4%]) | 0/3 (0.0%, CI [0.0%, 56.1%]) |
| Qwen2.5-7B 8-bit | 0/10 (0.0%, CI [0.0%, 27.8%]) | 0/3 (0.0%, CI [0.0%, 56.1%]) |
| Qwen3-4B | 2/6 (33.3%, CI [9.7%, 70.0%]) | 2/4 (50.0%, CI [15.0%, 85.0%]) |

## Interpretation

- Across the 600 model-item slots, 185 have Bangla or
  English correct while reviewed Banglish is wrong; 76
  are the stricter Bangla+English-correct/Banglish-wrong cases.
- Qwen3-4B retains reviewed-Banglish correctness on only
  33/65
  all-200 items where both Bangla and English are correct.
- Qwen2.5-7B 8-bit retains Banglish on
  39/107
  items where either Bangla or English is correct; Qwen2.5-3B retains
  34/92.
- BanglaMATH denominators are small because the models rarely solve
  those items in any script; keep that dataset as a stress test.

Thesis-safe phrasing:

> The reviewed-Banglish deficit is not just low overall competence:
> even after conditioning on same-model correctness in Bangla or
> English, many items lose correctness in reviewed Banglish.
