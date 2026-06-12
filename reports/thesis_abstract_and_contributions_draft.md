# Thesis Abstract and Contributions Draft

Updated: 2026-06-05

## Draft Abstract

Bangla speakers frequently write Bengali content in Latin script, often called
Banglish. Recent Bengali benchmarks increasingly cover knowledge, education,
culture, inference, and social interaction, but they rarely isolate script
choice while holding the underlying task and answer fixed. This thesis studies
whether orthography itself changes large language model behavior. We construct
controlled Bangla, clean Banglish, noisy Banglish, and English variants of
curriculum-style QA and math items drawn from BEnQA, BanglaMATH, and MGSM, and
evaluate compact open instruction models under a paired item-level protocol.

On a 200-item validation slice, competent Qwen models show a consistent
reviewed-Banglish deficit: Qwen2.5-3B scores 54/200 in Bangla but 41/200 in
Banglish, Qwen2.5-7B scores 65/200 vs 47/200, and Qwen3-4B scores 80/200 vs
49/200. The all-200 paired intervals remain negative for Qwen2.5-7B and
Qwen3-4B; the Qwen2.5-3B interval reaches zero, while its historical and
strict-197 checks remain negative. The gap is not explained by token count
alone, since Banglish is token-cheaper than native Bangla for the Qwen
tokenizers. Cross-script oracle and agreement analyses show that many Banglish
failures are recoverable under another script view in the reviewed-v5 refresh,
indicating that the items are often not inherently impossible.

A frozen v5 review of 140 queued Banglish rows changes the clean-Banglish
scores only slightly: Qwen2.5-3B moves from 39/200 to 41/200, Qwen3-4B from
47/200 to 49/200, and Qwen2.5-7B 8-bit from 48/200 to 47/200 relative to v4.
Reviewed cleanup improves benchmark quality without removing the
script-conditioned weakness.

A separately reported strict-197 sensitivity analysis excludes the three
flagged source-quality rows and preserves negative reviewed-Banglish-vs-Bangla
confidence intervals for all three thesis-facing Qwen rows.

The benchmark is strengthened by two externality checks. First, a natural
code-mixed BnSentMix sentiment layer shows that Bengali-English mixed-script
inputs remain difficult and that model errors are complementary rather than
uniform: the best single model reaches 99/200, while a diagnostic any-model
oracle reaches 154/200. Second, a BEnQA-only scale extension is now
human-reviewed: from 1,000 reviewed rows, 974 accepted/edited rows form a
gold/pass evaluation set. Six completed model rows on this 974-item set
preserve paired reviewed-Banglish deficits against Bangla: Qwen2.5-3B,
Groq Llama 3.3 70B, Gemini 3.5 Flash, GPT-5.5 none, Claude Sonnet 4.6, and
DeepSeek V4 Flash all score reviewed Banglish below native Bangla.

Frontier-model audits clarify the boundary. A five-model validation-200 v5 API
panel covers Gemini 3.5 Flash, GPT-5.5 low, Claude Sonnet 4.6, DeepSeek V4
Flash, and Groq-hosted Llama 3.3 70B. GPT-5.5 low nearly collapses the
mixed-task validation-200 gap under secondary scoring, but the new 974-row
BEnQA scale run shows that this does not erase the larger BEnQA robustness
problem: GPT-5.5 none scores 820/974 Bangla, 699/974 reviewed Banglish, and
825/974 English, with a paired reviewed-Banglish deficit of -12.42 points
against Bangla. Thus the problem is not simply "models are bad at Banglish"; it
is that script choice changes reliability, parsing, and cost even when strong
models recover much of the semantic answer.

Mitigation is model-dependent. Simple Banglish-aware prompting does not close
the gap. Same-model self-normalization helps Qwen2.5-3B, is flat for Qwen2.5-7B
after held-out testing, and hurts Qwen3-4B. A privileged Bangla+English
agreement route recovers substantial accuracy, but deployable generated-view
routing requires strict preservation checks; cheap generated views currently
remain too unstable for a held-out mitigation claim. Overall, the thesis shows
that Latin-script Banglish is an undermeasured orthographic robustness challenge
for Bangla LLM use and that reliable mitigation requires explicit script-aware
evaluation, not just larger models or prompt wrappers.

## Current Contributions

1. A controlled Bangla/Banglish/English evaluation protocol for Bangla
   curriculum QA and math, preserving item ids and gold answers across scripts.
2. Validation-200 evidence that competent Qwen models are substantially worse
   on clean Latin-script Banglish than on native Bengali script.
3. Robustness checks showing that the result survives targeted Banglish cleanup,
   auto-suggested spelling cleanup, and deterministic noisy-Banglish variants.
4. Tokenization and failure-pattern evidence showing that Banglish failures are
   not reducible to longer token sequences or impossible items.
5. Mitigation evidence showing that self-normalization is brittle and
   model-dependent, with held-out dev/test discipline preventing overclaiming.
6. Cross-script oracle and answer-agreement analyses motivating future
   generated-view consistency routing.
7. Generated-view preservation and answer-audit evidence showing why deployable
   consistency routing needs structural gates before GPU/API evaluation.
8. A completed v5 human-review queue, impact-ordered review workflow, and
   post-v5 rerun protocol supporting a thesis-grade benchmark release.
9. A transparent flagged-bad denominator sensitivity showing that the main
   all-200 policy and a separate strict-197 view support the same conclusion.
10. A five-model frontier API panel showing that stronger models reduce the
    mixed-task validation gap unevenly, plus a 974-row human-gold BEnQA scale
    panel showing that the reviewed-Banglish deficit persists across six model
    rows including GPT-5.5 none.
11. A natural code-mixed BnSentMix external layer showing ecological-validity
    evidence and cross-model error complementarity.
12. A two-tier dataset contribution: validation-200 v5 as the mixed-task
    controlled core plus a 974-row human-reviewed BEnQA gold/pass scale layer
    whose completed model rows all preserve negative paired reviewed-Banglish
    gaps against Bangla.

## Claims To Keep Out Of The Abstract For Now

- Do not claim the current Banglish slice is fully natural human Banglish.
- Do not claim Banglish is universally harder than Bangla for every model.
- Do not claim cross-script agreement is deployable accuracy until generated
  alternate-script views are tested.
- Do not claim self-normalization is a general solution.
- Do not claim Bengali lacks benchmarks; the sharper claim is that controlled
  Bangla/Banglish/English task-equivalence is missing.
- Do not claim cheap generated views solve the problem; current evidence is
  negative/diagnostic.
- Do not call the older AI-triaged BEnQA pass subset human-reviewed; it
  remains historical support behind the current reviewed panel.
- Do not claim the 974-row BEnQA scale result generalizes to all model
  families; the current scale evidence covers the six completed rows in the
  human-gold panel.
