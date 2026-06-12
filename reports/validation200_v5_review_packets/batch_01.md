# Validation-200 v5 Review Packet 01

Source queue: `data/slices/validation_200_v5_review_queue.csv`
Batch: 1/6
Rows in batch: 25

Fill the source CSV, not this Markdown packet. Use this packet only for
source/context reading while editing `reviewed_banglish`,
`quality_label`, and `review_notes` in the queue.

Allowed labels: `ok`, `minor_edit`, `major_edit`, `bad`.

## 1. banglamath_0538

- CSV row: 2
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 8
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ayotakar->ayotokar (1); choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)

Bangla:

```text
একটি আয়তাকার বাগানের দৈর্ঘ্য ৬০ মিটার ও প্রস্থ ৪০ মিটার। এর ভিতরে ২ মিটার চওড়া রাস্তা থাকলে রাস্তার ক্ষেত্রফল কত
Return only the final answer.
```

English:

```text
A rectangular garden is 60m by 40m. If there’s a 2m wide path inside, what is the area of the path?
Return only the final answer.
```

Current Banglish:

```text
ekoti ayotakar baganer doirghy 60 mitar o prosth 40 mitar. er bhitore 2 mitar choora rasta thakole rastar kshetrofol kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti ayotokar baganer doirgho 60 mitar o prostho 40 mitar. er bhitore 2 mitar chowra rasta thakle rastar khetrofol koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 2. banglamath_0541

- CSV row: 3
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 8
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ayotakar->ayotokar (1); choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)

Bangla:

```text
একটি আয়তাকার বাগানের দৈর্ঘ্য ৫০ মি ও প্রস্থ ৩০ মি। এর ভিতরে ৩ মিটার চওড়া রাস্তা থাকলে রাস্তার ক্ষেত্রফল কত
Return only the final answer.
```

English:

```text
A rectangular garden is 50m by 30m. If there’s a 3m wide path inside, what is the area of the path?
Return only the final answer.
```

Current Banglish:

```text
ekoti ayotakar baganer doirghy 50 mi o prosth 30 mi. er bhitore 3 mitar choora rasta thakole rastar kshetrofol kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti ayotokar baganer doirgho 50 mi o prostho 30 mi. er bhitore 3 mitar chowra rasta thakle rastar khetrofol koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 3. banglamath_0549

- CSV row: 4
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 7
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)

Bangla:

```text
একটি বাগানের বাইরে ২.৫ মিটার চওড়া রাস্তা থাকলে রাস্তার ক্ষেত্রফল কত যদি বাগানের দৈর্ঘ্য ৫০ মি ও প্রস্থ ৩৫ মি হয়
Return only the final answer.
```

English:

```text
If a 2.5m wide path surrounds a garden of 50m by 35m, what is the area of the path?
Return only the final answer.
```

Current Banglish:

```text
ekoti baganer baire 2.5 mitar choora rasta thakole rastar kshetrofol kot jodi baganer doirghy 50 mi o prosth 35 mi hoy
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti baganer baire 2.5 mitar chowra rasta thakle rastar khetrofol koto jodi baganer doirgho 50 mi o prostho 35 mi hoy
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 4. banglamath_1688

- CSV row: 5
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 7
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); korote->korte (1); penyaj->peyaj (5)

Bangla:

```text
কোন একটি বিয়ের অনুষ্ঠানে রান্না করতে বাবুর্চি ও তার সহকর্মী মোট ৪০০টি পেঁয়াজ কাটেন। বাবুর্চি প্রতি মিনিটে অন্তত ৩টি পেঁয়াজ এবং তার সহকর্মী প্রতি মিনিটে অন্তত ২টি পেঁয়াজ কাটতে পারে। যদি বাবুর্চি তার সহকর্মীর চেয়ে ২৫ মিনিট আগে পেঁয়াজ কাটা বন্ধ, তবে কে কতটি পেঁয়াজ কেটেছিল আর কার কতক্ষণ সময় লেগেছিল?
Return only the final answer.
```

English:

```text
At a wedding, a chef and assistant cut 400 onions together. The chef cuts at least 3 onions per minute and the assistant cuts at least 2 per minute. If the chef stops 25 minutes before the assistant, how many onions did each cut and how long did they work?
Return only the final answer.
```

Current Banglish:

```text
kon ekoti biyer onushthane ranna korote baburchi o tar sohokormi mot 400ti penyaj katen. baburchi proti minite ontot 3ti penyaj ebong tar sohokormi proti minite ontot 2ti penyaj katote pare. jodi baburchi tar sohokormir cheye 25 minit age penyaj kata bondh, tobe ke kototi penyaj ketechhil ar kar kotokshon somoy legechhil?
Return only the final answer.
```

Auto-suggested Banglish:

```text
kon ekti biyer onushthane ranna korte baburchi o tar sohokormi mot 400ti peyaj katen. baburchi proti minite ontot 3ti peyaj ebong tar sohokormi proti minite ontot 2ti peyaj katote pare. jodi baburchi tar sohokormir cheye 25 minit age peyaj kata bondh, tobe ke kototi peyaj ketechhil ar kar kotokshon somoy legechhil?
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 5. banglamath_0519

