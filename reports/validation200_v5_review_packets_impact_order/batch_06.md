# Validation-200 v5 Review Packet 06

Source queue: `data/slices/validation_200_v5_review_queue.csv`
Batch: 6/7
Rows in batch: 20

Fill the source CSV, not this Markdown packet. Use this packet only for
source/context reading while editing `reviewed_banglish`,
`quality_label`, and `review_notes` in the queue.

Allowed labels: `ok`, `minor_edit`, `major_edit`, `bad`.

## 101. benqa_12th-Physics-I_0289

- CSV row: 99
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `qwen25_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `True`
- Suggestion notes: ekoti->ekti (1); kot->koto (1)
- Impact rank: 101
- Impact tier: `tier_3_medium`
- Impact score: 105
- Split: `test`
- Impact reasons: priority=qwen25_wrong_multi_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; 2_suggested_replacements

Bangla:

```text
30^{\circ}C তাপমাত্রায় একটি গ্যাসকে স্থিরচাপে উত্তপ্ত করে আয়তন তিনগুণ করা হলো। গ্যাসটির চূড়ান্ত তাপমাত্রা কত?
A. 90^{\circ}C
B. 300^{\circ}C
C. 436^{\circ}C
D. 636^{\circ}C
Answer with only A, B, C, or D.
```

English:

```text
At 30\degree temperature a gas is heated at constant pressure to three time in volume. What is the final temperature of the gas?
A. 90\degree C
B. 300\degree C
C. 436\degree C
D. 636\degree C
Answer with only A, B, C, or D.
```

Current Banglish:

```text
30^{\circ}C tapomatray ekoti gyasoke sthirochape uttopt kore ayoton tinogun kora holo. gyasotir churant tapomatra kot?
A. 90^{\circ}C
B. 300^{\circ}C
C. 436^{\circ}C
D. 636^{\circ}C
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
30^{\circ}C tapomatray ekti gyasoke sthirochape uttopt kore ayoton tinogun kora holo. gyasotir churant tapomatra koto?
A. 90^{\circ}C
B. 300^{\circ}C
C. 436^{\circ}C
D. 636^{\circ}C
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 102. benqa_10th-Physics_0045

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
- Impact rank: 102
- Impact tier: `tier_4_low`
- Impact score: 84
- Split: `dev`
- Impact reasons: priority=lower_priority; dev50_tuning_slice; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 1_suggested_replacements

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

## 103. benqa_10th-Physics_0150

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
- Impact rank: 103
- Impact tier: `tier_4_low`
- Impact score: 80
- Split: `test`
- Impact reasons: priority=lower_priority; heldout_test150; main_benqa_gap_slice; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 1_suggested_replacements

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

## 104. benqa_12th-Chemistry-II_0013

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
- Impact rank: 104
- Impact tier: `tier_4_low`
- Impact score: 80
- Split: `test`
- Impact reasons: priority=lower_priority; heldout_test150; main_benqa_gap_slice; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 1_suggested_replacements

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

## 105. benqa_12th-Physics-I_0133

- CSV row: 139
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
- Impact rank: 105
- Impact tier: `tier_4_low`
- Impact score: 80
- Split: `test`
- Impact reasons: priority=lower_priority; heldout_test150; main_benqa_gap_slice; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 1_suggested_replacements

Bangla:

```text
\frac{3}{2} মোল গ্যাসের জন্য আদর্শ গ্যাস সমীকরণ হবে কোনটি?
A. 3PV = 2RT
B. 2PV = \frac{1}{3} RT
C. 2PV = 3RT
D. \frac{PV}{RT}=\frac{2}{3}
Answer with only A, B, C, or D.
```

English:

```text
The equation of ideal gas for \frac{3}{2} mol is-
A. 3PV = 2RT
B. 2PV = \frac{1}{3} RT
C. 2PV = 3RT
D. \frac{PV}{RT} = \frac{2}{3}
Answer with only A, B, C, or D.
```

Current Banglish:

```text
\frac{3}{2} mol gyaser jony adorsh gyas somikoron hobe konoti?
A. 3PV = 2RT
B. 2PV = \frac{1}{3} RT
C. 2PV = 3RT
D. \frac{PV}{RT}=\frac{2}{3}
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
\frac{3}{2} mol gyaser jony adorsh gyas somikoron hobe konti?
A. 3PV = 2RT
B. 2PV = \frac{1}{3} RT
C. 2PV = 3RT
D. \frac{PV}{RT}=\frac{2}{3}
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
- Impact rank: 106
- Impact tier: `tier_4_low`
- Impact score: 74
- Split: `test`
- Impact reasons: priority=lower_priority; heldout_test150; main_benqa_gap_slice; qwen3_v4_wrong; qwen3_recoverable_by_other_script; 1_suggested_replacements; ksh_heavy

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

## 107. benqa_12th-Biology-II_0247

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
- Impact rank: 107
- Impact tier: `tier_4_low`
- Impact score: 70
- Split: `test`
- Impact reasons: priority=lower_priority; heldout_test150; main_benqa_gap_slice; qwen3_v4_wrong; qwen3_recoverable_by_other_script; 1_suggested_replacements

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

## 108. benqa_12th-Chemistry-I_0260

- CSV row: 130
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
- Impact rank: 108
- Impact tier: `tier_4_low`
- Impact score: 70
- Split: `test`
- Impact reasons: priority=lower_priority; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; 1_suggested_replacements

Bangla:

```text
ভিনেগারে কত শতাংশ পানি বিদ্যমান?
A. 6%
B. 15%
C. 70%
D. 90%
Answer with only A, B, C, or D.
```

English:

```text
What percentage of water contain in vinegar?
A. 6%
B. 15%
C. 70%
D. 90%
Answer with only A, B, C, or D.
```

Current Banglish:

```text
bhinegare kot shotangsh pani bidyoman?
A. 6%
B. 15%
C. 70%
D. 90%
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
bhinegare koto shotangsh pani bidyoman?
A. 6%
B. 15%
C. 70%
D. 90%
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 109. benqa_8th-Science_0078

