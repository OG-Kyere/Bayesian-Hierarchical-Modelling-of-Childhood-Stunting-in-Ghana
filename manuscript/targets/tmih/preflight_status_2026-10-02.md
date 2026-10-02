# TMIH preflight — 2 October 2026

This update follows the editorial review of the 29 September Wiley/Overleaf 2.0 package. The strengthened eight-chain Model 3 numerical results remain locked; no model was refitted.

## Corrected in the active TMIH source

- The methods operationalize the model community as the DHS survey cluster (`hv001`); households are uniquely identified by cluster and household number (`hv001`, `hv002`).
- The main-text comparison no longer treats the Model 1 to Model 3 variation change as solely due to added covariates; sample composition differs.
- GEE supplementary interval bounds are labeled as frequentist 95% confidence intervals, not posterior percentiles.
- The supplementary variance-comparison table includes the harmonized Model 2 on the same 4,503-child sample as Model 3, alongside the full-sample Model 2.
- The in-manuscript instruction about possible future co-authors has been removed; any authorship change remains a separate pre-submission task.
- The convergence limitation is explicit: community SD R-hat approximately 1.021 and household SD R-hat approximately 1.018 exceed the commonly used 1.01 guideline, so exact variance-component interval endpoints warrant caution.
- The supporting posterior predictive prevalence is identified as unweighted and based on the complete-case final-model sample, unlike the full-sample survey-weighted descriptive prevalence.
- Current approximate main-body length: 3,100 words, excluding abstract, references, and captions; confirm final length on the journal submission system.

The Wiley-template export also removes the duplicated correspondence label, retains S-numbering, and is compiled separately as an Overleaf upload ZIP. The repository's active `manuscript/targets/tmih/` source is the authoritative text source; the Wiley-export ZIP is the formatted submission copy.

## Still pending author action

- Supervisor approval and any substantive comments.
- Confirm final author list and contributions if new qualifying contributors join.
- Final reviewer conflict screen and current contact verification.
- Final author review of the AI disclosure and signature on the author statement.
- Wiley submission entry/upload.

The paper remains observational. No new convergence run was performed for this editorial update.