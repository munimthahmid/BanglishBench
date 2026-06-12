# GPT-5.5 Cap-256 Probe

Updated: 2026-06-04

This was an aborted preliminary run of the same 60-item diagnostic slice using
`reasoning.effort=low` and a 256 output-token cap.

- Raw partial responses: `results/api_audit/openai_gpt55_low_diagnostic_60_v5_cap256_partial_raw.jsonl`
- Completed before stop: 70/180 requests
- Finish reasons: STOP=66, MAX_TOKENS=4
- No-visible-text failures: 4
- Reported input tokens: 5370
- Reported output tokens: 5323
- Reported reasoning tokens: 4720

Reason for stopping: the max-token/no-text failures showed that a 256-token cap
can be too low for GPT-5.5 low-reasoning calls even when the requested visible
answer is very short. The corrected diagnostic therefore uses the same low
reasoning setting with a 1024 output-token cap.
