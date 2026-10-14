"""Independent arithmetic for the Undo / Insert-at-# check: for every final state the page reached
(undo_insert_check.mjs writes <out>_totals.json), recompute each team's nine category z-totals in
Python from the deck's own data (scripts/hoops.py: load_players + zscores + roster_totals, the
engine check_parity already holds equal to the page) and the owner's category ranks, and compare
with what the page computed. Team association is taken from the page's picks (player, seat); a
separate assertion holds every seat to the snake formula, so a wrong seat shows up twice.
  python3 totals_oracle.py <out>_totals.json [players.csv]"""
import json, sys
sys.path.insert(0, "/home/user/yahoo-fantasy-basketball/scripts")
import hoops
dumps = json.load(open(sys.argv[1]))
if len(sys.argv) > 2: hoops.DATA_PATH = sys.argv[2]
P = {p["player"]: p for p in hoops.zscores(hoops.load_players())}
TEAMS, SLOT = 12, 10
# the page bakes each player z to 6 decimals: a 13-man total can drift 13 x 5e-7 = 6.5e-6 from full precision
TOL = 13 * 5e-7
snake = lambda n, t: (n % t) + 1 if (n // t) % 2 == 0 else t - (n % t)
worst, bad, cells, rank_bad = 0.0, [], 0, []
for d in dumps:
    rosters = {s: [] for s in range(1, TEAMS + 1)}
    for i, (name, seat) in enumerate(d["picks"]):
        if name in P: rosters[seat].append(P[name])
    tot = {s: hoops.roster_totals(r) for s, r in rosters.items()}
    for s in range(1, TEAMS + 1):
        for c in hoops.CATS:
            got = d["totals"][str(s)][c]; want = tot[s][c]; cells += 1
            err = abs(got - want); worst = max(worst, err)
            if err > TOL: bad.append((d["id"], s, c, got, round(want, 9)))
    ranks = {c: 1 + sum(1 for s in range(1, TEAMS + 1) if s != SLOT and tot[s][c] > tot[SLOT][c]) for c in hoops.CATS}
    if ranks != d["ranks"]: bad.append((d["id"], "ranks", d["ranks"], ranks)); rank_bad.append(d["id"])
out = {"states": len(dumps), "team_category_cells": cells, "max_abs_error": worst, "mismatches": bad[:20], "n_mismatches": len(bad), "tolerance": TOL, "rank_mismatch_states": rank_bad}
print(json.dumps(out))
sys.exit(1 if bad else 0)
