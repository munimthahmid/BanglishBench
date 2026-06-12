# Validation-200 v5 Review Packet 01

Source queue: `data/slices/validation_200_v5_review_queue.csv`
Batch: 1/7
Rows in batch: 20

Fill the source CSV, not this Markdown packet. Use this packet only for
source/context reading while editing `reviewed_banglish`,
`quality_label`, and `review_notes` in the queue.

Allowed labels: `ok`, `minor_edit`, `major_edit`, `bad`.

## 1. benqa_10th-Math_0044

- CSV row: 34
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: achhe->ache (1); ekoti->ekti (1)
- Impact rank: 1
- Impact tier: `tier_1_review_first`
- Impact score: 177
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen25_agreement_route_gain; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 2_suggested_replacements

Bangla:

```text
একটি বর্গের কতটি প্রতিসাম্য রেখা আছে?
A. 8টি
B. 6টি
C. 4টি
D. 2টি
Answer with only A, B, C, or D.
```

English:

```text
How many lines of symmetry does a square have?
A. 8
B. 6
C. 4
D. 2
Answer with only A, B, C, or D.
```

Current Banglish:

```text
ekoti borger kototi protisamy rekha achhe?
A. 8ti
B. 6ti
C. 4ti
D. 2ti
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
ekti borger kototi protisamy rekha ache?
A. 8ti
B. 6ti
C. 4ti
D. 2ti
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 2. benqa_12th-Chemistry-II_0228

- CSV row: 37
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); konoti->konti (1)
- Impact rank: 2
- Impact tier: `tier_1_review_first`
- Impact score: 177
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen25_agreement_route_gain; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 2_suggested_replacements

Bangla:

```text
Ni(s) + 2Ag^{+}(aq) \xrightarrow{2e^{-}} Ni^{2+}(aq) + 2Ag(s); বিক্রিয়াটিতে- i. Ni জারিত হয় ii. Ag জারিত হয় iii. বিক্রিয়াটি একটি রিডক্স বিক্রিয়া নিচের কোনটি সঠিক?
A. i ও ii
B. ii ও iii
C. i ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

English:

```text
Ni(s) + 2Ag^{+}(aq) \overset{2e^{-}} {\rightarrow}Ni^{2+}(aq) + 2Ag(s); in this reaction- i. Ni becomes oxidized ii. Ag becomes oxidized iii. A redox reaction Which one is correct?
A. i and ii
B. ii and iii
C. i and iii
D. i, ii and iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
Ni(s) + 2Ag^{+}(aq) \xrightarrow{2e^{-}} Ni^{2+}(aq) + 2Ag(s); bikriyatite- i. Ni jarit hoy ii. Ag jarit hoy iii. bikriyati ekoti ridoks bikriya nicher konoti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
Ni(s) + 2Ag^{+}(aq) \xrightarrow{2e^{-}} Ni^{2+}(aq) + 2Ag(s); bikriyatite- i. Ni jarit hoy ii. Ag jarit hoy iii. bikriyati ekti ridoks bikriya nicher konti sothik?
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

## 3. benqa_8th-Math_0167

- CSV row: 9
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_multi_edit`
- Replacement count: 5
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ayotakar->ayotokar (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); prosth->prostho (1)
- Impact rank: 3
- Impact tier: `tier_1_review_first`
- Impact score: 173
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen25_agreement_route_gain; qwen3_v4_wrong; qwen3_recoverable_by_other_script; 5_suggested_replacements

Bangla:

```text
একটি আয়তাকার বাগানের দৈর্ঘ্য প্রস্থের দেড়গুণ। এর প্রস্থ 16 মিটার হলে, বাগানের পরিসীমা কত?
A. 40 মিটার
B. 64 মিটার
C. 80 মিটার
D. 96 মিটার
Answer with only A, B, C, or D.
```

English:

```text
The length of a rectangular garden is one and half times its breadth. If breadth is 16 metres , what is its peremeter?
A. 40m
B. 64m
C. 80m
D. 96m
Answer with only A, B, C, or D.
```

Current Banglish:

```text
ekoti ayotakar baganer doirghy prosther derogun. er prosth 16 mitar hole, baganer porisima kot?
A. 40 mitar
B. 64 mitar
C. 80 mitar
D. 96 mitar
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
ekti ayotokar baganer doirgho prosther derogun. er prostho 16 mitar hole, baganer porisima koto?
A. 40 mitar
B. 64 mitar
C. 80 mitar
D. 96 mitar
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 4. benqa_12th-Physics-II_0046

- CSV row: 38
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
- Impact rank: 4
- Impact tier: `tier_1_review_first`
- Impact score: 171
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen25_agreement_route_gain; qwen3_v4_wrong; qwen3_recoverable_by_other_script; 2_suggested_replacements; ksh_heavy

Bangla:

```text
রুদ্ধতাপীয় পরিবর্তনের ক্ষেত্রে- i. হঠাৎ সংঘটিত হয় ii. তাপমাত্রা স্থির থাকে iii. এনট্রপির পরিবর্তন শূন্য নিচের কোনটি সঠিক?
A. i ও ii
B. ii ও iii
C. i ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

English:

```text
For changing adiabatic process- i. occurs suddenly ii. temperature constant iii. change of entropy is zero Which one is correct?
A. i and ii
B. ii and iii
C. i and iii
D. i, ii and iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
ruddhotapiy poribortoner kshetre- i. hothat songghotit hoy ii. tapomatra sthir thake iii. enotropir poriborton shuny nicher konoti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
ruddhotapiy poribortoner khetre- i. hothat songghotit hoy ii. tapomatra sthir thake iii. enotropir poriborton shuny nicher konti sothik?
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

## 5. banglamath_0526

- CSV row: 12
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
- Impact rank: 5
- Impact tier: `tier_1_review_first`
- Impact score: 170
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen25_agreement_route_gain; qwen3_v4_wrong; qwen3_recoverable_by_other_script; 4_suggested_replacements; ksh_heavy

Bangla:

```text
একটি ত্রিভুজের ভূমি ১০ মিটার ও উচ্চতা ৬ মিটার হলে ক্ষেত্রফল কত
Return only the final answer.
```

English:

```text
If a triangle has a base of 10 meters and height of 6 meters, what is its area?
Return only the final answer.
```

Current Banglish:

```text
ekoti tribhujer bhumi 10 mitar o uchchota 6 mitar hole kshetrofol kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti tribhujer bhumi 10 mitar o ucchota 6 mitar hole khetrofol koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 6. benqa_10th-Physics_0021

- CSV row: 72
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
- Impact rank: 6
- Impact tier: `tier_1_review_first`
- Impact score: 170
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen25_agreement_route_gain; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 1_suggested_replacements

Bangla:

```text
কোনটি মৌলিক একক?
A. জুল
B. নিউটন
C. ক্যান্ডেলা
D. প্যাসকেল
Answer with only A, B, C, or D.
```

English:

```text
Which one is fundamental unit?
A. Joule
B. Newton
C. Candela
D. Pascal
Answer with only A, B, C, or D.
```

Current Banglish:

