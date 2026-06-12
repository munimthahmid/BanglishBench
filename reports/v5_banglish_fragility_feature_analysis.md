# Reviewed-V5 Banglish Fragility Feature Analysis

Updated: 2026-06-11

## Scope

This no-spend analysis joins the frozen-v5 cross-script failure rows with
validation-item metadata. A fragility event means a thesis-facing Qwen
model answered reviewed Banglish incorrectly while answering Bangla or
English correctly on the same item. Counts are descriptive; they are not
used as a deployable routing rule.

- Items: `data/slices/validation_200_v5.jsonl`
- Failure rows: `results/analysis/validation200_v5_cross_script_failure_patterns_items.csv`
- Item output: `results/analysis/v5_banglish_fragility_items.csv`
- Feature summary: `results/analysis/v5_banglish_fragility_feature_summary.csv`

## Overall

- Items: 200
- Model-item slots: 600
- Banglish fragility events: 185/600 (30.8%)
- Strict Bangla+English-correct/Banglish-wrong events: 76/600 (12.7%)
- Items with at least one fragile model: 108/200 (54.0%)
- Items fragile for all three thesis-facing models: 21/200 (10.5%)
- All-script-wrong events: 278/600 (46.3%)

## Highest Fragility Domains

| Domain | Items | Fragility events | Event rate | Any fragile | Strict events |
| --- | ---: | ---: | ---: | ---: | ---: |
| biology-i | 11 | 19/33 | 57.6% | 10/11 | 8 |
| biology-ii | 11 | 16/33 | 48.5% | 9/11 | 4 |
| chemistry-ii | 11 | 16/33 | 48.5% | 9/11 | 11 |
| biology | 12 | 17/36 | 47.2% | 10/12 | 3 |
| chemistry-i | 11 | 14/33 | 42.4% | 7/11 | 6 |
| science | 11 | 14/33 | 42.4% | 8/11 | 7 |
| chemistry | 11 | 13/33 | 39.4% | 6/11 | 6 |
| physics | 11 | 12/33 | 36.4% | 8/11 | 5 |

## Feature Signals

| Feature | Value | Items | Fragility events | Event rate | All-script-wrong event rate | Any fragile |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `dataset` | `benqa` | 144 | 164/432 | 38.0% | 30.8% | 95/144 |
| `dataset` | `banglamath` | 56 | 21/168 | 12.5% | 86.3% | 13/56 |
| `task_type` | `mcq` | 144 | 164/432 | 38.0% | 30.8% | 95/144 |
| `task_type` | `short_answer` | 56 | 21/168 | 12.5% | 86.3% | 13/56 |
| `review_label` | `unreviewed` | 60 | 74/180 | 41.1% | 36.1% | 44/60 |
| `review_label` | `minor_edit` | 126 | 108/378 | 28.6% | 47.6% | 63/126 |
| `review_label` | `major_edit` | 11 | 3/33 | 9.1% | 84.9% | 1/11 |
| `has_digits` | `True` | 139 | 93/417 | 22.3% | 56.1% | 60/139 |
| `has_digits` | `False` | 61 | 92/183 | 50.3% | 24.0% | 48/61 |
| `has_formula_or_operator` | `True` | 93 | 79/279 | 28.3% | 37.6% | 50/93 |
| `has_formula_or_operator` | `False` | 107 | 106/321 | 33.0% | 53.9% | 58/107 |
| `has_roman_statement_list` | `True` | 25 | 25/75 | 33.3% | 32.0% | 12/25 |
| `has_science_symbol` | `True` | 8 | 9/24 | 37.5% | 33.3% | 4/8 |
| `long_banglish_words_q4` | `True` | 51 | 36/153 | 23.5% | 46.4% | 21/51 |

## Most Fragile Items

