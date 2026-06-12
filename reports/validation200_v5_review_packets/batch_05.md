# Validation-200 v5 Review Packet 05

Source queue: `data/slices/validation_200_v5_review_queue.csv`
Batch: 5/6
Rows in batch: 25

Fill the source CSV, not this Markdown packet. Use this packet only for
source/context reading while editing `reviewed_banglish`,
`quality_label`, and `review_notes` in the queue.

Allowed labels: `ok`, `minor_edit`, `major_edit`, `bad`.

## 101. benqa_12th-Math-I_0218

- CSV row: 102
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `qwen3_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `True`
- Qwen3 v4 correct: `False`
- Suggestion notes: konoti->konti (1); kshetre->khetre (1)

Bangla:

```text
যেকোনো ত্রিভুজ ABC এর ক্ষেত্রে নিচের কোনটি সঠিক?
A. c = acosB + bcosA
B. b = csinA + asinC
C. \Delta = \frac{1}{2} abcosC
D. cosA = \frac{b^{2} + c^{2} + a^{2}}{2bc}
Answer with only A, B, C, or D.
```

English:

```text
In any triangle ABC which of the following is correct?
A. c = acosB + bcosA
B. b = csinA + asinC
C. \Delta = \frac{1}{2} abcosC
D. cosA = \frac{b^{2} + c^{2} + a^{2}}{2bc}
Answer with only A, B, C, or D.
```

Current Banglish:

```text
jekono tribhuj ABC er kshetre nicher konoti sothik?
A. c = acosB + bcosA
B. b = csinA + asinC
C. \Delta = \frac{1}{2} abcosC
D. cosA = \frac{b^{2} + c^{2} + a^{2}}{2bc}
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
jekono tribhuj ABC er khetre nicher konti sothik?
A. c = acosB + bcosA
B. b = csinA + asinC
C. \Delta = \frac{1}{2} abcosC
D. cosA = \frac{b^{2} + c^{2} + a^{2}}{2bc}
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 102. benqa_10th-Physics_0130

- CSV row: 103
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 2
- Artifact patterns: `tb_virama_b`
- Status: `pending`
- Qwen2.5 v4 correct: `True`
- Qwen3 v4 correct: `True`
- Suggestion notes: konoti->konti (1); kot->koto (1)

Bangla:

```text
মানবদেহের ঘনত্ব কত? i. কন্ট্রোল রড থাকে ii. বিপুল পরিমাণ তাপ শক্তি নির্গত হয় iii. জ্বালানি হিসেবে ইউরেনিয়াম ব্যবহৃত হয় নিচের কোনটি সঠিক?
A. i ও ii
B. i ও iii
C. ii ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

English:

```text
In nuclear rector - i. there is control rod ii. huge amunt of heat energy is radiated iii.uranium is used as fuel Which one is correct?
A. i and ii
B. i and iii
C. ii and iii
D. i, ii and iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
manobodeher ghonotb kot? i. kontrol rod thake ii. bipul poriman tap shokti nirgot hoy iii. jbalani hisebe iureniyam byobohrit hoy nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
manobodeher ghonotb koto? i. kontrol rod thake ii. bipul poriman tap shokti nirgot hoy iii. jbalani hisebe iureniyam byobohrit hoy nicher konti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 103. benqa_12th-Physics-II_0085

- CSV row: 104
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 2
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `True`
- Qwen3 v4 correct: `True`
- Suggestion notes: konoti->konti (1); kshetre->khetre (1)

Bangla:

```text
ফোটনের ক্ষেত্রে- i. স্থির ভর শূন্য ii. শক্তি h\upsilon iii. বেগ 3 \times 10^{8} ms^{-1} নিচের কোনটি সঠিক?
A. i ও ii
B. i ও iii
C. ii ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

English:

```text
For photon's- i. rest mass zero ii. energy h\upsilon iii. velocity 3 \times 10^{8} ms^{-1} Which one is correct?
A. i and ii
B. i and iii
C. ii and iii
D. i, ii and iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
fotoner kshetre- i. sthir bhor shuny ii. shokti h\upsilon iii. beg 3 \times 10^{8} ms^{-1} nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
fotoner khetre- i. sthir bhor shuny ii. shokti h\upsilon iii. beg 3 \times 10^{8} ms^{-1} nicher konti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 104. banglamath_1699

