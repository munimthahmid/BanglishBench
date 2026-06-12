# Validation-200 v5 Substitution Review Playbook

Updated: 2026-06-11

This playbook turns the repeated substitution summary into a practical
human-review sequence. It is not an auto-accept list; every row must still
be checked against the Bangla and English source views.

## Inputs

- `data/slices/validation_200_v5_review_queue.csv`
- `results/analysis/validation200_v5_review_impact_ranking.csv`
- `results/analysis/validation200_v5_review_impact_substitutions.csv`

## Batch Review Order

The order prioritizes current pending-row coverage, then tier-1 and
held-out test coverage. Impact scores are still shown so high-value rows
remain visible during review.

| Order | Substitution | Rows | Tier-1 rows | Test rows | Mean score | First examples |
| ---: | --- | ---: | ---: | ---: | ---: | --- |
| 1 | `kot` -> `koto` | 72 | 17 | 55 | 115.3 | benqa_8th-Math_0167; banglamath_0526; banglamath_0230; banglamath_0231; benqa_8th-Math_0085 |
| 2 | `konoti` -> `konti` | 56 | 23 | 45 | 110.9 | benqa_12th-Chemistry-II_0228; benqa_12th-Physics-II_0046; benqa_10th-Physics_0021; benqa_8th-Science_0202; benqa_12th-Biology-II_0287 |
| 3 | `ekoti` -> `ekti` | 37 | 13 | 26 | 133.9 | benqa_10th-Math_0044; benqa_12th-Chemistry-II_0228; benqa_8th-Math_0167; banglamath_0526; benqa_12th-Biology-I_0265 |
| 4 | `kshetrofol` -> `khetrofol` | 13 | 6 | 10 | 137.8 | banglamath_0526; banglamath_0552; banglamath_0538; banglamath_0541; banglamath_0549 |
| 5 | `doirghy` -> `doirgho` | 11 | 5 | 8 | 136.9 | benqa_8th-Math_0167; banglamath_0538; banglamath_0541; banglamath_0549; banglamath_0540 |
| 6 | `prosth` -> `prostho` | 9 | 4 | 7 | 138 | benqa_8th-Math_0167; banglamath_0538; banglamath_0541; banglamath_0549; banglamath_0519 |
| 7 | `ayotakar` -> `ayotokar` | 7 | 3 | 5 | 138.9 | benqa_8th-Math_0167; banglamath_0538; banglamath_0541; banglamath_0519; banglamath_0558 |
| 8 | `korote` -> `korte` | 7 | 1 | 5 | 118.7 | banglamath_1688; benqa_10th-Physics_0106; banglamath_1691; banglamath_0184; banglamath_0189 |
| 9 | `achhe` -> `ache` | 6 | 3 | 5 | 145.5 | benqa_10th-Math_0044; benqa_12th-Biology-I_0265; benqa_8th-Science_0127; banglamath_1691; banglamath_0183 |
| 10 | `thakole` -> `thakle` | 5 | 3 | 4 | 135.8 | banglamath_0538; banglamath_0541; banglamath_0549; banglamath_0522; banglamath_0181 |

## Review Rules

- Work substitution groups in the order above, but write decisions row by row.
- Repeated edit patterns are evidence for review efficiency, not authority.
- Prefer the shortest natural Banglish spelling that preserves the source meaning.
- Keep MCQ option labels and answer-only instructions unchanged.
- Do not normalize domain terms so aggressively that a real Banglish reader would
  see a different word.

## Batch Coverage

Rows overlap across substitutions. The cumulative column estimates how many
unique queue rows are reached if groups are reviewed in this order.

| Order | Substitution | Matching rows | New rows | Cumulative rows |
| ---: | --- | ---: | ---: | ---: |
| 1 | `kot->koto` | 72 | 72 | 72 |
| 2 | `konoti->konti` | 56 | 55 | 127 |
| 3 | `ekoti->ekti` | 37 | 9 | 136 |
| 4 | `kshetrofol->khetrofol` | 13 | 1 | 137 |
| 5 | `doirghy->doirgho` | 11 | 0 | 137 |
| 6 | `prosth->prostho` | 9 | 0 | 137 |
| 7 | `ayotakar->ayotokar` | 7 | 0 | 137 |
| 8 | `korote->korte` | 7 | 1 | 138 |
| 9 | `achhe->ache` | 6 | 1 | 139 |
| 10 | `thakole->thakle` | 5 | 1 | 140 |

## Terminal Helper Shortcuts

Review one repeated substitution group interactively:

```bash
python3 scripts/review_validation200_v5_queue.py --substitution konoti:konti
```

Combine it with the impact tier filter:

```bash
python3 scripts/review_validation200_v5_queue.py --tier tier_1_review_first --substitution kot:koto
```

## Substitution Packets

### `kot` -> `koto`

Rows: `72`; occurrences: `72`; tier-1 rows: `17`; test rows: `55`.

#### Example 1: `benqa_8th-Math_0167`

