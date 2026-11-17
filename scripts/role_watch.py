#!/usr/bin/env python3
"""Role watch (owner 2026-11-17, card picks "Starts watch" and "Hold check on drops"): two display-only lists for the
morning brief, both from the regular-season box scores on disk (form_board.game_log: data/actuals, DNPs excluded).

Why: the missed-pickup audit of 2026-11-17 (after-report-2026-11-17-missed-pickups.md). Of 16 rival pickups that then
played at top-100 level over 2026-10-20..11-16, the waiver scan had named 2; a pool-wide "30+ minutes three games
running" rule would have named none before the add, and "started his last two games" named 8 of the 14 the scan had
not, at about two new names a day. And three of the owner's own pickups that went on to play well were dropped
within two games. Neither list is a pick: about half the starts-watch names in the audit window did not go on to
play at roster level.

  starts watch   every player in the box scores who is on no roster and started each of his last START_RUN games,
                 the last of them within STALE_DAYS of the brief's date: the minutes and per-game line of his last
                 three games, the length of the run, whether the pool in use has a line for him (the waiver scan
                 cannot score a player it has no line for), ESPN's injury line when it lists him, and the day a
                 league-moves record of the last DROPPED_DAYS days shows a team dropped him. NEW marks a run that
                 reached START_RUN with his last game. New runs and fresh drops are always printed; the rest fill
                 the list to WATCH_SHOWN rows by minutes.
  hold check     the owner's active players who were added in the last HOLD_DAYS days, or are named as the drop by
                 today's waiver pairs or streaming line: the same last-three line, the games he has played since
                 the add, and HOLD when he would be on the starts watch were he free (he started each of his last
                 START_RUN games, or his only game). A player with no game since the add is said to be unjudged.

Display only: nothing here changes a line, a roster, a tag or a constant, and nothing reaches a graded record. The
four thresholds are display thresholds, hand-set (declared 2026-11-17); nothing downstream reads them.
Red-first tests: test_role_watch.py.
"""
import datetime
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import co_gm as CG  # noqa: E402
import form_board as FB  # noqa: E402
import league_intake as LI  # noqa: E402

ACTUALS = os.path.join(CG.KIT, "data", "actuals")
NEWS = os.path.join(CG.KIT, "data", "news")
START_RUN = 2       # straight starts that put a free player on the watch (audit 2026-11-17: 8 of 14 misses caught)
STALE_DAYS = 7      # his last game must be this recent; a free starter who stopped playing is not a pickup
DROPPED_DAYS = 3    # look-back for "a team dropped him", the waiver scan's own drop window (co_gm.WAIVER_DROP_WINDOW)
HOLD_DAYS = 7       # an owner pickup this recent gets a hold line
WATCH_SHOWN = 8     # rows printed in the brief once the news rows are in; the record keeps them all
LINE = ("pts", "reb", "ast", "stl", "blk", "tpm", "tov")


def load_log(folder=ACTUALS):
    """form_board's per-game log from every box-score record on disk."""
    return FB.game_log([json.load(open(f, encoding="utf-8")) for f in sorted(glob.glob(os.path.join(folder, "*.json")))])


def before(games, date):
    return [g for g in games if (g.get("date") or "") < date]


def start_run(games):
    """Straight starts ending with his most recent game."""
    n = 0
    for g in reversed(games):
        if not g.get("starter"):
            break
        n += 1
    return n


def last_three(games):
    """Minutes, starts and the per-game line of his last three games (fewer when he has fewer)."""
    gs = games[-3:]
    if not gs:
        return dict(games=0, minutes=[], starts=0, line=None)
    n = len(gs)
    return dict(games=n, minutes=[g.get("min", 0) for g in gs], starts=sum(1 for g in gs if g.get("starter")),
                line={c: round(sum(g.get(c, 0) or 0 for g in gs) / n, 1) for c in LINE})


def rostered_names(state):
    """Every name on a roster, in any slot, the pool's spelling or not, folded."""
    names = set()
    for t in state.get("teams") or []:
        names |= {p["player"] for p in t.get("players") or []}
        names |= {p.get("yahoo_name") for p in t.get("players") or [] if p.get("yahoo_name")}
        names |= set(t.get("unpooled_il") or [])
        names |= {u["player"] for u in t.get("unpooled") or [] if isinstance(u, dict) and u.get("player")}
    names |= {u["player"] for u in state.get("unpooled") or [] if u.get("player")}
    names |= set(state.get("unpooled_il") or {})
    return {LI.norm(n) for n in names}


