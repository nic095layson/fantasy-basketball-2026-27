#!/usr/bin/env python3
"""Package scan (owner 2026-11-11, audit pick C): packages of one or two moves scored for this week and for the title,
on demand. The brief scores single swaps once a morning; on 2026-11-10 the owner asked "Collins plus who, dropping
which two?" at night and the answer took scratch scripts. This is that answer as a command.

For the day's roster, free-agent list and week (the week card's own inputs and model):
  - adds: every available free agent with a pool line (availability above 0); --must-add fixes one of them;
  - drops: the DROP_POOL lowest-value players on the active roster (a star is never offered as a drop);
  - every package of K adds for K drops gets (1) this week's chance of 5+ categories (week_matchup's model; the
    moves count from tomorrow, as the decision card counts a pair, or from the day's games with --from-today) and (2) the season screen the brief uses (expected weekly categories against the
    other eleven teams);
  - the top SHORTLIST by each measure, and every --named package, get the title simulation: SEASONS x 2 seeds, IL
    players never returning (the brief's world).
An add that would be the lowest-value active player is flagged as the next cut when the owner's first IL player
returns: the return-on-time world then removes the add itself, so no return-world figure is given for it.

Display only: nothing here changes a line, a roster, a tag or a constant, and nothing reaches a graded record.

    SEASON_POOL=data/season/pool_season.csv python3 scripts/package_scan.py --date 2026-11-11 --must-add "John Collins" \\
        --named "John Collins+Ziaire Williams/Kris Dunn+Alex Caruso" [--k 2] [--yahoo-pull FILE] [--seasons 10000]
Prints 'PACKAGE SCAN: PASS — ...' or 'PACKAGE SCAN: HALT — <why>'. Exit 0 / 1.
"""
import argparse
import itertools
import json
import os
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

OWNER_SEAT = 10
SEEDS = (2026, 2027)
DROP_POOL = 7     # hand-set scan width (owner 2026-11-11): the seven lowest-value active players are offered as drops
SHORTLIST = 6     # hand-set: the top six by each measure are simulated; a named package always is
LABEL = ("Display only. Week: the week card's model, moves counted from the day's games on. Title: IL players never "
         "return; sampling error on a difference is about ±0.7 at 10,000 seasons x 2 seeds.")


class PackageError(Exception):
    pass


def parse_named(text):
    """'A+B/C+D' -> {adds: [A, B], drops: [C, D]}; the two sides must be the same size."""
    if "/" not in text:
        raise PackageError(f"a package is written adds/drops, for example 'A+B/C+D': {text!r}")
    a, d = (sorted(x.strip() for x in side.split("+") if x.strip()) for side in text.split("/", 1))
    if not a or len(a) != len(d):
        raise PackageError(f"a package needs as many drops as adds: {text!r}")
    return dict(adds=[x.strip() for x in text.split("/", 1)[0].split("+")], drops=[x.strip() for x in text.split("/", 1)[1].split("+")])


