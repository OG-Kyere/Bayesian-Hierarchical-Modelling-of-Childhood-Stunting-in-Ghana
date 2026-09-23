# Validation results (in progress)

All runs retain the prespecified likelihood/prior for their model scenario. Failed fits are retained. No effect estimate is used to select a run. These aggregate diagnostics are not a substitute for scientific review.

| Run | Model | Maximum R-hat | Minimum bulk ESS | Minimum tail ESS | Gate |
|---|---|---:|---:|---:|---|
| validation-v2 | m0 | 1.004388 | 618 | 1469 | Pass |
| validation-v2 | m1 | 1.010088 | 707 | 698 | Fail |
| validation-v2 | m2_harmonized | 1.004569 | 590 | 492 | Pass |
| validation-v2 | m3 | 1.013457 | 432 | 540 | Fail |
| validation-v2 | weighted | 1.014850 | 445 | 571 | Fail |

The initial m3, weighted, and m1 fits require longer reruns. The first runtime session was lost before completion and is not part of this evidence table. Completed private checkpoints have been preserved separately from public aggregate results.