- CSV row: 105
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `True`
- Suggestion notes: kot->koto (1)

Bangla:

```text
A - B = 10, AB = 16 হলে A² + B² = কত?
Return only the final answer.
```

English:

```text
If A - B = 10 and AB = 16, what is A² + B²?
Return only the final answer.
```

Current Banglish:

```text
A - B = 10, AB = 16 hole A² + B² = kot?
Return only the final answer.
```

Auto-suggested Banglish:

```text
A - B = 10, AB = 16 hole A² + B² = koto?
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 105. benqa_10th-Biology_0197

- CSV row: 106
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `True`
- Suggestion notes: konoti->konti (1)

Bangla:

```text
কোষের সকল জৈবিক ক্রিয়া নিয়ন্ত্রণ করে কোনটি?
A. নিউক্লয়াস
B. রাইবোজোম
C. লাইসোজোম
D. মাইটোকন্ড্রিয়া
Answer with only A, B, C, or D.
```

English:

```text
Which controls all the biological activities of a cell?
A. Nucleus
B. Ribosome
C. Luysosome
D. Mitochondria
Answer with only A, B, C, or D.
```

Current Banglish:

```text
kosher sokol joibik kriya niyontron kore konoti?
A. niukloyas
B. raibojom
C. laisojom
D. maitokondriya
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
kosher sokol joibik kriya niyontron kore konti?
A. niukloyas
B. raibojom
C. laisojom
D. maitokondriya
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 106. benqa_10th-Chemistry_0041

- CSV row: 107
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `True`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1)

Bangla:

```text
নিচের কোন তথ্যটি সঠিক?
A. C_{2}H_{4} অপেক্ষা C_{2}H{6} অধিক সক্রিয়
B. CH_{4} ক্ষারকের সাথে বিক্রিয়া করে
C. ইথানল একটি হাইড্রোকার্বন
D. পলিপ্রোপিনকে রি-সাইকেল করা যায়
Answer with only A, B, C, or D.
```

English:

```text
Which one of the following information is correct?
A. C_{3}H_{6} is more active than C_{2}H_{4}
B. CH_{4} reacts with base
C. Ethanol is a hydrocarbon
D. it is possible to recycle polypropene
Answer with only A, B, C, or D.
```

Current Banglish:

```text
nicher kon tothyoti sothik?
A. C_{2}H_{4} opeksha C_{2}H{6} odhik sokriy
B. CH_{4} ksharoker sathe bikriya kore
C. ithanol ekoti haidrokarbon
D. polipropinoke ri-saikel kora jay
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
nicher kon tothyoti sothik?
A. C_{2}H_{4} opeksha C_{2}H{6} odhik sokriy
B. CH_{4} ksharoker sathe bikriya kore
C. ithanol ekti haidrokarbon
D. polipropinoke ri-saikel kora jay
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 107. benqa_10th-Chemistry_0336

- CSV row: 108
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `True`
- Qwen3 v4 correct: `True`
- Suggestion notes: konoti->konti (1)

Bangla:

```text
A \rightarrow CaCO_{3}(s) \xrightarrow{\Delta} CaO(s) + X(g) B \rightarrow 250 mL 0.2 মোলার NaCl দ্রবণ A-এর 'X' গ্যাসটি- i. CO_{2} ii. অম্লধর্মী iii. বায়ু অপেক্ষা ভারী নিচের কোনটি সঠিক?
A. i ও ii
B. i ও iii
C. ii ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

English:

