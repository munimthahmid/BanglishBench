# Banglish Diff Report: banglish_clean

- Before: `data/slices/mgsm_bn_50_v1.jsonl`
- After: `data/slices/mgsm_bn_50_v2.jsonl`
- Changed items: 14
- Showing: 14

## 1. mgsm_bn_0006

- Dataset: `mgsm`
- Task type: `math_word_problem`

**Bangla**

```text
কাইলার তাঁর নতুন অ্যাপার্টমেন্টের জন্য কাঁচ কিনতে দোকানে গিয়েছিলেন। একটি কাঁচের দাম $5, কিন্তু প্রতি দ্বিতীয় গ্লাসের জন্য দাম হয় মূল্যের 60% মাত্র। কাইলার 16টি কাঁচ কিনতে চান। এগুলির জন্য তাঁকে কত ডলার অর্থপ্রদান করতে হবে?
Return only the final answer.
```

**Before**

```text
kailar tanr notun ojapartomenter jony kanch kinote dokane giyechhilen. ekoti kancher dam $5, kintu proti dbitiy glaser jony dam hoy mulyer 60% matr. kailar 16ti kanch kinote chan. egulir jony tanke kot dolar orthoprodan korote hobe?
Return only the final answer.
```

**After**

```text
kailar tanr notun apartomenter jony kanch kinote dokane giyechhilen. ekoti kancher dam $5, kintu proti dwitiy glaser jony dam hoy mulyer 60% matr. kailar 16ti kanch kinote chan. egulir jony tanke kot dolar orthoprodan korote hobe?
Return only the final answer.
```

## 2. mgsm_bn_0009

- Dataset: `mgsm`
- Task type: `math_word_problem`

**Bangla**

```text
জন প্রতি ঘণ্টায় 60 মাইল বেগে 3 ঘণ্টা গাড়ি চালানোর পরে বুঝতে পারেন যে তিনি বাড়িতে গুরুত্বপূর্ণ কিছু ভুলে এসেছেন এবং তাই তিনি ফিরে যান। তিনি 4 ঘণ্টায় বাড়ি ফেরার চেষ্টা করেন কিন্তু প্রথম 2 ঘণ্টা তাঁর ট্রাফিক জ্যামে ব্যয় হয়ে যায়। পরবর্তী আধ-ঘণ্টা তিনি প্রতি ঘণ্টা 30 মাইল বেগে গাড়ি চালানোয় ব্যয় করেন, অবশিষ্ট 4 ঘণ্টায় তিনি প্রতি ঘণ্টা 80 মাইল বেগে গাড়ি চালাতে সক্ষম হন। 4 ঘণ্টার শেষে তিনি বাড়ি থেকে কতদূরে আছেন?
Return only the final answer.
```

**Before**

```text
jon proti ghontay 60 mail bege 3 ghonta gari chalanor pore bujhote paren je tini barite gurutbopurn kichhu bhule esechhen ebong tai tini fire jan. tini 4 ghontay bari ferar cheshta koren kintu prothom 2 ghonta tanr trafik jyame byoy hoye jay. poroborti adh-ghonta tini proti ghonta 30 mail bege gari chalanoy byoy koren, oboshisht 4 ghontay tini proti ghonta 80 mail bege gari chalate sokshom hon. 4 ghontar sheshe tini bari theke kotodure achhen?
Return only the final answer.
```

**After**

```text
jon proti ghontay 60 mail bege 3 ghonta gari chalanor pore bujhote paren je tini barite guruttopurn kichhu bhule esechhen ebong tai tini fire jan. tini 4 ghontay bari ferar cheshta koren kintu prothom 2 ghonta tanr trafik jyame byoy hoye jay. poroborti adh-ghonta tini proti ghonta 30 mail bege gari chalanoy byoy koren, oboshisht 4 ghontay tini proti ghonta 80 mail bege gari chalate sokshom hon. 4 ghontar sheshe tini bari theke kotodure achhen?
Return only the final answer.
```

## 3. mgsm_bn_0011

- Dataset: `mgsm`
- Task type: `math_word_problem`

**Bangla**

