#!/usr/bin/env python3
"""The daily brief (Session 1 item 6; plan 2026-10-15 §6 E1): one short markdown note for a date.

Reads only records: data/league_state.json (rosters, Yahoo eligibility), the newest
data/status/status_*.json (availability tiers with receipts), report/schedule/games-2026-27.csv
(the NBA schedule), the v69 lines, data/league_schedule.json (the owner's opponents).

Sections: the owner's players with games; the lineup by the daily-fill rule; the waiver scan
(co_gm.waiver_pairs, lifted from waiver_moves.py, against the league state; the top 3 pairs
checked in the league simulator on the real schedule); streaming candidates by games left
this week; title odds on the real schedule (two seeds, the error stated).

    python3 scripts/daily_brief.py --date 2026-10-21 [--seasons 10000]
Writes report/briefs/brief_<date>.md and brief_<date>.json (the numbers behind the note).
"""
import argparse
import glob
import json
import math
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import co_gm as CG  # noqa: E402

OUTDIR = os.path.join(CG.KIT, "report", "briefs")
SEEDS = (2026, 2027)


def odds_line(a, b, n):
    m = (a + b) / 2
    e = 196 * math.sqrt(m / 100 * (1 - m / 100) / (2 * n))
    return f"{m:.1f}% ± {e:.1f} (seeds {SEEDS[0]} / {SEEDS[1]}: {a:.2f}% / {b:.2f}%; {n:,} seasons each)"


def newest_status():
    files = sorted(glob.glob(os.path.join(CG.KIT, "data", "status", "status_*.json")))
    return (json.load(open(files[-1], encoding="utf-8")), os.path.basename(files[-1])) if files else ({"rows": []}, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--seasons", type=int, default=10000)
    a = ap.parse_args()
    state = json.load(open(CG.STATE, encoding="utf-8"))
    sched = json.load(open(CG.SCHEDULE, encoding="utf-8"))
    status, status_file = newest_status()
    avail = {r["player"]: r for r in status["rows"]}
    P, by = CG.load_pool()
    ros = CG.rosters(state, by)
    games = CG.load_games()
    wk, wstart, wend = CG.week_of(a.date)
    today = {}
    for d, v, h in games:
        if d == a.date:
            v, h = CG.TEAM_CODE.get(v, v), CG.TEAM_CODE.get(h, h)
            today[v] = f"@ {h}"
            today[h] = f"vs {v}"
    left = CG.games_left(games, a.date, wend)
    me = next(t for t in state["teams"] if t["seat"] == CG.OWNER_SEAT)
    opp_seat = next((o["seat"] for o in sched["owner_opponents"] if o["week"] == wk), None)
    opp_team = next((t for t in state["teams"] if t["seat"] == opp_seat), None)

    # 1-2. my players today and the lineup
    mine, rows_today = [], []
    for p in me["players"]:
        if p["slot"] == "IL":
            continue
        team = p["yahoo_nba_team"]
        st = avail.get(p["player"])
        av = st["availability"] if st else 1.0
        val = sum(by[p["player"]]["z"][c] for c in CG.CATS)
        g = today.get(team)
        rows_today.append((p["player"], team, g, st["yahoo_status"] if st else None, av, left.get(team, 0)))
        if g:
            mine.append({"player": p["player"], "positions": p["positions"], "value": val, "availability": av})
    lineup, bench = CG.daily_lineup(mine)

    # 3. waiver scan
    fa = CG.free_agents(P, state)
    base_ecw, pairs = CG.waiver_pairs(ros, fa)
    pos = [x for x in pairs if x["d_ecw"] > 0]
    top, seen = [], set()
    for x in pos:
        if x["add"] not in seen:
            seen.add(x["add"])
            top.append(x)
        if len(top) == 3:
            break

    # 5. title odds (and the waiver check) on the real schedule
    work = tempfile.mkdtemp()
    base = {s: CG.run_league_sim(ros, s, a.seasons, work)["teams"][str(CG.OWNER_SEAT)] for s in SEEDS}
    for x in top:
        r2 = {s: list(r) for s, r in ros.items()}
        r2[CG.OWNER_SEAT] = [p for p in r2[CG.OWNER_SEAT] if p["player"] != x["drop"]] + [by[x["add"]]]
        t = CG.run_league_sim(r2, SEEDS[0], a.seasons, work, tag="w")["teams"][str(CG.OWNER_SEAT)]
        x["title_seed2026"] = round(t["champ"], 2)
        x["d_title_seed2026"] = round(t["champ"] - base[SEEDS[0]]["champ"], 2)

    # 4. streaming: free agents by per-game board value x games left this week
    weakest = min((p for p in ros[CG.OWNER_SEAT]), key=lambda p: CG.hoops.adj_value(p, ()))
    weak_games = left.get(next(x["yahoo_nba_team"] for x in me["players"] if x["player"] == weakest["player"]), 0)
    stream = CG.streaming([{"player": p["player"], "team": p["team"], "games_left": left.get(p["team"], 0),
                            "value_per_game": round(CG.hoops.adj_value(p, ()), 2)} for p in fa], weak_games)

    rec = {"date": a.date, "week": wk, "week_window": [wstart, wend], "league_state_as_of": state["as_of"],
           "status_file": status_file, "lines": CG.LINES_TAG, "opponent": opp_team["name"] if opp_team else None,
           "today": rows_today, "lineup": lineup, "bench": bench, "waiver_base_ecw": round(base_ecw, 4),
           "waiver_positive_pairs": len(pos), "waiver_pairs_scored": len(pairs), "waiver_top": top, "streaming": stream,
           "streaming_vs": {"player": weakest["player"], "games_left": weak_games,
                            "value_per_game": round(CG.hoops.adj_value(weakest, ()), 2)},
           "title": {str(s): base[s]["champ"] for s in SEEDS}, "playoffs": {str(s): base[s]["playoff"] for s in SEEDS},
           "seasons": a.seasons}
    os.makedirs(OUTDIR, exist_ok=True)
    json.dump(rec, open(os.path.join(OUTDIR, f"brief_{a.date}.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    L = [f"# Daily brief — {a.date} (week {wk}, {wstart} to {wend})", ""]
    L.append(f"Opponent this week: **{rec['opponent']}**. Rosters as of {state['as_of']} (owner's Yahoo page); "
             f"statuses from `{status_file}`; lines {CG.LINES_TAG}.")
    L += ["", "## Your players today", "", "| player | NBA | game | status | availability | games left this week |", "|---|---|---|---|---|---|"]
    for n, t, g, s, av, gl in rows_today:
        L.append(f"| {n} | {t} | {g or '—'} | {s or '—'} | {av:.2f} | {gl} |")
    L += ["", "## Lineup (daily-fill rule)", ""]
    L += [f"- **{s}** {p}" + (f" — {avail[p]['yahoo_status']}, check before lock" if p in avail else "") for s, p in lineup]
    if bench:
        L.append(f"- Bench (game today, no open slot): {', '.join(bench)}")
    idle = [n for n, t, g, s, av, gl in rows_today if not g]
    if idle:
        L.append(f"- No game today: {', '.join(idle)}")
    L += ["", "## Waiver scan", ""]
    if top:
        L.append(f"{len(pos)} of {len(pairs)} add/drop pairs raise expected weekly category wins (base {base_ecw:.3f}). "
                 f"Best three, checked in the simulator (seed {SEEDS[0]}, {a.seasons:,} seasons, real schedule):")
        L += [f"- Add **{x['add']}** ({x['add_team']}), drop {x['drop']}: {x['d_ecw']:+.3f} cats/week; "
              f"title {x['title_seed2026']:.2f}% ({x['d_title_seed2026']:+.2f} vs {base[SEEDS[0]]['champ']:.2f}%)" for x in top]
    else:
        L.append(f"No add/drop pair raises expected weekly category wins ({len(pairs)} scored). Stand pat.")
    L += ["", f"## Streaming ({a.date} to {wend})", "",
          f"Your weakest active player by board value is {weakest['player']} "
          f"({rec['streaming_vs']['value_per_game']:+.2f} per game, {weak_games} games left). "
          f"Free agents with more games left, best per game first:"]
    L += [f"- {r['player']} ({r['team']}): {r['games_left']} games, {r['value_per_game']:+.2f} per game" for r in stream] or ["- none"]
    L += ["", "## Title odds (real schedule)", "", f"- Title: {odds_line(base[SEEDS[0]]['champ'], base[SEEDS[1]]['champ'], a.seasons)}",
          f"- Playoffs: {(base[SEEDS[0]]['playoff'] + base[SEEDS[1]]['playoff']) / 2:.1f}%", "",
          "_Cannot see: news after the rosters/status paste; ESPN injuries (network-denied); minutes limits; "
          "other managers' pending claims. Q counts as a coin flip._"]
    path = os.path.join(OUTDIR, f"brief_{a.date}.md")
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"wrote {os.path.relpath(path, CG.KIT)}")


if __name__ == "__main__":
    main()
