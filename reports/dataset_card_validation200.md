# Dataset Card Draft: Script Matters Validation-200

Updated: 2026-05-30

## Dataset Summary

Script Matters validation-200 is a controlled orthographic robustness slice for
Bangla educational QA/math. Each item keeps the same id and gold answer across
script views:

- native Bangla,
- clean Latin-script Banglish,
- noisy Banglish where available,
- English translation where available.

The benchmark is designed to test whether model behavior changes when the
underlying task is held fixed but the script/orthography changes.

## Sources

| Source | Rows in validation-200 | Role |
| --- | ---: | --- |
| BEnQA | 144 | Bengali/English curriculum science MCQ questions. |
| BanglaMATH | 56 | Bengali/English elementary math word problems. |

MGSM is used separately as an external breadth check and is not part of
validation-200.

## Files

Current controlled slices:

- `data/slices/validation_200_v3.jsonl`
- `data/slices/validation_200_v4.jsonl`
- `data/slices/validation_200_v4_dev50.jsonl`
- `data/slices/validation_200_v4_test150.jsonl`
- `data/slices/validation_200_v4_auto_suggested.jsonl`
- `data/slices/validation_200_v5.jsonl`
- `data/slices/validation_200_v5.manifest.json`

Frozen-v5 review trail:

- `data/slices/validation_200_v5_review_queue.csv`
- `results/analysis/validation200_v5_banglish_review_audit.csv`
- `reports/validation200_v5_review_packets_impact_order/README.md`
- `reports/post_v5_rerun_protocol.md`

Validation-200 v5 is frozen under the all-200 denominator policy.

Scale-extension layer:

- `data/slices/benqa_extended_1000_v1.jsonl`
- `data/slices/benqa_extended_1000_v1_ai_reviewed.jsonl`
- `data/slices/benqa_extended_1000_v1_ai_pass.jsonl`
- `reports/benqa_extended_1000_v1.md`
- `reports/benqa_extended_1000_v1_ai_review.md`
- `reports/qwen25_3b_benqa_ext_full851.md`
- `reports/qwen25_3b_benqa_ext_full851_paired_gap_analysis.md`
- `reports/deepseek_v4_flash_benqa_ext_full851.md`
- `reports/deepseek_v4_flash_benqa_ext_full851_paired_gap_analysis.md`

The BEnQA extension is a silver layer, not a replacement for validation-200 v5.
It adds 1,000 BEnQA-only rows sampled from 4,939 eligible source rows after
excluding the frozen BEnQA gold-core rows. AI-assisted structural review marks
851 rows as pass, 149 as warning-only, and 0 as structural fail. This must be
disclosed as AI-assisted review, not human review.

The full 851-row pass-only extension has completed Qwen2.5-3B and DeepSeek V4
Flash triad runs. Qwen2.5-3B scores 291/851 Bangla, 248/851 reviewed Banglish,
and 437/851 English, with paired reviewed-Banglish gaps of -5.05 pts vs Bangla
and -22.21 pts vs English. DeepSeek V4 Flash scores 665/851 Bangla, 376/851
reviewed Banglish, and 697/851 English, with paired gaps of -33.96 pts vs
Bangla and -37.72 pts vs English.

## Fields

Core fields:

- `id`
- `dataset`
- `task_type`
- `answer_type`
- `answer`
- `bangla`
- `banglish_clean`
- `banglish_noisy`
- `english`
- `english_available`
- `metadata`
- `source_file`
- `source_row`
- `source_url`
- `quality_status`
- `transliteration_method`

## Splits

validation-200 v4 has a deterministic dev/test split:

| Split | Rows | Intended use |
| --- | ---: | --- |
| dev50 | 50 | Mitigation/routing selection and diagnostics. |
| test150 | 150 | Held-out reporting after a rule is fixed. |

Do not tune a mitigation on test150.

## Quality Status

v4 is the rule-based Banglish predecessor with targeted cleanup. It remains
useful for historical sensitivity comparisons.

v5 is the frozen reviewed successor:

- 140/140 queued rows reviewed,
- 126 `minor_edit`,
- 11 `major_edit`,
- 3 `bad`,
- 0 pending.

Rows labeled `bad` are kept and flagged under the frozen all-200 policy. A
future strict-subset analysis may use `--drop-bad`, but it must be reported
separately rather than mixed into the main tables. The separate strict-197
policy sensitivity is reported in `reports/v5_bad_row_policy_sensitivity.md`.

## Intended Uses

Appropriate:

- paired Bangla/Banglish/English model evaluation,
- orthographic robustness analysis,
- tokenization and failure-pattern analysis,
- mitigation diagnostics under dev/test discipline.

Not appropriate:

- claiming all real-world Banglish is represented,
- training a production transliterator,
- evaluating broad Bengali culture or social-media pragmatics,
- comparing models without reporting parser, prompt mode, and split policy.

## Known Limitations

- Frozen v5 Banglish is reviewed but still controlled rather than sampled from
  natural user conversations.
- The BEnQA extension is larger but has lower review strength than the
  validation-200 v5 gold core.
- Real social-media Banglish is shorter, more variable, and often code-mixed.
- Source English translations can contain noise.
- BanglaMATH accuracy is low for current compact open models.
- Extension scale evidence currently covers Qwen2.5-3B and DeepSeek V4 Flash;
  broader all-model-family claims require additional extension runs.

## Citation Pointers

Use source dataset citations for BEnQA and BanglaMATH, and cite Script Matters
as an orthographic robustness evaluation built from those sources. For
Romanized Bangla motivation, cite BanglaTLit, BanglishRev, BAN-TH, BnSentMix,
and MixSarc as related but task-different resources.
