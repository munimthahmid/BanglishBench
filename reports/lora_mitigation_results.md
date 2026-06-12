# LoRA Banglish-Mitigation Results (Qwen2.5-3B)

Updated: 2026-06-11

Arm A trains on Banglish-only completions; arm B on a 1:1:1 Bangla/
Banglish/English mix. Training data is disjoint from validation-200 v5 and
the 1,000-row extension (asserted in the build). Headline metric is gap
shrinkage, not Banglish accuracy.

## Dev-200 sanity (held-out, never trained)

| Condition | Bangla | Banglish | English |
| --- | ---: | ---: | ---: |
| base | 76/200 | 63/200 | 87/200 |
| armA | 72/200 | 75/200 | 105/200 |
| armB | 79/200 | 70/200 | 113/200 |

Dev Banglish gain vs base: arm A +6.0 pts (CI [-2.0, +14.5], McNemar p=0.1882); arm B +3.5 pts (CI [-4.5, +11.5], p=0.4570).

## Frozen validation-200 v5 triad

| Condition | Bangla | Banglish | English | Banglish-Bangla gap |
| --- | ---: | ---: | ---: | ---: |
| base | 54/200 | 41/200 | 71/200 | -6.5 pts |
| armA | 57/200 | 46/200 | 69/200 | -5.5 pts |
| armB | 55/200 | 47/200 | 76/200 | -4.0 pts |

## Deltas vs base on frozen v5 (paired bootstrap CI, McNemar exact p)

| Arm | View | Delta vs base | 95% CI | McNemar p |
| --- | --- | ---: | --- | ---: |
| armA | Banglish | +2.5 pts | [-3.5, +8.5] | 0.4996 |
| armA | Bangla | +1.5 pts | [-4.5, +7.5] | 0.7493 |
| armA | English | -1.0 pts | [-7.0, +4.5] | 0.8642 |
| armB | Banglish | +3.0 pts | [-2.5, +8.5] | 0.3616 |
| armB | Bangla | +0.5 pts | [-6.5, +7.5] | 1.0000 |
| armB | English | +2.5 pts | [-3.0, +8.0] | 0.4869 |

## Interpretation

Base Banglish-Bangla gap: -6.5 pts. Arm A gap: -5.5 pts. Arm B gap: -4.0 pts.

Script mitigation requires the Banglish-Bangla gap to move toward zero
while Bangla and English do not significantly regress. If all three views
rise by a similar amount, the adapter learned the task, not the script.
