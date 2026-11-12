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
import datetime
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


# owner 2026-10-26 ("re-measure the uncertainty ranges ... now that they use the updated stats"; "every Monday"): the
# newest season sweep dated on or before the brief's day (sweep_record.latest), named with its date and configuration
import sweep_record as SR  # noqa: E402


def lines_label():
    """Owner 2026-10-26: the lines the brief ran on (co_gm.lines_label, shared with the forecast ledger)."""
    return CG.lines_label()


def band_line(path=None, date=None):
    """The structural band every title figure carries (post-mortem 2026-10-19 D-PM-6, D-RT-2): each FRAGILE constant
    of the standing sweep with its shifts, read from the record, never typed."""
    path = path or SR.latest(date or datetime.date.today().isoformat())
    try:
        with open(path, encoding="utf-8") as f:
            sw = json.load(f)
    except (OSError, ValueError):
        return "Structural band: no sweep record found (scripts/redteam/sweep.py writes it)."
    parts = []
    for key in sw.get("fragile", []):
        c = sw["constants"][key]
        parts.append(f"{key.split('.')[-1]} is FRAGILE: " + " / ".join(f"{v['shift_mean']:+.1f} ({v['label']})" for v in c["variants"]))
    return "Structural band (" + SR.describe(sw, path, as_of=date) + ", deck " + str(sw.get("engine_commit", "?")) + "): " + ("; ".join(parts) if parts else "no FRAGILE constant") + "."


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


def add_flag(s):
    """The waiver pair's status flag: the day's code and its source, and for a short Out ESPN's date (owner 2026-10-28,
    item 5). Owner 2026-11-11: the date is worded as the earliest return; graded 10-28 to 11-11, a first quote was on
    time for 44% of pool players, late or still out for 53%, early for 3%."""
    if s.get("short_out"):
        return f"{s['code']} today ({s['source']}), {EARLIEST} {s['return_date'][:10]}"
    return f"{s['code']} today ({s['source']})"


EARLIEST = "ESPN's earliest return"


def aside_flag(x):
    """A player the waiver scan set aside as Out, with ESPN's date when it gives one."""
    return f"{x['player']} ({x['code']}, {x['source']}" + (f", {EARLIEST} {x['return_date'][:10]}" if x.get("return_date") else "") + ")"


def stream_flag(r):
    """A streamer's status note: games counted from ESPN's earliest return, or the tier's expected games."""
    if r.get("return_date"):
        return f" ({r['status']} today, {EARLIEST} {r['return_date']}: {r['exp_games']:g} from then)"
    return f" ({r['status']} today: {r['exp_games']:g} expected)" if r.get("status") else ""


def status_inputs(date, pull_dir=None, status_dir=None):
    """The day's status sources for the waiver gate (owner 2026-10-28, "Status gate"): Yahoo's available-player list
    from the pinned Flaim pull, and ESPN's injury feed pinned by status_feed. Each is None when the day has none."""
    pull_dir = pull_dir or os.path.join(CG.KIT, "data", "source", "flaim")
    status_dir = status_dir or os.path.join(CG.KIT, "data", "status")
    yahoo = espn = None
    pp = os.path.join(pull_dir, f"pull_{date}.json")
    if os.path.exists(pp):
        fa = (json.load(open(pp, encoding="utf-8")).get("free_agents") or {}).get("freeAgents")
        yahoo = fa or None
    ep = os.path.join(status_dir, f"espn_injuries_{date}.json")
    if os.path.exists(ep):
        espn = json.load(open(ep, encoding="utf-8"))["rows"]
    return yahoo, espn


def own_moves(date, window, news_dir=None):
    """The league-moves records for the "you dropped him" look-back (owner pick 2026-11-03): today and the window - 1
    days before it, the morning record and the afternoon one (_pm) of each day. Returns ({day: [records]}, [days with
    neither record]). Not data/managers/transactions.json: manager_log runs after the brief and misses that morning."""
    news_dir = news_dir or os.path.join(CG.KIT, "data", "news")
    d0 = datetime.date.fromisoformat(date)
    by_day, missing = {}, []
    for k in range(window - 1, -1, -1):
        day = (d0 - datetime.timedelta(days=k)).isoformat()
        recs = [json.load(open(p, encoding="utf-8")) for p in (os.path.join(news_dir, f"league_moves_{day}.json"),
                                                              os.path.join(news_dir, f"league_moves_{day}_pm.json"))
                if os.path.exists(p)]
        if recs:
            by_day[day] = recs
        else:
            missing.append(day)
    return by_day, missing


def waiver_note(name, info):
    """The display suffix for a pick (owner pick 2026-11-03): "on waivers until <date>" and/or "you dropped him
    <date>", joined by " · "; empty when neither holds or there is no record."""
    r = ((info or {}).get("by") or {}).get(name) or {}
    parts = ([f"on waivers until {r['waiver_date']}"] if r.get("waiver_date") else []) + \
            ([f"you dropped him {r['own_drop_date']}"] if r.get("own_drop_date") else [])
    return " · ".join(parts)


def annotate_waivers(rows, key, info):
    """Adds add_waiver_date and add_own_drop_date (None when none) to each pick; nothing else on the row changes."""
    for x in rows:
        r = ((info or {}).get("by") or {}).get(x[key]) or {}
        x["add_waiver_date"] = r.get("waiver_date")
        x["add_own_drop_date"] = r.get("own_drop_date")
    return rows


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


def unpooled_line(state, by=None):
    """Owner 2026-10-26, option (a): the names the intake carried without a pool row, or None. Never silent. Owner
    2026-11-09 ("Simulate them"): a name the pool in use has (`by`: the season pool's auto season line) is simulated
    and is listed as an auto row, never as "not simulated"."""
    un = (state or {}).get("unpooled") or []
    if not un:
        return None
    auto = [u for u in un if by and u["player"] in by]
    out = [u for u in un if u not in auto]
    fmt = lambda xs: ", ".join(f"{u['player']} ({u['fantasy_team']}, {u['slot']}, {u['nba_team']})" for u in xs)
    parts = []
    if out:
        parts.append(f"**Not in the pool, not simulated ({len(out)}):** {fmt(out)}. "
                     "Each needs a data/pool_additions.csv row before the simulator counts him.")
    if auto:
        parts.append(f"Auto row (blended), simulated ({len(auto)}): {fmt(auto)}.")
    return " ".join(parts)


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
    # owner 2026-10-28 ("Status gate"): the day's injury status gates the candidates; with no source the scan stops
    yahoo_fa, espn_rows = status_inputs(a.date)
    try:
        st = CG.fa_status(P, yahoo_fa, espn_rows, date=a.date)
        fa, aside = CG.free_agents(P, state, st)
        gate = {"sources": st["sources"], "set_aside": aside}
    except CG.StatusMissing as e:
        st, fa, aside = {"by": {}}, [], []
        gate = {"halt": str(e)}
        print(f"WAIVER SCAN: HALT — {e}; no waiver pairs or streaming today (never the pool unchecked)")
    base_ecw, pairs = CG.waiver_pairs(ros, fa) if fa else (None, [])
    pos = [x for x in pairs if x["d_ecw"] > 0]
    for x in pairs:
        s = st["by"].get(x["add"])
        if s:
            x["add_status"] = {"code": s["code"], "source": s["source"], "return_date": s.get("return_date"),
                               "short_out": s.get("short_out", False)}
    top, seen = [], set()
    for x in pos:
        if x["add"] not in seen:
            seen.add(x["add"])
            top.append(x)
        if len(top) == 3:
            break

    # 5. title odds (and the waiver check) on the real schedule
    work = tempfile.mkdtemp()
    sims = {s: CG.run_league_sim(ros, s, a.seasons, work) for s in SEEDS}
    base = {s: sims[s]["teams"][str(CG.OWNER_SEAT)] for s in SEEDS}
    absent = sims[SEEDS[0]]["absent_from_sim"]   # sim-roster names the sim pool lacks; never state "unpooled" (co_gm)
    for x in top:
        r2 = {s: list(r) for s, r in ros.items()}
        r2[CG.OWNER_SEAT] = [p for p in r2[CG.OWNER_SEAT] if p["player"] != x["drop"]] + [by[x["add"]]]
        # owner 2026-10-20: the waiver check runs both seeds, so its title figure is the same two-run average
        sw = {s: CG.run_league_sim(r2, s, a.seasons, work, tag="w") for s in SEEDS}
        t = {s: sw[s]["teams"][str(CG.OWNER_SEAT)]["champ"] for s in SEEDS}
        if sw[SEEDS[0]]["absent_from_sim"] != absent:
            x["absent_from_sim"] = sw[SEEDS[0]]["absent_from_sim"]
        x["title_by_seed"] = {str(s): round(t[s], 2) for s in SEEDS}
        x["title"] = round(sum(t.values()) / len(SEEDS), 2)
        x["d_title"] = round(x["title"] - sum(base[s]["champ"] for s in SEEDS) / len(SEEDS), 2)

    # 4. streaming: free agents by per-game board value x games left this week
    weakest = min((p for p in ros[CG.OWNER_SEAT]), key=lambda p: CG.hoops.adj_value(p, ()))
    weak_games = left.get(next(x["yahoo_nba_team"] for x in me["players"] if x["player"] == weakest["player"]), 0)
    # owner 2026-10-28 (item 5): a short Out streams on its games from ESPN's return date
    stream = CG.streaming(CG.stream_rows(fa, st, games, a.date, wend), weak_games)
    # owner pick 2026-11-03 (display only): Yahoo's waiver date and the owner's own recent drop beside each pick; the
    # ranking, the candidates and every number above are untouched
    mv_days, mv_missing = own_moves(a.date, CG.WAIVER_DROP_WINDOW)
    winfo = CG.waiver_info(P, yahoo_fa, mv_days)
    annotate_waivers(top, "add", winfo)
    annotate_waivers(stream, "player", winfo)

    tx = transactions_for(a.date)

    lm = league_moves_for(a.date)
    ilr = il_return_for(a.date)
    rec = {"date": a.date, "week": wk, "week_window": [wstart, wend], "league_state_as_of": state["as_of"],
           "unpooled": state.get("unpooled") or [],
           "status_file": status_file, "lines": lines_label(), "opponent": opp_team["name"] if opp_team else None,
           "today": rows_today, "lineup": lineup, "bench": bench,
           "waiver_base_ecw": round(base_ecw, 4) if base_ecw is not None else None, "waiver_gate": gate,
           "waiver_positive_pairs": len(pos), "waiver_pairs_scored": len(pairs), "waiver_top": top, "streaming": stream,
           "waiver_notes": {"read": winfo["read"], "window_days": CG.WAIVER_DROP_WINDOW, "missing_days": mv_missing,
                            "by": winfo["by"]},
           "streaming_vs": {"player": weakest["player"], "games_left": weak_games,
                            "value_per_game": round(CG.hoops.adj_value(weakest, ()), 2)},
           "title": {str(s): base[s]["champ"] for s in SEEDS}, "playoffs": {str(s): base[s]["playoff"] for s in SEEDS},
           "seasons": a.seasons, "absent_from_sim": absent, "transactions": tx and {"window": tx["window"], "ok": tx["source"].get("ok"), "hits": tx["hits"]},
           "league_moves": lm and lm["moves"],
           # owner 2026-10-31: the IL-return scenario range, read from il_return.py's record when one exists for the
           # day; a separate section, never the headline
           "il_return": ilr and {k: ilr[k] for k in ("espn_date", "n_il", "room_rule", "error", "seasons", "label", "room_band", "slip_range") if k in ilr}
           | {"scenarios": {k: {"title": v["title"], "playoffs": v["playoffs"]} for k, v in ilr["scenarios"].items()
                            if k in ("never", "on_time", "late_2", "late_4")}}}
    os.makedirs(OUTDIR, exist_ok=True)
    json.dump(rec, open(os.path.join(OUTDIR, f"brief_{a.date}.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    L = [f"# Daily brief — {a.date} (week {wk}, {wstart} to {wend})", ""]
    L.append(f"Opponent this week: **{rec['opponent']}**. Rosters as of {state['as_of']} "
             f"({'FantasyBot live pull' if 'fantasybot' in (state.get('sources') or {}) else chr(39).join(['owner', 's Yahoo page'])}); "
             f"statuses from `{status_file}`; lines: {lines_label()}.")
    if unpooled_line(state, by):
        L += ["", unpooled_line(state, by)]
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
    L += ["", "## Waiver scan", ""]
    if "halt" in gate:
        L.append(f"**HALT** — {gate['halt']}. No pairs and no streaming list today: the scan never runs on the pool unchecked.")
    elif top:
        L.append(f"{len(pos)} of {len(pairs)} add/drop pairs raise expected weekly category wins (base {base_ecw:.3f}). "
                 f"Best {len(top)}, checked in the simulator (avg of 2 runs × {a.seasons:,} seasons, real schedule):")
        L += [f"- Add **{x['add']}** ({x['add_team']}), drop {x['drop']}: {x['d_ecw']:+.3f} cats/week; "
              f"title {x['title']:.1f}% ({x['d_title']:+.1f})"
              + (f" — {add_flag(x['add_status'])}, check before claiming" if x.get("add_status") else "")
              + ((" · " if x.get("add_status") else " — ") + waiver_note(x["add"], winfo) if waiver_note(x["add"], winfo) else "")
              for x in top]
    else:
        L.append(f"No add/drop pair raises expected weekly category wins ({len(pairs)} scored). Stand pat.")
    if "halt" not in gate:
        srcs = " and ".join(k.upper() if k == "espn" else "Yahoo" for k, v in gate["sources"].items() if v)
        miss = [("Yahoo's available list" if k == "yahoo" else "ESPN's injury feed") for k, v in gate["sources"].items() if not v]
        L.append(f"Status from {srcs}" + (f" ({', '.join(miss)} not read today)" if miss else "") + "."
                 + (" Set aside as Out: " + ", ".join(aside_flag(x) for x in aside) + "."
                    if aside else ""))
        if not winfo["read"]:
            L.append("Waiver dates not read today (no Yahoo available-player list pinned): a pick may be on waivers.")
        if mv_missing:
            L.append(f"Own drops checked over {CG.WAIVER_DROP_WINDOW} days; no league-moves record for {', '.join(mv_missing)}.")
    L += ["", f"## Streaming ({a.date} to {wend})", "",
          f"Your weakest active player by board value is {weakest['player']} "
          f"({rec['streaming_vs']['value_per_game']:+.2f} per game, {weak_games} games left). "
          f"Free agents with more games left, best per game first:"]
    L += [f"- {r['player']} ({r['team']}): {r['games_left']} games"
          + stream_flag(r)
          + f", {r['value_per_game']:+.2f} per game"
          + (f" — {waiver_note(r['player'], winfo)}" if waiver_note(r["player"], winfo) else "") for r in stream] or ["- none"]
    L += ["", "## Title odds (real schedule)", "", f"- Title: {odds_line(base[SEEDS[0]]['champ'], base[SEEDS[1]]['champ'], a.seasons)}",
          f"- Playoffs: {(base[SEEDS[0]]['playoff'] + base[SEEDS[1]]['playoff']) / 2:.1f}%",
          f"- {band_line(date=a.date)}"] + ([f"- {sim_absent_line(absent)}"] if absent else []) + (
          ["", "### If IL players return (scenario range)", ""] + ["- " + x if not x.startswith("- ") else x for x in ilr["lines"]] if ilr else []) + ["",
          "_Cannot see: news after the morning FantasyBot pull (or the last paste) beyond ESPN's transactions and injury feeds (the injury feed gates the waiver scan only); minutes limits; "
          "other managers' pending claims. Q counts as a coin flip._"]
    path = os.path.join(OUTDIR, f"brief_{a.date}.md")
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"wrote {os.path.relpath(path, CG.KIT)}")


def il_return_for(date, outdir=None):
    """il_return.py's record for the day, or None (the section is drawn only from a record; nothing is simulated here)."""
    p = os.path.join(outdir or os.path.join(CG.KIT, "report", "il_return"), f"il_return_{date}.json")
    if not os.path.exists(p):
        return None
    try:
        return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        return None


def sim_absent_line(names):
    """The title odds' caveat when the season simulator could not play a rostered player (owner option (b),
    2026-10-21; since 2026-10-26 the simulator plays SEASON_POOL when set, so this names a player missing from that pool)."""
    if not names:
        return None
    return (f"{', '.join(names)}: left out of the season simulation (not in its pool; the rule "
            f"for IL players, D-IS-8); the waiver scan still counts {'him' if len(names) == 1 else 'them'}.")


if __name__ == "__main__":
    main()
