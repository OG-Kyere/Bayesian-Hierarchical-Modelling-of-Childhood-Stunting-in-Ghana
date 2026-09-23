# Publication-strengthening roadmap

The project is already suitable for thesis drafting. The remaining work is aimed at making the manuscript more defensible and reviewer-resistant rather than simply adding more variables.

## Highest-priority upgrades

### 1. Final production MCMC
Run all preferred models in the pinned environment with at least four chains, 1,000 warmup iterations, and 1,000 retained draws per chain. Require:

- zero divergences;
- R-hat <= 1.01 for all reported parameters;
- bulk and tail ESS >= 400 for key fixed effects and variance parameters;
- acceptable BFMI;
- no problematic tree-depth saturation.

Use `src/10_final_production_diagnostics.py` to summarize the locked fits.

### 2. Predictive comparison with PSIS-LOO
The current WAIC difference between harmonized Model 2 and Model 3 is negligible relative to its uncertainty, and the present WAIC diagnostics are not ideal. The final comparison should therefore use PSIS-LOO with Pareto-k diagnostics. If influential observations make PSIS unreliable, use exact/K-fold alternatives rather than forcing a ranking.

### 3. Functional-form sensitivity for age
The main analysis uses six age groups. This is interpretable but arbitrary. A spline-age sensitivity model is included in `src/11_age_functional_form_sensitivity.py`.

An independent GEE check already shows that replacing age categories with a cubic spline barely changes the major fixed-effect conclusions.

### 4. WASH coding sensitivity
The primary model uses improved/unimproved source/facility types. The detailed sensitivity model in `src/12_wash_coding_sensitivity.py` separates:

- improved water;
- unprotected groundwater;
- surface water;
- improved sanitation;
- other unimproved sanitation;
- open defecation.

The independent GEE diagnostic suggests that the binary water association is driven most clearly by surface-water exposure, while adjusted sanitation associations remain weak.

## Findings from the new independent robustness check

On the 4,503-child complete maternal-information sample, household-clustered GEE produced:

### Age functional-form robustness
Changing from age categories to a cubic spline gave almost identical adjusted estimates:

- unimproved water OR: 1.40 vs 1.39;
- unimproved sanitation OR: 1.10 vs 1.10;
- higher maternal education OR: 0.40 vs 0.39;
- male sex OR: 1.40 vs 1.42;
- richest vs poorest OR: 0.43 vs 0.43.

This suggests the key conclusions are not artifacts of the six age bands.

### More detailed WASH coding
Compared with improved water sources:

- surface water OR: 1.43 (95% CI 1.12–1.83);
- unprotected groundwater OR: 1.34 (0.93–1.94).

Compared with improved sanitation:

- open defecation OR: 1.18 (0.93–1.50);
- other unimproved sanitation OR: 0.94 (0.70–1.26).

These are diagnostic GEE estimates rather than the final Bayesian results. They motivate the Bayesian detailed-WASH sensitivity analysis rather than replacing it.

## What not to do

- Do not keep adding unrelated covariates simply to make the thesis look more complex.
- Do not describe associations as causal.
- Do not claim Bayesian modelling of stunting in Ghana is novel by itself.
- Do not rank Model 2 and Model 3 strongly when predictive differences are negligible.
- Do not interpret binary improved/unimproved WASH variables as complete JMP service levels.
- Do not report random-effect variance estimates as final until the longer production runs meet the diagnostic thresholds.

## Manuscript contribution to emphasize

The strongest contribution remains the combination of:

1. the latest nationally representative 2022 Ghana DHS;
2. explicit separation of household and community heterogeneity;
3. sequential WASH and maternal-education extensions;
4. same-sample model comparisons;
5. survey-weight, prior, missing-data, functional-form, and WASH-coding sensitivity;
6. transparent posterior predictive and predictive-model diagnostics.

This is stronger than presenting the paper as merely another list of stunting predictors.
