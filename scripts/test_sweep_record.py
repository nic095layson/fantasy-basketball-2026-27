#!/usr/bin/env python3
"""Red-first tests for scripts/sweep_record.py (owner 2026-10-26, "re-measure the ranges every Monday"): the brief and
the deck quote the newest season sweep dated on or before the day, name its date and configuration, and fall back to
the draft sweep before the first season record.

    python3 scripts/test_sweep_record.py
"""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sweep_record as SR  # noqa: E402


class Latest(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        for d in ("redteam-2026-10-19", "redteam-2026-10-26-season", "redteam-2026-11-02-season", "redteam-2026-11-09-season",
                  "redteam-2026-11-16-season"):
            os.makedirs(os.path.join(self.root, d))
            if d != "redteam-2026-11-16-season":                       # a Monday whose sweep failed: no record
                json.dump({}, open(os.path.join(self.root, d, "sweep.json"), "w"))

    def test_the_newest_season_record_on_or_before_the_day(self):
        self.assertTrue(SR.latest("2026-11-05", self.root).endswith(os.path.join("redteam-2026-11-02-season", "sweep.json")))
        self.assertTrue(SR.latest("2026-11-02", self.root).endswith(os.path.join("redteam-2026-11-02-season", "sweep.json")))

    def test_a_monday_with_no_record_keeps_the_last_one(self):
        self.assertTrue(SR.latest("2026-11-17", self.root).endswith(os.path.join("redteam-2026-11-09-season", "sweep.json")))

    def test_a_same_day_real_schedule_record_wins_over_the_practice_one(self):
        os.makedirs(os.path.join(self.root, "redteam-2026-11-02-season-real"))
        json.dump({}, open(os.path.join(self.root, "redteam-2026-11-02-season-real", "sweep.json"), "w"))
        self.assertTrue(SR.latest("2026-11-05", self.root).endswith(os.path.join("redteam-2026-11-02-season-real", "sweep.json")))

    def test_before_the_first_season_record_the_draft_sweep(self):
        self.assertTrue(SR.latest("2026-10-21", self.root).endswith(os.path.join("redteam-2026-10-19", "sweep.json")))


class Describe(unittest.TestCase):
    def test_the_configuration_and_its_date(self):
        p = os.path.join("x", "redteam-2026-11-02-season", "sweep.json")
        self.assertEqual(SR.describe({"state_sha256": "a", "schedule": "s"}, p),
                         "season sweep of 2026-11-02 (current rosters, season pool, real schedule)")
        self.assertEqual(SR.describe({"state_sha256": "a"}, os.path.join("x", "redteam-2026-10-26-season", "sweep.json")),
                         "season sweep of 2026-10-26 (current rosters, season pool, practice schedule)")
        self.assertEqual(SR.describe({}, os.path.join("x", "redteam-2026-10-19", "sweep.json")),
                         "draft sweep of 2026-10-19 (draft rosters, frozen pool)")


if __name__ == "__main__":
    unittest.main(verbosity=2)
