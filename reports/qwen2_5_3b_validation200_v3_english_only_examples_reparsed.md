# Script-Gap Examples: `english_only_correct`

Source gaps: `results/analysis/qwen25_validation200_v3_script_gap_items_reparsed.csv`
Items: `data/slices/validation_200_v3.jsonl`
Examples exported: 24

## 1. banglamath_0228 (banglamath, short_answer)

Gold: `২/৫`

**Bangla Prompt**

```text
৪০% কে সাধারণ ভগ্নাংশে প্রকাশ করলে কী হয়
Return only the final answer.
```

Bangla parsed: `40% একটি সাধারণ ভগ্নাংশে প্রকাশ করলে 4/10 হয়.`; correct: `False`

**Banglish Prompt**

```text
40% ke sadharon bhognangshe prokash korole ki hoy
Return only the final answer.
```

Banglish parsed: `40% of the population reads or writes`; correct: `False`

**English Prompt**

```text
What is 40% expressed as a proper fraction?
Return only the final answer.
```

English parsed: `2/5`; correct: `True`

## 2. banglamath_0231 (banglamath, short_answer)

Gold: `২০ টাকা`

**Bangla Prompt**

```text
একটি কলম ২০% লাভে ২৪ টাকায় বিক্রয় করলে ক্রয়মূল্য কত
Return only the final answer.
```

Bangla parsed: `12`; correct: `False`

**Banglish Prompt**

```text
ekoti kolom 20% labhe 24 takay bikroy korole kroyomuly kot
Return only the final answer.
```

Banglish parsed: `Ekot kolom 20% labhe 24 takay bikroy korle kroyomuly kot.`; correct: `False`

**English Prompt**

```text
If a pen is sold for 24 Taka with 20% profit, what was the cost price?
Return only the final answer.
```

English parsed: `20 Taka`; correct: `True`

## 3. benqa_10th-Biology_0215 (benqa, mcq)

Gold: `B`

**Bangla Prompt**

