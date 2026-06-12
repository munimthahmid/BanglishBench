# Chapter 10 Conclusion Draft

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
