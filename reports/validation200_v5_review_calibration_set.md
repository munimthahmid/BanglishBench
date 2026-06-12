# Validation-200 v5 Review Calibration Set

Updated: 2026-05-28

Use this packet before reviewing the full 140-row v5 queue. The goal is
to establish a consistent editing style for repeated Banglish patterns,
not to auto-accept the suggested edits.

Authoritative worksheet:
`data/slices/validation_200_v5_review_queue.csv`.

## Calibration Procedure

1. Read each item's Bangla, English, current Banglish, and auto-suggested
   Banglish.
2. Decide whether the current Banglish is acceptable.
3. If editing, write the full replacement prompt, not only the changed word.
4. After the calibration set, apply the same style to the impact-ordered
   packets.

## Selected Items

### benqa_10th-Math_0044

- Calibration reason: top impact tier-1 row
- CSV line: 34
- Impact rank/tier: 1 / tier_1_review_first
- Split: test
- Dataset/task: benqa / mcq
- Answer: C
- Priority: both_wrong_multi_edit
- Suggestions: achhe->ache (1); ekoti->ekti (1)

**Bangla**

একটি বর্গের কতটি প্রতিসাম্য রেখা আছে? A. 8টি B. 6টি C. 4টি D. 2টি Answer with only A, B, C, or D.

**English**

How many lines of symmetry does a square have? A. 8 B. 6 C. 4 D. 2 Answer with only A, B, C, or D.

**Current Banglish**

ekoti borger kototi protisamy rekha achhe? A. 8ti B. 6ti C. 4ti D. 2ti Answer with only A, B, C, or D.

**Auto-Suggested Banglish**

ekti borger kototi protisamy rekha ache? A. 8ti B. 6ti C. 4ti D. 2ti Answer with only A, B, C, or D.

Review fields to fill in the CSV:

- `quality_label`: `ok`, `minor_edit`, `major_edit`, or `bad`
- `reviewed_banglish`: blank for `ok`/`bad`; full replacement for edits
- `review_notes`: short reason when useful

### benqa_12th-Chemistry-II_0228

- Calibration reason: top impact tier-1 row
- CSV line: 37
- Impact rank/tier: 2 / tier_1_review_first
- Split: test
- Dataset/task: benqa / mcq
- Answer: C
- Priority: both_wrong_multi_edit
- Suggestions: ekoti->ekti (1); konoti->konti (1)

**Bangla**

Ni(s) + 2Ag^{+}(aq) \xrightarrow{2e^{-}} Ni^{2+}(aq) + 2Ag(s); বিক্রিয়াটিতে- i. Ni জারিত হয় ii. Ag জারিত হয় iii. বিক্রিয়াটি একটি রিডক্স বিক্রিয়া নিচের কোনটি সঠিক? A. i ও ii B. ii ও iii C. i ও iii D. i, ii ও iii Answer...

**English**

Ni(s) + 2Ag^{+}(aq) \overset{2e^{-}} {\rightarrow}Ni^{2+}(aq) + 2Ag(s); in this reaction- i. Ni becomes oxidized ii. Ag becomes oxidized iii. A redox reaction Which one is correct? A. i and ii B. ii and iii C. i and i...

**Current Banglish**

Ni(s) + 2Ag^{+}(aq) \xrightarrow{2e^{-}} Ni^{2+}(aq) + 2Ag(s); bikriyatite- i. Ni jarit hoy ii. Ag jarit hoy iii. bikriyati ekoti ridoks bikriya nicher konoti sothik? A. i o ii B. ii o iii C. i o iii D. i, ii o iii An...

**Auto-Suggested Banglish**

Ni(s) + 2Ag^{+}(aq) \xrightarrow{2e^{-}} Ni^{2+}(aq) + 2Ag(s); bikriyatite- i. Ni jarit hoy ii. Ag jarit hoy iii. bikriyati ekti ridoks bikriya nicher konti sothik? A. i o ii B. ii o iii C. i o iii D. i, ii o iii Answ...

Review fields to fill in the CSV:

- `quality_label`: `ok`, `minor_edit`, `major_edit`, or `bad`
- `reviewed_banglish`: blank for `ok`/`bad`; full replacement for edits
- `review_notes`: short reason when useful

