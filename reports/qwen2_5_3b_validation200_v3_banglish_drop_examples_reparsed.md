# Script-Gap Examples: `banglish_drop_vs_bangla_english`

Source gaps: `results/analysis/qwen25_validation200_v3_script_gap_items_reparsed.csv`
Items: `data/slices/validation_200_v3.jsonl`
Examples exported: 16

## 1. banglamath_0229 (banglamath, short_answer)

Gold: `1.5`

**Bangla Prompt**

```text
১৫০% কে দশমিক ভগ্নাংশে প্রকাশ করলে কী হয়
Return only the final answer.
```

Bangla parsed: `1.50`; correct: `True`

**Banglish Prompt**

```text
150% ke doshomik bhognangshe prokash korole ki hoy
Return only the final answer.
```

Banglish parsed: `50%`; correct: `False`

**English Prompt**

```text
What is 150% expressed as a decimal?
Return only the final answer.
```

English parsed: `1.5`; correct: `True`

## 2. banglamath_0230 (banglamath, short_answer)

Gold: `20%`

**Bangla Prompt**

```text
২৫ টাকা ১২৫ টাকার শতকরা কত
Return only the final answer.
```

Bangla parsed: `20%`; correct: `True`

**Banglish Prompt**

```text
25 taka 125 takar shotokora kot
Return only the final answer.
```

Banglish parsed: `125/25 = 5`; correct: `False`

**English Prompt**

```text
25 Taka is what percent of 125 Taka?
Return only the final answer.
```

English parsed: `20%`; correct: `True`

## 3. banglamath_0526 (banglamath, short_answer)

Gold: `৩০ বর্গ মিটার`

**Bangla Prompt**

```text
একটি ত্রিভুজের ভূমি ১০ মিটার ও উচ্চতা ৬ মিটার হলে ক্ষেত্রফল কত
Return only the final answer.
```

Bangla parsed: `30 বর্গমিটার`; correct: `True`

**Banglish Prompt**

```text
ekoti tribhujer bhumi 10 mitar o uchchota 6 mitar hole kshetrofol kot
Return only the final answer.
```

Banglish parsed: `60`; correct: `False`

**English Prompt**

```text
If a triangle has a base of 10 meters and height of 6 meters, what is its area?
Return only the final answer.
```

English parsed: `30 square meters`; correct: `True`

## 4. benqa_10th-Biology_0128 (benqa, mcq)

Gold: `A`

**Bangla Prompt**

```text
ইস্টের শ্বসন প্রক্রিয়ায় কোনটি উৎপন্ন হয়?
A. ল্যাকটিক এসিড
B. গ্লুকোজ
C. অক্সালো অ্যাসিটিক এসিড
D. গ্লিসারিক এসিড
Answer with only A, B, C, or D.
```

Bangla parsed: `A`; correct: `True`

**Banglish Prompt**

```text
ister shboson prokriyay konoti utoponn hoy?
A. lyakotik esid
B. glukoj
C. oksalo ojasitik esid
D. glisarik esid
Answer with only A, B, C, or D.
```

Banglish parsed: `C`; correct: `False`

**English Prompt**

```text
Which one is produce by respiration of yeast?
A. Lactic acid
B. Glucose
C. Oxaloacetic acid
D. Glyceric acid
Answer with only A, B, C, or D.
```

English parsed: `A`; correct: `True`

## 5. benqa_10th-Chemistry_0374 (benqa, mcq)

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

Banglish parsed: `C`; correct: `False`

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

## 6. benqa_10th-Math_0032 (benqa, mcq)

Gold: `B`

**Bangla Prompt**

```text
(\sqrt{3})^{x+2} = 27 হলে x এর মান কত?
A. 6
B. 4
C. 3
D. 2
Answer with only A, B, C, or D.
```

Bangla parsed: `B`; correct: `True`

**Banglish Prompt**

```text
(\sqrt{3})^{x+2} = 27 hole x er man kot?
A. 6
B. 4
C. 3
D. 2
Answer with only A, B, C, or D.
```

Banglish parsed: `A`; correct: `False`

**English Prompt**

```text
If (\sqrt{3})^{x+2} = 27, what is the value of x?
A. 6
B. 4
C. 3
D. 2
Answer with only A, B, C, or D.
```

English parsed: `B`; correct: `True`

## 7. benqa_10th-Math_0044 (benqa, mcq)

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

Banglish parsed: `B`; correct: `False`

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

## 8. benqa_10th-Physics_0021 (benqa, mcq)

Gold: `C`

**Bangla Prompt**

```text
কোনটি মৌলিক একক?
A. জুল
B. নিউটন
C. ক্যান্ডেলা
D. প্যাসকেল
Answer with only A, B, C, or D.
```