```text
A\rightarrow CaCO_{3}\overset{\Delta }{\rightarrow}CaO(s)+X(g) B\rightarrow 250 mL 0.2 olar NaCl solution The 'X' gas of A is- i. CO_{2} ii. acidic iii. heavier than air Which one is correct?
A. i and ii
B. i and iii
C. ii and iii
D. i, ii and iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
A \rightarrow CaCO_{3}(s) \xrightarrow{\Delta} CaO(s) + X(g) B \rightarrow 250 mL 0.2 molar NaCl drobon A-er 'X' gyasoti- i. CO_{2} ii. omlodhormi iii. bayu opeksha bhari nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
A \rightarrow CaCO_{3}(s) \xrightarrow{\Delta} CaO(s) + X(g) B \rightarrow 250 mL 0.2 molar NaCl drobon A-er 'X' gyasoti- i. CO_{2} ii. omlodhormi iii. bayu opeksha bhari nicher konti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 108. benqa_10th-Chemistry_0388

- CSV row: 109
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `True`
- Suggestion notes: konoti->konti (1)

Bangla:

```text
স্ক্যান্ডিয়ামের সর্বশেষ শক্তিস্তরের সঠিক ইলেকট্রন বিন্যাস কোনটি?
A. 3s^{2}3p^{6}3d^{5}4s^{1}
B. 3s^{2}3p^{6}3d^{3}4s^{2}
C. 3s^{2}3p^{6}3d^{2}4s^{2}
D. 3s^{2}3p^{6}3d^{1}4s^{2}
Answer with only A, B, C, or D.
```

English:

```text
What is the correct electronic configuration of the outermost shell of Scandium?
A. 3s^{2}3p^{6}3d^{5}4s^{1}
B. 3s^{2}3p^{6}3d^{3}4s^{2}
C. 3s^{2}3p^{6}3d^{2}4s^{2}
D. 3s^{2}3p^{6}3d^{1}4s^{2}
Answer with only A, B, C, or D.
```

Current Banglish:

```text
skyandiyamer sorboshesh shoktistorer sothik ilekotron binyas konoti?
A. 3s^{2}3p^{6}3d^{5}4s^{1}
B. 3s^{2}3p^{6}3d^{3}4s^{2}
C. 3s^{2}3p^{6}3d^{2}4s^{2}
D. 3s^{2}3p^{6}3d^{1}4s^{2}
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
skyandiyamer sorboshesh shoktistorer sothik ilekotron binyas konti?
A. 3s^{2}3p^{6}3d^{5}4s^{1}
B. 3s^{2}3p^{6}3d^{3}4s^{2}
C. 3s^{2}3p^{6}3d^{2}4s^{2}
D. 3s^{2}3p^{6}3d^{1}4s^{2}
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 109. benqa_10th-Math-II_0062

- CSV row: 110
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `True`
- Qwen3 v4 correct: `False`
- Suggestion notes: konoti->konti (1)

Bangla:

```text
M(3, 3), N(6, 6) এবং R(12, 3t) তিনটি বিন্দু। M ও N বিন্দু দ্বারা সংযোগকারী রেখার সমীকরণ নিচের কোনটি?
A. x - 3y - 12 = 0
B. 3x - y - 6 = 0
C. 3x - y - 12 = 0
D. x - 3y + 12 = 0
Answer with only A, B, C, or D.
```

English:

```text
M(3, 3), N(6, 6) and R(12, 3t) are three points. Which is the equation of the straight line connecting the points M and N?
A. x - 3y - 12 = 0
B. 3x - y - 6 = 0
C. 3x - y - 12 = 0
D. x - 3y + 12 = 0
Answer with only A, B, C, or D.
```

Current Banglish:

```text
M(3, 3), N(6, 6) ebong R(12, 3t) tinoti bindu. M o N bindu dwara songjogokari rekhar somikoron nicher konoti?
A. x - 3y - 12 = 0
B. 3x - y - 6 = 0
C. 3x - y - 12 = 0
D. x - 3y + 12 = 0
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
M(3, 3), N(6, 6) ebong R(12, 3t) tinoti bindu. M o N bindu dwara songjogokari rekhar somikoron nicher konti?
A. x - 3y - 12 = 0
B. 3x - y - 6 = 0
C. 3x - y - 12 = 0
D. x - 3y + 12 = 0
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 110. benqa_10th-Math-II_0102

- CSV row: 111
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `True`
- Suggestion notes: kot->koto (1)

Bangla:

```text
M(1, - 1), N(2, 2) এবং R(4, a) বিন্দু তিনটি সমরেখ হলে, a এর মান কত?
A. 2
B. 4
C. 6
D. 8
Answer with only A, B, C, or D.
```

English:

```text
If the three points M(1, - 1), N(2, 2) and R(4, a) are collinear, what is the value of a ?
A. 2
B. 4
C. 6
D. 8
Answer with only A, B, C, or D.
```

Current Banglish:

```text
M(1, - 1), N(2, 2) ebong R(4, a) bindu tinoti somorekh hole, a er man kot?
A. 2
B. 4
C. 6
D. 8
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
M(1, - 1), N(2, 2) ebong R(4, a) bindu tinoti somorekh hole, a er man koto?
A. 2
B. 4
C. 6
D. 8
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 111. benqa_10th-Math-II_0326

