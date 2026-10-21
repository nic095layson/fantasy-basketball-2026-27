#!/usr/bin/env python3
"""Red-first tests for the run-ledger (scripts/run_ledger.py) and its producers and consumer (Council 2026-10-21).

The ledger exists so "ran and passed" and "never ran" stop looking identical. These tests pin the properties that
make that true: rows are only ever appended; a gate that did not run has no row and reads as FALSIFIED, not as
silence; a stale or wrong-engine PASS is refused when the claim asks for fresh / live; and the two producers write
one row per gate or step, in order, without the test suite touching the real ledger.

    python3 scripts/test_run_ledger.py
"""
import datetime
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run_ledger as L  # noqa: E402
import gates as G  # noqa: E402
import morning as M  # noqa: E402
import check_claims as C  # noqa: E402

PY = sys.executable
FP = {"kit_head": "kkkkkkk", "deck_head": "ddddddd", "engine_commit": "eeeeeee"}


class Base(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.ledger = os.path.join(self.d, "report", "run-ledger.jsonl")
        self._fp = L.fingerprint
        L.fingerprint = lambda deck=None, kit=None: dict(FP)

    def tearDown(self):
        L.fingerprint = self._fp


class Ledger(Base):
    def test_record_appends_and_never_rewrites(self):
        L.record("a", "PASS", ledger=self.ledger)
        before = open(self.ledger, "rb").read()
        L.record("b", "FAIL", "why", ledger=self.ledger)
        after = open(self.ledger, "rb").read()
        self.assertTrue(after.startswith(before))
        rows = L.read(self.ledger)
        self.assertEqual([r["name"] for r in rows], ["a", "b"])
        self.assertEqual(rows[1]["engine_commit"], "eeeeeee")
        self.assertEqual(set(rows[0]), {"name", "ran_at", "verdict", "kit_head", "deck_head", "engine_commit", "detail"})

    def test_bad_verdict_and_empty_name_refused(self):
        with self.assertRaises(ValueError):
            L.record("a", "OK", ledger=self.ledger)
        with self.assertRaises(ValueError):
            L.record("", "PASS", ledger=self.ledger)
        self.assertFalse(os.path.exists(self.ledger))

    def test_never_ran_is_a_fail_with_a_reason(self):
        ok, why = L.check("ghost", ledger=self.ledger)
        self.assertFalse(ok)
        self.assertIn("never been recorded", why)

    def test_latest_row_decides(self):
        L.record("g", "PASS", ledger=self.ledger)
        L.record("g", "FAIL", ledger=self.ledger)
        self.assertFalse(L.check("g", ledger=self.ledger)[0])
        L.record("g", "PASS", ledger=self.ledger)
        self.assertTrue(L.check("g", ledger=self.ledger)[0])

    def test_age_limit(self):
        L.record("g", "PASS", ledger=self.ledger, ran_at="2026-10-01T00:00:00Z")
        now = datetime.datetime(2026, 10, 2, 0, 0, tzinfo=datetime.timezone.utc)
        self.assertTrue(L.check("g", max_age_hours=25, ledger=self.ledger, now=now)[0])
        self.assertFalse(L.check("g", max_age_hours=23, ledger=self.ledger, now=now)[0])

    def test_live_engine(self):
        L.record("g", "PASS", ledger=self.ledger)
        self.assertTrue(L.check("g", live_engine=True, ledger=self.ledger)[0])
        L.fingerprint = lambda deck=None, kit=None: dict(FP, engine_commit="fffffff")
        ok, why = L.check("g", live_engine=True, ledger=self.ledger)
        self.assertFalse(ok)
        self.assertIn("eeeeeee", why)
        self.assertEqual(list(L.stale(self.ledger)[0]), ["g"])

    def test_malformed_line_skipped_not_fatal(self):
        L.record("g", "PASS", ledger=self.ledger)
        with open(self.ledger, "a") as f:
            f.write("{not json\n")
        self.assertEqual(len(L.read(self.ledger)), 1)

    def test_live_fingerprint_reads_the_engine_files(self):
        L.fingerprint = self._fp
        fp = L.fingerprint()
        self.assertEqual(len(fp["engine_commit"].replace("+dirty", "")), 7, fp)

    def test_dirty_engine_is_marked(self):
        import subprocess
        repo = os.path.join(self.d, "deck")
        os.makedirs(os.path.join(repo, "arena"))
        os.makedirs(os.path.join(repo, "scripts"))
        for f in ("arena/arena.py", "scripts/hoops.py"):
            open(os.path.join(repo, f), "w").write("x = 1\n")
        run = lambda *a: subprocess.run(["git", "-C", repo] + list(a), capture_output=True, check=True)
        run("init", "-q"); run("add", "."); run("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "e")
        L.fingerprint = self._fp
        clean = L.fingerprint(deck=repo)["engine_commit"]
        self.assertEqual(len(clean), 7)
        open(os.path.join(repo, "arena/arena.py"), "w").write("x = 2\n")
        self.assertEqual(L.fingerprint(deck=repo)["engine_commit"], clean + "+dirty")


class Producers(Base):
    def test_gates_run_all_records_each_gate_in_order(self):
        ok = {"name": "one", "cmd": [PY, "-c", "print('GATE: PASS')"], "cwd": ".", "pass_re": "GATE: PASS"}
        bad = {"name": "two", "cmd": [PY, "-c", "raise SystemExit(1)"], "cwd": ".", "pass_re": "GATE: PASS"}
        G.run_all([ok, bad], inputs=[], root=self.d, ledger=self.ledger)
        rows = L.read(self.ledger)
        self.assertEqual([(r["name"], r["verdict"]) for r in rows], [("one", "PASS"), ("two", "FAIL")])

    def test_gates_without_ledger_writes_nothing(self):
        ok = {"name": "one", "cmd": [PY, "-c", "print('GATE: PASS')"], "cwd": ".", "pass_re": "GATE: PASS"}
        G.run_all([ok], inputs=[], root=self.d)
        self.assertFalse(os.path.exists(self.ledger))

    def test_morning_steps_recorded_including_skipped_never(self):
        ok = dict(name="s1", cmd=[PY, "-c", "print('S: PASS')"], cwd=".", pass_re="S: PASS")
        bad = dict(name="s2", cmd=[PY, "-c", "raise SystemExit(1)"], cwd=".", pass_re="S: PASS")
        M.run_steps([ok, bad, ok], os.path.join(self.d, "m.json"), ledger=self.ledger)
        rows = L.read(self.ledger)
        # the step after a fatal failure is SKIPPED: it did not run, so it has no row
        self.assertEqual([(r["name"], r["verdict"]) for r in rows], [("morning: s1", "PASS"), ("morning: s2", "FAIL")])

    def test_gates_main_appends_claims_gate_last(self):
        self.assertEqual(G.claims_gate()["name"], "kit check_claims --gate")
        self.assertIn("--gate", G.claims_gate()["cmd"])


class Consumer(Base):
    def test_ledger_pass_kind(self):
        L.record("kit check_report", "PASS", ledger=self.ledger)
        r = C.ledger_pass(self.d, "kit check_report")
        self.assertEqual(r["verdict"], "SUPPORTED")
        self.assertEqual(C.ledger_pass(self.d, "never ran")["verdict"], "FALSIFIED")

    def test_gate_code(self):
        self.assertEqual(C.gate_code([{"as_expected": True}, {"as_expected": True}]), 0)
        self.assertEqual(C.gate_code([{"as_expected": True}, {"as_expected": False}]), 1)
        self.assertEqual(C.gate_code([]), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
