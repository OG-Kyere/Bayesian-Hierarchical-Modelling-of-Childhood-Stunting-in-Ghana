# Manuscript

This folder contains the journal-paper version of the project.

The thesis covers the full analysis. The paper is narrower. It focuses on the result that turned out to be the most interesting statistically: **the residual household variation in stunting is much larger than the residual community variation once both levels are modelled together.**

That is the thread the manuscript should keep.

## Files

- `main.tex` — general manuscript version
- `supplement.tex` — diagnostics and sensitivity analyses
- `results_snapshot.md` — locked numerical values used in the paper
- `reviewer_objections.md` — questions a skeptical reviewer is likely to ask
- `strobe_self_audit.md` — reporting check against STROBE
- `submission_gap_audit.md` — remaining submission-stage gaps
- `targets/tmih/` — **active** version prepared for *Tropical Medicine & International Health*
- `targets/mcn/` — archived earlier version prepared for *Maternal & Child Nutrition*

## Locked numbers currently used in the paper

The core sample has 4,928 children in 3,545 households and 616 survey communities. Weighted stunting prevalence is 17.4%.

The strengthened final Model 3 gives:

- household SD: 1.23
- community SD: 0.39
- household VPC: 0.31
- community ICC: 0.03
- household MOR: 3.24
- community MOR: 1.45
- unimproved water OR: 1.50 (1.15–1.99)
- higher maternal education OR: 0.37 (0.20–0.65)
- richest vs poorest OR: 0.36 (0.20–0.64)
- male vs female OR: 1.50 (1.24–1.82)
- age 24–35 vs 0–5 months OR: 2.91 (2.06–4.21)

These values are also stored in `results_snapshot.md` so journal-format edits can be checked against one source of truth.

## Active journal version

The active target is *Tropical Medicine & International Health (TMIH)*. The submission package is under:

```text
manuscript/targets/tmih/
```

It contains the TMIH manuscript, supplement, title page, cover letter, Vancouver reference check, author-statement template, reviewer suggestions, dated author-guidelines snapshot, and submission checklist.

The earlier MCN package is retained only as a provenance archive.

## Analysis lock

The statistical analysis is complete. Do not rerun models, add covariates, add spatial analysis, replace the primary model, or modify locked numerical results merely for journal retargeting.

The remaining work before submission is editorial and administrative: finalize correspondence details, funding/conflict declarations, the signed author statement, reviewer conflict screening, and the final rendered manuscript. The active paper is presented as independent research and does not claim an additional institutional ethics approval.
