# Results

Everything in this folder is an aggregate, non-identifying output from the 2022 Ghana DHS analysis.

The raw DHS records stay outside the repository.

## Descriptive results

The main descriptive files are:

- `tables/descriptive_all.csv` — weighted prevalence estimates, Taylor-linearized SEs, and 95% CIs;
- `tables/analysis_sample_summary.csv` — sample, household, and community counts;
- `tables/household_structure.csv` — number of eligible children per household;
- `figures/stunting_by_*.svg` — descriptive figures used in the thesis and manuscript.

`descriptive_all.csv` is the authoritative source for the descriptive numbers quoted in the text.

## Bayesian results

The strengthened final Model 3 summaries are:

- `tables/model3_final_8chain_key_or.csv`
- `tables/model3_final_8chain_variance_summary.csv`
- `tables/model3_final_8chain_parameter_diagnostics.csv`
- `tables/model3_final_8chain_sampler_diagnostics.csv`
- `tables/model3_final_8chain_loo_summary.csv`

Those are the files to check first if a manuscript number looks wrong.

Earlier Model 1 and Model 2 summaries are retained because they show how the household/community variance structure changes as WASH and maternal education are added.

## Sensitivity analyses

The folder also contains aggregate results for:

- tighter and wider priors;
- the survey-weight pseudo-posterior;
- missing maternal education retained as a category;
- spline-based age modelling;
- detailed WASH coding;
- posterior predictive checks;
- harmonized Model 2 versus Model 3 PSIS-LOO comparison.

The current predictive comparison is based on **PSIS-LOO**. Older WAIC outputs remain in the repository as part of the analysis history but are not the main model-comparison result used in the manuscript.

## Figures

The main Bayesian figures include:

- `figures/model3_posterior_or_forest.svg`
- `figures/model_variance_comparison.svg`
- `figures/model3_ppc_age.svg`

All public figures are generated from aggregate outputs. No row-level DHS records are stored here.
