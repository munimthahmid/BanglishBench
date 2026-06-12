# Chapter 2 Related Work Draft

Updated: 2026-05-29

## 2.1 Bengali Evaluation Benchmarks

Bengali language evaluation has expanded quickly in recent work. BEnQA provides
Bengali-English science examination questions from the Bangladeshi curriculum
and shows that large language models can perform substantially worse in Bengali
than in English. BanglaMATH focuses on elementary mathematical word problems in
Bangla and translated English, exposing language bias in mathematical
reasoning. MGSM provides a broader multilingual arithmetic benchmark and serves
as an external check beyond local curriculum data.

Other recent Bengali resources broaden the evaluation landscape. BanglaQuAD
offers native-speaker open-domain extractive QA from Bengali Wikipedia. BnMMLU
extends Bengali evaluation to multitask multiple-choice knowledge. BLUCK
focuses on Bengali linguistic and cultural knowledge. NCTB-QA provides
textbook-grounded Bangla question answering. BNLI covers natural-language
inference, and Bangla Social Bench studies Bangladeshi sociopragmatic and
cultural alignment.

The 2026 landscape further reinforces that Bengali evaluation is active across
modalities and application domains. BanglaVerse evaluates Bengali cultural
understanding in multilingual vision-language models across linked languages
and regional dialects. Bengali-Loop builds community benchmarks for long-form
Bangla ASR and speaker diarization. BanglaGuard studies Bangla LLM safety and
defense, while BanglaMedQA/BanglaMMedBench focuses on Bangla biomedical QA and
retrieval-augmented generation. These resources broaden the ecosystem, but they
do not remove the need for a controlled text-only Bangla/Banglish/English
orthographic robustness benchmark.

These benchmarks are important because they show that Bengali is not simply
unevaluated. They also define the gap this thesis targets. Most evaluate native
Bengali script, English translation, or task-specific Bengali prompts. They do
not usually hold the same item and gold answer fixed across native Bangla,
Latin-script Banglish, and English to isolate orthographic robustness.

## 2.2 Romanized And Code-Mixed Bangla

Romanized Bangla is a common user practice. BanglaTLit demonstrates that
Romanized Bangla is widespread and highly spelling-variable, and it builds a
large back-transliteration resource. BanglishRev shows that real e-commerce
review data contains Bangla, English, code-mixed text, and Banglish. These
resources motivate treating Banglish as a practical user-facing condition rather
than an artificial benchmark trick.

Several social-media and classification datasets also center transliterated or
code-mixed Bangla. BAN-TH covers transliterated Bangla hate speech. BnSentMix
targets Bengali-English code-mixed sentiment. MixSarc studies implicit meaning,
humor, sarcasm, and offense in Bangla-English code-mixed text. These resources
show that Banglish and code-mixed Bangla matter for online NLP, but they are
mostly classification datasets. They do not measure whether a model can solve
the same QA or math item across native and Romanized scripts.

Bhasha-Abhijnaanam adds an infrastructure perspective. It builds language
identification resources for native-script and Romanized text across Indic
languages, including Bangla. This supports a practical point: Roman-script
Indic text is not merely misspelling. It often requires dedicated detection,
normalization, and modeling support.

## 2.3 Transliteration And Script Robustness

Script and transliteration have long been recognized as modeling variables in
Indic NLP. Work on transliteration for multilingual language modeling argues
that mapping related Indo-Aryan languages into a common script can improve
representation learning during pretraining. This suggests that script choice can
affect model representations and downstream performance.

The closest Bangla robustness predecessor studies transliteration perturbations:
Bangla text is partially replaced with transliterated words or sentences, and
model behavior is measured under those perturbations. This establishes that
script mixing can expose vulnerabilities in Bangla models.

Script Matters differs in three ways. First, it evaluates full item-level
equivalence across native Bangla, clean Banglish, noisy Banglish, and English,
rather than only perturbing parts of a native-script input. Second, it studies
downstream QA and math answer accuracy with paired item ids and gold answers.
Third, it connects measurement to mitigation audits, including prompting,
self-normalization, cross-script agreement, and generated-view preservation.

Script Gap provides a broader framing by studying native versus Romanized
scripts in Indian-language healthcare triage and reporting degradation on
Romanized messages. This supports the importance of script robustness in
high-impact settings. Our thesis transfers that concern to Bangla educational
QA and mathematical reasoning, where the user impact is learning access and
educational support.

Adjacent romanized-language work points in the same direction. The Romanized
Nepali LLM benchmark evaluates comparable open-weight models on Romanized
Nepali adaptation and shows that romanized South Asian language use deserves
direct LLM evaluation rather than being treated as an informal spelling variant.
Its language and task setup differ from Script Matters, but it strengthens the
regional motivation for explicit Roman-script low-resource evaluation.

## 2.4 Tokenization And Cost Inequality

Tokenizer design can produce unequal costs across languages. Prior tokenization
fairness work shows that some languages require more tokens for the same
content, which can increase inference cost, latency, and context usage. This is
especially relevant for low-resource and non-Latin-script languages, where
subword tokenizers may fragment text heavily.

This thesis measures tokenization because token count is an obvious alternative
explanation for script-gap results. However, the current Qwen results complicate
a simple token-length account. Banglish is token-cheaper than native Bangla for
the Qwen tokenizers, yet competent Qwen models are less accurate on Banglish
than on native Bangla. Cross-script failure-pattern analysis further shows that
recoverable Banglish misses are not simply the longest Banglish prompts.

The conclusion should be phrased carefully. Tokenization may still matter, and
spelling variation may interact with token boundaries. The current evidence only
rules out token count alone as a sufficient explanation.

## 2.5 Latent Pivots And English-Centric Mechanisms

Several mechanistic and representation studies suggest that multilingual LLMs
may use English-centric intermediate representations. Do Llamas Work in English?
uses logit-lens analysis to argue that Llama-family models can pass through
English-like concept-space representations before producing target-language
tokens. Do Multilingual LLMs Think in English? extends this framing to
multi-token generation and reports English-centric semantic decisions across
several models and languages. RomanLens argues that romanized forms can act as
an internal bridge for non-Roman-script languages.

MALT studies Urdu and argues that low-resource language understanding and
target-language generation can separate: internal latent responses may be more
coherent than final target-language outputs when translation features are lossy.
This is useful mechanism-adjacent context for Script Matters because it warns
against treating "understanding the item" and "producing a robust answer under a
specific script/language condition" as the same thing.

Script Matters does not currently prove an internal mechanism. Its contribution
is behavioral and diagnostic: the same item can be answered under one script and
missed under another, and privileged cross-script agreement can recover some
Banglish failures. The latent-pivot literature helps interpret why English
views and cross-script agreement are informative, but it should not be used to
claim causal internal behavior without additional representation probes.

## 2.6 Mitigation: Normalization, Translation, And Routing

Romanized Bangla resources naturally suggest normalization as a mitigation:
convert Banglish to native Bangla, then ask the model to answer. BanglaTLit and
IndoTranslit support this direction by providing transliteration data and models
for Romanized-to-native conversion. Translation or English-pivot prompting is
another common strategy for low-resource tasks.

The current experiments show why mitigation must be evaluated rather than
assumed. Simple Banglish-aware prompting and few-shot prompting were weak.
Same-model self-normalization helped Qwen2.5-3B but did not scale cleanly to
Qwen2.5-7B after held-out testing and hurt Qwen3-4B. Same-model English pivot
was also weak in validation and MGSM probes.

Cross-script agreement gives a stronger signal. If Bangla and English views
agree on an answer that differs from the Banglish answer, the model often
recovers a Banglish miss. However, this is a privileged diagnostic because the
benchmark already contains Bangla and English views. A deployable system would
need generated alternate-script views, and the generated-view audits show that
preservation gates are mandatory: generators can corrupt options, digits,
formulas, or answer instructions.

## 2.7 Bangla Model Ecosystem

Bangla-focused modeling work is also growing. BanglaNLG/BanglaT5 provides
sequence-to-sequence generation resources and a BanglaT5 model. BanglaByT5
argues for byte-level modeling as a way to reduce tokenizer mismatch for a
morphologically rich language. TituLLMs and TigerLLM show active development of
small Bangla-focused LLMs and benchmarks.

These models are relevant to future robustness work, but they do not by
themselves answer the Script Matters question. Some are generation or
encoder-decoder systems rather than instruction-following answerers; some
require prompt/template work before fair evaluation; and none substitute for a
controlled Bangla/Banglish/English item-level robustness benchmark.

## 2.8 Positioning Of This Thesis

The thesis should be positioned as an orthographic robustness study for Bangla
LLM use. Existing work establishes Bengali benchmark gaps, Romanized Bangla
prevalence, script robustness concerns, tokenization inequity, and possible
English-centric internal mechanisms. The missing piece is a controlled
downstream evaluation where the same Bangla QA/math item is tested in native
Bangla, Latin-script Banglish, and English, with paired item-level analysis and
mitigation audits.

This framing avoids two overclaims. First, Bengali is not unevaluated in
general. Second, Banglish is not solved merely because Romanized text exists in
training data or because models may internally use romanized bridges. The
empirical question is whether explicit user-facing Banglish input preserves
task-solving accuracy. The current evidence shows that for competent open Qwen
baselines, it often does not.

## Citation Key Checklist

Use these keys from `literature/references_seed.bib` when converting this draft
to the final thesis format:

| Section | Citation keys |
| --- | --- |
| Bengali evaluation benchmarks | `shafayat-etal-2024-benqa`, `banglamath2025`, `mgsm2022`, `banglaquad2024`, `bnmmlu2025`, `bluck2025`, `nctbqa2026`, `bnli2025`, `banglasocialbench2026`, `banglaverse2026`, `bengaliloop2026`, `banglaguard2026`, `banglamedqa2025` |
| Romanized/code-mixed Bangla | `fahim-etal-2024-banglatlit`, `banglishrev2024`, `banth2024`, `bnsentmix2024`, `mixsarc2026`, `bhashaabhijnaanam2023` |
| Transliteration and script robustness | `haider-etal-2025-robustness`, `scriptgap2025`, `indotranslit2025`, `romanizednepali2026` |
| Tokenization and cost | `tokenizerfairness2023` |
| Latent pivots and mechanisms | `wendler-etal-2024-llamas`, `thinkenglish2025`, `romanlens2025`, `malturdu2025` |
| Bangla model ecosystem | `banglanlg2022`, `banglabyt52025`, `titullms2025`, `raihan-zampieri-2025-tigerllm` |
| Math benchmark background | `gsm8k2021`, `mgsm2022`, `banglamath2025` |
