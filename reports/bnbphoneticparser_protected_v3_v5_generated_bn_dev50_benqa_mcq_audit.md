# Generated-View Output Audit

Updated: 2026-06-11

## Inputs

- Prompt set: `data/generated_views/validation200_v5_dev50_benqa_mcq_generation_prompts.jsonl`
- Generator outputs: `results/generated_views/bnbphoneticparser_protected_v3_v5_dev50_benqa_mcq_generated_bn.jsonl`
- Item audit CSV: `results/analysis/bnbphoneticparser_protected_v3_v5_dev50_benqa_mcq_generated_bn_audit_items.csv`
- Summary CSV: `results/analysis/bnbphoneticparser_protected_v3_v5_dev50_benqa_mcq_generated_bn_audit_summary.csv`

## Counts

- Expected prompt rows: 36
- Missing outputs: 0
- Extra output keys: 0
- Hard-fail rows: 0
- Warning rows: 0

| Dataset | Target view | n | Hard fail | Warning | Option fails | Digit fails | Formula fails | Extra answer markers | Target-script issues | Latin-fragment warnings |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| benqa | generated_bn | 36 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Routing Rule

Generated views with `hard_fail=True` must be excluded from
agreement routing. Line-count warnings require inspection but are
not automatically blocking if options, digits, formulas, target
script, and answer-marker checks pass. Generated-BN Latin-fragment
warnings also require inspection because formal preservation does
not prove lexical quality.
