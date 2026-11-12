#!/usr/bin/env python3
"""Red-first tests for scripts/morning.py (the in-season morning run: box scores, season lines, season board,
status feed, daily brief, each step recorded like a gate; Council 2026-10-19 decisions 6 and 7).

    python3 scripts/test_morning.py
"""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import morning as M  # noqa: E402

PY = sys.executable


class Steps(unittest.TestCase):
    def test_steps_in_order_with_dates(self):
        st = M.steps("2026-10-21", fetch=True, seasons=10000)
        # 2026-10-21: "preflight" became step 0 (independent-audit adoption); the indices below moved by one.
        # 2026-10-23 (owner, Build 1): "league table" after the week matchup, before the deck that draws it
        # 2026-10-26 (owner, "results so far"): "league pairings" before the brief that runs the simulator
        self.assertEqual([s["name"] for s in st], ["preflight", "league live", "matchup live", "box scores 2026-10-20", "manager log 2026-10-20", "tag outcomes", "lineup log", "accuracy render", "season lines", "minutes line", "threes line", "season board", "status feed", "transactions", "league pairings", "il return", "daily brief", "decision log", "title watch", "week matchup", "decision card", "league table", "form board", "season deck"])
        self.assertIn("2026-10-20", st[3]["cmd"])
        self.assertIn("2026-10-20", st[4]["cmd"])   # 2026-11-12 (audit F1): "manager log" logs yesterday; indices below +1
        self.assertIn("2026-10-20", st[5]["cmd"])   # 2026-10-27: "tag outcomes" grades yesterday; indices below moved by one
        self.assertIn("2026-10-21", st[6]["cmd"])    # 2026-11-05: "lineup log" takes the morning date and grades the day before
        self.assertIn("2026-10-21", st[15]["cmd"])   # 2026-11-12: "threes line" after the minutes line; +1; 2026-10-27: "minutes line" after season lines; +1 again; 2026-11-02: "accuracy render"; +1; 2026-11-05: "lineup log"; +1
        self.assertTrue(all(s["pass_re"] for s in st))

    def test_no_fetch_skips_the_box_score_step(self):
        st = M.steps("2026-10-21", fetch=False, seasons=10000)
        self.assertEqual(st[1]["name"], "tag outcomes")  # st[0] is the preflight since 2026-10-21; tag outcomes since 2026-10-27
        self.assertEqual(st[2]["name"], "lineup log")  # since 2026-11-05
        self.assertEqual(st[3]["name"], "accuracy render")  # since 2026-11-02
        self.assertEqual(st[4]["name"], "season lines")
        self.assertEqual(st[5]["name"], "minutes line")
        self.assertNotIn("transactions", [s["name"] for s in st])
        self.assertNotIn("league live", [s["name"] for s in st])

    def test_status_gate_checks_the_runs_own_dated_file(self):
        # 2026-10-20: --check with no file read the newest-dated file (a test run's 10/21), not the morning's own
        st = M.steps("2026-10-20", fetch=False, seasons=10000)
        gate = next(s for s in st if s["name"] == "status feed")["cmd"][-1]
        self.assertIn("--check", gate); self.assertTrue(gate.endswith("status_2026-10-20.json"))

    def test_since_reaches_the_transcript_readers_and_only_them(self):
        # GAUNTLET 2026-10-21 item 7: the persistent runner passes its start time so yesterday's pull never counts
        st = M.steps("2026-10-21", fetch=True, seasons=10000, since="2026-10-21T12:53:00Z")
        for s in st:
            has = "--since" in s["cmd"]
            self.assertEqual(has, s["name"] in ("league live", "matchup live", "manager log 2026-10-20"), s["name"])   # 2026-11-12 (audit F1): the manager log reads get_transactions from the transcript
            if has:
                self.assertEqual(s["cmd"][s["cmd"].index("--since") + 1], "2026-10-21T12:53:00Z")
        self.assertFalse(any("--since" in s["cmd"] for s in M.steps("2026-10-21", fetch=True, seasons=10000)))

    def test_brief_runs_on_the_season_pool(self):
        st = M.steps("2026-10-21", fetch=True, seasons=10000)
        brief = next(s for s in st if s["name"] == "daily brief")
        self.assertTrue(brief["env"]["SEASON_POOL"].endswith(os.path.join("data", "season", "pool_season.csv")))


    def test_week_matchup_runs_on_the_season_pool_before_the_deck_and_never_stops_the_run(self):
        # owner 2026-10-21: the Today tab's week card; a failure leaves the deck without the card, never without a deck
        for fetch in (True, False):
            names = [s["name"] for s in M.steps("2026-10-22", fetch=fetch, seasons=10000)]
            self.assertLess(names.index("daily brief"), names.index("week matchup"))
            self.assertLess(names.index("week matchup"), names.index("season deck"))
        wm = next(s for s in M.steps("2026-10-22", fetch=True, seasons=10000) if s["name"] == "week matchup")
        self.assertIs(wm["fatal"], False)
        self.assertIn("2026-10-22", wm["cmd"]); self.assertEqual(wm["pass_re"], r"^WEEK MATCHUP: PASS")
        self.assertTrue(wm["env"]["SEASON_POOL"].endswith(os.path.join("data", "season", "pool_season.csv")))

