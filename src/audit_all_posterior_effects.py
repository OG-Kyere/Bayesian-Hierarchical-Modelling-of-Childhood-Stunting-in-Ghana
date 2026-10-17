"""Private, read-only Bayesian posterior convergence audit.

Run from repository root after obtaining authorised posterior NetCDF files:
    python src/audit_all_posterior_effects.py

Prints aggregate diagnostics to standard output; does not write any report files.
Never upload full parameter-level outputs or NetCDF files without privacy review.
Exit 2 on missing files or review-level diagnostic concerns.
"""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import arviz as az

MODELS = {
    "model1": "model1_household_community.nc",
    "model2_full": "model2_wash_full.nc",
    "model2_harmonized": "model2_wash_harmonized.nc",
    "model3": "model3_maternal_education.nc",
}
ROOT = Path("results/model_outputs")
LIMIT_RHAT = 1.01
MIN_ESS = 400

def worst_metrics(idata, var):
    """Summarise all elements of a variable without disclosing factor labels."""
    summary = az.summary(idata, var_names=[var], kind="diagnostics", round_to=None)
    vals = summary[["r_hat", "ess_bulk", "ess_tail"]].replace([np.inf, -np.inf], np.nan)
    bad = int(((vals["r_hat"] > LIMIT_RHAT) |
               (vals["ess_bulk"] < MIN_ESS) |
               (vals["ess_tail"] < MIN_ESS) |
               vals.isna().any(axis=1)).sum())
    return {
        "parameter": var,
        "elements": len(vals),
        "max_rhat": float(vals["r_hat"].max()),
        "min_ess_bulk": float(vals["ess_bulk"].min()),
        "min_ess_tail": float(vals["ess_tail"].min()),
        "elements_requiring_review": bad,
    }

def inspect(model_name, path):
    idata = az.from_netcdf(path)
    if "posterior" not in idata.groups():
        raise ValueError("No posterior group")
    required = ("alpha", "beta", "tau_community", "tau_household",
                "z_community", "z_household", "u_community", "u_household")
    available = set(idata.posterior.data_vars)
    missing = [v for v in required if v not in available]
    if missing:
        raise ValueError(f"Missing required variables: {missing}")
    chains = int(idata.posterior.sizes.get("chain", 0))
    draws = int(idata.posterior.sizes.get("draw", 0))
    if chains < 2 or draws < 4:
        raise ValueError(f"Too few chains/draws: {chains}, {draws}")
    rows = [dict(model=model_name, chains=chains, draws_per_chain=draws,
                 **worst_metrics(idata, v)) for v in required]
    for name in ("icc_community", "vpc_household", "icc_same_household",
                 "mor_community", "mor_household"):
        if name in available:
            rows.append(dict(model=model_name, chains=chains,
                             draws_per_chain=draws, **worst_metrics(idata, name)))
    divergences = (int(idata.sample_stats["diverging"].sum())
                   if "sample_stats" in idata.groups() and
                   "diverging" in idata.sample_stats else None)
    bfmi = [float(v) for v in np.asarray(az.bfmi(idata))] if "sample_stats" in idata.groups() else []
    print(f"{model_name}: chains={chains}, retained_draws={draws}, "
          f"divergences={divergences}, min_BFMI={min(bfmi) if bfmi else 'NA'}")
    return rows, divergences, bfmi

def main():
    all_rows = []
    problems = []
    for name, filename in MODELS.items():
        path = ROOT / filename
        if not path.is_file():
            problems.append(f"{name}: private NetCDF not accessible at {path}")
            continue
        try:
            rows, divergences, bfmi = inspect(name, path)
            all_rows.extend(rows)
            if divergences is None or divergences > 0:
                problems.append(f"{name}: divergences missing or nonzero")
            if not bfmi or min(bfmi) < 0.3:
                problems.append(f"{name}: BFMI missing or below 0.3")
            if any(row["elements_requiring_review"] for row in rows):
                problems.append(f"{name}: some posterior components require review")
        except Exception as exc:
            problems.append(f"{name}: audit unable to complete: {exc}")
    if all_rows:
        table = pd.DataFrame(all_rows)
        pd.set_option("display.max_rows", None)
        print("\nAGGREGATE convergence report (no individual random-effect IDs):")
        print(table.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    for problem in problems:
        print("REVIEW:", problem, file=sys.stderr)
    return 2 if problems else 0

if __name__ == "__main__":
    raise SystemExit(main())
