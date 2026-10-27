#!/usr/bin/env python3
"""Red-first tests for weekly_preview.py's league-wide record (owner 2026-10-27, the weekly accuracy card): every
matchup's pre-week forecast, recorded before the week starts, append-only; a repeat is reported, not an error, so
the Sunday morning step can run every week whether or not a session already recorded the owner's matchup.

    python3 scripts/test_weekly_preview.py
"""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import weekly_preview as WP  # noqa: E402

PAIRS = [dict(a=1, b=2, p_win=0.6, exp_cats=5.0), dict(a=3, b=4, p_win=0.4, exp_cats=4.0)]


class LeagueRecord(unittest.TestCase):
    def setUp(self):
        self.p = os.path.join(tempfile.mkdtemp(), "calibration_league.json")

    def test_recorded_before_the_week(self):
        self.assertTrue(WP.record_league(self.p, 3, PAIRS, "2026-11-01T12:00:00Z", "2026-11-02"))
        w = json.load(open(self.p))["weeks"]["3"]
        self.assertEqual(w["pairs"], PAIRS); self.assertEqual(w["recorded_at"], "2026-11-01T12:00:00Z")

    def test_too_late_is_an_error(self):
        with self.assertRaises(WP.LedgerError):
            WP.record_league(self.p, 3, PAIRS, "2026-11-02T12:00:00Z", "2026-11-02")

    def test_a_repeat_is_reported_and_nothing_is_rewritten(self):
        WP.record_league(self.p, 3, PAIRS, "2026-11-01T12:00:00Z", "2026-11-02")
        self.assertFalse(WP.record_league(self.p, 3, [dict(PAIRS[0], p_win=0.99)], "2026-11-01T13:00:00Z", "2026-11-02"))
        self.assertEqual(json.load(open(self.p))["weeks"]["3"]["pairs"][0]["p_win"], 0.6)

    def test_the_owner_record_reports_a_repeat_when_asked(self):
        p = os.path.join(tempfile.mkdtemp(), "calibration.json")
        pred = dict(week=3, p_win=0.5)
        WP.record(p, pred, "2026-11-01T12:00:00Z", "2026-11-02")
        self.assertIsNone(WP.record(p, pred, "2026-11-01T13:00:00Z", "2026-11-02", if_absent=True))


if __name__ == "__main__":
    unittest.main(verbosity=2)
