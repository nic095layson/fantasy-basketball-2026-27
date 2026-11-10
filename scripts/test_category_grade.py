#!/usr/bin/env python3
"""Red-first tests for scripts/category_grade.py (owner 2026-11-10, pick "P5 + P7"): every pre-week category forecast
the kit recorded for every matchup (report/calibration_league.json flat, calibration_league_real.json real games),
graded against the week's final lines, by category. Nine forecasts a week came from the owner's matchup alone; this
reads all six matchups. Figures below are hand-derived.

    python3 scripts/test_category_grade.py
"""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import category_grade as G  # noqa: E402

CATS = G.CATS


def line(**kw):
    base = {"FG%": 0.47, "FT%": 0.78, "3PTM": 50, "PTS": 500, "REB": 200, "AST": 110, "ST": 30, "BLK": 20, "TO": 60}
    base.update(kw); return base


class Grade(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(); self.weeks = os.path.join(self.d, "weeks"); os.makedirs(self.weeks)
        # week 3: seat 1 beats seat 2 on PTS and TO (fewer turnovers), loses REB, ties AST; the rest tie
        json.dump(dict(week=3, teams={"A": dict(seat=1, line=line(PTS=520, TO=55, REB=190)), "B": dict(seat=2, line=line())}),
                  open(os.path.join(self.weeks, "week_3.json"), "w"))
        cat_p = {c: 0.5 for c in CATS}; cat_p.update(PTS=0.8, TO=0.3, REB=0.6, AST=0.7)
        self.flat = os.path.join(self.d, "flat.json"); self.real = os.path.join(self.d, "real.json")
        json.dump({"weeks": {"3": {"pairs": [dict(a=1, b=2, p_win=0.6, cat_p=cat_p)]},
                             "4": {"pairs": [dict(a=1, b=2, p_win=0.6, cat_p=cat_p)]}}}, open(self.flat, "w"))
        json.dump({"weeks": {"3": {"pairs": [dict(a=1, b=2, p_win=0.6, cat_p=dict(cat_p, PTS=0.9))]}}}, open(self.real, "w"))

    def rec(self):
        return G.grade(self.weeks, {"flat": self.flat, "real_games": self.real})

    def test_each_category_is_graded_with_ties_as_half_and_turnovers_low(self):
        r = self.rec()["methods"]["flat"]
        self.assertEqual(r["weeks"], [3])                       # week 4 has forecasts and no result yet
        by = r["by_cat"]
        self.assertAlmostEqual(by["PTS"]["brier"], (0.8 - 1) ** 2); self.assertAlmostEqual(by["TO"]["brier"], (0.3 - 1) ** 2)
        self.assertAlmostEqual(by["REB"]["brier"], (0.6 - 0) ** 2); self.assertAlmostEqual(by["AST"]["brier"], (0.7 - 0.5) ** 2)
        self.assertEqual(by["PTS"]["n"], 1)
        self.assertEqual((by["PTS"]["calls"], by["PTS"]["hits"]), (1, 1))     # favourite (0.8) won
        self.assertEqual((by["TO"]["calls"], by["TO"]["hits"]), (1, 0))       # the kit favoured seat 2 (0.3); seat 1 won it
        self.assertEqual((by["REB"]["calls"], by["REB"]["hits"]), (1, 0))
        self.assertEqual(by["AST"]["calls"], 0)                               # a tie is no call either way
        self.assertEqual(by["FG%"]["calls"], 0)                               # a 50% forecast favours nobody

    def test_the_total_pools_every_category(self):
        t = self.rec()["methods"]["flat"]["all"]
        self.assertEqual(t["n"], 9); self.assertEqual((t["calls"], t["hits"]), (3, 1))
        want = ((0.8 - 1) ** 2 + (0.3 - 1) ** 2 + 0.6 ** 2 + (0.7 - 0.5) ** 2 + 5 * 0.0) / 9
        self.assertAlmostEqual(t["brier"], want)
        self.assertAlmostEqual(t["confidence"], (0.8 + 0.7 + 0.6) / 3)        # mean stated chance of the favoured side

    def test_both_methods_are_graded_on_the_weeks_each_has(self):
        r = self.rec()["methods"]
        self.assertAlmostEqual(r["real_games"]["by_cat"]["PTS"]["brier"], (0.9 - 1) ** 2)
        self.assertEqual(r["real_games"]["weeks"], [3])

    def test_a_missing_forecast_file_or_seat_is_named_not_guessed(self):
        r = G.grade(self.weeks, {"flat": os.path.join(self.d, "none.json")})
        self.assertEqual(r["methods"]["flat"]["all"]["n"], 0); self.assertIn("no forecast record", r["methods"]["flat"]["note"])
        json.dump({"weeks": {"3": {"pairs": [dict(a=1, b=9, cat_p={c: 0.6 for c in CATS})]}}}, open(self.flat, "w"))
        r = G.grade(self.weeks, {"flat": self.flat})
        self.assertEqual(r["methods"]["flat"]["all"]["n"], 0); self.assertIn("week 3: seat 9 has no final line", r["methods"]["flat"]["note"])

    def test_render_and_summary(self):
        r = self.rec()
        text = "\n".join(G.render(r))
        for s in ("| PTS |", "coin flip", "flat", "real games", "favourite"):
            self.assertIn(s, text)
        self.assertEqual(G.summary(r), "flat 9 forecasts over 1 week(s), Brier 0.103, favourite right 1 of 3; real games 9, Brier 0.100")

    def test_run_writes_the_record_and_the_page(self):
        out = os.path.join(self.d, "category_grades.json")
        r = G.run(self.weeks, {"flat": self.flat, "real_games": self.real}, out)
        self.assertEqual(json.load(open(out))["methods"]["flat"]["all"]["n"], 9)
        self.assertTrue(os.path.exists(os.path.join(self.d, "category_grades.md")))
        self.assertEqual(r["methods"]["flat"]["all"]["n"], 9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
