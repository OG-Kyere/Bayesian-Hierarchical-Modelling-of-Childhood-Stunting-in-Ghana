# Analysis Protocol

## Working title
**Bayesian Hierarchical Modelling of Childhood Stunting in Ghana**

## Data source
2022 Ghana Demographic and Health Survey (GDHS).

## Outcome
Childhood stunting among children under five, defined from height-for-age z scores according to the DHS/WHO convention used in the survey data.

## Primary objective
Estimate associations between child-, household-, and community-level characteristics and childhood stunting while quantifying residual household and community heterogeneity.

## Core modelling framework
For child i in household j and community k:

```
Y_ijk ~ Bernoulli(p_ijk)
logit(p_ijk) = alpha + X_ijk beta + u_k + v_jk
```

where:
- `u_k` is a community-level random intercept.
- `v_jk` is a household-level random intercept.

## Planned model sequence
- Model 0: demographic and socioeconomic covariates + community random intercept.
- Model 1: Model 0 + household random intercept.
- Model 2: Model 1 + water and sanitation variables.
- Model 3: Model 2 + maternal education.
- Sensitivity analyses: survey weighting, alternative priors, and same-sample model comparisons.

## Key estimands
- Posterior odds ratios and credible intervals.
- Household and community variance components.
- Latent-scale ICCs.
- Median odds ratios (MORs).
- Posterior predictive performance.
- Model-comparison criteria appropriate to the final Bayesian workflow.

## Reproducibility principles
- All modelling decisions are documented before interpretation.
- Raw DHS files remain local and are never committed.
- Model comparisons will use harmonized samples where required.
- Pilot estimates are provisional until the full specification and sensitivity analyses are complete.

## Publication strategy
The thesis will provide full methodological and substantive detail. The journal manuscript will focus on the strongest defensible contribution established after literature review and model-comparison results.
