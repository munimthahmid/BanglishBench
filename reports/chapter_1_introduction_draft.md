# Chapter 1 Introduction Draft

Updated: 2026-05-30

## 1.1 Motivation

Bangla is one of the world's most widely spoken languages, yet many language
technologies are still evaluated primarily through native-script Bangla or
English. This misses a common user behavior: Bangla speakers often write
Bengali-language content in Latin script, usually called Banglish. In everyday
messaging, search, comments, reviews, and informal learning contexts, a user may
ask a Bangla question without using Bengali script at all.

For language models, this creates a practical robustness problem. A model that
can answer a question in native Bangla may fail when the same Bangla content is
written in Latin characters. Conversely, a model may appear strong in English
because English is heavily represented in training data, while still failing on
Latin-script Bengali. Evaluating only Bangla and English therefore gives an
incomplete picture of how useful a model is for Bangla-speaking users.

Recent Bengali benchmarks cover increasingly broad tasks: science and
curriculum QA, math word problems, open-domain QA, multitask knowledge,
linguistic/cultural knowledge, textbook QA, natural-language inference, and
social alignment. Romanized and code-mixed Bangla resources also exist for
transliteration, sentiment, safety, sarcasm, and review analysis. The remaining
gap is narrower: these resources rarely isolate script choice while holding the
underlying item, answer, and task fixed across native Bangla, Latin-script
Banglish, and English.

This thesis studies that gap directly.

## 1.2 Problem Statement

The central question is whether orthography itself changes large language model
behavior for Bangla tasks. In this thesis, orthography means the written form of
the same Bengali-language content: native Bengali script versus Latin-script
Banglish. The evaluation keeps item identity and gold answers fixed wherever
possible, so a model's performance difference cannot be explained by comparing
different questions.

The project focuses on educational and reasoning tasks because they are
high-value use cases and because source benchmarks already expose Bengali
language gaps. The validation-200 slice combines BEnQA multiple-choice
curriculum QA and BanglaMATH word problems, with Bangla, clean Banglish, noisy
Banglish, and English views. The Banglish view is controlled and
pipeline-generated, then reviewed through the frozen v5 workflow before final
analysis.

The thesis does not claim that the current Banglish slice represents all natural
human Banglish. Instead, it uses controlled Banglish to test whether script
choice alone can change answer accuracy under paired conditions, then uses real
Romanized Bangla resources to frame limitations and future work.

## 1.3 Research Questions

RQ1. Do compact open instruction models answer the same Bangla educational
items less accurately when the content is written in clean Latin-script
Banglish instead of native Bangla script or English?

RQ2. Is any observed Banglish deficit explained by simple artifacts such as
token count, deterministic romanizer artifacts, noisy spelling, or impossible
items?

RQ3. How stable is the effect across model families and model sizes?

RQ4. Do low-cost mitigations such as prompt instructions, self-normalization,
external normalization, or cross-script answer agreement recover the lost
accuracy?

RQ5. What benchmark-quality controls are needed before claiming a thesis-grade
Banglish evaluation slice?

## 1.4 Summary Of Current Findings

The strongest current result is the validation-200 script gap for competent Qwen
models. In the frozen-v5 main table, Qwen2.5-3B scores 54/200 in Bangla,
41/200 in reviewed Banglish, and 71/200 in English. Qwen2.5-7B 8-bit scores
65/200, 47/200, and 94/200. Qwen3-4B scores 80/200, 49/200, and 88/200.
Paired Banglish-minus-Bangla intervals remain negative for Qwen2.5-7B and
Qwen3-4B. The Qwen2.5-3B all-200 interval reaches zero, while its historical
v3 estimate and strict-197 sensitivity remain negative.

The result is not simply a token-count story. For the Qwen tokenizers, Banglish
is token-cheaper than native Bangla, yet the main models are less accurate on
Banglish. Cross-script failure analysis also shows that many Banglish misses are
not impossible items: the same model often answers the item correctly in Bangla
or English. In the reviewed-v5 diagnostic refresh, a privileged cross-script
agreement route recovers substantial accuracy, which suggests useful signal
exists across views, but this route is diagnostic because it uses
benchmark-provided alternate-script views.

