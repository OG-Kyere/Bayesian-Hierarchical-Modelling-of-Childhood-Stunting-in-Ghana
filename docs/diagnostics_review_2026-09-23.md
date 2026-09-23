# Bayesian Diagnostics Review — 23 September 2026

This report summarizes the current diagnostic status of the childhood-stunting hierarchical models and the fresh data-level checks run against the authorized 2022 Ghana DHS PR recode.

## Fresh data reconstruction check

The analytic sample was reconstructed directly from the PR file using the current project rules:

- de facto child population: `hv103 = yes`
- age: 0–59 months
- valid height-for-age z-score: `hc70` between -600 and 600
- stunting: `hc70 < -200`

The reconstruction reproduced:

- 4,928 children
- 927 stunted children
- 3,545 households
- 616 communities
- weighted denominator: 4,292.97481
- weighted stunting prevalence: 0.1738503
- unweighted stunting prevalence: 0.1881088

These values agree with the current repository outputs and the official survey totals used in the thesis validation.

## Independent clustering diagnostic

A fresh logistic GEE analysis with exchangeable working correlation produced:

- household working correlation: 0.1539
- community working correlation: 0.0237

Both GEE fits converged.

This independently supports the central hierarchical finding that residual dependence is materially stronger within households than within communities.

Selected GEE estimates were also stable:

- male vs female OR: ~1.38
- age 24–35 vs 0–5 months OR: ~2.66 (household-grouped GEE)
- richest vs poorest OR: ~0.28
- rural vs urban OR: ~0.88, with interval including 1

These directions are consistent with the Bayesian models.

## Bayesian convergence diagnostics

### Model 1
- posterior draws: 1,600
- divergences: 0
- maximum key-parameter R-hat: 1.0179
- minimum key-parameter ESS: 165
- community SD median: 0.416
- household SD median: 1.066

Assessment: fixed effects are well behaved; household SD mixes more slowly than ideal.

### Model 2 — full sample
- posterior draws: 1,200
- divergences: 0
- maximum key-parameter R-hat: 1.0116
- minimum key-parameter ESS: 162

Assessment: broadly acceptable for current thesis drafting; variance parameters still mix more slowly than fixed effects.

### Model 2 — harmonized maternal-education sample
- posterior draws: 1,200
- divergences: 0
- maximum key-parameter R-hat: 1.0364
- minimum key-parameter ESS: 172

Assessment: fixed effects remain stable, but hierarchical SD diagnostics are not yet publication-grade.

### Model 3
- posterior draws: 1,200
- divergences: 0
- maximum key-parameter R-hat: 1.0333
- minimum key-parameter ESS: 120

Assessment: substantive fixed-effect conclusions are stable, but the community and household SDs require a longer final production run.

## Posterior predictive checks

Current Model 3 posterior predictive summaries reproduce the observed stunting pattern well:

- observed overall prevalence: 0.1845
- replicated mean: 0.1841
- replicated 95% range: 0.1719–0.1979

Observed age-specific prevalence lies inside the corresponding posterior-predictive intervals for all six age groups.

Assessment: no major lack of fit is visible for the overall or age-specific prevalence summaries currently checked.

## Prior sensitivity

The major substantive conclusions are stable under tighter and wider priors.

Examples:

- unimproved water:
  - tight prior OR: 1.48
  - primary OR: 1.50
  - wide prior OR: 1.48

- maternal higher education:
  - tight prior OR: 0.44
  - primary OR: 0.38
  - wide prior OR: 0.35

Assessment: the principal fixed-effect findings are not being driven by the primary prior scale.

## Survey-weight sensitivity

The weighted pseudo-posterior preserves the main directions for sex, age, wealth, and higher maternal education.

The unimproved-water association becomes less precise:

- primary OR: 1.50 (1.14–2.00)
- weighted OR: 1.38 (0.90–2.07)

Assessment: water should be described as supported by the primary model but sensitive in precision to weighting.

The weighted variance decomposition should not be used substantively until its hierarchical SD chains mix adequately.

## Missing maternal-education sensitivity

Treating missing maternal education as an explicit category on the full 4,928-child sample preserves the main conclusions.

Examples:

- unimproved water OR: 1.35 (1.01–1.74)
- maternal higher education OR: 0.38 (0.22–0.63)
- missing maternal education OR: 1.11 (0.80–1.53)

Assessment: the main fixed-effect conclusions are not strongly driven by the 4,503-child complete-case restriction.

## Predictive model comparison

The current harmonized Model 2 vs Model 3 WAIC comparison shows almost no predictive difference:

- Model 2 WAIC: 3983.30
- Model 3 WAIC: 3982.69
- difference: ~0.61
- ELPD difference SE: ~4.66

However, the current WAIC output also shows many observations with pointwise log-likelihood variance greater than 0.4:

- Model 2: 562 observations
- Model 3: 542 observations

This is a warning that fine model ranking by WAIC is unstable.

### Correction made

The repository has now been updated so Models 2 and 3 explicitly save pointwise log-likelihood in their production InferenceData objects.

The model-comparison script has also been upgraded to compute:

- PSIS-LOO
- Pareto-k diagnostics
- stacking-based LOO comparison
- WAIC as a secondary check
- overall PPC summary

PSIS-LOO should be preferred over WAIC for the final locked comparison when Pareto-k diagnostics are satisfactory.

## Code/reproducibility issues identified and fixed

1. Models 2 and 3 did not explicitly request pointwise log-likelihood, although the model-comparison script expected it.
   - Fixed with `idata_kwargs={"log_likelihood": True}`.

2. The model-comparison script relied only on WAIC.
   - Updated to include PSIS-LOO and Pareto-k diagnostics.

3. The global execution environment currently has an incompatible PyMC/ArviZ combination.
   - Repository requirements already pin ArviZ to a compatible pre-1.0 release.
   - Final diagnostics should be rerun inside that pinned clean environment.

## Current diagnostic verdict

### Strong / reliable
- sample reconstruction
- weighted descriptive prevalence
- fixed-effect directions and magnitudes
- household > community clustering signal
- posterior predictive fit for overall and age-group prevalence
- prior sensitivity
- missing-maternal-information sensitivity

### Needs final production confirmation
- household and community SD intervals in Models 2 harmonized and 3
- weighted-model variance decomposition
- PSIS-LOO/Pareto-k model comparison
- BFMI and maximum tree-depth diagnostics from the final saved InferenceData objects
- final longer-chain R-hat and ESS for hierarchical SDs

## Recommended final production standard

For the locked thesis/manuscript run:

- 4 chains
- at least 1,000 warmup iterations per chain
- at least 1,000 retained draws per chain
- target_accept >= 0.95
- zero divergences
- R-hat <= 1.01 for all reported parameters
- bulk and tail ESS >= 400 for key fixed and variance parameters
- inspect BFMI and maximum tree depth
- save pointwise log-likelihood
- run PSIS-LOO and inspect Pareto-k
- regenerate all posterior tables and figures from the final saved InferenceData files

The current results are suitable for thesis drafting, but the final submitted variance-component estimates should come from that locked production run.
