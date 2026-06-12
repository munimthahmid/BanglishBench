# Final API Audit Cost Plan

Updated: 2026-06-05

## Purpose

Paid frontier APIs should be used only after v5 is frozen and open-model thesis
tables are stable. The role is external validity, not exploration.

Official pricing checked on 2026-06-05:

- OpenAI API pricing: https://developers.openai.com/api/docs/pricing
- OpenAI `gpt-5.4`: https://developers.openai.com/api/docs/models/gpt-5.4
- OpenAI `gpt-5.5`: https://developers.openai.com/api/docs/models/gpt-5.5
- OpenAI `gpt-5.5-pro`: https://developers.openai.com/api/docs/models/gpt-5.5-pro
- Gemini API pricing: https://ai.google.dev/gemini-api/docs/pricing
- Anthropic pricing: https://docs.anthropic.com/en/docs/about-claude/pricing
- Anthropic Claude Sonnet 4.6: https://www.anthropic.com/claude/sonnet
- DeepSeek models/pricing: https://api-docs.deepseek.com/quick_start/pricing
- DeepSeek thinking-mode control:
  https://api-docs.deepseek.com/guides/thinking_mode
- Groq Llama 3.3 70B model/pricing:
  https://console.groq.com/docs/model/llama-3.3-70b-versatile
- Groq OpenAI-compatible API:
  https://console.groq.com/docs/api-reference

Re-check provider pages before spending money; API prices and model names change.

## Candidate Paid Models

| Provider | Model tier | Current standard pricing noted | Use |
| --- | --- | --- | --- |
| OpenAI | `gpt-5.4` | $2.50 / 1M input, $15.00 / 1M output | Strong but cheaper than top pro tier. |
| OpenAI | `gpt-5.5` | $5.00 / 1M input, $30.00 / 1M output | Stronger late-stage audit if budget allows. |
| OpenAI | `gpt-5.5-pro` or `gpt-5.4-pro` | $30.00 / 1M input, $180.00 / 1M output | Avoid for full benchmark under a $20 budget. |
| Gemini | `gemini-3.1-pro-preview` | $2.00 / 1M input, $12.00 / 1M output for prompts <= 200k tokens | Current stronger Google smoke candidate, but preview status weakens reproducibility. |
| Gemini | `gemini-2.5-pro` | $1.25 / 1M input, $10.00 / 1M output for prompts <= 200k tokens | Good cost/performance candidate. |
| Gemini | `gemini-3.5-flash` | $1.50 / 1M input, $9.00 / 1M output | Current strong low-cost Google alternative, not a replacement for the Pro audit. |
| Gemini | `gemini-2.5-flash` | $0.30 / 1M input, $2.50 / 1M output | Stable cheap sanity-check candidate, not frontier. |
| Anthropic | `claude-sonnet-4-6` | Sonnet-tier pricing listed as $3.00 / 1M input, $15.00 / 1M output; re-check before run | High-value cross-family frontier replication. Use validation-200 v5, not full851 by default. |
| DeepSeek | `deepseek-v4-flash` non-thinking | $0.14 / 1M input cache miss, $0.28 / 1M output | Cheap cross-family row. Good candidate for validation-200 and, if clean, one additional full851 silver-scale run. |
| Groq | `llama-3.3-70b-versatile` | $0.59 / 1M input, $0.79 / 1M output | Hosted-open Llama row. Use validation-200 only; current request limits make full851 inappropriate. |

Output prices include reasoning/thinking tokens where the provider bills them.
Keep prompts answer-only and disable optional tools/search/grounding.

## Cost Scenarios

Assume validation-200 full triad:

- 200 items
- 3 variants: Bangla, Banglish, English
- 600 calls per model

Actual current prompt-budget heuristic on frozen validation-200 v5:

- `reports/validation200_v5_prompt_budget.md`
- `reports/api_audit_smoke_10_v5_prompt_budget.md`
- Full triad prompt total: about 36.5k approximate input tokens under
  `ceil(characters / 4)`.
