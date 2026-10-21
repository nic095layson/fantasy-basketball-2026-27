#!/usr/bin/env python3
"""Red-first cases for the claim-vs-reality check (GAUNTLET 2026-10-21).

The defect this check exists for: three claims the system made about itself
in one night had no live counterpart — the self-audit's "the weekly in-season
pull keeps it green", the scheduled tasks' "the kit is this session's own
repository", and D-INT-1's "run the re-dating pass". Each read as a fact and
each was false. check_claims.py asserts a registry of such claims mechanically.
"""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_claims as cc  # noqa: E402


class WriterExists(unittest.TestCase):
    def test_falsified_when_nothing_writes_the_path(self):
        # roster-provenance.csv: referenced only by readers.
        v = cc.writer_exists(cc.KIT, "report/roster-provenance.csv")
        self.assertEqual(v["verdict"], "FALSIFIED", v)
        self.assertEqual(v["writers"], [], v)

    def test_supported_when_a_writer_exists(self):
        # known-answer control: gates.json is written by scripts/gates.py.
        v = cc.writer_exists(cc.KIT, "gates.json")
        self.assertEqual(v["verdict"], "SUPPORTED", v)
        self.assertIn("scripts/gates.py", v["writers"], v)

    def test_sees_a_writer_routed_through_an_argparse_default(self):
        # Regression guard, 2026-10-21: the detector FAILED this known-answer
        # case on its first run. gates.py never names gates.json next to an
        # open() --- the path is --out's default and reaches the write as
        # a.out. A detector blind to that idiom reports "no writer" for most
        # scripts in this repo, which is the broadly-failing-checker trap
        # (adversarial-verify rule 9).
        src = cc._read(cc.KIT + "/scripts/gates.py")
        self.assertIn('default=os.path.join(KIT, "gates.json")', src)
        self.assertIn('open(a.out, "w"', src)
        self.assertEqual(
            cc.writer_exists(cc.KIT, "gates.json")["verdict"], "SUPPORTED")


class InvokedBy(unittest.TestCase):
    def test_falsified_when_not_invoked(self):
        v = cc.invoked_by(cc.KIT, "check_provenance.py", "scripts/morning.py")
        self.assertEqual(v["verdict"], "FALSIFIED", v)

    def test_supported_when_invoked(self):
        # known-answer control: the detector must be able to say yes.
        v = cc.invoked_by(cc.KIT, "season_deck.py", "scripts/morning.py")
        self.assertEqual(v["verdict"], "SUPPORTED", v)


class Registry(unittest.TestCase):
    def test_registry_loads_and_every_row_is_checkable(self):
        rows = cc.load_registry(cc.KIT)
        self.assertGreaterEqual(len(rows), 4)
        for r in rows:
            self.assertIn(r["check"]["kind"], cc.KINDS, r["id"])
            for k in ("id", "claim", "asserted_in"):
                self.assertTrue(r.get(k), r)

    def test_run_reports_both_verdicts(self):
        # A checker that fails everything indicts itself (adversarial-verify
        # rule 9), so the registry must contain at least one SUPPORTED row.
        res = cc.run(cc.KIT)
        verdicts = {r["verdict"] for r in res}
        self.assertIn("FALSIFIED", verdicts)
        self.assertIn("SUPPORTED", verdicts)

    def test_exit_code_nonzero_when_a_claim_is_falsified(self):
        self.assertEqual(cc.exit_code(cc.run(cc.KIT)), 1)


if __name__ == "__main__":
    unittest.main()
