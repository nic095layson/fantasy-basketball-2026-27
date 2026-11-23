"""Which assumption-sweep record the brief and the deck quote (owner 2026-10-26, "re-measure the ranges every Monday"):
the newest report/after-reports/redteam-<date>-season/sweep.json dated on or before the day (a Monday whose sweep
failed wrote none, so the last one stands); before the first season record, the draft sweep of 2026-10-19."""
import datetime
import glob
import os
import re
import subprocess

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


ENGINE_FILES = ("scripts/hoops.py", "arena/arena.py")   # run_ledger.ENGINE_FILES: the deck files that are "the engine"


def _engine_at(deck, rev):
    """The last deck commit at or before `rev` that touched the engine files (run_attacks.engine_commit's rule), or ''
    when `rev` is not in the checkout or the deck is unreadable."""
    try:
        return subprocess.run(["git", "-C", deck, "log", "-1", "--format=%h", "--abbrev=7", rev, "--", *ENGINE_FILES],
                              capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def stale(rec, deck):
    """Owner 2026-11-17 (card: "Flag it and re-sweep"): is this sweep's engine the live one? On 2026-11-17 the brief
    and the deck quoted Monday morning's sweep (engine c933f07: shock 0.06, healthy 0.88) beside a title share computed
    after that afternoon's constants changed, with nothing to say so. The rule is the attack runner's: the record is
    CURRENT when the engine files are unchanged between its commit and the deck's HEAD, STALE when they differ, and
    UNKNOWN (never guessed) when the record names no engine or its commit is not in the deck checkout.
    Returns {"status", "why"}. A change of the season lines' method is not seen here: only the engine is."""
    c = (rec or {}).get("engine_commit") or (rec or {}).get("engine")
    if not c:
        return dict(status="UNKNOWN", why="the record names no engine")
    if not deck or not os.path.isdir(deck):
        return dict(status="UNKNOWN", why="no deck checkout to compare with")
    live = _engine_at(deck, "HEAD")
    if not live:
        return dict(status="UNKNOWN", why="the deck checkout has no readable history")
    then = _engine_at(deck, str(c))
    if not then:
        return dict(status="UNKNOWN", why=f"commit {c} is not in the deck checkout")
    if then == live:
        return dict(status="CURRENT", why="")
    return dict(status="STALE", why=f"measured on engine {then}, the live engine is {live}")


def stale_note(s):
    """The words the brief and the deck print for stale()'s answer: loud for STALE, plain for UNKNOWN, none for CURRENT."""
    if not s or s.get("status") == "CURRENT":
        return ""
    if s["status"] == "STALE":
        return f"STALE: {s['why']}, so these shifts are not today's"
    return f"not compared with the live engine: {s['why']}"


def shown_bands(rec):
    """The constants whose band the brief and the deck print beside a title share: every FRAGILE one; when none is
    FRAGILE, the SENSITIVE one that moves the headline most (owner 2026-11-17, card "Show the largest band anyway":
    the sweep of that day had none at 2 points while the availability tiers moved the title share by 1.9). A record
    with neither shows none."""
    consts = (rec or {}).get("constants") or {}
    fragile = (rec or {}).get("fragile") or [k for k, c in consts.items() if c.get("tier") == "FRAGILE"]
    if fragile:
        return list(fragile)
    size = lambda k: consts[k].get("max_abs_shift", max((abs(v["shift_mean"]) for v in consts[k].get("variants") or []), default=0.0))
    sens = [k for k, c in consts.items() if c.get("tier") == "SENSITIVE"]
    return [max(sens, key=size)] if sens else []

