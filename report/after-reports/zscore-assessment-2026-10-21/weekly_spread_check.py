#!/usr/bin/env python3
"""Measurement 2 of the z-score assessment (owner 2026-10-21: "Measure first"; adjustment chosen: fit the weekly
variance). Before any fit: is the deck model's hand-set per-game variance (arena.CV) in the right range for the weekly
spread this league actually showed? Data: the owner's 2025-26 regular-season weekly team totals (deck
arena/data/weekly_matchups_2025-26.csv), weeks 1-18 except week 17 (two calendar weeks). Per counting category, the
per-game rate r_w = total_w / gp_w; observed spread = coefficient of variation of r_w across the weeks. Model side:
a team's weekly per-game rate has CV = CV_pg * sqrt(D / gp) with D >= 1 the players' spread factor; D = 1 (equal
players) gives the LOWER bound printed here. Caveats: gp is unverified for most rows (README); the owner's roster
changed during the season, and the week's schedule mix varies which players' games make up the week (the model gives every
player 3.5 games); both add spread the model does not attribute to per-game noise. A range test, not a fit."""
import csv, math, os, statistics, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "..", "yahoo-fantasy-basketball")
sys.path.insert(0, os.path.join(DECK, "arena")); sys.path.insert(0, os.path.join(DECK, "scripts"))
import arena  # noqa: E402
rows = [r for r in csv.DictReader(open(os.path.join(DECK, "arena", "data", "weekly_matchups_2025-26.csv")))
        if r["manager"] == "David" and int(r["week"]) <= 18 and int(r["week"]) != 17]
cols = {"PTS": "pts", "REB": "reb", "AST": "ast", "3PTM": "tpm", "ST": "stl", "BLK": "blk", "TO": "tov"}
gp = [int(r["gp"]) for r in rows]
mgp = statistics.mean(gp)
print(f"weeks {len(rows)}, games played per week mean {mgp:.1f} (min {min(gp)}, max {max(gp)})")
print(f"{'cat':<5} {'hand-set CV_pg':>14} {'model rate CV (D=1)':>20} {'observed rate CV':>17} {'ratio obs/model':>16} {'implied CV_pg (D=1)':>20}")
out = {}
for c, col in cols.items():
    rate = [int(r[col]) / int(r["gp"]) for r in rows]
    obs = statistics.stdev(rate) / statistics.mean(rate)
    model = arena.CV[c] / math.sqrt(mgp)
    out[c] = dict(cv_hand=arena.CV[c], model_rate_cv=round(model, 4), observed_rate_cv=round(obs, 4),
                  ratio=round(obs / model, 2), implied_cv_pg_upper=round(obs * math.sqrt(mgp), 3))
    print(f"{c:<5} {arena.CV[c]:>14.2f} {model:>20.3f} {obs:>17.3f} {obs/model:>16.2f} {obs*math.sqrt(mgp):>20.3f}")
import json
json.dump(dict(weeks=[int(r["week"]) for r in rows], gp_mean=round(mgp, 2), categories=out,
               note=("observed spread includes per-game noise, unequal players (D), the week's schedule mix (which players' games make up "
                     "the week; the model gives every player 3.5 games), roster changes and gp transcription error; D=1 is a lower "
                     "bound on the model side, so implied_cv_pg is an UPPER bound on per-game CV and the observed/model ratio is not "
                     "attributable to arena.CV alone")),
          open(os.path.join(HERE, "weekly_spread_check.json"), "w"), indent=1)
