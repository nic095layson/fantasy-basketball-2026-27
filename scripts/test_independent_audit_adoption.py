#!/usr/bin/env python3
"""Red-first tests for the kit's adoption of the library's independent-audit gates (owner 2026-10-21: "Build all
the recommended … This is not just for Fantasy Basketball, but Claude Global"; the library skill is
nic095layson/claude-core-skills .claude/skills/independent-audit/).

What the kit adopts, each against a recorded 10/19–10/21 failure:
  - morning preflight (step 0, fatal): the runner said "deck still missing" and published no deck; the render
    step needs playwright; a fresh session had no checkout (10/20 evening run did nothing).
  - claim receipts on every after-report (advisory): "the weekly pull keeps it green", "changes nothing either way".
  - deck replay over the last recorded real mornings (`gates.py --replay`): the 10/21 deck lost its tabs, and the
    no-matchup morning crashed, both after passing every test.

    python3 scripts/test_independent_audit_adoption.py
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import gates as G  # noqa: E402
import morning as M  # noqa: E402

IA = os.path.join(HERE, "independent_audit")
SPEC = os.path.join(IA, "morning_preflight.json")


class MorningPreflight(unittest.TestCase):
    def test_preflight_is_the_first_step_and_fatal(self):
        for fetch in (True, False):
            st = M.steps("2026-10-22", fetch=fetch, seasons=10000)
            self.assertEqual(st[0]["name"], "preflight")
            self.assertTrue(st[0].get("fatal", True))
            self.assertEqual(st[0]["pass_re"], r"^PREFLIGHT: PASS")
            self.assertIn(SPEC, st[0]["cmd"])

    def test_spec_declares_what_the_run_assumes(self):
        spec = json.load(open(SPEC))
        names = [c["name"] for c in spec["checks"]]
        for want in ("kit checkout", "deck repo beside the kit", "briefs writable"):
            self.assertIn(want, names)
        # 2026-10-21 (kit session's merge check of #155/#156): the runner had no playwright at 18:34Z and every
        # step through the brief still passed; only the deck failed, closed. A fatal preflight on playwright would
        # have stopped the whole morning. The preflight holds only what the WHOLE run needs; a dependency of one
        # step stays that step's own fail-closed check.
        self.assertFalse(any("playwright" in (c.get("cmd", "") + c["name"]).lower() for c in spec["checks"]),
                         "a one-step dependency must not stop the whole morning")
        self.assertTrue(all(c.get("hint") for c in spec["checks"]), "every check says what to do when it fails")

    def test_spec_fails_loudly_outside_the_kit(self):
        with tempfile.TemporaryDirectory() as d:
            r = subprocess.run([sys.executable, os.path.join(IA, "preflight.py"), "--spec", SPEC], cwd=d,
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertIn("PREFLIGHT: FAIL", r.stdout)

    def test_spec_passes_in_a_kit_that_has_its_preconditions(self):
        # known-answer control (2026-10-21): the first spec looked for hoops.py at the deck root and FAILED a correctly
        # set-up kit — the checker was wrong, not the kit. A preflight that cries wolf gets switched off.
        if not os.path.isfile(os.path.join(KIT, "..", "yahoo-fantasy-basketball", "scripts", "hoops.py")):
            self.skipTest("deck repo not beside the kit here")
        r = subprocess.run([sys.executable, os.path.join(IA, "preflight.py"), "--spec", SPEC], cwd=KIT,
                           capture_output=True, text=True, env={k: v for k, v in os.environ.items() if k != "DECK_REPO"})
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_spec_fails_when_the_deck_is_missing(self):
        env = dict(os.environ, DECK_REPO="/nonexistent/deck")
        r = subprocess.run([sys.executable, os.path.join(IA, "preflight.py"), "--spec", SPEC], cwd=KIT,
                           capture_output=True, text=True, env=env)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("deck repo beside the kit", r.stdout)


class AuditGates(unittest.TestCase):
    def test_audit_gates_with_and_without_replay(self):
        self.assertEqual([s["name"] for s in G.audit_gates("/x/r.md", replay=False)], ["claim receipts"])
        specs = G.audit_gates("/x/r.md", replay=True)
        self.assertEqual([s["name"] for s in specs], ["claim receipts", "deck replay"])
        cr, rp = specs
        self.assertIn("/x/r.md", cr["cmd"])
        self.assertRegex("CLAIM RECEIPTS: ADVISORY — 2 unreceipted", cr["pass_re"])
        self.assertRegex("CLAIM RECEIPTS: PASS — 1 file", cr["pass_re"])
        self.assertNotRegex("CLAIM RECEIPTS: FAIL — 1", cr["pass_re"])
        self.assertIn("--last", rp["cmd"])
        self.assertTrue(any("deck_record_" in c for c in rp["cmd"]), "replays the mornings that really produced a deck")
        self.assertEqual(rp["pass_re"], r"^REPLAY: PASS")


class Vendored(unittest.TestCase):
    LIB = os.environ.get("CORE_SKILLS") or os.path.join(KIT, "..", "claude-core-skills")

    def test_vendored_scripts_match_the_library_when_present(self):
        src = os.path.join(self.LIB, ".claude", "skills", "independent-audit", "scripts")
        if not os.path.isdir(src):
            self.skipTest("library checkout not beside the kit")
        for f in ("claim_receipts.py", "replay_gate.py", "preflight.py"):
            a = hashlib.sha256(open(os.path.join(IA, f), "rb").read()).hexdigest()
            b = hashlib.sha256(open(os.path.join(src, f), "rb").read()).hexdigest()
            self.assertEqual(a, b, f"{f} drifted from the library copy")


if __name__ == "__main__":
    unittest.main(verbosity=1)
