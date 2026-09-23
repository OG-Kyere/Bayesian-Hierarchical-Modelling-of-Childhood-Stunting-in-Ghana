"""Generate aggregate figures and a status table from exact run outputs."""
import argparse
import json
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from stunting_data import ROOT
plt.rcParams['svg.hashsalt']='ghana-stunting'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run-id',required=True);a=p.parse_args()
    base=ROOT/'results/runs'/a.run_id
    out=base/'summary';out.mkdir(exist_ok=True)
    rows=[]
    for f in sorted(base.glob('*/manifest.json')):
        m=json.loads(f.read_text());diag=m.get('diagnostics',{})
        rows.append(dict(model=m['model'],status=m['status'],n=m['n'],**diag))
        if not diag.get('diagnostic_gate_passed',False):continue
        effects=pd.read_csv(f.parent/'odds_ratios.csv')
        effects=effects.loc[~effects.term.str.startswith('region_')].copy()
        fig,ax=plt.subplots(figsize=(8,7))
        y=range(len(effects))
        ax.errorbar(effects.or_median,y,xerr=[effects.or_median-effects.or_lower,effects.or_upper-effects.or_median],fmt='o',capsize=3)
        ax.set_yticks(list(y),effects.term);ax.axvline(1,color='gray',linestyle='--');ax.set_xscale('log')
        ax.set_xlabel('Posterior median odds ratio and equal-tail 95% interval')
        ax.set_title(m['model']+' — diagnostic gate passed; scientific review pending')
        fig.tight_layout();fig.savefig(f.parent/'odds_ratios.svg',metadata={'Date':None});plt.close(fig)
        ppc=pd.read_csv(f.parent/'ppc_prevalence.csv');ppc=ppc.loc[ppc.variable.eq('age')].set_index('category').reindex(['0-5','6-11','12-23','24-35','36-47','48-59'])
        fig,ax=plt.subplots(figsize=(7,4))
        y=ppc.replicated_median
        ax.errorbar(ppc.index,y,yerr=[y-ppc.replicated_lower,ppc.replicated_upper-y],fmt='o',label='Replicated 95% interval')
        ax.scatter(ppc.index,ppc.observed,marker='x',label='Observed');ax.set_ylabel('Unweighted sample prevalence');ax.set_xlabel('Age (months)');ax.legend()
        fig.tight_layout();fig.savefig(f.parent/'ppc_age.svg',metadata={'Date':None});plt.close(fig)
    if not rows:raise ValueError('No run manifests found')
    pd.DataFrame(rows).to_csv(out/'validation_status.csv',index=False)
    print(pd.DataFrame(rows).to_string(index=False))

if __name__=='__main__':main()
