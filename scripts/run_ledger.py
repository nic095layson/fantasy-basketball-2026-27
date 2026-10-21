#!/usr/bin/env python3
"""The run-ledger: one append-only record of every gate that ran (Council 2026-10-21, 4-1; owner "build council's
fixes" the same night).

The defect it answers. On 2026-10-21 twelve errors were inventoried and eleven were confident claims about whether a
mechanism RUNS — a gate, a writer, a checkout, a connector — including a report line saying a governor had been
loaded when it had not. "Ran and passed" and "never ran" looked identical, because nothing wrote down that a run had
happened. The fix is reporting, not a new judgment: every gate appends one line here, and the questions "did it run,
on which engine, and did it pass" become a query instead of a recollection.

One JSON object per line in report/run-ledger.jsonl:

  {"name": ..., "ran_at": "YYYY-MM-DDTHH:MM:SSZ", "verdict": "PASS"|"FAIL",
   "kit_head": <7>, "deck_head": <7>, "engine_commit": <7>, "detail": ...}

engine_commit is the last deck commit that touched the engine files (ENGINE_FILES), not the deck HEAD — so a docs or
data commit does not make an attack "stale" while the engine is byte-identical (the 259c630 / d33942f case of
2026-10-21). deck_head is kept beside it for anyone who wants the stricter reading.

Producers: scripts/gates.py (each gate, as it finishes), scripts/morning.py (each step), scripts/redteam/
run_attacks.py (--check). Consumer: scripts/check_claims.py, claim kind "ledger_pass". The file is only ever opened
in append mode here; .gitattributes merges it with the union driver so two branches' appends never conflict.

    python3 scripts/run_ledger.py --last NAME                       # the latest row for NAME
    python3 scripts/run_ledger.py --check NAME [--max-age-hours H] [--live-engine]
                                                                     # exit 0 iff the latest row PASSED (fresh / on the live engine)
    python3 scripts/run_ledger.py --stale                           # names whose latest row is not on the live engine
    python3 scripts/run_ledger.py --record NAME --verdict PASS|FAIL [--detail TEXT]
"""
import argparse
import datetime
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
DECK = os.path.abspath(os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball"))
LEDGER = os.path.join(KIT, "report", "run-ledger.jsonl")
ENGINE_FILES = ("scripts/hoops.py", "arena/arena.py")
VERDICTS = ("PASS", "FAIL")


def _git(repo, *args):
    try:
        return subprocess.run(["git", "-C", repo] + list(args), capture_output=True, text=True,
                              check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def fingerprint(deck=DECK, kit=KIT):
    """kit HEAD, deck HEAD, and the last deck commit touching ENGINE_FILES (7 chars each; '' when unreadable).
    An engine file with uncommitted changes appends '+dirty': a run on an edited working tree is not a run on the
    committed engine, and must never be recorded as one (found 2026-10-21, the first row this ledger wrote)."""
    eng = _git(deck, "log", "-1", "--format=%h", "--abbrev=7", "--", *ENGINE_FILES)
    if eng and _git(deck, "status", "--porcelain", "--", *ENGINE_FILES):
        eng += "+dirty"
    return {"kit_head": _git(kit, "rev-parse", "--short=7", "HEAD"),
            "deck_head": _git(deck, "rev-parse", "--short=7", "HEAD"),
            "engine_commit": eng}


def _now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def record(name, verdict, detail="", ledger=LEDGER, deck=DECK, kit=KIT, ran_at=None):
    """Append one row. Never rewrites the file. Returns the row."""
    if verdict not in VERDICTS:
        raise ValueError(f"verdict must be one of {VERDICTS}, got {verdict!r}")
    if not name:
        raise ValueError("a ledger row needs a name")
    row = {"name": name, "ran_at": ran_at or _now(), "verdict": verdict}
    row.update(fingerprint(deck, kit))
    row["detail"] = (detail or "")[:300]
    os.makedirs(os.path.dirname(ledger), exist_ok=True)
    with open(ledger, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    return row


def safe_record(name, verdict, detail="", **kw):
    """record() for producers whose own run must not fail because the ledger could not be written."""
    try:
        return record(name, verdict, detail, **kw)
    except (OSError, ValueError) as e:
        print(f"run-ledger: not recorded ({e})", file=sys.stderr)
        return None


def read(ledger=LEDGER):
    """All rows, oldest first. A malformed line is skipped and counted, never silently dropped."""
    rows, bad = [], 0
    try:
        with open(ledger, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    bad += 1
    except OSError:
        pass
    if bad:
        print(f"run-ledger: {bad} malformed line(s) skipped in {ledger}", file=sys.stderr)
    return rows


def last(name, ledger=LEDGER):
    hit = None
    for r in read(ledger):
        if r.get("name") == name:
            hit = r
    return hit


def check(name, max_age_hours=None, live_engine=False, ledger=LEDGER, deck=DECK, now=None):
    """(ok, reason): the latest row for `name` exists and PASSED, and is within max_age_hours, and (live_engine)
    was made on the deck's current engine_commit."""
    r = last(name, ledger)
    if r is None:
        return False, f"no ledger row for {name!r} — it has never been recorded as run"
    if r.get("verdict") != "PASS":
        return False, f"latest {name!r} row ({r.get('ran_at')}) is {r.get('verdict')}"
    if max_age_hours is not None:
        now = now or datetime.datetime.now(datetime.timezone.utc)
        try:
            ran = datetime.datetime.strptime(r["ran_at"], "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=datetime.timezone.utc)
        except (KeyError, ValueError):
            return False, f"latest {name!r} row has no readable ran_at"
        age = (now - ran).total_seconds() / 3600
        if age > max_age_hours:
            return False, f"latest {name!r} PASS is {age:.1f}h old (limit {max_age_hours}h)"
    if live_engine:
        live = fingerprint(deck)["engine_commit"]
        if not live:
            return False, "live engine commit unreadable (deck repo missing?)"
        if r.get("engine_commit") != live:
            return False, (f"latest {name!r} PASS was on engine {r.get('engine_commit') or '?'}, "
                           f"live engine is {live}")
    return True, f"latest {name!r} PASSED at {r.get('ran_at')} on engine {r.get('engine_commit') or '?'}"


def stale(ledger=LEDGER, deck=DECK):
    """{name: latest row} for every name whose latest row is not on the live engine_commit."""
    live = fingerprint(deck)["engine_commit"]
    latest = {}
    for r in read(ledger):
        latest[r.get("name")] = r
    return {n: r for n, r in latest.items() if r.get("engine_commit") != live}, live


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ledger", default=LEDGER)
    ap.add_argument("--deck", default=DECK)
    ap.add_argument("--record", metavar="NAME")
    ap.add_argument("--verdict", choices=VERDICTS)
    ap.add_argument("--detail", default="")
    ap.add_argument("--last", metavar="NAME")
    ap.add_argument("--check", metavar="NAME")
    ap.add_argument("--max-age-hours", type=float)
    ap.add_argument("--live-engine", action="store_true")
    ap.add_argument("--stale", action="store_true")
    a = ap.parse_args()
    if a.record:
        if not a.verdict:
            ap.error("--record needs --verdict")
        print(json.dumps(record(a.record, a.verdict, a.detail, ledger=a.ledger, deck=a.deck)))
        return 0
    if a.last:
        r = last(a.last, a.ledger)
        print(json.dumps(r) if r else f"no ledger row for {a.last!r}")
        return 0 if r else 1
    if a.check:
        ok, why = check(a.check, a.max_age_hours, a.live_engine, a.ledger, a.deck)
        print(f"LEDGER CHECK: {'PASS' if ok else 'FAIL'} — {why}")
        return 0 if ok else 1
    if a.stale:
        st, live = stale(a.ledger, a.deck)
        print(f"live engine {live or '?'}; {len(st)} name(s) whose latest row is on another engine:")
        for n, r in sorted(st.items()):
            print(f"  {n}: {r.get('engine_commit') or '?'} ({r.get('verdict')}, {r.get('ran_at')})")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
