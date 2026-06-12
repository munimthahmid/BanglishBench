# Script-Gap Examples: `bangla_english_correct_banglish_wrong`

Source gaps: `results/analysis/validation200_v3_cross_script_failure_patterns_items.csv`
Items: `data/slices/validation_200_v3.jsonl`
Filters: `{'model': 'Qwen/Qwen3-4B-Instruct-2507'}`
Examples exported: 8

## 1. banglamath_0229 (banglamath, short_answer)

Model: `Qwen/Qwen3-4B-Instruct-2507`

Gold: `1.5`

**Bangla Prompt**

```text
১৫০% কে দশমিক ভগ্নাংশে প্রকাশ করলে কী হয়
Return only the final answer.
```

Bangla parsed: `1.5`; correct: `True`

**Banglish Prompt**

```text
150% ke doshomik bhognangshe prokash korole ki hoy
Return only the final answer.
```

Banglish parsed: `150`; correct: `False`

**English Prompt**

```text
What is 150% expressed as a decimal?
Return only the final answer.
```

English parsed: `1.5`; correct: `True`

## 2. banglamath_0230 (banglamath, short_answer)

Model: `Qwen/Qwen3-4B-Instruct-2507`

Gold: `20%`

**Bangla Prompt**

```text
২৫ টাকা ১২৫ টাকার শতকরা কত
Return only the final answer.
```

Bangla parsed: `25 টাকা 125 টাকার শতকরা = (25 / 125) × 100 = 20%`; correct: `True`

**Banglish Prompt**

```text
25 taka 125 takar shotokora kot
Return only the final answer.
```

Banglish parsed: `invalid input`; correct: `False`

**English Prompt**

```text
25 Taka is what percent of 125 Taka?
Return only the final answer.
```

English parsed: `20%`; correct: `True`

## 3. banglamath_1697 (banglamath, short_answer)

Model: `Qwen/Qwen3-4B-Instruct-2507`

Gold: `70`

**Bangla Prompt**

```text
৩০ কে ১/২ দিয়ে ভাগ করে ১০ যোগ করলে কত হয়?
Return only the final answer.
```

Bangla parsed: `70`; correct: `True`

**Banglish Prompt**

```text
30 ke 1/2 diye bhag kore 10 jog korole kot hoy?
Return only the final answer.
```

Banglish parsed: `600`; correct: `False`

**English Prompt**

```text
Divide 30 by ½ and add 10. What is the result?
Return only the final answer.
```

English parsed: `70`; correct: `True`

## 4. benqa_10th-Biology_0156 (benqa, mcq)

Model: `Qwen/Qwen3-4B-Instruct-2507`

Gold: `C`

**Bangla Prompt**

```text
আমিষে শতকরা কত ভাগ নাইট্রোজেন বিদ্যমান
A. 12
B. 14
C. 16
D. 18
Answer with only A, B, C, or D.
```

Bangla parsed: `C`; correct: `True`

**Banglish Prompt**

```text
amishe shotokora kot bhag naitrojen bidyoman
A. 12
B. 14
C. 16
D. 18
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
What percentage of Nitrogen is present in protein?
A. 12
B. 14
C. 16
D. 18
Answer with only A, B, C, or D.
```

English parsed: `C`; correct: `True`

## 5. benqa_10th-Chemistry_0132 (benqa, mcq)

Model: `Qwen/Qwen3-4B-Instruct-2507`

Gold: `A`

**Bangla Prompt**

```text
বিস্ফোরক পদার্থ কোনটি?
A. টি.এন.টি
B. বেনজিন
C. টলুইন
D. জাইলিন
Answer with only A, B, C, or D.
```

Bangla parsed: `A`; correct: `True`

**Banglish Prompt**

```text
bisforok podarth konoti?
A. ti.en.ti
B. benojin
C. toluin
D. jailin
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
Which one is explosive substance?
A. TNT
B. Benzene
C. Toluene
D. Xylene
Answer with only A, B, C, or D.
```

English parsed: `A`; correct: `True`

## 6. benqa_10th-Chemistry_0322 (benqa, mcq)

Model: `Qwen/Qwen3-4B-Instruct-2507`

Gold: `B`

**Bangla Prompt**

```text
কোনটির অণুতে দ্বি-বন্ধন বিদ্যমান?
A. হাইড্রোজেন
B. অক্সিজেন
C. নাইট্রোজেন
D. ক্লোরিন
Answer with only A, B, C, or D.
```

Bangla parsed: `B`; correct: `True`

**Banglish Prompt**

```text
konotir onute dbi-bondhon bidyoman?
A. haidrojen
B. oksijen
C. naitrojen
D. klorin
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
Which molecule contains double bond?
A. Hydrogen
B. Oxygen
C. Nitrogen
D. Chlorine
Answer with only A, B, C, or D.
```

English parsed: `B`; correct: `True`

## 7. benqa_10th-Chemistry_0374 (benqa, mcq)

Model: `Qwen/Qwen3-4B-Instruct-2507`

Gold: `B`

**Bangla Prompt**

```text
ইথিলিন গ্লাইকল কোন ধরনের যৌগ?
A. অ্যালডিহাইড
B. অ্যালকোহল
C. অ্যালকিন
D. অ্যালকাইন
Answer with only A, B, C, or D.
```

Bangla parsed: `B`; correct: `True`

**Banglish Prompt**

```text
ithilin glaikol kon dhoroner joug?
A. ojalodihaid
B. ojalokohol
C. ojalokin
D. ojalokain
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
What is the type of the compound Ethylene Glycol?
A. Aldehydes
B. Alcohols
C. Alkenes
D. Alkynes
Answer with only A, B, C, or D.
```

English parsed: `B`; correct: `True`

## 8. benqa_10th-Math_0044 (benqa, mcq)

Model: `Qwen/Qwen3-4B-Instruct-2507`

Gold: `C`

**Bangla Prompt**

```text
একটি বর্গের কতটি প্রতিসাম্য রেখা আছে?
A. 8টি
B. 6টি
C. 4টি
D. 2টি
Answer with only A, B, C, or D.
```

Bangla parsed: `C`; correct: `True`

**Banglish Prompt**

```text
ekoti borger kototi protisamy rekha achhe?
A. 8ti
B. 6ti
C. 4ti
D. 2ti
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
How many lines of symmetry does a square have?
A. 8
B. 6
C. 4
D. 2
Answer with only A, B, C, or D.
```

English parsed: `C`; correct: `True`
