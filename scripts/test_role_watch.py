#!/usr/bin/env python3
"""Red-first tests for scripts/role_watch.py (owner 2026-11-17: "Starts watch", "Hold check on drops").

    python3 scripts/test_role_watch.py
"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import form_board as FB  # noqa: E402
import league_intake as LI  # noqa: E402
import role_watch as RW  # noqa: E402


def box(date, *players):
    """One day's box-score record; each player is (name, minutes, starter, pool_name or None[, dnp])."""
    return {"date": date, "games": [{"espn_id": "g" + date, "season_type": 2}],
            "players": [dict(name=p[0], pool_name=p[3], team="AAA", game="g" + date, min=p[1], starter=p[2],
                             dnp=bool(p[4]) if len(p) > 4 else False, pts=10, reb=4, ast=2, stl=1, blk=0, tpm=1, tov=1,
                             fgm=4, fga=8, ftm=1, fta=2) for p in players]}


def log_of(*records):
    return FB.game_log(list(records))


STATE = {"teams": [{"name": "Mine", "seat": 10, "players": [{"player": "Own Rental", "slot": "BN"}, {"player": "Own Star", "slot": "PG"},
                                                           {"player": "Own Hurt", "slot": "IL"}]},
                   {"name": "Rival", "seat": 3, "players": [{"player": "Rival Guy", "yahoo_name": "Rival Guy Jr.", "slot": "C"}],
                    "unpooled": [{"player": "Carried Man", "slot": "BN"}]}],
         "unpooled": [{"player": "Carried Man", "fantasy_team": "Rival", "seat": 3}]}


class StartRun(unittest.TestCase):
    def test_counts_straight_starts_back_from_the_last_game(self):
        g = lambda s: {"starter": s}  # noqa: E731
        self.assertEqual(RW.start_run([g(True), g(False), g(True), g(True)]), 2)
        self.assertEqual(RW.start_run([g(True), g(True), g(False)]), 0)
        self.assertEqual(RW.start_run([]), 0)


class StartsWatch(unittest.TestCase):
    def setUp(self):
        self.log = log_of(
            box("2026-11-10", ("Free Starter", 30, True, "Free Starter"), ("Bench Guy", 25, False, "Bench Guy"),
                ("Rival Guy", 33, True, "Rival Guy"), ("No Line", 28, True, None), ("Carried Man", 30, True, None)),
            box("2026-11-12", ("Free Starter", 34, True, "Free Starter"), ("Bench Guy", 31, True, "Bench Guy"),
                ("Rival Guy", 35, True, "Rival Guy"), ("No Line", 31, True, None), ("Carried Man", 30, True, None)),
            box("2026-11-14", ("Free Starter", 36, True, "Free Starter"), ("Bench Guy", 20, False, "Bench Guy")))
        self.rostered = RW.rostered_names(STATE)

    def rows(self, date="2026-11-15", **kw):
        return RW.starts_watch(self.log, self.rostered, date, pool_names=["Free Starter", "Bench Guy", "Rival Guy"], **kw)

    def test_a_free_player_who_started_his_last_two_is_listed_and_a_rostered_one_is_not(self):
        names = [r["player"] for r in self.rows()]
        self.assertEqual(names, ["No Line", "Free Starter"])       # the new run first; Rival Guy and Carried Man are rostered

    def test_a_broken_run_is_not_listed(self):
        self.assertNotIn("Bench Guy", [r["player"] for r in self.rows()])

    def test_the_row_carries_the_run_the_minutes_and_whether_the_pool_has_a_line(self):
        r = {x["player"]: x for x in self.rows()}
        self.assertEqual((r["Free Starter"]["starts_in_a_row"], r["Free Starter"]["minutes"], r["Free Starter"]["new"]), (3, [30, 34, 36], False))
        self.assertTrue(r["Free Starter"]["pooled"])
        self.assertEqual((r["No Line"]["pooled"], r["No Line"]["new"], r["No Line"]["starts_in_a_row"]), (False, True, 2))
        self.assertEqual(r["Free Starter"]["line"]["pts"], 10.0)

    def test_only_games_before_the_brief_date_count(self):
        # on the morning of 11-12 Free Starter has one game: no run yet
        self.assertEqual(self.rows("2026-11-12"), [])

    def test_a_starter_who_stopped_playing_drops_off(self):
        self.assertNotIn("No Line", [r["player"] for r in self.rows("2026-11-25")])
        self.assertEqual(self.rows("2026-11-25"), [])

    def test_a_dnp_is_not_a_game(self):
        log = log_of(box("2026-11-10", ("A", 30, True, "A")), box("2026-11-11", ("A", 0, False, "A", True)),
                     box("2026-11-12", ("A", 30, True, "A")))
        self.assertEqual([r["starts_in_a_row"] for r in RW.starts_watch(log, set(), "2026-11-13")], [2])

    def test_the_injury_line_and_a_recent_drop_ride_along(self):
        rows = self.rows(espn=[{"player": "Free Starter", "status": "Day-To-Day", "return_date": "2026-11-18"}],
                         dropped={LI.norm("Free Starter"): ("2026-11-14", "Rival", 3)})
        r = rows[0]
        self.assertEqual(r["player"], "Free Starter")   # a fresh drop is news: it leads with the new run
        self.assertEqual(r["status"], {"status": "Day-To-Day", "return_date": "2026-11-18"})
        self.assertEqual(r["dropped"], {"day": "2026-11-14", "team": "Rival"})

    def test_a_yahoo_spelling_on_a_roster_still_counts_as_rostered(self):
        log = log_of(box("2026-11-10", ("Rival Guy Jr.", 30, True, None)), box("2026-11-12", ("Rival Guy Jr.", 30, True, None)))
        self.assertEqual(RW.starts_watch(log, self.rostered, "2026-11-13"), [])


