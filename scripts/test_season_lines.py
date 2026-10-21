#!/usr/bin/env python3
"""Red-first tests for scripts/season_lines.py (in-season tool, Council 2026-10-19 decision 8: a season line
blended from the pinned preseason line and the season's actuals, per-category prior strengths in games).

    python3 scripts/test_season_lines.py
"""
import csv
import io
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import season_lines as S  # noqa: E402

KIT_ROW = dict(name="Test Guard", team="BOS", pos="PG", gp="70", mpg="30.0", fgp="0.450", fga="12.0", ftp="0.800",
               fta="4.0", tpm="2.0", pts="18.0", reb="4.0", ast="5.0", stl="1.0", blk="0.5", tov="2.0")
DECK_ROW = dict(player="Test Guard", team="BOS", pos="PG", fg_pct="0.450", fga="12.0", ft_pct="0.800", fta="4.0",
                tpm="2.0", pts="18.0", reb="4.0", ast="5.0", stl="1.0", blk="0.5", tov="2.0", note="")


def box(name, n, **per_game):
    """n identical regular-season box lines for a player, per-game values given."""
    base = dict(min=30, pts=18, fgm=5, fga=12, tpm=2, tpa=5, ftm=3, fta=4, reb=4, ast=5, tov=2, stl=1, blk=0)
    base.update(per_game)
    return [dict(base, name=name, pool_name=name, team="BOS", dnp=False, game=str(i)) for i in range(n)]


def record(date, players, season_type=2):
    return dict(date=date, players=players, games=[dict(espn_id=str(i), season_type=season_type) for i in range(len({p["game"] for p in players}))])


class Priors(unittest.TestCase):
    def test_prior_games_derive_from_the_measured_stability(self):
        # k = n (1 - rho) / rho at n = 65 games, rho the three-transition mean of after-report-2026-10-09-market.md
        self.assertAlmostEqual(S.prior_games(0.872, 65), 9.5, places=1)   # 3PM
        self.assertAlmostEqual(S.prior_games(0.634, 65), 37.5, places=1)  # FT%
        for c, k in S.PRIOR_GAMES.items():
            self.assertAlmostEqual(k, S.prior_games(S.STABILITY[c], S.SEASON_GAMES), places=1, msg=c)


class Totals(unittest.TestCase):
    def test_regular_season_games_only_and_dnp_excluded(self):
        recs = [record("2026-10-16", box("Test Guard", 2), season_type=1), record("2026-10-21", box("Test Guard", 3))]
        recs[1]["players"].append(dict(box("Test Guard", 1)[0], dnp=True, min=0, game="dnp"))
        t = S.totals(recs)
        self.assertEqual(t["Test Guard"]["games"], 3)

    def test_unpooled_lines_are_kept_under_their_source_name(self):
        rows = box("Nobody Here", 2); rows = [dict(r, pool_name=None) for r in rows]
        t = S.totals([record("2026-10-21", rows)])
        self.assertEqual(t["Nobody Here"]["games"], 2); self.assertTrue(t["Nobody Here"]["unpooled"])


class Blend(unittest.TestCase):
    def test_zero_games_returns_the_preseason_line_exactly(self):
        out = S.blend_kit(dict(KIT_ROW), None)
        self.assertEqual(out, KIT_ROW)

    def test_counting_cat_moves_by_n_over_k_plus_n(self):
        t = S.totals([record("2026-10-21", box("Test Guard", 10, pts=30))])["Test Guard"]
        out = S.blend_kit(dict(KIT_ROW), t)
        k = S.PRIOR_GAMES["PTS"]
        self.assertAlmostEqual(float(out["pts"]), (k * 18.0 + 10 * 30.0) / (k + 10), delta=0.05)  # lines carry one decimal

    def test_percentages_blend_on_attempts(self):
        t = S.totals([record("2026-10-21", box("Test Guard", 10, fgm=3, fga=12))])["Test Guard"]  # .250 on 12 attempts
        out = S.blend_kit(dict(KIT_ROW), t)
        k = S.PRIOR_GAMES["FG%"]
        exp = (k * 12.0 * 0.450 + 10 * 3) / (k * 12.0 + 10 * 12)
        self.assertAlmostEqual(float(out["fgp"]), exp, places=3)

    def test_deck_schema_blends_the_same_way_and_keeps_the_note(self):
        t = S.totals([record("2026-10-21", box("Test Guard", 10, pts=30))])["Test Guard"]
        out = S.blend_deck(dict(DECK_ROW, note="keep me"), t)
        k = S.PRIOR_GAMES["PTS"]
        self.assertAlmostEqual(float(out["pts"]), (k * 18.0 + 10 * 30.0) / (k + 10), delta=0.05)  # lines carry one decimal
        self.assertEqual(out["note"], "keep me")

    def test_three_point_attempts_are_not_a_pool_column_but_tpm_blends(self):
        t = S.totals([record("2026-10-21", box("Test Guard", 10, tpm=4))])["Test Guard"]
        out = S.blend_kit(dict(KIT_ROW), t)
        self.assertGreater(float(out["tpm"]), 2.0)


class Run(unittest.TestCase):
    def test_identity_run_writes_byte_equal_lines_and_zero_movers(self):
        with tempfile.TemporaryDirectory() as d:
            kit = os.path.join(d, "kit.csv"); deck = os.path.join(d, "deck.csv")
            with open(kit, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(KIT_ROW)); w.writeheader(); w.writerow(KIT_ROW)
            with open(deck, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(DECK_ROW)); w.writeheader(); w.writerow(DECK_ROW)
            rec = S.run(date="2026-10-20", actuals=[], kit_csv=kit, deck_csv=deck, out_dir=d)
            self.assertEqual(rec["players_with_games"], 0); self.assertEqual(rec["movers"], [])
            self.assertEqual(open(os.path.join(d, "projections_season.csv")).read().replace("\r", ""),
                             open(kit).read().replace("\r", ""))
            self.assertEqual(open(os.path.join(d, "pool_season.csv")).read().replace("\r", ""),
                             open(deck).read().replace("\r", ""))

    def test_additions_join_the_deck_plane_after_the_snapshot_rows(self):
        # owner 2026-10-21 option (b): the frozen Version 69 snapshot stays untouched; in-season pickups follow it
        with tempfile.TemporaryDirectory() as d:
            kit = os.path.join(d, "kit.csv"); deck = os.path.join(d, "deck.csv"); adds = os.path.join(d, "adds.csv")
            with open(kit, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(KIT_ROW)); w.writeheader(); w.writerow(KIT_ROW)
            for path, name in ((deck, DECK_ROW["player"]), (adds, "Pickup Center")):
                with open(path, "w", newline="") as f:
                    w = csv.DictWriter(f, fieldnames=list(DECK_ROW)); w.writeheader(); w.writerow(dict(DECK_ROW, player=name))
            S.run(date="2026-10-20", actuals=[], kit_csv=kit, deck_csv=deck, out_dir=d, additions_csv=adds)
            names = [r["player"] for r in csv.DictReader(open(os.path.join(d, "pool_season.csv")))]
            self.assertEqual(names, [DECK_ROW["player"], "Pickup Center"])

    def test_an_addition_already_in_the_snapshot_is_refused(self):
        # written after the code (green from the start, stated): a pickup the snapshot already carries would be two lines
        with tempfile.TemporaryDirectory() as d:
            kit = os.path.join(d, "kit.csv"); deck = os.path.join(d, "deck.csv"); adds = os.path.join(d, "adds.csv")
            with open(kit, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(KIT_ROW)); w.writeheader(); w.writerow(KIT_ROW)
            for path in (deck, adds):
                with open(path, "w", newline="") as f:
                    w = csv.DictWriter(f, fieldnames=list(DECK_ROW)); w.writeheader(); w.writerow(DECK_ROW)
            with self.assertRaisesRegex(ValueError, DECK_ROW["player"]):
                S.run(date="2026-10-20", actuals=[], kit_csv=kit, deck_csv=deck, out_dir=d, additions_csv=adds)
            self.assertFalse(os.path.exists(os.path.join(d, "pool_season.csv")))

    def test_the_command_line_run_reads_the_kits_additions_file(self):
        # end to end on the real inputs, written to a scratch folder: Drummond's pickup row reaches pool_season.csv
        import subprocess
        with tempfile.TemporaryDirectory() as d:
            p = subprocess.run([sys.executable, os.path.join(HERE, "season_lines.py"), "--date", "2026-10-21", "--out", d],
                               capture_output=True, text=True)
            self.assertIn("SEASON LINES: PASS", p.stdout, p.stdout + p.stderr)
            names = [r["player"] for r in csv.DictReader(open(os.path.join(d, "pool_season.csv"), encoding="utf-8"))]
            self.assertIn("Andre Drummond", names)


if __name__ == "__main__":
    unittest.main(verbosity=2)
