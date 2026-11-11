#!/usr/bin/env python3
"""Team updates (owner 2026-11-11, runner after-report pick D3, "Team-update path"): a pooled player's NBA team is
changed only when two sources agree on the move.

The rule: Yahoo's roster pull shows the player on a club other than the pool's, AND an ESPN transactions item names
that player moving to that same club. Yahoo alone, or ESPN alone, changes nothing: the first stays a flagged
disagreement in data/league_state.json as before, the second is not a disagreement at all.

What "moving to" means in ESPN's wording (transactions.py keeps each item's listing club and its description):
  - "Traded <pos> <player> to the <club name>."            -> the named club
  - "Acquired ...", "Signed ...", "Claimed ..." (an item listed under the arriving club) -> the listing club
Any other wording (waived, recalled, assigned, a club name ESPN's own list does not carry) names no arrival.
Club names are read against ESPN's team list, pinned with its receipt at data/reference/nba_teams_espn.json.

Every change is one append-only row in data/team_changes.jsonl with its receipts: the Yahoo pull file and sha256
and the team it showed; the ESPN item's date, text, listing club and the transactions file it was read from. A
change is reversed by appending a revert row (never by editing): the pool team applies again, the disagreement is
flagged again, and that same change is not made a second time.

Who applies it: league_intake.run makes the decision and clears the flag (the roster intake has Yahoo's teams);
season_lines.run writes the changed team into the season pool and projections files (the team column only), which
is where the real-games forecast, games-left counts, the board and the deck read a player's club. The preseason
files are never edited, and no projection line, injury tag or engine constant is touched.

    python3 scripts/team_updates.py --list
    python3 scripts/team_updates.py --revert "Nique Clifford" --note "why"
Prints 'TEAM UPDATES: PASS — ...' or 'TEAM UPDATES: HALT — <why>'. Exit 0 / 1.
"""
import argparse
import datetime
import glob
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import box_pull  # noqa: E402

LEDGER = os.path.join(KIT, "data", "team_changes.jsonl")
NEWS = os.path.join(KIT, "data", "news")
TEAMS = os.path.join(KIT, "data", "reference", "nba_teams_espn.json")
LOOKBACK_DAYS = 14   # hand-set (owner 2026-11-11): Yahoo can show a trade days after ESPN lists it
RULE = "Yahoo's team differs from the pool and an ESPN transactions item names the player moving to that team"
ARRIVAL = re.compile(r"^\s*(acquired|signed|claimed)\b", re.I)
TRADED_TO = re.compile(r"^\s*traded\b.*?\bto the (.+?)(?:\s+(?:for|in exchange|as part|in a)\b.*)?\.?\s*$", re.I)


class TeamUpdateError(Exception):
    pass


def team_names(path=TEAMS):
    """{club name, lower case: pool code} from the pinned ESPN list."""
    with open(path, encoding="utf-8") as f:
        return {t["name"].lower(): t["pool_code"] for t in json.load(f)["teams"]}


def _fold(text):
    """Lower case, accents and punctuation dropped, so "P.J. Washington" and "Luka Dončić" match the pool's spelling."""
    t = "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c)).lower()
    return " ".join(re.sub(r"[^a-z0-9 ]", "", t).split())


def destination(item, names, player=None):
    """The pool code of the club an ESPN item moves its player to, or None when the wording names no arrival. With
    `player`, a trade is read as his move only when his name stands before "to the": a player named after the club
    is what came back, and the item does not say in these words where he went."""
    text = item.get("description") or ""
    m = TRADED_TO.match(text)
    if m:
        if player and _fold(player) not in _fold(text[:m.start(1)]):
            return None
        return names.get(m.group(1).strip().lower())
    if ARRIVAL.match(text) and item.get("nba_team"):
        code = box_pull.ESPN_CODE.get(item["nba_team"], item["nba_team"])
        return code if code in set(names.values()) else None
    return None


def espn_items(news_dir=NEWS, as_of=None, days=LOOKBACK_DAYS):
    """The ESPN items naming a pool player (transactions.py's hits) from the transactions files dated within `days`
    before `as_of`, each once, carrying the newest file it was read from."""
    end = datetime.date.fromisoformat(as_of)
    start = (end - datetime.timedelta(days=days)).isoformat()
    out = {}
    for p in sorted(glob.glob(os.path.join(news_dir, "transactions_*.json"))):
        m = re.fullmatch(r"transactions_(\d{4}-\d{2}-\d{2})\.json", os.path.basename(p))
        if not m or not (start <= m.group(1) <= as_of):
            continue
        try:
            with open(p, encoding="utf-8") as f:
                hits = json.load(f).get("hits") or []
        except (OSError, ValueError):
            continue
        for h in hits:
            out[(h.get("player"), h.get("date"), h.get("description"))] = dict(h, file=os.path.basename(p))
    return sorted(out.values(), key=lambda h: (h.get("date") or "", h.get("player") or ""))


