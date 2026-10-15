#!/usr/bin/env python3
"""Weekly preview and the calibration ledger (Session 1 item 7; plan 2026-10-15 §4 B6, §6 E2).

Preview: the owner against the week's real opponent (data/league_schedule.json), category by
category, on the league state's non-IL rosters and the v69 lines: each side's expected weekly
line from arena.team_week_model, and 10,000 simulated matchups per seed (2026, 2027) with the
house simulator's weekly draw (the method of the 2026-10-15 owner assessment,
h2h_assessment.py, lifted here). Status tiers are not applied to the weekly model yet.

Ledger: report/calibration.json holds each week's prediction, recorded BEFORE the week starts
and append-only (a recorded week cannot be rewritten — the only non-circular grade must not be
editable after the fact). `--score WEEK --won CAT,CAT,...` adds the result and its Brier scores;
report/calibration.md is regenerated from the JSON.

    python3 scripts/weekly_preview.py --week 1 [--record]
    python3 scripts/weekly_preview.py --score 1 --won "FG%,FT%,BLK,TO,ST"
"""
import argparse
import datetime
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import co_gm as CG  # noqa: E402

LEDGER = os.path.join(CG.KIT, "report", "calibration.json")
LEDGER_MD = os.path.join(CG.KIT, "report", "calibration.md")
PREVIEWS = os.path.join(CG.KIT, "report", "previews")
SEEDS = (2026, 2027)


class LedgerError(Exception):
    pass


def simulate(models, sig, a, b, n, seed):
    rng = random.Random(seed)
    counting = set(CG.hoops.COUNT_COLS)
    wins = cats = 0
    per = {c: 0 for c in CG.CATS}
    for _ in range(n):
        sa, sb = rng.gauss(1, CG.arena.TEAM_WEEK_SHOCK), rng.gauss(1, CG.arena.TEAM_WEEK_SHOCK)
        k = 0
        for c in CG.CATS:
            ma = models[a][0][c] * (sa if c in counting else 1)
            mb = models[b][0][c] * (sb if c in counting else 1)
            xa, xb = rng.gauss(ma, sig[a][c]), rng.gauss(mb, sig[b][c])
            w = xa < xb if c == "TO" else xa > xb
            per[c] += w
            k += w
        cats += k
        wins += k >= 5
    return {"p_win": wins / n, "exp_cats": cats / n, "cat_p": {c: per[c] / n for c in CG.CATS}}


def preview(week, n=10000):
    state = json.load(open(CG.STATE, encoding="utf-8"))
    sched = json.load(open(CG.SCHEDULE, encoding="utf-8"))
    o = next(x for x in sched["owner_opponents"] if x["week"] == week)
    P, by = CG.load_pool()
    ros = CG.rosters(state, by)
    models = {s: CG.arena.team_week_model(r) for s, r in ros.items()}
    sig = {s: {c: math.sqrt(models[s][1][c]) or 1e-6 for c in CG.CATS} for s in ros}
    runs = {s: simulate(models, sig, CG.OWNER_SEAT, o["seat"], n, s * 100 + week) for s in SEEDS}
    mean = {"p_win": sum(r["p_win"] for r in runs.values()) / 2,
            "exp_cats": sum(r["exp_cats"] for r in runs.values()) / 2,
            "cat_p": {c: sum(r["cat_p"][c] for r in runs.values()) / 2 for c in CG.CATS}}
    team = {t["seat"]: t["name"] for t in state["teams"]}
    return {"week": week, "opponent_seat": o["seat"], "opponent_manager": o["manager"], "opponent_team": team[o["seat"]],
            "rosters_as_of": state["as_of"], "lines": CG.LINES_TAG, "n_per_seed": n, "seeds": list(SEEDS),
            "by_seed": {str(s): r for s, r in runs.items()}, **mean,
            "means": {"owner": {c: models[CG.OWNER_SEAT][0][c] for c in CG.CATS},
                      "opponent": {c: models[o["seat"]][0][c] for c in CG.CATS}}}


def record(path, pred, recorded_at, week_start):
    if recorded_at[:10] >= week_start:
        raise LedgerError(f"week {pred['week']} starts {week_start}; a prediction recorded {recorded_at} is too late")
    led = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {"weeks": {}}
    key = str(pred["week"])
    if key in led["weeks"]:
        raise LedgerError(f"week {key} is already recorded ({led['weeks'][key]['recorded_at']}); the ledger is append-only")
    led["weeks"][key] = dict(pred, recorded_at=recorded_at, week_start=week_start)
    json.dump(led, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return led


def score(pred, actual):
    won = set(actual["won"])
    bc = sum((pred["cat_p"][c] - (1.0 if c in won else 0.0)) ** 2 for c in pred["cat_p"]) / len(pred["cat_p"])
    bm = (pred["p_win"] - (1.0 if len(won) >= 5 else 0.0)) ** 2
    return {"won": sorted(won), "cats_won": len(won), "brier_cats": bc, "brier_matchup": bm}


def render_ledger(led):
    L = ["# Calibration ledger", "",
         "Each week's prediction is recorded before the week starts and cannot be rewritten "
         "(`scripts/weekly_preview.py`; `report/calibration.json` is the record). Brier: 0 is perfect, "
         "0.25 is a coin flip's score.", "",
         "| week | opponent | recorded | P(win) | expected cats | result | cats won | Brier (cats) | Brier (matchup) |",
         "|---|---|---|---|---|---|---|---|---|"]
    for k in sorted(led["weeks"], key=int):
        w = led["weeks"][k]
        s = w.get("score")
        L.append(f"| {k} | {w['opponent_team']} ({w['opponent_manager']}) | {w['recorded_at']} | {w['p_win']:.3f} | "
                 f"{w['exp_cats']:.2f} | {('W' if s['cats_won'] >= 5 else 'L') if s else 'pending'} | "
                 f"{s['cats_won'] if s else '—'} | {f'{s[chr(98)+"rier_cats"]:.3f}' if s else '—'} | "
                 f"{f'{s[chr(98)+"rier_matchup"]:.3f}' if s else '—'} |")
    return "\n".join(L) + "\n"


def render_preview(p, week_start, week_end):
    L = [f"# Week {p['week']} preview — vs {p['opponent_team']} ({p['opponent_manager']}), {week_start} to {week_end}", "",
         f"P(win the week): **{p['p_win']:.1%}** (seeds {SEEDS[0]} / {SEEDS[1]}: "
         f"{p['by_seed'][str(SEEDS[0])]['p_win']:.3f} / {p['by_seed'][str(SEEDS[1])]['p_win']:.3f}; "
         f"±{196 * math.sqrt(p['p_win'] * (1 - p['p_win']) / (2 * p['n_per_seed'])):.1f} points). "
         f"Expected categories: {p['exp_cats']:.2f} of 9.", "",
         "| category | you (weekly mean) | them | P(you win) |", "|---|---|---|---|"]
    for c in CG.CATS:
        f = (lambda v: f"{v:.3f}") if "%" in c else (lambda v: f"{v:.1f}")
        L.append(f"| {c} | {f(p['means']['owner'][c])} | {f(p['means']['opponent'][c])} | {p['cat_p'][c]:.0%} |")
    L += ["", f"_Rosters as of {p['rosters_as_of']}; lines {p['lines']}; Q/O statuses not applied to the weekly model; "
          "a two-week matchup (weeks 7, 17) is modelled as one week._"]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", type=int)
    ap.add_argument("--record", action="store_true")
    ap.add_argument("--score", type=int)
    ap.add_argument("--won", default="")
    ap.add_argument("--n", type=int, default=10000)
    a = ap.parse_args()
    if a.score:
        led = json.load(open(LEDGER, encoding="utf-8"))
        w = led["weeks"][str(a.score)]
        if "score" in w:
            raise LedgerError(f"week {a.score} is already scored")
        w["score"] = score(w, {"won": [c.strip() for c in a.won.split(",") if c.strip()]})
        json.dump(led, open(LEDGER, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        open(LEDGER_MD, "w", encoding="utf-8").write(render_ledger(led))
        print(f"scored week {a.score}: {w['score']}")
        return
    wk, ws, we = None, None, None
    import importlib.util
    spec = importlib.util.spec_from_file_location("bs", os.path.join(CG.KIT, "report", "schedule", "build_schedule.py"))
    bs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bs)
    for n, s, e in bs.weeks():
        if n == a.week:
            ws, we = s.isoformat(), e.isoformat()
    p = preview(a.week, a.n)
    os.makedirs(PREVIEWS, exist_ok=True)
    md = os.path.join(PREVIEWS, f"week_{a.week:02d}.md")
    open(md, "w", encoding="utf-8").write(render_preview(p, ws, we))
    print(f"wrote {os.path.relpath(md, CG.KIT)}")
    if a.record:
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        led = record(LEDGER, {k: v for k, v in p.items() if k != "means"}, now, ws)
        open(LEDGER_MD, "w", encoding="utf-8").write(render_ledger(led))
        print(f"recorded week {a.week} in {os.path.relpath(LEDGER, CG.KIT)} at {now} (week starts {ws})")


if __name__ == "__main__":
    main()
