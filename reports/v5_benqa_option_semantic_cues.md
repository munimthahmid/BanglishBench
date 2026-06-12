# Frozen-V5 BEnQA Option Semantic-Cue Audit

Updated: 2026-06-11

## Scope

This no-spend audit checks whether the Qwen3 reviewed-Banglish BEnQA
D-attractor is reducible to simple option cues: composite roman-marker
answers such as `i, ii, o iii`, numeric/formula-like strings, or
all/none/both markers. It uses only frozen-v5 option text plus existing
choice-bias and option-switching rows.

- Item table: `results/analysis/v5_benqa_option_semantic_cues_items.csv`
- Summary table: `results/analysis/v5_benqa_option_semantic_cues_summary.csv`

## Headline

- D has a composite/numeric/formula cue on 97/144 BEnQA rows, leaving 47/144 rows where D has no simple semantic cue under this audit.
- On those no-cue rows, Qwen3 still predicts D on 38/47 rows (80.9%), versus 9/47 for Qwen2.5-3B and 4/47 for Qwen2.5-7B.
- Among correct non-D alternate-script predictions where D has no cue, Qwen3 switches to wrong reviewed-Banglish D on 15/18 Bangla rows and 18/23 English rows.
- The corresponding Bangla-side Qwen2.5 counts are only 1/11 and 3/21.

## No-Cue Bucket

| Model | Correct | Pred D on D-no-cue rows | Bangla correct non-D -> wrong D | English correct non-D -> wrong D |
| --- | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 8/47 | 9/47 | 1/11 | 2/20 |
| Qwen2.5-7B 8-bit | 16/47 | 4/47 | 3/21 | 1/27 |
| Qwen3-4B | 11/47 | 38/47 | 15/18 | 18/23 |

## Cue Feature Counts

- D composite: 25/144.
- D numeric/formula-like: 72/144.
- D all/none/both marker: 0/144.
- Any option composite: 25/144; all four options composite: 23/144.

## Interpretation

- Composite and numeric/formula-like options are real local features, but
  they do not explain away Qwen3's D-attractor: the strongest model still
  over-selects D when D lacks these cues.
- The audit is cue-based and behavioral. It should be cited as a confound
  check, not as proof of an internal semantic mechanism.

## Reproducibility

- Builder: `scripts/analyze_v5_benqa_option_semantic_cues.py`
- Item rows: 432
- Summary rows: 25
