# Qwen2.5-3B Protected-v3 BN + Guarded-EN Agreement Route: Dev

Updated: 2026-06-11

## Inputs

- Generated-BN answer audit: `results/runs/qwen25_3b_generated_bn_v5_pv3_dev50/results/runs/qwen25_3b_generated_bn_v5_pv3_dev50.jsonl`
- Generated-EN self-translate audit: `results/runs/qwen25_3b_guarded_generated_en_v5_dev50/results/runs/qwen25_3b_guarded_generated_en_v5_dev50.jsonl`
- Item route CSV: `results/analysis/qwen25_3b_pv3_bn_guarded_en_agreement_route_dev_items.csv`
- Summary CSV: `results/analysis/qwen25_3b_pv3_bn_guarded_en_agreement_route_dev_summary.csv`

## Result

- n: 36
- Banglish: 9/36
- Protected-v3 phonetic generated-BN: 10/36
- Guarded generated-English: 11/36
- Agreement routed: 8/36
- Routed minus Banglish: -1
- Routed items: 1
- Fallback due generated-EN hard gate: 0
- Fallback Banglish items: 35

## Routed Items

- `benqa_12th-Physics-I_0106` gold=D banglish=D bn=C en=C routed=C correct=False

## Decision Rule

This is a dev-only diagnostic using generated-BN plus generated-EN.
This route uses reviewed-v5 protected-v3 generated-BN plus guarded generated-English. It is negative on dev and should not be launched on test150.
Do not launch test150 unless the generation method, preservation
gates, and routing rule are frozen in advance.
