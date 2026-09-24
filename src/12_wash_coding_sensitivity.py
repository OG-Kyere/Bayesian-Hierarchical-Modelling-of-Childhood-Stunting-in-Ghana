"""Bayesian sensitivity analysis for alternative WASH coding.

Replaces the binary WASH indicators in Model 3 with:
- water: improved / unprotected groundwater / surface water
- sanitation: improved / other unimproved / open defecation

This tests whether the primary binary WASH association is driven by a specific
high-risk source or sanitation subgroup.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import pymc as pm

RAW = Path("data/raw/GHPR8CFL.DTA")
OUT = Path("results/model_outputs")
OUT.mkdir(parents=True, exist_ok=True)

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


def prepare():
    df = pd.read_stata(RAW, convert_categoricals=True)
    age = pd.to_numeric(df["hc1"], errors="coerce")
    haz = pd.to_numeric(df["hc70"], errors="coerce")
    keep = (
        df["hv103"].astype(str).eq("yes")
        & age.between(0, 59)
        & haz.between(-600, 600)
        & df["hc61"].notna()
    )
    d = df.loc[keep].copy()
    d["age_num"] = age.loc[keep]
    d["stunted"] = (haz.loc[keep] < -200).astype(int)
    d["age_group"] = pd.cut(
        d["age_num"], [-0.1, 5, 11, 23, 35, 47, 59],
        labels=["0-5", "6-11", "12-23", "24-35", "36-47", "48-59"],
    )
    d["household_id"] = (
        pd.to_numeric(d["hv001"], errors="coerce").astype(int).astype(str)
        + "_"
        + pd.to_numeric(d["hv002"], errors="coerce").astype(int).astype(str)
    )

    water = d["hv201"].astype(str)
    sanitation = d["hv205"].astype(str)
    d["water3"] = np.where(
        water.eq("river/dam/lake/ponds/stream/canal/irrigation channel"),
        "surface water",
        np.where(
            water.isin(["unprotected well", "unprotected spring"]),
            "unprotected groundwater",
            "improved",
        ),
    )
    d["san3"] = np.where(
        sanitation.eq("no facility/bush/field"),
        "open defecation",
        np.where(
            sanitation.isin(IMPROVED_SANITATION),
            "improved",
            "other unimproved",
        ),
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
    maternal = pd.get_dummies(
        d["hc61"].astype(str), prefix="maternal_education", dtype=float
    ).drop(columns=["maternal_education_no education"])
    water_d = pd.get_dummies(
        d["water3"], prefix="water", dtype=float
    ).drop(columns=["water_improved"])
    san_d = pd.get_dummies(
        d["san3"], prefix="sanitation", dtype=float
    ).drop(columns=["sanitation_improved"])

    X = pd.concat(
        [
            fixed[["male"]], age_d, wealth, region, fixed[["rural"]],
            water_d, san_d, maternal,
        ],
        axis=1,
    ).astype(float)

    ci, communities = pd.factorize(d["hv001"], sort=True)
    hi, households = pd.factorize(d["household_id"], sort=True)
    return d, X, ci, hi, communities, households


def main():
    d, X, ci, hi, communities, households = prepare()

    coords = {
        "obs": np.arange(len(d)),
        "coef": X.columns.tolist(),
        "community": np.arange(len(communities)),
        "household": np.arange(len(households)),
    }

    with pm.Model(coords=coords):
        x = pm.Data("X", X.to_numpy(), dims=("obs", "coef"))
        c = pm.Data("community_idx", ci, dims="obs")
        h = pm.Data("household_idx", hi, dims="obs")

        alpha = pm.Normal("alpha", 0, 1.5)
        beta = pm.Normal("beta", 0, 1, dims="coef")
        tau_c = pm.HalfNormal("tau_community", 1)
        z_c = pm.Normal("z_community", 0, 1, dims="community")
        tau_h = pm.HalfNormal("tau_household", 1)
        z_h = pm.Normal("z_household", 0, 1, dims="household")

        eta = alpha + pm.math.dot(x, beta) + tau_c * z_c[c] + tau_h * z_h[h]
        pm.Bernoulli(
            "stunted",
            logit_p=eta,
            observed=d["stunted"].to_numpy(),
            dims="obs",
        )

        idata = pm.sample(
            draws=1500,
            tune=2000,
            chains=4,
            target_accept=0.99,
            random_seed=20262500,
            return_inferencedata=True,
            idata_kwargs={"log_likelihood": True},
        )

    idata.to_netcdf(OUT / "model3_detailed_wash_sensitivity.nc")


if __name__ == "__main__":
    main()
