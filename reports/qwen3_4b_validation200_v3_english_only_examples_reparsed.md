# Script-Gap Examples: `english_only_correct`

Source gaps: `results/analysis/qwen3_validation200_v3_script_gap_items_reparsed.csv`
Items: `data/slices/validation_200_v3.jsonl`
Examples exported: 20

## 1. banglamath_0231 (banglamath, short_answer)

Gold: `২০ টাকা`

**Bangla Prompt**

```text
একটি কলম ২০% লাভে ২৪ টাকায় বিক্রয় করলে ক্রয়মূল্য কত
Return only the final answer.
```

Bangla parsed: `1.2x = 24`; correct: `False`

**Banglish Prompt**

```text
ekoti kolom 20% labhe 24 takay bikroy korole kroyomuly kot
Return only the final answer.
```

Banglish parsed: `{20% of 24 = 0.20 × 24 = 4.8}`; correct: `False`

**English Prompt**

```text
If a pen is sold for 24 Taka with 20% profit, what was the cost price?
Return only the final answer.
```

English parsed: `The cost price is **20 Taka**.`; correct: `True`

## 2. banglamath_0526 (banglamath, short_answer)

Gold: `৩০ বর্গ মিটার`

**Bangla Prompt**

```text
একটি ত্রিভুজের ভূমি ১০ মিটার ও উচ্চতা ৬ মিটার হলে ক্ষেত্রফল কত
Return only the final answer.
```

Bangla parsed: `30`; correct: `False`

**Banglish Prompt**

```text
ekoti tribhujer bhumi 10 mitar o uchchota 6 mitar hole kshetrofol kot
Return only the final answer.
```

Banglish parsed: `{60}`; correct: `False`

**English Prompt**

```text
If a triangle has a base of 10 meters and height of 6 meters, what is its area?
Return only the final answer.
```

English parsed: `30 square meters`; correct: `True`

## 3. benqa_10th-Biology_0090 (benqa, mcq)

Gold: `C`

**Bangla Prompt**

```text
পতঙ্গপরাগী ফুল কোনটি?
A. ধান
B. কচু
C. সরিষা
D. আখ
Answer with only A, B, C, or D.
```

Bangla parsed: `D`; correct: `False`

**Banglish Prompt**

```text
potonggoporagi ful konoti?
A. dhan
B. kochu
C. sorisha
D. akh
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
Which one is insects pollinated flower?
A. Rice
B. Taro
C. Mustard
D. Sugarcane
Answer with only A, B, C, or D.
```

English parsed: `C`; correct: `True`

## 4. benqa_10th-Biology_0149 (benqa, mcq)

Gold: `B`

**Bangla Prompt**

```text
কোনটির প্রান্তীয় প্রাচীর গলে নলের সৃষ্টি হয়?
A. সিভকোষ
B. ভেসেল
C. ট্রাকিড
D. সঙ্গীকোষ
Answer with only A, B, C, or D.
```

Bangla parsed: `D`; correct: `False`

**Banglish Prompt**

```text
konotir prantiy prachir gole noler srishti hoy?
A. sibhokosh
B. bhesel
C. trakid
D. songgikosh
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
Which one of the following develop a long tube when their terminal walls are dissolved?
A. Sieve cell
B. Vessels
C. Tracheid
D. Companion cell
Answer with only A, B, C, or D.
```

English parsed: `B`; correct: `True`

## 5. benqa_10th-Chemistry_0041 (benqa, mcq)

Gold: `D`

**Bangla Prompt**

```text
নিচের কোন তথ্যটি সঠিক?
A. C_{2}H_{4} অপেক্ষা C_{2}H{6} অধিক সক্রিয়
B. CH_{4} ক্ষারকের সাথে বিক্রিয়া করে
C. ইথানল একটি হাইড্রোকার্বন
D. পলিপ্রোপিনকে রি-সাইকেল করা যায়
Answer with only A, B, C, or D.
```

Bangla parsed: `A`; correct: `False`

**Banglish Prompt**

