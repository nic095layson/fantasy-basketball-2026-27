#!/usr/bin/env python3
"""Red-first tests: the season tools run on the deck's arena.SEASON_CV (D-ZS-3, owner 2026-10-21: "Adopt the fitted
values", then "Season tools only"). The waiver swap values, the weekly preview, the title-odds simulator and the
standing sweep pass the per-game variation fitted to the 2025-26 game logs; the draft engine's arena.CV stays
frozen with the draft page. Needs the deck at the commit that adds SEASON_CV (deck PR, merged with this one).

    python3 scripts/test_season_cv.py
"""
import json
import os
import random
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "redteam"))
import co_gm as CG  # noqa: E402
import weekly_preview as WP  # noqa: E402
import sweep as S  # noqa: E402

arena = CG.arena
REG = os.path.join(HERE, "redteam", "constants_registry.json")


class Spy:
    """Wraps arena.team_week_model and records the cv each call used."""
    def __init__(self):
        self.orig, self.cvs = arena.team_week_model, []

    def __enter__(self):
        def wrapped(roster, cv=None):
            self.cvs.append(cv)
            return self.orig(roster, cv)
        arena.team_week_model = wrapped
        return self

    def __exit__(self, *a):
        arena.team_week_model = self.orig


class SeasonTools(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.P, cls.by = CG.load_pool()
        cls.state = json.load(open(CG.STATE, encoding="utf-8"))
        cls.ros = CG.rosters(cls.state, cls.by)

    def test_waiver_swaps_use_the_season_cv(self):
        fa = CG.free_agents(self.P, self.state, CG.fa_status(self.P, [], []))[0][:2]   # status gate, nothing flagged
        with Spy() as s:
            CG.waiver_pairs(self.ros, fa)
        self.assertTrue(s.cvs)
        self.assertTrue(all(c is arena.SEASON_CV for c in s.cvs), set(map(id, s.cvs)))

    def test_the_weekly_preview_uses_the_season_cv(self):
        with Spy() as s:
            WP.preview(1, n=50)
        self.assertTrue(s.cvs)
        self.assertTrue(all(c is arena.SEASON_CV for c in s.cvs))

    def test_the_title_odds_simulator_runs_on_the_season_cv(self):
        with tempfile.TemporaryDirectory() as d:
            rec = CG.run_league_sim(self.ros, 2026, 40, d)
        self.assertEqual(rec.get("cv"), "season")

    def test_the_standing_sweep_runs_on_the_season_cv(self):
        self.assertIn("_scv", S.REFERENCE)
        label, seed, title, _ = S._job(("baseline", {}, 2026, 300, CG.DECK))
        ros = {s: [] for s in range(1, arena.TEAMS + 1)}
        import hoops
        hoops.DATA_PATH = os.path.join(CG.DECK, S.POOL)
        by = {p["player"]: p for p in hoops.zscores(hoops.load_players())}
        for pk in json.load(open(os.path.join(CG.DECK, S.STATE), encoding="utf-8"))["picks"]:
            ros[pk["slot"]].append(by[pk["player"]])
        champ, _ = arena.simulate_seasons(ros, 300, random.Random(2026), cv=arena.SEASON_CV)
        self.assertAlmostEqual(title, 100 * champ[S.OWNER_SEAT] / 300, places=9)

    def test_the_registry_holds_the_fit_and_freezes_the_draft_cv(self):
        reg = {(e["module"], e["name"]): e for e in json.load(open(REG, encoding="utf-8"))["constants"]}
        scv = reg[("arena", "SEASON_CV")]
        self.assertEqual(scv["status"], "measured")
        self.assertEqual(scv["value"], arena.SEASON_CV)
        self.assertIn("gscore_weights_2025-26.json", scv["record"])
        cv = reg[("arena", "CV")]
        self.assertEqual(cv["status"], "uncalibrated")
        self.assertNotIn("band", cv)


if __name__ == "__main__":
    unittest.main(verbosity=2)
