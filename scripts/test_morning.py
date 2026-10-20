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
        self.assertEqual([s["name"] for s in st], ["league live", "box scores 2026-10-20", "season lines", "season board", "status feed", "transactions", "daily brief", "season deck"])
        self.assertIn("2026-10-20", st[1]["cmd"])
        self.assertIn("2026-10-21", st[6]["cmd"])
        self.assertTrue(all(s["pass_re"] for s in st))

    def test_no_fetch_skips_the_box_score_step(self):
        st = M.steps("2026-10-21", fetch=False, seasons=10000)
        self.assertEqual(st[0]["name"], "season lines")
        self.assertNotIn("transactions", [s["name"] for s in st])
        self.assertNotIn("league live", [s["name"] for s in st])

    def test_status_gate_checks_the_runs_own_dated_file(self):
        # 2026-10-20: --check with no file read the newest-dated file (a test run's 10/21), not the morning's own
        st = M.steps("2026-10-20", fetch=False, seasons=10000)
        gate = next(s for s in st if s["name"] == "status feed")["cmd"][-1]
        self.assertIn("--check", gate); self.assertTrue(gate.endswith("status_2026-10-20.json"))

    def test_brief_runs_on_the_season_pool(self):
        st = M.steps("2026-10-21", fetch=True, seasons=10000)
        brief = next(s for s in st if s["name"] == "daily brief")
        self.assertTrue(brief["env"]["SEASON_POOL"].endswith(os.path.join("data", "season", "pool_season.csv")))


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
        live = next(s for s in st if s["name"] == "league live")
        self.assertFalse(live.get("fatal", True))

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
