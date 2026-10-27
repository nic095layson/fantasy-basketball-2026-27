#!/usr/bin/env python3
"""Red-first tests for scripts/accuracy_week.py (owner 2026-10-27, "Weekly accuracy card ... build all four parts"):
each finished week graded on the player lines, the availability tiers, the owner's forecasts and every matchup's
pre-week forecast, appended to report/accuracy.json. Every expected figure is worked by hand from the fixture.

    python3 scripts/test_accuracy_week.py
"""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import accuracy_week as AW  # noqa: E402


def box(pts, reb=0, ast=0, stl=0, blk=0, tpm=0, tov=0, fgm=0, fga=0, ftm=0, fta=0, team="AAA", game="g"):
    return dict(pts=pts, reb=reb, ast=ast, stl=stl, blk=blk, tpm=tpm, tov=tov, fgm=fgm, fga=fga, ftm=ftm, fta=fta, team=team, game=game)


def line(pts, fg=0.5, fga=10.0, ft=0.8, fta=2.0, **k):
    d = dict(pts=pts, reb=0.0, ast=0.0, stl=0.0, blk=0.0, tpm=0.0, tov=0.0, fg_pct=fg, fga=fga, ft_pct=ft, fta=fta)
    d.update(k); return d


class Lines(unittest.TestCase):
    def test_bias_error_and_ranking_per_category(self):
        lines = {"A": line(20), "B": line(10), "C": line(5)}
        games = {"A": [box(18), box(22)], "B": [box(8), box(8)], "C": [box(6), box(4)], "D": [box(9), box(9)]}  # D: no line
        g = AW.grade_lines(lines, games, min_games=2)
        p = g["cats"]["pts"]
        self.assertEqual(g["players"], 3)
        self.assertAlmostEqual(p["proj"], 35 / 3); self.assertAlmostEqual(p["actual"], 33 / 3)
        self.assertAlmostEqual(p["bias_pct"], 100 * (35 / 3 - 33 / 3) / (33 / 3))
        self.assertAlmostEqual(p["mae"], (0 + 2 + 0) / 3)
        self.assertAlmostEqual(p["rank_corr"], 1.0)

    def test_one_game_players_are_left_out(self):
        g = AW.grade_lines({"A": line(20), "B": line(10)}, {"A": [box(20)], "B": [box(9), box(11)]}, min_games=2)
        self.assertEqual(g["players"], 1)

    def test_percentages_are_pooled_makes_over_attempts(self):
        lines = {"A": line(10, fg=0.5, fga=10.0), "B": line(10, fg=0.4, fga=30.0)}
        games = {"A": [box(10, fgm=6, fga=10), box(10, fgm=4, fga=10)], "B": [box(10, fgm=12, fga=30), box(10, fgm=12, fga=30)]}
        f = AW.grade_lines(lines, games, min_games=2)["pct"]["fg_pct"]
        self.assertAlmostEqual(f["proj"], (0.5 * 10 + 0.4 * 30) / 40)
        self.assertAlmostEqual(f["actual"], (6 + 4 + 12 + 12) / (10 + 10 + 30 + 30))
        self.assertEqual(f["attempts"], 80)


class Availability(unittest.TestCase):
    def test_share_of_team_games_played_by_assumed_tier(self):
        tier = {"A": 0.88, "B": 0.88, "C": 0.75, "D": 0.0}
        team = {"A": "X", "B": "Y", "C": "X", "D": "Y"}
        played = {"A": 3, "B": 2, "C": 1}
        team_games = {"X": 3, "Y": 4}
        a = AW.grade_availability(tier, team, played, team_games)
        self.assertEqual(a["0.88"], dict(assumed=0.88, played=5, team_games=7, share=5 / 7))
        self.assertEqual(a["0.75"], dict(assumed=0.75, played=1, team_games=3, share=1 / 3))
        self.assertEqual(a["0.00"]["played"], 0)


class Matchups(unittest.TestCase):
    def week(self):
        t = {}
        for a, b, wa in ((1, 2, 6), (3, 4, 3)):
            t[f"T{a}"] = dict(seat=a, opponent=f"T{b}", yahoo_score=dict(wins=wa, losses=9 - wa, ties=0))
            t[f"T{b}"] = dict(seat=b, opponent=f"T{a}", yahoo_score=dict(wins=9 - wa, losses=wa, ties=0))
        return {"week": 1, "teams": t}

    def test_every_forecast_matchup_is_scored_from_the_lower_seats_side(self):
        fc = {"pairs": [dict(a=1, b=2, p_win=0.8, exp_cats=5.5), dict(a=3, b=4, p_win=0.7, exp_cats=5.2)]}
        m = AW.grade_matchups(fc, self.week())
        self.assertEqual(m["n"], 2)
        self.assertAlmostEqual(m["brier"], ((0.8 - 1) ** 2 + (0.7 - 0) ** 2) / 2)
        self.assertEqual([r["won"] for r in m["rows"]], [1, 0])

    def test_no_forecast_recorded_says_so(self):
        self.assertEqual(AW.grade_matchups(None, self.week()), dict(n=0, note="no pre-week forecast recorded for this week"))


class RealGamesColumn(unittest.TestCase):
    """Owner 2026-10-27 (build 5, first slice): the real-games forecast is graded beside the flat one, by the same rule."""
    def test_both_forecasts_are_graded_from_their_own_ledgers(self):
        import tempfile
        d = tempfile.mkdtemp()
        wk = Matchups().week()
        flat = {"weeks": {"1": {"pairs": [dict(a=1, b=2, p_win=0.8, exp_cats=5.5)]}}}
        real = {"weeks": {"1": {"pairs": [dict(a=1, b=2, p_win=0.9, exp_cats=5.7)]}}}
        json.dump(flat, open(os.path.join(d, "calibration_league.json"), "w")); json.dump(real, open(os.path.join(d, "calibration_league_real.json"), "w"))
        g = AW.grade_matchup_ledgers(1, wk, os.path.join(d, "calibration_league.json"), os.path.join(d, "calibration_league_real.json"))
        self.assertAlmostEqual(g["matchups"]["brier"], (0.8 - 1) ** 2); self.assertAlmostEqual(g["matchups_real"]["brier"], (0.9 - 1) ** 2)

    def test_a_missing_real_ledger_is_named(self):
        import tempfile
        d = tempfile.mkdtemp(); wk = Matchups().week()
        g = AW.grade_matchup_ledgers(1, wk, os.path.join(d, "none.json"), os.path.join(d, "none_real.json"))
        self.assertEqual(g["matchups"]["n"], 0); self.assertEqual(g["matchups_real"]["n"], 0)

class Record(unittest.TestCase):
    def test_a_week_is_appended_once_and_never_rewritten(self):
        p = os.path.join(tempfile.mkdtemp(), "accuracy.json")
        AW.append(p, 1, {"lines": {}})
        self.assertIn("1", json.load(open(p))["weeks"])
        with self.assertRaises(AW.AccuracyError):
            AW.append(p, 1, {"lines": {"x": 1}})


class Snapshots(unittest.TestCase):
    """Owner 2026-10-27 (build 2): the week's in-season snapshot and the minutes-trend candidate snapshot are graded
    side by side; a missing file is named, never substituted."""
    def setUp(self):
        import csv, tempfile
        self.d = tempfile.mkdtemp()
        for name, pts in (("lines_week3.csv", "10.0"), ("lines_week3_mt.csv", "12.0")):
            with open(os.path.join(self.d, name), "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=["player", "pts", "reb", "ast", "stl", "blk", "tpm", "tov", "fg_pct", "fga", "ft_pct", "fta"])
                w.writeheader(); w.writerow(dict(player="A", pts=pts, reb="0", ast="0", stl="0", blk="0", tpm="0", tov="0", fg_pct="0.5", fga="10", ft_pct="0.8", fta="2"))
        self.games = {"A": [box(12), box(12)]}

    def test_both_snapshots_are_graded(self):
        g = AW.grade_snapshots(3, self.games, self.d)
        self.assertAlmostEqual(g["in_season"]["cats"]["pts"]["mae"], 2.0)
        self.assertAlmostEqual(g["candidate_minutes"]["cats"]["pts"]["mae"], 0.0)

    def test_a_missing_candidate_is_named(self):
        os.remove(os.path.join(self.d, "lines_week3_mt.csv"))
        g = AW.grade_snapshots(3, self.games, self.d)
        self.assertIn("note", g["candidate_minutes"]); self.assertEqual(g["in_season"]["players"], 1)

class RealWeekOne(unittest.TestCase):
    """The back-fill reproduces the 2026-10-27 audit (preseason lines, players with 2+ games, Oct 20-25)."""
    def test_week_one_matches_the_audit(self):
        actuals = os.environ.get("ACCURACY_ACTUALS")
        if not actuals or not os.path.isdir(actuals):
            self.skipTest("set ACCURACY_ACTUALS to the records branch's data/actuals")
        g = AW.grade_week_lines(1, actuals, AW.FROZEN)
        self.assertEqual(g["players"], 261)
        self.assertAlmostEqual(g["cats"]["pts"]["proj"], 13.50, places=2)
        self.assertAlmostEqual(g["cats"]["pts"]["actual"], 11.95, places=2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