- CSV row: 112
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `True`
- Qwen3 v4 correct: `False`
- Suggestion notes: kot->koto (1)

Bangla:

```text
sin B = \sqrt{2} - cosB হলে, B = কত?
A. \frac{\pi}{2}
B. \frac{\pi}{3}
C. \frac{\pi}{4}
D. \frac{\pi}{6}
Answer with only A, B, C, or D.
```

English:

```text
If sin B = \sqrt{2} - cosB, then B = ?
A. \frac{\pi}{2}
B. \frac{\pi}{3}
C. \frac{\pi}{4}
D. \frac{\pi}{6}
Answer with only A, B, C, or D.
```

Current Banglish:

```text
sin B = \sqrt{2} - cosB hole, B = kot?
A. \frac{\pi}{2}
B. \frac{\pi}{3}
C. \frac{\pi}{4}
D. \frac{\pi}{6}
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
sin B = \sqrt{2} - cosB hole, B = koto?
A. \frac{\pi}{2}
B. \frac{\pi}{3}
C. \frac{\pi}{4}
D. \frac{\pi}{6}
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 112. benqa_10th-Math-II_0347

- CSV row: 113
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `True`
- Suggestion notes: kot->koto (1)

Bangla:

```text
cos\left ( - \frac{35\pi}{6} \right ) এর মান কত?
A. - \frac{\sqrt{3}}{2}
B. - \frac{1}{2}
C. \frac{1}{2}
D. \frac{\sqrt{3}}{2}
Answer with only A, B, C, or D.
```

English:

```text
What is the value of cos\left ( - \frac{35\pi}{6} \right )?
A. - \frac{\sqrt{3}}{2}
B. - \frac{1}{2}
C. \frac{1}{2}
D. \frac{\sqrt{3}}{2}
Answer with only A, B, C, or D.
```

Current Banglish:

```text
cos\left ( - \frac{35\pi}{6} \right ) er man kot?
A. - \frac{\sqrt{3}}{2}
B. - \frac{1}{2}
C. \frac{1}{2}
D. \frac{\sqrt{3}}{2}
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
cos\left ( - \frac{35\pi}{6} \right ) er man koto?
A. - \frac{\sqrt{3}}{2}
B. - \frac{1}{2}
C. \frac{1}{2}
D. \frac{\sqrt{3}}{2}
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 113. benqa_10th-Math-II_0357

- CSV row: 114
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `True`
- Suggestion notes: konoti->konti (1)

Bangla:

```text
\left ( 2 - \frac{x}{2} \right ){6} এর বিস্তৃতিতে (1.8875)^{6} নির্ণয়ের জন্য x এর মান নিচের কোনটি?
A. -0.225
B. -0.1125
C. 0.01125
D. 0.225
Answer with only A, B, C, or D.
```

English:

```text
What is the value of x for determining (1.8875)^{6} from the expansion of \left ( 2 - \frac{x}{2} \right ){6}?
A. -0.225
B. -0.1125
C. 0.01125
D. 0.225
Answer with only A, B, C, or D.
```

Current Banglish:

```text
\left ( 2 - \frac{x}{2} \right ){6} er bistritite (1.8875)^{6} nirnoyer jony x er man nicher konoti?
A. -0.225
B. -0.1125
C. 0.01125
D. 0.225
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
\left ( 2 - \frac{x}{2} \right ){6} er bistritite (1.8875)^{6} nirnoyer jony x er man nicher konti?
A. -0.225
B. -0.1125
C. 0.01125
D. 0.225
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 114. benqa_10th-Physics_0036

- CSV row: 115
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `True`
- Qwen3 v4 correct: `True`
- Suggestion notes: kot->koto (1)

Bangla:

```text
70 কেজি ওজনের একজন ব্যক্তি 5 মিনিটে 100 m উচু পাহাড়ে উঠে, তার ক্ষমতা কত ওয়াট? [g = 9.8 ms^{-2}]
A. 3500
B. 1400
C. 228.67
D. 0.14
Answer with only A, B, C, or D.
```

English:

```text
How much power in Watt when a man of mass 70 kg clinb in the hill of height 100 m for using 5 minutes? [g = 9.8 ms^{-2}]
A. 3500
B. 1400
C. 228.67
D. 0.14
Answer with only A, B, C, or D.
```

Current Banglish:

```text
70 keji ojoner ekojon byokti 5 minite 100 m uchu pahare uthe, tar kshomota kot oyat? [g = 9.8 ms^{-2}]
A. 3500
B. 1400
C. 228.67
D. 0.14
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
70 keji ojoner ekojon byokti 5 minite 100 m uchu pahare uthe, tar kshomota koto oyat? [g = 9.8 ms^{-2}]
A. 3500
B. 1400
C. 228.67
D. 0.14
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 115. benqa_10th-Physics_0045

