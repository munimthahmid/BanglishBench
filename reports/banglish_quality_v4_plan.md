# Banglish Quality v4 Plan

Updated: 2026-05-28

## Why This Matters

The current v3 benchmark is good enough for the main open-model result because
both models show large clean-Banglish drops even after two romanizer cleanups.
However, the final thesis should not rely only on unreviewed rule-based
Banglish. v4 should make the Banglish fields more natural and explicitly mark
what remains machine-generated.

## Current Audit Signal

Validation-200 v3 artifact audit:

| Pattern | Clean Items | Clean Occurrences | Noisy Items | Noisy Occurrences |
| --- | ---: | ---: | ---: | ---: |
| `tb` virama-b cluster | 11 | 14 | 11 | 14 |
| `boij` scientific-name pattern | 1 | 1 | 0 | 0 |
| `oja` loanword pattern | 13 | 20 | 13 | 20 |
| `khady` Sanskritized food word | 5 | 6 | 0 | 0 |
| `ksh` heavy conjunct | 41 | 48 | 0 | 0 |
| `db` cluster | 15 | 16 | 15 | 16 |
| `jn` cluster | 1 | 1 | 1 | 1 |

Primary files:

- `results/analysis/validation200_v3_banglish_artifact_summary.csv`
- `results/analysis/validation200_v3_banglish_artifact_examples.csv`
- `data/slices/banglish_human_review_priority_v1.csv`

## Safe Deterministic Fix Candidates

These are likely worth implementing in `scripts/bn_romanize.py` before building
`pilot_v4` and `validation_200_v4`.

| Current | Better v4 direction | Reason |
| --- | --- | --- |
| `dbitiy`, `dbigun`, `dbara` | `dwitiy`, `dwigun`, `dwara` | The current `db` cluster is visibly unnatural for `দ্ব`. |
| `ojamoniyam`, `ojaluminiyam`, `ojampiyar` | `amoniyam`, `aluminiyam`, `ampiyar` | Bengali `অ্য` loanword spelling should not become `oja`. |
| `boijnanik` | `boigganik` | Common Banglish for `বৈজ্ঞানিক` is closer to `boigganik`. |
| `khady`, `khadye`, `khadyer` | `khaddo`, `khadde`, `khadder` | The current form is too Sanskritized for natural Banglish. |

## Risky or Context-Dependent Fixes

These should not be globally replaced without manual examples.

| Pattern | Risk |
| --- | --- |
| `tb` from `ত্ব` | Some words prefer `tw` (`tworon`, `twok`), while others prefer `tto` (`durotto`, `gurutto`). A single global rule will be wrong for some items. |
| `ksh` from `ক্ষ` | `kshetra`-style transliteration is formal but not always invalid. Natural Banglish may use `kkh`, `kh`, or `khe` depending on the word. |
| `jn` from `জ্ঞ` | `boigganik` is clear, but other `জ্ঞ` words may be written as `gg`, `gy`, `jn`, or rewritten lexically. |

## Proposed v4 Procedure

1. Patch the romanizer for safe deterministic cases only.
2. Rebuild `data/pilot_v4/items.jsonl`.
3. Rebuild `data/slices/validation_200_v4.jsonl` with the same item ids as
   validation-200 v3, so item identity stays fixed and only Banglish changes.
4. Re-run artifact audit on v4 and compare v3 vs v4 text diffs.
5. Keep validation-200 v3 as the already-computed empirical baseline.
6. Use v4 only after auditing the text changes and deciding whether another GPU
   confirmation run is worth the cost.

## Human Review Policy

For the thesis, the safest final statement is:

- v3/v4 clean Banglish is controlled rule-based Banglish, not claimed to be a
  fully natural user distribution.
- Noisy Banglish is a deterministic stress variant, not a natural corpus.
- A small human-reviewed subset should be used to estimate how often the
  romanizer is acceptable, awkward, or wrong.

The priority review CSV already exists:

- `data/slices/banglish_human_review_priority_v1.csv`

Minimum useful review target:

- 50 high-priority items across validation and MGSM.
- Labels: `good`, `awkward_but_understandable`, `wrong_or_misleading`.
- Optional corrected Banglish in `reviewed_banglish`.

## Decision

Do not replace the current thesis-facing validation-200 v3 result yet. First
finish the active noisy-Banglish runs, then implement v4 as a dataset-quality
upgrade and evaluate whether the change affects the measured script gap.

## v4 Implementation Checkpoint

Implemented:

- `scripts/rebuild_banglish_fields.py`
- `scripts/export_banglish_diff_report.py`
- v4 romanizer post-processing in `scripts/bn_romanize.py`

Generated slices:

- `data/pilot_v4/items.jsonl`
- `data/slices/validation_100_v4.jsonl`
- `data/slices/validation_200_v4.jsonl`
- `data/slices/mgsm_bn_50_v2.jsonl`

All generated slices preserve item ids and item order from their v3/v1 inputs.

Change counts:

| Slice | Changed clean | Changed noisy |
| --- | ---: | ---: |
| Pilot v4 | 46/300 | 46/300 |
| Validation-100 v4 | 16/100 | 16/100 |
| Validation-200 v4 | 38/200 | 38/200 |
| MGSM bn50 v2 | 14/50 | 14/50 |

Validation-200 artifact counts after v4:

| Pattern | Clean Items | Noisy Items |
| --- | ---: | ---: |
| `tb` virama-b cluster | 4 | 4 |
| `boij` scientific-name pattern | 0 | 0 |
| `oja` loanword pattern | 2 | 2 |
| `khady` Sanskritized food word | 0 | 0 |
| `ksh` heavy conjunct | 41 | 0 |
| `db` cluster | 0 | 0 |
| `jn` cluster | 0 | 0 |

Inspection reports:

- `reports/validation200_v3_to_v4_banglish_diff.md`
- `reports/mgsm_bn50_v1_to_v2_banglish_diff.md`

Next decision:

- Do not immediately rerun all baselines on v4. First inspect the diff report
  and finish validation-200 noisy v3, then decide whether v4 merits a focused
  Banglish-only confirmation run.
