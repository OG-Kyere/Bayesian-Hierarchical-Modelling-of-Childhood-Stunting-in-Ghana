"""Scientific-parameter trace/rank plots; individual latent effects stay private."""
import argparse
import arviz as az
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from stunting_data import ROOT
plt.rcParams['svg.hashsalt']='ghana-stunting'


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run-id',required=True);p.add_argument('--model',required=True)
    a=p.parse_args()
    d=ROOT/'results/model_outputs'/a.run_id/a.model
    out=ROOT/'results/runs'/a.run_id/a.model
    fit=az.from_netcdf(d/'sampled.nc')
    variables=[v for v in ['alpha','tau_community','tau_household','sd_difference'] if v in fit.posterior]
    az.plot_trace(fit,var_names=variables,compact=True)
    plt.tight_layout();plt.savefig(out/'trace_scientific.svg',metadata={'Date':None});plt.close('all')
    az.plot_rank(fit,var_names=variables)
    plt.tight_layout();plt.savefig(out/'rank_scientific.svg',metadata={'Date':None});plt.close('all')

if __name__=='__main__':main()
