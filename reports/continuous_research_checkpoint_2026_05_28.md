# Continuous Research Checkpoint

Updated: 2026-05-28

Historical checkpoint. The generated-view preservation gate was tightened on
2026-05-30 to detect standalone scientific tokens, annotated units, and nested
LaTeX payloads. Use `reports/generated_view_diagnostics_summary.md` for the
current generated-view accounting.

## Scope

This checkpoint records the work completed after the generated-view and v5
review workflow resumed. It is a compact resume note, not a replacement for the
individual reports.

## v5 Review Workflow

Added:

- `scripts/validate_banglish_review_queue.py`
- `scripts/export_validation200_v5_review_packets.py`
- `scripts/rank_validation200_v5_review_impact.py`
- `scripts/summarize_validation200_v5_review_impact_patterns.py`
- `scripts/summarize_validation200_v5_review_metadata.py`
- `scripts/review_validation200_v5_queue.py`
- `scripts/summarize_v5_review_progress.py`
- `scripts/build_v5_review_calibration_set.py`
- `scripts/apply_banglish_review.py --drop-bad`
- `scripts/export_v5_substitution_review_playbook.py`
- `reports/validation200_v5_review_validation.md`
- `reports/validation200_v5_review_packets/README.md`
- `reports/validation200_v5_review_packets_impact_order/README.md`
- `reports/validation200_v5_review_calibration_set.md`
- `reports/validation200_v5_review_impact_ranking.md`
- `reports/validation200_v5_review_impact_substitutions.md`
- `reports/validation200_v5_review_metadata_summary.md`
- `reports/validation200_v5_review_progress.md`
- `reports/validation200_v5_substitution_review_playbook.md`

Current status:

- Review queue: `data/slices/validation_200_v5_review_queue.csv`
- Rows: 140
- Reviewed rows: 0
- Pending rows: 140
- Validator baseline: 0 errors, 0 warnings, 140 pending.
- Impact ranking: 43 tier-1 review-first rows, 52 tier-2 high rows.
- Highest-impact repeated substitutions:
  - `konoti` -> `konti`: 56 rows, 23 tier-1 rows.
  - `kot` -> `koto`: 72 rows, 17 tier-1 rows.
  - `ekoti` -> `ekti`: 37 rows, 13 tier-1 rows.
- Metadata coverage: 109/140 rows are in test150; top domain is `math` with
  55 rows, so review pressure is substantial in math/geometry wording.

Decision:

- Do not freeze validation-200 v5 until
  `python3 scripts/validate_banglish_review_queue.py --require-complete`
  has zero errors and zero pending rows.
- Start manual review from
  `reports/validation200_v5_review_packets_impact_order/README.md`, or use:

```bash
python3 scripts/review_validation200_v5_queue.py --tier tier_1_review_first
```
- For repeated-substitution batches, use:

```bash
python3 scripts/review_validation200_v5_queue.py --tier tier_1_review_first --substitution konoti:konti
```

- Track progress after each review session with:

```bash
python3 scripts/summarize_v5_review_progress.py
```

- Decide the `bad` row denominator policy before post-v5 reruns. Default freeze
  keeps bad rows flagged; `--drop-bad` creates a strict subset.

## Generated-View Preservation

Added:

- `scripts/audit_generated_view_outputs.py`
- `scripts/run_phonetic_bangla_generated_bn.py`
- `scripts/run_bnbphoneticparser_generated_bn.py`
- `scripts/run_protected_deterministic_generated_bn.py`

Raw deterministic generated-BN preservation:

| Generator | n | Hard failures | Main issue |
| --- | ---: | ---: | --- |
| `phonetic-bangla==1.0.0` | 36 | 36 | Option labels corrupted. |
| `bnbphoneticparser==0.1.5` | 36 | 36 | Option labels corrupted. |

Protected structural-mask preservation:

| Generator | n | Hard failures | Decision |
| --- | ---: | ---: | --- |
| `phonetic-bangla==1.0.0` | 36 | 0 | Eligible only for dev answer audit. |
| `bnbphoneticparser==0.1.5` | 36 | 0 | Eligible only for dev answer audit. |

Masking protects option prefixes, answer-format lines, LaTeX commands, and
formula-like tokens. Passing preservation gates does not prove lexical quality.

## Generated-BN Answer Audits

Prepared:

- `scripts/build_generated_bn_answer_audit_slice.py`
- `scripts/analyze_generated_bn_answer_audit.py`
- `data/generated_views/validation200_v4_dev50_benqa_mcq_protected_generated_bn_answer_audit.jsonl`

Qwen3-4B dev result:

| Variant | Correct |
| --- | ---: |
| Banglish baseline | 15/36 |
| Protected `phonetic-bangla` generated-BN | 11/36 |
| Protected `bnbphoneticparser` generated-BN | 17/36 |

Qwen2.5-3B dev result:

| Variant | Correct |
| --- | ---: |
| Banglish baseline | 8/36 |
| Protected `phonetic-bangla` generated-BN | 14/36 |
| Protected `bnbphoneticparser` generated-BN | 7/36 |

Decision:

- Generated-BN gains are model/generator-specific.
- Paired bootstrap intervals are wide:
  - Qwen3 protected BNB: +5.6 points CI [-8.3,+19.4].
  - Qwen3 protected phonetic: -11.1 points CI [-25.0,+2.8].
  - Qwen2.5 protected phonetic: +16.7 points CI [0.0,+33.3].
  - Qwen2.5 protected BNB: -2.8 points CI [-16.7,+11.1].
- Do not launch test150 for either deterministic generated-BN route.

## Generated-English And Agreement Route

Added:

- `scripts/extract_rewrite_outputs_for_generated_view_audit.py`
- `scripts/analyze_generated_view_agreement_route_dev.py`

Qwen3 generated-English self-translation:

- Answer accuracy: 7/36.
- Preservation hard failures: 6/36.
- Line-count warnings: 18/36.

Generated-BN + generated-EN agreement route:

| Route | Banglish | Generated-BN | Generated-EN | Routed |
| --- | ---: | ---: | ---: | ---: |
| BNB generated-BN + Qwen3 generated-EN agreement | 15/36 | 17/36 | 7/36 | 16/36 |

Decision:

- Do not launch test150.
- Generated-English quality is the current bottleneck.
- Keep this as mitigation-design evidence only.

## Updated Thesis Tables

Updated:

- `results/tables/deterministic_generated_view_smokes.csv`
- `results/tables/generated_bn_answer_audit_dev50.csv`
- `results/tables/generated_view_agreement_route_dev.csv`
- `results/tables/thesis_tables.md`

The generated-BN answer audit table now includes paired bootstrap intervals and
direction p-values.

## Literature And Rerun Planning

Added:

- `literature/notes/core_paper_notes.md`
- `literature/notes/script_matters_literature_synthesis.md`
- `literature/notes/benchmark_gap_matrix.md`
- `reports/post_v5_rerun_protocol.md`
- `reports/v5_analysis_preregistration.md`
- `scripts/analyze_banglish_variant_sensitivity.py`
- `reports/final_api_audit_cost_plan.md`
- `reports/threats_to_validity.md`
- `reports/dataset_card_validation200.md`
- `reports/thesis_defense_qna.md`
- `reports/thesis_defense_slide_outline.md`
- `reports/thesis_figures_and_tables_plan.md`
- `reports/thesis_figure_captions.md`
- `reports/thesis_qualitative_examples.md`
- `reports/thesis_appendix_plan.md`
- `reports/post_v5_thesis_revision_todo.md`
- `literature/references_seed.bib`
- `literature/notes/citation_key_map.md`
- `reports/chapter_1_introduction_draft.md`
- `reports/chapter_2_related_work_draft.md`
- `reports/chapter_3_benchmark_construction_draft.md`
- `reports/chapter_4_main_results_draft.md`
- `reports/chapter_5_robustness_and_model_breadth_draft.md`
- `reports/chapter_6_failure_analysis_draft.md`
- `reports/chapter_7_tokenization_mechanism_draft.md`
- `reports/chapter_8_mitigation_draft.md`
- `reports/chapter_9_limitations_draft.md`
- `reports/chapter_10_conclusion_draft.md`
- `reports/thesis_draft_compiled.md`
- `scripts/compile_thesis_draft.py`
- `reports/figures/README.md`
- `scripts/build_thesis_figures.py`
- `reports/reproducibility_release_checklist.md`
- `reports/reproducibility_artifact_manifest.md`
- `scripts/build_artifact_manifest.py`
- `reports/local_artifact_reference_check.md`
- `scripts/check_local_artifact_refs.py`
- `scripts/run_research_checks.py`

Positioning update:

- Do not claim Bengali lacks benchmarks. Recent work covers BnMMLU, BLUCK,
  BanglaQuAD, NCTB-QA, BNLI, Bangla Social Bench, BAN-TH, BnSentMix, MixSarc,
  BanglaTLit, BanglishRev, and Bhasha-Abhijnaanam-style Roman-script Indic
  infrastructure.
- The novelty claim is controlled orthographic robustness for the same QA/math
  item across native Bangla, Latin-script Banglish, and English.
- Mechanism framing should cite RomanLens, Do Llamas Work in English, Do
  Multilingual LLMs Think in English, and MALT Urdu as related latent-pivot or
  low-resource generation evidence, without claiming our current results prove
  an internal causal mechanism.

Release prep added:

- A defense Q&A converts the current evidence into short answers for likely
  committee questions, including novelty, rule-based Banglish, tokenization,
  Qwen-family scope, mitigation brittleness, and paid API timing.
- A figures/tables plan maps each major thesis table and figure to its current
  source artifact and marks which ones must be updated after v5.
- Draft SVG figures now cover the main script gap, self-normalization deltas,
  and cross-script recovery signals from `results/tables/*.csv`.
- A Chapter 1 introduction draft now turns the evidence into a thesis narrative
  with motivation, problem statement, research questions, contributions,
  limitations, and roadmap.
- A Chapter 2 related-work draft now positions Bengali benchmarks,
  Romanized/code-mixed Bangla resources, transliteration robustness,
  tokenization, latent pivots, and mitigation work around the Script Matters
  novelty claim.
- Citation support now includes a generated bibliography seed and citation-key
  map built from official ACL Anthology BibTeX exports and arXiv API metadata.
- Thesis-facing qualitative examples, figure captions, appendix plan, and
  defense slide outline are now drafted so final writing can update numbers
  instead of rebuilding structure.
- `scripts/run_research_checks.py` is the current one-command local QA pass:
  it compiles the thesis draft, regenerates v5 review progress, validates the
  queue, checks local references, compiles scripts, and rebuilds the manifest.
- A Chapter 3 benchmark construction draft now documents source tasks, script
  variants, validation slices, v5 review labels, freeze policy, evaluation
  format, and reproducibility artifacts.
- A Chapter 4 main-results draft now turns the validation-200 script-gap,
  robustness, scaling, and subject-spread evidence into thesis prose.
- A Chapter 5 robustness/model-breadth draft now separates cleanup/noise
  sensitivity, Qwen scaling, non-Qwen breadth, specialized-model diagnostics,
  and compute constraints from the primary result.
- A Chapter 6 failure-analysis draft now explains cross-script oracle,
  taxonomy, answer agreement, qualitative examples, and tokenization/failure
  joins.
- A Chapter 7 tokenization/mechanism draft now frames token count as a ruled-out
  simple explanation while keeping internal mechanism claims cautious.
- A Chapter 8 mitigation draft now covers prompts, self-normalization,
  answer-signal routing, cross-script agreement, generated-view gates, and
  external-normalization caveats.
- Chapter 9 and Chapter 10 drafts now cover limitations, scope boundaries,
  future work, and the final thesis conclusion.
- A compiled thesis draft now concatenates Chapters 1-10 into
  `reports/thesis_draft_compiled.md`.
- A reproducibility/release checklist defines the v5 freeze gate, post-freeze
  audit commands, minimal reruns, thesis-table regeneration, API audit gate,
  and secret-hygiene rules.
- A v5 analysis preregistration locks the primary models, comparisons,
  denominator policy, bootstrap statistics, and no-peeking rules before any
  post-v5 output exists.
- A non-secret artifact manifest now records 524 local thesis artifacts with
  SHA-256 hashes while excluding Kaggle keys, PEM files, and credential files.
- A local artifact-reference checker reports zero unexpected missing local
  references; current missing references are all expected future/planned v5 or
  blocked-pilot artifacts.

Post-v5 policy:

- After v5 freezes, rerun clean Banglish only for Qwen2.5-3B and Qwen3-4B
  first.
- Rerun Qwen2.5-7B 8-bit only if v5 materially affects held-out/main-table
  rows.
- No Bangla/English reruns unless source fields changed.
- Treat `reports/v5_analysis_preregistration.md` as fixed before any post-v5
  model output is inspected.
- Paid API audit is deferred until v5/open-model tables are locked. The cost
  plan estimates GPT-5.4/GPT-5.5 plus Gemini 2.5 Pro can fit under a $20 cap
  under answer-only token budgets; re-check pricing before spending.
- Threats-to-validity note now records dataset, evaluation, mechanism, and
  scope risks plus safe claim boundaries.
- Dataset-card draft now describes validation-200 sources, fields, splits,
  quality status, intended uses, and limitations.

## Current Compute State

- Active Kaggle jobs: none.
- Last completed kernels:
  - `munimthahmid/qwen3-4b-generated-bn-dev50`
  - `munimthahmid/qwen3-4b-generated-en-dev50`
  - `munimthahmid/qwen25-3b-generated-bn-dev50`

## Next Priority

Return to the highest-value blocker:

1. Human-review `data/slices/validation_200_v5_review_queue.csv`.
2. Calibrate on `reports/validation200_v5_review_calibration_set.md`.
3. Use the impact-ordered packets or interactive helper.
4. Run the validator with `--require-complete`.
5. Freeze v5 only after the queue is complete.
6. Follow `reports/v5_analysis_preregistration.md` and
   `reports/post_v5_rerun_protocol.md`.
7. Defer more generated-view GPU until either v5 is complete or a better
   generated-English source is selected.
