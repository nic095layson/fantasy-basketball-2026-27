#!/usr/bin/env python3
"""Red-first tests for report/check_report.py's Runner impact line (RULES rule 11, owner 2026-10-28: "Proceed with
both"). Every after-report states what it does to the runner's scheduled tasks: none, code-only, or a prompt edit.

    python3 scripts/test_check_report.py
"""
import importlib.util
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("check_report", os.path.join(KIT, "report", "check_report.py"))
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

BODY = """# A report

Pull window: 2026-10-28 → 2026-10-28 (test)

## 1. Something

text

{impact}

## Watchlist

- item

## Open-item receipts

| item | status | receipt |
|---|---|---|
| x | done | §1 |

## Repeat-name market check

carried
"""


class RunnerImpact(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.log = os.path.join(self.d, "pull-log.md")
        open(self.log, "w").write("| 2026-10-28 | test | 0 | 0 | 0 | r.md |\n")
        self.orig = C.PULL_LOG
        C.PULL_LOG = self.log

    def tearDown(self):
        C.PULL_LOG = self.orig

    def run_check(self, impact):
        p = os.path.join(self.d, "after-report-2026-10-28-x.md")
        open(p, "w", encoding="utf-8").write(BODY.format(impact=impact))
        out = io.StringIO()
        with redirect_stdout(out):
            code = C.check(p)
        return code, out.getvalue()

    def test_each_stated_value_passes(self):
        for v in ("Runner impact: none", "Runner impact: code-only (each run merges main)",
                  "Runner impact: prompt edit, read back byte-equal"):
            code, out = self.run_check(v)
            self.assertEqual(code, 0, out)

    def test_a_report_without_the_line_fails_and_names_it(self):
        code, out = self.run_check("")
        self.assertEqual(code, 1)
        self.assertIn("Runner impact", out)

    def test_a_value_outside_the_three_fails(self):
        code, out = self.run_check("Runner impact: maybe")
        self.assertEqual(code, 1)
        self.assertIn("Runner impact", out)

    def test_the_line_must_start_a_line(self):
        code, _ = self.run_check("See the Runner impact: none line elsewhere.")
        self.assertEqual(code, 1)



SLIM = """# A report

Pull window: 2026-11-12 → 2026-11-12 (test)

## 1. Something

text

Runner impact: none

{line}
"""


class PoolRowsTouched(unittest.TestCase):
    """Council verdict 2026-11-12 (owner: "proceed with their verdicts"): 33 reports carried an identical copied tail
    (a past watch item and preseason receipt tables marked "did not check"). A report that states
    "Pool rows touched: none", and whose claim holds against main, does not owe the Watchlist, Open-item receipts and
    Repeat-name sections; any other report owes them as before."""
    def run_check(self, text, changed=()):
        d = tempfile.mkdtemp(); path = os.path.join(d, "after-report-2026-11-12-x.md")
        open(path, "w", encoding="utf-8").write(text)
        log = os.path.join(d, "pull-log.md"); open(log, "w").write("| 2026-11-12 | t | 0 | 0 | 0 | x |\n")
        old_log, old_fn = C.PULL_LOG, C.changed_pool_files
        C.PULL_LOG, C.changed_pool_files = log, (lambda root=None: changed)
        try:
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = C.check(path)
            return rc, buf.getvalue()
        finally:
            C.PULL_LOG, C.changed_pool_files = old_log, old_fn

    def test_the_stated_and_verified_line_lifts_the_three_sections(self):
        rc, out = self.run_check(SLIM.format(line="Pool rows touched: none"), changed=[])
        self.assertEqual(rc, 0, out); self.assertIn("no pool row touched", out)

    def test_without_the_line_the_three_sections_are_owed(self):
        rc, out = self.run_check(SLIM.format(line=""), changed=[])
        self.assertEqual(rc, 1)
        for name in ("watchlist section", "Open-item receipts", "Repeat-name market check"):
            self.assertIn(name, out)

    def test_the_line_is_refused_when_a_projection_file_differs_from_main(self):
        rc, out = self.run_check(SLIM.format(line="Pool rows touched: none"), changed=["report/projections-2026-27.csv"])
        self.assertEqual(rc, 1); self.assertIn("report/projections-2026-27.csv", out); self.assertIn("watchlist section", out)

    def test_the_line_is_refused_when_main_cannot_be_read(self):
        rc, out = self.run_check(SLIM.format(line="Pool rows touched: none"), changed=None)
        self.assertEqual(rc, 1); self.assertIn("could not be checked against main", out)

    def test_the_rest_of_the_gate_still_applies(self):
        rc, out = self.run_check(SLIM.format(line="Pool rows touched: none").replace("Runner impact: none", ""), changed=[])
        self.assertEqual(rc, 1); self.assertIn("Runner impact", out)

    def test_exempt_reads_the_same_rule_for_the_gate_runner(self):
        d = tempfile.mkdtemp(); path = os.path.join(d, "r.md"); open(path, "w").write(SLIM.format(line="Pool rows touched: none"))
        old = C.changed_pool_files
        try:
            C.changed_pool_files = lambda root=None: []
            self.assertTrue(C.pool_exempt(path)[0])
            C.changed_pool_files = lambda root=None: ["data/pool_additions.csv"]
            self.assertFalse(C.pool_exempt(path)[0])
        finally:
            C.changed_pool_files = old


if __name__ == "__main__":
    unittest.main(verbosity=2)
