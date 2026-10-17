"""Read-only preflight for DHS WASH source/facility coding.

Usage (from repository root, authorised private workstation):
    python src/audit_wash_categories.py

Does not change the DHS data, fitted models, locked results, or manuscript.
Prints aggregate counts only; does not save child-level data.
Exit code 2 indicates missing or unrecognised labels requiring human review.
"""
from pathlib import Path
import sys
import pandas as pd

DATA = Path("data/raw/GHPR8CFL.DTA")

IMPROVED_WATER = {
    "piped into dwelling", "piped to yard/plot", "piped to neighbor",
    "public tap/standpipe", "tube well or borehole", "protected well",
    "protected spring", "rainwater", "tanker truck", "cart with small tank",
    "bottled water", "sachet water",
}
UNIMPROVED_WATER = {
    "unprotected well", "unprotected spring",
    "river/dam/lake/ponds/stream/canal/irrigation channel",
}
IMPROVED_SANITATION = {
    "flush to piped sewer system", "flush to septic tank",
    "flush to pit latrine", "flush, bio-digester (biofil)",
    "ventilated improved pit latrine (vip)", "pit latrine with slab",
    "composting toilet",
}
# Only this known 'no facility' code is provisionally classified here.
# All other sanitation labels require explicit review before a final whitelist.
UNIMPROVED_SANITATION = {"no facility/bush/field"}


def classify(series, improved, unimproved):
    counts = series.value_counts(dropna=False)
    observations = []
    unexpected = False
    for value, n in counts.items():
        if pd.isna(value):
            category = "MISSING"
            label = "<missing>"
            unexpected = True
        else:
            label = str(value)
            if label in improved:
                category = "improved"
            elif label in unimproved:
                category = "unimproved"
            else:
                category = "UNRECOGNISED—REVIEW"
                unexpected = True
        observations.append((label, int(n), category))
    return observations, unexpected


def main():
    if not DATA.exists():
        print(f"Private DHS input not found: {DATA}", file=sys.stderr)
        return 2
    df = pd.read_stata(DATA, convert_categoricals=True)
    required = ["hv103", "hc1", "hc70", "hc61", "hv201", "hv205"]
    absent = sorted(set(required) - set(df.columns))
    if absent:
        print(f"Missing required source fields: {absent}", file=sys.stderr)
        return 2
    age = pd.to_numeric(df["hc1"], errors="coerce")
    haz = pd.to_numeric(df["hc70"], errors="coerce")
    selection = df["hv103"].astype(str).eq("yes") & age.between(0, 59) & haz.between(-600, 600)
    base = df.loc[selection]
    samples = [("core", base), ("Model 3 complete case", base.loc[base["hc61"].notna()])]
    review = False
    for name, subset in samples:
        print(f"\n=== {name}: N={len(subset)} ===")
        for field, improved, unimproved in [
            ("hv201 water", IMPROVED_WATER, UNIMPROVED_WATER),
            ("hv205 sanitation", IMPROVED_SANITATION, UNIMPROVED_SANITATION),
        ]:
            col = field.split()[0]
            rows, problem = classify(subset[col], improved, unimproved)
            review |= problem
            print(f"\n{field}: label | N | provisional classification")
            for label, count, classification in rows:
                print(f"{label} | {count} | {classification}")
    if review:
        print("\nREVIEW REQUIRED: no models should be refit until category labels are reconciled.")
        return 2
    print("\nNo missing/unrecognised source/facility labels under provisional lists.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