- CSV row: 116
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `True`
- Suggestion notes: kot->koto (1)

Bangla:

```text
কোন নির্দিষ্ট ভরের কোনো বস্তুর বেগ দ্বিগুন করলে গতিশক্তি কত গুন হবে?
A. চারগুন
B. দ্বিগুন
C. অর্ধেক
D. সমান
Answer with only A, B, C, or D.
```

English:

```text
How many times the kinetic energy of a definite mass when it's velocity replaced by twice time?
A. Four time
B. Twice time
C. Half
D. Equal
Answer with only A, B, C, or D.
```

Current Banglish:

```text
kon nirdisht bhorer kono bostur beg dwigun korole gotishokti kot gun hobe?
A. charogun
B. dwigun
C. ordhek
D. soman
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
kon nirdisht bhorer kono bostur beg dwigun korole gotishokti koto gun hobe?
A. charogun
B. dwigun
C. ordhek
D. soman
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 116. benqa_10th-Physics_0055

- CSV row: 117
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `True`
- Qwen3 v4 correct: `True`
- Suggestion notes: korote->korte (1)

Bangla:

```text
পানিতে সাঁতার কাটার সময় কোন বাধা অতিক্রম করতে হয়?
A. স্থিতি ঘর্ষণ
B. গতি ঘর্ষণ
C. আবর্ত ঘর্ষণ
D. প্রবাহী ঘর্ষণ
Answer with only A, B, C, or D.
```

English:

```text
Which friction one faces while swimming ?
A. Static friction
B. sliding griction
C. Rolling friction
D. Fluid friction
Answer with only A, B, C, or D.
```

Current Banglish:

```text
panite santar katar somoy kon badha otikrom korote hoy?
A. sthiti ghorshon
B. goti ghorshon
C. abort ghorshon
D. probahi ghorshon
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
panite santar katar somoy kon badha otikrom korte hoy?
A. sthiti ghorshon
B. goti ghorshon
C. abort ghorshon
D. probahi ghorshon
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 117. benqa_10th-Physics_0150

- CSV row: 118
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `True`
- Qwen3 v4 correct: `False`
- Suggestion notes: konoti->konti (1)

Bangla:

```text
কোনটি স্কেলার রাশি?
A. বেগ
B. দ্রুতি
C. সরণ
D. ত্বরণ
Answer with only A, B, C, or D.
```

English:

```text
Which one is the scalar quantity?
A. Velocity
B. Speed
C. Displacement
D. Acceleration
Answer with only A, B, C, or D.
```

Current Banglish:

```text
konoti skelar rashi?
A. beg
B. druti
C. soron
D. tworon
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
konti skelar rashi?
A. beg
B. druti
C. soron
D. tworon
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 118. benqa_10th-Physics_0280

- CSV row: 119
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `tb_virama_b`
- Status: `pending`
- Qwen2.5 v4 correct: `True`
- Qwen3 v4 correct: `True`
- Suggestion notes: konoti->konti (1)

Bangla:

```text
তামার রোধকত্ব কোনটি?
A. 1.6 \times 10^{-8}\Omega m
B. 1.68 \times 10^{-8}\Omega m
C. 2.44 \times 10^{-8}\Omega m
D. 5.5 \times 10^{-8}\Omega m
Answer with only A, B, C, or D.
```

English:

```text
Which one is the resistivity of copper?
A. 1.6 \times 10^{-8}\Omega m
B. 1.68 \times 10^{-8}\Omega m
C. 2.44 \times 10^{-8}\Omega m
D. 5.5 \times 10^{-8}\Omega m
Answer with only A, B, C, or D.
```

Current Banglish:

```text
tamar rodhokotb konoti?
A. 1.6 \times 10^{-8}\Omega m
B. 1.68 \times 10^{-8}\Omega m
C. 2.44 \times 10^{-8}\Omega m
D. 5.5 \times 10^{-8}\Omega m
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
tamar rodhokotb konti?
A. 1.6 \times 10^{-8}\Omega m
B. 1.68 \times 10^{-8}\Omega m
C. 2.44 \times 10^{-8}\Omega m
D. 5.5 \times 10^{-8}\Omega m
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 119. benqa_12th-Biology-II_0128

