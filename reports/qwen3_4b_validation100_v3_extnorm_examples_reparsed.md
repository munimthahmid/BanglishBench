# Self-Normalization Rewrite Report

Items: `data/slices/validation_100_v3.jsonl`
Eval rows: `results/runs/qwen3_4b_validation100_v3_extnorm/results/runs/qwen3_4b_validation100_v3_extnorm.jsonl`
Examples exported: 23

Compare file: `results/analysis/qwen3_validation100_v3_baseline_vs_extnorm_items_reparsed.csv`

## 1. banglamath_0229 (banglamath)

Gold: `1.5`
Self-normalized parsed: `can be provided based on the given input.`; correct: `False`

Baseline parsed: `Doshomik bhognangshe prokash korle, 1.5 = 1.5`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
150% ke doshomik bhognangshe prokash korole ki hoy
Return only the final answer.
```

**Model Rewrite**

```text
কে দোশোমিক ভোগনাংশে প্রোকাশ কোরোলে কি হোয়া
N only the final answer.
```

**Final Raw Output**

```text
The question appears to be garbled or incorrectly formatted. It does not make coherent sense in Bengali or English. Therefore, no valid answer can be provided based on the given input.

Final answer: অস্পষ্ট প্রশ্ন, উত্তর দ
```


## 2. banglamath_0519 (banglamath)

Gold: `৭৫০০ বর্গমিটার`
Self-normalized parsed: `150 × 50 = 7500 বর্গমিটার`; correct: `True`

Baseline parsed: `Unable to evaluate due to unclear or nonsens`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
ekoti ayotakar baganer doirghy 150 mitar o prosth 50 mitar hole kshetrofol kot
Return only the final answer.
```

**Model Rewrite**

```text
/ আয়োটকর বাগানের দৈরঘy 150 মিটার ও প্রোস্থ 50 মিটার হোলে kshetrofol কোট
N only the final answer.
```

**Final Raw Output**

```text
150 × 50 = 7500 বর্গমিটার
```


## 3. benqa_10th-Biology_0090 (benqa)

Gold: `C`
Self-normalized parsed: `C`; correct: `True`

Baseline parsed: `D`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
potonggoporagi ful konoti?
A. dhan
B. kochu
C. sorisha
D. akh
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
Griporagi ful কোনোটি?
A. 
B. 
C. Ait
D. 
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
C
```


## 4. benqa_10th-Biology_0143 (benqa)

Gold: `C`
Self-normalized parsed: `A`; correct: `False`

Baseline parsed: `C`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
akosmik kidoni okejo hote pare kon karone?
A. dayabetis
B. nefraitis
C. maratmok dayoriya
D. uchch roktochap
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
তেমনি কিডোনি ওকেজো হোতে পারে কোন করোনে?
A. Cricket
B. Cricinfo
C. Ke সেরাোরিয়া
D. Notopath
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
A
```


## 5. benqa_10th-Biology_0188 (benqa)

Gold: `A`
Self-normalized parsed: `A`; correct: `True`

Baseline parsed: `D`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
torol jojok tisyu koy prokar?
A. 2
B. 3
C. 4
D. 5
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
Jojok tisyu koy prokar?
A. 
B. 
C. 
D. 
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
A
```


## 6. benqa_10th-Chemistry_0041 (benqa)

Gold: `D`
Self-normalized parsed: `D`; correct: `True`

Baseline parsed: `A`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
nicher kon tothyoti sothik?
A. C_{2}H_{4} opeksha C_{2}H{6} odhik sokriy
B. CH_{4} ksharoker sathe bikriya kore
C. ithanol ekoti haidrokarbon
D. polipropinoke ri-saikel kora jay
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
ঔthyoti সোথিক?
A. {2}H_{4} opeksha C_{2}H{6} অধিক sokriy
B. _{4} ক্রুরোকের সাথে বিক্রিয়াঃ কোরে
C. থানোল এনোটি হাইড্রোকারবোন
D. প্রোপিনোকে রি-সাইকেল কোরা যায়
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
D
```


## 7. benqa_10th-Chemistry_0194 (benqa)

Gold: `D`
Self-normalized parsed: `A`; correct: `False`

