# Submission-gap audit

## Already strong
- Clear, defensible contribution.
- Main results reproduced in tables rather than only prose.
- Eight-chain diagnostics available.
- Multiple sensitivity analyses.
- Conditional nature of PSIS-LOO now stated.
- Main manuscript is below the journal word limit.
- Two tables + two figures = four main display items, below the MCN limit of five.
- Double-blind MCN manuscript version exists.
- Cover letter, title page, key messages, supplement, and data-access statement exist.

## Highest-priority remaining gaps

### 1. Reference style
The currently cited references have been checked and an APA 7-style comparison list is stored under `manuscript/targets/mcn/references_apa7_check.md`. The LaTeX manuscript still uses `apalike`, which is not a true APA 7 implementation, so the final rendered bibliography must still be converted or formatted using the journal's production workflow.

### 2. Reference verification
Completed for all references currently cited in the manuscript. Journal-article metadata and DOIs have been checked against publisher or official records, and the 2022 GDHS and WHO/UNICEF JMP reports have been checked against official sources. The APA 7-style comparison list is stored in `manuscript/targets/mcn/references_apa7_check.md`. Re-check only if references are added or changed.

### 3. Final author metadata
Need:
- exact affiliation(s);
- corresponding email;
- ORCID if available;
- final co-author list;
- agreed CRediT statement;
- funding;
- conflicts.

### 4. Ethics wording
The DHS survey ethics are documented, but the manuscript should use the exact wording required by the corresponding author's institution for secondary analysis/exemption.

### 5. Final environment lock
The executed environment and the later independent local rerun are documented under `docs/`. Before submission, record the exact package versions associated with whichever posterior files are formally designated as the archival production fit, and keep that environment record with the submission archive.

### 6. Variance-component Monte Carlo precision
The household/community contrast is stable, but the two SD parameters remain around R-hat 1.02. Keep this limitation transparent. A longer unrestricted run would still be useful if practical.

### 7. Target-journal keywords
Seven MeSH-aligned terms are now used: Growth Disorders; Multilevel Analysis; Bayes Theorem; Socioeconomic Factors; Educational Status; Drinking Water; Africa, Western.

### 8. AI disclosure
Keep the disclosure factual and narrow. Do not describe AI as an author. State what it assisted with and that authors verified all outputs.

## Do not change unless a reviewer asks
- Do not add many more covariates.
- Do not add spatial modelling just to make the paper look more advanced.
- Do not replace the main hierarchical model with the weighted pseudo-posterior.
- Do not over-focus on predictive model ranking.
- Do not claim a causal effect of water, maternal education, or wealth.
