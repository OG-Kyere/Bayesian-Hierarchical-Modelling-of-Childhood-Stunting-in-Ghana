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
The manuscript currently uses `apalike`, which is not a true APA 7 implementation. Before submission, use the Wiley/MCN preferred reference workflow or an APA 7 BibLaTeX/CSL style and inspect the rendered bibliography manually.

### 2. Reference verification
The bibliography is internally consistent, but each cited item should be verified against the publisher page. One missing DOI (Iddrisu & Gyabaah, 2023) has already been corrected.

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
Record exact versions of:
- Python;
- PyMC;
- ArviZ;
- NumPy;
- pandas;
- PyTensor;
- statsmodels;
- scipy.

### 6. Variance-component Monte Carlo precision
The household/community contrast is stable, but the two SD parameters remain around R-hat 1.02. Keep this limitation transparent. A longer unrestricted run would still be useful if practical.

### 7. Target-journal keywords
MCN requests seven keywords drawn from MeSH where possible. The current keyword list is not yet verified against MeSH terminology.

### 8. AI disclosure
Keep the disclosure factual and narrow. Do not describe AI as an author. State what it assisted with and that authors verified all outputs.

## Do not change unless a reviewer asks
- Do not add many more covariates.
- Do not add spatial modelling just to make the paper look more advanced.
- Do not replace the main hierarchical model with the weighted pseudo-posterior.
- Do not over-focus on predictive model ranking.
- Do not claim a causal effect of water, maternal education, or wealth.
