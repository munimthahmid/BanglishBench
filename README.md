# BanglishBench

BanglishBench is a public benchmark release for measuring how reliably large
language models handle Latin-script Banglish compared with native-script Bangla
and English.

The benchmark is centered on paired script views: the same underlying item is
evaluated across Bangla, reviewed Banglish, and English variants so that script
choice is measured directly instead of being mixed with item difficulty.

## Repository Layout

- `data/slices/`: benchmark slices, manifests, review queues, and public evaluation inputs.
- `results/tables/`: compact result tables used in the public report.
- `results/analysis/`: curated analysis outputs for robustness checks and diagnostics.
- `reports/`: public experiment notes, dataset cards, and reproducibility summaries.
- `scripts/`: analysis and artifact-generation scripts.
- `paper/`: source and compiled PDF for the technical report.

Local credentials, raw model outputs, API payloads, Kaggle job assets, slide
decks, virtual environments, and LaTeX build byproducts are intentionally
excluded from the repository.

## Technical Report

The report source is in `paper/`, and the compiled PDF is:

`paper/banglishbench-report.pdf`

To rebuild:

```bash
cd paper
pdflatex -interaction=nonstopmode -halt-on-error banglishbench-report.tex
pdflatex -interaction=nonstopmode -halt-on-error banglishbench-report.tex
```

## Key Artifacts

- Main validation report: `reports/main_results_validation200_v5.md`
- Frontier/API panel: `reports/frontier_api_panel_validation200_v5.md`
- BEnQA human-reviewed extension freeze: `reports/benqa_extended_1000_v1_human_review_freeze.md`
- BEnQA 974-row scale summary: `reports/benqa_human_gold_974_scale_summary.md`
- Dataset card: `reports/dataset_card_validation200.md`
- Reproducibility manifest: `reports/reproducibility_artifact_manifest.md`

## License

Code is released under the MIT License. Benchmark data, reports, figures, and
other written materials created by the author are released under CC BY 4.0,
except for third-party source datasets or materials, which remain under their
original licenses.
