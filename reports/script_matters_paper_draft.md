# Script Matters: Measuring Latin-Script Banglish Robustness in Bangla LLMs

Updated: 2026-06-05

Draft status: full paper manuscript draft. This version is intentionally
long-form. It is written to make the argument clear before later compression for
a venue format.

## Abstract

Bangla users do not always meet language models through the script assumed by
standard benchmarks. The same Bengali question may be typed in native Bengali
script, in English, or in Latin-script Banglish. Existing Bengali benchmarks
increasingly cover question answering, mathematical reasoning, knowledge,
safety, culture, and social interaction, but they rarely isolate this script
choice while holding the underlying item and answer fixed. We study whether
orthography itself changes large language model behavior. We construct a paired
evaluation in which each item is asked in native Bengali script, reviewed
Latin-script Banglish, and English, while preserving the item id and gold
answer. The main gold-core evaluation contains 200 curriculum-style QA and math
items from BEnQA and BanglaMATH, with 144 BEnQA questions and 56 BanglaMATH
questions. A v5 review pass freezes the Banglish variant after targeted human
review of the highest-impact rows.

Across three compact Qwen instruction models, reviewed Banglish is consistently
harder than native-script Bangla and English. Qwen2.5-3B scores 54/200 in
Bangla and 41/200 in reviewed Banglish; Qwen2.5-7B 8-bit scores 65/200 and
47/200; Qwen3-4B scores 80/200 and 49/200. The paired Banglish-minus-Bangla
intervals are negative for Qwen2.5-7B and Qwen3-4B, while Qwen2.5-3B remains
negative in point estimate and in stricter sensitivity checks. The gap is not a
simple token-length effect: for the audited Qwen tokenizers, reviewed Banglish
is token-cheaper than native Bangla, and recoverable Banglish misses are not the
longest Banglish prompts. Nor is the gap removed by cleanup: the v5 human review
changes Banglish scores by at most two items per main model.

We then test the boundary of the result. A five-model hosted API panel on the
same 200-item protocol shows that stronger models reduce the effect unevenly.
GPT-5.5 low nearly closes the gap under secondary scoring; Gemini 3.5 Flash
reduces it; Claude Sonnet 4.6 remains strong but gap-positive; DeepSeek V4 Flash
and Groq-hosted Llama 3.3 70B retain large reviewed-Banglish deficits. To answer
the dataset-size objection, we build a human-reviewed BEnQA extension: 974
accepted/edited rows from a 1,000-row review. Six completed rows on this larger
gold/pass layer all keep reviewed Banglish below Bangla, including GPT-5.5 none
at 820/974 Bangla, 699/974 reviewed Banglish, and 825/974 English.

Finally, we test mitigation paths. Same-model self-normalization helps
Qwen2.5-3B but hurts Qwen3-4B. Generated Bengali and generated English views
require strict preservation checks and do not yet justify a held-out routing
claim. A natural BnSentMix code-mixed sentiment layer shows that real
Bengali-English mixed text remains difficult, but it is unpaired and therefore
does not replace the controlled script-gap estimate. The central lesson is
practical: Banglish should not be treated as harmless informal spelling noise.
It is a real access path for Bangla users, and its reliability must be measured
directly.

## 1. Introduction

Bangla is normally written in Bengali script. In everyday digital use, however,
many speakers also write Bengali-language content with Latin characters. This
Latin-script form is often called Banglish. It appears in messaging, search
queries, comments, reviews, and informal learning contexts, often because Latin
keyboards are convenient or because the surrounding conversation is already
code-mixed. For a Bangla-facing language model, this means the same user intent
can arrive through more than one written form.

That small interface detail can matter. A student may ask the same science
question in Bangla script, in English, or in Banglish. A model may answer one
version and fail another, even though the gold answer has not changed. If we
only evaluate native-script Bangla and English, this access gap can remain
hidden.

This paper asks a simple question:

**If the task and gold answer are held fixed, does changing the script to
Latin-script Banglish change model reliability?**

This is not the same as asking whether Bangla is hard for LLMs. Existing Bengali
benchmarks already show that Bangla evaluation is important. BEnQA evaluates
Bengali and English science questions from Bangladeshi educational material
[@shafayat-etal-2024-benqa]. BanglaMATH evaluates Bengali math word problems
[@banglamath2025]. Other work expands Bengali evaluation across reading
comprehension, multitask knowledge, cultural understanding, inference, safety,
and social interaction [@banglaquad2024; @bnmmlu2025; @bluck2025;
@nctbqa2026; @bnli2025; @banglasocialbench2026]. These benchmarks establish
that Bengali LLM evaluation is active and necessary.

