#!/usr/bin/env python3
"""Attack runner: the standing attack list (scripts/redteam/attacks.json) checked against its records and the
live engine, written as a numbered artifact (post-mortem 2026-10-19; RULES.md rule 5).

For each attack: the script must exist, the record it writes must exist, and where the record carries an engine
commit it must equal the live deck's HEAD, otherwise the attack is STALE: it was run on a different engine than
the one the report would describe (the 10/19 finding that the engine changed under the report). A record with no
commit field is UNFINGERPRINTED (allowed, named). --out writes the artifact; the PASS line carries the counts.

    python3 scripts/redteam/run_attacks.py --check [--out report/.../attacks.json] [--deck PATH]
"""
import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(HERE))
DECK = os.path.abspath(os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball"))
ATTACKS = os.path.join(HERE, "attacks.json")
sys.path.insert(0, os.path.dirname(HERE))
import run_ledger  # noqa: E402


def live_commit(deck=DECK):
    try:
        return subprocess.run(["git", "-C", deck, "rev-parse", "--short", "HEAD"], capture_output=True,
                              text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


ENGINE_FILES = run_ledger.ENGINE_FILES  # the ledger's definition of "the engine" (scripts/hoops.py, arena/arena.py)


def engine_commit(deck, rev="HEAD"):
    """The last commit at or before `rev` that touched ENGINE_FILES: the engine's content fingerprint (owner 2026-10-23,
    D1 — a deck commit that touches no engine file, such as CLAUDE.md, must not stale an attack record). '' when
    `rev` is not in the deck's history or the deck is unreadable."""
    try:
        return subprocess.run(["git", "-C", deck, "log", "-1", "--format=%h", "--abbrev=7", rev, "--", *ENGINE_FILES],
                              capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def _same(a, b):
    return bool(a) and bool(b) and (str(a).startswith(str(b)[:7]) or str(b).startswith(str(a)[:7]))


def _dig(rec, dotted):
    cur = rec
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()[:12]


def check(attacks, root, live_commit, deck=None):
    """With `deck`, a record made on another commit is CURRENT when the engine files are unchanged between its
    commit and `live_commit` (engine_commit of both agree); without `deck`, only the commit itself counts."""
    live_eng = engine_commit(deck, live_commit) if deck else ""
    rows, problems, seen = [], [], set()
    for a in attacks.get("attacks", []):
        row = dict(id=a.get("id"), name=a.get("name"), question=a.get("question"), script=a.get("script"),
                   record=a.get("record"), status="CURRENT", why="")
        if a.get("id") in seen:
            problems.append(f"duplicate attack id {a.get('id')}")
            row["status"] = "DUPLICATE"
        seen.add(a.get("id"))
        if a.get("retired"):
            row["status"] = "RETIRED"
            row["why"] = str(a["retired"])
            rows.append(row)
            continue
        sp = os.path.join(root, a.get("script") or "")
        rp = os.path.join(root, a.get("record") or "")
        if not a.get("script") or not os.path.exists(sp):
            row["status"], row["why"] = "MISSING", f"script {a.get('script')} not found"
        elif not a.get("record") or not os.path.exists(rp):
            row["status"], row["why"] = "MISSING", f"record {a.get('record')} not found"
        else:
            row["record_sha256"] = _sha(rp)
            if a.get("commit_field"):
                try:
                    with open(rp, encoding="utf-8") as f:
                        c = _dig(json.load(f), a["commit_field"])
                except ValueError as e:
                    c = None
                    row["why"] = f"record unreadable: {e}"
                if not c:
                    row["status"], row["why"] = "MISSING", row["why"] or f"record has no {a['commit_field']}"
                elif _same(live_commit, c):
                    row["engine_commit"] = c
                elif deck and live_eng and _same(engine_commit(deck, str(c)), live_eng):
                    row["engine_commit"] = c
                    row["why"] = f"made on {c}; engine files unchanged since (last engine commit {live_eng})"
                else:
                    row["status"], row["why"] = "STALE", (f"record made on engine {c}, live engine is {live_commit}"
                                                          + (f" (engine files last changed {live_eng})" if live_eng else ""))
            else:
                row["status"] = "UNFINGERPRINTED"
        if row["status"] in ("MISSING", "STALE", "DUPLICATE"):
            problems.append(f"{row['id']} {row['status']}: {row['why']}")
        rows.append(row)
    if not rows:
        problems.append("no attacks registered")
    counts = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    return dict(checked_at_utc=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                live_engine_commit=live_commit, live_engine_files_commit=live_eng, attacks=rows, by_status=counts,
                problems=problems,
                verdict="PASS" if not problems else "FAIL")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--attacks", default=ATTACKS)
    ap.add_argument("--deck", default=DECK)
    ap.add_argument("--out")
    ap.add_argument("--ledger", default=run_ledger.LEDGER,
                    help="run-ledger to append this check's verdict to as 'run_attacks' ('' to skip)")
    a = ap.parse_args()
    with open(a.attacks, encoding="utf-8") as f:
        attacks = json.load(f)
    rec = check(attacks, KIT, live_commit(os.path.abspath(a.deck)), deck=os.path.abspath(a.deck))
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(rec, f, indent=1, ensure_ascii=False)
            f.write("\n")
    if rec["verdict"] == "PASS":
        print(f"ATTACKS CHECK: PASS — {len(rec['attacks'])} attacks on engine {rec['live_engine_commit']}"
              + (f" (engine files last changed {rec['live_engine_files_commit']})" if rec.get('live_engine_files_commit') else "") + "; "
              + ", ".join(f"{k} {v}" for k, v in sorted(rec["by_status"].items())))
    else:
        print("ATTACKS CHECK: FAIL")
        for p in rec["problems"]:
            print("  " + p)
    if a.check and a.ledger:
        run_ledger.safe_record("run_attacks", rec["verdict"],
                               "; ".join(f"{k} {v}" for k, v in sorted(rec["by_status"].items())),
                               ledger=a.ledger, deck=os.path.abspath(a.deck))
    return 0 if rec["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
