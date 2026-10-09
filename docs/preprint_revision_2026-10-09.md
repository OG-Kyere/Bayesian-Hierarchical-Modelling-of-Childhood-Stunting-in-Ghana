# Prepared preprint revision — 9 October 2026

This revision is prepared from current remote main (`f31a985`) and is not a replacement or merge of the older repair PR #1. It preserves current author metadata, manuscript sources, citations, locked numerical tables and public figures. Publication on Research Square remains a separate step; no new preprint version has been posted by this workflow.

## Evidence incorporated

The 9 October saved-posterior audit is documented in PR #1 commits `95a5db7` and `a233be9`. Authorized PR data reconstruction independently reproduced all 41 descriptive rows in main's committed table: counts exactly and prevalence, design SE and CI endpoints within 1e-16. The reconstructed harmonized M2 and M3 samples have identical ordered child keys and outcomes for 4,503 children.

The full-parameter audit read nine saved four-chain reproduction fits, including all stored household/community latent and scaled effects and six reconstructed scientific variance quantities. The strict screen requires at least four chains, finite R-hat below 1.01, both ESS values at least 400, zero divergences, minimum BFMI at least 0.3 and no tree-depth saturation flags. Local Model 3 and survey weighting pass the numerical screen pending scientific review; seven fits fail R-hat. All nine have otherwise adequate finite diagnostics, ESS and sampler statistics. Aggregate extrema are in `results/tables/local_full_posterior_audit_2026-10-09.csv` and the revised supplements.

These are distinct from the locked eight-chain Model 3 used in the manuscript. Its public community and household SD R-hat values are 1.021127 and 1.017634, which also fail the strict threshold. A passing local four-chain fit does not certify that locked posterior. Matching stored outcomes in eight reproduction files does not establish exact source, seed or ordered-child identity; the weighted file has no stored observed-outcome array. No saved missing-maternal-education fit was available in the set of nine, so that sensitivity remains unaudited.

## Manuscript corrections

- The abstract, discussion and conclusions describe the retained Bayesian results as exploratory and the full sensitivity sequence as incompletely validated.
- Methods explain the retrospective full-parameter audit, thresholds and distinction between locked and reproduction fits.
- Both supplements add the nine-fit audit table and provenance limits.
- The retained observation-level PSIS-LOO comparison is explicitly inconclusive; it establishes neither predictive equivalence nor performance in new households/communities.
- Existing effect estimates, variance summaries and public figures are retained with their limitations; no fit is silently re-locked and no model is rerun.
- Current generic preprint and TMIH sources are kept aligned. Archived alternate target/report texts are not silently replaced.

## Remaining diagnostic work

Trace/rank and estimand-specific Monte Carlo error review remains unfinished. This session prepared a read-only scientific-scale review script, but execution was blocked by denied access to the existing diagnostic library files. Automatic approval review rejected escalation because the current sandbox approval category is disabled. No alternative route was used to bypass that rejection. The failed/incomplete fits are not presented as validated, and the two numerical passes do not provide scientific sign-off.

The read-only audit is `src/posterior_audit.py`. The additional scale review can be run locally with the diagnostic dependencies installed:

```bash
python src/review_scientific_diagnostics.py --input-dir results/model_outputs
```

It produces scientific-scale trace/rank panels and MCSE summaries in an ignored local diagnostic directory, never individual random-effect identifiers. Review those outputs and the provenance before choosing any new sampling configuration. Preserve the original posterior files and retain failed runs; use a new output stem for any future fit. Exact revalidation of the locked eight-chain posterior requires its original private archive or an explicitly labelled new reproduction. No automatic replacement of locked outputs is allowed.

## Preprint comparison and release status

The live Research Square v1 abstract and supplementary-file listing were inspected. Its abstract states that sensitivities preserved the household/community pattern without the new diagnostic qualification. The original manuscript was subsequently downloaded through the author dashboard before replacing any draft file. Its 15-page PDF is labelled Version 1, dated 29 September 2026, and its abstract matches the live v1 abstract. The original PDF already acknowledges the locked variance-scale R-hat values around 1.021 and 1.018, but qualifies only interval endpoints while retaining broad robustness and predictive-comparison claims. The revision addresses that gap using the canonical generic/TMIH sources at f31a985, preserving the reported numerical results, references, sole author, affiliation, ORCID and email-only correspondence. The original posted physical layout is not reproduced byte-for-byte; the revised export is visually checked separately.

The public source has been checked with the repository's numeric-consistency and integrity scripts. Compiled revision PDFs are checked separately for unresolved citations, missing figures, clipping and layout. Public revision materials contain aggregate results only. Raw DHS inputs, posterior objects, latent coordinates and row-level arrays remain private and uncommitted.

## Supporting-content preservation

The original nine-page supplement was also downloaded before replacement. It contains eleven supporting tables and nine figures, including prior, weighted, missing-education, GEE and PSIS-LOO tables and sex/residence figures absent from the generic source. The revision restores all eleven original tables and all nine figures, retains their S1–S11/S1–S9 sequence, and appends the new audit as Table S12. Historical numbers are copied from the existing public aggregate tables or unchanged target source and remain labelled with their diagnostic limitations. The inconclusive PSIS-LOO interpretation replaces the original equivalence wording.
