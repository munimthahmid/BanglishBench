# Script Matters

This repository contains the public thesis materials for:

**Script Matters: Measuring Latin-Script Banglish Robustness in Bangla LLMs**

The main thesis source is in `Thesis Template UG/`. The compiled thesis PDF is:

`Thesis Template UG/buetcseugthesis.pdf`

## Repository Contents

- `Thesis Template UG/chapters/`: thesis chapter sources.
- `Thesis Template UG/figures/`: thesis figures.
- `reports/`: written experiment reports and reproducibility notes.
- `results/tables/`: curated thesis-facing result tables.
- `results/analysis/`: curated analysis CSV outputs.
- `data/slices/`: public evaluation and review slices used by the study.
- `scripts/`: analysis, audit, and table/figure generation scripts.
- `presentation/`: defense presentation source and public assets.

Local credentials, raw model runs, API payloads, Kaggle job assets, virtual
environments, and LaTeX build byproducts are intentionally excluded by
`.gitignore`.

## Build

From the thesis directory:

```bash
cd "Thesis Template UG"
pdflatex -interaction=nonstopmode -halt-on-error buetcseugthesis.tex
pdflatex -interaction=nonstopmode -halt-on-error buetcseugthesis.tex
```

## Key Artifacts

- Main validation report: `reports/main_results_validation200_v5.md`
- Frontier/API panel: `reports/frontier_api_panel_validation200_v5.md`
- BEnQA human-reviewed extension freeze: `reports/benqa_extended_1000_v1_human_review_freeze.md`
- BEnQA 974-row scale summary: `reports/benqa_human_gold_974_scale_summary.md`
- Dataset card: `reports/dataset_card_validation200.md`
- Reproducibility manifest: `reports/reproducibility_artifact_manifest.md`
