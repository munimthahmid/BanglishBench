# Chapter 3 Benchmark Construction Draft

Updated: 2026-05-30

## 3.1 Design Goal

The benchmark is designed to isolate the effect of script choice on Bangla task
solving. Each item should preserve the same underlying question, gold answer,
answer format, and item id while changing only the written form presented to the
model. This paired design is the core methodological choice of the thesis.

The benchmark is not intended to replace natural Banglish corpora. Instead, it
serves as a controlled orthographic robustness test: if the same item becomes
harder when written in Latin-script Banglish, then script choice is a real
evaluation variable even before modeling the full diversity of natural
Banglish.

## 3.2 Source Tasks

The validation-200 slice uses two source tasks.

BEnQA contributes curriculum-style multiple-choice science and subject
questions with Bengali and English views. It provides the clearest
script-controlled QA signal because current open models have enough competence
to answer a non-trivial portion of the items.

BanglaMATH contributes elementary Bangla math word problems and English
translations. It is harder for the current open models and should be treated as
a stress test. It remains useful because arithmetic and units create strong
preservation requirements for any Banglish or generated-view transformation.

MGSM Bengali is used as an external arithmetic breadth check rather than as the
main validation-200 source. It helps test whether mitigation behavior transfers
outside the local curriculum slice.

## 3.3 Script Variants

Each validation item can contain several views.

Native Bangla:

- Bengali-script source prompt.
- Used as the native-script comparison.

Clean Banglish:

- Latin-script Bengali produced by the project romanization pipeline and later
  cleaned through v4/v5 workflows.
- Used as the main orthographic robustness condition.

Noisy Banglish:

- Deterministic perturbation of clean Banglish.
- Used as a stress/sensitivity condition, not as a natural social-media model.

English:

- Source or translated English prompt.
- Used as a high-resource control and as a cross-script recoverability view.

Generated views:

- Optional generated Bengali or English views from Banglish input.
- Used only for mitigation diagnostics after preservation gates.

## 3.4 Validation Slices

The current core slices are:

| Slice | Items | Role |
| --- | ---: | --- |
| `validation_100_v3` | 100 | Early aligned QA/math validation and mitigation development. |
| `validation_200_v3` | 200 | Main historical full-slice evidence for Qwen2.5-3B and Qwen3-4B. |
| `validation_200_v4` | 200 | Same item ids with conservative Banglish cleanup and dev/test split. |
| `validation_200_v4_dev50` | 50 | Development split for routing/prompt decisions. |
| `validation_200_v4_test150` | 150 | Held-out split for dev-selected decisions. |
| `validation_200_v4_auto_suggested` | 200 | Unreviewed automatic spelling-suggestion sensitivity slice. |
| `validation_200_v5` | 200 | Frozen human-reviewed Banglish slice used for post-v5 sensitivity. |

The dev/test split is deterministic with seed `20260528` and stratified by BEnQA
subject and BanglaMATH grade. Future prompt, routing, generated-view, or paid
API decisions should be selected on dev50 and evaluated unchanged on test150.

## 3.5 Banglish Quality Workflow

The Banglish pipeline has progressed through several quality stages.

v2 removed major nukta artifacts. v3 fixed major conjunct-y artifacts such as
`songkhja` to `songkhya`. v4 applied conservative cleanup without changing item
ids. v4 sensitivity reruns showed that the main Qwen script-gap conclusion did
not depend on these targeted cleanup changes.

The v5 review is complete. Its queue contains 140 rows selected from the
validation-200 slice because they have suggested edits, known artifact patterns,
model-relevant failures, or high replacement burden. The queue includes the
Bangla source, English source, current Banglish, auto-suggested Banglish, model
correctness flags, and the completed human-review fields.

The review workflow is impact-ordered but executed through exact generated
sessions:

- `reports/validation200_v5_review_quickstart.md`
- `reports/validation200_v5_review_impact_ranking.md`
- `reports/validation200_v5_review_calibration_set.md`
- `reports/validation200_v5_review_session_plan.md`
- `reports/validation200_v5_review_session_packets/README.md`
- `reports/validation200_v5_review_session_log.md`
- `scripts/review_validation200_v5_queue.py`

The generated session plan covered all 140 rows in 12 sessions and used exact
helper commands such as
`python3 scripts/review_validation200_v5_queue.py --session 1`. Repeated
patterns such as `konoti -> konti`, `kot -> koto`, and `ekoti -> ekti` were
handled consistently. The full queue remains authoritative; packet Markdown
files are read-only audit aids.

