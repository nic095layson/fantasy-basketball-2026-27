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
# owner 2026-10-27 (the weekly accuracy card): every matchup's pre-week forecast, and the in-season lines it rests on
LEAGUE = os.path.join(CG.KIT, "report", "calibration_league.json")
# owner 2026-10-27 (build 5, first slice): the same forecast on each NBA team's real games that week, candidate only
LEAGUE_REAL = os.path.join(CG.KIT, "report", "calibration_league_real.json")
SNAPSHOTS = os.path.join(CG.KIT, "report", "accuracy")
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
    # 2026-10-22 (week 2): only the two teams in the matchup are modelled; a player without a line on a third team
    # (Drummond, seat 9, D-DR-1) stopped the record, one on either side of the matchup stops it by name
    seats = (CG.OWNER_SEAT, o["seat"])
    unlined = sorted(p["player"] for t in state["teams"] if t["seat"] in seats for p in t["players"]
                     if p["slot"] != "IL" and p["player"] not in by)
    if unlined:
        raise LedgerError(f"week {week}: no {CG.LINES_TAG} line for {', '.join(unlined)} in the matchup")
    ros = CG.rosters(dict(state, teams=[t for t in state["teams"] if t["seat"] in seats]), by)
    models = {s: CG.arena.team_week_model(r, CG.arena.SEASON_CV) for s, r in ros.items()}  # D-ZS-3: the season CV
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


def record(path, pred, recorded_at, week_start, if_absent=False):
    """if_absent (owner 2026-10-27, the Sunday step): a week already recorded returns None instead of an error; the
    record is never rewritten either way."""
    if recorded_at[:10] >= week_start:
        raise LedgerError(f"week {pred['week']} starts {week_start}; a prediction recorded {recorded_at} is too late")
    led = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {"weeks": {}}
    key = str(pred["week"])
    if key in led["weeks"]:
        if if_absent:
            return None
        raise LedgerError(f"week {key} is already recorded ({led['weeks'][key]['recorded_at']}); the ledger is append-only")
    led["weeks"][key] = dict(pred, recorded_at=recorded_at, week_start=week_start)
    json.dump(led, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return led


def score(pred, actual):
    won = set(actual["won"])
    bc = sum((pred["cat_p"][c] - (1.0 if c in won else 0.0)) ** 2 for c in pred["cat_p"]) / len(pred["cat_p"])
    bm = (pred["p_win"] - (1.0 if len(won) >= 5 else 0.0)) ** 2
    return {"won": sorted(won), "cats_won": len(won), "brier_cats": bc, "brier_matchup": bm}


def record_league(path, week, pairs, recorded_at, week_start, method=None):
    """Every matchup's pre-week forecast for the week, recorded before it starts (append-only). Returns False, and
    rewrites nothing, when the week is already recorded."""
    if recorded_at[:10] >= week_start:
        raise LedgerError(f"week {week} starts {week_start}; a league forecast recorded {recorded_at} is too late")
    led = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {"weeks": {}}
    if str(week) in led["weeks"]:
        return False
    led["weeks"][str(week)] = dict(pairs=pairs, recorded_at=recorded_at, week_start=week_start,
                                   method=method or "weekly_preview.simulate on team_week_model (season CV), seeds 2026/2027; p_win is seat a's")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(led, f, indent=1, ensure_ascii=False); f.write("\n")
    return True


def preview_league(week, n=10000, real_games=False):
    """Every pairing of the week from the real schedule (data/league_schedule.json pairings), each as the owner's own
    preview models it. A pair with a rostered player the pool has no line for is skipped and named. real_games
    (owner 2026-10-27, build 5): the week model on each NBA team's real games in the window (real_games.py) instead
    of the flat 3.5; the record names any NBA code the schedule lacked."""
    state = json.load(open(CG.STATE, encoding="utf-8"))
    sched = json.load(open(CG.SCHEDULE, encoding="utf-8"))
    pairs = (sched.get("pairings") or {}).get(str(week))
    if not pairs:
        raise LedgerError(f"week {week}: no pairings in {CG.SCHEDULE}")
    P, by = CG.load_pool()
    games = None
    if real_games:
        import real_games as RG
        games = RG.week_games(week)
    out, skipped, unscheduled = [], [], set()
    for a, b in pairs:
        unlined = sorted(p["player"] for t in state["teams"] if t["seat"] in (a, b) for p in t["players"]
                         if p["slot"] != "IL" and p["player"] not in by)
        if unlined:
            skipped.append(dict(a=a, b=b, unlined=unlined)); continue
        ros = CG.rosters(dict(state, teams=[t for t in state["teams"] if t["seat"] in (a, b)]), by)
        if games is not None:
            import real_games as RG
            models = {}
            for s_, r in ros.items():
                mu, var, un = RG.team_week_model_games(r, CG.arena.SEASON_CV, games, report=True)
                models[s_] = (mu, var); unscheduled.update(un)
        else:
            models = {s: CG.arena.team_week_model(r, CG.arena.SEASON_CV) for s, r in ros.items()}
        sig = {s: {c: math.sqrt(models[s][1][c]) or 1e-6 for c in CG.CATS} for s in ros}
        runs = [simulate(models, sig, a, b, n, s * 100 + week * 13 + a) for s in SEEDS]
        out.append(dict(a=a, b=b, p_win=sum(r["p_win"] for r in runs) / len(runs), exp_cats=sum(r["exp_cats"] for r in runs) / len(runs),
                        cat_p={c: sum(r["cat_p"][c] for r in runs) / len(runs) for c in CG.CATS}))
    if real_games and unscheduled:
        for o in out:
            o["unscheduled_teams"] = sorted(unscheduled)
    return out, skipped, state.get("as_of")


def snapshot(week, src=None, dst_dir=SNAPSHOTS, state=None, status=None):
    """The in-season lines the week's forecasts rest on, copied before the week, and beside them the minutes-trend
    candidate pool (pool_season_mt.csv next to the live pool; owner 2026-10-27, build 2) when it exists. Nothing is
    overwritten. Returns the paths written."""
    import shutil
    src = src or os.environ.get("SEASON_POOL")
    if not src:
        raise LedgerError("no SEASON_POOL to snapshot")
    pairs = [(src, os.path.join(dst_dir, f"lines_week{week}.csv"))]
    mt = os.path.join(os.path.dirname(src), "pool_season_mt.csv")
    if os.path.exists(mt):
        pairs.append((mt, os.path.join(dst_dir, f"lines_week{week}_mt.csv")))
    # owner 2026-10-27 (build 3): the rosters and the day's status file the week's forecasts rest on, for the Monday fit
    for extra, name in ((state, f"state_week{week}.json"), (status, f"status_week{week}.json")):
        if extra and os.path.exists(extra):
            pairs.append((extra, os.path.join(dst_dir, name)))
    written = []
    os.makedirs(dst_dir, exist_ok=True)
    for a, b in pairs:
        if os.path.exists(b):
            continue
        shutil.copyfile(a, b); written.append(b)
    return written


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
                 f"{s['cats_won'] if s else '—'} | {('%.3f' % s['brier_cats']) if s else '—'} | "
                 f"{('%.3f' % s['brier_matchup']) if s else '—'} |")
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
    ap.add_argument("--league", action="store_true", help="with --record: also every matchup (report/calibration_league.json); "
                                                           "a week already recorded is reported, not an error (owner 2026-10-27)")
    ap.add_argument("--snapshot", action="store_true", help="copy SEASON_POOL to report/accuracy/lines_week<N>.csv")
    ap.add_argument("--score", type=int)
    ap.add_argument("--won", default="")
    ap.add_argument("--n", type=int, default=10000)
    ap.add_argument("--ledger", default=LEDGER, help="calibration ledger path (tests pass a scratch file; owner 2026-10-24)")
    a = ap.parse_args()
    if a.score:
        led = json.load(open(a.ledger, encoding="utf-8"))
        w = led["weeks"][str(a.score)]
        if "score" in w:
            raise LedgerError(f"week {a.score} is already scored")
        w["score"] = score(w, {"won": [c.strip() for c in a.won.split(",") if c.strip()]})
        json.dump(led, open(a.ledger, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        open(LEDGER_MD if a.ledger == LEDGER else a.ledger[:-5] + ".md", "w", encoding="utf-8").write(render_ledger(led))
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
        led = record(LEDGER, {k: v for k, v in p.items() if k != "means"}, now, ws, if_absent=a.league)
        if led is None:
            print(f"week {a.week} already recorded in {os.path.relpath(LEDGER, CG.KIT)}; not rewritten")
        else:
            open(LEDGER_MD, "w", encoding="utf-8").write(render_ledger(led))
            print(f"recorded week {a.week} in {os.path.relpath(LEDGER, CG.KIT)} at {now} (week starts {ws})")
        if a.league:
            pairs, skipped, as_of = preview_league(a.week, a.n)
            new = record_league(LEAGUE, a.week, pairs, now, ws)
            print(f"league: {len(pairs)} matchup(s) " + ("recorded" if new else "already recorded; not rewritten")
                  + (f"; skipped {skipped}" if skipped else "") + f" (rosters as of {as_of})")
            # build 5, first slice: the same forecast on each NBA team's real games, its own ledger, candidate only
            pairs_r, skipped_r, _ = preview_league(a.week, a.n, real_games=True)
            new_r = record_league(LEAGUE_REAL, a.week, pairs_r, now, ws,
                                  method="weekly_preview.simulate on real_games.team_week_model_games (each NBA team's games in the window x availability; season CV), seeds 2026/2027; p_win is seat a's")
            print(f"league (real games): {len(pairs_r)} matchup(s) " + ("recorded" if new_r else "already recorded; not rewritten")
                  + (f"; skipped {skipped_r}" if skipped_r else ""))
    if a.snapshot:
        today = datetime.date.today().isoformat()
        dst = snapshot(a.week, state=CG.STATE, status=os.path.join(CG.KIT, "data", "status", f"status_{today}.json"))
        print("snapshot: " + (", ".join(os.path.relpath(d, CG.KIT) for d in dst) if dst else f"lines_week{a.week}.csv already exists; not overwritten"))
    if a.record or a.snapshot:
        print(f"WEEKLY PREVIEW: PASS — week {a.week}")


if __name__ == "__main__":
    main()
