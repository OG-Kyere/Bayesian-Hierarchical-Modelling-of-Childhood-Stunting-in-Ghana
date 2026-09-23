# Bayesian diagnostics — current status

This note summarizes the diagnostic position of the main hierarchical models as of 23 September 2026.

## Data reconstruction

Rebuilding the analytic sample directly from the authorized PR recode reproduces the project outputs:

- 4,928 children
- 927 stunted children
- 3,545 households
- 616 survey communities
- weighted denominator: 4,292.97
- weighted stunting prevalence: 17.385%

These numbers match the descriptive tables used in the thesis and manuscript.

## Independent clustering check

A separate logistic GEE analysis gives an exchangeable working correlation of about 0.154 when observations are grouped by household and about 0.024 when grouped by community.

I do not use those GEE correlations as substitutes for the Bayesian variance components. They are useful because they independently point in the same direction: residual dependence is much stronger within households.

## Main Bayesian diagnostics

### Model 1

- 1,600 retained posterior draws
- 0 divergences
- maximum key-parameter R-hat: 1.018
- minimum key-parameter ESS: about 165

The fixed effects are stable; the household SD mixes more slowly.

### Model 2, full sample

- 1,200 retained posterior draws
- 0 divergences
- maximum key-parameter R-hat: 1.012
- minimum key-parameter ESS: about 162

### Harmonized Model 2

The later strengthened run has 2,000 retained draws, 0 divergences, maximum R-hat about 1.013, and minimum bulk ESS about 379. Its PSIS-LOO comparison with Model 3 has five observations with Pareto k above 0.70 and none above 1.

### Strengthened Model 3

The strongest diagnostic run currently available combines eight independent chains with 500 warmup and 500 retained draws per chain:

- 4,000 retained posterior draws
- 0 divergences
- BFMI range: 0.51–0.66
- no maximum-tree-depth hits
- maximum fixed-effect R-hat: about 1.003
- fixed-effect bulk ESS values above 2,200
- community SD R-hat: 1.021, bulk ESS about 544
- household SD R-hat: 1.018, bulk ESS about 524

The corresponding variance summaries are:

- community SD: 0.389 (0.067–0.610)
- household SD: 1.234 (0.940–1.535)
- community ICC: 0.030
- household VPC: 0.307
- community MOR: 1.45
- household MOR: 3.24

The fixed effects are very well behaved. The two SDs remain the only parameters for which I would still like a cleaner Monte Carlo margin.

## Posterior predictive checks

The final model reproduces the observed overall prevalence closely:

- observed complete-case prevalence: 18.45%
- replicated posterior-predictive mean: 18.41%

The observed prevalence in each age group also falls inside the corresponding posterior-predictive interval.

## Sensitivity checks

The main fixed-effect pattern survives tighter/wider priors, alternative treatment of missing maternal education, age splines, and more detailed WASH coding.

The survey-weight pseudo-posterior weakens the precision of the water result. The primary Model 3 estimate is OR 1.50 (1.15–1.99); the weighted sensitivity gives OR 1.38 (0.90–2.07). I therefore describe the water association as stable in direction but more sensitive in precision than the age, sex, wealth, and higher-education findings.

## PSIS-LOO

For harmonized Model 2 and Model 3:

- Model 2 ELPD-LOO: -2012.39
- Model 3 ELPD-LOO: -2011.47
- difference: 0.92
- SE of difference: 3.38

Model 3 has no Pareto-k values above 0.70 and a maximum of about 0.69. Model 2 has five values above 0.70 and a maximum of about 0.79. Neither model has k above 1.

This is an observation-level comparison within the fitted hierarchy. It is not a test of prediction for completely new households or communities.

## Bottom line

The fixed-effect results and the household-versus-community contrast are supported by several independent checks. The main remaining diagnostic caution is the slower mixing of the two hierarchical SDs.

For a final locked submission, I would still prefer one clean longer run in the pinned environment if computing resources allow it. If that run is not feasible, the manuscript should keep the current wording: strong fixed-effect convergence, stable household-versus-community contrast, and more caution around the exact variance-component intervals.
