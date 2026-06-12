# Validation-200 v5 Review Packet 04

Source queue: `data/slices/validation_200_v5_review_queue.csv`
Batch: 4/7
Rows in batch: 20

Fill the source CSV, not this Markdown packet. Use this packet only for
source/context reading while editing `reviewed_banglish`,
`quality_label`, and `review_notes` in the queue.

Allowed labels: `ok`, `minor_edit`, `major_edit`, `bad`.

## 61. benqa_10th-Biology_0057

- CSV row: 58
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
- Impact rank: 61
- Impact tier: `tier_2_high`
- Impact score: 130
- Split: `dev`
- Impact reasons: priority=both_wrong_single_edit; dev50_tuning_slice; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_v4_wrong; 1_suggested_replacements

Bangla:

```text
গনি সাহেব তার বাগানে এমন কিছু গাছ লাগিয়েছেন যার CO_{2} বিজারণের প্রথম স্থায়ী পদার্থ অক্সালো এসিটিক এসিড। গনি সাহেব লাগিয়েছেন- i. ভুট্টা ii. বেগুন iii. আখ নিচের কোনটি সঠিক?
A. i ও ii
B. ii ও iii
C. i ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

English:

```text
Mr. Goni planted some trees in his garden in which the first stable sustance of CO_2 reduction path way is Oxaloacetic acid. Mr. Goni planted- i. maize ii. brinjal iii. sugarcane Which one is correct?
A. i and ii
B. ii and iii
C. i and iii
D. i, ii and iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
goni saheb tar bagane emon kichhu gachh lagiyechhen jar CO_{2} bijaroner prothom sthayi podarth oksalo esitik esid. goni saheb lagiyechhen- i. bhutta ii. begun iii. akh nicher konoti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
goni saheb tar bagane emon kichhu gachh lagiyechhen jar CO_{2} bijaroner prothom sthayi podarth oksalo esitik esid. goni saheb lagiyechhen- i. bhutta ii. begun iii. akh nicher konti sothik?
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

## 62. banglamath_0188

- CSV row: 24
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); kot->koto (1)
- Impact rank: 62
- Impact tier: `tier_2_high`
- Impact score: 128
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen3_v4_wrong; 2_suggested_replacements

Bangla:

```text
২৫ জন লোক দৈনিক ৬ ঘণ্টা পরিশ্রম করে একটি কাজ ৮ দিনে শেষ করে। ১০ জন লোক দৈনিক কত ঘণ্টা পরিশ্রম করে ঐ কাজটি শেষ করবে
Return only the final answer.
```

English:

```text
25 people working 6 hours a day complete a job in 8 days. How many hours per day must 10 people work to complete the same job?
Return only the final answer.
```

Current Banglish:

```text
25 jon lok doinik 6 ghonta porishrom kore ekoti kaj 8 dine shesh kore. 10 jon lok doinik kot ghonta porishrom kore oi kajoti shesh korobe
Return only the final answer.
```

Auto-suggested Banglish:

```text
25 jon lok doinik 6 ghonta porishrom kore ekti kaj 8 dine shesh kore. 10 jon lok doinik koto ghonta porishrom kore oi kajoti shesh korobe
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 63. banglamath_0233

- CSV row: 27
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); kot->koto (1)
- Impact rank: 63
- Impact tier: `tier_2_high`
- Impact score: 128
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen3_v4_wrong; 2_suggested_replacements

Bangla:

```text
৬ জন লোক একটি কাজ ২৮ দিনে করলে ২৪ জন লোক কত দিনে করবে
Return only the final answer.
```

English:

```text
If 6 people complete a task in 28 days, how many days will 24 people take?
Return only the final answer.
```

Current Banglish:

```text
6 jon lok ekoti kaj 28 dine korole 24 jon lok kot dine korobe
Return only the final answer.
```

Auto-suggested Banglish:

```text
6 jon lok ekti kaj 28 dine korole 24 jon lok koto dine korobe
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 64. banglamath_0557

- CSV row: 31
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); kot->koto (1)
- Impact rank: 64
- Impact tier: `tier_2_high`
- Impact score: 128
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen3_v4_wrong; 2_suggested_replacements

Bangla:

