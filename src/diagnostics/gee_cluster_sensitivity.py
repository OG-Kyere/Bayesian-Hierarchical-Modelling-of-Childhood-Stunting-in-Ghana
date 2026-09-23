"""Interim clustering diagnostic using GEE.

This is NOT the primary Bayesian model. It is an independent sensitivity check
used while the PyMC/NUTS environment is unavailable. The exchangeable working
correlations quantify residual dependence at the household and community levels
but are not interpreted as Bayesian variance components or ICCs.
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


def prepare_data():
    df = pd.read_stata(RAW, convert_categoricals=True)
    hc1 = pd.to_numeric(df["hc1"], errors="coerce")
    hc70 = pd.to_numeric(df["hc70"], errors="coerce")
    keep = (
        df["hv103"].astype(str).eq("yes")
        & hc1.between(0, 59)
        & hc70.between(-600, 600)
    )
    d = df.loc[keep].copy()
    d["age"] = hc1.loc[keep]
    d["stunted"] = (hc70.loc[keep] < -200).astype(int)
    d["community"] = pd.to_numeric(d["hv001"], errors="coerce").astype(int).astype(str)
    d["household"] = (
        d["community"]
        + "_"
        + pd.to_numeric(d["hv002"], errors="coerce").astype(int).astype(str)
    )
    d["age_group"] = pd.cut(
        d["age"], [-0.1, 5, 11, 23, 35, 47, 59],
        labels=["0-5", "6-11", "12-23", "24-35", "36-47", "48-59"]
    )
    return d


FORMULA = (
    'stunted ~ C(age_group, Treatment(reference="0-5"))'
    ' + C(hv104, Treatment(reference="female"))'
    ' + C(hv270, Treatment(reference="poorest"))'
    ' + C(hv024, Treatment(reference="western"))'
    ' + C(hv025, Treatment(reference="urban"))'
)


def fit_gee(d, group):
    model = smf.gee(
        FORMULA,
        groups=group,
        data=d,
        family=sm.families.Binomial(),
        cov_struct=Exchangeable(),
    )
    result = model.fit(maxiter=100)

    table = pd.DataFrame({
        "term": result.params.index,
        "coef": result.params.values,
        "robust_se": result.bse.values,
    })
    table["OR"] = np.exp(table["coef"])
    table["OR_l95"] = np.exp(table["coef"] - 1.96 * table["robust_se"])
    table["OR_u95"] = np.exp(table["coef"] + 1.96 * table["robust_se"])
    return result, table


def main():
    d = prepare_data()
    rows = []
    for group in ["household", "community"]:
        result, table = fit_gee(d, group)
        table.to_csv(OUT / f"gee_{group}.csv", index=False)
        rows.append({
            "grouping_level": group,
            "exchangeable_working_correlation": float(result.cov_struct.dep_params),
        })

    pd.DataFrame(rows).to_csv(
        OUT / "gee_working_correlations.csv", index=False
    )


if __name__ == "__main__":
    main()
