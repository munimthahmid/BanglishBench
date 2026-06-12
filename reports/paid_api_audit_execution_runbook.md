# Paid API Audit Execution Runbook

Updated: 2026-06-05

## Purpose

This runbook defines the no-surprises path for the optional paid external-
validity audit. It does not authorize spending and does not contain provider
credentials.

## Current State

- Frozen slice: `data/slices/validation_200_v5.jsonl`
- Smoke subset: `data/slices/api_audit_smoke_10_v5.jsonl`
- Smoke requests: `data/api_audit/api_audit_smoke_10_v5_requests.jsonl`
- Prompt manifest report: `reports/api_audit_prompt_manifest_v5.md`
- Full validation-200 request manifest:
  `data/api_audit/validation200_v5_requests.jsonl`
- Full validation-200 prompt manifest report:
  `reports/validation200_v5_api_audit_prompt_manifest.md`
- Manifest integrity report: `reports/api_audit_manifest_integrity_check.md`
- Import round-trip report: `reports/api_audit_import_roundtrip_check.md`
- Budget plan: `reports/final_api_audit_cost_plan.md`

The smoke manifest contains 30 provider-neutral requests: 10 items across
Bangla, reviewed Banglish, and English. Request rows intentionally exclude gold
answers. The importer has a no-spend round-trip check that verifies complete
mock-response import, parser output, source-item gold joins, variant counts,
and token-usage propagation before any paid call is made.

Current controlled frontier panel:

- Completed validation-200 v5 rows: Gemini 3.5 Flash, GPT-5.5 low,
  Claude Sonnet 4.6, DeepSeek V4 Flash non-thinking, and Groq Llama 3.3 70B.
- Qwen API rows are intentionally out of scope; the thesis already has
  compact/local Qwen evidence.
- Full851 extension is not automatic for all API models. DeepSeek V4 Flash
  full851 is complete as the only authorized API full851 follow-up because it
  is cheap, validation-clean, and tests non-Qwen scale replication.

## Regenerate The No-Spend Manifest

```bash
python3 scripts/build_api_audit_smoke_subset.py
python3 scripts/build_api_audit_prompt_manifest.py
python3 scripts/estimate_prompt_budget.py \
  --input data/slices/api_audit_smoke_10_v5.jsonl \
  --output results/analysis/api_audit_smoke_10_v5_prompt_budget_summary.csv \
  --report reports/api_audit_smoke_10_v5_prompt_budget.md
python3 scripts/check_api_audit_manifest.py
python3 scripts/check_api_audit_import_roundtrip.py
```

## Provider Sender Contract

A provider-specific sender must read the request JSONL and send only:

- `system_message`
- `prompt`
- `max_output_tokens`

Use temperature 0 or the closest deterministic setting. Disable tools, search,
grounding, and optional browsing. Record one response JSONL row per request:

```json
{"request_id":"...","raw_output":"...","provider_response_id":"...","usage_input_tokens":0,"usage_output_tokens":0,"seconds":0.0}
```

Do not place API keys in command-line arguments, reports, notebooks, or JSONL
artifacts.

## Authorized Smoke Commands

Claude Sonnet 4.6:

```bash
python3 scripts/run_anthropic_api_audit.py \
  --requests data/api_audit/api_audit_smoke_10_v5_requests.jsonl \
  --output results/api_audit/claude_sonnet_4_6_smoke10_v5_raw.jsonl \
  --model claude-sonnet-4-6 \
  --write-each
```

DeepSeek V4 Flash, non-thinking:

```bash
python3 scripts/run_openai_compatible_chat_api_audit.py \
  --requests data/api_audit/api_audit_smoke_10_v5_requests.jsonl \
  --output results/api_audit/deepseek_v4_flash_smoke10_v5_raw.jsonl \
  --model deepseek-v4-flash \
  --base-url https://api.deepseek.com \
  --thinking disabled \
  --write-each
```

Groq Llama 3.3 70B:

```bash
python3 scripts/run_openai_compatible_chat_api_audit.py \
  --requests data/api_audit/api_audit_smoke_10_v5_requests.jsonl \
  --output results/api_audit/groq_llama33_70b_smoke10_v5_raw.jsonl \
  --model llama-3.3-70b-versatile \
  --base-url https://api.groq.com/openai/v1 \
  --key-env GROQ_API_KEY \
  --thinking omit \
  --write-each
```

