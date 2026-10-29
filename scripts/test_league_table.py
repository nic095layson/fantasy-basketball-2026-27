#!/usr/bin/env python3
"""Red-first tests for scripts/league_table.py (owner 2026-10-23, "Build 1": the League tab — every team's cumulative
nine-category totals from Yahoo's weekly matchup blocks, the all-play power ranking, the week-in-progress to date).
Every expected figure below is computed by hand from the fixture, not by the code under test.

    python3 scripts/test_league_table.py
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import league_table as LT  # noqa: E402
import test_flaim_live as TFL  # noqa: E402

TEAMS = [f"Team {i}" for i in range(1, 13)]
STATE = {"as_of": "2026-10-23", "teams": [{"name": t, "seat": i + 1, "manager": f"M{i + 1}", "players": []} for i, t in enumerate(TEAMS)]}


def tot(fgm, fga, ftm, fta, tpm, pts, reb, ast, stl, blk, tov):
    return dict(fgm=fgm, fga=fga, ftm=ftm, fta=fta, tpm=tpm, pts=pts, reb=reb, ast=ast, stl=stl, blk=blk, tov=tov)


def block(week, status="in_progress", scale=1):
    """Six matchups, Team 1 vs 2, 3 vs 4, ...; Team k's totals are k-shaped so every team differs."""
    ms = []
    for i in range(6):
        a, b = 2 * i + 1, 2 * i + 2
        sides = []
        for k in (a, b):
            s = TFL.side(k, TEAMS[k - 1], 100 + k, 40 + k, 20, 10 + k, (k, 100 + 10 * k, 50 + k, 20 + k, 5 + k % 3, 3 + k % 2, 20 - k), 24 - k)
            s["categoryScore"] = dict(wins=5 if k == a else 4, losses=4 if k == a else 5, ties=0)
            sides.append(s)
        ms.append(dict(matchupId=i + 1, week=week, status=status, home=sides[0], away=sides[1]))
    data = dict(leagueKey=TFL.KEY, currentWeek=week, matchupWeek=week, matchups=ms)
    if scale != 1:
        for m in data["matchups"]:
            for sd in (m["home"], m["away"]):
                for c in sd["categories"]:
                    if "/" in c["value"]:
                        x, y = c["value"].split("/"); c["value"] = f"{int(x) * scale}/{int(y) * scale}"
                    elif c["value"] != "x":
                        c["value"] = str(int(c["value"]) * scale)
    return data


def pull(date, weeks):
    return {"source": "flaim", "league_key": TFL.KEY, "rosters": {}, "daily": {}, "matchups": {str(w): b for w, b in weeks.items()}}


class Yahoo(unittest.TestCase):
    def test_a_weeks_block_gives_every_team_its_totals_opponent_score_and_games_left(self):
        wk = LT.week_from_yahoo(block(1), STATE)
        self.assertEqual(sorted(wk), sorted(TEAMS))
        t = wk["Team 10"]
        self.assertEqual(t["totals"], tot(50, 110, 20, 20, 10, 200, 60, 30, 6, 3, 10))
        self.assertEqual((t["seat"], t["opponent"], t["games_remaining"]), (10, "Team 9", 14))
        self.assertEqual(t["score"], dict(wins=4, losses=5, ties=0))

    def test_a_block_naming_a_team_the_state_lacks_halts(self):
        b = block(1); b["matchups"][0]["home"]["teamName"] = "Nobody"
        with self.assertRaises(LT.TableError):
            LT.week_from_yahoo(b, STATE)


class AllPlay(unittest.TestCase):
    A = tot(50, 100, 10, 20, 10, 100, 50, 20, 5, 5, 10)
    B = tot(45, 100, 10, 20, 12, 90, 50, 25, 5, 4, 12)
    C = tot(55, 100, 8, 20, 8, 110, 40, 20, 6, 5, 8)

    def test_each_team_against_every_other_on_nine_categories_turnovers_reversed_ties_half(self):
        ap = LT.allplay({"A": self.A, "B": self.B, "C": self.C})
        # by hand: A vs B 4-2-3, A vs C 3-4-2; B vs A 2-4-3, B vs C 4-5-0; C vs A 4-3-2, C vs B 5-4-0
        self.assertEqual((ap["A"]["w"], ap["A"]["l"], ap["A"]["t"]), (7, 6, 5))
        self.assertEqual((ap["B"]["w"], ap["B"]["l"], ap["B"]["t"]), (6, 9, 3))
        self.assertEqual((ap["C"]["w"], ap["C"]["l"], ap["C"]["t"]), (9, 7, 2))
        self.assertAlmostEqual(ap["A"]["pct"], (7 + 2.5) / 18)

    def test_category_ranks_put_the_fewest_turnovers_first(self):
        r = LT.ranks({"A": LT.cat_values(self.A), "B": LT.cat_values(self.B), "C": LT.cat_values(self.C)})
        self.assertEqual((r["C"]["TO"], r["A"]["TO"], r["B"]["TO"]), (1, 2, 3))
        self.assertEqual((r["C"]["FG%"], r["A"]["FG%"], r["B"]["FG%"]), (1, 2, 3))
        self.assertEqual(r["A"]["REB"], r["B"]["REB"])          # a tie shares the rank
        self.assertEqual(r["C"]["REB"], 3)


