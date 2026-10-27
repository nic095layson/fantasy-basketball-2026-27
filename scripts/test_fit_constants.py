#!/usr/bin/env python3
"""Red-first tests for scripts/fit_constants.py (owner 2026-10-27, build 3): the two FRAGILE hand-set constants
measured from the finished weeks — the shared weekly games shock (TEAM_WEEK_SHOCK) and the availability tiers
(weekly_availability) — proposed with their error, never applied. Expected figures are hand-derived or recovered
from synthetic data with a known truth.

    python3 scripts/test_fit_constants.py
"""
import json
import math
import os
import random
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fit_constants as FC  # noqa: E402

CATS = ("3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO")


def synthetic(n, shock, seed):
    """n team-weeks: per cat an expected mu and model var (no shock), an actual drawn as mu*(1+s)+noise, s~N(0,shock)."""
    rng = random.Random(seed); rows = []
    mu = {"3PTM": 60, "PTS": 550, "REB": 200, "AST": 125, "ST": 35, "BLK": 22, "TO": 75}
    cv = {"3PTM": 0.12, "PTS": 0.07, "REB": 0.08, "AST": 0.10, "ST": 0.18, "BLK": 0.22, "TO": 0.12}
    for _ in range(n):
        s = rng.gauss(0, shock) if shock else 0.0
        rows.append({c: dict(actual=mu[c] * (1 + s) + rng.gauss(0, cv[c] * mu[c]), mu=mu[c], var=(cv[c] * mu[c]) ** 2) for c in CATS})
    return rows


class Shock(unittest.TestCase):
    def test_a_known_shock_is_recovered_within_its_error(self):
        r = FC.shock_estimate(synthetic(1200, 0.06, 1), boots=200, seed=1)
        self.assertIsNotNone(r["shock"])
        self.assertLess(abs(r["shock"] - 0.06), 0.012)
        self.assertLess(abs(r["shock"] - 0.06), 3 * r["se"] + 0.004)
        self.assertEqual(r["n"], 1200)

    def test_no_shock_reports_none_detectable_not_a_number(self):
        r = FC.shock_estimate(synthetic(1200, 0.0, 2), boots=200, seed=2)
        self.assertIsNone(r["shock"]); self.assertIn("no shock detectable", r["note"])

    def test_a_season_sized_sample_recovers_the_live_value_roughly(self):
        # 144 team-weeks (12 teams x 12 weeks): the error is wide, but 0.06 is inside two SE of the estimate
        r = FC.shock_estimate(synthetic(144, 0.06, 3), boots=300, seed=3)
        self.assertTrue(r["shock"] is None or abs(r["shock"] - 0.06) < 2 * r["se"] + 0.01, r)

    def test_the_factor_is_the_mean_ratio_over_counting_cats(self):
        row = {c: dict(actual=110.0, mu=100.0, var=25.0) for c in CATS}
        self.assertAlmostEqual(FC.factor(row), 1.10)
        self.assertAlmostEqual(FC.model_term(row), (25.0 / 100.0 ** 2) / 7)   # mean of var/mu^2 over 7 cats, / 7


class Availability(unittest.TestCase):
    def test_pooled_shares_with_binomial_error_and_the_live_value_inside_or_outside_2se(self):
        weeks = [{"0.88": dict(assumed=0.88, played=670, team_games=809), "0.75": dict(assumed=0.75, played=55, team_games=96)},
                 {"0.88": dict(assumed=0.88, played=700, team_games=800), "0.75": dict(assumed=0.75, played=60, team_games=100)}]
        a = FC.availability_pool(weeks)
        p = (670 + 700) / (809 + 800)
        self.assertAlmostEqual(a["0.88"]["measured"], p); self.assertEqual(a["0.88"]["n"], 1609)
        self.assertAlmostEqual(a["0.88"]["se"], math.sqrt(p * (1 - p) / 1609))
        self.assertFalse(a["0.88"]["live_within_2se"])          # 0.88 is far above ~0.85 at n=1609
        q = (55 + 60) / 196
        self.assertAlmostEqual(a["0.75"]["measured"], q)
        self.assertFalse(a["0.75"]["live_within_2se"])          # 0.75 vs ~0.59 at n=196


