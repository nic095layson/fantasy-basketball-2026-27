#!/usr/bin/env python3
"""The decision log's two ledgers (owner 2026-10-31: "a log for us to keep 'score' between you and I").

data/decisions/recommendations.jsonl  what the kit said: the morning brief's top waiver pair, one row per day
                                      (kind "hold" on a day with no positive pair), written by the morning run
data/decisions/session.jsonl          what a session advised the owner in chat, written by the session in the same
                                      turn (a separate file so the Runner's branch and a session's branch never
                                      append to the same ledger)
data/decisions/moves.jsonl            what the owner did: every seat-10 move the league pulls recorded
                                      (data/news/league_moves_<date>[_pm].json), joined to a recommendation
                                      mechanically — same add within the horizon → exact / add_match_drop_differs,
                                      same drop → drop_match_add_differs, neither → unrelated, no row in horizon → none

All three are append-only: a brief day already logged is refused, a move already logged (same record file, team,
add, drop) is skipped, a session row is never edited (a correction is a new row with "supersedes"). Nothing here
changes a line, a tag, a roster or a constant; the log records.

    python3 scripts/decision_log.py --brief 2026-10-30            # the day's brief row (refused if the day is logged)
    python3 scripts/decision_log.py --moves                       # every unlogged seat-10 move on disk
    python3 scripts/decision_log.py --session --date 2026-10-30 --add "Cameron Johnson" --drop "Collin Gillespie" \
        --d-title 1.15 --alternatives '[{"drop":"Neemias Queta","d_title":0.35}]' --note "..." [--record path]
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
DIR = os.path.join(KIT, "data", "decisions")
RECS = os.path.join(DIR, "recommendations.jsonl")
SESSION = os.path.join(DIR, "session.jsonl")
MOVES = os.path.join(DIR, "moves.jsonl")
BRIEFS = os.path.join(KIT, "report", "briefs")
NEWS = os.path.join(KIT, "data", "news")
OWNER_SEAT = 10
HORIZON_DAYS = 28   # the default grading window (decision_grade.WINDOW_DAYS states it to the owner)


class LogError(Exception):
    pass


def read(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(ln) for ln in f if ln.strip()]


def append(path, rows):
    """Append rows whose id is not already in the file; a repeated id is refused (append-only). Returns the count."""
    have = {r["id"] for r in read(path)}
    dup = [r["id"] for r in rows if r["id"] in have]
    if dup:
        raise LogError(f"{', '.join(dup)} already in {os.path.relpath(path, KIT)}; the ledger is append-only")
    if not rows:
        return 0
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return len(rows)


def next_id(rows, prefix, date):
    n = 1 + sum(1 for r in rows if r["id"].startswith(f"{prefix}-{date}-"))
    return f"{prefix}-{date}-{n:02d}"


def now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def brief_row(brief, rows, made_at=None, backfilled=False):
    """The brief's top waiver pair as a recommendation row, or a hold row when the brief scored no positive pair."""
    date = brief["date"]
    if any(r.get("source") == "brief" and r.get("date") == date for r in rows):
        raise LogError(f"brief {date} is already logged; the ledger is append-only")
    top = (brief.get("waiver_top") or [None])[0]
    row = {"id": next_id(rows, "R", date), "date": date, "made_at": made_at or now(), "source": "brief",
           "horizon_days": HORIZON_DAYS, "basis": {"seasons": brief.get("seasons"), "lines": brief.get("lines"),
                                                   "state_as_of": brief.get("league_state_as_of"),
                                                   "title_base": brief.get("title")}}
    if top and (top.get("d_title") or 0) > 0:
        row.update(kind="add_drop", add=top["add"], add_nba=top.get("add_team"), drop=top["drop"],
                   status_at_rec={"add": top.get("add_status")},
                   alternatives=[{"add": x["add"], "drop": x["drop"], "d_title": x.get("d_title")} for x in brief["waiver_top"][1:]])
        row["basis"].update(d_ecw=top.get("d_ecw"), d_title=top.get("d_title"), title_by_seed=top.get("title_by_seed"))
    else:
        row.update(kind="hold", add=None, drop=None, alternatives=[],
                   note="no positive pair in the brief" if not top else f"top pair {top['add']} for {top['drop']} scored {top.get('d_title')}")
    if backfilled:
        row["backfilled"] = True
    return row


def session_row(rows, date, add, drop, d_title, alternatives=None, note="", record=None, kind=None, made_at=None,
                supersedes=None, basis=None, backfilled=False):
    kind = kind or ("add_drop" if add and drop else "add_only" if add else "drop_only" if drop else "hold")
    row = {"id": next_id(rows, "S", date), "date": date, "made_at": made_at or now(), "source": "session", "kind": kind,
           "add": add, "drop": drop, "alternatives": alternatives or [], "horizon_days": HORIZON_DAYS,
           "basis": dict(basis or {}, d_title=d_title), "note": note, "record": record}
    if supersedes:
        row["supersedes"] = supersedes
    if backfilled:
        row["backfilled"] = True
    return row


def recommendations(recs=RECS, session=SESSION):
    """Every recommendation row, both files, oldest first; a superseded row is dropped."""
    rows = read(recs) + read(session)
    gone = {r["supersedes"] for r in rows if r.get("supersedes")}
    return sorted((r for r in rows if r["id"] not in gone), key=lambda r: (r["date"], r["id"]))


def _date_of_record(path):
    m = re.search(r"league_moves_(\d{4}-\d{2}-\d{2})(_pm)?\.json$", path)
    return (m.group(1), "pm" if m.group(2) else "am") if m else (None, None)


def join(move, recs):
    """(match id, match kind): the newest recommendation inside its horizon before the move that shares the add;
    failing that the drop; "unrelated" when rows are in horizon but none share either; "none" when no row is."""
    d = dt.date.fromisoformat(move["date"])
    cands = [r for r in recs if r.get("kind") != "hold" and
             0 <= (d - dt.date.fromisoformat(r["date"])).days <= int(r.get("horizon_days") or HORIZON_DAYS)]
    cands.sort(key=lambda r: (r["date"], r["id"]), reverse=True)
    adds, drops = set(move.get("added") or []), set(move.get("dropped") or [])
    for r in cands:
        if r.get("add") in adds:
            return r["id"], "exact" if (r.get("drop") in drops or (not r.get("drop") and not drops)) else "add_match_drop_differs"
    for r in cands:
        if r.get("drop") in drops:
            return r["id"], "drop_match_add_differs"
    return None, "unrelated" if cands else "none"


def move_key(m):
    return (m.get("team"), tuple(m.get("added") or []), tuple(m.get("dropped") or []),
            tuple(m.get("to_il") or []), tuple(m.get("from_il") or []))


def _repeat(row, existing):
    """True when the same move (team, adds, drops, IL) is already logged from a record dated within a day: the
    afternoon record and the next morning's record both see a move made between the two mornings (the morning
    diffs against the previous morning's baseline), and one move is one row."""
    d = dt.date.fromisoformat(row["date"])
    return any(move_key(m) == move_key(row) and abs((d - dt.date.fromisoformat(m["date"])).days) <= 1 for m in existing)


def moves_rows(news_dir, existing, recs, seat=OWNER_SEAT, seen_at=None, backfilled=False):
    """Seat `seat`'s moves in every league_moves record under news_dir that the ledger lacks, oldest record first."""
    out, rows = [], list(existing)
    paths = sorted(glob.glob(os.path.join(news_dir, "league_moves_*.json")), key=lambda p: (_date_of_record(p)[0] or "", "_pm" in p))
    for p in paths:
        date, phase = _date_of_record(p)
        if not date:
            continue
        try:
            rec = json.load(open(p, encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for m in rec.get("moves") or []:
            if m.get("seat") != seat or not any(m.get(k) for k in ("added", "dropped", "to_il", "from_il")):
                continue
            row = {"id": next_id(rows, "M", date), "date": date, "phase": phase, "seen_at": seen_at or now(),
                   "team": m.get("team"), "added": m.get("added") or [], "dropped": m.get("dropped") or [],
                   "to_il": m.get("to_il") or [], "from_il": m.get("from_il") or [],
                   "source": os.path.relpath(p, KIT) if p.startswith(KIT) else p}
            if _repeat(row, rows):
                continue
            row["matches"], row["match_kind"] = join(row, recs)
            if backfilled:
                row["backfilled"] = True
            out.append(row); rows.append(row)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--brief", metavar="DATE", help="append the day's brief row from report/briefs/brief_DATE.json")
    ap.add_argument("--moves", action="store_true", help="append every unlogged seat-10 move from data/news")
    ap.add_argument("--session", action="store_true", help="append a session row (needs --date, --add/--drop, --d-title)")
    ap.add_argument("--date"); ap.add_argument("--add"); ap.add_argument("--drop"); ap.add_argument("--d-title", type=float)
    ap.add_argument("--alternatives", default="[]", help="JSON list of {add?, drop, d_title}")
    ap.add_argument("--note", default=""); ap.add_argument("--record"); ap.add_argument("--supersedes")
    ap.add_argument("--made-at", help="ISO time; a back-filled row carries the time the advice was given")
    ap.add_argument("--backfilled", action="store_true")
    ap.add_argument("--dir", default=DIR); ap.add_argument("--briefs", default=BRIEFS); ap.add_argument("--news-dir", default=NEWS)
    a = ap.parse_args(argv)
    recs, sess, moves = (os.path.join(a.dir, os.path.basename(p)) for p in (RECS, SESSION, MOVES))
    out = []
    try:
        if a.brief:
            p = os.path.join(a.briefs, f"brief_{a.brief}.json")
            if not os.path.exists(p):
                raise LogError(f"no brief on disk for {a.brief} ({os.path.relpath(p, KIT)})")
            row = brief_row(json.load(open(p, encoding="utf-8")), read(recs), made_at=a.made_at, backfilled=a.backfilled)
            append(recs, [row]); out.append(f"{row['id']} {row['kind']} {row.get('add')} for {row.get('drop')}")
        if a.session:
            if not a.date or a.d_title is None or not (a.add or a.drop):
                raise LogError("--session needs --date, --d-title and --add and/or --drop")
            row = session_row(read(sess), a.date, a.add, a.drop, a.d_title, json.loads(a.alternatives), a.note, a.record,
                              made_at=a.made_at, supersedes=a.supersedes, backfilled=a.backfilled)
            append(sess, [row]); out.append(f"{row['id']} {row['kind']} {a.add} for {a.drop} ({a.d_title:+.2f})")
        if a.moves:
            rows = moves_rows(a.news_dir, read(moves), recommendations(recs, sess), backfilled=a.backfilled)
            append(moves, rows)
            out += [f"{r['id']} {r['phase']} +{','.join(r['added']) or '-'} -{','.join(r['dropped']) or '-'} -> {r['match_kind']} {r['matches'] or ''}".rstrip() for r in rows]
            if not rows:
                out.append("moves: nothing new")
    except LogError as e:
        print(f"DECISION LOG: HALT {e}")
        return 2
    print("DECISION LOG: PASS " + ("; ".join(out) if out else "nothing to do"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