class Build(unittest.TestCase):
    """Two weeks: week 1 finished (its finals in a pull dated after the week), week 2 in progress at 2026-10-28."""
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.pulls = os.path.join(self.d, "flaim"); os.makedirs(self.pulls)
        self.state = os.path.join(self.d, "state.json"); json.dump(STATE, open(self.state, "w"))
        # 10/25 (Sunday): week 1 still in progress at the morning pull
        json.dump(pull("2026-10-25", {1: block(1)}), open(os.path.join(self.pulls, "pull_2026-10-25.json"), "w"))
        # 10/26 (Monday): the pull carries week 2 (current) and week 1's finals, doubled (Sunday's games)
        json.dump(pull("2026-10-26", {1: block(1, "finished", scale=2), 2: block(2)}), open(os.path.join(self.pulls, "pull_2026-10-26.json"), "w"))
        json.dump(pull("2026-10-28", {2: block(2, scale=3)}), open(os.path.join(self.pulls, "pull_2026-10-28.json"), "w"))
        self.paths = dict(state=self.state, pull_dir=self.pulls, actuals=os.path.join(self.d, "actuals"))

    def test_finished_weeks_use_the_post_week_pull_and_the_current_week_the_days_pull(self):
        rec = LT.build("2026-10-28", self.paths)
        self.assertEqual(rec["week"], 2)
        self.assertEqual([w["status"] for w in rec["weeks"]], ["finished", "in_progress"])
        self.assertEqual([w["source"] for w in rec["weeks"]], ["yahoo", "yahoo"])
        self.assertEqual(rec["weeks"][0]["pull"], "pull_2026-10-26.json")
        self.assertEqual(rec["weeks"][1]["pull"], "pull_2026-10-28.json")
        self.assertEqual(rec["weeks"][0]["teams"]["Team 10"]["totals"]["pts"], 400)   # the finals, not Sunday morning's 200
        self.assertEqual(rec["weeks"][1]["teams"]["Team 10"]["totals"]["pts"], 600)

    def test_cumulative_percentages_are_total_makes_over_total_attempts(self):
        rec = LT.build("2026-10-28", self.paths)
        c = rec["cumulative"]["Team 10"]
        self.assertEqual(c["totals"]["fgm"], 100 + 150); self.assertEqual(c["totals"]["fga"], 220 + 330)
        self.assertAlmostEqual(c["cats"]["FG%"], 250 / 550)
        self.assertEqual(c["cats"]["PTS"], 400 + 600)
        self.assertEqual(c["weeks"], 2)
        self.assertTrue(c["mine"]); self.assertFalse(rec["cumulative"]["Team 9"]["mine"])
        self.assertEqual(c["manager"], "M10")

    def test_power_ranks_by_cumulative_all_play_and_names_the_luck_gap(self):
        rec = LT.build("2026-10-28", self.paths)
        p = rec["power"]
        self.assertEqual([x["rank"] for x in p], list(range(1, 13)))
        self.assertTrue(all(p[i]["allplay"]["pct"] >= p[i + 1]["allplay"]["pct"] for i in range(11)))
        t10 = next(x for x in p if x["team"] == "Team 10")
        # actual = the Yahoo category score summed over the weeks (4-5-0 twice as the away side)
        self.assertEqual(t10["actual"], dict(w=8, l=10, t=0))
        self.assertAlmostEqual(t10["luck"], 8 / 18 - t10["allplay"]["pct"])
        self.assertEqual(sum(x["allplay"]["w"] for x in p), sum(x["allplay"]["l"] for x in p))

    def test_the_current_week_block_alone_builds_when_no_week_has_finished(self):
        rec = LT.build("2026-10-25", self.paths)
        self.assertEqual([w["status"] for w in rec["weeks"]], ["in_progress"])
        self.assertEqual(rec["cumulative"]["Team 10"]["cats"]["PTS"], 200)

    def test_a_finished_week_with_no_post_week_pull_is_rebuilt_from_box_scores_and_says_so(self):
        os.remove(os.path.join(self.pulls, "pull_2026-10-26.json"))
        json.dump(pull("2026-10-27", {2: block(2)}), open(os.path.join(self.pulls, "pull_2026-10-27.json"), "w"))
        st = json.load(open(self.state))
        st["teams"][9]["players"] = [dict(player="Starter Guy", slot="PG", yahoo_nba_team="DEN", positions=["PG"], status=None),
                                     dict(player="Bench Guy", slot="BN", yahoo_nba_team="DEN", positions=["PG"], status=None)]
        json.dump(st, open(self.state, "w"))
        os.makedirs(self.paths["actuals"])
        json.dump(dict(date="2026-10-21", games=[dict(espn_id="g1", season_type=2)], players=[
            dict(name="Starter Guy", pool_name="Starter Guy", team="DEN", dnp=False, game="g1", **tot(5, 10, 2, 2, 1, 13, 4, 5, 2, 1, 1)),
            dict(name="Bench Guy", pool_name="Bench Guy", team="DEN", dnp=False, game="g1", **tot(9, 9, 0, 0, 0, 18, 1, 1, 0, 0, 0))]),
            open(os.path.join(self.paths["actuals"], "2026-10-21.json"), "w"))
        rec = LT.build("2026-10-28", self.paths)
        w1 = rec["weeks"][0]
        self.assertEqual((w1["status"], w1["source"]), ("finished", "rebuild"))
        self.assertEqual(w1["teams"]["Team 10"]["totals"]["pts"], 13)       # the active slot only
        self.assertIsNone(w1["teams"]["Team 10"]["score"])                    # no Yahoo result for a rebuilt week
        self.assertIn("2026-10-21", w1["days_read"])

    def test_cli_writes_the_record_and_prints_pass(self):
        out = os.path.join(self.d, "out")
        p = subprocess.run([sys.executable, os.path.join(HERE, "league_table.py"), "--date", "2026-10-28", "--state", self.state,
                            "--pull-dir", self.pulls, "--actuals", self.paths["actuals"], "--out-dir", out, "--ledger", ""],
                           capture_output=True, text=True)   # --ledger '': no row in the kit's run-ledger from a test
        self.assertIn("LEAGUE TABLE: PASS", p.stdout, p.stdout + p.stderr)
        rec = json.load(open(os.path.join(out, "league_2026-10-28.json")))
        self.assertEqual(len(rec["power"]), 12)
        self.assertIn("pull_2026-10-28.json", json.dumps(rec["inputs"]))




