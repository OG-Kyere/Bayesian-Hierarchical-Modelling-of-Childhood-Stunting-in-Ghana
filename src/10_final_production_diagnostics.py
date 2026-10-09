"""Diagnostics for locally saved PyMC InferenceData files.

This script diagnoses whichever local NetCDF files are present under
results/model_outputs. It does not recreate or certify the archived locked
eight-chain result set by itself; see docs/locked_model3_result_provenance.md.

Sampler diagnostics and PSIS-LOO diagnostics are reported separately.  A model
can therefore have healthy NUTS sampling while still requiring review of a few
high-Pareto-k observations.

The tree-depth fields deliberately distinguish the largest depth *observed*
from actual maximum-tree-depth hits.  The previous implementation counted
draws at the largest observed depth, which is not the same thing as sampler
saturation.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import arviz as az
from posterior_audit import diagnostics

OUT = Path("results/model_outputs")
TABLES = Path("results/tables")
TABLES.mkdir(parents=True, exist_ok=True)

MODELS = {
    "model1": OUT / "model1_household_community.nc",
    "model2_full": OUT / "model2_wash_full.nc",
    "model2_harmonized": OUT / "model2_wash_harmonized.nc",
    "model3": OUT / "model3_maternal_education.nc",
    "age_spline": OUT / "model3_age_spline_sensitivity.nc",
    "detailed_wash": OUT / "model3_detailed_wash_sensitivity.nc",
    "prior_tight": OUT / "model3_prior_tight.nc",
    "prior_wide": OUT / "model3_prior_wide.nc",
    "weighted": OUT / "model3_weighted_sensitivity.nc",
}


def _max_treedepth_hits(sample_stats):
    """Return (hits, fraction) when PyMC stored a saturation flag."""
    for key in ("reached_max_treedepth", "reached_max_tree_depth"):
        if key in sample_stats:
            flag = np.asarray(sample_stats[key], dtype=bool)
            return int(flag.sum()), float(flag.mean())
    return np.nan, np.nan


def summarize_model(name, path):
    idata = az.from_netcdf(path)

    # Strict, unrounded joint audit includes all latent/scaled effects and
    # reconstructed scientific variance quantities. Missing evidence cannot pass.
    summary, audit = diagnostics(idata)

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
        "chains": audit["chains"],
        "parameters_checked": audit["parameters_checked"],
        "nonfinite_parameter_diagnostics": audit["nonfinite_parameter_diagnostics"],
        "audit_status": audit["status"],
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
        row["max_tree_depth_observed"] = int(td.max())
    else:
        row["max_tree_depth_observed"] = np.nan

    hits, hit_fraction = _max_treedepth_hits(idata.sample_stats)
    row["max_tree_depth_hits"] = hits
    row["fraction_reached_max_tree_depth"] = hit_fraction

    if audit["diagnostic_gate_passed"] and "log_likelihood" in idata.groups():
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

    # Keep MCMC convergence separate from predictive-importance diagnostics.
    sampler_review = not audit["diagnostic_gate_passed"]
    row["sampling_status"] = "REVIEW" if sampler_review else "PASS_PENDING_SCIENTIFIC_REVIEW"

    if np.isnan(row["pareto_k_gt_0_7"]):
        row["loo_status"] = "SKIPPED_DIAGNOSTIC_GATE" if sampler_review else "NOT_AVAILABLE"
    elif row["pareto_k_gt_0_7"] > 0:
        row["loo_status"] = "REVIEW"
    else:
        row["loo_status"] = "PASS"

    if not sampler_review and row["loo_status"] == "REVIEW":
        row["diagnostic_status"] = "PASS_SAMPLING_LOO_REVIEW_PENDING_SCIENTIFIC_REVIEW"
    elif row["sampling_status"] == "REVIEW":
        row["diagnostic_status"] = "SAMPLING_REVIEW"
    else:
        row["diagnostic_status"] = "PASS_PENDING_SCIENTIFIC_REVIEW"

    idata.close()
    return row


def main():
    rows = []
    for name, path in MODELS.items():
        if path.exists():
            rows.append(summarize_model(name, path))
        else:
            rows.append({
                "model": name,
                "sampling_status": "FILE_MISSING",
                "loo_status": "FILE_MISSING",
                "diagnostic_status": "FILE_MISSING",
            })

    table = pd.DataFrame(rows)
    table.to_csv(TABLES / "final_production_diagnostics.csv", index=False)
    print(table.to_string(index=False))


if __name__ == "__main__":
    main()