class Gate(unittest.TestCase):
    def test_fewer_than_four_weeks_is_reported_not_proposed(self):
        self.assertEqual(FC.proposal_status(1), "too few weeks to propose (1 of 4)")
        self.assertEqual(FC.proposal_status(4), "proposal")

    def test_the_record_is_append_only(self):
        d = tempfile.mkdtemp(); p = os.path.join(d, "fit_week1.json")
        FC.write_fit(p, dict(week=1))
        with self.assertRaises(FC.FitError):
            FC.write_fit(p, dict(week=1))


class BoardComparison(unittest.TestCase):
    """Owner 2026-10-27 ("Fold into the week-4 fit"): the realized risk/healthy and mild/healthy ratios, by the frozen
    preseason tag, beside the same ratios on the deck board, the simulator and the kit board; proposals only."""
    WEEKS = [{"0.88": dict(assumed=0.88, played=670, team_games=809), "0.75": dict(assumed=0.75, played=55, team_games=96),
              "0.79": dict(assumed=0.79, played=4, team_games=5)}]
    INSTR = {"risk": dict(deck=0.78, simulator=0.8523, kit=0.95), "mild": dict(deck=0.85, simulator=0.8977, kit=None)}

    def test_the_ratio_and_its_delta_method_error(self):
        a = FC.availability_pool(self.WEEKS)
        c = FC.board_comparison(a, self.INSTR, keys=dict(healthy="0.88", risk="0.75", mild="0.79"))
        p, q = 670 / 809, 55 / 96
        r = q / p
        se = r * math.sqrt((math.sqrt(q * (1 - q) / 96) / q) ** 2 + (math.sqrt(p * (1 - p) / 809) / p) ** 2)
        self.assertAlmostEqual(c["risk"]["measured"], r); self.assertAlmostEqual(c["risk"]["se"], se)
        self.assertEqual(c["risk"]["deck"], 0.78)
        # by hand: r = 0.5729/0.8282 = 0.692, SE 0.062, 2 SE 0.124: the deck's 0.78 is 0.088 away (inside),
        # the simulator's 0.852 is 0.160 away (outside)
        self.assertTrue(c["risk"]["within_2se"]["deck"]); self.assertFalse(c["risk"]["within_2se"]["simulator"])
        self.assertIsNone(c["mild"]["within_2se"]["kit"])      # no kit number: no verdict, never a guess

    def test_a_missing_tier_is_named_not_dropped(self):
        a = FC.availability_pool([{"0.88": dict(assumed=0.88, played=670, team_games=809)}])
        c = FC.board_comparison(a, self.INSTR, keys=dict(healthy="0.88", risk="0.75", mild="0.79"))
        self.assertIsNone(c["risk"]["measured"]); self.assertIn("no risk", c["risk"]["note"])

    def test_the_instruments_are_read_from_the_engines(self):
        i = FC.board_instruments()
        self.assertEqual(i["risk"]["deck"], 0.78); self.assertEqual(i["mild"]["deck"], 0.85)
        self.assertAlmostEqual(i["risk"]["simulator"], round(0.75 / 0.88, 4))
        self.assertIn("kit", i["risk"])

    def test_the_weekly_record_carries_the_comparison(self):
        d = tempfile.mkdtemp(); acc = os.path.join(d, "accuracy.json")
        json.dump({"weeks": {"1": {"availability": self.WEEKS[0]}}}, open(acc, "w"))
        r = FC.run(1, weeks_dir=d, snapshots=d, accuracy=acc, out_dir=os.path.join(d, "fits"), boots=10)
        self.assertIn("risk", r["board_comparison"])
        self.assertIn("board comparison", open(os.path.join(d, "fits.md")).read())


if __name__ == "__main__":
    unittest.main(verbosity=2)