- 10-item smoke triad prompt total: about 1.7k approximate input tokens.

The table below remains deliberately conservative because provider tokenizers
and billed reasoning/output tokens can differ from this simple heuristic.

| Scenario | Input tokens / call | Output tokens / call | Tokens / model | Approx cost: GPT-5.5 | Approx cost: Claude Sonnet 4.6 | Approx cost: Gemini 3.1 Pro Preview | Approx cost: DeepSeek V4 Flash |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| Tight answer-only | 500 | 20 | 0.30M in, 0.012M out | $1.86 | $1.08 | $0.74 | $0.05 |
| Conservative | 1,000 | 128 | 0.60M in, 0.077M out | $5.30 | $2.96 | $2.12 | $0.11 |
| Very conservative | 1,500 | 256 | 0.90M in, 0.154M out | $9.11 | $5.01 | $3.65 | $0.17 |

Controlled frontier-panel estimate:

- The completed five-model validation-200 v5 panel remains below the old $20
  guardrail across the added Claude, DeepSeek, and Groq rows.
- Claude Sonnet 4.6 is affordable for validation-200 but verbose under
  answer-only prompting; do not promote it to full851 by default.
- Do not run GPT-5.5-pro, Opus-tier models, or additional prestige rows unless
  a reviewer-risk question specifically requires them.

## Recommended Paid Audit

After v5 and open-model tables are locked:

1. Keep the completed Gemini 3.5 Flash, GPT-5.5 low, Claude Sonnet 4.6,
   DeepSeek V4 Flash, and Groq Llama 3.3 70B validation-200 rows as the
   controlled frontier panel.
2. Use the completed DeepSeek V4 Flash full851 run as the only API
   silver-scale replication.
3. Do not run Qwen API rows; the thesis already has compact/local Qwen
   evidence.
4. Do not run full851 for every frontier model. DeepSeek V4 Flash already
   answers the cheap, non-Qwen scale-replication question.

Current v5 smoke subset for dry-run/token estimation:

- `data/slices/api_audit_smoke_10_v5.jsonl`
- `data/api_audit/validation200_v5_requests.jsonl`
- `reports/api_audit_smoke_subset_v5.md`
- `data/api_audit/api_audit_smoke_10_v5_requests.jsonl`
- `reports/validation200_v5_api_audit_prompt_manifest.md`
- `reports/api_audit_prompt_manifest_v5.md`
- `reports/api_audit_manifest_integrity_check.md`
- `reports/api_audit_import_roundtrip_check.md`
- `reports/paid_api_audit_execution_runbook.md`
- `reports/frontier_api_panel_validation200_v5.md`
- `reports/claude_sonnet_4_6_validation200_v5_cap1024_results.md`
- `reports/deepseek_v4_flash_benqa_ext_full851.md`

No-spend integrity status:

- `scripts/check_api_audit_manifest.py` validates 10 smoke items, 30 requests,
  per-item Bangla/Banglish/English coverage, unique request ids, absence of
  gold/source fields in request rows, prompt contract, output-token cap, and
  budget-token consistency.
- Latest result: 18 checks, 0 issues; total approximate prompt tokens 1,736.
- `scripts/check_api_audit_import_roundtrip.py` synthesizes temporary
  parser-friendly mock responses and verifies the response importer with
  `--require-complete`.
- Latest result: 16 checks, 0 issues; 30/30 mock responses imported, 30/30
  parsed correct, and reported input/output token usage preserved.

## Budget Guardrails

- Hard cap: $20 unless explicitly raised.
- Start with a 10-item triad smoke per provider and inspect actual token usage.
- Stop if actual average output tokens exceed 256 per call.
- Never enable web/search/grounding/tool use for the benchmark audit.
- Log provider, model id, pricing page date, input/output tokens, and dollar
  cost in `results/experiment_log.md`.
- For DeepSeek V4 Flash, use non-thinking mode first:
  `thinking={"type":"disabled"}`. Thinking mode can be a later protocol-control
  experiment, not the default benchmark row.
