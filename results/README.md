> **Status correction (2026-09-23):** The Bayesian numerical results described below are legacy exploratory outputs, not validated publication findings. See `docs/reproducibility_repair.md` and per-run manifests under `results/runs/` for the repaired workflow and current validation status. Historical assertions of stability do not supersede the diagnostic gate.

# Results

This directory contains only **aggregate, non-identifying derived outputs** from the 2022 Ghana DHS analysis.

## What is public here

- `tables/descriptive_all.csv`: authoritative aggregate data behind the descriptive figures, including Taylor-linearized design SEs and 95% CIs.
- `tables/analysis_sample_summary.csv`: analytic-sample counts and clustering summary.
- `tables/household_structure.csv`: distribution of eligible children per household.
- `figures/`: publication-ready descriptive SVG figures.
- `tables/model*_variance_summary.csv`: aggregate posterior variance summaries for Models 1--3.
- `tables/model_comparison_variance.csv`: harmonized comparison of household/community heterogeneity across models.
- `tables/model3_key_effects.csv`: selected posterior odds ratios from Model 3.
- `tables/prior_sensitivity_key_effects.csv`: fixed-effect robustness under tighter and wider priors.
- `tables/survey_weight_sensitivity_key_effects.csv`: fixed-effect comparison under the weighted pseudo-posterior.
- `figures/model3_posterior_or_forest.svg`: Model 3 posterior odds-ratio forest plot.
- `figures/model_variance_comparison.svg`: household/community SD comparison across models.
- `tables/model3_ppc_summary.csv`: observed versus replicated prevalence for the Model 3 posterior predictive check.
- `figures/model3_ppc_age.svg`: overall and age-specific posterior predictive check figure.
- `tables/model_predictive_comparison.csv`: harmonized Model 2 versus Model 3 conditional WAIC comparison.

## What is deliberately not public

No raw DHS file and no row-level child or household extract is stored in this repository. The source microdata are licensed by The DHS Program and must be obtained independently by authorized users.

A researcher with authorized access can reproduce the public outputs by placing `GHPR8CFL.DTA` under `data/raw/` and running:

```bash
python src/02_descriptive_analysis.py
```

The Bayesian model scripts use the same principle: code and aggregate outputs are public; DHS microdata remain local.

## Repaired run outputs

New outputs are isolated under `runs/<run-id>/<model>/` and must be read together with `manifest.json`. The existing Bayesian tables and figures in this directory are retained as historical exploratory outputs, not regenerated production evidence. `src/11_report_runs.py` creates current status summaries and figures from exact run tables, emitting inferential figures only for fits passing the diagnostic gate. Scientific review is still required.
