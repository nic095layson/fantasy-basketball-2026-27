#!/usr/bin/env python3
"""The league schedule file and league_sim.py --schedule (plan 2026-10-15 §4 B2).

data/league_schedule.json holds the owner's 17 opponents (owner message pinned in
data/source/). league_sim.py --schedule must play seat 10 against the listed opponent in
every simulated week and record that it did.

    python3 scripts/test_schedule.py
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK = os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball")
SCHED = os.path.join(KIT, "data", "league_schedule.json")
SETTINGS = os.path.join(KIT, "data", "league_settings.json")
STATE = os.path.join(DECK, "arena", "data", "states", "draft_state_100.json")


class ScheduleFile(unittest.TestCase):
    def test_matches_settings(self):
        s, st = json.load(open(SCHED)), json.load(open(SETTINGS))
        self.assertEqual(s["regular_season_weeks"], st["regular_season_weeks"]["value"])
        self.assertEqual(s["playoff_weeks"], st["playoffs"]["value"]["weeks"])
        self.assertEqual([o["week"] for o in s["owner_opponents"]], list(range(1, s["regular_season_weeks"] + 1)))

    def test_every_other_team_appears_and_never_self(self):
        s = json.load(open(SCHED))
        seats = [o["seat"] for o in s["owner_opponents"]]
        self.assertNotIn(s["owner_seat"], seats)
        self.assertEqual(set(seats), set(range(1, 13)) - {s["owner_seat"]})


class LeagueSimSchedule(unittest.TestCase):
    def test_owner_plays_the_listed_opponent_every_week(self):
        seasons = 20
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "sim.json")
            p = subprocess.run([sys.executable, "arena/mocks/league_sim.py", STATE, "v69", str(seasons), "7", out,
                                "--schedule", SCHED], cwd=DECK, capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr[-2000:])
            rec = json.load(open(out))
        sched = json.load(open(SCHED))
        weeks = sched["regular_season_weeks"]
        # 2026-10-26 (#196): the weeks already final in "played" are not simulated, so the owner's opponent is honoured
        # in the remaining weeks only
        self.assertEqual(rec["schedule"]["owner_seat"], 10)
        self.assertEqual(rec["schedule"]["honored"], seasons * (weeks - len(sched.get("played") or {})))
        self.assertEqual(rec["weeks"], weeks)


if __name__ == "__main__":
    unittest.main(verbosity=2)
