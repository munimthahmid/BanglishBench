# Script-Gap Examples: `banglish_drop_vs_bangla_english`

Source gaps: `results/analysis/qwen3_4b_validation100_v2_script_gap_items.csv`
Items: `data/slices/validation_100_v2.jsonl`
Examples exported: 15

## 1. benqa_10th-Chemistry_0132 (benqa, mcq)

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

Bangla parsed: `A`; correct: `True`

**Banglish Prompt**

```text
bisforok podarth konoti?
A. ti.en.ti
B. benojin
C. toluin
D. jailin
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

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

## 2. benqa_10th-Math_0044 (benqa, mcq)

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
ekoti borger kototi protisamj rekha achhe?
A. 8ti
B. 6ti
C. 4ti
D. 2ti
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

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

## 3. benqa_10th-Math_0324 (benqa, mcq)

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

Bangla parsed: `A`; correct: `True`

**Banglish Prompt**

```text
a = \sqrt{3} ebong b = \sqrt{12} hole nicher konoti omulod songkhja?
A. a + b
B. ab
C. \frac{a}{b}
D. \frac{b}{a}
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

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

## 4. benqa_10th-Physics_0045 (benqa, mcq)

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

Bangla parsed: `A`; correct: `True`

**Banglish Prompt**

```text
kon nirdisht bhorer kono bostur beg dbigun korole gotishokti kot gun hobe?
A. charogun
B. dbigun
C. ordhek
D. soman
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

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

## 5. benqa_12th-Biology-II_0287 (benqa, mcq)

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

Bangla parsed: `B`; correct: `True`

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

## 6. benqa_12th-Biology-I_0283 (benqa, mcq)

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

Bangla parsed: `A`; correct: `True`

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

## 7. benqa_12th-Chemistry-II_0013 (benqa, mcq)

Gold: `C`

**Bangla Prompt**

```text
ঘুমের ঔষধ হিসেবে ব্যবহৃত হয় কোনটি?
A. ফরমালডিহাইড
B. অ্যাসিটালডিহাইড
C. প্যারালডিহাইড
D. মেটালডিহাইড
Answer with only A, B, C, or D.
```

Bangla parsed: `C`; correct: `True`

**Banglish Prompt**

```text
ghumer oushodh hisebe bjobohrit hoy konoti?
A. foromalodihaid
B. ojasitalodihaid
C. pjaralodihaid
D. metalodihaid
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
Which one is used as a medicine of sleep?
A. Formaldehyde
B. Acetaldehyde
C. Paraldehyde
D. Metaldehyde
Answer with only A, B, C, or D.
```

English parsed: `C`; correct: `True`

## 8. benqa_12th-Chemistry-II_0194 (benqa, mcq)

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

Bangla parsed: `A`; correct: `True`

**Banglish Prompt**

```text
semikondaktor hisebe bjobohrit hoy-
A. Ge
B. Zn
C. Cu
D. Al
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

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

## 9. benqa_12th-Chemistry-II_0228 (benqa, mcq)

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

## 10. benqa_12th-Chemistry-II_0240 (benqa, mcq)

Gold: `B`

**Bangla Prompt**

```text
CH_{3} - CH_{2} - COONa + NaOH \xrightarrow[\Delta]{CaO} A + Na_{2}CO_{3} উদ্দীপকের বিক্রিয়াটি কী নামে পরিচিত?
A. উর্টজ বিক্রিয়া
B. ডি-কার্বোক্সিলেশন বিক্রিয়া
C. উর্টজ ফিটিগ বিক্রিয়া
D. ফ্রিডেল ক্রাফ্‌ট বিক্রিয়া
Answer with only A, B, C, or D.
```

Bangla parsed: `B`; correct: `True`

**Banglish Prompt**

```text
CH_{3} - CH_{2} - COONa + NaOH \xrightarrow[\Delta]{CaO} A + Na_{2}CO_{3} uddipoker bikriyati ki name porichit?
A. urtoj bikriya
B. di-karboksileshon bikriya
C. urtoj fitig bikriya
D. fridel kraf‌t bikriya
Answer with only A, B, C, or D.
```

Banglish parsed: `C`; correct: `False`

**English Prompt**