```text
একটি নতুন প্রোগ্রাম প্রথম মাসে 60 বার ডাউনলোড করা হয়েছিল। দ্বিতীয় মাসে ডাউনলোডের সংখ্যা প্রথম মাসের ডাউনলোডের থেকে তিনগুণ বেশি ছিল, কিন্তু তারপর তৃতীয় মাসে তা 30% হ্রাস পেয়েছিল। তিন মাসে প্রোগ্রামটিকে মোট কতবার ডাউনলোড করা হয়েছিল?
Return only the final answer.
```

**Before**

```text
ekoti notun program prothom mase 60 bar daunolod kora hoyechhil. dbitiy mase daunoloder songkhya prothom maser daunoloder theke tinogun beshi chhil, kintu taropor tritiy mase ta 30% hras peyechhil. tin mase programotike mot kotobar daunolod kora hoyechhil?
Return only the final answer.
```

**After**

```text
ekoti notun program prothom mase 60 bar daunolod kora hoyechhil. dwitiy mase daunoloder songkhya prothom maser daunoloder theke tinogun beshi chhil, kintu taropor tritiy mase ta 30% hras peyechhil. tin mase programotike mot kotobar daunolod kora hoyechhil?
Return only the final answer.
```

## 4. mgsm_bn_0017

- Dataset: `mgsm`
- Task type: `math_word_problem`

**Bangla**

```text
দুটি ট্রেন একই সময়ে সান রাফায়েল থেকে যাত্রা শুরু করে। তারা পশ্চিমের দিকে যেতে শুরু করে, উভয়ই 80 মাইল করে যাত্রা করে। পরের দিন, তারা উত্তরের দিকে যাত্রা করে 150 মাইল পথ যাওয়া সম্পূর্ণ করে। তাহলে দুইদিনে প্রতিটি ট্রেন কত দূরত্ব অতিক্রম করেছে?
Return only the final answer.
```

**Before**

```text
duti tren ekoi somoye san rafayel theke jatra shuru kore. tara poshchimer dike jete shuru kore, ubhoyoi 80 mail kore jatra kore. porer din, tara uttorer dike jatra kore 150 mail poth jaoya sompurn kore. tahole duidine protiti tren kot durotb otikrom korechhe?
Return only the final answer.
```

**After**

```text
duti tren ekoi somoye san rafayel theke jatra shuru kore. tara poshchimer dike jete shuru kore, ubhoyoi 80 mail kore jatra kore. porer din, tara uttorer dike jatra kore 150 mail poth jaoya sompurn kore. tahole duidine protiti tren kot durotto otikrom korechhe?
Return only the final answer.
```

## 5. mgsm_bn_0020

- Dataset: `mgsm`
- Task type: `math_word_problem`

**Bangla**

```text
মারিসা 12 মাইল পথ পাড়ি দিচ্ছেন। এরমধ্যে প্রথম 4 মাইল হাঁটতে তিনি 1 ঘণ্টা এবং পরের দুই মাইল হাঁটতে আরও এক ঘণ্টা সময় নিয়েছেন। যদি তিনি চান তাঁর হাঁটার গতিবেগ গড়ে প্রতি ঘণ্টায় 4 মাইল হবে, তাহলে অবশিষ্ট দূরত্ব অতিক্রম করার জন্য তাঁকে কত বেগে (মাইল প্রতি ঘণ্টায়) হাঁটতে হবে?
Return only the final answer.
```

**Before**

```text
marisa 12 mail poth pari dichchhen. eromodhye prothom 4 mail hantote tini 1 ghonta ebong porer dui mail hantote aroo ek ghonta somoy niyechhen. jodi tini chan tanr hantar gotibeg gore proti ghontay 4 mail hobe, tahole oboshisht durotb otikrom korar jony tanke kot bege (mail proti ghontay) hantote hobe?
Return only the final answer.
```

**After**

```text
marisa 12 mail poth pari dichchhen. eromodhye prothom 4 mail hantote tini 1 ghonta ebong porer dui mail hantote aroo ek ghonta somoy niyechhen. jodi tini chan tanr hantar gotibeg gore proti ghontay 4 mail hobe, tahole oboshisht durotto otikrom korar jony tanke kot bege (mail proti ghontay) hantote hobe?
Return only the final answer.
```

