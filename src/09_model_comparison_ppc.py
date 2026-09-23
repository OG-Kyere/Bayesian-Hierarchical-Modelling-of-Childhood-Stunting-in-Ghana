"""Conditional WAIC on identical observations; no new-community prediction claim."""
import argparse
import json
from pathlib import Path
import numpy as np
import arviz as az
import pandas as pd
from stunting_data import ROOT


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run-id',required=True)
    args=p.parse_args()
    base=ROOT/'results/runs'/args.run_id
    manifests=[json.loads((base/m/'manifest.json').read_text()) for m in ['m2_harmonized','m3']]
    if manifests[0]['sample_sha256']!=manifests[1]['sample_sha256']:
        raise ValueError('Models do not use identical ordered children')
    if not all(m.get('diagnostics',{}).get('diagnostic_gate_passed',False) for m in manifests):
        raise ValueError('Both models must pass the diagnostic gate before comparison')
    fits={m:az.from_netcdf(ROOT/'results/model_outputs'/args.run_id/m/'posterior.nc') for m in ['m2_harmonized','m3']}
    for fit in fits.values():
        if 'log_likelihood' not in fit.groups():raise ValueError('Missing log likelihood: rerun updated model script')
    if not np.array_equal(fits['m2_harmonized'].observed_data.stunted,fits['m3'].observed_data.stunted):
        raise ValueError('Observed outcomes differ')
    out=base/'comparison';out.mkdir(exist_ok=True)
    rows=[]
    for name,fit in fits.items():
        w=az.waic(fit,pointwise=True)
        ll=fit.log_likelihood.stunted
        rows.append(dict(model=name,elpd_waic=float(w.elpd_waic),se=float(w.se),p_waic=float(w.p_waic),
            warning=bool(w.warning),pointwise_variance_gt_04=int((ll.var(dim=('chain','draw'))>.4).sum())))
    pd.DataFrame(rows).to_csv(out/'conditional_waic.csv',index=False)
    az.compare(fits,ic='waic').to_csv(out/'conditional_comparison.csv')
    (out/'interpretation.txt').write_text('Conditional observation-level comparison only. Random effects are informed by fitted groups. '
        'WAIC warnings limit interpretation; do not infer equivalence or predictive performance in new households/communities. '
        'Use explicitly grouped validation if generalization becomes a study objective.\n')

if __name__=='__main__':main()