### benqa_8th-Math_0167

- Calibration reason: top impact tier-1 row
- CSV line: 9
- Impact rank/tier: 3 / tier_1_review_first
- Split: test
- Dataset/task: benqa / mcq
- Answer: C
- Priority: both_wrong_multi_edit
- Suggestions: ayotakar->ayotokar (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); prosth->prostho (1)

**Bangla**

একটি আয়তাকার বাগানের দৈর্ঘ্য প্রস্থের দেড়গুণ। এর প্রস্থ 16 মিটার হলে, বাগানের পরিসীমা কত? A. 40 মিটার B. 64 মিটার C. 80 মিটার D. 96 মিটার Answer with only A, B, C, or D.

**English**

The length of a rectangular garden is one and half times its breadth. If breadth is 16 metres , what is its peremeter? A. 40m B. 64m C. 80m D. 96m Answer with only A, B, C, or D.

**Current Banglish**

ekoti ayotakar baganer doirghy prosther derogun. er prosth 16 mitar hole, baganer porisima kot? A. 40 mitar B. 64 mitar C. 80 mitar D. 96 mitar Answer with only A, B, C, or D.

**Auto-Suggested Banglish**

ekti ayotokar baganer doirgho prosther derogun. er prostho 16 mitar hole, baganer porisima koto? A. 40 mitar B. 64 mitar C. 80 mitar D. 96 mitar Answer with only A, B, C, or D.

Review fields to fill in the CSV:

- `quality_label`: `ok`, `minor_edit`, `major_edit`, or `bad`
- `reviewed_banglish`: blank for `ok`/`bad`; full replacement for edits
- `review_notes`: short reason when useful

### benqa_12th-Physics-II_0046

- Calibration reason: top impact tier-1 row
- CSV line: 38
- Impact rank/tier: 4 / tier_1_review_first
- Split: test
- Dataset/task: benqa / mcq
- Answer: C
- Priority: both_wrong_multi_edit
- Suggestions: konoti->konti (1); kshetre->khetre (1)

**Bangla**

রুদ্ধতাপীয় পরিবর্তনের ক্ষেত্রে- i. হঠাৎ সংঘটিত হয় ii. তাপমাত্রা স্থির থাকে iii. এনট্রপির পরিবর্তন শূন্য নিচের কোনটি সঠিক? A. i ও ii B. ii ও iii C. i ও iii D. i, ii ও iii Answer with only A, B, C, or D.

**English**

For changing adiabatic process- i. occurs suddenly ii. temperature constant iii. change of entropy is zero Which one is correct? A. i and ii B. ii and iii C. i and iii D. i, ii and iii Answer with only A, B, C, or D.

**Current Banglish**

ruddhotapiy poribortoner kshetre- i. hothat songghotit hoy ii. tapomatra sthir thake iii. enotropir poriborton shuny nicher konoti sothik? A. i o ii B. ii o iii C. i o iii D. i, ii o iii Answer with only A, B, C, or D.

**Auto-Suggested Banglish**

ruddhotapiy poribortoner khetre- i. hothat songghotit hoy ii. tapomatra sthir thake iii. enotropir poriborton shuny nicher konti sothik? A. i o ii B. ii o iii C. i o iii D. i, ii o iii Answer with only A, B, C, or D.

Review fields to fill in the CSV:

- `quality_label`: `ok`, `minor_edit`, `major_edit`, or `bad`
- `reviewed_banglish`: blank for `ok`/`bad`; full replacement for edits
- `review_notes`: short reason when useful

### banglamath_0526

- Calibration reason: top impact tier-1 row
- CSV line: 12
- Impact rank/tier: 5 / tier_1_review_first
- Split: test
- Dataset/task: banglamath / short_answer
- Answer: ৩০ বর্গ মিটার
- Priority: both_wrong_multi_edit
- Suggestions: ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); uchchota->ucchota (1)

**Bangla**

একটি ত্রিভুজের ভূমি ১০ মিটার ও উচ্চতা ৬ মিটার হলে ক্ষেত্রফল কত Return only the final answer.

**English**

