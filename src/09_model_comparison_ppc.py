"""Posterior predictive checks and predictive model comparison.

The primary comparison is observation-level PSIS-LOO for harmonized Model 2
and Model 3 on the same 4,503 children. Pareto-k diagnostics are always saved.

WAIC is not run by default because pointwise log-predictive-density variance
can make it unreliable for these hierarchical fits. Use --include-waic only
when a secondary WAIC diagnostic is explicitly wanted.
"""

from pathlib import Path
import argparse
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


def _paired_loo_se(loo2, loo3):
    d = np.asarray(loo3.loo_i, dtype=float).reshape(-1) - np.asarray(
        loo2.loo_i, dtype=float
    ).reshape(-1)
    return float(np.sqrt(d.size * np.var(d, ddof=1)))


def main(include_waic=False, write_final=False):
    m2 = az.from_netcdf(OUT / "model2_wash_harmonized.nc")
    m3 = az.from_netcdf(OUT / "model3_maternal_education.nc")

    _require_loglik(m2, "Model 2 harmonized")
    _require_loglik(m3, "Model 3")

    loo2 = az.loo(m2, pointwise=True)
    loo3 = az.loo(m3, pointwise=True)

    delta = float(loo3.elpd_loo - loo2.elpd_loo)
    se_delta = _paired_loo_se(loo2, loo3)

    k2 = np.asarray(loo2.pareto_k, dtype=float)
    k3 = np.asarray(loo3.pareto_k, dtype=float)

    summary = pd.DataFrame([{
        "model2_elpd_loo": float(loo2.elpd_loo),
        "model3_elpd_loo": float(loo3.elpd_loo),
        "delta_model3_minus_model2": delta,
        "se_delta": se_delta,
        "model2_bad_k": int((k2 > 0.7).sum()),
        "model3_bad_k": int((k3 > 0.7).sum()),
    }])
    summary.to_csv(TABLES / "model_predictive_comparison_loo.csv", index=False)
    if write_final:
        summary.to_csv(TABLES / "loo_model_compare_final.csv", index=False)

    pareto = pd.DataFrame({
        "model": ["model2_harmonized", "model3"],
        "n_observations": [int(k2.size), int(k3.size)],
        "pareto_k_gt_0_7": [int((k2 > 0.7).sum()), int((k3 > 0.7).sum())],
        "pareto_k_gt_1": [int((k2 > 1.0).sum()), int((k3 > 1.0).sum())],
        "max_pareto_k": [float(np.nanmax(k2)), float(np.nanmax(k3))],
    })
    pareto.to_csv(TABLES / "loo_pareto_k_diagnostics.csv", index=False)

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

    print("PSIS-LOO summary")
    print(summary.to_string(index=False))
    print("\nPareto-k diagnostics")
    print(pareto.to_string(index=False))
    if abs(delta) < se_delta:
        print(
            "\nThe ELPD difference is smaller than its paired standard error; "
            "treat the two models as predictively similar."
        )

    if include_waic:
        waic_comp = az.compare(
            {"Model 2 harmonized": m2, "Model 3": m3},
            ic="waic",
        )
        waic_comp.to_csv(TABLES / "model_predictive_comparison_waic.csv")
        print("\nWAIC comparison (secondary diagnostic)")
        print(waic_comp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--include-waic",
        action="store_true",
        help="Also compute WAIC as a secondary diagnostic.",
    )
    parser.add_argument(
        "--write-final",
        action="store_true",
        help=(
            "Also overwrite loo_model_compare_final.csv. Use only when the "
            "current posterior files are the intentionally locked final fits."
        ),
    )
    args = parser.parse_args()
    main(include_waic=args.include_waic, write_final=args.write_final)