class Run(unittest.TestCase):
    def test_a_failing_step_fails_the_morning_and_later_steps_do_not_run(self):
        ok = {"name": "ok", "cmd": [PY, "-c", "print('STEP: PASS')"], "cwd": ".", "pass_re": "STEP: PASS", "env": {}}
        bad = {"name": "bad", "cmd": [PY, "-c", "print('STEP: FAIL'); raise SystemExit(1)"], "cwd": ".", "pass_re": "STEP: PASS", "env": {}}
        with tempfile.TemporaryDirectory() as d:
            rec = M.run_steps([ok, bad, ok], os.path.join(d, "m.json"))
            self.assertEqual(rec["verdict"], "FAIL")
            self.assertEqual([s["verdict"] for s in rec["steps"]], ["PASS", "FAIL", "SKIPPED"])
            self.assertTrue(os.path.exists(os.path.join(d, "m.json")))

    def test_all_pass_is_pass_with_the_pass_lines(self):
        ok = {"name": "ok", "cmd": [PY, "-c", "print('STEP: PASS — fine')"], "cwd": ".", "pass_re": "STEP: PASS", "env": {}}
        with tempfile.TemporaryDirectory() as d:
            rec = M.run_steps([ok, ok], os.path.join(d, "m.json"))
            self.assertEqual(rec["verdict"], "PASS"); self.assertIn("fine", rec["steps"][0]["pass_line"])



class NonFatal(unittest.TestCase):
    """Owner 2026-10-20 (plan-gate A5): a failed live pull keeps the last paste and the morning goes on."""

    def test_league_live_is_marked_non_fatal(self):
        st = M.steps("2026-10-21", fetch=True, seasons=10000)
        for name in ("league live", "matchup live"):
            step = next(s for s in st if s["name"] == name)
            self.assertFalse(step.get("fatal", True), name)

    def test_a_non_fatal_fail_does_not_stop_the_run(self):
        import tempfile, os, sys
        st = [dict(name="a", cmd=[sys.executable, "-c", "print('NOPE'); raise SystemExit(1)"], cwd=".", pass_re=r"^YES", env={}, fatal=False),
              dict(name="b", cmd=[sys.executable, "-c", "print('OK B')"], cwd=".", pass_re=r"^OK B", env={})]
        out = os.path.join(tempfile.mkdtemp(), "m.json")
        rec = M.run_steps(st, out)
        self.assertEqual([x["verdict"] for x in rec["steps"]], ["FAIL (non-fatal)", "PASS"])
        self.assertEqual(rec["verdict"], "PASS")


class Pairings(unittest.TestCase):
    def test_the_morning_refreshes_the_schedules_played_weeks_before_the_brief(self):
        # owner 2026-10-26 ("full pairings + results so far"): the simulator starts each season from the weeks already
        # final, so the schedule file's played block is recompiled every morning from data/weeks, before the brief
        # that runs the simulator; non-fatal (a failed compile leaves the last schedule file standing)
        names = [s["name"] for s in M.steps("2026-10-27")]
        self.assertIn("league pairings", names)
        self.assertLess(names.index("league pairings"), names.index("daily brief"))
        st = next(s for s in M.steps("2026-10-27") if s["name"] == "league pairings")
        self.assertFalse(st.get("fatal", True))
        self.assertIn("league_pairings.py", " ".join(st["cmd"]))


class MondaySweep(unittest.TestCase):
    """Owner 2026-10-26 ("re-measure the ranges every Monday"): on a Monday the season sweep runs on the real schedule
    before the brief, writes a dated record with its inputs pinned, and a failure does not stop the morning."""
    def test_a_monday_runs_the_season_sweep_before_the_brief(self):
        st = M.steps("2026-11-02")
        names = [s["name"] for s in st]
        self.assertIn("season sweep", names)
        self.assertLess(names.index("league pairings"), names.index("season sweep"))
        self.assertLess(names.index("season sweep"), names.index("daily brief"))
        sw = next(s for s in st if s["name"] == "season sweep")
        self.assertFalse(sw.get("fatal", True))
        cmd = " ".join(sw["cmd"])
        for part in ("sweep.py", "--season", "--real-schedule", os.path.join("redteam-2026-11-02-season", "sweep.json")):
            self.assertIn(part, cmd)

    def test_another_day_does_not(self):
        self.assertNotIn("season sweep", [s["name"] for s in M.steps("2026-11-03")])


class SundayForecasts(unittest.TestCase):
    """Owner 2026-10-27 (the weekly accuracy card): on the Sunday before a week, the morning records next week's
    forecasts (the owner's matchup and every matchup) and snapshots the season lines they rest on; non-fatal."""
    def test_a_sunday_records_next_weeks_forecasts(self):
        st = next((s for s in M.steps("2026-11-01") if s["name"] == "next week forecasts"), None)
        self.assertIsNotNone(st)
        self.assertFalse(st.get("fatal", True))
        cmd = " ".join(st["cmd"])
        for part in ("weekly_preview.py", "--week 3", "--record", "--league", "--snapshot"):
            self.assertIn(part, cmd)
        self.assertIn("SEASON_POOL", st["env"])

    def test_another_day_does_not(self):
        self.assertNotIn("next week forecasts", [s["name"] for s in M.steps("2026-11-02")])


class ManagerLog(unittest.TestCase):
    """Audit finding F1 (2026-11-12): the league's moves file was rewritten after the morning deck had pinned it,
    because the manager log ran outside the sequence. It is a step: after the pull and the box scores it reads,
    before everything that reads the moves file, non-fatal, on fetch runs only."""
    def test_it_runs_after_its_inputs_and_before_every_reader_of_the_moves_file(self):
        st = M.steps("2026-11-12", since="2026-11-12T13:03:00Z")
        names = [s["name"] for s in st]
        i = names.index("manager log 2026-11-11")
        self.assertLess(names.index("league live"), i)
        self.assertLess(names.index("box scores 2026-11-11"), i)
        for reader in ("daily brief", "week matchup", "season deck"):
            self.assertLess(i, names.index(reader), reader)
        m = st[i]
        self.assertIs(m["fatal"], False)
        self.assertEqual(m["pass_re"], r"^MANAGER LOG: PASS")
        self.assertIn("--date 2026-11-11 --since 2026-11-12T13:03:00Z", " ".join(m["cmd"]))

    def test_a_run_without_fetches_does_not_read_the_transcript(self):
        self.assertEqual([s for s in M.steps("2026-11-12", fetch=False) if s["name"].startswith("manager log")], [])


class TagOutcomes(unittest.TestCase):
    """Owner 2026-10-27 (build 4, "capture now"): after yesterday's box scores land, what each player flagged in
    yesterday's status file then did is appended to the tag-outcomes ledger; non-fatal."""
    def test_yesterdays_tags_are_graded_after_the_box_scores_and_before_the_status_feed(self):
        st = M.steps("2026-10-27")
        names = [s["name"] for s in st]
        self.assertIn("tag outcomes", names)
        self.assertLess(names.index("box scores 2026-10-26"), names.index("tag outcomes"))
        self.assertLess(names.index("tag outcomes"), names.index("status feed"))
        t = next(s for s in st if s["name"] == "tag outcomes")
        self.assertFalse(t.get("fatal", True))
        self.assertIn("--date 2026-10-26", " ".join(t["cmd"]))

    def test_no_fetch_still_grades_yesterday(self):
        self.assertIn("tag outcomes", [s["name"] for s in M.steps("2026-10-27", fetch=False)])


class MinutesLine(unittest.TestCase):
    """Owner 2026-10-27 (build 2): the minutes-trend candidate line is written every morning right after the season
    lines it scales; non-fatal, and nothing downstream reads it."""
    def test_the_candidate_runs_after_season_lines_and_is_non_fatal(self):
        st = M.steps("2026-10-28")
        names = [s["name"] for s in st]
        self.assertEqual(names.index("minutes line"), names.index("season lines") + 1)
        m = next(s for s in st if s["name"] == "minutes line")
        self.assertFalse(m.get("fatal", True))
        self.assertIn("--date 2026-10-28", " ".join(m["cmd"]))


class Manifest(unittest.TestCase):
    """Owner 2026-10-26, option 2A: the run says which paths it wrote, measured from the tree, so a new output script
    can never go silently uncommitted (report/league, report/form and report/calibration* each drifted out of the
    prompt's hand-kept list)."""
    def repo(self):
        import subprocess, tempfile, os
        d = tempfile.mkdtemp()
        for c in (["init", "-q", "-b", "main"], ["config", "user.email", "t@t"], ["config", "user.name", "t"]):
            subprocess.run(["git", *c], cwd=d, capture_output=True)
        os.makedirs(os.path.join(d, "data"), exist_ok=True)
        open(os.path.join(d, "data", "seed.txt"), "w").write("x\n")
        subprocess.run(["git", "add", "-A"], cwd=d, capture_output=True)
        subprocess.run(["git", "-c", "commit.gpgsign=false", "commit", "-qm", "seed"], cwd=d, capture_output=True)
        return d

    def test_each_step_reports_the_paths_it_wrote_and_the_run_lists_them_all(self):
        import os
        d = self.repo()
        mk = lambda name, rel: dict(name=name, cwd=d, pass_re="STEP: PASS", env={},
                                    cmd=[PY, "-c", f"import os,pathlib;p=pathlib.Path({rel!r});p.parent.mkdir(parents=True,exist_ok=True);p.write_text('v');print('STEP: PASS')"])
        st = [mk("a", "report/league/league_2026-10-26.json"), mk("b", "report/form/form_2026-10-26.csv")]
        rec = M.run_steps(st, os.path.join(d, "m.json"), root=d)
        self.assertEqual(rec["steps"][0]["wrote"], ["report/league/league_2026-10-26.json"])
        self.assertEqual(rec["steps"][1]["wrote"], ["report/form/form_2026-10-26.csv"])
        self.assertEqual(rec["wrote"], ["report/form/form_2026-10-26.csv", "report/league/league_2026-10-26.json"])

    def test_a_step_that_writes_nothing_reports_an_empty_list(self):
        import os
        d = self.repo()
        st = [dict(name="quiet", cwd=d, pass_re="STEP: PASS", env={}, cmd=[PY, "-c", "print('STEP: PASS')"])]
        rec = M.run_steps(st, os.path.join(d, "m.json"), root=d)
        self.assertEqual(rec["steps"][0]["wrote"], []); self.assertEqual(rec["wrote"], [])

    def test_outside_a_git_tree_the_manifest_says_unattributed_not_empty(self):
        import os, tempfile
        d = tempfile.mkdtemp()
        st = [dict(name="a", cwd=d, pass_re="STEP: PASS", env={}, cmd=[PY, "-c", "print('STEP: PASS')"])]
        rec = M.run_steps(st, os.path.join(d, "m.json"), root=d)
        self.assertIsNone(rec["steps"][0]["wrote"])
        self.assertEqual(rec["wrote"], "unattributed (not a git checkout)")

    def test_the_wrote_block_is_printed_for_the_runner_to_commit(self):
        import os, io, contextlib
        d = self.repo()
        st = [dict(name="a", cwd=d, pass_re="STEP: PASS", env={},
                   cmd=[PY, "-c", "import pathlib;p=pathlib.Path('report/league/x.json');p.parent.mkdir(parents=True,exist_ok=True);p.write_text('v');print('STEP: PASS')"])]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rec = M.run_steps(st, os.path.join(d, "m.json"), root=d)
            M.print_manifest(rec)
        out = buf.getvalue()
        self.assertIn("WROTE: 1 path(s)", out); self.assertIn("report/league/x.json", out)


class DecisionLog(unittest.TestCase):
    """Owner 2026-10-31 (the decision log): the brief's row and the owner's moves are logged right after the brief every
    day; on a Monday the grader runs after them. Both non-fatal."""

    def test_log_follows_the_brief_every_day_and_the_grader_runs_on_mondays(self):
        for day, monday in (("2026-10-30", False), ("2026-11-02", True)):
            st = M.steps(day, fetch=False, seasons=10)
            names = [s["name"] for s in st]
            self.assertEqual(names.index("decision log"), names.index("daily brief") + 1, day)
            self.assertEqual("decision grades" in names, monday, day)
            log = next(s for s in st if s["name"] == "decision log")
            self.assertEqual(log["cmd"][-4:], ["--brief", day, "--moves", "--rejoin"]); self.assertFalse(log["fatal"])
            if monday:
                g = next(s for s in st if s["name"] == "decision grades")
                self.assertEqual(g["cmd"][-2:], ["--as-of", day]); self.assertFalse(g["fatal"])
                self.assertLess(names.index("decision log"), names.index("decision grades"))



class IlReturn(unittest.TestCase):
    """Owner 2026-10-31 (4a): the IL-return scenario range runs right before the brief every day, on the season pool,
    non-fatal."""

    def test_il_return_runs_before_the_brief_on_the_season_pool_and_is_not_fatal(self):
        st = M.steps("2026-11-03", fetch=False, seasons=10)
        names = [s["name"] for s in st]
        self.assertEqual(names.index("il return"), names.index("daily brief") - 1)
        step = next(s for s in st if s["name"] == "il return")
        self.assertEqual(step["cmd"][-4:], ["--date", "2026-11-03", "--seasons", "10"]); self.assertFalse(step["fatal"])
        self.assertEqual(step["env"], next(s for s in st if s["name"] == "daily brief")["env"])



class PreviewStaleness(unittest.TestCase):
    """Owner 2026-11-09 ("Band + staleness"): Mondays only, the week's preview names the moves since its rosters."""
    def test_monday_runs_the_note_for_the_current_week_and_other_days_do_not(self):
        mon = [x for x in M.steps("2026-11-09") if x["name"] == "preview staleness"]
        self.assertEqual(len(mon), 1)
        self.assertEqual(mon[0]["cmd"][-4:], ["--week", str(M._week_of("2026-11-09")), "--stale-note", "2026-11-09"])
        self.assertFalse(mon[0]["fatal"])
        self.assertEqual([x for x in M.steps("2026-11-10") if x["name"] == "preview staleness"], [])


class Resume(unittest.TestCase):
    """Owner 2026-11-11 (audit pick A, "Self-healing morning"): a failed morning is finished by running only the steps
    that did not pass; the record keeps both attempts. On 2026-11-11 this was done by hand."""
    def steps(self, d, bad_ok):
        mark = os.path.join(d, "ran.txt")
        def step(name, code, fatal=True):
            return {"name": name, "cmd": [PY, "-c", f"open({mark!r},'a').write({name!r}+'\\n'); {code}"], "cwd": ".",
                    "pass_re": "STEP: PASS", "env": {}, "fatal": fatal}
        ok = "print('STEP: PASS')"; bad = ok if bad_ok else "print('no'); raise SystemExit(1)"
        return [step("a", ok), step("b", bad), step("c", ok)], mark

    def test_only_the_steps_that_did_not_pass_run_again(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "m.json")
            st, mark = self.steps(d, bad_ok=False)
            first = M.run_steps(st, out)
            self.assertEqual([s["verdict"] for s in first["steps"]], ["PASS", "FAIL", "SKIPPED"])
            os.remove(mark)
            st, mark = self.steps(d, bad_ok=True)
            rec = M.resume_steps(st, out)
            self.assertEqual(open(mark).read().split(), ["b", "c"])            # a passed the first time: not run again
            self.assertEqual(rec["verdict"], "PASS")
            self.assertEqual([(s["name"], s["verdict"]) for s in rec["steps"]], [("a", "PASS"), ("b", "PASS"), ("c", "PASS")])
            self.assertEqual(rec["ran_at_utc"], first["ran_at_utc"])
            self.assertEqual(len(rec["attempts"]), 1)
            self.assertEqual(rec["attempts"][0]["verdict"], "FAIL")
            self.assertEqual([s["name"] for s in rec["attempts"][0]["not_passed"]], ["b", "c"])
            self.assertIn("resumed_at_utc", rec)
            self.assertEqual(json.load(open(out)), rec)                         # the merged record is the one on disk

    def test_a_resume_that_fails_again_stays_fail_and_can_be_resumed_again(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "m.json")
            st, _ = self.steps(d, bad_ok=False)
            M.run_steps(st, out)
            rec = M.resume_steps(st, out)
            self.assertEqual(rec["verdict"], "FAIL")
            self.assertEqual([s["verdict"] for s in rec["steps"]], ["PASS", "FAIL", "SKIPPED"])
            st, _ = self.steps(d, bad_ok=True)
            rec = M.resume_steps(st, out)
            self.assertEqual(rec["verdict"], "PASS"); self.assertEqual(len(rec["attempts"]), 2)

    def test_nothing_to_resume_runs_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "m.json")
            st, mark = self.steps(d, bad_ok=True)
            first = M.run_steps(st, out); os.remove(mark)
            rec = M.resume_steps(st, out)
            self.assertFalse(os.path.exists(mark))
            self.assertEqual(rec, first)

    def test_no_record_yet_is_a_full_run(self):
        with tempfile.TemporaryDirectory() as d:
            st, mark = self.steps(d, bad_ok=True)
            rec = M.resume_steps(st, os.path.join(d, "m.json"))
            self.assertEqual(open(mark).read().split(), ["a", "b", "c"]); self.assertNotIn("attempts", rec)

    def test_a_non_fatal_failure_is_retried_too(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "m.json")
            st, mark = self.steps(d, bad_ok=False); st[1]["fatal"] = False
            first = M.run_steps(st, out)
            self.assertEqual([s["verdict"] for s in first["steps"]], ["PASS", "FAIL (non-fatal)", "PASS"])
            os.remove(mark)
            st, mark = self.steps(d, bad_ok=True); st[1]["fatal"] = False
            rec = M.resume_steps(st, out)
            self.assertEqual(open(mark).read().split(), ["b"])
            self.assertEqual([s["verdict"] for s in rec["steps"]], ["PASS", "PASS", "PASS"])

    def test_the_command_line_lists_resume(self):
        import subprocess
        out = subprocess.run([PY, os.path.join(HERE, "morning.py"), "--help"], capture_output=True, text=True).stdout
        self.assertIn("--resume", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)


class LedgerParent(unittest.TestCase):
    def test_every_step_runs_with_the_morning_named_as_ledger_parent(self):
        # owner 2026-10-23 (D5): the step scripts record their own ledger rows when run alone; under the morning run
        # they must not, since run_steps records 'morning: <step>' itself
        d = tempfile.mkdtemp()
        step = {"name": "echo", "cmd": [PY, "-c", "import os; print('PARENT ' + os.environ.get('KIT_LEDGER_PARENT', 'none'))"],
                "cwd": ".", "pass_re": r"^PARENT morning$", "env": {}}
        rec = M.run_steps([step], os.path.join(d, "m.json"))
        self.assertEqual(rec["steps"][0]["verdict"], "PASS", rec["steps"][0])


class DecisionCardStep(unittest.TestCase):
    """Owner 2026-11-10 (pick "Decision card + watchdog"): the card runs every day after the week card, which scores
    the brief's pairs for it, and before the deck; non-fatal."""
    def test_the_card_follows_the_week_card_and_precedes_the_deck(self):
        names = [x["name"] for x in M.steps("2026-11-10")]
        self.assertLess(names.index("daily brief"), names.index("week matchup"))
        self.assertLess(names.index("week matchup"), names.index("decision card"))
        self.assertLess(names.index("decision card"), names.index("season deck"))
        s = next(x for x in M.steps("2026-11-10", seasons=2000) if x["name"] == "decision card")
        self.assertFalse(s["fatal"]); self.assertIn("SEASON_POOL", s["env"])
        self.assertEqual(s["cmd"][-4:], ["--date", "2026-11-10", "--seasons", "2000"])
        self.assertTrue(s["pass_re"].startswith("^DECISION CARD: PASS"))
