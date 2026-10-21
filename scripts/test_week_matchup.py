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
               ("Derrick White", "BOS", "PG,SG", None)]
        rec = WM.build("2026-10-21", dict(self.paths, yahoo_pull=self.pull(fas=fas)))
        pk = rec["pickups"]
        self.assertEqual(pk["status"], "ran")
        pool = pk["pool"]
        self.assertEqual((pool["source"], pool["listed"], pk["pool_size"]), ("yahoo", 5, 1))
        self.assertEqual([r["add"] for r in pk["top"]], ["Jrue Holiday"])
        self.assertEqual([x["name"] for x in pool["unknown_status"]], ["Isaiah Stewart"])   # "D": never guessed
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
                   dict(name="Hugo González", team="BOS", position="SF")]
        scored, out, unknown, notp = WM.yahoo_free_agents(entries, pool)
        self.assertEqual([(s["player"], s["availability"], s["positions"]) for s in scored],
                         [("Jrue Holiday", 1.0, ["PG", "SG"]), ("Nikola Vucevic", 0.5, ["C"])])
        self.assertEqual([x["name"] for x in out], ["Max Strus"])
        self.assertEqual([x["name"] for x in unknown], ["Isaiah Stewart"])
        self.assertEqual([x["name"] for x in notp], ["Hugo González"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
