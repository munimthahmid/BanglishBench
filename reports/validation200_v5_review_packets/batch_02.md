# Validation-200 v5 Review Packet 02

Source queue: `data/slices/validation_200_v5_review_queue.csv`
Batch: 2/6
Rows in batch: 25

Fill the source CSV, not this Markdown packet. Use this packet only for
source/context reading while editing `reviewed_banglish`,
`quality_label`, and `review_notes` in the queue.

Allowed labels: `ok`, `minor_edit`, `major_edit`, `bad`.

## 26. banglamath_0233

- CSV row: 27
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); kot->koto (1)

Bangla:

```text
৬ জন লোক একটি কাজ ২৮ দিনে করলে ২৪ জন লোক কত দিনে করবে
Return only the final answer.
```

English:

```text
If 6 people complete a task in 28 days, how many days will 24 people take?
Return only the final answer.
```

Current Banglish:

```text
6 jon lok ekoti kaj 28 dine korole 24 jon lok kot dine korobe
Return only the final answer.
```

Auto-suggested Banglish:

```text
6 jon lok ekti kaj 28 dine korole 24 jon lok koto dine korobe
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 27. banglamath_0234

- CSV row: 28
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); kot->koto (1)

Bangla:

```text
একটি কাজ ক ১০ দিনে ও খ ১৫ দিনে করলে তারা একত্রে কত দিনে করবে
Return only the final answer.
```

English:

```text
If A can do a job in 10 days and B in 15 days, how many days will they take together?
Return only the final answer.
```

Current Banglish:

```text
ekoti kaj k 10 dine o kh 15 dine korole tara ekotre kot dine korobe
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti kaj k 10 dine o kh 15 dine korole tara ekotre koto dine korobe
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 28. banglamath_0550

- CSV row: 29
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: kot->koto (1); kshetrofol->khetrofol (1)

Bangla:

```text
রাস্তাসহ বাগানের পরিসীমা ১৯০ মিটার হলে সমান পরিসীমা বিশিষ্ট বর্গাকার মাঠের ক্ষেত্রফল কত
Return only the final answer.
```

English:

```text
If the total perimeter (including path) of a garden is 190m, what is the area of a square field with the same perimeter?
Return only the final answer.
```

Current Banglish:

```text
rastasoh baganer porisima 190 mitar hole soman porisima bishisht borgakar mather kshetrofol kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
rastasoh baganer porisima 190 mitar hole soman porisima bishisht borgakar mather khetrofol koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 29. banglamath_0553

- CSV row: 30
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: kshetrofol->khetrofol (2)

Bangla:

```text
সামান্তরিকের মেঝে পাথর দ্বারা ঢাকতে কতটি পাথর লাগবে যদি মেঝের ক্ষেত্রফল ৪৫০০ বর্গগজ ও পাথরের ক্ষেত্রফল ৪ বর্গগজ হয়
Return only the final answer.
```

English:

```text
To cover a parallelogram floor of 4500 sq. yards with stones each covering 4 sq. yards, how many stones are needed?
Return only the final answer.
```

Current Banglish:

```text
samantoriker mejhe pathor dwara dhakote kototi pathor lagobe jodi mejher kshetrofol 4500 borgogoj o pathorer kshetrofol 4 borgogoj hoy
Return only the final answer.
```

Auto-suggested Banglish:

```text
samantoriker mejhe pathor dwara dhakote kototi pathor lagobe jodi mejher khetrofol 4500 borgogoj o pathorer khetrofol 4 borgogoj hoy
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 30. banglamath_0557

- CSV row: 31
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); kot->koto (1)

Bangla:

```text
একটি বাগানের পরিসীমা ১২০ মিটার হলে চারদিকে বেড়া দিতে কত খরচ হবে যদি প্রতি মিটারে খরচ ৩১/৪ টাকা হয়
Return only the final answer.
```

English:

```text
If the perimeter of a garden is 120 meters and fencing costs 3¼ Taka per meter, what is the total fencing cost?
Return only the final answer.
```