Baseline parsed: `D`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
nicher kon mouloti odhik sokriy?
A. O
B. P
C. N
D. F
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
নিম্নোক্ত অধিক সোক্রিয়া?
A. -
B. 
C. 
D. 
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
A
```


## 8. benqa_10th-Chemistry_0336 (benqa)

Gold: `D`
Self-normalized parsed: ``; correct: `False`

Baseline parsed: `D`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
A \rightarrow CaCO_{3}(s) \xrightarrow{\Delta} CaO(s) + X(g) B \rightarrow 250 mL 0.2 molar NaCl drobon A-er 'X' gyasoti- i. CO_{2} ii. omlodhormi iii. bayu opeksha bhari nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
\rightarrow CaCO_{3}(s) \xrightarrow{\Delta} CaO(s) + X(g) B \rightarrow 250 mL 0.2 molar NaCl drobon A-er 'X' gyasoti- i. CO_{2} i. অম্লodhormi iii. bayu opeksha ভারী নিচের কোনোটি সোথিক?
A. ই ইই
B. ই ইইই
C. ই এ ইইই
D. , ইই ও ইইই
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
The given chemical reaction is:

\[
\text{CaCO}_3(s) \xrightarrow{\Delta} \text{CaO}(s) + X(g)
\]

From this, we know that calcium carbonate decomposes on heating to form calcium oxide and a gas \( X \). The gas \( X
```


## 9. benqa_10th-Math-II_0326 (benqa)

Gold: `C`
Self-normalized parsed: `A`; correct: `False`

Baseline parsed: `C`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
sin B = \sqrt{2} - cosB hole, B = kot?
A. \frac{\pi}{2}
B. \frac{\pi}{3}
C. \frac{\pi}{4}
D. \frac{\pi}{6}
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
= \sqrt{2} - cosB hole, B = kor?
A. frac{\pi}{2}
B. frac{\pi}{3}
C. frac{\pi}{4}
D. frac{\pi}{6}
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
The expression given is:

$$
\sqrt{2} - \cos B \quad \text{and} \quad B = ?
$$

We are to find the value of $ B $ such that this expression makes sense, and the options are:

A. $ \frac{\pi}{2} $
```


## 10. benqa_10th-Math-II_0347 (benqa)

Gold: `D`
Self-normalized parsed: ``; correct: `False`

Baseline parsed: `D`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
cos\left ( - \frac{35\pi}{6} \right ) er man kot?
A. - \frac{\sqrt{3}}{2}
B. - \frac{1}{2}
C. \frac{1}{2}
D. \frac{\sqrt{3}}{2}
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
\left ( - \frac{35\pi}{6} \right ) এর মান কোট?
A. Vfrac{\sqrt{3}}{2}
B. Manfrac{1}{2}
C. frac{1}{2}
D. frac{\sqrt{3}}{2}
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
The question asks for the value of $ \left( -\frac{35\pi}{6} \right) $ in terms of trigonometric values, specifically asking "কোট?" which seems to be a translation of "cotangent?" in Bengali.

So, we are to find the
```


## 11. benqa_10th-Physics_0036 (benqa)

Gold: `C`
Self-normalized parsed: ``; correct: `False`

Baseline parsed: `C`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
70 keji ojoner ekojon byokti 5 minite 100 m uchu pahare uthe, tar kshomota kot oyat? [g = 9.8 ms^{-2}]
A. 3500
B. 1400
C. 228.67
D. 0.14
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
১০y ojoner ekojon byokti 5 মিনিটে 100 m উঁচু paharে উঠে, তার kshomota kol oyat? [g = 9.8 ms^{-2}]
A. 
B. 
C. .67an
D. #
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
The question appears to be in a mix of Bengali and English, and there are some typographical or formatting errors (e.g., "১০y ojoner ekojon byokti", "kshomota kol oyat", "g = 9.8 ms^{-2}").
```


## 12. benqa_10th-Physics_0084 (benqa)

Gold: `D`
Self-normalized parsed: `D`; correct: `True`

Baseline parsed: `B`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
sthir obosthan theke somotborone bostur jekono somoyer beg bostur otikrant durotber-
A. somanupatik
B. borger somanupatik
C. borger byostanupatik
D. borgomuler somanupatik
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
অনুমান থেকে somotborone বোসতুর যেকোনো সোমবারের বেগ বোস্তুর অতিক্রান্ত দূরোত্বের-
A. উইকিউপাত্তে
B. Websiteপাইক
C. byঅস্টান্তুমটিক
D. বাংলার সোমালুপাতিক
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
D
```


