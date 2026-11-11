#!/usr/bin/env python3
"""Run watch (owner 2026-11-10, pick "Decision card + watchdog", P4): did the day's morning or afternoon run leave its
records? One line, for a scheduled check that pushes to the owner only on ALERT. The scheduler's own "succeeded"
means the wake was delivered to the Runner, not that the run passed; nothing else looked.

    python3 scripts/run_watch.py --date 2026-11-10 --phase am --ref origin/season/daily   # read a git ref (fetch first)
    python3 scripts/run_watch.py --date 2026-11-10 --phase pm --root /path/to/checkout

am: report/briefs/morning_<date>.json must exist, read, say verdict PASS and hold no failed step (a non-fatal failure
    is named too: the run went on without that record); the morning report and the deck must exist. A failed morning's
    line names the command that finishes it (morning.py --resume). Owner 2026-11-11 (audit pick D): when the schedule
    on record shows NBA games the day before, that day's box scores (data/actuals) and manager-log day (data/managers)
    must exist too; with no schedule on record this is not checked.
pm: the afternoon report, the afternoon status file and the afternoon deck must exist.
Dates are the runs' own (UTC). Prints 'RUN WATCH: PASS — ...' (exit 0) or 'RUN WATCH: ALERT — ...' (exit 1). Reads only.
"""
import argparse
import datetime
import json
import os
import subprocess
import sys

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEDULE = "report/schedule/games-2026-27.csv"


def check(date, phase, read):
    """read(path) -> the file's text, or None when it is not there. Returns (verdict, line)."""
    probs = []
    if phase == "am":
        rec_p = f"report/briefs/morning_{date}.json"
        raw, ok = read(rec_p), None
        if raw is None:
            probs.append(f"no morning record ({rec_p})")
        else:
            try:
                rec = json.loads(raw)
                steps = rec.get("steps") or []
                bad = [s.get("name", "?") for s in steps if not str(s.get("verdict", "")).startswith("PASS")]
                if rec.get("verdict") != "PASS":
                    probs.append(f"morning verdict {rec.get('verdict')}" + (f" (failed: {', '.join(bad)})" if bad else "")
                                 + f"; finish it with: python3 scripts/morning.py --date {date} --resume")
                elif bad:
                    probs.append(f"morning PASS but {len(bad)} step{'s' if len(bad) > 1 else ''} failed: {', '.join(bad)}")
                else:
                    ok = f"morning PASS, {len(steps)} steps, no step failed"
            except ValueError:
                probs.append(f"morning record unreadable ({rec_p})")
        if read(f"report/briefs/morning_report_{date}.md") is None:
            probs.append("no morning report")
        if read(f"report/season/deck_{date}.html") is None:
            probs.append("no deck")
        sched = read(SCHEDULE)
        prev = (datetime.date.fromisoformat(date) - datetime.timedelta(days=1)).isoformat()
        if sched is not None and any(ln.startswith(prev + ",") for ln in sched.splitlines()):
            if read(f"data/actuals/{prev}.json") is None:
                probs.append(f"no box scores for {prev}")
            if read(f"data/managers/day_{prev}.json") is None:
                probs.append(f"no manager-log day for {prev}")
    else:
        for path, word in ((f"report/briefs/afternoon_report_{date}.md", "no afternoon report"),
                           (f"data/status/status_{date}_pm.json", "no afternoon status"),
                           (f"report/season/deck_{date}_pm.html", "no afternoon deck")):
            if read(path) is None:
                probs.append(word)
        ok = "afternoon report, status and deck are in"
    if probs:
        return "ALERT", f"RUN WATCH: ALERT — {phase} {date}: " + "; ".join(probs)
    return "PASS", f"RUN WATCH: PASS — {phase} {date}: {ok}"


def ref_reader(ref, cwd=KIT):
    def read(path):
        r = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=cwd, capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else None
    return read


def root_reader(root):
    def read(path):
        p = os.path.join(root, path)
        if not os.path.exists(p):
            return None
        with open(p, encoding="utf-8", errors="replace") as f:
            return f.read()
    return read


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", required=True); ap.add_argument("--phase", choices=("am", "pm"), required=True)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--ref", help="read the records from this git ref (for example origin/season/daily)")
    g.add_argument("--root", help="read the records from this directory (default: the kit checkout)")
    a = ap.parse_args()
    verdict, line = check(a.date, a.phase, ref_reader(a.ref) if a.ref else root_reader(a.root or KIT))
    print(line)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
