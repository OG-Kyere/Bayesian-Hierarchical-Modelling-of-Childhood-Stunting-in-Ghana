# Full project diagnostic and remediation report — 25 September 2026

## Scope

This audit covered the tracked research repository for **Bayesian Hierarchical Modelling of Childhood Stunting in Ghana**, including Python source code, saved aggregate outputs, figures, LaTeX/Overleaf sources, the long-form report, journal manuscripts, references, reproducibility checks, and submission documentation.

The statistical analysis was treated as **locked**. No Bayesian model, sensitivity model, GEE analysis, posterior predictive analysis, or PSIS-LOO comparison was rerun. Numerical corrections were made only by reconciling prose against the existing locked aggregate outputs.

## Overall status

**PASS after remediation.**

The project is internally consistent at the code/source/output level. All principal LaTeX entry points compiled successfully in the audit environment after the fixes below. Remaining TMIH work is author-supplied submission metadata rather than an analytical defect.

## Diagnostics completed

### Python source
- 18 tracked Python files parsed successfully.
- `python -m compileall -q src` passed.
- No hard-coded local Windows user paths, API keys, passwords, or wildcard imports were found in the audit scan.

### Saved outputs
- 43 tracked CSV result files parsed successfully and contained data rows.
- 11 tracked SVG figures parsed successfully as XML.
- Public result-consistency checks passed after being strengthened.
- Repository-integrity checks passed after being strengthened.

### Repository integrity
- 26 BibTeX entries; no duplicate keys.
- All LaTeX citation keys resolve.
- All referenced figures exist.
- No restricted DHS/raw-data format is tracked.
- The archived MCN manuscript remains blinded.
- The active TMIH target is identified as independent research and is protected against stale KNUST/MCN targeting text.

### LaTeX / Overleaf
The following entry points were compiled independently during the audit:
1. repository-root `main.tex`;
2. `thesis/main.tex`;
3. `manuscript/main.tex`;
4. `manuscript/targets/mcn/main_blinded.tex`;
5. `manuscript/targets/tmih/main.tex`;
6. `manuscript/targets/tmih/supplement.tex`.

All six completed with no unresolved citations/references, overfull boxes, underfull boxes, or package warnings after remediation.

## Issues found and fixed

1. **Fatal LaTeX math-mode bug** — a raw `\hat{R}` appeared outside math mode in Chapter 3 and prevented the full report from compiling. It was corrected.

2. **Stale future-tense methodology** — completed analyses were still described as planned or future work. The methodology now describes the work actually performed.

3. **WAIC still presented as primary model comparison** — the long-form report now uses the locked PSIS-LOO result:
   - Model 3 minus Model 2 ELPD: +0.92;
   - SE: 3.38;
   - Model 3 Pareto k > 0.70: 0;
   - Model 2 Pareto k > 0.70: 5;
   - neither model has Pareto k > 1.
   The interpretation remains conditional observation-level prediction within the observed hierarchy.

4. **Stale preliminary Model 3 intervals** — long-form text was reconciled to the locked eight-chain values, including water, sanitation, maternal education, sex, age, wealth, household SD, community SD, household VPC, and community ICC.

5. **Stale requirement for another production run** — another run is no longer presented as a pre-submission requirement. Longer chains are optional future work if tighter Monte Carlo precision is desired.

6. **Outdated weighted-sensitivity convergence description** — the text now reflects the strengthened weighted fit while retaining the correct caution that pseudo-posterior variance components do not replace the primary hierarchical decomposition.

7. **Institutional thesis placeholders** — the long-form document is now an **Independent Research Report** by **Independent Researcher, Ghana**. University, supervisor, degree, and unconfirmed institutional-ethics placeholders were removed.

8. **Archived MCN paths** — relative figure and bibliography paths were corrected so the archived target compiles from its own directory.

9. **TMIH layout warnings** — URL/email line breaking was improved and the unused supplement bibliography was removed.

10. **Long-form layout warnings** — an overlong List-of-Figures caption and wide result tables were corrected.

11. **BibTeX cleanup** — unsupported report entry types were replaced with `@techreport`, and the verified DOI for Boah et al. (2019), `10.1371/journal.pone.0219665`, was added.

12. **Consistency automation did not protect the active TMIH target** — `src/13_public_output_consistency.py` now checks the active TMIH manuscript and the long-form report against the locked results.

13. **Integrity automation did not protect independent-research targeting** — `src/14_repository_integrity.py` now checks that the active TMIH manuscript remains independent and does not drift back to KNUST/MCN targeting language.

14. **Stale submission documentation** — current planning/checklist files were updated for TMIH, Vancouver references, independent-research ethics wording, and the locked analysis state. Historical dated records were retained as provenance.

## Writing-quality pass

The prose was edited for a more natural academic voice without changing the analysis:
- repetitive “present study/thesis” phrasing was reduced;
- canned transitions were removed where the logic already carried the paragraph;
- completed work was described in accurate past/present tense;
- repeated methodological justifications were shortened;
- statistical interpretation was made more concrete;
- non-causal wording and uncertainty were preserved.

The factual generative-AI disclosure remains in the submission package. No attempt was made to manipulate AI-detection systems or conceal tool use.

## Locked result set preserved

The governing numerical source remains `manuscript/results_snapshot.md` and the strengthened eight-chain Model 3 aggregate outputs. No model was rerun and no locked result was changed during this audit.

## Remaining author-only items before TMIH submission

- correspondence email;
- correspondence postal address;
- ORCID, if available;
- final author list and CRediT statement;
- funding declaration;
- conflict-of-interest declaration;
- signed TMIH author statement;
- final reviewer conflict screen.
