"""Read scientific-scale saved draws locally; export no latent identifiers."""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import arviz as az
import h5py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import rankdata

base = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--input-dir', type=Path, default=base / 'results/model_outputs')
args = parser.parse_args()
out = args.input_dir / 'scientific-diagnostic-review'
out.mkdir(parents=True, exist_ok=True)
local = args.input_dir
labels = {'model1_household_community': 'Model 1', 'model2_wash_full': 'Model 2 full',
          'model2_wash_harmonized': 'Model 2 harmonized', 'model3_age_spline_sensitivity': 'Spline age',
          'model3_detailed_wash_sensitivity': 'Detailed WASH', 'model3_maternal_education': 'Local Model 3',
          'model3_prior_tight': 'Tight prior', 'model3_prior_wide': 'Wide prior',
          'model3_weighted_sensitivity': 'Survey weighted'}
rows = []
paths = sorted(local.glob('*.nc'))
if not paths:
    parser.error('No saved NetCDF files found')
for index, path in enumerate(paths, 1):
    label = labels.get(path.stem, f'Fit {index}')
    with h5py.File(path, 'r') as f:
        th = np.asarray(f['posterior/tau_household'])
        tc = np.asarray(f['posterior/tau_community'])
    draws = dict(tau_household=th, tau_community=tc, sd_difference=th-tc)
    idata = az.from_dict(posterior=draws)
    summary = az.summary(idata, round_to='none')
    for name, stats in summary.iterrows():
        row = dict(model=label, quantity=name, **{k: float(stats[k]) for k in ('mean','sd','mcse_mean','mcse_sd','ess_bulk','ess_tail','r_hat')})
        row['mcse_mean_over_posterior_sd'] = row['mcse_mean'] / row['sd']
        rows.append(row)
    fig, axes = plt.subplots(3, 2, figsize=(12, 9), constrained_layout=True)
    colors = ['#2364aa', '#e07a26', '#33936d', '#af519d']
    for n, (name, a) in enumerate(draws.items()):
        ranks = rankdata(a.ravel()).reshape(a.shape)
        bins = np.linspace(1, a.size, 21)
        for chain in range(a.shape[0]):
            axes[n,0].plot(a[chain], color=colors[chain], alpha=.65, linewidth=.5, label=f'Chain {chain+1}')
            counts, edges = np.histogram(ranks[chain], bins=bins)
            axes[n,1].step((edges[:-1]+edges[1:])/2, counts, color=colors[chain], where='mid', linewidth=1)
        axes[n,0].set_ylabel(name.replace('_',' '))
        axes[n,0].set_xlabel('Retained iteration')
        axes[n,1].set_xlabel('Pooled rank')
        axes[n,1].set_ylabel('Count in rank bin')
        axes[n,1].axhline(a.shape[1]/20, color='#666666', linestyle=':', linewidth=.8)
    axes[0,0].legend(ncol=4, fontsize=8)
    fig.suptitle(label + ' | scientific-scale trace and rank review\nSeparate reproduction fit; locked manuscript estimates retained', fontsize=13)
    fig.savefig(out / f'fit-{index:02d}.png', dpi=140)
    plt.close(fig)
pd.DataFrame(rows).to_csv(out / 'scientific_mcse.csv', index=False)
print(f'Saved {len(paths)} scientific-scale trace/rank panels and {len(rows)} aggregate MCSE rows; no model sampling.')
