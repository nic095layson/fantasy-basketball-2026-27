#!/usr/bin/env python3
"""League-state intake (Session 1 item 5; plan 2026-10-15 §6 E0).

Reads the pinned transcription of the owner's Yahoo "Starting Rosters" page
(data/source/yahoo-starting-rosters-2026-10-20-view.transcribed.csv, transcribed from
the pinned PDF's page images because the PDF has no text layer), resolves every name
to the deck's pool, maps each fantasy team to its draft seat by roster overlap with the
2026-10-14 draft board, and writes data/league_state.json with its date.

Resolution: the deck's name fold (verify_rosters.norm: accents, punctuation, suffixes,
aliases), then Yahoo's own abbreviations as recorded on the draft board (recap.json
"abbr" -> "player"). Nothing else: a name neither rule resolves HALTS the intake and
nothing is written (RULES.md rule 4; the Session 1 prompt: "halt on any miss").

    python3 scripts/league_intake.py [--as-of YYYY-MM-DD]

Exit 0 = written. Exit 1 = halted, misses listed.
"""
import argparse
import csv
import datetime
import hashlib
import json
import os
import sys

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK = os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball")
sys.path.insert(0, os.path.join(DECK, "scripts"))
from verify_rosters import norm  # noqa: E402

SRC = os.path.join(KIT, "data", "source", "yahoo-starting-rosters-2026-10-20-view.transcribed.csv")
PDF = os.path.join(KIT, "data", "source", "yahoo-starting-rosters-2026-10-20-view.pdf")
RECAP = os.path.join(KIT, "report", "after-reports", "draft-league-2026-10-14", "recap.json")
POOL = os.path.join(DECK, "data", "players.csv")
OUT = os.path.join(KIT, "data", "league_state.json")
EMPTY = "(Empty)"


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


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def run(src, out, pool, abbr, draft, as_of, managers=None, sources=None):
    rows = list(csv.DictReader(open(src, encoding="utf-8")))
    names = [r["player"] for r in rows if r["player"] != EMPTY]
    res, miss = resolve(names, pool, abbr)
    if miss:
        print(f"LEAGUE INTAKE: HALT — {len(miss)} name(s) not in the pool; nothing written:")
        for n in miss:
            r = next(x for x in rows if x["player"] == n)
            print(f"  - {n} ({r['fantasy_team']}, {r['slot']}, {r['nba_team']}, status {r['status'] or '-'})")
        return 1
    team_of = {p["player"]: p["team"] for p in pool}
    teams, order = {}, []
    for r in rows:
        t = r["fantasy_team"]
        if t not in teams:
            teams[t] = {"name": t, "players": [], "empty_slots": []}
            order.append(t)
        if r["player"] == EMPTY:
            teams[t]["empty_slots"].append(r["slot"])
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
    state = {"as_of": as_of, "sources": sources or {}, "standings": None, "scoreboard": None,
             "standings_note": "pre-season: no standings or scoreboard exist before week 1 (2026-10-20)",
             "teams": [teams[t] for t in order], "nba_team_disagreements": disagreements}
    with open(out, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=1, ensure_ascii=False)
        f.write("\n")
    n = sum(len(teams[t]["players"]) for t in order)
    print(f"LEAGUE INTAKE: PASS — {len(order)} teams, {n} players, {n} of {n} resolved; "
          f"{len(disagreements)} NBA-team disagreement(s) with the pool; wrote {os.path.relpath(out, KIT)}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--as-of", default=datetime.date.today().isoformat())
    a = ap.parse_args()
    pool = list(csv.DictReader(open(POOL, encoding="utf-8")))
    recap = json.load(open(RECAP, encoding="utf-8"))
    abbr = {p["abbr"]: p["player"] for p in recap}
    draft, managers = {}, {}
    for p in recap:
        draft.setdefault(p["slot"], []).append(p["player"])
        managers[p["slot"]] = p["manager"]
    sources = {"pdf": {"file": os.path.relpath(PDF, KIT), "sha256": sha(PDF), "view": "Yahoo Starting Rosters, Tue Oct 20 tab"},
               "transcription": {"file": os.path.relpath(SRC, KIT), "sha256": sha(SRC),
                                 "method": "agent transcription of the page images (no text layer)"},
               "draft_board": os.path.relpath(RECAP, KIT), "pool": "deck data/players.csv"}
    sys.exit(run(SRC, OUT, pool, abbr, draft, a.as_of, managers, sources))


if __name__ == "__main__":
    main()
