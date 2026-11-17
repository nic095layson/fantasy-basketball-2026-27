#!/usr/bin/env python3
"""Red-first tests for scripts/sweep_record.py (owner 2026-10-26, "re-measure the ranges every Monday"): the brief and
the deck quote the newest season sweep dated on or before the day, name its date and configuration, and fall back to
the draft sweep before the first season record.

    python3 scripts/test_sweep_record.py
"""
import json
import os
import subprocess
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
                         "season sweep of 2026-11-02 (rosters of that date, season pool, real schedule)")
        self.assertEqual(SR.describe({"state_sha256": "a"}, os.path.join("x", "redteam-2026-10-26-season", "sweep.json")),
                         "season sweep of 2026-10-26 (rosters of that date, season pool, practice schedule)")
        self.assertEqual(SR.describe({}, os.path.join("x", "redteam-2026-10-19", "sweep.json")),
                         "draft sweep of 2026-10-19 (draft rosters, frozen pool)")

    def test_the_age_on_the_day_it_is_quoted(self):
        # audit finding F2 (2026-11-12): a sweep three days old was labelled "current rosters"
        p = os.path.join("x", "redteam-2026-11-09-season", "sweep.json")
        rec = {"state_sha256": "a", "schedule": "s"}
        self.assertEqual(SR.describe(rec, p, as_of="2026-11-12"),
                         "season sweep of 2026-11-09 (3 days old; rosters of that date, season pool, real schedule)")
        self.assertEqual(SR.describe(rec, p, as_of="2026-11-10"),
                         "season sweep of 2026-11-09 (1 day old; rosters of that date, season pool, real schedule)")
        self.assertEqual(SR.describe(rec, p, as_of="2026-11-09"),
                         "season sweep of 2026-11-09 (made today; rosters of that date, season pool, real schedule)")
        self.assertNotIn("current rosters", SR.describe(rec, p, as_of="2026-11-12"))



def _git(d, *args):
    subprocess.run(["git", "-C", d, "-c", "user.name=t", "-c", "user.email=t@t", *args], check=True, capture_output=True)


class Stale(unittest.TestCase):
    """Owner 2026-11-17 (card: "Flag it and re-sweep"): on 2026-11-17 the brief and the deck printed the band of a sweep
    made on Monday morning's engine (shock 0.06, healthy 0.88) beside a title share computed on the engine changed that
    afternoon. The record now says so: STALE when the engine files at its commit are not the live ones (the attack
    runner's own rule), and "not compared" when it cannot tell."""
    def setUp(self):
        self.deck = tempfile.mkdtemp()
        _git(self.deck, "init", "-q")
        for f in ("scripts", "arena"):
            os.makedirs(os.path.join(self.deck, f))
        self.write("scripts/hoops.py", "A = 1\n"); self.write("arena/arena.py", "SHOCK = 0.06\n")
        self.first = self.commit("engine v1")
        self.write("README.md", "docs\n")
        self.docs = self.commit("docs only")

    def write(self, rel, text):
        with open(os.path.join(self.deck, rel), "w") as f:
            f.write(text)

    def commit(self, msg):
        _git(self.deck, "add", "-A"); _git(self.deck, "commit", "-q", "-m", msg)
        return subprocess.run(["git", "-C", self.deck, "rev-parse", "--short=7", "HEAD"], capture_output=True, text=True).stdout.strip()

    def test_a_record_on_the_live_engine_is_current_even_after_a_docs_commit(self):
        self.assertEqual(SR.stale({"engine_commit": self.first}, self.deck), dict(status="CURRENT", why=""))
        self.assertEqual(SR.stale({"engine_commit": self.docs}, self.deck)["status"], "CURRENT")

    def test_a_record_made_before_an_engine_change_is_stale_and_says_which_engines(self):
        self.write("arena/arena.py", "SHOCK = 0.11\n")
        live = self.commit("engine v2")
        s = SR.stale({"engine_commit": self.docs}, self.deck)
        self.assertEqual(s["status"], "STALE")
        self.assertEqual(s["why"], f"measured on engine {self.first}, the live engine is {live}")

    def test_a_commit_the_checkout_does_not_hold_is_not_compared(self):
        s = SR.stale({"engine_commit": "0123abc"}, self.deck)
        self.assertEqual(s["status"], "UNKNOWN"); self.assertIn("0123abc is not in the deck checkout", s["why"])

    def test_a_record_with_no_engine_or_no_deck_is_not_compared(self):
        self.assertEqual(SR.stale({}, self.deck)["status"], "UNKNOWN")
        self.assertEqual(SR.stale({"engine_commit": self.first}, None)["status"], "UNKNOWN")
        self.assertEqual(SR.stale({"engine_commit": self.first}, os.path.join(self.deck, "nowhere"))["status"], "UNKNOWN")

    def test_the_older_records_engine_key_is_read_too(self):
        self.assertEqual(SR.stale({"engine": self.first}, self.deck)["status"], "CURRENT")

    def test_the_note_is_loud_for_stale_quiet_for_unknown_and_empty_for_current(self):
        self.assertEqual(SR.stale_note(dict(status="CURRENT", why="")), "")
        self.assertEqual(SR.stale_note(dict(status="STALE", why="measured on engine aaa, the live engine is bbb")),
                         "STALE: measured on engine aaa, the live engine is bbb, so these shifts are not today's")
        self.assertEqual(SR.stale_note(dict(status="UNKNOWN", why="commit x is not in the deck checkout")),
                         "not compared with the live engine: commit x is not in the deck checkout")

if __name__ == "__main__":
    unittest.main(verbosity=2)