The missing piece is narrower. Most benchmarks do not ask whether the same
Bangla content remains answerable when written in Banglish. This matters because
Banglish is not an academic curiosity. BanglaTLit documents romanized Bangla as
a large back-transliteration problem with substantial spelling variation
[@fahim-etal-2024-banglatlit]. BanglishRev, BAN-TH, BnSentMix, MixSarc, and
other datasets show that Bangla-English, code-mixed, and transliterated Bangla
appear in reviews, social media, sentiment, hate-speech, humor, and sarcasm
settings [@banglishrev2024; @banth2024; @bnsentmix2024; @mixsarc2026].
Romanized Indic language identification is itself treated as an infrastructure
problem [@bhashaabhijnaanam2023]. If models fail on Banglish, then a large class
of users can receive lower-quality answers even when their request is
semantically equivalent to a request the model can answer in another script.

We therefore frame Banglish as an **orthographic access problem**. The central
claim is not that Banglish is always harder for every model or every item. The
claim is that script choice is a measurable robustness variable: it can change
accuracy, strict answer compliance, recoverability, and cost under controlled
conditions.

The study is built around three design principles.

First, evaluation must be paired. We preserve the same item id and gold answer
across Bangla, reviewed Banglish, and English variants. Aggregate accuracy alone
is not enough; we need to know whether the same item becomes wrong under one
script and correct under another.

Second, the Banglish variant must be audited. A rule-based romanizer is useful
for controlled construction, but it can introduce unnatural or ambiguous forms.
We therefore freeze a reviewed-v5 validation slice after targeted human review
of high-impact Banglish rows. We also keep a strict policy for flagged source
quality issues and report a stricter 197-row sensitivity view.

Third, stronger models should be treated as boundary tests, not as shortcuts.
GPT-5.5 compresses the mixed-task validation gap, but the 974-row BEnQA
human-gold scale panel shows that this boundary does not erase the BEnQA scale
deficit. Conversely, Claude, DeepSeek, Groq-hosted Llama, Gemini, and local
Qwen all remain gap-positive on the scale layer, so model/provider prestige
alone is not a reliable guarantee of Banglish robustness.

In the following chapters, we first describe the paired benchmark construction
and scoring protocol. We then present the main validation-200 result, test
whether it survives review and tokenization controls, examine recoverable
failures, and finally study frontier models, scale extension, natural
code-mixed text, and mitigation attempts.

## 2. Contributions

This paper makes five contributions.

1. **A paired Bangla/Banglish/English evaluation protocol.** We evaluate the
   same curriculum-style QA and math items in three script views while
   preserving the item id, answer type, and gold answer.

2. **A reviewed gold-core validation set.** The main validation-200 v5 slice
   contains 144 BEnQA and 56 BanglaMATH items. Its reviewed Banglish field is
   frozen after a targeted review pass, and all main claims use the same
   all-200 denominator.

3. **Evidence that Banglish failure is not just cleanup or token length.** Human
   review changes scores only slightly. Tokenization audits show that reviewed
   Banglish is shorter than native Bangla for the audited Qwen tokenizers, and
   recoverable Banglish misses are not the longest Banglish prompts.

4. **A frontier and scale boundary.** A five-model API panel shows that GPT-5.5
   nearly closes the mixed-task validation gap, but a 974-row human-reviewed
   BEnQA scale panel shows the reviewed-Banglish deficit persists across
   Qwen2.5-3B, Groq, Gemini, GPT-5.5 none, Claude, and DeepSeek.

5. **Negative mitigation evidence.** Self-normalization, generated Bengali
   views, and generated English views do not produce a general deployable
   solution. Preservation gates are necessary, and current cheap generated views
   are too unstable for a held-out routing claim.

## 3. Related Work

### 3.1 Bengali evaluation

BEnQA introduced a Bengali-English question answering benchmark based on
science questions from Bangladeshi education [@shafayat-etal-2024-benqa].
BanglaMATH introduced a Bengali math word-problem benchmark and showed language
bias in mathematical reasoning [@banglamath2025]. MGSM provides multilingual
GSM8K-style arithmetic items and supports broader multilingual reasoning
evaluation [@mgsm2022; @gsm8k2021].

Recent Bengali benchmarks cover many other directions: open-domain QA
[@banglaquad2024], multitask knowledge [@bnmmlu2025], linguistic and cultural
knowledge [@bluck2025], textbook QA [@nctbqa2026], inference [@bnli2025],
social and cultural alignment [@banglasocialbench2026], multimodal cultural
understanding [@banglaverse2026], long-form speech [@bengaliloop2026], safety
[@banglaguard2026], and biomedical QA [@banglamedqa2025]. This growing
landscape is important for positioning our work. We do not claim that Bengali
is unevaluated. The gap is more specific: controlled downstream
Bangla/Banglish/English script-equivalence evaluation remains undermeasured.

### 3.2 Romanized Bangla and code-mixed text

