# Bayesian model run log

This file records the posterior runs currently used for the thesis results. The current results are scientifically informative but are **not yet the final locked publication runs**. Longer production runs will replace or confirm these summaries before submission.

| Fit | Sample | Chains × retained draws | Divergences | Max key R-hat | Minimum basic ESS among key parameters | Status |
|---|---:|---:|---:|---:|---:|---|
| Model 0 pilot | 4,928 | 4 × 1,000 | 0 | ~1.008 | ~827 | Completed pilot |
| Model 1: household + community | 4,928 | 4 × 400 | 0 | 1.018 | 165 | Current inferential result; variance parameters slower mixing |
| Model 2: + WASH | 4,928 | 4 × 300 | 0 | 1.012 | 162 | Current inferential result |
| Model 2 harmonized | 4,503 | 4 × 300 | 0 | 1.036 | 172 | Same-sample comparison with Model 3; variance parameters slower mixing |
| Model 3: + maternal education | 4,503 | 4 × 300 | 0 | 1.033 | 120 | Current substantive model; fixed effects stable, variance parameters slower mixing |
| Tight-prior sensitivity | 4,503 | 4 × 250 | 0 | ~1.052 | ~204 for hierarchical SDs | Fixed-effect sensitivity only |
| Wide-prior sensitivity | 4,503 | 4 × 250 | 0 | ~1.028 | ~113 for community SD | Fixed-effect sensitivity only |
| Centered-intercept sensitivity | 4,503 | 4 × 220 | 0 | ~1.050 | ~144 for community SD | Fixed-effect sensitivity only |
| Survey-weight pseudo-posterior | 4,503 | sensitivity chains | 0 | community SD mixed poorly | — | Fixed effects reported; variance decomposition not used |
| Missing-maternal-category sensitivity | 4,928 | 4 × 250 (independent seeds 0,1,2,4) | 0 | 1.041 | 106 for community SD | Fixed-effect sensitivity only |

## Interpretation of diagnostic status

- Fixed-effect coefficients in the main models generally have R-hat values very close to 1.00 and substantially larger effective sample sizes than the hierarchical standard deviations.
- The household and community standard deviations mix more slowly because the model contains thousands of household random effects and many households contain only one eligible child.
- No divergent transitions were observed in the reported fits.
- The main substantive conclusions are therefore supported by multiple model and prior specifications, but final submission will use longer production runs in a stable PyMC environment to strengthen Monte Carlo precision for the variance components.

## Posterior predictive check

The current Model 3 posterior predictive diagnostic uses two independent NUTS runs (180 retained draws each) and manually generates replicated outcomes from the sampled fixed and random effects. Observed overall and age-specific prevalence values fall within the corresponding 95% posterior predictive intervals.

## Predictive comparison

Conditional WAIC was evaluated for harmonized Model 2 and Model 3 using the same 4,503 children. The WAIC values were approximately 3983.3 and 3982.7, respectively; the elpd difference was 0.30 with an approximate SE of 4.66. The models are therefore not meaningfully distinguishable on this predictive criterion, and pointwise log-likelihood variability indicates that fine WAIC distinctions should be treated cautiously.