```text
একটি বাগানের পরিসীমা ১২০ মিটার হলে চারদিকে বেড়া দিতে কত খরচ হবে যদি প্রতি মিটারে খরচ ৩১/৪ টাকা হয়
Return only the final answer.
```

English:

```text
If the perimeter of a garden is 120 meters and fencing costs 3¼ Taka per meter, what is the total fencing cost?
Return only the final answer.
```

Current Banglish:

```text
ekoti baganer porisima 120 mitar hole charodike bera dite kot khoroch hobe jodi proti mitare khoroch 31/4 taka hoy
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti baganer porisima 120 mitar hole charodike bera dite koto khoroch hobe jodi proti mitare khoroch 31/4 taka hoy
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 65. banglamath_1692

- CSV row: 32
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); kot->koto (1)
- Impact rank: 65
- Impact tier: `tier_2_high`
- Impact score: 128
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen3_v4_wrong; 2_suggested_replacements

Bangla:

```text
একটি যৌথ পরিবারের মোট সদস্য (পুরুষ, মহিলা ও শিশু) ২০ জন। পরিবারের কর্তাবাবুর আদেশ ২০ মণ ধান পরিবারের সকল সদস্যের মধ্যে ভাগ করে দেয়া হবে। ভাগের নিয়ম হলঃ প্রত্যেক পুরুষ পাবে ৩ মণ, প্রত্যেক মহিলা পাবে ২ মণ, এবং প্রত্যেক শিশু পাবে ১ মণ ধান। প্রশ্ন হচ্ছে, কতজন করে ধান পাবে? অর্থাৎ পরিবারটির পুরুষ, মহিলাদের ও শিশুদের সংখ্যা কত?
Return only the final answer.
```

English:

```text
A joint family has 20 members (men, women, and children). 20 mon of rice is to be divided where each man gets 3 mon, each woman 2 mon, and each child 1 mon. How many men, women, and children are there?
Return only the final answer.
```

Current Banglish:

```text
ekoti jouth poribarer mot sodosy (purush, mohila o shishu) 20 jon. poribarer kortababur adesh 20 mon dhan poribarer sokol sodosyer modhye bhag kore deya hobe. bhager niyom holoh protyek purush pabe 3 mon, protyek mohila pabe 2 mon, ebong protyek shishu pabe 1 mon dhan. proshn hochchhe, kotojon kore dhan pabe? orthat poribarotir purush, mohilader o shishuder songkhya kot?
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti jouth poribarer mot sodosy (purush, mohila o shishu) 20 jon. poribarer kortababur adesh 20 mon dhan poribarer sokol sodosyer modhye bhag kore deya hobe. bhager niyom holoh protyek purush pabe 3 mon, protyek mohila pabe 2 mon, ebong protyek shishu pabe 1 mon dhan. proshn hochchhe, kotojon kore dhan pabe? orthat poribarotir purush, mohilader o shishuder songkhya koto?
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 66. banglamath_0522

- CSV row: 11
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 4
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: choora->chowra (1); kot->koto (1); kshetrofol->khetrofol (1); thakole->thakle (1)
- Impact rank: 66
- Impact tier: `tier_2_high`
- Impact score: 128
- Split: `dev`
- Impact reasons: priority=both_wrong_multi_edit; dev50_tuning_slice; qwen25_v4_wrong; qwen3_v4_wrong; 4_suggested_replacements; ksh_heavy

Bangla:

```text
জমির ভিতরে ২ মিটার চওড়া রাস্তা থাকলে রাস্তাবাদে জমির ক্ষেত্রফল কত
Return only the final answer.
```

English:

```text
If there is a 2-meter-wide path inside the land, what is the area of the land including the path?
Return only the final answer.
```

Current Banglish:

```text
jomir bhitore 2 mitar choora rasta thakole rastabade jomir kshetrofol kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
jomir bhitore 2 mitar chowra rasta thakle rastabade jomir khetrofol koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 67. benqa_10th-Biology_0277

- CSV row: 63
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
- Impact rank: 67
- Impact tier: `tier_2_high`
- Impact score: 126
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen3_v4_wrong; 1_suggested_replacements

Bangla:

```text
মতিন তামাক পাতায় এক ধরনের মোজাইক রোগ দেখতে পেল। উল্লিখিত রোগের ভাইরাসের বংশগতীয় বস্তুতে বন্ধন বিদ্যমান- i. A = T ii. G = C iii. A = U নিচের কোনটি সঠিক?
A. i ও ii
B. i ও iii
C. ii ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

