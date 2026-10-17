# Four-chain versus locked eight-chain replication comparison
Date: 2026-10-17
Status: descriptive comparison, not independent full statistical certification.

## Provenance
Four-chain posterior summaries were calculated by the analyst locally from `results/model_outputs/model3_maternal_education.nc` (4 chains, 1000 retained draws each) using ArviZ and NumPy. Values below are copied from the analyst's terminal output. The locked eight-chain values are from public `results/tables/model3_final_8chain_key_or.csv` and `results/tables/model3_final_8chain_variance_summary.csv`. No private NetCDF, raw DHS data, or individual random effects are committed here.

All intervals compared below are equal-tailed 95% posterior quantile intervals, NOT 94% HDIs.

| Quantity | Four-chain median [2.5%, 97.5%] | Locked eight-chain median [2.5%, 97.5%] |
|---|---|---|
| tau_community | 0.385256 [0.065381, 0.617527] | 0.388710 [0.066908, 0.609775] |
| tau_household | 1.240495 [0.938121, 1.558379] | 1.233550 [0.940484, 1.534729] |
| Male OR | 1.504340 [1.245334, 1.838402] | 1.504747 [1.244183, 1.820032] |
| Age 24–35 OR | 2.931714 [2.068514, 4.218325] | 2.914502 [2.056, 4.210] |
| Richest wealth OR | 0.361103 [0.206878, 0.619730] | 0.360608 [0.197, 0.639] |
| Unimproved water OR | 1.493522 [1.123926, 1.978505] | 1.498235 [1.148265, 1.987154] |
| Unimproved sanitation OR | 1.111305 [0.871366, 1.451571] | 1.118779 [0.856000, 1.457976] |
| Higher maternal education OR | 0.369271 [0.197481, 0.661644] | 0.366645 [0.197109, 0.648422] |
| Rural OR | 0.846257 [0.643614, 1.099626] | approximately 0.845 [0.636, 1.116] |

## Full posterior element convergence check on available four-chain files
Reported by the analyst after running `python src/audit_all_posterior_effects.py`:
- Models 1, 2 full, 2 harmonized and 3: 4 chains x 1000 draws; 0 divergences; minimum BFMI 0.49585, 0.51510, 0.50875, 0.48188, respectively.
- Every reported parameter family, including all available z_community, z_household, u_community, u_household effects, had 0 flagged elements using the script's threshold R-hat >1.01, bulk/tail ESS <400, or missing diagnostics. Printed R-hat values round to two/three decimal places; the code's actual threshold comparison controls flags.
- Model 3 has 616 community effects and 3283 household effects in the four-chain file; there are 31 coefficients.
- These four-chain files are not the archived eight-chain locked draws. The locked eight-chain tau R-hat values (~1.021 community and ~1.018 household) must remain disclosed and are **not** superseded.

## Real-data WASH category audit
Analyst ran `python src/audit_wash_categories.py`; printed sample sizes core 4928 and Model 3 complete case 4503, matching archived records.
- All 15 observed hv201 labels were recognised by the provisional validator.
- Sanitation hv205 contained 686 children labelled 'pit latrine without slab/open pit', 7 'hanging toilet/latrine', 3 'flush to somewhere else', and 6 'other' (full sample); these were initially flagged because they were absent from the explicit sanitation whitelist.
- A subsequent validation-script edit categorises the first three types as unimproved (and 'bucket toilet', zero observed). The six 'other' observations remain deliberately unresolved. Zero-count unused categorical levels can still appear in pandas value_counts; avoid treating them as observed children.
- Because the production model coded all non-improved labels as unimproved, this initial warning does not demonstrate a changed research result. It also does **not** establish that treating 'other' as unimproved is valid. Review DHS variable documentation/underlying categorisation before modifying model coding.

## Interpretation and decision
- Agreement of fixed-effect summaries and the two tau summaries across 4-chain and locked 8-chain draws is encouraging; retain original locked numbers pending formal provenance and convergence reconciliation.
- This is NOT a proof that every fixed effect or variance component has been independently verified against DHS microdata, or that sampling-design limitations and model fit concerns are resolved.
- Do not silently switch posterior runs, overwrite archived outputs or update manuscript values.
- Next: resolve the 6 ambiguous sanitation 'other' observations (non-disclosive aggregate treatment), inspect provenance of the 8-chain run and consider strengthened runs only if necessary; preserve eight-chain convergence caveat.
