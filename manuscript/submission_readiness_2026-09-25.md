# Submission readiness — 25 September 2026

The statistical analysis and public reproducibility repository are complete for the current TMIH submission-preparation stage. The analysis is frozen: no additional modelling is needed before submission.

## Ready

- analytic sample reconstruction is reproduced exactly;
- public manuscript numbers match the locked aggregate results;
- restricted DHS microdata and local NetCDF posterior files are excluded from Git tracking;
- GitHub Actions pass the public-output and repository-integrity checks;
- the strengthened eight-chain Model 3 result set is clearly separated from later local reproducibility checks;
- sensitivity analyses already cover priors, survey weighting, missing maternal education, age functional form, detailed WASH coding, posterior predictive checks, PSIS-LOO, and independent GEE checks;
- the manuscript identifies the study as a cross-sectional secondary analysis and avoids causal interpretation;
- the TMIH manuscript uses a structured Objectives / Methods / Results / Conclusions abstract under the 300-word limit;
- the current TMIH main body is approximately 2,870 words, below the journal's 3,500-word target;
- the main manuscript contains two tables and two figures;
- the TMIH reference target is Vancouver/numerical;
- the current cited-reference metadata and DOIs have been checked;
- a TMIH-specific cover letter, title page, author statement, reviewer list, reference check, guidelines snapshot and submission checklist are present under `manuscript/targets/tmih/`;
- five reviewer contacts have been externally verified and remain subject to final conflict screening;
- the AI disclosure states the tool and role and preserves human responsibility for all analysis, interpretation and reporting;
- the data-availability statement preserves DHS redistribution restrictions while linking the public reproducibility repository.

## Still requires author confirmation

- correspondence postal address;
- corresponding-author email;
- ORCID, if available;
- final author/co-author list;
- funding statement;
- conflict-of-interest confirmation;
- final author review of the AI disclosure;
- signed TMIH author statement.

## Final production tasks only

These are formatting/submission tasks, not new analysis:

- replace bracketed metadata placeholders;
- compile/render the TMIH manuscript and supplement;
- inspect figure readability and final reference numbering;
- ensure manuscript, title page, cover letter and portal metadata use the same title and author list;
- perform final reviewer-conflict screening;
- upload through Wiley Authors using the standard non-OnlineOpen route unless publication funding is intentionally added.

## Locked interpretation

The household/community variance contrast is reported from the strengthened eight-chain Model 3 run. Fixed-effect odds ratios remain associations. GEE results remain independent sensitivity checks. Observation-level PSIS-LOO remains a conditional comparison within the observed hierarchy and is not described as prediction for entirely new households or communities.
