# Script-Gap Examples: `banglish_drop_vs_bangla_english`

Source gaps: `results/analysis/qwen3_validation200_v3_script_gap_items_reparsed.csv`
Items: `data/slices/validation_200_v3.jsonl`
Examples exported: 24

## 1. banglamath_0229 (banglamath, short_answer)

Gold: `1.5`

**Bangla Prompt**

```text
১৫০% কে দশমিক ভগ্নাংশে প্রকাশ করলে কী হয়
Return only the final answer.
```

Bangla parsed: `1.5`; correct: `True`

**Banglish Prompt**

```text
150% ke doshomik bhognangshe prokash korole ki hoy
Return only the final answer.
```

Banglish parsed: `150`; correct: `False`

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

Bangla parsed: `25 টাকা 125 টাকার শতকরা = (25 / 125) × 100 = 20%`; correct: `True`

**Banglish Prompt**

```text
25 taka 125 takar shotokora kot
Return only the final answer.
```

Banglish parsed: `invalid input`; correct: `False`

**English Prompt**

```text
25 Taka is what percent of 125 Taka?
Return only the final answer.
```

English parsed: `20%`; correct: `True`

## 3. banglamath_1697 (banglamath, short_answer)

Gold: `70`

**Bangla Prompt**

```text
৩০ কে ১/২ দিয়ে ভাগ করে ১০ যোগ করলে কত হয়?
Return only the final answer.
```

Bangla parsed: `70`; correct: `True`

**Banglish Prompt**

```text
30 ke 1/2 diye bhag kore 10 jog korole kot hoy?
Return only the final answer.
```

Banglish parsed: `600`; correct: `False`

**English Prompt**

```text
Divide 30 by ½ and add 10. What is the result?
Return only the final answer.
```

English parsed: `70`; correct: `True`

## 4. benqa_10th-Biology_0156 (benqa, mcq)

Gold: `C`

**Bangla Prompt**

```text
আমিষে শতকরা কত ভাগ নাইট্রোজেন বিদ্যমান
A. 12
B. 14
C. 16
D. 18
Answer with only A, B, C, or D.
```

Bangla parsed: `C`; correct: `True`

**Banglish Prompt**

```text
amishe shotokora kot bhag naitrojen bidyoman
A. 12
B. 14
C. 16
D. 18
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
What percentage of Nitrogen is present in protein?
A. 12
B. 14
C. 16
D. 18
Answer with only A, B, C, or D.
```

English parsed: `C`; correct: `True`

## 5. benqa_10th-Chemistry_0132 (benqa, mcq)

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

## 6. benqa_10th-Chemistry_0322 (benqa, mcq)

Gold: `B`

**Bangla Prompt**

```text
কোনটির অণুতে দ্বি-বন্ধন বিদ্যমান?
A. হাইড্রোজেন
B. অক্সিজেন
C. নাইট্রোজেন
D. ক্লোরিন
Answer with only A, B, C, or D.
```

Bangla parsed: `B`; correct: `True`

**Banglish Prompt**

```text
konotir onute dbi-bondhon bidyoman?
A. haidrojen
B. oksijen
C. naitrojen
D. klorin
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
Which molecule contains double bond?
A. Hydrogen
B. Oxygen
C. Nitrogen
D. Chlorine
Answer with only A, B, C, or D.
```

English parsed: `B`; correct: `True`

## 7. benqa_10th-Chemistry_0374 (benqa, mcq)

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

Banglish parsed: `D`; correct: `False`

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

## 8. benqa_10th-Math_0044 (benqa, mcq)

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

## 9. benqa_10th-Math_0271 (benqa, mcq)

Gold: `D`

**Bangla Prompt**

```text
স্থূলকোণী ত্রিভুজের স্থূলকোণ ছাড়া বাকি কোণ দুটি কত হলে ত্রিভুজ অংকন সম্ভব?
A. 30\degree ও 60\degree
B. 40\degree ও 50\degree
C. 45\degree ও 45\degree
D. 50\degree ও 30\degree
Answer with only A, B, C, or D.
```

Bangla parsed: `D`; correct: `True`

**Banglish Prompt**

```text
sthulokoni tribhujer sthulokon chhara baki kon duti kot hole tribhuj ongkon sombhob?
A. 30\degree o 60\degree
B. 40\degree o 50\degree
C. 45\degree o 45\degree
D. 50\degree o 30\degree
Answer with only A, B, C, or D.
```

Banglish parsed: `C`; correct: `False`

**English Prompt**

```text
To draw a triangle which is the value of rest two angles except obtuse angle of obtuse angle triangle?
A. 30\degree and 60\degree
B. 40\degree and 50\degree
C. 45\degree and 45\degree
D. 50\degree and 30\degree
Answer with only A, B, C, or D.
```

English parsed: `D`; correct: `True`

## 10. benqa_10th-Physics_0021 (benqa, mcq)

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

Banglish parsed: `D`; correct: `False`

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

## 11. benqa_10th-Physics_0045 (benqa, mcq)

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

## 12. benqa_10th-Physics_0150 (benqa, mcq)

Gold: `B`

**Bangla Prompt**

