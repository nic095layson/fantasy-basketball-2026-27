#!/usr/bin/env python3
"""Minutes & role board (owner 2026-10-23, "what can we do today"): the in-season signal that stabilizes first.

For every player on the 12 rosters (league_state.json) and on Yahoo's available-player list (the morning pull), from
the regular-season box scores on disk (data/actuals, the same files and the same rules as season_lines.totals):

  games, minutes per game, starts, role         role = starter (started every game) / mixed / bench
  per-36 PTS REB AST STL BLK 3PM TOV, FG%, FT%  rates on the minutes actually played, beside the season line
  last-3 minutes vs the games before them       drawn only at TREND_MIN_GAMES or more; +-TREND_MIN minutes = up/down

What it is not: a projection. The season line (season_lines.py) stays the per-game line the board and the simulator
run on; this record shows the minutes and starts behind it, with the games count on every row, so a 1-game row reads
as a 1-game row. The pool CSV carries no minutes, so there is no preseason minutes expectation to compare against
(stated 2026-10-23); the trend is within-season only.

Output: report/form/form_<date>.json (+ .csv), rows by minutes per game descending. Red-first tests: test_form_board.py.

    python3 scripts/form_board.py --date 2026-10-23 [--actuals DIR] [--state FILE] [--pull FILE] [--pool CSV] [--out-dir DIR] [--ledger PATH]
"""
import argparse
import csv
import datetime
import glob
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import co_gm as CG  # noqa: E402
import league_intake as LI  # noqa: E402
import run_ledger  # noqa: E402

KIT = CG.KIT
ACTUALS = os.path.join(KIT, "data", "actuals")
STATE = CG.STATE
PULL_DIR = os.path.join(KIT, "data", "source", "flaim")
POOL = os.path.join(KIT, "data", "season", "pool_season.csv")
OUT = os.path.join(KIT, "report", "form")
OWNER_SEAT = CG.OWNER_SEAT
BOX = ("pts", "fgm", "fga", "tpm", "ftm", "fta", "reb", "ast", "tov", "stl", "blk")
PER36 = ("pts", "reb", "ast", "stl", "blk", "tpm", "tov")
TREND_MIN_GAMES = 4      # a last-3 needs at least one game before it
TREND_MIN = 6.0          # minutes; display threshold, hand-set (declared 2026-10-23), nothing downstream reads it


class FormError(Exception):
    pass


def game_log(records):
    """{pool name (else the source name, flagged unpooled): [game, ...] in date order} from regular-season box scores,
    DNPs excluded — season_lines.totals' rules, kept per game instead of summed."""
    out = {}
    for rec in sorted(records, key=lambda r: r.get("date") or ""):
        regular = {g["espn_id"] for g in rec.get("games", []) if g.get("season_type") == 2}
        for p in rec.get("players", []):
            if p.get("dnp") or p.get("game") not in regular:
                continue
            key = p.get("pool_name") or p["name"]
            g = dict(date=rec.get("date"), min=p.get("min", 0) or 0, starter=bool(p.get("starter")),
                     team=p.get("team"), unpooled=p.get("pool_name") is None, source_name=p["name"])
            for k in BOX:
                g[k] = p.get(k, 0) or 0
            out.setdefault(key, []).append(g)
    return out


def summarize(log):
    """games, mpg, starts, role, per-36 rates, FG/FT, the last-3 minutes trend (None under TREND_MIN_GAMES)."""
    n = len(log)
    mins = [g["min"] for g in log]
    tot_min = sum(mins)
    tot = {k: sum(g[k] for g in log) for k in BOX}
    s = dict(games=n, mpg=round(tot_min / n, 1) if n else None, starts=sum(1 for g in log if g["starter"]),
             minutes=mins, team=(log[-1].get("team") if log else None))
    s["role"] = None if not n else ("starter" if s["starts"] == n else "bench" if s["starts"] == 0 else "mixed")
    s["per36"] = {k: round(tot[k] * 36 / tot_min, 3) for k in PER36} if tot_min else {}
    s["fg"] = dict(made=tot["fgm"], att=tot["fga"], pct=round(tot["fgm"] / tot["fga"], 4) if tot["fga"] else None)
    s["ft"] = dict(made=tot["ftm"], att=tot["fta"], pct=round(tot["ftm"] / tot["fta"], 4) if tot["fta"] else None)
    s["per_game"] = {k: round(tot[k] / n, 2) for k in PER36} if n else {}
    if n >= TREND_MIN_GAMES:
        last3, prior = mins[-3:], mins[:-3]
        s["last3_mpg"] = round(sum(last3) / 3, 1)
        s["prior_mpg"] = round(sum(prior) / len(prior), 1)
        d = s["last3_mpg"] - s["prior_mpg"]
        s["trend"] = "up" if d >= TREND_MIN else "down" if d <= -TREND_MIN else "flat"
    else:
        s["last3_mpg"] = s["prior_mpg"] = s["trend"] = None
    return s


