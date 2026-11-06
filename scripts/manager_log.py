#!/usr/bin/env python3
"""Per-manager behaviour log (owner 2026-10-22, "A and B": A records each manager's habits; B, feeding lineup diligence
to the simulator, waits for 4-6 weeks of data and the owner's word on the engine constant). Record only: nothing here
changes a line, a tag, a roster, a status tier or any engine value.

For one game day D it reads:
  - each team's locked Yahoo lineup for D (Flaim get_roster with as_of_date D), from the pinned pulls'
    "daily" block (flaim_live.keep_daily; the latest pin holding that team and day wins);
  - who played on D, from data/actuals/D.json (a box line with minutes; a DNP line is not a game);
  - the league's adds and drops (Flaim get_transactions), from this session's transcript, unioned by transaction id
    into data/managers/transactions.json (Yahoo keeps 30 days; the union keeps the season).

Per team and day it records:
  starts        players in an active slot who played
  best_starts   the most players who played that the ten active slots could hold, by Yahoo position eligibility
                (a matching, so a reshuffle that frees a slot counts); IL-slot players are never startable
  starts_lost   best_starts - starts: the engine's uniform daily-fill start rate, measured per manager
  benched_played, il_slots_used, il_played, and no_box_line (a player whose NBA team played but who has no box line:
  inactive, which ESPN's box omits, or a name the fold missed; named, never guessed)

data/managers/profile.json rolls every day file up per team (days, starts, best_starts, starts_lost, start_rate,
il_player_days, adds, drops) with its window. No priors from past seasons: the pinned history holds no lineups or
transactions (owner question open).

    python3 scripts/manager_log.py --date 2026-10-22 [--since ISO-TIME] [--transcript FILE] [--no-transactions]
Prints 'MANAGER LOG: PASS — ...' (or HALT naming what is missing) and writes data/managers/.
"""
import argparse
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
DECK = os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball")
sys.path.insert(0, os.path.join(DECK, "scripts"))
sys.path.insert(0, HERE)
from verify_rosters import norm  # noqa: E402
import league_live as LL  # noqa: E402

LEAGUE_KEY = "478.l.36464"
N_TEAMS = 12
PIN_DIR = os.path.join(KIT, "data", "source", "flaim")
ACTUALS = os.path.join(KIT, "data", "actuals")
OUT_DIR = os.path.join(KIT, "data", "managers")
ACTIVE_SLOTS = ["PG", "SG", "G", "SF", "PF", "F", "C", "C", "Util", "Util"]  # data/league_settings.json roster_positions
ELIGIBLE = {"PG": {"PG"}, "SG": {"SG"}, "G": {"PG", "SG"}, "SF": {"SF"}, "PF": {"PF"}, "F": {"SF", "PF"},
            "C": {"C"}, "Util": {"PG", "SG", "SF", "PF", "C"}}
NOT_ACTIVE = {"BN", "IL", "IL+"}


class LogError(Exception):
    pass


def _fold(name):
    return norm(LL.ALIASES.get(name, name) or "")


def played_index(actuals):
    """(folded names with a box line with minutes, folded names with any box line, NBA teams that played)."""
    played, seen, teams = set(), set(), set()
    for p in actuals.get("players") or []:
        names = {_fold(p["name"])} | ({_fold(p["pool_name"])} if p.get("pool_name") else set())
        seen |= names
        teams.add(p.get("team"))
        if not p.get("dnp") and (p.get("min") or 0) > 0:
            played |= names
    return played, seen, teams


def _best(players):
    """Most of these players (each a set of positions) the active slots can hold: bipartite matching (Kuhn)."""
    owner = [None] * len(ACTIVE_SLOTS)

    def place(i, tried):
        for s, slot in enumerate(ACTIVE_SLOTS):
            if s in tried or not (players[i] & ELIGIBLE[slot]):
                continue
            tried.add(s)
            if owner[s] is None or place(owner[s], tried):
                owner[s] = i
                return True
        return False

    return sum(place(i, set()) for i in range(len(players)))


