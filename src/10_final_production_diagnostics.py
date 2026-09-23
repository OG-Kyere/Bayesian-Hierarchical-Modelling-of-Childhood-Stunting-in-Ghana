"""Final production diagnostic runner for saved PyMC InferenceData files.

Creates a compact diagnostics table with:
- divergences
- maximum R-hat
- minimum bulk/tail ESS
- BFMI
- maximum observed tree depth
- fraction of draws at maximum tree depth
- PSIS-LOO / Pareto-k diagnostics when log-likelihood is available

Run this only on the final locked NetCDF posterior files.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import arviz as az

OUT = Path("results/model_outputs")
TABLES = Path("results/tables")
TABLES.mkdir(parents=True, exist_ok=True)

MODELS = {
    "model1": OUT / "model1_household_community.nc",
    "model2_full": OUT / "model2_wash_full.nc",
    "model2_harmonized": OUT / "model2_wash_harmonized.nc",
    "model3": OUT / "model3_maternal_education.nc",
}


def summarize_model(name, path):
    idata = az.from_netcdf(path)

    vars_present = [
        v for v in ["alpha", "beta", "tau_community", "tau_household"]
        if v in idata.posterior
    ]
    summary = az.summary(
        idata,
        var_names=vars_present,
        kind="diagnostics",
        round_to=None,
    )

    row = {
        "model": name,
        "draws_total": int(
            idata.posterior.sizes.get("chain", 1)
            * idata.posterior.sizes.get("draw", 1)
        ),
        "divergences": int(idata.sample_stats["diverging"].sum())
        if "diverging" in idata.sample_stats else np.nan,
        "max_rhat": float(summary["r_hat"].max()),
        "min_ess_bulk": float(summary["ess_bulk"].min()),
        "min_ess_tail": float(summary["ess_tail"].min()),
    }

    try:
        bfmi = np.asarray(az.bfmi(idata), dtype=float)
        row["min_bfmi"] = float(np.nanmin(bfmi))
        row["mean_bfmi"] = float(np.nanmean(bfmi))
    except Exception:
        row["min_bfmi"] = np.nan
        row["mean_bfmi"] = np.nan

    if "tree_depth" in idata.sample_stats:
        td = np.asarray(idata.sample_stats["tree_depth"])
        max_td = int(td.max())
        row["max_tree_depth_observed"] = max_td
        row["fraction_at_max_tree_depth"] = float((td == max_td).mean())
    else:
        row["max_tree_depth_observed"] = np.nan
        row["fraction_at_max_tree_depth"] = np.nan

    if "log_likelihood" in idata.groups():
        loo = az.loo(idata, pointwise=True)
        k = np.asarray(loo.pareto_k, dtype=float)
        row["elpd_loo"] = float(loo.elpd_loo)
        row["p_loo"] = float(loo.p_loo)
        row["pareto_k_max"] = float(np.nanmax(k))
        row["pareto_k_gt_0_7"] = int((k > 0.7).sum())
        row["pareto_k_gt_1"] = int((k > 1.0).sum())
    else:
        row["elpd_loo"] = np.nan
        row["p_loo"] = np.nan
        row["pareto_k_max"] = np.nan
        row["pareto_k_gt_0_7"] = np.nan
        row["pareto_k_gt_1"] = np.nan

    # Conservative production flags.
    row["diagnostic_status"] = "PASS"
    if (
        row["divergences"] != 0
        or row["max_rhat"] > 1.01
        or row["min_ess_bulk"] < 400
        or row["min_ess_tail"] < 400
        or (not np.isnan(row["min_bfmi"]) and row["min_bfmi"] < 0.3)
        or (not np.isnan(row["pareto_k_gt_0_7"]) and row["pareto_k_gt_0_7"] > 0)
    ):
        row["diagnostic_status"] = "REVIEW"

    return row


def main():
    rows = []
    for name, path in MODELS.items():
        if path.exists():
            rows.append(summarize_model(name, path))
        else:
            rows.append({"model": name, "diagnostic_status": "FILE_MISSING"})

    pd.DataFrame(rows).to_csv(
        TABLES / "final_production_diagnostics.csv", index=False
    )
    print(pd.DataFrame(rows).to_string(index=False))


if __name__ == "__main__":
    main()
