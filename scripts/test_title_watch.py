#!/usr/bin/env python3
"""F5 (owner 2026-11-10): the overnight title-change check. Red first."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import title_watch as TW  # noqa: E402
import morning as M  # noqa: E402


def brief(date, a, b, moves=(), seasons=10000):
    return dict(date=date, seasons=seasons, title={"2026": a, "2027": b}, league_moves=list(moves))


MOVES = [dict(team="SNOWTIME WHITE WALKERS", seat=3, added=[], dropped=["Jake LaRavia"], to_il=[], from_il=["Luka Doncic"]),
         dict(team="Mine", seat=10, added=["John Collins"], dropped=["Cameron Johnson"], to_il=[], from_il=[]),
         dict(team="Quiet", seat=5, added=[], dropped=[], to_il=[], from_il=[])]


class Check(unittest.TestCase):
    def test_a_move_past_the_band_names_merges_and_roster_moves(self):
        r = TW.check(brief("2026-11-10", 12.32, 12.23, MOVES), brief("2026-11-09", 18.1, 17.96),
                     merges=["Merge pull request #246: simulate auto-row players"])
        self.assertAlmostEqual(r["title"], 12.275); self.assertAlmostEqual(r["prev_title"], 18.03)
        self.assertAlmostEqual(r["delta"], -5.755)
        self.assertTrue(r["moved"])
        self.assertEqual(r["merges"], ["Merge pull request #246: simulate auto-row players"])
        self.assertEqual([m["team"] for m in r["moves"]], ["SNOWTIME WHITE WALKERS", "Mine"])   # the empty row is dropped
        self.assertEqual([m["owner"] for m in r["moves"]], [False, True])
        line = TW.pass_line(r, "x.json")
        self.assertTrue(line.startswith("TITLE WATCH: PASS"))
        for s in ("12.3%", "18.0%", "-5.8", "#246", "Luka Doncic", "John Collins"):
            self.assertIn(s, line)

    def test_the_band_is_the_sampling_error_of_the_difference(self):
        import math
        r = TW.check(brief("2026-11-10", 12.0, 12.0), brief("2026-11-09", 12.0, 12.0), merges=[])
        e = 196 * math.sqrt(0.12 * 0.88 / 20000)
        self.assertAlmostEqual(r["band"], math.sqrt(2) * e, places=6)
        self.assertFalse(r["moved"])
        self.assertIn("within", TW.pass_line(r, "x.json"))

    def test_a_small_change_inside_the_band_is_not_flagged(self):
        r = TW.check(brief("2026-11-10", 12.5, 12.4, MOVES), brief("2026-11-09", 12.3, 12.2), merges=["Merge pull request #1: x"])
        self.assertFalse(r["moved"])
        self.assertNotIn("#1", TW.pass_line(r, "x.json"))       # causes are named only when the title moved

    def test_no_earlier_brief_is_a_pass_that_says_so(self):
        r = TW.check(brief("2026-11-10", 12.5, 12.4), None, merges=None)
        self.assertIsNone(r["moved"]); self.assertIsNone(r["delta"])
        self.assertIn("no earlier brief", TW.pass_line(r, "x.json"))

    def test_unreadable_git_history_is_said_not_guessed(self):
        r = TW.check(brief("2026-11-10", 12.3, 12.2, MOVES), brief("2026-11-09", 18.1, 18.0), merges=None)
        self.assertTrue(r["moved"]); self.assertIsNone(r["merges"])
        self.assertIn("kit merges not readable", TW.pass_line(r, "x.json"))

    def test_a_gap_of_more_than_one_day_is_named(self):
        r = TW.check(brief("2026-11-10", 12.3, 12.2), brief("2026-11-07", 18.1, 18.0), merges=[])
        self.assertEqual(r["gap_days"], 3)
        self.assertIn("3 days", TW.pass_line(r, "x.json"))

    def test_a_moved_title_with_nothing_found_says_unexplained(self):
        r = TW.check(brief("2026-11-10", 12.3, 12.2), brief("2026-11-09", 18.1, 18.0), merges=[])
        self.assertIn("no kit merge and no roster move", TW.pass_line(r, "x.json"))


class MethodChange(unittest.TestCase):
    """Owner 2026-11-16 (card: "Mark method changes"): a move that comes from a change of method (the line method or a
    registered constant) is named as such, first among the causes, so it is not read as a league result."""

    def test_a_line_switch_that_began_between_the_runs_is_named(self):
        prev, today = dict(date="2026-11-16"), dict(date="2026-11-17", line_switch=dict(cats=["pts", "reb", "ast"]))
        self.assertEqual(TW.line_method_changes(prev, today),
                         ["line method: the minutes ratio now applies to PTS, REB, AST (before: none)"])
        self.assertEqual(TW.line_method_changes(today, dict(today, date="2026-11-18")), [])
        self.assertEqual(TW.line_method_changes(None, today), ["line method: no season-lines record for the earlier run"])

    def test_registered_constants_added_removed_or_changed_are_named(self):
        old = [dict(module="arena", name="X", value=0.88), dict(module="season_lines", name="GONE", value=1)]
        new = [dict(module="arena", name="X", value=0.80), dict(module="season_lines", name="SWITCH_CATS", value=["pts"])]
        self.assertEqual(TW.registry_changes(old, new),
                         ["constant arena.X: 0.88 to 0.8", "constant season_lines.SWITCH_CATS added", "constant season_lines.GONE removed"])
        self.assertEqual(TW.registry_changes(new, new), [])

    def test_a_moved_title_with_a_method_change_says_so_first(self):
        r = TW.check(brief("2026-11-17", 11.3, 12.2, MOVES), brief("2026-11-16", 14.9, 14.6),
                     merges=["Merge pull request #274: x"], method=["line method: the minutes ratio now applies to PTS, REB, AST (before: none)"])
        self.assertTrue(r["moved"])
        causes = TW._causes(r)
        self.assertTrue(causes[0].startswith("METHOD CHANGE"))
        self.assertIn("part or all of the move is the method, not the league", causes[0])
        self.assertIn("METHOD CHANGE", TW.pass_line(r, "x.json"))
        self.assertIn("**Method change between the two runs.**", "\n".join(TW.render(r)))

    def test_no_method_change_reads_as_before(self):
        r = TW.check(brief("2026-11-10", 12.3, 12.2, MOVES), brief("2026-11-09", 18.1, 18.0), merges=[], method=[])
        self.assertNotIn("METHOD CHANGE", TW.pass_line(r, "x.json"))

    def test_main_reads_the_two_season_lines_records(self):
        d, s = tempfile.mkdtemp(), tempfile.mkdtemp()
        json.dump(brief("2026-11-16", 14.9, 14.6), open(os.path.join(d, "brief_2026-11-16.json"), "w"))
        json.dump(brief("2026-11-17", 11.3, 12.2), open(os.path.join(d, "brief_2026-11-17.json"), "w"))
        json.dump(dict(date="2026-11-16"), open(os.path.join(s, "season_lines_2026-11-16.json"), "w"))
        json.dump(dict(date="2026-11-17", line_switch=dict(cats=["pts", "reb", "ast"])), open(os.path.join(s, "season_lines_2026-11-17.json"), "w"))
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            TW.main(["--date", "2026-11-17", "--briefs", d, "--season", s, "--root", tempfile.mkdtemp()])
        rec = json.load(open(os.path.join(d, "title_watch_2026-11-17.json")))
        self.assertEqual(rec["method_changes"], ["line method: the minutes ratio now applies to PTS, REB, AST (before: none)"])
        self.assertIn("METHOD CHANGE", buf.getvalue())


class Walk(unittest.TestCase):
    """Owner 2026-11-17 (pick F1, after-report-2026-11-17-gaps-and-fixes.md): on a day with a method change the two
    figures are walked like for like, one input at a time on today's engine. On 2026-11-17 the watch printed
    "-0.5, within the band" over +1.9 (constants), +1.9 (rosters and results) and -4.3 (lines)."""

    METHOD = ["line method: the minutes ratio now applies to PTS, REB, AST (before: none)"]

    def test_the_walk_splits_a_small_net_change_into_its_offsetting_steps(self):
        w = TW.walk(14.6, 14.1, dict(prev_inputs=16.5, rosters=18.4, today=14.1))
        self.assertTrue(w["reproduced"])
        self.assertEqual([(s["what"], round(s["delta"], 1)) for s in w["steps"]],
                         [("the engine and its constants, on the earlier run's inputs", 1.9),
                          ("rosters and results recorded since", 1.9),
                          ("the lines file (line method and the day's games)", -4.3)])
        self.assertAlmostEqual(sum(s["delta"] for s in w["steps"]), 14.1 - 14.6)

    def test_a_change_inside_the_band_still_prints_its_walk(self):
        r = TW.check(brief("2026-11-17", 13.98, 14.19), brief("2026-11-16", 14.69, 14.52), merges=[], method=self.METHOD)
        self.assertFalse(r["moved"])
        r["walk"] = TW.walk(r["prev_title"], r["title"], dict(prev_inputs=16.5, rosters=18.4, today=r["title"]))
        text = "\n".join(TW.render(r))
        self.assertIn("Like for like", text)
        self.assertIn("| the lines file (line method and the day's games) | -4.3 |", text)
        self.assertNotIn("no larger than two runs of the same simulator differ by", text)
        self.assertIn("walk: +1.9 engine, +1.9 rosters and results, -4.3 lines", TW.pass_line(r, "x.json"))

    def test_a_brief_that_does_not_reproduce_shows_no_steps(self):
        w = TW.walk(14.6, 14.1, dict(prev_inputs=16.5, rosters=18.4, today=15.0))
        self.assertFalse(w["reproduced"]); self.assertEqual(w["steps"], [])
        self.assertIn("did not reproduce", w["error"])
        r = TW.check(brief("2026-11-17", 13.98, 14.19), brief("2026-11-16", 14.69, 14.52), merges=[], method=self.METHOD)
        r["walk"] = w
        self.assertIn("did not reproduce", "\n".join(TW.render(r)))

    def _repo(self):
        d = tempfile.mkdtemp()
        env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
        git = lambda *a: subprocess.run(["git", "-C", d] + list(a), check=True, env=env, capture_output=True)
        git("init", "-q", "-b", "daily")
        def put(rel, text):
            os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
            open(os.path.join(d, rel), "w").write(text)
        for rel, text in (("data/league_state.json", "state-am-16"), ("data/season/pool_season.csv", "pool-16"),
                          ("data/league_schedule.json", "sched-16"), ("report/briefs/brief_2026-11-16.json", "{}")):
            put(rel, text)
        git("add", "-A"); git("commit", "-q", "-m", "Morning run 2026-11-16")
        put("data/league_state.json", "state-pm-16"); git("add", "-A"); git("commit", "-q", "-m", "Afternoon check 2026-11-16")
        for rel, text in (("data/league_state.json", "state-am-17"), ("data/season/pool_season.csv", "pool-17"),
                          ("data/league_schedule.json", "sched-17"), ("report/briefs/brief_2026-11-17.json", "{}")):
            put(rel, text)
        return d

    def test_the_earlier_inputs_come_from_the_commit_that_added_its_brief(self):
        d = self._repo()
        got = TW.inputs_at(d, "2026-11-16")
        self.assertEqual({k: open(v).read() for k, v in got.items()},
                         dict(state="state-am-16", pool="pool-16", schedule="sched-16"))
        self.assertIsNone(TW.inputs_at(d, "2026-11-10"))
        self.assertIsNone(TW.inputs_at(tempfile.mkdtemp(), "2026-11-16"))

    def test_like_for_like_runs_the_three_rows_one_input_at_a_time(self):
        d, calls = self._repo(), []
        def sim(state, pool, schedule, seasons):
            row = (open(state).read(), open(pool).read(), open(schedule).read(), seasons); calls.append(row)
            return {("state-am-16", "pool-16", "sched-16"): 16.5, ("state-am-17", "pool-16", "sched-17"): 18.4,
                    ("state-am-17", "pool-17", "sched-17"): 14.1}[row[:3]]
        today = dict(state=os.path.join(d, "data/league_state.json"), pool=os.path.join(d, "data/season/pool_season.csv"),
                     schedule=os.path.join(d, "data/league_schedule.json"))
        w = TW.like_for_like(d, "2026-11-16", 14.6, 14.1, today, 10000, sim=sim)
        self.assertEqual(len(calls), 3); self.assertTrue(all(c[3] == 10000 for c in calls))
        self.assertEqual([round(s["delta"], 1) for s in w["steps"]], [1.9, 1.9, -4.3])
        self.assertEqual(w["rows"], dict(prev_inputs=16.5, rosters=18.4, today=14.1))

    def test_unreadable_history_is_said_not_guessed(self):
        w = TW.like_for_like(tempfile.mkdtemp(), "2026-11-16", 14.6, 14.1, {}, 10000, sim=lambda *a: self.fail("no run without inputs"))
        self.assertEqual(w["steps"], [])
        self.assertIn("not readable from git history", w["error"])

    def test_main_walks_only_on_a_method_change(self):
        import io, contextlib
        d = self._repo(); b = os.path.join(d, "report", "briefs"); s = tempfile.mkdtemp()
        json.dump(brief("2026-11-16", 14.69, 14.52), open(os.path.join(b, "brief_2026-11-16.json"), "w"))
        json.dump(brief("2026-11-17", 13.98, 14.19), open(os.path.join(b, "brief_2026-11-17.json"), "w"))
        subprocess.run(["git", "-C", d, "add", "-A"], check=True)
        json.dump(dict(date="2026-11-16"), open(os.path.join(s, "season_lines_2026-11-16.json"), "w"))
        json.dump(dict(date="2026-11-17"), open(os.path.join(s, "season_lines_2026-11-17.json"), "w"))
        calls, old = [], TW.SIM
        TW.SIM = lambda state, pool, schedule, seasons: (calls.append(1), {"pool-16": 16.5, "pool-17": 14.085}[open(pool).read()]
                                                         if open(state).read() == "state-am-16" or open(pool).read() == "pool-17" else 18.4)[1]
        try:
            args = ["--date", "2026-11-17", "--briefs", b, "--season", s, "--root", d, "--state", os.path.join(d, "data/league_state.json"),
                    "--pool", os.path.join(d, "data/season/pool_season.csv"), "--schedule", os.path.join(d, "data/league_schedule.json")]
            with contextlib.redirect_stdout(io.StringIO()):
                TW.main(args)
            self.assertEqual(calls, [])                                   # no method change: no walk, no simulator run
            self.assertIsNone(json.load(open(os.path.join(b, "title_watch_2026-11-17.json"))).get("walk"))
            json.dump(dict(date="2026-11-17", line_switch=dict(cats=["pts", "reb", "ast"])), open(os.path.join(s, "season_lines_2026-11-17.json"), "w"))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                TW.main(args)
            rec = json.load(open(os.path.join(b, "title_watch_2026-11-17.json")))
            self.assertEqual(len(calls), 3)
            self.assertEqual([round(x["delta"], 1) for x in rec["walk"]["steps"]], [1.9, 1.9, -4.3])
            self.assertIn("walk:", buf.getvalue())
            with contextlib.redirect_stdout(io.StringIO()):
                TW.main(args + ["--no-walk"])
            self.assertEqual(len(calls), 3)
        finally:
            TW.SIM = old

    def test_the_simulator_row_plays_the_files_it_is_given(self):
        """One real run at a small size: the row reads the state, pool and schedule handed to it, in its own process."""
        kit = os.path.dirname(HERE)
        t = TW.SIM(os.path.join(kit, "data", "league_state.json"), os.path.join(kit, "data", "season", "pool_season.csv"),
                   os.path.join(kit, "data", "league_schedule.json"), 200)
        self.assertTrue(0.0 <= t <= 100.0)


class Files(unittest.TestCase):
    def test_the_previous_brief_is_the_newest_before_the_date_and_never_a_pm_file(self):
        d = tempfile.mkdtemp()
        for n in ("brief_2026-11-07.json", "brief_2026-11-09.json", "brief_2026-11-10.json", "brief_2026-11-09_pm.json", "morning_2026-11-09.json"):
            json.dump(dict(date=n[6:16]), open(os.path.join(d, n), "w"))
        self.assertEqual(os.path.basename(TW.prev_brief("2026-11-10", d)), "brief_2026-11-09.json")
        self.assertIsNone(TW.prev_brief("2026-11-07", d))

    def test_merges_between_two_runs_come_from_git(self):
        d = tempfile.mkdtemp()
        env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
        def git(*a, date=None):
            e = dict(env, GIT_COMMITTER_DATE=date, GIT_AUTHOR_DATE=date) if date else env
            subprocess.run(["git", "-C", d] + list(a), check=True, env=e, capture_output=True)
        git("init", "-q", "-b", "daily")
        git("commit", "--allow-empty", "-m", "base", date="2026-11-08T10:00:00Z")
        git("checkout", "-q", "-b", "feat"); git("commit", "--allow-empty", "-m", "work", date="2026-11-08T11:00:00Z")
        git("checkout", "-q", "daily")
        git("merge", "--no-ff", "-m", "Merge pull request #7: old", "feat", date="2026-11-08T12:00:00Z")
        git("checkout", "-q", "-b", "feat2"); git("commit", "--allow-empty", "-m", "work2", date="2026-11-09T15:00:00Z")
        git("checkout", "-q", "daily")
        git("merge", "--no-ff", "-m", "Merge pull request #8: new", "feat2", date="2026-11-09T16:00:00Z")
        self.assertEqual(TW.kit_merges(d, "2026-11-09T13:00:00Z"), ["Merge pull request #8: new"])
        self.assertEqual(TW.kit_merges(d, "2026-11-09T17:00:00Z"), [])
        self.assertIsNone(TW.kit_merges(tempfile.mkdtemp(), "2026-11-09T13:00:00Z"))
        self.assertIsNone(TW.kit_merges(d, None))

    def test_main_writes_the_record_beside_the_briefs(self):
        d = tempfile.mkdtemp()
        json.dump(brief("2026-11-09", 18.1, 17.96), open(os.path.join(d, "brief_2026-11-09.json"), "w"))
        json.dump(brief("2026-11-10", 12.32, 12.23, MOVES), open(os.path.join(d, "brief_2026-11-10.json"), "w"))
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = TW.main(["--date", "2026-11-10", "--briefs", d, "--root", tempfile.mkdtemp()])
        self.assertEqual(rc, 0)
        self.assertTrue(buf.getvalue().startswith("TITLE WATCH: PASS"))
        rec = json.load(open(os.path.join(d, "title_watch_2026-11-10.json")))
        self.assertTrue(rec["moved"])
        self.assertTrue(os.path.exists(os.path.join(d, "title_watch_2026-11-10.md")))

    def test_no_brief_for_the_day_halts(self):
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = TW.main(["--date", "2026-11-10", "--briefs", tempfile.mkdtemp()])
        self.assertEqual(rc, 1); self.assertIn("HALT", buf.getvalue())


class MorningStep(unittest.TestCase):
    def test_the_step_runs_after_the_brief_and_is_not_fatal(self):
        st = M.steps("2026-11-10", seasons=2000)
        names = [s["name"] for s in st]
        self.assertLess(names.index("daily brief"), names.index("title watch"))
        s = st[names.index("title watch")]
        self.assertFalse(s.get("fatal", True))
        self.assertEqual(s["pass_re"], r"^TITLE WATCH: PASS")


if __name__ == "__main__":
    unittest.main()
