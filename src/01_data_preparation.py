"""Audit the authorized input without exporting child-level data."""
import json
from stunting_data import load_data, sample_hash

if __name__ == '__main__':
    d, frame = load_data()
    print(json.dumps(dict(n=len(d), stunted=int(d.stunted.sum()),
        households=d.household_id.nunique(), communities=d.hv001.nunique(),
        survey_psus=len(frame), strata=frame.stratum.nunique(),
        maternal_missing=int(d.maternal_education.isna().sum()),
        sample_sha256=sample_hash(d)), indent=2))