## 6. mgsm_bn_0029

- Dataset: `mgsm`
- Task type: `math_word_problem`

**Bangla**

```text
60 মাইলের বাইক ট্রিপে হেনরি দুবার থেমেছিলেন। 20 মাইল চলার পর তিনি প্রথমবার থেমেছিলেন। তাঁর ট্রিপ শেষ হওয়ার 15 মাইল আগে তিনি দ্বিতীয়বার থেমেছিলেন। প্রথমবার ও দ্বিতীয়বার থামার মধ্যে তিনি কত মাইল যাত্রা করেছিলেন?
Return only the final answer.
```

**Before**

```text
60 mailer baik tripe henori dubar themechhilen. 20 mail cholar por tini prothomobar themechhilen. tanr trip shesh hooyar 15 mail age tini dbitiyobar themechhilen. prothomobar o dbitiyobar thamar modhye tini kot mail jatra korechhilen?
Return only the final answer.
```

**After**

```text
60 mailer baik tripe henori dubar themechhilen. 20 mail cholar por tini prothomobar themechhilen. tanr trip shesh hooyar 15 mail age tini dwitiyobar themechhilen. prothomobar o dwitiyobar thamar modhye tini kot mail jatra korechhilen?
Return only the final answer.
```

## 7. mgsm_bn_0030

- Dataset: `mgsm`
- Task type: `math_word_problem`

**Bangla**

```text
গ্লোরিয়া জুতো কেনাকাটা করার সময় তাঁর বাজেটের সাথে মানানসই একজোড়া বুট দেখতে পান। কিন্তু, তাঁকে বুট ও দুজোড়া উঁচু হিল জুতোর মধ্যে একটিকে বেছে নিতে হবে যেগুলির দাম একত্রে বুটের থেকে পাঁচ ডলার কম। যদি একজোড়া হিল জুতোর দাম $33 হয় এবং অন্যটির দাম এটির দ্বিগুণ হয়, তবে বুটের দাম কত ডলার?
Return only the final answer.
```

**Before**

```text
gloriya juto kenakata korar somoy tanr bajeter sathe mananosoi ekojora but dekhote pan. kintu, tanke but o dujora unchu hil jutor modhye ekotike bechhe nite hobe jegulir dam ekotre buter theke panch dolar kom. jodi ekojora hil jutor dam $33 hoy ebong onyotir dam etir dbigun hoy, tobe buter dam kot dolar?
Return only the final answer.
```

**After**

```text
gloriya juto kenakata korar somoy tanr bajeter sathe mananosoi ekojora but dekhote pan. kintu, tanke but o dujora unchu hil jutor modhye ekotike bechhe nite hobe jegulir dam ekotre buter theke panch dolar kom. jodi ekojora hil jutor dam $33 hoy ebong onyotir dam etir dwigun hoy, tobe buter dam kot dolar?
Return only the final answer.
```

## 8. mgsm_bn_0031

- Dataset: `mgsm`
- Task type: `math_word_problem`

**Bangla**

```text
ড্যারেল ও অ্যালেনের বয়সের অনুপাত 7:11। যদি তাঁদের দুজনের মোট বয়স এখন 162 বছর হয়, তাহলে এখন থেকে 10 বছর পরে অ্যালেনের বয়স কত হবে তা নির্ণয় করুন।
Return only the final answer.
```

**Before**

```text
dyarel o ojalener boyoser onupat 7:11. jodi tander dujoner mot boyos ekhon 162 bochhor hoy, tahole ekhon theke 10 bochhor pore ojalener boyos kot hobe ta nirnoy korun.
Return only the final answer.
```

**After**

```text
dyarel o alener boyoser onupat 7:11. jodi tander dujoner mot boyos ekhon 162 bochhor hoy, tahole ekhon theke 10 bochhor pore alener boyos kot hobe ta nirnoy korun.
Return only the final answer.
```

## 9. mgsm_bn_0035

- Dataset: `mgsm`
- Task type: `math_word_problem`

**Bangla**