- CSV row: 120
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `True`
- Qwen3 v4 correct: `False`
- Suggestion notes: konoti->konti (1)

Bangla:

```text
শ্বাসকেন্দ্র মস্তিষ্কের যে অংশে থাকে- i. পনস ii. সেরেবেলাম iii. মেডুলা অবলংগাটা নিচের কোনটি সঠিক?
A. i ও ii
B. i ও iii
C. ii ও iii
D. i, ii, ও iii
Answer with only A, B, C, or D.
```

English:

```text
The respiratory centre of the brain located on- i. pons ii.cerebellum iii.medulla oblongata Which one is correct?
A. i & ii
B. i & iii
C. ii & iii
D. i, ii & iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
shbasokendr mostishker je ongshe thake- i. ponos ii. serebelam iii. medula obolonggata nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
shbasokendr mostishker je ongshe thake- i. ponos ii. serebelam iii. medula obolonggata nicher konti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 120. benqa_12th-Biology-II_0203

- CSV row: 121
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `True`
- Qwen3 v4 correct: `True`
- Suggestion notes: konoti->konti (1)

Bangla:

```text
পিত্তরসের কাজ হচ্ছে- i. চর্বিজাতীয় খাদ্যকে ইমালসিফাই করা ii. ভিটামিন A,D,E,ও K শোষণে সহায়তা করে iii. কপার, জিংক, পারদ ও টক্সিন পদার্থ নিষ্কাশিত করা নিচের কোনটি সঠিক?
A. i ও ii
B. i ও iii
C. ii ও iii
D. i, ii, ও iii
Answer with only A, B, C, or D.
```

English:

```text
Function of bile- i.emulsifies of fatty foods ii. To help in the absorption of vitamin A,D E and K iii.to expel out copper,zinc,mercury and toxin substance Which one is correct?
A. i & ii
B. i & iii
C. ii & iii
D. i, ii & iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
pittoroser kaj hochchhe- i. chorbijatiy khaddoke imalosifai kora ii. bhitamin A,D,E,o K shoshone sohayota kore iii. kopar, jingk, parod o toksin podarth nishkashit kora nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
pittoroser kaj hochchhe- i. chorbijatiy khaddoke imalosifai kora ii. bhitamin A,D,E,o K shoshone sohayota kore iii. kopar, jingk, parod o toksin podarth nishkashit kora nicher konti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 121. benqa_12th-Biology-II_0247

- CSV row: 122
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `True`
- Qwen3 v4 correct: `False`
- Suggestion notes: kot->koto (1)

Bangla:

```text
P \rightarrow DdEe \times ddEE উদ্দীপকে উল্লিখিত ক্রস দ্বারা মূক ও বধির সন্তান হবার সম্ভাবনা কত?
A. 25%
B. 50%
C. 75%
D. 100%
Answer with only A, B, C, or D.
```

English:

```text
P\rightarrow DdEe\times ddEE Which is the possiblity of producing deaf and dump offspring by above mentioned cross?
A. 25%
B. 50%
C. 75%
D. 100%
Answer with only A, B, C, or D.
```

Current Banglish:

```text
P \rightarrow DdEe \times ddEE uddipoke ullikhit kros dwara muk o bodhir sontan hobar sombhabona kot?
A. 25%
B. 50%
C. 75%
D. 100%
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
P \rightarrow DdEe \times ddEE uddipoke ullikhit kros dwara muk o bodhir sontan hobar sombhabona koto?
A. 25%
B. 50%
C. 75%
D. 100%
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 122. benqa_12th-Biology-I_0042

- CSV row: 123
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `True`
- Qwen3 v4 correct: `True`
- Suggestion notes: konoti->konti (1)

Bangla:

```text
সাইকাসের প্রধান মূল নষ্ট হওয়ার ফলে- i. অস্থানিক মূল সৃষ্টি হয় ii. Anabaena দ্বারা আক্রান্ত হয় iii. এর আকৃতি সামুদ্রিক প্রবালের মত হয় নিচের কোনটি সঠিক?
A. i ও ii
B. i ও iii
C. ii ও iii
D. i, ii, ও iii
Answer with only A, B, C, or D.
```

English:

```text
In case of damage of the ta root of cycas- i. produces adventitious roof ii. attached by anabaena iii. its shape is as like as sea coral Which one is correct?
A. i and ii
B. i and iii
C. ii and iii
D. i, ii and iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
saikaser prodhan mul nosht hooyar fole- i. osthanik mul srishti hoy ii. Anabaena dwara akrant hoy iii. er akriti samudrik probaler mot hoy nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
saikaser prodhan mul nosht hooyar fole- i. osthanik mul srishti hoy ii. Anabaena dwara akrant hoy iii. er akriti samudrik probaler mot hoy nicher konti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 123. benqa_12th-Chemistry-II_0013