def _fingerprint(path):
    try:
        return hashlib.sha256(open(path, "rb").read()).hexdigest()[:12]
    except OSError:
        return None


def latest_pull(pull_dir, date):
    cands = sorted(f for f in glob.glob(os.path.join(pull_dir, "pull_????-??-??.json")) if os.path.basename(f)[5:15] <= date)
    return cands[-1] if cands else None


def build(date, paths):
    state = json.load(open(paths["state"], encoding="utf-8"))
    files = sorted(glob.glob(os.path.join(paths["actuals"], "*.json")))
    records = [json.load(open(f, encoding="utf-8")) for f in files]
    log = game_log(records)
    days = sorted({g["date"] for gs in log.values() for g in gs if g["date"]})
    pull = json.load(open(paths["pull"], encoding="utf-8")) if paths.get("pull") and os.path.exists(paths["pull"]) else None
    rows, seen = [], set()
    by_norm0 = {}
    for k in log:
        by_norm0.setdefault(LI.norm(k), k)
    for t in state["teams"]:
        for p in t["players"]:
            name = p["player"]
            box_name = name if name in log else by_norm0.get(LI.norm(name))
            s = summarize(log.get(box_name, []) if box_name else [])
            rows.append(dict(name=name, yahoo_name=p.get("yahoo_name") or name, box_name=box_name, owner=t["name"], seat=t["seat"],
                             mine=t["seat"] == OWNER_SEAT, fa=False, slot=p.get("slot"), status=p.get("status"),
                             nba=s.pop("team") or p.get("pool_team") or p.get("yahoo_nba_team"), **s))
            seen.add(name)
    fa_list = ((pull or {}).get("free_agents") or {}).get("freeAgents") or []
    # Yahoo's spelling -> the pool's: the season pool CSV plus every name the box scores know (a free agent with no
    # regular-season game yet gets a 0-game row, as a rostered one does; only a name in neither list is unresolved)
    pool_names = set()
    if paths.get("pool") and os.path.exists(paths["pool"]):
        with open(paths["pool"], encoding="utf-8") as f:
            pool_names = {r["player"] for r in csv.DictReader(f)}
    # the pool's spelling wins; a box-score name the pool spells differently ("Kelly Oubre" for "Kelly Oubre Jr.",
    # an alias the box puller missed) is looked up by its folded form, so the games are his and the row is pooled
    by_norm = {}
    for k in log:
        by_norm.setdefault(LI.norm(k), k)
    pool_norm = {LI.norm(n) for n in pool_names}
    cands = sorted(pool_names) + sorted(k for k in log if LI.norm(k) not in pool_norm)
    res, _ = LI.resolve([e["name"] for e in fa_list], [dict(player=n) for n in cands], {})
    unresolved = []
    for e in fa_list:
        name = res.get(e["name"])
        if name is None:
            unresolved.append(e["name"]); continue
        if name in seen:
            continue
        box_name = name if name in log else by_norm.get(LI.norm(name))
        s = summarize(log.get(box_name, []) if box_name else [])
        rows.append(dict(name=name, yahoo_name=e["name"], box_name=box_name, owner=None, seat=None, mine=False, fa=True, slot=None,
                         status=e.get("status"), nba=s.pop("team") or CG.TEAM_CODE.get(e.get("team"), e.get("team")), **s))
        seen.add(name)
    rows.sort(key=lambda r: (-(r["mpg"] or -1), -r["games"], r["name"]))
    claimed = {r["box_name"] for r in rows if r.get("box_name")}
    unpooled = sorted(n for n, gs in log.items() if gs and gs[0]["unpooled"] and n not in claimed)
    return dict(date=date, window=[days[0], days[-1]] if days else None, league_state_as_of=state.get("as_of"),
                pull=os.path.basename(paths["pull"]) if paths.get("pull") else None, rows=rows,
                fa_unresolved=unresolved, unpooled_with_games=unpooled,
                counts=dict(rostered=sum(1 for r in rows if not r["fa"]), free_agents=sum(1 for r in rows if r["fa"]),
                            with_games=sum(1 for r in rows if r["games"]), no_game=sum(1 for r in rows if not r["games"]),
                            days=len(days)),
                method=dict(source="regular-season box scores in data/actuals (season_lines.totals' rules, per game), "
                                   "DNPs excluded", rate_base=36, trend_min_games=TREND_MIN_GAMES, trend_min=TREND_MIN,
                            role="starter = started every game; bench = none; mixed otherwise (the box score's starter flag)",
                            not_a_projection="the season line stays the per-game line; minutes have no preseason expectation "
                                             "in the pool CSV, so the trend is within-season only"),
                inputs=dict(actuals={os.path.basename(f): _fingerprint(f) for f in files},
                            state=_fingerprint(paths["state"]), pull=_fingerprint(paths["pull"]) if paths.get("pull") else None,
                            pool=_fingerprint(paths["pool"]) if paths.get("pool") else None))


def write(rec, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    jp = os.path.join(out_dir, f"form_{rec['date']}.json")
    with open(jp, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False)
    cp = os.path.join(out_dir, f"form_{rec['date']}.csv")
    cols = ["name", "nba", "owner", "mine", "fa", "slot", "games", "mpg", "starts", "role", "last3_mpg", "prior_mpg", "trend"] + \
           [f"p36_{k}" for k in PER36] + ["fg_pct", "ft_pct"]
    with open(cp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for r in rec["rows"]:
            w.writerow(dict({c: r.get(c) for c in cols[:13]}, **{f"p36_{k}": r["per36"].get(k) for k in PER36},
                            fg_pct=r["fg"]["pct"], ft_pct=r["ft"]["pct"]))
    return jp


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--actuals", default=ACTUALS); ap.add_argument("--state", default=STATE)
    ap.add_argument("--pull", default=None, help="a Flaim pull with Yahoo's available list; default: the latest on or before --date")
    ap.add_argument("--pull-dir", default=PULL_DIR); ap.add_argument("--out-dir", default=OUT)
    ap.add_argument("--pool", default=POOL, help="season pool CSV, for Yahoo-name resolution (absent: box-score names only)")
    ap.add_argument("--ledger", default=run_ledger.LEDGER, help="run-ledger path; '' records no row")
    a = ap.parse_args()
    led = lambda v, d: run_ledger.standalone_record("form_board", v, d, ledger=a.ledger) if a.ledger else None
    try:
        pull = a.pull or latest_pull(a.pull_dir, a.date)
        rec = build(a.date, dict(actuals=a.actuals, state=a.state, pull=pull, pool=a.pool))
        jp = write(rec, a.out_dir)
    except (FormError, OSError, KeyError, ValueError) as e:
        print(f"FORM BOARD: FAIL — {e}"); led("FAIL", str(e)[:200]); return 1
    c = rec["counts"]
    msg = (f"{c['rostered']} rostered + {c['free_agents']} free agents, {c['with_games']} with games over {c['days']} box days"
           f"{' (' + rec['window'][0] + ' to ' + rec['window'][1] + ')' if rec['window'] else ''}; "
           f"({c['no_game']} without a game yet); {len(rec['fa_unresolved'])} Yahoo names in neither pool nor box scores; "
           f"{os.path.relpath(jp, KIT)}")
    print(f"FORM BOARD: PASS — {msg}"); led("PASS", msg[:200])
    return 0


if __name__ == "__main__":
    sys.exit(main())