```text
CH_{3}-CH_{2}-COONa+NaOH\xrightarrow[\Delta]{CaO}A+Na_{2}CO_{3} What is the name of the chemical reaction of the stem?
A. Wurtz reaction
B. Decarboxylation reaction
C. Wurtz-fitig reaction
D. Friedal Crafts reaction
Answer with only A, B, C, or D.
```

English parsed: `B`; correct: `True`

## 11. benqa_12th-Chemistry-I_0174 (benqa, mcq)

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

Bangla parsed: `A`; correct: `True`

**Banglish Prompt**

```text
bhinegar- i. khadjer bjakoteriya dhbongs kora ii. khabarer ruchi briddhi kore iii. rokt sonchalon komay nicher konoti sothik?
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

## 12. benqa_12th-Chemistry-I_0328 (benqa, mcq)

Gold: `B`

**Bangla Prompt**

```text
Cl(17) কোন ব্লকের মৌল?
A. s-ব্লক
B. p-ব্লক
C. d-ব্লক
D. f-ব্লক
Answer with only A, B, C, or D.
```

Bangla parsed: `B`; correct: `True`

**Banglish Prompt**

```text
Cl(17) kon bloker moul?
A. s-blok
B. p-blok
C. d-blok
D. f-blok
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
In which block the element CI(17) is present?
A. s-block
B. p-block
C. d-block
D. f-block
Answer with only A, B, C, or D.
```

English parsed: `B`; correct: `True`

## 13. benqa_12th-Math-I_0218 (benqa, mcq)

Gold: `A`

**Bangla Prompt**

```text
যেকোনো ত্রিভুজ ABC এর ক্ষেত্রে নিচের কোনটি সঠিক?
A. c = acosB + bcosA
B. b = csinA + asinC
C. \Delta = \frac{1}{2} abcosC
D. cosA = \frac{b^{2} + c^{2} + a^{2}}{2bc}
Answer with only A, B, C, or D.
```

Bangla parsed: `A`; correct: `True`

**Banglish Prompt**

```text
jekono tribhuj ABC er kshetre nicher konoti sothik?
A. c = acosB + bcosA
B. b = csinA + asinC
C. \Delta = \frac{1}{2} abcosC
D. cosA = \frac{b^{2} + c^{2} + a^{2}}{2bc}
Answer with only A, B, C, or D.
```

Banglish parsed: `C`; correct: `False`

**English Prompt**

```text
In any triangle ABC which of the following is correct?
A. c = acosB + bcosA
B. b = csinA + asinC
C. \Delta = \frac{1}{2} abcosC
D. cosA = \frac{b^{2} + c^{2} + a^{2}}{2bc}
Answer with only A, B, C, or D.
```

English parsed: `A`; correct: `True`

## 14. benqa_12th-Physics-I_0133 (benqa, mcq)

Gold: `C`

**Bangla Prompt**

```text
\frac{3}{2} মোল গ্যাসের জন্য আদর্শ গ্যাস সমীকরণ হবে কোনটি?
A. 3PV = 2RT
B. 2PV = \frac{1}{3} RT
C. 2PV = 3RT
D. \frac{PV}{RT}=\frac{2}{3}
Answer with only A, B, C, or D.
```

Bangla parsed: `C`; correct: `True`

**Banglish Prompt**

```text
\frac{3}{2} mol gjaser jonj adorsh gjas somikoron hobe konoti?
A. 3PV = 2RT
B. 2PV = \frac{1}{3} RT
C. 2PV = 3RT
D. \frac{PV}{RT}=\frac{2}{3}
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
The equation of ideal gas for \frac{3}{2} mol is-
A. 3PV = 2RT
B. 2PV = \frac{1}{3} RT
C. 2PV = 3RT
D. \frac{PV}{RT} = \frac{2}{3}
Answer with only A, B, C, or D.
```

English parsed: `C`; correct: `True`

## 15. benqa_8th-Science_0202 (benqa, mcq)

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
sothik khadj-shringkhol konoti?
A. ghas \rightarrow faitopljangkoton \rightarrow juplangkoton
B. ju-plangkoton \rightarrow faitopljangkoton\rightarrow chhotomas
C. faitoplangkoton \rightarrow ju-plangkoton \rightarrow chhotomachh
D. ghas\rightarrow bjang\rightarrow bagh
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

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
