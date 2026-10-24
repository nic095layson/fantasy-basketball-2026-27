#!/usr/bin/env python3
"""Red-first tests for scripts/form_board.py (owner 2026-10-23: the minutes & role board — each rostered player's and
free agent's minutes per game, starts, per-36 production and a minutes trend from the box scores on disk, beside the
season line). Every expected figure below is computed by hand from the fixture, not by the code under test.

    python3 scripts/test_form_board.py
"""
import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import form_board as FB  # noqa: E402
import season_lines as SL  # noqa: E402


def box(name, team, mn, starter=True, pts=0, fgm=0, fga=0, tpm=0, tpa=0, ftm=0, fta=0, reb=0, ast=0, tov=0, stl=0, blk=0,
        game="g1", pool_name="same", dnp=False):
    return dict(name=name, espn_id="1", team=team, starter=starter, dnp=dnp, min=mn, pts=pts, fgm=fgm, fga=fga, tpm=tpm,
                tpa=tpa, ftm=ftm, fta=fta, reb=reb, ast=ast, tov=tov, stl=stl, blk=blk, game=game,
                pool_name=(name if pool_name == "same" else pool_name))


def day(date, games, players, season_type=2):
    return dict(date=date, games=[dict(espn_id=g, season_type=season_type) for g in games], players=players)


STATE = dict(as_of="2026-10-23", teams=[
    dict(name="MY TEAM", seat=10, manager="David", players=[dict(player="Alpha Man", slot="PG", status=None),
                                                            dict(player="Bench Guy", slot="BN", status=None),
                                                            dict(player="Hurt Guy", slot="IL", status="O")]),
    dict(name="THEM", seat=11, manager="Cayas", players=[dict(player="Their Star", slot="C", status=None)])])

PULL = dict(free_agents=dict(freeAgents=[dict(name="Luka Dončić", team="LAL", status=None, position="PG,SG"),
                                         dict(name="Kelly Oubre Jr.", team="IND", status=None, position="SF"),   # box: "Kelly Oubre", unpooled
                                         dict(name="Hurt FA", team="MIA", status="O", position="C"),       # in the pool, no game yet
                                         dict(name="Nobody Known", team="BOS", status=None, position="SF")]))
POOL_CSV = "player,team,pos\nLuka Doncic,LAL,PG\nHurt FA,MIA,C\nAlpha Man,DEN,PG\nKelly Oubre Jr.,IND,SF\n"


def records():
    """Two regular-season days, one preseason day, one DNP. Alpha Man: 30 + 36 min, 20 + 16 pts, 10 + 8 fga, starts both.
    Bench Guy: 12 min once, off the bench. Luka Doncic (pool spelling) 34 min once. Their Star 40 min. Hurt Guy DNP."""
    return [
        day("2026-10-16", ["p1"], [box("Alpha Man", "DEN", 25, pts=30, game="p1")], season_type=1),      # preseason: ignored
        day("2026-10-20", ["g1", "g2"], [
            box("Alpha Man", "DEN", 30, pts=20, fgm=8, fga=10, tpm=2, ftm=2, fta=4, reb=6, ast=4, tov=3, stl=1, blk=1, game="g1"),
            box("Luka Doncic", "LAL", 34, pts=28, fgm=10, fga=20, ftm=6, fta=8, reb=8, ast=9, tov=4, game="g2"),
            box("Hurt Guy", "DEN", 0, dnp=True, game="g1"),
            box("Mystery Man", "BOS", 20, pts=9, game="g2", pool_name=None)]),
        day("2026-10-22", ["g3", "g4"], [
            box("Alpha Man", "DEN", 36, pts=16, fgm=6, fga=8, tpm=1, ftm=3, fta=3, reb=4, ast=6, tov=1, stl=2, blk=0, game="g3"),
            box("Bench Guy", "DAL", 12, starter=False, pts=4, fgm=2, fga=4, reb=3, game="g3"),
            box("Their Star", "NYK", 40, pts=30, fgm=12, fga=24, reb=10, game="g4"),
            box("Kelly Oubre", "IND", 28, pts=4, game="g4", pool_name=None)]),              # the box puller missed the alias
    ]


class GameLog(unittest.TestCase):
    def test_regular_season_games_only_and_dnp_excluded(self):
        log = FB.game_log(records())
        self.assertEqual([g["min"] for g in log["Alpha Man"]], [30, 36])      # the 25-minute preseason game is not there
        self.assertNotIn("Hurt Guy", log)
        self.assertEqual(log["Mystery Man"][0]["unpooled"], True)

    def test_summary_arithmetic_by_hand(self):
        s = FB.summarize(FB.game_log(records())["Alpha Man"])
        self.assertEqual(s["games"], 2); self.assertEqual(s["starts"], 2)
        self.assertAlmostEqual(s["mpg"], 33.0)
        self.assertAlmostEqual(s["per36"]["pts"], 36 * 36 / 66, places=3)     # 36 pts in 66 min
        self.assertAlmostEqual(s["per36"]["ast"], 10 * 36 / 66, places=3)
        self.assertAlmostEqual(s["per36"]["tov"], 4 * 36 / 66, places=3)
        self.assertAlmostEqual(s["fg"]["pct"], 14 / 18, places=4)             # 8/10 + 6/8
        self.assertAlmostEqual(s["ft"]["pct"], 5 / 7, places=4)
        self.assertEqual(s["role"], "starter")

    def test_trend_is_null_under_four_games_and_signed_at_four(self):
        self.assertIsNone(FB.summarize(FB.game_log(records())["Alpha Man"])["trend"])
        log = [dict(date=f"2026-10-2{i}", min=m, starter=True, pts=0, fgm=0, fga=0, tpm=0, ftm=0, fta=0, reb=0, ast=0, tov=0, stl=0, blk=0)
               for i, m in enumerate([18, 30, 31, 32])]
        s = FB.summarize(log)
        self.assertAlmostEqual(s["last3_mpg"], 31.0); self.assertAlmostEqual(s["prior_mpg"], 18.0)
        self.assertEqual(s["trend"], "up")                                    # +13 over the ±6 threshold
        self.assertEqual(FB.summarize(log[::-1])["trend"], "flat")           # 32 then 31,30,18: last3 26.3 vs 32 = -5.7, inside the band
        down = [dict(g, min=m) for g, m in zip(log, [32, 31, 20, 18])]
        self.assertEqual(FB.summarize(down)["trend"], "down")                 # last3 23.0 vs 32 = -9
        flat = [dict(g, min=30) for g in log]
        self.assertEqual(FB.summarize(flat)["trend"], "flat")

    def test_role_flags(self):
        log = FB.game_log(records())
        self.assertEqual(FB.summarize(log["Bench Guy"])["role"], "bench")
        mixed = log["Alpha Man"] + [dict(log["Alpha Man"][0], starter=False)]
        self.assertEqual(FB.summarize(mixed)["role"], "mixed")


class Build(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.act = os.path.join(self.d, "actuals"); os.makedirs(self.act)
        for r in records():
            json.dump(r, open(os.path.join(self.act, f"{r['date']}.json"), "w"))
        self.state = os.path.join(self.d, "state.json"); json.dump(STATE, open(self.state, "w"))
        self.pull = os.path.join(self.d, "pull_2026-10-23.json"); json.dump(PULL, open(self.pull, "w"))
        self.pool = os.path.join(self.d, "pool.csv"); open(self.pool, "w").write(POOL_CSV)
        self.rec = FB.build("2026-10-23", dict(actuals=self.act, state=self.state, pull=self.pull, pool=self.pool))

    def row(self, name):
        return next(r for r in self.rec["rows"] if r["name"] == name)

    def test_rostered_rows_carry_owner_slot_and_mine(self):
        a = self.row("Alpha Man")
        self.assertEqual((a["owner"], a["seat"], a["mine"], a["slot"]), ("MY TEAM", 10, True, "PG"))
        self.assertEqual((self.row("Their Star")["owner"], self.row("Their Star")["mine"]), ("THEM", False))
        self.assertEqual(self.row("Hurt Guy")["games"], 0)                   # rostered, no game: still a row

    def test_free_agents_resolve_yahoo_spelling_and_unknown_names_are_listed(self):
        l = self.row("Luka Doncic")
        self.assertEqual((l["owner"], l["fa"], l["yahoo_name"]), (None, True, "Luka Dončić"))
        self.assertEqual(self.rec["fa_unresolved"], ["Nobody Known"])             # in neither the pool nor a box score
        self.assertEqual((self.row("Hurt FA")["fa"], self.row("Hurt FA")["games"], self.row("Hurt FA")["nba"]), (True, 0, "MIA"))
        self.assertEqual(self.rec["unpooled_with_games"], ["Mystery Man"])   # Kelly Oubre is pooled through the pool spelling
        k = self.row("Kelly Oubre Jr.")                                         # the pool's spelling wins; the box's games are his
        self.assertEqual((k["fa"], k["games"], k["mpg"], k["box_name"]), (True, 1, 28.0, "Kelly Oubre"))

    def test_totals_agree_with_season_lines_on_the_same_files(self):
        t = SL.totals(SL.load_actuals(self.act))
        for r in self.rec["rows"]:
            if r["games"]:
                k = r["box_name"]                                             # the box scores' key for this player
                self.assertEqual(r["games"], t[k]["games"], r["name"])
                self.assertAlmostEqual(r["mpg"] * r["games"], t[k]["min"], places=6, msg=r["name"])

    def test_rows_sorted_by_minutes_and_counts_in_the_record(self):
        names = [r["name"] for r in self.rec["rows"] if r["games"]]
        self.assertEqual(names[:2], ["Their Star", "Luka Doncic"])            # 40, 34, then Alpha 33
        self.assertEqual(self.rec["counts"], dict(rostered=4, free_agents=3, with_games=5, no_game=2, days=2))
        self.assertEqual(self.rec["window"], ["2026-10-20", "2026-10-22"])
        self.assertEqual(self.rec["method"]["trend_min_games"], 4)

    def test_cli_writes_the_record_and_prints_pass(self):
        out = os.path.join(self.d, "form")
        p = subprocess.run([sys.executable, os.path.join(HERE, "form_board.py"), "--date", "2026-10-23", "--actuals", self.act,
                            "--state", self.state, "--pull", self.pull, "--pool", self.pool, "--out-dir", out, "--ledger", ""],
                           capture_output=True, text=True)
        self.assertIn("FORM BOARD: PASS", p.stdout, p.stdout + p.stderr)
        rec = json.load(open(os.path.join(out, "form_2026-10-23.json")))
        self.assertEqual(rec["counts"]["rostered"], 4)
        with open(os.path.join(out, "form_2026-10-23.csv")) as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(rows[0]["name"], "Their Star")


if __name__ == "__main__":
    unittest.main(verbosity=2)
