"""Print the analysis environment for reproducibility records."""
from importlib.metadata import version, PackageNotFoundError
import platform

PACKAGES = [
    "pymc", "arviz", "numpy", "pandas", "pytensor",
    "statsmodels", "scipy", "patsy", "matplotlib", "pyreadstat",
]

print("python", platform.python_version())
for package in PACKAGES:
    try:
        print(package, version(package))
    except PackageNotFoundError:
        print(package, "NOT_INSTALLED")
