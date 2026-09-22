# Data

The source data are the **2022 Ghana Demographic and Health Survey (GDHS)** recode files obtained through authorized access from The DHS Program.

## Local-only source files

Place authorized source files in:

```
data/raw/
```

The current workflow expects, as required:

- `GHPR8CFL.DTA` — Household Member Recode (PR)
- `GHHR8CFL.DTA` — Household Recode (HR)
- `GHKR8CFL.DTA` — Children's Recode (KR)

These files and their ZIP archives are excluded by `.gitignore`.

## Why the microdata are not on GitHub

DHS microdata are provided under data-use conditions and are not redistributed in this repository. The project therefore publishes:

1. code that reconstructs the analytic sample from authorized DHS files;
2. aggregate, non-identifying tables used in the thesis;
3. aggregate data behind every public figure; and
4. model summaries and diagnostics after validation.

No row-level DHS-derived dataset is committed.

## Reproducing the current descriptive analysis

After placing `GHPR8CFL.DTA` in `data/raw/`:

```bash
python src/02_descriptive_analysis.py
```

This regenerates the descriptive CSV files and SVG figures under `results/`.
