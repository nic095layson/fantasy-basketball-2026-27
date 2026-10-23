#!/usr/bin/env python3
"""The Yahoo league through the Flaim connector (owner 2026-10-21: "Build A, B, C, D"). The morning agent calls
Flaim's read-only tools — get_roster for every team (current), get_matchups for the current week, get_free_agents —
and this module extracts those responses mechanically from the session transcript, like league_live does for
FantasyBot: nothing is retyped.

  C  every team's real Yahoo slot (PG … Util, BN, IL) — FantasyBot showed rivals as BN/IL only
  B  every rostered player's Yahoo status letter; a letter status_feed.TIERS does not know halts, never guessed
  A  this week's Yahoo category totals per team (week_matchup's to-date column)
  D  Yahoo's available-player list (week_matchup's pickup pool)
  E  a past day's lineup (get_roster with as_of_date): week_matchup's rebuild counts that day's active slots
     (owner 2026-10-22, "Read daily rosters")

Responses are told apart by shape and kept only for this league (LEAGUE_KEY): a roster has data.teamKey under the
league, data.snapshot.type == "current" and data.players (a dated snapshot is history, never today's roster — it is
kept apart, under daily, by team and date, and a later pin for the same date keeps it: keep_daily); a matchup
response has data.matchups; an available-player list has
data.freeAgents. With since (the run's start), only transcript entries stamped at or after it count.

league_live.py uses this first and FantasyBot only when the Flaim pull is missing or incomplete; history() pins
past seasons' responses for the record.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import league_live as LL  # noqa: E402
import status_feed  # noqa: E402

LEAGUE_KEY = "478.l.36464"  # ANTI MARTIN MARTIN CLUB 2026-27 (Flaim get_user_session, 2026-10-21)
N_TEAMS = 12
PIN_DIR = os.path.join(LL.KIT, "data", "source", "flaim")
SLOT_OF = {"Util": "UTIL"}  # the kit's league_state spelling (FantasyBot wrote UTIL)
STATS = ["fgm", "fga", "ftm", "fta", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"]
COUNT_CATS = {"3PTM": "tpm", "PTS": "pts", "REB": "reb", "AST": "ast", "ST": "stl", "BLK": "blk", "TO": "tov"}


class PullError(Exception):
    pass


def _data(text):
    """The data object of a Flaim response carried as a JSON string, or None."""
    j = LL._loads(text)
    if isinstance(j, dict) and j.get("success") is True and isinstance(j.get("data"), dict):
        return j["data"]
    return None


def _ours(key):
    return isinstance(key, str) and key.startswith(LEAGUE_KEY + ".")


def extract_pull(transcript, since=None):
    """Walk the transcript for this league's Flaim responses: the latest current roster per team, the latest dated
    roster per team and day, the latest matchup response per week, the latest available-player list."""
    since = LL.since_instant(since)
    rosters, daily, weeks, fa = {}, {}, {}, None

    def take(d):
        nonlocal fa
        snap = d.get("snapshot") or {}
        if "players" in d and _ours(d.get("teamKey")) and snap.get("type") == "current":
            rosters[d["teamKey"]] = d
        elif "players" in d and _ours(d.get("teamKey")) and snap.get("type") == "date" and snap.get("date"):
            daily.setdefault(d["teamKey"], {})[snap["date"]] = d
        elif "matchups" in d and d.get("leagueKey") == LEAGUE_KEY:
            weeks[str(d.get("matchupWeek") or d.get("currentWeek"))] = d
        elif "freeAgents" in d and d.get("leagueKey") == LEAGUE_KEY:
            fa = d

    def walk(x):
        if isinstance(x, str):
            if '"success"' in x and LEAGUE_KEY in x:
                d = _data(x)
                if d is not None:
                    take(d)
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    with open(transcript, encoding="utf-8") as f:
        for ln in f:
            if LEAGUE_KEY not in ln:
                continue
            o = LL._loads(ln)
            if o is not None and LL.recent(o, since):
                walk(o.get("message") if isinstance(o, dict) and "message" in o else o)
    return {"source": "flaim", "league_key": LEAGUE_KEY, "rosters": rosters, "daily": daily, "matchups": weeks,
            "free_agents": fa}


def keep_daily(pull, path):
    """The pull to pin at path, carrying the dated lineups an earlier pin there holds. A later run for the same date
    (the afternoon check) rewrites the morning's file with a pull that has none, and the week card reads the morning's
    on later days; a past day's lineup is history, so it is kept. For the same team and day the later pull wins.
    The week's matchups and the available-player list are kept the same way when the later pull has none (the 3 PM
    check pulls rosters only; owner 2026-10-22, "Carry them forward"), and carried_forward names what was kept: those
    are the earlier pin's, pulled by the day's first run. A later pull that has its own wins."""
    if not os.path.exists(path):
        return pull
    with open(path, encoding="utf-8") as f:
        pin = json.load(f)
    daily = {team: dict(days) for team, days in (pin.get("daily") or {}).items()}
    for team, days in (pull.get("daily") or {}).items():
        daily.setdefault(team, {}).update(days)
    out = dict(pull, daily=daily)
    carried = set(pin.get("carried_forward") or ())
    for key in ("matchups", "free_agents"):
        if not pull.get(key) and pin.get(key):
            out[key] = pin[key]
            carried.add(key)
        else:
            carried.discard(key)
    if carried:
        out["carried_forward"] = sorted(carried)
    else:
        out.pop("carried_forward", None)
    return out


def check_pull(pull):
    """Twelve current rosters, every status letter one status_feed tiers; otherwise PullError naming what failed."""
    n = len(pull.get("rosters") or {})
    if n != N_TEAMS:
        raise PullError(f"{n} of {N_TEAMS} current Flaim rosters in the pull")
    unknown = sorted({(p.get("status"), p.get("name"), r.get("teamName")) for r in pull["rosters"].values()
                      for p in r["players"] if p.get("status") and p.get("status") not in status_feed.TIERS},
                     key=lambda x: str(x))
    if unknown:
        raise PullError("Yahoo status letter(s) the kit does not tier: "
                        + "; ".join(f"{s} on {n} ({t})" for s, n, t in unknown) + " — add to status_feed.TIERS on the record, do not guess")


def to_rows(pull):
    """The transcription schema league_intake reads: every team with its Yahoo slots and letters."""
    rows = []
    for key in sorted(pull["rosters"], key=lambda k: int(k.rsplit(".", 1)[-1])):
        r = pull["rosters"][key]
        for p in r["players"]:
            rows.append(dict(fantasy_team=r["teamName"], page=1, slot=SLOT_OF.get(p.get("selectedPosition"), p.get("selectedPosition") or "BN"),
                             player=LL.ALIASES.get(p["name"], p["name"]), nba_team=p.get("team") or "",
                             positions=(p.get("position") or "").replace("/", ","), status=p.get("status") or ""))
    return rows


# ---------------------------------------------------------------- matchups (A)
def _pair(v):
    m = re.fullmatch(r"\s*(\d+)\s*/\s*(\d+)\s*", str(v))
    if not m:
        raise PullError(f"unreadable makes/attempts value {v!r}")
    return int(m.group(1)), int(m.group(2))


def side_totals(side):
    """One matchup side's Yahoo category values as the kit's stat totals (makes and attempts, counts)."""
    by = {c.get("displayName"): c.get("value") for c in side.get("categories") or []}
    if "FGM/A" not in by or "FTM/A" not in by:
        raise PullError(f"{side.get('teamName')}: no FGM/A or FTM/A in the matchup categories")
    t = {}
    t["fgm"], t["fga"] = _pair(by["FGM/A"])
    t["ftm"], t["fta"] = _pair(by["FTM/A"])
    for cat, k in COUNT_CATS.items():
        if cat not in by:
            raise PullError(f"{side.get('teamName')}: no {cat} in the matchup categories")
        t[k] = int(by[cat])
    return {k: t[k] for k in STATS}


def find_sides(matchup_data, me, opp):
    """(my side, opponent side) of the matchup naming both teams, or (None, None)."""
    for m in matchup_data.get("matchups") or []:
        sides = {s.get("teamName"): s for s in (m.get("home"), m.get("away")) if s}
        if me in sides and opp in sides:
            return sides[me], sides[opp]
    return None, None


# ---------------------------------------------------------------- history (owner 2026-10-21: "pull previous season data")
def history(transcript, league_keys, out_dir, since=None):
    """Pin every Flaim response for the named past leagues, one file per response kind (and week), raw. Returns the
    list of files written."""
    since = LL.since_instant(since)
    found = {}

    def key_of(d):
        for k in ("leagueKey", "league_key", "leagueId"):
            v = d.get(k)
            if isinstance(v, str) and v in league_keys:
                return v
        tk = d.get("teamKey")
        if isinstance(tk, str):
            lk = tk.rsplit(".t.", 1)[0]
            if lk in league_keys:
                return lk
        return None

    def kind_of(d):
        if "matchups" in d:
            return f"matchups_week{int(d.get('matchupWeek') or d.get('currentWeek')):02d}"
        if "standings" in d:
            return "standings"
        if "picks" in d or "draft" in d:
            return "draft"
        if "teams" in d and "scoringType" in d:
            return "league_info"
        return None

    def walk(x):
        if isinstance(x, str):
            if '"success"' in x:
                d = _data(x)
                if d is not None:
                    lk, kind = key_of(d), kind_of(d)
                    if lk and kind:
                        found[(lk, kind)] = d
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    with open(transcript, encoding="utf-8") as f:
        for ln in f:
            if not any(k in ln for k in league_keys):
                continue
            o = LL._loads(ln)
            if o is not None and LL.recent(o, since):
                walk(o.get("message") if isinstance(o, dict) and "message" in o else o)
    written = []
    for (lk, kind), d in sorted(found.items()):
        p = os.path.join(out_dir, lk, f"{kind}.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=1, ensure_ascii=False, sort_keys=True)
            f.write("\n")
        written.append(p)
    return written


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--history", nargs="+", metavar="LEAGUE_KEY", help="pin past seasons' Flaim responses for these league keys")
    ap.add_argument("--transcript")
    ap.add_argument("--out-dir", default=os.path.join(PIN_DIR, "history"))
    ap.add_argument("--since")
    a = ap.parse_args()
    if not a.history:
        print(__doc__)
        return 2
    try:
        files = history(a.transcript or LL.newest_transcript(), set(a.history), a.out_dir, a.since)
    except (LL.PullError, OSError) as e:
        print(f"FLAIM HISTORY: FAIL — {e}")
        return 1
    print(f"FLAIM HISTORY: PASS — {len(files)} response(s) pinned under {os.path.relpath(a.out_dir, LL.KIT) if a.out_dir.startswith(LL.KIT) else a.out_dir}")
    for p in files:
        print("  " + (os.path.relpath(p, LL.KIT) if p.startswith(LL.KIT) else p))
    return 0 if files else 1


if __name__ == "__main__":
    sys.exit(main())
