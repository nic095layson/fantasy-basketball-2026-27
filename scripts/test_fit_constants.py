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


if __name__ == "__main__":
    unittest.main(verbosity=2)