```text
nicher kon tothyoti sothik?
A. C_{2}H_{4} opeksha C_{2}H{6} odhik sokriy
B. CH_{4} ksharoker sathe bikriya kore
C. ithanol ekoti haidrokarbon
D. polipropinoke ri-saikel kora jay
Answer with only A, B, C, or D.
```

Banglish parsed: `A`; correct: `False`

**English Prompt**

```text
Which one of the following information is correct?
A. C_{3}H_{6} is more active than C_{2}H_{4}
B. CH_{4} reacts with base
C. Ethanol is a hydrocarbon
D. it is possible to recycle polypropene
Answer with only A, B, C, or D.
```

English parsed: `D`; correct: `True`

## 6. benqa_10th-Chemistry_0110 (benqa, mcq)

Gold: `C`

**Bangla Prompt**

```text
চুনের পানির সংকেত কোনটি?
A. CaCO_{3}
B. CaO
C. Ca(OH)_{2}
D. Ca(HCO_{3})_{2}
Answer with only A, B, C, or D.
```

Bangla parsed: `D`; correct: `False`

**Banglish Prompt**

```text
chuner panir songket konoti?
A. CaCO_{3}
B. CaO
C. Ca(OH)_{2}
D. Ca(HCO_{3})_{2}
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
Which one is the formula of lime water?
A. CaCO_{3}
B. CaO
C. Ca(OH)_{2}
D. Ca(HCO_{3})_{2}
Answer with only A, B, C, or D.
```

English parsed: `C`; correct: `True`

## 7. benqa_10th-Physics_0084 (benqa, mcq)

Gold: `D`

**Bangla Prompt**

```text
স্থির অবস্থান থেকে সমত্বরণে বস্তুর যেকোনো সময়ের বেগ বস্তুর অতিক্রান্ত দূরত্বের-
A. সমানুপাতিক
B. বর্গের সমানুপাতিক
C. বর্গের ব্যস্তানুপাতিক
D. বর্গমূলের সমানুপাতিক
Answer with only A, B, C, or D.
```

Bangla parsed: `B`; correct: `False`

**Banglish Prompt**

```text
sthir obosthan theke somotborone bostur jekono somoyer beg bostur otikrant durotber-
A. somanupatik
B. borger somanupatik
C. borger byostanupatik
D. borgomuler somanupatik
Answer with only A, B, C, or D.
```

Banglish parsed: `B`; correct: `False`

**English Prompt**

```text
The velocity of a body starting from rest with uniform acceleration is ____ the distance.
A. proportional to
B. proportional to the square of
C. inversely proportional to the square of
D. proportional to the square root of
Answer with only A, B, C, or D.
```

English parsed: `D`; correct: `True`

## 8. benqa_12th-Biology-II_0034 (benqa, mcq)

Gold: `B`

**Bangla Prompt**

```text
ক্ষুদ্রান্ত্রের ক্ষুদ্র অংশ কোনটি?
A. পাইলোরাস
B. ডিওডেনাম
C. জেজুনাম
D. ইলিয়াম
Answer with only A, B, C, or D.
```

Bangla parsed: `D`; correct: `False`

**Banglish Prompt**

```text
kshudrantrer kshudr ongsh konoti?
A. pailoras
B. diodenam
C. jejunam
D. iliyam
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
Which is the smallest part of small intestine?
A. Pylorus
B. Duodenum
C. Jejunum
D. Ileum
Answer with only A, B, C, or D.
```

English parsed: `B`; correct: `True`

## 9. benqa_12th-Biology-II_0325 (benqa, mcq)

Gold: `A`

**Bangla Prompt**

```text
রুই মাছের শ্রেণি পাখনায় রক্ত পরিবহন করে নিচের কোন ধমনি?
A. ইলিয়াক
B. প্যারাইল
C. সিলিয়াকো-মেসেন্টারিক
D. সাবক্লাভিয়ান
Answer with only A, B, C, or D.
```

Bangla parsed: `C`; correct: `False`

**Banglish Prompt**