- CSV row: 124
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `True`
- Qwen3 v4 correct: `False`
- Suggestion notes: konoti->konti (1)

Bangla:

```text
ঘুমের ঔষধ হিসেবে ব্যবহৃত হয় কোনটি?
A. ফরমালডিহাইড
B. অ্যাসিটালডিহাইড
C. প্যারালডিহাইড
D. মেটালডিহাইড
Answer with only A, B, C, or D.
```

English:

```text
Which one is used as a medicine of sleep?
A. Formaldehyde
B. Acetaldehyde
C. Paraldehyde
D. Metaldehyde
Answer with only A, B, C, or D.
```

Current Banglish:

```text
ghumer oushodh hisebe byobohrit hoy konoti?
A. foromalodihaid
B. asitalodihaid
C. pyaralodihaid
D. metalodihaid
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
ghumer oushodh hisebe byobohrit hoy konti?
A. foromalodihaid
B. asitalodihaid
C. pyaralodihaid
D. metalodihaid
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 124. benqa_12th-Chemistry-II_0294

- CSV row: 125
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `True`
- Qwen3 v4 correct: `True`
- Suggestion notes: konoti->konti (1)

Bangla:

```text
বেনজিনের কার্বন-কার্বন দ্বি-বন্ধন কোন অরবিটারলের অধিক্রমণে সৃষ্টি হয়? i. sp^{2} - sp^{2} ii. p - p iii. sp^{2} - sp^{3} নিচের কোনটি সঠিক?
A. i
B. iii
C. i ও ii
D. ii ও iii
Answer with only A, B, C, or D.
```

English:

```text
Carbon-carbon double bond of benzene is created by which kind of orbital overlaping? i. SP^{2} - SP^{2} ii. P - P iii. SP^{2} - SP^{3} Which one is correct?
A. i
B. iii
C. i and ii
D. ii and iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
benojiner karbon-karbon dwi-bondhon kon orobitaroler odhikromone srishti hoy? i. sp^{2} - sp^{2} ii. p - p iii. sp^{2} - sp^{3} nicher konoti sothik?
A. i
B. iii
C. i o ii
D. ii o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
benojiner karbon-karbon dwi-bondhon kon orobitaroler odhikromone srishti hoy? i. sp^{2} - sp^{2} ii. p - p iii. sp^{2} - sp^{3} nicher konti sothik?
A. i
B. iii
C. i o ii
D. ii o iii
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 125. benqa_12th-Chemistry-II_0305

- CSV row: 126
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `True`
- Suggestion notes: kot->koto (1)

Bangla:

```text
27^oC তাপমাত্রায় O_2 এর RMS মান কত?
A. 453.23 ms^{-1}
B. 463.34 ms^{-1}
C. 473.45 ms^{-1}
D. 483.56 ms^{-1}
Answer with only A, B, C, or D.
```

English:

```text
What is the RMS value of O_{2} at 27\degree C temperature?
A. 453.23ms^{-1}
B. 463.34ms^{-1}
C. 473.45ms^{-1}
D. 483.56ms^{-1}
Answer with only A, B, C, or D.
```

Current Banglish:

```text
27^oC tapomatray O_2 er RMS man kot?
A. 453.23 ms^{-1}
B. 463.34 ms^{-1}
C. 473.45 ms^{-1}
D. 483.56 ms^{-1}
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
27^oC tapomatray O_2 er RMS man koto?
A. 453.23 ms^{-1}
B. 463.34 ms^{-1}
C. 473.45 ms^{-1}
D. 483.56 ms^{-1}
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank
