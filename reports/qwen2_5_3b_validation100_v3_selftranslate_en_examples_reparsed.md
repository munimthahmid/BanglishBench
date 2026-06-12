# Self-Normalization Rewrite Report

Items: `data/slices/validation_100_v3.jsonl`
Eval rows: `results/runs/qwen2_5_3b_validation100_v3_selftranslate_en/results/runs/qwen2_5_3b_validation100_v3_selftranslate_en.jsonl`
Examples exported: 24

Compare file: `results/analysis/qwen2_5_3b_validation100_v3_baseline_vs_selftranslate_en_items_reparsed.csv`

## 1. banglamath_0182 (banglamath)

Gold: `৬০০ টাকা`
Self-normalized parsed: `The calculation can be broken down as follows:`; correct: `False`

Baseline parsed: `280 * 15 = 4200`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
7 keji chaler dam 280 taka hole 15 keji chaler dam kot
Return only the final answer.
```

**Model Rewrite**

```text
7 keji chaler dam 280 taka hole 15 keji chaler dam kot
```

**Final Raw Output**

```text
The calculation can be broken down as follows:

7 keji * 280 taka/keji + 15 keji * 280 taka/keji

First, calculate the total amount for 7 keji:
7 * 280 = 1960 t
```


## 2. banglamath_0183 (banglamath)

Gold: `৩০ দিন`
Self-normalized parsed: `The evaluation suggests that at Ekotir Chatrabi, 50 Joner earn 15 Day Khadyo, while 25 Day Khadyo earn 25 Days.`; correct: `False`

Baseline parsed: `Khady mojud achhe 50 joner, na-achhe 25 joner.`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
ekoti chhatrabase 50 joner 15 diner khady mojud achhe. oi khadye 25 joner kot din cholobe
Return only the final answer.
```

**Model Rewrite**

```text
at ekotir chatrabi 50 joner 15 day khadyo ashbe. Aise khadyo 25 day koti cholo.
```

**Final Raw Output**

```text
The evaluation suggests that at Ekotir Chatrabi, 50 Joner earn 15 Day Khadyo, while 25 Day Khadyo earn 25 Days.
```


## 3. banglamath_0185 (banglamath)

Gold: `২০০ কেজি`
Self-normalized parsed: `To solve this problem, we need to determine how many days remain after accounting for both the initial travel period and the subsequent leave period.`; correct: `False`

Baseline parsed: `120 keji chale 27 + 45 = 72 din cholote koto keji chal proyojon hobe.`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
120 keji chale 10 jon loker 27 din chole. 45 din cholote kot keji chal proyojon hobe
Return only the final answer.
```

**Model Rewrite**

```text
120 days travel 10 months leave 27 days remain. 45 days remaining in the country will be required
```

**Final Raw Output**

```text
To solve this problem, we need to determine how many days remain after accounting for both the initial travel period and the subsequent leave period.

1. The total travel duration is 120 days.
2. The leave duration is 27 days.
3. We start by subtracting the leave duration from the travel
```


## 4. banglamath_0226 (banglamath)

Gold: `২৫০ টাকা`
Self-normalized parsed: `The given verse appears to be in Bengali and translates roughly to English as: "From the fifth verse of 5:6, the first chapter begins with this line." However, without the full context or the original text, an exact translation or detailed explanation cannot be provided.`; correct: `False`

Baseline parsed: `150`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
550 takake 5:6 onupate bhag korole prothom ongsh kot hobe
Return only the final answer.
```

**Model Rewrite**

```text
Fifth of verse 5:6 on upato bhaga korle prothom ongo kot hobe
```

**Final Raw Output**

```text
The given verse appears to be in Bengali and translates roughly to English as: "From the fifth verse of 5:6, the first chapter begins with this line." However, without the full context or the original text, an exact translation or detailed explanation cannot be provided.
```


## 5. banglamath_0227 (banglamath)

Gold: `৭.৫ কিমি`
Self-normalized parsed: `The first boy went to school 5 times a day, while the second boy went to school once a day. The first boy also went to school an additional time compared to the second boy's schedule, making it 6 times a day in total for him.`; correct: `False`

