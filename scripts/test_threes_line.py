#!/usr/bin/env python3
"""Tests for threes_line.py (owner 2026-11-12, card: "Split threes into attempts and %"). Arithmetic by hand."""
import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import threes_line as TL  # noqa: E402


def box(name, tpm, tpa, mn=30, dnp=False, pool="same", game="g1"):
    return dict(name=name, pool_name=(name if pool == "same" else pool), team="DEN", min=mn, dnp=dnp, tpm=tpm, tpa=tpa, game=game)


def day(date, players, season_type=2):
    return dict(date=date, games=[dict(espn_id="g1", season_type=season_type)], players=players)


class Split(unittest.TestCase):
    def test_no_games_returns_the_preseason_threes(self):
        tpm, att, pct = TL.split(2.4, 0.40, 0, 0, 0, att_prior=10.0, pct_prior=750.0)
        self.assertAlmostEqual(att, 6.0); self.assertAlmostEqual(pct, 0.40); self.assertAlmostEqual(tpm, 2.4)

    def test_a_cold_start_on_the_same_volume_barely_moves_the_percentage(self):
        # preseason 2.4 at 40% = 6.0 attempts. Ten games, 60 attempts, 15 made (25%).
        tpm, att, pct = TL.split(2.4, 0.40, 10, 15, 60, att_prior=10.0, pct_prior=750.0)
        self.assertAlmostEqual(att, (10 * 6.0 + 60) / 20)                    # 6.0: the volume held
        self.assertAlmostEqual(pct, (750 * 0.40 + 15) / 810)                 # 0.3889, not 0.25
        self.assertAlmostEqual(tpm, 6.0 * 315 / 810)                         # 2.33 against the count blend's (10 x 2.4 + 15) / 20 = 1.95
        self.assertGreater(tpm, (10 * 2.4 + 15) / 20)

    def test_more_attempts_at_the_old_percentage_lifts_the_line(self):
        # ten games at 9 attempts a game, 36 made (40%): attempts move to 7.5, the percentage stays 40%
        tpm, att, pct = TL.split(2.4, 0.40, 10, 36, 90, att_prior=10.0, pct_prior=750.0)
        self.assertAlmostEqual(att, 7.5); self.assertAlmostEqual(pct, 0.40); self.assertAlmostEqual(tpm, 3.0)

    def test_no_prior_percentage_or_no_preseason_threes_cannot_be_split(self):
        self.assertIsNone(TL.split(2.4, None, 10, 15, 60, 10.0)); self.assertIsNone(TL.split(None, 0.4, 10, 15, 60, 10.0))
        self.assertIsNone(TL.split(0.0, 0.4, 10, 15, 60, 10.0)); self.assertIsNone(TL.split(2.4, 0.0, 10, 15, 60, 10.0))


