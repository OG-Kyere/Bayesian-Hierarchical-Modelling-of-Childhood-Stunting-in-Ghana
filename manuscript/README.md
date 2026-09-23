# Manuscript

This folder contains the journal-paper version of the project.

The thesis covers the full analysis. The paper is narrower. It focuses on the result that turned out to be the most interesting statistically: **the residual household variation in stunting is much larger than the residual community variation once both levels are modelled together.**

That is the thread I want the manuscript to keep.

## Files

- `main.tex` — general manuscript version
- `supplement.tex` — diagnostics and sensitivity analyses
- `results_snapshot.md` — numerical values currently used in the paper
- `reviewer_objections.md` — questions a skeptical reviewer is likely to ask
- `strobe_self_audit.md` — reporting check against STROBE
- `submission_gap_audit.md` — what is still missing before submission
- `targets/mcn/` — version prepared for *Maternal & Child Nutrition*

## Numbers currently used in the paper

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

Those values are also stored in `results_snapshot.md` so that manuscript edits can be checked against one place.

## Journal version

The first target currently being prepared is *Maternal & Child Nutrition*. The blinded manuscript, title page, key messages, cover letter, reference check, and submission checklist are under:

```text
manuscript/targets/mcn/
```

The paper is kept shorter than the thesis on purpose. Most of the detailed convergence checks and sensitivity results belong in the supplement rather than the main text.

## What still needs to be completed

Before submission, I still need to finalize the author list and affiliations, funding/conflict statements, the submitting institution's ethics wording, and the final journal reference formatting. A clean production rerun would also be useful if I can improve the two random-effect SD R-hat values beyond the current ~1.02.

The analysis itself is not being expanded with extra covariates just for complexity. At this point, the priority is accuracy, reproducibility, and a clear paper.