```text
অ্যারনের থেকে সিওভানের কাছে 2টি কম রত্ন আছে। রেমন্ডের রত্নের অর্ধেকের থেকে 5টি বেশি রত্ন অ্যারনের কাছে আছে। যদি রেমন্ডের কাছে 40টি রত্ন থাকে, তাহলে সিওভানের কাছে কটি রত্ন আছে?
Return only the final answer.
```

**Before**

```text
ojaroner theke siobhaner kachhe 2ti kom rotn achhe. remonder rotner ordheker theke 5ti beshi rotn ojaroner kachhe achhe. jodi remonder kachhe 40ti rotn thake, tahole siobhaner kachhe koti rotn achhe?
Return only the final answer.
```

**After**

```text
aroner theke siobhaner kachhe 2ti kom rotn achhe. remonder rotner ordheker theke 5ti beshi rotn aroner kachhe achhe. jodi remonder kachhe 40ti rotn thake, tahole siobhaner kachhe koti rotn achhe?
Return only the final answer.
```

## 10. mgsm_bn_0036

- Dataset: `mgsm`
- Task type: `math_word_problem`

**Bangla**

```text
মাইক 40 মিনিট ধরে পিং-পং খেলেন। প্রথম 20 মিনিটে তিনি 4 পয়েন্ট স্কোর করেছেন। দ্বিতীয় 20 মিনিটে তিনি 25% বেশি পয়েন্ট স্কোর করেছেন। তিনি মোট কত পয়েন্ট স্কোর করেছেন?
Return only the final answer.
```

**Before**

```text
maik 40 minit dhore ping-pong khelen. prothom 20 minite tini 4 poyent skor korechhen. dbitiy 20 minite tini 25% beshi poyent skor korechhen. tini mot kot poyent skor korechhen?
Return only the final answer.
```

**After**

```text
maik 40 minit dhore ping-pong khelen. prothom 20 minite tini 4 poyent skor korechhen. dwitiy 20 minite tini 25% beshi poyent skor korechhen. tini mot kot poyent skor korechhen?
Return only the final answer.
```

## 11. mgsm_bn_0041

- Dataset: `mgsm`
- Task type: `math_word_problem`

**Bangla**

```text
ব্র্যান্ডনের iPhone বেনের iPhone-এর থেকে চারগুণ পুরনো। আবার বেনের iPhone সুজির iPhone-এর তুলনায় দ্বিগুণ পুরনো। যদি সুজির iPhone 1 বছর পুরনো হয়, তাহলে ব্র্যান্ডনের iPhone কত বছরের পুরনো?
Return only the final answer.
```

**Before**

```text
bryandoner iPhone bener iPhone-er theke charogun purono. abar bener iPhone sujir iPhone-er tulonay dbigun purono. jodi sujir iPhone 1 bochhor purono hoy, tahole bryandoner iPhone kot bochhorer purono?
Return only the final answer.
```

**After**

```text
bryandoner iPhone bener iPhone-er theke charogun purono. abar bener iPhone sujir iPhone-er tulonay dwigun purono. jodi sujir iPhone 1 bochhor purono hoy, tahole bryandoner iPhone kot bochhorer purono?
Return only the final answer.
```

## 12. mgsm_bn_0042

- Dataset: `mgsm`
- Task type: `math_word_problem`

**Bangla**

```text
মাউন্ট ফার্বোর শীর্ষে বসে বিশালাকার ড্রাগন পার্গ 1000 ফুট দূরত্বের মধ্যে থাকা যে কোনও কিছুর উপরে মুখ থেকে অগ্নিশিখা বর্ষণ করছে। ড্রাগনটিকে হত্যা করতে পারে এমন একমাত্র জ্ঞাত অস্ত্র হল স্বর্ণ জ্যাভলিন, যেটিকে পলি 400 ফুট দূরত্ব অবধি নিক্ষেপ করতে পারেন, কিন্তু সেই দূরত্ব ড্রাগনের অগ্নিশিখার নাগালের মধ্যেই রয়েছে। কিন্তু পলি যখন নীলকান্ত মণি ধরে রাখেন তখন তিনি মণিটি ধরে না থাকা অবস্থার তুলনায় তিনগুণ দূরত্ব অবধি জ্যাভলিনটিকে নিক্ষেপ করতে পারেন। যদি তিনি মণিটি ধরে রাখেন, তাহলে ড্রাগনের অগ্নিশিখার নাগালের বাইরে কত দূরত্ব অবধি দাঁড়িয়ে পলি স্বর্ণ জ্যাভলিন দিয়ে ড্রাগনকে আঘাত করতে পারবেন?
Return only the final answer.
```

