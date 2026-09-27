# Independent GEE robustness diagnostics

These files are **not the primary thesis inference**. They are independent clustering and fixed-effect robustness diagnostics fitted with logistic generalized estimating equations (GEE). They were first produced while the primary PyMC/NUTS workflow was being troubleshot and are retained as an external check on the completed Bayesian analysis.

The exchangeable working correlations were:

- household: 0.154
- community: 0.024

These quantities are not interchangeable with Bayesian random-effect variances, ICCs, VPCs, or MORs. They are retained because they provide an independent check that within-household dependence is materially stronger than within-community dependence in the current analytic sample.

The fixed-effect directions are also broadly consistent with the completed Bayesian household/community models. The GEE results do not replace the Bayesian models; they provide an independent robustness check.
