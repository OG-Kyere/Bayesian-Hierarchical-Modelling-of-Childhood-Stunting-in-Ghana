# Running the project

This is the practical run order for a fresh clone.

## 1. Create a clean Python environment

Python 3.11 or 3.12 is the safest choice for the current project environment.

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `py -3.12` is not available, use an installed Python 3.11/3.12 executable.

Do not install from `requirements-pilot.txt` for the main analysis. That file is retained only as a historical record of the original pilot environment.

## 2. Add the DHS file locally

Put the authorized PR recode at:

```text
data/raw/GHPR8CFL.DTA
```

Raw DHS data are ignored by Git and must not be committed.

## 3. Run the cheap validation steps first

```powershell
python src/00_capture_environment.py
python src/01_data_preparation.py
python src/02_descriptive_analysis.py
```

`01_data_preparation.py` should reproduce:

- 4,928 children
- 927 stunted children
- 3,545 households
- 616 communities

If those counts do not match, stop before fitting Bayesian models.

## 4. Optional pilot

```powershell
python src/03_pilot_model.py
```

This is the older community-only baseline. It is useful for reproducibility but is not required for the final manuscript.

## 5. Main Bayesian models

Run these in order:

```powershell
python src/04_household_community_model.py
python src/05_wash_model.py
python src/06_maternal_education_model.py
```

These are computationally expensive. Each main production fit uses four chains with 1,000 warmup and 1,000 retained draws per chain.

They create local NetCDF posterior files under `results/model_outputs/`. Those files are intentionally ignored by Git because they can be large.

## 6. Main-model comparison and diagnostics

Only run these **after** Models 1–3 have finished:

```powershell
python src/09_model_comparison_ppc.py
python src/10_final_production_diagnostics.py
```

`09_model_comparison_ppc.py` specifically requires:

- `results/model_outputs/model2_wash_harmonized.nc`
- `results/model_outputs/model3_maternal_education.nc`

`10_final_production_diagnostics.py` uses the saved Model 1–3 NetCDF files. If they are absent, it can only report them as missing.

## 7. Sensitivity analyses

These can be run after the core sample has been validated. They are independent of the Model 1–3 NetCDF files but are computationally expensive:

```powershell
python src/07_survey_weight_sensitivity.py
python src/08_prior_sensitivity.py
python src/11_age_functional_form_sensitivity.py
python src/12_wash_coding_sensitivity.py
```

The prior-sensitivity script fits two full models, so it will usually take longer than a single model script.

## 8. GEE cross-checks

These require the raw PR file but are much cheaper than the Bayesian models:

```powershell
python src/diagnostics/gee_cluster_sensitivity.py
python src/diagnostics/gee_functional_form_wash_sensitivity.py
```

## 9. Public repository checks

These need no DHS data and no PyMC environment:

```powershell
python src/13_public_output_consistency.py
python src/14_repository_integrity.py
```

They are also run by GitHub Actions.

## If a model run stops

For PyMC/ArviZ import errors, first confirm that the virtual environment is active and reinstall from `requirements.txt`:

```powershell
python -m pip uninstall -y pymc arviz pytensor
pip install -r requirements.txt
```

Then confirm:

```powershell
python -c "import pymc, arviz; print('PyMC', pymc.__version__, 'ArviZ', arviz.__version__)"
```

The project intentionally pins ArviZ below 1.0 because the previously observed PyMC 5.27 / ArviZ 1.1 combination was incompatible in the analysis environment.

## What can run without the DHS file?

Only these:

- `src/00_capture_environment.py`
- `src/13_public_output_consistency.py`
- `src/14_repository_integrity.py`

Everything that analyses children or fits a model needs the authorized `GHPR8CFL.DTA` file locally.
