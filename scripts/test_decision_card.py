#!/usr/bin/env python3
"""Red-first tests for scripts/decision_card.py (owner 2026-11-10, pick "Decision card + watchdog"; council 4-1):
the brief's top pickup pairs scored in two worlds (IL players never return, the brief's own; IL players return on
ESPN's dates), the top pair re-scored under the declared availability band, and each pair's effect on this week
beside its effect on the season. Display only: the brief's figures and its ranking are never changed.

    python3 scripts/test_decision_card.py
"""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import decision_card as DC  # noqa: E402

BY = {n: {"player": n, "adj": v} for n, v in (("Star", 9.0), ("Dunn", 2.0), ("Cam", 1.0), ("Hurt", 8.0), ("Collins", 3.0),
                                              ("Other", 1.5), ("Rival", 5.0))}
STATE = {"as_of": "2026-11-10", "teams": [
    {"seat": 10, "name": "MINE", "players": [{"player": "Star", "slot": "PG"}, {"player": "Dunn", "slot": "G"},
                                             {"player": "Cam", "slot": "F"}, {"player": "Hurt", "slot": "IL"}]},
    {"seat": 3, "name": "THEM", "players": [{"player": "Rival", "slot": "PG"}]}]}
BRIEF = {"date": "2026-11-10", "seasons": 100, "title": {"2026": 12.0, "2027": 12.0},
         "waiver_top": [{"add": "Collins", "drop": "Dunn", "title": 15.0, "d_title": 3.0, "d_ecw": 0.12},
                        {"add": "Collins", "drop": "Cam", "title": 13.5, "d_title": 1.5, "d_ecw": 0.05}]}
ILR = {"date": "2026-11-10", "weeks": 17, "seasons": 100, "espn_date": "2026-11-10",
       "il_players": [{"seat": 10, "team": "MINE", "player": "Hurt", "espn": "Hurt", "status": "Out", "return_date": "2026-11-13", "week": 4}]}
WEEK = {"date": "2026-11-10", "p_5plus": 0.82, "exp_cats": 5.6,
        "pair_checks": [{"add": "Collins", "drop": "Dunn", "d_exp": -0.05, "p_5plus": 0.81, "d_p_5plus": -0.01, "games": 3},
                        {"add": "Collins", "drop": "Cam", "d_exp": 0.13, "p_5plus": 0.85, "d_p_5plus": 0.03, "games": 3}]}
VARIANTS = [("harsh", {"k": 1}), ("mild", {"k": 2})]


def fake_sim(calls):
    """Title = a fixed table of the seat-10 names. With windows (the return world) Dunn is worth more than Cam; without,
    the reverse. A patch shifts every figure, so differences hold."""
    def sim(ros, seed, seasons, work, tag="cur", windows=None, patch=None):
        names = sorted(p["player"] for p in ros[10])
        calls.append(dict(names=names, seed=seed, windows=windows, patch=patch, tag=tag))
        v = {"Star": 6.0, "Dunn": 3.0 if windows else 1.0, "Cam": 1.0 if windows else 2.5, "Collins": 4.0, "Hurt": 5.0 if windows else 0.0}
        t = sum(v.get(n, 0.0) for n in names) + (patch or {}).get("k", 0) + (0.1 if seed == 2027 else 0.0)
        return {"teams": {"10": {"champ": t, "playoff": 90.0}}, "absent_from_sim": []}
    return sim