class Moves(unittest.TestCase):
    def test_reads_morning_and_afternoon_records_in_the_window(self):
        d = tempfile.mkdtemp()
        json.dump({"moves": [{"team": "Mine", "seat": 10, "added": ["Own Rental"], "dropped": ["Old Guy"]}]},
                  open(os.path.join(d, "league_moves_2026-11-13.json"), "w"))
        json.dump({"moves": [{"team": "Rival", "seat": 3, "added": [], "dropped": ["Free Starter"]}]},
                  open(os.path.join(d, "league_moves_2026-11-14_pm.json"), "w"))
        json.dump({"moves": [{"team": "Rival", "seat": 3, "added": ["Ancient"], "dropped": []}]},
                  open(os.path.join(d, "league_moves_2026-11-01.json"), "w"))
        added, dropped = RW.moves("2026-11-15", 7, d)
        self.assertEqual(added, {LI.norm("Own Rental"): ("2026-11-13", "Mine", 10)})
        self.assertEqual(dropped[LI.norm("Free Starter")], ("2026-11-14", "Rival", 3))
        self.assertEqual(RW.moves("2026-11-15", 1, d), ({}, {}))

    def test_an_add_is_dated_from_the_first_record_of_the_current_spell(self):
        d = tempfile.mkdtemp()

        def rec(name, added=(), dropped=()):
            with open(os.path.join(d, name), "w") as f:
                json.dump({"moves": [{"team": "Mine", "seat": 10, "added": list(added), "dropped": list(dropped)}]}, f)
        rec("league_moves_2026-11-10.json", added=["Back Again"])
        rec("league_moves_2026-11-12.json", dropped=["Back Again"])
        rec("league_moves_2026-11-13_pm.json", added=["Back Again", "Evening Add"])
        rec("league_moves_2026-11-14.json", added=["Evening Add"])       # the morning record repeats last evening's add
        added, dropped = RW.moves("2026-11-15", 7, d)
        self.assertEqual(added[LI.norm("Back Again")][0], "2026-11-13")
        self.assertEqual(added[LI.norm("Evening Add")][0], "2026-11-13")
        self.assertEqual(dropped[LI.norm("Back Again")][0], "2026-11-12")


class HoldCheck(unittest.TestCase):
    def setUp(self):
        self.mine = [p for p in STATE["teams"][0]["players"] if p["slot"] != "IL"]

    def test_a_recent_pickup_who_keeps_starting_is_a_hold(self):
        log = log_of(box("2026-11-12", ("Own Rental", 31, True, "Own Rental")), box("2026-11-14", ("Own Rental", 33, True, "Own Rental")))
        rows = RW.hold_check(log, self.mine, "2026-11-15", added={LI.norm("Own Rental"): ("2026-11-11", "Mine", 10)}, owner_seat=10)
        self.assertEqual([(r["player"], r["hold"], r["games_since_add"], r["unjudged"]) for r in rows], [("Own Rental", True, 2, False)])
        self.assertEqual(rows[0]["why"], ["added 2026-11-11"])

    def test_a_pickup_with_no_game_since_the_add_is_unjudged(self):
        # the Anthony Black case (added 10-22, dropped 10-24 before he played)
        log = log_of(box("2026-11-08", ("Own Rental", 26, False, "Own Rental")))
        r = RW.hold_check(log, self.mine, "2026-11-15", added={LI.norm("Own Rental"): ("2026-11-13", "Mine", 10)}, owner_seat=10)[0]
        self.assertEqual((r["unjudged"], r["games_since_add"], r["hold"]), (True, 0, False))

    def test_a_player_named_as_a_drop_is_checked_and_one_start_in_one_game_holds(self):
        # the Christian Braun case: one regular-season game, a 33-minute start, named as the drop
        log = log_of(box("2026-11-12", ("Own Star", 33, True, "Own Star")))
        rows = RW.hold_check(log, self.mine, "2026-11-15", drops=["Own Star"])
        self.assertEqual([(r["player"], r["hold"], r["why"]) for r in rows], [("Own Star", True, ["named as a drop today"])])

    def test_a_bench_player_is_shown_without_a_hold(self):
        log = log_of(box("2026-11-12", ("Own Rental", 20, False, "Own Rental")), box("2026-11-14", ("Own Rental", 21, True, "Own Rental")))
        r = RW.hold_check(log, self.mine, "2026-11-15", drops=["Own Rental"])[0]
        self.assertEqual((r["hold"], r["starts_in_a_row"], r["minutes"]), (False, 1, [20, 21]))

    def test_another_teams_pickup_of_the_same_name_is_not_the_owners(self):
        log = log_of(box("2026-11-12", ("Own Rental", 31, True, "Own Rental")))
        self.assertEqual(RW.hold_check(log, self.mine, "2026-11-15", added={LI.norm("Own Rental"): ("2026-11-11", "Rival", 3)}, owner_seat=10), [])

    def test_nobody_recent_and_nobody_named_is_an_empty_list(self):
        self.assertEqual(RW.hold_check({}, self.mine, "2026-11-15"), [])


class Build(unittest.TestCase):
    def test_the_record_names_its_rule_and_leaves_il_players_out_of_the_hold_check(self):
        a, n = tempfile.mkdtemp(), tempfile.mkdtemp()
        for rec in (box("2026-11-12", ("Free Starter", 30, True, "Free Starter"), ("Own Hurt", 30, True, "Own Hurt")),
                    box("2026-11-14", ("Free Starter", 34, True, "Free Starter"), ("Own Hurt", 30, True, "Own Hurt"))):
            json.dump(rec, open(os.path.join(a, rec["date"] + ".json"), "w"))
        rw = RW.build("2026-11-15", STATE, ["Free Starter"], drops=["Own Hurt"], owner_seat=10, actuals=a, news_dir=n)
        self.assertEqual(rw["rule"], dict(start_run=2, stale_days=7, dropped_days=3, hold_days=7, shown=8))
        self.assertEqual([r["player"] for r in rw["starts_watch"]], ["Free Starter"])
        self.assertEqual(rw["hold_check"], [])
        self.assertEqual(rw["box_scores"], ["2026-11-12", "2026-11-14"])


class Lines(unittest.TestCase):
    RW_REC = {"box_scores": ["2026-10-20", "2026-11-14"], "rule": dict(start_run=2, stale_days=7, dropped_days=3, hold_days=7, shown=1),
              "starts_watch": [dict(player="Free Starter", team="AAA", starts_in_a_row=3, new=False, last_game="2026-11-14", season_games=3,
                                    pooled=True, status=None, dropped={"day": "2026-11-14", "team": "Rival"}, games=3, minutes=[30, 34, 36],
                                    starts=3, line=dict(pts=10.0, reb=4.0, ast=2.0, stl=1.0, blk=0.0, tpm=1.0, tov=1.0)),
                               dict(player="No Line", team="AAA", starts_in_a_row=2, new=True, last_game="2026-11-12", season_games=2,
                                    pooled=False, status=None, dropped=None, games=2, minutes=[28, 31], starts=2,
                                    line=dict(pts=10.0, reb=4.0, ast=2.0, stl=1.0, blk=0.0, tpm=1.0, tov=1.0))],
              "hold_check": [dict(player="Own Rental", why=["added 2026-11-13"], added="2026-11-13", games_since_add=0, unjudged=True,
                                  starts_in_a_row=0, hold=False, season_games=1, games=1, minutes=[26], starts=0,
                                  line=dict(pts=10.0, reb=4.0, ast=2.0, stl=1.0, blk=0.0, tpm=1.0, tov=1.0)),
                             dict(player="Own Star", why=["named as a drop today"], added=None, games_since_add=None, unjudged=False,
                                  starts_in_a_row=2, hold=True, season_games=2, games=2, minutes=[33, 35], starts=2,
                                  line=dict(pts=10.0, reb=4.0, ast=2.0, stl=1.0, blk=0.0, tpm=1.0, tov=1.0))]}

    def test_the_watch_says_it_is_a_screen_and_shows_the_cap(self):
        L = RW.watch_lines(self.RW_REC)
        self.assertIn("2 free players have started the last 2 games", L[0])
        self.assertIn("not a pick", L[0])
        self.assertEqual(len(L), 3)      # both rows are news (a fresh drop, a new run): news is never cut by the cap
        self.assertIn("**Free Starter** (AAA): 3 starts in a row; last 3: 30/34/36 min, 3 starts; 10 pts", L[1])
        self.assertIn("dropped 2026-11-14 by Rival", L[1])

    def test_standing_rows_fill_the_list_to_the_cap_and_the_count_is_said(self):
        quiet = [dict(self.RW_REC["starts_watch"][0], player=f"Standing {i}", new=False, dropped=None) for i in range(3)]
        L = RW.watch_lines(dict(self.RW_REC, starts_watch=quiet))
        self.assertIn("3 free players", L[0])
        self.assertIn("; 1 shown", L[0])
        self.assertEqual(len(L), 2)

    def test_a_player_with_no_pool_line_says_the_scan_cannot_score_him(self):
        rec = dict(self.RW_REC, rule=dict(self.RW_REC["rule"], shown=8))
        self.assertIn("NEW; no line in the pool, so the waiver scan cannot score him", RW.watch_lines(rec)[2])

    def test_the_hold_check_says_unjudged_and_hold(self):
        L = RW.hold_lines(self.RW_REC)
        self.assertIn("**Own Rental** (added 2026-11-13; 0 games since the add)", L[0])
        self.assertIn("has not played since you added him", L[0])
        self.assertIn("**HOLD?** he started his last 2 games", L[1])

    def test_an_empty_record_and_an_error_read_plainly(self):
        empty = dict(self.RW_REC, starts_watch=[], hold_check=[])
        self.assertEqual(RW.watch_lines(empty), ["No free player has started his last 2 games."])
        self.assertIn("None of your active players", RW.hold_lines(empty)[0])
        self.assertEqual(RW.watch_lines({"error": "KeyError: 'x'"}), ["Not available today (KeyError: 'x')."])
        self.assertEqual(RW.hold_lines(None), ["Not available today (no record)."])


if __name__ == "__main__":
    unittest.main()