```text
C_{6}H_{12}O_{6}\xarrowright{এনজাইম}C_{3}H_{4}O_{3} উদ্দীপকের প্রক্রিয়াটি- i. সবাত ও অবাত শ্বসনের প্রথম ধাপ ii. কোষের মাইটোকন্ড্রিয়ায় ঘটে থাকে iii. এতে নিট অণু ATP উৎপন্ন হয় নিচের কোনটি সঠিক?
A. i ও ii
B. i ও iii
C. ii ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

Bangla parsed: `D`; correct: `False`

**Banglish Prompt**

```text
C_{6}H_{12}O_{6}\xarrowright{enojaim}C_{3}H_{4}O_{3} uddipoker prokriyati- i. sobat o obat shbosoner prothom dhap ii. kosher maitokondriyay ghote thake iii. ete nit onu ATP utoponn hoy nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
C_{6}H_{12}O_{6} \xrightarrow{Enzyme} C_{3}H_{4}O_{3} the process of the stem- i. is the inital stage of both acrobic and anacrobic respiration ii. takes place in the mitochondria of a cell iii. produces & molecules of neat ATP Which one is correct?
A. i and ii
B. i and iii
C. ii and iii
D. i, ii and iii
Answer with only A, B, C, or D.
```

English parsed: `B`; correct: `True`

## 4. benqa_10th-Biology_0339 (benqa, mcq)

Gold: `D`

**Bangla Prompt**

```text
নিচের কোন উদ্ভিদে সালোকসংশ্লেষণ হার বেশি?
A. বট গাছ
B. কাঁঠাল
C. পেয়ারা
D. কচুরিপানা
Answer with only A, B, C, or D.
```

Bangla parsed: `B`; correct: `False`

**Banglish Prompt**

```text
nicher kon udbhide salokosongshleshon har beshi?
A. bot gachh
B. kanthal
C. peyara
D. kochuripana
Answer with only A, B, C, or D.
```

Banglish parsed: `A`; correct: `False`

**English Prompt**

```text
Which of the following plants has a higher rate of photosynthesis?
A. Banyan tree
B. Jack fruit
C. Guava
D. Water hyacinth
Answer with only A, B, C, or D.
```

English parsed: `D`; correct: `True`

## 5. benqa_10th-Chemistry_0110 (benqa, mcq)

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

Banglish parsed: `A`; correct: `False`

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

## 6. benqa_10th-Chemistry_0132 (benqa, mcq)

Gold: `A`

**Bangla Prompt**

```text
বিস্ফোরক পদার্থ কোনটি?
A. টি.এন.টি
B. বেনজিন
C. টলুইন
D. জাইলিন
Answer with only A, B, C, or D.
```

Bangla parsed: `C`; correct: `False`

**Banglish Prompt**

```text
bisforok podarth konoti?
A. ti.en.ti
B. benojin
C. toluin
D. jailin
Answer with only A, B, C, or D.
```

Banglish parsed: `B`; correct: `False`

**English Prompt**

```text
Which one is explosive substance?
A. TNT
B. Benzene
C. Toluene
D. Xylene
Answer with only A, B, C, or D.
```

English parsed: `A`; correct: `True`

## 7. benqa_10th-Chemistry_0194 (benqa, mcq)

Gold: `D`

**Bangla Prompt**

```text
নিচের কোন মৌলটি অধিক সক্রিয়?
A. O
B. P
C. N
D. F
Answer with only A, B, C, or D.
```

Bangla parsed: `A`; correct: `False`

**Banglish Prompt**

```text
nicher kon mouloti odhik sokriy?
A. O
B. P
C. N
D. F
Answer with only A, B, C, or D.
```

Banglish parsed: `C`; correct: `False`

**English Prompt**

```text
Which element of the following is more active?
A. O
B. P
C. N
D. F
Answer with only A, B, C, or D.
```

English parsed: `D`; correct: `True`

## 8. benqa_10th-Math_0324 (benqa, mcq)

Gold: `A`

**Bangla Prompt**

```text
a = \sqrt{3} এবং b = \sqrt{12} হলে নিচের কোনটি অমূলদ সংখ্যা?
A. a + b
B. ab
C. \frac{a}{b}
D. \frac{b}{a}
Answer with only A, B, C, or D.
```

Bangla parsed: `C`; correct: `False`

**Banglish Prompt**

```text
a = \sqrt{3} ebong b = \sqrt{12} hole nicher konoti omulod songkhya?
A. a + b
B. ab
C. \frac{a}{b}
D. \frac{b}{a}
Answer with only A, B, C, or D.
```

Banglish parsed: `B`; correct: `False`

**English Prompt**

```text
If a = \sqrt{3} and b = \sqrt{12}, which one is irrational number?
A. a + b
B. ab
C. \frac{a}{b}
D. \frac{b}{a}
Answer with only A, B, C, or D.
```

English parsed: `A`; correct: `True`

## 9. benqa_10th-Physics_0045 (benqa, mcq)

Gold: `A`

**Bangla Prompt**

```text
কোন নির্দিষ্ট ভরের কোনো বস্তুর বেগ দ্বিগুন করলে গতিশক্তি কত গুন হবে?
A. চারগুন
B. দ্বিগুন
C. অর্ধেক
D. সমান
Answer with only A, B, C, or D.
```

Bangla parsed: `B`; correct: `False`

**Banglish Prompt**

```text
kon nirdisht bhorer kono bostur beg dbigun korole gotishokti kot gun hobe?
A. charogun
B. dbigun
C. ordhek
D. soman
Answer with only A, B, C, or D.
```

Banglish parsed: `B`; correct: `False`

**English Prompt**

```text
How many times the kinetic energy of a definite mass when it's velocity replaced by twice time?
A. Four time
B. Twice time
C. Half
D. Equal
Answer with only A, B, C, or D.
```

English parsed: `A`; correct: `True`

## 10. benqa_10th-Physics_0296 (benqa, mcq)

Gold: `D`

**Bangla Prompt**

```text
ইউরেনিয়ামের চেইন বিক্রিয়ার দ্বিতীয় ধাপে কতটি নিউট্রন নির্গত হয়?
A. 2 টি
B. 3 টি
C. 6 টি
D. 9 টি
Answer with only A, B, C, or D.
```

Bangla parsed: `B`; correct: `False`

**Banglish Prompt**

```text
iureniyamer chein bikriyar dbitiy dhape kototi niutron nirgot hoy?
A. 2 ti
B. 3 ti
C. 6 ti
D. 9 ti
Answer with only A, B, C, or D.
```

Banglish parsed: `B`; correct: `False`

**English Prompt**

```text
In chain reaction of Uranium how many neutrons will be emitted?
A. 2
B. 3
C. 6
D. 9
Answer with only A, B, C, or D.
```

English parsed: `D`; correct: `True`

## 11. benqa_12th-Biology-II_0034 (benqa, mcq)

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

Bangla parsed: `A`; correct: `False`

**Banglish Prompt**

```text
kshudrantrer kshudr ongsh konoti?
A. pailoras
B. diodenam
C. jejunam
D. iliyam
Answer with only A, B, C, or D.
```

Banglish parsed: `C`; correct: `False`

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

## 12. benqa_12th-Biology-II_0179 (benqa, mcq)

Gold: `A`

**Bangla Prompt**

```text
রক্ত জমাট বাঁধতে কোন ধাতব আয়ন সহায়তা করে?
A. Ca^{++}
B. Mg^{++}
C. Cu^{++}
D. Fe^{++}
Answer with only A, B, C, or D.
```

Bangla parsed: `D`; correct: `False`

**Banglish Prompt**

```text
rokt jomat bandhote kon dhatob ayon sohayota kore?
A. Ca^{++}
B. Mg^{++}
C. Cu^{++}
D. Fe^{++}
Answer with only A, B, C, or D.
```

Banglish parsed: `B`; correct: `False`

**English Prompt**

```text
Which metallic ion help to blood clotting?
A. Ca^{++}
B. Mg^{++}
C. Cu^{++}
D. Fe^{++}
Answer with only A, B, C, or D.
```

English parsed: `A`; correct: `True`

## 13. benqa_12th-Biology-II_0287 (benqa, mcq)

Gold: `B`

**Bangla Prompt**

```text
প্রোটিন পরিপাকে অংশ নেয় কোনটি? i. পেপসিন ii. অ্যামাইলেজ iii. কার্বক্সিপেপটাইড নিচের কোনটি সঠিক?
A. i ও ii
B. i ও iii
C. ii ও iii
D. i, ii, ও iii
Answer with only A, B, C, or D.
```

Bangla parsed: `D`; correct: `False`

**Banglish Prompt**

```text
protin poripake ongsh ney konoti? i. peposin ii. ojamailej iii. karboksipepotaid nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
What participate in protein digestion? i. pepsin ii.Amylase iii.Carboxypeptide Which one is correct?
A. i & ii
B. i & iii
C. ii & iii
D. I,ii & iii
Answer with only A, B, C, or D.
```

English parsed: `B`; correct: `True`

## 14. benqa_12th-Biology-II_0325 (benqa, mcq)

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

Banglish parsed: `B`; correct: `False`

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

## 15. benqa_12th-Biology-I_0077 (benqa, mcq)

Gold: `C`

**Bangla Prompt**

```text
নিচের কোন ধাপে ক্রোমাটিডগুলো মেরুমুখী চলতে শুরু করে?
A. প্রোফেজ
B. মেটাফেজ
C. অ্যানাফেজ
D. টেলোফেজ
Answer with only A, B, C, or D.
```

Bangla parsed: `B`; correct: `False`

**Banglish Prompt**

```text
nicher kon dhape kromatidogulo merumukhi cholote shuru kore?
A. profej
B. metafej
C. ojanafej
D. telofej
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
In which step of the following, chromatids move towards the poles?
A. Prohase
B. Metaphase
C. Anaphase
D. Telophase
Answer with only A, B, C, or D.
```

English parsed: `C`; correct: `True`

## 16. benqa_12th-Biology-I_0218 (benqa, mcq)

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

Bangla parsed: `A`; correct: `False`

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

## 17. benqa_12th-Biology-I_0265 (benqa, mcq)

Gold: `A`

**Bangla Prompt**

```text
মি. 'ক' ব্যবহারিক ক্লাসে একটি নমুনার পর্যবেক্ষণ করে দেখলো মেটাজাইলেম কেন্দ্রের দিকে, ভাস্কুলার বান্ডল ৯টি এবং কিছু এককোষী রোম আছে। পর্যবেক্ষিত বৈশিষ্ট্যগুলো কীভাবে উদ্ভিদকে বাঁচিয়ে রাখতে সাহায্য করে? i. পানি ও খনিজ লবণ পরিবহন করে ii. প্রস্তুতকৃত খাবার পরিবহন করে iii. খাদ্য প্রস্তুত করে নিচের কোনটি সঠিক?
A. i ও ii
B. ii ও iii
C. i ও iii
D. i, ii, ও iii
Answer with only A, B, C, or D.
```

Bangla parsed: `D`; correct: `False`

**Banglish Prompt**

```text
mi. 'k' byoboharik klase ekoti nomunar poryobekshon kore dekholo metajailem kendrer dike, bhaskular bandol 9ti ebong kichhu ekokoshi rom achhe. poryobekshit boishishtyogulo kibhabe udbhidoke banchiye rakhote sahajy kore? i. pani o khonij lobon poribohon kore ii. prostutokrit khabar poribohon kore iii. khady prostut kore nicher konoti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
Mr. 'X' observed a transverse section of a sample and noticed that metaxylem is present towards the center, 9 (nine) vascular bundles and there are some unicellular hairs. How does the observe features help to protect the plant? i. By transporting water and mineral salts ii. By transporting prepared food iii. By preparing food Which one is correct?
A. i & ii
B. ii & iii
C. i & iii
D. i, ii & iii
Answer with only A, B, C, or D.
```

English parsed: `A`; correct: `True`

## 18. benqa_12th-Biology-I_0277 (benqa, mcq)

Gold: `D`

**Bangla Prompt**

```text
কোনটিকে ঘাস গোত্র বলা হয়?
A. সোলানেসি
B. সাইক্যাডেসি
C. মালভেসি
D. পোয়েসি
Answer with only A, B, C, or D.
```

Bangla parsed: `B`; correct: `False`

**Banglish Prompt**

```text
konotike ghas gotr bola hoy?
A. solanesi
B. saikyadesi
C. malobhesi
D. poyesi
Answer with only A, B, C, or D.
```

Banglish parsed: `B`; correct: `False`

**English Prompt**

```text
Which is called grass family?
A. Solanaceae
B. Cyeadaceae
C. Malvaceae
D. Poaceae
Answer with only A, B, C, or D.
```

English parsed: `D`; correct: `True`

## 19. benqa_12th-Biology-I_0283 (benqa, mcq)

Gold: `A`

**Bangla Prompt**

```text
পেঁপের রিং স্পট রোগের লক্ষণ হলো- i. পাতার বোটায় পানি ভেজা সবুজ দাগ দেখা যায় ii. পেঁপের মিষ্টতা হ্রাস পায় iii. ফলের আকার বড় হয় নিচের কোনটি সঠিক?
A. i ও ii
B. ii ও iii
C. i ও iii
D. i, ii, ও iii
Answer with only A, B, C, or D.
```

Bangla parsed: `D`; correct: `False`

**Banglish Prompt**

```text
penper ring spot roger lokshon holo- i. patar botay pani bheja sobuj dag dekha jay ii. penper mishtota hras pay iii. foler akar bor hoy nicher konoti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
Symptoms of ring spot disease in papaya is- i. observance of wet green spot on the petiole of leaves ii. reduction of sweetness of papaya iii. enlarging of the size of fruit Which one is correct?
A. i & ii
B. ii & iii
C. i & iii
D. i, ii & iii
Answer with only A, B, C, or D.
```

English parsed: `A`; correct: `True`

## 20. benqa_12th-Chemistry-II_0194 (benqa, mcq)

Gold: `A`

**Bangla Prompt**

```text
সেমিকন্ডাক্টর হিসেবে ব্যবহৃত হয়-
A. Ge
B. Zn
C. Cu
D. Al
Answer with only A, B, C, or D.
```

Bangla parsed: `D`; correct: `False`

**Banglish Prompt**

```text
semikondaktor hisebe byobohrit hoy-
A. Ge
B. Zn
C. Cu
D. Al
Answer with only A, B, C, or D.
```

Banglish parsed: `B`; correct: `False`

**English Prompt**

```text
Used as semiconductor is-
A. Ge
B. Zn
C. Cu
D. Al
Answer with only A, B, C, or D.
```

English parsed: `A`; correct: `True`

## 21. benqa_12th-Chemistry-II_0235 (benqa, mcq)

Gold: `A`

**Bangla Prompt**

```text
নিচের কোনটি লুইস এসিড?
A. AlCl_{3}
B. H_{2}CO_{3}
C. NH_{3}
D. H_{3}PO_{4}
Answer with only A, B, C, or D.
```

Bangla parsed: `D`; correct: `False`

**Banglish Prompt**

```text
nicher konoti luis esid?
A. AlCl_{3}
B. H_{2}CO_{3}
C. NH_{3}
D. H_{3}PO_{4}
Answer with only A, B, C, or D.
```

Banglish parsed: `C`; correct: `False`

**English Prompt**

```text
Which one of the following is the Lewis acid?
A. AlCl_{3}
B. H_{2}CO_{3}
C. NH_{3}
D. H_{3}PO_{4}
Answer with only A, B, C, or D.
```

English parsed: `A`; correct: `True`

## 22. benqa_12th-Chemistry-I_0140 (benqa, mcq)

Gold: `D`

**Bangla Prompt**

```text
CaF_{2}-এর সম্পৃক্ত জলীয় দ্রবণে ফ্লোরাইড আয়নের ঘনমাত্রা 0.00655 gL^{-1} হলে CaF_{2} এর দ্রাব্যতা গুণফল কত হবে?
A. 3.7\times 10^{-13}
B. 2.048\times 10^{-10}
C. 3.7\times 10^{-12}
D. 2.048\times 10^{-11}
Answer with only A, B, C, or D.
```

Bangla parsed: `B`; correct: `False`

**Banglish Prompt**

```text
CaF_{2}-er somprikt joliy drobone floraid ayoner ghonomatra 0.00655 gL^{-1} hole CaF_{2} er drabyota gunofol kot hobe?
A. 3.7\times 10^{-13}
B. 2.048\times 10^{-10}
C. 3.7\times 10^{-12}
D. 2.048\times 10^{-11}
Answer with only A, B, C, or D.
```

Banglish parsed: `B`; correct: `False`

**English Prompt**

```text
Conecntration of F^{-} ion in saturated sol^{n} of CaF_{2} is 0.00655 gL^{-1}; What is its solubility product?
A. 3.7\times 10^{-13}
B. 2.048\times 10^{-10}
C. 3.7\times 10^{-12}
D. 2.048\times 10^{-11}
Answer with only A, B, C, or D.
```

English parsed: `D`; correct: `True`

## 23. benqa_12th-Chemistry-I_0174 (benqa, mcq)

Gold: `A`

**Bangla Prompt**

```text
ভিনেগার- i. খাদ্যের ব্যাকটেরিয়া ধ্বংস করা ii. খাবারের রুচি বৃদ্ধি করে iii. রক্ত সঞ্চালন কমায় নিচের কোনটি সঠিক?
A. i ও ii
B. i ও iii
C. ii ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

