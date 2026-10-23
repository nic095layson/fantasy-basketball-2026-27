#!/usr/bin/env python3
"""Red-first tests for scripts/week_matchup.py (owner 2026-10-21: "show a Week 1 Categories against my opponent,
updated from the game results the day prior ... show a 'faded' color which are the projections ... forecast what
free agent player pickups could contribute to me winning the categories I am deficient in"). Every expected figure
below is computed by hand from the fixture, not by the code under test.

    python3 scripts/test_week_matchup.py
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import week_matchup as WM  # noqa: E402
import test_flaim_live as TFL  # noqa: E402  (the Flaim response shapes)

ALLPOS = ["PG", "SG", "SF", "PF", "C"]


def box(**kw):
    s = dict(fgm=0, fga=0, ftm=0, fta=0, tpm=0, pts=0, reb=0, ast=0, stl=0, blk=0, tov=0)
    s.update(kw)
    return s


def dump(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f)
    return path


def line(**kw):
    s = dict(fg_pct=0.0, fga=0.0, ft_pct=0.0, fta=0.0, tpm=0.0, pts=0.0, reb=0.0, ast=0.0, stl=0.0, blk=0.0, tov=0.0)
    s.update(kw)
    return s


class Window(unittest.TestCase):
    def test_to_date_runs_from_the_weeks_first_day_through_yesterday(self):
        self.assertEqual(WM.days_to_date("2026-10-22", "2026-10-20"), ["2026-10-20", "2026-10-21"])
        self.assertEqual(WM.days_to_date("2026-10-20", "2026-10-20"), [])

    def test_remaining_runs_from_today_through_the_weeks_last_day(self):
        self.assertEqual(WM.days_remaining("2026-10-24", "2026-10-25"), ["2026-10-24", "2026-10-25"])


class BoxScores(unittest.TestCase):
    def test_only_pooled_regular_season_players_who_played_are_read(self):
        rec = dict(games=[dict(espn_id="g1", season_type=2), dict(espn_id="g2", season_type=1)],
                   players=[dict(name="A", pool_name="A", dnp=False, game="g1", **box(pts=10)),
                            dict(name="B", pool_name="B", dnp=True, game="g1", **box()),
                            dict(name="C", pool_name=None, dnp=False, game="g1", **box(pts=7)),
                            dict(name="D", pool_name="D", dnp=False, game="g2", **box(pts=9))])
        got = WM.played(rec)
        self.assertEqual(sorted(got), ["A"])
        self.assertEqual(got["A"]["pts"], 10)

    def test_given_the_cards_names_a_line_is_read_under_the_cards_spelling(self):
        # owner 2026-10-22 (the name-mismatch fix): the box pull files lines under the kit's spelling or none at all;
        # the card's rosters carry Yahoo's. Acuff's line had no pool name; Cameron Johnson's is filed as "Cam Johnson"
        rec = dict(games=[dict(espn_id="g1", season_type=2)],
                   players=[dict(name="Darius Acuff Jr.", pool_name=None, dnp=False, game="g1", **box(pts=12)),
                            dict(name="Cameron Johnson", pool_name="Cam Johnson", dnp=False, game="g1", **box(pts=9)),
                            dict(name="A", pool_name="A", dnp=False, game="g1", **box(pts=10)),
                            dict(name="Nobody Here", pool_name=None, dnp=False, game="g1", **box(pts=7))])
        got = WM.played(rec, names=["Darius Acuff Jr.", "Cameron Johnson", "A"])
        self.assertEqual(sorted(got), ["A", "Cameron Johnson", "Darius Acuff Jr."])
        self.assertEqual((got["Darius Acuff Jr."]["pts"], got["Cameron Johnson"]["pts"]), (12, 9))

    def test_the_recent_box_scores_are_read_under_the_cards_spelling_too(self):
        with tempfile.TemporaryDirectory() as d:
            dump(dict(games=[dict(espn_id="g1", season_type=2)],
                      players=[dict(name="Darius Acuff Jr.", pool_name=None, team="SAC", dnp=False, game="g1", **box(pts=12))]),
                 os.path.join(d, "2026-10-21.json"))
            (day, who, teams), = WM._recent_boxes(d, "2026-10-22", names=["Darius Acuff Jr."])
            self.assertEqual((day, who), ("2026-10-21", {"Darius Acuff Jr.": ("SAC", False)}))


class ToDate(unittest.TestCase):
    def test_sums_the_rostered_players_who_played_and_nobody_else(self):
        roster = [dict(player="A", positions=["C"], value=2.0), dict(player="B", positions=["PG"], value=1.0)]
        days = {"d1": {"A": box(fgm=5, fga=10, ftm=2, fta=4, tpm=1, pts=13, reb=8, ast=2, stl=1, blk=2, tov=3),
                       "Z": box(pts=40)},
                "d2": {"B": box(fgm=3, fga=9, ftm=4, fta=5, tpm=2, pts=12, reb=3, ast=7, stl=2, blk=0, tov=4)}}
        r = WM.to_date(roster, days)
        t = r["totals"]
        self.assertEqual((t["fgm"], t["fga"], t["ftm"], t["fta"]), (8, 19, 6, 9))
        self.assertEqual((t["tpm"], t["pts"], t["reb"], t["ast"], t["stl"], t["blk"], t["tov"]), (3, 25, 11, 9, 3, 2, 7))
        v = WM.cat_values(t)
        self.assertAlmostEqual(v["FG%"], 8 / 19)
        self.assertAlmostEqual(v["FT%"], 6 / 9)
        self.assertEqual(r["days"]["d1"]["counted"], ["A"])

    def test_more_than_ten_who_played_count_ten_and_the_lowest_value_sits(self):
        roster = [dict(player=f"P{i}", positions=ALLPOS, value=float(i)) for i in range(1, 12)]
        days = {"d1": {f"P{i}": box(pts=i) for i in range(1, 12)}}
        r = WM.to_date(roster, days)
        self.assertEqual(r["days"]["d1"]["benched"], ["P1"])
        self.assertEqual(r["totals"]["pts"], sum(range(2, 12)))


class Projection(unittest.TestCase):
    def test_line_times_games_times_availability_with_makes_from_attempts(self):
        roster = [dict(player="A", team="DEN", positions=["C"], value=1.0),
                  dict(player="Out", team="DEN", positions=["PG"], value=3.0),
                  dict(player="Idle", team="BOS", positions=["SF"], value=2.0)]
        lines = {"A": line(fg_pct=0.5, fga=10, ft_pct=0.8, fta=5, tpm=1, pts=20, reb=10, ast=3, stl=1, blk=2, tov=2),
                 "Out": line(pts=30), "Idle": line(pts=25)}
        sched = {"d1": {"DEN"}, "d2": {"DEN"}}
        r = WM.remaining(roster, sched, {"A": 0.5, "Out": 0.0}, lines)
        t = r["totals"]
        self.assertAlmostEqual(t["pts"], 20.0)        # 20 x 2 games x 0.5
        self.assertAlmostEqual(t["fga"], 10.0)        # 10 x 2 x 0.5
        self.assertAlmostEqual(t["fgm"], 5.0)         # 0.5 x 10
        self.assertAlmostEqual(t["ftm"], 4.0)         # 0.8 x 5 x 2 x 0.5
        self.assertAlmostEqual(t["reb"], 10.0)
        self.assertEqual(r["games"], {"A": 2})        # Out never starts; Idle's team has no game

    def test_the_ten_slot_cap_applies_to_projected_days_too(self):
        roster = [dict(player=f"P{i}", team="DEN", positions=ALLPOS, value=float(i)) for i in range(1, 12)]
        lines = {f"P{i}": line(pts=float(i)) for i in range(1, 12)}
        r = WM.remaining(roster, {"d1": {"DEN"}}, {}, lines)
        self.assertAlmostEqual(r["totals"]["pts"], float(sum(range(2, 12))))
        self.assertNotIn("P1", r["games"])

    def test_final_adds_actual_and_projected_and_percentages_pool_the_attempts(self):
        fin = WM.add(box(fgm=8, fga=20, pts=30), dict(box(fgm=5.0, fga=10.0, pts=20.0)))
        self.assertAlmostEqual(WM.cat_values(fin)["FG%"], 13 / 30)
        self.assertAlmostEqual(fin["pts"], 50.0)


class Compare(unittest.TestCase):
    def test_higher_wins_turnovers_lower_wins_equal_ties(self):
        me = dict(WM.cat_values(box(fgm=5, fga=10, ftm=0, fta=0, pts=10, reb=4, tov=3)))
        opp = dict(WM.cat_values(box(fgm=4, fga=10, ftm=0, fta=0, pts=12, reb=4, tov=5)))
        c = WM.compare(me, opp)
        self.assertEqual(c["FG%"], "me")
        self.assertEqual(c["PTS"], "opp")
        self.assertEqual(c["REB"], "tie")
        self.assertEqual(c["TO"], "me")
        self.assertEqual(c["FT%"], "tie")  # no attempts on either side


class Finished(unittest.TestCase):
    def test_finished_and_below_the_median_value_is_a_drop_candidate(self):
        roster = [dict(player=n, team=t, value=v) for n, t, v in
                  [("Star", "BOS", 5.0), ("Mid", "DEN", 3.0), ("Low", "BOS", 1.0), ("Low2", "DEN", 2.0), ("High", "DEN", 4.0)]]
        got = WM.drop_candidates(roster, {"DEN": 2})
        self.assertEqual([c["player"] for c in got], ["Low"])   # Star is finished but above the median
        self.assertEqual(got[0]["value_rank"], 5)
        self.assertEqual(got[0]["of"], 5)


class Pickups(unittest.TestCase):
    def test_the_free_agent_who_flips_a_losing_category_ranks_first(self):
        # me to date: REB 10, BLK 1; opponent final: REB 12, BLK 2; my remaining roster plays nothing more.
        me_td = box(fgm=10, fga=20, ftm=5, fta=6, pts=30, reb=10, ast=5, stl=2, blk=1, tov=4)
        opp_fin = box(fgm=9, fga=20, ftm=4, fta=6, pts=25, reb=12, ast=4, stl=1, blk=2, tov=5)
        roster = [dict(player="Done", team="BOS", positions=["C"], value=-1.0)]
        fas = [dict(player="Blocker", team="DEN", positions=["C"], value=0.5),
               dict(player="Idle", team="BOS", positions=["C"], value=3.0),
               dict(player="Bricks", team="DEN", positions=["C"], value=1.0)]
        lines = {"Blocker": line(blk=2.0, fga=1.0, fg_pct=0.5),
                 "Idle": line(reb=10.0, blk=5.0),
                 "Bricks": line(reb=3.0, fga=20.0, fg_pct=0.1)}
        sched = {"d1": {"DEN"}}
        res = WM.rank_pickups(me_td, opp_fin, roster, "Done", fas, sched, {}, lines, n=3)
        self.assertEqual(res[0]["add"], "Blocker")
        self.assertEqual(res[0]["flips_to_win"], ["BLK"])
        self.assertEqual(res[0]["net"], 1)                     # BLK 1 -> 3 beats 2 (a loss turned into a win)
        bricks = next(r for r in res if r["add"] == "Bricks")
        self.assertEqual(bricks["flips_to_win"], ["REB"])      # 13 beats 12
        self.assertEqual(bricks["flips_to_loss"], ["FG%"])     # 12/40 under 9/20
        self.assertEqual(bricks["net"], 0)
        idle = next(r for r in res if r["add"] == "Idle")
        self.assertEqual((idle["games_left"], idle["net"]), (0, 0))
        self.assertEqual([r["add"] for r in res], ["Blocker", "Bricks", "Idle"])


class ThisWeek(unittest.TestCase):
    """P1 (owner 2026-10-22, "Full build"): each free agent judged by the change in expected categories won this week.
    Method stated before the build: P(win c) = the normal approximation on the final totals (to date fixed; each
    remaining started game adds a*(x*cv)^2 + a*(1-a)*x^2, the season CV; FG%/FT% the binomial floor on remaining
    makes x PCT_MIX_INFL^2); the swap starts tomorrow; drop candidates are the active players below the median value,
    finished or not. Hand figures below use math.erf, not the code under test."""

    @staticmethod
    def phi(z):
        import math
        return 0.5 * (1 + math.erf(z / math.sqrt(2)))

    def test_remaining_carries_the_per_game_variance_of_what_it_projects(self):
        cv = WM.CG.arena.SEASON_CV
        roster = [dict(player="A", team="DEN", positions=["C"], value=1.0)]
        lines = {"A": line(fg_pct=0.5, fga=10, ft_pct=0.8, fta=5, pts=20, blk=2, tov=2)}
        r = WM.remaining(roster, {"d1": {"DEN"}, "d2": {"DEN"}}, {"A": 0.5}, lines)
        self.assertAlmostEqual(r["var"]["PTS"], 2 * (0.5 * (20 * cv["PTS"]) ** 2 + 0.5 * 0.5 * 20 ** 2))
        self.assertAlmostEqual(r["var"]["BLK"], 2 * (0.5 * (2 * cv["BLK"]) ** 2 + 0.25 * 4))
        self.assertAlmostEqual(r["var"]["fg_mk"], 2 * 0.5 * 10 * 0.5 * 0.5)
        self.assertAlmostEqual(r["var"]["ft_mk"], 2 * 0.5 * 5 * 0.8 * 0.2)

    def test_category_chances_are_the_normal_approximation_on_the_final_totals(self):
        import math
        infl = WM.CG.arena.PCT_MIX_INFL
        z = {k: 0.0 for k in ("3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO", "fg_mk", "ft_mk")}
        me_now, opp_now = box(fgm=170, fga=360, pts=560, blk=22, tov=50), box(fgm=160, fga=350, pts=500, blk=24, tov=40)
        me_rem = dict(totals=box(fgm=28.5, fga=60.0), var=dict(z, PTS=1600.0, BLK=9.0, TO=4.0, fg_mk=60 * 0.475 * 0.525))
        opp_rem = dict(totals=box(), var=dict(z, PTS=1600.0, BLK=9.0, TO=4.0))
        p = WM.cat_chances(me_now, me_rem, opp_now, opp_rem)
        self.assertAlmostEqual(p["PTS"], self.phi(60 / math.sqrt(3200)))
        self.assertAlmostEqual(p["BLK"], self.phi(-2 / math.sqrt(18)))
        self.assertAlmostEqual(p["TO"], 1 - self.phi(10 / math.sqrt(8)))           # fewer turnovers wins
        mu, var = (170 + 28.5) / 420, infl ** 2 * 60 * 0.475 * 0.525 / 420 ** 2
        self.assertAlmostEqual(p["FG%"], self.phi((mu - 160 / 350) / math.sqrt(var)))
        self.assertEqual(p["FT%"], 0.5)                                           # no attempts either side: a tie
        self.assertEqual(p["REB"], 0.5)                                           # level and nothing left to play

    def _fixture(self):
        me_now = box(fgm=100, fga=210, ftm=40, fta=50, tpm=20, pts=280, reb=120, ast=60, stl=15, blk=10, tov=30)
        opp_now = box(fgm=100, fga=210, ftm=40, fta=50, tpm=20, pts=240, reb=120, ast=60, stl=15, blk=13, tov=30)
        roster = [dict(player="Keeper", team="BOS", positions=["PG"], value=5.0),
                  dict(player="Scorer", team="DEN", positions=["SF"], value=1.0),
                  dict(player="Done", team="NYK", positions=["PF"], value=0.5)]
        lines = {"Keeper": line(pts=20, reb=5, ast=5, fga=15, fg_pct=0.45, tov=2),
                 "Scorer": line(pts=25, fga=20, fg_pct=0.45, tov=2),
                 "Done": line(pts=5),
                 "Rim": line(blk=2.5, reb=8, pts=7, fga=5, fg_pct=0.6, tov=1),
                 "Gunner": line(pts=18, blk=0.3, fga=15, fg_pct=0.42, tov=2),
                 "TodayOnly": line(blk=4, pts=10, fga=8, fg_pct=0.5),
                 "Idle": line(blk=5, pts=30)}
        sched = {"t0": {"BOS", "DEN", "LAL", "PHX"}, "t1": {"BOS", "DEN", "LAL"}, "t2": {"DEN", "LAL"}}
        fas = [dict(player=n, team=t, positions=["C"], value=0.0) for n, t in
               (("Rim", "LAL"), ("Gunner", "LAL"), ("TodayOnly", "PHX"), ("Idle", "MIA"))]
        return me_now, opp_now, roster, lines, sched, fas

    def scan(self):
        me_now, opp_now, roster, lines, sched, fas = self._fixture()
        opp_rem = dict(totals=box(), var={k: 0.0 for k in ("3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO", "fg_mk", "ft_mk")})
        return WM.scan_this_week(me_now, opp_now, opp_rem, roster, ["Scorer", "Done"], fas, sched, "t0", {}, lines)

    def test_the_category_changes_add_up_to_the_change_in_expected_categories(self):
        for r in self.scan():
            self.assertAlmostEqual(sum(r["d_cat"].values()), r["d_exp"], places=12)
            self.assertEqual(sorted(r["d_cat"]), sorted(WM.CATS))

    def test_a_free_agent_with_no_game_after_today_changes_nothing_when_his_drop_is_done(self):
        me_now, opp_now, roster, lines, sched, fas = self._fixture()
        opp_rem = dict(totals=box(), var={k: 0.0 for k in ("3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO", "fg_mk", "ft_mk")})
        by = {r["add"]: r for r in WM.scan_this_week(me_now, opp_now, opp_rem, roster, ["Done"], fas, sched, "t0", {}, lines)}
        for n in ("TodayOnly", "Idle"):        # PHX plays only today (the swap starts tomorrow); MIA never
            self.assertEqual(by[n]["drop"], "Done")
            self.assertEqual(by[n]["games"], 0)
            self.assertEqual(by[n]["d_exp"], 0.0)

    def test_the_drop_loses_his_remaining_games(self):
        me_now, opp_now, roster, lines, sched, fas = self._fixture()
        opp_rem = dict(totals=box(), var={k: 0.0 for k in ("3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO", "fg_mk", "ft_mk")})
        r = WM.scan_this_week(me_now, opp_now, opp_rem, roster, ["Scorer"], [fas[3]], sched, "t0", {}, lines)[0]
        self.assertEqual((r["add"], r["drop"], r["games"]), ("Idle", "Scorer", 0))
        self.assertLess(r["d_cat"]["PTS"], 0)                  # Scorer's two games after today come off: fewer points,
        self.assertGreater(r["d_cat"]["TO"], 0)                # fewer turnovers (a better TO chance)
        # an add with no games contributes nothing: the whole change is the drop's
        self.assertEqual(r["d_exp_add"], 0.0)
        self.assertEqual(r["d_exp"], r["d_exp_drop"])

    def test_the_drop_alone_is_reported_so_a_drop_that_helps_on_its_own_is_not_credited_to_the_add(self):
        # in this fixture Scorer's .45 shooting and turnovers cost more than his points (safe already) gain
        rows = self.scan()
        rim = next(r for r in rows if r["add"] == "Rim")
        self.assertAlmostEqual(rim["d_exp"], rim["d_exp_drop"] + rim["d_exp_add"], places=12)
        idle = next(r for r in rows if r["add"] == "Idle")
        self.assertGreater(idle["d_exp_drop"], 0)
        self.assertEqual(idle["d_exp_add"], 0.0)

    def test_the_rim_protector_outranks_the_scorer_when_points_are_safe_and_blocks_are_close(self):
        rows = self.scan()
        names = [r["add"] for r in rows]
        self.assertLess(names.index("Rim"), names.index("Gunner"))
        rim = rows[names.index("Rim")]
        self.assertEqual(rim["games"], 2)                      # LAL on t1 and t2; t0 is before the swap
        self.assertGreater(rim["d_cat"]["BLK"], 0)
        self.assertEqual([r["d_exp"] for r in rows], sorted((r["d_exp"] for r in rows), reverse=True))

    def test_swap_candidates_are_the_active_players_below_the_median_finished_or_not(self):
        roster = [dict(player=n, team="BOS", value=v) for n, v in (("A", 5.0), ("B", 3.0), ("C", 1.0), ("D", 2.0), ("E", 4.0))]
        self.assertEqual(WM.swap_candidates(roster), ["C", "D"])


class LineupToday(unittest.TestCase):
    """Owner 2026-10-22: at the 3 PM check, tell me when a bench player with a game today should start. Rules stated
    before the build: an empty slot (a starter with no game or Out, a bench player who plays) always; a worse starter
    when the bench player's season value per game beats his by LINEUP_GAP (1.0) or more, or when starting him adds
    LINEUP_D_EXP (0.05) or more expected categories this week (today's swap only, the rest of the week unchanged)."""

    def me(self, *rows):
        return [dict(player=n, slot=s, positions=pos, team=t) for n, s, pos, t in rows]

    def test_a_bench_player_who_plays_takes_a_starter_slot_whose_player_has_no_game(self):
        me = self.me(("Idle", "C", ["C"], "MIA"), ("Sitter", "BN", ["C"], "BOS"))
        moves = WM.lineup_moves(me, {"BOS"}, {}, {"Idle": 3.0, "Sitter": 0.5})
        self.assertEqual([(m["start"], m["sit"], m["kind"]) for m in moves], [("Sitter", "Idle", "empty")])

    def test_an_out_starter_is_an_empty_slot_too(self):
        me = self.me(("Hurt", "C", ["C"], "BOS"), ("Sitter", "BN", ["C"], "BOS"))
        moves = WM.lineup_moves(me, {"BOS"}, {"Hurt": 0.0}, {"Hurt": 3.0, "Sitter": 0.5})
        self.assertEqual([(m["start"], m["sit"], m["kind"]) for m in moves], [("Sitter", "Hurt", "empty")])

    def test_a_better_bench_player_is_paired_with_the_weakest_starter_he_can_replace(self):
        # ten starters who all play, Star on the bench: the best lineup starts Star over the weakest player he fits
        rows = [("S%d" % i, "UTIL", ["PG", "SG", "SF", "PF", "C"], "BOS") for i in range(10)] + \
               [("Star", "BN", ["PG", "SG", "SF", "PF", "C"], "BOS")]
        value = {"S%d" % i: float(i) for i in range(10)}
        value["Star"] = 5.5
        moves = WM.lineup_moves(self.me(*rows), {"BOS"}, {}, value)
        self.assertEqual([(m["start"], m["sit"], m["kind"], m["gap"]) for m in moves], [("Star", "S0", "better", 5.5)])

    def test_no_move_when_the_lineup_is_already_the_best(self):
        # all ten slots filled by players who play and are worth more than the bench player (with fewer than ten
        # starters a slot is open, and starting the bench player is a real move)
        rows = [("S%d" % i, "UTIL", ["PG", "SG", "SF", "PF", "C"], "BOS") for i in range(10)] + \
               [("Bad", "BN", ["PG", "SG", "SF", "PF", "C"], "BOS")]
        value = {"S%d" % i: 1.0 + i for i in range(10)}
        value["Bad"] = 0.5
        self.assertEqual(WM.lineup_moves(self.me(*rows), {"BOS"}, {}, value), [])

    def test_an_open_slot_with_a_bench_player_who_plays_is_an_empty_slot_move(self):
        me = self.me(("Good", "C", ["C"], "BOS"), ("Bench", "BN", ["C"], "BOS"))
        self.assertEqual([(m["start"], m["sit"], m["kind"]) for m in WM.lineup_moves(me, {"BOS"}, {}, {"Good": 3.0, "Bench": 0.5})],
                         [("Bench", None, "empty")])

    def test_a_bench_player_with_no_game_is_never_suggested(self):
        me = self.me(("Idle", "C", ["C"], "MIA"), ("AlsoIdle", "BN", ["C"], "NYK"))
        self.assertEqual(WM.lineup_moves(me, {"BOS"}, {}, {"Idle": 0.5, "AlsoIdle": 3.0}), [])

    def test_the_week_value_of_todays_swap_is_its_change_in_expected_categories(self):
        # one slot today; Keeper (bench) outscores Scorer's points line, so starting him raises P(win PTS) this week
        me_now = box(fgm=100, fga=210, pts=280, reb=120, blk=10, tov=30)
        opp_now = box(fgm=100, fga=210, pts=280, reb=120, blk=12, tov=30)
        roster = [dict(player="Weak", team="BOS", positions=["C"], value=0.0),
                  dict(player="Strong", team="BOS", positions=["C"], value=2.0)]
        lines = {"Weak": line(pts=4, fga=4, fg_pct=0.4), "Strong": line(pts=30, blk=3, fga=20, fg_pct=0.5)}
        sched = {"t0": {"BOS"}}
        opp_rem = dict(totals=box(), var={k: 0.0 for k in ("3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO", "fg_mk", "ft_mk")})
        d = WM.today_swap_value(me_now, opp_now, opp_rem, roster, ["Weak"], ("Strong", "Weak"), sched, "t0", {}, lines)
        base = WM.cat_chances(me_now, WM.remaining([roster[0]], sched, {}, lines), opp_now, opp_rem)
        new = WM.cat_chances(me_now, WM.remaining([roster[1]], sched, {}, lines), opp_now, opp_rem)
        self.assertAlmostEqual(d, sum(new[c] - base[c] for c in WM.CATS))
        self.assertGreater(d, 0)

    def test_alert_flags_empty_slots_and_gaps_past_either_threshold(self):
        moves = [dict(start="A", sit="X", kind="empty", gap=None, d_exp=0.0),
                 dict(start="B", sit="Y", kind="better", gap=1.2, d_exp=0.01),
                 dict(start="C", sit="Z", kind="better", gap=0.3, d_exp=0.06),
                 dict(start="D", sit="W", kind="better", gap=0.3, d_exp=0.01)]
        self.assertEqual([m["start"] for m in WM.lineup_alerts(moves)], ["A", "B", "C"])


class FreeAgentNotice(unittest.TestCase):
    """Owner 2026-10-22: the Today tab names a free agent whose season value per game beats my weakest non-IL player
    by FA_NOTICE_GAP (1.0) or more (top 3), and the This Week table's best move when it adds 0.10+ expected categories."""

    def test_free_agents_past_the_gap_over_my_weakest_player_best_first_top_three(self):
        mine = [dict(player="Weakest", value=-1.0), dict(player="Fine", value=2.0)]
        fas = [dict(player=n, team="BOS", value=v) for n, v in (("Near", -0.2), ("Big", 1.5), ("Ok", 0.0), ("Mid", 0.4), ("Top", 3.0))]
        n = WM.fa_notice(mine, fas, [])
        self.assertEqual([(r["add"], r["drop"], r["gap"]) for r in n["rows"]], [("Top", "Weakest", 4.0), ("Big", "Weakest", 2.5), ("Mid", "Weakest", 1.4)])
        self.assertIsNone(n["this_week"])

    def test_the_this_week_best_move_shows_only_past_its_bar(self):
        mine = [dict(player="W", value=0.0)]
        self.assertIsNone(WM.fa_notice(mine, [], [dict(add="A", drop="W", d_exp=0.09)])["this_week"])
        self.assertEqual(WM.fa_notice(mine, [], [dict(add="A", drop="W", d_exp=0.12)])["this_week"]["add"], "A")


class WinWeek(unittest.TestCase):
    """Owner 2026-10-22 ("Live + pre-week"): the chance of 5+ of 9 categories from the card's per-category chances,
    categories treated as independent (stated on the tile). Hand figures use math.comb, not the code under test."""

    def test_all_coin_flips_give_exactly_one_half(self):
        self.assertAlmostEqual(WM.win_week_chance([0.5] * 9), 0.5, places=12)

    def test_certain_categories_decide_it(self):
        self.assertEqual(WM.win_week_chance([1.0] * 5 + [0.0] * 4), 1.0)
        self.assertEqual(WM.win_week_chance([1.0] * 4 + [0.0] * 5), 0.0)

    def test_nine_equal_chances_match_the_binomial(self):
        import math
        want = sum(math.comb(9, k) * 0.7 ** k * 0.3 ** (9 - k) for k in range(5, 10))
        self.assertAlmostEqual(WM.win_week_chance([0.7] * 9), want, places=12)


class Record(unittest.TestCase):
    """End to end on fixture files and the real season pool (names from data/season/pool_season.csv)."""

    def setUp(self):
        self.d = tempfile.mkdtemp()
        j = lambda name, obj: dump(obj, os.path.join(self.d, name))
        os.makedirs(os.path.join(self.d, "actuals")); os.makedirs(os.path.join(self.d, "status"))
        pl = lambda n, team, slot, pos: dict(player=n, slot=slot, yahoo_nba_team=team, positions=pos, status=None)
        self.state = j("state.json", dict(as_of="2026-10-20", teams=[
            dict(name="MINE", seat=10, players=[pl("Nikola Jokic", "DEN", "C", ["C"]), pl("Derrick White", "BOS", "UTIL", ["PG", "SG"]),
                                                pl("Max Strus", "LAC", "IL", ["SF"])]),
            dict(name="THEIRS", seat=11, players=[pl("Tyrese Maxey", "PHI", "BN", ["PG"]), pl("Joel Embiid", "PHI", "IL", ["C"])]),
            dict(name="OTHER", seat=3, players=[])]))
        self.sched = j("sched.json", dict(owner_opponents=[dict(week=1, seat=11)]))
        with open(os.path.join(self.d, "games.csv"), "w") as f:
            f.write("date,yahoo_week,visitor,home,note\n2026-10-20,1,BOS,PHI,\n2026-10-21,1,DEN,PHI,\n2026-10-23,1,DEN,LAL,\n")
        dump(dict(date="2026-10-20", games=[dict(espn_id="g1", season_type=2)], players=[
            dict(name="Derrick White", pool_name="Derrick White", team="BOS", dnp=False, game="g1",
                 **box(fgm=4, fga=9, ftm=2, fta=2, tpm=3, pts=13, reb=4, ast=5, stl=2, blk=1, tov=1)),
            dict(name="Tyrese Maxey", pool_name="Tyrese Maxey", team="PHI", dnp=False, game="g1",
                 **box(fgm=10, fga=21, ftm=6, fta=7, tpm=4, pts=30, reb=3, ast=6, stl=1, blk=0, tov=2)),
            dict(name="Joel Embiid", pool_name="Joel Embiid", team="PHI", dnp=False, game="g1",
                 **box(fgm=9, fga=15, ftm=10, fta=12, tpm=0, pts=28, reb=11, ast=3, stl=0, blk=2, tov=4))]),
            os.path.join(self.d, "actuals", "2026-10-20.json"))
        dump(dict(date="2026-10-21", rows=[dict(player="Nikola Jokic", availability=0.5, yahoo_status="Q")]),
             os.path.join(self.d, "status", "status_2026-10-21.json"))
        self.paths = dict(state=self.state, schedule=self.sched, games=os.path.join(self.d, "games.csv"),
                          actuals=os.path.join(self.d, "actuals"), status=os.path.join(self.d, "status"))
        saved = os.environ.get("SEASON_POOL")
        self.addCleanup(lambda: os.environ.__setitem__("SEASON_POOL", saved) if saved is not None else os.environ.pop("SEASON_POOL", None))
        os.environ["SEASON_POOL"] = os.path.join(os.path.dirname(HERE), "data", "season", "pool_season.csv")

    def test_lineup_check_alerts_when_a_bench_player_plays_and_a_starter_does_not(self):
        # 2026-10-21: DEN plays, BOS does not; Jokic on the bench, White (no game) in a starting slot
        st = json.load(open(self.state))
        st["teams"][0]["players"][0]["slot"], st["teams"][0]["players"][1]["slot"] = "BN", "UTIL"
        dump(st, self.state)
        out = os.path.join(self.d, "news")
        r = subprocess.run([sys.executable, os.path.join(HERE, "lineup_check.py"), "--date", "2026-10-21",
                            "--state", self.state, "--schedule", self.sched, "--games", self.paths["games"],
                            "--actuals", self.paths["actuals"], "--status-dir", self.paths["status"],
                            "--yahoo-pull", os.path.join(self.d, "none.json"), "--out-dir", out],
                           capture_output=True, text=True)
        self.assertIn("LINEUP CHECK: ALERT", r.stdout, r.stdout + r.stderr)
        self.assertIn("PUSH: Lineup — Start Nikola Jokic (DEN) for Derrick White", r.stdout)
        rec = json.load(open(os.path.join(out, "lineup_2026-10-21.json")))
        self.assertEqual([(m["start"], m["sit"], m["kind"]) for m in rec["alerts"]], [("Nikola Jokic", "Derrick White", "empty")])

    def test_lineup_check_is_quiet_when_the_lineup_is_already_the_best(self):
        out = os.path.join(self.d, "news")
        r = subprocess.run([sys.executable, os.path.join(HERE, "lineup_check.py"), "--date", "2026-10-21",
                            "--state", self.state, "--schedule", self.sched, "--games", self.paths["games"],
                            "--actuals", self.paths["actuals"], "--status-dir", self.paths["status"],
                            "--yahoo-pull", os.path.join(self.d, "none.json"), "--out-dir", out],
                           capture_output=True, text=True)
        self.assertIn("LINEUP CHECK: OK", r.stdout, r.stdout + r.stderr)
        self.assertNotIn("PUSH:", r.stdout)

    def test_the_record_carries_to_date_projection_and_leaders_for_both_teams(self):
        rec = WM.build("2026-10-21", self.paths)
        self.assertEqual((rec["week"], rec["window"]), (1, ["2026-10-20", "2026-10-25"]))
        self.assertEqual(rec["to_date_days"], ["2026-10-20"]); self.assertEqual(rec["missing_days"], [])
        cats = {c["cat"]: c for c in rec["cats"]}
        self.assertEqual(list(cats), WM.CATS)
        self.assertEqual(cats["PTS"]["me_to_date"], 13)            # White only; Strus is IL
        self.assertEqual(cats["PTS"]["opp_to_date"], 30)           # Maxey only; Embiid is IL
        self.assertAlmostEqual(cats["FG%"]["me_to_date"], 4 / 9, places=3)
        # Jokic: 2 DEN games left x availability 0.5 = one expected game of his season line
        self.assertEqual(rec["games"]["me"]["remaining_by_player"], {"Nikola Jokic": 2})
        self.assertEqual(rec["games"]["opp"]["remaining_by_player"], {"Tyrese Maxey": 1})
        self.assertIn(cats["PTS"]["leader"], ("me", "opp", "tie"))
        self.assertGreater(cats["PTS"]["me_final"], 13)
        self.assertEqual(rec["opponent"], dict(name="THEIRS", seat=11))
        # White (BOS) has no game after 10/20 and sits below the active roster's median value: the scan runs
        self.assertEqual(rec["pickups"]["status"], "ran")
        self.assertEqual(rec["pickups"]["drop"]["player"], "Derrick White")
        self.assertTrue(rec["pickups"]["top"]); self.assertGreater(rec["pickups"]["pool_size"], 300)
        self.assertNotIn("Joel Embiid", [r["add"] for r in rec["pickups"]["top"]])   # rostered (IL) is not a free agent

    def test_a_line_the_kits_file_spells_differently_still_counts_for_its_roster(self):
        # owner 2026-10-22 (the name-mismatch fix): Darius Acuff Jr.'s 10/21 game was missing from the rebuild because
        # the box pull left it unpooled ("Darius Acuff" in the kit's file); his 12 points now count for THEIRS
        st = json.load(open(self.state))
        st["teams"][1]["players"].append(dict(player="Darius Acuff Jr.", slot="UTIL", yahoo_nba_team="SAC", positions=["PG"], status=None))
        dump(st, self.state)
        f = os.path.join(self.paths["actuals"], "2026-10-20.json"); box_rec = json.load(open(f))
        box_rec["players"].append(dict(name="Darius Acuff Jr.", pool_name=None, team="SAC", dnp=False, game="g1",
                                       **box(fgm=5, fga=24, ftm=2, fta=5, tpm=0, pts=12, reb=3, ast=3, stl=3, blk=0, tov=4)))
        dump(box_rec, f)
        cats = {c["cat"]: c for c in WM.build("2026-10-21", self.paths)["cats"]}
        self.assertEqual(cats["PTS"]["opp_to_date"], 42)            # Maxey 30 + Acuff 12

    def test_the_card_carries_each_categorys_chance_and_the_this_week_scan_runs_before_anyone_finishes(self):
        rec = WM.build("2026-10-20", self.paths)
        ps = [c["p_win"] for c in rec["cats"]]
        self.assertTrue(all(0.0 <= x <= 1.0 for x in ps))
        self.assertAlmostEqual(rec["exp_cats"], sum(ps), places=3)    # each p_win is rounded to 4 places on the card
        self.assertAlmostEqual(rec["p_5plus"], WM.win_week_chance([c["p_win"] for c in rec["cats"]]), places=3)
        tw = rec["pickups"]["this_week"]
        self.assertEqual(tw["status"], "ran")
        self.assertEqual(tw["drops"], ["Derrick White"])           # below the median, not finished on 10/20
        self.assertTrue(tw["rows"])
        self.assertTrue(all(r["games"] > 0 for r in tw["rows"]))   # no playable game: listed apart, not ranked
        self.assertIsInstance(tw["no_games"], list)
        top = tw["rows"][0]
        self.assertEqual(sorted(top["d_cat"]), sorted(WM.CATS))
        self.assertIsInstance(top["season_d_ecw"], float)
        self.assertNotIn("Joel Embiid", [r["add"] for r in tw["rows"]])

    def test_before_anyone_finishes_the_scan_says_so_and_names_who_finishes_next(self):
        rec = WM.build("2026-10-20", self.paths)
        self.assertEqual(rec["to_date_days"], [])
        self.assertEqual(rec["pickups"]["status"], "no finished low-value player")
        self.assertIn("Derrick White", [x["player"] for x in rec["pickups"]["next_finish"]])

    def test_a_week_day_with_games_and_no_box_score_file_is_named_missing(self):
        rec = WM.build("2026-10-22", self.paths)
        self.assertEqual(rec["to_date_days"], ["2026-10-20"])
        self.assertEqual(rec["missing_days"], ["2026-10-21"])

    def test_cli_writes_the_record_and_prints_pass(self):
        out = os.path.join(self.d, "out")
        p = subprocess.run([sys.executable, os.path.join(HERE, "week_matchup.py"), "--date", "2026-10-21", "--out-dir", out,
                            "--state", self.state, "--schedule", self.sched, "--games", self.paths["games"],
                            "--actuals", self.paths["actuals"], "--status-dir", self.paths["status"],
                            "--yahoo-pull", os.path.join(self.d, "no_pull.json")],
                           capture_output=True, text=True, env=dict(os.environ))
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertRegex(p.stdout, r"(?m)^WEEK MATCHUP: PASS")
        self.assertTrue(os.path.exists(os.path.join(out, "week_matchup_2026-10-21.json")))

    # ---- A: Yahoo's own week totals for the to-date column, the rebuild kept as the cross-check (owner 2026-10-21)
    def pull(self, me_pts=13, names=("MINE", "THEIRS"), fas=None):
        """A Flaim pull: the week-1 matchup between `names` (MINE's line is White's 10/20 box score with PTS
        `me_pts`; THEIRS's is Maxey's) and, when given, Yahoo's available-player list."""
        me = TFL.side(11, names[0], 9, 4, 2, 2, (3, me_pts, 4, 5, 2, 1, 1), 2)
        opp = TFL.side(10, names[1], 21, 10, 7, 6, (4, 30, 3, 6, 1, 0, 2), 1)
        p = dict(source="flaim", matchups={"1": TFL.matchups(1, [(opp, me)])["data"]}, rosters={},
                 free_agents=TFL.free_agents(fas)["data"] if fas is not None else None)
        return dump(p, os.path.join(self.d, f"pull_{me_pts}_{names[0]}.json"))

    def test_yahoos_totals_are_the_to_date_column_and_a_rebuild_difference_is_listed(self):
        rec = WM.build("2026-10-21", dict(self.paths, yahoo_pull=self.pull(me_pts=15)))
        cats = {c["cat"]: c for c in rec["cats"]}
        self.assertEqual(cats["PTS"]["me_to_date"], 15)                      # Yahoo's figure, not the rebuild's 13
        self.assertEqual(cats["PTS"]["opp_to_date"], 30)
        src = rec["to_date_source"]
        self.assertEqual(src["source"], "yahoo")
        self.assertFalse(src["rebuild_agrees"])
        self.assertEqual(src["differences"], [dict(side="me", stat="pts", yahoo=15, rebuild=13)])
        self.assertEqual(src["yahoo_games_remaining"], dict(me=2, opp=1))
        self.assertEqual(rec["totals"]["me"]["to_date"]["pts"], 15)
        self.assertEqual(rec["totals"]["me"]["rebuild_to_date"]["pts"], 13)
        # the final adds the projection to Yahoo's figure: 15 + Jokic's expected points
        self.assertAlmostEqual(cats["PTS"]["me_final"], round(15 + rec["totals"]["me"]["remaining"]["pts"], 1), places=1)

    def test_when_the_rebuild_matches_yahoo_on_every_stat_the_record_says_so(self):
        src = WM.build("2026-10-21", dict(self.paths, yahoo_pull=self.pull()))["to_date_source"]
        self.assertEqual((src["source"], src["rebuild_agrees"], src["differences"]), ("yahoo", True, []))

    # ---- the rebuild reads each past day's Yahoo lineup (owner 2026-10-22, "Read daily rosters")
    def daily_pull(self, fname, days, matchup=True):
        """A Flaim pull carrying Yahoo's lineups by day; days is {(team id, Yahoo name): {date: [(player, slot)]}}."""
        p = json.load(open(self.pull())) if matchup else dict(source="flaim", matchups={}, rosters={}, free_agents=None)
        p["daily"] = {}
        for (tid, name), by_day in days.items():
            for day, players in by_day.items():
                r = TFL.roster(tid, name, [(n, "PHI", "PG", slot, None) for n, slot in players], snapshot=day)["data"]
                p["daily"].setdefault(r["teamKey"], {})[day] = r
        return dump(p, os.path.join(self.d, fname))

    def test_a_days_yahoo_lineup_counts_its_active_slots_and_not_its_bench(self):
        # that day Maxey sat on THEIRS's bench and Embiid (IL in today's state) started at C: Embiid's 28 count
        pull = self.daily_pull("pull_2026-10-21.json", {(10, "THEIRS"): {"2026-10-20": [("Tyrese Maxey", "BN"), ("Joel Embiid", "C")]}})
        rec = WM.build("2026-10-21", dict(self.paths, yahoo_pull=pull))
        self.assertEqual(rec["totals"]["opp"]["rebuild_to_date"]["pts"], 28)
        self.assertEqual(rec["games"]["opp"]["to_date_benched"], [["2026-10-20", "Tyrese Maxey"]])
        self.assertEqual(rec["rebuild_rosters"]["opp"], {"2026-10-20": "yahoo"})

    def test_a_player_dropped_after_playing_still_counts_on_his_day(self):
        # Darius Acuff Jr. started for THEIRS on 10/20 and is on no roster in today's state
        f = os.path.join(self.paths["actuals"], "2026-10-20.json"); box_rec = json.load(open(f))
        box_rec["players"].append(dict(name="Darius Acuff Jr.", pool_name=None, team="SAC", dnp=False, game="g1",
                                       **box(fgm=5, fga=24, ftm=2, fta=5, tpm=0, pts=12, reb=3, ast=3, stl=3, blk=0, tov=4)))
        dump(box_rec, f)
        pull = self.daily_pull("pull_2026-10-21.json", {(10, "THEIRS"): {"2026-10-20": [("Tyrese Maxey", "PG"), ("Darius Acuff Jr.", "Util")]}})
        rec = WM.build("2026-10-21", dict(self.paths, yahoo_pull=pull))
        self.assertEqual(rec["totals"]["opp"]["rebuild_to_date"]["pts"], 42)       # Maxey 30 + Acuff 12

    def test_a_day_without_a_yahoo_lineup_falls_back_to_todays_roster_and_says_so(self):
        pull = self.daily_pull("pull_2026-10-21.json", {(11, "MINE"): {"2026-10-20": [("Derrick White", "SG"), ("Nikola Jokic", "C")]}})
        rec = WM.build("2026-10-21", dict(self.paths, yahoo_pull=pull))
        self.assertEqual(rec["rebuild_rosters"], dict(me={"2026-10-20": "yahoo"}, opp={"2026-10-20": "today"}))
        self.assertEqual(rec["totals"]["opp"]["rebuild_to_date"]["pts"], 30)       # Maxey, today's rule
        self.assertEqual(rec["totals"]["me"]["rebuild_to_date"]["pts"], 13)

    def test_a_lineup_pinned_by_an_earlier_run_this_week_is_read(self):
        self.daily_pull("pull_2026-10-21.json", {(10, "THEIRS"): {"2026-10-20": [("Tyrese Maxey", "BN"), ("Joel Embiid", "C")]}},
                        matchup=False)
        run = dump(json.load(open(self.pull())), os.path.join(self.d, "pull_2026-10-22.json"))   # today's: no lineups
        rec = WM.build("2026-10-22", dict(self.paths, yahoo_pull=run))
        self.assertEqual(rec["totals"]["opp"]["rebuild_to_date"]["pts"], 28)
        self.assertEqual(rec["rebuild_rosters"]["opp"], {"2026-10-20": "yahoo"})

    def test_no_pull_file_falls_back_to_the_rebuild_and_says_why(self):
        rec = WM.build("2026-10-21", dict(self.paths, yahoo_pull=os.path.join(self.d, "absent.json")))
        self.assertEqual(rec["to_date_source"]["source"], "rebuild")
        self.assertIn("no Yahoo pull", rec["to_date_source"]["reason"])
        self.assertEqual({c["cat"]: c for c in rec["cats"]}["PTS"]["me_to_date"], 13)

    def test_an_unreadable_pull_falls_back_and_the_card_still_builds(self):
        bad = os.path.join(self.d, "torn.json")
        with open(bad, "w") as f:
            f.write('{"source": "flaim", "matchups": {')
        rec = WM.build("2026-10-21", dict(self.paths, yahoo_pull=bad))
        self.assertEqual(rec["to_date_source"]["source"], "rebuild")
        self.assertIn("unreadable", rec["to_date_source"]["reason"])
        self.assertEqual(rec["pickups"]["pool"]["source"], "kit")

    def test_a_matchup_that_does_not_name_both_teams_falls_back_and_names_them(self):
        src = WM.build("2026-10-21", dict(self.paths, yahoo_pull=self.pull(names=("Renamed", "THEIRS"))))["to_date_source"]
        self.assertEqual(src["source"], "rebuild")
        self.assertIn("MINE", src["reason"]); self.assertIn("THEIRS", src["reason"])

    def test_a_team_renamed_on_yahoo_is_found_by_its_roster_in_the_pull(self):
        p = json.load(open(self.pull(names=("Renamed", "THEIRS"))))
        p["rosters"] = {"t11": TFL.roster(11, "Renamed", [("Nikola Jokić", "DEN", "C", "C", None),
                                                          ("Derrick White", "BOS", "PG,SG", "Util", None),
                                                          ("Max Strus", "LAC", "SF", "IL", None)])["data"]}
        src = WM.build("2026-10-21", dict(self.paths, yahoo_pull=dump(p, os.path.join(self.d, "renamed.json"))))["to_date_source"]
        self.assertEqual((src["source"], src["yahoo_names"]), ("yahoo", dict(me="Renamed", opp="THEIRS")))

    # ---- D: Yahoo's available-player list is the pickup pool (owner 2026-10-21)
    def test_yahoos_free_agent_list_is_the_pickup_pool_and_every_exclusion_is_named(self):
        fas = [("Jrue Holiday", "POR", "PG,SG", None), ("Not In The Pool", "BOS", "C", None),
               ("Isaiah Stewart", "MEM", "PF,C", "D"), ("Anthony Black", "ORL", "PG,SG,SF", "O"),
               ("Derrick White", "BOS", "PG,SG", None), ("A Made-Up Letter", "BOS", "C", "ZZ")]
        rec = WM.build("2026-10-21", dict(self.paths, yahoo_pull=self.pull(fas=fas)))
        pk = rec["pickups"]
        self.assertEqual(pk["status"], "ran")
        pool = pk["pool"]
        self.assertEqual((pool["source"], pool["listed"], pk["pool_size"]), ("yahoo", 6, 2))
        self.assertEqual(sorted(r["add"] for r in pk["top"]), ["Isaiah Stewart", "Jrue Holiday"])
        self.assertEqual({r["add"]: r["status"] for r in pk["top"]}["Isaiah Stewart"], "D")  # doubtful, scored at 0.25
        self.assertEqual([x["name"] for x in pool["unknown_status"]], ["A Made-Up Letter"])  # unknown: never guessed
        self.assertEqual([x["name"] for x in pool["out"]], ["Anthony Black"])
        self.assertEqual([x["name"] for x in pool["not_projected"]], ["Not In The Pool"])
        self.assertEqual([x["name"] for x in pool["skipped"]], ["Derrick White"])           # rostered in the state
        self.assertGreater(pool["kit_pool_not_listed"], 300)

    def test_without_a_yahoo_list_the_pool_is_the_kits_and_says_so(self):
        pk = WM.build("2026-10-21", dict(self.paths, yahoo_pull=self.pull()))["pickups"]
        self.assertEqual(pk["pool"]["source"], "kit")
        self.assertGreater(pk["pool_size"], 300)


class YahooFreeAgents(unittest.TestCase):
    def test_letters_tier_names_resolve_and_unknowns_are_set_aside(self):
        pool = [dict(player="Jrue Holiday"), dict(player="Nikola Vucevic"), dict(player="Max Strus")]
        entries = [dict(name="Jrue Holiday", team="POR", position="PG,SG"),
                   dict(name="Nikola Vučević", team="ORL", position="C", status="Q"),
                   dict(name="Max Strus", team="CLE", position="SF", status="NA"),
                   dict(name="Isaiah Stewart", team="MEM", position="PF,C", status="D"),
                   dict(name="A Made-Up Letter", team="BOS", position="C", status="ZZ"),
                   dict(name="Hugo González", team="BOS", position="SF")]
        pool.append(dict(player="Isaiah Stewart"))
        scored, out, unknown, notp = WM.yahoo_free_agents(entries, pool)
        self.assertEqual([(s["player"], s["availability"], s["positions"]) for s in scored],
                         [("Jrue Holiday", 1.0, ["PG", "SG"]), ("Nikola Vucevic", 0.5, ["C"]),
                          ("Isaiah Stewart", 0.25, ["PF", "C"])])                # D = doubtful (owner 2026-10-21)
        self.assertEqual([x["name"] for x in out], ["Max Strus"])
        self.assertEqual([x["name"] for x in unknown], ["A Made-Up Letter"])
        self.assertEqual([x["name"] for x in notp], ["Hugo González"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
