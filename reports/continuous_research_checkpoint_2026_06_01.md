# Continuous Research Checkpoint: 2026-06-01

## Current State

The frozen validation-200 v5 benchmark remains locked. Manual review is
complete, required and optional post-v5 open-model reruns are complete, and the
local dashboard is green. Work today focused on a no-spend BEnQA semantic-cue
confound audit for the Qwen3 reviewed-Banglish D-attractor.

## BEnQA Option Semantic-Cue Audit

The new audit checks whether Qwen3's reviewed-Banglish D-attractor can be
reduced to simple option cues: composite roman-marker answers such as
`i, ii, o iii`, numeric/formula-like option strings, or all/none/both markers.

Artifacts:

- `scripts/analyze_v5_benqa_option_semantic_cues.py`
- `reports/v5_benqa_option_semantic_cues.md`
- `results/analysis/v5_benqa_option_semantic_cues_items.csv`
- `results/analysis/v5_benqa_option_semantic_cues_summary.csv`

Key result:

- D has a composite/numeric/formula cue on 97/144 BEnQA rows, leaving 47/144
  rows where D has no simple cue under this audit.
- On those no-cue rows, Qwen3-4B still predicts D on 38/47 rows, versus 9/47
  for Qwen2.5-3B and 4/47 for Qwen2.5-7B 8-bit.
- Among correct non-D alternate-script predictions where D has no cue, Qwen3
  switches to wrong reviewed-Banglish D on 15/18 Bangla rows and 18/23 English
  rows. The Qwen2.5 Bangla-side counts are only 1/11 and 3/21.

Interpretation: composite and numeric/formula-like choices are real local
features, but they do not explain away Qwen3's D-attractor. This remains a
behavioral confound audit, not a causal internal-mechanism claim.

## QA Snapshot

- Full local QA rerun completed on 2026-06-02 after the interrupted runner was
  restarted from the top.
- Dashboard: 52 rows, 0 blocked, 0 failing.
- Research log compactness: 56 checks, 0 issues; `research_log.md` is 237
  lines / 13.0 KB.
- Secret hygiene: 865 files checked, 0 suspicious findings.
- Local artifact references: 3,804 checked, 0 unexpected missing, 19 expected
  future references.
- Reproducibility manifest: 863 non-secret artifacts.
