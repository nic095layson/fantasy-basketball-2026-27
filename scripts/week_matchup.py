#!/usr/bin/env python3
"""Week matchup (owner 2026-10-21: "After each morning refresh pull, I'd like the "Today" tab to show a Week 1
Categories against my opponent, updated from the game results the day prior. Then, using the data and projections
you have for the games remaining in the matchup this week, show a "faded" color which are the projections ... if one
of my lower valued players on my team - IF they have completed their games for the week, this tool can forecast what
free agent player pickups could contribute to me winning the categories I am deficient in").

Writes report/briefs/week_matchup_<date>.json, which the Season Deck draws on its Today tab. Method, stated to the
owner before the first run (2026-10-21):
  M1 window      the Yahoo week from the kit calendar (co_gm.week_of); to date = box scores from the week's first day
                 through yesterday; remaining = NBA games from today through the week's last day (bref schedule).
  M2 to date     Yahoo's own week totals (owner 2026-10-21, "A"): the current week's get_matchups values read through
                 Flaim at the morning pull (data/source/flaim/pull_<date>.json), so through yesterday's games. The
                 reconstruction still runs as the cross-check, and every stat where it differs from Yahoo is listed.
                 A day whose Yahoo lineup is pinned (get_roster with as_of_date, in this week's pulls; owner
                 2026-10-22, "Read daily rosters") counts the box lines of the players in an active slot that day (not
                 BN, IL or IL+), so a player dropped after playing still counts on his day. Any other day falls back:
                 every non-IL player on the current roster who played counts; on a day more than ten of a team's
                 players played, the ten counted are the brief's daily-fill rule (co_gm.daily_lineup: positions, then
                 board value). The record names each day's source (rebuild_rosters). No pull, no week in it, or a
                 matchup that does not name both teams: the reconstruction is the column, and the record says why.
  M3 projection  season-pool per-game line (SEASON_POOL, the brief's blended lines) x each remaining game x today's
                 availability from the status file (no row: 1.0, the brief's rule); the same ten-slot fill each day;
                 IL counts 0 (D-IS-8).
  M4 percentages FG% and FT% are total makes / total attempts, actual plus projected; makes projected as line % x
                 attempts.
  M5 leader      higher final wins; TO lower wins; equal (or no attempts) is a tie. Point estimates, no probability.
  M6 drop        "finished" = 0 NBA games from today through the week's end; "lower valued" = board value
                 (hoops.adj_value, the brief's streaming measure) below the active roster's median.
  M7 pickups     Yahoo's available-player list from the same pull (owner 2026-10-21, "D"; Flaim returns at most 100,
                 ordered by Yahoo-wide ownership), each added in place of the finished player from today on; ranked by
                 projected category wins gained (ties count half), then by the share of each losing category's gap
                 closed. A listed player's Yahoo letter sets his availability (status_feed.TIERS); O and NA are out, a
                 letter the kit does not tier is set aside and named, never guessed; a name the season pool cannot
                 resolve is named as not projected; one the league state still shows rostered, on the do-not-draft
                 list, or out in the kit pool is skipped and named. No list in the pull: every pooled free agent (not
                 rostered, availability > 0, not on the do-not-draft list), as before. A free agent absent from his
                 team's last box score in the past week is flagged, not dropped. Waiver players cannot be told apart
                 from free agents.
  M8 this week   owner 2026-10-22 (P1, "Full build"): each category's chance of winning is the normal approximation
                 on the final totals (co_gm._pcat): to date is fixed; each remaining started game adds
                 a*(x*cv)^2 + a*(1-a)*x^2 to a counting stat's variance (arena.SEASON_CV, the compound sum of
                 team_week_model one game at a time) and a*attempts*p*(1-p) to the makes, FG%/FT% then
                 x PCT_MIX_INFL^2 / total attempts^2; no remaining variance and a level total is a tie (0.5). The
                 shared weekly shock (TEAM_WEEK_SHOCK) is left out: the games come from the real schedule. A free
                 agent's worth this week is the change in expected categories won (the sum of the nine changes in
                 P(win), exact by linearity), in place of the drop candidate that helps most; candidates are the
                 active players below the median value (M6's measure), finished or not; the swap starts tomorrow
                 (waivers cannot be told apart, so the conservative day). The season cost of that drop is the change
                 in expected weekly categories against the other eleven teams (co_gm.waiver_pairs' measure).

    python3 scripts/week_matchup.py --date YYYY-MM-DD [--out-dir report/briefs] [--yahoo-pull PATH]
Prints 'WEEK MATCHUP: PASS — ...' and exits 0, or 'WEEK MATCHUP: FAIL — ...' and exits 1.
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import box_pull as BP  # noqa: E402
import co_gm as CG  # noqa: E402
import flaim_live as FL  # noqa: E402
import league_intake as LI  # noqa: E402
import status_feed  # noqa: E402

KIT = CG.KIT
OUTDIR = os.path.join(KIT, "report", "briefs")
ACTUALS = os.path.join(KIT, "data", "actuals")
STATUS = os.path.join(KIT, "data", "status")
PULLS = FL.PIN_DIR  # data/source/flaim/pull_<date>.json, pinned by league_live
CATS = ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]
STATS = ["fgm", "fga", "ftm", "fta", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"]
PICKUPS_SHOWN = 5
COUNT = {"3PTM": "tpm", "PTS": "pts", "REB": "reb", "AST": "ast", "ST": "stl", "BLK": "blk", "TO": "tov"}
LOOKBACK_DAYS = 7  # how far back a free agent's last team game is looked for (the missed-game flag)
BENCH_SLOTS = ("BN", "IL", "IL+")  # Yahoo slots whose games do not count


def _d(s):
    return datetime.date.fromisoformat(s)


def days_to_date(date, wstart):
    out, d = [], _d(wstart)
    while d < _d(date):
        out.append(d.isoformat()); d += datetime.timedelta(days=1)
    return out


def days_remaining(date, wend):
    out, d = [], _d(date)
    while d <= _d(wend):
        out.append(d.isoformat()); d += datetime.timedelta(days=1)
    return out


def zero():
    return {k: 0 for k in STATS}


def add(a, b):
    return {k: a[k] + b[k] for k in STATS}


def _card_name(p, index):
    """The name a box line is read under: the record's pool name, or, given the card's own names, the one its source
    spelling (then its pool name) matches there (owner 2026-10-22: the box pull files lines under the kit file's
    spelling, the rosters carry Yahoo's — "Darius Acuff" / "Darius Acuff Jr.", "Cam Johnson" / "Cameron Johnson")."""
    if index is None:
        return p.get("pool_name")
    return BP.match_name(p["name"], index) or (BP.match_name(p["pool_name"], index) if p.get("pool_name") else None)


def played(rec, names=None):
    """{name: box line} for players who played a regular-season game in one data/actuals record, keyed by pool name,
    or by the card's own spelling when its names are given."""
    regular = {g["espn_id"] for g in rec.get("games", []) if g.get("season_type") == 2}
    index = BP.name_index(names) if names is not None else None
    out = {}
    for p in rec.get("players", []):
        n = _card_name(p, index)
        if n and not p.get("dnp") and p.get("game") in regular:
            out[n] = {k: p.get(k) or 0 for k in STATS}
    return out


def _fill(players):
    """co_gm.daily_lineup over dicts with player, positions, value, availability: (counted names, benched names)."""
    lineup, bench = CG.daily_lineup(players)
    return [p for _, p in lineup], bench


def to_date(roster, days, lineups=None, recs=None):
    """roster: [{player, positions, value}]; days: {date: {name: box}}. The counted totals under M2: a day with the
    team's Yahoo lineup (lineups: {date: dated Flaim roster}, recs: {date: that day's box-score record}) counts the
    players in an active slot, read under the lineup's spelling; any other day falls back to today's roster."""
    t, out = zero(), {}
    for d in sorted(days):
        if lineups and d in lineups and recs and d in recs:
            slots = {_alias(p["name"]): p.get("selectedPosition") or "BN" for p in lineups[d].get("players", [])}
            box = played(recs[d], names=list(slots))
            counted = [n for n in slots if n in box and slots[n] not in BENCH_SLOTS]
            benched = [n for n in slots if n in box and slots[n] in BENCH_SLOTS]
            source = "yahoo"
        else:
            box = days[d]
            counted, benched = _fill([dict(r, availability=1.0) for r in roster if r["player"] in box])
            source = "today"
        for n in counted:
            t = add(t, box[n])
        out[d] = dict(counted=counted, benched=benched, roster=source)
    return dict(totals=t, days=out)


def week_lineups(pull_path, ws, date):
    """{Yahoo team name: {date: dated roster}} for the week's days before `date`, from the dated rosters pinned in
    this week's pulls (data/source/flaim/pull_<date>.json) and the run's own pull, read last: a lineup one morning
    pinned is read by every later run of the week, and the latest pin of a day wins."""
    if not pull_path:
        return {}
    run = os.path.abspath(pull_path)
    earlier = sorted(f for f in glob.glob(os.path.join(os.path.dirname(run), "pull_????-??-??.json"))
                     if ws <= os.path.basename(f)[5:15] <= date and os.path.abspath(f) != run)
    out = {}
    for f in earlier + [run]:
        pull, _ = load_pull(f)
        for by_day in ((pull or {}).get("daily") or {}).values():
            for day, r in by_day.items():
                if ws <= day < date:
                    out.setdefault(r.get("teamName"), {})[day] = r
    return out


def per_game(ln):
    return dict(fgm=ln["fg_pct"] * ln["fga"], fga=ln["fga"], ftm=ln["ft_pct"] * ln["fta"], fta=ln["fta"],
                tpm=ln["tpm"], pts=ln["pts"], reb=ln["reb"], ast=ln["ast"], stl=ln["stl"], blk=ln["blk"], tov=ln["tov"])


def remaining(roster, sched, avail, lines):
    """roster: [{player, team, positions, value}]; sched: {date: set of teams playing}; avail: {player: probability}
    (missing = 1.0); lines: {player: per-game line}. Expected totals under M3, each player's projected starts, and
    the variance of the totals (M8): per started game a*(x*cv)^2 + a*(1-a)*x^2 by counting category, a*att*p*(1-p)
    on the makes."""
    cv = CG.arena.SEASON_CV
    t, games, started = {k: 0.0 for k in STATS}, {}, {}
    var = {k: 0.0 for k in list(COUNT) + ["fg_mk", "ft_mk"]}
    for d in sorted(sched):
        cand = [dict(r, availability=avail.get(r["player"], 1.0)) for r in roster if r["team"] in sched[d]]
        counted, _ = _fill(cand)
        started[d] = counted
        for n in counted:
            a, g = avail.get(n, 1.0), per_game(lines[n])
            t = {k: t[k] + g[k] * a for k in STATS}
            games[n] = games.get(n, 0) + 1
            for c, k in COUNT.items():
                var[c] += a * (g[k] * cv[c]) ** 2 + a * (1 - a) * g[k] ** 2
            var["fg_mk"] += a * lines[n]["fga"] * lines[n]["fg_pct"] * (1 - lines[n]["fg_pct"])
            var["ft_mk"] += a * lines[n]["fta"] * lines[n]["ft_pct"] * (1 - lines[n]["ft_pct"])
    return dict(totals=t, games=games, started=started, var=var)


def cat_chances(me_now, me_rem, opp_now, opp_rem):
    """P(I win) per category (M8): the normal approximation on the final totals, to date fixed and the remaining games
    carrying the variance; no attempts on either side, or level with nothing left to vary, is a tie (0.5)."""
    infl = CG.arena.PCT_MIX_INFL

    def side(now, rem):
        fin, v = add(now, rem["totals"]), rem["var"]
        mu, var = {c: fin[k] for c, k in COUNT.items()}, {c: v[c] for c in COUNT}
        for c, mk, at, vk in (("FG%", "fgm", "fga", "fg_mk"), ("FT%", "ftm", "fta", "ft_mk")):
            mu[c] = fin[mk] / fin[at] if fin[at] else None
            var[c] = infl ** 2 * v[vk] / fin[at] ** 2 if fin[at] else 0.0
        return mu, var
    m, o = side(me_now, me_rem), side(opp_now, opp_rem)
    out = {}
    for c in CATS:
        if m[0][c] is None or o[0][c] is None:
            out[c] = 0.5
        elif m[1][c] + o[1][c] == 0:
            g = margin(c, m[0][c], o[0][c])
            out[c] = 0.5 if abs(g) < 1e-12 else (1.0 if g > 0 else 0.0)
        else:
            out[c] = CG._pcat(m, o, c)
    return out


def win_week_chance(ps, need=5):
    """P(at least `need` of the categories) from per-category chances, the categories taken as independent (owner
    2026-10-22, "Live + pre-week": a simplification, said so on the tile; counting categories move together)."""
    d = [1.0]
    for q in ps:
        d = [(d[k] if k < len(d) else 0.0) * (1 - q) + (d[k - 1] if k > 0 else 0.0) * q for k in range(len(d) + 1)]
    return sum(d[need:])


def swap_candidates(roster):
    """M8's drop candidates: the active players below the active roster's median value, finished or not, lowest first."""
    med = statistics.median(r["value"] for r in roster)
    return [r["player"] for r in sorted(roster, key=lambda r: r["value"]) if r["value"] < med]


def _split(sched, today):
    return {d: t for d, t in sched.items() if d == today}, {d: t for d, t in sched.items() if d != today}


def _both(a, b):
    return dict(totals=add(a["totals"], b["totals"]), var={k: a["var"][k] + b["var"][k] for k in a["var"]})


def scan_drop_alone(me_now, opp_now, opp_rem, roster, drops, sched, today, avail, lines):
    """Each drop candidate with nobody added, from the day after `today`: the change in expected categories won. A drop
    whose remaining games hurt (a poor shooter, a turnover cost) helps on its own; that is not the add's doing."""
    now_s, rest = _split(sched, today)
    r_today = remaining(roster, now_s, avail, lines)
    base = cat_chances(me_now, _both(r_today, remaining(roster, rest, avail, lines)), opp_now, opp_rem)
    out = {}
    for d in drops:
        p = cat_chances(me_now, _both(r_today, remaining([r for r in roster if r["player"] != d], rest, avail, lines)),
                        opp_now, opp_rem)
        out[d] = sum(p[c] - base[c] for c in CATS)
    return out


def scan_this_week(me_now, opp_now, opp_rem, roster, drops, fas, sched, today, avail, lines):
    """Each free agent in place of the drop candidate that helps most, from the day after `today` (M8): the change in
    P(win) per category and their sum, the change in expected categories won, split into the drop alone (nobody
    added) and the add's share; best first."""
    now_s, rest = _split(sched, today)
    r_today = remaining(roster, now_s, avail, lines)
    base = cat_chances(me_now, _both(r_today, remaining(roster, rest, avail, lines)), opp_now, opp_rem)
    alone = scan_drop_alone(me_now, opp_now, opp_rem, roster, drops, sched, today, avail, lines)
    out = []
    for fa in fas:
        best = None
        for d in drops:
            rr = remaining([r for r in roster if r["player"] != d] + [fa], rest, avail, lines)
            p = cat_chances(me_now, _both(r_today, rr), opp_now, opp_rem)
            dc = {c: p[c] - base[c] for c in CATS}
            de = sum(dc[c] for c in CATS)
            if best is None or de > best["d_exp"]:
                best = dict(add=fa["player"], team=fa["team"], drop=d, d_exp=de, d_cat=dc,
                            d_exp_drop=alone[d], d_exp_add=de - alone[d],
                            games=rr["games"].get(fa["player"], 0),
                            games_left=sum(1 for x in rest if fa["team"] in rest[x]),
                            value=round(fa.get("adj", fa["value"]), 2), status=fa.get("status"), missed=fa.get("missed"))
        if best:
            out.append(best)
    out.sort(key=lambda r: (-r["d_exp"], -r["games"], r["add"]))
    return out


def cat_values(t):
    return {"FG%": t["fgm"] / t["fga"] if t["fga"] else None, "FT%": t["ftm"] / t["fta"] if t["fta"] else None,
            "3PTM": t["tpm"], "PTS": t["pts"], "REB": t["reb"], "AST": t["ast"], "ST": t["stl"], "BLK": t["blk"],
            "TO": t["tov"]}


def margin(c, me, opp):
    """Signed lead in category c (positive = mine; TO reversed); None when either side has no attempts."""
    if me is None or opp is None:
        return None
    return (opp - me) if c == "TO" else (me - opp)


def compare(me, opp):
    out = {}
    for c in CATS:
        m = margin(c, me[c], opp[c])
        out[c] = "tie" if m is None or abs(m) < 1e-9 else ("me" if m > 0 else "opp")
    return out


def _points(cmp):
    return sum(1.0 if v == "me" else 0.5 if v == "tie" else 0.0 for v in cmp.values())


def drop_candidates(roster, left):
    """Active players with no game left this week whose value is below the active roster's median (M6), lowest
    value first, each with its rank (1 = highest value) among the active roster."""
    med = statistics.median(r["value"] for r in roster)
    order = sorted(roster, key=lambda r: -r["value"])
    rank = {r["player"]: i + 1 for i, r in enumerate(order)}
    out = [dict(player=r["player"], team=r["team"], value=round(r["value"], 2), value_rank=rank[r["player"]],
                of=len(roster)) for r in roster if left.get(r["team"], 0) == 0 and r["value"] < med]
    return sorted(out, key=lambda x: x["value"])


def next_finish(roster, sched):
    """Below-median players who still have games: the date of their team's last game this week."""
    med = statistics.median(r["value"] for r in roster)
    out = []
    for r in roster:
        last = max((d for d, teams in sched.items() if r["team"] in teams), default=None)
        if last and r["value"] < med:
            out.append(dict(player=r["player"], team=r["team"], last_game=last, value=round(r["value"], 2)))
    return sorted(out, key=lambda x: (x["last_game"], x["value"]))


def rank_pickups(me_td, opp_fin, roster, drop, fas, sched, avail, lines, n=PICKUPS_SHOWN):
    """Each free agent in place of `drop` from today on (M7): projected category wins gained (ties half), the
    categories it flips each way, and the share of each losing category's gap it closes."""
    opp_v = cat_values(opp_fin)
    base = add(me_td, remaining(roster, sched, avail, lines)["totals"])
    base_v = cat_values(base)
    base_cmp = compare(base_v, opp_v)
    lost = [c for c in CATS if base_cmp[c] == "opp"]
    keep = [r for r in roster if r["player"] != drop]
    out = []
    for fa in fas:
        rem = remaining(keep + [fa], sched, avail, lines)
        fin_v = cat_values(add(me_td, rem["totals"]))
        cmp2 = compare(fin_v, opp_v)
        closed = 0.0
        for c in lost:
            m0, m1 = margin(c, base_v[c], opp_v[c]), margin(c, fin_v[c], opp_v[c])
            if m0 and m1 is not None:
                closed += max(0.0, min(1.0, (m1 - m0) / -m0))
        out.append(dict(add=fa["player"], team=fa["team"], value=round(fa.get("adj", fa["value"]), 2),
                        games_left=sum(1 for d in sched if fa["team"] in sched[d]),
                        starts=rem["games"].get(fa["player"], 0),
                        net=round(_points(cmp2) - _points(base_cmp), 1),
                        flips_to_win=[c for c in CATS if base_cmp[c] != "me" and cmp2[c] == "me"],
                        flips_to_loss=[c for c in CATS if base_cmp[c] == "me" and cmp2[c] != "me"],
                        gap_closed=round(closed, 3), missed=fa.get("missed"), status=fa.get("status")))
    out.sort(key=lambda r: (-r["net"], -r["gap_closed"], -r["games_left"], r["add"]))
    return out[:n]


def this_week_block(state, by, me_now, opp_now, opp_rem, by_value, fas, sched, date, avail, lines):
    """M8 on the morning's roster and pool: every free agent scored, best first, each with the season cost of his drop
    (co_gm.waiver_pairs' measure: expected weekly categories against the other eleven teams, season CV)."""
    drops = swap_candidates(by_value) if by_value else []
    if not drops or not fas:
        return dict(status="no drop candidate" if not drops else "no free agent", drops=drops, rows=[], no_games=[],
                    pool_size=len(fas), drop_alone={})
    scored = scan_this_week(me_now, opp_now, opp_rem, by_value, drops, fas, sched, date, avail, lines)
    rows = [r for r in scored if r["games"] > 0]
    no_games = sorted(r["add"] for r in scored if r["games"] == 0)
    cv = CG.arena.SEASON_CV
    ros = {t["seat"]: [by[p["player"]] for p in t["players"] if p["slot"] != "IL" and p["player"] in by] for t in state["teams"]}
    opp = [CG.arena.team_week_model(r, cv) for s, r in ros.items() if s != CG.OWNER_SEAT]
    mine = ros[CG.OWNER_SEAT]
    base = CG.pwins(CG.arena.team_week_model(mine, cv), opp)
    for r in rows:
        swapped = [x for x in mine if x["player"] != r["drop"]] + [by[r["add"]]]
        r["season_d_ecw"] = round(CG.pwins(CG.arena.team_week_model(swapped, cv), opp) - base, 4)
    return dict(status="ran", drops=drops, rows=rows, no_games=no_games, pool_size=len(fas),
                drop_alone={d: round(x, 4) for d, x in
                            scan_drop_alone(me_now, opp_now, opp_rem, by_value, drops, sched, date, avail, lines).items()})


# ---------------------------------------------------------------- Yahoo through Flaim (A, D)
def load_pull(path):
    """(pull, reason): the pinned Flaim pull, or None and why not."""
    if not path or not os.path.isfile(path):
        return None, f"no Yahoo pull file ({os.path.basename(path) if path else 'none named'})"
    try:
        pull = json.load(open(path, encoding="utf-8"))
    except (ValueError, OSError) as e:
        return None, f"{os.path.basename(path)} is unreadable ({type(e).__name__})"
    if not isinstance(pull, dict) or pull.get("source") != "flaim":
        return None, f"{os.path.basename(path)} is not a Flaim pull"
    return pull, None


def yahoo_name(team, pull):
    """The team's name on Yahoo: its league-state name when a pulled roster carries it, otherwise the one pulled
    roster holding more than half of the team's players (a team renamed since the state was written)."""
    rosters = list((pull.get("rosters") or {}).values())
    if any(r.get("teamName") == team["name"] for r in rosters):
        return team["name"]
    mine = {LI.norm(p["player"]) for p in team["players"]}
    hits = sorted(((sum(1 for p in r.get("players", []) if LI.norm(_alias(p["name"])) in mine), r.get("teamName"))
                   for r in rosters), reverse=True)
    if hits and 2 * hits[0][0] > len(mine) and (len(hits) == 1 or hits[1][0] < hits[0][0]):
        return hits[0][1]
    return team["name"]


def _alias(name):
    return FL.LL.ALIASES.get(name, name)


def yahoo_to_date(pull, wk, me_t, opp_t):
    """(my totals, opponent totals, games remaining {me, opp}, Yahoo names {me, opp}, reason): Yahoo's week totals
    (M2), or Nones and why."""
    md = (pull.get("matchups") or {}).get(str(wk))
    if not md:
        return None, None, None, None, f"the Yahoo pull has no week {wk} matchup"
    names = dict(me=yahoo_name(me_t, pull), opp=yahoo_name(opp_t, pull))
    me, opp = FL.find_sides(md, names["me"], names["opp"])
    if me is None:
        return None, None, None, None, f"no week {wk} Yahoo matchup names both {names['me']} and {names['opp']}"
    try:
        return (FL.side_totals(me), FL.side_totals(opp), dict(me=me.get("gamesRemaining"), opp=opp.get("gamesRemaining")),
                names, None)
    except FL.PullError as e:
        return None, None, None, None, f"Yahoo's week {wk} totals could not be read: {e}"


def yahoo_free_agents(entries, pool):
    """Yahoo's available-player list against the season pool (M7): (scored, out, unknown_status, not_projected).
    A letter the kit does not tier is set aside first, never guessed; then out (availability 0); then unresolved."""
    res, _ = LI.resolve([e["name"] for e in entries], pool, {})
    scored, out, unknown, notp = [], [], [], []
    for e in entries:
        st = e.get("status") or None
        item = dict(name=e["name"], team=CG.TEAM_CODE.get(e.get("team"), e.get("team")), status=st)
        if st not in status_feed.TIERS:
            unknown.append(item)
        elif status_feed.TIERS[st][1] <= 0:
            out.append(item)
        elif e["name"] not in res:
            notp.append(item)
        else:
            scored.append(dict(item, player=res[e["name"]], availability=status_feed.TIERS[st][1],
                               positions=[x.strip() for x in (e.get("position") or "").split(",") if x.strip()]))
    return scored, out, unknown, notp


# ---------------------------------------------------------------- the record
def _sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if p and os.path.exists(p) else None


def _status(status_dir, date):
    files = sorted(f for f in glob.glob(os.path.join(status_dir, "status_*.json"))
                   if os.path.basename(f)[len("status_"):-len(".json")] <= date)
    return (json.load(open(files[-1], encoding="utf-8")), files[-1]) if files else ({"rows": []}, None)


def _sched(games, days):
    out = {d: set() for d in days}
    for d, v, h in games:
        if d in out:
            out[d] |= {CG.TEAM_CODE.get(v, v), CG.TEAM_CODE.get(h, h)}
    return out


def _r(x, nd):
    return None if x is None else round(x, nd)


def build(date, paths):
    state = json.load(open(paths["state"], encoding="utf-8"))
    sched_rec = json.load(open(paths["schedule"], encoding="utf-8"))
    games = CG.load_games(paths["games"])
    wk, ws, we = CG.week_of(date)
    opp_seat = next((o["seat"] for o in sched_rec["owner_opponents"] if o["week"] == wk), None)
    me_t = next(t for t in state["teams"] if t["seat"] == CG.OWNER_SEAT)
    opp_t = next((t for t in state["teams"] if t["seat"] == opp_seat), None)
    if opp_t is None:
        raise ValueError(f"no opponent for week {wk} (seat {opp_seat}) in the league state")
    P, by = CG.load_pool()
    zsum = lambda n: sum(by[n]["z"][c] for c in CG.CATS)

    unpooled = []

    def active(t):
        out = []
        for p in t["players"]:
            if p["slot"] == "IL":
                continue
            if p["player"] not in by:
                unpooled.append(p["player"]); continue
            out.append(dict(player=p["player"], team=p["yahoo_nba_team"], positions=p["positions"],
                            value=zsum(p["player"]), adj=CG.hoops.adj_value(by[p["player"]], ())))
        return out
    mine, theirs = active(me_t), active(opp_t)

    # to date: the week's days through yesterday; a day with scheduled games and no box-score file is missing
    td_days = days_to_date(date, ws)
    sched_td = _sched(games, td_days)
    boxes, recs, missing, read = {}, {}, [], []
    for d in td_days:
        f = os.path.join(paths["actuals"], f"{d}.json")
        if os.path.exists(f):
            recs[d] = json.load(open(f, encoding="utf-8"))
            boxes[d] = played(recs[d], names=list(by)); read.append(d)
        elif sched_td[d]:
            missing.append(d)

    # A: Yahoo's own week totals are the column when the pull carries this matchup; the rebuild is the cross-check
    pull, why = load_pull(paths.get("yahoo_pull"))
    pull_why = why
    y_me = y_opp = y_left = y_names = None
    if pull is not None:
        y_me, y_opp, y_left, y_names, why = yahoo_to_date(pull, wk, me_t, opp_t)
    # the rebuild reads each day's Yahoo lineup where one is pinned this week, today's roster otherwise
    lineups = week_lineups(paths.get("yahoo_pull"), ws, date)
    on_yahoo = y_names or {s: (yahoo_name(t, pull) if pull is not None else t["name"]) for s, t in (("me", me_t), ("opp", opp_t))}
    me_td = to_date(mine, boxes, lineups.get(on_yahoo["me"]), recs)
    opp_td = to_date(theirs, boxes, lineups.get(on_yahoo["opp"]), recs)
    if y_me is not None:
        diffs = [dict(side=side, stat=k, yahoo=y[k], rebuild=r["totals"][k])
                 for side, y, r in (("me", y_me, me_td), ("opp", y_opp, opp_td)) for k in STATS if y[k] != r["totals"][k]]
        src = dict(source="yahoo", reason=None, rebuild_agrees=not diffs, differences=diffs, yahoo_games_remaining=y_left,
                   yahoo_names=y_names)
        me_now, opp_now = y_me, y_opp
    else:
        src = dict(source="rebuild", reason=why, rebuild_agrees=None, differences=[], yahoo_games_remaining=None,
                   yahoo_names=None)
        me_now, opp_now = me_td["totals"], opp_td["totals"]

    # remaining: today through the week's last day, status availability, the ten-slot fill
    rem_days = days_remaining(date, we)
    sched = _sched(games, rem_days)
    status, status_file = _status(paths["status"], date)
    avail = {r["player"]: r["availability"] for r in status.get("rows", [])}
    lines = {p["player"]: p for p in P}
    me_rem, opp_rem = remaining(mine, sched, avail, lines), remaining(theirs, sched, avail, lines)
    me_fin, opp_fin = add(me_now, me_rem["totals"]), add(opp_now, opp_rem["totals"])
    v = dict(me_td=cat_values(me_now), opp_td=cat_values(opp_now),
             me_fin=cat_values(me_fin), opp_fin=cat_values(opp_fin))
    lead_td, lead = compare(v["me_td"], v["opp_td"]), compare(v["me_fin"], v["opp_fin"])
    nd = lambda c, fin: 3 if c in ("FG%", "FT%") else (1 if fin else 0)
    chance = cat_chances(me_now, me_rem, opp_now, opp_rem)  # M8
    cats = [dict(cat=c, me_to_date=_r(v["me_td"][c], nd(c, False)), opp_to_date=_r(v["opp_td"][c], nd(c, False)),
                 me_final=_r(v["me_fin"][c], nd(c, True)), opp_final=_r(v["opp_fin"][c], nd(c, True)),
                 leader_to_date=lead_td[c], leader=lead[c], p_win=round(chance[c], 4),
                 margin=_r(margin(c, v["me_fin"][c], v["opp_fin"][c]), 3 if c in ("FG%", "FT%") else 1)) for c in CATS]

    def games_block(td, rem, roster):
        return dict(to_date_counted=sum(len(x["counted"]) for x in td["days"].values()),
                    to_date_benched=[[d, n] for d, x in sorted(td["days"].items()) for n in x["benched"]],
                    remaining_uncapped=sum(1 for d in sched for r in roster if r["team"] in sched[d]),
                    remaining_started=sum(rem["games"].values()), remaining_by_player=rem["games"])

    # pickups (M6, M7)
    left = CG.games_left(games, date, we)
    by_value = [dict(r, value=r["adj"]) for r in mine]
    cands = drop_candidates(by_value, left)
    fa_list = ((pull or {}).get("free_agents") or {}).get("freeAgents")
    pool = dict(source="yahoo" if fa_list is not None else "kit",
                reason=None if fa_list is not None else (pull_why or "the Yahoo pull carries no available-player list"),
                listed=len(fa_list) if fa_list is not None else None,
                ordering=((pull or {}).get("free_agents") or {}).get("ordering"),
                out=[], unknown_status=[], not_projected=[], skipped=[], kit_pool_not_listed=None)
    pick = dict(status="no finished low-value player", drop_candidates=cands, next_finish=next_finish(by_value, sched),
                top=[], pool_size=0, drop=None, pool=pool)
    # the pool is built every morning (M8 scans before anyone finishes); M7's scan still runs only on a finished player
    rostered = {p["player"] for t in state["teams"] for p in t["players"]}
    veto = CG.hoops.do_not_draft()
    recent = _recent_boxes(paths["actuals"], date, names=list(by))
    kit_free = [p for p in P if p["player"] not in rostered and p["player"] not in veto and CG.hoops.availability(p) > 0]
    fas, fa_avail = [], {}
    if fa_list is not None:
        scored, pool["out"], pool["unknown_status"], pool["not_projected"] = yahoo_free_agents(fa_list, P)
        for y in scored:
            n, p = y["player"], by[y["player"]]
            why_skip = ("rostered in the league state" if n in rostered else "on the do-not-draft list" if n in veto
                        else "out in the kit pool" if CG.hoops.availability(p) <= 0 else None)
            if why_skip:
                pool["skipped"].append(dict(name=y["name"], team=y["team"], status=y["status"], reason=why_skip)); continue
            team, missed = _last_team_game(n, y["team"], recent)
            fas.append(dict(player=n, team=team, positions=y["positions"] or [x.strip() for x in p["pos"].split(",")],
                            value=zsum(n), adj=CG.hoops.adj_value(p, ()), missed=missed, status=y["status"]))
            fa_avail[n] = y["availability"]
        listed = {f["player"] for f in fas} | {y["player"] for y in scored}
        pool["kit_pool_not_listed"] = sum(1 for p in kit_free if p["player"] not in listed)
    else:
        for p in kit_free:
            team, missed = _last_team_game(p["player"], CG.TEAM_CODE.get(p["team"], p["team"]), recent)
            fas.append(dict(player=p["player"], team=team, positions=[x.strip() for x in p["pos"].split(",")],
                            value=zsum(p["player"]), adj=CG.hoops.adj_value(p, ()), missed=missed))
    if cands:
        drop = cands[0]["player"]
        top = rank_pickups(me_now, opp_fin, mine, drop, fas, sched, dict(avail, **fa_avail), lines)
        pick.update(status="ran", drop=cands[0], top=top, pool_size=len(fas))
    pick["this_week"] = this_week_block(state, by, me_now, opp_now, opp_rem, by_value, fas, sched, date,
                                        dict(avail, **fa_avail), lines)

    W = sum(1 for x in lead.values() if x == "me"); L = sum(1 for x in lead.values() if x == "opp")
    paths_used = dict(paths, status_file=status_file, pool=os.environ.get("SEASON_POOL") or "v69 preseason pool")
    return dict(
        date=date, week=wk, window=[ws, we], me=dict(name=me_t["name"], seat=me_t["seat"]),
        opponent=dict(name=opp_t["name"], seat=opp_t["seat"]), league_state_as_of=state.get("as_of"),
        to_date_days=read, missing_days=missing, to_date_source=src, remaining_days=[d for d in rem_days if sched[d]],
        status_file=os.path.basename(status_file) if status_file else None, cats=cats,
        projected=dict(wins=W, losses=L, ties=len(CATS) - W - L), exp_cats=sum(chance[c] for c in CATS),
        p_5plus=win_week_chance([chance[c] for c in CATS]),
        totals=dict(me=dict(to_date=me_now, rebuild_to_date=me_td["totals"],
                            remaining={k: round(x, 2) for k, x in me_rem["totals"].items()}),
                    opp=dict(to_date=opp_now, rebuild_to_date=opp_td["totals"],
                             remaining={k: round(x, 2) for k, x in opp_rem["totals"].items()})),
        games=dict(me=games_block(me_td, me_rem, mine), opp=games_block(opp_td, opp_rem, theirs)),
        rebuild_rosters=dict(me={d: x["roster"] for d, x in me_td["days"].items()},
                             opp={d: x["roster"] for d, x in opp_td["days"].items()}),
        pickups=pick, unpooled_active=sorted(set(unpooled)),
        method=dict(
            to_date=("Yahoo's week totals (get_matchups through Flaim, the morning pull); the box-score rebuild is the "
                     "cross-check" if src["source"] == "yahoo" else
                     "reconstructed from box scores (" + str(src["reason"]) + ")"),
            rebuild=("a day with Yahoo's pinned lineup counts its active slots (not BN, IL or IL+); any other day "
                     "counts every non-IL player on today's roster who played, ten per day by the daily-fill rule "
                     "when more played; each day's source is in rebuild_rosters"),
            projection="season-pool per-game line x each remaining game x today's status availability; ten-slot "
                       "daily fill; IL counts 0",
            percentages="total makes / total attempts, actual plus projected",
            drop="no game left this week and board value below the active roster's median",
            chances=("P(win) per category: the normal approximation on the final totals; to date fixed, the remaining "
                     "games' variance from the season per-game CV (FG%/FT%: binomial makes x PCT_MIX_INFL^2); the "
                     "shared weekly shock left out"),
            this_week=("each free agent in place of the below-median player whose drop helps most, from tomorrow; "
                       "ranked by the change in expected categories won (the sum of the nine changes in P(win)); "
                       "season cost = the change in expected weekly categories against the other eleven teams"),
            pickups=("Yahoo's available-player list (" + str(pool["listed"]) + " listed, Yahoo-wide ownership order), "
                     "each from today on at his Yahoo letter's availability" if pool["source"] == "yahoo" else
                     "every pooled free agent from today on") + ", ranked by projected category wins gained, then gap closed"),
        inputs={k: dict(path=os.path.relpath(p, KIT) if isinstance(p, str) and p.startswith(KIT) else p,
                        sha256=_sha(p) if isinstance(p, str) and os.path.isfile(p) else None)
                for k, p in paths_used.items()})


def _recent_boxes(actuals_dir, date, names=None):
    """The last LOOKBACK_DAYS of box-score records before `date`: [(date, {name: (team, dnp)}, teams played)], names
    as played() reads them."""
    index = BP.name_index(names) if names is not None else None
    out = []
    for i in range(1, LOOKBACK_DAYS + 1):
        d = (_d(date) - datetime.timedelta(days=i)).isoformat()
        f = os.path.join(actuals_dir, f"{d}.json")
        if os.path.exists(f):
            rec = json.load(open(f, encoding="utf-8"))
            who = {n: (p.get("team"), bool(p.get("dnp"))) for p in rec.get("players", []) for n in [_card_name(p, index)] if n}
            teams = {CG.TEAM_CODE.get(p.get("team"), p.get("team")) for p in rec.get("players", []) if p.get("team")}
            out.append((d, who, teams))
    return out


def _last_team_game(name, pool_team, recent):
    """(team, missed): the team from his most recent box score in the lookback (the pool's team otherwise), and the
    date of his team's latest game in the lookback if he did not play in it."""
    team = pool_team
    for d, who, _ in recent:
        if name in who and who[name][0]:
            team = CG.TEAM_CODE.get(who[name][0], who[name][0]); break
    for d, who, teams in recent:
        if team in teams:
            return team, (None if name in who and not who[name][1] else d)
    return team, None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", required=True)
    ap.add_argument("--out-dir", default=OUTDIR)
    ap.add_argument("--state", default=CG.STATE); ap.add_argument("--schedule", default=CG.SCHEDULE)
    ap.add_argument("--games", default=CG.GAMES); ap.add_argument("--actuals", default=ACTUALS)
    ap.add_argument("--status-dir", default=STATUS)
    ap.add_argument("--yahoo-pull", help="the Flaim pull (default data/source/flaim/pull_<date>.json)")
    a = ap.parse_args()
    pull = a.yahoo_pull or os.path.join(PULLS, f"pull_{a.date}.json")
    try:
        rec = build(a.date, dict(state=a.state, schedule=a.schedule, games=a.games, actuals=a.actuals, status=a.status_dir,
                                 yahoo_pull=pull))
    except Exception as e:  # noqa: BLE001 — any failure is one FAIL line; the deck then draws no card
        print(f"WEEK MATCHUP: FAIL — {a.date}: {type(e).__name__}: {e}")
        return 1
    os.makedirs(a.out_dir, exist_ok=True)
    out = os.path.join(a.out_dir, f"week_matchup_{a.date}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False); f.write("\n")
    p, pk = rec["projected"], rec["pickups"]
    pick = (f"pickups ran (drop {pk['drop']['player']}, {pk['pool_size']} free agents scored from the "
            f"{'Yahoo list' if pk['pool']['source'] == 'yahoo' else 'kit pool'})" if pk["status"] == "ran"
            else "pickups: no finished low-value player")
    src = rec["to_date_source"]
    tds = ("to date from Yahoo (" + ("rebuild agrees" if src["rebuild_agrees"] else
                                     f"rebuild differs on {len(src['differences'])} stat(s)") + ")"
           if src["source"] == "yahoo" else f"to date rebuilt ({src['reason']})")
    print(f"WEEK MATCHUP: PASS — {a.date}: week {rec['week']} vs {rec['opponent']['name']}; {tds}; to date "
          f"{len(rec['to_date_days'])} day(s), {len(rec['missing_days'])} missing; projected {p['wins']}-{p['losses']}-{p['ties']}; "
          f"{pick}; wrote {os.path.relpath(out, KIT) if out.startswith(KIT) else out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
