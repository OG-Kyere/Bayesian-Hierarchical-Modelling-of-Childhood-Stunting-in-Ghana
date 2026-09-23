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

## What is deliberately not public

No raw DHS file and no row-level child or household extract is stored in this repository. The source microdata are licensed by The DHS Program and must be obtained independently by authorized users.

A researcher with authorized access can reproduce the public outputs by placing `GHPR8CFL.DTA` under `data/raw/` and running:

```bash
python src/02_descriptive_analysis.py
```

The Bayesian model scripts use the same principle: code and aggregate outputs are public; DHS microdata remain local.
