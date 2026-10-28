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


if __name__ == "__main__":
    unittest.main(verbosity=2)
