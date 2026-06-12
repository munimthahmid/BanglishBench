# Frozen-V5 Cross-Script Diagnostics

Updated: 2026-06-11

## Scope

This report refreshes the diagnostic cross-script oracle, failure taxonomy,
and privileged Bangla+English agreement route against frozen-v5 reviewed
Banglish outputs. Bangla and English outputs are reused because those fields
did not change. No new model inference or paid API call is required.

The agreement route remains diagnostic rather than deployable: it uses
benchmark-provided alternate-script views.

## Reviewed-V5 Route Result

| Model | Reviewed Banglish | Agreement route | Delta | 95% CI | Any-script oracle |
| --- | ---: | ---: | ---: | --- | ---: |
| Qwen2.5-3B | 41/200 | 49/200 | +4.0 pts | [-0.5, +8.5] | 99/200 |
| Qwen2.5-7B 8-bit | 47/200 | 71/200 | +12.0 pts | [+6.5, +17.5] | 115/200 |
| Qwen3-4B | 49/200 | 76/200 | +13.5 pts | [+8.0, +19.0] | 108/200 |

## Historical-To-Reviewed Comparison

| Model | Historical Banglish | Historical route | Reviewed Banglish | Reviewed route |
| --- | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 38/200 | 47/200 | 41/200 | 49/200 |
| Qwen2.5-7B 8-bit | 48/200 | 71/200 | 47/200 | 71/200 |
| Qwen3-4B | 46/200 | 76/200 | 49/200 | 76/200 |

## Reviewed-V5 Failure Taxonomy

| Model | Banglish misses recoverable under Bangla or English | Bangla+English correct, Banglish wrong |
| --- | ---: | ---: |
| Qwen2.5-3B | 58/200 | 15/200 |
| Qwen2.5-7B 8-bit | 68/200 | 29/200 |
| Qwen3-4B | 59/200 | 32/200 |

## Reviewed-V5 Oracle By Dataset

| Model | Dataset | Bangla | Reviewed Banglish | English | Any-script oracle |
| --- | --- | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | benqa | 49/144 | 41/144 | 66/144 | 92/144 |
| Qwen2.5-3B | banglamath | 5/56 | 0/56 | 5/56 | 7/56 |
| Qwen2.5-7B 8-bit | benqa | 60/144 | 47/144 | 86/144 | 105/144 |
| Qwen2.5-7B 8-bit | banglamath | 5/56 | 0/56 | 8/56 | 10/56 |
| Qwen3-4B | benqa | 76/144 | 47/144 | 82/144 | 102/144 |
| Qwen3-4B | banglamath | 4/56 | 2/56 | 6/56 | 6/56 |

## Interpretation

- Reviewed cleanup does not remove cross-script recoverability.
- The privileged agreement route remains clearly positive for Qwen2.5-7B
  8-bit and Qwen3-4B.
- Qwen2.5-3B retains a +4.0-point route gain, but its reviewed-v5 interval
  crosses zero. Keep that uncertainty explicit.
- Oracle headroom remains large for every thesis-facing Qwen row.
- Use these results as mitigation-design evidence, not deployed accuracy.

## Artifacts

- Builder: `scripts/build_v5_cross_script_diagnostics.py`
- Summary: `results/analysis/validation200_v5_cross_script_diagnostics_summary.csv`
- Agreement items: `results/analysis/validation200_v5_cross_script_answer_agreement_items.csv`
- Agreement buckets: `results/analysis/validation200_v5_cross_script_answer_agreement_buckets.csv`
- Agreement routes: `results/analysis/validation200_v5_cross_script_answer_agreement_routes.csv`
- Failure items: `results/analysis/validation200_v5_cross_script_failure_patterns_items.csv`
- Failure summary: `results/analysis/validation200_v5_cross_script_failure_patterns_summary.csv`
- Oracle summary: `results/analysis/validation200_v5_cross_script_oracle_union.csv`
