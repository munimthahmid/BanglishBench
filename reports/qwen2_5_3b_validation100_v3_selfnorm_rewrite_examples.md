# Self-Normalization Rewrite Report

Items: `data/slices/validation_100_v3.jsonl`
Eval rows: `results/runs/qwen2_5_3b_validation100_v3_selfnorm/results/runs/qwen2_5_3b_validation100_v3_selfnorm.jsonl`
Examples exported: 18

Compare file: `results/analysis/qwen2_5_3b_validation100_v3_baseline_vs_selfnorm_items.csv`

## 1. banglamath_0229 (banglamath)

Gold: `1.5`
Self-normalized parsed: `1.5`; correct: `True`

Baseline parsed: `50%`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
150% ke doshomik bhognangshe prokash korole ki hoy
Return only the final answer.
```

**Model Rewrite**

```text
150% দশমিক ভগ্নাংশে প্রকাশ করলে কয়েকথা হবে
```

**Final Raw Output**

```text
1.5
```


## 2. banglamath_0233 (banglamath)

Gold: `৭ দিন`
Self-normalized parsed: `The correct answer is that 24 people can complete the same job in 7 days.`; correct: `True`

Baseline parsed: `6 jon lok ekoti kaj 28 dine korole 24 jon lok kot dine korobe = 10 jon lok`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
6 jon lok ekoti kaj 28 dine korole 24 jon lok kot dine korobe
Return only the final answer.
```

**Model Rewrite**

```text
৬ জন লোকের একটি কাজ ২৮ দিনে করেন ২৪ জন লোকের কাজ ২৪ দিনে করেন
```

**Final Raw Output**

```text
The correct answer is that 24 people can complete the same job in 7 days.
```


## 3. banglamath_0526 (banglamath)

Gold: `৩০ বর্গ মিটার`
Self-normalized parsed: `৩০ বর্গমিটার`; correct: `True`

Baseline parsed: `60`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
ekoti tribhujer bhumi 10 mitar o uchchota 6 mitar hole kshetrofol kot
Return only the final answer.
```

**Model Rewrite**

```text
একটি ত্রিভুজের ধারা ১০ মিটার ও উচ্চতা ৬ মিটার হলে ক্ষেত্রফল কত

১০ মিটার × ৬ মিটার ÷ ২ = ৩০ বর্গমিটার
```

**Final Raw Output**

```text
৩০ বর্গমিটার
```


## 4. benqa_10th-Biology_0143 (benqa)

Gold: `C`
Self-normalized parsed: `C`; correct: `True`

Baseline parsed: `B`; baseline correct: `False`
Change: `gain`

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
কোসমিক কিডনী ওকেজো হতে পারেন কি?  
A. দয়াবিতিস  
B. নেফ্রাটিস  
C. মারাত্মক দীর্ঘতা  
D. উচ্চ রক্তচাপ  
Answer with only A, B, C or D.  
C
```

**Final Raw Output**

```text
C
```


## 5. benqa_10th-Biology_0188 (benqa)

Gold: `A`
Self-normalized parsed: `A`; correct: `True`

Baseline parsed: `B`; baseline correct: `False`
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
তোরল জোয়াক তিনি কোয় প্রকার?
A. 2
B. 3
C. 4
D. 5
```

**Final Raw Output**

```text
The name "তোরল জোয়াক" does not correspond to any specific person or entity that I can identify from the options provided in the answer choices A, B, C, and D. Therefore, there isn't enough information to determine which option (A, B,
```


## 6. benqa_10th-Chemistry_0194 (benqa)

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
নিচের কোন মোটেয় সংখ্যা সকল উত্তরে এক অধিক?
A. O
B. P
C. N
D. F
Answer with only A, B, C or D.
```

**Final Raw Output**

```text
D
```


## 7. benqa_10th-Chemistry_0336 (benqa)

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
A. i o ii
```

**Final Raw Output**

```text
A. i o ii
```


## 8. benqa_10th-Math_0186 (benqa)

Gold: `C`
Self-normalized parsed: `C`; correct: `True`

Baseline parsed: `D`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
2x + y = 1 o x = - 4 somikoronodboyer somadhan bindu kon chortubhage obosthit?
A. 4th
B. 3rd
C. 2nd
D. 1st
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
2x + y = 1 সমীকরণ এবং x = -4 সমাধান বিন্দুতে কোন সংখ্যার উপর ভিত্তি করে প্রথম সংখ্যা শ্রেণী অবস্থিত?
A. 4তম
B. 3তম
C. 2তম
D. 1তম
Answer with only A, B, C, or D.
C
```

**Final Raw Output**

```text
C
```


## 9. benqa_10th-Math_0324 (benqa)

Gold: `A`
Self-normalized parsed: `A`; correct: `True`

Baseline parsed: `B`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
a = \sqrt{3} ebong b = \sqrt{12} hole nicher konoti omulod songkhya?
A. a + b
B. ab
C. \frac{a}{b}
D. \frac{b}{a}
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
A. a + b
```

**Final Raw Output**

```text
a + b
```


## 10. benqa_10th-Physics_0084 (benqa)

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
A. somanupatik
B. borger somanupatik
C. borger byostanupatik
D. borgomuler somanupatik
Answer with only A, B, C or D.
```