```text
কোনটি স্কেলার রাশি?
A. বেগ
B. দ্রুতি
C. সরণ
D. ত্বরণ
Answer with only A, B, C, or D.
```

Bangla parsed: `B`; correct: `True`

**Banglish Prompt**

```text
konoti skelar rashi?
A. beg
B. druti
C. soron
D. tboron
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
Which one is the scalar quantity?
A. Velocity
B. Speed
C. Displacement
D. Acceleration
Answer with only A, B, C, or D.
```

English parsed: `B`; correct: `True`

## 13. benqa_10th-Physics_0198 (benqa, mcq)

Gold: `D`

**Bangla Prompt**

```text
নিচের কোন রাশিগুলো ভেক্টর রাশি?
A. দ্রুতি, কাজ ও বেগ
B. তড়িৎ বিভব, সরণ ও ত্বরণ
C. দ্রুতি, সরণ ও বেগ
D. ভরবেগ, সরণ ও ওজন
Answer with only A, B, C, or D.
```

Bangla parsed: `D`; correct: `True`

**Banglish Prompt**

```text
nicher kon rashigulo bhektor rashi?
A. druti, kaj o beg
B. torit bibhob, soron o tboron
C. druti, soron o beg
D. bhorobeg, soron o ojon
Answer with only A, B, C, or D.
```

Banglish parsed: `C`; correct: `False`

**English Prompt**

```text
Which of the following are vector quantities?
A. Speed, work and velocity
B. Elecr = trtc potential, displacement and acceleration
C. Speed, displacement and velocity
D. Momentumn, displacement and Weight
Answer with only A, B, C, or D.
```

English parsed: `D`; correct: `True`

## 14. benqa_12th-Biology-II_0179 (benqa, mcq)

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

Bangla parsed: `A`; correct: `True`

**Banglish Prompt**

```text
rokt jomat bandhote kon dhatob ayon sohayota kore?
A. Ca^{++}
B. Mg^{++}
C. Cu^{++}
D. Fe^{++}
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

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

## 15. benqa_12th-Biology-II_0287 (benqa, mcq)

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

## 16. benqa_12th-Biology-I_0077 (benqa, mcq)

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

Bangla parsed: `C`; correct: `True`

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

## 17. benqa_12th-Biology-I_0160 (benqa, mcq)

Gold: `B`

**Bangla Prompt**

```text
ট্রোফোজয়েট \rightarrow সিগনেট রিং \rightarrow A \rightarrow সাইজন্ট \rightarrow মেরোজয়েট A ধাপে নিচের কোন পদার্থটি তৈরি হয়?
A. হিমোলাইসিন
B. হিমোজয়েন
C. লাইসোলেসিথিন
D. পাইরোজেন
Answer with only A, B, C, or D.
```

Bangla parsed: `B`; correct: `True`

**Banglish Prompt**

```text
trofojoyet \rightarrow sigonet ring \rightarrow A \rightarrow saijont \rightarrow merojoyet A dhape nicher kon podarthoti toiri hoy?
A. himolaisin
B. himojoyen
C. laisolesithin
D. pairojen
Answer with only A, B, C, or D.
```

Banglish parsed: `D`; correct: `False`

**English Prompt**

```text
Trophozoite \rightarrow Signet ring \rightarrow A \rightarrow Schizent \rightarrow Merozoite Which of the following substance is formed in step A?
A. Haemolysin
B. Haemozoin
C. Lysolecithin
D. Pyrogen
Answer with only A, B, C, or D.
```

English parsed: `B`; correct: `True`

## 18. benqa_12th-Biology-I_0265 (benqa, mcq)

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

Bangla parsed: `A`; correct: `True`

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

## 20. benqa_12th-Chemistry-II_0013 (benqa, mcq)

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
ghumer oushodh hisebe byobohrit hoy konoti?
A. foromalodihaid
B. ojasitalodihaid
C. pyaralodihaid
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

## 21. benqa_12th-Chemistry-II_0054 (benqa, mcq)

Gold: `A`

**Bangla Prompt**

```text
অ্যামাইডের কার্যকরী মূলক হলো-
A. \text{-CONH_{2}}
B. \text{-COX}
C. \text{-CHO}
D. \text{-NH_{2}}
Answer with only A, B, C, or D.
```

Bangla parsed: `A`; correct: `True`

**Banglish Prompt**

```text
ojamaider karyokori mulok holo-
A. \text{-CONH_{2}}
B. \text{-COX}
C. \text{-CHO}
D. \text{-NH_{2}}
Answer with only A, B, C, or D.
```

Banglish parsed: `C`; correct: `False`

**English Prompt**

```text
The functional group of amide is-
A. - CONH_{2}
B. - COX
C. - CHO
D. - NH_{2}
Answer with only A, B, C, or D.
```

English parsed: `A`; correct: `True`

## 22. benqa_12th-Chemistry-II_0194 (benqa, mcq)

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
semikondaktor hisebe byobohrit hoy-
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

## 23. benqa_12th-Chemistry-II_0228 (benqa, mcq)

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

## 24. benqa_12th-Chemistry-II_0235 (benqa, mcq)

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

Bangla parsed: `A`; correct: `True`

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
