"""
Data preparation for the 2022 Ghana DHS childhood stunting analysis.

Raw DHS files must be stored locally under data/raw/ and are intentionally
excluded from version control.
"""
from pathlib import Path

RAW_DIR = Path("data/raw")
DERIVED_DIR = Path("data/derived")
DERIVED_DIR.mkdir(parents=True, exist_ok=True)

def main():
    raise NotImplementedError(
        "Wire this script to the authorized Ghana DHS recode files before running."
    )

if __name__ == "__main__":
    main()
