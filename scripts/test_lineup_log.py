#!/usr/bin/env python3
"""Red-first tests for lineup_log.py (owner 2026-11-05: the start/sit ledger and its hit/miss rate)."""
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lineup_log as LL  # noqa: E402

ME = "KEL'EL YAXEL HALQUETA"


def box(name, team, mins, pts, fgm, fga, ftm, fta, tpm, reb, ast, stl, blk, tov, dnp=False):
    return dict(name=name, pool_name=name, team=team, min=mins, pts=pts, fgm=fgm, fga=fga, ftm=ftm, fta=fta, tpm=tpm,
                reb=reb, ast=ast, stl=stl, blk=blk, tov=tov, dnp=dnp, starter=True, game="g1")


class Fixture(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.briefs = os.path.join(self.d, "briefs"); self.pins = os.path.join(self.d, "flaim"); self.acts = os.path.join(self.d, "actuals")
        for p in (self.briefs, self.pins, self.acts):
            os.makedirs(p)
        self.ledger = os.path.join(self.d, "decisions", "lineup.jsonl")
        self.sc = os.path.join(self.d, "report", "lineup_scorecard.json")

    def tearDown(self):
        shutil.rmtree(self.d, ignore_errors=True)

    def brief(self, day, moves, games=True):
        with open(os.path.join(self.briefs, f"week_matchup_{day}.json"), "w") as f:
            json.dump(dict(date=day, me=dict(name=ME, seat=10), lineup_today=dict(date=day, games_today=games, moves=moves)), f)

    def pin(self, pull_name, day, lineup, team=ME):
        with open(os.path.join(self.pins, f"pull_{pull_name}.json"), "w") as f:
            json.dump(dict(daily={"478.l.36464.t.11": {day: dict(teamName=team, snapshot=dict(date=day),
                                                                   players=[dict(name=n, selectedPosition=s) for n, s in lineup])}}), f)

    def actuals(self, day, rows):
        # a pool of filler lines so the engine's top-156 fixed point has something to standardize over
        filler = [box(f"Filler {i}", "XXX", 20 + i % 10, 8 + i % 7, 3, 7 + i % 4, 2, 2, 1, 4 + i % 5, 2 + i % 3, i % 2, i % 2, 1 + i % 3) for i in range(40)]
        with open(os.path.join(self.acts, f"{day}.json"), "w") as f:
            json.dump(dict(date=day, players=rows + filler), f)

    def run_days(self, days, dry_run=False):
        return LL.run(days, ledger=self.ledger, briefs=self.briefs, pin_dir=self.pins, actuals=self.acts, scorecard_path=self.sc, dry_run=dry_run)


class Grading(Fixture):
    def test_a_followed_start_and_an_ignored_sit_with_the_night_scored_by_the_engine(self):
        self.brief("2026-11-04", [dict(start="Kyrie Irving", sit="Karlo Matkovic", kind="better", gap=7.44, d_exp=0.173)])
        self.pin("2026-11-05", "2026-11-04", [("Kyrie Irving", "Util"), ("Karlo Matković", "F"), ("P.J. Washington", "BN")])
        self.actuals("2026-11-04", [box("Kyrie Irving", "DAL", 36, 29, 9, 27, 6, 8, 5, 7, 5, 1, 0, 1),
                                    box("Karlo Matkovic", "NOP", 21, 5, 2, 3, 0, 0, 1, 4, 2, 0, 1, 1)])
        row = LL.grade_day("2026-11-04", self.briefs, self.pins, self.acts, aliases={})
        self.assertEqual(row["status"], "graded"); self.assertTrue(row["lineup_record"]); self.assertTrue(row["box_record"])
        p = row["pairs"][0]
        self.assertTrue(p["start_followed"]); self.assertFalse(p["sit_followed"])
        self.assertEqual(p["locked"], {"Kyrie Irving": "Util", "Karlo Matkovic": "F"})  # the accent folds to the brief's spelling
        self.assertEqual(p["night"], "kit"); self.assertGreater(p["z_gap"], 0)
        self.assertEqual(p["box"]["Kyrie Irving"]["pts"], 29); self.assertEqual(p["box"]["Karlo Matkovic"]["fg"], "2/3")

    def test_a_day_without_a_suggestion_is_agreed_and_a_missing_lineup_pin_is_named_not_guessed(self):
        self.brief("2026-11-03", [])
        self.actuals("2026-11-03", [])
        row = LL.grade_day("2026-11-03", self.briefs, self.pins, self.acts, aliases={})
        self.assertEqual(row["status"], "agreed"); self.assertFalse(row["lineup_record"]); self.assertEqual(row["pairs"], [])
        self.brief("2026-11-02", [dict(start="A Guy", sit="B Guy", kind="better", gap=1.0)])
        self.actuals("2026-11-02", [box("A Guy", "AAA", 30, 20, 8, 15, 4, 4, 0, 5, 5, 1, 1, 2)])  # B Guy: no box line
        row = LL.grade_day("2026-11-02", self.briefs, self.pins, self.acts, aliases={})
        p = row["pairs"][0]
        self.assertIsNone(p["locked"]); self.assertIsNone(p["start_followed"]); self.assertIsNone(p["sit_followed"])
        self.assertEqual(p["night"], "no grade"); self.assertIsNone(p["box"]["B Guy"])

    def test_no_brief_and_an_empty_sit_slot(self):
        row = LL.grade_day("2026-10-01", self.briefs, self.pins, self.acts, aliases={})
        self.assertEqual(row["status"], "no brief"); self.assertEqual(row["pairs"], [])
        self.brief("2026-11-01", [dict(start="A Guy", sit=None, kind="empty", gap=None)])
        self.pin("2026-11-02", "2026-11-01", [("A Guy", "PG")])
        self.actuals("2026-11-01", [box("A Guy", "AAA", 30, 20, 8, 15, 4, 4, 0, 5, 5, 1, 1, 2)])
        p = LL.grade_day("2026-11-01", self.briefs, self.pins, self.acts, aliases={})["pairs"][0]
        self.assertTrue(p["start_followed"]); self.assertIsNone(p["sit_followed"]); self.assertEqual(p["night"], "no grade")


class Ledger(Fixture):
    def test_append_only_waits_for_box_scores_and_rolls_the_scorecard_up(self):
        self.brief("2026-10-26", [dict(start="Ty Jerome", sit="PJ Washington", kind="better", gap=4.48),
                                  dict(start="Miles Bridges", sit="Collin Gillespie", kind="better", gap=0.36)])
        self.pin("2026-10-27", "2026-10-26", [("Ty Jerome", "G"), ("P.J. Washington", "Util"), ("Miles Bridges", "BN"), ("Collin Gillespie", "BN")])
        self.actuals("2026-10-26", [box("Ty Jerome", "CLE", 30, 15, 4, 15, 6, 7, 1, 1, 8, 1, 0, 1), box("PJ Washington", "DAL", 41, 20, 6, 15, 4, 4, 4, 9, 2, 2, 1, 3),
                                    box("Miles Bridges", "CHA", 32, 17, 7, 17, 1, 2, 2, 8, 4, 1, 0, 3), box("Collin Gillespie", "PHX", 23, 9, 3, 9, 0, 0, 3, 1, 2, 2, 0, 2)])
        self.brief("2026-10-27", [])  # agreed, box scores not in yet → waits
        new, skipped, sc, pending, missing = self.run_days(["2026-10-26", "2026-10-27"], dry_run=True)
        self.assertEqual([r["id"] for r in new], ["L-2026-10-26"]); self.assertEqual(pending, ["2026-10-27"])
        self.assertFalse(os.path.exists(self.ledger))
        new, skipped, sc, pending, missing = self.run_days(["2026-10-26", "2026-10-27"])
        self.assertTrue(os.path.exists(self.ledger)); self.assertEqual(sc["days"], 1); self.assertEqual(sc["pairs"], 2)
        self.assertEqual((sc["start_followed"], sc["sit_followed"], sc["both_followed"]), (1, 1, 0))
        self.assertEqual((sc["night_kit"], sc["night_against"]), (1, 1)); self.assertEqual(sc["start_followed_rate"], 0.5)
        self.assertEqual(sc["gap_sum_followed"], 4.48); self.assertEqual(sc["gap_sum_ignored"], 0.36)
        # the box scores land: the waiting day is logged; the logged day is left as it is
        self.actuals("2026-10-27", [])
        new, skipped, sc, pending, missing = self.run_days(["2026-10-26", "2026-10-27"])
        self.assertEqual(skipped, ["2026-10-26"]); self.assertEqual([r["id"] for r in new], ["L-2026-10-27"]); self.assertEqual(pending, [])
        self.assertEqual((sc["days"], sc["days_agreed"], sc["days_graded"]), (2, 1, 1))
        with open(self.ledger) as f:
            self.assertEqual(sum(1 for ln in f if ln.strip()), 2)
        md = open(self.sc[:-5] + ".md").read()
        self.assertIn("| 2026-10-26 | Ty Jerome | PJ Washington | 4.48 | yes | no | against |", md)
        self.assertIn("| 2026-10-27 | — | — | — | agreed |", md)
        self.assertIn("not a verdict", md)

    def test_a_day_with_no_games_is_logged_without_box_scores_and_a_day_without_a_brief_is_only_reported(self):
        self.brief("2026-10-30", [], games=False)
        new, skipped, sc, pending, missing = self.run_days(["2026-10-30", "2026-10-29"])
        self.assertEqual([r["id"] for r in new], ["L-2026-10-30"]); self.assertEqual(pending, []); self.assertEqual(missing, ["2026-10-29"])
        self.assertEqual(sc["days"], 1)

    def test_main_prints_the_pass_line_and_the_morning_form_grades_yesterday(self):
        import io
        from contextlib import redirect_stdout
        LL.BRIEFS, LL.PIN_DIR, LL.ACTUALS, LL.LEDGER, LL.SCORECARD = self.briefs, self.pins, self.acts, self.ledger, self.sc
        self.brief("2026-11-04", [dict(start="A Guy", sit="B Guy", kind="better", gap=2.0)])
        self.pin("2026-11-05", "2026-11-04", [("A Guy", "PG"), ("B Guy", "BN")])
        self.actuals("2026-11-04", [box("A Guy", "AAA", 30, 20, 8, 15, 4, 4, 0, 5, 5, 1, 1, 2), box("B Guy", "BBB", 30, 10, 4, 15, 2, 4, 0, 5, 5, 1, 1, 2)])
        out = io.StringIO()
        with redirect_stdout(out):
            rc = LL.main(["--date", "2026-11-05"])
        self.assertEqual(rc, 0)
        self.assertRegex(out.getvalue(), r"^LINEUP LOG: PASS — 2026-11-04: 1 pair\(s\), start followed 1; ledger 1 days, 1 pairs, start followed 1/1, night kit 1 / against 0")
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(LL.main(["--date", "2026-11-05"]), 0)
        self.assertIn("already logged: 2026-11-04", out.getvalue())
        self.assertEqual(LL.main([]), 2)


class LockedLineupByKey(unittest.TestCase):
    """F3 (owner 2026-11-10): the locked lineup is read by team key, so a pin made before a rename is still found."""
    def test_a_pin_made_under_the_old_name_is_read_after_a_rename(self):
        d = tempfile.mkdtemp(); K = "478.l.36464.t.11"
        def pin(fn, day, name, player):
            json.dump(dict(daily={K: {day: dict(teamKey=K, teamName=name, players=[dict(name=player, selectedPosition="PG")])},
                                  "478.l.36464.t.1": {day: dict(teamName="Other", players=[dict(name="Not Mine", selectedPosition="C")])}}),
                      open(os.path.join(d, fn), "w"))
        pin("pull_2026-11-10.json", "2026-11-09", "Old Name", "A One")
        pin("pull_2026-11-11.json", "2026-11-10", "New Name", "B Two")
        self.assertEqual(LL.locked_lineup("2026-11-09", "New Name", d), {"A One": "PG"})
        self.assertEqual(LL.locked_lineup("2026-11-10", "New Name", d), {"B Two": "PG"})
        self.assertIsNone(LL.locked_lineup("2026-11-09", "Nobody", d))


if __name__ == "__main__":
    unittest.main()