Current Banglish:

```text
ekoti baganer porisima 120 mitar hole charodike bera dite kot khoroch hobe jodi proti mitare khoroch 31/4 taka hoy
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti baganer porisima 120 mitar hole charodike bera dite koto khoroch hobe jodi proti mitare khoroch 31/4 taka hoy
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 31. banglamath_1692

- CSV row: 32
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); kot->koto (1)

Bangla:

```text
একটি যৌথ পরিবারের মোট সদস্য (পুরুষ, মহিলা ও শিশু) ২০ জন। পরিবারের কর্তাবাবুর আদেশ ২০ মণ ধান পরিবারের সকল সদস্যের মধ্যে ভাগ করে দেয়া হবে। ভাগের নিয়ম হলঃ প্রত্যেক পুরুষ পাবে ৩ মণ, প্রত্যেক মহিলা পাবে ২ মণ, এবং প্রত্যেক শিশু পাবে ১ মণ ধান। প্রশ্ন হচ্ছে, কতজন করে ধান পাবে? অর্থাৎ পরিবারটির পুরুষ, মহিলাদের ও শিশুদের সংখ্যা কত?
Return only the final answer.
```

English:

```text
A joint family has 20 members (men, women, and children). 20 mon of rice is to be divided where each man gets 3 mon, each woman 2 mon, and each child 1 mon. How many men, women, and children are there?
Return only the final answer.
```

Current Banglish:

```text
ekoti jouth poribarer mot sodosy (purush, mohila o shishu) 20 jon. poribarer kortababur adesh 20 mon dhan poribarer sokol sodosyer modhye bhag kore deya hobe. bhager niyom holoh protyek purush pabe 3 mon, protyek mohila pabe 2 mon, ebong protyek shishu pabe 1 mon dhan. proshn hochchhe, kotojon kore dhan pabe? orthat poribarotir purush, mohilader o shishuder songkhya kot?
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti jouth poribarer mot sodosy (purush, mohila o shishu) 20 jon. poribarer kortababur adesh 20 mon dhan poribarer sokol sodosyer modhye bhag kore deya hobe. bhager niyom holoh protyek purush pabe 3 mon, protyek mohila pabe 2 mon, ebong protyek shishu pabe 1 mon dhan. proshn hochchhe, kotojon kore dhan pabe? orthat poribarotir purush, mohilader o shishuder songkhya koto?
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 32. banglamath_1694

- CSV row: 33
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (2)

Bangla:

```text
একটি ৫০০ মিটার লম্বা ট্রেনের গতি ৬০ কিলোমিটার হলে ,অর্ধকিলোমীটার লম্বা একটি সেতু পাড়ি দিতে ট্রেনটির কতক্ষণ সময় লাগবে?
Return only the final answer.
```

English:

```text
A train 500 meters long moves at 60 km/h. How long will it take to cross a bridge 500 meters long?
Return only the final answer.
```

Current Banglish:

```text
ekoti 500 mitar lomba trener goti 60 kilomitar hole ,ordhokilomitar lomba ekoti setu pari dite trenotir kotokshon somoy lagobe?
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti 500 mitar lomba trener goti 60 kilomitar hole ,ordhokilomitar lomba ekti setu pari dite trenotir kotokshon somoy lagobe?
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 33. benqa_10th-Math_0044

- CSV row: 34
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: achhe->ache (1); ekoti->ekti (1)

Bangla:

```text
একটি বর্গের কতটি প্রতিসাম্য রেখা আছে?
A. 8টি
B. 6টি
C. 4টি
D. 2টি
Answer with only A, B, C, or D.
```

English:

```text
How many lines of symmetry does a square have?
A. 8
B. 6
C. 4
D. 2
Answer with only A, B, C, or D.
```

Current Banglish:

```text
ekoti borger kototi protisamy rekha achhe?
A. 8ti
B. 6ti
C. 4ti
D. 2ti
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
ekti borger kototi protisamy rekha ache?
A. 8ti
B. 6ti
C. 4ti
D. 2ti
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 34. benqa_10th-Physics_0106

