#!/usr/bin/env python3
"""Red-first tests for scripts/season_board.py: the in-season board built from data/season/projections_season.csv
with the kit rank engine's own functions, never by editing the preseason board.

    python3 scripts/test_season_board.py
"""
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import season_board as SB  # noqa: E402

KIT = os.path.dirname(HERE)
PRE = os.path.join(KIT, "report", "projections-2026-27.csv")


class Board(unittest.TestCase):
    def test_identity_board_matches_the_preseason_order(self):
        b_pre = SB.build(PRE)
        b_season = SB.build(os.path.join(KIT, "data", "season", "projections_season.csv"))
        self.assertEqual([r["name"] for r in b_pre["board"]][:200], [r["name"] for r in b_season["board"]][:200])
        self.assertEqual(b_pre["n_held"], b_season["n_held"])

    def test_render_names_its_inputs_and_date(self):
        b = SB.build(PRE)
        md = SB.render(b, "2026-10-19", "data/season/projections_season.csv", movers=[])
        self.assertIn("2026-10-19", md); self.assertIn("projections_season.csv", md); self.assertIn("| 1 |", md)

    def test_write_produces_md_and_json(self):
        with tempfile.TemporaryDirectory() as d:
            paths = SB.write(PRE, "2026-10-19", d, movers=[])
            self.assertTrue(all(os.path.exists(p) for p in paths))


if __name__ == "__main__":
    unittest.main(verbosity=2)
