# Public-output consistency validation — 2026-10-17

The analyst executed `python src/13_public_output_consistency.py` locally on the audit branch and provided the terminal output:

```
Public-output consistency check passed.
- weighted prevalence: 17.39%
- male OR: 1.50 (1.24–1.82)
- water OR: 1.50 (1.15–1.99)
- household SD: 1.23
- community SD: 0.39
- LOO delta: 0.92 (SE 3.38)
- public summary CSVs: synchronized
- public Bayesian SVGs: synchronized
```

This is evidence that the **selected** checks implemented by `src/13_public_output_consistency.py` passed for the working tree tested by the analyst. It does not verify every model parameter, full posterior provenance, raw-data analyses, or external journal formatting. Keep archived eight-chain convergence caveats in the manuscript.

Related: `docs/audits/wash_category_audit_executed_2026-10-17.md`, `docs/audits/model3_four_vs_eight_chain_comparison_2026-10-17.md`. Six synthetic WASH unittest cases also passed in the analyst's terminal. No locked results, manuscript text, or private data were changed in this commit.
