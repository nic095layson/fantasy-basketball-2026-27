#!/usr/bin/env python3
"""Red-first tests for scripts/scoreboard_intake.py (in-season tool, Council 2026-10-19 decision 3: the league
scoreboard with all six matchups' nine category totals, one CSV per week; the owner's cats won go to the ledger,
every team-week's totals go to the calibration dataset for D-PM-1).

    python3 scripts/test_scoreboard_intake.py
"""
import csv
import json
import subprocess
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scoreboard_intake as SI  # noqa: E402

TEAMS = [f"Team {i}" for i in range(1, 13)]
STATE = {"teams": [{"name": t, "seat": i + 1} for i, t in enumerate(TEAMS)]}
CATS = ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]


def rows(week=1, owner_vals=None, opp_vals=None):
    out = []
    for k in range(6):
        a, b = TEAMS[2 * k], TEAMS[2 * k + 1]
        va = dict(zip(CATS, [0.480, 0.800, 40, 600, 220, 130, 35, 25, 60]))
        vb = dict(zip(CATS, [0.470, 0.780, 38, 590, 230, 120, 30, 28, 70]))
        if k == 4:  # Team 9 vs Team 10 (the owner's seat 10)
            if owner_vals: vb = dict(zip(CATS, owner_vals))
            if opp_vals: va = dict(zip(CATS, opp_vals))
        out.append(dict(week=week, team=a, opponent=b, **va)); out.append(dict(week=week, team=b, opponent=a, **vb))
    return out


def write_csv(path, rs):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["week", "team", "opponent"] + CATS); w.writeheader(); w.writerows(rs)


class Parse(unittest.TestCase):
    def test_twelve_rows_six_matchups_resolve_to_seats(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "w1.csv"); write_csv(p, rows())
            wk = SI.parse(p, STATE)
            self.assertEqual(wk["week"], 1); self.assertEqual(len(wk["teams"]), 12); self.assertEqual(len(wk["matchups"]), 6)
            self.assertEqual(wk["teams"]["Team 10"]["seat"], 10)

    def test_unknown_team_name_halts(self):
        with tempfile.TemporaryDirectory() as d:
            rs = rows(); rs[0]["team"] = "Mystery Squad"; rs[1]["opponent"] = "Mystery Squad"
            p = os.path.join(d, "w1.csv"); write_csv(p, rs)
            with self.assertRaises(SI.IntakeError):
                SI.parse(p, STATE)

    def test_missing_team_or_bad_number_halts(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "w1.csv"); write_csv(p, rows()[:11])
            with self.assertRaises(SI.IntakeError):
                SI.parse(p, STATE)
            rs = rows(); rs[3]["PTS"] = "n/a"; write_csv(p, rs)
            with self.assertRaises(SI.IntakeError):
                SI.parse(p, STATE)


class Score(unittest.TestCase):
    def test_owner_cats_won_with_turnovers_reversed_and_ties_named(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "w1.csv")
            write_csv(p, rows(owner_vals=[0.500, 0.700, 45, 650, 200, 140, 30, 25, 50], opp_vals=[0.480, 0.800, 40, 600, 220, 130, 30, 20, 60]))
            wk = SI.parse(p, STATE); res = SI.owner_result(wk, owner_seat=10)
            self.assertEqual(res["won"], ["FG%", "3PTM", "PTS", "AST", "BLK", "TO"])
            self.assertEqual(res["lost"], ["FT%", "REB"]); self.assertEqual(res["tied"], ["ST"])
            self.assertEqual(res["opponent"], "Team 9")


class Dataset(unittest.TestCase):
    def test_team_weeks_append_is_idempotent_per_week(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "w1.csv"); write_csv(p, rows()); wk = SI.parse(p, STATE)
            ds = os.path.join(d, "team_weeks.csv")
            SI.append_team_weeks(wk, ds); SI.append_team_weeks(wk, ds)
            with open(ds) as f:
                self.assertEqual(len(list(csv.DictReader(f))), 12)

class FromPull(unittest.TestCase):
    """Owner 2026-10-23 (Build 1): a finished week's six matchups come from the Yahoo pull, not a hand-filled CSV."""
    def setUp(self):
        import test_league_table as TLT
        self.d = tempfile.mkdtemp()
        self.state = os.path.join(self.d, "state.json"); json.dump(TLT.STATE, open(self.state, "w"))
        self.pull = os.path.join(self.d, "pull_2026-10-26.json")
        json.dump(TLT.pull("2026-10-26", {1: TLT.block(1, "finished", scale=2), 2: TLT.block(2)}), open(self.pull, "w"))

    def test_a_finished_week_parses_to_twelve_lines_with_percentages_from_makes_and_attempts(self):
        wk = SI.from_pull(self.pull, 1, json.load(open(self.state)))
        self.assertEqual(wk["week"], 1)
        self.assertEqual(len(wk["teams"]), 12); self.assertEqual(len(wk["matchups"]), 6)
        t = wk["teams"]["Team 10"]
        self.assertEqual(t["opponent"], "Team 9")
        self.assertAlmostEqual(t["line"]["FG%"], 100 / 220, places=4)   # 50/110 doubled
        self.assertEqual(t["line"]["PTS"], 400)
        self.assertEqual(SI.owner_result(wk)["opponent"], "Team 9")

    def test_a_week_still_in_progress_halts(self):
        with self.assertRaises(SI.IntakeError):
            SI.from_pull(self.pull, 2, json.load(open(self.state)))

    def test_a_week_the_pull_does_not_carry_halts(self):
        with self.assertRaises(SI.IntakeError):
            SI.from_pull(self.pull, 3, json.load(open(self.state)))

    def test_cli_from_pull_writes_the_week_and_team_weeks(self):
        out = os.path.join(self.d, "weeks")
        p = subprocess.run([sys.executable, os.path.join(HERE, "scoreboard_intake.py"), "--week", "1", "--from-pull", self.pull,
                            "--state", self.state, "--weeks-dir", out, "--no-ledger"], capture_output=True, text=True)
        self.assertIn("SCOREBOARD INTAKE: PASS", p.stdout, p.stdout + p.stderr)
        self.assertTrue(os.path.exists(os.path.join(out, "week_1.json")))
        with open(os.path.join(out, "team_weeks.csv")) as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 12)
        self.assertEqual(rows[9]["team"], "Team 10"); self.assertEqual(float(rows[9]["PTS"]), 400)


if __name__ == "__main__":
    unittest.main(verbosity=2)
