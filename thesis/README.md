# Long-form research report

Working title: **Bayesian Hierarchical Modelling of Childhood Stunting in Ghana**

This folder contains the long-form version of the project: background and literature review, methodology, descriptive results, the full Bayesian model sequence, sensitivity analyses, diagnostics, discussion, and recommendations. The work is presented as an independent research report rather than as an institutional degree submission.

## Chapters

1. Introduction
2. Literature Review
3. Methodology
4. Results
5. Discussion, Conclusions, and Recommendations

The repository-root `main.tex` is the recommended Overleaf entry point. It pulls the chapter files from this folder and figures from `results/figures/`.

The local `thesis/main.tex` file provides the same document when working directly inside this folder.

## Front matter

The report includes:

- independent title page;
- declaration;
- abstract;
- acknowledgements;
- ethical-considerations statement;
- table of contents;
- list of tables;
- list of figures;
- list of abbreviations.

No university, supervisor, or degree metadata is assumed.

## Current formatting

The report uses an institution-neutral layout:

- A4 paper;
- 12-point text;
- 1-inch margins;
- 1.5 line spacing for the main text;
- Roman numbering in the front matter;
- Arabic numbering from Chapter 1.

## Locked result files

The main locked Model 3 summaries are:

- `../results/tables/model3_final_8chain_key_or.csv`
- `../results/tables/model3_final_8chain_variance_summary.csv`
- `../results/tables/model3_final_8chain_sampler_diagnostics.csv`
- `../results/tables/model3_final_8chain_loo_summary.csv`

The prose is protected by `../src/13_public_output_consistency.py`, which checks key long-form and manuscript quantities against the saved aggregate outputs.
