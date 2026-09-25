# STROBE reporting checklist — manuscript self-audit

This is a working self-audit for the observational cross-sectional manuscript. It is not a substitute for the official STROBE checklist required by a journal.

## Title and abstract
- [x] Study design and analytic approach are identifiable from the abstract.
- [x] Abstract reports sample size, primary results, and major limitations in interpretation.
- [ ] If requested by the target journal, add the words "cross-sectional study" explicitly to the title or subtitle.

## Introduction
- [x] Scientific background and rationale are stated.
- [x] Existing Ghanaian multilevel/spatial literature is acknowledged.
- [x] The specific contribution is stated without claiming Bayesian modelling itself is novel.
- [x] Research question is clear: household versus community residual heterogeneity and stability after WASH/maternal education.

## Methods
- [x] Data source identified as 2022 Ghana DHS.
- [x] Cross-sectional secondary-data design is clear.
- [x] Analytic population and inclusion rules are described.
- [x] Outcome definition is explicit.
- [x] Core covariates and reference categories are described.
- [x] WASH coding limitations are described.
- [x] Missing maternal education and complete-case sample are reported.
- [x] Survey weights, PSU, and strata are described for descriptive inference.
- [x] Hierarchical likelihood and priors are specified.
- [x] Household and community random effects are specified.
- [x] Derived ICC/VPC/MOR definitions are provided.
- [x] MCMC diagnostics are described.
- [x] Sensitivity analyses are described.
- [x] Ethics/data-access statement is included.
- [x] Exact Python/PyMC/ArviZ and supporting package versions for the strengthened locked analysis are recorded in `docs/executed_environment_2026-09-23.md`; the later independent reproducibility environment is documented separately.
- [ ] If required by the journal, state the exact GDHS fieldwork dates in Methods.

## Results
- [x] Flow from eligible sample to analytic sample is clear numerically.
- [x] Number of children, households, communities, and stunted children is reported.
- [x] Descriptive weighted prevalence and 95% CI are reported.
- [x] Main posterior ORs and intervals are reported.
- [x] Random-effect variance summaries are reported.
- [x] MCMC convergence limitations are disclosed.
- [x] Posterior predictive checks are reported.
- [x] Survey-weight, missing-data, prior, age-form, and WASH-coding sensitivities are reported.
- [x] PSIS-LOO is interpreted as conditional observation-level prediction.
- [ ] Consider adding a compact participant/sample-flow figure only if the target journal or reviewers ask for it.

## Discussion
- [x] Main findings are summarized without repeating every result.
- [x] Findings are compared with previous Ghanaian/SSA literature.
- [x] Household random effect is not described as a causal household effect.
- [x] Cross-sectional causal limitation is explicit.
- [x] Survey-design limitation is explicit.
- [x] WASH measurement limitation is explicit.
- [x] Missing maternal education limitation is explicit.
- [x] Random-effect mixing limitation is explicit.
- [x] Generalizability is limited to the target population represented by the 2022 GDHS.
- [x] Predictive comparison is not overstated.

## Other information
- [x] Data availability statement drafted.
- [x] Conflict-of-interest placeholder drafted.
- [x] Funding placeholder drafted.
- [x] AI-use disclosure drafted.
- [ ] Finalize author list and CRediT contributions.
- [ ] Finalize affiliations, ORCID, and corresponding-author details.
- [ ] Confirm institutional ethics/exemption wording.
- [ ] Convert bibliography output to the target journal's exact APA 7 implementation.
- [x] Verify all currently cited references and DOIs against publisher/official records. Re-check only if the reference list changes.