def scan(mine, fas, by, avail, rosters, k, must_add, drop_pool, shortlist, named, seasons, sim, work, week_fn, ecw_fn,
         il=None, value=None, seeds=SEEDS, workers=1):
    """mine / fas: [{player, value}] (the week card's rows); rosters: {seat: [pool rows]} (the simulator's);
    week_fn(names) -> (P(5+), expected categories); ecw_fn(names) -> expected weekly categories against the league;
    sim: co_gm.run_league_sim or a stand-in. Returns the record."""
    value = value or (lambda p: p["adj"])
    my = [r["player"] for r in mine]
    free = sorted(f["player"] for f in fas if f["player"] in by and avail.get(f["player"], 1.0) > 0)
    if must_add and must_add not in free:
        raise PackageError(f"{must_add} is not an available free agent with a pool line today")
    pool = [r["player"] for r in sorted(mine, key=lambda r: r["value"])[:drop_pool]]
    for n in named:
        bad = [a for a in n["adds"] if a not in free] + [d for d in n["drops"] if d not in my]
        if bad or len(n["adds"]) != len(n["drops"]):
            raise PackageError("not available or not on my active roster: " + ", ".join(bad) if bad else "a package needs as many drops as adds")
    key = lambda adds, drops: (tuple(sorted(adds)), tuple(sorted(drops)))
    packs = {}
    for adds in itertools.combinations(free, k):
        if must_add and must_add not in adds:
            continue
        for drops in itertools.combinations(sorted(pool), k):
            packs[key(adds, drops)] = False
    n_pool = len(packs)
    for n in named:
        packs[key(n["adds"], n["drops"])] = True
    roster_after = lambda adds, drops: [x for x in my if x not in drops] + list(adds)
    b5, bexp = week_fn(my)
    becw = ecw_fn(my)
    first_il = min((x for x in il or [] if x.get("seat") == OWNER_SEAT and x.get("week") is not None), key=lambda x: x["week"], default=None)
    rows = []
    for (adds, drops), is_named in packs.items():
        after = roster_after(adds, drops)
        p5, ex = week_fn(after)
        cut = None
        if first_il:
            weak = min(after, key=lambda n: value(by[n]))
            if weak in adds:
                cut = dict(player=weak, when=first_il["player"], return_date=first_il.get("return_date"))
        rows.append(dict(adds=list(adds), drops=list(drops), week=dict(p5=p5, d_p5=p5 - b5, d_exp=ex - bexp),
                         season_d_ecw=ecw_fn(after) - becw, title=None, first_cut=cut, **({"named": True} if is_named else {})))
    by_week = sorted(rows, key=lambda x: -x["week"]["p5"])
    by_ecw = sorted(rows, key=lambda x: -x["season_d_ecw"])
    for i, x in enumerate(by_week, 1):
        x["rank_week"] = i
    for i, x in enumerate(by_ecw, 1):
        x["rank_season"] = i
    picked = {id(x): x for x in by_week[:shortlist] + by_ecw[:shortlist] + [x for x in rows if x.get("named")]}

    def swap(adds, drops):
        r = {s: list(v) for s, v in rosters.items()}
        r[OWNER_SEAT] = [p for p in r[OWNER_SEAT] if p["player"] not in drops] + [by[a] for a in adds]
        return r

    def run(job):
        n, ros = job
        v = [sim(ros, s, seasons, work, tag=f"ps{n}")["teams"][str(OWNER_SEAT)]["champ"] for s in seeds]
        return sum(v) / len(v), v
    jobs = [(0, rosters)] + [(i, swap(x["adds"], x["drops"])) for i, x in enumerate(picked.values(), 1)]
    if workers > 1 and len(jobs) > 1:
        with ThreadPoolExecutor(workers) as ex:
            res = list(ex.map(run, jobs))
    else:
        res = [run(j) for j in jobs]
    base_title = res[0][0]
    for x, (m, v) in zip(picked.values(), res[1:]):
        x["title"] = dict(mean=m, d=m - base_title, by_seed=v)
    rows.sort(key=lambda x: (x["title"] is None, -(x["title"] or {}).get("d", 0.0), -x["season_d_ecw"]))
    return dict(k=k, must_add=must_add, drop_pool=pool, n_free=len(free), n_packages=n_pool, shortlist=shortlist, seasons=seasons,
                seeds=list(seeds), base=dict(week_p5=b5, ecw=becw, title=base_title), rows=rows, label=LABEL)


def _pct(x):
    return f"{100 * x:.1f}%"


def render(rec, top=12):
    L = [f"## Package scan — {rec.get('date')}", "",
         f"{rec['n_packages']} packages scored ({rec['n_free']} free agents; drops from {', '.join(rec['drop_pool'])})"
         + (f"; every package includes {rec['must_add']}" if rec.get("must_add") else "") + ".",
         f"No move: {_pct(rec['base']['week_p5'])} to win this week, title {rec['base']['title']:.1f}%.", "",
         "| add | drop | win this week | title, vs no move | week rank | note |", "|---|---|---|---|---|---|"]
    shown = [x for x in rec["rows"] if x["title"]][:top]
    shown += [x for x in rec["rows"] if x.get("named") and x not in shown]
    for x in shown:
        notes = (["your package"] if x.get("named") else []) + \
                ([f"{x['first_cut']['player']} would be the next cut when {x['first_cut']['when']} returns"
                  + (f" (ESPN: {x['first_cut']['return_date']})" if x["first_cut"].get("return_date") else "")] if x["first_cut"] else [])
        L.append(f"| {' + '.join(x['adds'])} | {' + '.join(x['drops'])} | {_pct(x['week']['p5'])} ({100 * x['week']['d_p5']:+.1f}) | "
                 + (f"{x['title']['d']:+.1f}" if x["title"] else "not simulated") + f" | {x['rank_week']} of {len(rec['rows'])} | {'; '.join(notes)} |")
    return L + ["", rec["label"]]


def pass_line(rec, out):
    best = next((x for x in rec["rows"] if x["title"]), None)
    lead = (f"; best for the title: {' + '.join(best['adds'])} for {' + '.join(best['drops'])} ({best['title']['d']:+.1f}, "
            f"{_pct(best['week']['p5'])} this week)") if best else ""
    return f"PACKAGE SCAN: PASS — {rec.get('date')}: {rec['n_packages']} packages{lead}; wrote {out}"


def main(argv=None):
    import co_gm as CG
    import week_matchup as WM
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", required=True)
    ap.add_argument("--k", type=int, choices=(1, 2), default=2, help="moves per package")
    ap.add_argument("--must-add"); ap.add_argument("--named", action="append", default=[], help="'A+B/C+D'; repeatable")
    ap.add_argument("--drop-pool", type=int, default=DROP_POOL); ap.add_argument("--shortlist", type=int, default=SHORTLIST)
    ap.add_argument("--seasons", type=int, default=10000); ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--yahoo-pull", help="a Flaim pull to read rosters, totals and free agents from (default: the day's)")
    ap.add_argument("--from-today", action="store_true", help="count the moves in the day's own games (default: from "
                                                              "tomorrow, as the decision card counts a pair)")
    ap.add_argument("--status-file"); ap.add_argument("--out-dir", default=WM.OUTDIR)
    a = ap.parse_args(argv)
    try:
        named = [parse_named(t) for t in a.named]
        paths = WM.default_paths(a.date)
        if a.yahoo_pull:
            paths["yahoo_pull"] = a.yahoo_pull
        if a.status_file:
            paths["status_file"] = a.status_file
        cap = {}
        WM.build(a.date, paths, capture=cap)
        if not cap.get("fas"):
            raise PackageError("no free-agent list for the day (the week card scored none)")
        _, by = CG.load_pool()
        with open(paths["state"], encoding="utf-8") as f:
            state = json.load(f)
        rosters = CG.rosters(state, by)
        cv = CG.arena.SEASON_CV
        opp = [CG.arena.team_week_model(r, cv) for s, r in rosters.items() if s != CG.OWNER_SEAT]
        wk = {r["player"]: r for r in cap["mine"] + cap["fas"]}

        # as the decision card counts a pair: the day's own games on the roster as it stands, the moves from tomorrow;
        # --from-today counts the moves in the day's games too (a free agent added before tip-off)
        now_s, rest = ({}, cap["sched"]) if a.from_today else WM._split(cap["sched"], a.date)
        r_today = WM.remaining(cap["mine"], now_s, cap["avail"], cap["lines"])

        def week_fn(names):
            rem = WM._both(r_today, WM.remaining([wk[n] for n in names], rest, cap["avail"], cap["lines"]))
            ch = WM.cat_chances(cap["me_now"], rem, cap["opp_now"], cap["opp_rem"])
            return WM.win_week_chance([ch[c] for c in WM.CATS]), sum(ch[c] for c in WM.CATS)

        def ecw_fn(names):
            return CG.pwins(CG.arena.team_week_model([by[n] for n in names if n in by], cv), opp)
        ilp = os.path.join(CG.KIT, "report", "il_return", f"il_return_{a.date}.json")
        il = json.load(open(ilp, encoding="utf-8"))["il_players"] if os.path.exists(ilp) else []
        rec = scan(cap["mine"], cap["fas"], by, cap["avail"], rosters, a.k, a.must_add, a.drop_pool, a.shortlist, named, a.seasons,
                   CG.run_league_sim, tempfile.mkdtemp(), week_fn, ecw_fn, il=il,
                   value=lambda p: CG.hoops.adj_value(p, ()), workers=a.workers)
    except (PackageError, FileNotFoundError, KeyError) as e:
        print(f"PACKAGE SCAN: HALT — {e}"); return 1
    rec["moves_count_from"] = "today" if a.from_today else "tomorrow"
    rec["label"] = LABEL.replace("moves counted from the day's games on", f"moves counted from {rec['moves_count_from']}")
    rec.update(date=a.date, inputs=dict(yahoo_pull=os.path.basename(paths.get("yahoo_pull") or ""), state_as_of=state.get("as_of"),
                                        pool=os.environ.get("SEASON_POOL"), il_return=bool(il)))
    out = os.path.join(a.out_dir, f"package_scan_{a.date}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False); f.write("\n")
    with open(out[:-5] + ".md", "w", encoding="utf-8") as f:
        f.write("\n".join(render(rec)) + "\n")
    print("\n".join(render(rec)))
    print(pass_line(rec, os.path.relpath(out, CG.KIT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
