"""Reproduce design-adjusted descriptive results and public figures from authorized 2022 GDHS PR data.

Requirements
------------
Place GHPR8CFL.DTA in data/raw/. Raw or row-level DHS data must not be committed.
All public outputs are aggregate and non-identifying.

Descriptive standard errors use Taylor linearization for a ratio estimator,
with hv021 as PSU and hv022 as sampling stratum. This reproduces the national
stunting SE reported in the 2022 GDHS Appendix B.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

RAW = Path("data/raw/GHPR8CFL.DTA")
TABLE_DIR = Path("results/tables")
FIG_DIR = Path("results/figures")
TABLE_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

AGE_ORDER = ["0-5", "6-11", "12-23", "24-35", "36-47", "48-59"]
WEALTH_ORDER = ["poorest", "poorer", "middle", "richer", "richest"]
MAT_ED_ORDER = ["no education", "primary", "secondary", "higher", "Missing"]

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
    full = pd.read_stata(RAW, convert_categoricals=True)
    full["stratum"] = full["hv022"].astype(str)
    full["psu"] = pd.to_numeric(full["hv021"], errors="coerce").astype("Int64")
    psu_frame = full[["stratum", "psu"]].drop_duplicates()

    hc1_num = pd.to_numeric(full["hc1"], errors="coerce")
    hc70_num = pd.to_numeric(full["hc70"], errors="coerce")
    keep = (
        full["hv103"].astype(str).eq("yes")
        & hc1_num.between(0, 59)
        & hc70_num.between(-600, 600)
    )

    d = full.loc[keep].copy()
    d["hc1_num"] = hc1_num.loc[keep]
    d["hc70_num"] = hc70_num.loc[keep]
    d["stunted"] = (d["hc70_num"] < -200).astype(int)
    d["weight"] = pd.to_numeric(d["hv005"], errors="coerce") / 1_000_000
    d["age_group"] = pd.cut(
        d["hc1_num"], [-0.1, 5, 11, 23, 35, 47, 59], labels=AGE_ORDER
    )
    d["household_id"] = (
        pd.to_numeric(d["hv001"], errors="coerce").astype(int).astype(str)
        + "_"
        + pd.to_numeric(d["hv002"], errors="coerce").astype(int).astype(str)
    )
    d["maternal_education"] = d["hc61"].astype(str).replace("nan", np.nan)
    d["water_source_group"] = np.where(
        d["hv201"].astype(str).isin(IMPROVED_WATER),
        "Improved source", "Unimproved source"
    )
    d["sanitation_group"] = np.where(
        d["hv205"].astype(str).isin(IMPROVED_SANITATION),
        "Improved facility", "Unimproved/no facility"
    )
    return d, psu_frame


def taylor_ratio(d, psu_frame, mask):
    """Weighted prevalence and Taylor-linearized SE for a survey domain."""
    sub = d.loc[mask, ["stratum", "psu", "weight", "stunted"]].copy()
    sub["x"] = sub["weight"]
    sub["y"] = sub["weight"] * sub["stunted"]

    agg = (
        sub.groupby(["stratum", "psu"], observed=True)[["x", "y"]]
        .sum()
        .reset_index()
    )
    work = psu_frame.merge(agg, on=["stratum", "psu"], how="left")
    work[["x", "y"]] = work[["x", "y"]].fillna(0.0)

    x_total = work["x"].sum()
    y_total = work["y"].sum()
    estimate = y_total / x_total
    work["z"] = work["y"] - estimate * work["x"]

    numerator = 0.0
    for _, g in work.groupby("stratum", observed=True):
        m = len(g)
        if m > 1:
            zbar = g["z"].mean()
            numerator += m / (m - 1) * ((g["z"] - zbar) ** 2).sum()

    se = np.sqrt(numerator / x_total**2)
    lower = max(0.0, estimate - 1.96 * se)
    upper = min(1.0, estimate + 1.96 * se)
    return estimate, se, lower, upper


def summarize(d, psu_frame):
    groups = {
        "overall": pd.Series("All", index=d.index),
        "age_group": d["age_group"],
        "sex": d["hv104"].astype(str),
        "wealth": d["hv270"].astype(str),
        "residence": d["hv025"].astype(str),
        "region": d["hv024"].astype(str),
        "maternal_education": d["maternal_education"].fillna("Missing"),
        "water_source": d["water_source_group"],
        "sanitation": d["sanitation_group"],
    }

    rows = []
    for variable, series in groups.items():
        for category in pd.unique(series.astype(str)):
            mask = series.astype(str).eq(category)
            estimate, se, lower, upper = taylor_ratio(d, psu_frame, mask)
            rows.append({
                "variable": variable,
                "category": str(category),
                "n_unweighted": int(mask.sum()),
                "stunted_unweighted": int(d.loc[mask, "stunted"].sum()),
                "weighted_prevalence": estimate,
                "design_se": se,
                "ci95_lower": lower,
                "ci95_upper": upper,
            })
    return pd.DataFrame(rows)


def plot_group(summary, variable, title, filename, order=None, horizontal=False):
    s = summary.loc[summary["variable"].eq(variable)].copy()
    if order is not None:
        s["category"] = pd.Categorical(s["category"], categories=order, ordered=True)
        s = s.sort_values("category")

    values = 100 * s["weighted_prevalence"].to_numpy()
    lower = 100 * s["ci95_lower"].to_numpy()
    upper = 100 * s["ci95_upper"].to_numpy()
    errors = np.vstack([values - lower, upper - values])
    labels = s["category"].astype(str).to_numpy()

    fig, ax = plt.subplots(figsize=(8, 5.2))
    if horizontal:
        y = np.arange(len(s))
        ax.barh(y, values, xerr=errors, capsize=3)
        ax.set_yticks(y, labels)
        ax.set_xlabel("Weighted stunting prevalence (%)")
        for i, value in enumerate(values):
            ax.text(value + errors[1, i] + 0.4, i, f"{value:.1f}%", va="center", fontsize=9)
    else:
        x = np.arange(len(s))
        ax.bar(x, values, yerr=errors, capsize=3)
        ax.set_xticks(x, labels, rotation=35, ha="right")
        ax.set_ylabel("Weighted stunting prevalence (%)")
        for i, value in enumerate(values):
            ax.text(i, upper[i] + 0.5, f"{value:.1f}%", ha="center", fontsize=9)
        ax.set_ylim(0, max(upper) * 1.18)

    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(FIG_DIR / filename, format="svg")
    plt.close(fig)


def main():
    d, psu_frame = prepare()
    summary = summarize(d, psu_frame)
    summary.to_csv(TABLE_DIR / "descriptive_all.csv", index=False)

    hh = d.groupby("household_id").size()
    hh_table = hh.value_counts().sort_index().rename_axis(
        "eligible_children_in_household"
    ).reset_index(name="n_households")
    hh_table["percent_households"] = (
        100 * hh_table["n_households"] / hh_table["n_households"].sum()
    )
    hh_table.to_csv(TABLE_DIR / "household_structure.csv", index=False)

    overall = summary.loc[summary["variable"].eq("overall")].iloc[0]
    sample = pd.DataFrame({
        "metric": [
            "eligible_children", "stunted_unweighted", "weighted_stunting_prevalence",
            "weighted_stunting_design_se", "weighted_stunting_ci95_lower",
            "weighted_stunting_ci95_upper", "weighted_denominator",
            "communities", "households", "multi_child_households",
            "children_in_multi_child_households", "maternal_education_missing_n",
            "maternal_education_missing_percent",
        ],
        "value": [
            len(d), int(d["stunted"].sum()), overall["weighted_prevalence"],
            overall["design_se"], overall["ci95_lower"], overall["ci95_upper"],
            d["weight"].sum(), d["hv001"].nunique(), d["household_id"].nunique(),
            int((hh > 1).sum()),
            int(d[d["household_id"].isin(hh[hh > 1].index)].shape[0]),
            int(d["maternal_education"].isna().sum()),
            100 * d["maternal_education"].isna().mean(),
        ],
    })
    sample.to_csv(TABLE_DIR / "analysis_sample_summary.csv", index=False)

    plot_group(summary, "age_group", "Weighted stunting prevalence by child age",
               "stunting_by_age.svg", AGE_ORDER)
    plot_group(summary, "sex", "Weighted stunting prevalence by sex",
               "stunting_by_sex.svg", ["male", "female"])
    plot_group(summary, "wealth", "Weighted stunting prevalence by household wealth",
               "stunting_by_wealth.svg", WEALTH_ORDER)
    plot_group(summary, "residence", "Weighted stunting prevalence by residence",
               "stunting_by_residence.svg", ["urban", "rural"])
    plot_group(summary, "region", "Weighted stunting prevalence by region",
               "stunting_by_region.svg", horizontal=True)
    plot_group(summary, "maternal_education",
               "Weighted stunting prevalence by maternal education",
               "stunting_by_maternal_education.svg", MAT_ED_ORDER)
    plot_group(summary, "water_source",
               "Weighted stunting prevalence by drinking-water source",
               "stunting_by_water_source.svg",
               ["Improved source", "Unimproved source"])
    plot_group(summary, "sanitation",
               "Weighted stunting prevalence by sanitation",
               "stunting_by_sanitation.svg",
               ["Improved facility", "Unimproved/no facility"])

    print(summary)
    print(sample)


if __name__ == "__main__":
    main()
