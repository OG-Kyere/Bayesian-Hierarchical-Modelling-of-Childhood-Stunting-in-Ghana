# Journal manuscript

This folder contains a publication-oriented manuscript derived from the thesis.

## Manuscript focus

The paper is intentionally narrower than the thesis. Its central contribution is:

> separating residual household and community heterogeneity in childhood stunting using the 2022 Ghana DHS, then examining whether that hierarchy changes after WASH and maternal education are introduced.

This framing avoids claiming that Bayesian or multilevel stunting analysis in Ghana is itself novel.

## Files

- `main.tex` — standalone journal-style manuscript
- `supplement.tex` — diagnostic and sensitivity-analysis supplement

Both compile against the public figures under `../results/figures/` and the shared bibliography under `../thesis/references.bib`.

## Current key results used in the manuscript

- weighted stunting prevalence: 17.4% (95% CI 15.8–18.9)
- final household SD: 1.23
- final community SD: 0.39
- household VPC: 0.31
- community ICC: 0.03
- household MOR: 3.24
- community MOR: 1.45
- unimproved water OR: 1.50 (1.15–1.99)
- higher maternal education OR: 0.37 (0.20–0.65)
- richest vs poorest OR: 0.36 (0.20–0.64)
- male vs female OR: 1.50 (1.24–1.82)
- age 24–35 vs 0–5 months OR: 2.91 (2.06–4.21)

## Before journal submission

1. Finalize co-authorship and affiliations.
2. Select a target journal and reformat to its author instructions.
3. Confirm whether the journal requires a structured abstract and specific word limit.
4. Re-run the final preferred models in the pinned environment if exact variance-component R-hat <= 1.01 is required.
5. Freeze the final posterior objects and regenerate all tables/figures from them.
6. Add data-availability, ethics, funding, conflicts-of-interest, and author-contribution statements in the journal's required format.
7. Verify every bibliography entry and DOI.