Bangla parsed: `C`; correct: `True`

**Banglish Prompt**

```text
konoti moulik ekok?
A. jul
B. niuton
C. kyandela
D. pyasokel
Answer with only A, B, C, or D.
```

Banglish parsed: `A`; correct: `False`

**English Prompt**

```text
Which one is fundamental unit?
A. Joule
B. Newton
C. Candela
D. Pascal
Answer with only A, B, C, or D.
```

English parsed: `C`; correct: `True`

## 9. benqa_12th-Biology-I_0222 (benqa, mcq)

Gold: `A`

**Bangla Prompt**

```text
উদ্ভিদ কোনটি মাটি হতে নেয়?
A. নাইট্রোজেন
B. হাইড্রোজেন
C. অক্সিজেন
D. কার্বন
Answer with only A, B, C, or D.
```

Bangla parsed: `A`; correct: `True`

**Banglish Prompt**

```text
udbhid konoti mati hote ney?
A. naitrojen
B. haidrojen
C. oksijen
D. karbon
Answer with only A, B, C, or D.
```

Banglish parsed: `C`; correct: `False`

**English Prompt**

```text
What does the plant take from the soild?
A. Nitrogen
B. Hydrogen
C. Oxygen
D. Carbon
Answer with only A, B, C, or D.
```

English parsed: `A`; correct: `True`

## 10. benqa_12th-Chemistry-II_0228 (benqa, mcq)

Gold: `C`

**Bangla Prompt**

```text
Ni(s) + 2Ag^{+}(aq) \xrightarrow{2e^{-}} Ni^{2+}(aq) + 2Ag(s); বিক্রিয়াটিতে- i. Ni জারিত হয় ii. Ag জারিত হয় iii. বিক্রিয়াটি একটি রিডক্স বিক্রিয়া নিচের কোনটি সঠিক?
A. i ও ii
B. ii ও iii
C. i ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

Bangla parsed: `C`; correct: `True`

**Banglish Prompt**

```text
Ni(s) + 2Ag^{+}(aq) \xrightarrow{2e^{-}} Ni^{2+}(aq) + 2Ag(s); bikriyatite- i. Ni jarit hoy ii. Ag jarit hoy iii. bikriyati ekoti ridoks bikriya nicher konoti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
Ni(s) + 2Ag^{+}(aq) \overset{2e^{-}} {\rightarrow}Ni^{2+}(aq) + 2Ag(s); in this reaction- i. Ni becomes oxidized ii. Ag becomes oxidized iii. A redox reaction Which one is correct?
A. i and ii
B. ii and iii
C. i and iii
D. i, ii and iii
Answer with only A, B, C, or D.
```

English parsed: `C`; correct: `True`

## 11. benqa_12th-Chemistry-II_0354 (benqa, mcq)

Gold: `B`

**Bangla Prompt**

```text
স্থির তাপমাত্রায় নির্দিষ্ট ভরের গ্যাসের আয়তন বনাম চাপের লেখচিত্রটি কোন ধরনের?
A. পরাবৃত্তাকার
B. অধিবৃত্তাকার
C. বৃত্তাকার
D. সরলরৈখিক
Answer with only A, B, C, or D.
```

Bangla parsed: `B`; correct: `True`

**Banglish Prompt**

```text
sthir tapomatray nirdisht bhorer gyaser ayoton bonam chaper lekhochitroti kon dhoroner?
A. porabrittakar
B. odhibrittakar
C. brittakar
D. soroloroikhik
Answer with only A, B, C, or D.
```

Banglish parsed: `C`; correct: `False`

**English Prompt**

```text
What is the type of the graph of volume Vs pressure at constant temperature of a gas having definite mass?
A. Parabolic
B. Hyperbolic
C. Circular
D. Linear
Answer with only A, B, C, or D.
```

English parsed: `B`; correct: `True`

## 12. benqa_12th-Physics-II_0046 (benqa, mcq)

Gold: `C`

**Bangla Prompt**

```text
রুদ্ধতাপীয় পরিবর্তনের ক্ষেত্রে- i. হঠাৎ সংঘটিত হয় ii. তাপমাত্রা স্থির থাকে iii. এনট্রপির পরিবর্তন শূন্য নিচের কোনটি সঠিক?
A. i ও ii
B. ii ও iii
C. i ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

Bangla parsed: `C`; correct: `True`

**Banglish Prompt**

```text
ruddhotapiy poribortoner kshetre- i. hothat songghotit hoy ii. tapomatra sthir thake iii. enotropir poriborton shuny nicher konoti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
For changing adiabatic process- i. occurs suddenly ii. temperature constant iii. change of entropy is zero Which one is correct?
A. i and ii
B. ii and iii
C. i and iii
D. i, ii and iii
Answer with only A, B, C, or D.
```

