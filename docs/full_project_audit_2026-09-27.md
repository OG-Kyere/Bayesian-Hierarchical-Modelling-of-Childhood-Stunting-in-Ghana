# Full project audit — 27 September 2026

## Scope

This audit reviewed the current tracked repository for **Bayesian Hierarchical Modelling of Childhood Stunting in Ghana** end to end:

- Python analysis and diagnostic scripts;
- locked aggregate Bayesian outputs;
- descriptive tables and figures;
- the long-form thesis/report;
- generic and TMIH manuscript sources;
- supplementary material;
- bibliography and citation resolution;
- author/submission metadata;
- GitHub/Overleaf build workflows; and
- reproducibility/provenance documentation.

The statistical analysis was treated as **locked**. No Bayesian model, sensitivity model, GEE model, posterior predictive analysis, or PSIS-LOO comparison was rerun during this audit. Corrections reconciled public outputs and documentation to the existing locked results.

## Overall conclusion

**PASS after remediation.**

No evidence was found that the primary scientific conclusion or the locked eight-chain Model 3 result set is wrong. The main problems were consistency, provenance, and presentation problems around older preliminary outputs that remained in the public repository.

The central result remains unchanged: residual household heterogeneity is substantially larger than residual community heterogeneity after the measured covariates are included.

## Current locked source of truth

The primary Model 3 result set remains:

- 4,503 children in the complete-case final model;
- 8 independent chains;
- 500 warmup + 500 retained draws per chain;
- 4,000 retained posterior draws;
- 0 divergences;
- BFMI approximately 0.51--0.66;
- no maximum-tree-depth hits.

Primary fixed effects and hierarchical summaries are stored in:

- `results/tables/model3_final_8chain_key_or.csv`
- `results/tables/model3_final_8chain_variance_summary.csv`
- `results/tables/model3_final_8chain_parameter_diagnostics.csv`
- `results/tables/model3_final_8chain_sampler_diagnostics.csv`
- `results/tables/model3_final_8chain_loo_summary.csv`
- `manuscript/results_snapshot.md`

## Confirmed issues found and fixed

### 1. Public Model 3 figures were stale

The repository forest plot still showed preliminary Model 3 intervals, including:

- age 24--35 months: 2.98 (2.00--4.35) instead of the locked 2.91 (2.06--4.21);
- water: 1.50 (1.14--2.00) instead of 1.50 (1.15--1.99);
- higher maternal education: 0.38 (0.19--0.70) instead of 0.37 (0.20--0.65).

The variance-comparison plot also used an older Model 3 community SD near 0.41 rather than the locked 0.389.

**Remediation:** the Bayesian forest, variance-comparison, and PPC figures were regenerated from version-controlled aggregate result tables. A new script, `src/15_build_public_figures.py`, makes this reproducible.

### 2. Several public summary CSVs mixed preliminary and locked Model 3 values

The following files used older Model 3 values in some rows or comparator columns:

- `key_posterior_odds_ratios.csv`
- `model_comparison_variance.csv`
- `prior_sensitivity_key_effects.csv`
- `survey_weight_sensitivity_key_effects.csv`
- `executed_model_metadata.csv`

**Remediation:** all public Model 3 comparator values now point to the locked eight-chain result set. The preliminary four-chain Model 3 metadata is explicitly labelled `superseded`, while the eight-chain result is labelled `locked`.

### 3. The consistency checker protected prose but not figures/tables

The earlier automated check could pass even if the manuscript text was correct while a public SVG or comparison CSV was stale.

**Remediation:** `src/13_public_output_consistency.py` now verifies:

- manuscript/report prose;
- public Model 3 OR summary rows;
- variance-comparison rows;
- prior-sensitivity primary comparators;
- survey-weight primary comparators;
- the forest SVG; and
- the variance-comparison SVG.

### 4. Generic manuscript/report author metadata had drifted

Older generic files still used `Kyere Ofosu Gideon` and contained unresolved funding/conflict placeholders.

**Remediation:** active/generic metadata now uses:

- **Gideon Ofosu Kyere**
- **Independent Researcher, Ghana**
- ORCID **0009-0003-9848-8437**
- confirmed correspondence details
- no specific funding
- no declared conflict of interest.

`CITATION.cff` was also corrected.

### 5. The generic supplement could fail because `[H]` floats lacked the float package

