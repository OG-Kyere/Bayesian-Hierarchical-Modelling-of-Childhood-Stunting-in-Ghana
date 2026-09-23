# Thesis

Working title: **Bayesian Hierarchical Modelling of Childhood Stunting in Ghana**

## Current structure

1. Introduction
2. Literature Review
3. Methodology
4. Results
5. Discussion, Conclusions, and Recommendations

The thesis includes the full methodological workflow, Bayesian model sequence, sensitivity analyses, posterior predictive checks, and reproducibility documentation.

## Overleaf workflow

The project is institution-neutral and designed for a full-repository Overleaf sync.

Select the **root-level `main.tex`** as the Overleaf main document. It includes the chapter files under `thesis/` and accesses figures under `results/figures/`.

The file `thesis/main.tex` is retained as a convenience entry point when working inside the thesis folder.

### Front matter currently included

- title page
- declaration
- abstract
- acknowledgements
- ethical considerations
- table of contents
- list of tables
- list of figures
- list of abbreviations

These are generic templates. Their wording and order should be changed to match the actual university or programme requirements once those requirements are available.

### Metadata to complete

Edit `thesis/config.tex` and replace:

- `[INSERT DEPARTMENT / SCHOOL]`
- `[INSERT UNIVERSITY / INSTITUTION]`
- `[INSERT CITY / COUNTRY IF REQUIRED]`
- `[INSERT OFFICIAL DEGREE NAME]`
- `[INSERT MONTH]`
- `[INSERT SUPERVISOR NAME]`

The current abstract is approximately 264 words.

### Formatting

The current Overleaf setup intentionally uses neutral defaults:

- A4 paper
- 12-point report class
- 1-inch margins
- one-and-a-half spacing for main text
- single-spaced captions, abstract, and references
- Roman page numbers for preliminary pages
- Arabic numbering for the main chapters
- centred page numbers
- separate lists of tables and figures

No university-specific formatting should be inferred from the current template. Once the actual institutional guide or thesis template is supplied, only the layout/front-matter layer should need to change; the chapter files and statistical content can remain intact.
