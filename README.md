# Bayesian Hierarchical Modelling of Childhood Stunting in Ghana

This project uses the 2022 Ghana Demographic and Health Survey (GDHS) to study childhood stunting in Ghana.

I started with a question that became more important as the analysis developed: **how much of the unexplained variation in stunting is shared within households, and how much is shared at the community level?**

That led to a three-level Bayesian logistic model with children nested within households and households nested within survey communities. I then extended the model to examine household water and sanitation conditions, maternal education, and the stability of the results under different modelling choices.

## Data

The analysis uses the 2022 Ghana DHS Household Member Recode.

The core sample contains 4,928 children aged 0–59 months with valid height-for-age measurements:

- 927 stunted children
- 3,545 households
- 616 survey communities

The survey-weighted prevalence of stunting is 17.39%, which reproduces the published 2022 GDHS estimate.

Raw DHS files are not included in this repository. They are restricted data and must be requested directly from [The DHS Program](https://dhsprogram.com/). The repository contains code, aggregate tables, figures, and other non-identifying outputs only.

## What I found

The main result is the difference between household and community heterogeneity.

Once both levels are included in the model, the household random effect is much larger than the community random effect. In the strengthened final model, the posterior median household SD is about 1.23 compared with 0.39 at the community level. This corresponds to a household VPC of about 0.31 and a community ICC of about 0.03.

The household median odds ratio is about 3.24, compared with 1.45 for communities. I interpret this as evidence that a large amount of the remaining clustering in childhood stunting is shared within households rather than between survey communities.

Some of the fixed-effect results are also quite stable across the different model specifications:

- boys have higher posterior odds of stunting than girls: OR 1.50 (95% posterior interval 1.24–1.82);
- children aged 24–35 months have higher odds than children aged 0–5 months: OR 2.91 (2.06–4.21);
- children in the richest households have lower odds than those in the poorest: OR 0.36 (0.20–0.64);
- unimproved drinking-water source has OR 1.50 (1.15–1.99);
- higher maternal education has OR 0.37 (0.20–0.65).

The sanitation estimate is weaker and more uncertain after adjustment: OR 1.12 (0.86–1.46).

A more detailed WASH sensitivity analysis suggests that the water result is clearest for surface-water use. The water estimate also becomes less precise when survey weights are incorporated through a pseudo-posterior, so I treat that result more cautiously than the age, sex, wealth, and maternal-education results.

## Model checks

The final Model 3 diagnostic run combines eight independent chains and 4,000 retained posterior draws.

There were no divergences, BFMI ranged from 0.51 to 0.66, and none of the chains reached the maximum tree depth. The fixed effects mix well. The household and community standard deviations remain the slowest-mixing parameters, with R-hat values around 1.02, so their exact intervals should be read with a little more caution.

Posterior predictive checks reproduce the observed overall stunting prevalence and the age-specific pattern well.

I also checked whether the conclusions changed when I:

- used tighter or wider priors;
- incorporated survey weights through a pseudo-posterior;
- retained children with missing maternal education;
- replaced the age groups with a spline;
- used more detailed WASH categories.

The broad conclusions remained similar.

## Figures

### Stunting by age

![Weighted stunting prevalence by child age](results/figures/stunting_by_age.svg)

### Stunting by household wealth

![Weighted stunting prevalence by household wealth](results/figures/stunting_by_wealth.svg)

### Regional pattern

![Weighted stunting prevalence by region](results/figures/stunting_by_region.svg)

### Maternal education

![Weighted stunting prevalence by maternal education](results/figures/stunting_by_maternal_education.svg)

### Drinking-water source

![Weighted stunting prevalence by drinking-water source](results/figures/stunting_by_water_source.svg)

### Sanitation

![Weighted stunting prevalence by sanitation](results/figures/stunting_by_sanitation.svg)

## Repository structure

```text
src/                 analysis and diagnostic scripts
results/tables/      aggregate model and descriptive results
results/figures/     figures used in the thesis and manuscript
docs/                variable definitions, audits, and diagnostic notes
thesis/              LaTeX thesis files
manuscript/          journal manuscript and supplementary material
```

A few useful starting points are:

- `src/02_descriptive_analysis.py` — survey-weighted descriptive analysis;
- `src/04_household_community_model.py` — household + community model;
- `src/05_wash_model.py` — WASH extension;
- `src/06_maternal_education_model.py` — maternal-education extension;
- `src/10_final_production_diagnostics.py` — MCMC diagnostics;
- `results/tables/model3_final_8chain_key_or.csv` — key final-model odds ratios;
- `results/tables/model3_final_8chain_variance_summary.csv` — household/community variance results.

## Reproducing the analysis

After obtaining authorized access to the GDHS data, place the required PR recode file under:

```text
data/raw/GHPR8CFL.DTA
```

Then install the Python dependencies in `requirements.txt` and run the analysis scripts in numerical order.

The exact sandbox environment used for the strengthened diagnostic work is documented in `docs/executed_environment_2026-09-23.md`. Because that environment required a PyMC/ArviZ compatibility workaround, `requirements.txt` is the preferred starting point for a clean rerun.

## Thesis and manuscript

The repository contains both the thesis version of the work and a shorter journal manuscript.

The manuscript focuses on the part of the project I think is most useful: separating household and community heterogeneity rather than presenting another list of factors associated with stunting.

The analysis is still observational, so the reported odds ratios are interpreted as associations rather than causal effects.
