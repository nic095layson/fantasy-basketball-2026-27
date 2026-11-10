#!/usr/bin/env python3
"""Red-first tests for scripts/run_watch.py (owner 2026-11-10, pick "Decision card + watchdog", P4): one line saying
whether the day's morning or afternoon run left its records, for a scheduled check that alerts the owner only on a
miss. The scheduler's own "succeeded" only means the wake was delivered.

    python3 scripts/test_run_watch.py
"""
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run_watch as RW  # noqa: E402

D = "2026-11-10"


def reader(files):
    return lambda path: files.get(path)


def morning(verdict="PASS", bad=()):
    steps = [dict(name=n, verdict="PASS") for n in ("preflight", "daily brief", "season deck")]
    steps += [dict(name=n, verdict=v) for n, v in bad]
    return json.dumps(dict(verdict=verdict, steps=steps))


class Morning(unittest.TestCase):
    AM = {f"report/briefs/morning_{D}.json": morning(), f"report/briefs/morning_report_{D}.md": "x",
          f"report/season/deck_{D}.html": "x"}

    def test_a_clean_morning_passes(self):
        v, line = RW.check(D, "am", reader(self.AM))
        self.assertEqual(v, "PASS")
        self.assertEqual(line, f"RUN WATCH: PASS — am {D}: morning PASS, 3 steps, no step failed")

    def test_no_record_alerts_and_names_the_file(self):
        v, line = RW.check(D, "am", reader({}))
        self.assertEqual(v, "ALERT"); self.assertIn(f"no morning record (report/briefs/morning_{D}.json)", line)
        self.assertTrue(line.startswith(f"RUN WATCH: ALERT — am {D}: "))

    def test_a_failed_morning_alerts_with_the_steps(self):
        f = dict(self.AM); f[f"report/briefs/morning_{D}.json"] = morning("FAIL", [("daily brief 2", "FAIL")])
        v, line = RW.check(D, "am", reader(f))
        self.assertEqual(v, "ALERT"); self.assertIn("morning verdict FAIL", line); self.assertIn("daily brief 2", line)

    def test_a_non_fatal_step_failure_alerts_by_name(self):
        f = dict(self.AM); f[f"report/briefs/morning_{D}.json"] = morning("PASS", [("league table", "FAIL (non-fatal)")])
        v, line = RW.check(D, "am", reader(f))
        self.assertEqual(v, "ALERT"); self.assertIn("morning PASS but 1 step failed: league table", line)

    def test_a_missing_deck_or_report_alerts(self):
        for gone, word in ((f"report/season/deck_{D}.html", "no deck"), (f"report/briefs/morning_report_{D}.md", "no morning report")):
            f = dict(self.AM); del f[gone]
            v, line = RW.check(D, "am", reader(f))
            self.assertEqual(v, "ALERT"); self.assertIn(word, line)

    def test_an_unreadable_record_alerts(self):
        f = dict(self.AM); f[f"report/briefs/morning_{D}.json"] = "{not json"
        v, line = RW.check(D, "am", reader(f))
        self.assertEqual(v, "ALERT"); self.assertIn("unreadable", line)


class Afternoon(unittest.TestCase):
    PM = {f"report/briefs/afternoon_report_{D}.md": "x", f"report/season/deck_{D}_pm.html": "x", f"data/status/status_{D}_pm.json": "{}"}

    def test_a_clean_afternoon_passes(self):
        v, line = RW.check(D, "pm", reader(self.PM))
        self.assertEqual((v, line), ("PASS", f"RUN WATCH: PASS — pm {D}: afternoon report, status and deck are in"))

    def test_each_missing_piece_is_named(self):
        v, line = RW.check(D, "pm", reader({f"data/status/status_{D}_pm.json": "{}"}))
        self.assertEqual(v, "ALERT")
        self.assertIn("no afternoon report", line); self.assertIn("no afternoon deck", line); self.assertNotIn("no afternoon status", line)


class Cli(unittest.TestCase):
    def test_a_root_directory_is_read_and_the_exit_code_follows_the_verdict(self):
        import subprocess, tempfile
        d = tempfile.mkdtemp()
        r = subprocess.run([sys.executable, os.path.join(HERE, "run_watch.py"), "--date", D, "--phase", "am", "--root", d],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 1); self.assertIn("RUN WATCH: ALERT", r.stdout)
        for p, body in Morning.AM.items():
            os.makedirs(os.path.dirname(os.path.join(d, p)), exist_ok=True)
            open(os.path.join(d, p), "w").write(body)
        r = subprocess.run([sys.executable, os.path.join(HERE, "run_watch.py"), "--date", D, "--phase", "am", "--root", d],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0); self.assertIn("RUN WATCH: PASS", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