```text
rui machher shreni pakhonay rokt poribohon kore nicher kon dhomoni?
A. iliyak
B. pyarail
C. siliyako-mesentarik
D. saboklabhiyan
Answer with only A, B, C, or D.
```

Banglish parsed: `C`; correct: `False`

**English Prompt**

```text
Which artery of the below transmits blood in Ruie fishe's pelvic fin?
A. Iliac
B. parietal
C. Coeliaco-mesenteric
D. Subclavian
Answer with only A, B, C, or D.
```

English parsed: `A`; correct: `True`

## 10. benqa_12th-Biology-I_0218 (benqa, mcq)

Gold: `B`

**Bangla Prompt**

```text
গমের বৈজ্ঞানিক নাম কী?
A. Oryza sativa
B. Triticum aestivum
C. Zea mays
D. Bambusa tulda
Answer with only A, B, C, or D.
```

Bangla parsed: `D`; correct: `False`

**Banglish Prompt**

```text
gomer boijnanik nam ki?
A. Oryza sativa
B. Triticum aestivum
C. Zea mays
D. Bambusa tulda
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
What is scientific name of wheat?
A. Oryza sativa
B. Triticum aestirum
C. Zea mays
D. Bambusa tulda
Answer with only A, B, C, or D.
```

English parsed: `B`; correct: `True`

## 11. benqa_12th-Chemistry-II_0117 (benqa, mcq)

Gold: `C`

**Bangla Prompt**

```text
অ্যালডিহাইড ও কিটোনের মধ্যে পার্থক্য নিরূপনের জন্য ব্যবহৃত বিকারক- i. টলেন বিকারক ii. 2 : 4 - DNPH iii. ফেলিং দ্রবণ নিচের কোনটি সঠিক?
A. i ও ii
B. ii ও iii
C. i ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

Bangla parsed: `D`; correct: `False`

**Banglish Prompt**

```text
ojalodihaid o kitoner modhye parthoky niruponer jony byobohrit bikarok- i. tolen bikarok ii. 2 : 4 - DNPH iii. feling drobon nicher konoti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
For the differentiation between aldehyde and ketone usable reagent is- i. tollen's reagent ii. 2 : 4 - DNPH iii. fehling solution Which one is correct?
A. i and ii
B. ii and iii
C. i and iii
D. i, ii and iii
Answer with only A, B, C, or D.
```

English parsed: `C`; correct: `True`

## 12. benqa_12th-Chemistry-II_0354 (benqa, mcq)

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

Bangla parsed: `D`; correct: `False`

**Banglish Prompt**

```text
sthir tapomatray nirdisht bhorer gyaser ayoton bonam chaper lekhochitroti kon dhoroner?
A. porabrittakar
B. odhibrittakar
C. brittakar
D. soroloroikhik
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

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

## 13. benqa_12th-Chemistry-I_0190 (benqa, mcq)

Gold: `B`

**Bangla Prompt**

```text
নিচের কোনটির বন্ধন কোন সবচেয়ে বড়?
A. CH_{4}
B. BCl_{3}
C. NH_{3}
D. H_{2}O
Answer with only A, B, C, or D.
```

Bangla parsed: `D`; correct: `False`

**Banglish Prompt**

```text
nicher konotir bondhon kon sobocheye bor?
A. CH_{4}
B. BCl_{3}
C. NH_{3}
D. H_{2}O
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
Which one of the following has maximum bond angle?
A. CH_{4}
B. BCI_{3}
C. NH_{3}
D. H_{2}O
Answer with only A, B, C, or D.
```

English parsed: `B`; correct: `True`

## 14. benqa_12th-Math-I_0088 (benqa, mcq)

Gold: `C`

**Bangla Prompt**

```text
x-এর সাপেক্ষে ln ax এর অন্তরজ-
A. \frac{a}{x}
B. \frac{x}{a}
C. \frac{1}{x}
D. \frac{1}{ax}
Answer with only A, B, C, or D.
```

Bangla parsed: `D`; correct: `False`

