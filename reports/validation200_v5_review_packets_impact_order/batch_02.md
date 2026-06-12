# Validation-200 v5 Review Packet 02

Source queue: `data/slices/validation_200_v5_review_queue.csv`
Batch: 2/7
Rows in batch: 20

Fill the source CSV, not this Markdown packet. Use this packet only for
source/context reading while editing `reviewed_banglish`,
`quality_label`, and `review_notes` in the queue.

Allowed labels: `ok`, `minor_edit`, `major_edit`, `bad`.

## 21. benqa_10th-Chemistry_0110

- CSV row: 64
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
- Impact rank: 21
- Impact tier: `tier_1_review_first`
- Impact score: 150
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_v4_wrong; qwen3_recoverable_by_other_script; 1_suggested_replacements

Bangla:

```text
চুনের পানির সংকেত কোনটি?
A. CaCO_{3}
B. CaO
C. Ca(OH)_{2}
D. Ca(HCO_{3})_{2}
Answer with only A, B, C, or D.
```

English:

```text
Which one is the formula of lime water?
A. CaCO_{3}
B. CaO
C. Ca(OH)_{2}
D. Ca(HCO_{3})_{2}
Answer with only A, B, C, or D.
```

Current Banglish:

```text
chuner panir songket konoti?
A. CaCO_{3}
B. CaO
C. Ca(OH)_{2}
D. Ca(HCO_{3})_{2}
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
chuner panir songket konti?
A. CaCO_{3}
B. CaO
C. Ca(OH)_{2}
D. Ca(HCO_{3})_{2}
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 22. banglamath_0552

- CSV row: 13
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 4
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); uchchota->ucchota (1)
- Impact rank: 22
- Impact tier: `tier_1_review_first`
- Impact score: 148
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_v4_wrong; 4_suggested_replacements; ksh_heavy

Bangla:

```text
একটি সামান্তরিকের ভূমি ৯০ গজ ও উচ্চতা ৫০ গজ হলে তার ক্ষেত্রফল কত
Return only the final answer.
```

English:

```text
If a parallelogram has a base of 90 yards and height of 50 yards, what is its area?
Return only the final answer.
```

Current Banglish:

```text
ekoti samantoriker bhumi 90 goj o uchchota 50 goj hole tar kshetrofol kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti samantoriker bhumi 90 goj o ucchota 50 goj hole tar khetrofol koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 23. benqa_10th-Biology_0156

- CSV row: 61
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
- Impact rank: 23
- Impact tier: `tier_1_review_first`
- Impact score: 148
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 1_suggested_replacements

Bangla:

```text
আমিষে শতকরা কত ভাগ নাইট্রোজেন বিদ্যমান
A. 12
B. 14
C. 16
D. 18
Answer with only A, B, C, or D.
```

English:

```text
What percentage of Nitrogen is present in protein?
A. 12
B. 14
C. 16
D. 18
Answer with only A, B, C, or D.
```

Current Banglish:

```text
amishe shotokora kot bhag naitrojen bidyoman
A. 12
B. 14
C. 16
D. 18
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
amishe shotokora koto bhag naitrojen bidyoman
A. 12
B. 14
C. 16
D. 18
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 24. benqa_10th-Math_0271

- CSV row: 70
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
- Impact rank: 24
- Impact tier: `tier_1_review_first`
- Impact score: 148
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 1_suggested_replacements

Bangla:

```text
স্থূলকোণী ত্রিভুজের স্থূলকোণ ছাড়া বাকি কোণ দুটি কত হলে ত্রিভুজ অংকন সম্ভব?
A. 30\degree ও 60\degree
B. 40\degree ও 50\degree
C. 45\degree ও 45\degree
D. 50\degree ও 30\degree
Answer with only A, B, C, or D.
```

English:

```text
To draw a triangle which is the value of rest two angles except obtuse angle of obtuse angle triangle?
A. 30\degree and 60\degree
B. 40\degree and 50\degree
C. 45\degree and 45\degree
D. 50\degree and 30\degree
Answer with only A, B, C, or D.
```

Current Banglish:

```text
sthulokoni tribhujer sthulokon chhara baki kon duti kot hole tribhuj ongkon sombhob?
A. 30\degree o 60\degree
B. 40\degree o 50\degree
C. 45\degree o 45\degree
D. 50\degree o 30\degree
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
sthulokoni tribhujer sthulokon chhara baki kon duti koto hole tribhuj ongkon sombhob?
A. 30\degree o 60\degree
B. 40\degree o 50\degree
C. 45\degree o 45\degree
D. 50\degree o 30\degree
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 25. benqa_12th-Biology-I_0222