## 13. benqa_10th-Physics_0280 (benqa)

Gold: `B`
Self-normalized parsed: `A`; correct: `False`

Baseline parsed: `B`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
tamar rodhokotb konoti?
A. 1.6 \times 10^{-8}\Omega m
B. 1.68 \times 10^{-8}\Omega m
C. 2.44 \times 10^{-8}\Omega m
D. 5.5 \times 10^{-8}\Omega m
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
রোধোকোত্ব কোনোটি?
A. 6 \times 10^{-8}\Omega m
B. 68 \times 10^{-8}\Omega m
C. 44 \times 10^{-8}\Omega m
D. 5 \times 10^{-8}\Omega m
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
A
```


## 14. benqa_12th-Biology-I_0042 (benqa)

Gold: `D`
Self-normalized parsed: `C`; correct: `False`

Baseline parsed: `D`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
saikaser prodhan mul nosht hooyar fole- i. osthanik mul srishti hoy ii. Anabaena dbara akrant hoy iii. er akriti samudrik probaler mot hoy nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
Er prodhan mul nosht hooyar fole- i. oস্থানিক মূল সৃষ্টি hoy ii. Anabaena dbara আক্রান্ত hoy iii. এর আকৃতি সামুদ্রিক প্রোবলের মোট হোয়া নিচের কোনোটি সোথিক?
A. ই ইই
B. ই ইইই
C. ই এ ইইই
D. , ইই, ও ইইই
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
C. ই এ ইইই
```


## 15. benqa_12th-Biology-I_0056 (benqa)

Gold: `A`
Self-normalized parsed: `A`; correct: `True`

Baseline parsed: `D`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
konotite haidothod thakote pare?
A. pata
B. ful
C. mul
D. kand
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
মোবাইলডোড থাকোতে পারে?
A. 
B. 
C. 
D. 
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
A
```


## 16. benqa_12th-Chemistry-II_0194 (benqa)

Gold: `A`
Self-normalized parsed: `A`; correct: `True`

Baseline parsed: `D`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
semikondaktor hisebe byobohrit hoy-
A. Ge
B. Zn
C. Cu
D. Al
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
Daktor hisebe byobohrit hoy-
A. 
B. 
C. 
D. 
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
A
```


## 17. benqa_12th-Chemistry-I_0140 (benqa)

Gold: `D`
Self-normalized parsed: ``; correct: `False`

