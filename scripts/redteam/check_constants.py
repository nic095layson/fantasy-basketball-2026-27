#!/usr/bin/env python3
"""Engine constants: registry vs live engine (post-mortem 2026-10-19, D-PM-1 / D-PM-4; RULES.md rule 5).

The 10/19 red team found that the simulator's judgment constants (the games shock, the per-game CVs, the
availability tiers, 3.5 games a week) were hand-set, had never been tested against anything but themselves,
and moved the owner's title share by ±3 points — more than the ±0.4 the report quoted. Nothing could fail,
because nothing recorded what each constant was FOR or what vouched for it. This check makes that a gate:

  * every constant in scripts/redteam/constants_registry.json must equal the live deck value (drift);
  * every module-level UPPER_CASE constant of arena.py / hoops.py that the engine reads must be registered;
  * every entry carries a status — settings | structural | measured | declared_band | uncalibrated — with a
    record path for measured/declared_band/settings and a decision id for uncalibrated;
  * the deck commit is recorded (engine fingerprint).

    python3 scripts/redteam/check_constants.py [--deck PATH] [--json OUT]
Prints 'CONSTANTS CHECK: PASS — ...' and exits 0, or 'CONSTANTS CHECK: FAIL' with each problem, exit 1.
"""
import argparse
import importlib
import inspect
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(HERE))
DECK = os.path.abspath(os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball"))
REGISTRY = os.path.join(HERE, "constants_registry.json")
STATUSES = ("settings", "structural", "measured", "declared_band", "uncalibrated")
# Module-level names that are paths, derived aliases or environment, not judgment constants.
IGNORE = {"arena": {"ARENA_DIR", "REPO", "DATA", "CATS", "BASE_POS", "STRATEGIES", "DEFAULT"},
          "hoops": {"DATA_PATH", "FRESH_PATH", "STATE_PATH", "POSITIONAL_SLOTS", "COUNT_COLS", "MUST_HAVE",
                    "NUMERIC_COLS", "DECK_HTML", "NICKNAMES", "NAME_SUFFIXES"},
          # the kit's in-season blend (2026-10-19): paths and column maps are not judgment constants
          "season_lines": {"HERE", "KIT", "DECK", "KIT_CSV", "DECK_CSV", "ACTUALS", "OUT", "KIT_COLS", "DECK_COLS", "DEC"}}
TIER_NOTES = {"healthy": "", "mild": "inj-acl-mild", "risk": "inj-knee-risk", "recovery": "inj-achilles-recovery",
              "out": "out-season"}


def load_registry(path=REGISTRY):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _plain(v):
    """JSON-comparable form: tuples -> lists, dict order ignored, floats rounded."""
    if isinstance(v, dict):
        return {str(k): _plain(x) for k, x in sorted(v.items(), key=lambda kv: str(kv[0]))}
    if isinstance(v, (list, tuple)):
        return [_plain(x) for x in v]
    if isinstance(v, float):
        return round(v, 9)
    return v


def read_live(deck=DECK):
    """{(module, name): value} from the live deck modules, plus the two tier functions and the 3.5 games/week
    literal read out of team_week_model's source (it is not a module constant)."""
    for d in (os.path.join(deck, "scripts"), os.path.join(deck, "arena")):
        if d not in sys.path:
            sys.path.insert(0, d)
    hoops = importlib.import_module("hoops")
    arena = importlib.import_module("arena")
    kit_scripts = os.path.join(KIT, "scripts")
    if kit_scripts not in sys.path:
        sys.path.insert(0, kit_scripts)
    season_lines = importlib.import_module("season_lines")
    live = {}
    for modname, mod in (("arena", arena), ("hoops", hoops), ("season_lines", season_lines)):
        for name, val in vars(mod).items():
            if name.isupper() and not name.startswith("_") and name not in IGNORE[modname] \
                    and not callable(val) and not inspect.ismodule(val):
                live[(modname, name)] = val
    live[("hoops", "CATS")] = hoops.CATS
    live[("hoops", "availability")] = {t: hoops.availability({"note": n}) for t, n in TIER_NOTES.items()}
    live[("arena", "weekly_availability")] = {t: arena.weekly_availability({"note": n}) for t, n in TIER_NOTES.items()}
    src = inspect.getsource(arena.team_week_model)
    m = re.search(r"\bg\s*=\s*([0-9.]+)\s*\*\s*a\b", src)
    live[("arena", "GAMES_PER_WEEK")] = float(m.group(1)) if m else None
    return live


def deck_commit(deck=DECK):
    try:
        return subprocess.run(["git", "-C", deck, "rev-parse", "--short", "HEAD"], capture_output=True,
                              text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def check(registry, live):
    """(ok, problems) for a registry dict against a {(module, name): value} map."""
    problems = []
    seen = set()
    for e in registry.get("constants", []):
        key = (e.get("module"), e.get("name"))
        seen.add(key)
        label = f"{key[0]}.{key[1]}"
        if e.get("status") not in STATUSES:
            problems.append(f"{label}: status {e.get('status')!r} is not one of {', '.join(STATUSES)}")
        elif not (e.get("record") or "").strip():
            problems.append(f"{label}: status {e['status']} needs a record path or note")
        if e.get("status") == "uncalibrated" and not (e.get("decision") or "").strip():
            problems.append(f"{label}: uncalibrated needs a decision id (where the calibration is decided)")
        if not (e.get("role") or "").strip():
            problems.append(f"{label}: no role stated")
        if key not in live:
            problems.append(f"{label}: registered but not found in the live engine")
        elif _plain(live[key]) != _plain(e.get("value")):
            problems.append(f"{label}: registry {e.get('value')!r} != live {live[key]!r}")
    for key in sorted(live, key=str):
        if key not in seen:
            problems.append(f"{key[0]}.{key[1]}: live constant not registered (value {live[key]!r})")
    return not problems, problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--deck", default=DECK)
    ap.add_argument("--registry", default=REGISTRY)
    ap.add_argument("--json", help="write the check record here")
    a = ap.parse_args()
    reg = load_registry(a.registry)
    live = read_live(os.path.abspath(a.deck))
    ok, problems = check(reg, live)
    commit = deck_commit(os.path.abspath(a.deck))
    counts = {}
    for e in reg["constants"]:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    rec = {"verdict": "PASS" if ok else "FAIL", "engine_commit": commit,
           "registered": len(reg["constants"]), "live": len(live), "by_status": counts,
           "uncalibrated": [f"{e['module']}.{e['name']}" for e in reg["constants"] if e["status"] == "uncalibrated"],
           "declared_band": [f"{e['module']}.{e['name']}" for e in reg["constants"] if e["status"] == "declared_band"],
           "problems": problems}
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(rec, f, indent=1)
            f.write("\n")
    if ok:
        print(f"CONSTANTS CHECK: PASS — {len(reg['constants'])} registered = {len(live)} live on deck {commit}; "
              + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    else:
        print("CONSTANTS CHECK: FAIL")
        for p in problems:
            print("  " + p)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
