# Chapter 9 Limitations Draft

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
