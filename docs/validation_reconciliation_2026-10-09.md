# Branch reconciliation and saved-posterior audit — 9 October 2026

## Evidence identity

Inspected main at `f31a985` and draft PR #1 at `cc6501c` (base recorded by GitHub: `bd7c1c6`). The branches have diverged; GitHub reports the draft as non-mergeable. This correction is prepared on a local branch based on the draft. It does not replace main's manuscripts, authorship, affiliation, or locked result tables. A broad merge must reconcile those later changes explicitly.

## Later evidence versus the draft protocol

Main's `docs/local_reproduction_2026-09-24.md` reports independent sample reconstruction and four-chain Bayesian reproduction. These are historical reports, not computations repeated in this session. Its principal-model PASS summaries must not be equated with the draft's joint-posterior gate: main's `src/10_final_production_diagnostics.py` selects only alpha, beta, and the two tau parameters. It omits household/community z and u effects, uses rounded diagnostics, does not enforce four chains or finite diagnostics, and can pass with missing BFMI/tree-depth evidence. This session implements a separate read-only full-posterior audit, including scaled effects and the household/community SD difference, and connects the draft workflow to the same gate.

Main's locked eight-chain Model 3 diagnostics record community SD R-hat **1.021127** and household SD R-hat **1.017634**, both exceeding the draft requirement of finite R-hat **below 1.01**. Adequate reported ESS and zero divergences do not override that failure. Later main manuscripts acknowledge this convergence caveat. The public locked parameter table is selected aggregate evidence and cannot certify all latent parameters or reconstruct the exact posterior. Main explicitly documents that exact replay of the private eight-chain posterior is unavailable from public files.

The draft's validation-v2 results and main's later runs have different execution histories. Keep their provenance separate; do not relabel main's results as passes under the draft protocol. Main's observation-level PSIS-LOO and the draft's conditional WAIC are different criteria. Neither establishes predictive equivalence or performance in new households/communities. Small ELPD differences relative to their paired SE indicate an inconclusive ranking. GEE working correlations provide complementary evidence and are not Bayesian ICCs or MCMC diagnostics.

## Read-only audit before any rerun

Use a diagnostic environment with ArviZ 0.22.0 and the required NumPy/xarray/NetCDF readers:

```bash
python src/posterior_audit.py --input-dir /absolute/local/path/results/model_outputs --expected-files 9
```

The command reads every recursively discovered `.nc` file; it never loads raw records, samples a model, modifies a posterior, computes row-level predictions, or writes latent diagnostics. Output uses file indices and aggregate diagnostic extrema only. Nine files need not mean nine distinct fits: inspect checkpoint/run provenance privately to identify duplicates and locked versus reproduction outputs. A missing/incorrect file count, diagnostic error, failure, or incomplete evidence produces a nonzero exit status. If tree-depth saturation flags are absent, specify `--max-treedepth` only when the configured cap is independently documented for every file audited together. Never infer a cap from the largest observed depth.

All stored posterior variables are checked without a parameter whitelist. Scaled household/community intercepts and their SD contrast are added when reconstructible. PASS requires four chains, finite diagnostics for every parameter, R-hat below 1.01, both ESS values at least 400, zero divergences, minimum BFMI at least 0.3, and no saturation hits. Missing sampler evidence is INCOMPLETE. PASS still requires trace/rank, Monte Carlo error, provenance, and scientific review. No model reruns are authorized by this command.

## Session limitations

The initial workspace/Documents search did not locate the private files. A subsequent authorized search outside the sandbox located the user's existing repository, with three raw input files and exactly nine saved posterior files. Its clean local main checkout is at `1c57a36e77c5ebd4cd9758190dc486518feff6c8`; it is distinct from the current remote-main snapshot above. That checkout and its private files were not modified.

Reading the authorized PR input through the draft's shared preparation independently reproduced 4,928 children, 927 stunting cases, 3,545 households, 616 represented communities, 618 survey PSUs in 32 strata, weighted denominator 4,292.97481, prevalence 0.17385025722990444, and design SE 0.007953419314553406. All 41 descriptive rows matched remote main's committed table: counts exactly, prevalence/SE/CI endpoints within 1e-16. The prepared harmonized M2 and M3 datasets have identical ordered child keys and outcomes for 4,503 children.

The nine saved files are local four-chain reproduction fits: Model 1, full/harmonized Model 2, Model 3, spline-age and detailed-WASH sensitivities, tight/wide prior sensitivities, and survey weighting. Eight have 1,000 retained draws per chain; weighting has 1,500. Metadata reports PyMC 5.28.5 and ArviZ 0.23.4. Stored observed outcomes match the corresponding reconstructed full/complete sample in all eight files retaining observed outcomes. The weighted file has no stored observed-outcome array. These matches do not verify exact original source code, seeds, or ordered child identity of the archived fit; matching binary outcomes alone is insufficient provenance. None of the nine files is the locked eight-chain Model 3 posterior.

No raw records, posterior draws, latent identifiers, or private arrays have been uploaded or committed. No model sampling was performed.

## Completed full-posterior audit

All nine files were audited with Python 3.12 and ArviZ 0.22.0. Each full audit included 7,832–8,359 scalar posterior elements, including all stored latent/scaled household and community intercepts and reconstructed SD contrasts. A supplemental check audited six scientific derived quantities from the same saved tau draws: SD difference, community ICC, household VPC, same-household ICC, and both median odds ratios. The table takes the most conservative extrema across both checks; no posterior was resampled.

| Saved local fit | Maximum R-hat | Minimum bulk ESS | Minimum tail ESS | Strict joint gate |
|---|---:|---:|---:|---|
| Model 1 | 1.010885 | 485.491 | 533.425 | Fail |
| Model 2 full | 1.011620 | 650.933 | 1041.671 | Fail |
| Model 2 harmonized | 1.010417 | 568.335 | 534.125 | Fail |
| Spline-age sensitivity | 1.012751 | 447.136 | 611.622 | Fail |
| Detailed-WASH sensitivity | 1.015940 | 499.849 | 748.063 | Fail |
| Model 3 | 1.009845 | 456.294 | 513.627 | Pass pending scientific review |
| Tight prior sensitivity | 1.011931 | 456.367 | 619.870 | Fail |
| Wide prior sensitivity | 1.011403 | 419.215 | 687.594 | Fail |
| Survey-weight sensitivity | 1.008136 | 425.278 | 1064.848 | Pass pending scientific review |

Every file had four chains, finite full-parameter diagnostics, zero divergences, zero stored maximum-tree-depth saturation flags, and minimum chain BFMI above 0.3 (range across fits 0.481884–0.761925). Thus seven failures are R-hat failures under the strict below-1.01 rule, despite adequate ESS and otherwise healthy sampler statistics. Rounded selected-parameter summaries cannot establish the joint gate. Full/ harmonized Model 2 and the tight-prior fit illustrate why auditing latent effects changes earlier PASS assessments.

Only local Model 3 and survey weighting pass this numerical screen. Trace/rank plots, estimand-specific Monte Carlo errors, and provenance review remain necessary; this is not publication sign-off or validation of the entire sensitivity sequence. The local four-chain Model 3 pass does not certify the distinct locked eight-chain posterior. No new WAIC/LOO ranking was run because harmonized Model 2 fails the joint gate. No model reruns were performed or prescribed solely on the basis of effect estimates.

Validation of the corrected audit: all 12 scientific/synthetic tests passed, including latent-chain disagreement, unavailable sampler diagnostics, configured versus observed tree depth, nonfinite diagnostics, divergent/saturated draws, and read-only NetCDF/file-count handling. Remote main's public consistency and repository-integrity checks also passed. The public files support consistency verification, not full private-posterior provenance or trace review.
