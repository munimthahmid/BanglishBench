# Validation-200 v5 Review Packet 03

Source queue: `data/slices/validation_200_v5_review_queue.csv`
Batch: 3/7
Rows in batch: 20

Fill the source CSV, not this Markdown packet. Use this packet only for
source/context reading while editing `reviewed_banglish`,
`quality_label`, and `review_notes` in the queue.

Allowed labels: `ok`, `minor_edit`, `major_edit`, `bad`.

## 41. benqa_12th-Physics-II_0195

- CSV row: 88
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_single_edit`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: kot->koto (1)
- Impact rank: 41
- Impact tier: `tier_1_review_first`
- Impact score: 138
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_v4_wrong; 1_suggested_replacements

Bangla:

```text
পৃথিবীর ব্যাসার্ধ 6500 km এর ধারকত্ব কত?
A. 711 F
B. 722 \mu F
C. 640 \mu F
D. 614 \mu F
Answer with only A, B, C, or D.
```

English:

```text
The radius of earth is 6500 km. What is its capacitance?
A. 711 F
B. 722 \mu F
C. 640 \mu F
D. 614 \mu F
Answer with only A, B, C, or D.
```

Current Banglish:

```text
prithibir byasardh 6500 km er dharokotto kot?
A. 711 F
B. 722 \mu F
C. 640 \mu F
D. 614 \mu F
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
prithibir byasardh 6500 km er dharokotto koto?
A. 711 F
B. 722 \mu F
C. 640 \mu F
D. 614 \mu F
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 42. benqa_8th-Science_0159

- CSV row: 95
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_single_edit`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: konoti->konti (1)
- Impact rank: 42
- Impact tier: `tier_1_review_first`
- Impact score: 138
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen3_v4_wrong; qwen3_recoverable_by_other_script; 1_suggested_replacements

Bangla:

```text
নিচের কোনটি রসালো ফল?
A. আতা
B. কলা
C. আনারস
D. কাঁঠাল
Answer with only A, B, C, or D.
```

English:

```text
Which of the followings is fleshy fruits?
A. Custard apple
B. Banana
C. Pineapple
D. Jackfruit
Answer with only A, B, C, or D.
```

Current Banglish:

```text
nicher konoti rosalo fol?
A. ata
B. kola
C. anaros
D. kanthal
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
nicher konti rosalo fol?
A. ata
B. kola
C. anaros
D. kanthal
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 43. benqa_12th-Physics-I_0254

- CSV row: 40
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: konoti->konti (1); kshetre->khetre (1)
- Impact rank: 43
- Impact tier: `tier_1_review_first`
- Impact score: 137
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen3_v4_wrong; 2_suggested_replacements; ksh_heavy

Bangla:

```text
মহাকর্ষ ক্ষেত্র প্রাবল্যের মাত্রার ক্ষেত্রে কোনটি সঠিক?
A. [LT^{-1}]
B. [LT^{-2}]
C. [MLT^{-1}]
D. [MLT^{-2}]
Answer with only A, B, C, or D.
```

English:

```text
Which one is correct for the dimention of gravitational field intensity?
A. [LT^{-1}]
B. [LT^{-2}]
C. [MLT^{-1}]
D. [MLT^{-2}]
Answer with only A, B, C, or D.
```

Current Banglish:

```text
mohakorsh kshetr prabolyer matrar kshetre konoti sothik?
A. [LT^{-1}]
B. [LT^{-2}]
C. [MLT^{-1}]
D. [MLT^{-2}]
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
mohakorsh kshetr prabolyer matrar khetre konti sothik?
A. [LT^{-1}]
B. [LT^{-2}]
C. [MLT^{-1}]
D. [MLT^{-2}]
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 44. banglamath_0559

- CSV row: 22
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 3
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1)
- Impact rank: 44
- Impact tier: `tier_2_high`
- Impact score: 134
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen3_v4_wrong; 3_suggested_replacements; ksh_heavy

Bangla:

```text
একটি বর্গক্ষেত্রের পরিসীমা ১৬০ মিটার হলে তার ক্ষেত্রফল কত
Return only the final answer.
```

English:

```text
If a square has a perimeter of 160 meters, what is its area?
Return only the final answer.
```

Current Banglish:

```text
ekoti borgokshetrer porisima 160 mitar hole tar kshetrofol kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti borgokshetrer porisima 160 mitar hole tar khetrofol koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 45. banglamath_0185

