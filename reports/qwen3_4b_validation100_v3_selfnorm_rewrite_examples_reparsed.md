# Self-Normalization Rewrite Report

Items: `data/slices/validation_100_v3.jsonl`
Eval rows: `results/runs/qwen3_4b_validation100_v3_selfnorm/results/runs/qwen3_4b_validation100_v3_selfnorm.jsonl`
Examples exported: 23

Compare file: `results/analysis/qwen3_4b_validation100_v3_baseline_vs_selfnorm_items_reparsed.csv`

## 1. banglamath_0229 (banglamath)

Gold: `1.5`
Self-normalized parsed: `{১৫০% কে দোস্তিক ভোগন্ধে প্রকাশ করলে কোনও মানে নেই। এটি এক`; correct: `False`

Baseline parsed: `150% ke doshomik bhognangshe prokash korole ki hoy, tai 150% = 150/100 = 1.5`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
150% ke doshomik bhognangshe prokash korole ki hoy
Return only the final answer.
```

**Model Rewrite**

```text
১৫০% কে দোস্তিক ভোগন্ধে প্রকাশ করলে কি হয়
```

**Final Raw Output**

```text
{১৫০% কে দোস্তিক ভোগন্ধে প্রকাশ করলে কোনও মানে নেই। এটি এক
```


## 2. benqa_10th-Biology_0143 (benqa)

Gold: `C`
Self-normalized parsed: `D`; correct: `False`

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
আকোসমিক কিডোনি ওকেজো হোতে পারে কোন করণে?  
A. ডায়াবেটিস  
B. নেফ্রাইটিস  
C. মারাটমোক দায়োরিয়া  
D. উচ্চ রোক্তচাপ  
Answer with only A, B, C, or D.
```

**Final Raw Output**

```text
D
```


## 3. benqa_10th-Chemistry_0194 (benqa)

Gold: `D`
Self-normalized parsed: ``; correct: `False`

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
নিচের কোন মুলতি ওঠিক সক্রিয়?  
A. O  
B. P  
C. N  
D. F
```

**Final Raw Output**

```text
প্রশ্ন: নিচের কোন মুলতি ওঠিক সক্রিয়?

"ওঠিক" শব্দটি বাংলা ভা�
```


## 4. benqa_10th-Chemistry_0336 (benqa)

Gold: `D`
Self-normalized parsed: `A`; correct: `False`

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
A → CaCO₃(s) →Δ→ CaO(s) + X(g) B → 250 mL 0.2 মোলার NaCl দ্রবণ A-এর 'X' গ্যাসটি কোনটি?  
i. CO₂  
ii. অম্ল দ্রবণ  
iii. বায়ু প্রসারিত ভারি  
নিচের কোনটি সঠিক?  
A. i এবং ii  
B. i এবং iii  
C. ii এবং iii  
D. i, ii এবং iii
```

**Final Raw Output**

```text
The reaction given is:

A → CaCO₃(s) →Δ→ CaO(s) + X(g)

This is the thermal decomposition of calcium carbonate:

CaCO₃(s) →Δ→ CaO(s) + CO₂(g)

So, X(g) is **CO₂**.

Now,
```


## 5. benqa_10th-Math-II_0347 (benqa)

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
cos\left ( - \frac{35\pi}{6} \right ) এর মান কত?  
A. - \frac{\sqrt{3}}{2}  
B. - \frac{1}{2}  
C. \frac{1}{2}  
D. \frac{\sqrt{3}}{2}
```

**Final Raw Output**

```text
We are asked to find the value of:

$$
\cos\left( -\frac{35\pi}{6} \right)
$$

---

### Step 1: Use the even property of cosine
Cosine is an **even function**, so:

$$
\cos(-\theta) =
```


## 6. benqa_10th-Physics_0036 (benqa)

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
70 কেজি ওজনের একজন ব্যক্তি 5 মিনিট 100 মি উঠে পাহারে উঠে, তার ক্ষমতা কত ওয়াট? [g = 9.8 ms^{-2}]  
A. 3500  
B. 1400  
C. 228.67  
D. 0.14
```

**Final Raw Output**

```text
We are given:

- Mass of the person, \( m = 70 \) kg  
- Distance climbed, \( h = 100 \) m  
- Time taken, \( t = 5 \) minutes = \( 5 \times 60 = 300 \) seconds
```


## 7. benqa_10th-Physics_0045 (benqa)

Gold: `A`
Self-normalized parsed: `A`; correct: `True`

Baseline parsed: `D`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
kon nirdisht bhorer kono bostur beg dbigun korole gotishokti kot gun hobe?
A. charogun
B. dbigun
C. ordhek
D. soman
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
কোন নির্দেশিত ভরের কোনো বস্তু বেগ দিয়ে কোরলে গতিশক্তি কত গুন হবে?  
A. চার গুন  
B. বেগ গুন  
C. অর্ধেক  
D. সমান  
Answer with only A, B, C, or D.
```

**Final Raw Output**

```text
A
```


## 8. benqa_10th-Physics_0280 (benqa)

Gold: `B`
Self-normalized parsed: ``; correct: `False`

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
টামার রোধকত কোনটি?  
A. 1.6 × 10⁻⁸ Ω m  
B. 1.68 × 10⁻⁸ Ω m  
C. 2.44 × 10⁻⁸ Ω m  
D. 5.5 × 10⁻⁸ Ω m
```

**Final Raw Output**

```text
টামার রোধকত হল 1.68 × 10⁻⁸ Ω m।

সঠিক উত্তর: B. 1.68 × 10⁻⁸ Ω m

Final Answer
```


## 9. benqa_12th-Biology-II_0034 (benqa)

Gold: `B`
Self-normalized parsed: `B`; correct: `True`

Baseline parsed: `D`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
kshudrantrer kshudr ongsh konoti?
A. pailoras
B. diodenam
C. jejunam
D. iliyam
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
ক্ষুদ্রান্তর ক্ষুদ্র অন্গশ কোনটি?  
A. পাইলোরাস  
B. ডায়োডেনাম  
C. জেজুনাম  
D. ইলিয়াম
```

**Final Raw Output**

```text
ক্ষুদ্রান্তর ক্ষুদ্র অন্গশ কোনটি?  
A. পাইলোরাস  
B. ডায়োডেনা�
```


## 10. benqa_12th-Biology-II_0049 (benqa)

Gold: `C`
Self-normalized parsed: `C`; correct: `True`

Baseline parsed: `D`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
otitis midiya' kon ongger rog?
A. chokh
B. nak
C. kan
D. gola
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
মিডিয়া অ্যাটিস কোন রোগ?  
A. চোখ  
B. নাক  
C. কান  
D. গোলা  
Answer with only A, B, C, or D.
```

**Final Raw Output**

```text
C
```


## 11. benqa_12th-Biology-I_0042 (benqa)

Gold: `D`
Self-normalized parsed: ``; correct: `False`

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
সাইকেসার প্রধান মুল নোস্ট হয় ফোলে- i. অস্থানিক মুল স্রষ্টি হয় ii. অনাবাএনা দ্বারা অক্রান্ত হয় iii. এর আকৃতি সমুদ্রিক প্রবলের মোট হয় নিচের কোনটি সঠিক সংযোগ হয়?  
A. i ও ii  
B. i ও iii  
C. ii ও iii  
D. i, ii, o iii
```

**Final Raw Output**

```text
The given question appears to be in a mix of Bengali and possibly corrupted or misformatted English. The content seems to refer to a geological or biological concept, possibly about "sikecer" (possibly a typo or misrendering of "skeleton" or "seafloor" related term), and mentions "
```


## 12. benqa_12th-Biology-I_0277 (benqa)

Gold: `D`
Self-normalized parsed: ``; correct: `False`

Baseline parsed: `D`; baseline correct: `True`
Change: `loss`

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
কোনটিকে গাছ গোট্র বলা হয়?  
A. সোলানেসি  
B. সাইক্যাদেসি  
C. মালোবহেসি  
D. পয়েসি
```

**Final Raw Output**

```text
গাছ গোট্র বলা হয় সাইক্যাদেসি।

সঠিক উত্তর: B. সাইক্যাদেসি
```


## 13. benqa_12th-Chemistry-II_0194 (benqa)

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
সেমিকন্ডাক্টর হিসেবে ব্যবহার করা হয়-  
A. Ge  
B. Zn  
C. Cu  
D. Al
```

**Final Raw Output**

```text
সেমিকন্ডাক্টর হিসেবে ব্যবহার করা হয় -  
A. Ge  

স্পষ্ট করে বলা যায় �
```


## 14. benqa_12th-Chemistry-I_0140 (benqa)

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
CaF_{2}-এর সম্পূর্ণ ক্ষুদ্র জলীয় দ্রবণে ফ্লোরাইড আয়নের গ্রাম প্রতি লিটার 0.00655 gL^{-1} হলে CaF_{2} এর দ্রব্যতা গুণোফল কত হবে?  
A. 3.7\times 10^{-13}  
B. 2.048\times 10^{-10}  
C. 3.7\times 10^{-12}  
D. 2.048\times 10^{-11}
```

**Final Raw Output**

```text
CaF₂ এর দ্রব্যতা গুণোফল (solubility product, Ksp) হল এর দ্রবণে দ্রবীভূত হওয়া
```


## 15. benqa_12th-Chemistry-I_0286 (benqa)

Gold: `C`
Self-normalized parsed: `C`; correct: `True`

Baseline parsed: `D`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
urbor matir jony otyanukul pH kot?
A. 3.0-4
B. 6-May
C. 8-Jul
D. 11-Oct
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
আর্বর মাটির জন্য অত্যন্ত কোটি pH কত?  
A. 3.0-4  
B. 6-5  
C. 8-7  
D. 11-10  
Answer with only A, B, C, or D.
```

**Final Raw Output**

```text
C
```


## 16. benqa_12th-Math-II_0230 (benqa)

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
5 একক দুরোত্বে A ও B বিন্দুতে ক্রিয়ারত 9 এবং 5 একক মানের সমান্তর বলোদবয়- i. সোড়িষ্ট হলে লোবদ্ধির মান 4 একক ii. সোড়িষ্ট এবং লোবদ্ধি C বিন্দুতে ক্রিয়ারত হলে BC = \frac{45}{14} একক iii. সোড়িষ্ট হলে লোবদ্ধির মান 14 একক নিচের কোনটি সঠিক?  
A. i o ii  
B. i o iii  
C
```

**Final Raw Output**

```text
The question appears to contain a mix of incorrect or non-standard terminology such as "সোড়িষ্ট", "লোবদ্ধি", and "সমান্তর বলোদবয়", which are not standard physics terms in
```


## 17. benqa_12th-Math-I_0383 (benqa)

Gold: `D`
Self-normalized parsed: ``; correct: `False`

Baseline parsed: `D`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
\frac{d}{dx} (log_{5}x) = kot?
A. \frac{1}{x}
B. \frac{1}{x}log_{e}5
C. \frac{1}{5 lnx}
D. \frac{1}{x ln5}
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
\frac{d}{dx} (log_{5}x) = kot?  
A. \frac{1}{x}  
B. \frac{1}{x}log_{e}5  
C. \frac{1}{5 lnx}  
D. \frac{1}{x ln5}
```

**Final Raw Output**

```text
We are asked to evaluate the derivative:

$$
\frac{d}{dx} (\log_5 x)
$$

### Step 1: Use the change of base formula
$$
\log_5 x = \frac{\ln x}{\ln 5}
$$

### Step 2: Different
```


## 18. benqa_12th-Physics-II_0292 (benqa)

Gold: `C`
Self-normalized parsed: `C`; correct: `True`

Baseline parsed: `D`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
drishyoman bornalir toronggodoirghyer bistriti-
A. 2000 \AA theke 3000 \AA poryont
B. 3000 \AA theke 4000 \AA poryont
C. 4000 \AA theke 8000 \AA poryont
D. 8000 \AA theke 12000 \AA poryont
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
দ্রিশ্যমান বর্নালির তরঙ্গদৈর্ঘ্যের বিস্তার হয়—  
A. 2000 \AA থেকে 3000 \AA পর্যন্ত  
B. 3000 \AA থেকে 4000 \AA পর্যন্ত  
C. 4000 \AA থেকে 8000 \AA পর্যন্ত  
D. 8000 \AA থেকে 12000 \AA পর্যন্ত  
উত্তর: C
```

**Final Raw Output**

```text
C
```


## 19. benqa_12th-Physics-I_0133 (benqa)

Gold: `C`
Self-normalized parsed: `C`; correct: `True`

Baseline parsed: `D`; baseline correct: `False`
Change: `gain`

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
\frac{3}{2} মোল গ্যাসের জন্য আদর্শ গ্যাসের সমীকরণ হবে কোনটি?  
A. 3PV = 2RT  
B. 2PV = \frac{1}{3} RT  
C. 2PV = 3RT  
D. \frac{PV}{RT}=\frac{2}{3}  
Answer with only A, B, C, or D.
```

**Final Raw Output**

```text
C
```


## 20. benqa_8th-Math_0031 (benqa)

Gold: `D`
Self-normalized parsed: ``; correct: `False`

Baseline parsed: `D`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
ekoti garir chakar poridhi 5.15 mitar hole, chakatir byas kot?
A. 0.82 mitar
B. 0.96 mitar
C. 1.28 mitar
D. 1.64 mitar
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
একটি গারির চকর পরিধি 5.15 মিটার হলে, চকতির ব্যাস কত?  
A. 0.82 মিটার  
B. 0.96 মিটার  
C. 1.28 মিটার  
D. 1.64 মিটার
```

**Final Raw Output**

```text
গারির চকর পরিধি (Circumference) = 5.15 মিটার

চকরের পরিধি নির্ণয়ের সূত্র:
```


## 21. benqa_8th-Science_0062 (benqa)

Gold: `D`
Self-normalized parsed: ``; correct: `False`

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
নিচের কোনটাই মুট্র তোড়িরি করক্ষান হিসেবে অবদ্ধ করা যায়?  
A. fusofus  
B. tbok  
C. jokrit  
D. britt
```

**Final Raw Output**

```text
মুট্র তোড়িরি করক্ষান হিসেবে অবদ্ধ করা যায় না কোনও প্রতিটি
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
আলো কাচ থেকে বায়ু মাঝে যায় এর সময় আপটন কোণ 32^{\circ} হলে প্রতিসরণ রোশনিতি মাঝে বিভেদিত হয়। একস্থানে প্রতিসরণ কোণ কত?  
A. 0^{\circ}  
B. 32^{\circ}  
C. 90^{\circ}  
D. 180^{\circ}
```

**Final Raw Output**

```text
প্রতিসরণ কোণ ও আপটন কোণের মধ্যে সম্পর্ক প্রতিসরণ রোশনিতি (Snell's Law
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
সোথিক খাদ্য-শ্রেণীকোল কোনটি?  
A. গাছ \rightarrow ফেইটোপলাঙ্কটন \rightarrow জুপলাঙ্কটন  
B. জু-পলাঙ্কটন \rightarrow ফেইটোপলাঙ্কটন \rightarrow চহটোমাস  
C. ফেইটোপলাঙ্কটন \rightarrow জু-পলাঙ্কটন \rightarrow চহটোমাচ্চ  
D. গাছ \rightarrow ব্যাঙ্গ \rightarrow বাগহ  
Answer with only A, B, C, or D.
```

**Final Raw Output**

```text
C
```

