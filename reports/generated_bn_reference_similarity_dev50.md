# Generated-BN Reference Similarity: Dev50 BEnQA MCQ

Updated: 2026-06-11

## Scope

This report compares generated Bengali views with benchmark-provided
native-Bangla references on the locked dev50 BEnQA MCQ subset. It is a
privileged dev-only generator-selection diagnostic, not deployed
accuracy and not a held-out mitigation result.

- Native reference slice: `data/slices/validation_200_v4_dev50.jsonl`
- Item metrics: `results/analysis/generated_bn_reference_similarity_items.csv`
- Summary metrics: `results/analysis/generated_bn_reference_similarity_summary.csv`

Generated inputs:

- `protected_phonetic_bangla`: `results/generated_views/phonetic_bangla_protected_v2_dev50_benqa_mcq_generated_bn.jsonl`
- `protected_bnbphoneticparser`: `results/generated_views/bnbphoneticparser_protected_v2_dev50_benqa_mcq_generated_bn.jsonl`
- `protected_fms_byte_mbart`: `results/generated_views/fms_byte_protected_dev50_benqa_mcq_generated_bn.jsonl`

## Summary

| Generator | n | Mean CER | Median CER | Mean sequence similarity | Mean Bengali ratio | Exact matches |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| protected_phonetic_bangla | 36 | 0.0906 | 0.0665 | 0.8915 | 0.4036 | 0 |
| protected_bnbphoneticparser | 36 | 0.1235 | 0.1032 | 0.8598 | 0.3925 | 1 |
| protected_fms_byte_mbart | 36 | 0.1855 | 0.1928 | 0.8103 | 0.3839 | 1 |

## Interpretation Boundary

- Lower character error rate (CER) and higher sequence similarity mean
  the generated view is textually closer to the native-Bangla reference.
- Similarity does not prove semantic equivalence or downstream answer
  improvement.
- Generator selection remains dev-only until a routing rule is locked
  and evaluated unchanged on held-out test items.
