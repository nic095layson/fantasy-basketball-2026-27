#!/usr/bin/env python3
"""League-state intake (Session 1 item 5; plan 2026-10-15 §6 E0).

Reads the pinned transcription of the owner's Yahoo "Starting Rosters" page
(data/source/yahoo-starting-rosters-2026-10-20-view.transcribed.csv, transcribed from
the pinned PDF's page images because the PDF has no text layer), resolves every name
to the deck's pool, maps each fantasy team to its draft seat by roster overlap with the
2026-10-14 draft board, and writes data/league_state.json with its date.

Resolution: the deck's name fold (verify_rosters.norm: accents, punctuation, suffixes,
aliases), then Yahoo's own abbreviations as recorded on the draft board (recap.json
"abbr" -> "player"). Nothing else: a name neither rule resolves is never guessed (RULES.md rule 4).
Council 2026-10-15 (4-1), unchanged: a name listed in data/unpooled_il.json that sits in an IL slot is
carried as `unpooled_il` with no line.
Owner 2026-10-26, option (a) (the 10/26 Brazile halt froze every roster for a rival's bench pickup): any
OTHER name the pool lacks no longer halts the intake. It is carried as `unpooled` (per team, and listed in
the state's top-level `unpooled`) with no projection line, a named LEAGUE INTAKE: WARN line is printed,
and the brief and the deck's Today tab show it as "not in the pool, not simulated". The simulator reads
only `players`, so it never sees an unpooled name; the gap stays visible every day until a
data/pool_additions.csv row lands. This widens the Council rule from "a listed IL stash" to "any slot,
flagged"; the IL path itself is untouched.

The pool is the deck's data/players.csv (frozen at the draft lock) followed by the kit's data/pool_additions.csv:
in-season pickups the draft pool never carried, one deck-schema row each (owner 2026-10-21, option (b)). A name
in both files is refused (load_pool raises), never carried twice.

    python3 scripts/league_intake.py [--as-of YYYY-MM-DD]

Exit 0 = written. Exit 1 = halted, misses listed.
"""
import argparse
import csv
import datetime
import hashlib
import json
import os
import re
import sys

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK = os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball")
sys.path.insert(0, os.path.join(DECK, "scripts"))
from verify_rosters import norm  # noqa: E402

SRC = os.path.join(KIT, "data", "source", "yahoo-starting-rosters-2026-10-20-view.transcribed.csv")
PDF = os.path.join(KIT, "data", "source", "yahoo-starting-rosters-2026-10-20-view.pdf")
RECAP = os.path.join(KIT, "report", "after-reports", "draft-league-2026-10-14", "recap.json")
POOL = os.path.join(DECK, "data", "players.csv")
ADDITIONS = os.path.join(KIT, "data", "pool_additions.csv")
POOL_LABEL = "deck data/players.csv + kit data/pool_additions.csv"
OUT = os.path.join(KIT, "data", "league_state.json")
UNPOOLED = os.path.join(KIT, "data", "unpooled_il.json")
EMPTY = "(Empty)"
SLOT_RE = re.compile(r"^(PG|SG|G|SF|PF|F|C|Util|BN|IL|IL\+)\t?\s*$")
NBA_RE = re.compile(r"^([A-Z]{2,4}) - ([A-Z,]+)\s*$")
NOTE_RE = re.compile(r"^(?P<name>.+?)(?P<status>Q|O|P|D|DTD|GTD|INJ|NA|SUSP)?(?:New Player Note|No new player Notes|Player Note)\s*$")
GAME_RE = re.compile(r"^\d{1,2}:\d{2} [ap]m (vs|@) [A-Z]{2,4}\s*$")
DATE_RE = re.compile(r"^(Mon|Tue|Wed|Thu|Fri|Sat|Sun), [A-Z][a-z]{2} \d{1,2}\s*$")


class PasteError(Exception):
    pass


