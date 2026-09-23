# What is left before submission

Most of the statistical work is now done. This file records the remaining jobs that would actually improve the paper, rather than adding more analysis for its own sake.

## Final production run

The fixed effects are already stable across the main model and the sensitivity analyses. The only persistent computational weakness is the slower mixing of the household and community SDs.

The strengthened Model 3 run used eight chains and 4,000 retained posterior draws. It had:

- zero divergences;
- BFMI between 0.51 and 0.66;
- no tree-depth saturation;
- fixed-effect R-hat values near 1.00;
- bulk ESS above 500 for both random-effect SDs.

The SD R-hat values are still around 1.02. A longer clean run would be useful if the available computing environment makes that practical. It is not a reason to keep changing the model.

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

The main remaining tasks are practical:

- finalize authorship and affiliations;
- confirm the submitting institution's ethics/exemption wording;
- freeze the final software environment;
- render references in the journal's exact style;
- verify the final manuscript against the saved aggregate result tables;
- run one longer variance-component fit if computing resources allow it.

At this point, clarity and reproducibility matter more than extra model complexity.
