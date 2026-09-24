"""Validate and reconstruct the core 2022 Ghana DHS analytic sample.

This script performs the first reproducibility check in the project. It does
not write row-level DHS-derived data to disk. Raw DHS data remain local.

Expected input
--------------
data/raw/GHPR8CFL.DTA

Public output
-------------
results/tables/data_preparation_check.csv
"""

from pathlib import Path
import sys
import pandas as pd

RAW = Path("data/raw/GHPR8CFL.DTA")
TABLES = Path("results/tables")
TABLES.mkdir(parents=True, exist_ok=True)

REQUIRED = {
    "hv001", "hv002", "hv005", "hv021", "hv022", "hv024", "hv025",
    "hv103", "hv104", "hv201", "hv205", "hv270",
    "hc1", "hc61", "hc68", "hc70",
}


def main() -> int:
    if not RAW.exists():
        print(
            f"Missing DHS file: {RAW}\n"
            "Request the 2022 Ghana DHS from The DHS Program and place "
            "GHPR8CFL.DTA under data/raw/."
        )
        return 2

    df = pd.read_stata(RAW, convert_categoricals=True)

    missing = sorted(REQUIRED.difference(df.columns))
    if missing:
        print("The PR file is missing required variables:")
        for name in missing:
            print(f"- {name}")
        return 3

    age = pd.to_numeric(df["hc1"], errors="coerce")
    haz = pd.to_numeric(df["hc70"], errors="coerce")

    keep = (
        df["hv103"].astype(str).eq("yes")
        & age.between(0, 59)
        & haz.between(-600, 600)
    )
    d = df.loc[keep].copy()
    d["stunted"] = (haz.loc[keep] < -200).astype(int)
    d["weight"] = pd.to_numeric(d["hv005"], errors="coerce") / 1_000_000
    d["household_id"] = (
        pd.to_numeric(d["hv001"], errors="coerce").astype(int).astype(str)
        + "_"
        + pd.to_numeric(d["hv002"], errors="coerce").astype(int).astype(str)
    )

    weighted_prev = float(
        (d["stunted"] * d["weight"]).sum() / d["weight"].sum()
    )

    out = pd.DataFrame(
        {
            "metric": [
                "children",
                "stunted_children",
                "households",
                "communities",
                "weighted_denominator",
                "weighted_stunting_prevalence",
                "missing_maternal_education",
            ],
            "value": [
                len(d),
                int(d["stunted"].sum()),
                d["household_id"].nunique(),
                d["hv001"].nunique(),
                float(d["weight"].sum()),
                weighted_prev,
                int(d["hc61"].isna().sum()),
            ],
        }
    )
    out.to_csv(TABLES / "data_preparation_check.csv", index=False)

    print(out.to_string(index=False))

    expected = {
        "children": 4928,
        "stunted": 927,
        "households": 3545,
        "communities": 616,
    }
    observed = {
        "children": len(d),
        "stunted": int(d["stunted"].sum()),
        "households": d["household_id"].nunique(),
        "communities": d["hv001"].nunique(),
    }

    mismatches = [
        f"{key}: expected {expected[key]}, got {observed[key]}"
        for key in expected
        if observed[key] != expected[key]
    ]
    if mismatches:
        print("\nWARNING: reconstructed sample differs from the validated sample:")
        for item in mismatches:
            print(f"- {item}")
        return 1

    print("\nCore analytic sample matches the validated project counts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