def parse_paste(text):
    """The Yahoo league 'Starting Rosters' page pasted as text (owner sample 2026-10-19), to the transcription
    schema (fantasy_team, page, slot, player, nba_team, positions, status). The page lists each fantasy team as a
    header line, then 'Pos' / 'Player', then per slot: the slot line, '<Name><status letter?><note label>', the
    '<NBA> - <POS,...>' line, and an optional game-time line. Date tabs and blank lines are skipped. Anything
    else inside a player block HALTS the parse (RULES.md rule 4: no guessing)."""
    lines = [ln.rstrip("\n") for ln in text.splitlines()]
    rows, team, i, pending = [], None, 0, None
    while i < len(lines):
        ln = lines[i].strip()
        if not ln or ln in ("Starting Rosters", "Pos", "Player") or DATE_RE.match(ln) or GAME_RE.match(ln):
            i += 1; continue
        if SLOT_RE.match(lines[i].strip()):
            if team is None:
                raise PasteError(f"line {i + 1}: slot before any team header")
            slot = SLOT_RE.match(lines[i].strip()).group(1)
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j >= len(lines):
                raise PasteError(f"line {i + 1}: slot {slot} with no player line")
            m = NOTE_RE.match(lines[j].strip())
            if lines[j].strip() == EMPTY:
                rows.append(dict(fantasy_team=team, page=1, slot=slot, player=EMPTY, nba_team="", positions="", status="")); i = j + 1; continue
            if not m:
                raise PasteError(f"line {j + 1}: {lines[j].strip()!r} is not a '<Name><status><note label>' line")
            k = j + 1
            while k < len(lines) and not lines[k].strip():
                k += 1
            n = NBA_RE.match(lines[k].strip()) if k < len(lines) else None
            if not n:
                raise PasteError(f"line {k + 1}: {lines[k].strip() if k < len(lines) else '<eof>'!r} is not an '<NBA> - <POS>' line for {m.group('name')!r}")
            rows.append(dict(fantasy_team=team, page=1, slot=slot, player=m.group("name").strip(), nba_team=n.group(1),
                             positions=n.group(2), status=m.group("status") or ""))
            i = k + 1; continue
        # anything else is a fantasy-team header (the page prints it with a trailing space)
        team = ln
        i += 1
    if not rows:
        raise PasteError("no roster rows found")
    return rows


def write_rows(rows, path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["fantasy_team", "page", "slot", "player", "nba_team", "positions", "status"], lineterminator="\n")
        w.writeheader(); w.writerows(rows)


def resolve(names, pool, abbr):
    idx = {}
    for p in pool:
        idx.setdefault(norm(p["player"]), []).append(p["player"])
    res, miss = {}, []
    for n in names:
        hit = idx.get(norm(n), [])
        if len(hit) == 1:
            res[n] = hit[0]
        elif n in abbr:
            res[n] = abbr[n]
        else:
            miss.append(n)
    return res, miss


