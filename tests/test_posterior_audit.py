"""Synthetic saved draws test joint-posterior gates without fitting a model."""
import sys
import unittest
import contextlib
import hashlib
import io
import json
import tempfile
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import arviz as az
from posterior_audit import diagnostics, main


def draws():
    rng = np.random.default_rng(42)
    shape = (4, 1000)
    return az.from_dict(posterior={
        'alpha': rng.normal(size=shape),
        'tau_household': np.abs(rng.normal(size=shape)),
        'tau_community': np.abs(rng.normal(size=shape)),
        'z_household': rng.normal(size=shape + (2,)),
        'z_community': rng.normal(size=shape + (2,))},
        sample_stats={'diverging': np.zeros(shape, dtype=bool),
            'energy': rng.normal(size=shape), 'tree_depth': np.full(shape, 6),
            'reached_max_treedepth': np.zeros(shape, dtype=bool)})


class PosteriorGate(unittest.TestCase):
    def test_includes_latents_scaled_effects_and_contrast(self):
        diag, metrics = diagnostics(draws())
        for prefix in ('z_household[', 'z_community[', 'u_household[', 'u_community['):
            self.assertTrue(any(str(i).startswith(prefix) for i in diag.index))
        self.assertIn('sd_difference', diag.index)
        self.assertTrue(metrics['diagnostic_gate_passed'])

    def test_bad_household_latent_blocks_good_scalar_parameters(self):
        data = draws()
        data.posterior.z_household.values[0, :, 0] += 5
        _, metrics = diagnostics(data)
        self.assertFalse(metrics['diagnostic_gate_passed'])
        self.assertEqual(metrics['status'], 'FAIL')

    def test_missing_sampler_evidence_is_incomplete(self):
        for key in ('energy', 'diverging'):
            data = draws()
            data.sample_stats = data.sample_stats.drop_vars(key)
            _, metrics = diagnostics(data)
            self.assertEqual(metrics['status'], 'INCOMPLETE')

    def test_observed_maximum_is_not_configured_cap(self):
        data = draws()
        data.sample_stats = data.sample_stats.drop_vars('reached_max_treedepth')
        _, metrics = diagnostics(data)
        self.assertEqual(metrics['status'], 'INCOMPLETE')
        self.assertIsNone(metrics['max_depth_hits'])
        self.assertTrue(diagnostics(data, 12)[1]['diagnostic_gate_passed'])
        self.assertFalse(diagnostics(data, 6)[1]['diagnostic_gate_passed'])

    def test_nonfinite_parameter_cannot_be_skipped(self):
        data = draws()
        data.posterior.z_community.values[:, :, 0] = 0
        _, metrics = diagnostics(data)
        self.assertFalse(metrics['diagnostic_gate_passed'])
        self.assertGreater(metrics['nonfinite_parameter_diagnostics'], 0)

    def test_divergence_and_depth_hit_block_pass(self):
        for key in ('diverging', 'reached_max_treedepth'):
            data = draws()
            data.sample_stats[key].values[0, 0] = True
            self.assertFalse(diagnostics(data)[1]['diagnostic_gate_passed'])

    def test_saved_file_audit_is_read_only_and_checks_file_count(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'synthetic.nc'
            draws().to_netcdf(path)
            before = hashlib.sha256(path.read_bytes()).digest()
            stream = io.StringIO()
            with contextlib.redirect_stdout(stream):
                code = main(['--input-dir', temp, '--expected-files', '9'])
            result = json.loads(stream.getvalue())
            self.assertEqual(code, 1)
            self.assertEqual(result['files_found'], 1)
            self.assertFalse(result['expected_count_matches'])
            self.assertNotIn('synthetic', stream.getvalue())
            self.assertEqual(before, hashlib.sha256(path.read_bytes()).digest())
            self.assertEqual(list(Path(temp).iterdir()), [path])


if __name__ == '__main__':
    unittest.main()