- CSV row: 6
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 6
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ayotakar->ayotokar (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1)

Bangla:

```text
একটি আয়তাকার বাগানের দৈর্ঘ্য ১৫০ মিটার ও প্রস্থ ৫০ মিটার হলে ক্ষেত্রফল কত
Return only the final answer.
```

English:

```text
If the length of a rectangular garden is 150 meters and width is 50 meters, what is the area?
Return only the final answer.
```

Current Banglish:

```text
ekoti ayotakar baganer doirghy 150 mitar o prosth 50 mitar hole kshetrofol kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti ayotokar baganer doirgho 150 mitar o prostho 50 mitar hole khetrofol koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 6. banglamath_0518

- CSV row: 7
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 5
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ayotakar->ayotokar (1); doirghy->doirgho (2); ekoti->ekti (1); kot->koto (1)

Bangla:

```text
একটি আয়তাকার বাগানের দৈর্ঘ্য প্রস্থের তিনগুণ এবং পরিসীমা ৪০০ মিটার হলে বাগানের দৈর্ঘ্য কত
Return only the final answer.
```

English:

```text
In a rectangular garden, the length is three times the width and the perimeter is 400 meters. What is the length?
Return only the final answer.
```

Current Banglish:

```text
ekoti ayotakar baganer doirghy prosther tinogun ebong porisima 400 mitar hole baganer doirghy kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti ayotokar baganer doirgho prosther tinogun ebong porisima 400 mitar hole baganer doirgho koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 7. banglamath_0540

- CSV row: 8
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 5
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: doirghy->doirgho (2); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1)

Bangla:

```text
একটি ঘরের দৈর্ঘ্য প্রস্থের তিনগুণ এবং ক্ষেত্রফল ১৪৭ বর্গমিটার হলে ঘরটির দৈর্ঘ্য কত
Return only the final answer.
```

English:

```text
If a room's length is three times its width and the area is 147 sq. meters, what is the length?
Return only the final answer.
```

Current Banglish:

```text
ekoti ghorer doirghy prosther tinogun ebong kshetrofol 147 borgomitar hole ghorotir doirghy kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti ghorer doirgho prosther tinogun ebong khetrofol 147 borgomitar hole ghorotir doirgho koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 8. benqa_8th-Math_0167

- CSV row: 9
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_multi_edit`
- Replacement count: 5
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ayotakar->ayotokar (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); prosth->prostho (1)

Bangla:

```text
একটি আয়তাকার বাগানের দৈর্ঘ্য প্রস্থের দেড়গুণ। এর প্রস্থ 16 মিটার হলে, বাগানের পরিসীমা কত?
A. 40 মিটার
B. 64 মিটার
C. 80 মিটার
D. 96 মিটার
Answer with only A, B, C, or D.
```

English:

```text
The length of a rectangular garden is one and half times its breadth. If breadth is 16 metres , what is its peremeter?
A. 40m
B. 64m
C. 80m
D. 96m
Answer with only A, B, C, or D.
```