**Remediation:** `manuscript/supplement.tex` now loads `float`; its unused bibliography block was removed. CI now compiles the generic manuscript and supplement in addition to the active TMIH targets and long-form report.

### 6. The literature review leaked this project's own findings

A Chapter 2 WASH paragraph used the present study's water/sanitation results while supposedly reviewing prior literature.

**Remediation:** that paragraph now synthesizes prior evidence and explains why separate and more detailed WASH sensitivity analyses are warranted. Results remain in the Results/Discussion chapters.

### 7. Exact posterior-direction probabilities were not preserved in the locked eight-chain aggregate files

Chapter 4 quoted exact posterior probabilities for selected Model 3 coefficients that could be traced to an earlier fit but not independently verified from the locked final aggregate files.

**Remediation:** those exact probabilities were removed from the locked Model 3 prose. Odds ratios and posterior intervals, which are directly preserved, remain.

### 8. An auxiliary centered-intercept prior check lacked a preserved public runner

Aggregate rows for an additional centered-intercept prior check have commit provenance, but the exact source script that produced that auxiliary fit is not present in the public tree.

**Remediation:** this check remains as historical aggregate provenance only. The thesis's formal prior-sensitivity evidence is now based on the reproducible tighter/wider prior fits whose runners are preserved.

### 9. GEE documentation still described the Bayesian model as “planned”

**Remediation:** the GEE files are now described correctly as independent robustness checks on the completed Bayesian analysis.

### 10. Locked-result provenance was not explicit enough

The public Model 3 script performs a clean reproducibility rerun of the same model specification, but its default chain schedule is not a bit-for-bit recreation of the archived strengthened eight-chain result. The exact chain-level NetCDF objects from the strengthened run are not committed publicly.

**Remediation:** `docs/locked_model3_result_provenance.md` now distinguishes:

- model/specification reproducibility;
- aggregate result verification; and
- exact chain-level posterior replay.

The public scripts and diagnostics documentation now point to this distinction explicitly.

### 11. Detailed-WASH coding could silently absorb an unexpected water category

The detailed-WASH sensitivity grouped any non-surface/non-unprotected-groundwater response into “improved.” If an unexpected country-specific DHS response were ever present, that fallback could silently misclassify it.

**Remediation:** `src/12_wash_coding_sensitivity.py` now fails loudly if WASH values are missing or if an unexpected drinking-water category is encountered. No locked estimate was changed.

## Validation completed

- all Python source files parse/compile;
- all tracked result CSVs parse successfully;
- all SVGs are valid XML;
- all BibTeX citation keys used by LaTeX resolve;
- no duplicate BibTeX keys were found;
- no restricted DHS row-level data are tracked;
- the archived blinded manuscript remains blinded;
- active author metadata are synchronized;
- public result-consistency checks pass;
- repository-integrity checks pass;
- root long-form report compiles;
- generic manuscript compiles;
- generic supplement compiles;
- TMIH manuscript compiles;
- TMIH supplement compiles.

## Reference audit

Recent/key citations were spot-checked against publisher or indexed records, including the 2022 GDHS report and recent Ghana/SSA papers used to establish the literature gap. No obvious fabricated or mismatched recent citation was identified in the sampled verification. Internal citation-key resolution is fully checked by CI.

## Remaining limitations — not errors

1. **Cross-sectional design.** Associations must not be interpreted as causal effects.
2. **Exact chain-level replay.** The strengthened eight-chain NetCDF posterior object is not public; the repository preserves model code, locked aggregate outputs, diagnostics, and an independent later reproduction.
3. **Variance-component Monte Carlo precision.** The household/community SDs mix more slowly than the fixed effects. Their exact interval endpoints deserve more caution, although the household-versus-community contrast is stable.
4. **Survey design.** The primary Bayesian likelihood is not a full design-based Bayesian survey model. The rescaled pseudo-posterior is correctly treated as a sensitivity analysis.
5. **Unmeasured household factors.** The household random effect is residual heterogeneity, not evidence for one specific causal household exposure.
6. **Restricted DHS data.** Raw microdata cannot be redistributed; external users need their own DHS authorization.
7. **Authorship.** If additional contributors are added, the author list and CRediT statement must be revisited before journal submission.

## Bottom line

After this audit, the project has no known contradiction that overturns the primary result. The most important corrections were stale public figures/tables and provenance/documentation drift, not flaws in the core Bayesian hierarchy or the locked scientific conclusion.
