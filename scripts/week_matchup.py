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
  M2 to date     a reconstruction, not Yahoo's figure (no record carries Yahoo's daily lineups; FantasyBot's matchup
                 outlook has no category totals and reads rival slots as BN/IL only): every non-IL player on the current
                 roster who played counts; on a day more than ten of a team's players played, the ten counted are the
                 brief's daily-fill rule (co_gm.daily_lineup: positions, then board value).
  M3 projection  season-pool per-game line (SEASON_POOL, the brief's blended lines) x each remaining game x today's
                 availability from the status file (no row: 1.0, the brief's rule); the same ten-slot fill each day;
                 IL counts 0 (D-IS-8).
  M4 percentages FG% and FT% are total makes / total attempts, actual plus projected; makes projected as line % x
                 attempts.
  M5 leader      higher final wins; TO lower wins; equal (or no attempts) is a tie. Point estimates, no probability.
  M6 drop        "finished" = 0 NBA games from today through the week's end; "lower valued" = board value
                 (hoops.adj_value, the brief's streaming measure) below the active roster's median.
  M7 pickups     every pooled free agent (not rostered, availability > 0, not on the do-not-draft list) added in place
                 of the finished player from today on; ranked by projected category wins gained (ties count half), then
                 by the share of each losing category's gap closed. A free agent absent from his team's last box score
                 in the past week is flagged, not dropped. Waiver players cannot be told apart from free agents.

    python3 scripts/week_matchup.py --date YYYY-MM-DD [--out-dir report/briefs]
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
import co_gm as CG  # noqa: E402

KIT = CG.KIT
OUTDIR = os.path.join(KIT, "report", "briefs")
ACTUALS = os.path.join(KIT, "data", "actuals")
STATUS = os.path.join(KIT, "data", "status")
CATS = ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]
STATS = ["fgm", "fga", "ftm", "fta", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"]
PICKUPS_SHOWN = 5
LOOKBACK_DAYS = 7  # how far back a free agent's last team game is looked for (the missed-game flag)


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


def played(rec):
    """{pool name: box line} for pooled players who played a regular-season game in one data/actuals record."""
    regular = {g["espn_id"] for g in rec.get("games", []) if g.get("season_type") == 2}
    return {p["pool_name"]: {k: p.get(k) or 0 for k in STATS} for p in rec.get("players", [])
            if p.get("pool_name") and not p.get("dnp") and p.get("game") in regular}


def _fill(players):
    """co_gm.daily_lineup over dicts with player, positions, value, availability: (counted names, benched names)."""
    lineup, bench = CG.daily_lineup(players)
    return [p for _, p in lineup], bench


def to_date(roster, days):
    """roster: [{player, positions, value}]; days: {date: {name: box}}. The counted totals under M2."""
    t, out = zero(), {}
    for d in sorted(days):
        who = [dict(r, availability=1.0) for r in roster if r["player"] in days[d]]
        counted, benched = _fill(who)
        for n in counted:
            t = add(t, days[d][n])
        out[d] = dict(counted=counted, benched=benched)
    return dict(totals=t, days=out)


def per_game(ln):
    return dict(fgm=ln["fg_pct"] * ln["fga"], fga=ln["fga"], ftm=ln["ft_pct"] * ln["fta"], fta=ln["fta"],
                tpm=ln["tpm"], pts=ln["pts"], reb=ln["reb"], ast=ln["ast"], stl=ln["stl"], blk=ln["blk"], tov=ln["tov"])


def remaining(roster, sched, avail, lines):
    """roster: [{player, team, positions, value}]; sched: {date: set of teams playing}; avail: {player: probability}
    (missing = 1.0); lines: {player: per-game line}. Expected totals under M3 and each player's projected starts."""
    t, games, started = {k: 0.0 for k in STATS}, {}, {}
    for d in sorted(sched):
        cand = [dict(r, availability=avail.get(r["player"], 1.0)) for r in roster if r["team"] in sched[d]]
        counted, _ = _fill(cand)
        started[d] = counted
        for n in counted:
            a, g = avail.get(n, 1.0), per_game(lines[n])
            t = {k: t[k] + g[k] * a for k in STATS}
            games[n] = games.get(n, 0) + 1
    return dict(totals=t, games=games, started=started)


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
                        gap_closed=round(closed, 3), missed=fa.get("missed")))
    out.sort(key=lambda r: (-r["net"], -r["gap_closed"], -r["games_left"], r["add"]))
    return out[:n]


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
    boxes, missing, read = {}, [], []
    for d in td_days:
        f = os.path.join(paths["actuals"], f"{d}.json")
        if os.path.exists(f):
            boxes[d] = played(json.load(open(f, encoding="utf-8"))); read.append(d)
        elif sched_td[d]:
            missing.append(d)
    me_td, opp_td = to_date(mine, boxes), to_date(theirs, boxes)

    # remaining: today through the week's last day, status availability, the ten-slot fill
    rem_days = days_remaining(date, we)
    sched = _sched(games, rem_days)
    status, status_file = _status(paths["status"], date)
    avail = {r["player"]: r["availability"] for r in status.get("rows", [])}
    lines = {p["player"]: p for p in P}
    me_rem, opp_rem = remaining(mine, sched, avail, lines), remaining(theirs, sched, avail, lines)
    me_fin, opp_fin = add(me_td["totals"], me_rem["totals"]), add(opp_td["totals"], opp_rem["totals"])
    v = dict(me_td=cat_values(me_td["totals"]), opp_td=cat_values(opp_td["totals"]),
             me_fin=cat_values(me_fin), opp_fin=cat_values(opp_fin))
    lead_td, lead = compare(v["me_td"], v["opp_td"]), compare(v["me_fin"], v["opp_fin"])
    nd = lambda c, fin: 3 if c in ("FG%", "FT%") else (1 if fin else 0)
    cats = [dict(cat=c, me_to_date=_r(v["me_td"][c], nd(c, False)), opp_to_date=_r(v["opp_td"][c], nd(c, False)),
                 me_final=_r(v["me_fin"][c], nd(c, True)), opp_final=_r(v["opp_fin"][c], nd(c, True)),
                 leader_to_date=lead_td[c], leader=lead[c],
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
    pick = dict(status="no finished low-value player", drop_candidates=cands, next_finish=next_finish(by_value, sched),
                top=[], pool_size=0, drop=None)
    if cands:
        rostered = {p["player"] for t in state["teams"] for p in t["players"]}
        veto = CG.hoops.do_not_draft()
        recent = _recent_boxes(paths["actuals"], date)
        fas = []
        for p in P:
            if p["player"] in rostered or p["player"] in veto or CG.hoops.availability(p) <= 0:
                continue
            team, missed = _last_team_game(p["player"], CG.TEAM_CODE.get(p["team"], p["team"]), recent)
            fas.append(dict(player=p["player"], team=team, positions=[x.strip() for x in p["pos"].split(",")],
                            value=zsum(p["player"]), adj=CG.hoops.adj_value(p, ()), missed=missed))
        drop = cands[0]["player"]
        top = rank_pickups(me_td["totals"], opp_fin, mine, drop, fas, sched, avail, lines)
        pick.update(status="ran", drop=cands[0], top=top, pool_size=len(fas))

    W = sum(1 for x in lead.values() if x == "me"); L = sum(1 for x in lead.values() if x == "opp")
    paths_used = dict(paths, status_file=status_file, pool=os.environ.get("SEASON_POOL") or "v69 preseason pool")
    return dict(
        date=date, week=wk, window=[ws, we], me=dict(name=me_t["name"], seat=me_t["seat"]),
        opponent=dict(name=opp_t["name"], seat=opp_t["seat"]), league_state_as_of=state.get("as_of"),
        to_date_days=read, missing_days=missing, remaining_days=[d for d in rem_days if sched[d]],
        status_file=os.path.basename(status_file) if status_file else None, cats=cats,
        projected=dict(wins=W, losses=L, ties=len(CATS) - W - L),
        totals=dict(me=dict(to_date=me_td["totals"], remaining={k: round(x, 2) for k, x in me_rem["totals"].items()}),
                    opp=dict(to_date=opp_td["totals"], remaining={k: round(x, 2) for k, x in opp_rem["totals"].items()})),
        games=dict(me=games_block(me_td, me_rem, mine), opp=games_block(opp_td, opp_rem, theirs)),
        pickups=pick, unpooled_active=sorted(set(unpooled)),
        method=dict(
            to_date="reconstructed from box scores: every non-IL rostered player who played; ten per day by the "
                    "daily-fill rule when more played (Yahoo's own lineups are not in any record)",
            projection="season-pool per-game line x each remaining game x today's status availability; ten-slot "
                       "daily fill; IL counts 0",
            percentages="total makes / total attempts, actual plus projected",
            drop="no game left this week and board value below the active roster's median",
            pickups="every pooled free agent from today on, ranked by projected category wins gained, then gap closed"),
        inputs={k: dict(path=os.path.relpath(p, KIT) if isinstance(p, str) and p.startswith(KIT) else p,
                        sha256=_sha(p) if isinstance(p, str) and os.path.isfile(p) else None)
                for k, p in paths_used.items()})


def _recent_boxes(actuals_dir, date):
    """The last LOOKBACK_DAYS of box-score records before `date`: [(date, {pool name: (team, dnp)}, teams played)]."""
    out = []
    for i in range(1, LOOKBACK_DAYS + 1):
        d = (_d(date) - datetime.timedelta(days=i)).isoformat()
        f = os.path.join(actuals_dir, f"{d}.json")
        if os.path.exists(f):
            rec = json.load(open(f, encoding="utf-8"))
            who = {p["pool_name"]: (p.get("team"), bool(p.get("dnp"))) for p in rec.get("players", []) if p.get("pool_name")}
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
    a = ap.parse_args()
    try:
        rec = build(a.date, dict(state=a.state, schedule=a.schedule, games=a.games, actuals=a.actuals, status=a.status_dir))
    except Exception as e:  # noqa: BLE001 — any failure is one FAIL line; the deck then draws no card
        print(f"WEEK MATCHUP: FAIL — {a.date}: {type(e).__name__}: {e}")
        return 1
    os.makedirs(a.out_dir, exist_ok=True)
    out = os.path.join(a.out_dir, f"week_matchup_{a.date}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False); f.write("\n")
    p, pk = rec["projected"], rec["pickups"]
    pick = (f"pickups ran (drop {pk['drop']['player']}, {pk['pool_size']} free agents scored)" if pk["status"] == "ran"
            else "pickups: no finished low-value player")
    print(f"WEEK MATCHUP: PASS — {a.date}: week {rec['week']} vs {rec['opponent']['name']}; to date "
          f"{len(rec['to_date_days'])} day(s), {len(rec['missing_days'])} missing; projected {p['wins']}-{p['losses']}-{p['ties']}; "
          f"{pick}; wrote {os.path.relpath(out, KIT) if out.startswith(KIT) else out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