Current Banglish:

```text
ekoti ayotakar baganer doirghy prosther derogun. er prosth 16 mitar hole, baganer porisima kot?
A. 40 mitar
B. 64 mitar
C. 80 mitar
D. 96 mitar
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
ekti ayotokar baganer doirgho prosther derogun. er prostho 16 mitar hole, baganer porisima koto?
A. 40 mitar
B. 64 mitar
C. 80 mitar
D. 96 mitar
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 9. banglamath_0521

- CSV row: 10
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 4
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); prosth->prostho (1)

Bangla:

```text
একটি জমির দৈর্ঘ্য ২০ মিটার ও প্রস্থ ১৫ মিটার হলে তার পরিসীমা কত
Return only the final answer.
```

English:

```text
If a plot is 20 meters long and 15 meters wide, what is its perimeter?
Return only the final answer.
```

Current Banglish:

```text
ekoti jomir doirghy 20 mitar o prosth 15 mitar hole tar porisima kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti jomir doirgho 20 mitar o prostho 15 mitar hole tar porisima koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 10. banglamath_0522

- CSV row: 11
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 4
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: choora->chowra (1); kot->koto (1); kshetrofol->khetrofol (1); thakole->thakle (1)

Bangla:

```text
জমির ভিতরে ২ মিটার চওড়া রাস্তা থাকলে রাস্তাবাদে জমির ক্ষেত্রফল কত
Return only the final answer.
```

English:

```text
If there is a 2-meter-wide path inside the land, what is the area of the land including the path?
Return only the final answer.
```

Current Banglish:

```text
jomir bhitore 2 mitar choora rasta thakole rastabade jomir kshetrofol kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
jomir bhitore 2 mitar chowra rasta thakle rastabade jomir khetrofol koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 11. banglamath_0526

- CSV row: 12
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 4
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); uchchota->ucchota (1)

Bangla:

```text
একটি ত্রিভুজের ভূমি ১০ মিটার ও উচ্চতা ৬ মিটার হলে ক্ষেত্রফল কত
Return only the final answer.
```

English:

```text
If a triangle has a base of 10 meters and height of 6 meters, what is its area?
Return only the final answer.
```

Current Banglish:

```text
ekoti tribhujer bhumi 10 mitar o uchchota 6 mitar hole kshetrofol kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti tribhujer bhumi 10 mitar o ucchota 6 mitar hole khetrofol koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 12. banglamath_0552

- CSV row: 13
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 4
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); uchchota->ucchota (1)

Bangla:

```text
একটি সামান্তরিকের ভূমি ৯০ গজ ও উচ্চতা ৫০ গজ হলে তার ক্ষেত্রফল কত
Return only the final answer.
```

English:

```text
If a parallelogram has a base of 90 yards and height of 50 yards, what is its area?
Return only the final answer.
```

Current Banglish:

```text
ekoti samantoriker bhumi 90 goj o uchchota 50 goj hole tar kshetrofol kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti samantoriker bhumi 90 goj o ucchota 50 goj hole tar khetrofol koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 13. banglamath_0558

- CSV row: 14
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 4
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ayotakar->ayotokar (1); doirghy->doirgho (1); kot->koto (1); prosth->prostho (1)

Bangla:

```text
৬০ মিটার দীর্ঘ আয়তাকার বাগানের দৈর্ঘ্য প্রস্থের ৩ গুণ হলে প্রস্থ কত
Return only the final answer.
```

English:

```text
A rectangular garden is 60 meters long and the length is 3 times the width. What is the width?
Return only the final answer.
```

Current Banglish:

```text
60 mitar dirgh ayotakar baganer doirghy prosther 3 gun hole prosth kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
60 mitar dirgh ayotokar baganer doirgho prosther 3 gun hole prostho koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 14. banglamath_1691

- CSV row: 15
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 4
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: achhe->ache (1); ekoti->ekti (2); korote->korte (1)

Bangla:

```text
বেরু গোয়ালার কাছে একটি কলসিতে ১০ লিটার দুধ এবং দুধ মাপার দুটি খালি পাত্র , একটি ৫ লিটারের, অপরটি ৩ লিটারের। সে ক্রেতাকে ১ লিটার দুধ বিক্রি করতে চায়। গোয়ালার কাছে জেডযেসব পাত্র আছে শুধু তা দিয়ে কিভাবে ক্রেতাকে ১ লিটার দুধ দেয়া সম্ভব?
Return only the final answer.
```

English:

```text
Beru the milkman has 10 liters of milk in a jar, and two empty containers: one of 5 liters and one of 3 liters. How can he measure exactly 1 liter using only these two containers?
Return only the final answer.
```

Current Banglish:

```text
beru goyalar kachhe ekoti kolosite 10 litar dudh ebong dudh mapar duti khali patr , ekoti 5 litarer, oporoti 3 litarer. se kretake 1 litar dudh bikri korote chay. goyalar kachhe jedojesob patr achhe shudhu ta diye kibhabe kretake 1 litar dudh deya sombhob?
Return only the final answer.
```

Auto-suggested Banglish:

```text
beru goyalar kachhe ekti kolosite 10 litar dudh ebong dudh mapar duti khali patr , ekti 5 litarer, oporoti 3 litarer. se kretake 1 litar dudh bikri korte chay. goyalar kachhe jedojesob patr ache shudhu ta diye kibhabe kretake 1 litar dudh deya sombhob?
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 15. banglamath_0183

- CSV row: 16
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 3
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: achhe->ache (1); ekoti->ekti (1); kot->koto (1)

Bangla:

```text
একটি ছাত্রাবাসে ৫০ জনের ১৫ দিনের খাদ্য মজুদ আছে। ঐ খাদ্যে ২৫ জনের কত দিন চলবে
Return only the final answer.
```

English:

```text
A hostel has food for 50 people for 15 days. How many days will it last for 25 people?
Return only the final answer.
```

Current Banglish:

```text
ekoti chhatrabase 50 joner 15 diner khaddo mojud achhe. oi khadde 25 joner kot din cholobe
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti chhatrabase 50 joner 15 diner khaddo mojud ache. oi khadde 25 joner koto din cholobe
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 16. banglamath_0184

- CSV row: 17
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 3
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: korote->korte (2); kot->koto (1)

Bangla:

```text
৯০০০ টাকা বিনিয়োগে প্রতিদিন ৪৫০ টাকা লাভ হলে ৬০০ টাকা লাভ করতে কত বিনিয়োগ করতে হবে
Return only the final answer.
```

English:

```text
If an investment of 9000 Taka yields 450 Taka profit per day, how much should be invested to earn 600 Taka per day?
Return only the final answer.
```

Current Banglish:

```text
9000 taka biniyoge protidin 450 taka labh hole 600 taka labh korote kot biniyog korote hobe
Return only the final answer.
```

Auto-suggested Banglish:

```text
9000 taka biniyoge protidin 450 taka labh hole 600 taka labh korte koto biniyog korte hobe
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 17. banglamath_0187

- CSV row: 18
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 3
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); korote->korte (2)

Bangla:

```text
একটি বাঁধ তৈরি করতে ৩৬০ জন শ্রমিকের ২৫ দিন লাগে। ১৮ দিনে কাজটি শেষ করতে কতজন অতিরিক্ত শ্রমিক লাগবে
Return only the final answer.
```

English:

```text
To build a dam, 360 workers are needed for 25 days. How many extra workers are needed to finish it in 18 days?
Return only the final answer.
```

Current Banglish:

```text
ekoti bandh toiri korote 360 jon shromiker 25 din lage. 18 dine kajoti shesh korote kotojon otirikt shromik lagobe
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti bandh toiri korte 360 jon shromiker 25 din lage. 18 dine kajoti shesh korte kotojon otirikt shromik lagobe
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 18. banglamath_0189

- CSV row: 19
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 3
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); korote->korte (2)

Bangla:

```text
একটি কাজ ২ জন পুরুষ অথবা ৩ জন বালক সম্পন্ন করতে পারে। ৯ জন বালক কতজন পুরুষের সমান কাজ করতে পারবে
Return only the final answer.
```

