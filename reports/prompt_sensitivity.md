# Prompt and Decoding Sensitivity (Qwen2.5-3B, validation-200 v5)

Updated: 2026-06-11

The Banglish-minus-Bangla gap under the frozen baseline versus two neutral
alternate prompt templates and a temperature=0.7 decoding variant. Neutral
templates contain no Banglish hint, so they test prompt-wording sensitivity.

- Table: `results/analysis/prompt_sensitivity_summary.csv`
- Builder: `scripts/analyze_prompt_sensitivity.py`

| Condition | Bangla | Banglish | English | Banglish-Bangla | Banglish-English |
| --- | ---: | ---: | ---: | ---: | ---: |
| baseline (greedy) | 54/200 | 41/200 | 71/200 | -6.5 pts | -15.0 pts |
| neutral template B | 51/200 | 45/200 | 71/200 | -3.0 pts | -13.0 pts |
| neutral template C | 53/200 | 45/200 | 74/200 | -4.0 pts | -14.5 pts |
| temperature 0.7 | 53/200 | 44/200 | 71/200 | -4.5 pts | -13.5 pts |
