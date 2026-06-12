# Draft Thesis Figures

Generated from `results/tables/*.csv` by:

```bash
python3 scripts/build_thesis_figures.py
```

Files:

- `main_script_gap.svg`: Bangla/reviewed-Banglish/English accuracy for the frozen-v5 main Qwen table.
- `selfnorm_delta.svg`: self-normalization delta vs Banglish baseline.
- `cross_script_recovery.svg`: frozen-v5 reviewed Banglish, privileged agreement route, and oracle.

Regenerate after `scripts/build_thesis_tables.py` changes the source CSVs.
