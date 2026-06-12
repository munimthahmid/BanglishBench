# Cross-Script Answer Agreement Examples

Updated: 2026-06-11

These examples support `reports/cross_script_diagnostics_validation200_v5.md`.
Prompt snippets and Banglish outputs use frozen reviewed validation-200 v5.
Bangla and English outputs are reused because those fields did not change.

## Qwen2.5-3B

### Bangla+English Agreement Recovers Banglish Failure

### Example 1: Qwen2.5-3B / banglamath_0230

- Dataset: `banglamath`
- Gold: `20%`
- Agreement bucket: `bangla_english_agree_banglish_differs`
- Bangla parsed: `20%`; correct: `True`
- Banglish parsed: `100 taka`; correct: `False`
- English parsed: `20%`; correct: `True`

Banglish prompt snippet:

```text
25 taka 125 takar shotkora koto Return only the final answer.
```

English prompt snippet:

```text
25 Taka is what percent of 125 Taka? Return only the final answer.
```

### Example 2: Qwen2.5-3B / banglamath_0526

- Dataset: `banglamath`
- Gold: `৩০ বর্গ মিটার`
- Agreement bucket: `bangla_english_agree_banglish_differs`
- Bangla parsed: `30 বর্গমিটার`; correct: `True`
- Banglish parsed: `3`; correct: `False`
- English parsed: `30 square meters`; correct: `True`

Banglish prompt snippet:

```text
ekti tribhujer bhumi 10 mitar o ucchota 6 mitar hole khetrofol koto Return only the final answer.
```

English prompt snippet:

```text
If a triangle has a base of 10 meters and height of 6 meters, what is its area? Return only the final answer.
```

### Recoverable But All Three Answers Differ

### Example 3: Qwen2.5-3B / banglamath_0185

- Dataset: `banglamath`
- Gold: `২০০ কেজি`
- Agreement bucket: `all_three_different`
- Bangla parsed: `২০০ কেজি`; correct: `True`
- Banglish parsed: `20 keji chale`; correct: `False`
- English parsed: `384 kg`; correct: `False`

Banglish prompt snippet:

```text
120 keji chale 10 jon loker 27 din chole. 45 din cholote koto keji chal proyojon hobe Return only the final answer.
```

English prompt snippet:

```text
120 kg of rice lasts 10 people for 27 days. How much rice is needed to last 45 days? Return only the final answer.
```

## Qwen2.5-7B 8-bit

### Bangla+English Agreement Recovers Banglish Failure

### Example 4: Qwen2.5-7B 8-bit / banglamath_0229

- Dataset: `banglamath`
- Gold: `1.5`
- Agreement bucket: `bangla_english_agree_banglish_differs`
- Bangla parsed: `1.5`; correct: `True`
- Banglish parsed: `3七年五个月`; correct: `False`
- English parsed: `1.5`; correct: `True`

Banglish prompt snippet:

```text
150% ke doshomik bhognangshe prokash korole ki hoy Return only the final answer.
```

English prompt snippet:

```text
What is 150% expressed as a decimal? Return only the final answer.
```

### Example 5: Qwen2.5-7B 8-bit / banglamath_0230

- Dataset: `banglamath`
- Gold: `20%`
- Agreement bucket: `bangla_english_agree_banglish_differs`
- Bangla parsed: `20%`; correct: `True`
- Banglish parsed: `5`; correct: `False`
- English parsed: `20%`; correct: `True`

Banglish prompt snippet:

```text
25 taka 125 takar shotkora koto Return only the final answer.
```

English prompt snippet:

```text
25 Taka is what percent of 125 Taka? Return only the final answer.
```

### Recoverable But All Three Answers Differ

### Example 6: Qwen2.5-7B 8-bit / banglamath_0182

- Dataset: `banglamath`
- Gold: `৬০০ টাকা`
- Agreement bucket: `all_three_different`
- Bangla parsed: `600টাকা`; correct: `True`
- Banglish parsed: `400`; correct: `False`
- English parsed: `600`; correct: `False`

Banglish prompt snippet:

```text
7 keji chaler dam 280 taka hole 15 keji chaler dam koto Return only the final answer.
```

English prompt snippet:

```text
If 7 kg of rice costs 280 Taka, what is the cost of 15 kg? Return only the final answer.
```

## Qwen3-4B

### Bangla+English Agreement Recovers Banglish Failure

### Example 7: Qwen3-4B / banglamath_0229

- Dataset: `banglamath`
- Gold: `1.5`
- Agreement bucket: `bangla_english_agree_banglish_differs`
- Bangla parsed: `1.5`; correct: `True`
- Banglish parsed: `150`; correct: `False`
- English parsed: `1.5`; correct: `True`

Banglish prompt snippet:

```text
150% ke doshomik bhognangshe prokash korole ki hoy Return only the final answer.
```

English prompt snippet:

```text
What is 150% expressed as a decimal? Return only the final answer.
```

### Example 8: Qwen3-4B / benqa_10th-Biology_0156

- Dataset: `benqa`
- Gold: `C`
- Agreement bucket: `bangla_english_agree_banglish_differs`
- Bangla parsed: `C`; correct: `True`
- Banglish parsed: `D`; correct: `False`
- English parsed: `C`; correct: `True`

Banglish prompt snippet:

```text
amishe shotkora koto bhag naitrojen bidyoman A. 12 B. 14 C. 16 D. 18 Answer with only A, B, C, or D.
```

English prompt snippet:

```text
What percentage of Nitrogen is present in protein? A. 12 B. 14 C. 16 D. 18 Answer with only A, B, C, or D.
```

### Recoverable But All Three Answers Differ

### Example 9: Qwen3-4B / banglamath_0231

- Dataset: `banglamath`
- Gold: `২০ টাকা`
- Agreement bucket: `all_three_different`
- Bangla parsed: `1.2x = 24`; correct: `False`
- Banglish parsed: `19.2`; correct: `False`
- English parsed: `The cost price is **20 Taka**.`; correct: `True`

Banglish prompt snippet:

```text
ekti kolom 20% labhe 24 takay bikroy korle kroyomullo koto Return only the final answer.
```

English prompt snippet:

```text
If a pen is sold for 24 Taka with 20% profit, what was the cost price? Return only the final answer.
```
