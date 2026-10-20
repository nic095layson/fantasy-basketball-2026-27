#!/usr/bin/env python3
"""Live league intake from FantasyBot (owner 2026-10-20: "Build all 3"). The morning agent calls
get_my_roster once and get_league_team for each rival team; this script extracts those responses
mechanically from the session transcript (or a saved pull file), pins the raw pull under
data/source/fantasybot/, converts it to the transcription schema, and hands it to
league_intake.run() — the same name resolution, seat mapping, and halts as the owner's pastes.

Mapping, stated 2026-10-20 (plan-gate A2/A3/A4):
 - rival slots: FantasyBot reserve == "ir" -> IL, everything else -> BN (the sim only
   distinguishes IL from not-IL); my team keeps its Yahoo slots from get_my_roster
 - status: injury "Out" -> O (0.00), "Day-to-day" -> Q (0.50), null -> healthy; any other
   label halts (status_feed.tier would refuse it anyway)
 - names: FantasyBot "Yanic Konan Niederhäuser" -> the unpooled_il key "Y. Konan Niederhäuser";
   everything else through verify_rosters.norm (suffixes, accents, punctuation), misses halt

On any failure nothing is written over data/league_state.json and the exit is nonzero; the
morning run treats the step as non-fatal and the brief says the last paste still stands.

    python3 scripts/league_live.py --as-of 2026-10-20 [--transcript FILE | --pull FILE]
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import league_intake  # noqa: E402
import league_moves  # noqa: E402

LEAGUE = "ANTI MARTIN MARTIN CLUB"
MY_TEAM = "KEL'EL YAXEL HALQUETA"
N_TEAMS = 12
PIN_DIR = os.path.join(KIT, "data", "source", "fantasybot")
TRANSCRIPTS = os.path.expanduser("~/.claude/projects/-home-user-fantasy-basketball-2026-27")
STATUS_OF = {None: "", "Out": "O", "Day-to-day": "Q"}
ALIASES = {"Yanic Konan Niederhäuser": "Y. Konan Niederhäuser"}


class PullError(Exception):
    pass


def _loads(x):
    try:
        return json.loads(x)
    except (json.JSONDecodeError, TypeError):
        return None


def extract_pull(transcript):
    """Walk a session transcript jsonl for FantasyBot responses naming this league: the latest
    get_league_team per team (mode=="team", found) and the latest get_my_roster ("starters")."""
    teams, mine = {}, None

    def walk(x):
        nonlocal mine
        if isinstance(x, str):
            if '"leagueName"' in x and LEAGUE in x:
                j = _loads(x)
                if isinstance(j, dict):
                    if j.get("mode") == "team" and j.get("found"):
                        teams[j["teamName"]] = j
                    elif "starters" in j:
                        mine = j
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    with open(transcript, encoding="utf-8") as f:
        for line in f:
            if LEAGUE not in line:
                continue
            o = _loads(line)
            if o is not None:
                walk(o)
    return {"teams": teams, "mine": mine}


def check_pull(pull):
    teams, mine = pull["teams"], pull["mine"]
    if mine is None:
        raise PullError("no get_my_roster response in the pull")
    for j in list(teams.values()) + [mine]:
        if j.get("leagueName") != LEAGUE:
            raise PullError(f"league name {j.get('leagueName')!r} is not {LEAGUE!r}")
    rivals = [t for t in teams if t != MY_TEAM]
    if len(rivals) + 1 != N_TEAMS:
        raise PullError(f"{len(rivals)} rival team(s) + mine != {N_TEAMS}: {sorted(rivals)}")


def _status(injury, who):
    if injury not in STATUS_OF:
        raise PullError(f"unknown FantasyBot injury label {injury!r} on {who}: add it to STATUS_OF, do not guess")
    return STATUS_OF[injury]


def _row(team, slot, name, nba, positions, injury):
    return dict(fantasy_team=team, page=1, slot=slot, player=ALIASES.get(name, name), nba_team=nba or "",
                positions=",".join(positions) if isinstance(positions, list) else (positions or "").replace("/", ","),
                status=_status(injury, name))


def to_rows(pull):
    """The pull to the transcription schema (fantasy_team, page, slot, player, nba_team, positions, status)."""
    rows = []
    mine = pull["mine"]
    if mine is not None:
        for s in mine["starters"]:
            p = s.get("player")
            if p:
                rows.append(_row(MY_TEAM, s["slot"], p["name"], p.get("team"), p.get("positions") or p.get("position"), p.get("injury")))
        for key, slot in (("bench", "BN"), ("ir", "IL")):
            for p in mine.get(key) or []:
                rows.append(_row(MY_TEAM, slot, p["name"], p.get("team"), p.get("positions") or p.get("position"), p.get("injury")))
    for name, t in pull["teams"].items():
        if name == MY_TEAM:
            continue
        for grp in t["positions"]:
            for p in grp["players"]:
                slot = "IL" if p.get("reserve") == "ir" else "BN"
                rows.append(_row(name, slot, p["name"], p.get("team"), p.get("positions"), p.get("injury")))
    return rows


def newest_transcript():
    files = sorted(glob.glob(os.path.join(TRANSCRIPTS, "*.jsonl")), key=os.path.getmtime)
    if not files:
        raise PullError(f"no session transcript under {TRANSCRIPTS}")
    return files[-1]


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--as-of", default=datetime.date.today().isoformat())
    ap.add_argument("--transcript", help="session transcript jsonl (default: the newest in the project dir)")
    ap.add_argument("--pull", help="a saved raw pull file instead of a transcript")
    ap.add_argument("--out", default=league_intake.OUT)
    ap.add_argument("--pin-dir", default=PIN_DIR)
    a = ap.parse_args()
    try:
        if a.pull:
            pull = json.load(open(a.pull, encoding="utf-8"))
            src_note = {"file": os.path.relpath(a.pull, KIT), "method": "saved FantasyBot pull file"}
        else:
            tr = a.transcript or newest_transcript()
            pull = extract_pull(tr)
            src_note = {"transcript": os.path.basename(tr),
                        "method": "mechanical json extraction of FantasyBot tool results from the session transcript"}
        check_pull(pull)
        rows = to_rows(pull)
    except (PullError, OSError, KeyError) as e:
        print(f"LEAGUE LIVE: HALT — {e}; league_state.json not touched (last paste stands)")
        return 1
    os.makedirs(a.pin_dir, exist_ok=True)
    pin = os.path.join(a.pin_dir, f"pull_{a.as_of}.json")
    with open(pin, "w", encoding="utf-8") as f:
        json.dump(pull, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    src = os.path.join(a.pin_dir, f"rosters_{a.as_of}.transcribed.csv")
    league_intake.write_rows(rows, src)
    pool = list(__import__("csv").DictReader(open(league_intake.POOL, encoding="utf-8")))
    recap = json.load(open(league_intake.RECAP, encoding="utf-8"))
    abbr = {p["abbr"]: p["player"] for p in recap}
    draft, managers = {}, {}
    for p in recap:
        draft.setdefault(p["slot"], []).append(p["player"])
        managers[p["slot"]] = p["manager"]
    sources = {"fantasybot": dict(src_note, pull_file=os.path.relpath(pin, KIT), pull_sha256=sha(pin),
                                  view="FantasyBot connector: get_my_roster + get_league_team per rival team"),
               "transcription": {"file": os.path.relpath(src, KIT), "sha256": sha(src),
                                 "method": "league_live.to_rows (mechanical; rival slots BN/IL only)"},
               "draft_board": os.path.relpath(league_intake.RECAP, KIT), "pool": "deck data/players.csv"}
    unpooled = (json.load(open(league_intake.UNPOOLED, encoding="utf-8"))["players"]
                if os.path.exists(league_intake.UNPOOLED) else {})
    old = json.load(open(a.out, encoding="utf-8")) if os.path.exists(a.out) else None
    code = league_intake.run(src, a.out, pool, abbr, draft, a.as_of, managers, sources, unpooled)
    if code != 0:
        print("LEAGUE LIVE: HALT — intake refused the pull; league_state.json not touched (last paste stands)")
        return code
    new = json.load(open(a.out, encoding="utf-8"))
    if old is not None:
        rec, outp = league_moves.write_record(old, new, a.as_of)
        n = sum(len(m["added"]) + len(m["dropped"]) + len(m["to_il"]) + len(m["from_il"]) for m in rec["moves"])
        print(f"LEAGUE MOVES: PASS — {len(rec['moves'])} team(s) changed, {n} move(s), "
              f"{old['as_of']} to {new['as_of']}; wrote {os.path.relpath(outp, KIT)}")
    print(f"LEAGUE LIVE: PASS — rosters from FantasyBot, pinned {os.path.relpath(pin, KIT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
