"""Model 0: community-level Bayesian pilot model.

This reproduces the project's original community-only pilot specification.
It is retained as a baseline check; the substantive analysis uses the later
household + community models.

Expected input
--------------
data/raw/GHPR8CFL.DTA
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pymc as pm
import arviz as az

RAW = Path("data/raw/GHPR8CFL.DTA")
OUT = Path("results/model_outputs")
TABLES = Path("results/tables")
OUT.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)

SEED = 20260922


def prepare_data():
    if not RAW.exists():
        raise FileNotFoundError(
            f"{RAW} was not found. Place the authorized 2022 Ghana DHS "
            "PR recode at data/raw/GHPR8CFL.DTA."
        )

    df = pd.read_stata(RAW, convert_categoricals=True)
    age = pd.to_numeric(df["hc1"], errors="coerce")
    haz = pd.to_numeric(df["hc70"], errors="coerce")

    keep = (
        df["hv103"].astype(str).eq("yes")
        & age.between(0, 59)
        & haz.between(-600, 600)
    )
    d = df.loc[keep].copy()
    d["age_num"] = age.loc[keep]
    d["stunted"] = (haz.loc[keep] < -200).astype("int8")
    d["age_group"] = pd.cut(
        d["age_num"],
        [-0.1, 5, 11, 23, 35, 47, 59],
        labels=["0-5", "6-11", "12-23", "24-35", "36-47", "48-59"],
    )

    fixed = pd.DataFrame(index=d.index)
    fixed["male"] = (d["hv104"].astype(str) == "male").astype(float)
    fixed["rural"] = (d["hv025"].astype(str) == "rural").astype(float)

    age_d = pd.get_dummies(
        d["age_group"], prefix="age", dtype=float
    ).drop(columns=["age_0-5"])
    wealth = pd.get_dummies(
        d["hv270"].astype(str), prefix="wealth", dtype=float
    ).drop(columns=["wealth_poorest"])
    region = pd.get_dummies(
        d["hv024"].astype(str), prefix="region", dtype=float
    ).drop(columns=["region_western"])

    X = pd.concat(
        [fixed[["male"]], age_d, wealth, region, fixed[["rural"]]],
        axis=1,
    ).astype(float)

    community_idx, communities = pd.factorize(d["hv001"], sort=True)
    return d, X, community_idx, communities


def main():
    d, X, community_idx, communities = prepare_data()

    coords = {
        "obs": np.arange(len(d)),
        "coef": X.columns.tolist(),
        "community": np.arange(len(communities)),
    }

    with pm.Model(coords=coords):
        x = pm.Data("X", X.to_numpy(), dims=("obs", "coef"))
        ci = pm.Data("community_idx", community_idx, dims="obs")

        alpha = pm.Normal("alpha", 0.0, 1.5)
        beta = pm.Normal("beta", 0.0, 1.0, dims="coef")

        tau_c = pm.HalfNormal("tau_community", 1.0)
        z_c = pm.Normal("z_community", 0.0, 1.0, dims="community")
        u_c = pm.Deterministic(
            "u_community", tau_c * z_c, dims="community"
        )

        eta = alpha + pm.math.dot(x, beta) + u_c[ci]

        pm.Bernoulli(
            "stunted",
            logit_p=eta,
            observed=d["stunted"].to_numpy(),
            dims="obs",
        )

        idata = pm.sample(
            draws=1000,
            tune=1000,
            chains=4,
            target_accept=0.95,
            random_seed=SEED,
            return_inferencedata=True,
            idata_kwargs={"log_likelihood": True},
        )

    tc = idata.posterior["tau_community"]
    logistic_var = np.pi**2 / 3
    idata.posterior["icc_community"] = tc**2 / (tc**2 + logistic_var)
    q75 = 0.6744897501960817
    idata.posterior["mor_community"] = np.exp(np.sqrt(2) * q75 * tc)

    idata.to_netcdf(OUT / "model0_community_pilot.nc")

    summary = az.summary(
        idata,
        var_names=[
            "alpha", "beta", "tau_community",
            "icc_community", "mor_community",
        ],
        hdi_prob=0.95,
    )
    summary.to_csv(TABLES / "model0_community_pilot_summary.csv")

    print(f"N children: {len(d)}")
    print(f"Communities: {len(communities)}")
    print(f"Divergences: {int(idata.sample_stats['diverging'].sum())}")
    print(summary)

    return idata


if __name__ == "__main__":
    main()
