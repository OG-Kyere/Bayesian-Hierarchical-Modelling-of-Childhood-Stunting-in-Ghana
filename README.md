# Bayesian Hierarchical Modelling of Childhood Stunting in Ghana

This repository contains the reproducible analysis, thesis materials, and manuscript workflow for a publication-oriented thesis on childhood stunting in Ghana using the 2022 Ghana Demographic and Health Survey (GDHS).

## Research aim

The project investigates individual-, household-, and community-level factors associated with childhood stunting in Ghana using Bayesian hierarchical logistic regression.

## Planned modelling sequence

1. Baseline community-level hierarchical model.
2. Household + community random-intercept model.
3. Extension with water and sanitation variables.
4. Extension with maternal education.
5. Survey-weight sensitivity analysis.
6. Prior sensitivity analysis.
7. Posterior predictive checks and model comparison.
8. Publication-ready tables, figures, and manuscript outputs.

## Data access and confidentiality

Raw DHS datasets are **not stored in this repository**. Users must obtain the 2022 Ghana DHS data directly from The DHS Program under its data-use conditions.

The analysis code expects locally stored DHS recode files and produces only derived, non-identifying research outputs suitable for reproducible academic work.

## Project status

Ongoing thesis research intended for publication and PhD application support.


## Current validated descriptive results

The current analytic sample contains **4,928 children**, **927 stunted children**, **3,545 households**, and **616 communities**. The survey-weighted stunting prevalence is **17.39%**.

All figures below are generated from aggregate, non-identifying outputs committed under `results/tables/`. They can be regenerated from authorized DHS microdata with `src/02_descriptive_analysis.py`.

### Age pattern

![Weighted stunting prevalence by child age](results/figures/stunting_by_age.svg)

### Household wealth gradient

![Weighted stunting prevalence by household wealth](results/figures/stunting_by_wealth.svg)

### Regional pattern

![Weighted stunting prevalence by region](results/figures/stunting_by_region.svg)

### Maternal education

![Weighted stunting prevalence by maternal education](results/figures/stunting_by_maternal_education.svg)

### WASH indicators

![Weighted stunting prevalence by drinking-water source](results/figures/stunting_by_water_source.svg)

![Weighted stunting prevalence by sanitation](results/figures/stunting_by_sanitation.svg)

Additional figures for sex and residence are available in `results/figures/`.

## Reproducible public outputs

- `results/tables/descriptive_all.csv` — exact aggregate data behind the descriptive figures.
- `results/tables/analysis_sample_summary.csv` — analytic sample and clustering counts.
- `results/tables/household_structure.csv` — distribution of eligible children per household.
- `results/figures/` — publication-ready SVG figures.
- `docs/variable_dictionary.md` — mapping of thesis constructs to DHS source variables.

Raw DHS microdata and row-level derived extracts are deliberately excluded from the repository. Researchers must obtain the 2022 Ghana DHS files directly from The DHS Program under its access conditions.
