#!/usr/bin/env python3
"""availability_calibration.py red-first tests (D-PM-4 option d, owner "implement fixes" 2026-10-21): realized share
of team games by injury tier, from regular-season box scores only, measured against a known answer, with an
INSUFFICIENT verdict until the sample is large enough. It changes no value."""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import availability_calibration as AC


def box(date, games, played, season_type=2):
    """games: {game_id: (team_a, team_b)}; played: [(pool_name, team, game_id, minutes)]"""
    return dict(date=date, games=[dict(espn_id=g, season_type=season_type) for g in games],
                players=[dict(pool_name=n, team=t, game=g, dnp=(m == 0), min=m) for n, t, g, m in played]
                + [dict(pool_name=None, team=a, game=g, dnp=False, min=30) for g, (a, b) in games.items()]
                + [dict(pool_name=None, team=b, game=g, dnp=False, min=30) for g, (a, b) in games.items()])


def season(n_games, plays):
    """n_games for teams AAA and BBB (they play each other); plays: {name: (team, games_played)}"""
    recs = []
    for i in range(n_games):
        g = f"g{i}"
        played = [(n, t, g, 20 if i < k else 0) for n, (t, k) in plays.items()]
        recs.append(box(f"2026-10-{20 + i:02d}", {g: ("AAA", "BBB")}, played))
    return recs


TIERS = {"Healthy One": "healthy", "Healthy Two": "healthy", "Risky": "risk", "Mildly": "mild", "Gone": "recovery"}
TEAM = {"Healthy One": "AAA", "Healthy Two": "BBB", "Risky": "AAA", "Mildly": "BBB", "Gone": "AAA"}
PLAYS = {"Healthy One": ("AAA", 16), "Healthy Two": ("BBB", 14), "Risky": ("AAA", 12), "Mildly": ("BBB", 14),
         "Gone": ("AAA", 0)}


class Calibration(unittest.TestCase):
    def test_known_answer(self):
        r = AC.calibrate(season(16, PLAYS), list(TIERS), TIERS, TEAM, min_team_games=15, min_risk=1)
        self.assertEqual(r["team_games"], {"AAA": 16, "BBB": 16})
        self.assertAlmostEqual(r["tiers"]["healthy"]["mean_share"], (16 / 16 + 14 / 16) / 2)
        self.assertAlmostEqual(r["tiers"]["risk"]["mean_share"], 12 / 16)
        self.assertAlmostEqual(r["ratio"]["risk"], 0.75 / 0.9375)
        self.assertAlmostEqual(r["ratio"]["mild"], 0.875 / 0.9375)
        self.assertEqual(r["verdict"], "MEASURED")
        self.assertEqual(r["tiers"]["recovery"]["n"], 1)
        self.assertNotIn("recovery", r["ratio"])

    def test_preseason_and_dnp_do_not_count(self):
        recs = season(16, PLAYS) + [box("2026-10-10", {"p1": ("AAA", "BBB")},
                                        [("Risky", "AAA", "p1", 30)], season_type=1)]
        r = AC.calibrate(recs, list(TIERS), TIERS, TEAM, min_team_games=15, min_risk=1)
        self.assertEqual(r["team_games"]["AAA"], 16)
        self.assertAlmostEqual(r["tiers"]["risk"]["mean_share"], 12 / 16)

    def test_insufficient_until_the_sample_is_large_enough(self):
        r = AC.calibrate(season(10, {k: (t, min(g, 10)) for k, (t, g) in PLAYS.items()}),
                         list(TIERS), TIERS, TEAM, min_team_games=15, min_risk=1)
        self.assertEqual(r["verdict"], "INSUFFICIENT")
        self.assertIn("median team games 10 < 15", r["why"])
        r = AC.calibrate(season(16, PLAYS), list(TIERS), TIERS, TEAM, min_team_games=15, min_risk=10)
        self.assertEqual(r["verdict"], "INSUFFICIENT")
        self.assertIn("1 risk-tagged with games < 10", r["why"])

    def test_no_regular_season_games(self):
        r = AC.calibrate([], list(TIERS), TIERS, TEAM, min_team_games=15, min_risk=1)
        self.assertEqual(r["verdict"], "INSUFFICIENT")
        self.assertEqual(r["team_games"], {})
        # thresholds at zero must not turn "nothing measured" into a verdict
        r = AC.calibrate([], list(TIERS), TIERS, TEAM, min_team_games=0, min_risk=0)
        self.assertEqual(r["verdict"], "INSUFFICIENT")
        self.assertIn("no realized ratio", r["why"])


if __name__ == "__main__":
    unittest.main()
