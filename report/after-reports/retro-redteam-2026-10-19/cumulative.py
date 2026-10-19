#!/usr/bin/env python3
"""The close-to-real curve: the robust swaps of retro_redteam.json taken one at a time in order of their single-swap
title gain (largest first), each cumulative board run 10,000 seasons on seeds 2026 and 2027 on the shipped engine, so
the owner can see how much of the gain the first one, two, three changes carry. Writes cumulative.json."""
import json, os, random, sys
from concurrent.futures import ProcessPoolExecutor
H = os.path.dirname(os.path.abspath(__file__))
import retro_redteam as R
REC = json.load(open(os.path.join(H, "retro_redteam.json"), encoding="utf-8"))
SEEDS = tuple(REC["seeds"]); SEASONS = REC["seasons"]
close = sorted(REC["close_to_real"]["swaps"], key=lambda s: -s["d_title_mean"])
boards, picks, applied = [], [dict(pk) for pk in R.PICKS], []
for s in close:
    picks = R.swap_picks(picks, s["pick"] - 1, s["alt"]); applied.append(s)
    boards.append((len(applied), [dict(pk) for pk in picks], [dict(a) for a in applied]))
jobs = [(f"k{k}", b, sd, SEASONS, None) for k, b, _ in boards for sd in SEEDS]
if __name__ == "__main__":
    with ProcessPoolExecutor(4) as ex: RR = list(ex.map(R.sim_job, jobs))
    got = {}
    for key, sd, _, c, p in RR: got.setdefault(key, {})[str(sd)] = dict(title=round(c, 2), playoff=round(p, 2))
    base = {str(sd): REC["baseline"][str(sd)]["title"] for sd in SEEDS}
    out = dict(engine_commit=REC["engine_commit"], seeds=list(SEEDS), seasons=SEASONS, baseline=base, order="single-swap mean title gain, largest first",
               steps=[dict(k=k, swaps=[dict(pick=a["pick"], owner=a["owner"], alt=a["alt"], d_title_mean=a["d_title_mean"]) for a in ap],
                           title=got[f"k{k}"], d_title={sd: round(got[f"k{k}"][sd]["title"] - base[sd], 2) for sd in base},
                           d_title_mean=round(sum(got[f"k{k}"][sd]["title"] - base[sd] for sd in base) / 2, 2)) for k, _, ap in boards])
    json.dump(out, open(os.path.join(H, "cumulative.json"), "w"), indent=1, ensure_ascii=False)
    for st in out["steps"]:
        print(f"k={st['k']}  +{st['swaps'][-1]['alt']} for {st['swaps'][-1]['owner']} (#{st['swaps'][-1]['pick']})  title {st['title']['2026']['title']:.2f} / {st['title']['2027']['title']:.2f}  d {st['d_title']['2026']:+.2f} / {st['d_title']['2027']:+.2f}  mean {st['d_title_mean']:+.2f}")
