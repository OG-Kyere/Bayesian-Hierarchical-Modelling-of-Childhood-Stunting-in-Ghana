# Strengthened-run execution environment — 23 September 2026

This file records the package versions present in the sandbox used for the strengthened diagnostic work.

## Installed versions

- Python 3.13.5
- PyMC 5.27.1
- ArviZ 1.1.0
- NumPy 2.3.5
- pandas 2.2.3
- PyTensor 2.37.0
- statsmodels 0.14.6
- SciPy 1.17.0
- patsy 1.0.2
- Matplotlib 3.10.8

## Important compatibility note

The installed PyMC 5.27.1 / ArviZ 1.1.0 combination is not a recommended clean environment. A compatibility workaround was required in the constrained execution environment because current ArviZ namespace changes break normal PyMC import paths.

For that reason:

1. this file records the environment in which the strengthened eight-chain diagnostic work was executed;
2. `requirements.txt` remains the preferred specification for clean reproducibility, with ArviZ constrained below 1.0;
3. a later independent local rerun under Python 3.11 reproduced the analytic sample, the main fixed-effect pattern, healthy sampler diagnostics, and the principal sensitivity conclusions; see `docs/local_reproduction_2026-09-24.md`.

The strengthened eight-chain summaries remain the locked manuscript results, while the later local run is retained as an independent reproducibility check. The exact manuscript numbers are preserved in version-controlled aggregate tables under `results/tables/`.