- CSV row: 35
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: korote->korte (1); kot->koto (1)

Bangla:

```text
বিনা বাধায় পড়ন্ত বস্তু 5 সেকেন্ডে 50 মিটার পথ অতিক্রম করলে 72 মিটার পথ অতিক্রম করতে কত সেকেন্ড সময় লাগবে?
A. 6
B. 7.2
C. 9.5
D. 12
Answer with only A, B, C, or D.
```

English:

```text
If a freely falling body travels 50 m in 5 sec then how much time in second will need to travel thr distance of 72 meter?
A. 6
B. 7.2
C. 9.5
D. 12
Answer with only A, B, C, or D.
```

Current Banglish:

```text
bina badhay poront bostu 5 sekende 50 mitar poth otikrom korole 72 mitar poth otikrom korote kot sekend somoy lagobe?
A. 6
B. 7.2
C. 9.5
D. 12
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
bina badhay poront bostu 5 sekende 50 mitar poth otikrom korole 72 mitar poth otikrom korte koto sekend somoy lagobe?
A. 6
B. 7.2
C. 9.5
D. 12
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 35. benqa_12th-Biology-II_0287

- CSV row: 36
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: konoti->konti (2)

Bangla:

```text
প্রোটিন পরিপাকে অংশ নেয় কোনটি? i. পেপসিন ii. অ্যামাইলেজ iii. কার্বক্সিপেপটাইড নিচের কোনটি সঠিক?
A. i ও ii
B. i ও iii
C. ii ও iii
D. i, ii, ও iii
Answer with only A, B, C, or D.
```

English:

```text
What participate in protein digestion? i. pepsin ii.Amylase iii.Carboxypeptide Which one is correct?
A. i & ii
B. i & iii
C. ii & iii
D. I,ii & iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
protin poripake ongsh ney konoti? i. peposin ii. amailej iii. karboksipepotaid nicher konoti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
protin poripake ongsh ney konti? i. peposin ii. amailej iii. karboksipepotaid nicher konti sothik?
A. i o ii
B. i o iii
C. ii o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 36. benqa_12th-Chemistry-II_0228

- CSV row: 37
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); konoti->konti (1)

Bangla:

```text
Ni(s) + 2Ag^{+}(aq) \xrightarrow{2e^{-}} Ni^{2+}(aq) + 2Ag(s); বিক্রিয়াটিতে- i. Ni জারিত হয় ii. Ag জারিত হয় iii. বিক্রিয়াটি একটি রিডক্স বিক্রিয়া নিচের কোনটি সঠিক?
A. i ও ii
B. ii ও iii
C. i ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

English:

```text
Ni(s) + 2Ag^{+}(aq) \overset{2e^{-}} {\rightarrow}Ni^{2+}(aq) + 2Ag(s); in this reaction- i. Ni becomes oxidized ii. Ag becomes oxidized iii. A redox reaction Which one is correct?
A. i and ii
B. ii and iii
C. i and iii
D. i, ii and iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
Ni(s) + 2Ag^{+}(aq) \xrightarrow{2e^{-}} Ni^{2+}(aq) + 2Ag(s); bikriyatite- i. Ni jarit hoy ii. Ag jarit hoy iii. bikriyati ekoti ridoks bikriya nicher konoti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
Ni(s) + 2Ag^{+}(aq) \xrightarrow{2e^{-}} Ni^{2+}(aq) + 2Ag(s); bikriyatite- i. Ni jarit hoy ii. Ag jarit hoy iii. bikriyati ekti ridoks bikriya nicher konti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 37. benqa_12th-Physics-II_0046

- CSV row: 38
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: konoti->konti (1); kshetre->khetre (1)

Bangla:

```text
রুদ্ধতাপীয় পরিবর্তনের ক্ষেত্রে- i. হঠাৎ সংঘটিত হয় ii. তাপমাত্রা স্থির থাকে iii. এনট্রপির পরিবর্তন শূন্য নিচের কোনটি সঠিক?
A. i ও ii
B. ii ও iii
C. i ও iii
D. i, ii ও iii
Answer with only A, B, C, or D.
```

English:

```text
For changing adiabatic process- i. occurs suddenly ii. temperature constant iii. change of entropy is zero Which one is correct?
A. i and ii
B. ii and iii
C. i and iii
D. i, ii and iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
ruddhotapiy poribortoner kshetre- i. hothat songghotit hoy ii. tapomatra sthir thake iii. enotropir poriborton shuny nicher konoti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
ruddhotapiy poribortoner khetre- i. hothat songghotit hoy ii. tapomatra sthir thake iii. enotropir poriborton shuny nicher konti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii o iii
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 38. benqa_12th-Physics-II_0290

- CSV row: 39
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); kot->koto (1)

Bangla:

```text
একটি কার্নো ইঞ্জিনের কার্যনির্বাহক বস্তু 400 K তাপমাত্রার তাপ উৎস হতে 840 J তাপ গ্রহণ করে তাপগ্রাহকে 630 J তাপ বর্জন করে। তাপ গ্রাহকের তাপমাত্রা কত?
A. 210 K
B. 300 K
C. 400 K
D. 440 K
Answer with only A, B, C, or D.
```

English:

```text
In Carnot's engine 840 J of heat is absorbed from a source at 400 K and is released 630 J of heat in the sink. What is the temperature of the sink?
A. 210 K
B. 300 K
C. 400 K
D. 440 K
Answer with only A, B, C, or D.
```

Current Banglish:

```text
ekoti karno injiner karyonirbahok bostu 400 K tapomatrar tap utos hote 840 J tap grohon kore tapograhoke 630 J tap borjon kore. tap grahoker tapomatra kot?
A. 210 K
B. 300 K
C. 400 K
D. 440 K
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
ekti karno injiner karyonirbahok bostu 400 K tapomatrar tap utos hote 840 J tap grohon kore tapograhoke 630 J tap borjon kore. tap grahoker tapomatra koto?
A. 210 K
B. 300 K
C. 400 K
D. 440 K
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 39. benqa_12th-Physics-I_0254

- CSV row: 40
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: konoti->konti (1); kshetre->khetre (1)

Bangla:

```text
মহাকর্ষ ক্ষেত্র প্রাবল্যের মাত্রার ক্ষেত্রে কোনটি সঠিক?
A. [LT^{-1}]
B. [LT^{-2}]
C. [MLT^{-1}]
D. [MLT^{-2}]
Answer with only A, B, C, or D.
```

English:

```text
Which one is correct for the dimention of gravitational field intensity?
A. [LT^{-1}]
B. [LT^{-2}]
C. [MLT^{-1}]
D. [MLT^{-2}]
Answer with only A, B, C, or D.
```

Current Banglish:

```text
mohakorsh kshetr prabolyer matrar kshetre konoti sothik?
A. [LT^{-1}]
B. [LT^{-2}]
C. [MLT^{-1}]
D. [MLT^{-2}]
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
mohakorsh kshetr prabolyer matrar khetre konti sothik?
A. [LT^{-1}]
B. [LT^{-2}]
C. [MLT^{-1}]
D. [MLT^{-2}]
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 40. benqa_8th-Science_0098

- CSV row: 41
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_multi_edit`
- Replacement count: 2
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); kot->koto (1)

Bangla:

```text
ইশার বাসার বেডরুমে দুটি টিউবলাইট ও একটি ফ্যান প্যারালালে সংযুক্ত করা হয়। বেডরুমের বর্তনীর সাথে ১০ অ্যাম্পিয়ার মানের ফিউজ ব্যবহার করা হয়। দ্বিতীয় উপকরণটির জন্য কার্যকরী ফিউজ কত?
A. ৫ অ্যাম্পিয়ার
B. ১০ অ্যাম্পিয়ার
C. ১৫ অ্যাম্পিয়ার
D. ৩০ অ্যাম্পিয়ার
Answer with only A, B, C, or D.
```