- CSV row: 44
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_single_edit`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: kot->koto (1)
- Impact rank: 45
- Impact tier: `tier_2_high`
- Impact score: 133
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_v4_wrong; 1_suggested_replacements

Bangla:

```text
১২০ কেজি চালে ১০ জন লোকের ২৭ দিন চলে। ৪৫ দিন চলতে কত কেজি চাল প্রয়োজন হবে
Return only the final answer.
```

English:

```text
120 kg of rice lasts 10 people for 27 days. How much rice is needed to last 45 days?
Return only the final answer.
```

Current Banglish:

```text
120 keji chale 10 jon loker 27 din chole. 45 din cholote kot keji chal proyojon hobe
Return only the final answer.
```

Auto-suggested Banglish:

```text
120 keji chale 10 jon loker 27 din chole. 45 din cholote koto keji chal proyojon hobe
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 46. benqa_10th-Physics_0106

- CSV row: 35
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: korote->korte (1); kot->koto (1)
- Impact rank: 46
- Impact tier: `tier_2_high`
- Impact score: 133
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen3_v4_wrong; 2_suggested_replacements

Bangla:

```text
বিনা বাধায় পড়ন্ত বস্তু 5 সেকেন্ডে 50 মিটার পথ অতিক্রম করলে 72 মিটার পথ অতিক্রম করতে কত সেকেন্ড সময় লাগবে?
A. 6
B. 7.2
C. 9.5
D. 12
Answer with only A, B, C, or D.
```

English:

```text
If a freely falling body travels 50 m in 5 sec then how much time in second will need to travel thr distance of 72 meter?
A. 6
B. 7.2
C. 9.5
D. 12
Answer with only A, B, C, or D.
```

Current Banglish:

```text
bina badhay poront bostu 5 sekende 50 mitar poth otikrom korole 72 mitar poth otikrom korote kot sekend somoy lagobe?
A. 6
B. 7.2
C. 9.5
D. 12
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
bina badhay poront bostu 5 sekende 50 mitar poth otikrom korole 72 mitar poth otikrom korte koto sekend somoy lagobe?
A. 6
B. 7.2
C. 9.5
D. 12
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 47. benqa_8th-Science_0098

- CSV row: 41
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); kot->koto (1)
- Impact rank: 47
- Impact tier: `tier_2_high`
- Impact score: 133
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen3_v4_wrong; 2_suggested_replacements

Bangla:

```text
ইশার বাসার বেডরুমে দুটি টিউবলাইট ও একটি ফ্যান প্যারালালে সংযুক্ত করা হয়। বেডরুমের বর্তনীর সাথে ১০ অ্যাম্পিয়ার মানের ফিউজ ব্যবহার করা হয়। দ্বিতীয় উপকরণটির জন্য কার্যকরী ফিউজ কত?
A. ৫ অ্যাম্পিয়ার
B. ১০ অ্যাম্পিয়ার
C. ১৫ অ্যাম্পিয়ার
D. ৩০ অ্যাম্পিয়ার
Answer with only A, B, C, or D.
```

English:

```text
In the bedroom of Esha's house, there are two tube lights and e one fan conndctied in paralled. Afuse of 10 ampere is used in the circuit of bedrood. What is the appropriate fuse for the second element?
A. 5 ampere
B. 10 ampere
C. 15 ampere
D. 30 ampere
Answer with only A, B, C, or D.
```

Current Banglish:

```text
ishar basar bedorume duti tiubolait o ekoti fyan pyaralale songjukt kora hoy. bedorumer bortonir sathe 10 ampiyar maner fiuj byobohar kora hoy. dwitiy upokoronotir jony karyokori fiuj kot?
A. 5 ampiyar
B. 10 ampiyar
C. 15 ampiyar
D. 30 ampiyar
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
ishar basar bedorume duti tiubolait o ekti fyan pyaralale songjukt kora hoy. bedorumer bortonir sathe 10 ampiyar maner fiuj byobohar kora hoy. dwitiy upokoronotir jony karyokori fiuj koto?
A. 5 ampiyar
B. 10 ampiyar
C. 15 ampiyar
D. 30 ampiyar
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 48. banglamath_0550

