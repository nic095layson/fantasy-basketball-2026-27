#!/usr/bin/env python3
"""D-ZS-3 record (owner 2026-10-21: "Adopt the fitted values", "Season tools only"): what the season CV changes in the
brief on the committed league state (data/league_state.json) — the waiver swap values on the brief's own shortlist
(co_gm.free_agents, the top 40 by z) and the title odds (league_sim, 10,000 seasons x seeds 2026 and 2027 on the
league schedule, as the brief runs them) — each computed twice: on the draft engine's arena.CV ("before") and on
arena.SEASON_CV ("after"). "Before" sets arena.SEASON_CV to arena.CV for the call, so both go through the same code.
Writes compare.json beside itself."""
import json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(KIT, "scripts"))
import co_gm as CG  # noqa: E402
arena = CG.arena
SEEDS, SEASONS = (2026, 2027), 10000


def swaps(ros, fa, cv):
    keep = arena.SEASON_CV
    arena.SEASON_CV = cv
    try:
        base, pairs = CG.waiver_pairs(ros, fa)
    finally:
        arena.SEASON_CV = keep
    return base, pairs


def title(ros, season_cv):
    out = {}
    with tempfile.TemporaryDirectory() as d:
        sp = os.path.join(d, "state.json")
        json.dump(CG.sim_state({s: [p for p in r if p["player"] in CG.sim_pool_names()] for s, r in ros.items()}), open(sp, "w"))
        for seed in SEEDS:
            op = os.path.join(d, f"o{seed}.json")
            cmd = [sys.executable, os.path.join(CG.DECK, "arena", "mocks", "league_sim.py"), sp, CG.LINES_TAG, str(SEASONS),
                   str(seed), op, "--schedule", CG.SCHEDULE] + (["--season-cv"] if season_cv else [])
            subprocess.run(cmd, check=True, capture_output=True)
            t = json.load(open(op))["teams"][str(CG.OWNER_SEAT)]
            out[str(seed)] = dict(title=t["champ"], playoffs=t["playoff"], cats_per_week=t["cats_per_week"])
    return out


def main():
    P, by = CG.load_pool()
    state = json.load(open(CG.STATE, encoding="utf-8"))
    ros = CG.rosters(state, by)
    fa = CG.free_agents(P, state)
    b0, p0 = swaps(ros, fa, arena.CV)
    b1, p1 = swaps(ros, fa, arena.SEASON_CV)
    key = lambda x: (x["add"], x["drop"])
    new = {key(x): x["d_ecw"] for x in p1}
    top = [dict(add=x["add"], drop=x["drop"], before=x["d_ecw"], after=new[key(x)]) for x in p0[:5]]
    pos0, pos1 = [x for x in p0 if x["d_ecw"] > 0], [x for x in p1 if x["d_ecw"] > 0]
    rec = dict(state=os.path.relpath(CG.STATE, KIT), shortlist=len(fa), pairs=len(p0),
               expected_categories=dict(before=round(b0, 4), after=round(b1, 4)),
               positive_swaps=dict(before=[(x["add"], x["drop"], x["d_ecw"]) for x in pos0],
                                   after=[(x["add"], x["drop"], x["d_ecw"]) for x in pos1]),
               top5_before_with_after=top,
               title_odds=dict(before=title(ros, False), after=title(ros, True)))
    with open(os.path.join(HERE, "compare.json"), "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False); f.write("\n")
    print(json.dumps(rec, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