English:

```text
Motin found a bind of mosaic disease on tobacco leaves. Which bond is present in the heredity component of virus given in the stem? i. A = T ii. G = C iii. A = U Which one is correct?
A. i and ii
B. i and iii
C. ii and iii
D. i, ii and iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
motin tamak patay ek dhoroner mojaik rog dekhote pel. ullikhit roger bhairaser bongshogotiy bostute bondhon bidyoman- i. A = T ii. G = C iii. A = U nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
motin tamak patay ek dhoroner mojaik rog dekhote pel. ullikhit roger bhairaser bongshogotiy bostute bondhon bidyoman- i. A = T ii. G = C iii. A = U nicher konti sothik?
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

## 68. benqa_10th-Math-II_0139

- CSV row: 68
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
- Impact rank: 68
- Impact tier: `tier_2_high`
- Impact score: 126
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen3_v4_wrong; 1_suggested_replacements

Bangla:

```text
\frac{1}{2},\frac{1}{10},\frac{1}{30}, ..... অনুক্রমটির 10 তম পদ কত?
A. \frac{1}{1010}
B. \frac{1}{1100}
C. \frac{1}{11000}
D. \frac{1}{10010}
Answer with only A, B, C, or D.
```

English:

```text
\frac{1}{2},\frac{1}{10},\frac{1}{30}\cdots What is the 10^{th} term of the sequence?
A. \frac{1}{1010}
B. \frac{1}{1100}
C. \frac{1}{11000}
D. \frac{1}{10010}
Answer with only A, B, C, or D.
```

Current Banglish:

```text
\frac{1}{2},\frac{1}{10},\frac{1}{30}, ..... onukromotir 10 tom pod kot?
A. \frac{1}{1010}
B. \frac{1}{1100}
C. \frac{1}{11000}
D. \frac{1}{10010}
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
\frac{1}{2},\frac{1}{10},\frac{1}{30}, ..... onukromotir 10 tom pod koto?
A. \frac{1}{1010}
B. \frac{1}{1100}
C. \frac{1}{11000}
D. \frac{1}{10010}
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 69. benqa_12th-Biology-II_0321

- CSV row: 75
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
- Impact rank: 69
- Impact tier: `tier_2_high`
- Impact score: 126
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen3_v4_wrong; 1_suggested_replacements

Bangla:

```text
প্রাণিজগতের দ্বিতীয় বৃহত্তম পর্ব কোনটি?
A. Cnidaria
B. Annelida
C. Mollusca
D. Athropoda
Answer with only A, B, C, or D.
```

English:

```text
Which is the second largest phylum of amimal kingdom?
A. Cnidaria
B. Annelida
C. Mollusca
D. Arthropoda
Answer with only A, B, C, or D.
```

Current Banglish:

```text
pranijogoter dwitiy brihottom porb konoti?
A. Cnidaria
B. Annelida
C. Mollusca
D. Athropoda
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
pranijogoter dwitiy brihottom porb konti?
A. Cnidaria
B. Annelida
C. Mollusca
D. Athropoda
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 70. benqa_12th-Chemistry-II_0067

- CSV row: 78
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
- Impact rank: 70
- Impact tier: `tier_2_high`
- Impact score: 126
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen3_v4_wrong; 1_suggested_replacements

Bangla:

```text
32g O_{2} এর অর্থ হলো- i. 1 mole O_{2} ii. প্রমাণ অবস্থায় 24.8L আয়তন iii. অ্যাডোগেড্রোর সংখ্যার সমাণ অণু নিচের কোনটি সঠিক?
A. i
B. i ও ii
C. i ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

English:

```text
32g O_{2} means- i. 1 mole O_{2} ii. 24.8L volume in STP iii. equal to Avogadro's number of molecule Which one is correct?
A. i
B. i and ii
C. i and iii
D. i, ii and iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
32g O_{2} er orth holo- i. 1 mole O_{2} ii. proman obosthay 24.8L ayoton iii. adogedror songkhyar soman onu nicher konoti sothik?
A. i
B. i o ii
C. i o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
32g O_{2} er orth holo- i. 1 mole O_{2} ii. proman obosthay 24.8L ayoton iii. adogedror songkhyar soman onu nicher konti sothik?
A. i
B. i o ii
C. i o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 71. benqa_12th-Chemistry-I_0286

- CSV row: 83
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
- Impact rank: 71
- Impact tier: `tier_2_high`
- Impact score: 126
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen3_v4_wrong; 1_suggested_replacements

Bangla:

```text
উর্বর মাটির জন্য অত্যানুকূল pH কত?
A. 3.0-4
B. 6-May
C. 8-Jul
D. 11-Oct
Answer with only A, B, C, or D.
```

English:

```text
What is the optimum oH of fertile soil?
A. 3.0-4
B. 6-May
C. 8-Jul
D. 11-Oct
Answer with only A, B, C, or D.
```

Current Banglish:

```text
urbor matir jony otyanukul pH kot?
A. 3.0-4
B. 6-May
C. 8-Jul
D. 11-Oct
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
urbor matir jony otyanukul pH koto?
A. 3.0-4
B. 6-May
C. 8-Jul
D. 11-Oct
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 72. benqa_12th-Math-I_0187

- CSV row: 85
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
- Impact rank: 72
- Impact tier: `tier_2_high`
- Impact score: 126
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen3_v4_wrong; 1_suggested_replacements

Bangla:

```text
2x - ky + 1 = 0 ও 3x + 2y - 6 = 0 দুইটি সরলরেখার সমীকরণ। দ্বিতীয় রেখাটির লম্ব রেখার ঢাল কত?
A. \frac{3}{2}
B. \frac{2}{3}
C. - \frac{2}{3}
D. - \frac{3}{2}
Answer with only A, B, C, or D.
```

English:

```text
2x - ky + 1 = 0 and 3x + 2y - 6 = 0 are equation of two straight lines. What is the slope of perpendicular of second straight line?
A. \frac{3}{2}
B. \frac{2}{3}
C. - \frac{2}{3}
D. - \frac{3}{2}
Answer with only A, B, C, or D.
```

Current Banglish:

```text
2x - ky + 1 = 0 o 3x + 2y - 6 = 0 duiti sorolorekhar somikoron. dwitiy rekhatir lomb rekhar dhal kot?
A. \frac{3}{2}
B. \frac{2}{3}
C. - \frac{2}{3}
D. - \frac{3}{2}
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
2x - ky + 1 = 0 o 3x + 2y - 6 = 0 duiti sorolorekhar somikoron. dwitiy rekhatir lomb rekhar dhal koto?
A. \frac{3}{2}
B. \frac{2}{3}
C. - \frac{2}{3}
D. - \frac{3}{2}
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 73. benqa_12th-Physics-II_0213

- CSV row: 89
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_single_edit`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1)
- Impact rank: 73
- Impact tier: `tier_2_high`
- Impact score: 126
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen3_v4_wrong; 1_suggested_replacements

Bangla:

```text
রুদ্ধতাপীয় প্রক্রিয়ায় একটি আদর্শ গ্যাসের চাপ ও তাপমাত্রার মধ্যে সম্পর্ক-
A. P^{\gamma - 1} = ধ্রুবক
B. P^{\gamma} T^{\gama + 1} = ধ্রুবক
C. P^{\gamma} T^{\gamma - 1} = ধ্রুবক
D. P^{1 - \gamma} T^{\gamma} = ধ্রুবক
Answer with only A, B, C, or D.
```

English:

```text
The relationship between the pressure and temperature of an ideal gas in adiabatic process-
A. P^{\gamma - 1} = constant
B. P^{\gamma} T^{\gama + 1} = constant
C. P^{\gamma} T^{\gamma - 1} = constant
D. P^{1 - \gamma} T^{\gamma} = constant
Answer with only A, B, C, or D.
```

Current Banglish:

```text
ruddhotapiy prokriyay ekoti adorsh gyaser chap o tapomatrar modhye sompork-
A. P^{\gamma - 1} = dhrubok
B. P^{\gamma} T^{\gama + 1} = dhrubok
C. P^{\gamma} T^{\gamma - 1} = dhrubok
D. P^{1 - \gamma} T^{\gamma} = dhrubok
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
ruddhotapiy prokriyay ekti adorsh gyaser chap o tapomatrar modhye sompork-
A. P^{\gamma - 1} = dhrubok
B. P^{\gamma} T^{\gama + 1} = dhrubok
C. P^{\gamma} T^{\gamma - 1} = dhrubok
D. P^{1 - \gamma} T^{\gamma} = dhrubok
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 74. benqa_12th-Physics-I_0253

- CSV row: 91
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
- Impact rank: 74
- Impact tier: `tier_2_high`
- Impact score: 126
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen3_v4_wrong; 1_suggested_replacements

Bangla:

```text
মহাকর্ষ সূত্র ব্যবহার করে যে সমস্ত কাজ করা সম্ভব- i. প্রাকৃতিক গ্যাস উত্তোলন ii. বিভিন্ন খনিজ পদার্থ উত্তোলন iii. ভূ-গর্ভস্থ তাপঘটিত শক্তি উত্তোলন নিচের কোনটি সঠিক?
A. i ও ii
B. i ও iii
C. ii ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

English:

```text
Which types of work done by the help ot the gravitational law? i. Natural gas extraction ii. Extraction of various minerals iii. Extraction of energy gernerated by underground heat Which one is correct?
A. i & ii
B. i & iii
C. ii & iii
D. i, ii & iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
mohakorsh sutr byobohar kore je somost kaj kora sombhob- i. prakritik gyas uttolon ii. bibhinn khonij podarth uttolon iii. bhu-gorbhosth tapoghotit shokti uttolon nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
mohakorsh sutr byobohar kore je somost kaj kora sombhob- i. prakritik gyas uttolon ii. bibhinn khonij podarth uttolon iii. bhu-gorbhosth tapoghotit shokti uttolon nicher konti sothik?
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

## 75. banglamath_0518

- CSV row: 7
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 5
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ayotakar->ayotokar (1); doirghy->doirgho (2); ekoti->ekti (1); kot->koto (1)
- Impact rank: 75
- Impact tier: `tier_2_high`
- Impact score: 126
- Split: `dev`
- Impact reasons: priority=both_wrong_multi_edit; dev50_tuning_slice; qwen25_v4_wrong; qwen3_v4_wrong; 5_suggested_replacements

Bangla:

```text
একটি আয়তাকার বাগানের দৈর্ঘ্য প্রস্থের তিনগুণ এবং পরিসীমা ৪০০ মিটার হলে বাগানের দৈর্ঘ্য কত
Return only the final answer.
```

English:

```text
In a rectangular garden, the length is three times the width and the perimeter is 400 meters. What is the length?
Return only the final answer.
```

Current Banglish:

```text
ekoti ayotakar baganer doirghy prosther tinogun ebong porisima 400 mitar hole baganer doirghy kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti ayotokar baganer doirgho prosther tinogun ebong porisima 400 mitar hole baganer doirgho koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 76. banglamath_0539

- CSV row: 20
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
- Impact rank: 76
- Impact tier: `tier_2_high`
- Impact score: 126
- Split: `dev`
- Impact reasons: priority=both_wrong_multi_edit; dev50_tuning_slice; qwen25_v4_wrong; qwen3_v4_wrong; 3_suggested_replacements; ksh_heavy

Bangla:

```text
একটি ঘরের মেঝে কার্পেট দিয়ে মুড়তে প্রতি বর্গমিটারে ৭.৫০ টাকা দরে ১১০২.৫০ টাকা খরচ হলে ঘরের ক্ষেত্রফল কত
Return only the final answer.
```

English:

```text
If carpeting a floor costs 7.50 Taka per sq. meter and the total cost is 1102.50 Taka, what is the area of the floor?
Return only the final answer.
```

Current Banglish:

```text
ekoti ghorer mejhe karpet diye murote proti borgomitare 7.50 taka dore 1102.50 taka khoroch hole ghorer kshetrofol kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti ghorer mejhe karpet diye murote proti borgomitare 7.50 taka dore 1102.50 taka khoroch hole ghorer khetrofol koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 77. banglamath_1703

- CSV row: 57
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_single_edit`
- Replacement count: 1
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1)
- Impact rank: 77
- Impact tier: `tier_2_high`
- Impact score: 125
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; qwen25_v4_wrong; qwen3_v4_wrong; 1_suggested_replacements; ksh_heavy