Baseline parsed: `1:1`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
dui bondhur bari theke skuler durotber onupat 2:3 ebong prothom bondhur durotb 5 kimi hole dbitiy bondhur durotb kot
Return only the final answer.
```

**Model Rewrite**

```text
two boys from the village went to school twice a day for 2:30 and the first boy went to school five times a day whereas the second boy went to school every day
```

**Final Raw Output**

```text
The first boy went to school 5 times a day, while the second boy went to school once a day. The first boy also went to school an additional time compared to the second boy's schedule, making it 6 times a day in total for him.
```


## 6. banglamath_0228 (banglamath)

Gold: `২/৫`
Self-normalized parsed: `The evaluated process involves 40% correctness in its steps.`; correct: `False`

Baseline parsed: `40% of the population reads or writes`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
40% ke sadharon bhognangshe prokash korole ki hoy
Return only the final answer.
```

**Model Rewrite**

```text
40% of the steps involved in the process are followed correctly
```

**Final Raw Output**

```text
The evaluated process involves 40% correctness in its steps.
```


## 7. banglamath_0229 (banglamath)

Gold: `1.5`
Self-normalized parsed: `3.75 times the daily consumption will be provided.`; correct: `False`

Baseline parsed: `50%`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
150% ke doshomik bhognangshe prokash korole ki hoy
Return only the final answer.
```

**Model Rewrite**

```text
150% of the daily consumption will be provided
```

**Final Raw Output**

```text
3.75 times the daily consumption will be provided.
```


## 8. banglamath_0230 (banglamath)

Gold: `20%`
Self-normalized parsed: `The given text "25 taka 125 takar shotokora kot" appears to be in Bengali and translates roughly to "25 taka 125 takar shotokora kot" in English, but it lacks proper context or punctuation for clear understanding. Without additional information, it`; correct: `False`

Baseline parsed: `125/25 = 5`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
25 taka 125 takar shotokora kot
Return only the final answer.
```

**Model Rewrite**

```text
25 taka 125 takar shotokora kot
```

**Final Raw Output**

```text
The given text "25 taka 125 takar shotokora kot" appears to be in Bengali and translates roughly to "25 taka 125 takar shotokora kot" in English, but it lacks proper context or punctuation for clear understanding. Without additional information, it
```


## 9. banglamath_0231 (banglamath)

Gold: `২০ টাকা`
Self-normalized parsed: `To determine the final score for the items that did not score 24, we need to establish the initial score and the decrement applied to the remaining items.`; correct: `False`

Baseline parsed: `Ekot kolom 20% labhe 24 takay bikroy korle kroyomuly kot.`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
ekoti kolom 20% labhe 24 takay bikroy korole kroyomuly kot
Return only the final answer.
```

**Model Rewrite**

```text
twenty percent of the items scored 24, while the rest decreased by the same amount.
```

**Final Raw Output**

```text
To determine the final score for the items that did not score 24, we need to establish the initial score and the decrement applied to the remaining items.

Given:
- Twenty percent of the items scored 24.
- The rest of the items decreased by the same amount.

Let's denote:
- Total number
```


## 10. banglamath_0232 (banglamath)

Gold: `২০০ টাকা`
Self-normalized parsed: `To calculate the commission earned, we use the formula:`; correct: `False`

Baseline parsed: `Ekti boi komishon 170 takar biyakro korole proritite muly kot 15%.`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
ekoti boi 15% komishone 170 takay bikroy korole prokrit muly kot
Return only the final answer.
```

**Model Rewrite**

```text
15% commission earned on a sale of 170 thousand taka
```

**Final Raw Output**

```text
To calculate the commission earned, we use the formula:

\[ \text{Commission} = \text{Sale Amount} \times \text{Commission Rate} \]

Given:
- Sale Amount = 170 thousand taka = 170,000 taka
- Commission Rate =
```


## 11. banglamath_0233 (banglamath)

Gold: `৭ দিন`
Self-normalized parsed: `The statement "24 people live in one room" contradicts the information that "28 people live in one room." Therefore, the correct information should be "28 people live in one room."`; correct: `False`