def team_day(lineup, actuals, nba_team_of):
    """One team's record for the lineup's day. nba_team_of: {Yahoo name: NBA team} (the dated roster has none)."""
    played, seen, teams = played_index(actuals)
    starts, startable, benched, il_used, il_played, no_line = 0, [], [], 0, [], []
    for p in lineup["players"]:
        slot, name = p.get("selectedPosition") or "BN", p["name"]
        f = _fold(name)
        did = f in played
        if f not in seen and nba_team_of.get(name) in teams:
            no_line.append({"name": name, "slot": slot})
        if slot in ("IL", "IL+"):
            il_used += 1
            if did:
                il_played.append(name)
            continue
        if not did:
            continue
        startable.append({x.strip() for x in (p.get("position") or "").split(",") if x.strip()})
        if slot in NOT_ACTIVE:
            benched.append(name)
        else:
            starts += 1
    best = _best(startable)
    return {"team": lineup.get("teamName"), "owner": lineup.get("ownerName"), "starts": starts, "best_starts": best,
            "starts_lost": best - starts, "benched_played": benched, "il_slots_used": il_used, "il_played": il_played,
            "no_box_line": no_line}


def pinned_lineups(pin_dir, date):
    """{teamKey: lineup for date} from every pinned pull's daily block; a later pin wins."""
    out = {}
    for path in sorted(glob.glob(os.path.join(pin_dir, "pull_*.json"))):
        with open(path, encoding="utf-8") as f:
            daily = json.load(f).get("daily") or {}
        for key, days in daily.items():
            if date in days:
                out[key] = days[date]
    return out


def nba_teams(pin_dir):
    """{Yahoo name: NBA team} from the current rosters and available lists of every pin (later pins win)."""
    out = {}
    for path in sorted(glob.glob(os.path.join(pin_dir, "pull_*.json"))):
        with open(path, encoding="utf-8") as f:
            pull = json.load(f)
        for r in (pull.get("rosters") or {}).values():
            out.update({p["name"]: p.get("team") for p in r.get("players") or [] if p.get("team")})
    return out


def extract_moves(transcript, since=None):
    """Flaim get_transactions rows for this league from the transcript (entries at or after since)."""
    since = LL.since_instant(since)
    rows = []

    def walk(x):
        if isinstance(x, str):
            if '"transactions"' in x and LEAGUE_KEY in x:
                j = LL._loads(x)
                d = j.get("data") if isinstance(j, dict) and j.get("success") is True else None
                if isinstance(d, dict) and d.get("league_id") == LEAGUE_KEY and isinstance(d.get("transactions"), list):
                    rows.extend(d["transactions"])
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    with open(transcript, encoding="utf-8") as f:
        for line in f:
            if LEAGUE_KEY not in line or '\\"transactions\\"' not in line and '"transactions"' not in line:
                continue
            o = LL._loads(line)
            if o is not None and LL.recent(o, since):
                walk(o)
    return rows


def union_moves(old, new):
    """Rows of both, one per transaction id (the newer copy wins), newest first; and how many ids are new."""
    by_id = {r["transaction_id"]: r for r in old}
    fresh = sum(1 for r in {r["transaction_id"]: r for r in new} if r not in by_id)
    by_id.update({r["transaction_id"]: r for r in new})
    rows = sorted(by_id.values(), key=lambda r: (r.get("timestamp") or 0, r["transaction_id"]), reverse=True)
    return rows, fresh


def move_counts(rows):
    """{teamKey: adds, drops, moves} over completed rows (a trade counts as a move for each side)."""
    out = {}
    for r in rows:
        if r.get("status", "complete") != "complete":
            continue
        for t in r.get("team_ids") or []:
            c = out.setdefault(t, {"adds": 0, "drops": 0, "moves": 0})
            c["adds"] += len(r.get("players_added") or [])
            c["drops"] += len(r.get("players_dropped") or [])
            c["moves"] += 1
    return out


def _team_key(name):
    return (name or "").replace("\u2019", "'").casefold().strip()


def managers_by_team(state):
    """{folded team name: manager} from the league state, which names each league mate as the owner does (owner
    2026-10-28: "assign my 11 league mates to their team ... for their fantasy profiles")."""
    return {_team_key(t["name"]): t.get("manager") for t in (state or {}).get("teams", [])}


def team_manager(managers, team):
    return (managers or {}).get(_team_key(team))


def rollup(days, counts, managers=None):
    """Per-team totals over the day records, with the window they cover. Each team carries Yahoo's account name
    (owner) and the league mate's name from the league state (manager; None when the state does not hold the team)."""
    teams = {}
    for day in days:
        for key, rec in day["teams"].items():
            t = teams.setdefault(key, {"team": rec["team"], "owner": rec["owner"], "days": 0, "starts": 0,
                                       "best_starts": 0, "starts_lost": 0, "il_player_days": 0})
            t.update(team=rec["team"], owner=rec["owner"])
            t["days"] += 1
            for k in ("starts", "best_starts", "starts_lost"):
                t[k] += rec[k]
            t["il_player_days"] += rec["il_slots_used"]
    for key, t in teams.items():
        t["manager"] = team_manager(managers, t["team"])
        t["start_rate"] = t["starts"] / t["best_starts"] if t["best_starts"] else None
        c = counts.get(key, {})
        t["adds"], t["drops"], t["moves"] = c.get("adds", 0), c.get("drops", 0), c.get("moves", 0)
    dates = sorted(d["date"] for d in days)
    return {"window": {"first": dates[0] if dates else None, "last": dates[-1] if dates else None, "days": len(dates)},
            "teams": dict(sorted(teams.items(), key=lambda kv: int(kv[0].rsplit(".", 1)[-1])))}


