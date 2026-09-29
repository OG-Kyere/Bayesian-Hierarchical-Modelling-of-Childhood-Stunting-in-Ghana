# TMIH final manuscript cleanup — 29 September 2026

This note records the final manuscript/package cleanup requested after reviewing the Wiley/Overleaf version.

## Changes made

- Explicitly defined the community level as DHS cluster `hv001`.
- Explicitly defined household IDs using `hv001` + `hv002`.
- Rephrased the Model 3 variance narrative so it no longer implies that a larger household/community contrast was necessarily caused by added covariates rather than the complete-case sample.
- Corrected the GEE robustness table headings from posterior-percentile language to frequentist 95% confidence-limit language.
- Added the harmonized Model 2 fit (same 4,503-child sample as Model 3) to the model-sequence variance table.
- Removed the internal reminder about revisiting authorship from the manuscript text.
- Removed submission-only reviewer/editorial information from the manuscript source; reviewer suggestions remain in the dedicated reviewer file/portal metadata.
- Made the variance-component convergence caveat explicit: community SD R-hat 1.021 and household SD R-hat 1.018 remain above the commonly used 1.01 guideline, so exact interval endpoints are interpreted more cautiously than fixed-effect intervals.
- Updated the estimated main-body word count to approximately 3,100 words.
- Refreshed upload/preflight documentation and removed stale placeholder instructions.
- Renamed the active preflight status to `preflight_status_2026-09-29.md`.
- Strengthened `src/14_repository_integrity.py` so these manuscript/supplement clarifications cannot silently regress.

## Analysis state

No Bayesian model, GEE model, posterior predictive check, sensitivity model, or PSIS-LOO analysis was rerun. The locked numerical result set is unchanged.