def load_pool(pool_path=POOL, additions_path=ADDITIONS):
    """The deck pool's rows, then the kit's in-season additions (none when the file is absent). Raises ValueError
    naming every addition whose folded name the deck pool already carries."""
    pool = list(csv.DictReader(open(pool_path, encoding="utf-8")))
    if not os.path.exists(additions_path):
        return pool
    adds = list(csv.DictReader(open(additions_path, encoding="utf-8")))
    have = {norm(p["player"]) for p in pool}
    dup = [a["player"] for a in adds if norm(a["player"]) in have]
    if dup:
        raise ValueError(f"already in the deck pool, remove from {os.path.relpath(additions_path, KIT)}: {', '.join(dup)}")
    return pool + adds


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def run(src, out, pool, abbr, draft, as_of, managers=None, sources=None, unpooled=None):
    unpooled = unpooled or {}
    rows = list(csv.DictReader(open(src, encoding="utf-8")))
    il_exempt = {r["player"] for r in rows if r["player"] in unpooled and r["slot"] == "IL"}
    names = [r["player"] for r in rows if r["player"] != EMPTY and r["player"] not in il_exempt]
    res, miss = resolve(names, pool, abbr)
    missed = set(miss)
    if miss:
        # owner 2026-10-26, option (a): carried, flagged, never simulated, never guessed
        print(f"LEAGUE INTAKE: WARN — {len(miss)} name(s) not in the pool, carried as unpooled (no line, not simulated): "
              + "; ".join(f"{n} ({r['fantasy_team']}, {r['slot']}, {r['nba_team']})"
                          for n in miss for r in [next(x for x in rows if x["player"] == n)]))
    team_of = {p["player"]: p["team"] for p in pool}
    teams, order = {}, []
    for r in rows:
        t = r["fantasy_team"]
        if t not in teams:
            teams[t] = {"name": t, "players": [], "empty_slots": [], "unpooled_il": [], "unpooled": []}
            order.append(t)
        if r["player"] == EMPTY:
            teams[t]["empty_slots"].append(r["slot"])
            continue
        if r["player"] in il_exempt:
            teams[t]["unpooled_il"].append(r["player"])
            continue
        if r["player"] in missed:
            teams[t]["unpooled"].append({"player": r["player"], "slot": r["slot"], "nba_team": r["nba_team"],
                                         "positions": r["positions"].split(",") if r["positions"] else [],
                                         "status": r["status"] or None})
            continue
        p = res[r["player"]]
        teams[t]["players"].append({"player": p, "yahoo_name": r["player"], "slot": r["slot"],
                                    "yahoo_nba_team": r["nba_team"], "pool_team": team_of.get(p),
                                    "positions": r["positions"].split(",") if r["positions"] else [],
                                    "status": r["status"] or None})
    problems, disagreements = [], []
    for t in order:
        names_t = {p["player"] for p in teams[t]["players"]}
        overlap = sorted(((len(names_t & set(picks)), seat) for seat, picks in draft.items()), reverse=True)
        if not overlap or overlap[0][0] == 0 or (len(overlap) > 1 and overlap[0][0] == overlap[1][0]):
            problems.append(f"{t}: no unique draft seat by roster overlap ({overlap[:2]})")
            continue
        seat = overlap[0][1]
        teams[t]["seat"] = seat
        teams[t]["manager"] = (managers or {}).get(seat)
        teams[t]["draft_overlap"] = overlap[0][0]
        teams[t]["added_since_draft"] = sorted(names_t - set(draft[seat]))
        teams[t]["dropped_since_draft"] = sorted(set(draft[seat]) - names_t)
        for p in teams[t]["players"]:
            if p["pool_team"] and p["yahoo_nba_team"] != p["pool_team"]:
                disagreements.append({"player": p["player"], "yahoo": p["yahoo_nba_team"], "pool": p["pool_team"]})
    seats = [teams[t].get("seat") for t in order]
    if len(set(s for s in seats if s)) != len([s for s in seats if s]):
        problems.append(f"two fantasy teams map to one seat: {seats}")
    if problems:
        print("LEAGUE INTAKE: HALT — seat mapping failed; nothing written:")
        for p in problems:
            print("  -", p)
        return 1
    flagged = [dict(player=u["player"], fantasy_team=teams[t]["name"], seat=teams[t].get("seat"), slot=u["slot"],
                    nba_team=u["nba_team"], status=u["status"]) for t in order for u in teams[t]["unpooled"]]
    state = {"as_of": as_of, "sources": sources or {}, "unpooled_il": {n: unpooled[n] for n in sorted(il_exempt)},
             "unpooled": flagged, "standings": None, "scoreboard": None,
             "standings_note": "pre-season: no standings or scoreboard exist before week 1 (2026-10-20)",
             "teams": [teams[t] for t in order], "nba_team_disagreements": disagreements}
    with open(out, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=1, ensure_ascii=False)
        f.write("\n")
    n = sum(len(teams[t]["players"]) for t in order)
    print(f"LEAGUE INTAKE: PASS — {len(order)} teams, {n} players, {n} of {n} resolved; {len(flagged)} unpooled; "
          f"{len(disagreements)} NBA-team disagreement(s) with the pool; wrote {os.path.relpath(out, KIT) if out.startswith(KIT) else out}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--as-of", default=datetime.date.today().isoformat())
    ap.add_argument("--paste", help="the Yahoo Starting Rosters page pasted as text (pinned under data/source/); parsed to the transcription schema")
    a = ap.parse_args()
    src, pdf = SRC, PDF
    if a.paste:
        try:
            rows = parse_paste(open(a.paste, encoding="utf-8").read())
        except (PasteError, OSError) as e:
            print(f"LEAGUE INTAKE: HALT — paste not parsed: {e}"); sys.exit(1)
        src = os.path.splitext(a.paste)[0] + ".transcribed.csv"
        write_rows(rows, src); pdf = None
    try:
        pool = load_pool()
    except ValueError as e:
        print(f"LEAGUE INTAKE: HALT — pool additions: {e}"); sys.exit(1)
    recap = json.load(open(RECAP, encoding="utf-8"))
    abbr = {p["abbr"]: p["player"] for p in recap}
    draft, managers = {}, {}
    for p in recap:
        draft.setdefault(p["slot"], []).append(p["player"])
        managers[p["slot"]] = p["manager"]
    if a.paste:
        sources = {"paste": {"file": os.path.relpath(a.paste, KIT), "sha256": sha(a.paste), "view": "Yahoo Starting Rosters page, pasted as text by the owner"},
                   "transcription": {"file": os.path.relpath(src, KIT), "sha256": sha(src), "method": "league_intake.parse_paste (mechanical)"},
                   "draft_board": os.path.relpath(RECAP, KIT), "pool": POOL_LABEL}
    else:
        sources = {"pdf": {"file": os.path.relpath(pdf, KIT), "sha256": sha(pdf), "view": "Yahoo Starting Rosters, Tue Oct 20 tab"},
                   "transcription": {"file": os.path.relpath(src, KIT), "sha256": sha(src),
                                     "method": "agent transcription of the page images (no text layer)"},
                   "draft_board": os.path.relpath(RECAP, KIT), "pool": POOL_LABEL}
    unpooled = json.load(open(UNPOOLED, encoding="utf-8"))["players"] if os.path.exists(UNPOOLED) else {}
    sys.exit(run(src, OUT, pool, abbr, draft, a.as_of, managers, sources, unpooled))


if __name__ == "__main__":
    main()