- CSV row: 141
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `lower_priority`
- Replacement count: 1
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `True`
- Suggestion notes: kot->koto (1)
- Impact rank: 109
- Impact tier: `tier_4_low`
- Impact score: 62
- Split: `test`
- Impact reasons: priority=lower_priority; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; 1_suggested_replacements; ksh_heavy

Bangla:

```text
আলো কাচ থেকে বায়ু মাধ্যমে যাওয়ার সময় আপতন কোণ ৩২^{\circ} হলে প্রতিসরিত রশ্নিটি মাধ্যমের বিভেদতল বরাবর যায়। এক্ষেত্রে প্রতিসরণ কোণের মান কত?
A. ০^{\circ}
B. ৩২^{\circ}
C. ৯০^{\circ}
D. ১৮০^{\circ}
Answer with only A, B, C, or D.
```

English:

```text
When a ray of light enters to wind medium from glass medium if the angle of incidence is 32 the refraton ray goes through the surface of separation medium. In this case whate is the refraction anlge?
A. 0^{\circ}
B. 32^{\circ}
C. 90^{\circ}
D. 180^{\circ}
Answer with only A, B, C, or D.
```

Current Banglish:

```text
alo kach theke bayu madhyome jaoyar somoy apoton kon 32^{\circ} hole protisorit roshniti madhyomer bibhedotol borabor jay. ekshetre protisoron koner man kot?
A. 0^{\circ}
B. 32^{\circ}
C. 90^{\circ}
D. 180^{\circ}
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
alo kach theke bayu madhyome jaoyar somoy apoton kon 32^{\circ} hole protisorit roshniti madhyomer bibhedotol borabor jay. ekshetre protisoron koner man koto?
A. 0^{\circ}
B. 32^{\circ}
C. 90^{\circ}
D. 180^{\circ}
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 110. benqa_10th-Biology_0197

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
- Impact rank: 110
- Impact tier: `tier_4_low`
- Impact score: 62
- Split: `dev`
- Impact reasons: priority=lower_priority; dev50_tuning_slice; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; 1_suggested_replacements

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

## 111. benqa_12th-Chemistry-I_0140

- CSV row: 128
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
- Impact rank: 111
- Impact tier: `tier_4_low`
- Impact score: 62
- Split: `dev`
- Impact reasons: priority=lower_priority; dev50_tuning_slice; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; 1_suggested_replacements

Bangla:

```text
CaF_{2}-এর সম্পৃক্ত জলীয় দ্রবণে ফ্লোরাইড আয়নের ঘনমাত্রা 0.00655 gL^{-1} হলে CaF_{2} এর দ্রাব্যতা গুণফল কত হবে?
A. 3.7\times 10^{-13}
B. 2.048\times 10^{-10}
C. 3.7\times 10^{-12}
D. 2.048\times 10^{-11}
Answer with only A, B, C, or D.
```

English:

```text
Conecntration of F^{-} ion in saturated sol^{n} of CaF_{2} is 0.00655 gL^{-1}; What is its solubility product?
A. 3.7\times 10^{-13}
B. 2.048\times 10^{-10}
C. 3.7\times 10^{-12}
D. 2.048\times 10^{-11}
Answer with only A, B, C, or D.
```

Current Banglish:

```text
CaF_{2}-er somprikt joliy drobone floraid ayoner ghonomatra 0.00655 gL^{-1} hole CaF_{2} er drabyota gunofol kot hobe?
A. 3.7\times 10^{-13}
B. 2.048\times 10^{-10}
C. 3.7\times 10^{-12}
D. 2.048\times 10^{-11}
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
CaF_{2}-er somprikt joliy drobone floraid ayoner ghonomatra 0.00655 gL^{-1} hole CaF_{2} er drabyota gunofol koto hobe?
A. 3.7\times 10^{-13}
B. 2.048\times 10^{-10}
C. 3.7\times 10^{-12}
D. 2.048\times 10^{-11}
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 112. benqa_12th-Math-I_0202

