#!/usr/bin/env python3
"""Owner 2026-10-19: "Can you please provide analysis for picking up Tre Jones and/or Jrue Holiday on my roster?
In place of PJ Washington and/or Braun."

Rosters: data/league_state.json as-of 2026-10-19 (the owner's Yahoo paste, 165/165 resolved; seat 10 = owner).
Lines: deck v69 (players_v69.csv, deck 259c630) — the locked 10/14 blend; the season blend holds zero
regular-season games on 2026-10-19, so these are the live lines. Measure 1: change in expected weekly category
wins (live_retro's pwins on arena.team_week_model) against the 11 current rosters, per category. Measure 2:
title/playoff odds through the verified league simulator, 10,000 seasons, seeds 2026 and 2027, random weekly
pairings (the baseline mode the draft grade used), current-roster baseline plus the five scenarios. Context: the
best available add per drop among the 40 best free agents by board value (same loop as waiver_moves.py).
Writes jones_holiday.json."""
import json, math, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
H = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.normpath(os.path.join(H, "..", "..", ".."))
DECK = "/home/user/yahoo-fantasy-basketball"
sys.path.insert(0, DECK + "/scripts"); sys.path.insert(0, DECK + "/arena")
import hoops, arena
hoops.DATA_PATH = f"{DECK}/arena/results/players_v69.csv"
P = hoops.zscores(hoops.load_players()); by = {p["player"]: p for p in P}
ls = json.load(open(os.path.join(KIT, "data", "league_state.json"), encoding="utf-8"))
assert ls["as_of"] == "2026-10-19"
ros = {t["seat"]: [by[p["player"]] for p in t["players"]] for t in ls["teams"]}
owned = {p["player"] for t in ls["teams"] for p in t["players"]}
OWNER = 10; CATS = hoops.CATS; SEEDS = (2026, 2027)
ADDS = ["Tre Jones", "Jrue Holiday"]; DROPS = ["PJ Washington", "Christian Braun"]
for n in ADDS: assert n not in owned and hoops.availability(by[n]) == 1.0, n
for n in DROPS: assert any(p["player"] == n for p in ls["teams"][[t["seat"] for t in ls["teams"]].index(OWNER)]["players"]), n

def pwins(m, opps):
    tot = 0.0
    for om in opps:
        for c in CATS:
            d = (m[0][c] - om[0][c]) / (math.sqrt(m[1][c] + om[1][c]) or 1e-9)
            pr = 0.5 * (1 + math.erf(d / math.sqrt(2))); tot += (1 - pr) if c == "TO" else pr
    return tot / len(opps)

def cat_wins(m, opps):
    return {c: sum(((1 - x) if c == "TO" else x) for x in
                   [0.5 * (1 + math.erf(((m[0][c] - om[0][c]) / (math.sqrt(m[1][c] + om[1][c]) or 1e-9)) / math.sqrt(2)))
                    for om in opps]) / len(opps) for c in CATS}

opp = [arena.team_week_model(r) for s, r in ros.items() if s != OWNER]
mine = ros[OWNER]
base_m = arena.team_week_model(mine)
base_e = pwins(base_m, opp); base_cats = cat_wins(base_m, opp)

def apply(adds, drops):
    new = [x for x in mine if x["player"] not in drops] + [by[a] for a in adds]
    assert len(new) == len(mine) + len(adds) - len(drops)
    return new

SCEN = [(("Tre Jones",), ("PJ Washington",)), (("Tre Jones",), ("Christian Braun",)),
        (("Jrue Holiday",), ("PJ Washington",)), (("Jrue Holiday",), ("Christian Braun",)),
        (("Tre Jones", "Jrue Holiday"), ("PJ Washington", "Christian Braun"))]
rows = []
for adds, drops in SCEN:
    new = apply(adds, drops); m = arena.team_week_model(new)
    cw = cat_wins(m, opp)
    rows.append(dict(add=list(adds), drop=list(drops), d_ecw=round(pwins(m, opp) - base_e, 4),
                     d_cats={c: round(cw[c] - base_cats[c], 4) for c in CATS}))

