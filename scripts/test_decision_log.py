#!/usr/bin/env python3
"""Red-first tests for scripts/decision_log.py and scripts/decision_grade.py (owner 2026-10-31, the decision log,
slice 1): append-only ledgers, the mechanical join of the owner's moves to the kit's recommendations, and a grader
that reads the board's z_adj for the verdict and reports box-score games beside it, never inside it.

    python3 scripts/test_decision_log.py
"""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import decision_log as DL  # noqa: E402
import decision_grade as DG  # noqa: E402

ALIASES = {"Cam Johnson": ["Cameron Johnson"]}


def brief(date, top=None, more=()):
    wt = ([dict(add=top[0], add_team="DEN", drop=top[1], d_ecw=0.02, d_title=top[2], title=16.7, title_by_seed={"2026": 16.8, "2027": 16.6},
                add_status={"code": "O"})] if top else []) + [dict(add=a, drop=d, d_title=t) for a, d, t in more]
    return dict(date=date, seasons=10000, lines="season lines", league_state_as_of=date, title={"2026": 15.6}, waiver_top=wt)


def moves_record(path, date, moves, phase="am"):
    json.dump(dict(date=date, phase=phase, moves=moves), open(path, "w"))


def board(path, date, rows):
    json.dump(dict(date=date, board=[dict(name=n, z_adj=z, gp=70) for n, z in rows]), open(path, "w"))


def actuals(path, date, rows):
    json.dump(dict(date=date, games=[], players=[dict(pool_name=n, team=t, min=m, dnp=m == 0, pts=p, reb=0, ast=0, stl=0, blk=0,
                                                       tov=0, tpm=0, fgm=0, fga=0, ftm=0, fta=0) for n, t, m, p in rows]), open(path, "w"))


class Ledgers(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.recs = os.path.join(self.d, "recommendations.jsonl")

    def test_brief_row_is_the_top_pair_and_a_second_day_is_refused(self):
        row = DL.brief_row(brief("2026-10-30", ("Cameron Johnson", "Collin Gillespie", 1.16), [("Tobias Harris", "Neemias Queta", 0.16)]), [], made_at="t")
        self.assertEqual((row["id"], row["kind"], row["add"], row["drop"], row["basis"]["d_title"]), ("R-2026-10-30-01", "add_drop", "Cameron Johnson", "Collin Gillespie", 1.16))
        self.assertEqual(row["alternatives"], [{"add": "Tobias Harris", "drop": "Neemias Queta", "d_title": 0.16}])
        DL.append(self.recs, [row])
        with self.assertRaises(DL.LogError):
            DL.brief_row(brief("2026-10-30", ("X", "Y", 0.3)), DL.read(self.recs))
        with self.assertRaises(DL.LogError):
            DL.append(self.recs, [row])  # same id
        self.assertEqual(len(DL.read(self.recs)), 1)

    def test_a_brief_with_no_positive_pair_logs_a_hold(self):
        row = DL.brief_row(brief("2026-10-31"), [], made_at="t")
        self.assertEqual((row["kind"], row["add"], row["drop"]), ("hold", None, None))
        row2 = DL.brief_row(brief("2026-11-01", ("A", "B", -0.2)), [], made_at="t")
        self.assertEqual(row2["kind"], "hold")
        self.assertIn("A for B", row2["note"])

    def test_session_row_ids_count_within_the_day_and_a_correction_supersedes(self):
        r1 = DL.session_row([], "2026-10-30", "Cameron Johnson", "Collin Gillespie", 1.15, [{"drop": "Neemias Queta", "d_title": 0.35}], made_at="t")
        r2 = DL.session_row([r1], "2026-10-30", "Cameron Johnson", "Neemias Queta", 0.35, made_at="t", supersedes="S-2026-10-30-01")
        self.assertEqual((r1["id"], r2["id"], r1["source"], r1["kind"]), ("S-2026-10-30-01", "S-2026-10-30-02", "session", "add_drop"))
        sess = os.path.join(self.d, "session.jsonl")
        DL.append(sess, [r1, r2])
        self.assertEqual([r["id"] for r in DL.recommendations(self.recs, sess)], ["S-2026-10-30-02"])

    def test_join_classifies_the_move(self):
        recs = [DL.session_row([], "2026-10-30", "Cameron Johnson", "Collin Gillespie", 1.15, made_at="t")]
        mk = lambda added, dropped, date="2026-10-31": dict(date=date, added=added, dropped=dropped)
        self.assertEqual(DL.join(mk(["Cameron Johnson"], ["Collin Gillespie"]), recs), ("S-2026-10-30-01", "exact"))
        self.assertEqual(DL.join(mk(["Cameron Johnson"], ["Julian Champagnie"]), recs), ("S-2026-10-30-01", "add_match_drop_differs"))
        self.assertEqual(DL.join(mk(["Jalen Smith"], ["Collin Gillespie"]), recs), ("S-2026-10-30-01", "drop_match_add_differs"))
        self.assertEqual(DL.join(mk(["Jalen Smith"], ["Neemias Queta"]), recs), (None, "unrelated"))
        self.assertEqual(DL.join(mk(["Cameron Johnson"], ["Collin Gillespie"], "2026-12-15"), recs), (None, "none"))
        self.assertEqual(DL.join(mk(["Cameron Johnson"], ["Collin Gillespie"], "2026-10-29"), recs), (None, "none"))  # before the advice

    def test_moves_rows_take_seat_10_only_and_skip_what_is_logged(self):
        news = os.path.join(self.d, "news"); os.makedirs(news)
        moves_record(os.path.join(news, "league_moves_2026-10-31.json"), "2026-10-31",
                     [dict(team="Me", seat=10, added=["Cameron Johnson"], dropped=["Julian Champagnie"], to_il=[], from_il=[]),
                      dict(team="Them", seat=1, added=["Aaron Nesmith"], dropped=["Keldon Johnson"], to_il=[], from_il=[])])
        moves_record(os.path.join(news, "league_moves_2026-10-31_pm.json"), "2026-10-31",
                     [dict(team="Me", seat=10, added=[], dropped=[], to_il=["X"], from_il=[])], phase="pm")
        recs = [DL.session_row([], "2026-10-30", "Cameron Johnson", "Collin Gillespie", 1.15, made_at="t")]
        rows = DL.moves_rows(news, [], recs, seen_at="t")
        self.assertEqual([(r["id"], r["phase"], r["match_kind"], r["matches"]) for r in rows],
                         [("M-2026-10-31-01", "am", "add_match_drop_differs", "S-2026-10-30-01"), ("M-2026-10-31-02", "pm", "unrelated", None)])
        self.assertEqual(DL.moves_rows(news, rows, recs, seen_at="t"), [])  # nothing new on a second scan

    def test_a_move_seen_by_the_afternoon_and_the_next_morning_is_one_row(self):
        news = os.path.join(self.d, "news"); os.makedirs(news)
        mv = dict(team="Me", seat=10, added=["Bobby Portis"], dropped=[], to_il=[], from_il=[])
        moves_record(os.path.join(news, "league_moves_2026-10-28_pm.json"), "2026-10-28", [mv], phase="pm")
        moves_record(os.path.join(news, "league_moves_2026-10-29.json"), "2026-10-29", [mv])
        moves_record(os.path.join(news, "league_moves_2026-11-05.json"), "2026-11-05", [mv])  # a week later: a new move
        rows = DL.moves_rows(news, [], [], seen_at="t")
        self.assertEqual([(r["id"], r["phase"]) for r in rows], [("M-2026-10-28-01", "pm"), ("M-2026-11-05-01", "am")])
        self.assertEqual(DL.moves_rows(news, rows, [], seen_at="t"), [])


class Grader(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.boards = os.path.join(self.d, "season"); self.acts = os.path.join(self.d, "actuals")
        os.makedirs(self.boards); os.makedirs(self.acts)
        self.rec = DL.session_row([], "2026-10-30", "Cameron Johnson", "Collin Gillespie", 1.15, made_at="t")
        self.move = dict(id="M-2026-10-31-01", date="2026-10-31", added=["Cameron Johnson"], dropped=["Julian Champagnie"],
                         matches="S-2026-10-30-01", match_kind="add_match_drop_differs")
        board(os.path.join(self.boards, "board_2026-10-30.json"), "2026-10-30", [("Cam Johnson", 1.0), ("Collin Gillespie", -1.4), ("Julian Champagnie", -1.0)])
        board(os.path.join(self.boards, "board_2026-11-28.json"), "2026-11-28", [("Cam Johnson", 2.1), ("Collin Gillespie", -0.9), ("Julian Champagnie", 1.9)])
        import datetime as dt
        for i in range(29):
            d = (dt.date(2026, 10, 31) + dt.timedelta(days=i)).isoformat()
            actuals(os.path.join(self.acts, f"{d}.json"), d, [("Cam Johnson", "DEN", 30, 20), ("Collin Gillespie", "PHX", 20, 8), ("Julian Champagnie", "SAS", 25, 9)])

    def test_window_opens_on_the_move_and_the_verdict_reads_the_end_board(self):
        g = DG.grade(self.rec, [self.move], "2026-11-30", self.boards, self.acts, aliases=ALIASES)
        self.assertEqual(g["window"], ["2026-10-31", "2026-11-28"])
        self.assertEqual(g["inputs"]["board_end"]["date"], "2026-11-28")
        self.assertAlmostEqual(g["kit_gap_end"], 3.0)      # 2.1 - (-0.9)
        self.assertAlmostEqual(g["kit_gap_start"], 2.4)    # 1.0 - (-1.4)
        self.assertEqual(g["verdict"], "KIT RIGHT")
        self.assertAlmostEqual(g["owner_gap_end"], 0.2)    # 2.1 - 1.9
        self.assertAlmostEqual(g["owner_minus_kit"], -2.8)
        self.assertEqual(g["owner_verdict"], "KIT BETTER")
        self.assertEqual(g["values"]["kit_add"]["board_name"], "Cam Johnson")  # the alias resolved
        self.assertTrue(all("sha256" in v for v in g["inputs"].values()))

    def test_games_are_reported_beside_the_verdict_and_never_change_it(self):
        g = DG.grade(self.rec, [self.move], "2026-11-30", self.boards, self.acts, aliases=ALIASES)
        self.assertEqual(g["games"]["kit_add"]["games"], 29)
        self.assertEqual(g["games"]["kit_add"]["totals"]["pts"], 580.0)
        # the drop scores 60 points a night for the whole window: the box totals move, the verdict does not
        for p in os.listdir(self.acts):
            d = p[:10]
            actuals(os.path.join(self.acts, p), d, [("Cam Johnson", "DEN", 30, 2), ("Collin Gillespie", "PHX", 36, 60), ("Julian Champagnie", "SAS", 25, 9)])
        g2 = DG.grade(self.rec, [self.move], "2026-11-30", self.boards, self.acts, aliases=ALIASES)
        self.assertEqual(g2["games"]["kit_drop"]["totals"]["pts"], 1740.0)
        self.assertEqual((g2["verdict"], g2["kit_gap_end"]), (g["verdict"], g["kit_gap_end"]))

    def test_a_player_absent_from_the_first_box_file_is_still_counted(self):
        # the first day of the window lists only one team's game; the add plays from day two
        first = sorted(os.listdir(self.acts))[0]
        actuals(os.path.join(self.acts, first), first[:10], [("Julian Champagnie", "SAS", 25, 9)])
        g = DG.grade(self.rec, [self.move], "2026-11-30", self.boards, self.acts, aliases=ALIASES)
        self.assertEqual((g["games"]["kit_add"]["games"], g["games"]["kit_drop"]["games"]), (28, 28))

    def test_open_window_and_too_few_games_stay_pending(self):
        g = DG.grade(self.rec, [self.move], "2026-11-10", self.boards, self.acts, aliases=ALIASES)
        self.assertEqual(g["verdict"], "PENDING"); self.assertIn("window open until 2026-11-28", g["note"])
        self.assertEqual(g["inputs"]["board_end"]["date"], "2026-10-30")  # the newest board as of the grading date
        for p in os.listdir(self.acts)[5:]:
            os.remove(os.path.join(self.acts, p))
        g = DG.grade(self.rec, [self.move], "2026-11-30", self.boards, self.acts, aliases=ALIASES)
        self.assertEqual(g["verdict"], "PENDING"); self.assertIn("fewer than 10 games", g["note"])
        self.assertNotIn("owner_verdict", g)

    def test_missing_board_name_and_hold_rows(self):
        rec = DL.session_row([], "2026-10-30", "Nobody Here", "Collin Gillespie", 0.4, made_at="t")
        g = DG.grade(rec, [], "2026-11-30", self.boards, self.acts, aliases=ALIASES)
        self.assertEqual(g["verdict"], "PENDING"); self.assertIn("Nobody Here", g["note"])
        self.assertEqual(g["window"], ["2026-10-30", "2026-11-27"])  # no move: the recommendation date opens it
        hold = DL.brief_row(brief("2026-10-31"), [], made_at="t")
        self.assertEqual(DG.grade(hold, [], "2026-11-30", self.boards, self.acts, aliases=ALIASES)["verdict"], "HOLD")

    def test_verdict_lines(self):
        self.assertEqual([DG.verdict_word(x) for x in (0.51, 0.5, -0.5, -0.51)], ["KIT RIGHT", "TOO CLOSE", "TOO CLOSE", "KIT WRONG"])
        self.assertEqual([DG.owner_word(x) for x in (0.6, 0.0, -0.6)], ["OWNER BETTER", "TOO CLOSE", "KIT BETTER"])

    def test_main_appends_final_rows_once_and_regenerates_the_card(self):
        dd = os.path.join(self.d, "decisions"); os.makedirs(dd); out = os.path.join(self.d, "out")
        DL.append(os.path.join(dd, "session.jsonl"), [self.rec]); DL.append(os.path.join(dd, "moves.jsonl"), [self.move])
        import unittest.mock as um
        with um.patch.object(DG.box_pull, "load_aliases", lambda *a, **k: ALIASES):
            self.assertEqual(DG.main(["--as-of", "2026-11-30", "--dir", dd, "--boards", self.boards, "--actuals", self.acts, "--out", out, "--dry-run"]), 0)
            self.assertFalse(os.path.exists(os.path.join(out, "grades.jsonl")))
            DG.main(["--as-of", "2026-11-30", "--dir", dd, "--boards", self.boards, "--actuals", self.acts, "--out", out])
            DG.main(["--as-of", "2026-12-01", "--dir", dd, "--boards", self.boards, "--actuals", self.acts, "--out", out])
        self.assertEqual(len(DL.read(os.path.join(out, "grades.jsonl"))), 1)  # the same window is not graded twice
        card = open(os.path.join(out, "scorecard.md")).read()
        self.assertIn("| kit vs its own drop | 1 | 1 | 0 | 0 | 0 | 1 | 0 |", card)
        self.assertIn("KIT RIGHT / KIT BETTER", card)


if __name__ == "__main__":
    unittest.main()
