#!/usr/bin/env python3
"""Attack A-9 comparison: the live season simulator (deck arena.py, via the kit's co_gm) vs a re-implementation
written by a separate attacker from SPEC.md alone (red-team skill step 2; Council 2026-10-21, Outsider: "the one
technique that demonstrably worked today, aimed at the only part that has never had it").

Pre-registered before the attacker's output was read (2026-10-21, stated to the owner in the plan):
  - hash, weights: exact equality
  - models, pcat, pwins: |diff| <= 1e-9 (relative for models)
  - availability: exact on every note EXCEPT tags starting 'out-' — SPEC.md §1 follows the documented intent
    ("mirrors the ranking engine", which excludes out-* at 0.0); the engine has no out-* branch and returns 0.88.
    Divergence there is predicted, is a finding (flagged, not fixed), and is behavioural evidence of independence.
  - season (stochastic, different random streams): title and playoff share per seat, |z| <= 3 with the binomial
    standard error of the difference.

Found on the first run and handled without moving a tolerance: the engine side had been seeded 20261021 and the
attacker chose the same seed AND, independently, the same draw order through the regular season and seeding, so the
two samples shared one random stream (all 12 playoff shares identical to the digit) — not the independent samples
the |z| test assumes, under which it is too lenient. The pre-registered test now runs the engine on an independent
seed (ENGINE_SEED); the same-seed run is kept as a separate, stronger check ("stream"): with one shared stream, every
regular season, standings table and seeding must match exactly, so the playoff shares must be equal seat for seat.
Title shares may still differ there: the two sides list the final's teams in a different order (SPEC.md left it
open; distributionally equivalent).

    python3 report/after-reports/redteam-sim-2026-10-21/compare.py --attacker PATH/attacker_out.json
Writes rt_sim.json beside this file.
"""
import argparse
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(KIT, "scripts"))
import co_gm as CG  # noqa: E402
import run_ledger  # noqa: E402

A, H = CG.arena, CG.hoops
SEASONS, ENGINE_SEED = 20000, 1021
TOL = 1e-9


def engine_player(r):
    p = {k: r[k] for k in ("player", "note", "fg_pct", "fga", "ft_pct", "fta", "tpm", "pts", "reb", "ast",
                           "stl", "blk", "tov")}
    p["pos"] = ",".join(r["positions"])
    p["z"] = {c: 0.0 for c in H.CATS}
    p["z"]["FG%"] = r["z_sum"]
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--attacker", required=True)
    ap.add_argument("--out", default=os.path.join(HERE, "rt_sim.json"))
    a = ap.parse_args()
    fx = json.load(open(os.path.join(HERE, "fixture.json"), encoding="utf-8"))
    at = json.load(open(a.attacker, encoding="utf-8"))
    ros = {s: [engine_player(r) for r in rs] for s, rs in fx["rosters"].items()}
    out = {"tolerances": {"exact": ["hash", "weights", "availability (non out-*)"], "abs_or_rel": TOL,
                          "season_z": 3}, "fingerprint": run_ledger.fingerprint(), "sections": {}}
    sec = out["sections"]

    # availability
    diffs, out_star = [], []
    for n in fx["notes"]:
        e, x = A.weekly_availability({"note": n}), at["availability"].get(n)
        if e != x:
            (out_star if H.note_tag(n).startswith("out-") else diffs).append({"note": n[:80], "engine": e, "attacker": x})
    sec["availability"] = {"n": len(fx["notes"]), "diff_non_out": diffs, "diff_out_predicted": out_star,
                           "pass": not diffs}

    # hash
    amap = {(h[0], h[1], h[2]): h[3] for h in at["hash"]}
    hd = [{"v": v, "engine": A.df_hash(*v), "attacker": amap.get(tuple(v))} for v in fx["hash_vectors"]
          if A.df_hash(*v) != amap.get(tuple(v))]
    sec["hash"] = {"n": len(fx["hash_vectors"]), "diff": hd[:20], "n_diff": len(hd), "pass": not hd}

    # weights + models
    wd, md, models = [], [], {}
    for s, r in ros.items():
        w = A.daily_fill_weights(r)
        for p in r:
            if w[id(p)] != at["weights"][s].get(p["player"]):
                wd.append({"seat": s, "player": p["player"], "engine": w[id(p)], "attacker": at["weights"][s].get(p["player"])})
        models[s] = A.team_week_model(r)
        for c in H.CATS:
            for i, lab in ((0, "mu"), (1, "var")):
                e, x = models[s][i][c], at["models"][s][c][i]
                if abs(e - x) > TOL * max(1.0, abs(e)):
                    md.append({"seat": s, "cat": c, lab: [e, x]})
    sec["weights"] = {"n": sum(len(r) for r in ros.values()), "diff": wd[:20], "n_diff": len(wd), "pass": not wd}
    sec["models"] = {"n": len(ros) * 9 * 2, "diff": md[:20], "n_diff": len(md), "pass": not md}

    # pcat + pwins
    pd, nd = [], 0
    for sa in ros:
        for sb in ros:
            if sa == sb:
                continue
            for c in H.CATS:
                nd += 1
                e, x = CG._pcat(models[sa], models[sb], c), at["pcat"][f"{sa}|{sb}"][c]
                if abs(e - x) > TOL:
                    pd.append({"pair": f"{sa}|{sb}", "cat": c, "engine": e, "attacker": x})
    sec["pcat"] = {"n": nd, "diff": pd[:20], "n_diff": len(pd), "pass": not pd}
    wwd = []
    for s in ros:
        e = CG.pwins(models[s], [models[o] for o in ros if o != s])
        if abs(e - at["pwins"][s]) > TOL:
            wwd.append({"seat": s, "engine": e, "attacker": at["pwins"][s]})
    sec["pwins"] = {"n": len(ros), "diff": wwd, "pass": not wwd}

    # season (stochastic)
    ids = {int(s): r for s, r in ros.items()}
    n2 = at["season"]["seasons"]
    aseed = at["season"].get("seed")
    stream = None
    if aseed is not None and n2 == SEASONS:
        _, splays = A.simulate_seasons(ids, SEASONS, random.Random(aseed))
        eq = [s for s in ros if splays[int(s)] / SEASONS == at["season"]["playoffs"][s]]
        stream = {"seed": aseed, "playoff_shares_identical": len(eq), "of": len(ros)}
    if ENGINE_SEED == aseed:
        raise SystemExit("engine seed equals the attacker's: the samples would share a stream")
    champs, plays = A.simulate_seasons(ids, SEASONS, random.Random(ENGINE_SEED))
    rows, worst = [], 0.0
    for s in ros:
        for lab, eng, att in (("title", champs[int(s)] / SEASONS, at["season"]["title"][s]),
                              ("playoffs", plays[int(s)] / SEASONS, at["season"]["playoffs"][s])):
            pbar = (eng * SEASONS + att * n2) / (SEASONS + n2)
            se = math.sqrt(max(pbar * (1 - pbar), 1e-12) * (1 / SEASONS + 1 / n2))
            z = (eng - att) / se
            worst = max(worst, abs(z))
            rows.append({"seat": s, "share": lab, "engine": round(eng, 5), "attacker": round(att, 5), "z": round(z, 2)})
    sec["season"] = {"engine_seasons": SEASONS, "engine_seed": ENGINE_SEED, "attacker_seasons": n2,
                     "same_seed_stream_check": stream,
                     "attacker_seed": at["season"].get("seed"), "rows": rows, "max_abs_z": round(worst, 2),
                     "n_over_3": sum(1 for r in rows if abs(r["z"]) > 3), "pass": worst <= 3}
    out["attacker_choices"] = at.get("choices", [])
    out["verdict"] = "PASS" if all(v["pass"] for v in sec.values()) else "FAIL"
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    for k, v in sec.items():
        extra = (f" out-* predicted diffs {len(v['diff_out_predicted'])}" if k == "availability" else "") + \
                (f" max|z| {v['max_abs_z']}" if k == "season" else "") + (f" n_diff {len(v['diff_non_out'])}" if k == "availability" else
                 f" n_diff {v.get('n_diff', len(v.get('diff', [])))}" if k != "season" else "")
        print(f"  {k}: {'PASS' if v['pass'] else 'FAIL'} (n={v.get('n', '')}){extra}")
    print(f"A-9 SIM ATTACK: {out['verdict']} — engine {out['fingerprint']['engine_commit']}")
    return 0 if out["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
