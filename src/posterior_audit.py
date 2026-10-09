"""Read-only, full-posterior diagnostic audit; never sample or export latent IDs."""
import argparse
import json
from pathlib import Path
import numpy as np


def diagnostics(idata, max_depth=None):
    import arviz as az
    posterior = idata.posterior.copy()
    # Audit actual intercepts and scientific contrasts even if not stored.
    for level in ('household', 'community'):
        tau, z, u = 'tau_' + level, 'z_' + level, 'u_' + level
        if tau in posterior and z in posterior and u not in posterior:
            posterior[u] = posterior[tau] * posterior[z]
    if 'tau_household' in posterior and 'tau_community' in posterior:
        posterior['sd_difference'] = posterior.tau_household - posterior.tau_community
    if 'tau_community' in posterior:
        tc = posterior.tau_community
        th = posterior.tau_household if 'tau_household' in posterior else 0.
        total = tc**2 + th**2 + np.pi**2 / 3
        posterior['icc_community'] = tc**2 / total
        posterior['mor_community'] = np.exp(np.sqrt(2) * .6744897501960817 * tc)
        if 'tau_household' in posterior:
            posterior['vpc_household'] = th**2 / total
            posterior['icc_same_household'] = (tc**2 + th**2) / total
            posterior['mor_household'] = np.exp(np.sqrt(2) * .6744897501960817 * th)
    diag = az.summary(posterior, kind='diagnostics', round_to='none')
    values = diag[['r_hat', 'ess_bulk', 'ess_tail']].to_numpy()
    finite = bool(values.size and np.isfinite(values).all())
    def number(value):
        return float(value) if np.isfinite(value) else None
    stats = getattr(idata, 'sample_stats', None)
    divergence = None
    bfmi = None
    hits = None
    if stats is not None:
        if 'diverging' in stats:
            a = np.asarray(stats.diverging)
            if np.isfinite(a).all() and np.isin(a, [0, 1]).all():
                divergence = int(a.sum())
        if 'energy' in stats:
            b = np.asarray(az.bfmi(idata))
            if np.isfinite(b).all():
                bfmi = float(b.min())
        for key in ('reached_max_treedepth', 'reached_max_tree_depth'):
            if key in stats:
                flag = np.asarray(stats[key])
                if np.isfinite(flag).all() and np.isin(flag, [0, 1]).all():
                    hits = int(flag.sum())
                break
        else:
            key = next((k for k in ('tree_depth', 'depth') if k in stats), None)
            if key and max_depth is not None:
                depth = np.asarray(stats[key])
                if np.isfinite(depth).all():
                    hits = int((depth >= max_depth).sum())
    metrics = dict(chains=int(posterior.sizes.get('chain', 0)),
        draws_per_chain=int(posterior.sizes.get('draw', 0)),
        parameters_checked=len(diag), nonfinite_parameter_diagnostics=int((~np.isfinite(values)).any(axis=1).sum()),
        divergences=divergence, max_rhat=number(diag.r_hat.max()),
        min_bulk_ess=number(diag.ess_bulk.min()), min_tail_ess=number(diag.ess_tail.min()),
        min_bfmi=bfmi, max_depth_hits=hits)
    complete = finite and all(metrics[k] is not None for k in ('divergences', 'min_bfmi', 'max_depth_hits'))
    passed = bool(complete and metrics['chains'] >= 4 and metrics['max_rhat'] < 1.01
        and metrics['min_bulk_ess'] >= 400 and metrics['min_tail_ess'] >= 400
        and divergence == 0 and bfmi >= .3 and hits == 0)
    metrics['diagnostic_gate_passed'] = passed
    metrics['status'] = 'PASS_PENDING_SCIENTIFIC_REVIEW' if passed else ('FAIL' if complete else 'INCOMPLETE')
    return diag, metrics


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input-dir', type=Path, default=Path('results/model_outputs'))
    p.add_argument('--max-treedepth', type=int, help='Use only a documented configured cap; never infer from observed depth')
    p.add_argument('--expected-files', type=int)
    args = p.parse_args(argv)
    if args.max_treedepth is not None and args.max_treedepth < 1:
        p.error('max-treedepth must be positive')
    import arviz as az
    paths = sorted(args.input_dir.rglob('*.nc'))
    rows = []
    for index, path in enumerate(paths, 1):
        try:
            idata = az.from_netcdf(path)
            try:
                _, metrics = diagnostics(idata, args.max_treedepth)
            finally:
                idata.close()
            rows.append(dict(file_index=index, **metrics))
        except Exception as exc:
            # Exception messages can contain private paths/coordinates.
            rows.append(dict(file_index=index, status='ERROR', error_type=type(exc).__name__))
    count_ok = args.expected_files is None or len(paths) == args.expected_files
    print(json.dumps(dict(files_found=len(paths), expected_count_matches=count_ok, audits=rows), indent=2, allow_nan=False))
    return 0 if paths and count_ok and all(r['status'] == 'PASS_PENDING_SCIENTIFIC_REVIEW' for r in rows) else 1


if __name__ == '__main__':
    raise SystemExit(main())
