# Routed Self-Normalization Examples

- Model: `Qwen/Qwen3-4B-Instruct-2507`
- Heuristic: `selfnorm_if_after_nonempty`
- Split: `test`

## Gains

### 1. banglamath_0236

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
Unable to evaluate due to unclear or malformed input.
```

Self-normalized parsed:

```text
উত্তর: 12 টাকা
```

### 2. banglamath_1697

- Dataset: `banglamath`
- Answer type: `short_answer`
- Gold: `70`
- Used selfnorm: `True`
- Baseline correct: `False`
- Selfnorm correct: `True`
- Routed correct: `True`

Banglish item:

```text
30 ke 1/2 diye bhag kore 10 jog korole kot hoy?
Return only the final answer.
```

Baseline parsed:

```text
600
```

Self-normalized parsed:

```text
70
```

### 3. benqa_10th-Physics_0198

- Dataset: `benqa`
- Answer type: `choice`
- Gold: `D`
- Used selfnorm: `True`
- Baseline correct: `False`
- Selfnorm correct: `True`
- Routed correct: `True`

Banglish item:

```text
nicher kon rashigulo bhektor rashi?
A. druti, kaj o beg
B. torit bibhob, soron o tworon
C. druti, soron o beg
D. bhorobeg, soron o ojon
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

### 4. benqa_12th-Biology-II_0049

- Dataset: `benqa`
- Answer type: `choice`
- Gold: `C`
- Used selfnorm: `True`
- Baseline correct: `False`
- Selfnorm correct: `True`
- Routed correct: `True`

Banglish item:

```text
otitis midiya' kon ongger rog?
A. chokh
B. nak
C. kan
D. gola
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

### 5. benqa_12th-Chemistry-II_0194

- Dataset: `benqa`
- Answer type: `choice`
- Gold: `A`
- Used selfnorm: `True`
- Baseline correct: `False`
- Selfnorm correct: `True`
- Routed correct: `True`

Banglish item:

```text
semikondaktor hisebe byobohrit hoy-
A. Ge
B. Zn
C. Cu
D. Al
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

### 6. benqa_12th-Chemistry-I_0286

- Dataset: `benqa`
- Answer type: `choice`
- Gold: `C`
- Used selfnorm: `True`
- Baseline correct: `False`
- Selfnorm correct: `True`
- Routed correct: `True`

Banglish item:

```text
urbor matir jony otyanukul pH kot?
A. 3.0-4
B. 6-May
C. 8-Jul
D. 11-Oct
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

### 2. benqa_12th-Chemistry-I_0260

- Dataset: `benqa`
- Answer type: `choice`
- Gold: `D`
- Used selfnorm: `True`
- Baseline correct: `True`
- Selfnorm correct: `False`
- Routed correct: `False`

Banglish item:

```text
bhinegare kot shotangsh pani bidyoman?
A. 6%
B. 15%
C. 70%
D. 90%
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

