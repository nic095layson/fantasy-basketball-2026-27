#!/usr/bin/env python3
"""Tests for scripts/draft_check.py (owner 2026-11-11: "implement this with updating tables every Monday, and include
this on the season deck replacing the Movers tab"): the draft-day system beside the season so far, one dated record
per Monday. Known answers are worked by hand on a three-player pool; one parity test reads the real draft-day lines
when the deck repository is beside the kit.

    python3 scripts/test_draft_check.py
"""
import contextlib
import csv
import io
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import draft_check as DC  # noqa: E402
import morning as M  # noqa: E402

LINE = dict(fg_pct=0.5, fga=10.0, ft_pct=0.8, fta=4.0, tpm=1.0, pts=10.0, reb=5.0, ast=3.0, stl=1.0, blk=0.0, tov=2.0)


def line(**k):
    return dict(LINE, **k)


def box(name, team, game, pts, minutes=30, dnp=False, **k):
    b = dict(name=name, pool_name=name, team=team, game=game, min=minutes, dnp=dnp, pts=pts, fgm=5, fga=10, ftm=4, fta=5,
             tpm=1, reb=5, ast=3, stl=1, blk=0, tov=2)
    b.update(k)
    return b


class Fold(unittest.TestCase):
    def test_accents_suffixes_and_punctuation_fold_to_one_key(self):
        self.assertEqual(DC.fold("Nikola Jokić"), DC.fold("Nikola Jokic"))
        self.assertEqual(DC.fold("P.J. Washington"), DC.fold("PJ Washington"))
        self.assertEqual(DC.fold("Kel'el Ware"), DC.fold("Kel’el Ware"))
        self.assertEqual(DC.fold("Jabari Smith Jr."), DC.fold("Jabari Smith"))
        self.assertNotEqual(DC.fold("Jalen Williams"), DC.fold("Jaylin Williams"))


class Scale(unittest.TestCase):
    def test_value_is_the_z_sum_and_one_scale_serves_both_columns(self):
        # three players who differ only in points (10, 20, 30): mean 20, population sd 8.165; every other category
        # is constant (sd 0, scored 0), so value = (pts - 20) / 8.165
        pool = [line(pts=10.0), line(pts=20.0), line(pts=30.0)]
        v = DC.fit_scale(pool, top_n=3)
        self.assertAlmostEqual(v(pool[0]), -1.2247, places=3)
        self.assertAlmostEqual(v(pool[1]), 0.0, places=6)
        self.assertAlmostEqual(v(pool[2]), 1.2247, places=3)
        # a line that was never in the pool is scored on the same mean and sd
        self.assertAlmostEqual(v(line(pts=28.165)), 1.0, places=3)

    def test_turnovers_count_against_and_percentages_weigh_by_attempts(self):
        pool = [line(tov=1.0), line(tov=2.0), line(tov=3.0)]
        v = DC.fit_scale(pool, top_n=3)
        self.assertGreater(v(pool[0]), v(pool[2]))
        pool = [line(fg_pct=0.6, fga=20.0), line(fg_pct=0.6, fga=2.0), line(fg_pct=0.4, fga=11.0)]
        v = DC.fit_scale(pool, top_n=3)
        self.assertGreater(v(pool[0]), v(pool[1]))   # the same rate on more attempts is worth more

    def test_a_pool_of_one_is_refused(self):
        with self.assertRaises(DC.DraftCheckError):
            DC.fit_scale([line()])

    @unittest.skipUnless(os.path.exists(os.path.join(DC.DECK, "arena", "results", "players_v69.csv"))
                         and os.path.exists(os.path.join(DC.DECK, "scripts", "hoops.py")), "deck repository not beside the kit")
    def test_the_scale_agrees_with_the_engines_own_z_scores_on_the_draft_day_lines(self):
        sys.path.insert(0, os.path.join(DC.DECK, "scripts"))
        import hoops
        path = os.path.join(DC.DECK, "arena", "results", "players_v69.csv")
        pre = DC.read_lines(path)
        v = DC.fit_scale(pre.values())
        with open(path, encoding="utf-8") as f:
            rows = [dict(r, **{k: float(r[k]) for k in DC.STATS}) for r in csv.DictReader(f)]
        hoops.zscores(rows)
        engine = {DC.fold(r["player"]): hoops.total_value(r) for r in rows}
        for name in ("Tyrese Haliburton", "Kevin Durant", "Kel'el Ware", "Miles Bridges", "Tyrese Maxey"):
            self.assertAlmostEqual(v(pre[DC.fold(name)]), engine[DC.fold(name)], delta=0.15, msg=name)


class SeasonLines(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()

    def day(self, date, players):
        with open(os.path.join(self.d, f"{date}.json"), "w") as f:
            json.dump(dict(date=date, players=players), f)

    def test_per_game_lines_games_and_team_games(self):
        self.day("2026-10-20", [box("A", "DEN", "g1", 10), box("B", "DEN", "g1", 0, minutes=0, dnp=True)])
        self.day("2026-10-21", [box("A", "DEN", "g2", 30), box("B", "DEN", "g2", 8)])
        out, days = DC.season_lines(self.d, "2026-10-22")
        self.assertEqual(days, ["2026-10-20", "2026-10-21"])
        la, ga, tga = out["a"]
        self.assertEqual((ga, tga), (2, 2)); self.assertEqual(la["pts"], 20.0)
        self.assertEqual(la["fg_pct"], 0.5)          # 10 makes on 20 attempts, not a mean of rates
        lb, gb, tgb = out["b"]
        self.assertEqual((gb, tgb), (1, 2)); self.assertEqual(lb["pts"], 8.0)   # the DNP is no game for him, a game for his team

    def test_the_window_starts_at_the_season_and_stops_before_the_record_date(self):
        self.day("2026-10-12", [box("A", "DEN", "pre", 50)])     # preseason: before SEASON_START
        self.day("2026-10-20", [box("A", "DEN", "g1", 10)])
        self.day("2026-10-26", [box("A", "DEN", "g2", 40)])      # the record's own Monday: not counted
        out, days = DC.season_lines(self.d, "2026-10-26")
        self.assertEqual(days, ["2026-10-20"]); self.assertEqual(out["a"][0]["pts"], 10.0)

    def test_a_day_with_no_game_is_not_a_box_score_day(self):
        self.day("2026-10-20", [box("A", "DEN", "g1", 10)])
        self.day("2026-10-21", [])
        self.assertEqual(DC.season_lines(self.d, "2026-10-25")[1], ["2026-10-20"])


class Spearman(unittest.TestCase):
    def test_known_answers(self):
        self.assertEqual(DC.spearman([1, 2, 3, 4], [1, 2, 3, 4]), 1.0)
        self.assertEqual(DC.spearman([1, 2, 3, 4], [4, 3, 2, 1]), -1.0)
        self.assertEqual(DC.spearman([1, 2, 3, 4, 5], [2, 1, 4, 3, 5]), 0.8)
        self.assertIsNone(DC.spearman([1, 2], [2, 1]))


def world(d, standings=True, games=6):
    """A three-player league on disk: lines, a two-turn draft card, two seeds of the draft-day simulation, box scores,
    one finished week, the league state and the Monday pull."""
    j = lambda name, obj: (json.dump(obj, open(os.path.join(d, name), "w")), os.path.join(d, name))[1]
    lines = os.path.join(d, "lines.csv")
    with open(lines, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["player", "team", "pos"] + list(DC.STATS) + ["note"])
        for name, pts in (("Star One", 30.0), ("Mid Two", 20.0), ("Low Three", 10.0)):
            w.writerow([name, "DEN", "G"] + [dict(LINE, pts=pts)[k] for k in DC.STATS] + [""])
    card = j("card.json", [dict(pick=10, actual="Star One", rows=[dict(n="Star One", target=True), dict(n="Mid Two")]),
                           dict(pick=15, actual="Low Three", rows=[dict(n="Mid Two", target=True), dict(n="Low Three")])])
    cat = lambda v: {c: v for c in DC.CATS}
    sims = [j(f"sim{i}.json", dict(teams={"10": dict(champ=20.0 + i, cat_win_pct=dict(cat(60.0), AST=30.0 + 2 * i)),
                                           "3": dict(champ=30.0, cat_win_pct=cat(50.0)),
                                           "5": dict(champ=5.0, cat_win_pct=cat(40.0))})) for i in (0, 1)]
    act = os.path.join(d, "actuals"); os.makedirs(act)
    for g in range(games):
        day = f"2026-10-{20 + g:02d}"
        json.dump(dict(date=day, players=[box("Star One", "DEN", f"g{g}", 20), box("Mid Two", "DEN", f"g{g}", 20),
                                          box("Low Three", "DEN", f"g{g}", 30, dnp=g >= 2, minutes=0 if g >= 2 else 30)]),
                  open(os.path.join(act, f"{day}.json"), "w"))
    weeks = os.path.join(d, "weeks"); os.makedirs(weeks)
    json.dump(dict(week=1, owner=dict(won=["FG%", "PTS"], lost=["AST"], tied=["TO"])), open(os.path.join(weeks, "week_1.json"), "w"))
    json.dump(dict(week=2, owner=dict(opponent="X")), open(os.path.join(weeks, "week_2.json"), "w"))   # not finished: no result
    state = j("state.json", dict(teams=[dict(name="MINE", seat=10), dict(name="RIVAL", seat=3), dict(name="LAST", seat=5)]))
    table = [dict(name="RIVAL", rank="1", wins="6", losses="3", ties=0), dict(name="MINE", rank="2", wins="5", losses="3", ties=1),
             dict(name="LAST", rank="3", wins="2", losses="7", ties=0)]
    pull = j("pull.json", dict(standings=dict(standings=table) if standings else {}))
    return dict(lines=lines, card=card, sims=sims, actuals=act, weeks=weeks, league_state=state, pull=pull)


class Build(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(); self.paths = world(self.d)
        self.rec = DC.build("2026-10-26", self.paths)

    def test_the_window_and_the_weeks_graded(self):
        self.assertEqual(self.rec["window"], ["2026-10-20", "2026-10-25"]); self.assertEqual(self.rec["days"], 6)
        self.assertEqual(self.rec["weeks_graded"], [1])

    def test_picks_carry_draft_day_and_actual_value_with_games(self):
        star, low = self.rec["picks"]
        self.assertEqual((star["pick"], star["name"], star["games"], star["team_games"]), (10, "Star One", 6, 6))
        self.assertEqual((star["pre"], star["pre_rank"]), (1.22, 1))      # (30 - 20) / 8.165
        self.assertEqual(star["act"], 0.0)                                 # 20 a game on the draft-day scale
        self.assertEqual((low["pick"], low["games"], low["team_games"]), (15, 2, 6))
        self.assertEqual(low["pre"], -1.22); self.assertEqual(low["act"], 1.22)   # 30 a game, in two games
        self.assertIsNone(low["act_rank"])                                 # fewer than MIN_GAMES: valued, not ranked

    def test_preferred_lists_only_the_turns_where_the_card_wanted_someone_else(self):
        self.assertEqual([(q["pick"], q["mine"]["name"], q["card"]["name"]) for q in self.rec["preferred"]],
                         [(15, "Low Three", "Mid Two")])

    def test_teams_set_the_draft_day_title_share_beside_the_standings(self):
        t = {x["name"]: x for x in self.rec["teams"]}
        self.assertEqual([x["name"] for x in self.rec["teams"]], ["RIVAL", "MINE", "LAST"])
        self.assertEqual((t["MINE"]["pre_title"], t["MINE"]["pre_rank"], t["MINE"]["rank"], t["MINE"]["mine"]), (20.5, 2, 2, True))
        self.assertEqual((t["MINE"]["wins"], t["MINE"]["losses"], t["MINE"]["ties"]), (5, 3, 1))
        self.assertEqual((t["RIVAL"]["pre_title"], t["RIVAL"]["pre_rank"]), (30.0, 1))
        self.assertEqual(self.rec["team_rank_agreement"], 1.0)

    def test_cats_set_the_plan_beside_the_weeks_won(self):
        c = {x["cat"]: x for x in self.rec["cats"]}
        self.assertEqual((c["AST"]["plan"], c["AST"]["won"], c["AST"]["lost"]), (31.0, 0, 1))   # mean of the two seeds
        self.assertEqual((c["FG%"]["plan"], c["FG%"]["won"]), (60.0, 1))
        self.assertEqual(c["TO"]["tied"], 1); self.assertEqual((c["REB"]["won"], c["REB"]["lost"]), (0, 0))

    def test_the_scatter_holds_players_with_enough_games_and_marks_the_owners(self):
        self.assertEqual({d["name"]: d["mine"] for d in self.rec["scatter"]}, {"Star One": True, "Mid Two": False})

    def test_sources_are_pinned_by_hash(self):
        self.assertEqual(set(self.rec["sources"]), {"lines", "card", "pull", "sim_2026", "sim_2027"})
        self.assertTrue(all(len(v["sha256"]) == 64 for v in self.rec["sources"].values()))

    def test_the_pass_line(self):
        self.assertEqual(DC.pass_line(self.rec),
                         "DRAFT CHECK: PASS — 2026-10-26: box scores 2026-10-20 to 2026-10-25 (6 days), 2 picks, 2 players "
                         "with 5+ games, rank agreement None; you were ranked 2 on draft day and stand 2 (5-3-1)")


class Halts(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()

    def test_a_pull_without_standings_halts(self):
        with self.assertRaises(DC.DraftCheckError) as e:
            DC.build("2026-10-26", world(self.d, standings=False))
        self.assertIn("carries no standings", str(e.exception))

    def test_a_missing_draft_file_halts_and_names_it(self):
        p = world(self.d); os.remove(p["card"])
        with self.assertRaises(DC.DraftCheckError) as e:
            DC.build("2026-10-26", p)
        self.assertIn("missing card", str(e.exception))

    def test_no_box_score_day_halts(self):
        with self.assertRaises(DC.DraftCheckError) as e:
            DC.build("2026-10-20", world(self.d))
        self.assertIn("no box-score day", str(e.exception))

    def test_a_standings_team_unknown_to_the_league_state_halts(self):
        p = world(self.d)
        json.dump(dict(teams=[dict(name="MINE", seat=10)]), open(p["league_state"], "w"))
        with self.assertRaises(DC.DraftCheckError) as e:
            DC.build("2026-10-26", p)
        self.assertIn("not in the league state", str(e.exception))


class Cli(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(); self.out = os.path.join(self.d, "out")
        paths = world(self.d)
        self._dp, self._argv = DC.default_paths, sys.argv
        DC.default_paths = lambda date: paths

    def tearDown(self):
        DC.default_paths, sys.argv = self._dp, self._argv

    def run_main(self, *args):
        sys.argv = ["draft_check.py", "--out", self.out] + list(args)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = DC.main()
        return code, buf.getvalue().strip()

    def test_a_run_writes_the_dated_record_and_a_second_run_does_not_rewrite_it(self):
        code, line1 = self.run_main("--date", "2026-10-26")
        self.assertEqual(code, 0); self.assertTrue(line1.startswith("DRAFT CHECK: PASS — 2026-10-26: box scores"))
        f = os.path.join(self.out, "draft_check_2026-10-26.json")
        before = open(f).read()
        self.assertEqual(json.loads(before)["date"], "2026-10-26")
        open(f, "w").write(before.replace("Star One", "Star 0ne"))
        code, line2 = self.run_main("--date", "2026-10-26")
        self.assertEqual(code, 0); self.assertIn("the record exists and is not rewritten", line2)
        self.assertIn("Star 0ne", open(f).read())
        self.run_main("--date", "2026-10-26", "--force")
        self.assertNotIn("Star 0ne", open(f).read())

    def test_a_halt_prints_one_line_and_exits_1_with_no_record(self):
        code, out = self.run_main("--date", "2026-10-20")
        self.assertEqual(code, 1); self.assertTrue(out.startswith("DRAFT CHECK: HALT — no box-score day"))
        self.assertFalse(os.path.exists(os.path.join(self.out, "draft_check_2026-10-20.json")))

    def test_latest_is_the_newest_record_on_or_before_the_day(self):
        os.makedirs(self.out)
        for day in ("2026-11-02", "2026-11-09"):
            open(os.path.join(self.out, f"draft_check_{day}.json"), "w").write("{}")
        base = lambda p: p and os.path.basename(p)
        self.assertEqual(base(DC.latest("2026-11-08", self.out)), "draft_check_2026-11-02.json")
        self.assertEqual(base(DC.latest("2026-11-09", self.out)), "draft_check_2026-11-09.json")
        self.assertIsNone(DC.latest("2026-11-01", self.out))


class MorningStep(unittest.TestCase):
    def test_the_step_runs_on_mondays_only_before_the_deck_and_is_non_fatal(self):
        mon = M.steps("2026-11-09"); names = [s["name"] for s in mon]
        self.assertIn("draft check", names)
        s = mon[names.index("draft check")]
        self.assertFalse(s["fatal"]); self.assertEqual(s["cmd"][-2:], ["--date", "2026-11-09"])
        self.assertTrue(s["cmd"][-3].endswith("draft_check.py"))
        self.assertLess(names.index("draft check"), names.index("season deck"))
        self.assertNotIn("draft check", [s["name"] for s in M.steps("2026-11-10")])


if __name__ == "__main__":
    unittest.main()
