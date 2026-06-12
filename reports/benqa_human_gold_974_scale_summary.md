# BEnQA Human-Reviewed Gold 974 Scale Summary

Updated: 2026-06-07

## Scope

This table summarizes completed model runs on the frozen 974-row
human-reviewed BEnQA extension. The full 1,000-row audit slice has 26
human-rejected rows; accepted and edited rows form the gold/pass
evaluation set.

- Summary CSV: `results/analysis/benqa_human_gold_974_scale_summary.csv`

## Results

| Model | Bangla | Reviewed Banglish | English | BG-Bangla | BG-English |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 323/974 (33.16%) | 285/974 (29.26%) | 490/974 (50.31%) | -3.90 pts [-7.19, -0.51] | -21.05 pts [-24.64, -17.35] |
| Groq Llama 3.3 70B | 547/974 (56.16%) | 333/974 (34.19%) | 622/974 (63.86%) | -21.97 pts [-25.67, -18.17] | -29.67 pts [-33.26, -26.08] |
| Gemini 3.5 Flash | 743/974 (76.28%) | 633/974 (64.99%) | 680/974 (69.82%) | -11.29 pts [-13.66, -8.93] | -4.83 pts [-7.39, -2.05] |
| GPT-5.5 none | 820/974 (84.19%) | 699/974 (71.77%) | 825/974 (84.70%) | -12.42 pts [-15.09, -9.75] | -12.94 pts [-15.91, -9.86] |
| Claude Sonnet 4.6 | 764/974 (78.44%) | 524/974 (53.80%) | 771/974 (79.16%) | -24.64 pts [-27.82, -21.25] | -25.36 pts [-28.64, -21.87] |
| DeepSeek V4 Flash | 756/974 (77.62%) | 438/974 (44.97%) | 791/974 (81.21%) | -32.65 pts [-36.04, -29.26] | -36.24 pts [-39.73, -32.96] |

## Interpretation

All six completed rows now show reviewed Banglish below Bangla and English on
the same 974 human-reviewed BEnQA items. The new GPT-5.5 none result is the
largest thesis update: unlike the validation-200 mixed-task panel where GPT-5.5
nearly collapsed the reviewed-Banglish gap under secondary scoring, the
human-gold BEnQA scale run keeps a clear paired deficit.

Gemini and Claude also preserve the deficit, but their strict scores include a
format/protocol component: both produce non-empty verbose or truncated answers
that the strict MCQ parser does not always reduce to a canonical option. Report
these as strict-parser benchmark results, with parser/format instability noted
as part of the frontier-model behavior.

## Source Reports

- Qwen2.5-3B: `reports/qwen25_3b_benqa_human_gold_974.md`
- Groq Llama 3.3 70B: `reports/groq_llama33_70b_benqa_human_gold_974.md`
- Gemini 3.5 Flash: `reports/gemini_3_5_flash_benqa_human_gold_974.md`
- GPT-5.5 none: `reports/openai_gpt55_none_benqa_human_gold_974.md`
- Claude Sonnet 4.6: `reports/claude_sonnet_4_6_benqa_human_gold_974.md`
- DeepSeek V4 Flash: `reports/deepseek_v4_flash_benqa_human_gold_974.md`
