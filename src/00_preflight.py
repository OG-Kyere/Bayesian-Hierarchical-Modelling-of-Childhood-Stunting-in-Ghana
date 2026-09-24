"""Preflight check for running the childhood-stunting project locally.

Run:
    python src/00_preflight.py

The script does not read or expose DHS records. It only checks file presence,
required variables, installed package versions, and whether downstream model
outputs exist.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/GHPR8CFL.DTA"
OUT = ROOT / "results/model_outputs"

PACKAGES = [
    "pandas", "numpy", "pyreadstat", "pymc", "arviz", "pytensor",
    "matplotlib", "statsmodels", "scipy", "patsy",
]

MODEL_OUTPUTS = {
    "Model 1": OUT / "model1_household_community.nc",
    "Model 2 full": OUT / "model2_wash_full.nc",
    "Model 2 harmonized": OUT / "model2_wash_harmonized.nc",
    "Model 3": OUT / "model3_maternal_education.nc",
}


def main() -> int:
    problems = []

    print("Python package check")
    for package in PACKAGES:
        try:
            print(f"  {package:<12} {version(package)}")
        except PackageNotFoundError:
            problems.append(f"missing package: {package}")
            print(f"  {package:<12} MISSING")

    print("\nDHS input")
    if RAW.exists():
        print(f"  FOUND   {RAW.relative_to(ROOT)}")
    else:
        print(f"  MISSING {RAW.relative_to(ROOT)}")
        problems.append(
            "missing data/raw/GHPR8CFL.DTA — required for scripts 01–08, "
            "11–12, and diagnostics/GEE scripts"
        )

    print("\nSaved Bayesian model outputs")
    for label, path in MODEL_OUTPUTS.items():
        state = "FOUND" if path.exists() else "MISSING"
        print(f"  {state:<7} {label}: {path.relative_to(ROOT)}")

    print("\nWhat can run now")
    print("  Always: 00_capture_environment.py, 13_public_output_consistency.py,")
    print("          14_repository_integrity.py")
    if RAW.exists():
        print("  DHS-dependent: 01, 02, 03, 04, 05, 06, 07, 08, 11, 12, GEE checks")
    else:
        print("  DHS-dependent scripts: BLOCKED until GHPR8CFL.DTA is added locally")

    if MODEL_OUTPUTS["Model 2 harmonized"].exists() and MODEL_OUTPUTS["Model 3"].exists():
        print("  09_model_comparison_ppc.py: READY")
    else:
        print("  09_model_comparison_ppc.py: BLOCKED until harmonized Model 2 and Model 3 .nc files exist")

    if any(path.exists() for path in MODEL_OUTPUTS.values()):
        print("  10_final_production_diagnostics.py: PARTIALLY READY")
        print("      Missing models will be reported as FILE_MISSING.")
    else:
        print("  10_final_production_diagnostics.py: no local .nc files to diagnose")

    if problems:
        print("\nPreflight completed with setup issues:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print("\nPreflight passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
