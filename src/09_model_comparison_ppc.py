"""Posterior predictive checks and predictive model comparison.

This script compares harmonized Model 2 and Model 3 on the same 4,503 children.
It reports both PSIS-LOO and WAIC. PSIS-LOO is preferred for the final model
comparison when Pareto-k diagnostics are satisfactory.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import arviz as az

OUT = Path("results/model_outputs")
TABLES = Path("results/tables")
TABLES.mkdir(parents=True, exist_ok=True)


def _require_loglik(idata, label):
    if "log_likelihood" not in idata.groups():
        raise RuntimeError(
            f"{label} has no pointwise log_likelihood. Refit with "
            'idata_kwargs={"log_likelihood": True}.'
        )


def main():
    m2 = az.from_netcdf(OUT / "model2_wash_harmonized.nc")
    m3 = az.from_netcdf(OUT / "model3_maternal_education.nc")

    _require_loglik(m2, "Model 2 harmonized")
    _require_loglik(m3, "Model 3")

    # PSIS-LOO with Pareto-k diagnostics.
    loo2 = az.loo(m2, pointwise=True)
    loo3 = az.loo(m3, pointwise=True)
    loo_comp = az.compare(
        {"Model 2 harmonized": m2, "Model 3": m3},
        ic="loo",
        method="stacking",
    )
    loo_comp.to_csv(TABLES / "model_predictive_comparison_loo.csv")

    # WAIC retained as a secondary check.
    waic2 = az.waic(m2, pointwise=True)
    waic3 = az.waic(m3, pointwise=True)
    waic_comp = az.compare(
        {"Model 2 harmonized": m2, "Model 3": m3},
        ic="waic",
    )
    waic_comp.to_csv(TABLES / "model_predictive_comparison_waic.csv")

    pareto = pd.DataFrame({
        "model": ["model2_harmonized", "model3"],
        "n_observations": [
            int(np.asarray(loo2.pareto_k).size),
            int(np.asarray(loo3.pareto_k).size),
        ],
        "pareto_k_gt_0_7": [
            int((np.asarray(loo2.pareto_k) > 0.7).sum()),
            int((np.asarray(loo3.pareto_k) > 0.7).sum()),
        ],
        "pareto_k_gt_1": [
            int((np.asarray(loo2.pareto_k) > 1.0).sum()),
            int((np.asarray(loo3.pareto_k) > 1.0).sum()),
        ],
        "max_pareto_k": [
            float(np.asarray(loo2.pareto_k).max()),
            float(np.asarray(loo3.pareto_k).max()),
        ],
    })
    pareto.to_csv(TABLES / "loo_pareto_k_diagnostics.csv", index=False)

    # Overall posterior predictive prevalence.
    if "posterior_predictive" in m3.groups():
        yrep = np.asarray(m3.posterior_predictive["stunted"])
        observed = np.asarray(m3.observed_data["stunted"])
        rep_prev = yrep.mean(axis=-1).reshape(-1)
        pd.DataFrame({
            "observed_prevalence": [float(observed.mean())],
            "replicated_mean": [float(rep_prev.mean())],
            "replicated_l95": [float(np.quantile(rep_prev, 0.025))],
            "replicated_u95": [float(np.quantile(rep_prev, 0.975))],
        }).to_csv(TABLES / "model3_ppc_overall_production.csv", index=False)

    print("PSIS-LOO comparison")
    print(loo_comp)
    print("\nPareto-k diagnostics")
    print(pareto)
    print("\nWAIC comparison")
    print(waic_comp)


if __name__ == "__main__":
    main()
