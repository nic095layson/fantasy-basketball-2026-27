#!/usr/bin/env python3
"""Red-first tests for scripts/redteam/check_constants.py (post-mortem 2026-10-19, D-PM-1/D-PM-4).

The checker must refuse what a glance accepts: a registry value that no longer matches the
live engine (drift), a live constant nobody registered, and a hand-set constant that carries
neither a sensitivity band nor an open decision id.

    python3 scripts/test_constants_registry.py
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "redteam"))
import check_constants as C  # noqa: E402


def reg(*entries):
    return {"constants": list(entries)}


GOOD = {"module": "arena", "name": "TEAM_WEEK_SHOCK", "value": 0.06, "role": "shock",
        "status": "declared_band", "record": "rt_sensitivity.json shock 0/0.12", "decision": "D-PM-1"}
LIVE = {("arena", "TEAM_WEEK_SHOCK"): 0.06}


class Drift(unittest.TestCase):
    def test_matching_registry_passes(self):
        ok, problems = C.check(reg(GOOD), LIVE)
        self.assertTrue(ok, problems)

    def test_stale_value_fails(self):
        stale = dict(GOOD, value=0.05)
        ok, problems = C.check(reg(stale), LIVE)
        self.assertFalse(ok)
        self.assertTrue(any("TEAM_WEEK_SHOCK" in p and "live" in p for p in problems), problems)

    def test_unregistered_live_constant_fails(self):
        live = dict(LIVE)
        live[("arena", "NEW_KNOB")] = 1.0
        ok, problems = C.check(reg(GOOD), live)
        self.assertFalse(ok)
        self.assertTrue(any("NEW_KNOB" in p and "not registered" in p for p in problems), problems)

    def test_registered_but_missing_live_fails(self):
        gone = dict(GOOD, name="RETIRED_KNOB")
        ok, problems = C.check(reg(GOOD, gone), LIVE)
        self.assertFalse(ok)
        self.assertTrue(any("RETIRED_KNOB" in p for p in problems), problems)

    def test_dict_values_compare_by_content(self):
        cv = {"module": "arena", "name": "CV", "value": {"PTS": 0.30, "REB": 0.35}, "role": "cv",
              "status": "declared_band", "record": "r", "decision": "d"}
        live = {("arena", "CV"): {"REB": 0.35, "PTS": 0.30}}
        self.assertTrue(C.check(reg(cv), live)[0])
        self.assertFalse(C.check(reg(cv), {("arena", "CV"): {"REB": 0.35, "PTS": 0.31}})[0])


class Status(unittest.TestCase):
    def test_uncalibrated_without_decision_fails(self):
        bare = dict(GOOD, status="uncalibrated")
        bare.pop("decision")
        ok, problems = C.check(reg(bare), LIVE)
        self.assertFalse(ok)
        self.assertTrue(any("decision" in p for p in problems), problems)

    def test_declared_band_without_record_fails(self):
        bare = dict(GOOD, record="")
        ok, problems = C.check(reg(bare), LIVE)
        self.assertFalse(ok)

    def test_unknown_status_fails(self):
        ok, problems = C.check(reg(dict(GOOD, status="fine")), LIVE)
        self.assertFalse(ok)
        self.assertTrue(any("status" in p for p in problems), problems)

    def test_measured_needs_a_record_path(self):
        ok, problems = C.check(reg(dict(GOOD, status="measured", record="")), LIVE)
        self.assertFalse(ok)


class LiveEngine(unittest.TestCase):
    """The shipped registry against the live deck (skipped when the deck is not beside the kit)."""
    def test_shipped_registry_matches_deck(self):
        if not os.path.isdir(C.DECK):
            self.skipTest("deck not present")
        live = C.read_live(C.DECK)
        ok, problems = C.check(C.load_registry(), live)
        self.assertTrue(ok, problems)
        self.assertIn(("arena", "GAMES_PER_WEEK"), live)
        self.assertIn(("hoops", "availability"), live)


if __name__ == "__main__":
    unittest.main(verbosity=2)
