# Self-Normalization Rewrite Report

Items: `data/slices/validation_100_v3.jsonl`
Eval rows: `results/runs/qwen2_5_3b_validation100_v3_extnorm/results/runs/qwen2_5_3b_validation100_v3_extnorm.jsonl`
Examples exported: 21

Compare file: `results/analysis/qwen25_validation100_v3_baseline_vs_extnorm_items_reparsed.csv`

## 1. benqa_10th-Biology_0215 (benqa)

Gold: `B`
Self-normalized parsed: `B`; correct: `True`

Baseline parsed: `D`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
C_{6}H_{12}O_{6}\xarrowright{enojaim}C_{3}H_{4}O_{3} uddipoker prokriyati- i. sobat o obat shbosoner prothom dhap ii. kosher maitokondriyay ghote thake iii. ete nit onu ATP utoponn hoy nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
{6}H_{12}O_{6}\xarrowright{enojaim}C_{3}H_{4}O_{3} uddipoker prokriyati- i. sobat o obat shbosoner prothom dhap ii. কোষের মাইtokondriy pakte thake iii. ete nit onu ATP utoponn hoy নিচের konoti sothik?
A. ই ইই
B. ই ইইই
C. ই এ ইইই
D. , ইই ও ইইই
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
B
```


## 2. benqa_10th-Chemistry_0194 (benqa)

Gold: `D`
Self-normalized parsed: `D`; correct: `True`

Baseline parsed: `C`; baseline correct: `False`
Change: `gain`

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
D.
```


## 3. benqa_10th-Chemistry_0336 (benqa)

Gold: `D`
Self-normalized parsed: `B`; correct: `False`

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
B
```


## 4. benqa_10th-Math-II_0347 (benqa)

Gold: `D`
Self-normalized parsed: `D`; correct: `True`

Baseline parsed: `B`; baseline correct: `False`
Change: `gain`

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
D
```


## 5. benqa_10th-Physics_0280 (benqa)

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


## 6. benqa_12th-Biology-II_0122 (benqa)

Gold: `A`
Self-normalized parsed: `A`; correct: `True`

Baseline parsed: `C`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
hritopinder olinder dayastoler somoyokal kot sekend?
A. 0.7
B. 0.5
C. 0.3
D. 0.1
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
Oপিঙ্কের অলিনদের ডায়াসটোলের সোমবারোকাল কোর সেকেন্ড?
A. |-
B. 5
C. 1
D. 
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
A. |-
The question seems to be asking about a specific time measurement related to the diastolic pressure of an artery on a Monday evening. However, the provided options do not match the expected format for such a question, and the reference to "Oপিঙ্কের অলিন
```


## 7. benqa_12th-Biology-II_0247 (benqa)

Gold: `B`
Self-normalized parsed: `C`; correct: `False`

Baseline parsed: `B`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
P \rightarrow DdEe \times ddEE uddipoke ullikhit kros dbara muk o bodhir sontan hobar sombhabona kot?
A. 25%
B. 50%
C. 75%
D. 100%
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
\rightarrow DdEe \times ddEE uddipoke ullikhit kros দ্বারা মুক ও বোধীর সোntan হোবার সোম্ভবোনা কোট?
A. %
B. 
C. =
D. 
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
C.
```


## 8. benqa_12th-Biology-II_0287 (benqa)

Gold: `B`
Self-normalized parsed: `B`; correct: `True`

Baseline parsed: `D`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
protin poripake ongsh ney konoti? i. peposin ii. ojamailej iii. karboksipepotaid nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
Baipake ongsh ney konoti? i. peposin ii. otomilej iii. Parisoksipepotaid নিচের konoti sothik?
A. ই ইই
B. ই ইইই
C. ই এ ইইই
D. , ইই, ও ইইই
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
B
```


## 9. benqa_12th-Biology-I_0042 (benqa)

Gold: `D`
Self-normalized parsed: `B`; correct: `False`

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
B
```


## 10. benqa_12th-Biology-I_0056 (benqa)

Gold: `A`
Self-normalized parsed: `A`; correct: `True`

Baseline parsed: `B`; baseline correct: `False`
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


## 11. benqa_12th-Biology-I_0277 (benqa)

Gold: `D`
Self-normalized parsed: `D`; correct: `True`

Baseline parsed: `B`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
konotike ghas gotr bola hoy?
A. solanesi
B. saikyadesi
C. malobhesi
D. poyesi
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
ঘাস গোত্র বোলা হোয়া?
A. Eti
B. আসাে
C. Iu.
D. Eti
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
D. Eti
```


## 12. benqa_12th-Biology-I_0283 (benqa)

Gold: `A`
Self-normalized parsed: `A`; correct: `True`

Baseline parsed: `D`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
penper ring spot roger lokshon holo- i. patar botay pani bheja sobuj dag dekha jay ii. penper mishtota hras pay iii. foler akar bor hoy nicher konoti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
রিং স্পোট রোগের লোকশোন হোলো- ই. পাতার বোটায় পানি ভেজা সোবুজ দাগ দেখা যায় ইই. পেনপের মিশটোটা হ্রাস পায় ইii. foler আকার বোর হোয়ে নিচের কোনোটি সোথিক?
A. ই ইই
B. ই এ ইইই
C. ই ইইই
D. , ইই, ও ইইই
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
A. ই ইই
```