Baseline parsed: `D`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
CaF_{2}-er somprikt joliy drobone floraid ayoner ghonomatra 0.00655 gL^{-1} hole CaF_{2} er drabyota gunofol kot hobe?
A. 3.7\times 10^{-13}
B. 2.048\times 10^{-10}
C. 3.7\times 10^{-12}
D. 2.048\times 10^{-11}
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
_{2}-er aluprikt joliy drobone floraid ayoner ghonomatra 0.00655 gL^{-1} hole CaF_{2} এর drabyota gunofol kol hobe?
A. 7\times 10^{-13}
B. 348\times 10^{-10}
C. 7\times 10^{-12}
D. 348\times 10^{-11}
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
The question appears to be asking for the solubility of calcium fluoride (CaF₂) in water, given that the fluoride ion concentration is 0.00655 g/L. However, the text contains several garbled or nonsensical phrases (like "er aluprikt", "gh
```


## 18. benqa_12th-Math-II_0230 (benqa)

Gold: `D`
Self-normalized parsed: ``; correct: `False`

Baseline parsed: `D`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
5 ekok durotbe A o B bindute kriyarot 9 ebong 5 ekok maner somantoral bolodboy- i. osodrish hole lobdhir man 4 ekok ii. sodrish ebong lobdhi C bindute kriyarot hole BC = \frac{45}{14} ekok iii. sodrish hole lobdhir man 14 ekok nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
কে দূরোতবে A o B বিন্দুতে ক্রিয়াআর্ot 9 ebong 5 ekok মানের somantoral bolodboy- i. osodrish hole lobdhir man 4 ekok ii. sodrish ebong lobdhi C bindute kriyarot hole BC = \frac{45}{14} Ekok ii. sodrish hole lobdhir man 14 ekok নিচের কোনোটি সোথিক?
A. ই ইই
B. ই ইইই
C. ই এ ইইই
D. , ইই ও ইইই
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
The given question is in a highly corrupted and nonsensical form, mixing Bengali and English with apparent typos, missing words, and unclear syntax. Phrases like "দূরোতবে A o B", "ক্রিয়াআর্ot 9 eb
```


## 19. benqa_12th-Physics-II_0046 (benqa)

Gold: `C`
Self-normalized parsed: `C`; correct: `True`

Baseline parsed: `D`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
ruddhotapiy poribortoner kshetre- i. hothat songghotit hoy ii. tapomatra sthir thake iii. enotropir poriborton shuny nicher konoti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
Oteby poribortoner kshetre- i. hothat songghotit hoy ii. tapoমাত্রা স্থির থাকে iii. enotropir poriborton shuny নিচের কোনোটি সোথিক?
A. ই ইই
B. ই এ ইইই
C. ই ইইই
D. , ইই ও ইইই
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
C. ই ইইই
```


## 20. benqa_8th-Science_0042 (benqa)

Gold: `B`
Self-normalized parsed: `B`; correct: `True`

Baseline parsed: `D`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
saban toirir mul upadan
A. esid
B. ksharok
C. lobon
D. glisarin
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
উন্মুক্ত মূল প্রজাতি
A. 
B. Rajshahi
C. 
D. Genin
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
B
```


## 21. benqa_8th-Science_0062 (benqa)

Gold: `D`
Self-normalized parsed: `B`; correct: `False`

Baseline parsed: `D`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
nicher konotike mutr toiriri karokhana hisebe obhihit kora jay?
A. fusofus
B. tbok
C. jokrit
D. britt
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
থেকে মূত্র তৈরিরই করোখানা হিসেবে অভিহিত কোরা যায়?
A. Cricinfo
B. Or
C. 
D. 
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
B. Or
```


## 22. benqa_8th-Science_0078 (benqa)

Gold: `C`
Self-normalized parsed: ``; correct: `False`

Baseline parsed: `C`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
alo kach theke bayu madhyome jaoyar somoy apoton kon 32^{\circ} hole protisorit roshniti madhyomer bibhedotol borabor jay. ekshetre protisoron koner man kot?
A. 0^{\circ}
B. 32^{\circ}
C. 90^{\circ}
D. 180^{\circ}
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
থেকে বয়ু মাধyome jaoyar aluoy apoton kon 32^{\circ} hole protisorit roshniti মাধyomer bibhedotol borabor jay. ekshetre protisoron কোণer man koঁড়া?
A. {\circ}
B. ^{\circ}
C. ^{\circ}
D. ^{\circ}
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
The question appears to be in a mix of Bengali and broken English, and the mathematical context is unclear. However, based on the structure and the mention of "protisoron kōṇer man kōḍḍā" (angle of incidence), and the reference to "32° hole protisorit
```


## 23. benqa_8th-Science_0202 (benqa)

Gold: `C`
Self-normalized parsed: `C`; correct: `True`

Baseline parsed: `A`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
sothik khady-shringkhol konoti?
A. ghas \rightarrow faitoplyangkoton \rightarrow juplangkoton
B. ju-plangkoton \rightarrow faitoplyangkoton\rightarrow chhotomas
C. faitoplangkoton \rightarrow ju-plangkoton \rightarrow chhotomachh
D. ghas\rightarrow byang\rightarrow bagh
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
খালি-শৃংকহোল কোনোটি?
A. Manrightarrow faitoplyangkoton \rightarrow juplangkoton
B. Plangkoton \rightarrow faitoplyangkoton\rightarrow chhotomas
C. Oplangkoton \rightarrow ju-plangkoton \rightarrow chhotomachh
D. rightarrow byang\rightarrow bagh
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
C
```

