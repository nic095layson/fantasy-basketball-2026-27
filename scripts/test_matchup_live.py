#!/usr/bin/env python3
"""Red-first tests for matchup_live.py: neutral facts only — FantasyBot's verdict never leaves the pin."""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import matchup_live as ML  # noqa: E402


def outlook(**kw):
    base = {"linked": True, "leagueName": ML.LEAGUE, "week": 1, "verdict": "Projected 2-7-0 (7% to win)",
            "myLeftToPlay": 30, "oppLeftToPlay": 37, "gamesInProgress": False, "final": False, "liveScoring": True,
            "myTeamName": "ME", "oppTeamName": "THEM",
            "myStarters": [{"name": "A", "team": "BOS", "gamesLeft": 2, "gameState": "pre"}],
            "oppStarters": [{"name": "B", "team": "DET", "gamesLeft": 3, "gameState": "pre"}]}
    base.update(kw)
    return base


class Record(unittest.TestCase):
    def test_neutral_facts_come_through(self):
        r = ML.record(outlook())
        self.assertEqual(r["my_left_to_play"], 30)
        self.assertEqual(r["opp_left_to_play"], 37)
        self.assertEqual(r["my_starters"][0]["games_left"], 2)

    def test_the_fantasybot_verdict_never_reaches_the_record(self):
        r = ML.record(outlook())
        import json
        self.assertNotIn("7%", json.dumps(r))
        self.assertNotIn("verdict", json.dumps(r).lower())

    def test_a_wrong_league_halts(self):
        with self.assertRaises(ML.PullError):
            ML.record(outlook(leagueName="OTHER"))

    def test_todays_transcript_yields_todays_outlook(self):
        o = ML.extract_outlook(ML.newest_transcript())
        self.assertIsNotNone(o)
        self.assertEqual(o.get("oppTeamName"), "KEVIN ELEVEN DOUBLES")


if __name__ == "__main__":
    unittest.main()