- CSV row: 29
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: kot->koto (1); kshetrofol->khetrofol (1)
- Impact rank: 48
- Impact tier: `tier_2_high`
- Impact score: 132
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen3_v4_wrong; 2_suggested_replacements; ksh_heavy

Bangla:

```text
রাস্তাসহ বাগানের পরিসীমা ১৯০ মিটার হলে সমান পরিসীমা বিশিষ্ট বর্গাকার মাঠের ক্ষেত্রফল কত
Return only the final answer.
```

English:

```text
If the total perimeter (including path) of a garden is 190m, what is the area of a square field with the same perimeter?
Return only the final answer.
```

Current Banglish:

```text
rastasoh baganer porisima 190 mitar hole soman porisima bishisht borgakar mather kshetrofol kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
rastasoh baganer porisima 190 mitar hole soman porisima bishisht borgakar mather khetrofol koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 49. banglamath_0553

- CSV row: 30
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: kshetrofol->khetrofol (2)
- Impact rank: 49
- Impact tier: `tier_2_high`
- Impact score: 132
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen3_v4_wrong; 2_suggested_replacements; ksh_heavy

Bangla:

```text
সামান্তরিকের মেঝে পাথর দ্বারা ঢাকতে কতটি পাথর লাগবে যদি মেঝের ক্ষেত্রফল ৪৫০০ বর্গগজ ও পাথরের ক্ষেত্রফল ৪ বর্গগজ হয়
Return only the final answer.
```

English:

```text
To cover a parallelogram floor of 4500 sq. yards with stones each covering 4 sq. yards, how many stones are needed?
Return only the final answer.
```

Current Banglish:

```text
samantoriker mejhe pathor dwara dhakote kototi pathor lagobe jodi mejher kshetrofol 4500 borgogoj o pathorer kshetrofol 4 borgogoj hoy
Return only the final answer.
```

Auto-suggested Banglish:

```text
samantoriker mejhe pathor dwara dhakote kototi pathor lagobe jodi mejher khetrofol 4500 borgogoj o pathorer khetrofol 4 borgogoj hoy
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 50. banglamath_0558

- CSV row: 14
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 4
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ayotakar->ayotokar (1); doirghy->doirgho (1); kot->koto (1); prosth->prostho (1)
- Impact rank: 50
- Impact tier: `tier_2_high`
- Impact score: 132
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen3_v4_wrong; 4_suggested_replacements

Bangla:

```text
৬০ মিটার দীর্ঘ আয়তাকার বাগানের দৈর্ঘ্য প্রস্থের ৩ গুণ হলে প্রস্থ কত
Return only the final answer.
```

English:

```text
A rectangular garden is 60 meters long and the length is 3 times the width. What is the width?
Return only the final answer.
```

Current Banglish:

