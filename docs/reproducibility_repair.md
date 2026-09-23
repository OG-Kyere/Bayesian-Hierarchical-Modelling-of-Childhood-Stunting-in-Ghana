# Reproducibility repair and validation protocol — 2026-09-23

This is a retrospective repair after exploratory analysis, not a preregistration.

## Scientific target

Estimate conditional associations and residual household/community heterogeneity in nonspatial Bayesian logistic models of childhood stunting in the 2022 Ghana DHS. The primary heterogeneity estimand is the posterior distribution of `tau_household - tau_community`, with its 95% equal-tail interval and posterior probability of being positive. These are latent-scale model quantities, not causal effects or population shares of binary-outcome variance.

The contribution under evaluation is the stability of this decomposition to household clustering, WASH adjustment, maternal-information selection, priors, and survey-weight treatment. Novelty is not claimed solely from using Bayesian methods or a newer survey. Literature positioning still needs confirmation against closely related Ghana studies.

## Shared data preparation

`src/stunting_data.py` defines the sample once. De facto children aged 0–59 months with hc70 in [-600,600] are retained, and hc70 < -200 defines stunting. Composite household/child keys are checked for duplicates. Source/facility type definitions are explicit; missing/unmapped WASH information cannot silently become unimproved. The `other` source/facility response is retained as unimproved by the inherited coding choice; this decision should be examined if its small cell affects conclusions.

The survey variance calculation retains all 618 PSUs in 32 strata, including zero-contributing PSUs in a domain. The 616 clusters in the analytic sample are not the complete survey variance frame. The normal 1.96-SE confidence interval differs slightly from the report's 2-SE convention.

Missing maternal education is not no education. Model 3 and harmonized Model 2 use the identical ordered set of 4,503 children. A full-sample missing-category sensitivity is descriptive of an alternative specification, not a correction for nonrandom missingness. PR is retained as the main source to avoid silently selecting only children linked to KR. A causal missing-data identification claim is outside scope.

## Reproduce

With authorized `data/raw/GHPR8CFL.DTA`, Python 3.12, and dependencies from `requirements.txt`:

```bash
python -m unittest discover -s tests -v
python src/01_data_preparation.py
python src/02_descriptive_analysis.py
python src/bayesian_workflow.py --model m3 --run-id production-v1 --sampler nutpie
```

Repeat the last command for `m0`, `m1`, `m2`, `m2_harmonized`, `weighted`, `tight`, `wide`, `intercept`, and `missing` with the same run ID. The numbered scripts are compatibility entry points into that shared workflow. Defaults: 4 independent chains sampled concurrently, 2,000 tuning and 2,000 retained draws per chain, target acceptance 0.97, maximum tree depth 12. The combined sampled posterior is checkpointed before postprocessing. Completed posterior checkpoints are preserved privately between sessions. Each model/run directory is immutable: use a new run ID for a changed fit.

A system lacking Python C development libraries can use `PYTENSOR_FLAGS=cxx=` with the nutpie sampler; compilation uses Numba. This is an environment workaround, not a model change. The pinned pilot file records a historical environment and is separate from the repaired environment.

## Provenance and public/private boundary

A manifest records input and ordered-sample hashes, source-file hashes, git revision, model options, seeds, versions, sample sizes, and status. Restricted inputs, chain objects, log likelihood arrays, individual random effects, and full latent diagnostics stay in ignored local directories. Public outputs contain aggregate summaries only. NetCDF posterior objects are deliberately not pushed to GitHub.

`posterior_summary.csv` gives means/HDIs for parameters. `odds_ratios.csv` explicitly uses medians and equal-tail 95% intervals on exp(beta), avoiding ambiguity between HDIs and quantile intervals. The old `results/tables/model*` files are historical, not automatically replaced or presented as new production results.

## Required diagnostic gate

Every model, including weighted and prior sensitivities, must have at least four chains; finite rank-normalized R-hat below 1.01; bulk and tail ESS at least 400 for all sampled/derived parameters including latent random effects; zero divergences; minimum chain BFMI at least 0.3; and no maximum-tree-depth hits. Full diagnostics remain private; scientific-parameter diagnostics and aggregate extrema are public. These thresholds are necessary screening conditions, not proof of accuracy. Examine trace/rank plots and Monte Carlo errors for the quantities used in conclusions before scientific sign-off. Longer chains are not an automatic cure for bad posterior geometry.

No failed joint posterior is salvaged by selectively reporting fixed effects. A passing computational gate yields `diagnostics_passed_pending_scientific_review`, never automatic publication approval.

## Predictive and prior assessment

Prior predictive summaries are generated for each specification. The mean-zero intercept prior implies a broad, often high prevalence distribution; retain or revise it using external scientific justification, not optimization against observed results. The shifted-intercept scenario uses Normal(-1.5,1.5) as an explicitly labelled external sensitivity, not a sample-estimated prior.

PPCs use the exact fitted posterior, cover prevalence by age/sex/wealth, and include distributions of household/community zero/all-stunted groups and group-prevalence variability. A good marginal prevalence PPC alone cannot validate variance decomposition. PPC simulation after weighted fitting describes Bernoulli outcomes under draws from the pseudo-posterior; it does not simulate the survey selection process.

Run `python src/09_model_comparison_ppc.py --run-id production-v1` only after both harmonized fits pass diagnostics. It verifies ordered sample identity and observed outcomes, and exposes pointwise WAIC warnings. Conditional observation-level WAIC is exploratory and does not evaluate new-community prediction. No such predictive claim is made; grouped validation is needed if that objective is added.

## Survey inference and writing

Primary hierarchical posteriors are unweighted model-based inference. Mean-one survey-weight pseudo-posteriors are sensitivity analyses and do not establish design-calibrated uncertainty. If the scientific target requires population-calibrated hierarchical inference, the sampling model/weighting approach must be strengthened before making that claim.

The independent-report title page and abstract no longer imply a degree submission or confirmed Bayesian effects. Legacy chapter estimates are clearly marked exploratory; a passing final model sequence and scientific review are required before replacing that status. The journal manuscript excludes unsupported substantive estimates.