**Before**

```text
maunt farbor shirshe bose bishalakar dragon parg 1000 fut durotber modhye thaka je konoo kichhur upore mukh theke ognishikha borshon korochhe. dragonotike hotya korote pare emon ekomatr jnat ostr hol sborn jyabholin, jetike poli 400 fut durotb obodhi nikshep korote paren, kintu sei durotb dragoner ognishikhar nagaler modhyei royechhe. kintu poli jokhon nilokant moni dhore rakhen tokhon tini moniti dhore na thaka obosthar tulonay tinogun durotb obodhi jyabholinotike nikshep korote paren. jodi tini moniti dhore rakhen, tahole dragoner ognishikhar nagaler baire kot durotb obodhi danriye poli sborn jyabholin diye dragonoke aghat korote paroben?
Return only the final answer.
```

**After**

```text
maunt farbor shirshe bose bishalakar dragon parg 1000 fut durotter modhye thaka je konoo kichhur upore mukh theke ognishikha borshon korochhe. dragonotike hotya korote pare emon ekomatr jnat ostr hol sborn jyabholin, jetike poli 400 fut durotto obodhi nikshep korote paren, kintu sei durotto dragoner ognishikhar nagaler modhyei royechhe. kintu poli jokhon nilokant moni dhore rakhen tokhon tini moniti dhore na thaka obosthar tulonay tinogun durotto obodhi jyabholinotike nikshep korote paren. jodi tini moniti dhore rakhen, tahole dragoner ognishikhar nagaler baire kot durotto obodhi danriye poli sborn jyabholin diye dragonoke aghat korote paroben?
Return only the final answer.
```

## 13. mgsm_bn_0048

- Dataset: `mgsm`
- Task type: `math_word_problem`

**Bangla**

```text
জন নীল টাই-এর দ্বিগুণ লাল টাই ক্রয় করেছেন। নীল টাই-এর তুলনায় লাল টাই-এর দাম 50% বেশি। প্রতি নীল টাই $40 দরে ক্রয় করতে তিনি $200 ব্যয় করেছেন। তিনি টাই বাবদ মোট কত ব্যয় করেছেন?
Return only the final answer.
```

**Before**

```text
jon nil tai-er dbigun lal tai kroy korechhen. nil tai-er tulonay lal tai-er dam 50% beshi. proti nil tai $40 dore kroy korote tini $200 byoy korechhen. tini tai babod mot kot byoy korechhen?
Return only the final answer.
```

**After**

```text
jon nil tai-er dwigun lal tai kroy korechhen. nil tai-er tulonay lal tai-er dam 50% beshi. proti nil tai $40 dore kroy korote tini $200 byoy korechhen. tini tai babod mot kot byoy korechhen?
Return only the final answer.
```

## 14. mgsm_bn_0050

- Dataset: `mgsm`
- Task type: `math_word_problem`

**Bangla**

```text
রিচার্ড 15 ফ্লোরের একটি অ্যাপার্টমেন্ট বিল্ডিং-এ থাকেন। প্রতিটি ফ্লোরে 8টি করে ইউনিট আছে, এবং বিল্ডিং-এর 3/4 অংশ অধিকৃত। বিল্ডিং-এ মোট অধিকৃত নয় এমন ইউনিটের সংখ্যা কত?
Return only the final answer.
```

**Before**

```text
richard 15 florer ekoti ojapartoment bilding-e thaken. protiti flore 8ti kore iunit achhe, ebong bilding-er 3/4 ongsh odhikrit. bilding-e mot odhikrit noy emon iuniter songkhya kot?
Return only the final answer.
```

**After**

```text
richard 15 florer ekoti apartoment bilding-e thaken. protiti flore 8ti kore iunit achhe, ebong bilding-er 3/4 ongsh odhikrit. bilding-e mot odhikrit noy emon iuniter songkhya kot?
Return only the final answer.
```
