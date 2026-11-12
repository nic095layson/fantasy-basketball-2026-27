#!/usr/bin/env python3
"""Audit finding F4 (after-report 2026-11-12 system audit): the drop-order figures of 2026-11-11 carried sampling error
only. This runs each drop pair under the assumption sweep's variants (red-team step 5, decision robustness), so the
order has a structural band. Analysis only: no roster, line, tag or constant is changed; nothing live reads the record.

Stated to the owner before the run (2026-11-12): the records checkout's league state and season pool of 2026-11-12
(afternoon), the real schedule, returns Tyrese Haliburton 2026-11-21 and Kawhi Leonard 2026-11-23 (reported, not
confirmed; the dates of the 2026-11-11 run), 6,000 seasons x seeds 2026 and 2027 (the sweep's own setting), baseline
plus every declared-band variant whose measured shift on 2026-11-12 was not zero (BENCH_WEIGHT's two were 0.00).

    SEASON_POOL=<records>/data/season/pool_season.csv python3 drop_band.py --records <records checkout> --out drop_band.json
"""
import argparse, copy, hashlib, json, os, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor

DATE = "2026-11-12"
RETURNS = {"Tyrese Haliburton": "2026-11-21", "Kawhi Leonard": "2026-11-23"}
PAIRS = {"Queta + Cam Johnson": ["Neemias Queta", "Cameron Johnson"],
         "Champagnie + Queta": ["Julian Champagnie", "Neemias Queta"],
         "Champagnie + Cam Johnson": ["Julian Champagnie", "Cameron Johnson"]}
SKIP = {"BENCH_WEIGHT"}
SEASONS = 6000


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--records", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--seasons", type=int, default=SEASONS); ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    sys.path.insert(0, os.path.join(a.records, "scripts"))
    import co_gm as CG, il_return as IR
    state = json.load(open(CG.STATE)); weeks = int(json.load(open(CG.SCHEDULE))["regular_season_weeks"])
    P, by = CG.load_pool()
    me = [t for t in state["teams"] if t["seat"] == CG.OWNER_SEAT][0]
    names = [p["player"] for p in me["players"]]
    missing = [n for ns in PAIRS.values() for n in ns if n not in names] + [n for n in RETURNS if n not in names]
    if missing:
        print(f"DROP BAND: HALT — not on the roster of {state.get('as_of')}: {sorted(set(missing))}"); return 1
    path, rows = IR.newest_espn(DATE, os.path.join(a.records, "data", "status"))
    il = IR.il_players(state, rows, DATE, weeks, by=by)
    for x in il:
        if x["player"] in RETURNS:
            x["return_date"] = RETURNS[x["player"]]; x["week"] = IR.return_week(RETURNS[x["player"]], DATE, weeks)
    ros = CG.rosters(state, by, include_il=True)
    rule = IR.windows_for(il, 0, ros, weeks, room=True)

    def custom(drops):
        win = copy.deepcopy(rule); w10 = {}
        for x, d in zip(sorted([x for x in il if x["seat"] == CG.OWNER_SEAT], key=lambda x: x["week"]), drops):
            w10[x["player"]] = (x["week"], weeks); w10[d] = (1, x["week"] - 1)
        win[CG.OWNER_SEAT] = w10; return win
    configs = {"rule's pick": rule}; configs.update({k: custom(v) for k, v in PAIRS.items()})
    reg = json.load(open(os.path.join(a.records, "scripts", "redteam", "constants_registry.json")))
    variants = [("baseline", None, None)]
    for e in reg["constants"]:
        if e.get("status") == "declared_band" and e["name"] not in SKIP:
            variants += [(b["label"], {k: v for k, v in b.items() if k != "label"}, f"{e['module']}.{e['name']}") for b in e["band"]]
    work = tempfile.mkdtemp()
    jobs = [(c, v, s) for c in configs for v in variants for s in IR.SEEDS]

    def run(j):
        c, (label, patch, _), s = j
        tag = "".join(ch if ch.isalnum() else "_" for ch in c + "__" + label)[:70]
        r = CG.run_league_sim(ros, s, a.seasons, work, tag=tag, windows=configs[c], patch=patch)
        return c, label, s, r["teams"][str(CG.OWNER_SEAT)]["champ"]
    res = {}
    with ThreadPoolExecutor(a.workers) as ex:
        for c, label, s, t in ex.map(run, jobs):
            res.setdefault(c, {}).setdefault(label, {})[str(s)] = t
            print(c, "|", label, s, t, flush=True)
    mean = lambda d: round(sum(d.values()) / len(d), 2)
    table = {c: {l: mean(v) for l, v in d.items()} for c, d in res.items()}
    order = {l: sorted(configs, key=lambda c: -table[c][l]) for l, _, _ in variants}
    rec = dict(attack="F4 drop-order decision robustness", date=DATE, seasons=a.seasons, seeds=list(IR.SEEDS), returns=RETURNS,
               espn_file=os.path.basename(path),
               windows_seat10={c: {p: list(w) for p, w in configs[c].get(CG.OWNER_SEAT, {}).items()} for c in configs},
               variants=[dict(label=l, constant=k, patch=p) for l, p, k in variants],
               title_by_seed=res, title=table, order=order,
               spread_best_minus_rule={l: round(max(table[c][l] for c in configs) - table["rule's pick"][l], 2) for l, _, _ in variants},
               fingerprint=dict(deck_head=subprocess.run(["git", "-C", CG.DECK, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip(),
                                records_head=subprocess.run(["git", "-C", a.records, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip(),
                                state_sha256=sha(CG.STATE), pool_sha256=sha(os.environ["SEASON_POOL"]), schedule_sha256=sha(CG.SCHEDULE),
                                kit_sha256={"report/after-reports/findings-fix-2026-11-12/drop_band.py": sha(os.path.abspath(__file__))}))
    json.dump(rec, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("DROP BAND: PASS —", json.dumps(order["baseline"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
