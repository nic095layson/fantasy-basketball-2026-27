"""Which assumption-sweep record the brief and the deck quote (owner 2026-10-26, "re-measure the ranges every Monday"):
the newest report/after-reports/redteam-<date>-season/sweep.json dated on or before the day (a Monday whose sweep
failed wrote none, so the last one stands); before the first season record, the draft sweep of 2026-10-19."""
import datetime
import glob
import os
import re

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(KIT, "report", "after-reports")
DRAFT = "redteam-2026-10-19"
_DIR = re.compile(r"redteam-(\d{4}-\d{2}-\d{2})(-season(-real)?)?$")


def latest(date, root=ROOT):
    found = []
    # "-season-real": the 2026-10-26 real-schedule record, written beside that day's practice-schedule one; on a tie
    # of dates it wins
    for p in glob.glob(os.path.join(root, "redteam-*-season*", "sweep.json")):
        m = _DIR.search(os.path.basename(os.path.dirname(p)))
        if m and m.group(1) <= date:
            found.append((m.group(1), bool(m.group(3)), p))
    return max(found)[2] if found else os.path.join(root, DRAFT, "sweep.json")


def describe(rec, path, as_of=None):
    """The record's configuration and date. Audit finding F2 (2026-11-12): the label said "current rosters" on a sweep
    three days old, so it names the rosters as the sweep's own and, given the day it is quoted on, the sweep's age."""
    m = _DIR.search(os.path.basename(os.path.dirname(path)))
    when = m.group(1) if m else "?"
    if rec.get("state_sha256"):
        age = ""
        if as_of and m:
            days = (datetime.date.fromisoformat(as_of) - datetime.date.fromisoformat(when)).days
            age = "made today; " if days == 0 else f"{days} day{'s' if days != 1 else ''} old; " if days > 0 else ""
        return (f"season sweep of {when} ({age}rosters of that date, season pool, "
                + ("real schedule" if rec.get("schedule") else "practice schedule") + ")")
    return f"draft sweep of {when} (draft rosters, frozen pool)"
