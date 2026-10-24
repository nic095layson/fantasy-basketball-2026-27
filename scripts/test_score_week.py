#!/usr/bin/env python3
"""Red-first tests for scripts/score_week.py (owner 2026-10-24, Council order step 2: the scoring loop — every morning's
per-category P(win) for a finished week graded against the finals; Brier, a lead-to-date baseline, reliability bins;
append-only). Every expected figure below is computed by hand from the fixture, not by the code under test.

    python3 scripts/test_score_week.py
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import score_week as SW  # noqa: E402

CATS = ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]


def card(date, p, lead):
    """A week_matchup.py record for one morning: p = {cat: P(win)}, lead = {cat: me|opp|tie}."""
    return dict(date=date, week=1, window=["2026-10-20", "2026-10-25"], me="MY TEAM", opponent="THEM",
                cats=[dict(cat=c, p_win=p[c], leader_to_date=lead[c]) for c in CATS])


def final(won, tied):
    """A scoreboard_intake week_N.json: only the owner block matters here."""
    lost = [c for c in CATS if c not in won and c not in tied]
    return dict(week=1, teams={}, matchups=[], owner=dict(team="MY TEAM", opponent="THEM", won=won, lost=lost, tied=tied,
                                                           cats_won=len(won), cats_tied=len(tied)))


P1 = {"FG%": 0.9, "FT%": 0.6, "3PTM": 0.1, "PTS": 0.3, "REB": 0.2, "AST": 0.5, "ST": 0.5, "BLK": 0.8, "TO": 0.7}
L1 = {"FG%": "me", "FT%": "me", "3PTM": "opp", "PTS": "opp", "REB": "opp", "AST": "tie", "ST": "tie", "BLK": "me", "TO": "me"}
P2 = {"FG%": 0.95, "FT%": 0.4, "3PTM": 0.05, "PTS": 0.2, "REB": 0.1, "AST": 0.6, "ST": 0.5, "BLK": 0.9, "TO": 0.8}
L2 = {"FG%": "me", "FT%": "opp", "3PTM": "opp", "PTS": "opp", "REB": "opp", "AST": "me", "ST": "tie", "BLK": "me", "TO": "me"}
WON = ["FG%", "AST", "BLK", "TO"]; TIED = ["ST"]          # lost: FT%, 3PTM, PTS, REB -> a 4-4-1 week


class Arithmetic(unittest.TestCase):
    def setUp(self):
        self.rec = SW.score(final(WON, TIED), [card("2026-10-22", P1, L1), card("2026-10-23", P2, L2)])

    def test_outcomes_win_one_tie_half_loss_zero_and_brier_by_hand(self):
        d = self.rec["days"]["2026-10-22"]
        self.assertEqual((d["FG%"]["outcome"], d["ST"]["outcome"], d["FT%"]["outcome"]), (1.0, 0.5, 0.0))
        self.assertAlmostEqual(d["FG%"]["brier"], 0.01)        # (0.9-1)^2
        self.assertAlmostEqual(d["FT%"]["brier"], 0.36)        # (0.6-0)^2
        self.assertAlmostEqual(d["ST"]["brier"], 0.0)          # (0.5-0.5)^2
        # day mean: FG .01 FT .36 3PTM .01 PTS .09 REB .04 AST .25 ST 0 BLK .04 TO .09 = .89 / 9
        self.assertAlmostEqual(self.rec["by_day"]["2026-10-22"]["brier"], 0.89 / 9, places=6)
        # 10/23: FG .0025 FT .16 3PTM .0025 PTS .04 REB .01 AST .16 ST 0 BLK .01 TO .04 = .425 / 9
        self.assertAlmostEqual(self.rec["by_day"]["2026-10-23"]["brier"], 0.425 / 9, places=6)
        self.assertAlmostEqual(self.rec["brier"], (0.89 + 0.425) / 18, places=6)
        self.assertEqual(self.rec["n_forecasts"], 18)

    def test_baseline_is_the_lead_to_date_and_the_skill_is_the_difference(self):
        # 10/22 lead-to-date as a forecast: me->1, opp->0, tie->.5; FG 0 FT (1-0)^2=1 3PTM 0 PTS 0 REB 0 AST (.5-1)^2=.25 ST 0 BLK 0 TO 0 = 1.25/9
        self.assertAlmostEqual(self.rec["by_day"]["2026-10-22"]["baseline_brier"], 1.25 / 9, places=6)
        # 10/23: every lead matched the final (FT% behind and lost, AST ahead and won, ST level and tied) -> 0
        self.assertAlmostEqual(self.rec["by_day"]["2026-10-23"]["baseline_brier"], 0.0, places=6)
        self.assertAlmostEqual(self.rec["baseline_brier"], 1.25 / 18, places=6)
        self.assertAlmostEqual(self.rec["skill"], 1.25 / 18 - (0.89 + 0.425) / 18, places=6)   # negative here: the lead beat the card

    def test_per_category_means(self):
        self.assertAlmostEqual(self.rec["by_cat"]["FT%"]["brier"], (0.36 + 0.16) / 2)
        self.assertEqual(self.rec["by_cat"]["ST"]["outcome"], 0.5)

    def test_reliability_bins_count_forecasts_and_hits(self):
        b = {x["bin"]: x for x in self.rec["reliability"]}
        # 0.8-1.0 bin: FG .9, BLK .8, FG .95, BLK .9, TO .8 -> 5 forecasts, all won -> hit rate 1.0, mean p .87
        self.assertEqual(b["0.8-1.0"]["n"], 5); self.assertAlmostEqual(b["0.8-1.0"]["hit_rate"], 1.0); self.assertAlmostEqual(b["0.8-1.0"]["mean_p"], 0.87)
        # 0.0-0.2 bin: 3PTM .1, REB .2? no (.2 is 0.2-0.4), 3PTM .05, REB .1, PTS .2? no -> .1 .05 .1 = 3 forecasts, all lost -> 0.0
        self.assertEqual(b["0.0-0.2"]["n"], 3); self.assertAlmostEqual(b["0.0-0.2"]["hit_rate"], 0.0)
        self.assertEqual(sum(x["n"] for x in self.rec["reliability"]), 18)

    def test_a_missing_morning_is_listed_not_filled(self):
        rec = SW.score(final(WON, TIED), [card("2026-10-23", P2, L2)], window=["2026-10-20", "2026-10-25"])
        self.assertEqual(rec["days_scored"], ["2026-10-23"])
        self.assertEqual(rec["days_missing"], ["2026-10-20", "2026-10-21", "2026-10-22", "2026-10-24", "2026-10-25"])
        self.assertEqual(rec["n_forecasts"], 9)


class Ledger(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.weeks = os.path.join(self.d, "weeks"); os.makedirs(self.weeks)
        json.dump(final(WON, TIED), open(os.path.join(self.weeks, "week_1.json"), "w"))
        self.briefs = os.path.join(self.d, "briefs"); os.makedirs(self.briefs)
        for dt, p, l in (("2026-10-22", P1, L1), ("2026-10-23", P2, L2)):
            json.dump(card(dt, p, l), open(os.path.join(self.briefs, f"week_matchup_{dt}.json"), "w"))
        self.out = os.path.join(self.d, "calibration_daily.json")

    def test_run_writes_the_week_and_a_rerun_with_the_same_inputs_is_a_no_op(self):
        r1 = SW.run(1, self.weeks, self.briefs, self.out)
        self.assertEqual(r1["status"], "scored")
        led = json.load(open(self.out)); self.assertEqual(list(led["weeks"]), ["1"])
        self.assertAlmostEqual(led["weeks"]["1"]["brier"], (0.89 + 0.425) / 18, places=6)
        r2 = SW.run(1, self.weeks, self.briefs, self.out)
        self.assertEqual(r2["status"], "unchanged")
        self.assertEqual(json.load(open(self.out)), led)

    def test_a_rerun_with_different_inputs_halts_and_leaves_the_ledger(self):
        SW.run(1, self.weeks, self.briefs, self.out)
        before = json.load(open(self.out))
        json.dump(card("2026-10-24", P2, L2), open(os.path.join(self.briefs, "week_matchup_2026-10-24.json"), "w"))
        with self.assertRaises(SW.ScoreError):
            SW.run(1, self.weeks, self.briefs, self.out)
        self.assertEqual(json.load(open(self.out)), before)

    def test_cli_prints_pass_and_the_scorecard_md(self):
        p = subprocess.run([sys.executable, os.path.join(HERE, "score_week.py"), "--week", "1", "--weeks-dir", self.weeks,
                            "--briefs-dir", self.briefs, "--out", self.out, "--ledger", ""], capture_output=True, text=True)
        self.assertIn("WEEK SCORE: PASS", p.stdout, p.stdout + p.stderr)
        self.assertIn("Brier", p.stdout)
        self.assertTrue(os.path.exists(self.out.replace(".json", ".md")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
