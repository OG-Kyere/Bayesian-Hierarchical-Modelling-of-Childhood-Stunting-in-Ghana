# TMIH submission target

This directory contains the manuscript package retargeted from *Maternal & Child Nutrition* to *Tropical Medicine & International Health* on 25 September 2026.

The statistical analysis is frozen. No model was rerun and no locked numerical result was changed during retargeting.

## Files

- `main.tex` — TMIH Research Article manuscript with structured abstract, IMRD structure, numerical references, data/ethics/AI declarations, word count, and Supporting Information statement.
- `supplement.tex` — existing locked sensitivity/diagnostic supplement with S-numbered tables and figures, GEE confidence-interval labels, and a same-sample harmonized Model 2 row.
- `title_page.md` — confirmed author metadata, funding/conflict declarations, ethics, data availability, AI disclosure, and current word count.
- `cover_letter.md` — TMIH-specific cover letter.
- `references_vancouver_check.md` — manual Vancouver-style cross-check for cited references.
- `reviewer_suggestions.md` — five provisional reviewer suggestions to be conflict-screened before submission.
- `author_statement.md` — signature template reflecting TMIH/ICMJE authorship requirements.
- `submission_checklist.md` — current requirement-by-requirement submission audit.
- `author_guidelines_snapshot.md` — dated record of the TMIH/Wiley rules used for this retarget.

## Locked interpretation

The paper remains observational. Odds ratios are associations, variance components summarize residual heterogeneity, GEE analyses remain sensitivity checks, and the existing observation-level PSIS-LOO is not described as out-of-household or out-of-community validation.


## Source-of-truth and Wiley layout

The tracked `main.tex` and `supplement.tex` in this directory are the canonical, version-controlled scientific content for the TMIH submission. The final Wiley-formatted Overleaf project may additionally contain journal template assets such as class/style files and logos. Those layout assets do not change the locked analysis or manuscript wording.

When a final Wiley/Overleaf package is prepared, its scientific text, tables, figures, affiliation, and declarations should match these tracked sources. The GitHub CI compiles the tracked TMIH sources and checks their numerical consistency against the locked result tables.
