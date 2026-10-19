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
        self.assertEqual([s["name"] for s in st], ["box scores 2026-10-20", "season lines", "season board", "status feed", "daily brief"])
        self.assertIn("--date", st[0]["cmd"]); self.assertIn("2026-10-20", st[0]["cmd"])
        self.assertIn("2026-10-21", st[4]["cmd"])
        self.assertTrue(all(s["pass_re"] for s in st))

    def test_no_fetch_skips_the_box_score_step(self):
        st = M.steps("2026-10-21", fetch=False, seasons=10000)
        self.assertEqual(st[0]["name"], "season lines")

    def test_brief_runs_on_the_season_pool(self):
        st = M.steps("2026-10-21", fetch=True, seasons=10000)
        brief = st[-1]
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
