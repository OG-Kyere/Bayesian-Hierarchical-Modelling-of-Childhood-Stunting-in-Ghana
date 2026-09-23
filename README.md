# Bayesian Hierarchical Modelling of Childhood Stunting in Ghana

Independent research using the **2022 Ghana DHS**, intended for a journal manuscript and doctoral applications. The agreed scope is **nonspatial**.

## Current evidence status

- **Verified:** sample construction and all descriptive table values were independently reproduced: 4,928 children, 927 unweighted stunting cases, 3,545 households, 616 represented communities, and weighted prevalence 17.385% (design SE 0.795 percentage points).
- **Exploratory:** numerical Bayesian tables under `results/tables/` and Chapters 4–5 are historical short-run outputs. They do not establish confirmed effects or household/community variance dominance.
- **Repaired workflow:** shared preparation, every planned model and sensitivity, per-chain checkpoints, source/sample hashes, full posterior diagnostic gates, and posterior predictive checks now have executable code. New runs under `results/runs/` carry explicit status in `manifest.json`.
- A computational pass remains subject to scientific review. The independent report and working article do not present unvalidated Bayesian estimates as final findings.

See [repair and validation protocol](docs/reproducibility_repair.md) for decisions, limitations, and exact commands. The original [run log](docs/model_run_log.md) documents historical fits.

## Research question

How does estimated residual household versus community heterogeneity in childhood stunting change under household clustering, WASH adjustment, maternal-information selection, prior specification, and survey-weight treatment?

Models estimate **conditional associations**, not causal effects. The primary hierarchical posterior is unweighted; the mean-one survey-weight pseudo-posterior is a sensitivity analysis, not a claim of fully design-calibrated inference.

## Reproduce

Obtain authorized DHS access and place `GHPR8CFL.DTA` in `data/raw/`. Use Python 3.12 and:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python src/01_data_preparation.py
python src/02_descriptive_analysis.py
python src/bayesian_workflow.py --model m3 --run-id production-v1 --sampler nutpie
```

Other model keys: `m0`, `m1`, `m2`, `m2_harmonized`, `weighted`, `tight`, `wide`, `intercept`, `missing`. Defaults are four chains, 2,000 tuning and 2,000 retained draws per chain. Use a new run ID for each changed execution. The documentation explains the optional `PYTENSOR_FLAGS=cxx=` workaround for environments without Python C development libraries.

```bash
python src/09_model_comparison_ppc.py --run-id production-v1
python src/11_report_runs.py --run-id production-v1
```

Model comparison refuses failed diagnostics or mismatched samples. It is conditional observation-level WAIC, not validation in new communities.

## Files and writing

- `src/stunting_data.py`: shared sample and covariate definitions.
- `src/bayesian_workflow.py`: models, sensitivity scenarios, diagnostics, metadata, and PPCs.
- `tests/`: scientific boundary and survey-domain checks.
- `results/tables/`, `results/figures/`: verified descriptives and explicitly historical Bayesian outputs.
- `results/runs/`: aggregate outputs with per-fit provenance and validation status.
- `main.tex`: independent technical report (Overleaf root entry point).
- `manuscript/main.tex`: working journal article, with verified descriptives and validation-pending Bayesian results.

Raw microdata, derived child-level data, posterior objects, latent-effect diagnostics, and row-level likelihood/prediction arrays stay local and are excluded from Git. They are not redistributed.