class Build(unittest.TestCase):
    def card(self, **kw):
        self.calls = []
        a = dict(brief=BRIEF, ilr=ILR, week=WEEK, state=STATE, by=BY, variants=VARIANTS, seasons=100,
                 sim=fake_sim(self.calls), work=tempfile.mkdtemp(), value=lambda p: p["adj"])
        a.update(kw)
        return DC.build(**a)

    def test_each_pair_carries_both_worlds_and_the_week(self):
        c = self.card()
        p = {x["drop"]: x for x in c["pairs"]}
        self.assertEqual([x["add"] for x in c["pairs"]], ["Collins", "Collins"])
        self.assertEqual(p["Dunn"]["never"]["d_title"], 3.0)            # the brief's own figure, not re-simulated
        self.assertEqual(p["Cam"]["never"]["d_title"], 1.5)
        self.assertAlmostEqual(p["Dunn"]["on_time"]["d_title"], 1.0, places=6)   # +Collins 4 -Dunn 3 in the return world
        self.assertAlmostEqual(p["Cam"]["on_time"]["d_title"], 3.0, places=6)    # +Collins 4 -Cam 1
        self.assertEqual(p["Cam"]["week"], {"d_exp": 0.13, "p_5plus": 0.85, "d_p_5plus": 0.03})
        self.assertAlmostEqual(c["base"]["never"], 12.0); self.assertAlmostEqual(c["base"]["on_time"], 15.05, places=6)

    def test_a_ranking_that_differs_between_the_worlds_is_flagged(self):
        c = self.card()
        self.assertEqual(c["order"]["never"], [["Collins", "Dunn"], ["Collins", "Cam"]])
        self.assertEqual(c["order"]["on_time"], [["Collins", "Cam"], ["Collins", "Dunn"]])
        self.assertIs(c["rank_flip"], True)
        same = dict(BRIEF, waiver_top=BRIEF["waiver_top"][1:])
        self.assertIs(self.card(brief=same)["rank_flip"], False)

    def test_the_return_world_uses_the_il_players_windows_and_the_room_rule(self):
        self.card()
        w = [c for c in self.calls if c["windows"]]
        self.assertTrue(w)
        for c in w:
            self.assertIn("Hurt", c["names"])                          # the IL player is on the roster handed over
            self.assertEqual(c["windows"][10]["Hurt"], (4, 17))        # from his ESPN week to the season's end
            self.assertEqual(len([n for n, (a, b) in c["windows"][10].items() if a == 1]), 1)   # one player leaves for him

    def test_the_top_pair_is_rescored_under_each_band_variant(self):
        c = self.card()
        r = c["robust"]
        self.assertEqual((r["add"], r["drop"]), ("Collins", "Dunn"))
        self.assertEqual([v["label"] for v in r["variants"]], ["harsh", "mild"])
        for v in r["variants"]:
            self.assertAlmostEqual(v["d_title"], 3.0, places=6)        # +Collins 4 -Dunn 1 in the never world, shift cancels
        self.assertIs(r["holds"], True); self.assertEqual(r["held"], 2)
        patched = [c for c in self.calls if c["patch"]]
        self.assertEqual(len(patched), 2 * 2 * 2)                       # 2 variants x (base, pair) x 2 seeds
        self.assertTrue(all(not c["windows"] for c in patched))

    def test_a_sign_change_under_a_variant_does_not_hold(self):
        calls = []
        base = fake_sim(calls)
        def sim(ros, seed, seasons, work, tag="cur", windows=None, patch=None):
            r = base(ros, seed, seasons, work, tag, windows, patch)
            if patch and patch.get("k") == 2 and "Collins" in [p["player"] for p in ros[10]]:
                r["teams"]["10"]["champ"] -= 10
            return r
        c = self.card(sim=sim)
        self.assertIs(c["robust"]["holds"], False); self.assertEqual(c["robust"]["held"], 1)

    def test_missing_inputs_leave_their_part_out_and_say_why(self):
        c = self.card(ilr=None)
        self.assertIsNone(c["pairs"][0]["on_time"]); self.assertIsNone(c["rank_flip"])
        self.assertTrue(any("il_return" in n for n in c["notes"]))
        c = self.card(week=dict(WEEK, pair_checks=None))
        self.assertIsNone(c["pairs"][0]["week"]); self.assertTrue(any("week card" in n for n in c["notes"]))
        c = self.card(variants=[])
        self.assertIsNone(c["robust"])
        skipped = dict(WEEK, pair_checks=[dict(add="Collins", drop="Dunn", skipped="add not in today's free-agent pool"), WEEK["pair_checks"][1]])
        c = self.card(week=skipped)
        self.assertIsNone(c["pairs"][0]["week"]); self.assertIsNotNone(c["pairs"][1]["week"])
        self.assertIn("Collins for Dunn: this week is not shown (add not in today's free-agent pool)", c["notes"])

    def test_a_hold_day_writes_an_empty_card(self):
        c = self.card(brief=dict(BRIEF, waiver_top=[]))
        self.assertEqual(c["pairs"], []); self.assertIsNone(c["robust"]); self.assertEqual(self.calls, [])

    def test_the_brief_is_never_changed(self):
        before = json.dumps(BRIEF, sort_keys=True)
        self.card()
        self.assertEqual(json.dumps(BRIEF, sort_keys=True), before)


class Render(unittest.TestCase):
    def test_the_lines_say_both_worlds_the_flip_and_the_band(self):
        calls = []
        c = DC.build(brief=BRIEF, ilr=ILR, week=WEEK, state=STATE, by=BY, variants=VARIANTS, seasons=100,
                     sim=fake_sim(calls), work=tempfile.mkdtemp(), value=lambda p: p["adj"])
        text = "\n".join(DC.render(c))
        for s in ("Collins", "never return", "return on time", "+3.0", "+1.0", "this week", "The order changes",
                  "holds in 2 of 2", "Display only"):
            self.assertIn(s, text)
        line = DC.pass_line(c, "x.json")
        self.assertTrue(line.startswith("DECISION CARD: PASS — 2026-11-10: 2 pair(s)"))
        self.assertIn("order changes between the worlds", line); self.assertIn("top pair holds in 2 of 2", line)


if __name__ == "__main__":
    unittest.main(verbosity=2)
