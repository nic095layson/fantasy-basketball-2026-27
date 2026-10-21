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



class SinceGuard(unittest.TestCase):
    """GAUNTLET 2026-10-21 item 7: in a persistent runner, yesterday's outlook stays in the transcript; with
    --since only today's counts, and none means a HALT, never yesterday's games-left line."""

    def setUp(self):
        import json, tempfile
        fd, self.tr = tempfile.mkstemp(suffix=".jsonl")

        def line(ts, payload):
            return json.dumps({"type": "user", "timestamp": ts, "message": {"content": [
                {"type": "tool_result", "content": [{"type": "text", "text": json.dumps(payload)}]}]}}) + "\n"
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(line("2026-10-21T12:56:00Z", outlook(oppTeamName="YESTERDAY", myLeftToPlay=30)))
            f.write(line("2026-10-22T12:56:00Z", outlook(oppTeamName="TODAY", myLeftToPlay=27)))

    def tearDown(self):
        os.remove(self.tr)

    def test_without_since_the_last_outlook_wins_as_before(self):
        self.assertEqual(ML.extract_outlook(self.tr)["oppTeamName"], "TODAY")

    def test_since_keeps_todays_outlook(self):
        self.assertEqual(ML.extract_outlook(self.tr, since="2026-10-22T12:53:00Z")["oppTeamName"], "TODAY")

    def test_since_after_every_outlook_finds_none(self):
        self.assertIsNone(ML.extract_outlook(self.tr, since="2026-10-23T12:53:00Z"))

    def test_the_cli_halts_rather_than_record_yesterday(self):
        import subprocess, tempfile
        out_dir = tempfile.mkdtemp()
        r = subprocess.run([sys.executable, os.path.join(HERE, "matchup_live.py"), "--date", "2026-10-23",
                            "--transcript", self.tr, "--since", "2026-10-23T12:53:00Z", "--out-dir", out_dir,
                            "--pin-dir", tempfile.mkdtemp()], capture_output=True, text=True)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("MATCHUP LIVE: HALT", r.stdout)
        self.assertEqual(os.listdir(out_dir), [])

if __name__ == "__main__":
    unittest.main()
