"""Functional-form and WASH-coding robustness diagnostics using GEE.

These are independent robustness checks, not replacements for the Bayesian
hierarchical models. They test whether major fixed-effect conclusions depend on
(1) categorical age bands versus a smooth spline for age and
(2) binary versus more detailed WASH coding.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.genmod.cov_struct import Exchangeable

RAW = Path("data/raw/GHPR8CFL.DTA")
OUT = Path("results/diagnostics")
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
    d["age_num"] = age.loc[keep].astype(float)
    d["stunted"] = (haz.loc[keep] < -200).astype(int)
    d["community"] = pd.to_numeric(d["hv001"], errors="coerce").astype(int).astype(str)
    d["household"] = (
        d["community"] + "_"
        + pd.to_numeric(d["hv002"], errors="coerce").astype(int).astype(str)
    )
    d["age_group"] = pd.cut(
        d["age_num"], [-0.1, 5, 11, 23, 35, 47, 59],
        labels=["0-5", "6-11", "12-23", "24-35", "36-47", "48-59"],
    )

    water = d["hv201"].astype(str)
    sanitation = d["hv205"].astype(str)
    d["water_unimproved"] = (~water.isin(IMPROVED_WATER)).astype(int)
    d["sanitation_unimproved"] = (~sanitation.isin(IMPROVED_SANITATION)).astype(int)

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
        np.where(sanitation.isin(IMPROVED_SANITATION), "improved", "other unimproved"),
    )
    return d


def fit(formula, d):
    return smf.gee(
        formula,
        groups="household",
        data=d,
        family=sm.families.Binomial(),
        cov_struct=Exchangeable(),
    ).fit()


def tidy(result, model):
    tab = pd.DataFrame({
        "term": result.params.index,
        "coef": result.params.values,
        "robust_se": result.bse.values,
    })
    tab["OR"] = np.exp(tab["coef"])
    tab["l95"] = np.exp(tab["coef"] - 1.96 * tab["robust_se"])
    tab["u95"] = np.exp(tab["coef"] + 1.96 * tab["robust_se"])
    tab["model"] = model
    tab["working_correlation"] = float(result.cov_struct.dep_params)
    return tab


def main():
    d = prepare()

    common = (
        ' + C(hv104, Treatment(reference="female"))'
        ' + C(hv270, Treatment(reference="poorest"))'
        ' + C(hv024, Treatment(reference="western"))'
        ' + C(hv025, Treatment(reference="urban"))'
        ' + C(hc61, Treatment(reference="no education"))'
    )

    categorical_age = (
        'stunted ~ C(age_group, Treatment(reference="0-5"))'
        + common
        + " + water_unimproved + sanitation_unimproved"
    )
    spline_age = (
        "stunted ~ bs(age_num, df=4, degree=3, include_intercept=False)"
        + common
        + " + water_unimproved + sanitation_unimproved"
    )
    detailed_wash = (
        'stunted ~ C(age_group, Treatment(reference="0-5"))'
        + common
        + ' + C(water3, Treatment(reference="improved"))'
        + ' + C(san3, Treatment(reference="improved"))'
    )

    results = [
        tidy(fit(categorical_age, d), "categorical_age_binary_wash"),
        tidy(fit(spline_age, d), "spline_age_binary_wash"),
        tidy(fit(detailed_wash, d), "categorical_age_detailed_wash"),
    ]
    pd.concat(results, ignore_index=True).to_csv(
        OUT / "gee_functional_form_wash_sensitivity.csv", index=False
    )


if __name__ == "__main__":
    main()
