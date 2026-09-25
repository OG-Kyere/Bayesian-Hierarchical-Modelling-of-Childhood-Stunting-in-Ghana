# Current manuscript results snapshot

This snapshot records the locked numerical results used in the current journal manuscript. Later local reproducibility runs are documented separately and do not replace these values unless the manuscript result set is deliberately re-locked.

## Sample
- children: 4,928
- stunted: 927
- households: 3,545
- communities: 616
- weighted prevalence: 17.4% (95% design-based CI 15.8–18.9)

## Final strengthened Model 3
- posterior draws: 4,000 across 8 chains
- divergences: 0
- BFMI range: 0.51–0.66
- tree-depth saturation: none

### Fixed effects
- male vs female: OR 1.50 (1.24–1.82)
- age 24–35 vs 0–5 months: OR 2.91 (2.06–4.21)
- richest vs poorest: OR 0.36 (0.20–0.64)
- rural vs urban: OR 0.85 (0.64–1.12)
- unimproved water: OR 1.50 (1.15–1.99)
- unimproved/no sanitation: OR 1.12 (0.86–1.46)
- maternal primary vs none: OR 1.02 (0.75–1.41)
- maternal secondary vs none: OR 0.89 (0.68–1.14)
- maternal higher vs none: OR 0.37 (0.20–0.65)

### Hierarchical variation
- community SD: 0.389 (0.067–0.610)
- household SD: 1.234 (0.940–1.535)
- community ICC: 0.030 (0.001–0.073)
- household VPC: 0.307 (0.203–0.406)
- same-household latent correlation: 0.339 (0.236–0.436)
- community MOR: 1.45 (1.07–1.79)
- household MOR: 3.24 (2.45–4.32)

### Variance diagnostics
- community SD R-hat: 1.021; bulk ESS 544
- household SD R-hat: 1.018; bulk ESS 524

## Predictive comparison
- Model 3 ELPD-LOO: -2011.47
- Model 2 ELPD-LOO: -2012.39
- difference: +0.92 for Model 3
- SE difference: 3.38
- Model 3 Pareto k > 0.70: 0
- Model 2 Pareto k > 0.70: 5

## Robustness
- spline-age water OR: 1.49 (1.12–2.00)
- detailed-WASH surface-water OR: 1.52 (1.10–2.08)
- weighted pseudo-posterior water OR: 1.38 (0.90–2.07)
- full-sample missing-maternal sensitivity water OR: 1.35 (1.01–1.74)

Interpret all estimates as conditional associations, not causal effects.
