# Frozen-V5 Shared Fragility Examples

Updated: 2026-06-11

## Scope

This reproducible packet selects qualitative examples from the frozen-v5
model-overlap table. The cleanest examples are items where every
thesis-facing Qwen row is correct in Bangla and English but wrong in
reviewed Banglish.

- Machine-readable examples: `results/analysis/v5_shared_fragility_examples.csv`
- Overlap source: `results/analysis/v5_banglish_fragility_model_overlap_items.csv`
- Failure-pattern source: `results/analysis/validation200_v5_cross_script_failure_patterns_items.csv`

## Summary

- Shared fragility: 56/200 items affect at least two Qwen rows.
- All-three fragility: 21/200 items affect all three Qwen rows.
- Shared strict fragility: 17/200 items affect at least two rows
  under the strongest Bangla+English-correct/Banglish-wrong pattern.
- All-three strict examples: 5/200 items.

## Recommended Main-Body Shortlist

| Item | Task | Gold | Why it belongs |
| --- | --- | --- | --- |
| `banglamath_0229` | BanglaMATH six | `1.5` | All three Qwen rows are strict; short arithmetic failure. |
| `banglamath_0230` | BanglaMATH six | `20%` | All three Qwen rows are strict; short arithmetic failure. |
| `benqa_10th-Physics_0021` | BEnQA 10th Physics | `C` | All three Qwen rows are strict; non-arithmetic MCQ failure with simple option parsing. |

## All-Three Strict Cases

| Item | Task | Gold | Reviewed-Banglish parsed answers |
| --- | --- | --- | --- |
| `banglamath_0229` | BanglaMATH six | `1.5` | `Qwen2.5-3B: 50%; Qwen2.5-7B 8-bit: 3七年五个月; Qwen3-4B: 150` |
| `banglamath_0230` | BanglaMATH six | `20%` | `Qwen2.5-3B: 100 taka; Qwen2.5-7B 8-bit: 5; Qwen3-4B: .` |
| `benqa_10th-Math_0044` | BEnQA 10th Math | `C` | `Qwen2.5-3B: B; Qwen2.5-7B 8-bit: A; Qwen3-4B: D` |
| `benqa_10th-Physics_0021` | BEnQA 10th Physics | `C` | `Qwen2.5-3B: B; Qwen2.5-7B 8-bit: A; Qwen3-4B: D` |
| `benqa_8th-Science_0202` | BEnQA 8th Science | `C` | `Qwen2.5-3B: A; Qwen2.5-7B 8-bit: A; Qwen3-4B: A` |

## Detailed Main-Body Examples

### banglamath_0229

- Task: BanglaMATH six
- Gold: `1.5`
- Review label: `unreviewed`
- Strict models: Qwen2.5-3B, Qwen2.5-7B 8-bit, Qwen3-4B

| Script | Prompt snippet |
| --- | --- |
| Bangla | `১৫০% কে দশমিক ভগ্নাংশে প্রকাশ করলে কী হয় Return only the final answer.` |
| Reviewed Banglish | `150% ke doshomik bhognangshe prokash korole ki hoy Return only the final answer.` |
| English | `What is 150% expressed as a decimal? Return only the final answer.` |

| Model | Pattern | Bangla parsed | Banglish parsed | English parsed |
| --- | --- | --- | --- | --- |
| Qwen2.5-3B | `bangla_english_correct_banglish_wrong` | `1.50` | `50%` | `1.5` |
| Qwen2.5-7B 8-bit | `bangla_english_correct_banglish_wrong` | `1.5` | `3七年五个月` | `1.5` |
| Qwen3-4B | `bangla_english_correct_banglish_wrong` | `1.5` | `150` | `1.5` |

Use this as a qualitative illustration only; the aggregate overlap and
failure-taxonomy reports remain the evidence for the claim.

### banglamath_0230

- Task: BanglaMATH six
- Gold: `20%`
- Review label: `minor_edit`
- Strict models: Qwen2.5-3B, Qwen2.5-7B 8-bit, Qwen3-4B

| Script | Prompt snippet |
| --- | --- |
| Bangla | `২৫ টাকা ১২৫ টাকার শতকরা কত Return only the final answer.` |
| Reviewed Banglish | `25 taka 125 takar shotkora koto Return only the final answer.` |
| English | `25 Taka is what percent of 125 Taka? Return only the final answer.` |

| Model | Pattern | Bangla parsed | Banglish parsed | English parsed |
| --- | --- | --- | --- | --- |
| Qwen2.5-3B | `bangla_english_correct_banglish_wrong` | `20%` | `100 taka` | `20%` |
| Qwen2.5-7B 8-bit | `bangla_english_correct_banglish_wrong` | `20%` | `5` | `20%` |
| Qwen3-4B | `bangla_english_correct_banglish_wrong` | `25 টাকা 125 টাকার শতকরা = (25 / 125) × 100 = 20%` | `.` | `20%` |

