"""Reproducible, checkpointed Bayesian fits. All row-level outputs stay private.

Example: python src/bayesian_workflow.py --model m3 --run-id production-v1
A diagnostic pass is necessary, not sufficient, for scientific validation.
"""
import argparse
import hashlib
import importlib.metadata
import json
import platform
import subprocess
from pathlib import Path
import numpy as np
import pandas as pd
from stunting_data import ROOT, RAW, load_data, design, sample_hash

SPECS = {
    'm0': dict(household=False),
    'm1': dict(household=True),
    'm2': dict(household=True, wash=True),
    'm2_harmonized': dict(household=True, wash=True, complete=True),
    'm3': dict(household=True, wash=True, complete=True, maternal=True),
    'weighted': dict(household=True, wash=True, complete=True, maternal=True, weighted=True),
    'tight': dict(household=True, wash=True, complete=True, maternal=True, beta_sd=.5, tau_sd=.5),
    'wide': dict(household=True, wash=True, complete=True, maternal=True, beta_sd=1.5, tau_sd=1.5),
    # External sensitivity scenario, not a prior estimated from this sample.
    'intercept': dict(household=True, wash=True, complete=True, maternal=True, alpha_mu=-1.5),
    'missing': dict(household=True, wash=True, maternal=True, missing_category=True),
}


def build_model(d, X, spec):
    import pymc as pm
    ci, communities = pd.factorize(d.hv001, sort=True)
    hi, households = pd.factorize(d.household_id, sort=True)
    coords = dict(obs=np.arange(len(d)), coef=X.columns.tolist(), community=np.arange(len(communities)))
    if spec.get('household'):
        coords['household'] = np.arange(len(households))
    with pm.Model(coords=coords) as model:
        alpha = pm.Normal('alpha', spec.get('alpha_mu', 0.), 1.5)
        beta = pm.Normal('beta', 0., spec.get('beta_sd', 1.), dims='coef')
        tc = pm.HalfNormal('tau_community', spec.get('tau_sd', 1.))
        zc = pm.Normal('z_community', 0., 1., dims='community')
        eta = alpha + pm.math.dot(X.to_numpy(), beta) + tc * zc[ci]
        th = 0.
        if spec.get('household'):
            th = pm.HalfNormal('tau_household', spec.get('tau_sd', 1.))
            zh = pm.Normal('z_household', 0., 1., dims='household')
            eta = eta + th * zh[hi]
        total = tc**2 + th**2 + np.pi**2 / 3
        pm.Deterministic('icc_community', tc**2 / total)
        pm.Deterministic('mor_community', pm.math.exp(np.sqrt(2) * .6744897501960817 * tc))
        if spec.get('household'):
            pm.Deterministic('vpc_household', th**2 / total)
            pm.Deterministic('icc_same_household', (tc**2 + th**2) / total)
            pm.Deterministic('mor_household', pm.math.exp(np.sqrt(2) * .6744897501960817 * th))
            pm.Deterministic('sd_difference', th - tc)
        y = d.stunted.to_numpy()
        if spec.get('weighted'):
            w = d.weight.to_numpy() / d.weight.mean()
            # Ordinary Bernoulli + correction equals sum(w * log p(y|theta)).
            pm.Bernoulli('stunted', logit_p=eta, observed=y, dims='obs')
            logp = pm.logp(pm.Bernoulli.dist(logit_p=eta), y)
            pm.Potential('weight_adjustment', pm.math.sum((w - 1.) * logp))
        else:
            pm.Bernoulli('stunted', logit_p=eta, observed=y, dims='obs')
    return model


def netcdf_safe(idata):
    # nutpie metadata can contain nested dictionaries; preserve them as JSON.
    for obj in [idata, *[getattr(idata, group) for group in idata.groups()]]:
        for key, value in list(obj.attrs.items()):
            if isinstance(value, dict):
                obj.attrs[key] = json.dumps(value)
    return idata


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, allow_nan=False) + '\n')


def diagnostics(idata, max_depth):
    import arviz as az
    # Include latent effects, not only selected scientific coefficients.
    diag = az.summary(idata, kind='diagnostics', round_to='none')
    bfmi = np.asarray(az.bfmi(idata))
    stats = idata.sample_stats
    depth_name = next((x for x in ['tree_depth', 'depth'] if x in stats), None)
    hits = int((stats[depth_name] >= max_depth).sum()) if depth_name else None
    metrics = dict(chains=int(idata.posterior.sizes['chain']), draws_per_chain=int(idata.posterior.sizes['draw']),
        divergences=int(stats.diverging.sum()), max_rhat=float(diag.r_hat.max()),
        min_bulk_ess=float(diag.ess_bulk.min()), min_tail_ess=float(diag.ess_tail.min()),
        min_bfmi=float(bfmi.min()), max_depth_hits=hits)
    finite = np.isfinite(diag[['r_hat','ess_bulk','ess_tail']].to_numpy()).all()
    passed = bool(finite and metrics['chains'] >= 4 and metrics['max_rhat'] < 1.01
        and metrics['min_bulk_ess'] >= 400 and metrics['min_tail_ess'] >= 400
        and metrics['divergences'] == 0 and metrics['min_bfmi'] >= .3 and hits == 0)
    metrics['diagnostic_gate_passed'] = passed
    return diag, metrics


def posterior_tables(idata, out, spec):
    import arviz as az
    names = [x for x in idata.posterior if not x.startswith('z_')]
    az.summary(idata, var_names=names, hdi_prob=.95).to_csv(out / 'posterior_summary.csv')
    beta = idata.posterior.beta.stack(sample=('chain','draw')).transpose('coef','sample')
    rows = []
    for term, values in zip(beta.coef.values, np.asarray(beta)):
        q = np.exp(np.quantile(values,[.025,.5,.975]))
        rows.append(dict(term=str(term),or_median=q[1],or_lower=q[0],or_upper=q[2],
            probability_or_gt_1=float((values>0).mean())))
    pd.DataFrame(rows).to_csv(out/'odds_ratios.csv',index=False)
    if spec.get('household'):
        delta=np.asarray(idata.posterior.sd_difference).ravel()
        write_json(out/'household_community_contrast.json',dict(
            probability_household_sd_gt_community_sd=float((delta>0).mean()),
            sd_difference_equal_tail_95=np.quantile(delta,[.025,.5,.975]).tolist()))


def aggregate_ppc(idata, d, out):
    """Observed and replicated aggregate discrepancies; never export group IDs."""
    yrep=np.asarray(idata.posterior_predictive.stunted).reshape(-1,len(d))
    rows=[]
    groups={'overall':pd.Series('All',index=d.index),'age':d.age_group.astype(str),
        'sex':d.hv104.astype(str),'wealth':d.hv270.astype(str)}
    for variable, categories in groups.items():
        for category in sorted(categories.unique()):
            mask=np.asarray(categories.eq(category))
            values=yrep[:,mask].mean(axis=1)
            q=np.quantile(values,[.025,.5,.975])
            rows.append(dict(variable=variable,category=category,n=int(mask.sum()),
                observed=float(d.stunted.to_numpy()[mask].mean()),replicated_lower=q[0],
                replicated_median=q[1],replicated_upper=q[2]))
    pd.DataFrame(rows).to_csv(out/'ppc_prevalence.csv',index=False)
    counts=[]
    y=d.stunted.to_numpy()
    for level in ['household_id','hv001']:
        codes, levels=pd.factorize(d[level],sort=True)
        sizes=np.bincount(codes)
        observed=np.bincount(codes,weights=y)
        rep=np.vstack([np.bincount(codes,weights=r,minlength=len(levels)) for r in yrep])
        for label, mask in [('all',np.ones(len(sizes),bool)),('multiple_children',sizes>1)]:
            for name, obs, vals in [
                ('zero_stunted_fraction',float((observed[mask]==0).mean()),(rep[:,mask]==0).mean(axis=1)),
                ('all_stunted_fraction',float((observed[mask]==sizes[mask]).mean()),(rep[:,mask]==sizes[mask]).mean(axis=1)),
                ('variance_group_prevalence',float(np.var(observed[mask]/sizes[mask])),np.var(rep[:,mask]/sizes[mask],axis=1))]:
                q=np.quantile(vals,[.025,.5,.975])
                counts.append(dict(level=level,groups=label,discrepancy=name,observed=obs,
                    replicated_lower=q[0],replicated_median=q[1],replicated_upper=q[2]))
    pd.DataFrame(counts).to_csv(out/'ppc_group_discrepancies.csv',index=False)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model',choices=SPECS,required=True)
    p.add_argument('--raw',type=Path,default=RAW)
    p.add_argument('--run-id',required=True)
    p.add_argument('--draws',type=int,default=2000)
    p.add_argument('--tune',type=int,default=2000)
    p.add_argument('--chains',type=int,default=4)
    p.add_argument('--seed',type=int,default=20260923)
    p.add_argument('--target-accept',type=float,default=.97)
    p.add_argument('--max-treedepth',type=int,default=12)
    p.add_argument('--sampler',choices=['pymc','nutpie'],default='pymc')
    p.add_argument('--prior-only',action='store_true')
    args=p.parse_args(argv)
    if not args.run_id.replace('-','').replace('_','').isalnum():
        p.error('run-id must contain only letters, numbers, hyphens, underscores')
    import pymc as pm
    import arviz as az
    spec=SPECS[args.model]
    d,_=load_data(args.raw)
    d,X=design(d,**{k:v for k,v in spec.items() if k in ['wash','maternal','complete','missing_category']})
    private=ROOT/'results/model_outputs'/args.run_id/args.model
    out=ROOT/'results/runs'/args.run_id/args.model
    if (out/'manifest.json').exists() or private.exists():
        raise FileExistsError('Run exists: use a new run-id to preserve provenance')
    private.mkdir(parents=True);out.mkdir(parents=True)
    packages={x:importlib.metadata.version(x) for x in ['pymc','arviz','numpy','pandas','pytensor']}
    if args.sampler=='nutpie':packages['nutpie']=importlib.metadata.version('nutpie')
    manifest=dict(model=args.model,specification=spec,settings={k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items() if k!='raw'},
        git_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        source_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [Path(__file__),ROOT/'src/stunting_data.py']},
        raw_sha256=hashlib.sha256(args.raw.read_bytes()).hexdigest(),sample_sha256=sample_hash(d),
        n=len(d),households=d.household_id.nunique(),communities=d.hv001.nunique(),
        columns=X.columns.tolist(),python=platform.python_version(),packages=packages,status='started')
    write_json(out/'manifest.json',manifest)
    model=build_model(d,X,spec)
    with model:
        prior=pm.sample_prior_predictive(draws=1000,random_seed=args.seed)
        prev=np.asarray(prior.prior_predictive.stunted).reshape(-1,len(d)).mean(axis=1)
        write_json(out/'prior_predictive.json',dict(prevalence_quantiles=np.quantile(prev,[.025,.5,.975]).tolist(),
            probability_prevalence_gt_080=float((prev>.8).mean()),note='Unweighted sample prevalence; plausibility requires scientific review.'))
        if args.prior_only:
            manifest['status']='prior_only';write_json(out/'manifest.json',manifest);return
        chains=[]
        for chain in range(args.chains):
            kwargs=dict(draws=args.draws,tune=args.tune,chains=1,cores=1,
                random_seed=args.seed+chain,target_accept=args.target_accept,
                idata_kwargs={'log_likelihood':not spec.get('weighted',False)},
                return_inferencedata=True,nuts_sampler=args.sampler)
            if args.sampler=='pymc':kwargs['nuts']={'max_treedepth':args.max_treedepth}
            else:kwargs['nuts_sampler_kwargs']={'maxdepth':args.max_treedepth}
            fitted=pm.sample(**kwargs)
            fitted=fitted.assign_coords(chain=[chain])
            netcdf_safe(fitted).to_netcdf(private/f'chain_{chain}.nc')
            chains.append(fitted)
        idata=az.concat(*chains,dim='chain')
        if not spec.get('weighted') and 'log_likelihood' not in idata.groups():
            pm.compute_log_likelihood(idata, extend_inferencedata=True)
        diag,metrics=diagnostics(idata,args.max_treedepth)
        # Individual latent diagnostics are private; only aggregate metrics are public.
        diag.to_csv(private/'all_parameter_diagnostics.csv')
        scientific=diag.loc[~diag.index.str.startswith('z_')]
        scientific.to_csv(out/'scientific_parameter_diagnostics.csv')
        posterior_tables(idata,out,spec)
        pm.sample_posterior_predictive(idata,random_seed=args.seed+10000,extend_inferencedata=True,var_names=['stunted'])
        aggregate_ppc(idata,d,out)
        netcdf_safe(idata).to_netcdf(private/'posterior.nc')
    manifest.update(diagnostics=metrics,status='diagnostics_passed_pending_scientific_review' if metrics['diagnostic_gate_passed'] else 'provisional_diagnostics_failed')
    write_json(out/'manifest.json',manifest)
    print(json.dumps(metrics,indent=2))

if __name__=='__main__':main()
