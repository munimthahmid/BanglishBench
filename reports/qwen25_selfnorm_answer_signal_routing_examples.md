# Routed Self-Normalization Examples

- Model: `Qwen/Qwen2.5-3B-Instruct`
- Heuristic: `selfnorm_if_after_nonempty`
- Split: `test`

## Gains

### 1. banglamath_0229

- Dataset: `banglamath`
- Answer type: `short_answer`
- Gold: `1.5`
- Used selfnorm: `True`
- Baseline correct: `False`
- Selfnorm correct: `True`
- Routed correct: `True`

Banglish item:

```text
150% ke doshomik bhognangshe prokash korole ki hoy
Return only the final answer.
```

Baseline parsed:

```text
50%
```

Self-normalized parsed:

```text
1.5
```

### 2. banglamath_0233

- Dataset: `banglamath`
- Answer type: `short_answer`
- Gold: `৭ দিন`
- Used selfnorm: `True`
- Baseline correct: `False`
- Selfnorm correct: `True`
- Routed correct: `True`

Banglish item:

```text
6 jon lok ekoti kaj 28 dine korole 24 jon lok kot dine korobe
Return only the final answer.
```

Baseline parsed:

```text
6 jon lok ekoti kaj 28 dine korole 24 jon lok kot dine korobe = 10 jon lok
```

Self-normalized parsed:

```text
that 24 people can complete the same job in 7 days.
```

### 3. banglamath_0236

- Dataset: `banglamath`
- Answer type: `short_answer`
- Gold: `১২ টাকা`
- Used selfnorm: `True`
- Baseline correct: `False`
- Selfnorm correct: `True`
- Routed correct: `True`

Banglish item:

```text
10ti bolopener dam 60 taka hole 2ti bolopener dam kot
Return only the final answer.
```

Baseline parsed:

```text
80 taka
```

Self-normalized parsed:

```text
Therefore, the cost for 2 tokens is 12 taka.
```

### 4. banglamath_0526

- Dataset: `banglamath`
- Answer type: `short_answer`
- Gold: `৩০ বর্গ মিটার`
- Used selfnorm: `True`
- Baseline correct: `False`
- Selfnorm correct: `True`
- Routed correct: `True`

Banglish item:

```text
ekoti tribhujer bhumi 10 mitar o uchchota 6 mitar hole kshetrofol kot
Return only the final answer.
```

Baseline parsed:

```text
60
```

Self-normalized parsed:

```text
৩০ বর্গমিটার
```

### 5. benqa_10th-Biology_0128

- Dataset: `benqa`
- Answer type: `choice`
- Gold: `A`
- Used selfnorm: `True`
- Baseline correct: `False`
- Selfnorm correct: `True`
- Routed correct: `True`

Banglish item:

```text
ister shboson prokriyay konoti utoponn hoy?
A. lyakotik esid
B. glukoj
C. oksalo asitik esid
D. glisarik esid
Answer with only A, B, C, or D.
```

Baseline parsed:

```text
C
```

Self-normalized parsed:

```text
A
```

### 6. benqa_10th-Chemistry_0194

- Dataset: `benqa`
- Answer type: `choice`
- Gold: `D`
- Used selfnorm: `True`
- Baseline correct: `False`
- Selfnorm correct: `True`
- Routed correct: `True`

Banglish item:

```text
nicher kon mouloti odhik sokriy?
A. O
B. P
C. N
D. F
Answer with only A, B, C, or D.
```

Baseline parsed:

```text
C
```

Self-normalized parsed:

```text
D
```

## Losses

### 1. benqa_10th-Chemistry_0336

- Dataset: `benqa`
- Answer type: `choice`
- Gold: `D`
- Used selfnorm: `True`
- Baseline correct: `True`
- Selfnorm correct: `False`
- Routed correct: `False`

Banglish item:

```text
A \rightarrow CaCO_{3}(s) \xrightarrow{\Delta} CaO(s) + X(g) B \rightarrow 250 mL 0.2 molar NaCl drobon A-er 'X' gyasoti- i. CO_{2} ii. omlodhormi iii. bayu opeksha bhari nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Baseline parsed:

```text
D
```

Self-normalized parsed:

```text
A
```

### 2. benqa_10th-Physics_0130

- Dataset: `benqa`
- Answer type: `choice`
- Gold: `D`
- Used selfnorm: `True`
- Baseline correct: `True`
- Selfnorm correct: `False`
- Routed correct: `False`

Banglish item:

```text
manobodeher ghonotb kot? i. kontrol rod thake ii. bipul poriman tap shokti nirgot hoy iii. jbalani hisebe iureniyam byobohrit hoy nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Baseline parsed:

```text
D
```

Self-normalized parsed:

```text
C
```

### 3. benqa_10th-Physics_0150

- Dataset: `benqa`
- Answer type: `choice`
- Gold: `B`
- Used selfnorm: `True`
- Baseline correct: `True`
- Selfnorm correct: `False`
- Routed correct: `False`

Banglish item:

```text
konoti skelar rashi?
A. beg
B. druti
C. soron
D. tworon
Answer with only A, B, C, or D.
```

Baseline parsed:

```text
B
```

Self-normalized parsed:

```text
D
```

### 4. benqa_12th-Biology-II_0128

- Dataset: `benqa`
- Answer type: `choice`
- Gold: `B`
- Used selfnorm: `True`
- Baseline correct: `True`
- Selfnorm correct: `False`
- Routed correct: `False`

Banglish item:

```text
shbasokendr mostishker je ongshe thake- i. ponos ii. serebelam iii. medula obolonggata nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

Baseline parsed:

```text
B
```

Self-normalized parsed:

```text
A
```

### 5. benqa_12th-Biology-II_0203

- Dataset: `benqa`
- Answer type: `choice`
- Gold: `D`
- Used selfnorm: `True`
- Baseline correct: `True`
- Selfnorm correct: `False`
- Routed correct: `False`

Banglish item:

```text
pittoroser kaj hochchhe- i. chorbijatiy khaddoke imalosifai kora ii. bhitamin A,D,E,o K shoshone sohayota kore iii. kopar, jingk, parod o toksin podarth nishkashit kora nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

Baseline parsed:

```text
D
```

Self-normalized parsed:

```text
A
```

### 6. benqa_12th-Chemistry-II_0294

- Dataset: `benqa`
- Answer type: `choice`
- Gold: `C`
- Used selfnorm: `True`
- Baseline correct: `True`
- Selfnorm correct: `False`
- Routed correct: `False`

Banglish item:

```text
benojiner karbon-karbon dwi-bondhon kon orobitaroler odhikromone srishti hoy? i. sp^{2} - sp^{2} ii. p - p iii. sp^{2} - sp^{3} nicher konoti sothik?
A. i
B. iii
C. i o ii
D. ii o iii
Answer with only A, B, C, or D.
```

Baseline parsed:

```text
C
```

Self-normalized parsed:

```text
D
```

