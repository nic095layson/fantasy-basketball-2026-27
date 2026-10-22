#!/usr/bin/env python3
"""Red-first tests for scripts/box_pull.py (in-season tool, Council 2026-10-19 decision 5: ESPN primary,
Basketball-Reference second outlet). Fixtures are trimmed copies of real fetches made 2026-10-19
(scripts/fixtures/): an ESPN scoreboard and one summary for 2026-10-16 (preseason, MIA at ORL), and the two
basic box tables of Basketball-Reference's 202604100ATL page.

    python3 scripts/test_box_pull.py
"""
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import box_pull as B  # noqa: E402

FX = os.path.join(HERE, "fixtures")


class Espn(unittest.TestCase):
    def setUp(self):
        self.sb = json.load(open(os.path.join(FX, "espn_scoreboard_2026-10-16.json")))
        self.sm = json.load(open(os.path.join(FX, "espn_summary_401898406_2026-10-16.json")))

    def test_scoreboard_lists_final_events(self):
        ev = B.espn_events(self.sb)
        self.assertEqual(len(ev), 12)
        self.assertEqual(ev[0]["id"], "401898406")
        self.assertTrue(all(e["final"] for e in ev))

    def test_summary_parses_a_known_line(self):
        rows = B.parse_espn_summary(self.sm)
        w = next(r for r in rows if r["name"] == "Andrew Wiggins")
        self.assertEqual((w["team"], w["min"], w["pts"], w["fgm"], w["fga"], w["tpm"], w["tpa"], w["ftm"], w["fta"],
                          w["reb"], w["ast"], w["tov"], w["stl"], w["blk"]), ("MIA", 15, 13, 4, 7, 1, 3, 4, 5, 2, 1, 0, 2, 0))
        self.assertTrue(w["starter"]); self.assertFalse(w["dnp"]); self.assertEqual(w["espn_id"], "3059319")

    def test_dashes_in_a_live_line_parse_as_zero_and_dnp(self):
        # seen live 2026-10-16: a listed athlete with stats ['--', '--', ...] (did not play, no DNP flag)
        sm = json.loads(json.dumps(self.sm))
        a = sm["boxscore"]["players"][0]["statistics"][0]["athletes"][0]
        a["stats"] = ["--"] * len(a["stats"]); a["didNotPlay"] = False
        r = B.parse_espn_summary(sm)[0]
        self.assertEqual((r["min"], r["pts"], r["fga"]), (0, 0, 0)); self.assertTrue(r["dnp"])

    def test_dnp_rows_carry_zero_minutes_and_the_flag(self):
        rows = B.parse_espn_summary(self.sm)
        dnp = [r for r in rows if r["dnp"]]
        self.assertTrue(all(r["min"] == 0 for r in dnp))
        self.assertEqual(len({r["team"] for r in rows}), 2)


class Bref(unittest.TestCase):
    def test_basic_tables_parse_with_pool_team_codes(self):
        html = open(os.path.join(FX, "bref_202604100ATL_basic_tables.html"), encoding="utf-8").read()
        rows = B.parse_bref_tables(html)
        self.assertEqual(sorted({r["team"] for r in rows}), ["ATL", "CLE"])
        r = next(x for x in rows if x["bref_id"] == "hardeja01")
        self.assertEqual(r["name"], "James Harden")
        for k in ("min", "pts", "fgm", "fga", "tpm", "tpa", "ftm", "fta", "reb", "ast", "tov", "stl", "blk"):
            self.assertIn(k, r)
        self.assertTrue(all(isinstance(x["min"], int) for x in rows))

    def test_team_code_translation(self):
        self.assertEqual(B.pool_team("BRK"), "BKN"); self.assertEqual(B.pool_team("CHO"), "CHA")
        self.assertEqual(B.pool_team("PHO"), "PHX"); self.assertEqual(B.pool_team("ATL"), "ATL")

    def test_index_links_for_a_date(self):
        links = open(os.path.join(FX, "bref_index_2026-04-10_links.txt")).read()
        self.assertEqual(len(B.bref_game_paths(links, "2026-04-10")), 15)


class Reconcile(unittest.TestCase):
    A = dict(name="Some Guard", team="ATL", min=30, pts=20, fgm=8, fga=15, tpm=2, tpa=5, ftm=2, fta=2, reb=5, ast=6, tov=3, stl=1, blk=0)

    def test_identical_lines_match(self):
        rec = B.reconcile([dict(self.A)], [dict(self.A)])
        self.assertEqual((rec["matched"], rec["mismatched"], rec["espn_only"], rec["bref_only"]), (1, [], [], []))

    def test_a_differing_cell_is_listed_not_averaged(self):
        b = dict(self.A, reb=6)
        rec = B.reconcile([dict(self.A)], [b])
        self.assertEqual(rec["matched"], 0)
        self.assertEqual(rec["mismatched"][0]["cells"], {"reb": [5, 6]})

    def test_suffix_and_short_first_name_variants_join(self):
        # seen live on 2026-04-10: Robert Williams III / Robert Williams, Ronald Holland II / Ron Holland,
        # Xavier Tillman / Xavier Tillman Sr., Trevon Scott / Tre Scott
        pairs = [("Robert Williams III", "Robert Williams"), ("Ronald Holland II", "Ron Holland"),
                 ("Xavier Tillman", "Xavier Tillman Sr."), ("Trevon Scott", "Tre Scott")]
        e = [dict(self.A, name=a, team="T%d" % i) for i, (a, _) in enumerate(pairs)]
        b = [dict(self.A, name=bn, team="T%d" % i) for i, (_, bn) in enumerate(pairs)]
        rec = B.reconcile(e, b)
        self.assertEqual((rec["matched"], rec["espn_only"], rec["bref_only"]), (4, [], []))

    def test_different_players_with_one_shared_surname_do_not_join(self):
        e = [dict(self.A, name="Keegan Murray", team="SAC")]; b = [dict(self.A, name="Kris Murray", team="SAC")]
        rec = B.reconcile(e, b)
        self.assertEqual(rec["matched"], 0); self.assertEqual(len(rec["espn_only"]), 1)

    def test_a_player_missing_from_one_outlet_is_named(self):
        rec = B.reconcile([dict(self.A)], [])
        self.assertEqual(rec["espn_only"], ["Some Guard (ATL)"])


class Resolve(unittest.TestCase):
    POOL = ["PJ Washington", "Nikola Jokic", "Herbert Jones", "Kristaps Porzingis"]

    def test_dots_and_accents_fold(self):
        res = B.resolve_names([dict(name="P.J. Washington", team="DAL"), dict(name="Nikola Jokić", team="DEN")], self.POOL, {})
        self.assertEqual([r["pool_name"] for r in res], ["PJ Washington", "Nikola Jokic"])

    def test_alias_table_resolves_and_unknown_stays_null(self):
        res = B.resolve_names([dict(name="Herb Jones", team="NOP"), dict(name="Nobody Here", team="X")], self.POOL,
                              {"Herbert Jones": ["Herb Jones"]})
        self.assertEqual(res[0]["pool_name"], "Herbert Jones")
        self.assertIsNone(res[1]["pool_name"])

    def test_record_lists_unpooled_and_never_guesses(self):
        rows = B.resolve_names([dict(name="Nobody Here", team="X", pts=5)], self.POOL, {})
        self.assertIsNone(rows[0]["pool_name"]); self.assertEqual(rows[0]["pts"], 5)

    def test_a_suffix_the_pool_leaves_off_resolves_when_one_name_shares_the_key(self):
        # owner 2026-10-22 (the name-mismatch fix): the kit's file spells "Darius Acuff" and "Dereck Lively"; ESPN's
        # box scores add Jr. / II, and the line was left unpooled
        res = B.resolve_names([dict(name="Darius Acuff Jr.", team="SAC"), dict(name="Dereck Lively II", team="DAL")],
                              self.POOL + ["Darius Acuff", "Dereck Lively"], {})
        self.assertEqual([r["pool_name"] for r in res], ["Darius Acuff", "Dereck Lively"])

    def test_two_pool_names_sharing_the_suffix_free_key_leave_the_line_unpooled(self):
        res = B.resolve_names([dict(name="Gary Payton III", team="GSW"), dict(name="Gary Payton II", team="GSW")],
                              self.POOL + ["Gary Payton", "Gary Payton II"], {})
        self.assertIsNone(res[0]["pool_name"])                    # two candidates: never guessed
        self.assertEqual(res[1]["pool_name"], "Gary Payton II")   # an exact spelling still wins


class Record(unittest.TestCase):
    def test_no_games_writes_an_empty_dated_record_with_receipts(self):
        rec = B.build_record("2026-10-19", [], [], single_source=True, sources={"espn": {"events": 0}, "bref": {"games": 0}})
        self.assertEqual(rec["date"], "2026-10-19"); self.assertEqual(rec["players"], []); self.assertTrue(rec["single_source"])
        self.assertIn("fetched_at_utc", rec)


if __name__ == "__main__":
    unittest.main(verbosity=2)