Use this as a qualitative illustration only; the aggregate overlap and
failure-taxonomy reports remain the evidence for the claim.

### benqa_10th-Physics_0021

- Task: BEnQA 10th Physics
- Gold: `C`
- Review label: `minor_edit`
- Strict models: Qwen2.5-3B, Qwen2.5-7B 8-bit, Qwen3-4B

| Script | Prompt snippet |
| --- | --- |
| Bangla | `কোনটি মৌলিক একক? A. জুল B. নিউটন C. ক্যান্ডেলা D. প্যাসকেল Answer with only A, B, C, or D.` |
| Reviewed Banglish | `konti moulik ekok? A. jul B. niuton C. kyandela D. pyasokel Answer with only A, B, C, or D.` |
| English | `Which one is fundamental unit? A. Joule B. Newton C. Candela D. Pascal Answer with only A, B, C, or D.` |

| Model | Pattern | Bangla parsed | Banglish parsed | English parsed |
| --- | --- | --- | --- | --- |
| Qwen2.5-3B | `bangla_english_correct_banglish_wrong` | `C` | `B` | `C` |
| Qwen2.5-7B 8-bit | `bangla_english_correct_banglish_wrong` | `C` | `A` | `C` |
| Qwen3-4B | `bangla_english_correct_banglish_wrong` | `C` | `D` | `C` |

Use this as a qualitative illustration only; the aggregate overlap and
failure-taxonomy reports remain the evidence for the claim.

## Appendix Shared-Strict Candidates

These rows are still strong qualitative candidates, but not all three
models satisfy the strict pattern. Use them when the appendix needs
broader domain coverage.

| Item | Task | Gold | Strict models | Fragile models |
| --- | --- | --- | --- | --- |
| `banglamath_0526` | BanglaMATH seven | `৩০ বর্গ মিটার` | Qwen2.5-3B, Qwen2.5-7B 8-bit | Qwen2.5-3B, Qwen2.5-7B 8-bit, Qwen3-4B |
| `benqa_12th-Biology-I_0222` | BEnQA 12th Biology-I | `A` | Qwen2.5-3B, Qwen2.5-7B 8-bit | Qwen2.5-3B, Qwen2.5-7B 8-bit |
| `benqa_12th-Biology-I_0283` | BEnQA 12th Biology-I | `A` | Qwen2.5-7B 8-bit, Qwen3-4B | Qwen2.5-3B, Qwen2.5-7B 8-bit, Qwen3-4B |
| `benqa_12th-Biology-II_0179` | BEnQA 12th Biology-II | `A` | Qwen2.5-7B 8-bit, Qwen3-4B | Qwen2.5-3B, Qwen2.5-7B 8-bit, Qwen3-4B |
| `benqa_12th-Biology-II_0287` | BEnQA 12th Biology-II | `B` | Qwen2.5-7B 8-bit, Qwen3-4B | Qwen2.5-7B 8-bit, Qwen3-4B |
| `benqa_10th-Chemistry_0132` | BEnQA 10th Chemistry | `A` | Qwen2.5-7B 8-bit, Qwen3-4B | Qwen2.5-3B, Qwen2.5-7B 8-bit, Qwen3-4B |
| `benqa_10th-Chemistry_0322` | BEnQA 10th Chemistry | `B` | Qwen2.5-7B 8-bit, Qwen3-4B | Qwen2.5-7B 8-bit, Qwen3-4B |
| `benqa_12th-Chemistry-I_0174` | BEnQA 12th Chemistry-I | `A` | Qwen2.5-7B 8-bit, Qwen3-4B | Qwen2.5-3B, Qwen2.5-7B 8-bit, Qwen3-4B |
| `benqa_12th-Chemistry-II_0228` | BEnQA 12th Chemistry-II | `C` | Qwen2.5-3B, Qwen3-4B | Qwen2.5-3B, Qwen3-4B |
| `benqa_12th-Chemistry-II_0235` | BEnQA 12th Chemistry-II | `A` | Qwen2.5-7B 8-bit, Qwen3-4B | Qwen2.5-7B 8-bit, Qwen3-4B |
| `benqa_12th-Physics-I_0133` | BEnQA 12th Physics-I | `C` | Qwen2.5-7B 8-bit, Qwen3-4B | Qwen2.5-7B 8-bit, Qwen3-4B |
| `benqa_8th-Science_0153` | BEnQA 8th Science | `C` | Qwen2.5-3B, Qwen3-4B | Qwen2.5-3B, Qwen3-4B |

## Thesis Boundary

Use these examples to make the aggregate script-gap and overlap results
concrete. Do not treat a small qualitative packet as standalone proof
of the mechanism; cite the frozen-v5 diagnostics and overlap counts for
the evidentiary claim.
