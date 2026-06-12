# Frozen-V5 Qwen Scaling-Transfer Audit

Updated: 2026-06-11

## Scope

This no-spend audit asks whether stronger Qwen rows transfer added
task competence equally across Bangla, reviewed Banglish, and English.
It uses the frozen-v5 thesis-facing Qwen correctness table; no new
model inference is involved.

- Transition table: `results/analysis/v5_qwen_scaling_transfer_transitions.csv`
- Summary table: `results/analysis/v5_qwen_scaling_transfer_summary.csv`

## Headline

- Same-family Qwen2.5 3B->7B scaling improves all-200 Bangla by 11 items and English by 23 items, but reviewed Banglish by only 6 items.
- The reviewed-Banglish-minus-Bangla count gap widens from -13 to -18 under Qwen2.5 3B->7B (change -5).
- Comparing Qwen2.5-3B to Qwen3-4B, Bangla gains 26 items and English gains 17 items, while reviewed Banglish gains 8 items.
- The Qwen2.5-3B->Qwen3-4B reviewed-Banglish-minus-Bangla count gap widens from -13 to -31 (change -18).
- Treat this as behavioral scaling-transfer evidence, not a causal model-size mechanism.

## All-200 Script Transitions

| Pair | Script | Source correct | Target correct | Gains | Losses | Net | Both correct | Both wrong |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B -> Qwen2.5-7B 8-bit | Bangla | 54/200 | 65/200 | 35 | 24 | 11 | 30 | 111 |
| Qwen2.5-3B -> Qwen2.5-7B 8-bit | Reviewed Banglish | 41/200 | 47/200 | 25 | 19 | 6 | 22 | 134 |
| Qwen2.5-3B -> Qwen2.5-7B 8-bit | English | 71/200 | 94/200 | 33 | 10 | 23 | 61 | 96 |
| Qwen2.5-3B -> Qwen3-4B | Bangla | 54/200 | 80/200 | 47 | 21 | 26 | 33 | 99 |
| Qwen2.5-3B -> Qwen3-4B | Reviewed Banglish | 41/200 | 49/200 | 30 | 22 | 8 | 19 | 129 |
| Qwen2.5-3B -> Qwen3-4B | English | 71/200 | 88/200 | 33 | 16 | 17 | 55 | 96 |
| Qwen2.5-7B 8-bit -> Qwen3-4B | Bangla | 65/200 | 80/200 | 45 | 30 | 15 | 35 | 90 |
| Qwen2.5-7B 8-bit -> Qwen3-4B | Reviewed Banglish | 47/200 | 49/200 | 33 | 31 | 2 | 16 | 120 |
| Qwen2.5-7B 8-bit -> Qwen3-4B | English | 94/200 | 88/200 | 21 | 27 | -6 | 67 | 85 |

## Banglish-Minus-Bangla Gap Change

| Dataset | Pair | Source gap | Target gap | Change |
| --- | --- | ---: | ---: | ---: |
| all | Qwen2.5-3B -> Qwen2.5-7B 8-bit | -13 | -18 | -5 |
| all | Qwen2.5-3B -> Qwen3-4B | -13 | -31 | -18 |
| all | Qwen2.5-7B 8-bit -> Qwen3-4B | -18 | -31 | -13 |
| benqa | Qwen2.5-3B -> Qwen2.5-7B 8-bit | -8 | -13 | -5 |
| benqa | Qwen2.5-3B -> Qwen3-4B | -8 | -29 | -21 |
| benqa | Qwen2.5-7B 8-bit -> Qwen3-4B | -13 | -29 | -16 |
| banglamath | Qwen2.5-3B -> Qwen2.5-7B 8-bit | -5 | -5 | 0 |
| banglamath | Qwen2.5-3B -> Qwen3-4B | -5 | -2 | 3 |
| banglamath | Qwen2.5-7B 8-bit -> Qwen3-4B | -5 | -2 | 3 |

## Interpretation

The frozen-v5 scaling pattern is not just that stronger models get more
items correct. Their added competence transfers unevenly across scripts.
For the same-family Qwen2.5 comparison, the 7B row gains many more
English items and somewhat more Bangla items than Banglish items. For the
Qwen2.5-3B to Qwen3-4B comparison, Bangla improves sharply while
reviewed Banglish improves only modestly.

This supports the thesis framing that script is a robustness variable:
more model competence does not automatically close the Latin-script
Banglish gap. The Qwen3 comparison crosses model families/generations,
so cite it as descriptive scaling-transfer evidence rather than as a
controlled parameter-count claim.

## Reproducibility

- Builder: `scripts/analyze_v5_qwen_scaling_transfer.py`
- Transition rows: 1800
- Summary rows: 63