English parsed: `C`; correct: `True`

## 13. benqa_8th-Math_0167 (benqa, mcq)

Gold: `C`

**Bangla Prompt**

```text
একটি আয়তাকার বাগানের দৈর্ঘ্য প্রস্থের দেড়গুণ। এর প্রস্থ 16 মিটার হলে, বাগানের পরিসীমা কত?
A. 40 মিটার
B. 64 মিটার
C. 80 মিটার
D. 96 মিটার
Answer with only A, B, C, or D.
```

Bangla parsed: `C`; correct: `True`

**Banglish Prompt**

```text
ekoti ayotakar baganer doirghy prosther derogun. er prosth 16 mitar hole, baganer porisima kot?
A. 40 mitar
B. 64 mitar
C. 80 mitar
D. 96 mitar
Answer with only A, B, C, or D.
```

Banglish parsed: `B`; correct: `False`

**English Prompt**

```text
The length of a rectangular garden is one and half times its breadth. If breadth is 16 metres , what is its peremeter?
A. 40m
B. 64m
C. 80m
D. 96m
Answer with only A, B, C, or D.
```

English parsed: `C`; correct: `True`

## 14. benqa_8th-Science_0042 (benqa, mcq)

Gold: `B`

**Bangla Prompt**

```text
সাবান তৈরির মূল উপাদান
A. এসিড
B. ক্ষারক
C. লবণ
D. গ্লিসারিন
Answer with only A, B, C, or D.
```

Bangla parsed: `B`; correct: `True`

**Banglish Prompt**

```text
saban toirir mul upadan
A. esid
B. ksharok
C. lobon
D. glisarin
Answer with only A, B, C, or D.
```

Banglish parsed: `A`; correct: `False`

**English Prompt**

```text
The main element of making soap is-
A. acid
B. alkali
C. satl
D. glycerlin
Answer with only A, B, C, or D.
```

English parsed: `B`; correct: `True`

## 15. benqa_8th-Science_0153 (benqa, mcq)

Gold: `C`

**Bangla Prompt**

```text
পাকস্থলীর এসিডিটি নিরাময়ে কোনটি উপযোগী?
A. ক্যালসিয়াম
B. এসিটিক এসিড
C. অ্যলুমিনিয়াম হাইড্রোক্সাইড
D. অ্যামোনিয়াম হাইড্রোক্সাইড
Answer with only A, B, C, or D.
```

Bangla parsed: `C`; correct: `True`

**Banglish Prompt**

```text
pakostholir esiditi niramoye konoti upojogi?
A. kyalosiyam
B. esitik esid
C. ojoluminiyam haidroksaid
D. ojamoniyam haidroksaid
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
Which is appropriate to remove acidity in the stomach?
A. Calcium Hydroxide
B. Acetic Acid
C. Aluminium Hydroxide
D. Ammonium Hydroxide
Answer with only A, B, C, or D.
```

English parsed: `C`; correct: `True`

## 16. benqa_8th-Science_0202 (benqa, mcq)

Gold: `C`

**Bangla Prompt**

```text
সঠিক খাদ্য-শৃঙ্খল কোনটি?
A. ঘাস \rightarrow ফাইটোপ্ল্যাংকটন \rightarrow জুপ্লাঙ্কটন
B. জু-প্লাঙ্কটন \rightarrow ফাইটোপ্ল্যাংকটন\rightarrow ছোটমাস
C. ফাইটোপ্লাঙ্কটন \rightarrow জু-প্লাঙ্কটন \rightarrow ছোটমাছ
D. ঘাস\rightarrow ব্যাঙ\rightarrow বাঘ
Answer with only A, B, C, or D.
```

Bangla parsed: `C`; correct: `True`

**Banglish Prompt**

```text
sothik khady-shringkhol konoti?
A. ghas \rightarrow faitoplyangkoton \rightarrow juplangkoton
B. ju-plangkoton \rightarrow faitoplyangkoton\rightarrow chhotomas
C. faitoplangkoton \rightarrow ju-plangkoton \rightarrow chhotomachh
D. ghas\rightarrow byang\rightarrow bagh
Answer with only A, B, C, or D.
```

Banglish parsed: `A`; correct: `False`

**English Prompt**

```text
Which one is the correct food chain
A. Grass\rightarrow Phytoplankton\rightarrow Zooplankton
B. Zooplankot\rightarrow Phytoplankton\rightarrow Small fish
C. Phytoplankton\rightarrow Zooplankton\rightarrow Small fish
D. Grass\rightarrow Frog\rightarrow Tiger
Answer with only A, B, C, or D.
```

English parsed: `C`; correct: `True`
