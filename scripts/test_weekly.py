#!/usr/bin/env python3
"""Red-first tests for scripts/weekly_preview.py and the calibration ledger (Session 1 item 7; plan §4 B6).

The ledger is the only grade that is not circular (L6), so it must be impossible to edit a
prediction after the week starts: a recorded week is append-only.

    python3 scripts/test_weekly.py
"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import weekly_preview as WP  # noqa: E402

PRED = {"week": 1, "opponent_seat": 11, "p_win": 0.6, "exp_cats": 4.9,
        "cat_p": {"FG%": 0.6, "FT%": 0.7, "3PTM": 0.5, "PTS": 0.4, "REB": 0.4, "AST": 0.3, "ST": 0.5, "BLK": 0.7, "TO": 0.9}}


class Ledger(unittest.TestCase):
    def test_records_before_the_week_and_refuses_a_rewrite(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "calibration.json")
            WP.record(p, PRED, recorded_at="2026-10-15T20:00:00Z", week_start="2026-10-20")
            with self.assertRaises(WP.LedgerError):
                WP.record(p, dict(PRED, p_win=0.9), recorded_at="2026-10-16T00:00:00Z", week_start="2026-10-20")
            self.assertEqual(json.load(open(p))["weeks"]["1"]["p_win"], 0.6)

    def test_refuses_a_prediction_recorded_after_the_week_started(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(WP.LedgerError):
                WP.record(os.path.join(d, "c.json"), PRED, recorded_at="2026-10-21T00:00:00Z", week_start="2026-10-20")

    def test_brier_scores_the_categories_and_the_matchup(self):
        actual = {"won": ["FG%", "FT%", "BLK", "TO", "ST"]}
        s = WP.score(PRED, actual)
        want = sum((PRED["cat_p"][c] - (1.0 if c in actual["won"] else 0.0)) ** 2 for c in PRED["cat_p"]) / 9
        self.assertAlmostEqual(s["brier_cats"], want)
        self.assertAlmostEqual(s["brier_matchup"], (0.6 - 1.0) ** 2)


class MatchupOnly(unittest.TestCase):
    """2026-10-22, week 2: the preview simulates the owner against one opponent, but built every team's model first, so a
    player without a line on a third team's roster (Andre Drummond, seat 9, D-DR-1) stopped the record. Only the two
    teams in the matchup are modelled; a player without a line on either of them still stops it, by name."""

    def _state(self, d, seat, name):
        st = json.load(open(WP.CG.STATE, encoding="utf-8"))
        for t in st["teams"]:
            if t["seat"] == seat:
                t["players"].append(dict(player=name, slot="BN"))
        p = os.path.join(d, "league_state.json")
        json.dump(st, open(p, "w", encoding="utf-8"))
        return p

    def _preview(self, state_path):
        old = WP.CG.STATE
        WP.CG.STATE = state_path
        try:
            return WP.preview(1, n=200)
        finally:
            WP.CG.STATE = old

    def test_a_third_team_player_without_a_line_does_not_stop_or_move_the_preview(self):
        o = next(x for x in json.load(open(WP.CG.SCHEDULE, encoding="utf-8"))["owner_opponents"] if x["week"] == 1)
        third = next(s for s in range(1, 13) if s not in (WP.CG.OWNER_SEAT, o["seat"]))
        with tempfile.TemporaryDirectory() as d:
            clean = self._preview(self._state(d, third, "No Such Player Zz"))
        with tempfile.TemporaryDirectory() as d:
            base = self._preview(self._state(d, -1, "unused"))
        self.assertEqual(clean["by_seed"], base["by_seed"])

    def test_a_matchup_player_without_a_line_stops_the_preview_by_name(self):
        o = next(x for x in json.load(open(WP.CG.SCHEDULE, encoding="utf-8"))["owner_opponents"] if x["week"] == 1)
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(WP.LedgerError, "No Such Player Zz"):
                self._preview(self._state(d, o["seat"], "No Such Player Zz"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
