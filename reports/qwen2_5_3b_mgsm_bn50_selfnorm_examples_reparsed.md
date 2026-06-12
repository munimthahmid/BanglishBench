# Self-Normalization Rewrite Report

Items: `data/slices/mgsm_bn_50_v1.jsonl`
Eval rows: `results/runs/qwen2_5_3b_mgsm_bn50_selfnorm/results/runs/qwen2_5_3b_mgsm_bn50_selfnorm.jsonl`
Examples exported: 12

Compare file: `results/analysis/qwen25_mgsm_bn50_baseline_vs_selfnorm_items_reparsed.csv`

## 1. mgsm_bn_0001 (mgsm)

Gold: `18`
Self-normalized parsed: `দুই করে দিমাগো পাওয়া এবং বন্ধুর জন্য পরিদর্শন চারটি দিনে দিতে মাফি হয়েছে। এই পরিদর্শনের দুর্ভাগ্যবশতঃ এই দিনের পরিদর্শ`; correct: `False`

Baseline parsed: `tini krishokoder bajare protidin kot dolar 2.12 uparjon koren.`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
jeneter hansoguli protidin 16ti kore dim pare. tini protidin pratorashe tinoti kore dim khan ebong bondhuder jony protidin charoti dim diye mafin toiri koren. oboshisht hanser dimoguli tini protidin krishokoder bajare proti dim $2 dore bikroy koren. tini krishokoder bajare protidin kot dolar uparjon koren?
Return only the final answer.
```

**Model Rewrite**

```text
জন্তু হাসনগুলি পরিদর্শন ১৬তম দিনে দুই করে দিমাগো পারে। এই দিনের পরিদর্শনে দুই করে দিমাগো পাওয়া এবং বন্ধুর জন্য পরিদর্শন চারটি দিনে দিমাগো দিতে মাফি হয়েছে। এই পরিদর্শনের দুর্ভাগ্যবশতঃ এই দিনের পরিদর্শনের দুর্ভাগ্যবশতঃ এই পরিদর্শনের দুর্ভ
```

**Final Raw Output**

```text
দুই করে দিমাগো পাওয়া এবং বন্ধুর জন্য পরিদর্শন চারটি দিনে দিতে মাফি হয়েছে। এই পরিদর্শনের দুর্ভাগ্যবশতঃ এই দিনের পরিদর্শ
```


## 2. mgsm_bn_0002 (mgsm)

Gold: `3`
Self-normalized parsed: `The story is about 2 red scarves, and for it, 2 ties will be tied.`; correct: `False`

Baseline parsed: `3 ril lagobe`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
ekoti poshak toiri korote 2 ril nil suto ebong tar ordhek sada suto lage. eti toiri korote mot kotoguli ril lagobe?
Return only the final answer.
```

**Model Rewrite**

```text
একটি পোশাক টোরি করেন ২ রিল নিরস্ত এবং তার উত্তরে একটি কোটো গুলি রিল লাগবে?
```

**Final Raw Output**

```text
The story is about 2 red scarves, and for it, 2 ties will be tied.
```


## 3. mgsm_bn_0003 (mgsm)

Gold: `70000`
Self-normalized parsed: `\[ F = V + \frac{150}{100}V = 2.5V \]`; correct: `False`

Baseline parsed: `tini labh korolen 120,000 dolarni.`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
josh ekoti bari flip korar siddhant niyechhen. tini $80,000-e ekoti bari kroy korolen ebong $50,000 diye meramot korolen. er fole baritir muly 150% briddhi pel. tini kot dolar labh korolen?
Return only the final answer.
```

**Model Rewrite**

```text
জোশ একটি ফ্লিপ করার সিদ্ধান্ত নিয়েছেন। একটি বাজারে একটি বস্তু প্রথমে ছয় হাজার ডলারে খরচ করে প্রাপ্ত হয়েছিল এবং দুই হাজার ডলারে বিক্রি করা হয়েছিল। এর ফলে মুল্য ১৫০% বৃদ্ধি ঘটে। এর ফলে তিনি কতগুলি ডলার লাভ করেছিলেন?
```

**Final Raw Output**

```text
To find out how much profit Joosh made, we first need to calculate the initial and final prices of the object.

1. Initial cost: 600 dollars
2. Selling price: 200 dollars

The increase in value is given as 150%, which means the final value is 150% more than the initial value.

Let's denote the initial value as V. The final value (F) can be calculated using the formula:
\[ F = V + \frac{150}{100}V = 2.5V \]