def _load(path, default):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
        f.write("\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", required=True, help="the game day to log (Yahoo's day, the box-score date)")
    ap.add_argument("--since", help="count only transcript entries at or after this ISO time (the run's start)")
    ap.add_argument("--transcript", help="session transcript jsonl (default: the newest in the project dir)")
    ap.add_argument("--no-transactions", action="store_true", help="skip the transcript; keep the moves on record")
    ap.add_argument("--pin-dir", default=PIN_DIR)
    ap.add_argument("--out-dir", default=OUT_DIR)
    ap.add_argument("--actuals-dir", default=ACTUALS)
    a = ap.parse_args()

    notes = []
    tx_path = os.path.join(a.out_dir, "transactions.json")
    moves = _load(tx_path, {"rows": []})["rows"]
    if not a.no_transactions:
        try:
            got = extract_moves(a.transcript or LL.newest_transcript(), a.since)
        except (LL.PullError, OSError) as e:
            got = None
            notes.append(f"transactions not read ({e})")
        if got:
            moves, fresh = union_moves(moves, got)
            _dump(tx_path, {"league_key": LEAGUE_KEY, "source": "Flaim get_transactions (Yahoo, rolling 30 days), unioned by id",
                            "rows": moves})
            notes.append(f"{fresh} new move(s), {len(moves)} on record")
        elif got is not None:
            notes.append(f"no get_transactions response in the transcript; {len(moves)} move(s) on record")

    lineups = pinned_lineups(a.pin_dir, a.date)
    act_path = os.path.join(a.actuals_dir, f"{a.date}.json")
    halt = []
    if len(lineups) != N_TEAMS:
        halt.append(f"{len(lineups)} of {N_TEAMS} locked lineups for {a.date} in the pins")
    if not os.path.exists(act_path):
        halt.append(f"no box scores at {os.path.relpath(act_path, KIT) if act_path.startswith(KIT) else act_path}")
    if not halt:
        actuals = _load(act_path, {})
        teams_of = nba_teams(a.pin_dir)
        day = {"date": a.date, "box_scores": os.path.relpath(act_path, KIT) if act_path.startswith(KIT) else act_path,
               "teams": {k: team_day(lineups[k], actuals, teams_of)
                         for k in sorted(lineups, key=lambda k: int(k.rsplit(".", 1)[-1]))}}
        _dump(os.path.join(a.out_dir, f"day_{a.date}.json"), day)
    days = [_load(p, None) for p in sorted(glob.glob(os.path.join(a.out_dir, "day_*.json")))]
    managers = managers_by_team(_load(os.path.join(KIT, "data", "league_state.json"), {}))
    prof = rollup([d for d in days if d], move_counts(moves), managers)
    unnamed = [t["team"] for t in prof["teams"].values() if t["manager"] is None]
    if unnamed:
        notes.append(f"no manager in the league state for {', '.join(unnamed)}")
    prof["note"] = "record only (owner 2026-10-22, option A); no engine value reads this"
    _dump(os.path.join(a.out_dir, "profile.json"), prof)

    tail = ("; " + "; ".join(notes)) if notes else ""
    if halt:
        print(f"MANAGER LOG: HALT — {'; '.join(halt)}; day not logged, profile stands at {prof['window']['days']} day(s){tail}")
        return 1
    lost = sum(t["starts_lost"] for t in day["teams"].values())
    no_line = sorted({x["name"] for t in day["teams"].values() for x in t["no_box_line"] if x["slot"] not in ("IL", "IL+")})
    print(f"MANAGER LOG: PASS — {a.date}: {len(day['teams'])} lineups, {lost} start(s) lost league-wide"
          + (f"; outside IL, team played but no box line (inactive or unmatched name): {', '.join(no_line)}" if no_line else "")
          + f"; profile {prof['window']['first']}..{prof['window']['last']} ({prof['window']['days']} day(s)){tail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