English:

```text
In the bedroom of Esha's house, there are two tube lights and e one fan conndctied in paralled. Afuse of 10 ampere is used in the circuit of bedrood. What is the appropriate fuse for the second element?
A. 5 ampere
B. 10 ampere
C. 15 ampere
D. 30 ampere
Answer with only A, B, C, or D.
```

Current Banglish:

```text
ishar basar bedorume duti tiubolait o ekoti fyan pyaralale songjukt kora hoy. bedorumer bortonir sathe 10 ampiyar maner fiuj byobohar kora hoy. dwitiy upokoronotir jony karyokori fiuj kot?
A. 5 ampiyar
B. 10 ampiyar
C. 15 ampiyar
D. 30 ampiyar
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
ishar basar bedorume duti tiubolait o ekti fyan pyaralale songjukt kora hoy. bedorumer bortonir sathe 10 ampiyar maner fiuj byobohar kora hoy. dwitiy upokoronotir jony karyokori fiuj koto?
A. 5 ampiyar
B. 10 ampiyar
C. 15 ampiyar
D. 30 ampiyar
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 41. banglamath_0181

- CSV row: 42
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_single_edit`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: thakole->thakle (1)

Bangla:

```text
কাজের পরিমাণ অপরিবর্তিত থাকলে লোক সংখ্যা বাড়ালে সময় কী হয়
Return only the final answer.
```

English:

```text
If the amount of work remains the same, what happens to time if the number of workers increases?
Return only the final answer.
```

Current Banglish:

```text
kajer poriman oporibortit thakole lok songkhya barale somoy ki hoy
Return only the final answer.
```

Auto-suggested Banglish:

```text
kajer poriman oporibortit thakle lok songkhya barale somoy ki hoy
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 42. banglamath_0182

- CSV row: 43
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_single_edit`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: kot->koto (1)

Bangla:

```text
৭ কেজি চালের দাম ২৮০ টাকা হলে ১৫ কেজি চালের দাম কত
Return only the final answer.
```

English:

```text
If 7 kg of rice costs 280 Taka, what is the cost of 15 kg?
Return only the final answer.
```

Current Banglish:

```text
7 keji chaler dam 280 taka hole 15 keji chaler dam kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
7 keji chaler dam 280 taka hole 15 keji chaler dam koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 43. banglamath_0185

- CSV row: 44
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_single_edit`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: kot->koto (1)

Bangla:

```text
১২০ কেজি চালে ১০ জন লোকের ২৭ দিন চলে। ৪৫ দিন চলতে কত কেজি চাল প্রয়োজন হবে
Return only the final answer.
```

English:

```text
120 kg of rice lasts 10 people for 27 days. How much rice is needed to last 45 days?
Return only the final answer.
```

Current Banglish:

```text
120 keji chale 10 jon loker 27 din chole. 45 din cholote kot keji chal proyojon hobe
Return only the final answer.
```

Auto-suggested Banglish:

```text
120 keji chale 10 jon loker 27 din chole. 45 din cholote koto keji chal proyojon hobe
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 44. banglamath_0186

- CSV row: 45
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_single_edit`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: kot->koto (1)

Bangla:

```text
২ কুইন্টাল চালে ১৫ জন ছাত্রের ৩০ দিন চলে। ঐ চালে ২০ জন ছাত্রের কত দিন চলবে
Return only the final answer.
```

English:

```text
2 quintals of rice last 15 students for 30 days. How many days will it last for 20 students?
Return only the final answer.
```

Current Banglish:

```text
2 kuintal chale 15 jon chhatrer 30 din chole. oi chale 20 jon chhatrer kot din cholobe
Return only the final answer.
```

