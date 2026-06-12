# Within-Family Qwen Scaling Curve (frozen v5)

Updated: 2026-06-11

Banglish-minus-Bangla gap on the frozen validation-200 v5 slice across
seven Qwen models. Small models (0.5B/1.5B Qwen2.5, 0.6B/1.7B Qwen3, all
no-thinking for Qwen3) were run for this analysis; 3B/7B/4B reuse the
frozen-v5 triad. CIs are paired bootstrap; p is McNemar exact.

- Table: `results/analysis/qwen_scaling_curve_v5.csv`
- Figure: `Thesis Template UG/figures/fig_scaling_curve.pdf`
- Builder: `scripts/analyze_scaling_curve.py`

| Model | Family | Params (B) | Bangla | Banglish | Gap (pts) | 95% CI | McNemar p |
| --- | --- | ---: | ---: | ---: | ---: | --- | ---: |
| Qwen2.5-0.5B | Qwen2.5 | 0.49 | 40/200 | 46/200 | +3.0 | [-1.5, +7.5] | 0.2632 |
| Qwen2.5-1.5B | Qwen2.5 | 1.54 | 46/200 | 40/200 | -3.0 | [-9.0, +3.0] | 0.4177 |
| Qwen2.5-3B | Qwen2.5 | 3.09 | 54/200 | 41/200 | -6.5 | [-13.0, +0.0] | 0.0660 |
| Qwen2.5-7B | Qwen2.5 | 7.62 | 65/200 | 47/200 | -9.0 | [-16.5, -1.5] | 0.0222 |
| Qwen3-0.6B | Qwen3 | 0.6 | 35/200 | 29/200 | -3.0 | [-8.0, +2.0] | 0.3449 |
| Qwen3-1.7B | Qwen3 | 1.72 | 33/200 | 35/200 | +1.0 | [-5.5, +7.5] | 0.8776 |
| Qwen3-4B | Qwen3 | 4.02 | 80/200 | 49/200 | -15.5 | [-22.0, -9.0] | 0.0000 |