- CSV row: 76
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
- Impact rank: 25
- Impact tier: `tier_1_review_first`
- Impact score: 148
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen25_agreement_route_gain; qwen3_v4_wrong; 1_suggested_replacements

Bangla:

```text
উদ্ভিদ কোনটি মাটি হতে নেয়?
A. নাইট্রোজেন
B. হাইড্রোজেন
C. অক্সিজেন
D. কার্বন
Answer with only A, B, C, or D.
```

English:

```text
What does the plant take from the soild?
A. Nitrogen
B. Hydrogen
C. Oxygen
D. Carbon
Answer with only A, B, C, or D.
```

Current Banglish:

```text
udbhid konoti mati hote ney?
A. naitrojen
B. haidrojen
C. oksijen
D. karbon
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
udbhid konti mati hote ney?
A. naitrojen
B. haidrojen
C. oksijen
D. karbon
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 26. benqa_8th-Science_0127

- CSV row: 93
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_single_edit`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: achhe->ache (1)
- Impact rank: 26
- Impact tier: `tier_1_review_first`
- Impact score: 148
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 1_suggested_replacements

Bangla:

```text
কোন গ্রহের সবচেয়ে বেশি উপগ্রহ আছে?
A. শনি
B. বৃহস্পতি
C. ইউরেনাস
D. নেপচুন
Answer with only A, B, C, or D.
```

English:

```text
Which planet has maximum satellites?
A. Saturn
B. Jupiter
C. Uranus
D. Neptune
Answer with only A, B, C, or D.
```

Current Banglish:

```text
kon groher sobocheye beshi upogroh achhe?
A. shoni
B. brihospoti
C. iurenas
D. nepochun
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
kon groher sobocheye beshi upogroh ache?
A. shoni
B. brihospoti
C. iurenas
D. nepochun
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 27. benqa_12th-Physics-II_0290

- CSV row: 39
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
- Impact rank: 27
- Impact tier: `tier_1_review_first`
- Impact score: 145
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen3_v4_wrong; qwen3_recoverable_by_other_script; 2_suggested_replacements

Bangla:

```text
একটি কার্নো ইঞ্জিনের কার্যনির্বাহক বস্তু 400 K তাপমাত্রার তাপ উৎস হতে 840 J তাপ গ্রহণ করে তাপগ্রাহকে 630 J তাপ বর্জন করে। তাপ গ্রাহকের তাপমাত্রা কত?
A. 210 K
B. 300 K
C. 400 K
D. 440 K
Answer with only A, B, C, or D.
```

English:

```text
In Carnot's engine 840 J of heat is absorbed from a source at 400 K and is released 630 J of heat in the sink. What is the temperature of the sink?
A. 210 K
B. 300 K
C. 400 K
D. 440 K
Answer with only A, B, C, or D.
```

Current Banglish:

```text
ekoti karno injiner karyonirbahok bostu 400 K tapomatrar tap utos hote 840 J tap grohon kore tapograhoke 630 J tap borjon kore. tap grahoker tapomatra kot?
A. 210 K
B. 300 K
C. 400 K
D. 440 K
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
ekti karno injiner karyonirbahok bostu 400 K tapomatrar tap utos hote 840 J tap grohon kore tapograhoke 630 J tap borjon kore. tap grahoker tapomatra koto?
A. 210 K
B. 300 K
C. 400 K
D. 440 K
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 28. banglamath_0538

- CSV row: 2
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 8
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ayotakar->ayotokar (1); choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)
- Impact rank: 28
- Impact tier: `tier_1_review_first`
- Impact score: 144
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen3_v4_wrong; 8_suggested_replacements; ksh_heavy

Bangla:

```text
একটি আয়তাকার বাগানের দৈর্ঘ্য ৬০ মিটার ও প্রস্থ ৪০ মিটার। এর ভিতরে ২ মিটার চওড়া রাস্তা থাকলে রাস্তার ক্ষেত্রফল কত
Return only the final answer.
```

English:

```text
A rectangular garden is 60m by 40m. If there’s a 2m wide path inside, what is the area of the path?
Return only the final answer.
```

Current Banglish:

```text
ekoti ayotakar baganer doirghy 60 mitar o prosth 40 mitar. er bhitore 2 mitar choora rasta thakole rastar kshetrofol kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti ayotokar baganer doirgho 60 mitar o prostho 40 mitar. er bhitore 2 mitar chowra rasta thakle rastar khetrofol koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 29. banglamath_0541

- CSV row: 3
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 8
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ayotakar->ayotokar (1); choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)
- Impact rank: 29
- Impact tier: `tier_1_review_first`
- Impact score: 144
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen3_v4_wrong; 8_suggested_replacements; ksh_heavy

Bangla:

```text
একটি আয়তাকার বাগানের দৈর্ঘ্য ৫০ মি ও প্রস্থ ৩০ মি। এর ভিতরে ৩ মিটার চওড়া রাস্তা থাকলে রাস্তার ক্ষেত্রফল কত
Return only the final answer.
```

English:

```text
A rectangular garden is 50m by 30m. If there’s a 3m wide path inside, what is the area of the path?
Return only the final answer.
```

Current Banglish:

```text
ekoti ayotakar baganer doirghy 50 mi o prosth 30 mi. er bhitore 3 mitar choora rasta thakole rastar kshetrofol kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti ayotokar baganer doirgho 50 mi o prostho 30 mi. er bhitore 3 mitar chowra rasta thakle rastar khetrofol koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 30. banglamath_1697

- CSV row: 56
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
- Impact rank: 30
- Impact tier: `tier_1_review_first`
- Impact score: 143
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; qwen25_v4_wrong; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 1_suggested_replacements

Bangla:

```text
৩০ কে ১/২ দিয়ে ভাগ করে ১০ যোগ করলে কত হয়?
Return only the final answer.
```

English:

```text
Divide 30 by ½ and add 10. What is the result?
Return only the final answer.
```

Current Banglish:

```text
30 ke 1/2 diye bhag kore 10 jog korole kot hoy?
Return only the final answer.
```

Auto-suggested Banglish:

```text
30 ke 1/2 diye bhag kore 10 jog korole koto hoy?
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 31. banglamath_0549

- CSV row: 4
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 7
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)
- Impact rank: 31
- Impact tier: `tier_1_review_first`
- Impact score: 142
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen3_v4_wrong; 7_suggested_replacements; ksh_heavy

Bangla:

```text
একটি বাগানের বাইরে ২.৫ মিটার চওড়া রাস্তা থাকলে রাস্তার ক্ষেত্রফল কত যদি বাগানের দৈর্ঘ্য ৫০ মি ও প্রস্থ ৩৫ মি হয়
Return only the final answer.
```

English:

```text
If a 2.5m wide path surrounds a garden of 50m by 35m, what is the area of the path?
Return only the final answer.
```

Current Banglish:

```text
ekoti baganer baire 2.5 mitar choora rasta thakole rastar kshetrofol kot jodi baganer doirghy 50 mi o prosth 35 mi hoy
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti baganer baire 2.5 mitar chowra rasta thakle rastar khetrofol koto jodi baganer doirgho 50 mi o prostho 35 mi hoy
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 32. banglamath_1688

- CSV row: 5
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 7
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); korote->korte (1); penyaj->peyaj (5)
- Impact rank: 32
- Impact tier: `tier_1_review_first`
- Impact score: 142
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen3_v4_wrong; 7_suggested_replacements; ksh_heavy

Bangla:

```text
কোন একটি বিয়ের অনুষ্ঠানে রান্না করতে বাবুর্চি ও তার সহকর্মী মোট ৪০০টি পেঁয়াজ কাটেন। বাবুর্চি প্রতি মিনিটে অন্তত ৩টি পেঁয়াজ এবং তার সহকর্মী প্রতি মিনিটে অন্তত ২টি পেঁয়াজ কাটতে পারে। যদি বাবুর্চি তার সহকর্মীর চেয়ে ২৫ মিনিট আগে পেঁয়াজ কাটা বন্ধ, তবে কে কতটি পেঁয়াজ কেটেছিল আর কার কতক্ষণ সময় লেগেছিল?
Return only the final answer.
```

English:

```text
At a wedding, a chef and assistant cut 400 onions together. The chef cuts at least 3 onions per minute and the assistant cuts at least 2 per minute. If the chef stops 25 minutes before the assistant, how many onions did each cut and how long did they work?
Return only the final answer.
```

Current Banglish:

```text
kon ekoti biyer onushthane ranna korote baburchi o tar sohokormi mot 400ti penyaj katen. baburchi proti minite ontot 3ti penyaj ebong tar sohokormi proti minite ontot 2ti penyaj katote pare. jodi baburchi tar sohokormir cheye 25 minit age penyaj kata bondh, tobe ke kototi penyaj ketechhil ar kar kotokshon somoy legechhil?
Return only the final answer.
```

Auto-suggested Banglish:

```text
kon ekti biyer onushthane ranna korte baburchi o tar sohokormi mot 400ti peyaj katen. baburchi proti minite ontot 3ti peyaj ebong tar sohokormi proti minite ontot 2ti peyaj katote pare. jodi baburchi tar sohokormir cheye 25 minit age peyaj kata bondh, tobe ke kototi peyaj ketechhil ar kar kotokshon somoy legechhil?
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 33. benqa_10th-Math_0032

- CSV row: 69
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
- Impact rank: 33
- Impact tier: `tier_1_review_first`
- Impact score: 140
- Split: `dev`
- Impact reasons: priority=both_wrong_single_edit; dev50_tuning_slice; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen25_agreement_route_gain; qwen3_v4_wrong; 1_suggested_replacements

Bangla:

```text
(\sqrt{3})^{x+2} = 27 হলে x এর মান কত?
A. 6
B. 4
C. 3
D. 2
Answer with only A, B, C, or D.
```

English:

```text
If (\sqrt{3})^{x+2} = 27, what is the value of x?
A. 6
B. 4
C. 3
D. 2
Answer with only A, B, C, or D.
```

Current Banglish:

```text
(\sqrt{3})^{x+2} = 27 hole x er man kot?
A. 6
B. 4
C. 3
D. 2
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
(\sqrt{3})^{x+2} = 27 hole x er man koto?
A. 6
B. 4
C. 3
D. 2
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 34. banglamath_0540

- CSV row: 8
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 5
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: doirghy->doirgho (2); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1)
- Impact rank: 34
- Impact tier: `tier_1_review_first`
- Impact score: 138
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen3_v4_wrong; 5_suggested_replacements; ksh_heavy

Bangla:

```text
একটি ঘরের দৈর্ঘ্য প্রস্থের তিনগুণ এবং ক্ষেত্রফল ১৪৭ বর্গমিটার হলে ঘরটির দৈর্ঘ্য কত
Return only the final answer.
```

English:

```text
If a room's length is three times its width and the area is 147 sq. meters, what is the length?
Return only the final answer.
```

Current Banglish:

```text
ekoti ghorer doirghy prosther tinogun ebong kshetrofol 147 borgomitar hole ghorotir doirghy kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti ghorer doirgho prosther tinogun ebong khetrofol 147 borgomitar hole ghorotir doirgho koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 35. benqa_10th-Biology_0090

- CSV row: 59
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
- Impact rank: 35
- Impact tier: `tier_1_review_first`
- Impact score: 138
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen3_v4_wrong; qwen3_recoverable_by_other_script; 1_suggested_replacements

Bangla:

```text
পতঙ্গপরাগী ফুল কোনটি?
A. ধান
B. কচু
C. সরিষা
D. আখ
Answer with only A, B, C, or D.
```

English:

```text
Which one is insects pollinated flower?
A. Rice
B. Taro
C. Mustard
D. Sugarcane
Answer with only A, B, C, or D.
```

Current Banglish:

```text
potonggoporagi ful konoti?
A. dhan
B. kochu
C. sorisha
D. akh
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
potonggoporagi ful konti?
A. dhan
B. kochu
C. sorisha
D. akh
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 36. benqa_10th-Biology_0215

- CSV row: 62
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_single_edit`
- Replacement count: 1
- Artifact patterns: `oja_loanword`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: konoti->konti (1)
- Impact rank: 36
- Impact tier: `tier_1_review_first`
- Impact score: 138
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_v4_wrong; 1_suggested_replacements

Bangla:

```text
C_{6}H_{12}O_{6}\xarrowright{এনজাইম}C_{3}H_{4}O_{3} উদ্দীপকের প্রক্রিয়াটি- i. সবাত ও অবাত শ্বসনের প্রথম ধাপ ii. কোষের মাইটোকন্ড্রিয়ায় ঘটে থাকে iii. এতে নিট অণু ATP উৎপন্ন হয় নিচের কোনটি সঠিক?
A. i ও ii
B. i ও iii
C. ii ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

English:

```text
C_{6}H_{12}O_{6} \xrightarrow{Enzyme} C_{3}H_{4}O_{3} the process of the stem- i. is the inital stage of both acrobic and anacrobic respiration ii. takes place in the mitochondria of a cell iii. produces & molecules of neat ATP Which one is correct?
A. i and ii
B. i and iii
C. ii and iii
D. i, ii and iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
C_{6}H_{12}O_{6}\xarrowright{enojaim}C_{3}H_{4}O_{3} uddipoker prokriyati- i. sobat o obat shbosoner prothom dhap ii. kosher maitokondriyay ghote thake iii. ete nit onu ATP utoponn hoy nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
C_{6}H_{12}O_{6}\xarrowright{enojaim}C_{3}H_{4}O_{3} uddipoker prokriyati- i. sobat o obat shbosoner prothom dhap ii. kosher maitokondriyay ghote thake iii. ete nit onu ATP utoponn hoy nicher konti sothik?
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

## 37. benqa_10th-Math_0324

- CSV row: 71
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
- Impact rank: 37
- Impact tier: `tier_1_review_first`
- Impact score: 138
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_v4_wrong; 1_suggested_replacements

Bangla:

```text
a = \sqrt{3} এবং b = \sqrt{12} হলে নিচের কোনটি অমূলদ সংখ্যা?
A. a + b
B. ab
C. \frac{a}{b}
D. \frac{b}{a}
Answer with only A, B, C, or D.
```

English:

```text
If a = \sqrt{3} and b = \sqrt{12}, which one is irrational number?
A. a + b
B. ab
C. \frac{a}{b}
D. \frac{b}{a}
Answer with only A, B, C, or D.
```

Current Banglish:

```text
a = \sqrt{3} ebong b = \sqrt{12} hole nicher konoti omulod songkhya?
A. a + b
B. ab
C. \frac{a}{b}
D. \frac{b}{a}
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
a = \sqrt{3} ebong b = \sqrt{12} hole nicher konti omulod songkhya?
A. a + b
B. ab
C. \frac{a}{b}
D. \frac{b}{a}
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 38. benqa_12th-Biology-II_0122

- CSV row: 74
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
- Impact rank: 38
- Impact tier: `tier_1_review_first`
- Impact score: 138
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_v4_wrong; 1_suggested_replacements

Bangla:

```text
হৃৎপিন্ডের অলিন্দের ডায়াস্টোলের সময়কাল কত সেকেন্ড?
A. 0.7
B. 0.5
C. 0.3
D. 0.1
Answer with only A, B, C, or D.
```

English:

```text
How mush second is the duration of diastole in the atrium of the heart?
A. 0.7
B. 0.5
C. 0.3
D. 0.1
Answer with only A, B, C, or D.
```

Current Banglish:

```text
hritopinder olinder dayastoler somoyokal kot sekend?
A. 0.7
B. 0.5
C. 0.3
D. 0.1
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
hritopinder olinder dayastoler somoyokal koto sekend?
A. 0.7
B. 0.5
C. 0.3
D. 0.1
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 39. benqa_12th-Chemistry-II_0117

- CSV row: 79
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
- Impact rank: 39
- Impact tier: `tier_1_review_first`
- Impact score: 138
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen3_v4_wrong; qwen3_recoverable_by_other_script; 1_suggested_replacements

Bangla:

```text
অ্যালডিহাইড ও কিটোনের মধ্যে পার্থক্য নিরূপনের জন্য ব্যবহৃত বিকারক- i. টলেন বিকারক ii. 2 : 4 - DNPH iii. ফেলিং দ্রবণ নিচের কোনটি সঠিক?
A. i ও ii
B. ii ও iii
C. i ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

English:

```text
For the differentiation between aldehyde and ketone usable reagent is- i. tollen's reagent ii. 2 : 4 - DNPH iii. fehling solution Which one is correct?
A. i and ii
B. ii and iii
C. i and iii
D. i, ii and iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
alodihaid o kitoner modhye parthoky niruponer jony byobohrit bikarok- i. tolen bikarok ii. 2 : 4 - DNPH iii. feling drobon nicher konoti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
alodihaid o kitoner modhye parthoky niruponer jony byobohrit bikarok- i. tolen bikarok ii. 2 : 4 - DNPH iii. feling drobon nicher konti sothik?
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

## 40. benqa_12th-Physics-II_0037

- CSV row: 86
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
- Impact rank: 40
- Impact tier: `tier_1_review_first`
- Impact score: 138
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_v4_wrong; 1_suggested_replacements

Bangla:

```text
এনট্রপির একক নিচের কোনটি?
A. NK^{-1}
B. JK^{-1}
C. JK^{-1} mol^{-1}
D. এককহীন রাশি
Answer with only A, B, C, or D.
```

English:

```text
Which one is the unit of entropy?
A. NK^{-1}
B. JK^{-1}
C. JK^{-1} mol^{-1}
D. Unitless quantity
Answer with only A, B, C, or D.
```

Current Banglish:

```text
enotropir ekok nicher konoti?
A. NK^{-1}
B. JK^{-1}
C. JK^{-1} mol^{-1}
D. ekokohin rashi
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
enotropir ekok nicher konti?
A. NK^{-1}
B. JK^{-1}
C. JK^{-1} mol^{-1}
D. ekokohin rashi
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank
