#!/usr/bin/env python3
"""The league table (owner 2026-10-23, "Build 1"): every team's nine-category totals per week and cumulative, the
category ranks, and a computed power ranking, from records the morning run already pulls.

Sources, in this order per week (M1, stated to the owner before the build):
  - a finished week: the Yahoo matchup block for that week in the latest pull dated AFTER the week ended (the
    finals); failing that, the kit rebuilds the week from box scores (data/actuals) and the pinned daily lineups,
    counting each team's active slots (BN/IL never count) and falling back to today's roster on a day with no
    pinned lineup, and says so (source "rebuild"; no Yahoo result for that week);
  - the week in progress: the day's pull (the latest pull on or before --date carrying that week).
Cumulative FG% and FT% are total makes over total attempts, never an average of weekly percentages.

Power ranking (M2): the all-play record. For each week, every team's totals are compared with all eleven others'
on the nine categories (TO reversed; a tie counts half); summed over the weeks, the win rate is the power score.
Beside it the actual matchup record (Yahoo's category scores summed) and the luck gap (actual rate - all-play rate).
Recomputed every morning.

    python3 scripts/league_table.py --date 2026-10-23 [--out-dir report/league]
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import co_gm as CG  # noqa: E402
import flaim_live as FL  # noqa: E402
import week_matchup as WM  # noqa: E402
import box_pull as BP  # noqa: E402
import run_ledger  # noqa: E402

KIT = CG.KIT
PULL_DIR = os.path.join(KIT, "data", "source", "flaim")
ACTUALS = os.path.join(KIT, "data", "actuals")
OUT = os.path.join(KIT, "report", "league")
WEEKS = os.path.join(KIT, "data", "weeks")
CATS = ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]
STATS = FL.STATS
COUNT = {"3PTM": "tpm", "PTS": "pts", "REB": "reb", "AST": "ast", "ST": "stl", "BLK": "blk", "TO": "tov"}
OWNER_SEAT = CG.OWNER_SEAT


class TableError(Exception):
    pass


def _fold(s):
    return BP.fold(str(s))


def cat_values(t):
    v = {"FG%": t["fgm"] / t["fga"] if t["fga"] else None, "FT%": t["ftm"] / t["fta"] if t["fta"] else None}
    v.update({c: t[k] for c, k in COUNT.items()})
    return v


def _cmp(c, a, b):
    """1 if a beats b in category c, -1 if b beats a, 0 tied (TO reversed; a missing percentage ties)."""
    if a is None or b is None or a == b:
        return 0
    better = a < b if c == "TO" else a > b
    return 1 if better else -1


def allplay(totals_by_team):
    """{team: {w, l, t, pct}}: each team against every other on the nine categories."""
    vals = {t: cat_values(x) for t, x in totals_by_team.items()}
    out = {t: dict(w=0, l=0, t=0) for t in vals}
    names = sorted(vals)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            for c in CATS:
                r = _cmp(c, vals[a][c], vals[b][c])
                if r == 1:
                    out[a]["w"] += 1; out[b]["l"] += 1
                elif r == -1:
                    out[a]["l"] += 1; out[b]["w"] += 1
                else:
                    out[a]["t"] += 1; out[b]["t"] += 1
    for t, r in out.items():
        n = r["w"] + r["l"] + r["t"]
        r["pct"] = (r["w"] + 0.5 * r["t"]) / n if n else None
    return out


def ranks(cats_by_team):
    """{team: {cat: rank}}, 1 = best; TO ascending; a tie shares the better rank; a missing value ranks last."""
    out = {t: {} for t in cats_by_team}
    for c in CATS:
        vals = [(t, v[c]) for t, v in cats_by_team.items()]
        have = [(t, x) for t, x in vals if x is not None]
        have.sort(key=lambda p: p[1], reverse=(c != "TO"))
        rank, prev = 0, None
        for i, (t, x) in enumerate(have):
            if x != prev:
                rank, prev = i + 1, x
            out[t][c] = rank
        for t, x in vals:
            if x is None:
                out[t][c] = len(have) + 1
    return out


def _seats(state):
    return {_fold(t["name"]): (t["name"], t["seat"], t.get("manager")) for t in state["teams"]}


def _not_started(side):
    """True when a side carries no stats at all: FGM/A and FTM/A read '/' (or empty) and every other cell is empty —
    Yahoo on day one of a week (owner 2026-10-26; the 10/26 FAIL). Anything else unreadable still raises, through
    flaim_live._pair, which stays strict for scoreboard_intake and week_matchup."""
    cats = side.get("categories") or []
    if not cats:
        return False
    for c in cats:
        v = c.get("value")
        if c.get("displayName") in ("FGM/A", "FTM/A"):
            if str(v if v is not None else "").strip() not in ("/", ""):
                return False
        elif str(v if v is not None else "").strip() != "":
            return False
    return True


def week_from_yahoo(block, state):
    """{team: {seat, totals, opponent, score, games_remaining}} from one Yahoo matchup block (all six matchups)."""
    seats = _seats(state)
    out = {}
    for m in block.get("matchups") or []:
        sides = [m.get("home"), m.get("away")]
        if not all(sides):
            raise TableError(f"matchup {m.get('matchupId')} lacks a side")
        names = []
        for s in sides:
            hit = seats.get(_fold(s.get("teamName")))
            if hit is None:
                raise TableError(f"Yahoo team {s.get('teamName')!r} is not in the league state")
            names.append(hit[0])
        for s, n, o in ((sides[0], names[0], names[1]), (sides[1], names[1], names[0])):
            blank = _not_started(s)
            if blank:
                totals = None   # no games yet: no totals, never an error (owner 2026-10-26)
            else:
                try:
                    totals = FL.side_totals(s)
                except FL.PullError as e:
                    raise TableError(str(e))
            sc = s.get("categoryScore") or {}
            score = dict(wins=sc.get("wins"), losses=sc.get("losses"), ties=sc.get("ties")) if sc else None
            out[n] = dict(seat=seats[_fold(n)][1], totals=totals, opponent=o, score=score,
                          games_remaining=s.get("gamesRemaining"), not_started=blank)
    # some sides played and some did not (a team idle on the first day): the idle ones carry zero totals
    if any(x["totals"] is not None for x in out.values()):
        for x in out.values():
            if x["totals"] is None:
                x["totals"] = {k: 0 for k in STATS}
    if len(out) != len(state["teams"]):
        raise TableError(f"the block names {len(out)} teams, the league state {len(state['teams'])}")
    return out


def load_pulls(pull_dir):
    """{date: pull} for every pull_<date>.json in the folder, oldest first."""
    out = {}
    for f in sorted(glob.glob(os.path.join(pull_dir, "pull_????-??-??.json"))):
        try:
            out[os.path.basename(f)[5:15]] = (os.path.basename(f), json.load(open(f, encoding="utf-8")))
        except (OSError, ValueError):
            continue
    return out


def _block(pull, week):
    return ((pull or {}).get("matchups") or {}).get(str(week))


def rebuild_week(week, ws, we, state, actuals_dir, pulls, date):
    """A finished week from box scores: each team's active slots per day (a pinned lineup for the day in any pull,
    else today's roster), summed through the week's last day. Returns (teams, days_read, days_missing)."""
    days, d = [], datetime.date.fromisoformat(ws)
    while d <= datetime.date.fromisoformat(we):
        days.append(d.isoformat()); d += datetime.timedelta(days=1)
    recs, read, missing = {}, [], []
    for day in days:
        f = os.path.join(actuals_dir, f"{day}.json")
        if os.path.exists(f):
            recs[day] = json.load(open(f, encoding="utf-8")); read.append(day)
        else:
            missing.append(day)
    # pinned daily lineups by Yahoo team name, latest pin of a day wins
    lineups = {}
    for pd, (fn, pull) in sorted(pulls.items()):
        for by_day in ((pull or {}).get("daily") or {}).values():
            for day, r in (by_day or {}).items():
                if ws <= day <= we and r.get("teamName"):
                    lineups.setdefault(r["teamName"], {})[day] = r
    teams = {}
    for t in state["teams"]:
        roster = [dict(player=p["player"], positions=p.get("positions") or [], value=0.0) for p in t["players"]
                  if (p.get("slot") or "") not in WM.BENCH_SLOTS]
        boxes = {day: WM.played(recs[day], names=[p["player"] for p in t["players"]]) for day in read}
        td = WM.to_date(roster, boxes, lineups.get(t["name"]), recs)
        teams[t["name"]] = dict(seat=t["seat"], totals=td["totals"], opponent=None, score=None, games_remaining=0,
                                days={day: x["roster"] for day, x in td["days"].items()})
    return teams, read, missing


def _calendar():
    """[(week, start, end)] from the kit's calendar (report/schedule/build_schedule.weeks)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("build_schedule", os.path.join(KIT, "report", "schedule", "build_schedule.py"))
    bs = importlib.util.module_from_spec(spec); spec.loader.exec_module(bs)
    return list(bs.weeks())


def _fingerprint(path):
    try:
        return hashlib.sha256(open(path, "rb").read()).hexdigest()
    except OSError:
        return None


def standings_of(pulls, date, state, weeks):
    """Owner 2026-10-26: Yahoo's standings from the latest pull on or before the date that carries them (M1), or None.
    vs_line (M2): category games ahead of 9th for the top eight, behind 8th (negative) for the rest. check (M4): each
    team's Yahoo W-L-T against the kit's summed score over its finished weeks."""
    cands = [(pd, fn, p["standings"]) for pd, (fn, p) in pulls.items() if pd <= date and (p or {}).get("standings")]
    if not cands:
        return None
    pd, fn, resp = cands[-1]
    by = {t["name"]: t for t in state["teams"]}
    po = CG.arena.PLAYOFF_TEAMS
    rows = []
    for x in sorted(resp["standings"], key=lambda x: int(x["rank"])):
        if x["name"] not in by:
            raise TableError(f"standings name {x['name']!r} is not a team in the league state")
        t = by[x["name"]]
        rows.append(dict(rank=int(x["rank"]), team=x["name"], seat=t["seat"], manager=t.get("manager"), mine=t["seat"] == OWNER_SEAT,
                         w=int(x["wins"]), l=int(x["losses"]), t=int(x["ties"] or 0), pct=float(x["percentage"]),
                         seed=x.get("playoffSeed"), waiver=x.get("waiverPriority"), faab=x.get("faabBalance")))
    gap = lambda a, b: ((a["w"] - b["w"]) + (b["l"] - a["l"])) / 2
    if len(rows) > po:
        for i, r in enumerate(rows):
            r["vs_line"] = gap(r, rows[po]) if i < po else -gap(rows[po - 1], r)
    fin = [w for w in weeks if w["status"] == "finished"]
    kit = {r["team"]: [0, 0, 0] for r in rows}
    for w in fin:
        for n, x in w["teams"].items():
            if x.get("score") and n in kit:
                kit[n] = [kit[n][0] + (x["score"]["wins"] or 0), kit[n][1] + (x["score"]["losses"] or 0), kit[n][2] + (x["score"]["ties"] or 0)]
    mism = [dict(team=r["team"], kit=kit[r["team"]], yahoo=[r["w"], r["l"], r["t"]]) for r in rows if kit[r["team"]] != [r["w"], r["l"], r["t"]]]
    return dict(pull=fn, pull_date=pd, playoff_teams=po, rows=rows,
                check=dict(finished_weeks=[w["week"] for w in fin], teams_checked=len(rows), mismatches=mism))


def standings_note(st):
    if not st:
        return "no Yahoo standings pinned"
    c = st["check"]
    return (f"standings {st['pull']}, " + (f"Yahoo W-L-T matches the kit's finished weeks for {c['teams_checked']} teams" if not c["mismatches"]
            else f"Yahoo W-L-T DIFFERS from the kit's finished weeks for {', '.join(m['team'] for m in c['mismatches'])}"))


def build(date, paths):
    state = json.load(open(paths["state"], encoding="utf-8"))
    pulls = load_pulls(paths["pull_dir"])
    wk, ws, we = CG.week_of(date)
    cal = {n: (s0.isoformat(), e0.isoformat()) for n, s0, e0 in _calendar()}
    weeks, inputs = [], {}
    for n in range(1, wk + 1):
        s, e = cal[n]
        if n < wk:
            # finished: the latest pull dated after the week's end that carries the week
            cands = [(pd, fn, _block(p, n)) for pd, (fn, p) in pulls.items() if pd > e and pd <= date and _block(p, n)]
            if cands:
                pd, fn, blk = cands[-1]
                teams = week_from_yahoo(blk, state)
                weeks.append(dict(week=n, window=[s, e], status="finished", source="yahoo", pull=fn, teams=teams))
                inputs[fn] = _fingerprint(os.path.join(paths["pull_dir"], fn))
            else:
                teams, read, missing = rebuild_week(n, s, e, state, paths.get("actuals") or ACTUALS, pulls, date)
                wk_rec = dict(week=n, window=[s, e], status="finished", source="rebuild", pull=None, teams=teams,
                              days_read=read, days_missing=missing)
                # owner 2026-10-26 (M3): a rebuilt week carries no Yahoo score; the verified week record has it
                rf = os.path.join(paths["weeks"], f"week_{n}.json") if paths.get("weeks") else None
                if rf and os.path.exists(rf):
                    scores = {t: x.get("yahoo_score") for t, x in json.load(open(rf, encoding="utf-8"))["teams"].items()}
                    lacking = sorted(t for t in teams if not scores.get(t))
                    if lacking:
                        raise TableError(f"week_{n}.json has no yahoo_score for {lacking}")
                    for t, x in teams.items():
                        x["score"] = {k: scores[t][k] for k in ("wins", "losses", "ties")}
                    wk_rec["score_source"] = os.path.basename(rf)
                    inputs[os.path.basename(rf)] = _fingerprint(rf)
                weeks.append(wk_rec)
                for day in read:
                    inputs[f"actuals/{day}.json"] = _fingerprint(os.path.join(paths.get("actuals") or ACTUALS, f"{day}.json"))
        else:
            cands = [(pd, fn, _block(p, n)) for pd, (fn, p) in pulls.items() if s <= pd <= date and _block(p, n)]
            if not cands:
                weeks.append(dict(week=n, window=[s, e], status="in_progress", source="none", pull=None, teams={}))
                continue
            pd, fn, blk = cands[-1]
            teams = week_from_yahoo(blk, state)
            started = any(x["totals"] is not None for x in teams.values())
            weeks.append(dict(week=n, window=[s, e], status="in_progress" if started else "not_started", source="yahoo",
                              pull=fn, teams=teams))
            inputs[fn] = _fingerprint(os.path.join(paths["pull_dir"], fn))
    # cumulative totals, ranks, all-play and actual records
    cum, ap_sum, act = {}, {}, {}
    for t in state["teams"]:
        cum[t["name"]] = dict(seat=t["seat"], manager=t.get("manager"), mine=t["seat"] == OWNER_SEAT,
                              totals={k: 0 for k in STATS}, weeks=0)
        ap_sum[t["name"]] = dict(w=0, l=0, t=0); act[t["name"]] = dict(w=0, l=0, t=0)
    for w in weeks:
        if not w["teams"] or w["status"] == "not_started":
            continue
        ap = allplay({n: x["totals"] for n, x in w["teams"].items()})
        w["allplay"] = ap
        for n, x in w["teams"].items():
            c = cum[n]
            c["totals"] = {k: c["totals"][k] + x["totals"][k] for k in STATS}; c["weeks"] += 1
            for k in ("w", "l", "t"):
                ap_sum[n][k] += ap[n][k]
            if x.get("score"):
                act[n]["w"] += x["score"]["wins"] or 0; act[n]["l"] += x["score"]["losses"] or 0; act[n]["t"] += x["score"]["ties"] or 0
    for n, c in cum.items():
        c["cats"] = cat_values(c["totals"])
    rk = ranks({n: c["cats"] for n, c in cum.items()})
    for n, c in cum.items():
        c["ranks"] = rk[n]
    power = []
    for n, c in cum.items():
        a = ap_sum[n]; na = a["w"] + a["l"] + a["t"]
        pct = (a["w"] + 0.5 * a["t"]) / na if na else None
        r = act[n]; nr = r["w"] + r["l"] + r["t"]
        apct = (r["w"] + 0.5 * r["t"]) / nr if nr else None
        power.append(dict(team=n, seat=c["seat"], manager=c["manager"], mine=c["mine"], allplay=dict(a, pct=pct),
                          actual=r if nr else None, actual_pct=apct, luck=(apct - pct) if (apct is not None and pct is not None) else None))
    power.sort(key=lambda x: (-(x["allplay"]["pct"] if x["allplay"]["pct"] is not None else -1), x["seat"]))
    for i, x in enumerate(power):
        x["rank"] = i + 1
    return dict(date=date, week=wk, window=[ws, we], league_state_as_of=state.get("as_of"), weeks=weeks, cumulative=cum,
                power=power, standings=standings_of(pulls, date, state, weeks),
                method=dict(sources="a finished week: Yahoo's block from the latest pull after the week's end, else the box-score "
                                    "rebuild of each team's active slots (pinned lineups, else today's roster); the week in "
                                    "progress: the day's pull",
                            cumulative="totals summed over the weeks; FG% and FT% as total makes over total attempts",
                            power="all-play: every team against all eleven others on the nine categories each week, TO "
                                  "reversed, a tie half; power = cumulative all-play win rate; luck = actual category "
                                  "win rate (Yahoo's scores) minus the all-play rate"),
                inputs=dict(pulls=inputs, state=dict(path=os.path.relpath(paths["state"], KIT) if paths["state"].startswith(KIT) else paths["state"],
                                                     sha256=_fingerprint(paths["state"]))))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--state", default=CG.STATE); ap.add_argument("--pull-dir", default=PULL_DIR)
    ap.add_argument("--actuals", default=ACTUALS); ap.add_argument("--out-dir", default=OUT)
    ap.add_argument("--weeks", default=WEEKS, help="the verified week records (scoreboard_intake), for a rebuilt week's score")
    ap.add_argument("--ledger", default=run_ledger.LEDGER, help="run-ledger path; '' records no row")
    a = ap.parse_args()
    led = lambda v, d: run_ledger.standalone_record("league_table", v, d, ledger=a.ledger) if a.ledger else None
    try:
        rec = build(a.date, dict(state=a.state, pull_dir=a.pull_dir, actuals=a.actuals, weeks=a.weeks))
    except (TableError, ValueError, OSError) as e:
        print(f"LEAGUE TABLE: FAIL — {e}"); led("FAIL", str(e)[:200]); return 1
    os.makedirs(a.out_dir, exist_ok=True)
    out = os.path.join(a.out_dir, f"league_{a.date}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False); f.write("\n")
    srcs = ", ".join(f"wk{w['week']} not started (Yahoo shows no stats yet)" if w["status"] == "not_started"
                     else f"wk{w['week']} {w['status']} ({w['source']})" for w in rec["weeks"])
    top = rec["power"][0]
    me = next(x for x in rec["power"] if x["mine"])
    msg = (f"{a.date}: week {rec['week']}; {srcs}; power #1 {top['team']} ({top['allplay']['pct']:.3f}), you #{me['rank']} "
           f"({(me['allplay']['pct'] or 0):.3f}); {standings_note(rec['standings'])}; wrote {os.path.relpath(out, KIT) if out.startswith(KIT) else out}")
    print(f"LEAGUE TABLE: PASS — {msg}"); led("PASS", msg[:200])
    return 0


if __name__ == "__main__":
    sys.exit(main())
