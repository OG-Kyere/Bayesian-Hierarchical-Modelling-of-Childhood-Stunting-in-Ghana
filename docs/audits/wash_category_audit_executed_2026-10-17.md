# Actual-data WASH classification audit — 2026-10-17

Evidence: analyst-provided console output from running `python src/audit_wash_categories.py` against their **authorised local** GHPR8CFL.DTA. No individual-level records were transferred or committed.

Result: `No missing/unrecognised source/facility labels under provisional lists.`

Analytic sample: core N=4928; Model 3 complete-maternal-education N=4503. For all labels reported in the console output the explicit water/sanitation sets now recognise the labels. 15 water labels have positive observations in each sample. Sanitation includes categorical unused levels with zero counts, which are not observed children.

Full-sample sanitation: `other` n=6, `pit latrine without slab/open pit` n=686, `hanging toilet/latrine` n=7, `flush to somewhere else` n=3. All are classified unimproved in the updated validation script. `flush, don't know where` and `bucket toilet` have zero observed counts. Model 3: other n=6, pit without slab/open pit n=613, hanging n=7, flush somewhere else n=3. No missing categories were reported.

This audit checks **category coverage of observed labelled codes** and alignment of the explicit categories in `src/audit_wash_categories.py`; it does not independently rederive the fitted-model input matrix or assess WASH causal effects, sanitation service ladders, survey selection, or cross-file correspondence. Original model treated non-improved categories as unimproved, so current observed classification is compatible with the original binarisation.

Next: verify `python -m unittest discover -s tests -p "test_audit_wash_categories.py" -v` completes; review exact WASH indicator methods wording in manuscript (source/facility types, not basic/safely managed service); finish eight-chain convergence caveat and confirm full manuscript numerical alignment. Keep locked results unchanged.