```text
60 mitar dirgh ayotakar baganer doirghy prosther 3 gun hole prosth kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
60 mitar dirgh ayotokar baganer doirgho prosther 3 gun hole prostho koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 51. banglamath_1691

- CSV row: 15
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 4
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: achhe->ache (1); ekoti->ekti (2); korote->korte (1)
- Impact rank: 51
- Impact tier: `tier_2_high`
- Impact score: 132
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen3_v4_wrong; 4_suggested_replacements

Bangla:

```text
বেরু গোয়ালার কাছে একটি কলসিতে ১০ লিটার দুধ এবং দুধ মাপার দুটি খালি পাত্র , একটি ৫ লিটারের, অপরটি ৩ লিটারের। সে ক্রেতাকে ১ লিটার দুধ বিক্রি করতে চায়। গোয়ালার কাছে জেডযেসব পাত্র আছে শুধু তা দিয়ে কিভাবে ক্রেতাকে ১ লিটার দুধ দেয়া সম্ভব?
Return only the final answer.
```

English:

```text
Beru the milkman has 10 liters of milk in a jar, and two empty containers: one of 5 liters and one of 3 liters. How can he measure exactly 1 liter using only these two containers?
Return only the final answer.
```

Current Banglish:

```text
beru goyalar kachhe ekoti kolosite 10 litar dudh ebong dudh mapar duti khali patr , ekoti 5 litarer, oporoti 3 litarer. se kretake 1 litar dudh bikri korote chay. goyalar kachhe jedojesob patr achhe shudhu ta diye kibhabe kretake 1 litar dudh deya sombhob?
Return only the final answer.
```

Auto-suggested Banglish:

```text
beru goyalar kachhe ekti kolosite 10 litar dudh ebong dudh mapar duti khali patr , ekti 5 litarer, oporoti 3 litarer. se kretake 1 litar dudh bikri korte chay. goyalar kachhe jedojesob patr ache shudhu ta diye kibhabe kretake 1 litar dudh deya sombhob?
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 52. banglamath_0519

- CSV row: 6
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 6
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ayotakar->ayotokar (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1)
- Impact rank: 52
- Impact tier: `tier_2_high`
- Impact score: 132
- Split: `dev`
- Impact reasons: priority=both_wrong_multi_edit; dev50_tuning_slice; qwen25_v4_wrong; qwen3_v4_wrong; 6_suggested_replacements; ksh_heavy

Bangla:

```text
একটি আয়তাকার বাগানের দৈর্ঘ্য ১৫০ মিটার ও প্রস্থ ৫০ মিটার হলে ক্ষেত্রফল কত
Return only the final answer.
```

English:

```text
If the length of a rectangular garden is 150 meters and width is 50 meters, what is the area?
Return only the final answer.
```

Current Banglish:

```text
ekoti ayotakar baganer doirghy 150 mitar o prosth 50 mitar hole kshetrofol kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti ayotokar baganer doirgho 150 mitar o prostho 50 mitar hole khetrofol koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 53. benqa_12th-Math-I_0218

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
- Impact rank: 53
- Impact tier: `tier_2_high`
- Impact score: 131
- Split: `test`
- Impact reasons: priority=qwen3_wrong_multi_edit; heldout_test150; main_benqa_gap_slice; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 2_suggested_replacements; ksh_heavy

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

## 54. banglamath_0183

- CSV row: 16
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 3
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: achhe->ache (1); ekoti->ekti (1); kot->koto (1)
- Impact rank: 54
- Impact tier: `tier_2_high`
- Impact score: 130
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen3_v4_wrong; 3_suggested_replacements

Bangla:

```text
একটি ছাত্রাবাসে ৫০ জনের ১৫ দিনের খাদ্য মজুদ আছে। ঐ খাদ্যে ২৫ জনের কত দিন চলবে
Return only the final answer.
```

English:

```text
A hostel has food for 50 people for 15 days. How many days will it last for 25 people?
Return only the final answer.
```

Current Banglish:

```text
ekoti chhatrabase 50 joner 15 diner khaddo mojud achhe. oi khadde 25 joner kot din cholobe
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti chhatrabase 50 joner 15 diner khaddo mojud ache. oi khadde 25 joner koto din cholobe
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 55. banglamath_0184

- CSV row: 17
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 3
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: korote->korte (2); kot->koto (1)
- Impact rank: 55
- Impact tier: `tier_2_high`
- Impact score: 130
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen3_v4_wrong; 3_suggested_replacements

Bangla:

```text
৯০০০ টাকা বিনিয়োগে প্রতিদিন ৪৫০ টাকা লাভ হলে ৬০০ টাকা লাভ করতে কত বিনিয়োগ করতে হবে
Return only the final answer.
```

English:

```text
If an investment of 9000 Taka yields 450 Taka profit per day, how much should be invested to earn 600 Taka per day?
Return only the final answer.
```

Current Banglish:

```text
9000 taka biniyoge protidin 450 taka labh hole 600 taka labh korote kot biniyog korote hobe
Return only the final answer.
```

