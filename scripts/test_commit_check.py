#!/usr/bin/env python3
"""Red-first tests for scripts/commit_check.py (owner 2026-10-26, option 2A): after the run's commit, anything the run
wrote that is still uncommitted must fail loudly instead of waiting to be stashed as a "leftover" by the next run.

    python3 scripts/test_commit_check.py
"""
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import commit_check as CC  # noqa: E402


def repo():
    d = tempfile.mkdtemp()
    for c in (["init", "-q", "-b", "main"], ["config", "user.email", "t@t"], ["config", "user.name", "t"]):
        subprocess.run(["git", *c], cwd=d, capture_output=True)
    os.makedirs(os.path.join(d, "data"))
    open(os.path.join(d, "data", "seed.txt"), "w").write("x\n")
    subprocess.run(["git", "add", "-A"], cwd=d, capture_output=True)
    subprocess.run(["git", "-c", "commit.gpgsign=false", "commit", "-qm", "seed"], cwd=d, capture_output=True)
    return d


class Check(unittest.TestCase):
    def test_a_clean_tree_passes(self):
        rc, msg = CC.check(repo())
        self.assertEqual(rc, 0); self.assertIn("COMMIT CHECK: PASS", msg)

    def test_an_uncommitted_run_output_fails_and_names_it(self):
        d = repo()
        os.makedirs(os.path.join(d, "report", "league"))
        open(os.path.join(d, "report", "league", "league_2026-10-26.json"), "w").write("{}")
        rc, msg = CC.check(d)
        self.assertEqual(rc, 1)
        self.assertIn("COMMIT CHECK: FAIL", msg); self.assertIn("report/league/league_2026-10-26.json", msg)

    def test_paths_outside_data_and_report_do_not_fail_the_check(self):
        d = repo()
        open(os.path.join(d, "scratch.txt"), "w").write("x")
        rc, msg = CC.check(d)
        self.assertEqual(rc, 0, msg)

    def test_expected_paths_may_be_named_and_are_still_reported_when_missing(self):
        d = repo()
        rc, msg = CC.check(d, expected=["report/league/league_2026-10-26.json"])
        self.assertEqual(rc, 1)
        self.assertIn("never committed", msg); self.assertIn("report/league/league_2026-10-26.json", msg)

    def test_cli_exits_nonzero_on_a_dirty_tree(self):
        d = repo()
        os.makedirs(os.path.join(d, "data", "news"))
        open(os.path.join(d, "data", "news", "x.json"), "w").write("{}")
        p = subprocess.run([sys.executable, os.path.join(HERE, "commit_check.py"), "--root", d], capture_output=True, text=True)
        self.assertEqual(p.returncode, 1)
        self.assertIn("COMMIT CHECK: FAIL", p.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
