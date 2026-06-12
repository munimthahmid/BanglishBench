# Qwen3-4B Generated-View Agreement Route: Dev

Updated: 2026-06-11

## Inputs

- Generated-BN answer audit: `results/runs/qwen3_4b_generated_bn_answer_audit_dev50/results/runs/qwen3_4b_generated_bn_answer_audit_dev50.jsonl`
- Generated-EN self-translate audit: `results/runs/qwen3_4b_generated_en_selftranslate_dev50/results/runs/qwen3_4b_generated_en_selftranslate_dev50.jsonl`
- Item route CSV: `results/analysis/qwen3_4b_generated_view_agreement_route_dev_items.csv`
- Summary CSV: `results/analysis/qwen3_4b_generated_view_agreement_route_dev_summary.csv`

## Result

- n: 36
- Banglish: 15/36
- Historical protected-v1 BNB generated-BN: 17/36
- Generated English self-translate: 7/36
- Agreement routed: 16/36
- Routed minus Banglish: 1
- Routed items: 1
- Fallback due generated-EN hard gate: 16
- Fallback Banglish items: 19

## Routed Items

- `benqa_8th-Science_0153` gold=C banglish=D bn=C en=C routed=C correct=True

## Decision Rule

This is a dev-only diagnostic using generated-BN plus generated-EN.
The generated-BN input is historical protected-v1 and fails the tightened scientific-token gate; it is not route-ready evidence.
Do not launch test150 unless the generation method, preservation
gates, and routing rule are frozen in advance.