English:

```text
A task can be completed by 2 men or 3 boys. How many men are equivalent to 9 boys?
Return only the final answer.
```

Current Banglish:

```text
ekoti kaj 2 jon purush othoba 3 jon balok somponn korote pare. 9 jon balok kotojon purusher soman kaj korote parobe
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti kaj 2 jon purush othoba 3 jon balok somponn korte pare. 9 jon balok kotojon purusher soman kaj korte parobe
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 19. banglamath_0539

- CSV row: 20
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 3
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1)

Bangla:

```text
একটি ঘরের মেঝে কার্পেট দিয়ে মুড়তে প্রতি বর্গমিটারে ৭.৫০ টাকা দরে ১১০২.৫০ টাকা খরচ হলে ঘরের ক্ষেত্রফল কত
Return only the final answer.
```

English:

```text
If carpeting a floor costs 7.50 Taka per sq. meter and the total cost is 1102.50 Taka, what is the area of the floor?
Return only the final answer.
```

Current Banglish:

```text
ekoti ghorer mejhe karpet diye murote proti borgomitare 7.50 taka dore 1102.50 taka khoroch hole ghorer kshetrofol kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti ghorer mejhe karpet diye murote proti borgomitare 7.50 taka dore 1102.50 taka khoroch hole ghorer khetrofol koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 20. banglamath_0542

- CSV row: 21
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 3
- Artifact patterns: `none`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: doirghy->doirgho (1); kot->koto (1); prosth->prostho (1)

Bangla:

```text
রাস্তাবাদে বাগানের পরিসীমায় বেড়া দিতে প্রতি মিটারে ২৫ টাকা হিসেবে মোট কত খরচ হবে যদি রাস্তাবাদে বাগানের দৈর্ঘ্য ৪৪ মি ও প্রস্থ ২৪ মি হয়
Return only the final answer.
```

English:

```text
If the garden including the path is 44m by 24m, and fencing costs 25 Taka per meter, what is the total cost?
Return only the final answer.
```

Current Banglish:

```text
rastabade baganer porisimay bera dite proti mitare 25 taka hisebe mot kot khoroch hobe jodi rastabade baganer doirghy 44 mi o prosth 24 mi hoy
Return only the final answer.
```

Auto-suggested Banglish:

```text
rastabade baganer porisimay bera dite proti mitare 25 taka hisebe mot koto khoroch hobe jodi rastabade baganer doirgho 44 mi o prostho 24 mi hoy
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 21. banglamath_0559

- CSV row: 22
- Dataset: `banglamath`
- Task type: `short_answer`
- Answer type: `short_answer`
- Priority: `both_wrong_multi_edit`
- Replacement count: 3
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1)

Bangla:

```text
একটি বর্গক্ষেত্রের পরিসীমা ১৬০ মিটার হলে তার ক্ষেত্রফল কত
Return only the final answer.
```

English:

```text
If a square has a perimeter of 160 meters, what is its area?
Return only the final answer.
```

Current Banglish:

```text
ekoti borgokshetrer porisima 160 mitar hole tar kshetrofol kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti borgokshetrer porisima 160 mitar hole tar khetrofol koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 22. benqa_12th-Biology-I_0265

- CSV row: 23
- Dataset: `benqa`
- Task type: `mcq`
- Answer type: `choice`
- Priority: `both_wrong_multi_edit`
- Replacement count: 3
- Artifact patterns: `ksh_heavy`
- Status: `pending`
- Qwen2.5 v4 correct: `False`
- Qwen3 v4 correct: `False`
- Suggestion notes: achhe->ache (1); ekoti->ekti (1); konoti->konti (1)

Bangla:

```text
মি. 'ক' ব্যবহারিক ক্লাসে একটি নমুনার পর্যবেক্ষণ করে দেখলো মেটাজাইলেম কেন্দ্রের দিকে, ভাস্কুলার বান্ডল ৯টি এবং কিছু এককোষী রোম আছে। পর্যবেক্ষিত বৈশিষ্ট্যগুলো কীভাবে উদ্ভিদকে বাঁচিয়ে রাখতে সাহায্য করে? i. পানি ও খনিজ লবণ পরিবহন করে ii. প্রস্তুতকৃত খাবার পরিবহন করে iii. খাদ্য প্রস্তুত করে নিচের কোনটি সঠিক?
A. i ও ii
B. ii ও iii
C. i ও iii
D. i, ii, ও iii
Answer with only A, B, C, or D.
```