Auto-suggested Banglish:

```text
9000 taka biniyoge protidin 450 taka labh hole 600 taka labh korte koto biniyog korte hobe
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 56. banglamath_0189

- CSV row: 19
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 3
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); korote->korte (2)
- Impact rank: 56
- Impact tier: `tier_2_high`
- Impact score: 130
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen3_v4_wrong; 3_suggested_replacements

Bangla:

```text
একটি কাজ ২ জন পুরুষ অথবা ৩ জন বালক সম্পন্ন করতে পারে। ৯ জন বালক কতজন পুরুষের সমান কাজ করতে পারবে
Return only the final answer.
```

English:

```text
A task can be completed by 2 men or 3 boys. How many men are equivalent to 9 boys?
Return only the final answer.
```

Current Banglish:

```text
ekoti kaj 2 jon purush othoba 3 jon balok somponn korote pare. 9 jon balok kotojon purusher soman kaj korote parobe
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti kaj 2 jon purush othoba 3 jon balok somponn korte pare. 9 jon balok kotojon purusher soman kaj korte parobe
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 57. banglamath_0542

- CSV row: 21
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 3
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: doirghy->doirgho (1); kot->koto (1); prosth->prostho (1)
- Impact rank: 57
- Impact tier: `tier_2_high`
- Impact score: 130
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen3_v4_wrong; 3_suggested_replacements

Bangla:

```text
রাস্তাবাদে বাগানের পরিসীমায় বেড়া দিতে প্রতি মিটারে ২৫ টাকা হিসেবে মোট কত খরচ হবে যদি রাস্তাবাদে বাগানের দৈর্ঘ্য ৪৪ মি ও প্রস্থ ২৪ মি হয়
Return only the final answer.
```

English:

```text
If the garden including the path is 44m by 24m, and fencing costs 25 Taka per meter, what is the total cost?
Return only the final answer.
```

Current Banglish:

```text
rastabade baganer porisimay bera dite proti mitare 25 taka hisebe mot kot khoroch hobe jodi rastabade baganer doirghy 44 mi o prosth 24 mi hoy
Return only the final answer.
```

Auto-suggested Banglish:

```text
rastabade baganer porisimay bera dite proti mitare 25 taka hisebe mot koto khoroch hobe jodi rastabade baganer doirgho 44 mi o prostho 24 mi hoy
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 58. benqa_10th-Chemistry_0191

- CSV row: 66
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_single_edit`
- Replacement count: 1
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: konoti->konti (1)
- Impact rank: 58
- Impact tier: `tier_2_high`
- Impact score: 130
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen3_v4_wrong; 1_suggested_replacements; ksh_heavy

Bangla:

```text
CH_{3}-CH_{2}-C \equiv CH + Cl_{2} \rightarrow A A + Cl_{2} \rightarrow B উদ্দীপকে A যৌগটি- i. সংযোজন বিক্রিয়া দেয় ii. প্লাস্টিক তৈরিতে ব্যবহৃত হয় iii. 'B' অপেক্ষা কম সক্রিয় নিচের কোনটি সঠিক?
A. i ও ii
B. ii ও iii
C. i ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

English:

```text
CH_{3}-CH_{2}-C\equiv CH+Cl_{2}\rightarrow A A+Cl_{2}\rightarrow B The compound 'A' of the stem- i. give addition reaction ii. is used to form plastic iii. is less active than 'B' Which of the following is correct?
A. i and ii
B. ii and iii
C. i and iii
D. i, ii and iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
CH_{3}-CH_{2}-C \equiv CH + Cl_{2} \rightarrow A A + Cl_{2} \rightarrow B uddipoke A jougoti- i. songjojon bikriya dey ii. plastik toirite byobohrit hoy iii. 'B' opeksha kom sokriy nicher konoti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
CH_{3}-CH_{2}-C \equiv CH + Cl_{2} \rightarrow A A + Cl_{2} \rightarrow B uddipoke A jougoti- i. songjojon bikriya dey ii. plastik toirite byobohrit hoy iii. 'B' opeksha kom sokriy nicher konti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 59. benqa_12th-Math-I_0186