Mitigation is brittle. Simple Banglish-aware prompting and few-shot prompting do
not close the gap. Same-model self-normalization helps Qwen2.5-3B on
validation-200, is flat for Qwen2.5-7B after held-out testing, and hurts
Qwen3-4B. Generated-view routing remains a promising direction, but cheap
generated views currently require strict preservation gates and have unstable
answer gains on dev-only audits.

Model-family evidence adds nuance. Phi-3.5-mini and Qwen3-1.7B no-thinking show
large Banglish-vs-English gaps but do not show a reliable Banglish-below-Bangla
ordering. Therefore, the thesis claim should not be that every model always
finds Banglish harder than Bangla. The safer claim is that controlled
Latin-script Banglish exposes a substantial orthographic robustness weakness in
the competent open Qwen baselines tested so far, and that this weakness is not
measured by standard Bangla-vs-English evaluation.

The frozen v5 review strengthens the data-quality argument. After 140 queued
Banglish rows were reviewed, Qwen2.5-3B moves from 39/200 on v4 Banglish to
41/200 on v5, Qwen3-4B moves from 47/200 to 49/200, and Qwen2.5-7B 8-bit moves
from 48/200 to 47/200. These small changes do not erase the script-conditioned
weakness.

## 1.5 Contributions

This thesis makes eight current contributions.

1. It defines a controlled Bangla/Banglish/English evaluation protocol for
   Bangla curriculum QA and math, preserving item ids and gold answers across
   scripts.
2. It provides validation-200 evidence that competent Qwen models are
   substantially worse on clean Latin-script Banglish than on native Bengali
   script.
3. It shows the result is stable under conservative cleanup, broader automatic
   spelling suggestions, deterministic noisy-Banglish variants, and a frozen
   v5 review of 140 queued Banglish rows.
4. It provides tokenization and failure-pattern evidence showing that the
   Banglish deficit is not reducible to longer token sequences or impossible
   items.
5. It evaluates low-cost mitigation attempts and shows that self-normalization
   is model-dependent and can fail under held-out testing.
6. It uses cross-script oracle and answer-agreement analyses to identify
   recoverable Banglish failures and motivate future consistency routing.
7. It audits generated alternate-script views and shows why deployable routing
   requires preservation gates before answer evaluation.
8. It completes a v5 human-review workflow, preregistered analysis plan,
   reproducibility manifest, and post-v5 rerun protocol for a thesis-grade
   benchmark release.

## 1.6 Scope And Limitations

The current benchmark is controlled educational Banglish, not a full
social-media Banglish benchmark. Natural Banglish includes spelling variation,
code-mixing, abbreviations, and informal pragmatics that are only partially
represented here. The validation-200 slice is also small enough that paired
bootstrap intervals and item-level examples should accompany aggregate
accuracy.

The current mechanism evidence is behavioral. Tokenization and cross-script
failure analysis rule out simple explanations, but they do not prove a causal
internal mechanism. Mechanistic claims should remain future work unless
representation-level probes are added.

Finally, the main result is strongest for compact open Qwen models. Other model
families show related but not identical patterns. Frontier API models remain an
optional final external-validity audit now that the human-reviewed v5 slice and
required open-model reruns are locked.

## 1.7 Thesis Roadmap

Chapter 2 reviews Bengali benchmarks, Romanized Bangla resources, script
robustness, tokenization fairness, and English-pivot mechanism work. Chapter 3
describes benchmark construction and the completed v5 human-review workflow. Chapter 4
presents the main script-gap results. Chapter 5 covers robustness checks and
model-family breadth. Chapter 6 analyzes cross-script recoverability and failure
taxonomy. Chapter 7 studies tokenization and mechanism-adjacent evidence.
Chapter 8 evaluates mitigation attempts. Chapter 9 discusses limitations,
release artifacts, and future directions.
