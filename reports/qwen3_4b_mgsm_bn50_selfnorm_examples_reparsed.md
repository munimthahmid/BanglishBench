# Self-Normalization Rewrite Report

Items: `data/slices/mgsm_bn_50_v1.jsonl`
Eval rows: `results/runs/qwen3_4b_mgsm_bn50_selfnorm/results/runs/qwen3_4b_mgsm_bn50_selfnorm.jsonl`
Examples exported: 5

Compare file: `results/analysis/qwen3_mgsm_bn50_baseline_vs_selfnorm_items_reparsed.csv`

## 1. mgsm_bn_0005 (mgsm)

Gold: `20`
Self-normalized parsed: `"তিন কপ মুরগির খাবারের মিশ্রণ খায়" এবং পরে "সকালে 15 কপ খবর`; correct: `False`

Baseline parsed: `20`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
oyendi protidin tanr protyekoti murogike susth rakhar jony tin kap kore murogir khabarer mishron khaoyan jate dana, milooyarm ebong sobji thake. tini murogider tinobare alada-alada kore khabar den. sokale, tini murogir jhankoke 15 kap khabar den. bikele, murogider tini aroo 25 kap khabar den. oyendir murogir jhanke jodi 20ti murogi thake tahole murogider diner shesh khabar khaoyanor jony tanke kot kap khabar dite hobe?
Return only the final answer.
```

**Model Rewrite**

```text
যোদি প্রতিদিন তান্র প্রত্যেক মুরগির সুস্থ রাখার জন্য তিন কপ মুরগির খাবারের মিশ্রণ খায় এবং মিলোয়ার্ম এবং সোজিত থাকে। তিনি মুরগির তিনটি বারে আলাদা-আলাদা করে খবর দেন। সকালে, তিনি মুরগির তিনটি বারে 15 কপ খবর দেন। বিকালে, মুরগির তিনটি বারে 25 কপ �
```

**Final Raw Output**

```text
প্রশ্নটি অস্পষ্ট এবং অনেক অংশ অস্পষ্ট বা ভুল হয়ে গেছে। যেমন:

- "তিন কপ মুরগির খাবারের মিশ্রণ খায়" এবং পরে "সকালে 15 কপ খবর
```


## 2. mgsm_bn_0023 (mgsm)

Gold: `7`
Self-normalized parsed: `পরবর্তী ২ জন গ্রাহকের প্রত্যেকে ২টি DVD ক্রয় করেন → মোট = 2`; correct: `False`

Baseline parsed: `7`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
bili DVD bikroy koren. monggolobare tanr 8 jon grahok hoyechhe. tanr prothom 3 jon grahoker protyeke ekoti kore DVD kroy koren. poroborti 2 jon grahoker protyeke 2ti kore DVD kroy koren. tanr shesh 3 jon grahok konoo DVD kroy korenoni. bili monggolobare kotoguli DVD bikroy korechhen?
Return only the final answer.
```

**Model Rewrite**

```text
বিলি DVD বিক্রয় করেন। মোট বার ৮ জন গ্রাহক হয়েছে। তাদের প্রথম ৩ জন গ্রাহকের প্রত্যেকে একটি করে DVD ক্রয় করেন। পরবর্তী ২ জন গ্রাহকের প্রত্যেকে ২টি করে DVD ক্রয় করেন। তাদের শেষ ৩ জন গ্রাহক কোনো DVD ক্রয় করেনি। মোট কতগুলি DVD বিক্রয় করেছেন?
```

**Final Raw Output**

```text
প্রথম ৩ জন গ্রাহকের প্রত্যেকে ১টি DVD ক্রয় করেন → মোট = 3 × 1 = 3 টি DVD  
পরবর্তী ২ জন গ্রাহকের প্রত্যেকে ২টি DVD ক্রয় করেন → মোট = 2
```


## 3. mgsm_bn_0024 (mgsm)

Gold: `8`
Self-normalized parsed: `প্রশ্ন: ১:০০ পিএম থেকে ৫:০০ পিএম পর্যন্ত জবলার পর মোমোবাতি`; correct: `False`

Baseline parsed: `8`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
ekoti momobati jbolole seti proti ghontay 2 sentimitar kore gole jay. 1:00 PM theke 5:00 PM poryont jbolar por ekoti momobati kot sentimitar chhot hoye jabe?
Return only the final answer.
```

**Model Rewrite**

```text
একটি মোমোবাতি জবলোলে সেটি প্রতি ঘন্টায় ২ সেন্টিমিটার করে গোলে যায়। ১:০০ পিএম থেকে ৫:০০ পিএম পর্যন্ত জবলার পর একটি মোমোবাতি কত সেন্টিমিটার চট হয়ে যাবে?
```

**Final Raw Output**

```text
মোমোবাতি জবলোলে প্রতি ঘন্টায় ২ সেন্টিমিটার গোলে যায়।

প্রশ্ন: ১:০০ পিএম থেকে ৫:০০ পিএম পর্যন্ত জবলার পর মোমোবাতি
```


## 4. mgsm_bn_0025 (mgsm)

Gold: `26`
Self-normalized parsed: `প্রশ্ন: জা অসল মূল্যের উপর 25% চারে পাওয়া গিয়েছে। এই চার হিসাবে বচ্চহরের মূল্য $19.50 হয়েছে। বোতির অসল মূল্য কত?`; correct: `False`

Baseline parsed: `26`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
kail got bochhorer sobotheke beshi bikroy hooya boiti $19.50 mulye kinechhilen. ja asol mulyer opor 25% chhare paoya giyechhil. boitir asol muly kot chhil?
Return only the final answer.
```

**Model Rewrite**

```text
কেই গোট বচ্চহরের সবতেকে বেশি বিক্রয় হয়া গিয়েছে $19.50 মূল্যে কেন চলেছে। জা অসল মূল্যের উপর 25% চারে পাওয়া গিয়েছে। বোতির অসল মূল্য কত চলেছে?
```

**Final Raw Output**

```text
প্রশ্ন: জা অসল মূল্যের উপর 25% চারে পাওয়া গিয়েছে। এই চার হিসাবে বচ্চহরের মূল্য $19.50 হয়েছে। বোতির অসল মূল্য কত?

সমস্ত ত
```


## 5. mgsm_bn_0036 (mgsm)

Gold: `9`
Self-normalized parsed: `২৫% বেশি মানে হল�`; correct: `False`

Baseline parsed: `9`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
maik 40 minit dhore ping-pong khelen. prothom 20 minite tini 4 poyent skor korechhen. dbitiy 20 minite tini 25% beshi poyent skor korechhen. tini mot kot poyent skor korechhen?
Return only the final answer.
```

**Model Rewrite**

```text
এক ৪০ মিনিট ধরে পিংপং খেলে। প্রথম ২০ মিনিটে তুই ৪ পয়েন্ট স্কোর করেছ। দ্বিতীয় ২০ মিনিটে তুই ২৫% বেশি পয়েন্ট স্কোর করেছ। তুই মোট কত পয়েন্ট স্কোর করেছ?
```

**Final Raw Output**

```text
প্রথম ২০ মিনিটে তুই ৪ পয়েন্ট স্কোর করেছ।

দ্বিতীয় ২০ মিনিটে তুই ২৫% বেশি পয়েন্ট স্কোর করেছ।  
২৫% বেশি মানে হল�
```

