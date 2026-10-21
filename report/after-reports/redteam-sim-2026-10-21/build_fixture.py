#!/usr/bin/env python3
"""Inputs for attack A-9 (separate-attacker re-implementation of the season simulator, 2026-10-21).

Writes fixture.json: the 12 real league rosters as the in-season simulator sees them (league_state.json of
2026-10-20, IL slots excluded per D-IS-8, the 10/21 season pool's lines), each player's stat line, positions,
note, and z-sum from the board engine (already independently verified, attack A-1 / the 1,800-cell audit); plus
every distinct note in the pool for the availability check and a fixed set of hash vectors. The attacker gets this
file and SPEC.md only.

    SEASON_POOL=data/season/pool_season.csv python3 report/after-reports/redteam-sim-2026-10-21/build_fixture.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(KIT, "scripts"))
os.environ.setdefault("SEASON_POOL", os.path.join(KIT, "data", "season", "pool_season.csv"))
import co_gm as CG  # noqa: E402

COLS = ("fg_pct", "fga", "ft_pct", "fta", "tpm", "pts", "reb", "ast", "stl", "blk", "tov")


def row(p):
    return dict(player=p["player"], positions=CG.arena.positions_of(p), note=p.get("note") or "",
                z_sum=round(sum(p["z"][c] for c in CG.hoops.CATS), 12), **{c: p[c] for c in COLS})


def main():
    P, by = CG.load_pool()
    state = json.load(open(os.path.join(KIT, "data", "league_state.json"), encoding="utf-8"))
    ros = CG.rosters(state, by)
    names = sorted({p["player"] for r in ros.values() for p in r})
    fx = {
        "_about": "A-9 fixture: in-season rosters (league_state 2026-10-20, IL excluded), season pool lines "
                  "(SEASON_POOL), z_sum from the verified board engine.",
        "rosters": {str(s): [row(p) for p in r] for s, r in sorted(ros.items())},
        "notes": sorted({p.get("note") or "" for p in P}),
        "hash_vectors": [[n, k, salt] for n in names[:40] for k in (0, 1, 31) for salt in (1, 10, 13, 20, 26)]
                        + [["Nikola Jokić", 0, 1], ["Luka Dončić", 5, 22], ["Kristaps Porziņģis", 7, 11]],
    }
    with open(os.path.join(HERE, "fixture.json"), "w", encoding="utf-8") as f:
        json.dump(fx, f, ensure_ascii=False, indent=1)
    print("fixture: %d rosters, %d players, %d notes, %d hash vectors" % (
        len(fx["rosters"]), sum(len(r) for r in fx["rosters"].values()), len(fx["notes"]), len(fx["hash_vectors"])))


if __name__ == "__main__":
    main()