English:

```text
Mr. 'X' observed a transverse section of a sample and noticed that metaxylem is present towards the center, 9 (nine) vascular bundles and there are some unicellular hairs. How does the observe features help to protect the plant? i. By transporting water and mineral salts ii. By transporting prepared food iii. By preparing food Which one is correct?
A. i & ii
B. ii & iii
C. i & iii
D. i, ii & iii
Answer with only A, B, C, or D.
```

Current Banglish:

```text
mi. 'k' byoboharik klase ekoti nomunar poryobekshon kore dekholo metajailem kendrer dike, bhaskular bandol 9ti ebong kichhu ekokoshi rom achhe. poryobekshit boishishtyogulo kibhabe udbhidoke banchiye rakhote sahajy kore? i. pani o khonij lobon poribohon kore ii. prostutokrit khabar poribohon kore iii. khaddo prostut kore nicher konoti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

Auto-suggested Banglish:

```text
mi. 'k' byoboharik klase ekti nomunar poryobekshon kore dekholo metajailem kendrer dike, bhaskular bandol 9ti ebong kichhu ekokoshi rom ache. poryobekshit boishishtyogulo kibhabe udbhidoke banchiye rakhote sahajy kore? i. pani o khonij lobon poribohon kore ii. prostutokrit khabar poribohon kore iii. khaddo prostut kore nicher konti sothik?
A. i o ii
B. ii o iii
C. i o iii
D. i, ii, o iii
Answer with only A, B, C, or D.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 23. banglamath_0188

- CSV row: 24
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
২৫ জন লোক দৈনিক ৬ ঘণ্টা পরিশ্রম করে একটি কাজ ৮ দিনে শেষ করে। ১০ জন লোক দৈনিক কত ঘণ্টা পরিশ্রম করে ঐ কাজটি শেষ করবে
Return only the final answer.
```

English:

```text
25 people working 6 hours a day complete a job in 8 days. How many hours per day must 10 people work to complete the same job?
Return only the final answer.
```

Current Banglish:

```text
25 jon lok doinik 6 ghonta porishrom kore ekoti kaj 8 dine shesh kore. 10 jon lok doinik kot ghonta porishrom kore oi kajoti shesh korobe
Return only the final answer.
```

Auto-suggested Banglish:

```text
25 jon lok doinik 6 ghonta porishrom kore ekti kaj 8 dine shesh kore. 10 jon lok doinik koto ghonta porishrom kore oi kajoti shesh korobe
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 24. banglamath_0231

- CSV row: 25
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
একটি কলম ২০% লাভে ২৪ টাকায় বিক্রয় করলে ক্রয়মূল্য কত
Return only the final answer.
```

English:

```text
If a pen is sold for 24 Taka with 20% profit, what was the cost price?
Return only the final answer.
```

Current Banglish:

```text
ekoti kolom 20% labhe 24 takay bikroy korole kroyomuly kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti kolom 20% labhe 24 takay bikroy korole kroyomuly koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank

## 25. banglamath_0232

- CSV row: 26
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
একটি বই ১৫% কমিশনে ১৭০ টাকায় বিক্রয় করলে প্রকৃত মূল্য কত
Return only the final answer.
```

English:

```text
If a book is sold at 15% commission for 170 Taka, what is its actual price?
Return only the final answer.
```

Current Banglish:

```text
ekoti boi 15% komishone 170 takay bikroy korole prokrit muly kot
Return only the final answer.
```

Auto-suggested Banglish:

```text
ekti boi 15% komishone 170 takay bikroy korole prokrit muly koto
Return only the final answer.
```

Reviewed Banglish in queue:

```text

```

Quality label in queue: `blank`

Review notes in queue: blank