| Item | Domain | Events | Strict | Patterns | Banglish preview |
| --- | --- | ---: | ---: | --- | --- |
| `banglamath_0229` | math | 3 | 3 | Qwen2.5-3B: bangla_english_correct_banglish_wrong, Qwen2.5-7B: bangla_english_correct_banglish_wrong, Qwen3-4B: bangla_english_correct_banglish_wrong | 150% ke doshomik bhognangshe prokash korole ki hoy Return only the final answer. |
| `banglamath_0230` | math | 3 | 3 | Qwen2.5-3B: bangla_english_correct_banglish_wrong, Qwen2.5-7B: bangla_english_correct_banglish_wrong, Qwen3-4B: bangla_english_correct_banglish_wrong | 25 taka 125 takar shotkora koto Return only the final answer. |
| `benqa_10th-Math_0044` | math | 3 | 3 | Qwen2.5-3B: bangla_english_correct_banglish_wrong, Qwen2.5-7B: bangla_english_correct_banglish_wrong, Qwen3-4B: bangla_english_correct_banglish_wrong | ekti borger kototi protisamy rekha ache? A. 8ti B. 6ti C. 4ti D. 2ti Answer with only A, B, C, or D. |
| `benqa_10th-Physics_0021` | physics | 3 | 3 | Qwen2.5-3B: bangla_english_correct_banglish_wrong, Qwen2.5-7B: bangla_english_correct_banglish_wrong, Qwen3-4B: bangla_english_correct_banglish_wrong | konti moulik ekok? A. jul B. niuton C. kyandela D. pyasokel Answer with only A, B, C, or D. |
| `benqa_8th-Science_0202` | science | 3 | 3 | Qwen2.5-3B: bangla_english_correct_banglish_wrong, Qwen2.5-7B: bangla_english_correct_banglish_wrong, Qwen3-4B: bangla_english_correct_banglish_wrong | sothik khaddo-shringkhol konti? A. ghas \rightarrow faitoplyangkoton \rightarrow juplangkoton B. ju-plangkoton \rightarrow fait... |
| `banglamath_0526` | math | 3 | 2 | Qwen2.5-3B: bangla_english_correct_banglish_wrong, Qwen2.5-7B: bangla_english_correct_banglish_wrong, Qwen3-4B: english_only_correct | ekti tribhujer bhumi 10 mitar o ucchota 6 mitar hole khetrofol koto Return only the final answer. |
| `benqa_10th-Chemistry_0132` | chemistry | 3 | 2 | Qwen2.5-3B: english_only_correct, Qwen2.5-7B: bangla_english_correct_banglish_wrong, Qwen3-4B: bangla_english_correct_banglish_wrong | bisforok podarth konti? A. ti.en.ti B. benojin C. toluin D. jailin Answer with only A, B, C, or D. |
| `benqa_12th-Biology-II_0179` | biology-ii | 3 | 2 | Qwen2.5-3B: english_only_correct, Qwen2.5-7B: bangla_english_correct_banglish_wrong, Qwen3-4B: bangla_english_correct_banglish_wrong | rokt jomat bandhote kon dhatob ayon sohayota kore? A. Ca^{++} B. Mg^{++} C. Cu^{++} D. Fe^{++} Answer with only A, B, C, or D. |
| `benqa_12th-Biology-I_0283` | biology-i | 3 | 2 | Qwen2.5-3B: english_only_correct, Qwen2.5-7B: bangla_english_correct_banglish_wrong, Qwen3-4B: bangla_english_correct_banglish_wrong | penper ring spot roger lokshon holo- i. patar botay pani bheja sobuj dag dekha jay ii. penper mishtota hras pay iii. foler akar... |
| `benqa_12th-Chemistry-I_0174` | chemistry-i | 3 | 2 | Qwen2.5-3B: english_only_correct, Qwen2.5-7B: bangla_english_correct_banglish_wrong, Qwen3-4B: bangla_english_correct_banglish_wrong | bhinegar- i. khadder byakoteriya dhbongs kora ii. khabarer ruchi briddhi kore iii. rokt sonchalon komay nicher konti sothik? A.... |

## Interpretation

- Banglish fragility is not confined to one dataset: the item-level output
  records both the concentrated domains and the all-script-wrong cases.
- Recoverable Banglish-specific fragility is concentrated in BEnQA MCQ
  science domains, especially biology and chemistry subjects.
- BanglaMATH short-answer rows show fewer recoverable fragility events
  because many are all-script-wrong; that is difficulty headroom rather
  than evidence that Banglish is solved for math.
- Digit/formula prompts remain a preservation-audit surface for generated
  views, but in the completed open-model outputs they more often appear as
  all-script difficulty than as recoverable Banglish-only fragility.
- The analysis strengthens the thesis failure-analysis chapter, but it does
  not change the main accuracy table or authorize any new held-out routing.
