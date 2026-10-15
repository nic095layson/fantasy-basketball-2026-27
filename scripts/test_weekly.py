#!/usr/bin/env python3
"""Red-first tests for scripts/weekly_preview.py and the calibration ledger (Session 1 item 7; plan §4 B6).

The ledger is the only grade that is not circular (L6), so it must be impossible to edit a
prediction after the week starts: a recorded week is append-only.

    python3 scripts/test_weekly.py
"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import weekly_preview as WP  # noqa: E402

PRED = {"week": 1, "opponent_seat": 11, "p_win": 0.6, "exp_cats": 4.9,
        "cat_p": {"FG%": 0.6, "FT%": 0.7, "3PTM": 0.5, "PTS": 0.4, "REB": 0.4, "AST": 0.3, "ST": 0.5, "BLK": 0.7, "TO": 0.9}}


class Ledger(unittest.TestCase):
    def test_records_before_the_week_and_refuses_a_rewrite(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "calibration.json")
            WP.record(p, PRED, recorded_at="2026-10-15T20:00:00Z", week_start="2026-10-20")
            with self.assertRaises(WP.LedgerError):
                WP.record(p, dict(PRED, p_win=0.9), recorded_at="2026-10-16T00:00:00Z", week_start="2026-10-20")
            self.assertEqual(json.load(open(p))["weeks"]["1"]["p_win"], 0.6)

    def test_refuses_a_prediction_recorded_after_the_week_started(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(WP.LedgerError):
                WP.record(os.path.join(d, "c.json"), PRED, recorded_at="2026-10-21T00:00:00Z", week_start="2026-10-20")

    def test_brier_scores_the_categories_and_the_matchup(self):
        actual = {"won": ["FG%", "FT%", "BLK", "TO", "ST"]}
        s = WP.score(PRED, actual)
        want = sum((PRED["cat_p"][c] - (1.0 if c in actual["won"] else 0.0)) ** 2 for c in PRED["cat_p"]) / 9
        self.assertAlmostEqual(s["brier_cats"], want)
        self.assertAlmostEqual(s["brier_matchup"], (0.6 - 1.0) ** 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
