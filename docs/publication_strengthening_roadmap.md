# What is left before submission

Most of the statistical work is now done. This file records the remaining jobs that would actually improve the paper, rather than adding more analysis for its own sake.

## Locked production result

The statistical analysis is closed for the current submission. The strengthened Model 3 run uses eight chains and 4,000 retained posterior draws and is the locked primary result set. It had:

- zero divergences;
- BFMI between 0.51 and 0.66;
- no tree-depth saturation;
- fixed-effect R-hat values near 1.00;
- bulk ESS above 500 for both random-effect SDs.

The SD R-hat values remain around 1.02, so exact variance-component interval endpoints are interpreted more cautiously than the fixed effects. A longer run could improve Monte Carlo precision in future work, but it is not required for the current submission and should not trigger another model-selection cycle.

## Model comparison

The old WAIC-only comparison has been superseded by PSIS-LOO.

For harmonized Model 2 versus Model 3, the ELPD difference is only about 0.92 with SE 3.38. Model 3 has no Pareto-k values above 0.70; Model 2 has five.

I treat those models as predictively similar. Maternal education stays in Model 3 because it is substantively relevant, not because Model 3 clearly predicts better.

## Robustness checks already completed

The main conclusions have now been checked against:

- tighter and wider priors;
- a survey-weight pseudo-posterior;
- missing maternal education retained as a category;
- a spline rather than grouped age;
- more detailed WASH coding;
- an independent GEE clustering analysis;
- posterior predictive checks.

The age specification makes very little difference to the main coefficients. In the detailed WASH model, the water association is clearest for surface-water use. Sanitation remains weak after adjustment.

## What I do not plan to add

I do not plan to keep adding covariates simply to make the model look more complicated. I also do not plan to add spatial modelling unless it becomes a separate research question.

The paper is stronger when it stays focused on:

1. household versus community residual heterogeneity;
2. how that pattern changes after WASH and maternal education;
3. whether the conclusions survive reasonable alternative specifications.

## Submission work still pending

The main remaining tasks are now practical rather than analytical:

- finalize authorship, correspondence details, ORCID (if available), funding, conflicts, and CRediT roles;
- keep the ethics statement limited to the documented GDHS approvals and authorized secondary-data use;
- preserve the executed-environment record associated with the locked analyses;
- render the references in TMIH's Vancouver style;
- complete the TMIH-specific formatting and submission checklist.

The public manuscript/result consistency check and repository-integrity check are automated in GitHub Actions and currently pass. Publisher/official records have also been checked for all references cited in the current manuscript.

A longer variance-component run remains optional future work if tighter Monte Carlo precision is desired; it is not a pre-submission requirement and does not resolve any contradiction in the substantive findings.

At this point, clarity, metadata, and reproducibility matter more than extra model complexity.
