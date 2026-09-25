# Submission readiness — 25 September 2026

The statistical analysis and public reproducibility repository are now substantially complete for manuscript preparation.

## Ready

- analytic sample reconstruction is reproduced exactly;
- public manuscript numbers match the locked aggregate results;
- restricted DHS microdata and local NetCDF posterior files are excluded from Git tracking;
- GitHub Actions pass the public-output and repository-integrity checks;
- the strengthened eight-chain Model 3 result set is clearly separated from later local reproducibility reruns;
- sensitivity analyses cover priors, survey weighting, missing maternal education, age functional form, detailed WASH coding, posterior predictive checks, PSIS-LOO, and independent GEE checks;
- the blinded manuscript explicitly identifies the study as a cross-sectional secondary analysis and avoids causal interpretation;
- the current MCN abstract is approximately 205 words;
- the current main text is approximately 2,620 words, comfortably below the 5,000-word limit;
- five key messages total approximately 88 words;
- the main blinded manuscript contains two tables and two figures;
- current cited-reference metadata and DOIs have been checked against publisher or official records.

## Still requires author input before submission

- final affiliation(s);
- corresponding-author email;
- ORCID, if available;
- final co-author list and agreed CRediT contributions;
- funding statement;
- conflict-of-interest confirmation from all authors;
- exact institutional wording for secondary-data ethics/exemption;
- final review of the generative-AI disclosure;
- conversion/rendering of the bibliography in the journal's exact APA 7 implementation.

## Optional rather than required analysis

A longer variance-component run could improve Monte Carlo precision for the household and community SDs, but it is not needed to resolve a substantive inconsistency. The broad household-versus-community contrast is supported by the strengthened run, local reproduction, sensitivity analyses, and independent GEE checks.

If prediction for entirely new households or communities becomes a reviewer priority, grouped cross-validation would be the appropriate extension rather than interpreting the current observation-level PSIS-LOO as out-of-cluster validation.