```text
konoti moulik ekok?
A. jul
B. niuton
C. kyandela
D. pyasokel
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
konti moulik ekok?
A. jul
B. niuton
C. kyandela
D. pyasokel
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 7. benqa_8th-Science_0202

- CSV row: 96
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
- Impact rank: 7
- Impact tier: `tier_1_review_first`
- Impact score: 170
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen25_agreement_route_gain; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 1_suggested_replacements

Bangla:

```text
সঠিক খাদ্য-শৃঙ্খল কোনটি?
A. ঘাস \rightarrow ফাইটোপ্ল্যাংকটন \rightarrow জুপ্লাঙ্কটন
B. জু-প্লাঙ্কটন \rightarrow ফাইটোপ্ল্যাংকটন\rightarrow ছোটমাস
C. ফাইটোপ্লাঙ্কটন \rightarrow জু-প্লাঙ্কটন \rightarrow ছোটমাছ
D. ঘাস\rightarrow ব্যাঙ\rightarrow বাঘ
Answer with only A, B, C, or D.
```

English:

```text
Which one is the correct food chain
A. Grass\rightarrow Phytoplankton\rightarrow Zooplankton
B. Zooplankot\rightarrow Phytoplankton\rightarrow Small fish
C. Phytoplankton\rightarrow Zooplankton\rightarrow Small fish
D. Grass\rightarrow Frog\rightarrow Tiger
Answer with only A, B, C, or D.
```

Current Banglish:

```text
sothik khaddo-shringkhol konoti?
A. ghas \rightarrow faitoplyangkoton \rightarrow juplangkoton
B. ju-plangkoton \rightarrow faitoplyangkoton\rightarrow chhotomas
C. faitoplangkoton \rightarrow ju-plangkoton \rightarrow chhotomachh
D. ghas\rightarrow byang\rightarrow bagh
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
sothik khaddo-shringkhol konti?
A. ghas \rightarrow faitoplyangkoton \rightarrow juplangkoton
B. ju-plangkoton \rightarrow faitoplyangkoton\rightarrow chhotomas
C. faitoplangkoton \rightarrow ju-plangkoton \rightarrow chhotomachh
D. ghas\rightarrow byang\rightarrow bagh
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 8. benqa_12th-Biology-II_0287

- CSV row: 36
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: konoti->konti (2)
- Impact rank: 8
- Impact tier: `tier_1_review_first`
- Impact score: 167
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 2_suggested_replacements

Bangla:

```text
প্রোটিন পরিপাকে অংশ নেয় কোনটি? i. পেপসিন ii. অ্যামাইলেজ iii. কার্বক্সিপেপটাইড নিচের কোনটি সঠিক?
A. i ও ii
B. i ও iii
C. ii ও iii
D. i, ii, ও iii
Answer with only A, B, C, or D.
```

English:

```text
What participate in protein digestion? i. pepsin ii.Amylase iii.Carboxypeptide Which one is correct?
A. i & ii
B. i & iii
C. ii & iii
D. I,ii & iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
protin poripake ongsh ney konoti? i. peposin ii. amailej iii. karboksipepotaid nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
protin poripake ongsh ney konti? i. peposin ii. amailej iii. karboksipepotaid nicher konti sothik?
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

## 9. benqa_12th-Biology-I_0265

- CSV row: 23
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_multi_edit`
- Replacement count: 3
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: achhe->ache (1); ekoti->ekti (1); konoti->konti (1)
- Impact rank: 9
- Impact tier: `tier_1_review_first`
- Impact score: 165
- Split: `dev`
- Impact reasons: priority=both_wrong_multi_edit; dev50_tuning_slice; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 3_suggested_replacements; ksh_heavy

Bangla:

```text
মি. 'ক' ব্যবহারিক ক্লাসে একটি নমুনার পর্যবেক্ষণ করে দেখলো মেটাজাইলেম কেন্দ্রের দিকে, ভাস্কুলার বান্ডল ৯টি এবং কিছু এককোষী রোম আছে। পর্যবেক্ষিত বৈশিষ্ট্যগুলো কীভাবে উদ্ভিদকে বাঁচিয়ে রাখতে সাহায্য করে? i. পানি ও খনিজ লবণ পরিবহন করে ii. প্রস্তুতকৃত খাবার পরিবহন করে iii. খাদ্য প্রস্তুত করে নিচের কোনটি সঠিক?
A. i ও ii
B. ii ও iii
C. i ও iii
D. i, ii, ও iii
Answer with only A, B, C, or D.
```

English:

