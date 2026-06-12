# Script Matters Thesis Draft

Updated: 2026-06-11

This compiled draft is generated from chapter drafts. Regenerate with:

```bash
python3 scripts/compile_thesis_draft.py
```

Source chapters:

- `reports/chapter_1_introduction_draft.md`
- `reports/chapter_2_related_work_draft.md`
- `reports/chapter_3_benchmark_construction_draft.md`
- `reports/chapter_4_main_results_draft.md`
- `reports/chapter_5_robustness_and_model_breadth_draft.md`
- `reports/chapter_6_failure_analysis_draft.md`
- `reports/chapter_7_tokenization_mechanism_draft.md`
- `reports/chapter_8_mitigation_draft.md`
- `reports/chapter_9_limitations_draft.md`
- `reports/chapter_10_conclusion_draft.md`


---

<!-- Source: reports/chapter_1_introduction_draft.md -->

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

---

<!-- Source: reports/chapter_2_related_work_draft.md -->

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

---

<!-- Source: reports/chapter_3_benchmark_construction_draft.md -->

Updated: 2026-05-30

## 3.1 Design Goal

The benchmark is designed to isolate the effect of script choice on Bangla task
solving. Each item should preserve the same underlying question, gold answer,
answer format, and item id while changing only the written form presented to the
model. This paired design is the core methodological choice of the thesis.

The benchmark is not intended to replace natural Banglish corpora. Instead, it
serves as a controlled orthographic robustness test: if the same item becomes
harder when written in Latin-script Banglish, then script choice is a real
evaluation variable even before modeling the full diversity of natural
Banglish.

## 3.2 Source Tasks

The validation-200 slice uses two source tasks.

BEnQA contributes curriculum-style multiple-choice science and subject
questions with Bengali and English views. It provides the clearest
script-controlled QA signal because current open models have enough competence
to answer a non-trivial portion of the items.

BanglaMATH contributes elementary Bangla math word problems and English
translations. It is harder for the current open models and should be treated as
a stress test. It remains useful because arithmetic and units create strong
preservation requirements for any Banglish or generated-view transformation.

MGSM Bengali is used as an external arithmetic breadth check rather than as the
main validation-200 source. It helps test whether mitigation behavior transfers
outside the local curriculum slice.

## 3.3 Script Variants

Each validation item can contain several views.

Native Bangla:

- Bengali-script source prompt.
- Used as the native-script comparison.

Clean Banglish:

- Latin-script Bengali produced by the project romanization pipeline and later
  cleaned through v4/v5 workflows.
- Used as the main orthographic robustness condition.

Noisy Banglish:

- Deterministic perturbation of clean Banglish.
- Used as a stress/sensitivity condition, not as a natural social-media model.

English:

- Source or translated English prompt.
- Used as a high-resource control and as a cross-script recoverability view.

Generated views:

- Optional generated Bengali or English views from Banglish input.
- Used only for mitigation diagnostics after preservation gates.

## 3.4 Validation Slices

The current core slices are:

| Slice | Items | Role |
| --- | ---: | --- |
| `validation_100_v3` | 100 | Early aligned QA/math validation and mitigation development. |
| `validation_200_v3` | 200 | Main historical full-slice evidence for Qwen2.5-3B and Qwen3-4B. |
| `validation_200_v4` | 200 | Same item ids with conservative Banglish cleanup and dev/test split. |
| `validation_200_v4_dev50` | 50 | Development split for routing/prompt decisions. |
| `validation_200_v4_test150` | 150 | Held-out split for dev-selected decisions. |
| `validation_200_v4_auto_suggested` | 200 | Unreviewed automatic spelling-suggestion sensitivity slice. |
| `validation_200_v5` | 200 | Frozen human-reviewed Banglish slice used for post-v5 sensitivity. |

The dev/test split is deterministic with seed `20260528` and stratified by BEnQA
subject and BanglaMATH grade. Future prompt, routing, generated-view, or paid
API decisions should be selected on dev50 and evaluated unchanged on test150.

## 3.5 Banglish Quality Workflow

The Banglish pipeline has progressed through several quality stages.

v2 removed major nukta artifacts. v3 fixed major conjunct-y artifacts such as
`songkhja` to `songkhya`. v4 applied conservative cleanup without changing item
ids. v4 sensitivity reruns showed that the main Qwen script-gap conclusion did
not depend on these targeted cleanup changes.

The v5 review is complete. Its queue contains 140 rows selected from the
validation-200 slice because they have suggested edits, known artifact patterns,
model-relevant failures, or high replacement burden. The queue includes the
Bangla source, English source, current Banglish, auto-suggested Banglish, model
correctness flags, and the completed human-review fields.

The review workflow is impact-ordered but executed through exact generated
sessions:

- `reports/validation200_v5_review_quickstart.md`
- `reports/validation200_v5_review_impact_ranking.md`
- `reports/validation200_v5_review_calibration_set.md`
- `reports/validation200_v5_review_session_plan.md`
- `reports/validation200_v5_review_session_packets/README.md`
- `reports/validation200_v5_review_session_log.md`
- `scripts/review_validation200_v5_queue.py`

The generated session plan covered all 140 rows in 12 sessions and used exact
helper commands such as
`python3 scripts/review_validation200_v5_queue.py --session 1`. Repeated
patterns such as `konoti -> konti`, `kot -> koto`, and `ekoti -> ekti` were
handled consistently. The full queue remains authoritative; packet Markdown
files are read-only audit aids.

## 3.6 Human Review Labels

The v5 queue uses three editable fields:

- `quality_label`
- `reviewed_banglish`
- `review_notes`

Allowed labels:

| Label | Meaning | `reviewed_banglish` |
| --- | --- | --- |
| `ok` | Current Banglish is acceptable | Blank |
| `minor_edit` | Small spelling/style edit needed | Full replacement prompt |
| `major_edit` | Substantial rewrite needed | Full replacement prompt |
| `bad` | Item should not be trusted as clean Banglish | Blank by default |

For `minor_edit` and `major_edit`, the reviewer must write the full replacement
prompt, not only the changed word. This prevents partial-edit ambiguity during
freeze. For `bad`, the reviewer must leave `reviewed_banglish` blank and write
a short reason in `review_notes`, because bad-row handling affects the final
denominator policy.

## 3.7 Validation And Freeze

The pre-freeze validator checks labels, required replacements, option
preservation, digit preservation, formula preservation, answer-format
instructions, and Bengali-script leakage. The final queue passes with zero
structural errors, zero warnings, and zero pending rows.

The v5 slice was frozen only after:

```bash
python3 scripts/validate_banglish_review_queue.py --require-complete
```

passed with zero errors and zero pending rows.

The applied default freeze keeps all 200 rows and flags three `bad` Banglish
rows with `quality_status=human_review_bad_banglish`. This all-200 denominator
remains the preregistered main policy. A separate strict-197 sensitivity view
excludes the flagged rows from existing outputs and is reported independently
in `reports/v5_bad_row_policy_sensitivity.md`; it is not mixed into the main
tables.

A review edit-distance sensitivity audit separates no-applied-change, tiny,
small, and larger applied edits. The 63 no-applied-change rows already keep
reviewed Banglish below Bangla and English for all three thesis-facing Qwen
rows, so the final gap is not introduced only by heavily edited review rows.
The audit is reproducible from `reports/v5_review_edit_distance_sensitivity.md`.

## 3.8 Evaluation Format

Prompts are answer-only. Multiple-choice items require only A, B, C, or D.
Short-answer items require only the final answer. This is necessary because
models differ in reasoning verbosity, and Qwen3-family thinking behavior can
break answer-only evaluation if not controlled.

All thesis-facing scores should use reparsed/rescored outputs. The answer
parser extracts MCQ labels and short answers consistently across baseline,
mitigation, and future API runs.

## 3.9 Reproducibility Artifacts

The benchmark construction is documented by:

- `reports/dataset_card_validation200.md`
- `reports/reproducibility_release_checklist.md`
- `reports/reproducibility_artifact_manifest.md`
- `reports/v5_analysis_preregistration.md`
- `reports/post_v5_rerun_protocol.md`
- `reports/post_v5_rerun_readiness.md`
- `reports/post_v5_kaggle_job_plan.md`

The artifact manifest records non-secret files and SHA-256 hashes. It excludes
credential files and its own generated outputs. It was rebuilt after the v5
freeze, post-v5 model reruns, and thesis-table regeneration.

A source-variant structural parity audit checks the frozen v5 Bangla, reviewed
Banglish, and English prompt fields for MCQ option labels, digit sequences,
formula-like tokens, and answer instructions. The primary Bangla-vs-reviewed
Banglish pair has 0/200 structural mismatches. The English comparisons have
39/200 diagnostic warnings, which are treated as upstream translation caveats
rather than exclusions from the primary paired Bangla-vs-Banglish analysis.
The audit is reproducible from `reports/v5_source_variant_structural_parity.md`.

## 3.10 Chapter Summary

The benchmark is a controlled paired evaluation of script choice for Bangla
tasks. Its strength is task equivalence across Bangla, Banglish, and English.
Its main limitation is that the current Banglish remains controlled educational
Banglish rather than a natural user corpus. The BanglaTLit distribution,
lexical-coverage, and spelling-variation audits make this limitation explicit
while showing that the measured gap is not confined to the least-attested or
least-spelling-variable rows; per-model coverage and high-variation-exposure
sensitivities keep reviewed Banglish below Bangla and English for each Qwen
row. The completed v5 review, freeze, and rerun protocol are part of the
benchmark contribution rather than administrative cleanup.

---

<!-- Source: reports/chapter_4_main_results_draft.md -->

Updated: 2026-05-31

## 4.1 Chapter Goal

This chapter answers the primary empirical question: when the same Bangla
educational item is written in native Bangla script, clean Latin-script
Banglish, or English, do model answers change?

The main evidence comes from validation-200. Each comparison is paired by item
id, so script-gap estimates measure how the same questions change across script
views rather than comparing different samples.

## 4.2 Main Validation-200 Results

The primary result is that competent Qwen baselines are worse on reviewed
Banglish than on native Bangla and English. Bangla and English are unchanged
from the controlled historical slice; the Banglish column uses the completed
frozen-v5 reruns.

| Model | Bangla | Reviewed Banglish | English | Banglish - Bangla | Banglish - English |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 54/200 | 41/200 | 71/200 | -6.5 pts, CI [-13.0, 0.0] | -15.0 pts, CI [-22.0, -7.5] |
| Qwen2.5-7B 8-bit | 65/200 | 47/200 | 94/200 | -9.0 pts, CI [-16.0, -2.0] | -23.5 pts, CI [-31.0, -16.0] |
| Qwen3-4B | 80/200 | 49/200 | 88/200 | -15.5 pts, CI [-22.0, -9.0] | -19.5 pts, CI [-27.0, -12.0] |