If a triangle has a base of 10 meters and height of 6 meters, what is its area? Return only the final answer.

**Current Banglish**

ekoti tribhujer bhumi 10 mitar o uchchota 6 mitar hole kshetrofol kot Return only the final answer.

**Auto-Suggested Banglish**

ekti tribhujer bhumi 10 mitar o ucchota 6 mitar hole khetrofol koto Return only the final answer.

Review fields to fill in the CSV:

- `quality_label`: `ok`, `minor_edit`, `major_edit`, or `bad`
- `reviewed_banglish`: blank for `ok`/`bad`; full replacement for edits
- `review_notes`: short reason when useful

### benqa_10th-Physics_0021

- Calibration reason: top impact tier-1 row
- CSV line: 72
- Impact rank/tier: 6 / tier_1_review_first
- Split: test
- Dataset/task: benqa / mcq
- Answer: C
- Priority: both_wrong_single_edit
- Suggestions: konoti->konti (1)

**Bangla**

কোনটি মৌলিক একক? A. জুল B. নিউটন C. ক্যান্ডেলা D. প্যাসকেল Answer with only A, B, C, or D.

**English**

Which one is fundamental unit? A. Joule B. Newton C. Candela D. Pascal Answer with only A, B, C, or D.

**Current Banglish**

konoti moulik ekok? A. jul B. niuton C. kyandela D. pyasokel Answer with only A, B, C, or D.

**Auto-Suggested Banglish**

konti moulik ekok? A. jul B. niuton C. kyandela D. pyasokel Answer with only A, B, C, or D.

Review fields to fill in the CSV:

- `quality_label`: `ok`, `minor_edit`, `major_edit`, or `bad`
- `reviewed_banglish`: blank for `ok`/`bad`; full replacement for edits
- `review_notes`: short reason when useful

### benqa_8th-Science_0202

- Calibration reason: calibrate `konoti -> konti`
- CSV line: 96
- Impact rank/tier: 7 / tier_1_review_first
- Split: test
- Dataset/task: benqa / mcq
- Answer: C
- Priority: both_wrong_single_edit
- Suggestions: konoti->konti (1)

**Bangla**

সঠিক খাদ্য-শৃঙ্খল কোনটি? A. ঘাস \rightarrow ফাইটোপ্ল্যাংকটন \rightarrow জুপ্লাঙ্কটন B. জু-প্লাঙ্কটন \rightarrow ফাইটোপ্ল্যাংকটন\rightarrow ছোটমাস C. ফাইটোপ্লাঙ্কটন \rightarrow জু-প্লাঙ্কটন \rightarrow ছোটমাছ D. ঘাস\ri...

**English**

Which one is the correct food chain A. Grass\rightarrow Phytoplankton\rightarrow Zooplankton B. Zooplankot\rightarrow Phytoplankton\rightarrow Small fish C. Phytoplankton\rightarrow Zooplankton\rightarrow Small fish D...

**Current Banglish**

sothik khaddo-shringkhol konoti? A. ghas \rightarrow faitoplyangkoton \rightarrow juplangkoton B. ju-plangkoton \rightarrow faitoplyangkoton\rightarrow chhotomas C. faitoplangkoton \rightarrow ju-plangkoton \rightarro...

**Auto-Suggested Banglish**

sothik khaddo-shringkhol konti? A. ghas \rightarrow faitoplyangkoton \rightarrow juplangkoton B. ju-plangkoton \rightarrow faitoplyangkoton\rightarrow chhotomas C. faitoplangkoton \rightarrow ju-plangkoton \rightarrow...

Review fields to fill in the CSV:

- `quality_label`: `ok`, `minor_edit`, `major_edit`, or `bad`
- `reviewed_banglish`: blank for `ok`/`bad`; full replacement for edits
- `review_notes`: short reason when useful

### benqa_12th-Biology-II_0287

- Calibration reason: calibrate `konoti -> konti`
- CSV line: 36
- Impact rank/tier: 8 / tier_1_review_first
- Split: test
- Dataset/task: benqa / mcq
- Answer: B
- Priority: both_wrong_multi_edit
- Suggestions: konoti->konti (2)

**Bangla**

