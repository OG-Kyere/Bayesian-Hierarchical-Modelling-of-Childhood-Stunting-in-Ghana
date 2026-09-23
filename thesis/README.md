# Thesis

Working title: **Bayesian Hierarchical Modelling of Childhood Stunting in Ghana**

The thesis contains the longer version of the project, including the descriptive analysis, full model sequence, sensitivity analyses, diagnostics, and discussion.

## Chapters

1. Introduction
2. Literature Review
3. Methodology
4. Results
5. Discussion, Conclusions, and Recommendations

The root-level `main.tex` is the easiest entry point for Overleaf. It pulls in the chapter files from this folder and the figures from `results/figures/`.

The local `thesis/main.tex` file does the same thing when working directly inside the thesis folder.

## Front matter

Generic versions of the following are already included:

- title page
- declaration
- abstract
- acknowledgements
- ethical considerations
- table of contents
- list of tables
- list of figures
- list of abbreviations

I have deliberately left the university-specific details out. They should only be added once the actual programme or institutional thesis template is known.

The metadata placeholders are in `config.tex`.

## Current formatting

For now the thesis uses simple, neutral formatting:

- A4 paper
- 12-point text
- 1-inch margins
- 1.5 line spacing for the main text
- Roman numbering in the front matter
- Arabic numbering from Chapter 1

The statistical content is independent of that layout, so the thesis can later be moved into an official university template without rewriting the chapters.

## Main result files

The results used in Chapter 4 are stored under `../results/tables/` and `../results/figures/`.

For the final Bayesian model, the most useful summary files are:

- `model3_final_8chain_key_or.csv`
- `model3_final_8chain_variance_summary.csv`
- `model3_final_8chain_sampler_diagnostics.csv`
- `model3_final_8chain_loo_summary.csv`

The thesis should always be checked against those files before final submission so that prose and numerical results stay synchronized.
