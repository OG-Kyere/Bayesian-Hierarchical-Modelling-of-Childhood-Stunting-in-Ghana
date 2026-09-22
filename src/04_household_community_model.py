"""Model 1: Bayesian logistic model with household and community random intercepts.

Raw DHS data are never committed. Place GHPR8CFL.DTA under data/raw/.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pymc as pm
import arviz as az

SEED = 20260922
RAW = Path("data/raw/GHPR8CFL.DTA")
OUT = Path("results/model_outputs")
TABLES = Path("results/tables")
OUT.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)


def prepare_data(path=RAW):
    df = pd.read_stata(path, convert_categoricals=True)

    # hv103 identifies whether the person slept in the household the previous night
    # (the de facto population used for DHS child anthropometry).
    hc1_num = pd.to_numeric(df["hc1"], errors="coerce")
    hc70_num = pd.to_numeric(df["hc70"], errors="coerce")
    keep = (
        df["hv103"].astype(str).eq("yes")
        & hc1_num.between(0, 59)
        & hc70_num.between(-600, 600)
    )
    d = df.loc[keep].copy()
    d["hc1_num"] = hc1_num.loc[keep]
    d["hc70_num"] = hc70_num.loc[keep]

    d["stunted"] = (d["hc70_num"] < -200).astype("int8")
    d["age_group"] = pd.cut(
        d["hc1_num"],
        bins=[-0.1, 5, 11, 23, 35, 47, 59],
        labels=["0-5", "6-11", "12-23", "24-35", "36-47", "48-59"],
    )
    d["household_id"] = (
        d["hv001"].astype(int).astype(str)
        + "_"
        + d["hv002"].astype(int).astype(str)
    )

    # Fixed effects, with thesis reference categories:
    fixed = pd.DataFrame(index=d.index)
    fixed["male"] = (d["hv104"] == "male").astype(float)
    fixed["rural"] = (d["hv025"] == "rural").astype(float)

    age = pd.get_dummies(d["age_group"], prefix="age", dtype=float)
    age = age.drop(columns=["age_0-5"])

    wealth = pd.get_dummies(d["hv270"], prefix="wealth", dtype=float)
    wealth = wealth.drop(columns=["wealth_poorest"])

    region = pd.get_dummies(d["hv024"], prefix="region", dtype=float)
    region = region.drop(columns=["region_western"])

    X = pd.concat([fixed[["male"]], age, wealth, region, fixed[["rural"]]], axis=1)
    X = X.astype(float)

    community_codes, community_levels = pd.factorize(d["hv001"], sort=True)
    household_codes, household_levels = pd.factorize(d["household_id"], sort=True)

    return d, X, community_codes, household_codes, community_levels, household_levels


def fit_model():
    d, X, community_idx, household_idx, communities, households = prepare_data()

    coords = {
        "obs": np.arange(len(d)),
        "coef": X.columns.tolist(),
        "community": np.arange(len(communities)),
        "household": np.arange(len(households)),
    }

    with pm.Model(coords=coords) as model:
        x = pm.Data("X", X.to_numpy(), dims=("obs", "coef"))
        ci = pm.Data("community_idx", community_idx, dims="obs")
        hi = pm.Data("household_idx", household_idx, dims="obs")

        alpha = pm.Normal("alpha", mu=0.0, sigma=1.5)
        beta = pm.Normal("beta", mu=0.0, sigma=1.0, dims="coef")

        tau_community = pm.HalfNormal("tau_community", sigma=1.0)
        z_community = pm.Normal("z_community", 0.0, 1.0, dims="community")
        u_community = pm.Deterministic(
            "u_community", tau_community * z_community, dims="community"
        )

        tau_household = pm.HalfNormal("tau_household", sigma=1.0)
        z_household = pm.Normal("z_household", 0.0, 1.0, dims="household")
        u_household = pm.Deterministic(
            "u_household", tau_household * z_household, dims="household"
        )

        eta = (
            alpha
            + pm.math.dot(x, beta)
            + u_community[ci]
            + u_household[hi]
        )

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
        )

        pm.sample_posterior_predictive(
            idata,
            var_names=["stunted"],
            extend_inferencedata=True,
            random_seed=SEED,
        )

    # Derived variance quantities from every posterior draw.
    tc = idata.posterior["tau_community"]
    th = idata.posterior["tau_household"]
    logistic_var = np.pi**2 / 3

    total_var = tc**2 + th**2 + logistic_var
    idata.posterior["icc_community"] = tc**2 / total_var
    idata.posterior["vpc_household"] = th**2 / total_var
    idata.posterior["icc_same_household"] = (tc**2 + th**2) / total_var

    q75 = 0.6744897501960817
    idata.posterior["mor_community"] = np.exp(np.sqrt(2) * q75 * tc)
    idata.posterior["mor_household"] = np.exp(np.sqrt(2) * q75 * th)

    idata.to_netcdf(OUT / "model1_household_community.nc")

    summary = az.summary(
        idata,
        var_names=[
            "alpha",
            "beta",
            "tau_community",
            "tau_household",
            "icc_community",
            "vpc_household",
            "icc_same_household",
            "mor_community",
            "mor_household",
        ],
        hdi_prob=0.95,
    )
    summary.to_csv(TABLES / "model1_posterior_summary.csv")

    # Basic reproducibility checks.
    print(f"N children: {len(d)}")
    print(f"Stunted: {int(d['stunted'].sum())}")
    print(f"Communities: {d['hv001'].nunique()}")
    print(f"Households: {d['household_id'].nunique()}")
    print(summary)
    print("Divergences:", int(idata.sample_stats["diverging"].sum()))

    return idata


if __name__ == "__main__":
    fit_model()