প্রোটিন পরিপাকে অংশ নেয় কোনটি? i. পেপসিন ii. অ্যামাইলেজ iii. কার্বক্সিপেপটাইড নিচের কোনটি সঠিক? A. i ও ii B. i ও iii C. ii ও iii D. i, ii, ও iii Answer with only A, B, C, or D.

**English**

What participate in protein digestion? i. pepsin ii.Amylase iii.Carboxypeptide Which one is correct? A. i & ii B. i & iii C. ii & iii D. I,ii & iii Answer with only A, B, C, or D.

**Current Banglish**

protin poripake ongsh ney konoti? i. peposin ii. amailej iii. karboksipepotaid nicher konoti sothik? A. i o ii B. i o iii C. ii o iii D. i, ii, o iii Answer with only A, B, C, or D.

**Auto-Suggested Banglish**

protin poripake ongsh ney konti? i. peposin ii. amailej iii. karboksipepotaid nicher konti sothik? A. i o ii B. i o iii C. ii o iii D. i, ii, o iii Answer with only A, B, C, or D.

Review fields to fill in the CSV:

- `quality_label`: `ok`, `minor_edit`, `major_edit`, or `bad`
- `reviewed_banglish`: blank for `ok`/`bad`; full replacement for edits
- `review_notes`: short reason when useful

### banglamath_0230

- Calibration reason: calibrate `kot -> koto`
- CSV line: 48
- Impact rank/tier: 17 / tier_1_review_first
- Split: test
- Dataset/task: banglamath / short_answer
- Answer: 20%
- Priority: both_wrong_single_edit
- Suggestions: kot->koto (1)

**Bangla**

২৫ টাকা ১২৫ টাকার শতকরা কত Return only the final answer.

**English**

25 Taka is what percent of 125 Taka? Return only the final answer.

**Current Banglish**

25 taka 125 takar shotokora kot Return only the final answer.

**Auto-Suggested Banglish**

25 taka 125 takar shotokora koto Return only the final answer.

Review fields to fill in the CSV:

- `quality_label`: `ok`, `minor_edit`, `major_edit`, or `bad`
- `reviewed_banglish`: blank for `ok`/`bad`; full replacement for edits
- `review_notes`: short reason when useful

### banglamath_0231

- Calibration reason: calibrate `kot -> koto`
- CSV line: 25
- Impact rank/tier: 19 / tier_1_review_first
- Split: test
- Dataset/task: banglamath / short_answer
- Answer: ২০ টাকা
- Priority: both_wrong_multi_edit
- Suggestions: ekoti->ekti (1); kot->koto (1)

**Bangla**

একটি কলম ২০% লাভে ২৪ টাকায় বিক্রয় করলে ক্রয়মূল্য কত Return only the final answer.

**English**

If a pen is sold for 24 Taka with 20% profit, what was the cost price? Return only the final answer.

**Current Banglish**

ekoti kolom 20% labhe 24 takay bikroy korole kroyomuly kot Return only the final answer.

**Auto-Suggested Banglish**

ekti kolom 20% labhe 24 takay bikroy korole kroyomuly koto Return only the final answer.

Review fields to fill in the CSV:

- `quality_label`: `ok`, `minor_edit`, `major_edit`, or `bad`
- `reviewed_banglish`: blank for `ok`/`bad`; full replacement for edits
- `review_notes`: short reason when useful

### benqa_12th-Biology-I_0265

- Calibration reason: calibrate `ekoti -> ekti`
- CSV line: 23
- Impact rank/tier: 9 / tier_1_review_first
- Split: dev
- Dataset/task: benqa / mcq
- Answer: A
- Priority: both_wrong_multi_edit
- Suggestions: achhe->ache (1); ekoti->ekti (1); konoti->konti (1)

**Bangla**

মি. 'ক' ব্যবহারিক ক্লাসে একটি নমুনার পর্যবেক্ষণ করে দেখলো মেটাজাইলেম কেন্দ্রের দিকে, ভাস্কুলার বান্ডল ৯টি এবং কিছু এককোষী রোম আছে। পর্যবেক্ষিত বৈশিষ্ট্যগুলো কীভাবে উদ্ভিদকে বাঁচিয়ে রাখতে সাহায্য করে? i. পানি ও খনিজ লব...

