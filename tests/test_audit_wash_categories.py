"""Synthetic tests for the read-only WASH category preflight.

Run from repository root:
    python -m unittest discover -s tests -p 'test_audit_wash_categories.py' -v
No DHS file required or accessed.
"""
import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from audit_wash_categories import (  # noqa: E402
    classify, IMPROVED_WATER, UNIMPROVED_WATER,
    IMPROVED_SANITATION, UNIMPROVED_SANITATION,
)


class TestWashCodingAudit(unittest.TestCase):
    def test_known_water_codes(self):
        series = pd.Series(["piped into dwelling", "unprotected well",
                            "piped into dwelling"])
        rows, review = classify(series, IMPROVED_WATER, UNIMPROVED_WATER)
        self.assertFalse(review)
        self.assertEqual({label: (count, category) for label, count, category in rows},
                         {"piped into dwelling": (2, "improved"),
                          "unprotected well": (1, "unimproved")})

    def test_missing_water_fails_closed(self):
        rows, review = classify(pd.Series(["piped into dwelling", None]),
                                IMPROVED_WATER, UNIMPROVED_WATER)
        self.assertTrue(review)
        self.assertIn(("<missing>", 1, "MISSING"), rows)

    def test_unknown_water_fails_closed(self):
        rows, review = classify(pd.Series(["unknown water label"]),
                                IMPROVED_WATER, UNIMPROVED_WATER)
        self.assertTrue(review)
        self.assertEqual(rows[0][2], "UNRECOGNISED—REVIEW")

    def test_sanitation_classification_and_unknown(self):
        values = pd.Series(["pit latrine with slab", "no facility/bush/field",
                            "pit latrine without slab"])
        rows, review = classify(values, IMPROVED_SANITATION, UNIMPROVED_SANITATION)
        self.assertTrue(review)
        kinds = {v: kind for v, _, kind in rows}
        self.assertEqual(kinds["pit latrine with slab"], "improved")
        self.assertEqual(kinds["no facility/bush/field"], "unimproved")
        self.assertEqual(kinds["pit latrine without slab"], "UNRECOGNISED—REVIEW")

    def test_empty_group(self):
        rows, review = classify(pd.Series([], dtype="object"),
                                IMPROVED_WATER, UNIMPROVED_WATER)
        self.assertEqual(rows, [])
        self.assertFalse(review)  # main() now separately rejects empty analytic samples

if __name__ == "__main__":
    unittest.main()