## 3.6 Human Review Labels

The v5 queue uses three editable fields:

- `quality_label`
- `reviewed_banglish`
- `review_notes`

Allowed labels:

| Label | Meaning | `reviewed_banglish` |
| --- | --- | --- |
| `ok` | Current Banglish is acceptable | Blank |
| `minor_edit` | Small spelling/style edit needed | Full replacement prompt |
| `major_edit` | Substantial rewrite needed | Full replacement prompt |
| `bad` | Item should not be trusted as clean Banglish | Blank by default |

For `minor_edit` and `major_edit`, the reviewer must write the full replacement
prompt, not only the changed word. This prevents partial-edit ambiguity during
freeze. For `bad`, the reviewer must leave `reviewed_banglish` blank and write
a short reason in `review_notes`, because bad-row handling affects the final
denominator policy.

## 3.7 Validation And Freeze

The pre-freeze validator checks labels, required replacements, option
preservation, digit preservation, formula preservation, answer-format
instructions, and Bengali-script leakage. The final queue passes with zero
structural errors, zero warnings, and zero pending rows.

The v5 slice was frozen only after:

```bash
python3 scripts/validate_banglish_review_queue.py --require-complete
```

passed with zero errors and zero pending rows.

The applied default freeze keeps all 200 rows and flags three `bad` Banglish
rows with `quality_status=human_review_bad_banglish`. This all-200 denominator
remains the preregistered main policy. A separate strict-197 sensitivity view
excludes the flagged rows from existing outputs and is reported independently
in `reports/v5_bad_row_policy_sensitivity.md`; it is not mixed into the main
tables.

A review edit-distance sensitivity audit separates no-applied-change, tiny,
small, and larger applied edits. The 63 no-applied-change rows already keep
reviewed Banglish below Bangla and English for all three thesis-facing Qwen
rows, so the final gap is not introduced only by heavily edited review rows.
The audit is reproducible from `reports/v5_review_edit_distance_sensitivity.md`.

## 3.8 Evaluation Format

Prompts are answer-only. Multiple-choice items require only A, B, C, or D.
Short-answer items require only the final answer. This is necessary because
models differ in reasoning verbosity, and Qwen3-family thinking behavior can
break answer-only evaluation if not controlled.

All thesis-facing scores should use reparsed/rescored outputs. The answer
parser extracts MCQ labels and short answers consistently across baseline,
mitigation, and future API runs.

## 3.9 Reproducibility Artifacts

The benchmark construction is documented by:

- `reports/dataset_card_validation200.md`
- `reports/reproducibility_release_checklist.md`
- `reports/reproducibility_artifact_manifest.md`
- `reports/v5_analysis_preregistration.md`
- `reports/post_v5_rerun_protocol.md`
- `reports/post_v5_rerun_readiness.md`
- `reports/post_v5_kaggle_job_plan.md`

The artifact manifest records non-secret files and SHA-256 hashes. It excludes
credential files and its own generated outputs. It was rebuilt after the v5
freeze, post-v5 model reruns, and thesis-table regeneration.

A source-variant structural parity audit checks the frozen v5 Bangla, reviewed
Banglish, and English prompt fields for MCQ option labels, digit sequences,
formula-like tokens, and answer instructions. The primary Bangla-vs-reviewed
Banglish pair has 0/200 structural mismatches. The English comparisons have
39/200 diagnostic warnings, which are treated as upstream translation caveats
rather than exclusions from the primary paired Bangla-vs-Banglish analysis.
The audit is reproducible from `reports/v5_source_variant_structural_parity.md`.

## 3.10 Chapter Summary

The benchmark is a controlled paired evaluation of script choice for Bangla
tasks. Its strength is task equivalence across Bangla, Banglish, and English.
Its main limitation is that the current Banglish remains controlled educational
Banglish rather than a natural user corpus. The BanglaTLit distribution,
lexical-coverage, and spelling-variation audits make this limitation explicit
while showing that the measured gap is not confined to the least-attested or
least-spelling-variable rows; per-model coverage and high-variation-exposure
sensitivities keep reviewed Banglish below Bangla and English for each Qwen
row. The completed v5 review, freeze, and rerun protocol are part of the
benchmark contribution rather than administrative cleanup.
