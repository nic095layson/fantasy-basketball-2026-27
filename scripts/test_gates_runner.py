#!/usr/bin/env python3
"""Red-first tests for scripts/gates.py (plan 2026-10-15 §4 D3; RULES.md rule 7).

The runner must refuse what a terminal glance accepts: a gate that exits 0 with no
PASS line (the 10/15 empty-log near-miss), a gate that prints PASS and exits 1, and a
gates.json whose recorded inputs no longer match the files on disk.

    python3 scripts/test_gates_runner.py
"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gates as G  # noqa: E402

PY = sys.executable


def gate(name, code, pass_re="GATE: PASS"):
    return {"name": name, "cmd": [PY, "-c", code], "cwd": ".", "pass_re": pass_re}


OK = gate("ok", "print('GATE: PASS — fine')")
EMPTY = gate("empty", "pass")                                  # exit 0, no output
LIAR = gate("liar", "print('GATE: PASS'); raise SystemExit(1)")  # PASS text, exit 1
FAIL = gate("fail", "print('GATE: FAIL'); raise SystemExit(1)")


class RunGate(unittest.TestCase):
    def test_pass_needs_exit0_and_pass_line(self):
        r = G.run_gate(OK)
        self.assertEqual((r["exit"], r["verdict"]), (0, "PASS"))
        self.assertIn("GATE: PASS", r["pass_line"])

    def test_exit0_with_empty_log_is_fail(self):
        r = G.run_gate(EMPTY)
        self.assertEqual(r["exit"], 0)
        self.assertEqual(r["verdict"], "FAIL")
        self.assertEqual(r["pass_line"], "")

    def test_pass_text_with_nonzero_exit_is_fail(self):
        self.assertEqual(G.run_gate(LIAR)["verdict"], "FAIL")

    def test_overall_verdict_fails_if_any_gate_fails(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(G.run_all([OK, OK], inputs=[], root=d)["verdict"], "PASS")
            self.assertEqual(G.run_all([OK, FAIL], inputs=[], root=d)["verdict"], "FAIL")
            self.assertEqual(G.run_all([], inputs=[], root=d)["verdict"], "FAIL")


class Verify(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.inp = os.path.join(self.d, "report.md")
        with open(self.inp, "w") as f:
            f.write("report v1\n")
        self.out = os.path.join(self.d, "gates.json")

    def write(self, specs):
        rec = G.run_all(specs, inputs=[self.inp], root=self.d)
        with open(self.out, "w") as f:
            json.dump(rec, f)
        return rec

    def test_fresh_pass_record_verifies(self):
        self.write([OK])
        ok, problems = G.verify(self.out, root=self.d)
        self.assertTrue(ok, problems)

    def test_changed_input_is_refused(self):
        self.write([OK])
        with open(self.inp, "a") as f:
            f.write("edited after the gates ran\n")
        ok, problems = G.verify(self.out, root=self.d)
        self.assertFalse(ok)
        self.assertTrue(any("report.md" in p for p in problems), problems)

    def test_missing_record_is_refused(self):
        ok, _ = G.verify(self.out, root=self.d)
        self.assertFalse(ok)

    def test_failing_record_is_refused(self):
        self.write([OK, EMPTY])
        ok, problems = G.verify(self.out, root=self.d)
        self.assertFalse(ok)
        self.assertTrue(any("empty" in p for p in problems), problems)

    def test_verify_refuses_a_record_that_does_not_cover_the_named_report(self):
        # 2026-10-15 (item 5): a failed chain left item 2's gates.json in place and --verify passed it
        self.write([OK])
        other = os.path.join(self.d, "other-report.md")
        open(other, "w").write("a different report\n")
        ok, problems = G.verify(self.out, root=self.d, report=other)
        self.assertFalse(ok)
        self.assertTrue(any("does not cover" in p for p in problems), problems)
        ok, problems = G.verify(self.out, root=self.d, report=self.inp)
        self.assertTrue(ok, problems)

    def test_quote_carries_pass_lines_and_exit_codes(self):
        rec = self.write([OK])
        q = G.quote(rec)
        self.assertIn("GATE: PASS — fine", q)
        self.assertIn("exit 0", q)
        self.assertIn("verdict: PASS", q)


class RedTeam(unittest.TestCase):
    """--redteam SWEEP adds the three standing red-team gates (post-mortem 2026-10-19 D-PM-1)."""
    def test_redteam_gates_are_the_three_checks(self):
        specs = G.redteam_gates("/x/report.md", "/x/sweep.json", "/deck")
        self.assertEqual([s["name"] for s in specs],
                         ["redteam constants", "redteam bands", "redteam attacks"])
        self.assertEqual([s["pass_re"] for s in specs],
                         [r"^CONSTANTS CHECK: PASS", r"^BANDS CHECK: PASS", r"^ATTACKS CHECK: PASS"])
        self.assertTrue(all(s["cwd"] == G.KIT for s in specs))
        bands = specs[1]["cmd"]
        self.assertIn("/x/report.md", bands)
        self.assertIn("/x/sweep.json", bands)

    def test_bands_gate_goes_red_on_a_report_missing_a_fragile_band(self):
        with tempfile.TemporaryDirectory() as d:
            sweep = os.path.join(d, "sweep.json")
            with open(sweep, "w") as f:
                json.dump({"constants": {"arena.TEAM_WEEK_SHOCK": {"tier": "FRAGILE", "variants": [
                    {"label": "no shock", "shift_mean": 3.4}, {"label": "doubled", "shift_mean": -2.3}]}},
                    "fragile": ["arena.TEAM_WEEK_SHOCK"], "engine_commit": "t"}, f)
            bad = os.path.join(d, "bad.md")
            with open(bad, "w") as f:
                f.write("title share 21.4 percent\n")
            good = os.path.join(d, "good.md")
            with open(good, "w") as f:
                f.write("TEAM_WEEK_SHOCK is FRAGILE: +3.4 / -2.3\n")
            self.assertEqual(G.run_gate(G.redteam_gates(bad, sweep, "/deck")[1])["verdict"], "FAIL")
            self.assertEqual(G.run_gate(G.redteam_gates(good, sweep, "/deck")[1])["verdict"], "PASS")



class BandsOnlyWhereATitleShareIsQuoted(unittest.TestCase):
    """Council verdict 2026-11-12: 89 reports carried the FRAGILE sentence, among them reports that quote no title
    share. The bands check's own rule is "a report that quotes a title share must quote every FRAGILE band"; a report
    that quotes none passes and says so."""
    def setUp(self):
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "redteam"))
        import check_bands
        self.B = check_bands
        self.d = tempfile.mkdtemp()
        self.sweep = os.path.join(self.d, "sweep.json")
        json.dump({"fragile": ["arena.weekly_availability"], "constants": {"arena.weekly_availability": {"variants": [
            {"label": "a", "shift_mean": -4.8}, {"label": "b", "shift_mean": 2.9}]}}}, open(self.sweep, "w"))

    def rep(self, text):
        p = os.path.join(self.d, "r.md"); open(p, "w", encoding="utf-8").write(text); return p

    def test_a_report_with_no_title_share_passes_without_the_band(self):
        ok, problems = self.B.check(self.rep("The header was centred. Shooting 35.8% from three.\n"), self.sweep)
        self.assertTrue(ok, problems); self.assertFalse(self.B.quotes_title_share("Shooting 35.8% from three."))

    def test_a_report_quoting_a_title_share_still_owes_the_band(self):
        for text in ("Title odds are 20.2% this morning.\n", "| Headline title odds | 20.2% |\n", "A 25.1% championship share.\n"):
            ok, problems = self.B.check(self.rep(text), self.sweep)
            self.assertFalse(ok, text); self.assertIn("FRAGILE", " ".join(problems))

    def test_a_report_quoting_one_with_the_band_passes(self):
        ok, problems = self.B.check(self.rep("Title odds 20.2%. weekly_availability is FRAGILE: -4.8 (a) / +2.9 (b).\n"), self.sweep)
        self.assertTrue(ok, problems)


class ReportGatesFollowThePoolLine(unittest.TestCase):
    def test_the_deck_receipt_gates_run_unless_the_report_is_exempt(self):
        names = lambda specs: [s["name"] for s in specs]
        full = names(G.report_gates("/x/r.md", "/deck", exempt=False))
        self.assertEqual(len(full), 3); self.assertIn("deck judgment_open_items --check-report", full)
        self.assertEqual(names(G.report_gates("/x/r.md", "/deck", exempt=True)), ["kit check_report"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
