#!/usr/bin/env python3
"""Red-first tests for scripts/minutes_line.py (owner 2026-10-27, build 2): a candidate season line, the live blend
scaled per player by a recency-weighted minutes forecast over his blended season minutes. Percentages untouched;
counting stats and attempts scaled. Every expected figure is worked by hand from the fixture.

    python3 scripts/test_minutes_line.py
"""
import csv
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import minutes_line as ML  # noqa: E402


class Forecast(unittest.TestCase):
    def test_no_games_is_the_preseason_minutes(self):
        self.assertAlmostEqual(ML.forecast_minutes([], 30.0, half_life=5, prior_games=10), 30.0)

    def test_recent_games_weigh_more_than_old_ones(self):
        # weights 0.5^(age/half_life): ages 2,1,0 at half-life 1 -> 0.25, 0.5, 1.0; prior 10 games at 30
        mins = [20, 20, 40]
        w = [0.25, 0.5, 1.0]
        recent = sum(m * x for m, x in zip(mins, w)) / sum(w)      # (5 + 10 + 40) / 1.75 = 31.428...
        n_eff = sum(w)                                             # 1.75 effective games
        expect = (10 * 30.0 + n_eff * recent) / (10 + n_eff)
        self.assertAlmostEqual(ML.forecast_minutes(mins, 30.0, half_life=1, prior_games=10), expect)

    def test_no_preseason_minutes_returns_none(self):
        self.assertIsNone(ML.forecast_minutes([30, 32], None, half_life=5, prior_games=10))


class Scale(unittest.TestCase):
    ROW = dict(player="A", team="BOS", pos="PG", fg_pct="0.450", fga="12.0", ft_pct="0.800", fta="4.0", tpm="2.0", pts="15.0",
               reb="4.0", ast="6.0", stl="1.0", blk="0.5", tov="2.0", note="x")

    def test_counting_and_attempts_scale_and_percentages_do_not(self):
        out = ML.scale_row(self.ROW, 1.25)
        self.assertEqual((out["fg_pct"], out["ft_pct"]), ("0.450", "0.800"))
        self.assertEqual((out["pts"], out["reb"], out["ast"], out["fga"], out["fta"], out["tpm"]), ("18.8", "5.0", "7.5", "15.0", "5.0", "2.5"))
        self.assertEqual(out["note"], "x")

    def test_ratio_one_leaves_the_row_byte_identical(self):
        self.assertEqual(ML.scale_row(self.ROW, 1.0), self.ROW)


class Build(unittest.TestCase):
    def test_the_candidate_pool_scales_each_player_by_his_own_ratio_and_names_the_unscaled(self):
        d = tempfile.mkdtemp()
        pool = os.path.join(d, "pool_season.csv"); kit = os.path.join(d, "projections_season.csv")
        with open(pool, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(Scale.ROW)); w.writeheader()
            w.writerow(Scale.ROW); w.writerow(dict(Scale.ROW, player="B")); w.writerow(dict(Scale.ROW, player="C"))
        with open(kit, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["name", "team", "pos", "gp", "mpg"]); w.writeheader()
            w.writerow(dict(name="A", team="BOS", pos="PG", gp="70", mpg="30.0"))
            w.writerow(dict(name="B", team="BOS", pos="PG", gp="70", mpg="30.0"))
            w.writerow(dict(name="C", team="BOS", pos="PG", gp="70", mpg=""))             # no preseason minutes
        minutes = {"A": [36, 36, 36, 36], "B": []}                                      # C: no games either
        rec = ML.build(pool, kit, minutes, half_life=5, prior_games=3, stats_prior_games=12)
        a = next(r for r in rec["rows"] if r["player"] == "A"); b = next(r for r in rec["rows"] if r["player"] == "B")
        c = next(r for r in rec["rows"] if r["player"] == "C")
        self.assertGreater(float(a["pts"]), 15.0)                 # four 36-minute games over a 30-minute prior: up
        self.assertEqual(b["pts"], "15.0"); self.assertEqual(c["pts"], "15.0")
        self.assertEqual(rec["unscaled"], ["C"])
        self.assertEqual(rec["ratios"]["B"], 1.0)
        # A by hand: implicit minutes at the blend's prior (12) = (12*30 + 4*36)/(12+4) = 31.5;
        # forecast at the minutes prior (3) = (3*30 + n_eff*36)/(3+n_eff), n_eff = sum of 0.5**(age/5) for ages 3,2,1,0
        w = [0.5 ** (age / 5) for age in (3, 2, 1, 0)]; n_eff = sum(w)
        fc = (3 * 30 + n_eff * 36) / (3 + n_eff); self.assertAlmostEqual(rec["ratios"]["A"], fc / 31.5, places=9)
        self.assertGreater(rec["ratios"]["A"], 1.04)        # the minutes prior trusts four 36s sooner than the stats prior does

    def test_one_prior_in_both_places_would_grade_the_blend_against_itself(self):
        # the flaw the red test caught 2026-10-27: same prior top and bottom -> ratio ~1 whatever the games say
        self.assertLess(abs(ML.forecast_minutes([36] * 4, 30.0, half_life=5, prior_games=12) / ML.implicit_minutes([36] * 4, 30.0, 12) - 1), 0.02)


if __name__ == "__main__":
    unittest.main(verbosity=2)
