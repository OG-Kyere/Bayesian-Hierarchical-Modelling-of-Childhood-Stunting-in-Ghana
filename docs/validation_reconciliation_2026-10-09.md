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

Authorized DHS records and the nine posterior files are absent from the current workspace and accessible Documents search. The earlier chat reference provides no attachment or local path. Consequently no private-data reconstruction or saved-posterior audit has been completed in this session. Historical sample counts and reproduction claims are source-reported; do not present them as newly independently verified. The local path has been requested. No raw records, posterior draws, latent identifiers, or private arrays have been uploaded or committed.