**English**

Mr. 'X' observed a transverse section of a sample and noticed that metaxylem is present towards the center, 9 (nine) vascular bundles and there are some unicellular hairs. How does the observe features help to protect...

**Current Banglish**

mi. 'k' byoboharik klase ekoti nomunar poryobekshon kore dekholo metajailem kendrer dike, bhaskular bandol 9ti ebong kichhu ekokoshi rom achhe. poryobekshit boishishtyogulo kibhabe udbhidoke banchiye rakhote sahajy ko...

**Auto-Suggested Banglish**

mi. 'k' byoboharik klase ekti nomunar poryobekshon kore dekholo metajailem kendrer dike, bhaskular bandol 9ti ebong kichhu ekokoshi rom ache. poryobekshit boishishtyogulo kibhabe udbhidoke banchiye rakhote sahajy kore...

Review fields to fill in the CSV:

- `quality_label`: `ok`, `minor_edit`, `major_edit`, or `bad`
- `reviewed_banglish`: blank for `ok`/`bad`; full replacement for edits
- `review_notes`: short reason when useful

### banglamath_0552

- Calibration reason: calibrate `kshetrofol -> khetrofol`
- CSV line: 13
- Impact rank/tier: 22 / tier_1_review_first
- Split: test
- Dataset/task: banglamath / short_answer
- Answer: ৪৫০০ বর্গগজ
- Priority: both_wrong_multi_edit
- Suggestions: ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); uchchota->ucchota (1)

**Bangla**

একটি সামান্তরিকের ভূমি ৯০ গজ ও উচ্চতা ৫০ গজ হলে তার ক্ষেত্রফল কত Return only the final answer.

**English**

If a parallelogram has a base of 90 yards and height of 50 yards, what is its area? Return only the final answer.

**Current Banglish**

ekoti samantoriker bhumi 90 goj o uchchota 50 goj hole tar kshetrofol kot Return only the final answer.

**Auto-Suggested Banglish**

ekti samantoriker bhumi 90 goj o ucchota 50 goj hole tar khetrofol koto Return only the final answer.

Review fields to fill in the CSV:

- `quality_label`: `ok`, `minor_edit`, `major_edit`, or `bad`
- `reviewed_banglish`: blank for `ok`/`bad`; full replacement for edits
- `review_notes`: short reason when useful

### banglamath_0538

- Calibration reason: calibrate `kshetrofol -> khetrofol`
- CSV line: 2
- Impact rank/tier: 28 / tier_1_review_first
- Split: test
- Dataset/task: banglamath / short_answer
- Answer: ৩৮৪ বর্গ মিটার
- Priority: both_wrong_multi_edit
- Suggestions: ayotakar->ayotokar (1); choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)

**Bangla**

একটি আয়তাকার বাগানের দৈর্ঘ্য ৬০ মিটার ও প্রস্থ ৪০ মিটার। এর ভিতরে ২ মিটার চওড়া রাস্তা থাকলে রাস্তার ক্ষেত্রফল কত Return only the final answer.

**English**

A rectangular garden is 60m by 40m. If there’s a 2m wide path inside, what is the area of the path? Return only the final answer.

**Current Banglish**

ekoti ayotakar baganer doirghy 60 mitar o prosth 40 mitar. er bhitore 2 mitar choora rasta thakole rastar kshetrofol kot Return only the final answer.

**Auto-Suggested Banglish**

ekti ayotokar baganer doirgho 60 mitar o prostho 40 mitar. er bhitore 2 mitar chowra rasta thakle rastar khetrofol koto Return only the final answer.

Review fields to fill in the CSV:

- `quality_label`: `ok`, `minor_edit`, `major_edit`, or `bad`
- `reviewed_banglish`: blank for `ok`/`bad`; full replacement for edits
- `review_notes`: short reason when useful

### banglamath_0541

- Calibration reason: calibrate `doirghy -> doirgho`
- CSV line: 3
- Impact rank/tier: 29 / tier_1_review_first
- Split: test
- Dataset/task: banglamath / short_answer
- Answer: ৪৪৪ বর্গমিটার
- Priority: both_wrong_multi_edit
- Suggestions: ayotakar->ayotokar (1); choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)