Bangla parsed: `D`; correct: `False`

**Banglish Prompt**

```text
bhinegar- i. khadyer byakoteriya dhbongs kora ii. khabarer ruchi briddhi kore iii. rokt sonchalon komay nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
Vinegar- i.destroys bacteria ii.increases the taste of meal iii.decreases blood circulation Which one is correct?
A. i&ii
B. i&iii
C. ii&iii
D. I,ii&iii
Answer with only A, B, C, or D.
```

English parsed: `A`; correct: `True`

## 24. benqa_12th-Chemistry-I_0260 (benqa, mcq)

Gold: `D`

**Bangla Prompt**

```text
ভিনেগারে কত শতাংশ পানি বিদ্যমান?
A. 6%
B. 15%
C. 70%
D. 90%
Answer with only A, B, C, or D.
```

Bangla parsed: `C`; correct: `False`

**Banglish Prompt**

```text
bhinegare kot shotangsh pani bidyoman?
A. 6%
B. 15%
C. 70%
D. 90%
Answer with only A, B, C, or D.
```

Banglish parsed: `B`; correct: `False`

**English Prompt**

```text
What percentage of water contain in vinegar?
A. 6%
B. 15%
C. 70%
D. 90%
Answer with only A, B, C, or D.
```

English parsed: `D`; correct: `True`
