"""One audited sample definition shared by descriptive and Bayesian analyses."""
from pathlib import Path
import hashlib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw/GHPR8CFL.DTA'
AGES = ['0-5', '6-11', '12-23', '24-35', '36-47', '48-59']
IMPROVED_WATER = {
    'piped into dwelling', 'piped to yard/plot', 'piped to neighbor',
    'public tap/standpipe', 'tube well or borehole', 'protected well',
    'protected spring', 'rainwater', 'tanker truck', 'cart with small tank',
    'bottled water', 'sachet water',
}
UNIMPROVED_WATER = {'unprotected well', 'unprotected spring',
    'river/dam/lake/ponds/stream/canal/irrigation channel', 'other'}
IMPROVED_SANITATION = {'flush to piped sewer system', 'flush to septic tank',
    'flush to pit latrine', 'flush, bio-digester (biofil)',
    'ventilated improved pit latrine (vip)', 'pit latrine with slab', 'composting toilet'}
UNIMPROVED_SANITATION = {'flush to somewhere else', "flush, don't know where",
    'pit latrine without slab/open pit', 'bucket toilet', 'hanging toilet/latrine',
    'no facility/bush/field', 'other'}


def classify(series, improved, unimproved):
    """Do not silently turn missing or unrecognized responses into unimproved."""
    s = series.astype('string')
    unknown = set(s.dropna().unique()) - improved - unimproved
    if unknown:
        raise ValueError(f'Unmapped {series.name} labels: {sorted(unknown)}')
    return s.map({**dict.fromkeys(improved, 0.0), **dict.fromkeys(unimproved, 1.0)})


def prepare_frame(full):
    full = full.copy()
    full['stratum'] = full.hv022.astype(str)
    full['psu'] = pd.to_numeric(full.hv021, errors='raise').astype('int64')
    frame = full[['stratum', 'psu']].drop_duplicates()
    if frame.psu.duplicated().any():
        raise ValueError('PSU assigned to multiple strata')
    age = pd.to_numeric(full.hc1, errors='coerce')
    haz = pd.to_numeric(full.hc70, errors='coerce')
    keep = full.hv103.astype(str).eq('yes') & age.between(0, 59) & haz.between(-600, 600)
    d = full.loc[keep].copy()
    d['hc1_num'] = age.loc[keep]
    d['hc70_num'] = haz.loc[keep]
    d['stunted'] = (d.hc70_num < -200).astype('int8')
    d['weight'] = pd.to_numeric(d.hv005, errors='raise') / 1e6
    if not np.isfinite(d.weight).all() or not d.weight.gt(0).all():
        raise ValueError('Weights must be finite and positive')
    for c in ['hv001', 'hv002', 'hvidx']:
        d[c] = pd.to_numeric(d[c], errors='raise').astype('int64')
    d['household_id'] = d.hv001.astype(str) + '_' + d.hv002.astype(str)
    d['child_id'] = d.household_id + '_' + d.hvidx.astype(str)
    if d.child_id.duplicated().any():
        raise ValueError('Duplicate child identifiers')
    d['age_group'] = pd.cut(d.hc1_num, [-.1, 5, 11, 23, 35, 47, 59], labels=AGES)
    d['maternal_education'] = d.hc61.astype('string')
    allowed = {'no education', 'primary', 'secondary', 'higher'}
    if not set(d.maternal_education.dropna()).issubset(allowed):
        raise ValueError('Unmapped maternal education category')
    d['water_unimproved'] = classify(d.hv201, IMPROVED_WATER, UNIMPROVED_WATER)
    d['sanitation_unimproved'] = classify(d.hv205, IMPROVED_SANITATION, UNIMPROVED_SANITATION)
    d['water_source_group'] = d.water_unimproved.map({0: 'Improved source', 1: 'Unimproved source'})
    d['sanitation_group'] = d.sanitation_unimproved.map({0: 'Improved facility', 1: 'Unimproved/no facility'})
    return d, frame


def load_data(path=RAW):
    return prepare_frame(pd.read_stata(path, convert_categoricals=True))


def design(d, wash=False, maternal=False, complete=False, missing_category=False):
    d = d.copy()
    if complete:
        d = d.loc[d.maternal_education.notna()].copy()
    if maternal and not missing_category and d.maternal_education.isna().any():
        raise ValueError('Maternal model requires complete sample or explicit missing category')
    fixed = pd.DataFrame(index=d.index)
    for c, positive, ref, name in [('hv104', 'male', 'female', 'male'), ('hv025', 'rural', 'urban', 'rural')]:
        if not d[c].astype(str).isin([positive, ref]).all():
            raise ValueError(f'Invalid or missing {c}')
        fixed[name] = d[c].astype(str).eq(positive).astype(float)
    parts = [fixed[['male']]]
    for c, prefix, ref in [('age_group','age','0-5'), ('hv270','wealth','poorest'), ('hv024','region','western')]:
        if d[c].isna().any():
            raise ValueError(f'Missing {c}')
        parts.append(pd.get_dummies(d[c].astype(str), prefix=prefix, dtype=float).drop(columns=[f'{prefix}_{ref}']))
    parts.append(fixed[['rural']])
    if wash:
        parts.append(d[['water_unimproved','sanitation_unimproved']].astype(float))
    if maternal:
        s = d.maternal_education.fillna('Missing')
        parts.append(pd.get_dummies(s, prefix='maternal_education', dtype=float).drop(columns=['maternal_education_no education']))
    X = pd.concat(parts, axis=1).astype(float)
    if not np.isfinite(X.to_numpy()).all():
        raise ValueError('Model covariates contain missing or nonfinite values')
    if np.linalg.matrix_rank(X.to_numpy()) != X.shape[1]:
        raise ValueError('Rank-deficient design matrix')
    return d, X


def sample_hash(d):
    # Only the digest is public; never publish child identifiers.
    return hashlib.sha256('\n'.join(d.child_id).encode()).hexdigest()
