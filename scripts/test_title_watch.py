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