Bangla:

```text
একটি ঝুরিতে ধারণক্ষমতা ১২০টি আনারস অথবা ১৪৪টি আমের । ঝুড়িতে ৯০টি আনারস রাখার পর আর কতটি আম রাখা যাবে?
Return only the final answer.
```

English:

```text
A basket can hold 120 pineapples or 144 mangoes. If 90 pineapples are stored, how many mangoes can still be added?
Return only the final answer.
```

Current Banglish:

```text
ekoti jhurite dharonokshomota 120ti anaros othoba 144ti amer . jhurite 90ti anaros rakhar por ar kototi am rakha jabe?
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti jhurite dharonokshomota 120ti anaros othoba 144ti amer . jhurite 90ti anaros rakhar por ar kototi am rakha jabe?
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 78. banglamath_0521

- CSV row: 10
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 4
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); prosth->prostho (1)
- Impact rank: 78
- Impact tier: `tier_2_high`
- Impact score: 124
- Split: `dev`
- Impact reasons: priority=both_wrong_multi_edit; dev50_tuning_slice; qwen25_v4_wrong; qwen3_v4_wrong; 4_suggested_replacements

Bangla:

```text
একটি জমির দৈর্ঘ্য ২০ মিটার ও প্রস্থ ১৫ মিটার হলে তার পরিসীমা কত
Return only the final answer.
```

English:

```text
If a plot is 20 meters long and 15 meters wide, what is its perimeter?
Return only the final answer.
```

Current Banglish:

```text
ekoti jomir doirghy 20 mitar o prosth 15 mitar hole tar porisima kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti jomir doirgho 20 mitar o prostho 15 mitar hole tar porisima koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 79. banglamath_1694

- CSV row: 33
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (2)
- Impact rank: 79
- Impact tier: `tier_2_high`
- Impact score: 124
- Split: `dev`
- Impact reasons: priority=both_wrong_multi_edit; dev50_tuning_slice; qwen25_v4_wrong; qwen3_v4_wrong; 2_suggested_replacements; ksh_heavy

Bangla:

```text
একটি ৫০০ মিটার লম্বা ট্রেনের গতি ৬০ কিলোমিটার হলে ,অর্ধকিলোমীটার লম্বা একটি সেতু পাড়ি দিতে ট্রেনটির কতক্ষণ সময় লাগবে?
Return only the final answer.
```

English:

```text
A train 500 meters long moves at 60 km/h. How long will it take to cross a bridge 500 meters long?
Return only the final answer.
```

Current Banglish:

```text
ekoti 500 mitar lomba trener goti 60 kilomitar hole ,ordhokilomitar lomba ekoti setu pari dite trenotir kotokshon somoy lagobe?
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti 500 mitar lomba trener goti 60 kilomitar hole ,ordhokilomitar lomba ekti setu pari dite trenotir kotokshon somoy lagobe?
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 80. banglamath_0187

- CSV row: 18
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
- Impact rank: 80
- Impact tier: `tier_2_high`
- Impact score: 122
- Split: `dev`
- Impact reasons: priority=both_wrong_multi_edit; dev50_tuning_slice; qwen25_v4_wrong; qwen3_v4_wrong; 3_suggested_replacements

Bangla:

```text
একটি বাঁধ তৈরি করতে ৩৬০ জন শ্রমিকের ২৫ দিন লাগে। ১৮ দিনে কাজটি শেষ করতে কতজন অতিরিক্ত শ্রমিক লাগবে
Return only the final answer.
```

English:

```text
To build a dam, 360 workers are needed for 25 days. How many extra workers are needed to finish it in 18 days?
Return only the final answer.
```

Current Banglish:

```text
ekoti bandh toiri korote 360 jon shromiker 25 din lage. 18 dine kajoti shesh korote kotojon otirikt shromik lagobe
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti bandh toiri korte 360 jon shromiker 25 din lage. 18 dine kajoti shesh korte kotojon otirikt shromik lagobe
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank
