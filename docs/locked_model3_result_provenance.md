# Locked Model 3 result provenance

The current manuscript and long-form report use the strengthened **eight-chain Model 3** as the locked primary result set.

## What is version-controlled

The repository preserves the aggregate outputs required to verify every primary reported quantity:

- `results/tables/model3_final_8chain_key_or.csv`
- `results/tables/model3_final_8chain_variance_summary.csv`
- `results/tables/model3_final_8chain_parameter_diagnostics.csv`
- `results/tables/model3_final_8chain_sampler_diagnostics.csv`
- `results/tables/model3_final_8chain_loo_summary.csv`
- `manuscript/results_snapshot.md`

The final run used eight independent chains with 500 warmup and 500 retained draws per chain, for 4,000 retained posterior draws. It had zero divergences, BFMI from approximately 0.51 to 0.66, and no maximum-tree-depth hits.

## What is not version-controlled

The chain-level NetCDF posterior objects from the strengthened run are not committed to the public repository. The public repository therefore supports verification of the reported aggregate results and reconstruction of the model specification, but it should not be described as providing a bit-for-bit replay of the exact archived eight-chain posterior object.

The model specification is encoded in the public PyMC scripts. The public Model 3 runner now also exposes the manuscript's strengthened sampling schedule:

```bash
python src/06_maternal_education_model.py --locked-schedule
```

That command uses eight chains with 500 warmup and 500 retained draws per chain and writes to a separate reproduction output stem. It reconstructs the model specification and sampling schedule without overwriting the locked aggregate files. Because the original chain-level posterior object and its exact random-number streams are not version-controlled, it should still not be described as a bit-for-bit replay of the archived locked posterior.

A later four-chain local rerun reconstructed the analytic sample and reproduced the same substantive conclusions; that independent check is documented in `docs/local_reproduction_2026-09-24.md`.

## Figures and public summaries

Public summary CSVs that compare against Model 3 use the locked eight-chain values as their primary comparator. The Bayesian SVG figures are regenerated from aggregate tables with:

```bash
python src/15_build_public_figures.py
```

The CI consistency check in `src/13_public_output_consistency.py` verifies the manuscript prose, public comparison tables, and Bayesian figures against the locked result files.

## Interpretation boundary

The locked values are conditional associations from a cross-sectional hierarchical model. They are not causal effects. Observation-level PSIS-LOO is conditional within the observed household/community hierarchy and is not a test of prediction for entirely new households or communities.


## Convergence-strengthening option

The locked manuscript values are not changed automatically. If a stricter variance-component convergence check is desired before or during peer review, run:

```bash
python src/06_maternal_education_model.py --convergence-run
```

This mode uses eight chains, 1,500 warmup iterations and 2,000 retained draws per chain with `target_accept=0.98`, and writes to a separate output stem. Its purpose is to assess whether the household/community SD \hat R values and effective sample sizes improve materially without silently replacing the locked manuscript result set. Any decision to re-lock results should be explicit and followed by the repository consistency checks.