**Final Raw Output**

```text
D
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
কোনটিকে ঘাস গত্র বলে যায়?
A. সোলানেসি
B. সাইক্যেডেসি
C. মালোভেসি
D. পয়েসি
Answer with only A, B, C or D.
```

**Final Raw Output**

```text
D
```


## 12. benqa_12th-Chemistry-II_0194 (benqa)

Gold: `A`
Self-normalized parsed: `A`; correct: `True`

Baseline parsed: `B`; baseline correct: `False`
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
সেমিক্রন্ডাক্টর হিসেবে বোবহরিত যাহা- 
A. গি
B. সিন
C. কু
D. এল
Answer with only A, B, C or D.
```

**Final Raw Output**

```text
A
```


## 13. benqa_12th-Math-II_0230 (benqa)

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
5 দুর্বলতা অক্ষ A এবং B হতে একটি ক্রিয়া প্রয়োগ করে। এর মান 9 এবং 5 দুর্বলতা মানের সমান হলে। সূচনা করলে লব্ধ মান 4 দুর্বলতা হবে। ই. সূচনা এবং লব্ধ মানের সমান 14 দুর্বলতা নিয়ে ক্রিয়া BC প্রয়োগ করলে কোনো সমীকরণ হবে BC = \frac{45}{14} দুর্বলতা। ই.
```

**Final Raw Output**

```text
BC = \frac{45}{14} দুর্বলতা
```


## 14. benqa_12th-Math-I_0186 (benqa)

Gold: `A`
Self-normalized parsed: `A`; correct: `True`

Baseline parsed: `B`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
(-2, 3) bindute kendr ebong y-okshoke sporsh kore erup britter somikoron konoti?
A. x^{2} + y^{2} + 4x - 6y + 9 = 0
B. x^{2} + y^{2} - 4x + 6y + 9 = 0
C. x^{2} + y^{2} + 4x - 6y + 4 = 0
D. x^{2} + y^{2} - 4x + 6y + 4 = 0
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
A. x^2 + y^2 + 4x - 6y + 9 = 0
```

**Final Raw Output**

```text
The given equation \(x^2 + y^2 + 4x - 6y + 9 = 0\) represents a circle when rearranged into the standard form \((x-h)^2 + (y-k)^2 = r^2\). To find the center and radius of this circle,
```


## 15. benqa_12th-Math-I_0218 (benqa)

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
কোনটিই নয়।
A. c = a cosB + b cosA
B. b = c sinA + a sinC
C. Δ = ½ absinC
D. cosA = ½ (b² + c² - a²)/bc
```

**Final Raw Output**

```text
D. cosA = ½ (b² + c² - a²)/bc
```


## 16. benqa_12th-Math-I_0310 (benqa)

Gold: `B`
Self-normalized parsed: ``; correct: `False`

Baseline parsed: `B`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
\frac{d}{dx}(log_{10}x) er man konoti?
A. \frac{1}{x}
B. \frac{1}{x}log_{10}e
C. \frac{1}{x}log_{e}10
D. log_{10}e
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
B. \frac{1}{x}log_{10}e
```

**Final Raw Output**

```text
The given expression is already in its simplest form and does not require further simplification or rearrangement. Therefore, the final answer is:

\(\frac{1}{x}\log_{10}e\)
```


## 17. benqa_12th-Physics-II_0213 (benqa)

Gold: `D`
Self-normalized parsed: `D`; correct: `True`

Baseline parsed: `C`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
ruddhotapiy prokriyay ekoti adorsh gyaser chap o tapomatrar modhye sompork-
A. P^{\gamma - 1} = dhrubok
B. P^{\gamma} T^{\gama + 1} = dhrubok
C. P^{\gamma} T^{\gamma - 1} = dhrubok
D. P^{1 - \gamma} T^{\gamma} = dhrubok
Answer with only A, B, C, or D.
```

**Model Rewrite**

```text
P^{\gamma - 1} = dhrubok
A. P^{\gamma - 1} = dhrubok
B. P^{\gamma} T^{\gama + 1} = dhrubok
C. P^{\gamma} T^{\gamma - 1} = dhrubok
D. P^{1 - \gamma} T^{\gamma} = dhrubok
Answer with only A, B, C or D.
```

**Final Raw Output**

```text
D
```


## 18. benqa_8th-Science_0078 (benqa)

Gold: `C`
Self-normalized parsed: `C`; correct: `True`

Baseline parsed: `B`; baseline correct: `False`
Change: `gain`

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
আলো কাছে থেকে বয়স্ম মধ্যের সমুদ্রতীর পথের সমূহের মধ্যে 32° হলে প্রতিটি সূর্যনির্দেশকের উপর আলোর সৃষ্টির সময় সূর্যের উপর দৃষ্টির মধ্যে বিভাজন কতটুকু হবে? এই সময়ে প্রতিটি সূর্যনির্দেশকের কোন অংশে মন করা উচিত?
A. 0°
B. 32°
C. 90°
D. 180°
Answer with
```

**Final Raw Output**

```text
C. 90°
```