Baseline parsed: `6 jon lok ekoti kaj 28 dine korole 24 jon lok kot dine korobe = 10 jon lok`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
6 jon lok ekoti kaj 28 dine korole 24 jon lok kot dine korobe
Return only the final answer.
```

**Model Rewrite**

```text
6 people live in one house and 28 people live in one room but 24 people live in one room
```

**Final Raw Output**

```text
The statement "24 people live in one room" contradicts the information that "28 people live in one room." Therefore, the correct information should be "28 people live in one room."
```


## 12. banglamath_0234 (banglamath)

Gold: `৬ দিন`
Self-normalized parsed: `The question "ekot? and k 10 dine o kh 15 dine korole tara ekot? r kot dine korob?" translates to English as "What is the interest rate for a loan of k 10,000 or k 15,000 per day`; correct: `False`

Baseline parsed: `ekot kaj k 10 dine, o kh 15 dine korole tara ekotre kot dine korobe`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
ekoti kaj k 10 dine o kh 15 dine korole tara ekotre kot dine korobe
Return only the final answer.
```

**Model Rewrite**

```text
ekot? and k 10 dine o kh 15 dine korole tara ekot? r kot dine korob?
```

**Final Raw Output**

```text
The question "ekot? and k 10 dine o kh 15 dine korole tara ekot? r kot dine korob?" translates to English as "What is the interest rate for a loan of k 10,000 or k 15,000 per day
```


## 13. banglamath_0236 (banglamath)

Gold: `১২ টাকা`
Self-normalized parsed: `The statement provided does not contain enough information to determine the cost of the 2nd bottle opener, as it is stated to "cost more" without specifying how much more or by how much. Therefore, no specific numerical answer can be given for the cost of the 2nd bottle opener based on the information provided.`; correct: `False`

Baseline parsed: `80 taka`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
10ti bolopener dam 60 taka hole 2ti bolopener dam kot
Return only the final answer.
```

**Model Rewrite**

```text
10th bottle opener costs 60 taka while 2nd bottle opener costs more
```

**Final Raw Output**

```text
The statement provided does not contain enough information to determine the cost of the 2nd bottle opener, as it is stated to "cost more" without specifying how much more or by how much. Therefore, no specific numerical answer can be given for the cost of the 2nd bottle opener based on the information provided.
```


## 14. banglamath_0518 (banglamath)

Gold: `১৫০ মিটার`
Self-normalized parsed: `The given text appears to be in a language other than English and does not provide clear information that can be directly evaluated without translation. However, based on the structure and content, it seems to be describing a situation involving 400 people from a specific area or group. Without further context or translation, I cannot provide`; correct: `False`

Baseline parsed: `ekoti ayotakar baganer doirghy prosther tinogun ebong porisima 400 mitar hole baganer doirghy kot`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
ekoti ayotakar baganer doirghy prosther tinogun ebong porisima 400 mitar hole baganer doirghy kot
Return only the final answer.
```

**Model Rewrite**

```text
ekoti ayotakar baganer doirghy prosther tinogun ebong porisima 400 mitar hole baganer doirghy kot
```

**Final Raw Output**

```text
The given text appears to be in a language other than English and does not provide clear information that can be directly evaluated without translation. However, based on the structure and content, it seems to be describing a situation involving 400 people from a specific area or group. Without further context or translation, I cannot provide
```


## 15. banglamath_0519 (banglamath)

Gold: `৭৫০০ বর্গমিটার`
Self-normalized parsed: `The given text appears to be in a language other than English and seems to contain numbers and possibly names or place-related information. Without additional context, it's challenging to provide a precise translation or detailed analysis. However, based on the numerical part provided (150 mitar o prosth 50 mitar),`; correct: `False`

Baseline parsed: `kshetrofol kot 200 mitar`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
ekoti ayotakar baganer doirghy 150 mitar o prosth 50 mitar hole kshetrofol kot
Return only the final answer.
```

**Model Rewrite**

```text
ekoti ayotakar baganer doirghy 150 mitar o prosth 50 mitar hole kshetrofol kot
```

**Final Raw Output**

```text
The given text appears to be in a language other than English and seems to contain numbers and possibly names or place-related information. Without additional context, it's challenging to provide a precise translation or detailed analysis. However, based on the numerical part provided (150 mitar o prosth 50 mitar),
```


## 16. banglamath_0522 (banglamath)

Gold: `১৭৬ বর্গমিটার`
Self-normalized parsed: `Unfortunately, no roads are listed or described in the given context. Therefore, it is impossible to determine which road the two brothers took to reach their village based on the information provided.`; correct: `False`

Baseline parsed: `jomir bhitore 2 mitar choora rasta thakole, jomir kshetrofol kot rastabade`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
jomir bhitore 2 mitar choora rasta thakole rastabade jomir kshetrofol kot
Return only the final answer.
```

