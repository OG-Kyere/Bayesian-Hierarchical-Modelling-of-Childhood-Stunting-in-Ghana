# Data

This project uses the 2022 Ghana Demographic and Health Survey.

The core analysis is built from the Household Member Recode:

```text
data/raw/GHPR8CFL.DTA
```

That file contains the child anthropometry, household identifiers, WASH variables, and linked maternal-education information used in the current models.

The Household Recode (`GHHR8CFL.DTA`) and Children's Recode (`GHKR8CFL.DTA`) are not needed for the main analysis. They can be kept locally if a later extension requires variables that are not available in the PR file.

## Why the raw files are not here

DHS microdata are restricted and cannot be redistributed through this repository. Anyone reproducing the analysis must request the 2022 Ghana DHS directly from The DHS Program and follow its data-use conditions.

The repository therefore contains:

- the code used to build the analytic sample;
- aggregate descriptive tables;
- aggregate posterior summaries and diagnostics;
- figures used in the thesis and manuscript.

It does **not** contain row-level DHS data or row-level derived extracts.

The raw-data directory and common DHS file formats are excluded through `.gitignore`.

## Starting the analysis

After obtaining authorized access, place `GHPR8CFL.DTA` in `data/raw/`.

The descriptive analysis can then be reproduced with:

```bash
python src/02_descriptive_analysis.py
```

The model scripts use the same local file path. See the root README for the model sequence and the results files used in the manuscript.