Given that the final value (
```


## 4. mgsm_bn_0004 (mgsm)

Gold: `540`
Self-normalized parsed: `The number of spins in one week is 1`; correct: `False`

Baseline parsed: `90`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
jemos ek soptahe 3 bar 3ti sprinte douranor siddhant niyechhen. tini proti sprinte 60 mitar kore douran. tini ek soptahe mot kot mitar kore douran?
Return only the final answer.
```

**Model Rewrite**

```text
জেমোস এক সোপ্তাহে ৩ বার ৩তি স্পিন্টে দৌরান সিড্ডং নিয়েছেন। একটি সোপ্তাহে ৬০ মিটারে দৌরান একটি স্পিন্ট করেন। একটি সোপ্তাহে কত মিটারে দৌরান কয়টি স্পিন্ট করেন?
```

**Final Raw Output**

```text
To solve this problem, we need to calculate the total distance covered in one week (7 days) based on the given information and then determine how many spins were made in that time.

From the information provided:
- In one week, Jemos spins 3 times for 60 meters each.
- Therefore, in one week, he spins 3 * 60 = 180 meters.

Now, we need to find out how many spins he makes if he covers 180 meters in one week.

Given that he spins 60 meters per spin:
- The number of spins in one week is 1
```


## 5. mgsm_bn_0005 (mgsm)

Gold: `20`
Self-normalized parsed: `ইয়োঁদেন্তি পরিদৃশ্য তন্র পর্যন্ত মুরোগীকে সুস্থ রাখার জন্য একটি নতুন পর্যায় হয়েছে, যেখানে একটি মুরোগীকে তিনটি ক`; correct: `False`

Baseline parsed: `30`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
oyendi protidin tanr protyekoti murogike susth rakhar jony tin kap kore murogir khabarer mishron khaoyan jate dana, milooyarm ebong sobji thake. tini murogider tinobare alada-alada kore khabar den. sokale, tini murogir jhankoke 15 kap khabar den. bikele, murogider tini aroo 25 kap khabar den. oyendir murogir jhanke jodi 20ti murogi thake tahole murogider diner shesh khabar khaoyanor jony tanke kot kap khabar dite hobe?
Return only the final answer.
```

**Model Rewrite**

```text
ইয়োঁদেন্তি পরিদৃশ্য তন্র পর্যন্ত মুরোগীকে সুস্থ রাখার জন্য একটি নতুন পর্যায় হয়েছে। এই নতুন পর্যায়ে একটি মুরোগীকে তিনটি কাঠামো বা কথা বলা হয়। সাধারণত, একটি মুরোগীকে তিনটি কথা বলা হয়। অন্যদিকে, মুরোগীদের একটি নতুন পর্যায়ে তি�
```

**Final Raw Output**

```text
ইয়োঁদেন্তি পরিদৃশ্য তন্র পর্যন্ত মুরোগীকে সুস্থ রাখার জন্য একটি নতুন পর্যায় হয়েছে, যেখানে একটি মুরোগীকে তিনটি ক
```


## 6. mgsm_bn_0006 (mgsm)

Gold: `64`
Self-normalized parsed: `Now, we calculate the total cost for 16 cans at the new price:`; correct: `False`

Baseline parsed: `12`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
kailar tanr notun ojapartomenter jony kanch kinote dokane giyechhilen. ekoti kancher dam $5, kintu proti dbitiy glaser jony dam hoy mulyer 60% matr. kailar 16ti kanch kinote chan. egulir jony tanke kot dolar orthoprodan korote hobe?
Return only the final answer.
```

**Model Rewrite**

```text
কাইলার তন্র নতুন উপরিস্থিতির জন্য কোনও পরিবর্তন করা হয়নি। একটি কোনও ক্ষেত্রে দাম $5, কিন্তু প্রতিটি ড্বিটি গ্লাস পরিবর্তন দাম হয়েছে মূল্যের 60%। কাইলার 16টি ক্যান্চ কিনতে চাই। এই জন্য একটি গ্রুপের জন্য কত ডলার পরিবর্তন হবে?
```

**Final Raw Output**

```text
To solve this problem, we need to calculate the new cost of one doublet glass after the price increase and then find out the total cost for 16 cans.

First, let's determine the new price of one doublet glass:
- Original price of one doublet glass = $5
- Price increase = 60%

New price of one doublet glass = $5 + (60% of $5) = $5 + ($5 * 0.60) = $5 + $3 = $8

Now, we calculate the total cost for 16 cans at the new price:
-
```


## 7. mgsm_bn_0007 (mgsm)

Gold: `260`
Self-normalized parsed: `2. \( C = S + 4 \)`; correct: `False`

Baseline parsed: `Yes`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
tulujer kachhe charlostoner theke duigun beshi bhera royechhe. charlostoner kachhe siyatoler theke 4gun beshi bhera royechhe. jodi siyatoler kachhe 20ti bhera thake tahole tuluj, charloston ebong siyatoler kachhe sorbomot kotoguli kore bhera achhe?
Return only the final answer.
```

**Model Rewrite**

```text
তুলুজের কাছে চারলোস্টনের থেকে ২০টি বছর বেশি বহন করে যায়। চারলোস্টনের কাছে সিয়াটলোর থেকে ৪টি বছর বেশি বহন করে যায়। যদি সিয়াটলোর কাছে ২০টি বছর বেশি বহন করে থাকে, তাহলে তুলু চারলোস্টন এবং সিয়াটলোর কাছে সর্বমোট বহন করে যাওয়া সম্ভব �
```

**Final Raw Output**

```text
To solve this problem, we need to establish relationships between the years of transportation based on the given conditions and then find the maximum possible total.

Let's denote:
- \( T \) as the number of years transported by Tulou from Charles Town.
- \( C \) as the number of years transported by Charles Town from Seattle.
- \( S \) as the number of years transported by Seattle.

From the problem statement:
1. \( T = C + 20 \)
2. \( C = S + 4 \)

We need to find the maximum possible value of \( T + C + S \).

First,
```


## 8. mgsm_bn_0008 (mgsm)

Gold: `160`
Self-normalized parsed: `কর্লা ২০০ গিগabyte (GB) ফাইলটি সদরদপ্তর থেকে ২ গিগabyte (GB) প্রতিটি মিনিটে ডাউনলোড করার জন্য শুরু করবে, কিন্তু ৪০% ডাউনলোড হওয়`; correct: `False`

Baseline parsed: `karla daunolod korar jony 20 minit shuru koroto hoy.`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
karla 200 GB-er ekoti fail daunolod korochhen. sadharonot tini 2 GB/minit hisebe daunolod korote paren, kintu 40% daunolod hooyar pore, Windows apodet inostol korar jony ristart hote shuru kore, ja 20 minit somoy ney. eropor karlake daunolodotike punoray shuru korote hoy. failoti daunolod korar jony kotota lod lagobe?
Return only the final answer.
```

**Model Rewrite**

```text
কর্লা ২০০ গিগabyte (GB) এর একটি ফাইল ডাউনলোড করতে যাচ্ছেন। সদরদপ্তরে তিনটি ২ গিগabyte (GB) প্রতিটি মিনিটে ডাউনলোড করে যাবে, কিন্তু ৪০% ডাউনলোড হওয়ার পর, ওয়াইন্স অপডেট আপডেট করার জন্য একটি রিস্টার্ট হবে, যা ২০ মিনিট সময় পায়। এর পর কর্লা ডাউনলোড করত
```

**Final Raw Output**

```text
কর্লা ২০০ গিগabyte (GB) ফাইলটি সদরদপ্তর থেকে ২ গিগabyte (GB) প্রতিটি মিনিটে ডাউনলোড করার জন্য শুরু করবে, কিন্তু ৪০% ডাউনলোড হওয়
```


## 9. mgsm_bn_0009 (mgsm)

Gold: `45`
Self-normalized parsed: `, I cannot provide a precise response. The text does not contain enough information to formulate an answer that matches the requested answer format.`; correct: `False`

Baseline parsed: `yes`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
jon proti ghontay 60 mail bege 3 ghonta gari chalanor pore bujhote paren je tini barite gurutbopurn kichhu bhule esechhen ebong tai tini fire jan. tini 4 ghontay bari ferar cheshta koren kintu prothom 2 ghonta tanr trafik jyame byoy hoye jay. poroborti adh-ghonta tini proti ghonta 30 mail bege gari chalanoy byoy koren, oboshisht 4 ghontay tini proti ghonta 80 mail bege gari chalate sokshom hon. 4 ghontar sheshe tini bari theke kotodure achhen?
Return only the final answer.
```

**Model Rewrite**

```text
জন পর্তি ঘন্টায় ৬০ মিনিটে গ্রহণ করে ৩ ঘন্টা গারি চলন ও পরে বৃদ্ধি হয় যে একটি দশটি বর্তমান গুরুত্বপূর্ণ কিছু ভুলে যায় এবং একটি দশটি ফাইর জন। একটি ৪ ঘন্টায় ফাইর চাষে কিছু সংখ্যা হয় কিন্তু প্রথম ২ ঘন্টা তার ট্রাফিক যায় যায় যায় য
```

**Final Raw Output**

```text
The given text appears to be in Bengali and seems to describe a firework display. However, it is not clear what specific question or evaluation item is being asked based on this text alone. Without additional context or details about the required format for the answer, I cannot provide a precise response. The text does not contain enough information to formulate an answer that matches the requested answer format.
```


## 10. mgsm_bn_0010 (mgsm)

Gold: `460`
Self-normalized parsed: `Total cost for 5 hours = 5 * $1`; correct: `False`

Baseline parsed: `47`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
proti soptahe prothom 40 ghonta kaj korar jony elija proti ghontay $10 dore kaj koren. otirikt somoy kaj korar jony tini tanr proti ghontar niyomit dorer 1.2 gun orth pan. jodi elija ei soptahe 45 ghonta kaj kore thaken, tahole ei soptahe tanr uparjon kot?
Return only the final answer.
```

**Model Rewrite**

```text
প্রতি সোপানের প্রথম ৪০ ঘণ্টা কাজ করার জন্য প্রতিটি ঘণ্টার ব্যয় $১০। অন্যরকম কাজ করার জন্য একটি তান্ত্রিক পরিমাণ হবে ১.২ গুন। যদি এই সোপানে ৪৫ ঘণ্টা কাজ করার উপর জন্য আসল ব্যয় হয়, তাহলে এই সোপানের উপর জন্য আসল ব্যয় কত?
```

**Final Raw Output**

```text
To find the total cost of working on the soap for 45 hours, we first need to break down the work into two parts: the first 40 hours and the remaining 5 hours.

For the first 40 hours:
- Cost per hour = $10
- Total cost for 40 hours = 40 * $10 = $400

For the remaining 5 hours:
- Cost per hour = $10 * 1.2 = $12 (since it's 1.2 times more)
- Total cost for 5 hours = 5 * $1
```


## 11. mgsm_bn_0011 (mgsm)

Gold: `366`
Self-normalized parsed: `তিন মাসে প্রোগ্রাম করেছিল 15 টি ডানোলোড.`; correct: `False`

Baseline parsed: `40%`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
ekoti notun program prothom mase 60 bar daunolod kora hoyechhil. dbitiy mase daunoloder songkhya prothom maser daunoloder theke tinogun beshi chhil, kintu taropor tritiy mase ta 30% hras peyechhil. tin mase programotike mot kotobar daunolod kora hoyechhil?
Return only the final answer.
```

**Model Rewrite**

```text
একটি নতুন প্রোগ্রাম প্রথম মাসে ৬০ টি ডানোলোড করেছিল। তবে দুই মাসের ডানোলোদের সংখ্যা প্রথম মাসের ডানোলোদের থেকে তিন গুণে কম হয়েছিল, কিন্তু তিনমাসের ডানোলোদ তারপরে ৩০% কম হয়েছিল। তিন মাসে প্রোগ্রামের কতটি ডানোলোড করেছিল?

তিন মাসে প্র�
```

**Final Raw Output**

```text
তিন মাসে প্রোগ্রাম করেছিল 15 টি ডানোলোড.
```


## 12. mgsm_bn_0012 (mgsm)

Gold: `694`
Self-normalized parsed: `3. For the $55 per six pieces (which is`; correct: `False`

Baseline parsed: `$197`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
tula bekarite giye bibhinn rokomer pestri kinechhilen. tini $68 dojon dore 3 dojon donat, $80 dojon dore 2 dojon chhot kapokek, ebong $55 dojon dore 6 dojon mini chijokek kinechhilen. mot kot khoroch hoyechhil?
Return only the final answer.
```

**Model Rewrite**

```text
তুলা বেকারিতেই গিয়ে বিভিন্ন প্রকারের পেস্টি কেনেচ্ছে। একটি ডোজনের $68 দরে ৩ ডোজন কম, একটি ডোজনের $80 দরে ২ ডোজন ছোট, এবং একটি ডোজনের $55 দরে ৬ ডোজন মিনি চিজের কেনেচ্ছে। মোট কত খরচ হয়েছে?
```

**Final Raw Output**

```text
To find the total cost, we need to calculate the cost for each type of pastry and then sum them up.

1. For the $68 per dozen:
   - Given that one dozen is 3 dozens less, it implies he buys 4 dozens.
   - Cost = 4 * $68 = $272

2. For the $80 per dozen:
   - Given that one dozen is 2 dozens smaller, it implies he buys 3 dozens.
   - Cost = 3 * $80 = $240

3. For the $55 per six pieces (which is
```