Qwen3-4B is the strongest current open baseline and shows the largest
Banglish-below-Bangla drop: 80/200 in Bangla versus 49/200 in Banglish. The
paired interval remains far below zero, so this is not just aggregate noise.

Qwen2.5-7B 8-bit confirms that the Qwen2.5 script gap persists at a stronger
scaling point. Qwen2.5-3B retains a -6.5-point all-200 deficit, but its
reviewed-v5 interval reaches zero. Its historical v3 interval and the
strict-197 sensitivity remain negative, so the final claim should preserve
this model-specific qualification.

The English column is also important. Banglish uses Latin characters, but the
models are much stronger on English than on Banglish. Therefore, the issue is
not simply that Latin script is easy and Bengali script is hard. Bengali content
written in Latin script remains a distinct robustness condition.

Primary artifacts:

- `results/tables/main_script_gap_validation200_v5.csv`
- `reports/main_results_validation200_v5.md`
- `reports/thesis_results_dashboard.md`
- `reports/figures/main_script_gap.svg`

## 4.3 Dataset-Level Breakdown

BEnQA carries most of the frozen-v5 script-gap signal because current open
models have non-trivial task competence on BEnQA. BanglaMATH remains difficult
across all scripts, so the release-facing interpretation should keep it as a
stress test rather than as fine-grained grade evidence.

| Model | Dataset | Bangla | Reviewed Banglish | English |
| --- | --- | ---: | ---: | ---: |
| Qwen2.5-3B | BEnQA | 49/144 | 41/144 | 66/144 |
| Qwen2.5-3B | BanglaMATH | 5/56 | 0/56 | 5/56 |
| Qwen2.5-7B 8-bit | BEnQA | 60/144 | 47/144 | 86/144 |
| Qwen2.5-7B 8-bit | BanglaMATH | 5/56 | 0/56 | 8/56 |
| Qwen3-4B | BEnQA | 76/144 | 47/144 | 82/144 |
| Qwen3-4B | BanglaMATH | 4/56 | 2/56 | 6/56 |

This matters for interpretation. The thesis should not use BanglaMATH to claim
fine-grained grade-level script effects under current open models. It should use
BanglaMATH as a hard stress test and use BEnQA as the clearer source of the
orthographic robustness signal.

The paired interval view sharpens this point. On BEnQA, Qwen3-4B has a
reviewed-Banglish-minus-Bangla delta of -20.1 points with CI [-28.5, -11.8].
Qwen2.5-3B and Qwen2.5-7B 8-bit are also directionally negative on BEnQA, but
their dataset-only intervals reach zero. BanglaMATH deltas are negative or near
zero, yet the models answer so few BanglaMATH items correctly that it remains a
low-accuracy stress test rather than the clearest dataset-level proof.

Exact paired sign tests give a complementary discordant-pair view. On the
all-200 Banglish-versus-Bangla comparison, Qwen2.5-7B 8-bit has 19 Banglish
gains and 37 Banglish losses, with a two-sided exact p-value of 0.0222.
Qwen3-4B has 8 gains and 39 losses, p<0.0001. Qwen2.5-3B again remains the
weakest row, with 15 gains and 28 losses, p=0.0660, so it should keep the
CI-reaches-zero qualification.

Clustered resampling addresses a stronger dependence concern by resampling
BEnQA subjects and BanglaMATH grades rather than individual items. Under this
cluster bootstrap, the all-200 Banglish-minus-Bangla interval stays below zero
for Qwen2.5-7B 8-bit and Qwen3-4B. Qwen2.5-3B remains directionally negative
but its cluster interval reaches zero, consistent with the main qualification
for that row. BanglaMATH has only three grade clusters, so its cluster
intervals should remain descriptive.

A leave-one-BEnQA-subject stability check further shows that this support is
not a single-subject artifact. Dropping any one BEnQA subject keeps the
reviewed-Banglish-minus-Bangla delta negative for all three thesis-facing Qwen
rows. The Qwen3-4B leave-one-subject range is -23.3 to -18.0 points; the
Qwen2.5 rows remain smaller but negative under all 13 drops.

Subject-macro balancing addresses a related weighting question. Equal-weighting
the 13 BEnQA subjects keeps reviewed Banglish below Bangla for all three
thesis-facing Qwen rows. Qwen3-4B is -20.2 points with a subject-bootstrap CI
[-28.6, -11.2], and Qwen2.5-7B 8-bit is -9.2 points with CI [-16.8, -1.6].
Qwen2.5-3B remains the qualified row at -5.3 points with CI [-15.2, +4.2].

An answer-format audit checks a different validity concern. Qwen2.5-3B has no
format failures across the 600 thesis-facing outputs. Qwen2.5-7B 8-bit has two
reviewed-Banglish BEnQA MCQ format failures; even crediting both as correct
leaves an all-200 Banglish-Bangla gap of -8.0 points. Qwen3-4B has more BEnQA
format failures in English and Bangla than in reviewed Banglish, so parser
failure does not explain the Qwen3 gap.

A BEnQA choice-bias audit separates malformed choices from systematic option
preferences. Qwen2.5-3B and Qwen2.5-7B do not collapse to a single
reviewed-Banglish option label: their largest Banglish option shares are 38.9%
and 39.6%. Qwen3-4B does show a script-conditioned failure mode, predicting D
on 111/144 reviewed-Banglish BEnQA rows even though the gold distribution has
D on only 39/144 rows. This should be reported as an important failure pattern
for Qwen3, not as a parser artifact or as an explanation for the Qwen2.5 gaps.

A distractor-transition audit strengthens that point. Among BEnQA misses where
Bangla or English is correct, reviewed Banglish emits a valid wrong option in
162/164 model-item cases. The Qwen2.5 wrong choices remain distributed, while
Qwen3 selects D on 44/55 recoverable reviewed-Banglish misses. Across items,
27/50 cases with at least two valid recoverable Banglish misses share the same
wrong option across models.

A gold-label balance sensitivity check makes the MCQ interpretation sharper.
After averaging accuracy across A/B/C/D gold-label strata, reviewed Banglish
remains below Bangla and English for all three thesis-facing Qwen rows.
Qwen3-4B is -21.7 points below Bangla on the balanced metric and -29.5 points
on the non-D slice, where option-D over-selection cannot help. Qwen2.5-3B and
Qwen2.5-7B 8-bit remain directionally negative under balancing; keep their
interval qualifications and use the result as sensitivity support.

A cross-model item-consensus audit summarizes the same paired result across the
three thesis-facing Qwen rows. Over 600 model-item slots, reviewed Banglish is
correct 137 times, compared with 199 for Bangla and 253 for English. Resampling
items as paired clusters gives a -10.3-point Banglish-minus-Bangla consensus
delta with CI [-14.7, -6.3], and a -19.3-point Banglish-minus-English delta
with CI [-25.0, -13.7].

The recoverability source decomposition adds one more guardrail for
interpretation. Of 463 reviewed-Banglish misses across the 600 model-item
slots, 185 are recoverable by Bangla or English and 278 are all-script hard.
Native Bangla participates in 104 recoverable misses, English in 157, and both
alternate scripts recover 76. Thus the recoverability evidence is not merely an
English-only effect, although English is the stronger alternate view overall.

The consensus result is not carried by a single Qwen row. In a leave-one-model
stability audit, every two-model subset keeps reviewed Banglish below both
Bangla and English on the all-200 slice and on BEnQA. On all-200, the
Banglish-minus-Bangla pairwise range is -7.8 to -12.2 points, with all
item-bootstrap intervals below zero.

A composition-sensitivity audit checks whether the gap is only a consequence
of number-heavy or formula-heavy educational rows. In the 61 no-digit rows, all
three Qwen rows keep reviewed Banglish below both Bangla and English; the
Banglish-minus-Bangla range is -13.1 to -32.8 points. The 107-row
no-formula/operator subset is also negative for all three Qwen rows. These are
not natural-Banglish samples, but they show that the release-facing result is
not solely a numeric/formula artifact.

Primary artifacts:

- `reports/main_results_validation200_v5.md`
- `reports/subject_breakdown_validation200_v5.md`
- `reports/v5_dataset_gap_intervals.md`
- `reports/v5_paired_sign_tests.md`
- `reports/v5_clustered_gap_robustness.md`
- `reports/v5_benqa_subject_stability.md`
- `reports/v5_benqa_subject_balance.md`
- `reports/v5_answer_format_audit.md`
- `reports/v5_benqa_choice_bias.md`
- `reports/v5_benqa_label_balance.md`
- `reports/v5_recoverability_source_decomposition.md`
- `reports/v5_item_consensus.md`
- `reports/v5_consensus_stability.md`
- `reports/v5_composition_sensitivity.md`

## 4.4 Model Scaling And Breadth

The script gap becomes most interpretable once a model has enough task
competence. The weakest model, Qwen2.5-0.5B, is noisy and does not provide a
useful anchor. Qwen2.5-1.5B shows a clear Banglish-vs-English gap but weaker
Banglish-vs-Bangla separation. Qwen2.5-3B and Qwen2.5-7B show reliable
Banglish-below-Bangla drops.

Qwen3 shows a similar competence threshold. Qwen3-1.7B no-thinking shows a
large Banglish-vs-English gap but no reliable Banglish-below-Bangla gap.
Qwen3-4B shows the strongest script-gap result.

Phi-3.5-mini is an important non-Qwen contrast. It scores 38/200 in Bangla,
40/200 in Banglish, and 80/200 in English. It does not replicate the
Banglish-below-Bangla ordering, but it does show that Banglish is much harder
than English. This constrains the thesis claim: the Banglish-below-Bangla result
is strongest for competent Qwen baselines, while the broader pattern is that
script/language choice strongly changes model behavior.

Primary artifacts:

- `results/tables/model_family_scaling_validation200.csv`
- `reports/model_family_scaling_synthesis_validation200.md`
- `reports/figures/main_script_gap.svg`

## 4.5 Robustness To Banglish Cleanup

The script-gap result is not removed by cleaning known romanization artifacts.
Validation-200 v4 changes 38/200 Banglish fields and removes targeted artifact
classes. Qwen2.5-3B moves from 38/200 to 39/200, and Qwen3-4B moves from
46/200 to 47/200. A broader automatic suggestion candidate changes each model
by only one additional item.

This does not prove the rule-based Banglish is fully natural. It does show that
the main validation-200 script-gap conclusion is not driven by the specific v3
artifact classes targeted by v4 or by the broader automatic suggestions tested
so far.

The frozen v5 review provides a stronger final sensitivity check. After 140
queued Banglish rows were reviewed, Qwen2.5-3B moves from 39/200 on v4 to
41/200 on v5, a +1.0-point change with CI [-1.0, +3.0]. Qwen3-4B moves from
47/200 to 49/200, a +1.0-point change with CI [0.0, +2.5]. Human-reviewed
cleanup slightly improves both required models. The pinned-stack Qwen2.5-7B
8-bit rerun
moves from 48/200 to 47/200, a -0.5-point change with CI [-3.5, +2.5]. Across
all three reruns, reviewed cleanup does not erase the main gap.

The separate strict-197 denominator sensitivity excludes the three flagged
source-quality rows without replacing the preregistered all-200 main policy.
Reviewed Banglish remains below native Bangla for Qwen2.5-3B (-7.1 points,
CI [-13.2, -1.0]), Qwen3-4B (-15.7 points, CI [-22.3, -9.6]), and
Qwen2.5-7B 8-bit (-9.6 points, CI [-16.8, -2.5]). The denominator choice
therefore does not drive the core conclusion.

Primary artifacts:

- `reports/v4_banglish_sensitivity_validation200.md`
- `reports/validation200_v4_auto_suggested_sensitivity.md`
- `results/tables/auto_suggested_banglish_sensitivity.csv`
- `results/tables/v5_reviewed_banglish_sensitivity.csv`
- `results/analysis/qwen25_validation200_v5_vs_v4_banglish.md`
- `results/analysis/qwen3_validation200_v5_vs_v4_banglish.md`
- `results/analysis/qwen25_7b_8bit_validation200_v5_vs_v4_banglish.md`
- `reports/v5_bad_row_policy_sensitivity.md`

## 4.6 Robustness To Deterministic Noise

The deterministic noisy-Banglish condition does not explain the main clean
Banglish gap. On validation-200, Qwen2.5-3B scores 38/200 on clean Banglish and
41/200 on noisy Banglish. Qwen3-4B scores 46/200 on both clean and noisy
Banglish. The current noise generator is therefore not the source of the
observed gap.

This should not be overclaimed. Natural Banglish spelling variation is broader
than the deterministic noise generator. The result only says that this
particular synthetic noise condition does not create the main deficit.

Primary artifact:

- `reports/noisy_banglish_validation200.md`

## 4.7 Subject Spread

Qwen3's BEnQA Banglish deficit is broad across subject strata under the
reviewed-v5 Banglish slice. Qwen3 reviewed Banglish is below Bangla in 12 of
13 BEnQA subject strata, with only Math-II slightly positive. Qwen2.5-7B 8-bit
is below Bangla in 8 of 13 BEnQA strata, and Qwen2.5-3B is more mixed at 7 of
13. The strata are small, so this should be treated as descriptive support
rather than a separate statistical claim.

Primary artifact:

- `reports/subject_breakdown_validation200_v5.md`

## 4.8 Chapter Conclusion

The main result is a paired orthographic robustness gap. Competent Qwen models
answer substantially fewer validation-200 items correctly when the same Bangla
content is written in reviewed Latin-script Banglish rather than native Bangla
script or English. The effect survives targeted Banglish cleanup, broader
automatic spelling suggestions, and the current deterministic noisy-Banglish
stress test.

The claim remains bounded. Banglish is not universally below Bangla for every
model tested, and the reviewed slice is still controlled educational Banglish
rather than a natural user corpus. The strongest thesis-safe statement is that
controlled Latin-script Banglish exposes a robust weakness in the competent
open Qwen baselines, and that this weakness is undermeasured by standard
Bangla-vs-English evaluation.

---

<!-- Source: reports/chapter_5_robustness_and_model_breadth_draft.md -->

Updated: 2026-05-31

## 5.1 Chapter Goal

Chapter 4 establishes the main validation-200 script gap. This chapter asks how
stable that result is under dataset cleanup, spelling stress tests, model size,
and model family. The goal is not to claim that every model behaves the same
way. The goal is to show which parts of the finding are robust and which parts
need careful qualification.

## 5.2 Cleanup Sensitivity

The first robustness concern is that the Banglish gap might be an artifact of a
bad romanizer. The project therefore created validation-200 v4, keeping the
same 200 item ids while applying conservative Banglish cleanup.

The v4 reruns show that targeted cleanup does not remove the main result.
Qwen2.5-3B changes from 38/200 on v3 Banglish to 39/200 on v4 Banglish.
Qwen3-4B changes from 46/200 to 47/200. Both shifts are only one item.

A broader automatic spelling-suggestion candidate also has little effect.
Qwen2.5-3B moves from 39/200 on v4 to 40/200 on the auto-suggested candidate.
Qwen3-4B moves from 47/200 to 48/200. This candidate is not human-reviewed and
should not be used as the final benchmark, but it is useful sensitivity
evidence.

Interpretation:

- The main Qwen script-gap result is not driven by the known v3 artifact classes
  targeted by v4.
- Automatic spelling cleanup does not materially change accuracy.
- The frozen v5 human review also produces small changes relative to v4:
  Qwen2.5-3B moves 39/200 -> 41/200, Qwen3-4B moves 47/200 -> 49/200, and
  Qwen2.5-7B 8-bit moves 48/200 -> 47/200.
- Review-label sensitivity shows the final deficit is not confined to rows
  that required edits. In unreviewed rows, reviewed Banglish is below Bangla
  for Qwen2.5-3B, Qwen2.5-7B 8-bit, and Qwen3-4B; the same is true for the
  reviewed non-bad bucket.
- Review edit-distance sensitivity sharpens that check: the 63 rows with no
  applied Banglish change already keep reviewed Banglish below Bangla and
  English for all three thesis-facing Qwen rows, while larger-edit rows are
  only 19 items.
- Source-variant structural parity shows the primary Bangla-vs-reviewed
  Banglish pair has 0/200 option-label, digit-sequence, formula-token, or
  answer-instruction mismatches. English comparisons have 39/200 diagnostic
  warnings and should remain privileged support rather than the main paired
  denominator.
- English-warning sensitivity shows those 39 warning rows do not carry the
  diagnostic story: on the 161 clean-English items, reviewed Banglish remains
  below both Bangla and English for all three thesis-facing Qwen rows.
- Human review strengthens benchmark quality without turning controlled
  educational Banglish into a fully natural user corpus.
- The BEnQA option-lexical audit makes that limitation concrete: all-option
  exact BanglaTLit coverage is only 18.5%, but the highest option-coverage
  quartile still has a negative reviewed-Banglish-minus-Bangla point gap.

Artifacts:

- `reports/v4_banglish_sensitivity_validation200.md`
- `reports/validation200_v4_auto_suggested_sensitivity.md`
- `reports/validation200_v5_review_queue.md`
- `reports/v5_review_label_sensitivity.md`
- `reports/v5_review_edit_distance_sensitivity.md`
- `reports/v5_source_variant_structural_parity.md`
- `reports/v5_english_warning_sensitivity.md`
- `reports/v5_benqa_option_lexical_coverage.md`
- `results/tables/v5_reviewed_banglish_sensitivity.csv`

## 5.3 Noisy Banglish Sensitivity

The current noisy-Banglish variant tests whether deterministic spelling noise
itself explains the gap. This historical v3 stress test predates reviewed v5
and remains a robustness diagnostic rather than the release-facing main table.
It does not explain the gap. Qwen2.5-3B scores 38/200 on clean
Banglish and 41/200 on noisy Banglish. Qwen3-4B scores 46/200 on both.

This result should be framed narrowly. The noisy generator is a deterministic
stress test, not a model of real social-media Banglish. Natural Banglish has
more diverse spelling variation, code-mixing, abbreviations, and pragmatic
context. The result only shows that this synthetic noise variant is not what
caused the clean Banglish deficit.

Artifact:

- `reports/noisy_banglish_validation200.md`

## 5.4 Qwen Scaling

The Qwen scaling results show that task competence matters. This historical
cross-model matrix intentionally retains the version-specific v3/v4 outputs
available for each model; use the frozen-v5 table in Chapter 4 for final
three-model release numbers.

| Model | Bangla | Banglish | English | Interpretation |
| --- | ---: | ---: | ---: | --- |
| Qwen2.5-0.5B | 40/200 | 44/200 | 40/200 | Too weak/noisy for the main claim. |
| Qwen2.5-1.5B | 46/200 | 38/200 | 72/200 | English gap appears; Bangla gap is weaker. |
| Qwen2.5-3B | 54/200 | 38/200 | 71/200 | Main Qwen2.5 result. |
| Qwen2.5-7B 8-bit | 65/200 | 48/200 | 94/200 | Stronger Qwen2.5 scaling point. |
| Qwen3-1.7B no-thinking | 34/200 | 36/200 | 61/200 | English gap, no reliable Banglish-below-Bangla. |
| Qwen3-4B | 80/200 | 46/200 | 88/200 | Strongest open-model result. |

For Qwen2.5, the Banglish-below-Bangla gap becomes reliable at 3B and persists
at the 7B 8-bit scaling point. For Qwen3, the 1.7B no-thinking model does not
show the Banglish-below-Bangla ordering, while Qwen3-4B shows the strongest
gap. This supports a competence-threshold interpretation: once the model is
capable enough to answer many native Bangla items, Banglish failures become more
visible and meaningful.

The frozen-v5 scaling-transfer audit adds an item-level version of this point.
Under same-family Qwen2.5 3B->7B scaling, all-200 Bangla gains 11 items and
English gains 23 items, while reviewed Banglish gains only 6. Comparing
Qwen2.5-3B to Qwen3-4B, Bangla gains 26 items and English gains 17, but
reviewed Banglish gains 8. Stronger Qwen competence therefore does not
automatically transfer to Latin-script Banglish.

Artifacts:

- `reports/qwen_scaling_validation200.md`
- `reports/model_family_scaling_synthesis_validation200.md`
- `reports/v5_qwen_scaling_transfer.md`
- `results/tables/model_family_scaling_validation200.csv`

## 5.5 Non-Qwen Breadth

Phi-3.5-mini is the strongest current non-Qwen validation-200 contrast. It
scores 38/200 in Bangla, 40/200 in Banglish, and 80/200 in English. The
Banglish-minus-Bangla interval crosses zero, while Banglish-minus-English is
clearly negative.

This matters because it prevents overclaiming. The thesis should not say that
Banglish is universally harder than native Bangla for every compact model. It
can say that script/language choice strongly affects model behavior, that
Banglish remains much weaker than English for Phi, and that the
Banglish-below-Bangla ordering is strongest in the competent Qwen baselines.

Mistral-7B and Indic-Gemma-2B were run only as pilot20 diagnostics. Mistral-7B
8-bit was feasible but weak and slow. Indic-Gemma-2B was parseable under an
Alpaca wrapper but around chance. These results should stay as diagnostic
breadth, not main evidence.

Artifacts:

- `reports/phi35_mini_validation200_v4.md`
- `reports/mistral7b_8bit_pilot20_validation200_v4.md`
- `reports/indic_gemma2b_pilot20_validation200_v4.md`

## 5.6 Bangla-Specialized Model Diagnostics

Bangla- or Indic-specialized labels are not enough to make a model a valid
baseline. BanglaLLM and TituLM pilots produced degenerate or unrelated outputs
under the current evaluator. Indic-Gemma-2B was parseable but low-accuracy.

This should be presented carefully. These pilots do not prove that Bangla
specialization is ineffective. They show that prompt template, answer-only
format, thinking mode, and parser compatibility must be validated before a
specialized model can become thesis evidence.

Artifact:

- `reports/bangla_specialized_model_pilots.md`

## 5.7 Compute-Limited Larger Models

Qwen3-8B was attempted but blocked on Kaggle P100. The 8-bit path failed due to
bitsandbytes backend compatibility, and older bitsandbytes was rejected by the
current Transformers stack. This is a compute/runtime constraint, not a thesis
choice.

The final API audit plan addresses external validity without turning frontier
APIs into exploratory spending. The v5 slice and required open-model reruns are
now locked, so a paid smoke audit is optional and budget-gated.

Artifacts:

- `reports/qwen3_8b_8bit_pilot20_failure.md`
- `reports/kaggle_gpu_feasibility_notes.md`
- `reports/final_api_audit_cost_plan.md`

## 5.8 Chapter Conclusion

The main Qwen script-gap result is robust to targeted Banglish cleanup,
automatic spelling suggestions, and the current deterministic noisy-Banglish
variant. It also persists across stronger competent Qwen baselines. However,
the exact Banglish-below-Bangla ordering is not universal across all compact
models tested. This is a strength rather than a weakness for the thesis: it
shows that the final claim should be precise, model-aware, and supported by
paired uncertainty estimates rather than stated as a universal law.

---

<!-- Source: reports/chapter_6_failure_analysis_draft.md -->

Updated: 2026-06-03

## 6.1 Chapter Goal

The main script-gap result shows that competent Qwen models answer fewer items
correctly in Banglish. This chapter asks whether those Banglish failures are
actually script-specific, or whether they are simply hard items that the model
would fail in any form.

The evidence comes from cross-script oracle analysis, failure taxonomy,
cross-script transfer retention, recoverability-source decomposition,
item-consensus analysis, difficulty-conditioned consensus buckets, qualitative
examples, and tokenization/failure joins.

These diagnostic analyses use frozen-v5 reviewed Banglish outputs. Bangla and
English outputs are reused because those fields did not change. The historical
v3/v4 reports remain available as audit trails.

## 6.2 Cross-Script Oracle

The any-script oracle asks whether the model answers an item correctly in at
least one script view. This is not deployable accuracy because it uses
benchmark-provided Bangla, Banglish, and English views. It is a diagnostic for
recoverability.

| Model | Banglish only | Any-script oracle | BEnQA oracle |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 41/200 | 99/200 | 92/144 |
| Qwen2.5-7B 8-bit | 47/200 | 115/200 | 105/144 |
| Qwen3-4B | 49/200 | 108/200 | 102/144 |

The oracle is much higher than Banglish-only accuracy. This means many
Banglish failures are not impossible questions for the model. The same model
often has enough task knowledge to answer the item when it is shown in Bangla
or English.

The transfer-retention view conditions on that same-model competence. Among
items where the same model is correct in Bangla or English, reviewed Banglish
retains correctness only 34/92 times for Qwen2.5-3B, 39/107 for Qwen2.5-7B
8-bit, and 44/103 for Qwen3-4B. This is a stricter way to say that Banglish
failures are not merely low overall task competence.

Artifact:

- `reports/cross_script_diagnostics_validation200_v5.md`
- `reports/v5_cross_script_transfer.md`

## 6.3 Failure Taxonomy

The failure taxonomy classifies each item by which script views are correct.
Two categories are especially important:

- Bangla and English correct, Banglish wrong.
- Bangla or English correct, Banglish wrong.

For Qwen3-4B, 32/200 items are correct in both Bangla and English but wrong in
reviewed Banglish. Recoverable misses remain substantial: 58/200 for
Qwen2.5-3B, 68/200 for Qwen2.5-7B 8-bit, and 59/200 for Qwen3-4B.

These categories support the core interpretation: Banglish can block access to
answers the model can otherwise produce.

The source decomposition sharpens this point. Across the 600 model-item slots,
reviewed Banglish is wrong in 463 slots. Of these misses, 185/463 are
recoverable by native Bangla or English and 278/463 are all-script hard. The
recoverable portion is not just an English-only effect: native Bangla
participates in 104/185 recoverable misses, English participates in 157/185,
and both alternate scripts recover 76/185. This keeps the analysis aligned
with the thesis claim: script form matters even when the task is available in
the language family, while English remains a stronger alternate view overall.

Artifacts:

- `reports/cross_script_diagnostics_validation200_v5.md`
- `reports/v5_cross_script_transfer.md`
- `reports/v5_recoverability_source_decomposition.md`
- `reports/v5_shared_fragility_examples.md`

## 6.4 Feature Concentration

The reviewed-v5 fragility analysis joins the cross-script failure taxonomy with
dataset metadata and prompt features. It counts a fragility event when a model
gets reviewed Banglish wrong while getting Bangla or English right on the same
item.

Across the three thesis-facing Qwen rows, 185/600 model-item slots are
Banglish-fragile by this definition. The stricter category where both Bangla
and English are correct but Banglish is wrong appears in 76/600 slots. At the
item level, 108/200 items have at least one fragile model, and 21/200 are
fragile for all three thesis-facing models.

The model-overlap refresh separates shared failure from one-model quirks.
Among the 108 any-fragile items, 52 affect exactly one model, 35 affect exactly
two models, and 21 affect all three models. In other words, 56/108 any-fragile
items affect at least two thesis-facing Qwen rows. This supports a family-level
fragility interpretation while preserving the model-specific caveat.

The concentration is not uniform. BEnQA MCQ rows account for most recoverable
Banglish-specific fragility: 164/432 model-item slots, compared with 21/168 in
BanglaMATH. BanglaMATH is still difficult, but much of its difficulty appears
as all-script-wrong behavior rather than recoverable Banglish-only failure. The
highest fragility rates are in science-heavy BEnQA domains such as Biology-I,
Biology-II, Chemistry-II, Biology, Chemistry-I, and general Science. This makes
the failure analysis more precise: the Banglish gap is broad, but recoverable
script-specific misses are especially visible where technical vocabulary and
curriculum terminology must be read through Latin-script Bangla.
The model-overlap report ranks shared fragility by dataset and domain, so
BEnQA math and BanglaMATH math are interpreted separately rather than merged
under one `math` label.

The item-consensus audit gives a second, model-family view of the same pattern.
Across 600 paired model-item slots, reviewed Banglish is correct 137 times,
versus 199 for Bangla and 253 for English. The item-cluster bootstrap deltas
remain negative against both Bangla and English. On BEnQA, 61/144 items have at
least two-model support in Bangla or English while reviewed Banglish has at
most one correct model; only 12/144 BEnQA items are all-script hard. This
supports the claim that many Banglish misses are recoverable script-specific
failures rather than uniformly impossible items.

The difficulty-conditioned consensus audit makes the item-difficulty argument
more direct. It buckets items by how many thesis-facing Qwen rows answer the
English, Bangla, or best alternate-script view correctly. In the all-200 bucket
where all three Qwen rows answer English correctly, reviewed Banglish has
50/147 correct model-item slots versus 92/147 for Bangla, a paired
item-bootstrap delta of -28.6 points with CI [-38.8,-18.4]. In the
English-consensus=2 bucket, reviewed Banglish is 36/108 versus 49/108 for
Bangla. These high-headroom buckets are the important ones: they show that the
Banglish deficit grows on items the Qwen family can answer in another script,
rather than appearing only in all-script-hard rows.

A leave-one-model-out stability audit checks that this consensus pattern is
not driven by any one Qwen row. Every two-model subset remains negative against
both Bangla and English on all-200 and BEnQA. This narrows the residual risk:
the result is still Qwen-family evidence, but it is not a single-model artifact
inside that family.

The composition-sensitivity audit addresses a related alternative explanation:
that the recoverable failures are mostly caused by numeric or formula-heavy
rows. In no-digit rows, no-formula/operator rows, and the stricter BEnQA
no-digit/no-formula subset, all three thesis-facing Qwen rows still answer
reviewed Banglish less accurately than Bangla and English. This does not erase
the benchmark-naturalness limitation, but it weakens a simple
numeric-composition explanation.

The BEnQA choice-bias audit adds a more specific MCQ failure mode. For Qwen2.5,
reviewed Banglish does not collapse to a single answer label, so the Qwen2.5
gap is not just a label-prior artifact. For Qwen3, reviewed Banglish strongly
over-selects option D: 111/144 predictions are D, while gold D appears on
39/144 rows. This is useful failure evidence because it shows script choice can
change not only correctness but also the model's answer-selection prior.

The prediction-diversity audit makes that collapse easier to quantify. Gold
BEnQA labels have 0.994 normalized entropy and 3.97 effective options. Qwen3
reviewed Banglish falls to 0.502 normalized entropy and 2.01 effective options,
while the same model has 3.52 effective options in Bangla and 3.69 in English.
The two Qwen2.5 reviewed-Banglish rows retain 3.75 and 3.77 effective options.

The distractor-transition audit shows that recoverable BEnQA Banglish misses
are usually real wrong-option choices rather than invalid MCQ outputs:
162/164 are valid distractors. Cross-model convergence is also visible: among
50 items where at least two models make valid recoverable Banglish misses, 27
share the same wrong option across at least two models. This is behavioral
evidence of script-conditioned distractor attraction, not an internal mechanism
claim.

The gold-label balance sensitivity check verifies that this is not merely a
gold-label distribution artifact. Label-balanced BEnQA accuracy keeps reviewed
Banglish below Bangla and English for every thesis-facing Qwen row; for Qwen3,
the reviewed-Banglish gap is -21.7 points versus Bangla under balancing and
-29.5 points after removing gold-D items. The non-D slice turns Qwen3's
D-heavy behavior into direct failure evidence rather than a confound.

The subject option-bias audit checks whether Qwen3's D-attractor is localized
to one subject. It is not: Qwen3-4B reviewed Banglish has majority-D
predictions in 12/13 BEnQA subjects, compared with 1/13 for Qwen2.5-3B and
0/13 for Qwen2.5-7B 8-bit. No subject has gold-D share above 45.5%, so this
extends the label-balance result to subject-level behavior.

The option position/content audit checks whether this is only because D is
often the longest option. D is tied for longest on 98/144 BEnQA items, but
Qwen3 still predicts D on 30/46 items where D is not longest, compared with
9/46 and 5/46 for the two Qwen2.5 rows. Length/content therefore contributes
to the behavior but does not reduce it to a length heuristic.

The option-switching audit compares reviewed-Banglish BEnQA predictions with
the same model's Bangla and English option choices. For Qwen3-4B, valid non-D
Bangla predictions become D in reviewed Banglish on 47/73 rows, and valid
non-D English predictions become D on 55/78 rows. Among correct non-D
alternate-script predictions, those switches become wrong-D reviewed-Banglish
answers on 30/44 Bangla rows and 37/54 English rows. The Qwen2.5 rows have
much smaller Bangla-side non-D-to-D rates, 14/99 and 17/126. This makes the
D-attractor a directional script-conditioned transition, not only an aggregate
label-frequency shift.

The cross-script option-agreement audit applies a stricter agreement filter.
When Qwen3 Bangla and English are both correct and agree on the same non-D
option, reviewed Banglish still switches to wrong D on 23/36 rows. The
corresponding Qwen2.5 rates are 2/23 and 7/44. In the broader Qwen3
Bangla-English non-D agreement slice, reviewed Banglish predicts D on 30/47
rows. This shows the D-attractor survives even when both alternate-script
views give the same non-D answer.

The cross-model Banglish-agreement audit holds the reviewed-Banglish input
fixed and asks what happens when both Qwen2.5 rows agree. The two Qwen2.5 rows
agree on a non-D reviewed-Banglish option in 42 BEnQA rows; Qwen3-4B predicts
D on 26 of those rows and wrong D on 18. In the stricter slice where both
Qwen2.5 rows are correct and agree on the same non-D answer, Qwen3 is wrong-D
on 8/15 rows and matches the Qwen2.5 agreement on 4/15. This makes the failure
mode model-specific under the same script, but the strict slice is small and
should be treated as corroborating evidence.

The order-confound audit checks whether the D-attractor is a simple execution
artifact. By reviewed-Banglish output-line quartile, Qwen3 predicts D on
26/36, 31/36, 28/36, and 26/36 rows; wrong-D counts are 20/36, 19/36, 19/36,
and 19/36. Qwen3 has 23 separate D-runs and a longest contiguous D-run of 13,
whereas the Qwen2.5 rows have lower D totals and longest D-runs of 3 and 2.
This rules out a simple late-run or single terminal-corruption explanation.

The review-label option-bias audit checks whether the D-attractor was created
by the v5 Banglish review edits. On unreviewed BEnQA rows, Qwen3 still predicts
D on 39/51 rows and wrong D on 28/51, while gold D appears on 13/51. On
reviewed nonbad rows, Qwen3 predicts D on 69/90 rows; the corresponding Qwen2.5
D counts are 28/90 and 17/90. This rules out a simple review-edit-only
explanation while preserving the caveat that major-edit and bad buckets are
too small for standalone claims.

The length/token confound audit checks whether the same Qwen3 collapse is just
prompt burden. It is not. By reviewed-Banglish HF-token quartile, Qwen3
predicts D on 32/36, 26/36, 27/36, and 26/36 rows, with wrong-D counts of
26/36, 17/36, 15/36, and 19/36. Character-length quartiles tell the same story:
Qwen3 predicts D on 31/36 shortest rows and 29/36 longest rows. The two Qwen2.5
rows stay far lower in the shortest and longest HF-token quartiles. This makes
the D-attractor a script/model behavior rather than a simple long-prompt
failure.

The option-coverage confound audit checks whether Qwen3 is simply choosing the
option with the most familiar BanglaTLit lexical overlap. On 101 BEnQA items,
all four answer options have identical exact coverage under the same tokenizer
used by the option-lexical audit. Qwen3 still predicts D on 76/101 of those
rows and wrong D on 52/101, while the two Qwen2.5 rows predict D on only
14/101 and 8/101. When at least one option has higher coverage than D, Qwen3
still predicts D on 31/35 rows. Exact option familiarity is therefore not a
sufficient explanation for the D-attractor.

The switch-confound audit joins the transition rows with option length/content
features. When the alternate-script prediction is correct, non-D, and D is not
the longest option, Qwen3 still switches to a wrong reviewed-Banglish D on
11/19 Bangla rows and 12/21 English rows. In the broader non-D, gold-not-D,
D-not-longest scope, Qwen3 switches to D on 13/25 Bangla rows and 15/26
English rows. The corresponding correct-non-D and D-not-longest Bangla-side
counts for Qwen2.5 rows are only 1/13 and 2/22. This keeps the failure mode
visible after removing the two most direct confounds: longest-option D and
gold-D rows.

The semantic-cue audit checks composite roman-marker answers, numeric/formula
strings, and all/none/both markers in option text. D has no such simple cue on
47/144 BEnQA rows; Qwen3 still predicts D on 38/47 of those rows, while the two
Qwen2.5 rows predict D on 9/47 and 4/47. Among correct non-D alternate-script
predictions where D has no cue, Qwen3 switches to wrong reviewed-Banglish D on
15/18 Bangla rows and 18/23 English rows; the Qwen2.5 Bangla-side switch counts
are only 1/11 and 3/21.

The multi-confound residual audit combines these local controls. In the primary
residual scope where gold is not D, D is not the longest option, and D has no
simple semantic cue, Qwen3 is wrong-D on 19/24 rows; Qwen2.5 rows are 4/24 and
1/24. In the stricter tied-coverage residual scope, Qwen3 is wrong-D on 16/20
rows, while Qwen2.5 rows are 4/20 and 1/20. When the same model's Bangla or
English answer is already correct and non-D in the primary residual scope,
Qwen3 still switches to wrong reviewed-Banglish D on 11/13 and 11/14 rows.

The controlled option-permutation dev probe moves beyond descriptive
confound slices. It rotates the semantic option content across A/B/C/D for 36
reviewed-v5 BEnQA dev MCQs while remapping gold labels. Among Qwen3 identity
wrong-D items, 35/45 rotated rows remain attached to literal label D and only
6/45 follow the original D content. Qwen2.5-3B shows the opposite tendency:
5/21 remain label D while 12/21 follow the original D content. This is strong
behavioral evidence for a Qwen3 label-position D-attractor under reviewed
Banglish. The probe is dev-only and does not prove an internal causal
mechanism.

The BEnQA option-lexical audit separates question stems from answer options.
Reviewed-Banglish stems average 31.3% exact BanglaTLit token coverage, while
all answer options average only 18.5% and gold options average 17.3%. This is
important limitations evidence, but it does not reduce the MCQ gap to fully
unattested option strings: in the highest all-option coverage quartile,
reviewed Banglish is 40/108 correct model-item slots versus 50/108 for Bangla.

The response-style drift audit adds a short-answer behavior check. On
BanglaMATH, Qwen3-4B reviewed Banglish produces 15/56 meta/uncertainty
outputs, compared with 0/56 for Bangla and 1/56 for English. Qwen3 is verbose
on BanglaMATH in general, so this should be framed as a model-specific
style-drift failure mode, not as a global gap explanation.

The BanglaMATH numeric-sensitivity audit adds a conservative-scoring check. It
generously credits any raw output containing the full gold numeric signature.
Even then, reviewed Banglish remains lowest for all three Qwen rows; for
Qwen3-4B the raw numeric-signature count is 10/56 for reviewed Banglish versus
19/56 for Bangla and 24/56 for English. This supports treating BanglaMATH as a
low-accuracy stress test with parser/unit caveats, not as a parser-artifact
explanation of the script gap.

The BanglaMATH numeric-transfer audit asks whether numeric evidence available in
Bangla or English carries over to reviewed Banglish. It often does not. For
Qwen3, Bangla or English contains the full raw numeric signature on 24/56 items;
reviewed Banglish retains it on 8/24 and is correct on 2/24. Qwen2.5 retention
is 1/12 and 4/24. In Qwen3's alternate-signature slice, 9/24 reviewed-Banglish
outputs contain meta/uncertainty language and 4/24 are wrong no-number outputs.
This reinforces the transfer-failure framing while keeping numeric signatures
as optimistic behavioral evidence.

Artifacts:

- `reports/v5_banglish_fragility_feature_analysis.md`
- `reports/v5_banglish_fragility_model_overlap.md`
- `reports/v5_recoverability_source_decomposition.md`
- `reports/v5_item_consensus.md`
- `reports/v5_difficulty_conditioned_gap.md`
- `reports/v5_consensus_stability.md`
- `reports/v5_composition_sensitivity.md`
- `reports/v5_benqa_choice_bias.md`
- `reports/v5_benqa_prediction_diversity.md`
- `reports/v5_benqa_subject_option_bias.md`
- `reports/v5_benqa_option_position_content.md`
- `reports/v5_benqa_option_switching.md`
- `reports/v5_benqa_cross_script_option_agreement.md`
- `reports/v5_benqa_cross_model_banglish_agreement.md`
- `reports/v5_benqa_order_confound.md`
- `reports/v5_benqa_review_label_option_bias.md`
- `reports/v5_benqa_length_token_confound.md`
- `reports/v5_benqa_option_coverage_confound.md`
- `reports/v5_benqa_multiconfound_residual.md`
- `reports/v5_benqa_option_permutation_probe_results.md`
- `reports/v5_benqa_option_switch_confound.md`
- `reports/v5_benqa_option_semantic_cues.md`
- `reports/v5_response_style_drift.md`
- `reports/v5_banglamath_numeric_sensitivity.md`
- `reports/v5_banglamath_numeric_transfer.md`
- `reports/v5_benqa_option_lexical_coverage.md`
- `reports/v5_benqa_label_balance.md`
- `results/analysis/v5_banglish_fragility_items.csv`
- `results/analysis/v5_banglish_fragility_feature_summary.csv`

## 6.5 Qualitative Failure Examples

Qualitative examples are useful because aggregate accuracy alone does not show
what changes across scripts. The frozen-v5 shared-fragility packet now exports
these examples directly from the model-overlap and failure-pattern tables. The
most thesis-relevant examples are items where:

1. Bangla and English answers agree with the gold answer.
2. Banglish produces a wrong but parseable answer.
3. The prompt content is visibly equivalent across scripts.

The cleanest current packet has five all-three strict cases: every
thesis-facing Qwen row answers Bangla and English correctly while answering
reviewed Banglish incorrectly. The recommended main-body shortlist is
`banglamath_0229`, `banglamath_0230`, and `benqa_10th-Physics_0021`, giving
two compact arithmetic examples and one non-arithmetic MCQ example.

These examples make the result concrete. They show that a failure can be
triggered by orthography rather than by a different question or a malformed
answer format.

The examples should be used sparingly in the thesis. Two or three well-chosen
examples are enough for the main body; the full packet can go in the appendix
or artifact list.

Artifacts:

- `reports/v5_shared_fragility_examples.md`
- `results/analysis/v5_shared_fragility_examples.csv`
- `reports/thesis_qualitative_examples.md`
- `reports/cross_script_answer_agreement_examples.md`

## 6.6 Cross-Script Answer Agreement

The reviewed-v5 cross-script agreement route is a stronger diagnostic. It uses
Bangla and English answer agreement as a signal for when to override Banglish.
This improves Banglish point accuracy for all main Qwen baselines:

| Model | Banglish | Bangla+English agreement route | Route delta |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 41/200 | 49/200 | +4.0 pts, CI [-0.5, +8.5] |
| Qwen2.5-7B 8-bit | 47/200 | 71/200 | +12.0 pts, CI [+6.5, +17.5] |
| Qwen3-4B | 49/200 | 76/200 | +13.5 pts, CI [+8.0, +19.0] |

This is not a final mitigation, because a deployed system usually does not have
gold Bangla and English views. But it shows that answer consistency across
scripts is informative. It motivates generated-view routing, retrieval, or
multi-view prompting as future mitigation directions.

The model-aware uncertainty matters: the reviewed-v5 interval remains clearly
positive for Qwen2.5-7B 8-bit and Qwen3-4B, while the Qwen2.5-3B interval
crosses zero.

Artifacts:

- `reports/cross_script_diagnostics_validation200_v5.md`
- `reports/figures/cross_script_recovery.svg`

## 6.7 Tokenization-Failure Join

A simple explanation would be that Banglish prompts are longer or more
fragmented than Bangla prompts. The tokenization audit does not support this as
a sufficient explanation. For Qwen tokenizers, Banglish is token-cheaper than
native Bangla, yet the main Qwen models are less accurate on Banglish.

Joining tokenization with failure categories gives another check. Under the
frozen-v5 token/failure join, recoverable Banglish misses are not merely the
longest Banglish prompts. In BEnQA, they are shorter on average than
non-recoverable or other items for Qwen2.5-3B, Qwen2.5-7B, and Qwen3-4B. The
strict `bangla_english_correct_banglish_wrong` pattern is also token-cheaper in
reviewed Banglish than native Bangla.

This does not mean tokenization is irrelevant. It means token count alone cannot
explain the Banglish deficit. The mechanism may involve spelling distribution,
subword identity, training frequency, representation alignment, or prompt
grounding.

Artifacts:

- `reports/tokenization_validation200.md`
- `reports/tokenization_cross_script_failure_patterns.md`
- `reports/v5_benqa_length_token_confound.md`

## 6.8 Limits Of The Failure Analysis

The oracle and agreement analyses use privileged benchmark views. They are not
deployable accuracy estimates. They should be presented as diagnostic evidence
that many Banglish misses are recoverable in principle.

The tokenization analysis is also descriptive. It rules out a simple
token-length explanation but does not identify the internal causal mechanism.
Representation-level or intervention experiments would be needed for a
mechanistic claim.

## 6.9 Chapter Conclusion

The Banglish gap is not just a hard-item effect. Many Banglish misses are
answered correctly by the same model under Bangla or English, and privileged
cross-script answer agreement recovers substantial accuracy. At the same time,
Banglish is token-cheaper than native Bangla for the Qwen tokenizers, so the
deficit cannot be reduced to longer token sequences. The feature-level
fragility analysis further shows that recoverable Banglish-specific failures
concentrate in BEnQA science domains, while BanglaMATH is more often hard
across all scripts. The safest conclusion is behavioral: Latin-script Banglish
changes access to task knowledge in ways that standard Bangla-vs-English
evaluation misses.

---

<!-- Source: reports/chapter_7_tokenization_mechanism_draft.md -->

Updated: 2026-05-31

## 7.1 Chapter Goal

This chapter asks what the current evidence can and cannot say about why
Banglish hurts model accuracy. The thesis has behavioral evidence, tokenization
evidence, and cross-script failure evidence. It does not yet have a causal
mechanistic intervention.

The main safe conclusion is narrow: token count alone is not a sufficient
explanation for the Banglish deficit.

## 7.2 Tokenization Motivation

Tokenizer behavior is an obvious place to look for script effects. Prior work
shows that different languages can incur very different token costs, which
affects inference cost, context length, and sometimes downstream quality.
Non-Latin scripts are often fragmented more heavily by tokenizers trained
largely on English or other Latin-script text.

If native Bangla were much more token-expensive than Banglish and also less
accurate, token count could be a candidate explanation for a Bangla deficit.
But the main result is the opposite: Banglish is often token-cheaper than native
Bangla while still producing lower accuracy.

## 7.3 Validation-200 Tokenization Pattern

For the Qwen tokenizers, Banglish uses fewer tokens per word than native Bangla.
The frozen-v5 validation-200 tokenization summaries show this clearly for both
BEnQA and BanglaMATH. The three thesis-facing Qwen tokenizers produce identical
item-level token counts on the 600 item/variant pairs.

| Dataset | Bangla tokens/word | Reviewed Banglish tokens/word | English tokens/word |
| --- | ---: | ---: | ---: |
| BEnQA | 4.0242 | 2.4942 | 1.9545 |
| BanglaMATH | 4.6285 | 2.1114 | 1.4080 |

Yet Qwen2.5-3B, Qwen2.5-7B, and Qwen3-4B are all less accurate on Banglish than
on native Bangla. This makes a simple "more tokens means worse accuracy"
explanation implausible for the main Banglish gap.

Artifacts:

- `reports/tokenization_validation200.md`
- `reports/tokenization_cross_script_failure_patterns.md`

## 7.4 Failure Patterns And Prompt Length

The tokenization/failure join asks whether recoverable Banglish misses are just
long Banglish prompts. They are not. Under frozen-v5, BEnQA recoverable
Banglish misses are shorter on average than other or non-recoverable items for
Qwen2.5-3B, Qwen2.5-7B, and Qwen3-4B. The strict
`bangla_english_correct_banglish_wrong` pattern is also token-cheaper in
reviewed Banglish than in native Bangla.

This strengthens the tokenization result. The model is not simply failing on
Banglish because Banglish prompts are too long. Many failures occur on prompts
that are token-cheaper than Bangla and not unusually long within the Banglish
distribution.

## 7.5 What Tokenization May Still Explain

Token count alone is insufficient, but tokenization may still matter in other
ways.

Possible tokenization-related mechanisms include:

- Rare or inconsistent subword pieces for Romanized Bangla words.
- Poor alignment between Banglish spellings and Bengali semantic units.
- High spelling variation causing related Banglish forms to split differently.
- Token identity effects even when total token count is low.
- Weak co-occurrence between Banglish subwords and formal QA/math contexts in
  training data.

These possibilities require deeper analysis than aggregate token counts. The
current thesis can motivate them, but should not present them as proven.

## 7.6 Latent-Pivot Framing

Mechanism-adjacent literature suggests that multilingual LLMs can use
English-centric internal representations or romanized bridges. This framing is
useful for interpreting Script Matters in two ways.

First, it explains why English views are informative. If English-centric
representations support task solving, English accuracy can reveal whether the
model has access to the underlying answer under a high-resource view.

Second, it explains why cross-script agreement may recover Banglish failures.
If different script views activate partially different routes to the same task
knowledge, answer agreement across views can be a useful signal.

However, this thesis should not claim that the tested Qwen models internally
translate Banglish to English or use a specific latent language mechanism. The
current evidence is behavioral.

Relevant literature:

- RomanLens.
- Do Llamas Work in English?
- Do Multilingual LLMs Think in English?
- MALT Urdu.

Local notes:

- `literature/notes/core_paper_notes.md`
- `literature/notes/script_matters_literature_synthesis.md`

## 7.7 Why Representation Probes Are Optional

A representation probe could strengthen the mechanism chapter. Possible probes
include:

- Hidden-state similarity between Bangla, Banglish, and English views.
- Layerwise logit-lens analysis on matched items.
- Attention or activation comparison for script-specific failures.
- Contrast between recoverable Banglish misses and all-script misses.

These probes are optional because the current thesis already has a strong
benchmark, analysis, and mitigation story. A weak or rushed representation probe
could distract from the main contribution. If added, it should be small,
pre-specified, and tied to the existing item taxonomy.

## 7.8 Chapter Conclusion

The Banglish deficit is not explained by token count alone. Banglish is
token-cheaper than native Bangla for the Qwen tokenizers, and recoverable
Banglish misses are not simply long prompts. The likely explanation involves
script-specific representation, training distribution, spelling variation, and
task grounding, but the current evidence remains behavioral. The thesis should
therefore present tokenization as a control and mechanism clue, not as a full
causal account.

---

<!-- Source: reports/chapter_8_mitigation_draft.md -->

Updated: 2026-05-30

## 8.1 Chapter Goal

This chapter evaluates low-cost ways to recover Banglish accuracy. The goal is
not only to find a positive result. Negative mitigation results are important
because they show that Banglish robustness is not fixed by a simple prompt
wrapper or by blindly rewriting Banglish into another script.

The safest current mitigation conclusion is that recovery is possible, but
reliable recovery requires routing, preservation checks, and held-out
evaluation.

The self-normalization tables intentionally retain historical v3/v4 baseline
outputs. The privileged cross-script agreement route is refreshed against
reviewed-v5 Banglish because that update is locally computable without new
model inference.

## 8.2 Prompting Baselines

Simple Banglish-aware instructions and few-shot Banglish prompting were tested
early on validation-100. They did not close the gap. Qwen3-4B was essentially
unchanged, and Qwen2.5-3B showed at most small prompt-specific gains that did
not solve the underlying issue.

Interpretation:

- The models are not merely missing an instruction that the input is Banglish.
- Few-shot prompting can add noise or distract from answer-only format.
- Prompting alone should not be presented as a strong mitigation.

Artifacts:

- `reports/mitigation_summary.md`
- `results/runs/validation100_v2_banglish_prompt_mitigation_summary_reparsed.csv`

## 8.3 Same-Model Self-Normalization

Self-normalization asks the same model to rewrite Banglish into a more standard
form before answering. This is attractive because it does not require an
external model. The results are strongly model-dependent.

| Model | Baseline Banglish | Self-normalized | Delta |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 38/200 | 51/200 | +6.5 pts, CI [+0.5, +13.0] |
| Qwen2.5-7B 8-bit | 48/200 | 47/200 | -0.5 pts, CI [-7.0, +6.5] |
| Qwen3-4B | 46/200 | 21/200 | -12.5 pts, CI [-19.5, -5.5] |

Qwen2.5-3B improves, but Qwen3-4B degrades sharply. Qwen2.5-7B is especially
important because it prevents a misleading scaling story: dev50 improved from
13/50 to 18/50, but held-out test150 dropped from 35/150 to 29/150. Full200 was
flat overall.

Interpretation:

- Self-normalization can recover signal for one model.
- It is not a general solution.
- Dev-only mitigation gains can reverse on held-out test.

Artifacts:

- `reports/selfnorm_validation200.md`
- `reports/qwen25_7b_8bit_selfnorm_validation200_v4.md`
- `reports/figures/selfnorm_delta.svg`

## 8.4 Answer-Signal Routing

Routing tries to choose between baseline Banglish and self-normalized answers.
The strongest exploratory answer-side rule is:

```text
use self-normalization if the self-normalized answer parses non-empty
```

On test150, this improves Qwen2.5-3B from 31/150 to 43/150 and Qwen3-4B from
32/150 to 40/150. These gains are promising, but they are exploratory because
the candidate rule came from scanning answer-side signals.

| Model | Baseline | Always selfnorm | Routed | Routed - Baseline |
| --- | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 31/150 | 41/150 | 43/150 | +8.0 pts, CI [+0.7, +15.3] |
| Qwen3-4B | 32/150 | 16/150 | 40/150 | +5.3 pts, CI [+1.3, +10.0] |

The same rule does not transfer to MGSM arithmetic. For MGSM, it routes every
item to self-normalization; Qwen2.5 remains 0/50 and Qwen3 drops from 5/50 to
0/50. This limits the generality of the routing result.

Artifacts:

- `reports/selfnorm_answer_signal_routing_validation200.md`
- `reports/mgsm_selfnorm_answer_signal_routing_transfer.md`
- `results/tables/answer_signal_routing_test150.csv`

## 8.5 Cross-Script Agreement As A Diagnostic Mitigation

Reviewed-v5 cross-script answer agreement is the strongest recovery signal. If
Bangla and English views agree on an answer, replacing the Banglish answer with
that agreement improves point accuracy for all main Qwen baselines.

| Model | Banglish | Agreement route | Route delta |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 41/200 | 49/200 | +4.0 pts, CI [-0.5, +8.5] |
| Qwen2.5-7B 8-bit | 47/200 | 71/200 | +12.0 pts, CI [+6.5, +17.5] |
| Qwen3-4B | 49/200 | 76/200 | +13.5 pts, CI [+8.0, +19.0] |

This is not deployable as stated because it uses benchmark-provided Bangla and
English views. It should be framed as a diagnostic upper-bound signal and a
design target: if a system can generate or retrieve faithful alternate-script
views, agreement may be useful.

The reviewed-v5 interval remains clearly positive for Qwen2.5-7B 8-bit and
Qwen3-4B. Qwen2.5-3B retains a positive point estimate, but its interval
crosses zero.

Artifacts:

- `reports/cross_script_diagnostics_validation200_v5.md`
- `reports/deployable_consistency_mitigation_plan.md`
- `reports/figures/cross_script_recovery.svg`

## 8.6 Generated-View Preservation

Generated-view routing only works if generated views preserve the task. The
audits show this is not automatic.

Raw deterministic Banglish-to-Bangla packages failed preservation on all 36
dev50 BEnQA MCQ generated-Bengali rows because option labels were corrupted.
The historical protected-v1 files used by the first answer audits still fail
the tightened scientific-token gate on 9/36 and 10/36 rows. Reviewed-v5
protected-v2 structural masking was then answered by Qwen3 and Qwen2.5, but the
tightened formula-expression gate rejects 16/36 rows for both deterministic
generators. Formulaish-token protected-v3 now passes 0/36 hard gates, but its
dev-only answer gains remain weak: Qwen3-4B BNB improves 15/36 to 17/36 with a
wide CI crossing zero, while Qwen2.5-3B is flat to +1 item.

Historical protected-v1 generated-BN answer audits were model/generator-specific:

- Qwen3-4B: Banglish 15/36, protected BNB 17/36, protected phonetic 11/36.
- Qwen2.5-3B: Banglish 8/36, protected phonetic 14/36, protected BNB 7/36.

The raw Qwen3 generated-English route was weak: generated-English accuracy was
7/36 and the tightened preservation audit found 16/36 hard failures. A guarded
generated-English repair passes 0/36 hard gates by restoring source
option/answer lines and falling back to the source Banglish row when needed,
but 15/36 rows are source fallbacks. With protected-v3 generated-BN, guarded
agreement routing is still not route-ready: Qwen3 improves only from 15/36 to
16/36 on dev, while Qwen2.5 drops from 9/36 to 8/36.
The bottleneck analysis shows that strict answer agreement is also too sparse:
Qwen3 has 5 baseline-wrong rows recoverable by at least one generated view but
only 1 recovered by generated-BN/generated-EN agreement, and Qwen2.5 has 10
such rows with 0 recovered by agreement.
A simple deployable rule scan does not solve this. Qwen3's best guarded
answer-level rules reach 17/36, only +2 over Banglish; Qwen2.5's best reaches
13/36, but with 5 losses and no matching Qwen3 improvement. The only weakly
positive rule on both current guarded routes is generated-BN-only, which is
already too uncertain as a generated-BN-only effect.

A protected `fms-byte/banglish_to_bangla` MBART Kaggle dry run adds a useful
negative result. Under the tightened formula-expression gate it fails 15/36
rows, leaves genuine Latin residue on 7/36 rows, and has worse privileged
native-reference mean CER than deterministic protected phonetic generation
(0.1855 vs 0.0906). Formal preservation is therefore necessary but not
sufficient for lexical quality, and the gate itself must include formula-like
operators rather than only chemistry-style tokens.

Interpretation:

- Generated views need preservation gates before answer evaluation.
- Generator choice interacts with model choice.
- Gate-passing structure alone is not enough: the protected-v2 answer effects
  were at most +1 gate-eligible item on reviewed-v5 dev.
- Protected-v3 repairs formula preservation, and guarded generated-English
  repairs hard preservation, but the resulting agreement route is only
  +1 item for Qwen3 and -1 item for Qwen2.5.
- Strict generated-view agreement misses most generated-view oracle recoveries,
  so future work needs either better agreement or a stronger pre-registered
  routing signal.
- Looser answer-level rules can recover more dev items but add losses and are
  too model-specific for a held-out launch.
- Current cheap generated-view routes are diagnostics, not held-out
  mitigations.

Artifacts:

- `reports/generated_view_diagnostics_summary.md`
- `reports/generated_view_preservation_audit_v2.md`
- `reports/qwen3_4b_generated_bn_answer_audit_dev50.md`
- `reports/qwen25_3b_generated_bn_answer_audit_dev50.md`
- `reports/qwen3_4b_generated_view_agreement_route_dev.md`
- `reports/qwen3_4b_selftranslate_guarded_v5_generated_en_dev50_benqa_mcq_audit.md`
- `reports/qwen3_4b_guarded_generated_en_v5_dev50.md`
- `reports/qwen25_3b_guarded_generated_en_v5_dev50.md`
- `reports/qwen3_4b_pv3_bn_guarded_en_agreement_route_dev.md`
- `reports/qwen25_3b_pv3_bn_guarded_en_agreement_route_dev.md`
- `reports/generated_view_route_bottleneck_analysis.md`
- `reports/generated_view_routing_candidate_scan.md`
- `reports/qwen3_4b_generated_bn_v5_pv2_dev50.md`
- `reports/qwen25_3b_generated_bn_v5_pv2_dev50.md`
- `reports/qwen3_4b_generated_bn_v5_pv3_dev50.md`
- `reports/qwen25_3b_generated_bn_v5_pv3_dev50.md`
- `reports/phonetic_bangla_protected_v3_v5_generated_bn_dev50_benqa_mcq_audit.md`
- `reports/bnbphoneticparser_protected_v3_v5_generated_bn_dev50_benqa_mcq_audit.md`
- `results/tables/generated_bn_answer_audit_dev50.csv`
- `results/tables/generated_bn_candidate_preservation.csv`
- `results/tables/generated_bn_reference_similarity_dev50.csv`

## 8.7 External Normalization And English Pivot

External normalization and English-pivot self-translation were also tested in
smaller validation/MGSM probes. Under the current setup, they were weak or
harmful. Some outputs changed digits or otherwise altered key task content.

These results should not be interpreted as proof that external normalization is
bad. They show that normalization quality, domain fit, and preservation checks
are central. A stronger transliterator or translation model may still be a good
future mitigation, but it must pass the same preservation and dev/test gates.

Artifacts:

- `reports/mitigation_summary.md`
- `reports/mgsm_bn50_v1_to_v2_banglish_diff.md`
- `reports/qwen3_4b_mgsm_bn50_selftranslate_examples_reparsed.md`

## 8.8 Chapter Conclusion

The mitigation story is deliberately cautious. Simple prompts do not close the
Banglish gap. Self-normalization can help one model and hurt another. Routing
can recover signal, but exploratory rules must be locked before held-out claims.
Cross-script agreement is a strong diagnostic target, but deployable generated
views need strict preservation gates. The practical conclusion is that Banglish
robustness needs explicit script-aware evaluation and reliability checks, not
just bigger models or generic prompt wrappers.

---

<!-- Source: reports/chapter_9_limitations_draft.md -->

Updated: 2026-05-31

## 9.1 Chapter Goal

This chapter states what the thesis does not prove. The main result is strong
because it is controlled and paired, but the scope is still limited by dataset
construction, model coverage, mitigation maturity, and mechanism evidence.

## 9.2 Controlled Banglish Is Not All Natural Banglish

The current validation-200 Banglish slice is controlled and pipeline-generated,
then reviewed through v5. This is useful for isolating orthographic effects
because the same item and gold answer are preserved across scripts. However,
natural Banglish is more diverse. It can include spelling variation,
abbreviations, English code-mixing, slang, incomplete grammar, and
context-dependent phrasing.

The refreshed BanglaTLit comparison shows that real Romanized Bangla is
shorter, less number-heavy, sometimes script-mixed, and more spelling-variable
than the frozen validation-200 v5 clean Banglish slice. The v5 content-only
Banglish rows average 86.2 characters and contain digits in 54.5% of rows;
BanglaTLit val/test rows average about 56-57 characters and contain digits in
about 18% of rows. Therefore, the benchmark should be described as controlled
educational Banglish, not a full model of social-media Banglish.

A lexical-coverage audit sharpens this boundary. Using exact Latin-token
overlap, BanglaTLit covers only 36.8% of frozen-v5 content Banglish tokens on
average, with lower coverage for BEnQA than BanglaMATH. At the same time, the
highest-coverage all-200 quartile still shows reviewed Banglish below Bangla,
28/150 correct model-item slots versus 40/150. This means naturalness mismatch
is a real limitation, but it is not a complete explanation for the measured
script gap.

A per-model coverage sensitivity adds the same caution at the model level:
within every all-200 BanglaTLit coverage quartile, reviewed Banglish remains
below both Bangla and English for Qwen2.5-3B, Qwen2.5-7B, and Qwen3-4B. This is
not a causal lexical mechanism, but it weakens the simpler claim that only rare
or low-coverage Banglish vocabulary drives the result.

A spelling-variation sensitivity adds a related naturalness check. The
BanglaTLit alignment contributes 24,418 aligned token pairs and 299 Bangla
tokens with at least two repeated Latin variants. In the highest all-200
repeated-variant-exposure quartile, reviewed Banglish remains below Bangla and
English for every Qwen row. The lowest-exposure bucket is mixed for
Qwen2.5-3B, so this should be cited as descriptive robustness evidence rather
than as a monotonic spelling-variation mechanism.

The completed v5 human-review workflow reduces rule-based artifact risk through
exact session review, read-only packets, validation checks, and an audit log. It
does not turn the benchmark into a natural user corpus.

The review-label sensitivity check adds a useful boundary: the Banglish deficit
is visible in both unreviewed rows and reviewed non-bad rows for the three
thesis-facing Qwen baselines. This means the result is not solely an artifact
of rows that required manual Banglish edits, while still leaving natural-user
Banglish diversity as future work.

The review edit-distance sensitivity audit sharpens this point: even the 63
rows with no applied Banglish change retain the reviewed-Banglish-below-Bangla
and below-English direction for all three thesis-facing Qwen rows. Larger-edit
rows remain a small 19-item quality caveat rather than a separate statistical
claim.

The main denominator keeps all 200 rows and flags three source-quality
problems. A separate strict-197 sensitivity analysis excludes those rows:
reviewed Banglish remains below native Bangla for all three thesis-facing Qwen
rows with negative paired confidence intervals. This supports the main result
while keeping the denominator decision visible rather than silently dropping
rows.

The source-variant structural audit also separates primary-pair quality from
English-source caveats. Bangla versus reviewed Banglish has 0/200 structural
mismatches for option labels, digits, formula-like tokens, and answer
instructions. English comparisons have 39/200 diagnostic warnings, so English
should be used as privileged support and recoverability evidence rather than
as proof that every upstream English translation is structurally identical.
Separating those warning rows does not remove the diagnostic pattern: on the
161 English-structurally-clean items, reviewed Banglish remains below both
Bangla and English for all three Qwen rows. This supports the use of English
as caveated diagnostic evidence, not as a deployable or perfectly parallel
source.

## 9.3 Dataset Size And Composition

Validation-200 is intentionally small enough to support careful paired analysis,
manual review, and repeated model evaluation under Kaggle constraints. The
tradeoff is that subject and grade strata are small. Subject-level findings are
descriptive support, not standalone claims.

BanglaMATH is especially difficult for the current open models. It is useful as
a stress test, but the thesis should avoid fine-grained math conclusions until
stronger models or an easier math subset are evaluated.

## 9.4 Model Coverage

The main Banglish-below-Bangla result is strongest for competent Qwen baselines:
Qwen2.5-3B, Qwen2.5-7B 8-bit, and Qwen3-4B. Other compact models show related
but not identical behavior. Phi-3.5-mini and Qwen3-1.7B no-thinking show large
Banglish-vs-English gaps but do not show a reliable Banglish-below-Bangla
ordering.

Therefore, the thesis should not claim that every model always finds Banglish
harder than native Bangla. The correct claim is model-aware: controlled
Latin-script Banglish exposes a substantial weakness in the competent open Qwen
baselines and remains much weaker than English across several compact models.

Frontier API models remain an optional final external-validity audit. The
required post-v5 open-model reruns are complete, but a paid audit should still
start with the budgeted 10-item smoke rather than exploratory full runs.

## 9.5 Evaluation And Parsing

Answer-only evaluation depends on parsing. The project has reparsed and
rescored outputs after parser improvements, and all thesis-facing results should
use reparsed/rescored files. Still, answer extraction can be brittle,
especially for short-answer math and models that generate reasoning traces.

The frozen-v5 answer-format audit reduces this concern for the main claim:
Qwen2.5-3B has no format failures in the thesis-facing rows, Qwen2.5-7B's two
reviewed-Banglish format failures cannot explain its gap, and Qwen3 has more
BEnQA format failures in English and Bangla than in reviewed Banglish. This
does not make short-answer parsing perfect, but it shows that the release-facing
Banglish deficit is not primarily a parser-empty or MCQ-format artifact.
The BEnQA distractor-transition audit adds that recoverable reviewed-Banglish
MCQ misses are usually valid distractor choices, not invalid labels; this is
behavioral failure evidence rather than a causal mechanism claim.

Qwen3-family thinking behavior is a specific risk. Earlier no-thinking probes
showed that default thinking/truncation can break answer-only evaluation. Future
Qwen3-family runs must record thinking mode and output-token limits.

## 9.6 Mitigation Overfitting

Mitigation experiments are vulnerable to overfitting because many prompt,
normalization, and routing variants can be tried. The validation-200 v4
dev50/test150 split reduces this risk, but only if future choices are selected
on dev and evaluated unchanged on test.

Answer-signal routing is promising but exploratory. Generated-view routing is
also not solved. Raw generated-English quality is weak; guarded
generated-English repairs hard preservation but relies on source fallback for
15/36 rows. Generated-BN gains are model/generator-specific. The protected
FMS-byte dry run fails the tightened formula-expression gate and leaves Latin
residue. The repaired protected-v3 deterministic route passes preservation,
but guarded agreement routing is only +1 item for Qwen3 and -1 item for
Qwen2.5 on dev. A route-bottleneck audit shows that strict agreement misses
most baseline-wrong generated-view recoveries, so routing signal design is also
unresolved. A simple answer-level candidate scan finds looser rules that can
gain on one model but add losses and do not transfer cleanly. These results
should motivate future work rather than be presented as final deployable
mitigation.

## 9.7 Privileged Views

The cross-script oracle and Bangla+English agreement route use benchmark
provided alternate-script views. They are useful diagnostics because they show
recoverability, but they are not deployable accuracy. A real system would need
generated, retrieved, or user-provided alternate views and strict preservation
checks.

## 9.8 Mechanism Evidence

The thesis rules out token count alone as a sufficient explanation, but it does
not prove a causal internal mechanism. Tokenization, failure taxonomy, and
cross-script agreement provide behavioral and descriptive evidence. A causal
mechanistic claim would require representation probes or interventions.

## 9.9 Compute And Budget Constraints

Kaggle P100 constraints shaped model selection. Qwen3-8B was blocked by
bitsandbytes/P100 compatibility, and some 7B-class models were slow or weak in
pilot runs. Paid API use is budget-limited and intentionally deferred.

These constraints should be reported transparently. They explain model coverage
without weakening the paired evidence for the models that were successfully
evaluated.

## 9.10 Chapter Conclusion

The thesis makes a controlled, paired, model-aware claim. It does not claim to
solve natural Banglish, prove universal model behavior, or identify a causal
internal mechanism. Its contribution is to show that script choice is a
measurable robustness variable for Bangla LLM use and to provide the benchmark,
analysis, and release workflow needed to study it rigorously.

---

<!-- Source: reports/chapter_10_conclusion_draft.md -->

Updated: 2026-05-30

## 10.1 Summary

This thesis studies whether script choice changes how large language models
handle Bangla content. The answer is yes for the competent open Qwen baselines
tested so far. On a paired validation-200 slice, the same educational QA and
math items become substantially harder when written in reviewed Latin-script
Banglish than when written in native Bangla or English.

The result is not explained by token count alone. Banglish is token-cheaper than
native Bangla for the Qwen tokenizers, yet accuracy is lower. It is also not
just an impossible-item effect: many Banglish misses are answered correctly by
the same model under Bangla or English. Cross-script agreement recovers
substantial accuracy in the reviewed-v5 diagnostic refresh, though deployable
routing still requires generated-view preservation and held-out validation.

## 10.2 Main Contributions

The thesis contributes:

1. A controlled Bangla/Banglish/English evaluation protocol for Bangla
   educational QA and math.
2. Paired validation-200 evidence of a substantial Banglish deficit in competent
   Qwen baselines.
3. Robustness checks showing the result survives targeted romanizer cleanup,
   broader automatic suggestions, and deterministic noisy-Banglish stress.
4. Tokenization and failure analysis showing the deficit is not reducible to
   token count or impossible items.
5. A mitigation study showing that prompt wrappers and self-normalization are
   brittle, while cross-script agreement is a promising diagnostic signal.
6. A generated-view audit showing preservation gates are mandatory before
   deployable routing.
7. A completed v5 human-review, preregistration, reproducibility, and post-v5
   rerun workflow for thesis-grade release.

## 10.3 Practical Lesson

Banglish should not be treated as ordinary English-like Latin text. It is
Bengali-language content in a different script, and that script change can alter
model behavior. Systems serving Bangla users should evaluate native Bangla,
Romanized Bangla, and English separately instead of assuming success in one view
transfers to another.

## 10.4 Future Work

Future work should extend four directions.

First, add a small natural-Banglish layer that complements the controlled
reviewed benchmark without weakening paired comparability.

Second, evaluate stronger frontier APIs with the cost guardrails and 10-item
smoke subset now that v5 and the required open-model reruns are locked.

Third, test stronger deployable normalization and generated-view routing with
strict preservation gates and dev/test discipline.

Fourth, add a small representation-level analysis only if it can be scoped
tightly around the existing failure taxonomy.

## 10.5 Final Statement

Banglish robustness is not solved by treating Latin-script Bangla as English
text or by wrapping the same model in a simple normalization prompt. Script
choice changes model behavior. Robust Bangla language technology needs explicit
evaluation and mitigation for Latin-script Banglish.
