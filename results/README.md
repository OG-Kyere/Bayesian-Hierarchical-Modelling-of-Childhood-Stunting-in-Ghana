# Results

This directory contains only **aggregate, non-identifying derived outputs** from the 2022 Ghana DHS analysis.

## What is public here

- `tables/descriptive_all.csv`: exact aggregate data behind the descriptive figures.
- `tables/analysis_sample_summary.csv`: analytic-sample counts and clustering summary.
- `tables/household_structure.csv`: distribution of eligible children per household.
- `tables/descriptive_weighted.csv`: first validated descriptive extract retained for audit history.
- `figures/`: publication-ready descriptive SVG figures.
- model-summary tables will be added only after each Bayesian model has been successfully fitted and checked.

## What is deliberately not public

No raw DHS file and no row-level child or household extract is stored in this repository. The source microdata are licensed by The DHS Program and must be obtained independently by authorized users.

A researcher with authorized access can reproduce the public outputs by placing `GHPR8CFL.DTA` under `data/raw/` and running:

```bash
python src/02_descriptive_analysis.py
```

The Bayesian model scripts use the same principle: code and aggregate outputs are public; DHS microdata remain local.