def moves(date, days, news_dir=None):
    """League-moves records of `date` and the days - 1 days before it (morning and afternoon), in order:
    {folded name: (day, team, seat)} for adds and for drops. A drop keeps its newest record. An add keeps the first
    record of the team's current spell with him: a morning record that repeats last evening's add does not move the
    day, and a player dropped and added again is dated from the second add."""
    news_dir = news_dir or NEWS
    d0 = datetime.date.fromisoformat(date)
    added, dropped = {}, {}
    for k in range(days - 1, -1, -1):
        day = (d0 - datetime.timedelta(days=k)).isoformat()
        for path in (os.path.join(news_dir, f"league_moves_{day}.json"), os.path.join(news_dir, f"league_moves_{day}_pm.json")):
            if not os.path.exists(path):
                continue
            with open(path, encoding="utf-8") as f:
                rec = json.load(f)
            for m in rec.get("moves") or []:
                for n in m.get("dropped") or []:
                    dropped[LI.norm(n)] = (day, m.get("team"), m.get("seat"))
                    if added.get(LI.norm(n), (None, None, None))[2] == m.get("seat"):
                        del added[LI.norm(n)]
                for n in m.get("added") or []:
                    if added.get(LI.norm(n), (None, None, None))[2] != m.get("seat"):
                        added[LI.norm(n)] = (day, m.get("team"), m.get("seat"))
    return added, dropped


def starts_watch(log, rostered, date, pool_names=(), espn=None, dropped=None, run=START_RUN, stale=STALE_DAYS):
    """Free players on a run of `run`+ straight starts whose last game is within `stale` days of `date`: the news
    first (a run that just reached `run`, or a player a team just dropped), then by the minutes of the last three
    games. `rostered` is folded names; `espn` the injury feed's rows; `dropped` moves()'s."""
    pooled = {LI.norm(n) for n in pool_names}
    inj = {LI.norm(r["player"]): r for r in espn or [] if r.get("player")}
    floor = (datetime.date.fromisoformat(date) - datetime.timedelta(days=stale)).isoformat()
    rows = []
    for name, games in log.items():
        key = LI.norm(name)
        gs = before(games, date)
        if key in rostered or len(gs) < run or gs[-1]["date"] < floor:
            continue
        streak = start_run(gs)
        if streak < run:
            continue
        e, d = inj.get(key), (dropped or {}).get(key)
        rows.append(dict(player=name, team=gs[-1].get("team"), starts_in_a_row=streak, new=streak == run,
                         last_game=gs[-1]["date"], season_games=len(gs), pooled=key in pooled,
                         status=e and dict(status=e.get("status"), return_date=e.get("return_date")),
                         dropped=d and dict(day=d[0], team=d[1]), **last_three(gs)))
    rows.sort(key=lambda r: (not (r["new"] or r["dropped"]), -sum(r["minutes"]) / len(r["minutes"]), r["player"]))
    return rows


def hold_check(log, players, date, added=None, drops=(), owner_seat=None, run=START_RUN):
    """The owner's active players (`players`: state rows, IL slot excluded by the caller) who were added in the
    look-back (`added`: moves()'s, the owner's seat only) or are named in `drops`."""
    named = {LI.norm(n) for n in drops if n}
    by_norm = {}
    for k in log:
        by_norm.setdefault(LI.norm(k), k)
    rows = []
    for p in players:
        key = LI.norm(p["player"])
        a = (added or {}).get(key)
        if a and owner_seat is not None and a[2] != owner_seat:
            a = None
        if not a and key not in named:
            continue
        gs = before(log.get(by_norm.get(key), []), date)
        since = [g for g in gs if a and g["date"] >= a[0]]
        why = ([f"added {a[0]}"] if a else []) + (["named as a drop today"] if key in named else [])
        streak = start_run(gs)
        hold = bool(gs) and streak >= min(run, len(gs))
        rows.append(dict(player=p["player"], why=why, added=a and a[0], games_since_add=len(since) if a else None,
                         unjudged=bool(a) and not since, starts_in_a_row=streak, hold=hold, season_games=len(gs),
                         **last_three(gs)))
    return rows


