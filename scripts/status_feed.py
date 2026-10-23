#!/usr/bin/env python3
"""Daily status feed (Session 1 item 4; plan 2026-10-15 §4 A3).

Reads the Yahoo status letters carried in data/league_state.json (the owner's pasted or
uploaded rosters page) and tries ESPN's injury feed; writes data/status/status_<date>.json
with an availability tier per flagged player and the dated receipts behind it. Owner
overrides (data/status_overrides.json) win, and must carry their own dated receipt.

Tiers (stated to the owner 2026-10-15 before the first run): Yahoo O -> out 0.00;
Q -> questionable 0.50 (a coin flip absent better information); no letter -> healthy 1.00.
An unknown letter is refused, never guessed.

Gate (`--check`): a Q/O-flagged row at availability 1.00 with no receipt FAILS, and every
flagged row needs at least one receipt with a date — the draft-night gap (Durant and
Bridges were Q and nothing read it).

    python3 scripts/status_feed.py [--date YYYY-MM-DD]     # build today's file
    python3 scripts/status_feed.py --check [FILE]           # gate the newest (or named) file
"""
import argparse
import datetime
import glob
import json
import os
import sys
import urllib.request

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_ledger  # noqa: E402
STATE = os.path.join(KIT, "data", "league_state.json")
OVERRIDES = os.path.join(KIT, "data", "status_overrides.json")
OUTDIR = os.path.join(KIT, "data", "status")
ESPN_INJURIES = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/injuries"
OWNER_SEAT = 10
TIERS = {None: ("healthy", 1.00), "Q": ("questionable", 0.50), "O": ("out", 0.00),
         # 2026-10-19: P (probable) seen on the owner's rosters paste (Curry); 0.75 is a stated default, D-IS-6
         "P": ("probable", 0.75),
         # 2026-10-20: NA (not active) seen on the owner's rosters paste (Kevin Porter Jr.); 0.00 like O, a stated default, D-IS-7
         "NA": ("not active", 0.00),
         # 2026-10-21: D seen on the Flaim available-player list (Isaiah Stewart); the owner: "Stewart's 'D' means
         # 'Doubtful'". 0.25 is a stated default, halfway between Q and O as P sits above Q, D-IS-10
         "D": ("doubtful", 0.25)}


def tier(letter):
    if letter not in TIERS:
        raise ValueError(f"unknown status letter {letter!r}: add it to TIERS on the record, do not guess")
    return TIERS[letter]


def try_espn(timeout=15):
    at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        with urllib.request.urlopen(ESPN_INJURIES, timeout=timeout) as r:
            return json.load(r), {"attempted": at, "ok": True, "url": ESPN_INJURIES}
    except Exception as e:  # recorded, never silent
        return None, {"attempted": at, "ok": False, "url": ESPN_INJURIES, "detail": f"{type(e).__name__}: {e}"}


def receipt_source(state):
    """(label, file, sha256) of the roster source the letters came from (owner 2026-10-21: Flaim first)."""
    s = state.get("sources", {})
    if "flaim" in s:
        return "Yahoo roster read through Flaim (get_roster, read-only)", s["flaim"].get("pull_file"), s["flaim"].get("pull_sha256")
    if "fantasybot" in s:
        return "FantasyBot roster pull", s["fantasybot"].get("pull_file"), s["fantasybot"].get("pull_sha256")
    src = s.get("pdf", {})
    return "Yahoo Starting Rosters page (owner upload)", src.get("file"), src.get("sha256")


def build(state, espn=None, espn_attempt=None, overrides=None):
    label, src_file, src_sha = receipt_source(state)
    rows = []
    for team in state["teams"]:
        for p in team["players"]:
            if not p.get("status"):
                continue
            name, avail = tier(p["status"])
            rows.append({
                "player": p["player"], "fantasy_team": team.get("name"), "seat": team.get("seat"),
                "slot": p.get("slot"), "yahoo_status": p["status"], "tier": name, "availability": avail,
                "receipts": [{"source": label, "file": src_file,
                              "sha256": src_sha, "captured": state["as_of"],
                              "text": f"{p['status']} beside {p['player']} ({team.get('name')}, {p.get('slot')})"}],
                "espn": espn_attempt or {"ok": False, "detail": "not attempted"},
            })
    for name, ov in (overrides or {}).items():
        for r in rows:
            if r["player"] == name:
                r["availability"] = ov["availability"]
                r["tier"] = ov.get("tier", r["tier"])
                r["receipts"].append(ov["receipt"])
    rows.sort(key=lambda r: (r["seat"] != OWNER_SEAT, r["seat"] or 99, r["player"]))
    return rows


def check(rows):
    problems = []
    for r in rows:
        if r.get("yahoo_status") not in ("Q", "O", "P", "NA", "D"):
            continue
        dated = [x for x in r.get("receipts", []) if x.get("captured") or x.get("date")]
        if r["availability"] >= 1.0 and not dated:
            problems.append(f"{r['player']}: Yahoo {r['yahoo_status']} at availability 1.00 with no dated receipt")
        elif not dated:
            problems.append(f"{r['player']}: Yahoo {r['yahoo_status']} tiered {r['availability']:.2f} with no dated receipt")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--check", nargs="?", const="__newest__")
    ap.add_argument("--ledger", default=run_ledger.LEDGER, help="run-ledger for a standalone run's row ('' to skip)")
    a = ap.parse_args()
    led = (lambda v, d: run_ledger.standalone_record("status_feed --check" if a.check else "status_feed", v, d, ledger=a.ledger)) if a.ledger else (lambda v, d: None)
    if a.check:
        path = a.check if a.check != "__newest__" else (sorted(glob.glob(os.path.join(OUTDIR, "status_*.json"))) or [None])[-1]
        if not path:
            print("STATUS GATE: FAIL — no status file"); led("FAIL", "no status file")
            sys.exit(1)
        rec = json.load(open(path, encoding="utf-8"))
        problems = check(rec["rows"])
        if problems:
            print(f"STATUS GATE: FAIL — {os.path.basename(path)}")
            for p in problems:
                print("  -", p)
            led("FAIL", f"{os.path.basename(path)}: {len(problems)} problem(s)")
            sys.exit(1)
        print(f"STATUS GATE: PASS — {os.path.basename(path)}: {len(rec['rows'])} flagged row(s), each tiered with a dated receipt")
        led("PASS", f"{os.path.basename(path)}: {len(rec['rows'])} flagged row(s)")
        sys.exit(0)
    state = json.load(open(STATE, encoding="utf-8"))
    espn, attempt = try_espn()
    overrides = json.load(open(OVERRIDES, encoding="utf-8")) if os.path.exists(OVERRIDES) else {}
    rows = build(state, espn, attempt, overrides)
    os.makedirs(OUTDIR, exist_ok=True)
    out = os.path.join(OUTDIR, f"status_{a.date}.json")
    rec = {"date": a.date, "league_state_as_of": state["as_of"], "tiers": {str(k): v for k, v in TIERS.items()},
           "espn": attempt, "rows": rows}
    json.dump(rec, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    mine = [r for r in rows if r["seat"] == OWNER_SEAT]
    print(f"status: {len(rows)} flagged row(s) league-wide; yours: "
          + ", ".join(f"{r['player']} {r['yahoo_status']}→{r['availability']:.2f}" for r in mine))
    print(f"ESPN injuries: {'read' if attempt['ok'] else 'NOT READ — ' + attempt['detail']}")
    print(f"wrote {os.path.relpath(out, KIT)}")


if __name__ == "__main__":
    main()
