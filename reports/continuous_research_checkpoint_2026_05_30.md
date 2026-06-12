# Continuous Research Checkpoint: 2026-05-30

## Current State

Validation-200 v5 is frozen and the two required post-v5 reruns are complete.

Reviewed slice:

- Source: `data/slices/validation_200_v5.jsonl`
- Items: 200
- Reviewed queue: 140/140 complete
- Labels: 126 `minor_edit`, 11 `major_edit`, 3 `bad`, 0 pending
- Freeze policy: keep all 200 rows and flag bad Banglish rows

Required post-v5 sensitivity:

| Model | v4 Banglish | v5 Banglish | Delta |
| --- | ---: | ---: | ---: |
| Qwen2.5-3B | 39/200 | 41/200 | +1.0 pts, CI [-1.0, +3.0] |
| Qwen3-4B | 47/200 | 49/200 | +1.0 pts, CI [0.0, +2.5] |

Interpretation:

- Reviewed cleanup slightly improves the required 3B and 4B rows; the optional
  7B row shifts slightly downward.
- The controlled Banglish weakness remains.
- Dataset QA is no longer the blocker.

## Completed Optional Kaggle Job

The optional Qwen2.5-7B v5 Banglish pinned retry completed:

- Kernel:
  `munimthahmid/qwen2-5-7b-8-bit-validation-200-v5-banglish-pinned`
- URL:
  `https://www.kaggle.com/code/munimthahmid/qwen2-5-7b-8-bit-validation-200-v5-banglish-pinned`
- Variants: `banglish_clean`
- Items: 200
- Model: `Qwen/Qwen2.5-7B-Instruct`
- Quantization: 8-bit
- Pinned stack:
  `transformers==4.43.4`, `accelerate==0.33.0`,
  `bitsandbytes==0.43.3`

Result:

| Model | v4 Banglish | v5 Banglish | Delta |
| --- | ---: | ---: | ---: |
| Qwen2.5-7B 8-bit | 48/200 | 47/200 | -0.5 pts, CI [-3.5, +2.5] |

Analysis:
`results/analysis/qwen25_7b_8bit_validation200_v5_vs_v4_banglish.md`

## Work Completed In This Block

- Condensed `research_log.md` from 6,701 lines to a restart-focused ledger.
- Preserved detailed run history in `results/experiment_log.md`.
- Refreshed stale v5 prose across Chapters 1, 3, 4, 5, 9, and 10.
- Refreshed abstract, defense Q&A, and defense slide outline.
- Refreshed selected qualitative examples and retired `banglamath_1697` as a
  current Qwen3 failure after its reviewed wording produced a correct answer.
- Made compiled-draft date generation dynamic.
- Extended `scripts/prepare_kaggle_model_run.py` with
  `--requirements-path` and `--bitsandbytes-requirement`.
- Extended `scripts/analyze_banglish_variant_sensitivity.py` to accept multiple
  baseline or candidate JSONL fragments; a backward-compatibility smoke
  reproduced the existing Qwen2.5-3B v4 39/200 -> v5 41/200 result.
- Packaged, launched, collected, and analyzed the pinned-stack optional 7B v5
  retry.
- Rechecked official OpenAI and Gemini pricing and refreshed the API-audit
  candidate set.
- Generated frozen-v5 paid-audit smoke assets and prompt budgets:
  30 smoke calls with about 1,736 heuristic input tokens and 600 full-triad
  calls with about 36,471 heuristic input tokens.
- Wired the v5 API smoke-subset and prompt-budget builders into
  `scripts/run_research_checks.py` so those assets stay synchronized.
- Refreshed the release-facing dataset card, threats note, results dashboard,
  write-up blueprint, and figure/table plan against frozen v5.
- Added a provider-neutral paid-audit request manifest, response importer, and
  no-spend execution runbook. The generated smoke manifest has 30 requests,
  excludes gold answers, and imports responses into the open-model schema.
- Added a separate strict-197 flagged-bad policy sensitivity report. Excluding
  the 3 flagged source-quality rows preserves negative reviewed-Banglish-vs-
  Bangla confidence intervals for all three thesis-facing Qwen rows.
- Promoted the reviewed-v5 all-200 Qwen table to the release-facing main result:
  Qwen2.5-3B 54/200 vs 41/200, Qwen2.5-7B 65/200 vs 47/200, and Qwen3-4B
  80/200 vs 49/200 for Bangla vs reviewed Banglish. Retained the historical
  v3/v4 table for provenance and mechanism analyses.
- Added an explicit Qwen2.5-3B qualification: its reviewed all-200
  Banglish-minus-Bangla interval reaches zero, while its historical v3 and
  strict-197 checks remain negative.
- Added explicit provenance labels for downstream noise, scaling, oracle,
  routing, and mitigation analyses that intentionally retain historical v3/v4
  outputs. These remain diagnostic support, not frozen-v5 main-result reruns.
- Added `scripts/build_v5_cross_script_diagnostics.py` and refreshed locally
  computable oracle, taxonomy, and privileged agreement-routing diagnostics
  against reviewed v5 Banglish while reusing unchanged Bangla/English outputs.
  Agreement routes are 41/200 -> 49/200 for Qwen2.5-3B, 47/200 -> 71/200 for
  Qwen2.5-7B 8-bit, and 49/200 -> 76/200 for Qwen3-4B. The 3B route interval
  crosses zero; 7B and Qwen3 remain clearly positive.
- Tightened `research_log.md` again by removing redundant artifact lists and
  compressing chronology while preserving restart-critical evidence.
- Added `scripts/run_fms_byte_generated_bn.py`, packaged the public
  `fms-byte/banglish_to_bangla` MBART candidate, recovered from the initial
  Kaggle P100 PyTorch incompatibility, and collected the pinned 36-item
  expanded-protection run.
- Tightened the shared generated-view auditor for scientific tokens, nested
  LaTeX identifiers, and genuine generated-BN Latin residue. Historical
  protected-v1 deterministic files now fail 9/36 and 10/36 tightened gates;
  separately regenerated expanded-v2 deterministic files pass 0/36 hard
  failures and 0/36 lexical warnings.
- Audited protected FMS-byte MBART: 0/36 hard failures, but 7/36 genuine
  Latin-residue warnings. Privileged dev-only native-reference similarity also
  ranks it behind expanded-v2 protected phonetic generation: mean CER 0.1855
  vs 0.0906.
- Added combined generated-BN candidate-preservation and native-reference
  similarity tables. Kept existing Qwen answer audits explicitly labeled as
  historical protected-v1 evidence; no generated-view route was escalated.

## Local QA

`python3 scripts/run_research_checks.py` passed on 2026-05-30.

- Thesis table integrity: 70 checks, 0 issues
- Thesis figure integrity: 25 checks, 0 issues
- v5 packet integrity: 6 checks, 0 issues
- Literature corpus: 33/33 complete
- Citation readiness: 33/33 complete
- Secret hygiene: 645 files checked, 0 suspicious findings
- Local artifact references: 2,528 checked, 0 unexpected missing
- Reproducibility manifest: 643 artifacts

## Next Actions

1. Decide whether the budgeted paid API smoke adds enough external-validity
   value to run.