# player values on the board (adjusted value, availability)
vals = {n: dict(team=by[n]["team"], pos=by[n].get("pos"), gp=by[n].get("gp"), avail=hoops.availability(by[n]),
                adj_value=round(hoops.adj_value(by[n], ()), 3),
                z={c: round(by[n]["z"][c], 2) for c in CATS} if "z" in by[n] else None)
        for n in ADDS + DROPS}

# context: best available add per drop (top-40 FAs by board value, owner veto off the pool)
veto = hoops.do_not_draft()
fa = sorted((p for p in P if p["player"] not in owned and hoops.availability(p) > 0 and p["player"] not in veto),
            key=lambda p: -hoops.adj_value(p, ()))[:40]
best = {}
for d in DROPS:
    cand = []
    for a in fa:
        m = arena.team_week_model(apply((a["player"],), (d,)))
        cand.append((a["player"], round(pwins(m, opp) - base_e, 4)))
    cand.sort(key=lambda x: -x[1]); best[d] = cand[:5]

# sims
def sim(job):
    key, roster, sd = job
    picks = []
    for s, r in ros.items():
        rr = roster if s == OWNER else r
        picks += [dict(slot=s, player=p["player"]) for p in rr]
    stt = dict(teams=12, slot=OWNER, size=max(len(r) for r in ros.values()), punt=[], picks=picks)
    sp = os.path.join(H, f"_jh_{key}_{sd}_state.json"); op = os.path.join(H, f"_jh_{key}_{sd}_out.json")
    json.dump(stt, open(sp, "w"), ensure_ascii=False)
    subprocess.run([sys.executable, f"{DECK}/arena/mocks/league_sim.py", sp, "v69", "10000", str(sd), op],
                   check=True, capture_output=True)
    r = json.load(open(op))["teams"][str(OWNER)]; os.remove(sp); os.remove(op)
    return key, sd, r["champ"], r["playoff"]

jobs = [("base", mine, sd) for sd in SEEDS]
for i, (adds, drops) in enumerate(SCEN): jobs += [(f"s{i}", apply(adds, drops), sd) for sd in SEEDS]
with ThreadPoolExecutor(4) as ex: res = list(ex.map(sim, jobs))
got = {(k, sd): (c, p) for k, sd, c, p in res}
base_t = {sd: got[("base", sd)][0] for sd in SEEDS}; base_p = {sd: got[("base", sd)][1] for sd in SEEDS}
for i, r in enumerate(rows):
    r["title"] = {sd: round(got[(f"s{i}", sd)][0], 2) for sd in SEEDS}
    r["d_title"] = {sd: round(got[(f"s{i}", sd)][0] - base_t[sd], 2) for sd in SEEDS}
    r["d_title_mean"] = round(sum(r["d_title"].values()) / 2, 2)
    r["d_playoff"] = {sd: round(got[(f"s{i}", sd)][1] - base_p[sd], 2) for sd in SEEDS}

out = dict(as_of="2026-10-19", lines="deck v69 (players_v69.csv, deck 259c630)", seasons=10000, seeds=list(SEEDS),
           base_ecw=round(base_e, 4), base_cats={c: round(v, 4) for c, v in base_cats.items()},
           base_title=base_t, base_playoff=base_p, players=vals, scenarios=rows, best_alternative_per_drop=best)
json.dump(out, open(os.path.join(H, "jones_holiday.json"), "w"), indent=1, ensure_ascii=False)
print("base ECW", round(base_e, 4), "| base title", base_t, "| base playoff", base_p)
for r in rows:
    print(f"+{'+'.join(r['add']):<32} -{'+'.join(r['drop']):<36} dECW {r['d_ecw']:+.4f}  dTitle {r['d_title'][2026]:+.2f}/{r['d_title'][2027]:+.2f} mean {r['d_title_mean']:+.2f}  dPO {r['d_playoff'][2026]:+.2f}/{r['d_playoff'][2027]:+.2f}")
print("values:", json.dumps(vals, indent=1))
print("best alt per drop:", json.dumps(best, indent=1))
