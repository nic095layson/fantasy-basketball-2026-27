#!/usr/bin/env python3
"""Red-first tests for scripts/season_board.py: the in-season board built from data/season/projections_season.csv
with the kit rank engine's own functions, never by editing the preseason board.

    python3 scripts/test_season_board.py
"""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import season_board as SB  # noqa: E402
import season_lines as SL  # noqa: E402
import rank_engine as RE  # noqa: E402  (season_board put report/ on the path)

KIT = os.path.dirname(HERE)
PRE = os.path.join(KIT, "report", "projections-2026-27.csv")


class Board(unittest.TestCase):
    def test_identity_board_matches_the_preseason_order(self):
        # zero regular-season games -> season lines equal the preseason lines -> the same board. Built here from a
        # zero-game season_lines run, not read from data/season/: from the first real games (10/20) the committed
        # season lines move by design, and a test that read them failed on every in-season record (owner 2026-10-21).
        b_pre = SB.build(PRE)
        with tempfile.TemporaryDirectory() as d:
            rec = SL.run(date="2026-10-19", actuals=[], kit_csv=PRE, out_dir=d)
            self.assertEqual(rec["players_with_games"], 0)
            b_season = SB.build(os.path.join(d, "projections_season.csv"))
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


# The G-score comparison column (D-ZS-2, owner 2026-10-21 "Build it": the paper's Table 5 beside z, no ranking change).
PIN = dict(kappa=26 / 25, games_per_week=3.5,
           tau=dict(pts=7.0, reb=3.5, ast=2.8, tpm=1.4, stl=1.05, blk=0.7, tov=1.75), tau_r=dict(fgp=0.05, ftp=0.05))
TOY = [dict(name="A", pts=10, reb=4, ast=2, tpm=1, stl=0.5, blk=0.2, tov=1, fga=10, fgp=0.40, fta=2, ftp=0.70),
       dict(name="B", pts=20, reb=6, ast=4, tpm=2, stl=1.0, blk=0.5, tov=2, fga=20, fgp=0.50, fta=4, ftp=0.80),
       dict(name="C", pts=30, reb=8, ast=6, tpm=3, stl=1.5, blk=0.8, tov=3, fga=10, fgp=0.60, fta=6, ftp=0.90)]


def pin_file(d, pin=PIN):
    p = os.path.join(d, "gscore_tau.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(pin, f)
    return p


class GScore(unittest.TestCase):
    def test_known_answer_on_a_hand_built_pool(self):
        # Table 5 by hand (population SDs over the three, kappa 26/25, tau on the per-game scale = tau / 3.5):
        # PTS sigma^2 200/3, (7/3.5)^2 = 4 -> C = 10 / sqrt(66.667 + 4.16) = 1.18823
        # FG% mu_A 40/3, mu_R 20/40 = .5, sigma_R^2 .02/3, tau_R .05 -> C = (10/13.333)(.1) / sqrt(.0066667 + .0026) = .77911
        # TOV sigma^2 2/3, (1.75/3.5)^2 = .25 -> A (fewest) = 1 / sqrt(.66667 + .26) = 1.03882; B on every mean = 0
        g = SB.gscores(TOY, TOY, PIN)
        self.assertAlmostEqual(g["C"]["pts"], 1.18823, places=5)
        self.assertAlmostEqual(g["A"]["pts"], -1.18823, places=5)
        self.assertAlmostEqual(g["C"]["fgp"], 0.77911, places=5)
        self.assertAlmostEqual(g["B"]["fgp"], 0.0, places=9)
        self.assertAlmostEqual(g["A"]["tov"], 1.03882, places=5)
        self.assertEqual(set(g["A"]), {"fgp", "ftp", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"})

    def test_counting_g_at_zero_tau_is_the_board_z(self):
        # Table 5's G with no week-to-week variance is the Z the board already uses, for every counting category
        zero = dict(PIN, tau={k: 0.0 for k in PIN["tau"]}, tau_r={k: 0.0 for k in PIN["tau_r"]})
        rows, _ = RE.exclude_held(RE.load(PRE))
        pool = rows[:RE.POOL_SIZE]
        z, g = RE.zscores(rows, pool), SB.gscores(rows, pool, zero)
        for r in rows:
            for cat in RE.COUNTING + ["tov"]:
                self.assertAlmostEqual(g[r["name"]][cat], z[r["name"]][cat], places=9, msg=(r["name"], cat))

    def test_week_to_week_variance_only_shrinks_a_category(self):
        g0 = SB.gscores(TOY, TOY, dict(PIN, tau={k: 0.0 for k in PIN["tau"]}, tau_r={k: 0.0 for k in PIN["tau_r"]}))
        g = SB.gscores(TOY, TOY, PIN)
        for cat in g["C"]:
            self.assertLessEqual(abs(g["C"][cat]), abs(g0["C"][cat]) + 1e-12, cat)

    def test_g_column_never_moves_the_board(self):
        with tempfile.TemporaryDirectory() as d:
            with_g = SB.build(PRE, gscore_path=pin_file(d))
        without = SB.build(PRE, gscore_path=os.path.join("no", "such", "file.json"))
        self.assertEqual([r["name"] for r in with_g["board"]], [r["name"] for r in without["board"]])
        self.assertEqual([r["z_adj"] for r in with_g["board"]], [r["z_adj"] for r in without["board"]])

    def test_g_adj_takes_the_same_availability_as_z(self):
        with tempfile.TemporaryDirectory() as d:
            b = SB.build(PRE, gscore_path=pin_file(d))
        for r in b["board"]:
            want = r["g_total"] * RE.avail(r["gp"]) if r["g_total"] > 0 else r["g_total"]
            self.assertAlmostEqual(r["g_adj"], want, places=12, msg=r["name"])
        ranks = sorted(r["g_rank"] for r in b["board"])
        self.assertEqual(ranks, list(range(1, len(b["board"]) + 1)))

    def test_no_pin_file_no_column(self):
        b = SB.build(PRE, gscore_path=os.path.join("no", "such", "file.json"))
        self.assertIsNone(b["gscore"])
        self.assertFalse(any("g_adj" in r for r in b["board"]))
        md = SB.render(b, "2026-10-21", "data/season/projections_season.csv", movers=[])
        self.assertNotIn("G (adj)", md)
        with tempfile.TemporaryDirectory() as d:
            _, js = SB.write(PRE, "2026-10-21", d, movers=[], gscore_path=os.path.join(d, "absent.json"))
            with open(js, encoding="utf-8") as f:
                rec = json.load(f)
        self.assertNotIn("gscore", rec)
        self.assertFalse(any("g_adj" in r for r in rec["board"]))

    def test_pinned_board_shows_g_beside_z(self):
        with tempfile.TemporaryDirectory() as d:
            p = pin_file(d)
            b = SB.build(PRE, gscore_path=p)
            md = SB.render(b, "2026-10-21", "data/season/projections_season.csv", movers=[])
            _, js = SB.write(PRE, "2026-10-21", d, movers=[], gscore_path=p)
            with open(js, encoding="utf-8") as f:
                rec = json.load(f)
        self.assertIn("| G (adj) | G # |", md)
        self.assertIn("2307.02188", md)
        self.assertIn("ranked by z", md)
        self.assertEqual(rec["gscore"]["kappa"], PIN["kappa"])
        top = rec["board"][0]
        self.assertTrue({"g_adj", "g_total", "g_rank", "g"} <= set(top))

    def test_a_pin_missing_a_category_is_refused(self):
        bad = dict(PIN, tau={k: v for k, v in PIN["tau"].items() if k != "stl"})
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                SB.build(PRE, gscore_path=pin_file(d, bad))


if __name__ == "__main__":
    unittest.main(verbosity=2)
