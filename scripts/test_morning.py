#!/usr/bin/env python3
"""Red-first tests for scripts/morning.py (the in-season morning run: box scores, season lines, season board,
status feed, daily brief, each step recorded like a gate; Council 2026-10-19 decisions 6 and 7).

    python3 scripts/test_morning.py
"""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import morning as M  # noqa: E402

PY = sys.executable


class Steps(unittest.TestCase):
    def test_steps_in_order_with_dates(self):
        st = M.steps("2026-10-21", fetch=True, seasons=10000)
        # 2026-10-21: "preflight" became step 0 (independent-audit adoption); the indices below moved by one.
        # 2026-10-23 (owner, Build 1): "league table" after the week matchup, before the deck that draws it
        self.assertEqual([s["name"] for s in st], ["preflight", "league live", "matchup live", "box scores 2026-10-20", "season lines", "season board", "status feed", "transactions", "daily brief", "week matchup", "league table", "form board", "season deck"])
        self.assertIn("2026-10-20", st[3]["cmd"])
        self.assertIn("2026-10-21", st[8]["cmd"])
        self.assertTrue(all(s["pass_re"] for s in st))

    def test_no_fetch_skips_the_box_score_step(self):
        st = M.steps("2026-10-21", fetch=False, seasons=10000)
        self.assertEqual(st[1]["name"], "season lines")  # st[0] is the preflight since 2026-10-21
        self.assertNotIn("transactions", [s["name"] for s in st])
        self.assertNotIn("league live", [s["name"] for s in st])

    def test_status_gate_checks_the_runs_own_dated_file(self):
        # 2026-10-20: --check with no file read the newest-dated file (a test run's 10/21), not the morning's own
        st = M.steps("2026-10-20", fetch=False, seasons=10000)
        gate = next(s for s in st if s["name"] == "status feed")["cmd"][-1]
        self.assertIn("--check", gate); self.assertTrue(gate.endswith("status_2026-10-20.json"))

    def test_since_reaches_both_transcript_readers_and_only_them(self):
        # GAUNTLET 2026-10-21 item 7: the persistent runner passes its start time so yesterday's pull never counts
        st = M.steps("2026-10-21", fetch=True, seasons=10000, since="2026-10-21T12:53:00Z")
        for s in st:
            has = "--since" in s["cmd"]
            self.assertEqual(has, s["name"] in ("league live", "matchup live"), s["name"])
            if has:
                self.assertEqual(s["cmd"][s["cmd"].index("--since") + 1], "2026-10-21T12:53:00Z")
        self.assertFalse(any("--since" in s["cmd"] for s in M.steps("2026-10-21", fetch=True, seasons=10000)))

    def test_brief_runs_on_the_season_pool(self):
        st = M.steps("2026-10-21", fetch=True, seasons=10000)
        brief = next(s for s in st if s["name"] == "daily brief")
        self.assertTrue(brief["env"]["SEASON_POOL"].endswith(os.path.join("data", "season", "pool_season.csv")))


    def test_week_matchup_runs_on_the_season_pool_before_the_deck_and_never_stops_the_run(self):
        # owner 2026-10-21: the Today tab's week card; a failure leaves the deck without the card, never without a deck
        for fetch in (True, False):
            names = [s["name"] for s in M.steps("2026-10-22", fetch=fetch, seasons=10000)]
            self.assertLess(names.index("daily brief"), names.index("week matchup"))
            self.assertLess(names.index("week matchup"), names.index("season deck"))
        wm = next(s for s in M.steps("2026-10-22", fetch=True, seasons=10000) if s["name"] == "week matchup")
        self.assertIs(wm["fatal"], False)
        self.assertIn("2026-10-22", wm["cmd"]); self.assertEqual(wm["pass_re"], r"^WEEK MATCHUP: PASS")
        self.assertTrue(wm["env"]["SEASON_POOL"].endswith(os.path.join("data", "season", "pool_season.csv")))

class Run(unittest.TestCase):
    def test_a_failing_step_fails_the_morning_and_later_steps_do_not_run(self):
        ok = {"name": "ok", "cmd": [PY, "-c", "print('STEP: PASS')"], "cwd": ".", "pass_re": "STEP: PASS", "env": {}}
        bad = {"name": "bad", "cmd": [PY, "-c", "print('STEP: FAIL'); raise SystemExit(1)"], "cwd": ".", "pass_re": "STEP: PASS", "env": {}}
        with tempfile.TemporaryDirectory() as d:
            rec = M.run_steps([ok, bad, ok], os.path.join(d, "m.json"))
            self.assertEqual(rec["verdict"], "FAIL")
            self.assertEqual([s["verdict"] for s in rec["steps"]], ["PASS", "FAIL", "SKIPPED"])
            self.assertTrue(os.path.exists(os.path.join(d, "m.json")))

    def test_all_pass_is_pass_with_the_pass_lines(self):
        ok = {"name": "ok", "cmd": [PY, "-c", "print('STEP: PASS — fine')"], "cwd": ".", "pass_re": "STEP: PASS", "env": {}}
        with tempfile.TemporaryDirectory() as d:
            rec = M.run_steps([ok, ok], os.path.join(d, "m.json"))
            self.assertEqual(rec["verdict"], "PASS"); self.assertIn("fine", rec["steps"][0]["pass_line"])



class NonFatal(unittest.TestCase):
    """Owner 2026-10-20 (plan-gate A5): a failed live pull keeps the last paste and the morning goes on."""

    def test_league_live_is_marked_non_fatal(self):
        st = M.steps("2026-10-21", fetch=True, seasons=10000)
        for name in ("league live", "matchup live"):
            step = next(s for s in st if s["name"] == name)
            self.assertFalse(step.get("fatal", True), name)

    def test_a_non_fatal_fail_does_not_stop_the_run(self):
        import tempfile, os, sys
        st = [dict(name="a", cmd=[sys.executable, "-c", "print('NOPE'); raise SystemExit(1)"], cwd=".", pass_re=r"^YES", env={}, fatal=False),
              dict(name="b", cmd=[sys.executable, "-c", "print('OK B')"], cwd=".", pass_re=r"^OK B", env={})]
        out = os.path.join(tempfile.mkdtemp(), "m.json")
        rec = M.run_steps(st, out)
        self.assertEqual([x["verdict"] for x in rec["steps"]], ["FAIL (non-fatal)", "PASS"])
        self.assertEqual(rec["verdict"], "PASS")

if __name__ == "__main__":
    unittest.main(verbosity=2)


class LedgerParent(unittest.TestCase):
    def test_every_step_runs_with_the_morning_named_as_ledger_parent(self):
        # owner 2026-10-23 (D5): the step scripts record their own ledger rows when run alone; under the morning run
        # they must not, since run_steps records 'morning: <step>' itself
        d = tempfile.mkdtemp()
        step = {"name": "echo", "cmd": [PY, "-c", "import os; print('PARENT ' + os.environ.get('KIT_LEDGER_PARENT', 'none'))"],
                "cwd": ".", "pass_re": r"^PARENT morning$", "env": {}}
        rec = M.run_steps([step], os.path.join(d, "m.json"))
        self.assertEqual(rec["steps"][0]["verdict"], "PASS", rec["steps"][0])
