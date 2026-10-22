#!/usr/bin/env python3
"""D-RR-1 record (owner 2026-10-22: "Remove it", route "Kit season override"): what data/tag_overrides.csv changes in
the season pool, run twice on the same inputs (the committed box scores, the deck's frozen players_v69.csv, the kit's
pool additions), once without the overrides file and once with it:

  - every cell of pool_season.csv that differs between the two runs;
  - De'Andre Hunter's board availability, weekly availability, adjusted value and free-agent rank on each pool, with
    the waiver shortlist's cut (co_gm.free_agents, the brief's own top 40 by adjusted value) on the committed
    data/league_state.json.

Writes compare.json beside itself."""
import csv
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(KIT, "scripts"))
import season_lines as S  # noqa: E402
import co_gm as CG  # noqa: E402

NAME, DATE = "De'Andre Hunter", "2026-10-22"


def pool_rows(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def hunter(pool_csv, state):
    os.environ["SEASON_POOL"] = pool_csv
    P, by = CG.load_pool()
    h = by[NAME]
    rostered = {p["player"] for t in state["teams"] for p in t["players"]}
    fa = sorted((p for p in P if p["player"] not in rostered and CG.hoops.availability(p) > 0),
                key=lambda p: -CG.hoops.adj_value(p, ()))
    names = [p["player"] for p in fa]
    short = [p["player"] for p in CG.free_agents(P, state)]
    return dict(note_tag=S.note_tag(h["note"]), availability=CG.hoops.availability(h),
                weekly_availability=CG.arena.weekly_availability(h), adj_value=round(CG.hoops.adj_value(h, ()), 4),
                rostered=NAME in rostered, free_agent_rank=names.index(NAME) + 1 if NAME in names else None,
                free_agents=len(names), in_waiver_shortlist=NAME in short,
                shortlist_cut_adj_value=round(CG.hoops.adj_value(CG.free_agents(P, state)[-1], ()), 4))


def main():
    acts = S.load_actuals()
    state = json.load(open(os.path.join(KIT, "data", "league_state.json"), encoding="utf-8"))
    out = {}
    with tempfile.TemporaryDirectory() as d:
        runs = {}
        for side, ov in (("without", None), ("with", S.OVERRIDES)):
            o = os.path.join(d, side)
            S.run(DATE, acts, out_dir=o, additions_csv=S.ADDITIONS, overrides_csv=ov)
            runs[side] = os.path.join(o, "pool_season.csv")
        a, b = pool_rows(runs["without"]), pool_rows(runs["with"])
        out["rows"] = [len(a), len(b)]
        out["cells_differing"] = [dict(player=x["player"], column=k, without=x[k], with_=y[k])
                                  for x, y in zip(a, b) for k in x if x[k] != y[k]]
        out["hunter"] = {side: hunter(runs[side], state) for side in runs}
    out["inputs"] = dict(date=DATE, deck=S.DECK_CSV, overrides=os.path.relpath(S.OVERRIDES, KIT),
                         state="data/league_state.json", actuals_records=len(acts))
    with open(os.path.join(HERE, "compare.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False); f.write("\n")
    print(f"cells differing: {len(out['cells_differing'])}; Hunter " + "; ".join(
        f"{s}: {v['note_tag']}, availability {v['availability']}, adj {v['adj_value']}, FA rank {v['free_agent_rank']}"
        f" of {v['free_agents']}, shortlist {v['in_waiver_shortlist']}" for s, v in out["hunter"].items()))


if __name__ == "__main__":
    main()