**Banglish Prompt**

```text
x-er sapekshe ln ax er ontoroj-
A. \frac{a}{x}
B. \frac{x}{a}
C. \frac{1}{x}
D. \frac{1}{ax}
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
The derivative of lnax with respect to x is-
A. \frac{a}{x}
B. \frac{x}{a}
C. \frac{1}{x}
D. \frac{1}{ax}
Answer with only A, B, C, or D.
```

English parsed: `C`; correct: `True`

## 15. benqa_12th-Physics-II_0046 (benqa, mcq)

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

Bangla parsed: `B`; correct: `False`

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

## 16. benqa_12th-Physics-II_0292 (benqa, mcq)

Gold: `C`

**Bangla Prompt**

```text
দৃশ্যমান বর্ণালির তরঙ্গদৈর্ঘ্যের বিস্তৃতি-
A. 2000 \AA থেকে 3000 \AA পর্যন্ত
B. 3000 \AA থেকে 4000 \AA পর্যন্ত
C. 4000 \AA থেকে 8000 \AA পর্যন্ত
D. 8000 \AA থেকে 12000 \AA পর্যন্ত
Answer with only A, B, C, or D.
```

Bangla parsed: `A`; correct: `False`

**Banglish Prompt**

```text
drishyoman bornalir toronggodoirghyer bistriti-
A. 2000 \AA theke 3000 \AA poryont
B. 3000 \AA theke 4000 \AA poryont
C. 4000 \AA theke 8000 \AA poryont
D. 8000 \AA theke 12000 \AA poryont
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
Which of the following is the range of wavelength for visible spectrum?
A. 2000 \AA - 3000 \AA
B. 3000 \AA - 4000 \AA
C. 4000 \AA - 8000 \AA
D. 8000 \AA - 12000 \AA
Answer with only A, B, C, or D.
```

English parsed: `C`; correct: `True`

## 17. benqa_8th-Math_0167 (benqa, mcq)

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

Bangla parsed: `D`; correct: `False`

**Banglish Prompt**

```text
ekoti ayotakar baganer doirghy prosther derogun. er prosth 16 mitar hole, baganer porisima kot?
A. 40 mitar
B. 64 mitar
C. 80 mitar
D. 96 mitar
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

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

## 18. benqa_8th-Science_0042 (benqa, mcq)

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

Bangla parsed: `C`; correct: `False`

**Banglish Prompt**

```text
saban toirir mul upadan
A. esid
B. ksharok
C. lobon
D. glisarin
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

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

## 19. benqa_8th-Science_0086 (benqa, mcq)

Gold: `A`

**Bangla Prompt**

```text
কোনটির প্রজনন অফসেটের মাধ্যমে হয়?
A. টোপাপানা
B. পুদিনা
C. পিঁয়াজ
D. পেয়ারা
Answer with only A, B, C, or D.
```

Bangla parsed: `D`; correct: `False`

**Banglish Prompt**

```text
konotir projonon ofoseter madhyome hoy?
A. topapana
B. pudina
C. pinyaj
D. peyara
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
The reproduction of which occurs through offset?
A. Spirodela
B. Minite
C. Onion
D. Guava
Answer with only A, B, C, or D.
```

English parsed: `A`; correct: `True`

## 20. benqa_8th-Science_0159 (benqa, mcq)

Gold: `B`

**Bangla Prompt**

```text
নিচের কোনটি রসালো ফল?
A. আতা
B. কলা
C. আনারস
D. কাঁঠাল
Answer with only A, B, C, or D.
```

Bangla parsed: `C`; correct: `False`

**Banglish Prompt**

```text
nicher konoti rosalo fol?
A. ata
B. kola
C. anaros
D. kanthal
Answer with only A, B, C, or D.
```

Banglish parsed: `C`; correct: `False`

**English Prompt**

```text
Which of the followings is fleshy fruits?
A. Custard apple
B. Banana
C. Pineapple
D. Jackfruit
Answer with only A, B, C, or D.
```

English parsed: `B`; correct: `True`