- Split: `test`; tier: `tier_1_review_first`; impact score: `173`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `yes`; Qwen3 recoverable: `yes`
- Suggested edits: `ayotakar->ayotokar (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); prosth->prostho (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `ekoti ayotakar baganer doirghy prosther derogun. er prosth 16 mitar hole, baganer porisima kot? A. 40 mitar B. 64 mitar C. 80 mitar D. 96 mitar Answer with only A, B, C, or D.` |
| Suggested Banglish | `ekti ayotokar baganer doirgho prosther derogun. er prostho 16 mitar hole, baganer porisima koto? A. 40 mitar B. 64 mitar C. 80 mitar D. 96 mitar Answer with only A, B, C, or D.` |
| Bangla source | `একটি আয়তাকার বাগানের দৈর্ঘ্য প্রস্থের দেড়গুণ। এর প্রস্থ 16 মিটার হলে, বাগানের পরিসীমা কত? A. 40 মিটার B. 64 মিটার C. 80 মিটার D. 96 মিটার Answer with only A, B, C, or D.` |
| English source | `The length of a rectangular garden is one and half times its breadth. If breadth is 16 metres , what is its peremeter? A. 40m B. 64m C. 80m D. 96m Answer with only A, B, C, or D.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

#### Example 2: `banglamath_0526`

- Split: `test`; tier: `tier_1_review_first`; impact score: `170`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `yes`; Qwen3 recoverable: `yes`
- Suggested edits: `ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); uchchota->ucchota (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `ekoti tribhujer bhumi 10 mitar o uchchota 6 mitar hole kshetrofol kot Return only the final answer.` |
| Suggested Banglish | `ekti tribhujer bhumi 10 mitar o ucchota 6 mitar hole khetrofol koto Return only the final answer.` |
| Bangla source | `একটি ত্রিভুজের ভূমি ১০ মিটার ও উচ্চতা ৬ মিটার হলে ক্ষেত্রফল কত Return only the final answer.` |
| English source | `If a triangle has a base of 10 meters and height of 6 meters, what is its area? Return only the final answer.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

#### Example 3: `banglamath_0230`

