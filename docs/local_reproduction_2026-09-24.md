# Local reproducibility check — 24 September 2026

This note records an independent rerun of the public analysis scripts on a local Windows/Python 3.11 environment using the authorized 2022 Ghana DHS PR recode. It is a reproducibility check, not a replacement for the strengthened eight-chain results used in the manuscript.

## Data reconstruction

The rerun reproduced the analytic sample exactly:

- 4,928 children
- 927 stunted children
- 3,545 households
- 616 survey communities
- weighted denominator: 4,292.97481
- weighted stunting prevalence: 17.385%

## Main Bayesian reruns

All four principal saved posterior fits had zero divergences and acceptable sampler diagnostics.

| Model | Draws | Max R-hat | Min bulk ESS | Min tail ESS | Min BFMI | Max observed tree depth | Sampling status |
|---|---:|---:|---:|---:|---:|---:|---|
| Model 1 | 4,000 | 1.01 | 490 | 533 | 0.496 | 7 | PASS |
| Model 2 full | 4,000 | 1.00 | 659 | 1,042 | 0.515 | 6 | PASS |
| Model 2 harmonized | 4,000 | 1.01 | 591 | 549 | 0.509 | 6 | PASS |
| Model 3 | 4,000 | 1.00 | 464 | 518 | 0.482 | 6 | PASS |

No fit recorded a maximum-tree-depth hit.

## Observation-level PSIS-LOO reproducibility check

For the local four-chain rerun:

- Model 2 harmonized ELPD-LOO: -2014.845
- Model 3 ELPD-LOO: -2011.838
- Model 3 minus Model 2 difference: 3.008
- paired SE of the difference: 3.243
- Model 2: 4 observations with Pareto k > 0.70; none > 1
- Model 3: 5 observations with Pareto k > 0.70; none > 1

The ELPD difference is smaller than its SE, so this rerun supports the same substantive conclusion as the locked comparison: the harmonized WASH and maternal-education models are predictively similar at the observation level. The Pareto-k warnings concern PSIS approximation for a small number of observations; they are not sampler-convergence failures.

The manuscript continues to use the strengthened locked comparison stored in `results/tables/loo_model_compare_final.csv`, rather than replacing it with this four-chain reproducibility rerun.

## Age functional-form sensitivity

Replacing age categories with a cubic B-spline gave:

- male: OR 1.529 (1.272–1.849)
- richest vs poorest: OR 0.356 (0.199–0.616)
- rural vs urban: OR 0.844 (0.643–1.101)
- unimproved water: OR 1.494 (1.116–1.997)
- unimproved sanitation: OR 1.109 (0.852–1.451)
- higher maternal education: OR 0.365 (0.193–0.651)

Diagnostics: 0 divergences, max R-hat 1.01, minimum bulk ESS 476, minimum tail ESS 616.

These results confirm that the main fixed-effect conclusions are not artifacts of the categorical age specification.

## Detailed WASH sensitivity

The detailed WASH model gave:

- surface water vs improved: OR 1.525 (1.108–2.117)
- unprotected groundwater vs improved: OR 1.416 (0.890–2.246)
- open defecation vs improved sanitation: OR 1.226 (0.932–1.634)
- other unimproved vs improved sanitation: OR 0.932 (0.650–1.308)
- male: OR 1.508 (1.244–1.826)
- richest vs poorest: OR 0.365 (0.204–0.633)
- higher maternal education: OR 0.371 (0.197–0.664)

There were 0 divergences. The maximum R-hat was 1.02 for the household SD; fixed effects were at 1.00. Because this is a secondary sensitivity fit, the substantive conclusion is retained, while a stronger future rerun configuration is now encoded in `src/12_wash_coding_sensitivity.py`.

## Survey-weight pseudo-posterior

After strengthening the sampler settings, the weighted sensitivity completed with:

- 0 divergences
- max R-hat 1.01
- minimum bulk ESS 425
- minimum tail ESS 1,090

Key weighted estimates included:

- male: OR 1.540 (1.208–1.968)
- richest vs poorest: OR 0.309 (0.156–0.608)
- unimproved water: OR 1.394 (0.930–2.089)
- unimproved sanitation: OR 1.143 (0.807–1.625)
- higher maternal education: OR 0.304 (0.144–0.630)

The broad pattern was preserved, but the water interval became less precise and included 1.

## Prior sensitivity

Tighter and wider priors produced no divergences and acceptable diagnostics. The main associations for sex, wealth, water, sanitation, and higher maternal education were stable across prior scales.

## Independent GEE checks

The exchangeable working correlations were:

- household: 0.1539
- community: 0.0237

These are not Bayesian ICCs. They provide an independent check pointing in the same direction: residual dependence is substantially stronger within households than within survey communities.

GEE fixed-effect sensitivity was also consistent with the Bayesian results. For example:

- binary-WASH model, unimproved water: OR 1.397 (1.121–1.741)
- spline-age model, unimproved water: OR 1.393 (1.117–1.736)
- detailed-WASH model, surface water: OR 1.428 (1.115–1.827)
- detailed-WASH model, unprotected groundwater: OR 1.345 (0.931–1.943)

## Conclusion

The local rerun reproduces the analytic sample, confirms healthy sampling for the principal models, and reproduces the main scientific pattern across alternative priors, survey weighting, age specification, detailed WASH coding, and independent GEE checks.

The strengthened eight-chain summaries remain the locked manuscript results. This rerun is retained as evidence that those conclusions are reproducible in a separate local environment.
