#!/usr/bin/env python3
"""Red-first tests for scripts/gates.py (plan 2026-10-15 §4 D3; RULES.md rule 7).

The runner must refuse what a terminal glance accepts: a gate that exits 0 with no
PASS line (the 10/15 empty-log near-miss), a gate that prints PASS and exits 1, and a
gates.json whose recorded inputs no longer match the files on disk.

    python3 scripts/test_gates_runner.py
"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gates as G  # noqa: E402

PY = sys.executable


def gate(name, code, pass_re="GATE: PASS"):
    return {"name": name, "cmd": [PY, "-c", code], "cwd": ".", "pass_re": pass_re}


OK = gate("ok", "print('GATE: PASS — fine')")
EMPTY = gate("empty", "pass")                                  # exit 0, no output
LIAR = gate("liar", "print('GATE: PASS'); raise SystemExit(1)")  # PASS text, exit 1
FAIL = gate("fail", "print('GATE: FAIL'); raise SystemExit(1)")


class RunGate(unittest.TestCase):
    def test_pass_needs_exit0_and_pass_line(self):
        r = G.run_gate(OK)
        self.assertEqual((r["exit"], r["verdict"]), (0, "PASS"))
        self.assertIn("GATE: PASS", r["pass_line"])

    def test_exit0_with_empty_log_is_fail(self):
        r = G.run_gate(EMPTY)
        self.assertEqual(r["exit"], 0)
        self.assertEqual(r["verdict"], "FAIL")
        self.assertEqual(r["pass_line"], "")

    def test_pass_text_with_nonzero_exit_is_fail(self):
        self.assertEqual(G.run_gate(LIAR)["verdict"], "FAIL")

    def test_overall_verdict_fails_if_any_gate_fails(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(G.run_all([OK, OK], inputs=[], root=d)["verdict"], "PASS")
            self.assertEqual(G.run_all([OK, FAIL], inputs=[], root=d)["verdict"], "FAIL")
            self.assertEqual(G.run_all([], inputs=[], root=d)["verdict"], "FAIL")


class Verify(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.inp = os.path.join(self.d, "report.md")
        with open(self.inp, "w") as f:
            f.write("report v1\n")
        self.out = os.path.join(self.d, "gates.json")

    def write(self, specs):
        rec = G.run_all(specs, inputs=[self.inp], root=self.d)
        with open(self.out, "w") as f:
            json.dump(rec, f)
        return rec

    def test_fresh_pass_record_verifies(self):
        self.write([OK])
        ok, problems = G.verify(self.out, root=self.d)
        self.assertTrue(ok, problems)

    def test_changed_input_is_refused(self):
        self.write([OK])
        with open(self.inp, "a") as f:
            f.write("edited after the gates ran\n")
        ok, problems = G.verify(self.out, root=self.d)
        self.assertFalse(ok)
        self.assertTrue(any("report.md" in p for p in problems), problems)

    def test_missing_record_is_refused(self):
        ok, _ = G.verify(self.out, root=self.d)
        self.assertFalse(ok)

    def test_failing_record_is_refused(self):
        self.write([OK, EMPTY])
        ok, problems = G.verify(self.out, root=self.d)
        self.assertFalse(ok)
        self.assertTrue(any("empty" in p for p in problems), problems)

    def test_verify_refuses_a_record_that_does_not_cover_the_named_report(self):
        # 2026-10-15 (item 5): a failed chain left item 2's gates.json in place and --verify passed it
        self.write([OK])
        other = os.path.join(self.d, "other-report.md")
        open(other, "w").write("a different report\n")
        ok, problems = G.verify(self.out, root=self.d, report=other)
        self.assertFalse(ok)
        self.assertTrue(any("does not cover" in p for p in problems), problems)
        ok, problems = G.verify(self.out, root=self.d, report=self.inp)
        self.assertTrue(ok, problems)

    def test_quote_carries_pass_lines_and_exit_codes(self):
        rec = self.write([OK])
        q = G.quote(rec)
        self.assertIn("GATE: PASS — fine", q)
        self.assertIn("exit 0", q)
        self.assertIn("verdict: PASS", q)


if __name__ == "__main__":
    unittest.main(verbosity=2)