BanglaTLit shows that romanized Bangla is widespread and spelling-variable,
requiring dedicated back-transliteration resources [@fahim-etal-2024-banglatlit].
BanglishRev documents Bangla-English and code-mixed product reviews
[@banglishrev2024]. BAN-TH focuses on transliterated Bangla hate speech
[@banth2024], BnSentMix on Bengali-English code-mixed sentiment
[@bnsentmix2024], and MixSarc on implicit meaning in Bangla-English code-mixed
text [@mixsarc2026]. These resources show that Banglish and related code-mixed
forms are practical user-facing formats.

Most of these datasets are classification corpora. They are useful prevalence
evidence, but they do not directly measure whether a QA or math item with the
same answer becomes harder when the script changes. That paired downstream
question is the core of Script Matters.

### 3.3 Script robustness and transliteration

Prior work on Bangla transliteration perturbations shows that replacing Bangla
words or sentences with transliterated forms can expose model vulnerabilities
[@haider-etal-2025-robustness]. Related transliteration resources also motivate
normalization as a possible bridge for Romanized Bengali inputs
[@indotranslit2025]. Recent work on
romanized scripts in Indian-language triage and Romanized Nepali LLM evaluation
supports the broader claim that romanized South Asian language inputs deserve
direct evaluation [@scriptgap2025; @romanizednepali2026].

Our work differs in three ways. We use full task-equivalent variants rather than
local perturbations. We preserve the item and gold answer across Bangla,
Banglish, and English. And we analyze failure recoverability, tokenization,
review sensitivity, frontier-model behavior, and mitigation attempts under one
protocol.

### 3.4 Tokenization and latent language

Tokenizer design can create unequal costs and context budgets across languages
[@tokenizerfairness2023]. At the same time, multilingual LLMs can show latent
English or romanized-language behavior [@wendler-etal-2024-llamas;
@thinkenglish2025; @romanlens2025]. These findings motivate our tokenization
and cross-script oracle analyses. However, they do not imply that explicit
Banglish input will be robust. Our results show the opposite for many models:
Banglish can be token-cheaper than native Bangla and still less accurate.

## 4. Benchmark Construction

### 4.1 Source tasks

The benchmark construction has one goal: make script the main variable, not the
question. To do this, the validation set combines two source tasks whose items
can be represented in multiple script views while preserving the answer.

**BEnQA.** BEnQA contributes multiple-choice science questions. These items are
well suited to paired script evaluation because the answer is a choice label and
the same item can be represented in Bangla, Banglish, and English.

**BanglaMATH.** BanglaMATH contributes short-answer math word problems. These
items stress numerical reasoning and answer normalization. They are harder to
score strictly because correct answers may appear with units, Bengali digits, or
intermediate reasoning.

The frozen validation-200 v5 slice contains 144 BEnQA items and 56 BanglaMATH
items. The BEnQA subset is the cleanest source of script-gap evidence because
choice-label scoring is less sensitive to answer formatting. BanglaMATH is kept
as a stress-test slice because it exposes answer-compliance and numeric-unit
issues that are important for deployment.

### 4.2 Script variants

Each item is represented in three main variants:

- **Bangla:** native Bengali script.
- **Reviewed Banglish:** Latin-script Banglish after the v5 review pass.
- **English:** English translation or English source variant.

All variants preserve the item id and gold answer. The prompt asks the model to
return only the answer. For BEnQA, the expected output is one of A, B, C, or D.
For BanglaMATH, the parser accepts short numeric or textual answers under strict
and secondary modes. In other words, a script gap means the same item changes
correctness when written differently; it does not mean that different questions
were compared.

The English variant is useful but not identical in status to the Bangla-Banglish
pair. English is a privileged comparison view. It helps identify whether an item
is semantically answerable for a model, but the main orthographic claim is the
Bangla-vs-reviewed-Banglish contrast.

### 4.3 Review and denominator policy

The v5 review pass targeted Banglish rows most likely to affect the thesis
claim. After review, validation-200 v5 is frozen under an all-200 denominator
policy. Three source-quality rows are also tracked under a strict-197
sensitivity view. The all-200 denominator remains primary because it avoids
changing the evaluation set after seeing outcomes. The strict-197 view is a
robustness check, not a replacement for the main result.

Review changed the main Banglish scores only slightly:

| Model | v4 Banglish | reviewed-v5 Banglish | Change |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 39/200 | 41/200 | +1.0 pts |
| Qwen2.5-7B 8-bit | 48/200 | 47/200 | -0.5 pts |
| Qwen3-4B | 47/200 | 49/200 | +1.0 pts |

This is important. The review improves dataset quality but does not erase the
script-conditioned weakness.

## 5. Evaluation Protocol

### 5.1 Models

The main open-model evaluation uses three compact Qwen instruction models:

- Qwen2.5-3B-Instruct
- Qwen2.5-7B-Instruct in 8-bit
- Qwen3-4B-Instruct

These models are small enough to run reproducibly on the available compute but
strong enough to avoid a trivial "all models fail everything" result. They are
therefore useful as thesis-facing baselines: failures are interpretable, but the
experiments remain repeatable.

The frontier/API panel adds five hosted models:

- Gemini 3.5 Flash
- GPT-5.5 low
- Claude Sonnet 4.6
- DeepSeek V4 Flash, non-thinking mode
- Groq-hosted Llama 3.3 70B

The API rows use the same frozen validation-200 v5 prompt manifest and the same
parser. They are not treated as a leaderboard. Their role is to test whether the
Banglish gap disappears under stronger or differently trained systems.

### 5.2 Scoring

We report strict accuracy for all rows. Strict scoring measures whether the
model produced the expected answer in a deployable form. For API rows we also
report secondary parser/unit sensitivity. Secondary scoring gives credit for
recoverable noncanonical answers, such as numeric-only answers with units or
choice answers embedded in light markdown.

This separation is deliberate. Strict accuracy answers one deployment question:
can the model follow the benchmark contract? Secondary accuracy answers a
diagnostic question: did the model appear to know the semantic answer even if it
violated the exact format?

### 5.3 Paired gaps

For each model and item, we compare correctness across script variants. The main
gap is:

`reviewed Banglish accuracy - Bangla accuracy`

We also report:

`reviewed Banglish accuracy - English accuracy`

For the core Qwen rows and full851 extension, we use paired bootstrap intervals.
For the API validation panel, we also report exact paired sign-test style
discordance summaries where available. Positive values mean Banglish is more
accurate than the comparator. Negative values mean Banglish is less accurate.

## 6. Main Result: Reviewed Banglish Remains Harder

Table 1 gives the main frozen validation-200 v5 result.

**Table 1. Main validation-200 v5 results.**

| Model | Bangla | Reviewed Banglish | English | Banglish - Bangla | Banglish - English |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 54/200 | 41/200 | 71/200 | -6.5 pts, CI [-13.0, 0.0] | -15.0 pts, CI [-22.0, -7.5] |
| Qwen2.5-7B 8-bit | 65/200 | 47/200 | 94/200 | -9.0 pts, CI [-16.0, -2.0] | -23.5 pts, CI [-31.0, -16.0] |
| Qwen3-4B | 80/200 | 49/200 | 88/200 | -15.5 pts, CI [-22.0, -9.0] | -19.5 pts, CI [-27.0, -12.0] |

The result is consistent across the three thesis-facing Qwen models. Reviewed
Banglish is lower than native-script Bangla and English for every model.
Qwen2.5-7B and Qwen3-4B have fully negative Banglish-minus-Bangla confidence
intervals. Qwen2.5-3B has a negative point estimate but the all-200 interval
touches zero. This is why the claim must be stated carefully: the strongest
all-200 evidence comes from Qwen2.5-7B and Qwen3-4B, while Qwen2.5-3B remains
supportive through point estimate, historical v3 results, and strict-197
sensitivity.

The English comparison is larger. For all three Qwen rows, reviewed Banglish is
15 to 23.5 points below English. This supports the idea that many failures are
not simply item difficulty. The same item can become answerable when shown in a
different script or language view.

## 7. Is the Gap Just Bad Banglish?

A natural first objection is that the Latin-script Banglish field might simply
be bad Banglish. The v5 review was designed to test that possibility. It
targeted rows where review could matter most, then froze the final
validation-200 slice. The result is clear: review changes scores only slightly
and does not remove the gap.

This matters for interpretation. If Banglish cleanup had raised scores to match
Bangla, the result would mostly be about romanizer artifacts. Instead, cleanup
improves quality while preserving the central pattern. The study therefore does
not need to claim that every romanization is perfect. It only needs to show that
the observed gap is not removed by targeted review.

We also keep denominator sensitivity explicit. Under the strict-197 policy that
excludes three flagged source-quality rows, the reviewed Banglish-minus-Bangla
intervals remain negative for all three thesis-facing Qwen rows:

| Model | Strict policy | Reviewed Banglish - Bangla |
| --- | --- | ---: |
| Qwen2.5-3B | 197 rows | -7.1 pts, CI [-13.2, -1.0] |
| Qwen2.5-7B 8-bit | 197 rows | -9.6 pts, CI [-16.8, -2.5] |
| Qwen3-4B | 197 rows | -15.7 pts, CI [-22.3, -9.6] |

The strict-197 view is not the primary denominator. It is a check that the main
result does not depend on a few questionable rows.

## 8. Is the Gap Just Token Length?

Another plausible explanation is tokenization. If Banglish were much longer
than Bangla, lower accuracy could be a context-budget or tokenization-efficiency
problem. The data do not support that simple explanation.

For the audited Qwen tokenizers, reviewed Banglish is token-cheaper than native
Bangla.

**Table 2. Mean tokens per word under the audited Qwen tokenizers.**

| Dataset | Bangla | Reviewed Banglish | English |
| --- | ---: | ---: | ---: |
| BEnQA | 4.0242 | 2.4942 | 1.9545 |
| BanglaMATH | 4.6285 | 2.1114 | 1.4080 |

The failure-pattern join also shows that recoverable Banglish misses are not
the longest Banglish prompts. In BEnQA, recoverable reviewed-Banglish misses are
shorter on average than other rows for all three thesis-facing Qwen models.

This does not prove tokenization is irrelevant. Tokenization can affect
representation quality in ways not captured by length. But it rules out the
simple explanation that Banglish fails because it uses more tokens. The failure
is more consistent with script-conditioned lexical grounding, training
distribution, spelling variation, and task interpretation.

## 9. What Kind of Failures Are These?

The paired design lets us separate hard items from script-specific failures.
This is the main advantage of keeping item ids fixed. Across the three Qwen
models and 200 validation items, reviewed Banglish is wrong in 463 of 600
model-item slots. Of these Banglish misses, 185 are recoverable: either Bangla
or English is correct on the same item. The remaining 278 are all-script hard.

**Table 3. Recoverability source decomposition over 600 Qwen model-item slots.**

| Category | Count |
| --- | ---: |
| Reviewed Banglish wrong | 463/600 |
| Recoverable by Bangla or English | 185/600 |
| All-script hard | 278/600 |
| Bangla-only recovery | 28/600 |
| English-only recovery | 81/600 |
| Both alternate scripts recover | 76/600 |
| Banglish-only success | 20/600 |

This decomposition gives two important messages.

First, a large share of Banglish errors are not impossible items. In BEnQA,
55.2% of Banglish misses are recoverable by Bangla or English. These are the
clearest qualitative examples for the paper: the same answer becomes reachable
when the script view changes.

Second, the result is not absolute. Banglish-only success exists. There are
20/600 model-item slots where reviewed Banglish is correct and both alternate
views are wrong. We therefore avoid saying "Banglish is always worse." The
claim is aggregate and paired: reviewed Banglish is systematically less reliable
for the models and tasks studied.

**Table 4. Example recoverable reviewed-Banglish misses from the BEnQA
extension.** `BN`, `BG`, and `EN` denote parsed answers under Bangla, reviewed
Banglish, and English prompts.

| Model | ID | Gold | Correct script views | Parsed answers | Banglish prompt fragment |
| --- | --- | ---: | --- | --- | --- |
| Qwen2.5-3B | `...0100` | C | Bangla, English | BN=C; BG=D; EN=C | `akotin o mayosin...` |
| Qwen2.5-3B | `...0120` | D | Bangla, English | BN=D; BG=B; EN=D | `byakoteriyate...` |
| DeepSeek V4 Flash | `...0001` | C | Bangla, English | BN=C; BG=B; EN=C | `salokosongshleshoner...` |
| DeepSeek V4 Flash | `...0023` | A | Bangla | BN=A; BG=D; EN=D | `kshariy mutr...` |

These examples should not be read as a separate test. They are explanatory
evidence. They show the mechanism of the paired result: the same item and answer
can become unreliable when the input is written in reviewed Banglish.

## 10. Frontier API Boundary

The frontier/API panel tests whether the gap disappears for stronger or hosted
models. The answer is not a simple yes or no. Stronger models can reduce the
gap, but the reduction is uneven and model-dependent.

**Table 5. Validation-200 v5 frontier/API panel.**

| Model | Score | Bangla | Reviewed Banglish | English | BG-BN | BG-EN |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Gemini 3.5 Flash | Strict | 163/200 | 136/200 | 144/200 | -13.5 pts | -4.0 pts |
| Gemini 3.5 Flash | Secondary | 170/200 | 161/200 | 165/200 | -4.5 pts | -2.0 pts |
| GPT-5.5 low | Strict | 172/200 | 169/200 | 154/200 | -1.5 pts | +7.5 pts |
| GPT-5.5 low | Secondary | 173/200 | 174/200 | 168/200 | +0.5 pts | +3.0 pts |
| Claude Sonnet 4.6 | Strict | 162/200 | 130/200 | 153/200 | -16.0 pts | -11.5 pts |
| Claude Sonnet 4.6 | Secondary | 167/200 | 133/200 | 166/200 | -17.0 pts | -16.5 pts |
| DeepSeek V4 Flash | Strict | 143/200 | 82/200 | 132/200 | -30.5 pts | -25.0 pts |
| DeepSeek V4 Flash | Secondary | 152/200 | 96/200 | 148/200 | -28.0 pts | -26.0 pts |
| Groq Llama 3.3 70B | Strict | 90/200 | 48/200 | 102/200 | -21.0 pts | -27.0 pts |
| Groq Llama 3.3 70B | Secondary | 92/200 | 56/200 | 111/200 | -18.0 pts | -27.5 pts |

GPT-5.5 low is the strongest boundary case. Under strict scoring it nearly
closes the Banglish-vs-Bangla gap: 172/200 Bangla versus 169/200 Banglish. Under
secondary scoring, Banglish is slightly ahead of Bangla. This is an important
limitation on the main claim. With enough capability and answer recovery, the
population gap can nearly disappear on validation-200.

But that is not the whole frontier story. Gemini 3.5 Flash reduces the gap but
retains a strict deficit. Claude Sonnet 4.6 has high absolute accuracy but still
scores 32 items lower on reviewed Banglish than on Bangla under strict scoring.
It also produces more long and multiline answers under an answer-only prompt,
which creates format-compliance and cost issues. DeepSeek V4 Flash and
Groq-hosted Llama 3.3 70B retain large Banglish deficits.

The correct conclusion is therefore not "frontier models solve Banglish." It is
more precise: stronger models can reduce the semantic gap, but script robustness
remains model-dependent, parser-dependent, and cost-dependent.

## 11. Scale Extension: Does the BEnQA Pattern Survive Beyond 200 Items?

The validation-200 gold core is deliberately small and carefully audited. That
is a strength for controlled analysis, but it also raises an obvious scale
question: does the pattern survive beyond the selected 200 items? We answer
that with a BEnQA-only silver extension.

The extension construction starts from 4,939 eligible BEnQA source rows after
excluding the frozen gold-core BEnQA items. We select 1,000 rows with
deterministic subject-balanced sampling. AI-assisted structural review marks
851 rows as pass, 149 as warning-only, and 0 as structural failure. The 851-pass
subset is used for conservative large-scale evaluation.

This extension is not human-reviewed and must not be described as a replacement
for validation-200 v5. Its purpose is scale support: does the BEnQA part of the
script-gap result survive outside the gold core?

**Table 6. BEnQA full851 scale results.**

| Model | Bangla | Reviewed Banglish | English | BG-BN | BG-EN |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 291/851 | 248/851 | 437/851 | -5.05 pts, CI [-8.46, -1.65] | -22.21 pts, CI [-26.20, -18.10] |
| DeepSeek V4 Flash | 665/851 | 376/851 | 697/851 | -33.96 pts, CI [-37.84, -30.08] | -37.72 pts, CI [-41.36, -33.96] |

Both full851 runs reproduce the same ordering:

**English > Bangla > reviewed Banglish.**

The two models behave differently in absolute accuracy. DeepSeek V4 Flash is far
stronger than Qwen2.5-3B on the extension. But the Banglish deficit remains, and
for DeepSeek it is much larger. This is one of the strongest results in the
paper. It shows that higher absolute accuracy does not guarantee Banglish
robustness, and that the extension result is not only a Qwen-local artifact.

The full851 runs also provide qualitative examples. Qwen2.5-3B has 311
recoverable reviewed-Banglish misses; DeepSeek V4 Flash has 380. These are
cases where reviewed Banglish is wrong but Bangla or English is correct on the
same item. They are useful for error analysis and defense slides, but they are
not a separate statistical test.

## 12. Natural Code-Mixed External Layer

The controlled benchmark uses curriculum-style QA and math. That gives strong
paired evidence, but it does not fully represent natural social media Banglish.
We therefore add a separate ecological-validity layer using BnSentMix, a
Bengali-English code-mixed sentiment dataset [@bnsentmix2024].

We build a balanced 200-row four-way sentiment slice with 50 positive, 50
negative, 50 neutral, and 50 mixed items. The task is not paired by script, so
it cannot estimate a Bangla-vs-Banglish script penalty. It answers a different
question: do compact open models handle naturally occurring Bengali-English
mixed text reliably?

**Table 7. BnSentMix natural code-mixed sentiment results.**

| Model | Accuracy | Macro-F1 | Valid outputs |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 89/200 | 0.431 | 200/200 |
| Qwen2.5-7B 8-bit | 98/200 | 0.479 | 200/200 |
| Qwen3-4B | 99/200 | 0.486 | 200/200 |

The models are above the 25% majority baseline, but absolute accuracy remains
modest. The error-overlap analysis shows substantial complementarity: the best
single model is 99/200, while a diagnostic any-model oracle reaches 154/200.
This oracle is not deployable because it chooses the correct model after seeing
the gold label. Its value is diagnostic: model errors on natural code-mixed text
are not uniform.

This layer supports the broader motivation that Bengali-English mixed text is
difficult and user-relevant. It does not replace the controlled paired
script-gap result.

## 13. Mitigation Attempts

The mitigation story should be honest. The thesis does not yet have a general
solution, and that negative result is still useful: it prevents the evaluation
problem from being hidden behind a fragile prompt wrapper.

### 13.1 Self-normalization

Same-model self-normalization asks the model to rewrite Banglish into Bangla and
then answer. It helps one model and hurts another.

**Table 8. Self-normalization on validation-200 v3.**

| Model | Clean Banglish baseline | Self-normalized | Delta |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 38/200 | 51/200 | +6.5 pts |
| Qwen3-4B | 46/200 | 21/200 | -12.5 pts |

The Qwen2.5-3B gain is real but brittle. It includes 27 gains and 14 losses,
and the rewrite audit shows option, digit, and formula preservation errors. The
Qwen3-4B result is more severe: accuracy collapses even though surface
preservation counters look better. This means the procedure changes model
decision behavior, not just text quality.

The conclusion is simple: self-normalization is not a general Banglish solution.

### 13.2 Generated alternate-script views

A stronger mitigation idea is to generate alternate script views and route only
when views agree. This is attractive because the cross-script oracle shows that
many Banglish misses are recoverable under Bangla or English. But the deployable
version cannot use gold benchmark views. It must generate those views reliably.

The generated-view audits show why this is hard.

Raw deterministic Bangla transliterators corrupt MCQ option labels. Protected
variants reduce some failures, but earlier versions fail tightened
formula-expression gates. A formulaish-token protected-v3 wrapper repairs the
hard preservation gate on the small dev audit, but answer gains remain small and
uncertain. A guarded generated-English repair passes preservation gates, but
15/36 rows fall back to the source Banglish text. Agreement routing is too
sparse: it misses most generated-view oracle recoveries.

The correct claim is therefore negative:

**Generated-view routing is promising, but current cheap generated views are not
reliable enough for a held-out mitigation claim.**

This matters because it prevents overclaiming. The paper diagnoses a real
orthographic robustness problem and shows that naive mitigation is brittle.

## 14. Discussion

### 14.1 What the result means

The result should be read with the right scope. It is not that Bangla is weak.
It is not that Banglish is always worse. It is not that stronger models never
solve the problem.

The result is that script choice changes reliability under controlled
conditions. A model can answer an item in Bangla or English and fail on reviewed
Banglish. This happens often enough to affect aggregate accuracy, paired gaps,
and qualitative examples. It survives review, tokenization controls, compact
model scaling, frontier-model comparison, and BEnQA scale extension.

The practical lesson is similar to many robustness studies: the visible system
may look multilingual, but the interface can still contain a hidden access
failure. Here the hidden variable is not the topic or the answer; it is the
orthography through which the user reaches the model.

### 14.2 Why GPT-5.5 matters

GPT-5.5 is the strongest boundary case. Under secondary scoring, it nearly
eliminates the validation-200 population gap. This is important and should not
be hidden. It tells us that high-capability models can recover much of the
semantic answer.

But GPT-5.5 does not make the broader problem disappear. On the 974-row
human-reviewed BEnQA scale layer, GPT-5.5 none keeps a clear paired deficit:
820/974 Bangla, 699/974 reviewed Banglish, and 825/974 English. First, the
validation-200 result mixes tasks and includes secondary parser recovery, while
the larger BEnQA result tests a cleaner MCQ scale setting. Second, other strong
or hosted models also remain gap-positive. Third, even when the semantic answer
is recoverable, cost and format compliance can change with script. For
deployment, the question is not only "can any model answer?" but "which models
answer reliably, cheaply, and in the required format?"

### 14.3 Why DeepSeek full851 matters

DeepSeek V4 Flash full851 is important because it separates model capability
from script robustness. DeepSeek is much stronger than Qwen2.5-3B on the BEnQA
extension. Yet its reviewed-Banglish deficit is much larger. This makes the
paper stronger than a small-model failure story. A model can be high-accuracy in
Bangla and English while still being fragile in Banglish.

### 14.4 Practical implications

For benchmark builders, script variants should be first-class conditions, not
informal noise. If a benchmark only measures native script or English, it can
miss a real access gap for users who write in Latin-script Banglish.

For model developers, normalization should be evaluated end to end. A
transliterator that preserves words may still corrupt options, digits, formulas,
or decision behavior. Preservation gates are necessary before routing or
generated-view mitigation claims.

For deployment, a model that is strong in Bangla is not automatically robust to
Banglish. Applications that serve Bangla users should log, test, and report
performance separately for native Bengali script and Latin-script Banglish.

## 15. Limitations

This paper has several limitations. These limitations are important because they
define what the results should and should not be used to claim.

**Controlled Banglish is not fully natural Banglish.** The reviewed Banglish
variant is designed for paired evaluation. It is cleaner and more task-like than
many user messages. Real Banglish can be shorter, noisier, more code-mixed, and
more spelling-variable. BanglaTLit and BnSentMix help motivate this, but they do
not replace a future naturally paired Bangla/Banglish QA dataset.

**The validation set is small by benchmark standards.** Validation-200 is a gold
core, not a massive benchmark. Its strength is the paired design, review, and
audits. The BEnQA full851 extension addresses scale for one task family, but it
is AI-assisted silver evidence, not human-reviewed gold evidence.

**The extension is BEnQA-only.** The full851 scale result covers science MCQs.
It does not scale the BanglaMATH part of the benchmark. BanglaMATH remains a
smaller stress-test slice for arithmetic and answer normalization.

**Model coverage is broad but not exhaustive.** The paper covers compact Qwen
models and five hosted API rows, but it does not cover every family. It should
not claim universal behavior across all LLMs. The correct claim is that script
robustness is model-dependent and must be measured.

**Secondary scoring is not a replacement for strict scoring.** Secondary scoring
helps separate semantic recoverability from format compliance. But in deployed
systems, strict format compliance often matters. Both views should be reported.

**Generated-view mitigation remains unresolved.** The current generated-view
experiments are dev-only diagnostics. They show preservation and routing
problems, not a deployable fix.

## 16. Reproducibility and Artifacts

The core artifacts are:

- Main validation-200 v5 report:
  `reports/main_results_validation200_v5.md`
- Main validation table:
  `results/tables/main_script_gap_validation200_v5.csv`
- Frontier API panel:
  `reports/frontier_api_panel_validation200_v5.md`
- Qwen2.5-3B full851 result:
  `reports/qwen25_3b_benqa_ext_full851.md`
- DeepSeek V4 Flash full851 result:
  `reports/deepseek_v4_flash_benqa_ext_full851.md`
- BEnQA extension strategy:
  `reports/benqa_extension_publication_strategy.md`
- BnSentMix external layer:
  `reports/bnsentmix_external_validation_results.md`
- Generated-view diagnostics:
  `reports/generated_view_diagnostics_summary.md`
- Dataset card:
  `reports/dataset_card_validation200.md`

The current status dashboard reports 71 rows, 0 blocked, and 0 failing:

- `reports/current_research_status_dashboard.md`

The local artifact reference checker reports 0 unexpected missing references,
and the reproducibility manifest tracks 1116 artifacts:

- `reports/local_artifact_reference_check.md`
- `reports/reproducibility_artifact_manifest.md`

## 17. Conclusion

Script choice matters for Bangla LLM evaluation. On a controlled
Bangla/Banglish/English validation set, reviewed Latin-script Banglish is less
reliable than native Bengali script and English for compact Qwen models. The
gap survives targeted review, denominator sensitivity, tokenization audits, and
recoverability analysis. Frontier models reduce the validation gap unevenly,
but the larger 974-row human-reviewed BEnQA panel makes the scale story
stronger: every completed row, including GPT-5.5 none, keeps reviewed Banglish
below Bangla on paired items.

The broader lesson is practical. Banglish should not be treated as informal
noise that models will automatically handle. For Bangla users, Latin-script
input is a real access path. Robust evaluation must measure it directly, and
robust mitigation must preserve task structure, answer format, and script
equivalence rather than assuming that larger models or simple normalization will
solve the problem.

## Appendix A. Claim Boundaries

Use these claims:

- Script choice is a measurable robustness variable for Bangla LLM evaluation.
- Reviewed Banglish is systematically less reliable than Bangla and English for
  the compact Qwen rows studied.
- GPT-5.5 is a boundary case that nearly closes the validation-200 gap under
  secondary scoring, but its 974-row BEnQA scale run still preserves a clear
  reviewed-Banglish deficit.
- Gemini, GPT-5.5 none, Claude, DeepSeek, Groq, and Qwen2.5-3B show that
  frontier or hosted status alone does not guarantee Banglish robustness.
- The 974-row human-reviewed BEnQA scale panel shows that the BEnQA ordering
  scales beyond the 200-item mixed-task core.
- Current mitigation evidence is negative or model-dependent.

Avoid these claims:

- Banglish is universally harder for every model.
- The controlled Banglish slice fully represents natural human Banglish.
- The BEnQA extension is human-reviewed.
- GPT-5.5 proves the problem is solved.
- Tokenization has no role at all.
- Generated-view routing is deployable today.

## Appendix B. Short Paper Compression Plan

For a venue with a strict page limit, compress this draft as follows:

1. Keep Sections 1, 2, 4, 5, 8, 10, 11, 15, and 17.
2. Merge related work into two paragraphs.
3. Move BnSentMix and mitigation to an appendix or analysis subsection.
4. Keep only four main tables:
   - validation-200 Qwen results,
   - frontier API panel,
   - full851 scale results,
   - recoverability/source decomposition.
5. State limitations early and briefly.

The paper should not become a model leaderboard. The main story is the paired
script-robustness result and its boundary.