class Inputs(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(); self.act = os.path.join(self.d, "actuals"); os.makedirs(self.act)
        recs = [day("2026-10-20", [box("Alpha Man", 2, 6), box("Bench Guy", 0, 1, dnp=True), box("Cam Johnson", 1, 4)]),
                day("2026-10-21", [box("Alpha Man", 1, 4), box("Nobody", 3, 3, pool=None)]),
                day("2026-10-10", [box("Alpha Man", 9, 9)], season_type=1)]            # preseason game: not counted
        for r in recs:
            json.dump(r, open(os.path.join(self.act, r["date"] + ".json"), "w"))

    def test_season_threes_counts_regular_season_pooled_players_who_played(self):
        self.assertEqual(TL.season_threes(self.act), {"Alpha Man": (2, 3, 10), "Cam Johnson": (1, 1, 4)})
        self.assertEqual(TL.season_threes(self.act, through="2026-10-20")["Alpha Man"], (1, 2, 6))

    def test_prior_percentage_needs_the_minimum_attempts_and_resolves_spelling(self):
        prior = [dict(player="Alpha Man", games=70, fg3=80, fg3a=200), dict(player="Few Shots", games=70, fg3=30, fg3a=60),
                 dict(player="Luka Dončić", games=70, fg3=210, fg3a=600)]
        got = TL.prior_pct(["Alpha Man", "Few Shots", "Luka Doncic", "Rookie"], prior, aliases={})
        self.assertEqual(sorted(got), ["Alpha Man", "Luka Doncic"]); self.assertAlmostEqual(got["Alpha Man"], 0.40); self.assertAlmostEqual(got["Luka Doncic"], 0.35)


class Build(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.pool = os.path.join(self.d, "pool.csv")
        with open(self.pool, "w") as f:
            f.write("player,team,pos,fg_pct,fga,tpm,pts\nAlpha Man,DEN,PG,0.450,15.0,1.9,20.0\nRookie,SAS,SF,0.400,8.0,1.0,9.0\n")

    def test_only_tpm_changes_and_an_unsplit_row_is_the_live_row(self):
        rec = TL.build(self.pool, {"Alpha Man": 2.4, "Rookie": 1.2}, {"Alpha Man": 0.40}, {"Alpha Man": (10, 15, 60)}, att_prior=10.0, pct_prior=750.0)
        a, r = rec["rows"]
        self.assertEqual(a["tpm"], "2.3"); self.assertEqual({k: v for k, v in a.items() if k != "tpm"}, dict(player="Alpha Man", team="DEN", pos="PG", fg_pct="0.450", fga="15.0", pts="20.0"))
        self.assertEqual(r, dict(player="Rookie", team="SAS", pos="SF", fg_pct="0.400", fga="8.0", tpm="1.0", pts="9.0"))
        self.assertEqual(rec["unsplit"], ["Rookie"]); self.assertEqual(rec["fields"], ["player", "team", "pos", "fg_pct", "fga", "tpm", "pts"])
        self.assertEqual(rec["detail"]["Alpha Man"]["live"], 1.9); self.assertEqual(rec["detail"]["Alpha Man"]["candidate"], 2.33)

    def test_attempts_prior_defaults_to_the_blends_own_threes_prior(self):
        import season_lines as SL
        self.assertEqual(TL.att_prior_games(), float(SL.PRIOR_GAMES["3PM"]))
        self.assertEqual(TL.build(self.pool, {}, {}, {})["method"]["att_prior_games"], float(SL.PRIOR_GAMES["3PM"]))

    def test_cli_writes_both_planes_and_the_record(self):
        act = os.path.join(self.d, "actuals"); os.makedirs(act); out = os.path.join(self.d, "out")
        json.dump(day("2026-10-20", [box("Alpha Man", 2, 6)]), open(os.path.join(act, "2026-10-20.json"), "w"))
        kit = os.path.join(self.d, "kit.csv"); pre = os.path.join(self.d, "pre.csv"); prior = os.path.join(self.d, "prior.csv")
        open(kit, "w").write("name,team,tpm\nAlpha Man,DEN,1.9\n"); open(pre, "w").write("name,team,tpm\nAlpha Man,DEN,2.4\n")
        open(prior, "w").write("player,bref_id,team,games,fg3,fg3a\nAlpha Man,x01,DEN,70,80,200\n")
        r = subprocess.run([sys.executable, os.path.join(HERE, "threes_line.py"), "--date", "2026-10-21", "--actuals", act, "--out-dir", out,
                            "--pool", self.pool, "--kit", kit, "--pre-kit", pre, "--prior", prior], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr); self.assertRegex(r.stdout, r"^THREES LINE: PASS — 2026-10-21: 2 players, 1 split, 1 unsplit")
        rec = json.load(open(os.path.join(out, "threes_line_2026-10-21.json")))
        self.assertEqual(rec["unsplit"], ["Rookie"]); self.assertEqual(rec["method"]["pct_prior_att"], 750.0)
        self.assertEqual([r["tpm"] for r in csv.DictReader(open(os.path.join(out, "projections_season_3s.csv")))], ["2.4"])   # one game, 2 of 6: (9.5 x 6.0 + 6) / 10.5 x (300 + 2) / 756 = 2.40


if __name__ == "__main__":
    unittest.main()
