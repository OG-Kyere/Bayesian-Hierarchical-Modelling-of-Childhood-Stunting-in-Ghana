# Analysis and Thesis Audit — 23 September 2026

This document records major consistency checks and corrections performed before drafting Chapter 5.

## Corrections completed

### DHS population definition
- Corrected the interpretation of `hv103`.
- `hv103 = yes` indicates that the person slept in the household the preceding night and is used to reproduce the DHS de facto anthropometry population.
- The earlier wording "usual household member" was removed.

### Analytic-sample validation
- Analytic sample: 4,928 children with valid height-for-age measurements.
- Stunted children: 927.
- Survey communities represented: 616.
- Households represented: 3,545.
- Sum of rescaled DHS weights: 4,292.97, matching the official weighted height-for-age denominator of 4,293 after rounding.
- Weighted stunting prevalence and Taylor-linearized SE reproduce the official GDHS estimates.

### Survey-design descriptive inference
- Descriptive prevalence estimates now use `hv005` weights.
- Taylor-linearized uncertainty uses `hv021` as PSU and `hv022` as sampling stratum.
- Aggregate CSVs and descriptive figures include 95% design-based confidence intervals.

### WASH coding
- `hv201`: drinking-water source.
- `hv205`: sanitation facility type.
- Groupings are described as improved versus unimproved **source/facility types**, not full JMP basic or safely managed service levels.
- This distinction is reflected in the thesis, variable dictionary, and code.

### Maternal education
- `hc61` is used for maternal educational attainment.
- 425 children (8.6%) have missing linked maternal education.
- Model 3 complete-case sample: 4,503 children.
- Harmonized Model 2 is fitted to the same 4,503 children before Model 2–3 comparisons.
- A full-sample missing-category sensitivity analysis was also performed.

### LaTeX / Overleaf
- Corrected malformed math notation and line breaks in Chapters 2–3.
- Added SVG, float, microtype, and caption support.
- Chapter 4 now embeds descriptive and Bayesian figures.
- Citation-key audit: no missing citation keys and no duplicate BibTeX keys at the time of this audit.
- University-specific front matter remains intentionally unconfigured until the official thesis formatting guide/template is available.

## Current Bayesian model sequence

### Model 1
Core child/socioeconomic covariates + household and community random intercepts.

Current fit:
- n = 4,928
- 4 chains × 400 retained draws
- 0 divergences
- max key-parameter R-hat ≈ 1.018

Main variance result:
- community SD median ≈ 0.416
- household SD median ≈ 1.066
- community ICC ≈ 0.038
- household VPC ≈ 0.246
- community MOR ≈ 1.49
- household MOR ≈ 2.76

### Model 2
Model 1 + WASH.

Full sample:
- n = 4,928
- unimproved water OR ≈ 1.36 (1.05–1.78)
- unimproved/no sanitation OR ≈ 1.16 (0.91–1.45)

### Harmonized Model 2
Same WASH model on the 4,503-child maternal-education-complete sample.

### Model 3
Harmonized Model 2 + maternal education.

Key posterior medians:
- male OR ≈ 1.50
- age 24–35 months OR ≈ 2.98
- unimproved water OR ≈ 1.50
- unimproved/no sanitation OR ≈ 1.11
- maternal higher education OR ≈ 0.38
- richest vs poorest OR ≈ 0.36

All current Model 1–3 runs had zero divergences. Fixed effects show strong cross-chain agreement. Hierarchical SDs mix more slowly and will be confirmed with longer production chains before submission.

## Sensitivity analyses completed

- tighter prior scale
- wider prior scale
- survey-weight pseudo-posterior with weights normalized to mean 1
- missing-maternal-education category sensitivity
- GEE clustering diagnostic
- posterior predictive checks
- harmonized Model 2 vs Model 3 conditional WAIC comparison

The pseudo-weighted variance decomposition is not used substantively because its community-SD chain mixing was unsatisfactory. Fixed-effect sensitivity results are reported transparently.

## Remaining production checks before final submission

1. Refit the preferred final models with longer chains in a stable pinned environment.
2. Confirm R-hat and effective sample sizes for household/community SDs.
3. Regenerate final posterior tables, PPCs, and predictive-comparison outputs from the locked production posterior objects.
4. Run a full Overleaf compilation with the official university thesis template.
5. Freeze package versions and analysis seeds for the submitted manuscript/thesis version.
6. Only after the production results are locked should Chapter 5 wording be treated as final.

This audit is intended to prevent discrepancies between thesis prose, code, public aggregate outputs, and final model results.