- CSV row: 84
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_single_edit`
- Replacement count: 1
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: konoti->konti (1)
- Impact rank: 59
- Impact tier: `tier_2_high`
- Impact score: 130
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen3_v4_wrong; 1_suggested_replacements; ksh_heavy

Bangla:

```text
(-2, 3) বিন্দুতে কেন্দ্র এবং y-অক্ষকে স্পর্শ করে এরূপ বৃত্তের সমীকরণ কোনটি?
A. x^{2} + y^{2} + 4x - 6y + 9 = 0
B. x^{2} + y^{2} - 4x + 6y + 9 = 0
C. x^{2} + y^{2} + 4x - 6y + 4 = 0
D. x^{2} + y^{2} - 4x + 6y + 4 = 0
Answer with only A, B, C, or D.
```

English:

```text
What is the equation of a circle which passe through the point (-2, 3) and touches y-axis?
A. x^{2} + y^{2} + 4x - 6y + 9 = 0
B. x^{2} + y^{2} - 4x + 6y + 9 = 0
C. x^{2} + y^{2} + 4x - 6y + 4 = 0
D. x^{2} + y^{2} - 4x + 6y + 4 = 0
Answer with only A, B, C, or D.
```

Current Banglish:

```text
(-2, 3) bindute kendr ebong y-okshoke sporsh kore erup britter somikoron konoti?
A. x^{2} + y^{2} + 4x - 6y + 9 = 0
B. x^{2} + y^{2} - 4x + 6y + 9 = 0
C. x^{2} + y^{2} + 4x - 6y + 4 = 0
D. x^{2} + y^{2} - 4x + 6y + 4 = 0
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
(-2, 3) bindute kendr ebong y-okshoke sporsh kore erup britter somikoron konti?
A. x^{2} + y^{2} + 4x - 6y + 9 = 0
B. x^{2} + y^{2} - 4x + 6y + 9 = 0
C. x^{2} + y^{2} + 4x - 6y + 4 = 0
D. x^{2} + y^{2} - 4x + 6y + 4 = 0
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 60. benqa_12th-Physics-II_0267

- CSV row: 90
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_single_edit`
- Replacement count: 1
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: konoti->konti (1)
- Impact rank: 60
- Impact tier: `tier_2_high`
- Impact score: 130
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen3_v4_wrong; 1_suggested_replacements; ksh_heavy

Bangla:

```text
আপেক্ষিকতার তত্ত্ব অনুসারে- i. t = \frac{t_{0}}{\sqrt{1 - \frac{v^{2}}{c^{2}}}} ii. L = \frac{L_{0}}{\sqrt{1 - \frac{v^{2}}{c^{2}}}} iii. m = \frac{m_{0}}{\sqrt{1 - \frac{v^{2}}{c^{2}}}} নিচের কোনটি সঠিক?
A. i ও ii
B. i ও iii
C. ii ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

English:

```text
According to the theory of relativity- i. t = \frac{t_{0}}{\sqrt{1 - \frac{v^{2}}{c^{2}}}} ii. L = \frac{L_{0}}{\sqrt{1 - \frac{v^{2}}{c^{2}}}} iii. m = \frac{m_{0}}{\sqrt{1 - \frac{v^{2}}{c^{2}}}} Which one is correct?
A. i and ii
B. i and iii
C. ii and iii
D. i, ii and iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
apekshikotar totto onusare- i. t = \frac{t_{0}}{\sqrt{1 - \frac{v^{2}}{c^{2}}}} ii. L = \frac{L_{0}}{\sqrt{1 - \frac{v^{2}}{c^{2}}}} iii. m = \frac{m_{0}}{\sqrt{1 - \frac{v^{2}}{c^{2}}}} nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
apekshikotar totto onusare- i. t = \frac{t_{0}}{\sqrt{1 - \frac{v^{2}}{c^{2}}}} ii. L = \frac{L_{0}}{\sqrt{1 - \frac{v^{2}}{c^{2}}}} iii. m = \frac{m_{0}}{\sqrt{1 - \frac{v^{2}}{c^{2}}}} nicher konti sothik?
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