- Split: `test`; tier: `tier_1_review_first`; impact score: `155`; priority: `both_wrong_single_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `yes`; Qwen3 recoverable: `yes`
- Suggested edits: `kot->koto (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `25 taka 125 takar shotokora kot Return only the final answer.` |
| Suggested Banglish | `25 taka 125 takar shotokora koto Return only the final answer.` |
| Bangla source | `২৫ টাকা ১২৫ টাকার শতকরা কত Return only the final answer.` |
| English source | `25 Taka is what percent of 125 Taka? Return only the final answer.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

### `konoti` -> `konti`

Rows: `56`; occurrences: `57`; tier-1 rows: `23`; test rows: `45`.

#### Example 1: `benqa_12th-Chemistry-II_0228`

- Split: `test`; tier: `tier_1_review_first`; impact score: `177`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `yes`; Qwen3 recoverable: `yes`
- Suggested edits: `ekoti->ekti (1); konoti->konti (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `Ni(s) + 2Ag^{+}(aq) \xrightarrow{2e^{-}} Ni^{2+}(aq) + 2Ag(s); bikriyatite- i. Ni jarit hoy ii. Ag jarit hoy iii. bikriyati ekoti ridoks bikriya nicher konoti sothik? A. i o ii B. ii o iii C. i o iii D. i, ii o iii Answer with only A, B, C, or D.` |
| Suggested Banglish | `Ni(s) + 2Ag^{+}(aq) \xrightarrow{2e^{-}} Ni^{2+}(aq) + 2Ag(s); bikriyatite- i. Ni jarit hoy ii. Ag jarit hoy iii. bikriyati ekti ridoks bikriya nicher konti sothik? A. i o ii B. ii o iii C. i o iii D. i, ii o iii Answer with only A, B, C, or D.` |
| Bangla source | `Ni(s) + 2Ag^{+}(aq) \xrightarrow{2e^{-}} Ni^{2+}(aq) + 2Ag(s); বিক্রিয়াটিতে- i. Ni জারিত হয় ii. Ag জারিত হয় iii. বিক্রিয়াটি একটি রিডক্স বিক্রিয়া নিচের কোনটি সঠিক? A. i ও ii B. ii ও iii C. i ও iii D. i, ii ও iii Answer with only A, B, C, or D.` |
| English source | `Ni(s) + 2Ag^{+}(aq) \overset{2e^{-}} {\rightarrow}Ni^{2+}(aq) + 2Ag(s); in this reaction- i. Ni becomes oxidized ii. Ag becomes oxidized iii. A redox reaction Which one is correct? A. i and ii B. ii and iii C. i and iii D. i, ii and iii Answer with only A, ...` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

#### Example 2: `benqa_12th-Physics-II_0046`

- Split: `test`; tier: `tier_1_review_first`; impact score: `171`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `yes`; Qwen3 recoverable: `yes`
- Suggested edits: `konoti->konti (1); kshetre->khetre (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `ruddhotapiy poribortoner kshetre- i. hothat songghotit hoy ii. tapomatra sthir thake iii. enotropir poriborton shuny nicher konoti sothik? A. i o ii B. ii o iii C. i o iii D. i, ii o iii Answer with only A, B, C, or D.` |
| Suggested Banglish | `ruddhotapiy poribortoner khetre- i. hothat songghotit hoy ii. tapomatra sthir thake iii. enotropir poriborton shuny nicher konti sothik? A. i o ii B. ii o iii C. i o iii D. i, ii o iii Answer with only A, B, C, or D.` |
| Bangla source | `রুদ্ধতাপীয় পরিবর্তনের ক্ষেত্রে- i. হঠাৎ সংঘটিত হয় ii. তাপমাত্রা স্থির থাকে iii. এনট্রপির পরিবর্তন শূন্য নিচের কোনটি সঠিক? A. i ও ii B. ii ও iii C. i ও iii D. i, ii ও iii Answer with only A, B, C, or D.` |
| English source | `For changing adiabatic process- i. occurs suddenly ii. temperature constant iii. change of entropy is zero Which one is correct? A. i and ii B. ii and iii C. i and iii D. i, ii and iii Answer with only A, B, C, or D.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

#### Example 3: `benqa_10th-Physics_0021`

- Split: `test`; tier: `tier_1_review_first`; impact score: `170`; priority: `both_wrong_single_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `yes`; Qwen3 recoverable: `yes`
- Suggested edits: `konoti->konti (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `konoti moulik ekok? A. jul B. niuton C. kyandela D. pyasokel Answer with only A, B, C, or D.` |
| Suggested Banglish | `konti moulik ekok? A. jul B. niuton C. kyandela D. pyasokel Answer with only A, B, C, or D.` |
| Bangla source | `কোনটি মৌলিক একক? A. জুল B. নিউটন C. ক্যান্ডেলা D. প্যাসকেল Answer with only A, B, C, or D.` |
| English source | `Which one is fundamental unit? A. Joule B. Newton C. Candela D. Pascal Answer with only A, B, C, or D.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

### `ekoti` -> `ekti`

Rows: `37`; occurrences: `40`; tier-1 rows: `13`; test rows: `26`.

#### Example 1: `benqa_10th-Math_0044`

- Split: `test`; tier: `tier_1_review_first`; impact score: `177`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `yes`; Qwen3 recoverable: `yes`
- Suggested edits: `achhe->ache (1); ekoti->ekti (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `ekoti borger kototi protisamy rekha achhe? A. 8ti B. 6ti C. 4ti D. 2ti Answer with only A, B, C, or D.` |
| Suggested Banglish | `ekti borger kototi protisamy rekha ache? A. 8ti B. 6ti C. 4ti D. 2ti Answer with only A, B, C, or D.` |
| Bangla source | `একটি বর্গের কতটি প্রতিসাম্য রেখা আছে? A. 8টি B. 6টি C. 4টি D. 2টি Answer with only A, B, C, or D.` |
| English source | `How many lines of symmetry does a square have? A. 8 B. 6 C. 4 D. 2 Answer with only A, B, C, or D.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

#### Example 2: `benqa_12th-Chemistry-II_0228`

- Split: `test`; tier: `tier_1_review_first`; impact score: `177`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `yes`; Qwen3 recoverable: `yes`
- Suggested edits: `ekoti->ekti (1); konoti->konti (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `Ni(s) + 2Ag^{+}(aq) \xrightarrow{2e^{-}} Ni^{2+}(aq) + 2Ag(s); bikriyatite- i. Ni jarit hoy ii. Ag jarit hoy iii. bikriyati ekoti ridoks bikriya nicher konoti sothik? A. i o ii B. ii o iii C. i o iii D. i, ii o iii Answer with only A, B, C, or D.` |
| Suggested Banglish | `Ni(s) + 2Ag^{+}(aq) \xrightarrow{2e^{-}} Ni^{2+}(aq) + 2Ag(s); bikriyatite- i. Ni jarit hoy ii. Ag jarit hoy iii. bikriyati ekti ridoks bikriya nicher konti sothik? A. i o ii B. ii o iii C. i o iii D. i, ii o iii Answer with only A, B, C, or D.` |
| Bangla source | `Ni(s) + 2Ag^{+}(aq) \xrightarrow{2e^{-}} Ni^{2+}(aq) + 2Ag(s); বিক্রিয়াটিতে- i. Ni জারিত হয় ii. Ag জারিত হয় iii. বিক্রিয়াটি একটি রিডক্স বিক্রিয়া নিচের কোনটি সঠিক? A. i ও ii B. ii ও iii C. i ও iii D. i, ii ও iii Answer with only A, B, C, or D.` |
| English source | `Ni(s) + 2Ag^{+}(aq) \overset{2e^{-}} {\rightarrow}Ni^{2+}(aq) + 2Ag(s); in this reaction- i. Ni becomes oxidized ii. Ag becomes oxidized iii. A redox reaction Which one is correct? A. i and ii B. ii and iii C. i and iii D. i, ii and iii Answer with only A, ...` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

#### Example 3: `benqa_8th-Math_0167`

- Split: `test`; tier: `tier_1_review_first`; impact score: `173`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `yes`; Qwen3 recoverable: `yes`
- Suggested edits: `ayotakar->ayotokar (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); prosth->prostho (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `ekoti ayotakar baganer doirghy prosther derogun. er prosth 16 mitar hole, baganer porisima kot? A. 40 mitar B. 64 mitar C. 80 mitar D. 96 mitar Answer with only A, B, C, or D.` |
| Suggested Banglish | `ekti ayotokar baganer doirgho prosther derogun. er prostho 16 mitar hole, baganer porisima koto? A. 40 mitar B. 64 mitar C. 80 mitar D. 96 mitar Answer with only A, B, C, or D.` |
| Bangla source | `একটি আয়তাকার বাগানের দৈর্ঘ্য প্রস্থের দেড়গুণ। এর প্রস্থ 16 মিটার হলে, বাগানের পরিসীমা কত? A. 40 মিটার B. 64 মিটার C. 80 মিটার D. 96 মিটার Answer with only A, B, C, or D.` |
| English source | `The length of a rectangular garden is one and half times its breadth. If breadth is 16 metres , what is its peremeter? A. 40m B. 64m C. 80m D. 96m Answer with only A, B, C, or D.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

### `kshetrofol` -> `khetrofol`

Rows: `13`; occurrences: `14`; tier-1 rows: `6`; test rows: `10`.

#### Example 1: `banglamath_0526`

- Split: `test`; tier: `tier_1_review_first`; impact score: `170`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `yes`; Qwen3 recoverable: `yes`
- Suggested edits: `ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); uchchota->ucchota (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `ekoti tribhujer bhumi 10 mitar o uchchota 6 mitar hole kshetrofol kot Return only the final answer.` |
| Suggested Banglish | `ekti tribhujer bhumi 10 mitar o ucchota 6 mitar hole khetrofol koto Return only the final answer.` |
| Bangla source | `একটি ত্রিভুজের ভূমি ১০ মিটার ও উচ্চতা ৬ মিটার হলে ক্ষেত্রফল কত Return only the final answer.` |
| English source | `If a triangle has a base of 10 meters and height of 6 meters, what is its area? Return only the final answer.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

#### Example 2: `banglamath_0552`

- Split: `test`; tier: `tier_1_review_first`; impact score: `148`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `yes`; Qwen3 recoverable: `no`
- Suggested edits: `ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); uchchota->ucchota (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `ekoti samantoriker bhumi 90 goj o uchchota 50 goj hole tar kshetrofol kot Return only the final answer.` |
| Suggested Banglish | `ekti samantoriker bhumi 90 goj o ucchota 50 goj hole tar khetrofol koto Return only the final answer.` |
| Bangla source | `একটি সামান্তরিকের ভূমি ৯০ গজ ও উচ্চতা ৫০ গজ হলে তার ক্ষেত্রফল কত Return only the final answer.` |
| English source | `If a parallelogram has a base of 90 yards and height of 50 yards, what is its area? Return only the final answer.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

#### Example 3: `banglamath_0538`

- Split: `test`; tier: `tier_1_review_first`; impact score: `144`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `no`; Qwen3 recoverable: `no`
- Suggested edits: `ayotakar->ayotokar (1); choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `ekoti ayotakar baganer doirghy 60 mitar o prosth 40 mitar. er bhitore 2 mitar choora rasta thakole rastar kshetrofol kot Return only the final answer.` |
| Suggested Banglish | `ekti ayotokar baganer doirgho 60 mitar o prostho 40 mitar. er bhitore 2 mitar chowra rasta thakle rastar khetrofol koto Return only the final answer.` |
| Bangla source | `একটি আয়তাকার বাগানের দৈর্ঘ্য ৬০ মিটার ও প্রস্থ ৪০ মিটার। এর ভিতরে ২ মিটার চওড়া রাস্তা থাকলে রাস্তার ক্ষেত্রফল কত Return only the final answer.` |
| English source | `A rectangular garden is 60m by 40m. If there’s a 2m wide path inside, what is the area of the path? Return only the final answer.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

### `doirghy` -> `doirgho`

Rows: `11`; occurrences: `13`; tier-1 rows: `5`; test rows: `8`.

#### Example 1: `benqa_8th-Math_0167`

- Split: `test`; tier: `tier_1_review_first`; impact score: `173`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `yes`; Qwen3 recoverable: `yes`
- Suggested edits: `ayotakar->ayotokar (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); prosth->prostho (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `ekoti ayotakar baganer doirghy prosther derogun. er prosth 16 mitar hole, baganer porisima kot? A. 40 mitar B. 64 mitar C. 80 mitar D. 96 mitar Answer with only A, B, C, or D.` |
| Suggested Banglish | `ekti ayotokar baganer doirgho prosther derogun. er prostho 16 mitar hole, baganer porisima koto? A. 40 mitar B. 64 mitar C. 80 mitar D. 96 mitar Answer with only A, B, C, or D.` |
| Bangla source | `একটি আয়তাকার বাগানের দৈর্ঘ্য প্রস্থের দেড়গুণ। এর প্রস্থ 16 মিটার হলে, বাগানের পরিসীমা কত? A. 40 মিটার B. 64 মিটার C. 80 মিটার D. 96 মিটার Answer with only A, B, C, or D.` |
| English source | `The length of a rectangular garden is one and half times its breadth. If breadth is 16 metres , what is its peremeter? A. 40m B. 64m C. 80m D. 96m Answer with only A, B, C, or D.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

#### Example 2: `banglamath_0538`

- Split: `test`; tier: `tier_1_review_first`; impact score: `144`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `no`; Qwen3 recoverable: `no`
- Suggested edits: `ayotakar->ayotokar (1); choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `ekoti ayotakar baganer doirghy 60 mitar o prosth 40 mitar. er bhitore 2 mitar choora rasta thakole rastar kshetrofol kot Return only the final answer.` |
| Suggested Banglish | `ekti ayotokar baganer doirgho 60 mitar o prostho 40 mitar. er bhitore 2 mitar chowra rasta thakle rastar khetrofol koto Return only the final answer.` |
| Bangla source | `একটি আয়তাকার বাগানের দৈর্ঘ্য ৬০ মিটার ও প্রস্থ ৪০ মিটার। এর ভিতরে ২ মিটার চওড়া রাস্তা থাকলে রাস্তার ক্ষেত্রফল কত Return only the final answer.` |
| English source | `A rectangular garden is 60m by 40m. If there’s a 2m wide path inside, what is the area of the path? Return only the final answer.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

#### Example 3: `banglamath_0541`

- Split: `test`; tier: `tier_1_review_first`; impact score: `144`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `no`; Qwen3 recoverable: `no`
- Suggested edits: `ayotakar->ayotokar (1); choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `ekoti ayotakar baganer doirghy 50 mi o prosth 30 mi. er bhitore 3 mitar choora rasta thakole rastar kshetrofol kot Return only the final answer.` |
| Suggested Banglish | `ekti ayotokar baganer doirgho 50 mi o prostho 30 mi. er bhitore 3 mitar chowra rasta thakle rastar khetrofol koto Return only the final answer.` |
| Bangla source | `একটি আয়তাকার বাগানের দৈর্ঘ্য ৫০ মি ও প্রস্থ ৩০ মি। এর ভিতরে ৩ মিটার চওড়া রাস্তা থাকলে রাস্তার ক্ষেত্রফল কত Return only the final answer.` |
| English source | `A rectangular garden is 50m by 30m. If there’s a 3m wide path inside, what is the area of the path? Return only the final answer.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

### `prosth` -> `prostho`

Rows: `9`; occurrences: `9`; tier-1 rows: `4`; test rows: `7`.

#### Example 1: `benqa_8th-Math_0167`

- Split: `test`; tier: `tier_1_review_first`; impact score: `173`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `yes`; Qwen3 recoverable: `yes`
- Suggested edits: `ayotakar->ayotokar (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); prosth->prostho (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `ekoti ayotakar baganer doirghy prosther derogun. er prosth 16 mitar hole, baganer porisima kot? A. 40 mitar B. 64 mitar C. 80 mitar D. 96 mitar Answer with only A, B, C, or D.` |
| Suggested Banglish | `ekti ayotokar baganer doirgho prosther derogun. er prostho 16 mitar hole, baganer porisima koto? A. 40 mitar B. 64 mitar C. 80 mitar D. 96 mitar Answer with only A, B, C, or D.` |
| Bangla source | `একটি আয়তাকার বাগানের দৈর্ঘ্য প্রস্থের দেড়গুণ। এর প্রস্থ 16 মিটার হলে, বাগানের পরিসীমা কত? A. 40 মিটার B. 64 মিটার C. 80 মিটার D. 96 মিটার Answer with only A, B, C, or D.` |
| English source | `The length of a rectangular garden is one and half times its breadth. If breadth is 16 metres , what is its peremeter? A. 40m B. 64m C. 80m D. 96m Answer with only A, B, C, or D.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

#### Example 2: `banglamath_0538`

- Split: `test`; tier: `tier_1_review_first`; impact score: `144`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `no`; Qwen3 recoverable: `no`
- Suggested edits: `ayotakar->ayotokar (1); choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `ekoti ayotakar baganer doirghy 60 mitar o prosth 40 mitar. er bhitore 2 mitar choora rasta thakole rastar kshetrofol kot Return only the final answer.` |
| Suggested Banglish | `ekti ayotokar baganer doirgho 60 mitar o prostho 40 mitar. er bhitore 2 mitar chowra rasta thakle rastar khetrofol koto Return only the final answer.` |
| Bangla source | `একটি আয়তাকার বাগানের দৈর্ঘ্য ৬০ মিটার ও প্রস্থ ৪০ মিটার। এর ভিতরে ২ মিটার চওড়া রাস্তা থাকলে রাস্তার ক্ষেত্রফল কত Return only the final answer.` |
| English source | `A rectangular garden is 60m by 40m. If there’s a 2m wide path inside, what is the area of the path? Return only the final answer.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

#### Example 3: `banglamath_0541`

- Split: `test`; tier: `tier_1_review_first`; impact score: `144`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `no`; Qwen3 recoverable: `no`
- Suggested edits: `ayotakar->ayotokar (1); choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `ekoti ayotakar baganer doirghy 50 mi o prosth 30 mi. er bhitore 3 mitar choora rasta thakole rastar kshetrofol kot Return only the final answer.` |
| Suggested Banglish | `ekti ayotokar baganer doirgho 50 mi o prostho 30 mi. er bhitore 3 mitar chowra rasta thakle rastar khetrofol koto Return only the final answer.` |
| Bangla source | `একটি আয়তাকার বাগানের দৈর্ঘ্য ৫০ মি ও প্রস্থ ৩০ মি। এর ভিতরে ৩ মিটার চওড়া রাস্তা থাকলে রাস্তার ক্ষেত্রফল কত Return only the final answer.` |
| English source | `A rectangular garden is 50m by 30m. If there’s a 3m wide path inside, what is the area of the path? Return only the final answer.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

### `ayotakar` -> `ayotokar`

Rows: `7`; occurrences: `7`; tier-1 rows: `3`; test rows: `5`.

#### Example 1: `benqa_8th-Math_0167`

- Split: `test`; tier: `tier_1_review_first`; impact score: `173`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `yes`; Qwen3 recoverable: `yes`
- Suggested edits: `ayotakar->ayotokar (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); prosth->prostho (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `ekoti ayotakar baganer doirghy prosther derogun. er prosth 16 mitar hole, baganer porisima kot? A. 40 mitar B. 64 mitar C. 80 mitar D. 96 mitar Answer with only A, B, C, or D.` |
| Suggested Banglish | `ekti ayotokar baganer doirgho prosther derogun. er prostho 16 mitar hole, baganer porisima koto? A. 40 mitar B. 64 mitar C. 80 mitar D. 96 mitar Answer with only A, B, C, or D.` |
| Bangla source | `একটি আয়তাকার বাগানের দৈর্ঘ্য প্রস্থের দেড়গুণ। এর প্রস্থ 16 মিটার হলে, বাগানের পরিসীমা কত? A. 40 মিটার B. 64 মিটার C. 80 মিটার D. 96 মিটার Answer with only A, B, C, or D.` |
| English source | `The length of a rectangular garden is one and half times its breadth. If breadth is 16 metres , what is its peremeter? A. 40m B. 64m C. 80m D. 96m Answer with only A, B, C, or D.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

#### Example 2: `banglamath_0538`

- Split: `test`; tier: `tier_1_review_first`; impact score: `144`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `no`; Qwen3 recoverable: `no`
- Suggested edits: `ayotakar->ayotokar (1); choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `ekoti ayotakar baganer doirghy 60 mitar o prosth 40 mitar. er bhitore 2 mitar choora rasta thakole rastar kshetrofol kot Return only the final answer.` |
| Suggested Banglish | `ekti ayotokar baganer doirgho 60 mitar o prostho 40 mitar. er bhitore 2 mitar chowra rasta thakle rastar khetrofol koto Return only the final answer.` |
| Bangla source | `একটি আয়তাকার বাগানের দৈর্ঘ্য ৬০ মিটার ও প্রস্থ ৪০ মিটার। এর ভিতরে ২ মিটার চওড়া রাস্তা থাকলে রাস্তার ক্ষেত্রফল কত Return only the final answer.` |
| English source | `A rectangular garden is 60m by 40m. If there’s a 2m wide path inside, what is the area of the path? Return only the final answer.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

#### Example 3: `banglamath_0541`

- Split: `test`; tier: `tier_1_review_first`; impact score: `144`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `no`; Qwen3 recoverable: `no`
- Suggested edits: `ayotakar->ayotokar (1); choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `ekoti ayotakar baganer doirghy 50 mi o prosth 30 mi. er bhitore 3 mitar choora rasta thakole rastar kshetrofol kot Return only the final answer.` |
| Suggested Banglish | `ekti ayotokar baganer doirgho 50 mi o prostho 30 mi. er bhitore 3 mitar chowra rasta thakle rastar khetrofol koto Return only the final answer.` |
| Bangla source | `একটি আয়তাকার বাগানের দৈর্ঘ্য ৫০ মি ও প্রস্থ ৩০ মি। এর ভিতরে ৩ মিটার চওড়া রাস্তা থাকলে রাস্তার ক্ষেত্রফল কত Return only the final answer.` |
| English source | `A rectangular garden is 50m by 30m. If there’s a 3m wide path inside, what is the area of the path? Return only the final answer.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

### `korote` -> `korte`

Rows: `7`; occurrences: `10`; tier-1 rows: `1`; test rows: `5`.

#### Example 1: `banglamath_1688`

- Split: `test`; tier: `tier_1_review_first`; impact score: `142`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `no`; Qwen3 recoverable: `no`
- Suggested edits: `ekoti->ekti (1); korote->korte (1); penyaj->peyaj (5)`

| Field | Text |
| --- | --- |
| Current Banglish | `kon ekoti biyer onushthane ranna korote baburchi o tar sohokormi mot 400ti penyaj katen. baburchi proti minite ontot 3ti penyaj ebong tar sohokormi proti minite ontot 2ti penyaj katote pare. jodi baburchi tar sohokormir cheye 25 minit age penyaj kata bondh,...` |
| Suggested Banglish | `kon ekti biyer onushthane ranna korte baburchi o tar sohokormi mot 400ti peyaj katen. baburchi proti minite ontot 3ti peyaj ebong tar sohokormi proti minite ontot 2ti peyaj katote pare. jodi baburchi tar sohokormir cheye 25 minit age peyaj kata bondh, tobe ...` |
| Bangla source | `কোন একটি বিয়ের অনুষ্ঠানে রান্না করতে বাবুর্চি ও তার সহকর্মী মোট ৪০০টি পেঁয়াজ কাটেন। বাবুর্চি প্রতি মিনিটে অন্তত ৩টি পেঁয়াজ এবং তার সহকর্মী প্রতি মিনিটে অন্তত ২টি পেঁয়াজ কাটতে পারে। যদি বাবুর্চি তার সহকর্মীর চেয়ে ২৫ মিনিট আগে পেঁয়াজ কাটা বন্ধ, তবে কে ক...` |
| English source | `At a wedding, a chef and assistant cut 400 onions together. The chef cuts at least 3 onions per minute and the assistant cuts at least 2 per minute. If the chef stops 25 minutes before the assistant, how many onions did each cut and how long did they work? ...` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

#### Example 2: `benqa_10th-Physics_0106`

- Split: `test`; tier: `tier_2_high`; impact score: `133`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `no`; Qwen3 recoverable: `no`
- Suggested edits: `korote->korte (1); kot->koto (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `bina badhay poront bostu 5 sekende 50 mitar poth otikrom korole 72 mitar poth otikrom korote kot sekend somoy lagobe? A. 6 B. 7.2 C. 9.5 D. 12 Answer with only A, B, C, or D.` |
| Suggested Banglish | `bina badhay poront bostu 5 sekende 50 mitar poth otikrom korole 72 mitar poth otikrom korte koto sekend somoy lagobe? A. 6 B. 7.2 C. 9.5 D. 12 Answer with only A, B, C, or D.` |
| Bangla source | `বিনা বাধায় পড়ন্ত বস্তু 5 সেকেন্ডে 50 মিটার পথ অতিক্রম করলে 72 মিটার পথ অতিক্রম করতে কত সেকেন্ড সময় লাগবে? A. 6 B. 7.2 C. 9.5 D. 12 Answer with only A, B, C, or D.` |
| English source | `If a freely falling body travels 50 m in 5 sec then how much time in second will need to travel thr distance of 72 meter? A. 6 B. 7.2 C. 9.5 D. 12 Answer with only A, B, C, or D.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

#### Example 3: `banglamath_1691`

- Split: `test`; tier: `tier_2_high`; impact score: `132`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `no`; Qwen3 recoverable: `no`
- Suggested edits: `achhe->ache (1); ekoti->ekti (2); korote->korte (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `beru goyalar kachhe ekoti kolosite 10 litar dudh ebong dudh mapar duti khali patr , ekoti 5 litarer, oporoti 3 litarer. se kretake 1 litar dudh bikri korote chay. goyalar kachhe jedojesob patr achhe shudhu ta diye kibhabe kretake 1 litar dudh deya sombhob? ...` |
| Suggested Banglish | `beru goyalar kachhe ekti kolosite 10 litar dudh ebong dudh mapar duti khali patr , ekti 5 litarer, oporoti 3 litarer. se kretake 1 litar dudh bikri korte chay. goyalar kachhe jedojesob patr ache shudhu ta diye kibhabe kretake 1 litar dudh deya sombhob? Retu...` |
| Bangla source | `বেরু গোয়ালার কাছে একটি কলসিতে ১০ লিটার দুধ এবং দুধ মাপার দুটি খালি পাত্র , একটি ৫ লিটারের, অপরটি ৩ লিটারের। সে ক্রেতাকে ১ লিটার দুধ বিক্রি করতে চায়। গোয়ালার কাছে জেডযেসব পাত্র আছে শুধু তা দিয়ে কিভাবে ক্রেতাকে ১ লিটার দুধ দেয়া সম্ভব? Return only the fin...` |
| English source | `Beru the milkman has 10 liters of milk in a jar, and two empty containers: one of 5 liters and one of 3 liters. How can he measure exactly 1 liter using only these two containers? Return only the final answer.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

### `achhe` -> `ache`

Rows: `6`; occurrences: `6`; tier-1 rows: `3`; test rows: `5`.

#### Example 1: `benqa_10th-Math_0044`

- Split: `test`; tier: `tier_1_review_first`; impact score: `177`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `yes`; Qwen3 recoverable: `yes`
- Suggested edits: `achhe->ache (1); ekoti->ekti (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `ekoti borger kototi protisamy rekha achhe? A. 8ti B. 6ti C. 4ti D. 2ti Answer with only A, B, C, or D.` |
| Suggested Banglish | `ekti borger kototi protisamy rekha ache? A. 8ti B. 6ti C. 4ti D. 2ti Answer with only A, B, C, or D.` |
| Bangla source | `একটি বর্গের কতটি প্রতিসাম্য রেখা আছে? A. 8টি B. 6টি C. 4টি D. 2টি Answer with only A, B, C, or D.` |
| English source | `How many lines of symmetry does a square have? A. 8 B. 6 C. 4 D. 2 Answer with only A, B, C, or D.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

#### Example 2: `benqa_8th-Science_0127`

- Split: `test`; tier: `tier_1_review_first`; impact score: `148`; priority: `both_wrong_single_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `no`; Qwen3 recoverable: `yes`
- Suggested edits: `achhe->ache (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `kon groher sobocheye beshi upogroh achhe? A. shoni B. brihospoti C. iurenas D. nepochun Answer with only A, B, C, or D.` |
| Suggested Banglish | `kon groher sobocheye beshi upogroh ache? A. shoni B. brihospoti C. iurenas D. nepochun Answer with only A, B, C, or D.` |
| Bangla source | `কোন গ্রহের সবচেয়ে বেশি উপগ্রহ আছে? A. শনি B. বৃহস্পতি C. ইউরেনাস D. নেপচুন Answer with only A, B, C, or D.` |
| English source | `Which planet has maximum satellites? A. Saturn B. Jupiter C. Uranus D. Neptune Answer with only A, B, C, or D.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

#### Example 3: `benqa_12th-Biology-I_0265`

- Split: `dev`; tier: `tier_1_review_first`; impact score: `165`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `yes`; Qwen3 recoverable: `yes`
- Suggested edits: `achhe->ache (1); ekoti->ekti (1); konoti->konti (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `mi. 'k' byoboharik klase ekoti nomunar poryobekshon kore dekholo metajailem kendrer dike, bhaskular bandol 9ti ebong kichhu ekokoshi rom achhe. poryobekshit boishishtyogulo kibhabe udbhidoke banchiye rakhote sahajy kore? i. pani o khonij lobon poribohon kor...` |
| Suggested Banglish | `mi. 'k' byoboharik klase ekti nomunar poryobekshon kore dekholo metajailem kendrer dike, bhaskular bandol 9ti ebong kichhu ekokoshi rom ache. poryobekshit boishishtyogulo kibhabe udbhidoke banchiye rakhote sahajy kore? i. pani o khonij lobon poribohon kore ...` |
| Bangla source | `মি. 'ক' ব্যবহারিক ক্লাসে একটি নমুনার পর্যবেক্ষণ করে দেখলো মেটাজাইলেম কেন্দ্রের দিকে, ভাস্কুলার বান্ডল ৯টি এবং কিছু এককোষী রোম আছে। পর্যবেক্ষিত বৈশিষ্ট্যগুলো কীভাবে উদ্ভিদকে বাঁচিয়ে রাখতে সাহায্য করে? i. পানি ও খনিজ লবণ পরিবহন করে ii. প্রস্তুতকৃত খাবার পরিবহ...` |
| English source | `Mr. 'X' observed a transverse section of a sample and noticed that metaxylem is present towards the center, 9 (nine) vascular bundles and there are some unicellular hairs. How does the observe features help to protect the plant? i. By transporting water and...` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

### `thakole` -> `thakle`

Rows: `5`; occurrences: `5`; tier-1 rows: `3`; test rows: `4`.

#### Example 1: `banglamath_0538`

- Split: `test`; tier: `tier_1_review_first`; impact score: `144`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `no`; Qwen3 recoverable: `no`
- Suggested edits: `ayotakar->ayotokar (1); choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `ekoti ayotakar baganer doirghy 60 mitar o prosth 40 mitar. er bhitore 2 mitar choora rasta thakole rastar kshetrofol kot Return only the final answer.` |
| Suggested Banglish | `ekti ayotokar baganer doirgho 60 mitar o prostho 40 mitar. er bhitore 2 mitar chowra rasta thakle rastar khetrofol koto Return only the final answer.` |
| Bangla source | `একটি আয়তাকার বাগানের দৈর্ঘ্য ৬০ মিটার ও প্রস্থ ৪০ মিটার। এর ভিতরে ২ মিটার চওড়া রাস্তা থাকলে রাস্তার ক্ষেত্রফল কত Return only the final answer.` |
| English source | `A rectangular garden is 60m by 40m. If there’s a 2m wide path inside, what is the area of the path? Return only the final answer.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

#### Example 2: `banglamath_0541`

- Split: `test`; tier: `tier_1_review_first`; impact score: `144`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `no`; Qwen3 recoverable: `no`
- Suggested edits: `ayotakar->ayotokar (1); choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `ekoti ayotakar baganer doirghy 50 mi o prosth 30 mi. er bhitore 3 mitar choora rasta thakole rastar kshetrofol kot Return only the final answer.` |
| Suggested Banglish | `ekti ayotokar baganer doirgho 50 mi o prostho 30 mi. er bhitore 3 mitar chowra rasta thakle rastar khetrofol koto Return only the final answer.` |
| Bangla source | `একটি আয়তাকার বাগানের দৈর্ঘ্য ৫০ মি ও প্রস্থ ৩০ মি। এর ভিতরে ৩ মিটার চওড়া রাস্তা থাকলে রাস্তার ক্ষেত্রফল কত Return only the final answer.` |
| English source | `A rectangular garden is 50m by 30m. If there’s a 3m wide path inside, what is the area of the path? Return only the final answer.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

#### Example 3: `banglamath_0549`

- Split: `test`; tier: `tier_1_review_first`; impact score: `142`; priority: `both_wrong_multi_edit`
- Qwen2.5 wrong: `yes`; Qwen3 wrong: `yes`; Qwen2.5 recoverable: `no`; Qwen3 recoverable: `no`
- Suggested edits: `choora->chowra (1); doirghy->doirgho (1); ekoti->ekti (1); kot->koto (1); kshetrofol->khetrofol (1); prosth->prostho (1); thakole->thakle (1)`

| Field | Text |
| --- | --- |
| Current Banglish | `ekoti baganer baire 2.5 mitar choora rasta thakole rastar kshetrofol kot jodi baganer doirghy 50 mi o prosth 35 mi hoy Return only the final answer.` |
| Suggested Banglish | `ekti baganer baire 2.5 mitar chowra rasta thakle rastar khetrofol koto jodi baganer doirgho 50 mi o prostho 35 mi hoy Return only the final answer.` |
| Bangla source | `একটি বাগানের বাইরে ২.৫ মিটার চওড়া রাস্তা থাকলে রাস্তার ক্ষেত্রফল কত যদি বাগানের দৈর্ঘ্য ৫০ মি ও প্রস্থ ৩৫ মি হয় Return only the final answer.` |
| English source | `If a 2.5m wide path surrounds a garden of 50m by 35m, what is the area of the path? Return only the final answer.` |

Review decision:

- Accept only if the suggested wording preserves the Bangla/English meaning.
- Edit manually if the repeated substitution is correct but another word is still awkward.
- Mark `bad` only for source/translation ambiguity, not for ordinary spelling cleanup.

## Completion Check

After a review session:

1. Save the edited CSV.
2. Run `python3 scripts/validate_banglish_review_queue.py --require-complete`
   only when all rows are filled.
3. Run `python3 scripts/validate_banglish_review_queue.py` during partial
   sessions to catch formatting errors without failing on pending rows.
4. Record accepted/rejected/bad counts in
   `reports/validation200_v5_review_session_log.md`.
5. Record final accepted/rejected/bad counts in the research log before
   freezing v5.