- CSV row: 133
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
- Impact rank: 112
- Impact tier: `tier_4_low`
- Impact score: 62
- Split: `dev`
- Impact reasons: priority=lower_priority; dev50_tuning_slice; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; 1_suggested_replacements

Bangla:

```text
\int \frac{cosx}{\sqrt{sinx}} dx = কত?
A. 2\sqrt{cosx} + c
B. 2\sqrt{sinx} + c
C. \frac{1}{2} \sqrt{cosx} + c
D. \frac{1}{2} \sqrt{sinx} + c
Answer with only A, B, C, or D.
```

English:

```text
\int \frac{cosx}{\sqrt{sinx}} dx = what?
A. 2\sqrt{cosx} + c
B. 2\sqrt{sinx} + c
C. \frac{1}{2} \sqrt{cosx} + c
D. \frac{1}{2} \sqrt{sinx} + c
Answer with only A, B, C, or D.
```

Current Banglish:

```text
\int \frac{cosx}{\sqrt{sinx}} dx = kot?
A. 2\sqrt{cosx} + c
B. 2\sqrt{sinx} + c
C. \frac{1}{2} \sqrt{cosx} + c
D. \frac{1}{2} \sqrt{sinx} + c
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
\int \frac{cosx}{\sqrt{sinx}} dx = koto?
A. 2\sqrt{cosx} + c
B. 2\sqrt{sinx} + c
C. \frac{1}{2} \sqrt{cosx} + c
D. \frac{1}{2} \sqrt{sinx} + c
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 113. benqa_12th-Physics-I_0106

- CSV row: 138
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
- Impact rank: 113
- Impact tier: `tier_4_low`
- Impact score: 62
- Split: `dev`
- Impact reasons: priority=lower_priority; dev50_tuning_slice; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; 1_suggested_replacements

Bangla:

```text
নিচের কোনটি শূন্য দশার সমতুল্য?
A. \pi/2
B. \pi
C. 3\pi/2
D. 2\pi
Answer with only A, B, C, or D.
```

English:

```text
Which one of the following is equivalent to zero phase?
A. \pi/2
B. \pi
C. 3\pi/2
D. 2\pi
Answer with only A, B, C, or D.
```

Current Banglish:

```text
nicher konoti shuny doshar somotuly?
A. \pi/2
B. \pi
C. 3\pi/2
D. 2\pi
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
nicher konti shuny doshar somotuly?
A. \pi/2
B. \pi
C. 3\pi/2
D. 2\pi
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 114. benqa_10th-Math-II_0062

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
- Impact rank: 114
- Impact tier: `tier_4_low`
- Impact score: 58
- Split: `test`
- Impact reasons: priority=lower_priority; heldout_test150; main_benqa_gap_slice; qwen3_v4_wrong; 1_suggested_replacements

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

## 115. benqa_10th-Math-II_0102

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
- Impact rank: 115
- Impact tier: `tier_4_low`
- Impact score: 58
- Split: `test`
- Impact reasons: priority=lower_priority; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; 1_suggested_replacements

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

## 116. benqa_10th-Math-II_0326

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
- Impact rank: 116
- Impact tier: `tier_4_low`
- Impact score: 58
- Split: `test`
- Impact reasons: priority=lower_priority; heldout_test150; main_benqa_gap_slice; qwen3_v4_wrong; 1_suggested_replacements

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

## 117. benqa_10th-Math-II_0347

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
- Impact rank: 117
- Impact tier: `tier_4_low`
- Impact score: 58
- Split: `test`
- Impact reasons: priority=lower_priority; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; 1_suggested_replacements

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

## 118. benqa_10th-Math-II_0357

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
- Impact rank: 118
- Impact tier: `tier_4_low`
- Impact score: 58
- Split: `test`
- Impact reasons: priority=lower_priority; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; 1_suggested_replacements

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
- Impact rank: 119
- Impact tier: `tier_4_low`
- Impact score: 58
- Split: `test`
- Impact reasons: priority=lower_priority; heldout_test150; main_benqa_gap_slice; qwen3_v4_wrong; 1_suggested_replacements

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

## 120. benqa_12th-Chemistry-I_0028

- CSV row: 127
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
- Impact rank: 120
- Impact tier: `tier_4_low`
- Impact score: 58
- Split: `test`
- Impact reasons: priority=lower_priority; heldout_test150; main_benqa_gap_slice; qwen3_v4_wrong; 1_suggested_replacements

Bangla:

```text
1% NaOH দ্রবণের pH কত?
A. 0.8
B. 13.4
C. 13.2
D. 1
Answer with only A, B, C, or D.
```

English:

```text
What is pH of 1% NaOH solution?
A. 0.8
B. 13.4
C. 13.2
D. 1
Answer with only A, B, C, or D.
```

Current Banglish:

```text
1% NaOH droboner pH kot?
A. 0.8
B. 13.4
C. 13.2
D. 1
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
1% NaOH droboner pH koto?
A. 0.8
B. 13.4
C. 13.2
D. 1
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank
