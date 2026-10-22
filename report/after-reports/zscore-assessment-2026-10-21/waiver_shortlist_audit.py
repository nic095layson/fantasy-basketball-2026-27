#!/usr/bin/env python3
"""Measurement 1 of the z-score assessment (owner 2026-10-21, "Measure first"): does the brief's waiver shortlist —
the top WAIVER_CANDIDATES pooled free agents by z value (co_gm.free_agents) — hide swaps that the brief's own
head-to-head model (co_gm.waiver_pairs: change in expected categories won per week vs the 11 opponents) rates
positive? Both sets are scored by the same function on the same inputs; only the shortlist differs.

Inputs pinned beside this file: the 10/21 league state built by league_live from the pinned Flaim pull, and the 10/21
season pool (season_lines with data/pool_additions.csv). Current hand-set weekly variance (arena.CV). Writes
waiver_shortlist_audit.json. Analysis only."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
os.environ["SEASON_POOL"] = os.path.join(HERE, "pool_season_2026-10-21.csv")
sys.path.insert(0, os.path.join(KIT, "scripts"))
import co_gm as CG  # noqa: E402

P, by = CG.load_pool()
state = json.load(open(os.path.join(HERE, "league_state_2026-10-21_flaim.json"), encoding="utf-8"))
ros = CG.rosters(state, by)
short = CG.free_agents(P, state)                       # the brief's rule: top 40 by adj_value
full = CG.free_agents(P, state, n=10 ** 6)            # every pooled free agent, same filters
zrank = {p["player"]: i + 1 for i, p in enumerate(full)}
base, pairs_short = CG.waiver_pairs(ros, short)
base2, pairs_full = CG.waiver_pairs(ros, full)
assert abs(base - base2) < 1e-12


def best_by_add(pairs):
    out = {}
    for x in pairs:
        if x["add"] not in out or x["d_ecw"] > out[x["add"]]["d_ecw"]:
            out[x["add"]] = x
    return out


bs, bf = best_by_add(pairs_short), best_by_add(pairs_full)
pos_full = sorted((x for x in bf.values() if x["d_ecw"] > 0), key=lambda x: -x["d_ecw"])
pos_short = [x for x in pos_full if x["add"] in bs]
hidden = [x for x in pos_full if x["add"] not in bs]
rec = dict(date="2026-10-21", owner_seat=CG.OWNER_SEAT, base_ecw=round(base, 4), shortlist_size=len(short),
           pooled_free_agents=len(full), positive_adds_full=len(pos_full), positive_adds_in_shortlist=len(pos_short),
           positive_adds_hidden=len(hidden),
           best_in_shortlist=pos_short[0] if pos_short else None, best_overall=pos_full[0] if pos_full else None,
           top10_overall=[dict(x, z_rank=zrank[x["add"]], in_shortlist=x["add"] in bs) for x in pos_full[:10]],
           variance="arena.CV hand-set (declared band x0.8/x1.2)", lines="season pool 10/21 (pool_season_2026-10-21.csv)")
json.dump(rec, open(os.path.join(HERE, "waiver_shortlist_audit.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps({k: rec[k] for k in ("base_ecw", "shortlist_size", "pooled_free_agents", "positive_adds_full",
                                      "positive_adds_in_shortlist", "positive_adds_hidden")}))
for x in rec["top10_overall"]:
    print(f"{x['add']:<26} z-rank {x['z_rank']:>3}  drop {x['drop']:<24} dECW {x['d_ecw']:+.4f}  {'in' if x['in_shortlist'] else 'HIDDEN'}")
