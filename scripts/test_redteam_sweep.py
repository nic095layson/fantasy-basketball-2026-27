#!/usr/bin/env python3
"""Red-first tests for scripts/redteam/sweep.py and check_bands.py (post-mortem 2026-10-19 D-PM-1; RULES.md 5, 6).

The sweep must build its variants from the registry (a declared_band constant with no band is an error, not
a silent skip), tier a shift by the post-mortem rule, and the bands check must refuse a report that does not
quote every FRAGILE band.

    python3 scripts/test_redteam_sweep.py
"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "redteam"))
import sweep as S  # noqa: E402
import check_bands as B  # noqa: E402


def registry(*entries):
    return {"constants": list(entries)}


SHOCK = {"module": "arena", "name": "TEAM_WEEK_SHOCK", "value": 0.06, "status": "declared_band",
         "band": [{"label": "no shock", "const": {"TEAM_WEEK_SHOCK": 0.0}},
                  {"label": "shock doubled", "const": {"TEAM_WEEK_SHOCK": 0.12}}]}
FIXED = {"module": "arena", "name": "WEEKS", "value": 17, "status": "settings"}


class Variants(unittest.TestCase):
    def test_variants_come_from_declared_bands_only(self):
        v = S.variants_from_registry(registry(SHOCK, FIXED))
        self.assertEqual([x["constant"] for x in v], ["arena.TEAM_WEEK_SHOCK"] * 2)
        self.assertEqual(v[0]["label"], "no shock")

    def test_declared_band_without_band_is_an_error(self):
        bare = dict(SHOCK)
        bare.pop("band")
        with self.assertRaises(ValueError):
            S.variants_from_registry(registry(bare))


class Tiers(unittest.TestCase):
    def test_tier_thresholds(self):
        self.assertEqual(S.tier(0.99), "ROBUST")
        self.assertEqual(S.tier(-1.0), "SENSITIVE")
        self.assertEqual(S.tier(1.99), "SENSITIVE")
        self.assertEqual(S.tier(2.0), "FRAGILE")
        self.assertEqual(S.tier(-3.4), "FRAGILE")

    def test_constant_tier_is_its_worst_variant(self):
        rec = S.summarize({"baseline": {"2026": 20.0, "2027": 20.0},
                           "no shock": {"2026": 23.0, "2027": 23.8},
                           "shock doubled": {"2026": 19.5, "2027": 19.7}},
                          [dict(constant="arena.TEAM_WEEK_SHOCK", label="no shock"),
                           dict(constant="arena.TEAM_WEEK_SHOCK", label="shock doubled")], ["2026", "2027"])
        c = rec["constants"]["arena.TEAM_WEEK_SHOCK"]
        self.assertEqual(c["tier"], "FRAGILE")
        self.assertEqual([v["shift_mean"] for v in c["variants"]], [3.4, -0.4])
        self.assertEqual(rec["fragile"], ["arena.TEAM_WEEK_SHOCK"])


class Bands(unittest.TestCase):
    SWEEP = {"constants": {"arena.TEAM_WEEK_SHOCK": {"tier": "FRAGILE", "variants": [
        {"label": "no shock", "shift_mean": 3.4}, {"label": "shock doubled", "shift_mean": -2.3}]},
        "arena.CV": {"tier": "ROBUST", "variants": [{"label": "x0.8", "shift_mean": 0.1}]}},
        "fragile": ["arena.TEAM_WEEK_SHOCK"]}

    def run_check(self, text):
        with tempfile.TemporaryDirectory() as d:
            r = os.path.join(d, "r.md")
            s = os.path.join(d, "s.json")
            with open(r, "w") as f:
                f.write(text)
            with open(s, "w") as f:
                json.dump(self.SWEEP, f)
            return B.check(r, s)

    def test_report_without_the_band_fails(self):
        ok, problems = self.run_check("# report\nthe title share is 21.4 percent.\n")
        self.assertFalse(ok)
        self.assertTrue(any("TEAM_WEEK_SHOCK" in p for p in problems), problems)

    def test_report_with_half_the_band_fails(self):
        ok, _ = self.run_check("TEAM_WEEK_SHOCK is FRAGILE: +3.4 without the shock.\n")
        self.assertFalse(ok)

    def test_report_quoting_the_band_passes(self):
        ok, problems = self.run_check("TEAM_WEEK_SHOCK is FRAGILE: +3.4 with no shock, -2.3 doubled.\n")
        self.assertTrue(ok, problems)

    def test_unicode_minus_is_accepted(self):
        ok, _ = self.run_check("TEAM_WEEK_SHOCK FRAGILE: +3.4 / −2.3\n")
        self.assertTrue(ok)

    def test_no_fragile_constant_passes_without_quotes(self):
        with tempfile.TemporaryDirectory() as d:
            r = os.path.join(d, "r.md")
            s = os.path.join(d, "s.json")
            with open(r, "w") as f:
                f.write("nothing here\n")
            with open(s, "w") as f:
                json.dump({"constants": {"arena.CV": {"tier": "ROBUST", "variants": []}}, "fragile": []}, f)
            ok, _ = B.check(r, s)
            self.assertTrue(ok)


class Smoke(unittest.TestCase):
    def test_sweep_runs_on_the_live_engine_at_test_size(self):
        if not os.path.isdir(S.DECK):
            self.skipTest("deck not present")
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "sweep.json")
            rec = S.run_sweep(seasons=10, seeds=(1, 2), out=out, workers=2,
                             registry=registry(SHOCK, FIXED))
            self.assertEqual(sorted(rec["variants"]), sorted(["baseline", "no shock", "shock doubled"]))
            self.assertEqual(rec["seasons"], 10)
            self.assertIn("engine_commit", rec)
            self.assertTrue(os.path.exists(out))


if __name__ == "__main__":
    unittest.main(verbosity=2)