**Model Rewrite**

```text
which of the following roads did the two brothers take to reach their village?
```

**Final Raw Output**

```text
Unfortunately, no roads are listed or described in the given context. Therefore, it is impossible to determine which road the two brothers took to reach their village based on the information provided.
```


## 17. banglamath_0526 (banglamath)

Gold: `৩০ বর্গ মিটার`
Self-normalized parsed: `The given phrase "equilateral triangle's base 10 meters and height 6 meters hole kshetrafol kot" does not appear to be a standard mathematical or geographical question, nor is it clear what "hole kshetrafol kot" means in this context. Without additional clarification, it's not`; correct: `False`

Baseline parsed: `60`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
ekoti tribhujer bhumi 10 mitar o uchchota 6 mitar hole kshetrofol kot
Return only the final answer.
```

**Model Rewrite**

```text
equilateral triangle's base 10 meters and height 6 meters hole kshetrafol kot
```

**Final Raw Output**

```text
The given phrase "equilateral triangle's base 10 meters and height 6 meters hole kshetrafol kot" does not appear to be a standard mathematical or geographical question, nor is it clear what "hole kshetrafol kot" means in this context. Without additional clarification, it's not
```


## 18. banglamath_0533 (banglamath)

Gold: `৬৬৬ মেট্রিক টন ৬৬৬ কেজি ৬৬৬ গ্রাম (প্রায়)`
Self-normalized parsed: `"Two thousand metric tons of rice are supposed to be delivered by the first party."`; correct: `False`

Baseline parsed: `20000`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
ek mase 20000 metrik ton rod toiri hole doinik ki poriman rod toiri hoy
Return only the final answer.
```

**Model Rewrite**

```text
two thousand metric tons of rice are supposed to be delivered by the first party
```

**Final Raw Output**

```text
"Two thousand metric tons of rice are supposed to be delivered by the first party."
```


## 19. banglamath_0538 (banglamath)

Gold: `৩৮৪ বর্গ মিটার`
Self-normalized parsed: `The given text appears to be in a language other than English, likely a local dialect or language. A careful translation and interpretation of the provided information would be:`; correct: `False`

Baseline parsed: `ekoti ayotakar baganer doirghy 60 mitar o prosth 38 mitar.`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
ekoti ayotakar baganer doirghy 60 mitar o prosth 40 mitar. er bhitore 2 mitar choora rasta thakole rastar kshetrofol kot
Return only the final answer.
```

**Model Rewrite**

```text
ekoti ayotakar baganer doirghy 60 mitar o prosth 40 mitar. er bhitore 2 mitar choora rasta thakole rastar kshetrofol kot
```

**Final Raw Output**

```text
The given text appears to be in a language other than English, likely a local dialect or language. A careful translation and interpretation of the provided information would be:

Ekti omar (1 person) has 60 mitar (units) of baganer (likely referring to a type of crop or agricultural
```


## 20. banglamath_0540 (banglamath)

Gold: `২১ মিটার`
Self-normalized parsed: `To accurately evaluate this statement, we need more specific information about Ekot's layout or arrangement. Without details on how the streets are laid out or numbered, it's impossible to determine the exact distances of the fourth and 147th neighbors from the fourth street. Therefore, no definitive statement can be made based solely`; correct: `False`

Baseline parsed: `ekoti ghorer doirghy prosther tinogun ebong kshetrofol 147 borgomitar hole ghorotir doirghy kot`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
ekoti ghorer doirghy prosther tinogun ebong kshetrofol 147 borgomitar hole ghorotir doirghy kot
Return only the final answer.
```

**Model Rewrite**

```text
which of the following is true for ekot's fourth neighbor and its 147th neighbor regarding their distance from the fourth street
Which of the following statements is true about ekot's fourth neighbor and its 147th neighbor concerning their distance from the fourth street
```

**Final Raw Output**

```text
To accurately evaluate this statement, we need more specific information about Ekot's layout or arrangement. Without details on how the streets are laid out or numbered, it's impossible to determine the exact distances of the fourth and 147th neighbors from the fourth street. Therefore, no definitive statement can be made based solely
```


## 21. banglamath_0541 (banglamath)

Gold: `৪৪৪ বর্গমিটার`
Self-normalized parsed: `The final answer is: 83 miles`; correct: `False`

Baseline parsed: `Ekoti ayotakar baganer doirghy 80 mi o prosth 30 mi. Er bhitore 3 mitar choora rasta thakole rastar kshetrofol kot.`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
ekoti ayotakar baganer doirghy 50 mi o prosth 30 mi. er bhitore 3 mitar choora rasta thakole rastar kshetrofol kot
Return only the final answer.
```

**Model Rewrite**

```text
ekoti ayotakar baganer doirghy 50 miles o prosth 30 miles. er bhitore 3 miles chhora rasta thakole rastar kshetrofol kot
```

**Final Raw Output**

```text
The final answer is: 83 miles
```


## 22. banglamath_0549 (banglamath)

Gold: `৪৫০ বর্গমিটার`
Self-normalized parsed: `The road width is 2.5 meters and the length of the road section is 50 meters. The total area of the road section is 125 square meters.`; correct: `False`

Baseline parsed: `Ekotii baganere baire 2.5 mitar choora rasta thakle, rastar kshetrafole kot jodi baganere doirghy 50 mi o prosth 35 mi hoy.`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
ekoti baganer baire 2.5 mitar choora rasta thakole rastar kshetrofol kot jodi baganer doirghy 50 mi o prosth 35 mi hoy
Return only the final answer.
```

**Model Rewrite**

```text
ekoti baganer baire 2.5 meters choora rasta thakole rastar kshetrofol kot jodi baganer doirghy 50 meters o prosth 35 meters hoy
```

**Final Raw Output**

```text
The road width is 2.5 meters and the length of the road section is 50 meters. The total area of the road section is 125 square meters.
```


## 23. banglamath_0550 (banglamath)

Gold: `২২৫৬.২৫ বর্গমিটার`
Self-normalized parsed: `None of the provided sentences have the same meaning as "190 houses in the street have 190 meters of pavement the sidewalk 190 meters long has 190 shops on both sides." The original sentence describes houses and pavement, while the second part about a sidewalk with shops is unrelated and`; correct: `False`

Baseline parsed: `Rastasoh baganer porisima 190 mitar hole soman porisima bishisht borgakar mather kshetrofol kot`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
rastasoh baganer porisima 190 mitar hole soman porisima bishisht borgakar mather kshetrofol kot
Return only the final answer.
```

**Model Rewrite**

```text
which of the following sentences has the same meaning as the sentence given above
190 houses in the street have 190 meters of pavement the sidewalk 190 meters long has 190 shops on both sides
```

**Final Raw Output**

```text
None of the provided sentences have the same meaning as "190 houses in the street have 190 meters of pavement the sidewalk 190 meters long has 190 shops on both sides." The original sentence describes houses and pavement, while the second part about a sidewalk with shops is unrelated and
```


## 24. banglamath_0552 (banglamath)

Gold: `৪৫০০ বর্গগজ`
Self-normalized parsed: `The given text appears to be in a language other than English, possibly a local or regional language. Without direct translation, it's challenging to provide an exact interpretation or answer in the required format. However, based on the structure and content, it seems to describe a measurement or comparison of some kind between two areas or regions`; correct: `False`

Baseline parsed: `Ekoti samantorikar bhumi 40 goj o uchchota hole tar kshetrafol kot.`; baseline correct: `False`
Change: `same_wrong`

**Banglish Input**

```text
ekoti samantoriker bhumi 90 goj o uchchota 50 goj hole tar kshetrofol kot
Return only the final answer.
```

**Model Rewrite**

```text
ekoti samantoriker bhumi 90 goj o uchchota 50 goj hole tar kshetrafol kot
```

**Final Raw Output**

```text
The given text appears to be in a language other than English, possibly a local or regional language. Without direct translation, it's challenging to provide an exact interpretation or answer in the required format. However, based on the structure and content, it seems to describe a measurement or comparison of some kind between two areas or regions
```

