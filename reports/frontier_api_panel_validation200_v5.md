# Frontier API Panel Validation-200 v5

Updated: 2026-06-05

## Purpose

This report puts the completed paid/hosted frontier API audits on one
frozen validation-200 v5 protocol. It is the main cross-family table for
claim-boundary writing, not a leaderboard.

- Machine-readable panel CSV: `results/analysis/frontier_api_panel_validation200_v5.csv`
- Scoring: strict parser plus secondary parser/unit sensitivity.
- Prompting: provider-neutral answer-only manifest.
- Claude Sonnet 4.6 uses the same 1024 output-token cap as the GPT-5.5
  validation-200 audit.

## Strict Accuracy And Gaps

| Model | Bangla | Reviewed Banglish | English | BG-BN | BG-EN | MAX_TOKENS | Cost |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Gemini 3.5 Flash | 163/200 (81.5%) | 136/200 (68.0%) | 144/200 (72.0%) | -13.5 pts | -4.0 pts | 10 | $0.4167 |
| GPT-5.5 low | 172/200 (86.0%) | 169/200 (84.5%) | 154/200 (77.0%) | -1.5 pts | +7.5 pts | 0 | $2.0774 |
| Claude Sonnet 4.6 | 162/200 (81.0%) | 130/200 (65.0%) | 153/200 (76.5%) | -16.0 pts | -11.5 pts | 2 | $0.9826 |
| DeepSeek V4 Flash | 143/200 (71.5%) | 82/200 (41.0%) | 132/200 (66.0%) | -30.5 pts | -25.0 pts | 11 | $0.0089 |
| Groq Llama 3.3 70B | 90/200 (45.0%) | 48/200 (24.0%) | 102/200 (51.0%) | -21.0 pts | -27.0 pts | 24 | $0.0579 |

## Secondary Accuracy And Gaps

| Model | Bangla | Reviewed Banglish | English | BG-BN | BG-EN |
| --- | ---: | ---: | ---: | ---: | ---: |
| Gemini 3.5 Flash | 170/200 (85.0%) | 161/200 (80.5%) | 165/200 (82.5%) | -4.5 pts | -2.0 pts |
| GPT-5.5 low | 173/200 (86.5%) | 174/200 (87.0%) | 168/200 (84.0%) | +0.5 pts | +3.0 pts |
| Claude Sonnet 4.6 | 167/200 (83.5%) | 133/200 (66.5%) | 166/200 (83.0%) | -17.0 pts | -16.5 pts |
| DeepSeek V4 Flash | 152/200 (76.0%) | 96/200 (48.0%) | 148/200 (74.0%) | -28.0 pts | -26.0 pts |
| Groq Llama 3.3 70B | 92/200 (46.0%) | 56/200 (28.0%) | 111/200 (55.5%) | -18.0 pts | -27.5 pts |

## Interpretation

- GPT-5.5 low is the strongest boundary case: the reviewed-Banglish
  population gap nearly collapses under secondary scoring.
- Gemini 3.5 Flash remains strong but still has a strict
  reviewed-Banglish deficit.
- Claude Sonnet 4.6 is strong in absolute accuracy, but still has a
  reviewed-Banglish deficit and is visibly less format-disciplined under
  answer-only prompts.
- DeepSeek V4 Flash and Groq-hosted Llama 3.3 70B show that the frontier
  story is not monotonic: strong/hosted models can still have large
  reviewed-Banglish deficits under the same prompt/parser protocol.
- Groq Llama 3.3 70B is useful as a hosted-open reference, but it is not a
  frontier-closed model and should not be over-weighted against GPT/Gemini.

## Cost And Scope Boundary

Costs are approximate text-token estimates from provider pricing checked on
2026-06-05 and reported API token usage. They exclude account-level free
credits, taxes, and any provider-specific billing nuances.

Do not run full851 across every API model. DeepSeek V4 Flash is the only
authorized full851 follow-up because it is cheap, validation-clean, and
answers a scale question for a non-Qwen family. Groq is blocked from full851
by daily request limits; Claude is too expensive and too verbose to justify
a silver full851 run unless the thesis later needs a Claude-specific scale
claim.

## Source Reports

- Gemini 3.5 Flash: `reports/gemini_3_5_flash_validation200_v5_results.md`
- GPT-5.5 low: `reports/openai_gpt55_low_validation200_v5_cap1024_results.md`
- Claude Sonnet 4.6: `reports/claude_sonnet_4_6_validation200_v5_cap1024_results.md`
- DeepSeek V4 Flash: `reports/deepseek_v4_flash_validation200_v5_results.md`
- Groq Llama 3.3 70B: `reports/groq_llama33_70b_validation200_v5_results.md`
