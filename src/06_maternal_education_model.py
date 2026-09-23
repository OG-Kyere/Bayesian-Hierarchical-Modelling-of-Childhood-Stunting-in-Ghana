"""Model 3: WASH model extended with maternal education.

Model 3 is fitted only to children with linked maternal-education information so
its results can be compared with the harmonized Model 2 on the same observations.
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

IMPROVED_WATER = {
    "piped into dwelling", "piped to yard/plot", "piped to neighbor",
    "public tap/standpipe", "tube well or borehole", "protected well",
    "protected spring", "rainwater", "tanker truck", "cart with small tank",
    "bottled water", "sachet water",
}
IMPROVED_SANITATION = {
    "flush to piped sewer system", "flush to septic tank", "flush to pit latrine",
    "flush, bio-digester (biofil)", "ventilated improved pit latrine (vip)",
    "pit latrine with slab", "composting toilet",
}

def prepare_base(complete_maternal=False):
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
        d["age_num"], [-0.1, 5, 11, 23, 35, 47, 59],
        labels=["0-5", "6-11", "12-23", "24-35", "36-47", "48-59"],
    )
    d["household_id"] = (
        pd.to_numeric(d["hv001"], errors="coerce").astype(int).astype(str)
        + "_"
        + pd.to_numeric(d["hv002"], errors="coerce").astype(int).astype(str)
    )
    d["water_unimproved"] = (~d["hv201"].astype(str).isin(IMPROVED_WATER)).astype(float)
    d["sanitation_unimproved"] = (~d["hv205"].astype(str).isin(IMPROVED_SANITATION)).astype(float)

    if complete_maternal:
        d = d.loc[d["hc61"].notna()].copy()

    fixed = pd.DataFrame(index=d.index)
    fixed["male"] = (d["hv104"].astype(str) == "male").astype(float)
    fixed["rural"] = (d["hv025"].astype(str) == "rural").astype(float)

    age_d = pd.get_dummies(d["age_group"], prefix="age", dtype=float).drop(columns=["age_0-5"])
    wealth = pd.get_dummies(d["hv270"].astype(str), prefix="wealth", dtype=float).drop(columns=["wealth_poorest"])
    region = pd.get_dummies(d["hv024"].astype(str), prefix="region", dtype=float).drop(columns=["region_western"])

    parts = [
        fixed[["male"]], age_d, wealth, region, fixed[["rural"]],
        d[["water_unimproved", "sanitation_unimproved"]].astype(float),
    ]
    return d, parts


def fit_hierarchical(d, X, output_stem, seed=20260922):
    community_idx, communities = pd.factorize(d["hv001"], sort=True)
    household_idx, households = pd.factorize(d["household_id"], sort=True)

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

        alpha = pm.Normal("alpha", 0.0, 1.5)
        beta = pm.Normal("beta", 0.0, 1.0, dims="coef")

        tau_c = pm.HalfNormal("tau_community", 1.0)
        z_c = pm.Normal("z_community", 0.0, 1.0, dims="community")
        u_c = pm.Deterministic("u_community", tau_c * z_c, dims="community")

        tau_h = pm.HalfNormal("tau_household", 1.0)
        z_h = pm.Normal("z_household", 0.0, 1.0, dims="household")
        u_h = pm.Deterministic("u_household", tau_h * z_h, dims="household")

        eta = alpha + pm.math.dot(x, beta) + u_c[ci] + u_h[hi]
        pm.Bernoulli("stunted", logit_p=eta, observed=d["stunted"].to_numpy(), dims="obs")

        idata = pm.sample(
            draws=1000, tune=1000, chains=4, target_accept=0.95,
            random_seed=seed, return_inferencedata=True,
            idata_kwargs={"log_likelihood": True},
        )
        pm.sample_posterior_predictive(
            idata, var_names=["stunted"], random_seed=seed, extend_inferencedata=True
        )

    tc = idata.posterior["tau_community"]
    th = idata.posterior["tau_household"]
    total = tc**2 + th**2 + np.pi**2 / 3
    idata.posterior["icc_community"] = tc**2 / total
    idata.posterior["vpc_household"] = th**2 / total
    idata.posterior["icc_same_household"] = (tc**2 + th**2) / total
    q75 = 0.6744897501960817
    idata.posterior["mor_community"] = np.exp(np.sqrt(2) * q75 * tc)
    idata.posterior["mor_household"] = np.exp(np.sqrt(2) * q75 * th)

    idata.to_netcdf(OUT / f"{output_stem}.nc")
    summary = az.summary(
        idata,
        var_names=[
            "alpha", "beta", "tau_community", "tau_household",
            "icc_community", "vpc_household", "icc_same_household",
            "mor_community", "mor_household",
        ],
        hdi_prob=0.95,
    )
    summary.to_csv(TABLES / f"{output_stem}_posterior_summary.csv")
    return idata


def main():
    d, parts = prepare_base(complete_maternal=True)
    maternal = pd.get_dummies(
        d["hc61"].astype(str), prefix="maternal_education", dtype=float
    ).drop(columns=["maternal_education_no education"])
    parts.append(maternal)
    X = pd.concat(parts, axis=1).astype(float)
    fit_hierarchical(d, X, "model3_maternal_education", seed=20261322)


if __name__ == "__main__":
    main()