def decide(disagreements, items, names, held=()):
    """[{player, from, to, espn: {date, description, nba_team, file}}] for each disagreement an ESPN item confirms.
    held: {(player, to)} changes that were reverted and are not made again."""
    out = []
    for d in disagreements:
        if (d["player"], d["yahoo"]) in set(held):
            continue
        hits = [i for i in items if i.get("player") == d["player"] and destination(i, names, player=d["player"]) == d["yahoo"]]
        if hits:
            i = max(hits, key=lambda i: i.get("date") or "")
            out.append({"player": d["player"], "from": d["pool"], "to": d["yahoo"],
                        "espn": {k: i.get(k) for k in ("date", "description", "nba_team", "file")}})
    return out


def read(path=LEDGER):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(ln) for ln in f if ln.strip()]


def append(path, rows):
    if rows:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return rows


def _next_id(rows, date):
    n = sum(1 for r in rows if r.get("id", "").startswith(f"T-{date}-"))
    return f"T-{date}-{n + 1:02d}"


def row(change, as_of, yahoo, existing):
    """A ledger row for one change. yahoo: {file, sha256} of the roster pull that showed the new team."""
    return {"id": _next_id(existing, as_of), "date": as_of, "player": change["player"], "from": change["from"], "to": change["to"],
            "yahoo": dict(yahoo or {}, team=change["to"]), "espn": change["espn"], "rule": RULE}


def revert_row(rows, player, date, note):
    """A row that undoes the player's standing change; TeamUpdateError when he has none."""
    live = [r for r in rows if r.get("player") == player]
    if not live or live[-1].get("revert"):
        raise TeamUpdateError(f"{player} has no standing team change to revert")
    last = live[-1]
    return {"id": _next_id(rows, date), "date": date, "player": player, "revert": last["id"], "from": last["to"], "to": last["from"],
            "note": note}


def current(rows):
    """{player: team} as the ledger stands: each player's newest row, unless that row is a revert."""
    out = {}
    for r in rows:
        if r.get("revert"):
            out.pop(r["player"], None)
        else:
            out[r["player"]] = r["to"]
    return out


def held(rows):
    """{(player, to)} for every change that was reverted: the same change is not made again."""
    by = {r["id"]: r for r in rows}
    return {(by[r["revert"]]["player"], by[r["revert"]]["to"]) for r in rows if r.get("revert") and r["revert"] in by}


def overlay(team_of, changes):
    """team_of with the ledger's teams over the pool's, for the players the ledger names."""
    return {n: changes.get(n, t) for n, t in team_of.items()}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ledger", default=LEDGER)
    ap.add_argument("--list", action="store_true", help="print every row and the standing changes")
    ap.add_argument("--revert", metavar="PLAYER", help="append a row undoing this player's standing change")
    ap.add_argument("--note", default=""); ap.add_argument("--date", default=datetime.date.today().isoformat())
    a = ap.parse_args(argv)
    rows = read(a.ledger)
    if a.revert:
        if not a.note:
            print("TEAM UPDATES: HALT — a revert needs --note saying why"); return 1
        try:
            r = revert_row(rows, a.revert, a.date, a.note)
        except TeamUpdateError as e:
            print(f"TEAM UPDATES: HALT — {e}"); return 1
        append(a.ledger, [r]); rows.append(r)
        print(f"TEAM UPDATES: PASS — {r['id']} reverts {r['revert']}: {a.revert} back to {r['to']}; that change will not be made again")
        return 0
    for r in rows:
        print(f"  {r['id']} {r['player']}: {r['from']} to {r['to']}" + (f" (reverts {r['revert']}: {r.get('note', '')})" if r.get("revert")
              else f" (ESPN {r['espn']['date']}: {r['espn']['description']})"))
    cur = current(rows)
    print(f"TEAM UPDATES: PASS — {len(rows)} row(s); standing: " + (", ".join(f"{n} {t}" for n, t in sorted(cur.items())) or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
