#!/usr/bin/env python3
"""Red-first tests for scripts/league_pairings.py (owner 2026-10-26, "full pairings + results so far"): the league's
real schedule for all 12 teams, compiled from the pinned Flaim matchup responses, and the weeks already final,
compiled from data/weeks/week_N.json, both into data/league_schedule.json for the deck's season simulator.
Every expected value below is hand-built from the fixture, not from the code under test.

    python3 scripts/test_league_pairings.py
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import league_pairings as LP  # noqa: E402

NAMES = {"1": "Alpha", "2": "Bravo", "3": "Charlie", "4": "Delta"}
SEATS = {"Alpha": 4, "Bravo": 1, "Charlie": 3, "Delta": 2}          # team_id -> seat is NOT the identity


def resp(week, pairs, status="upcoming"):
    """A Flaim get_matchups response body for one week: pairs = [(home_id, away_id)]."""
    return dict(leagueKey="478.l.36464", matchupWeek=week, scoringType="categories",
                matchups=[dict(matchupId=i + 1, week=week, status=status,
                               home=dict(teamId=h, teamName=NAMES[h]), away=dict(teamId=a, teamName=NAMES[a]))
                          for i, (h, a) in enumerate(pairs)])


def week_file(week, scores):
    """A scoreboard_intake week_N.json: teams[name] = {seat, yahoo_score}."""
    return dict(week=week, teams={n: dict(seat=SEATS[n], opponent="x", line={}, yahoo_score=dict(zip(("wins", "losses", "ties"), s)))
                                  for n, s in scores.items()})


class Compile(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.pins = os.path.join(self.d, "pins"); os.makedirs(self.pins)
        json.dump(resp(1, [("1", "2"), ("3", "4")], "final"), open(os.path.join(self.pins, "matchups_week01.json"), "w"))
        json.dump(resp(2, [("1", "3"), ("2", "4")]), open(os.path.join(self.pins, "matchups_week02.json"), "w"))
        self.weeks = os.path.join(self.d, "weeks"); os.makedirs(self.weeks)
        json.dump(week_file(1, {"Alpha": (6, 3, 0), "Bravo": (3, 6, 0), "Charlie": (4, 4, 1), "Delta": (4, 4, 1)}),
                  open(os.path.join(self.weeks, "week_1.json"), "w"))
        self.state = dict(teams=[dict(name=n, seat=s) for n, s in SEATS.items()])
        self.sched = dict(owner_seat=1, regular_season_weeks=2, playoff_weeks=[3],
                          owner_opponents=[dict(week=1, seat=4), dict(week=2, seat=2)])

    def test_a_team_renamed_since_the_pins_is_matched_by_its_yahoo_team_key(self):
        # owner 2026-10-29 ("Key on Yahoo team key"): the pins carry the name of the day they were pinned; the key does not change
        for f in os.listdir(self.pins):
            r = json.load(open(os.path.join(self.pins, f)))
            for m in r["matchups"]:
                for side in (m["home"], m["away"]):
                    side["teamKey"] = f"478.l.36464.t.{side['teamId']}"
            json.dump(r, open(os.path.join(self.pins, f), "w"))
        state = dict(teams=[dict(name=("Alpha Renamed" if n == "Alpha" else n), seat=s) for n, s in SEATS.items()])
        keys = {f"478.l.36464.t.{i}": ("Alpha Renamed" if n == "Alpha" else n) for i, n in NAMES.items()}
        with self.assertRaises(LP.PairingsError):
            LP.compile(self.sched, self.pins, self.weeks, state)
        out = LP.compile(self.sched, self.pins, self.weeks, state, keys=keys)
        self.assertEqual(out["pairings"], {"1": [[4, 1], [3, 2]], "2": [[4, 3], [1, 2]]})

    def test_the_key_to_name_map_comes_from_the_newest_pull(self):
        d = tempfile.mkdtemp()
        json.dump(dict(rosters={"478.l.36464.t.1": dict(teamKey="478.l.36464.t.1", teamName="Old")}), open(os.path.join(d, "pull_2026-10-28.json"), "w"))
        json.dump(dict(rosters={"478.l.36464.t.1": dict(teamKey="478.l.36464.t.1", teamName="New")}), open(os.path.join(d, "pull_2026-10-29.json"), "w"))
        self.assertEqual(LP.names_by_key(d), {"478.l.36464.t.1": "New"})
        self.assertEqual(LP.names_by_key(tempfile.mkdtemp()), {})

    def test_pairings_are_seat_pairs_per_week_from_the_pins(self):
        out = LP.compile(self.sched, self.pins, self.weeks, self.state)
        # week 1: Alpha(4)-Bravo(1), Charlie(3)-Delta(2); week 2: Alpha(4)-Charlie(3), Bravo(1)-Delta(2)
        self.assertEqual(out["pairings"], {"1": [[4, 1], [3, 2]], "2": [[4, 3], [1, 2]]})
        self.assertEqual(out["pairings_source"]["weeks"], 2)

    def test_the_owners_listed_opponents_are_checked_against_yahoo(self):
        out = LP.compile(self.sched, self.pins, self.weeks, self.state)
        self.assertEqual(out["owner_opponents_check"], "match")
        bad = dict(self.sched, owner_opponents=[dict(week=1, seat=3), dict(week=2, seat=2)])
        with self.assertRaises(LP.PairingsError):                   # a listed opponent Yahoo contradicts halts, never silently wins
            LP.compile(bad, self.pins, self.weeks, self.state)

    def test_played_weeks_carry_each_seats_category_record(self):
        out = LP.compile(self.sched, self.pins, self.weeks, self.state)
        self.assertEqual(out["played"], {"1": {"4": [6, 3, 0], "1": [3, 6, 0], "3": [4, 4, 1], "2": [4, 4, 1]}})

    def test_a_week_with_a_pairing_of_fewer_than_all_teams_halts(self):
        json.dump(resp(2, [("1", "3")]), open(os.path.join(self.pins, "matchups_week02.json"), "w"))
        with self.assertRaises(LP.PairingsError):
            LP.compile(self.sched, self.pins, self.weeks, self.state)

    def test_cli_rewrites_the_schedule_file_keeping_its_other_keys(self):
        sp = os.path.join(self.d, "league_schedule.json"); json.dump(self.sched, open(sp, "w"))
        st = os.path.join(self.d, "state.json"); json.dump(self.state, open(st, "w"))
        p = subprocess.run([sys.executable, os.path.join(HERE, "league_pairings.py"), "--schedule", sp, "--pins", self.pins,
                            "--weeks", self.weeks, "--state", st, "--ledger", os.path.join(self.d, "ledger.jsonl")], capture_output=True, text=True)
        self.assertIn("LEAGUE PAIRINGS: PASS", p.stdout, p.stdout + p.stderr)
        self.assertIn('"name": "league pairings"', open(os.path.join(self.d, "ledger.jsonl")).read())   # the ledger row is written
        s = json.load(open(sp))
        self.assertEqual(s["owner_seat"], 1); self.assertEqual(len(s["owner_opponents"]), 2)
        self.assertEqual(list(s["pairings"]), ["1", "2"]); self.assertEqual(list(s["played"]), ["1"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