```text
Mr. 'X' observed a transverse section of a sample and noticed that metaxylem is present towards the center, 9 (nine) vascular bundles and there are some unicellular hairs. How does the observe features help to protect the plant? i. By transporting water and mineral salts ii. By transporting prepared food iii. By preparing food Which one is correct?
A. i & ii
B. ii & iii
C. i & iii
D. i, ii & iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
mi. 'k' byoboharik klase ekoti nomunar poryobekshon kore dekholo metajailem kendrer dike, bhaskular bandol 9ti ebong kichhu ekokoshi rom achhe. poryobekshit boishishtyogulo kibhabe udbhidoke banchiye rakhote sahajy kore? i. pani o khonij lobon poribohon kore ii. prostutokrit khabar poribohon kore iii. khaddo prostut kore nicher konoti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
mi. 'k' byoboharik klase ekti nomunar poryobekshon kore dekholo metajailem kendrer dike, bhaskular bandol 9ti ebong kichhu ekokoshi rom ache. poryobekshit boishishtyogulo kibhabe udbhidoke banchiye rakhote sahajy kore? i. pani o khonij lobon poribohon kore ii. prostutokrit khabar poribohon kore iii. khaddo prostut kore nicher konti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 10. benqa_12th-Biology-I_0283

- CSV row: 77
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
- Impact rank: 10
- Impact tier: `tier_1_review_first`
- Impact score: 164
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 1_suggested_replacements; ksh_heavy

Bangla:

```text
পেঁপের রিং স্পট রোগের লক্ষণ হলো- i. পাতার বোটায় পানি ভেজা সবুজ দাগ দেখা যায় ii. পেঁপের মিষ্টতা হ্রাস পায় iii. ফলের আকার বড় হয় নিচের কোনটি সঠিক?
A. i ও ii
B. ii ও iii
C. i ও iii
D. i, ii, ও iii
Answer with only A, B, C, or D.
```

English:

```text
Symptoms of ring spot disease in papaya is- i. observance of wet green spot on the petiole of leaves ii. reduction of sweetness of papaya iii. enlarging of the size of fruit Which one is correct?
A. i & ii
B. ii & iii
C. i & iii
D. i, ii & iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
penper ring spot roger lokshon holo- i. patar botay pani bheja sobuj dag dekha jay ii. penper mishtota hras pay iii. foler akar bor hoy nicher konoti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
penper ring spot roger lokshon holo- i. patar botay pani bheja sobuj dag dekha jay ii. penper mishtota hras pay iii. foler akar bor hoy nicher konti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 11. benqa_12th-Chemistry-I_0037

- CSV row: 81
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
- Impact rank: 11
- Impact tier: `tier_1_review_first`
- Impact score: 164
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 1_suggested_replacements; ksh_heavy

Bangla:

```text
ধাতুর গলনাঙ্ক বৃদ্ধি পায়, যখন- i. ধাতব কেলাসে মুক্ত ইলেকট্রন বেশি থাকে ii. আয়নিকরণ বিভব হ্রাস পায় iii. পরমাণুর আকার ক্ষুদ্র হয় নিচের কোনটি সঠিক?
A. i ও ii
B. ii ও iii
C. i ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

English:

```text
Melting point of metal increases ,when- i.more electrons exist in metal lattice ii.ionization potential decreases iii.size of atoms become smaller Which one is correct?
A. i&ii
B. ii&iii
C. i&iii
D. i.ii,&iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
dhatur golonangk briddhi pay, jokhon- i. dhatob kelase mukt ilekotron beshi thake ii. ayonikoron bibhob hras pay iii. poromanur akar kshudr hoy nicher konoti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
dhatur golonangk briddhi pay, jokhon- i. dhatob kelase mukt ilekotron beshi thake ii. ayonikoron bibhob hras pay iii. poromanur akar kshudr hoy nicher konti sothik?
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

## 12. benqa_8th-Science_0153

- CSV row: 94
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
- Impact rank: 12
- Impact tier: `tier_1_review_first`
- Impact score: 162
- Split: `dev`
- Impact reasons: priority=both_wrong_single_edit; dev50_tuning_slice; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen25_agreement_route_gain; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 1_suggested_replacements

Bangla:

```text
পাকস্থলীর এসিডিটি নিরাময়ে কোনটি উপযোগী?
A. ক্যালসিয়াম
B. এসিটিক এসিড
C. অ্যলুমিনিয়াম হাইড্রোক্সাইড
D. অ্যামোনিয়াম হাইড্রোক্সাইড
Answer with only A, B, C, or D.
```

English:

```text
Which is appropriate to remove acidity in the stomach?
A. Calcium Hydroxide
B. Acetic Acid
C. Aluminium Hydroxide
D. Ammonium Hydroxide
Answer with only A, B, C, or D.
```

Current Banglish:

```text
pakostholir esiditi niramoye konoti upojogi?
A. kyalosiyam
B. esitik esid
C. ojoluminiyam haidroksaid
D. amoniyam haidroksaid
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
pakostholir esiditi niramoye konti upojogi?
A. kyalosiyam
B. esitik esid
C. ojoluminiyam haidroksaid
D. amoniyam haidroksaid
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 13. benqa_10th-Biology_0128

- CSV row: 60
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
- Impact rank: 13
- Impact tier: `tier_1_review_first`
- Impact score: 160
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen25_agreement_route_gain; qwen3_v4_wrong; qwen3_recoverable_by_other_script; 1_suggested_replacements

Bangla:

```text
ইস্টের শ্বসন প্রক্রিয়ায় কোনটি উৎপন্ন হয়?
A. ল্যাকটিক এসিড
B. গ্লুকোজ
C. অক্সালো অ্যাসিটিক এসিড
D. গ্লিসারিক এসিড
Answer with only A, B, C, or D.
```

English:

```text
Which one is produce by respiration of yeast?
A. Lactic acid
B. Glucose
C. Oxaloacetic acid
D. Glyceric acid
Answer with only A, B, C, or D.
```

Current Banglish:

```text
ister shboson prokriyay konoti utoponn hoy?
A. lyakotik esid
B. glukoj
C. oksalo asitik esid
D. glisarik esid
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
ister shboson prokriyay konti utoponn hoy?
A. lyakotik esid
B. glukoj
C. oksalo asitik esid
D. glisarik esid
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 14. benqa_10th-Chemistry_0132

- CSV row: 65
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
- Impact rank: 14
- Impact tier: `tier_1_review_first`
- Impact score: 160
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 1_suggested_replacements

Bangla:

```text
বিস্ফোরক পদার্থ কোনটি?
A. টি.এন.টি
B. বেনজিন
C. টলুইন
D. জাইলিন
Answer with only A, B, C, or D.
```

English:

```text
Which one is explosive substance?
A. TNT
B. Benzene
C. Toluene
D. Xylene
Answer with only A, B, C, or D.
```

Current Banglish:

```text
bisforok podarth konoti?
A. ti.en.ti
B. benojin
C. toluin
D. jailin
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
bisforok podarth konti?
A. ti.en.ti
B. benojin
C. toluin
D. jailin
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 15. benqa_12th-Chemistry-II_0235

- CSV row: 80
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
- Impact rank: 15
- Impact tier: `tier_1_review_first`
- Impact score: 160
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 1_suggested_replacements

Bangla:

```text
নিচের কোনটি লুইস এসিড?
A. AlCl_{3}
B. H_{2}CO_{3}
C. NH_{3}
D. H_{3}PO_{4}
Answer with only A, B, C, or D.
```

English:

```text
Which one of the following is the Lewis acid?
A. AlCl_{3}
B. H_{2}CO_{3}
C. NH_{3}
D. H_{3}PO_{4}
Answer with only A, B, C, or D.
```

Current Banglish:

```text
nicher konoti luis esid?
A. AlCl_{3}
B. H_{2}CO_{3}
C. NH_{3}
D. H_{3}PO_{4}
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
nicher konti luis esid?
A. AlCl_{3}
B. H_{2}CO_{3}
C. NH_{3}
D. H_{3}PO_{4}
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 16. benqa_12th-Chemistry-I_0174

- CSV row: 82
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
- Impact rank: 16
- Impact tier: `tier_1_review_first`
- Impact score: 160
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 1_suggested_replacements

Bangla:

```text
ভিনেগার- i. খাদ্যের ব্যাকটেরিয়া ধ্বংস করা ii. খাবারের রুচি বৃদ্ধি করে iii. রক্ত সঞ্চালন কমায় নিচের কোনটি সঠিক?
A. i ও ii
B. i ও iii
C. ii ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

English:

```text
Vinegar- i.destroys bacteria ii.increases the taste of meal iii.decreases blood circulation Which one is correct?
A. i&ii
B. i&iii
C. ii&iii
D. I,ii&iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
bhinegar- i. khadder byakoteriya dhbongs kora ii. khabarer ruchi briddhi kore iii. rokt sonchalon komay nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
bhinegar- i. khadder byakoteriya dhbongs kora ii. khabarer ruchi briddhi kore iii. rokt sonchalon komay nicher konti sothik?
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

## 17. banglamath_0230

- CSV row: 48
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
- Impact rank: 17
- Impact tier: `tier_1_review_first`
- Impact score: 155
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen25_agreement_route_gain; qwen3_v4_wrong; qwen3_recoverable_by_other_script; 1_suggested_replacements

Bangla:

```text
২৫ টাকা ১২৫ টাকার শতকরা কত
Return only the final answer.
```

English:

```text
25 Taka is what percent of 125 Taka?
Return only the final answer.
```

Current Banglish:

```text
25 taka 125 takar shotokora kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
25 taka 125 takar shotokora koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 18. benqa_12th-Biology-II_0034

- CSV row: 73
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
- Impact rank: 18
- Impact tier: `tier_1_review_first`
- Impact score: 154
- Split: `test`
- Impact reasons: priority=both_wrong_single_edit; heldout_test150; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_v4_wrong; qwen3_recoverable_by_other_script; 1_suggested_replacements; ksh_heavy

Bangla:

```text
ক্ষুদ্রান্ত্রের ক্ষুদ্র অংশ কোনটি?
A. পাইলোরাস
B. ডিওডেনাম
C. জেজুনাম
D. ইলিয়াম
Answer with only A, B, C, or D.
```

English:

```text
Which is the smallest part of small intestine?
A. Pylorus
B. Duodenum
C. Jejunum
D. Ileum
Answer with only A, B, C, or D.
```

Current Banglish:

```text
kshudrantrer kshudr ongsh konoti?
A. pailoras
B. diodenam
C. jejunam
D. iliyam
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
kshudrantrer kshudr ongsh konti?
A. pailoras
B. diodenam
C. jejunam
D. iliyam
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 19. banglamath_0231

- CSV row: 25
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
- Impact rank: 19
- Impact tier: `tier_1_review_first`
- Impact score: 152
- Split: `test`
- Impact reasons: priority=both_wrong_multi_edit; heldout_test150; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_v4_wrong; qwen3_recoverable_by_other_script; 2_suggested_replacements

Bangla:

```text
একটি কলম ২০% লাভে ২৪ টাকায় বিক্রয় করলে ক্রয়মূল্য কত
Return only the final answer.
```

English:

```text
If a pen is sold for 24 Taka with 20% profit, what was the cost price?
Return only the final answer.
```

Current Banglish:

```text
ekoti kolom 20% labhe 24 takay bikroy korole kroyomuly kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti kolom 20% labhe 24 takay bikroy korole kroyomuly koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 20. benqa_8th-Math_0085

- CSV row: 92
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
- Impact rank: 20
- Impact tier: `tier_1_review_first`
- Impact score: 152
- Split: `dev`
- Impact reasons: priority=both_wrong_single_edit; dev50_tuning_slice; main_benqa_gap_slice; qwen25_v4_wrong; qwen25_recoverable_by_other_script; qwen3_v4_wrong; qwen3_recoverable_by_other_script; qwen3_agreement_route_gain; 1_suggested_replacements

Bangla:

```text
4 ক্রমের ম্যাজিক বর্গের কোণাকুণি যোগফল কত?
A. 15
B. 16
C. 34
D. 65
Answer with only A, B, C, or D.
```

English:

```text
What is the sum of diagonal of magie square of order 4?
A. 15
B. 16
C. 34
D. 65
Answer with only A, B, C, or D.
```

Current Banglish:

```text
4 kromer myajik borger konakuni jogofol kot?
A. 15
B. 16
C. 34
D. 65
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
4 kromer myajik borger konakuni jogofol koto?
A. 15
B. 16
C. 34
D. 65
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank
