#!/usr/bin/env python3
"""Red-first tests for rank_engine's exclusion rule (D-1009-1, owner yes 2026-10-09).

The board prices only the rows the pool can draft: an unsigned free agent (team FA,
D-CAST-1) and any row at the exclusion class (GP <= EXCLUSION_GP, the deck's
out-*/recovery twin — the audit of 2026-10-09 found Butler #68, Lively #107, Mark
Williams #121, Shaedon Sharpe #136, Nurkic #172 and DiVincenzo #176 still priced
at their per-game value) are held off the board and out of the z-score pool.

    python3 report/test_rank_engine.py
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rank_engine as RE  # noqa: E402


def row(name, team="DAL", gp=70.0):
    r = {"name": name, "team": team, "pos": "C", "gp": gp, "mpg": 30.0, "fgp": 0.5, "fga": 10.0,
         "ftp": 0.8, "fta": 4.0, "tpm": 1.0, "pts": 15.0, "reb": 6.0, "ast": 3.0, "stl": 1.0,
         "blk": 0.8, "tov": 2.0}
    return r


class ExclusionRule(unittest.TestCase):
    def names(self, rows):
        return sorted(r["name"] for r in rows)

    def test_unsigned_free_agent_is_held(self):
        kept, held = RE.exclude_held([row("A", team="FA"), row("B")])
        self.assertEqual(self.names(held), ["A"])
        self.assertEqual(self.names(kept), ["B"])

    def test_exclusion_class_gp_is_held(self):
        kept, held = RE.exclude_held([row("A", gp=25.0), row("B", gp=15.0), row("C")])
        self.assertEqual(self.names(held), ["A", "B"])
        self.assertEqual(self.names(kept), ["C"])

    def test_one_game_above_the_class_stays(self):
        kept, held = RE.exclude_held([row("A", gp=26.0), row("B")])
        self.assertEqual(held, [])
        self.assertEqual(self.names(kept), ["A", "B"])

    def test_held_rows_leave_the_pool_and_the_board(self):
        # the z-score pool is built from kept only: a held row must not shift anyone's z
        pool = [row(f"P{i}", gp=70.0 - i) for i in range(10)]
        kept, held = RE.exclude_held(pool + [row("X", gp=10.0, team="FA"), row("Y", gp=20.0)])
        self.assertEqual(self.names(held), ["X", "Y"])
        z = RE.zscores(kept, kept)
        self.assertNotIn("X", z)
        self.assertNotIn("Y", z)
        self.assertEqual(len(z), 10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
