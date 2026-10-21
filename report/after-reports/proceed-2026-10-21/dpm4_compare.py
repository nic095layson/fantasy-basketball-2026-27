#!/usr/bin/env python3
"""D-PM-4 risk/mild, measurement only (owner "proceed with all", 2026-10-21, decision-sheet item 5). No value changes.

The three availability numbers that exist, per player, side by side:
  deck board   hoops.availability(note)        tier multiplier, healthy 1.00 (hoops.adj_value: tv x tier; no games term)
  kit board    rank_engine.avail(gp)           gp/82 + (1 - gp/82) x STREAM_R (no injury tier; GP carries it)
  simulator    arena.weekly_availability(note) share of a week's games, healthy 0.88
No instrument multiplies the deck tier by avail(gp); the 2026-10-21 audit's "tier x avail(gp)" premise was wrong, so
that product is not computed here. Each number is also shown relative to its own healthy reference, which is the
like-for-like reading ("this player's value against an otherwise identical healthy player"): deck / 1.00,
simulator / 0.88, kit / the median avail(gp) of the healthy players the kit board prices. Rows at the kit's
exclusion class (GP <= EXCLUSION_GP, or FA) are held off the kit board and counted, not priced.

Population (stated before the run): the in-season pool data/season/pool_season.csv (deck schema, notes), joined to
data/season/projections_season.csv (kit schema, gp) by the deck planes gate's name fold (check_planes.norm); and the
subset on active league rosters (data/league_state.json, IL slots excluded per D-IS-8). Unmatched rows are listed.
Writes dpm4.json beside this script."""
import csv, hashlib, json, os, statistics, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
DECK = os.path.abspath(os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball"))
sys.path.insert(0, os.path.join(DECK, "scripts")); sys.path.insert(0, os.path.join(DECK, "arena"))
sys.path.insert(0, os.path.join(KIT, "report")); sys.path.insert(0, os.path.join(KIT, "scripts"))
import hoops, arena, check_planes as CP, rank_engine as RE, run_ledger  # noqa: E402

POOL = os.path.join(KIT, "data", "season", "pool_season.csv")
LINES = os.path.join(KIT, "data", "season", "projections_season.csv")
STATE = os.path.join(KIT, "data", "league_state.json")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:12]


def tier(note):
    t = hoops.note_tag(note)
    if t.startswith("out-"):
        return "out"
    a = hoops.availability({"note": note})
    return {1.0: "healthy", 0.85: "mild", 0.78: "risk", 0.0: "recovery"}[a]


def summ(xs):
    return dict(n=len(xs), mean=round(statistics.mean(xs), 4), min=round(min(xs), 4), max=round(max(xs), 4)) if xs else dict(n=0)


def main():
    pool = list(csv.DictReader(open(POOL, encoding="utf-8")))
    kit = {CP.norm(r["name"]): r for r in csv.DictReader(open(LINES, encoding="utf-8"))}
    st = json.load(open(STATE, encoding="utf-8"))
    active = {p["player"] for t in st["teams"] for p in t["players"] if p["slot"] != "IL"}
    rows, unmatched = [], []
    for p in pool:
        k = kit.get(CP.norm(p["player"]))
        tr = tier(p["note"])
        if k is None:
            unmatched.append(dict(player=p["player"], tier=tr))
            continue
        gp = float(k["gp"])
        rows.append(dict(player=p["player"], tag=hoops.note_tag(p["note"]), tier=tr, gp=gp,
                         deck=hoops.availability(p), kit=round(RE.avail(gp), 4),
                         kit_held=k["team"] == "FA" or gp <= RE.EXCLUSION_GP,
                         sim=arena.weekly_availability(p), active=p["player"] in active))
    out = dict(fingerprint=run_ledger.fingerprint(DECK, KIT), stream_r=RE.STREAM_R,
               inputs={os.path.relpath(x, KIT): sha(x) for x in (POOL, LINES, STATE)},
               pool_rows=len(pool), matched=len(rows), unmatched=unmatched, populations={})
    for label, pop in (("pool", rows), ("active_rosters", [r for r in rows if r["active"]])):
        healthy = [r["kit"] for r in pop if r["tier"] == "healthy" and not r["kit_held"]]
        kref = statistics.median(healthy)
        sref = arena.weekly_availability({"note": ""})
        per = {}
        for tr in ("healthy", "mild", "risk", "recovery", "out"):
            g = [r for r in pop if r["tier"] == tr]
            if not g:
                continue
            priced = [r for r in g if not r["kit_held"]]
            per[tr] = dict(n=len(g), kit_held=len(g) - len(priced), gp=summ([r["gp"] for r in g]),
                           deck_abs=sorted({r["deck"] for r in g}), sim_abs=sorted({r["sim"] for r in g}),
                           kit_abs=summ([r["kit"] for r in priced]),
                           kit_at_or_above_healthy_median=sum(1 for r in priced if r["kit"] >= kref),
                           deck_rel=sorted({round(r["deck"] / 1.0, 4) for r in g}),
                           sim_rel=sorted({round(r["sim"] / sref, 4) for r in g}),
                           kit_rel=summ([r["kit"] / kref for r in priced]))  # held rows are off the kit board
        out["populations"][label] = dict(n=len(pop), kit_healthy_median=round(kref, 4), sim_healthy=sref, tiers=per,
                                         players=[dict(r, kit_rel=round(r["kit"] / kref, 4),
                                                       sim_rel=round(r["sim"] / sref, 4))
                                                  for r in pop if r["tier"] in ("mild", "risk")])
    with open(os.path.join(HERE, "dpm4.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"D-PM-4 measurement on engine {out['fingerprint']['engine_commit']}: {len(rows)}/{len(pool)} matched")
    for label, P in out["populations"].items():
        print(f"[{label}] n={P['n']} kit healthy median {P['kit_healthy_median']} sim healthy {P['sim_healthy']}")
        for tr, d in P["tiers"].items():
            print(f"  {tr:<9} n={d['n']:>3} (kit-held {d['kit_held']})  gp {d['gp'].get('mean')}  deck_rel {d['deck_rel']}  "
                  f"sim_rel {d['sim_rel']}  kit_rel mean {d['kit_rel'].get('mean')} [{d['kit_rel'].get('min')}, "
                  f"{d['kit_rel'].get('max')}]  kit >= healthy median {d['kit_at_or_above_healthy_median']}")


if __name__ == "__main__":
    main()
