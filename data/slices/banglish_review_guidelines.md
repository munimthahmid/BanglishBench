# Banglish Review Guidelines

Use this when filling `reviewed_banglish`, `quality_label`, and `review_notes`
in files such as:

- `data/slices/validation_100_v3_banglish_review.csv`
- `data/slices/validation_200_v5_review_queue.csv`

For validation-200 v5, start from:

- `reports/validation200_v5_review_calibration_set.md`
- `reports/validation200_v5_review_packets_impact_order/README.md`
- `reports/validation200_v5_review_impact_substitutions.md`
- `reports/validation200_v5_substitution_review_playbook.md`
- `reports/validation200_v5_review_session_plan.md`
- `reports/validation200_v5_review_session_packets/README.md`
- `reports/validation200_v5_review_session_log.md`
- `scripts/review_validation200_v5_queue.py`

## Goal

Create a natural Latin-script Bangla version that preserves the original
question exactly. Do not simplify the question, translate to English, fix the
gold answer, or add hints.

## `reviewed_banglish`

Write how a fluent Bangla speaker might naturally type the Bangla content using
Latin letters.

Preserve:

- Numbers and math symbols.
- MCQ option letters.
- Chemical formulas.
- The instruction line, e.g. `Answer with only A, B, C, or D.` or
  `Return only the final answer.`

Allowed:

- Natural Banglish spelling choices, e.g. `ki`, `koto`, `konoti`, `hoy`.
- Common English technical terms if the original already contains formulas or
  loanwords.
- Small spelling normalization where the rule-based output is awkward.

Not allowed:

- Changing the answer options.
- Adding explanation.
- Translating the entire item into English.
- Removing hard words just because the model may struggle.

## `quality_label`

Use one of:

- `ok`: rule-based Banglish is acceptable; no edit needed.
- `minor_edit`: understandable but one or two unnatural spellings should be fixed.
- `major_edit`: understandable only with effort; rewrite the Banglish.
- `bad`: corrupt or misleading; exclude until fixed.

For `ok` and `bad`, leave `reviewed_banglish` blank. For `minor_edit` and
`major_edit`, fill `reviewed_banglish` with the full replacement prompt, not
only the edited phrase.

For `bad`, add a short reason in `review_notes` so the final freeze policy can
justify whether the row is kept flagged or dropped from a strict reviewed
subset.

The auto-suggested Banglish in v5 is a candidate, not gold. Repeated edits such
as `kot` -> `koto`, `ekoti` -> `ekti`, or `konoti` -> `konti` still need
source-context review.

## `review_notes`

Keep notes short and concrete:

- `fixed tto ending`
- `loanword spelling`
- `option formula preserved`
- `rule output misleading`

## Examples

### Minor Edit

Rule output:

```text
tamar rodhokotb konoti?
```

Reviewed:

```text
tamar rodhokotto konoti?
```

Label: `minor_edit`

### Major Edit

Rule output:

```text
ghumer oushodh hisebe byobohrit hoy konoti?
A. foromalodihaid
B. ojasitalodihaid
C. pyaralodihaid
D. metalodihaid
```

Reviewed:

```text
ghumer oushodh hisebe byabohrito hoy konoti?
A. formaldehyde
B. acetaldehyde
C. paraldehyde
D. metaldehyde
```

Label: `major_edit`

### Bad

Use `bad` when the Banglish field changes the task, drops numbers/options,
corrupts formulas, or is too misleading to trust. Do not provide a replacement
unless you are confident enough to mark it `minor_edit` or `major_edit`.