**Bangla**

একটি আয়তাকার বাগানের দৈর্ঘ্য ৫০ মি ও প্রস্থ ৩০ মি। এর ভিতরে ৩ মিটার চওড়া রাস্তা থাকলে রাস্তার ক্ষেত্রফল কত Return only the final answer.

**English**

A rectangular garden is 50m by 30m. If there’s a 3m wide path inside, what is the area of the path? Return only the final answer.

**Current Banglish**

ekoti ayotakar baganer doirghy 50 mi o prosth 30 mi. er bhitore 3 mitar choora rasta thakole rastar kshetrofol kot Return only the final answer.

**Auto-Suggested Banglish**

ekti ayotokar baganer doirgho 50 mi o prostho 30 mi. er bhitore 3 mitar chowra rasta thakle rastar khetrofol koto Return only the final answer.

Review fields to fill in the CSV:

- `quality_label`: `ok`, `minor_edit`, `major_edit`, or `bad`
- `reviewed_banglish`: blank for `ok`/`bad`; full replacement for edits
- `review_notes`: short reason when useful

### banglamath_0549

- Calibration reason: calibrate `doirghy -> doirgho`
- CSV line: 4
- Impact rank/tier: 31 / tier_1_review_first
- Split: test
- Dataset/task: banglamath / short_answer
- Answer: ৪৫০ বর্গমিটার
- Priority: both_wrong_multi_edit
- Suggestions: choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)

**Bangla**

একটি বাগানের বাইরে ২.৫ মিটার চওড়া রাস্তা থাকলে রাস্তার ক্ষেত্রফল কত যদি বাগানের দৈর্ঘ্য ৫০ মি ও প্রস্থ ৩৫ মি হয় Return only the final answer.

**English**

If a 2.5m wide path surrounds a garden of 50m by 35m, what is the area of the path? Return only the final answer.

**Current Banglish**

ekoti baganer baire 2.5 mitar choora rasta thakole rastar kshetrofol kot jodi baganer doirghy 50 mi o prosth 35 mi hoy Return only the final answer.

**Auto-Suggested Banglish**

ekti baganer baire 2.5 mitar chowra rasta thakle rastar khetrofol koto jodi baganer doirgho 50 mi o prostho 35 mi hoy Return only the final answer.

Review fields to fill in the CSV:

- `quality_label`: `ok`, `minor_edit`, `major_edit`, or `bad`
- `reviewed_banglish`: blank for `ok`/`bad`; full replacement for edits
- `review_notes`: short reason when useful

### benqa_8th-Science_0153

- Calibration reason: include dev split example
- CSV line: 94
- Impact rank/tier: 12 / tier_1_review_first
- Split: dev
- Dataset/task: benqa / mcq
- Answer: C
- Priority: both_wrong_single_edit
- Suggestions: konoti->konti (1)

**Bangla**

পাকস্থলীর এসিডিটি নিরাময়ে কোনটি উপযোগী? A. ক্যালসিয়াম B. এসিটিক এসিড C. অ্যলুমিনিয়াম হাইড্রোক্সাইড D. অ্যামোনিয়াম হাইড্রোক্সাইড Answer with only A, B, C, or D.

**English**

Which is appropriate to remove acidity in the stomach? A. Calcium Hydroxide B. Acetic Acid C. Aluminium Hydroxide D. Ammonium Hydroxide Answer with only A, B, C, or D.

**Current Banglish**

pakostholir esiditi niramoye konoti upojogi? A. kyalosiyam B. esitik esid C. ojoluminiyam haidroksaid D. amoniyam haidroksaid Answer with only A, B, C, or D.

**Auto-Suggested Banglish**

pakostholir esiditi niramoye konti upojogi? A. kyalosiyam B. esitik esid C. ojoluminiyam haidroksaid D. amoniyam haidroksaid Answer with only A, B, C, or D.

Review fields to fill in the CSV:

- `quality_label`: `ok`, `minor_edit`, `major_edit`, or `bad`
- `reviewed_banglish`: blank for `ok`/`bad`; full replacement for edits
- `review_notes`: short reason when useful
