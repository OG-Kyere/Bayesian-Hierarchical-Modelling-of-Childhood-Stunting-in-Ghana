# Bayesian model run log

This file distinguishes the **locked manuscript results** from later local reproducibility reruns.

The strengthened eight-chain Model 3 summaries remain the primary manuscript results. A separate four-chain local rerun reproduced the analytic sample, main fixed-effect pattern, sampler health, and sensitivity conclusions; those results are documented in `docs/local_reproduction_2026-09-24.md`.

## Locked manuscript fits

| Fit | Sample | Posterior draws | Divergences | Diagnostic note | Status |
|---|---:|---:|---:|---|---|
| Model 1: household + community | 4,928 | archived aggregate summary | 0 | Household variation larger than community variation | Locked supporting result |
| Model 2: + WASH | 4,928 | archived aggregate summary | 0 | WASH extension | Locked supporting result |
| Model 2 harmonized | 4,503 | strengthened comparison run | 0 | Same-sample PSIS-LOO comparison with Model 3 | Locked comparison |
| Model 3: + maternal education | 4,503 | 4,000 across 8 chains | 0 | BFMI 0.51–0.66; fixed effects mix well; variance SDs slower | Locked primary result |
| Survey-weight sensitivity | 4,503 | sensitivity run | 0 | Water estimate less precise under weighting | Locked sensitivity |
| Missing-maternal-category sensitivity | 4,928 | sensitivity run | 0 | Main fixed-effect conclusions preserved | Locked sensitivity |
| Age-spline sensitivity | 4,503 | sensitivity run | 0 | Main covariate estimates stable | Locked sensitivity |
| Detailed-WASH sensitivity | 4,503 | sensitivity run | 0 | Surface-water association clearest | Locked sensitivity |

## Strengthened Model 3 diagnostics

The primary Model 3 diagnostic run combines eight independent chains with 500 warmup and 500 retained draws per chain, giving 4,000 retained posterior draws.

- divergences: 0
- BFMI range: 0.51–0.66
- no maximum-tree-depth hits
- maximum fixed-effect R-hat: about 1.003
- fixed-effect bulk ESS values above 2,200
- community SD R-hat: about 1.021; bulk ESS about 544
- household SD R-hat: about 1.018; bulk ESS about 524

The fixed effects are well mixed. The two hierarchical SDs remain the slowest-mixing parameters, so exact variance-component intervals are interpreted with more caution than the fixed effects.

## Posterior predictive checks

The strengthened Model 3 posterior predictive checks reproduce the observed overall prevalence and the age-specific prevalence pattern.

## Predictive comparison

The locked observation-level PSIS-LOO comparison on the common 4,503-child sample gives:

- Model 2 harmonized ELPD-LOO: -2012.39
- Model 3 ELPD-LOO: -2011.47
- difference: 0.92
- SE of difference: 3.38
- Model 2 observations with Pareto k > 0.70: 5
- Model 3 observations with Pareto k > 0.70: 0
- observations with Pareto k > 1: 0 in both models

The difference is much smaller than its SE, so the models are treated as predictively similar. This is an observation-level conditional comparison within the fitted hierarchy, not a validation exercise for entirely new households or communities.

A later local four-chain rerun produced a somewhat different numerical LOO estimate but the same substantive conclusion; see `docs/local_reproduction_2026-09-24.md`. Ordinary reruns of `src/09_model_comparison_ppc.py` no longer overwrite the locked comparison unless `--write-final` is supplied intentionally.

## Independent GEE check

The exchangeable GEE working correlations were approximately:

- household: 0.154
- community: 0.024

These are not Bayesian ICCs. They independently support the conclusion that residual dependence is substantially stronger within households than between survey communities.