def standings(rows, key=None):
    """A get_standings response: rows = [(team, wins, losses, ties)] in Yahoo's rank order."""
    return dict(leagueKey=key or TFL.KEY, seasonPhase="regular_season", standings=[
        dict(name=t, rank=str(i + 1), wins=str(w), losses=str(l), ties=tt, percentage=f"{(w + 0.5 * tt) / max(w + l + tt, 1):.3f}"[1:],
             playoffSeed=i + 1 if i < 8 else None, waiverPriority=12 - i, faabBalance=500) for i, (t, w, l, tt) in enumerate(rows)])


class Standings(unittest.TestCase):
    """Owner 2026-10-26 ("Standings card + fix records"): Yahoo's standings from the latest pull that carries them, the
    playoff line under 8th, the distance from it, and the kit's summed record checked against Yahoo's W-L-T; a finished
    week the kit had to rebuild takes its score from the verified week record (data/weeks/week_N.json)."""
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.pulls = os.path.join(self.d, "flaim"); os.makedirs(self.pulls)
        self.state = os.path.join(self.d, "state.json"); json.dump(STATE, open(self.state, "w"))
        json.dump(pull("2026-10-26", {1: block(1, "finished", scale=2), 2: block(2)}), open(os.path.join(self.pulls, "pull_2026-10-26.json"), "w"))
        self.weeks = os.path.join(self.d, "weeks"); os.makedirs(self.weeks)
        self.paths = dict(state=self.state, pull_dir=self.pulls, actuals=os.path.join(self.d, "actuals"), weeks=self.weeks)

    def put_standings(self, rows, date="2026-10-28"):
        pl = pull(date, {2: block(2, scale=3)}); pl["standings"] = standings(rows)
        json.dump(pl, open(os.path.join(self.pulls, f"pull_{date}.json"), "w"))

    def week1(self):
        # week 1 as block(1) scores it: the home side (odd team) 5-4-0, the away side 4-5-0
        return [(TEAMS[k - 1], 5 if k % 2 else 4, 4 if k % 2 else 5, 0) for k in range(1, 13)]

    def test_no_pull_with_standings_gives_none(self):
        json.dump(pull("2026-10-28", {2: block(2, scale=3)}), open(os.path.join(self.pulls, "pull_2026-10-28.json"), "w"))
        self.assertIsNone(LT.build("2026-10-28", self.paths)["standings"])

    def test_the_latest_pull_with_standings_on_or_before_the_date_gives_rank_record_seed_and_waiver(self):
        self.put_standings(self.week1())
        st = LT.build("2026-10-28", self.paths)["standings"]
        self.assertEqual(st["pull"], "pull_2026-10-28.json")
        self.assertEqual(st["playoff_teams"], 8)
        r = st["rows"]
        self.assertEqual([x["team"] for x in r], TEAMS)
        t10 = r[9]
        self.assertEqual((t10["rank"], t10["w"], t10["l"], t10["t"], t10["seed"], t10["waiver"]), (10, 4, 5, 0, None, 3))
        self.assertTrue(t10["mine"]); self.assertEqual(t10["manager"], "M10")

    def test_distance_from_the_line_in_category_games(self):
        # W = 14-k, L = k+4: 8th is 6-12, 9th is 5-13
        self.put_standings([(TEAMS[k - 1], 14 - k, k + 4, 0) for k in range(1, 13)])
        r = {x["team"]: x for x in LT.build("2026-10-28", self.paths)["standings"]["rows"]}
        self.assertEqual(r["Team 3"]["vs_line"], 6.0)    # ((11-5) + (13-7)) / 2 ahead of 9th
        self.assertEqual(r["Team 8"]["vs_line"], 1.0)    # ((6-5) + (13-12)) / 2
        self.assertEqual(r["Team 9"]["vs_line"], -1.0)   # ((6-5) + (13-12)) / 2 back of 8th
        self.assertEqual(r["Team 10"]["vs_line"], -2.0)  # ((6-4) + (14-12)) / 2

    def test_the_kits_finished_weeks_match_yahoos_record(self):
        self.put_standings(self.week1())
        st = LT.build("2026-10-28", self.paths)["standings"]
        self.assertEqual(st["check"]["mismatches"], [])
        self.assertEqual(st["check"]["teams_checked"], 12)
        self.assertEqual(st["check"]["finished_weeks"], [1])

    def test_a_disagreement_with_yahoo_is_named(self):
        rows = self.week1(); rows[2] = ("Team 3", 6, 3, 0)
        self.put_standings(rows)
        mm = LT.build("2026-10-28", self.paths)["standings"]["check"]["mismatches"]
        self.assertEqual(mm, [dict(team="Team 3", kit=[5, 4, 0], yahoo=[6, 3, 0])])

    def test_a_standings_team_the_state_lacks_halts(self):
        rows = self.week1(); rows[0] = ("Nobody FC", 5, 4, 0)
        self.put_standings(rows)
        with self.assertRaises(LT.TableError):
            LT.build("2026-10-28", self.paths)

    def test_a_team_renamed_since_the_week_record_is_matched_by_seat(self):
        # owner 2026-10-29 ("Key on Yahoo team key"): team 5 renamed itself after week 1; the week record still carries
        # the old name, and the score follows the seat, never the name
        os.remove(os.path.join(self.pulls, "pull_2026-10-26.json"))
        json.dump(pull("2026-10-27", {2: block(2)}), open(os.path.join(self.pulls, "pull_2026-10-27.json"), "w"))
        os.makedirs(self.paths["actuals"])
        json.dump(dict(date="2026-10-21", games=[], players=[]), open(os.path.join(self.paths["actuals"], "2026-10-21.json"), "w"))
        seat_of = {t["name"]: t["seat"] for t in STATE["teams"]}
        rows = {("Old Name" if t == "Team 10" else t): dict(seat=seat_of[t], yahoo_score=dict(wins=w, losses=l, ties=tt))
                for (t, w, l, tt) in self.week1()}
        json.dump(dict(week=1, teams=rows), open(os.path.join(self.weeks, "week_1.json"), "w"))
        rec = LT.build("2026-10-28", self.paths)
        self.assertEqual(rec["weeks"][0]["teams"]["Team 10"]["score"], dict(wins=4, losses=5, ties=0))

    def test_a_rebuilt_week_takes_its_score_from_the_week_record(self):
        os.remove(os.path.join(self.pulls, "pull_2026-10-26.json"))
        json.dump(pull("2026-10-27", {2: block(2)}), open(os.path.join(self.pulls, "pull_2026-10-27.json"), "w"))
        os.makedirs(self.paths["actuals"])
        json.dump(dict(date="2026-10-21", games=[], players=[]), open(os.path.join(self.paths["actuals"], "2026-10-21.json"), "w"))
        json.dump(dict(week=1, teams={t: dict(seat=k, yahoo_score=dict(wins=w, losses=l, ties=tt)) for k, (t, w, l, tt) in enumerate(self.week1(), 1)}),
                  open(os.path.join(self.weeks, "week_1.json"), "w"))
        rec = LT.build("2026-10-28", self.paths)
        w1 = rec["weeks"][0]
        self.assertEqual(w1["source"], "rebuild")
        self.assertEqual(w1["score_source"], "week_1.json")
        self.assertEqual(w1["teams"]["Team 10"]["score"], dict(wins=4, losses=5, ties=0))
        t10 = next(x for x in rec["power"] if x["team"] == "Team 10")
        self.assertEqual(t10["actual"], dict(w=8, l=10, t=0))   # week 1 from the record + week 2 to date (4-5-0)


def blank_side(seat, name):
    """A Yahoo matchup side on day one of a week: '/' for makes/attempts, '' for every other cell (the 10/26 pull)."""
    cats = [dict(displayName="FGM/A", value="/"), dict(displayName="FG%", value=""), dict(displayName="FTM/A", value="/"),
            dict(displayName="FT%", value="")] + [dict(displayName=c, value="") for c in ("3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO")]
    return dict(teamKey=f"{TFL.KEY}.t.{seat}", teamId=str(seat), teamName=name, categories=cats,
                categoryScore=dict(wins=0, losses=0, ties=9), gamesRemaining=40)


class NotStarted(unittest.TestCase):
    """Owner 2026-10-26: on day one of a week Yahoo shows '/' and '' — record the week as not started, not an error."""
    def block(self, bad=None):
        ms = []
        for i in range(6):
            a, b = 2 * i + 1, 2 * i + 2
            sa, sb = blank_side(a, TEAMS[a - 1]), blank_side(b, TEAMS[b - 1])
            ms.append(dict(matchupId=i + 1, week=2, status="in_progress", home=sa, away=sb))
        if bad:
            ms[0]["home"]["categories"][0]["value"] = bad
        return dict(leagueKey=TFL.KEY, currentWeek=2, matchupWeek=2, matchups=ms)

    def test_a_blank_week_is_not_started_with_no_totals_and_yahoos_score(self):
        out = LT.week_from_yahoo(self.block(), STATE)
        self.assertEqual(len(out), 12)
        x = out["Team 1"]
        self.assertIsNone(x["totals"]); self.assertTrue(x["not_started"])
        self.assertEqual(x["score"], dict(wins=0, losses=0, ties=9))

    def test_still_malformed_values_fail_loudly(self):
        for bad in ("12/", "abc"):
            with self.assertRaises(LT.TableError):
                LT.week_from_yahoo(self.block(bad), STATE)

    def test_build_records_the_week_as_not_started_and_leaves_it_out_of_the_totals(self):
        d = tempfile.mkdtemp()
        pull_dir = os.path.join(d, "flaim"); os.makedirs(pull_dir)
        st = os.path.join(d, "state.json"); json.dump(STATE, open(st, "w"))
        json.dump(pull("2026-10-26", {1: block(1, "final"), 2: self.block()}), open(os.path.join(pull_dir, "pull_2026-10-26.json"), "w"))
        rec = LT.build("2026-10-26", dict(state=st, pull_dir=pull_dir, actuals=os.path.join(d, "none")))
        w2 = rec["weeks"][-1]
        self.assertEqual((w2["week"], w2["status"]), (2, "not_started"))
        self.assertNotIn("allplay", w2)
        self.assertEqual(rec["cumulative"]["Team 1"]["weeks"], 1)                     # week 1 only
        p = subprocess.run([sys.executable, os.path.join(HERE, "league_table.py"), "--date", "2026-10-26", "--state", st,
                            "--pull-dir", pull_dir, "--actuals", os.path.join(d, "none"), "--out-dir", os.path.join(d, "out"), "--ledger", ""],
                           capture_output=True, text=True)
        self.assertIn("LEAGUE TABLE: PASS", p.stdout, p.stdout + p.stderr)
        self.assertIn("wk2 not started (Yahoo shows no stats yet)", p.stdout)

if __name__ == "__main__":
    unittest.main()
