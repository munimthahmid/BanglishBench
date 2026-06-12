# Self-Normalization Rewrite Report

Items: `data/slices/mgsm_bn_50_v1.jsonl`
Eval rows: `results/runs/qwen3_4b_mgsm_bn50_selftranslate/results/runs/qwen3_4b_mgsm_bn50_selftranslate.jsonl`
Examples exported: 5

Compare file: `results/analysis/qwen3_mgsm_bn50_baseline_vs_selftranslate_items_reparsed.csv`

## 1. mgsm_bn_0005 (mgsm)

Gold: `20`
Self-normalized parsed: `There are 20 messengers in total`; correct: `False`

Baseline parsed: `20`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
oyendi protidin tanr protyekoti murogike susth rakhar jony tin kap kore murogir khabarer mishron khaoyan jate dana, milooyarm ebong sobji thake. tini murogider tinobare alada-alada kore khabar den. sokale, tini murogir jhankoke 15 kap khabar den. bikele, murogider tini aroo 25 kap khabar den. oyendir murogir jhanke jodi 20ti murogi thake tahole murogider diner shesh khabar khaoyanor jony tanke kot kap khabar dite hobe?
Return only the final answer.
```

**Model Rewrite**

```text
In a village, the number of people who receive news through the medium of a messenger is distributed as follows: in the morning, 15 people receive news; in the afternoon, 25 people receive news. If there are 20 messengers in total, how many people will receive news in the evening?
```

**Final Raw Output**

```text
The problem states:

- In the morning: 15 people receive news  
- In the afternoon: 25 people receive news  
- There are 20 messengers in total  

We are asked: **How many people will receive news in the evening?**

However, the information provided does not specify how the messengers distribute the news or whether each messenger delivers news to a certain number of people. It only gives the number of people who received news in the morning and afternoon.

There is **no direct information** about how many people receive news in the evening, nor is there a rule or pattern (like each messenger delivering
```


## 2. mgsm_bn_0017 (mgsm)

Gold: `230`
Self-normalized parsed: `230`; correct: `True`

Baseline parsed: `150 মাইল`; baseline correct: `False`
Change: `gain`

**Banglish Input**

```text
duti tren ekoi somoye san rafayel theke jatra shuru kore. tara poshchimer dike jete shuru kore, ubhoyoi 80 mail kore jatra kore. porer din, tara uttorer dike jatra kore 150 mail poth jaoya sompurn kore. tahole duidine protiti tren kot durotb otikrom korechhe?
Return only the final answer.
```

**Model Rewrite**

```text
Two trains started from the same point at the same time. One train started towards the south and travelled 80 miles. The next day, the train started towards the north and travelled 150 miles. How much distance did the two trains cover in total?
```

**Final Raw Output**

```text
The two trains started from the same point at the same time.  

- The first train travelled 80 miles south.  
- The second train started the next day and travelled 150 miles north.  

Since they started at different times (one on the first day, the other the next day), we are only asked for the total distance covered by both trains, not the distance between them or their relative positions.

So, total distance covered = distance by first train + distance by second train  
= 80 miles + 150 miles  
= 230 miles

Final answer: 230
```


## 3. mgsm_bn_0023 (mgsm)

Gold: `7`
Self-normalized parsed: `8`; correct: `False`

Baseline parsed: `7`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
bili DVD bikroy koren. monggolobare tanr 8 jon grahok hoyechhe. tanr prothom 3 jon grahoker protyeke ekoti kore DVD kroy koren. poroborti 2 jon grahoker protyeke 2ti kore DVD kroy koren. tanr shesh 3 jon grahok konoo DVD kroy korenoni. bili monggolobare kotoguli DVD bikroy korechhen?
Return only the final answer.
```

**Model Rewrite**

```text
How many Mongolobare people bought DVD?  
8 people bought DVD.  
First 3 people bought DVD each.  
Next 2 people bought DVD each.  
Remaining 3 people did not buy any DVD.  
How many Mongolobare people bought DVD?
```

**Final Raw Output**

```text
8 people bought DVD.  

Final answer: 8
```


## 4. mgsm_bn_0024 (mgsm)

Gold: `8`
Self-normalized parsed: `The radius is reduced by 2 centimeters — this is a change in radius, not a time-based change.`; correct: `False`

Baseline parsed: `8`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
ekoti momobati jbolole seti proti ghontay 2 sentimitar kore gole jay. 1:00 PM theke 5:00 PM poryont jbolar por ekoti momobati kot sentimitar chhot hoye jabe?
Return only the final answer.
```

**Model Rewrite**

```text
How much will each diameter decrease if the radius is reduced by 2 centimeters from 1:00 PM to 5:00 PM?
```

**Final Raw Output**

```text
The question contains a logical inconsistency and lacks meaningful mathematical or physical context.

- The radius is reduced by 2 centimeters — this is a change in radius, not a time-based change.
- The time from 1:00 PM to 5:00 PM (4 hours) is irrelevant to the relationship between radius and diameter unless there's a dynamic process (e.g., shrinking over time), which is not described.
- Diameter is directly related to radius: diameter = 2 × radius. So, if the radius decreases by 2 cm, the diameter also decreases by 2 × 2 = 4 cm.
```


## 5. mgsm_bn_0025 (mgsm)

Gold: `26`
Self-normalized parsed: `0.25C`; correct: `False`

Baseline parsed: `26`; baseline correct: `True`
Change: `loss`

**Banglish Input**

```text
kail got bochhorer sobotheke beshi bikroy hooya boiti $19.50 mulye kinechhilen. ja asol mulyer opor 25% chhare paoya giyechhil. boitir asol muly kot chhil?
Return only the final answer.
```

**Model Rewrite**

```text
Kail got a profit of $19.50 on the total selling price. The profit is 25% of the cost price. What is the cost price?
```

**Final Raw Output**

```text
We are given:

- Kail made a profit of $19.50 on the **total selling price**.
- This profit is **25% of the cost price**.

We are to find the **cost price**.

---

Let the **cost price** be $ C $.

We are told that the profit is 25% of the cost price:

$$
\text{Profit} = 25\% \text{ of } C = 0.25C
$$

We are also told that this profit is $19.50:

$$
0.25C
```

