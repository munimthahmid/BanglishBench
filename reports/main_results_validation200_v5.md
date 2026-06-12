# Main Results: Frozen Validation-200 V5

Updated: 2026-06-11

## Scope

This is the final reviewed-v5 all-200 Qwen table. Bangla and English fields
are unchanged from the historical controlled validation slice. The Banglish
field uses the completed reviewed-v5 reruns. The older v3/v4 table remains
available for provenance and mechanism analyses.

- Machine-readable sensitivity summary: `results/analysis/v5_bad_row_policy_sensitivity.csv`
- Generated thesis table: `results/tables/main_script_gap_validation200_v5.csv`
- Strict-197 sensitivity report: `reports/v5_bad_row_policy_sensitivity.md`

## Frozen-V5 All-200 Results

| Model | Bangla | Reviewed Banglish | English | Banglish-Bangla | Banglish-English |
| --- | ---: | ---: | ---: | --- | --- |
| Qwen2.5-3B | 54/200 | 41/200 | 71/200 | -6.5 pts, CI [-13.0, 0.0] | -15.0 pts, CI [-22.0, -7.5] |
| Qwen2.5-7B 8-bit | 65/200 | 47/200 | 94/200 | -9.0 pts, CI [-16.0, -2.0] | -23.5 pts, CI [-31.0, -16.0] |
| Qwen3-4B | 80/200 | 49/200 | 88/200 | -15.5 pts, CI [-22.0, -9.0] | -19.5 pts, CI [-27.0, -12.0] |

## Interpretation

- Reviewed Banglish remains below native-script Bangla and English at every
  thesis-facing Qwen scaling point.
- The all-200 paired Banglish-Bangla intervals remain negative for Qwen3-4B
  and Qwen2.5-7B 8-bit.
- Qwen2.5-3B retains a -6.5 point all-200 Banglish-Bangla deficit, but its
  interval reaches zero. The historical v3 estimate and the strict-197
  sensitivity remain negative, so the release claim is model-aware.
- The preregistered all-200 denominator remains primary. Strict-197 exclusion
  is a secondary robustness check, not a replacement denominator.
