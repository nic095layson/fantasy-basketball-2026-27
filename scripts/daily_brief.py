#!/usr/bin/env python3
"""The daily brief (Session 1 item 6; plan 2026-10-15 §6 E1): one short markdown note for a date.

Reads only records: data/league_state.json (rosters, Yahoo eligibility), the newest
data/status/status_*.json (availability tiers with receipts), report/schedule/games-2026-27.csv
(the NBA schedule), the v69 lines, data/league_schedule.json (the owner's opponents).

Sections: the owner's players with games; the lineup by the daily-fill rule; the waiver scan
(co_gm.waiver_pairs, lifted from waiver_moves.py, against the league state; the top 3 pairs
checked in the league simulator on the real schedule); streaming candidates by games left
this week; title odds on the real schedule (the average of two seeded runs, the error stated).

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


SWEEP = os.path.join(CG.KIT, "report", "after-reports", "redteam-2026-10-19", "sweep.json")


def band_line(path=SWEEP):
    """The structural band every title figure carries (post-mortem 2026-10-19 D-PM-6, D-RT-2): each FRAGILE constant
    of the standing sweep with its shifts, read from the record, never typed."""
    try:
        with open(path, encoding="utf-8") as f:
            sw = json.load(f)
    except (OSError, ValueError):
        return "Structural band: no sweep record found (scripts/redteam/sweep.py writes it)."
    parts = []
    for key in sw.get("fragile", []):
        c = sw["constants"][key]
        parts.append(f"{key.split('.')[-1]} is FRAGILE: " + " / ".join(f"{v['shift_mean']:+.1f} ({v['label']})" for v in c["variants"]))
    return "Structural band (standing sweep, deck " + str(sw.get("engine_commit", "?")) + "): " + ("; ".join(parts) if parts else "no FRAGILE constant") + "."


def odds_line(a, b, n):
    m = (a + b) / 2
    e = 196 * math.sqrt(m / 100 * (1 - m / 100) / (2 * n))
    # owner 2026-10-20: one averaged figure; the per-run values stay in the JSON record
    return f"{m:.1f}% ± {e:.1f} (avg of 2 runs × {n:,} seasons)"


def newest_status(date):
    # the newest file dated on or before the brief: a later-dated file (a test run of tomorrow) must not shadow today's
    files = sorted(f for f in glob.glob(os.path.join(CG.KIT, "data", "status", "status_*.json"))
                   if os.path.basename(f)[len("status_"):-len(".json")] <= date)
    return (json.load(open(files[-1], encoding="utf-8")), os.path.basename(files[-1])) if files else ({"rows": []}, None)


def trades_for(date):
    """The trade-finder record for the brief's date (scripts/trade_finder.py; owner 2026-10-20 item 1), or None."""
    path = os.path.join(CG.KIT, "data", "news", f"trades_{date}.json")
    return json.load(open(path, encoding="utf-8")) if os.path.exists(path) else None


def trades_lines(rec):
    if rec is None:
        return ["No trade-finder record for the date (scripts/trade_finder.py writes it)."]
    if not rec["trades"]:
        return [f"{rec['pairs_swept']:,} one-for-one pairs swept: none raises my expected category wins "
                "without lowering the other side's. Stand pat."]
    out = [f"{rec['pairs_swept']:,} one-for-one pairs swept on the live rosters; {rec['proposable']} proposable "
           "(my cats/week up, theirs not down — the engine's acceptability proxy, not their judgment). Top:"]
    for t in rec["trades"][:3]:
        line = (f"- Send **{t['i_send']}** to {t.get('team') or t['seat']} for **{t['i_get']}**: "
                f"{t['d_ecw_me']:+.3f} cats/wk me, {t['d_ecw_them']:+.3f} them")
        if t.get("title") is not None:
            line += f"; title {t['title']:.1f}% ({t['d_title']:+.1f})"
        out.append(line)
    return out


def league_moves_for(date):
    """The league-moves record for the brief's date (scripts/league_moves.py; owner 2026-10-20 item 2), or None."""
    path = os.path.join(CG.KIT, "data", "news", f"league_moves_{date}.json")
    return json.load(open(path, encoding="utf-8")) if os.path.exists(path) else None


def league_moves_lines(rec, my_team):
    """Adds, drops and IL moves per fantasy team since the previous league state."""
    if rec is None:
        return ["No league-moves record for the date (the live pull did not run or had nothing to compare)."]
    if not rec["moves"]:
        return [f"No roster changed, {rec['old_as_of']} to {rec['new_as_of']}."]
    out = [f"Rosters {rec['old_as_of']} to {rec['new_as_of']}:"]
    for m in sorted(rec["moves"], key=lambda m: (m["team"] != my_team, m["team"])):
        who = f"**{m['team']}** (yours)" if m["team"] == my_team else f"**{m['team']}**"
        bits = ([f"added {', '.join(m['added'])}"] if m["added"] else []) \
            + ([f"dropped {', '.join(m['dropped'])}"] if m["dropped"] else []) \
            + ([f"to IL: {', '.join(m['to_il'])}"] if m["to_il"] else []) \
            + ([f"off IL: {', '.join(m['from_il'])}"] if m["from_il"] else [])
        out.append(f"- {who} — {'; '.join(bits)}")
    return out


def transactions_for(date):
    """The transactions record for the brief's date (scripts/transactions.py; owner 2026-10-20), or None."""
    path = os.path.join(CG.KIT, "data", "news", f"transactions_{date}.json")
    return json.load(open(path, encoding="utf-8")) if os.path.exists(path) else None


def transactions_lines(rec, my_team, opp_team):
    """Rostered players first (yours, then this week's opponent, then the league), then board players on no roster."""
    if rec is None:
        return ["Not read this morning (no transactions record for the date)."]
    if not rec["source"].get("ok"):
        return [f"ESPN's transactions feed was NOT read ({rec['source'].get('detail')}); waivers and signings unseen."]
    start, end = rec["window"]
    head = f"ESPN transactions feed, {start} to {end}: {rec['items_in_window']} moves, {len(rec['hits'])} naming a board player."
    rank = lambda h: (0 if h["fantasy_team"] == my_team else 1 if h["fantasy_team"] == opp_team else 2 if h["fantasy_team"] else 3, h["date"])
    out = [head]
    for h in sorted(rec["hits"], key=rank):
        who = ("yours" if h["fantasy_team"] == my_team else f"{h['fantasy_team']}, your opponent this week" if h["fantasy_team"] == opp_team
               else h["fantasy_team"] or "on no roster")
        out.append(f"- **{h['player']}** ({who}) — {h['nba_team']} {h['date']}: {h['description']}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--seasons", type=int, default=10000)
    a = ap.parse_args()
    state = json.load(open(CG.STATE, encoding="utf-8"))
    sched = json.load(open(CG.SCHEDULE, encoding="utf-8"))
    status, status_file = newest_status(a.date)
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
        # owner 2026-10-20: the waiver check runs both seeds, so its title figure is the same two-run average
        t = {s: CG.run_league_sim(r2, s, a.seasons, work, tag="w")["teams"][str(CG.OWNER_SEAT)]["champ"] for s in SEEDS}
        x["title_by_seed"] = {str(s): round(t[s], 2) for s in SEEDS}
        x["title"] = round(sum(t.values()) / len(SEEDS), 2)
        x["d_title"] = round(x["title"] - sum(base[s]["champ"] for s in SEEDS) / len(SEEDS), 2)

    # 4. streaming: free agents by per-game board value x games left this week
    weakest = min((p for p in ros[CG.OWNER_SEAT]), key=lambda p: CG.hoops.adj_value(p, ()))
    weak_games = left.get(next(x["yahoo_nba_team"] for x in me["players"] if x["player"] == weakest["player"]), 0)
    stream = CG.streaming([{"player": p["player"], "team": p["team"], "games_left": left.get(p["team"], 0),
                            "value_per_game": round(CG.hoops.adj_value(p, ()), 2)} for p in fa], weak_games)

    tx = transactions_for(a.date)

    lm = league_moves_for(a.date)
    tf = trades_for(a.date)
    rec = {"date": a.date, "week": wk, "week_window": [wstart, wend], "league_state_as_of": state["as_of"],
           "status_file": status_file, "lines": CG.LINES_TAG, "opponent": opp_team["name"] if opp_team else None,
           "today": rows_today, "lineup": lineup, "bench": bench, "waiver_base_ecw": round(base_ecw, 4),
           "waiver_positive_pairs": len(pos), "waiver_pairs_scored": len(pairs), "waiver_top": top, "streaming": stream,
           "streaming_vs": {"player": weakest["player"], "games_left": weak_games,
                            "value_per_game": round(CG.hoops.adj_value(weakest, ()), 2)},
           "title": {str(s): base[s]["champ"] for s in SEEDS}, "playoffs": {str(s): base[s]["playoff"] for s in SEEDS},
           "seasons": a.seasons, "transactions": tx and {"window": tx["window"], "ok": tx["source"].get("ok"), "hits": tx["hits"]},
           "league_moves": lm and lm["moves"],
           "trade_finder": tf and {"pairs_swept": tf["pairs_swept"], "proposable": tf["proposable"], "trades": tf["trades"][:3]}}
    os.makedirs(OUTDIR, exist_ok=True)
    json.dump(rec, open(os.path.join(OUTDIR, f"brief_{a.date}.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    L = [f"# Daily brief — {a.date} (week {wk}, {wstart} to {wend})", ""]
    L.append(f"Opponent this week: **{rec['opponent']}**. Rosters as of {state['as_of']} "
             f"({'FantasyBot live pull' if 'fantasybot' in (state.get('sources') or {}) else chr(39).join(['owner', 's Yahoo page'])}); "
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
    L += ["", "## League moves", ""] + league_moves_lines(lm, me["name"])
    L += ["", "## Transactions", ""] + transactions_lines(tx, me["name"], rec["opponent"])
    L += ["", "## Trades worth proposing", ""] + trades_lines(tf)
    L += ["", "## Waiver scan", ""]
    if top:
        L.append(f"{len(pos)} of {len(pairs)} add/drop pairs raise expected weekly category wins (base {base_ecw:.3f}). "
                 f"Best three, checked in the simulator (avg of 2 runs × {a.seasons:,} seasons, real schedule):")
        L += [f"- Add **{x['add']}** ({x['add_team']}), drop {x['drop']}: {x['d_ecw']:+.3f} cats/week; "
              f"title {x['title']:.1f}% ({x['d_title']:+.1f})" for x in top]
    else:
        L.append(f"No add/drop pair raises expected weekly category wins ({len(pairs)} scored). Stand pat.")
    L += ["", f"## Streaming ({a.date} to {wend})", "",
          f"Your weakest active player by board value is {weakest['player']} "
          f"({rec['streaming_vs']['value_per_game']:+.2f} per game, {weak_games} games left). "
          f"Free agents with more games left, best per game first:"]
    L += [f"- {r['player']} ({r['team']}): {r['games_left']} games, {r['value_per_game']:+.2f} per game" for r in stream] or ["- none"]
    L += ["", "## Title odds (real schedule)", "", f"- Title: {odds_line(base[SEEDS[0]]['champ'], base[SEEDS[1]]['champ'], a.seasons)}",
          f"- Playoffs: {(base[SEEDS[0]]['playoff'] + base[SEEDS[1]]['playoff']) / 2:.1f}%",
          f"- {band_line()}", "",
          "_Cannot see: news after the morning FantasyBot pull (or the last paste) beyond ESPN's transactions feed; ESPN injuries (network-denied); minutes limits; "
          "other managers' pending claims. Q counts as a coin flip._"]
    path = os.path.join(OUTDIR, f"brief_{a.date}.md")
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"wrote {os.path.relpath(path, CG.KIT)}")


if __name__ == "__main__":
    main()
