#!/usr/bin/env python3
"""Red-first tests for scripts/real_games.py (owner 2026-10-27, build 5 first slice): the week model on each NBA
team's real games that week instead of a flat 3.5 x availability. The engine's own weights, availability, categories
and percentage constant are imported, so the only thing that can differ is the games count — and the drift check
below proves it: at exactly 3.5 games for every team the two models agree to the last digit.

    python3 scripts/test_real_games.py
"""
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import co_gm as CG  # noqa: E402
import real_games as RG  # noqa: E402


def roster():
    P, by = CG.load_pool()
    st = json.load(open(CG.STATE, encoding="utf-8"))
    return CG.rosters(st, by)[CG.OWNER_SEAT]


class DriftCheck(unittest.TestCase):
    def test_at_three_and_a_half_games_everywhere_the_candidate_equals_the_engine(self):
        ros = roster()
        games = {p["team"]: 3.5 for p in ros}
        mu0, var0 = CG.arena.team_week_model(ros, CG.arena.SEASON_CV)
        mu1, var1 = RG.team_week_model_games(ros, CG.arena.SEASON_CV, games)
        for c in CG.CATS:
            self.assertAlmostEqual(mu1[c], mu0[c], places=9, msg=c); self.assertAlmostEqual(var1[c], var0[c], places=9, msg=c)
        self.assertEqual(mu1.keys(), mu0.keys())

    def test_a_team_with_four_games_scales_its_counting_means_by_four_over_three_and_a_half(self):
        ros = roster()
        one = [p for p in ros if p["team"] == ros[0]["team"]]       # the owner's players on one NBA team
        mu0, _ = CG.arena.team_week_model(one, CG.arena.SEASON_CV)
        mu4, _ = RG.team_week_model_games(one, CG.arena.SEASON_CV, {one[0]["team"]: 4})
        mu3, _ = RG.team_week_model_games(one, CG.arena.SEASON_CV, {one[0]["team"]: 3})
        for c in ("PTS", "REB", "AST"):
            self.assertAlmostEqual(mu4[c] / mu0[c], 4 / 3.5, places=9); self.assertAlmostEqual(mu3[c] / mu0[c], 3 / 3.5, places=9)

    def test_a_team_missing_from_the_schedule_gets_the_flat_count_and_is_named(self):
        ros = roster()
        mu, var, unscheduled = RG.team_week_model_games(ros, CG.arena.SEASON_CV, {}, report=True)
        mu0, _ = CG.arena.team_week_model(ros, CG.arena.SEASON_CV)
        self.assertAlmostEqual(mu["PTS"], mu0["PTS"], places=9)
        self.assertEqual(sorted(unscheduled), sorted({p["team"] for p in ros}))


class WeekGames(unittest.TestCase):
    def test_each_nba_teams_games_in_the_fantasy_week_window(self):
        g = RG.week_games(3)                      # 2026-11-02 .. 2026-11-08 from report/schedule/games-2026-27.csv
        self.assertEqual(len(g), 30)
        self.assertTrue(all(2 <= n <= 5 for n in g.values()), g)
        self.assertEqual(sum(g.values()), 2 * sum(1 for d, v, h in CG.load_games() if "2026-11-02" <= d <= "2026-11-08"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
