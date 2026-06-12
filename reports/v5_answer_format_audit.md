# Frozen-V5 Answer Format Audit

Updated: 2026-06-11

## Scope

This no-spend audit checks whether the release-facing script gap could be
explained by answer parsing or malformed answer formatting. It reuses the
same thesis-facing Qwen rows as the frozen-v5 main table: unchanged Bangla
and English outputs plus reviewed-v5 Banglish reruns.

- Item-level audit: `results/analysis/v5_answer_format_audit_items.csv`
- Summary table: `results/analysis/v5_answer_format_audit_summary.csv`

Format failure is defined as an empty parsed answer, or a BEnQA MCQ parsed
answer outside `A`/`B`/`C`/`D`. Long free-form BanglaMATH answers are
reported separately because they are parseable but indicate answer-format
drift.

## Main Gap Stress Test

| Model | Bangla correct | Reviewed Banglish correct | Banglish-Bangla gap | Bangla format failures | Banglish format failures | Gap if all Banglish format failures were correct |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen2.5-3B | 54/200 | 41/200 | -6.5 pts | 0 | 0 | -6.5 pts |
| Qwen2.5-7B 8-bit | 65/200 | 47/200 | -9.0 pts | 0 | 2 | -8.0 pts |
| Qwen3-4B | 80/200 | 49/200 | -15.5 pts | 4 | 3 | -14.0 pts |

## Format Failures By Dataset

| Model | Dataset | Bangla | Reviewed Banglish | English |
| --- | --- | ---: | ---: | ---: |
| Qwen2.5-3B | `benqa` | 0 | 0 | 0 |
| Qwen2.5-3B | `banglamath` | 0 | 0 | 0 |
| Qwen2.5-7B 8-bit | `benqa` | 0 | 2 | 0 |
| Qwen2.5-7B 8-bit | `banglamath` | 0 | 0 | 0 |
| Qwen3-4B | `benqa` | 4 | 3 | 8 |
| Qwen3-4B | `banglamath` | 0 | 0 | 0 |

## Long Raw Outputs

| Model | Dataset | Bangla | Reviewed Banglish | English |
| --- | --- | ---: | ---: | ---: |
| Qwen2.5-3B | `benqa` | 0 | 0 | 0 |
| Qwen2.5-3B | `banglamath` | 2 | 3 | 4 |
| Qwen2.5-7B 8-bit | `benqa` | 0 | 2 | 0 |
| Qwen2.5-7B 8-bit | `banglamath` | 1 | 0 | 1 |
| Qwen3-4B | `benqa` | 6 | 3 | 14 |
| Qwen3-4B | `banglamath` | 42 | 39 | 48 |

## Interpretation

- Qwen2.5-3B has zero format failures across all 600 thesis-facing outputs.
- Qwen2.5-7B 8-bit has two format failures, both reviewed-Banglish BEnQA
  MCQ rows. Even if both were credited as correct, its all-200
  Banglish-Bangla deficit remains -8.0 points.
- Qwen3-4B format failures are not Banglish-specific: BEnQA has 4 Bangla,
  3 reviewed-Banglish, and 8 English format failures.
- Long raw answers are concentrated in Qwen3 BanglaMATH across every
  script, supporting the existing claim that BanglaMATH is a low-accuracy
  stress test rather than a clean fine-grained script-gap source.

Thesis-safe phrasing:

> The frozen-v5 script gap is not an artifact of empty parsing or MCQ
> answer-format failures. Parse/format failures are rare for Qwen2.5,
> and for Qwen3 they are at least as common in English and Bangla as in
> reviewed Banglish.

Total format-failure rows: 17.
