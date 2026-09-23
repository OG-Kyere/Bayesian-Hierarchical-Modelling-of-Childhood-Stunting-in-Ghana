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
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from stunting_data import load_data
    d, _ = load_data(RAW)
    d['community'] = d.hv001.astype(str)
    d['household'] = d.household_id
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