def build(date, state, pool_names, espn=None, drops=(), owner_seat=CG.OWNER_SEAT, actuals=None, news_dir=None):
    """The brief's record: both lists and the rule they were made with."""
    log = load_log(actuals or ACTUALS)
    added_hold, _ = moves(date, HOLD_DAYS, news_dir)
    _, dropped = moves(date, DROPPED_DAYS, news_dir)
    me = next((t for t in state.get("teams") or [] if t.get("seat") == owner_seat), None)
    mine = [p for p in (me or {}).get("players") or [] if p.get("slot") != "IL"]
    days = sorted({g["date"] for gs in log.values() for g in gs if g.get("date") and g["date"] < date})
    return dict(box_scores=[days[0], days[-1]] if days else None,
                rule=dict(start_run=START_RUN, stale_days=STALE_DAYS, dropped_days=DROPPED_DAYS, hold_days=HOLD_DAYS,
                          shown=WATCH_SHOWN),
                starts_watch=starts_watch(log, rostered_names(state), date, pool_names, espn, dropped),
                hold_check=hold_check(log, mine, date, added_hold, drops, owner_seat))


def _line(r):
    if not r["line"]:
        return "no game this season"
    x = r["line"]
    return (f"last {r['games']}: {'/'.join(str(m) for m in r['minutes'])} min, {r['starts']} start{'s' if r['starts'] != 1 else ''}; "
            f"{x['pts']:g} pts, {x['reb']:g} reb, {x['ast']:g} ast, {x['stl']:g} stl, {x['blk']:g} blk, {x['tpm']:g} 3s, {x['tov']:g} to")


def watch_lines(rw):
    """Markdown lines for the brief's starts watch."""
    if not rw or rw.get("error"):
        return [f"Not available today ({(rw or {}).get('error') or 'no record'})."]
    rows = rw["starts_watch"]
    if not rows:
        return [f"No free player has started his last {rw['rule']['start_run']} games."]
    news = [r for r in rows if r["new"] or r["dropped"]]
    shown = news + [r for r in rows if not (r["new"] or r["dropped"])][:max(0, rw["rule"]["shown"] - len(news))]
    L = [f"{len(rows)} free player{'s have' if len(rows) != 1 else ' has'} started the last {rw['rule']['start_run']} games "
         f"(box scores to {rw['box_scores'][1]}); new runs and fresh drops first, then by minutes"
         + (f"; {len(shown)} shown" if len(shown) < len(rows) else "")
         + ". A screen to judge, not a pick: about half of such names did not go on to play at roster level (audit 2026-11-17)."]
    for r in shown:
        tags = (["NEW"] if r["new"] else []) + ([f"dropped {r['dropped']['day']} by {r['dropped']['team']}"] if r["dropped"] else []) \
            + ([] if r["pooled"] else ["no line in the pool, so the waiver scan cannot score him"]) \
            + ([f"ESPN: {r['status']['status']}" + (f", earliest return {r['status']['return_date']}" if r['status'].get('return_date') else "")]
               if r["status"] else [])
        L.append(f"- **{r['player']}** ({r['team']}): {r['starts_in_a_row']} starts in a row; {_line(r)}" + (" — " + "; ".join(tags) if tags else ""))
    return L


def hold_lines(rw):
    """Markdown lines for the brief's hold check."""
    if not rw or rw.get("error"):
        return [f"Not available today ({(rw or {}).get('error') or 'no record'})."]
    rows = rw["hold_check"]
    if not rows:
        return [f"None of your active players was added in the last {rw['rule']['hold_days']} days or is named as a drop today."]
    L = []
    for r in rows:
        if r["unjudged"]:
            verdict = "has not played since you added him: nothing to judge yet"
        elif r["hold"]:
            n = r["starts_in_a_row"]
            verdict = (f"**HOLD?** he started his last {n} games" if n > 1 else "**HOLD?** he started his only game") \
                + ": a free player with this run is on the starts watch"
        else:
            verdict = "no start run"
        since = f"; {r['games_since_add']} game{'s' if r['games_since_add'] != 1 else ''} since the add" if r["added"] else ""
        L.append(f"- **{r['player']}** ({', '.join(r['why'])}{since}): {_line(r)} — {verdict}")
    return L