Auto-suggested Banglish:

```text
2 kuintal chale 15 jon chhatrer 30 din chole. oi chale 20 jon chhatrer koto din cholobe
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 45. banglamath_0226

- CSV row: 46
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_single_edit`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: kot->koto (1)

Bangla:

```text
৫৫০ টাকাকে ৫:৬ অনুপাতে ভাগ করলে প্রথম অংশ কত হবে
Return only the final answer.
```

English:

```text
If 550 Taka is divided in a 5:6 ratio, what is the first part?
Return only the final answer.
```

Current Banglish:

```text
550 takake 5:6 onupate bhag korole prothom ongsh kot hobe
Return only the final answer.
```

Auto-suggested Banglish:

```text
550 takake 5:6 onupate bhag korole prothom ongsh koto hobe
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 46. banglamath_0227

- CSV row: 47
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_single_edit`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: kot->koto (1)

Bangla:

```text
দুই বন্ধুর বাড়ি থেকে স্কুলের দূরত্বের অনুপাত ২:৩ এবং প্রথম বন্ধুর দূরত্ব ৫ কিমি হলে দ্বিতীয় বন্ধুর দূরত্ব কত
Return only the final answer.
```

English:

```text
The ratio of the distances of two friends from school is 2:3. If the first friend is 5 km away, what is the second friend’s distance?
Return only the final answer.
```

Current Banglish:

```text
dui bondhur bari theke skuler durotter onupat 2:3 ebong prothom bondhur durotto 5 kimi hole dwitiy bondhur durotto kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
dui bondhur bari theke skuler durotter onupat 2:3 ebong prothom bondhur durotto 5 kimi hole dwitiy bondhur durotto koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 47. banglamath_0230

- CSV row: 48
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_single_edit`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: kot->koto (1)

Bangla:

```text
২৫ টাকা ১২৫ টাকার শতকরা কত
Return only the final answer.
```

English:

```text
25 Taka is what percent of 125 Taka?
Return only the final answer.
```

Current Banglish:

```text
25 taka 125 takar shotokora kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
25 taka 125 takar shotokora koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 48. banglamath_0236

- CSV row: 49
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_single_edit`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: kot->koto (1)

Bangla:

```text
১০টি বলপেনের দাম ৬০ টাকা হলে ২টি বলপেনের দাম কত
Return only the final answer.
```

English:

```text
If 10 pens cost 60 Taka, what is the cost of 2 pens?
Return only the final answer.
```

Current Banglish:

```text
10ti bolopener dam 60 taka hole 2ti bolopener dam kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
10ti bolopener dam 60 taka hole 2ti bolopener dam koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 49. banglamath_0237

- CSV row: 50
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_single_edit`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: kot->koto (1)

Bangla:

```text
১ ডজন ডিমের দাম ৪৮ টাকা হলে ১৬টি ডিমের দাম কত
Return only the final answer.
```

English:

```text
If 1 dozen eggs cost 48 Taka, what is the cost of 16 eggs?
Return only the final answer.
```

Current Banglish:

```text
1 dojon dimer dam 48 taka hole 16ti dimer dam kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
1 dojon dimer dam 48 taka hole 16ti dimer dam koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 50. banglamath_0531

- CSV row: 51
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_single_edit`
- Replacement count: 1
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: kot->koto (1)

Bangla:

```text
এক খন্ড জমিতে ৫০০ কেজি ৭০০ গ্রাম আলু হলে ১১ খন্ড জমিতে কত আলু হবে
Return only the final answer.
```

English:

```text
If one plot yields 500 kg 700 g of potatoes, how much will 11 plots yield?
Return only the final answer.
```

Current Banglish:

```text
ek khond jomite 500 keji 700 gram alu hole 11 khond jomite kot alu hobe
Return only the final answer.
```

Auto-suggested Banglish:

```text
ek khond jomite 500 keji 700 gram alu hole 11 khond jomite koto alu hobe
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank
