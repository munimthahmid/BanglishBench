# Chapter 7 Tokenization And Mechanism Draft

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
