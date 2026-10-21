#!/usr/bin/env python3
"""Red-first tests for trade_finder.py (owner 2026-10-20: "1, 2, 5 build"): the 1-for-1 trade
sweep on live rosters — both sides re-modeled, only mutually non-losing trades surface."""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("SEASON_POOL", os.path.join(os.path.dirname(HERE), "data", "season", "pool_season.csv"))
import co_gm as CG  # noqa: E402
import trade_finder as TF  # noqa: E402


class Sweep(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import json
        state = json.load(open(os.path.join(os.path.dirname(HERE), "data", "league_state.json"), encoding="utf-8"))
        P, by = CG.load_pool()
        cls.ros = CG.rosters(state, by)
        cls.trades, cls.n_swept = TF.sweep(cls.ros, return_count=True)

    def test_every_trade_helps_me_and_does_not_hurt_them(self):
        for t in self.trades:
            self.assertGreater(t["d_ecw_me"], 0, t)
            self.assertGreaterEqual(t["d_ecw_them"], 0, t)

    def test_deltas_are_post_trade_league_vs_pre_trade_league(self):
        """Hand-check one surfaced trade: rebuilding both rosters and re-scoring reproduces the deltas."""
        if not self.trades:
            self.skipTest("no proposable trades on this state (legal outcome)")
        t = self.trades[0]
        me, them = TF.apply_trade(self.ros, t)
        d_me, d_them = TF.deltas(self.ros, t["seat"], me, them)
        # stored deltas are rounded to 4 dp
        self.assertAlmostEqual(d_me, t["d_ecw_me"], places=3)
        self.assertAlmostEqual(d_them, t["d_ecw_them"], places=3)

    def test_a_self_trade_is_never_swept(self):
        self.assertTrue(all(t["seat"] != CG.OWNER_SEAT for t in self.trades))

    def test_sweep_covers_every_rival_pairing(self):
        n_expected = sum(len(self.ros[CG.OWNER_SEAT]) * len(r) for s, r in self.ros.items() if s != CG.OWNER_SEAT)
        self.assertEqual(self.n_swept, n_expected)


if __name__ == "__main__":
    unittest.main()
