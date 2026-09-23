# Likely reviewer questions and current responses

This memo is written from the perspective of a skeptical nutrition / epidemiology reviewer.

## 1. Why is a household random effect needed when many households contain only one eligible child?

**Likely concern:** The household variance may be weakly identified because 2,398 of 3,545 households contain only one eligible child.

**Current response:** The manuscript now states this limitation explicitly. Importantly, 1,147 households contain multiple eligible children and approximately 51.3% of analysed children live in multi-child households. An independent exchangeable GEE check also shows materially stronger within-household than within-community residual correlation (about 0.154 vs 0.024).

**Still worth doing:** Keep the household-structure table in the supplement and do not oversell the exact household variance interval.

## 2. Are the random-effect diagnostics good enough?

**Likely concern:** The fixed effects mix well, but the household/community SD R-hat values remain around 1.02.

**Current response:** Eight independent chains and 4,000 retained draws yielded zero divergences, BFMI about 0.51–0.66, no tree-depth saturation, and bulk ESS above 500 for both variance SDs. The household-versus-community contrast is stable across specifications.

**Recommended wording:** Treat the broad contrast as reliable but exact variance-component intervals as somewhat less precise than the fixed effects.

## 3. Why are survey weights not in the primary Bayesian likelihood?

**Likely concern:** DHS sampling is informative and the primary posterior does not fully incorporate the complex design.

**Current response:** Design weights, PSUs, and strata are used for descriptive inference. A rescaled pseudo-posterior is reported as sensitivity analysis. Main fixed-effect directions are similar, although the water interval widens.

**Still worth doing:** Avoid describing the primary Bayesian posterior as fully population-representative in a design-based sense.

## 4. Does the water result survive reasonable alternative definitions?

**Likely concern:** A binary improved/unimproved indicator may be crude.

**Current response:** Yes, directionally. A detailed-WASH model shows the clearest association for surface water, OR 1.52 (1.10–2.08). Unprotected groundwater is more uncertain. Survey-weight sensitivity weakens precision.

**Recommended wording:** State that the primary evidence is for an association with water-source type, especially surface-water exposure, not for a causal effect of a specific intervention.

## 5. Why is sanitation weak despite a large crude prevalence difference?

**Likely concern:** Apparent contradiction between descriptive and adjusted results.

**Current response:** The crude contrast is strongly confounded by wealth, residence, region, and other household conditions. Once adjusted, sanitation is not clearly separated from the null.

**Recommended wording:** Do not imply sanitation is unimportant for health; say this particular facility-type indicator does not show a clear independent association with stunting after adjustment.

## 6. Is maternal education genuinely adding value if predictive performance barely improves?

**Likely concern:** Why keep Model 3 when LOO is nearly identical to Model 2?

**Current response:** Model 3 addresses a substantive scientific question, not only prediction. Higher maternal education has a strong inverse posterior association. PSIS-LOO shows the larger model does not materially improve observation-level prediction.

**Recommended wording:** Keep the distinction between explanation/interpretation and prediction explicit.

## 7. Is the PSIS-LOO comparison valid for this hierarchical model?

**Likely concern:** Observation-level LOO can be optimistic if the scientific goal is prediction for new households or communities.

**Current response:** The manuscript now explicitly states that the comparison is conditional within the observed hierarchy. It is not presented as out-of-cluster prediction.

**Possible future extension:** Leave-one-household-out or K-fold group cross-validation if prediction for new households becomes a manuscript objective.

## 8. Why use age categories?

**Likely concern:** Arbitrary cut-points may distort associations.

**Current response:** A Bayesian spline-age sensitivity model gives nearly identical estimates for the key non-age variables.

## 9. What about missing maternal education?

**Likely concern:** Complete-case restriction may bias Model 3.

**Current response:** A full-sample sensitivity model treats missing maternal education as an explicit category. Water and higher-education results remain similar; the missing category is uncertain.

## 10. Could the household random effect be absorbing omitted child-level predictors?

**Likely concern:** The household effect may partly capture omitted confounding rather than an interpretable “household influence.”

**Current response:** Correct. The manuscript now describes the random effect as residual household heterogeneity, not a causal household effect. Missing variables such as diet, food insecurity, maternal nutrition, birth size, infection, and caregiving are acknowledged.

## 11. Is the contribution novel enough?

**Likely concern:** Bayesian and multilevel stunting analyses already exist in Ghana.

**Current response:** The manuscript explicitly avoids claiming otherwise. The contribution is the use of the 2022 GDHS full eligible under-five sample to separate household and community residual heterogeneity, followed by WASH/maternal-education extensions and extensive robustness checks.

## 12. Are the WASH categories true JMP service levels?

**Likely concern:** “Improved” source/facility type may be confused with basic or safely managed service.

**Current response:** The manuscript repeatedly states that the variables represent source/facility type only, not complete JMP service levels.

## 13. Is there enough information in the main paper to judge the results?

**Likely concern:** Important estimates were previously buried in prose.

**Current response:** Two main-text tables have now been added:
- selected descriptive prevalence estimates;
- selected final posterior ORs and hierarchical variance measures.

The supplement retains the detailed diagnostics and sensitivity tables.

## Remaining actions before submission

1. Verify every cited reference and DOI against the publisher record.
2. Convert the bibliography output to the target journal's exact APA 7 implementation.
3. Confirm all authors, affiliations, ORCIDs, funding, conflicts, and CRediT contributions.
4. Confirm ethics/exemption wording required by the corresponding author's institution.
5. Consider a final longer run only if exact variance-component R-hat <= 1.01 is required by the author team.
6. If reviewers emphasize prediction for new households, add grouped cross-validation rather than defending observation-level LOO as equivalent.