## 13. benqa_12th-Chemistry-II_0013 (benqa)

Gold: `C`
Self-normalized parsed: `B`; correct: `False`

Baseline parsed: `C`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
ghumer oushodh hisebe byobohrit hoy konoti?
A. foromalodihaid
B. ojasitalodihaid
C. pyaralodihaid
D. metalodihaid
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
ঔষধ হিসেবে byobohrit hoy konoti?
A. ফেডিলুল
B. উইকিউপাত্তে
C. Aroldilum
D. –
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
B
```


## 14. benqa_12th-Chemistry-I_0174 (benqa)

Gold: `A`
Self-normalized parsed: `A`; correct: `True`

Baseline parsed: `D`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
bhinegar- i. khadyer byakoteriya dhbongs kora ii. khabarer ruchi briddhi kore iii. rokt sonchalon komay nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
Gar- i. khadyer byakoteriya Chalongs kora ii. খাবারের রুচি বৃদ্ধি কোরে iii. rokt sonchalon komay নিচের কোনোটি সোথিক?
A. ই ইই
B. ই ইইই
C. ই এ ইইই
D. , ইই ও ইইই
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
A. ই ইই
```


## 15. benqa_12th-Math-II_0230 (benqa)

Gold: `D`
Self-normalized parsed: `B`; correct: `False`

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
B
```


## 16. benqa_12th-Math-I_0218 (benqa)

Gold: `A`
Self-normalized parsed: `D`; correct: `False`

Baseline parsed: `A`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
jekono tribhuj ABC er kshetre nicher konoti sothik?
A. c = acosB + bcosA
B. b = csinA + asinC
C. \Delta = \frac{1}{2} abcosC
D. cosA = \frac{b^{2} + c^{2} + a^{2}}{2bc}
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
ABC er kshetre নিচের কোনোটি সোথিক?
A. acosB + bcosA
B. = csinA + asinC
C. Delta = \frac{1}{2} abcosC
D. A = \frac{b^{2} + c^{2} + a^{2}}{2bc}
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
D
```


## 17. benqa_12th-Physics-I_0133 (benqa)

Gold: `C`
Self-normalized parsed: `A`; correct: `False`

Baseline parsed: `C`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
\frac{3}{2} mol gyaser jony adorsh gyas somikoron hobe konoti?
A. 3PV = 2RT
B. 2PV = \frac{1}{3} RT
C. 2PV = 3RT
D. \frac{PV}{RT}=\frac{2}{3}
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
frac{3}{2} mol gyaser jony adorsh gyas aluikoron hobe konoti?
A. V = 2৪১n
B. V = \frac{1}{3} RT
C. V = 3৪১
D. frac{PV}{RT}=\frac{2}{3}
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
A
```


## 18. benqa_12th-Physics-I_0214 (benqa)

Gold: `B`
Self-normalized parsed: `A`; correct: `False`

Baseline parsed: `B`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
sthir ayotone 0^{\circ}C tapomatray kono gyaser chap dbigun korole er churant tapomatra hobe-
A. 27^{\circ}C
B. 273^{\circ}C
C. 300^{\circ}C
D. 546^{\circ}C
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
Orone 0^{\circ}C tapomatray kono gyaser chap dbigun কোরোলে এর চূর্ণ তাপোমাত্রা হোবে-
A. ^{\circ}C
B. ^{\circ}C
C. ^{\circ}C
D. ^{\circ}C
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
A. ^{\circ}C
```


## 19. benqa_12th-Physics-I_0253 (benqa)

Gold: `A`
Self-normalized parsed: `A`; correct: `True`

Baseline parsed: `D`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
mohakorsh sutr byobohar kore je somost kaj kora sombhob- i. prakritik gyas uttolon ii. bibhinn khonij podarth uttolon iii. bhu-gorbhosth tapoghotit shokti uttolon nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
পেঁয়াজ সূত্র byobohar কোরে যে সোমোস্ট কাজ কোরা সোম্ভোব- ই. প্রাকৃতিক gyas uttolon ii. বিভিন্ন খোনিজ পোডারth uttolon ii. ভূ-গোরভোস্থ তাপোহোচিত শোকটি উত্তোলোন নিচের কোনোটি সোথিক?
A. ই ইই
B. ই ইইই
C. ই এ ইইই
D. , ইই ও ইইই
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
A. ই ইই
```


## 20. benqa_8th-Math_0072 (benqa)

Gold: `B`
Self-normalized parsed: `C`; correct: `False`

Baseline parsed: `B`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
779 songkhyati kon bijogonitiy rashir 111 tom pod?
A. 7k - 2
B. 7k + 2
C. 5555k + 224
D. 777k + 2
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
songkhyati kon bijogionitiy rashir 111 tom pod?
A. - 2
B. |-
C. ৩২k + 224
D. No + 2
Fer with only A, B, C, or D.
```

**Final Raw Output**

```text
C. ৩২k + 224
```


## 21. benqa_8th-Science_0202 (benqa)

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