The DeepSeek non-thinking setting is deliberate. The official API defaults to
thinking mode, but this benchmark row should first match the answer-only,
tool-free protocol used for the existing frontier audits.

## Import And Validate Responses

```bash
python3 scripts/import_api_audit_responses.py \
  --responses path/to/provider_smoke_responses.jsonl \
  --provider provider_name \
  --model exact_model_id \
  --output path/to/api_audit_provider_smoke_v5.jsonl \
  --report path/to/api_audit_provider_smoke_v5.md \
  --require-complete
```

The importer reuses the open-model parser and emits the same core fields:
`raw_output`, `parsed`, `gold`, and `correct`.

Analyze imported rows with the generic API analyzer:

```bash
python3 scripts/analyze_api_audit_results.py \
  --imported path/to/provider_imported.jsonl \
  --raw path/to/provider_raw.jsonl \
  --model-label "Provider model label" \
  --items-output path/to/provider_items.csv \
  --summary-output path/to/provider_summary.csv \
  --paired-output path/to/provider_paired_gaps.csv \
  --recovery-output path/to/provider_recoverability_items.csv \
  --comparison-output path/to/provider_gemini_comparison.csv \
  --report path/to/provider_results.md \
  --cost-label "provider pricing checked YYYY-MM-DD" \
  --input-cost-per-mtok 0 \
  --output-cost-per-mtok 0
```

Fill the provider-specific cost rates before writing final reports.

## Promotion Gate

Do not launch a full validation-200 triad until:

1. The 30-request smoke is complete for the provider.
2. Parsed-empty responses and formatting failures are inspected.
3. Actual token usage and cost are recorded.
4. Average output length stays under the guardrail in
   `reports/final_api_audit_cost_plan.md`.
5. The exact provider model id and pricing-page check date are logged in
   `results/experiment_log.md`.

## Full-Triad Manifest

After the smoke gate passes:

```bash
python3 scripts/build_api_audit_prompt_manifest.py \
  --input data/slices/validation_200_v5.jsonl \
  --output data/api_audit/validation200_v5_requests.jsonl \
  --report reports/validation200_v5_api_audit_prompt_manifest.md
```

This produces 600 provider-neutral requests without making paid calls.

## Authorized Full-Triad Commands

Only run these after the smoke gate passes.

Claude Sonnet 4.6:

```bash
python3 scripts/run_anthropic_api_audit.py \
  --requests data/api_audit/validation200_v5_requests.jsonl \
  --output results/api_audit/claude_sonnet_4_6_validation200_v5_cap1024_raw.jsonl \
  --model claude-sonnet-4-6 \
  --max-output-tokens-override 1024 \
  --write-each \
  --resume
```

DeepSeek V4 Flash, non-thinking:

```bash
python3 scripts/run_openai_compatible_chat_api_audit.py \
  --requests data/api_audit/validation200_v5_requests.jsonl \
  --output results/api_audit/deepseek_v4_flash_validation200_v5_raw.jsonl \
  --model deepseek-v4-flash \
  --base-url https://api.deepseek.com \
  --thinking disabled \
  --write-each \
  --resume
```

Groq Llama 3.3 70B:

```bash
python3 scripts/run_openai_compatible_chat_api_audit.py \
  --requests data/api_audit/validation200_v5_requests.jsonl \
  --output results/api_audit/groq_llama33_70b_validation200_v5_raw.jsonl \
  --model llama-3.3-70b-versatile \
  --base-url https://api.groq.com/openai/v1 \
  --key-env GROQ_API_KEY \
  --thinking omit \
  --write-each \
  --resume
```

Do not run Groq full851 under the current limits; the 2,553-request extension
exceeds the visible daily request budget for `llama-3.3-70b-versatile`.

## Completed API Full851 Command

DeepSeek V4 Flash was the only authorized API full851 scale follow-up:

```bash
python3 scripts/run_openai_compatible_chat_api_audit.py \
  --requests data/api_audit/deepseek_v4_flash_benqa_ext_full851_requests.jsonl \
  --output results/api_audit/deepseek_v4_flash_benqa_ext_full851_raw.jsonl \
  --model deepseek-v4-flash \
  --base-url https://api.deepseek.com \
  --thinking disabled \
  --write-each \
  --resume \
  --progress-every 250
```

Do not run Claude, Gemini, GPT, or Groq full851 by default. The current thesis
already has one no-paid-compute full851 scale result from Qwen2.5-3B and one
cheap non-Qwen API full851 replication from DeepSeek V4 Flash.
