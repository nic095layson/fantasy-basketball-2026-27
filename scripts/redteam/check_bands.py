#!/usr/bin/env python3
"""Bands check: a report that quotes a title share must quote every FRAGILE constant's band (post-mortem
2026-10-19, finding 1: the report said ±0.4 where the structural band was ±3).

For each constant the sweep record tiers FRAGILE, the report must contain the constant's name (TEAM_WEEK_SHOCK,
with or without the module prefix), the word FRAGILE, and each variant's mean shift as a signed one-decimal
figure (+3.4, -2.3; a unicode minus is accepted). Writers read the sweep record, so the figures match by
construction; a hand-typed band that drifted from the record fails here.

    python3 scripts/redteam/check_bands.py --report R.md --sweep sweep.json
Prints 'BANDS CHECK: PASS — ...' / 'BANDS CHECK: FAIL' + problems. Exit 0 / 1.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(HERE))
DECK = os.path.abspath(os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball"))
sys.path.insert(0, os.path.dirname(HERE))
import sweep_record as SR  # noqa: E402


def _signed(x):
    return f"{x:+.1f}"


# a title share: "title" or "championship" within 120 characters of a percentage on one line (council verdict
# 2026-11-12: the rule is for reports that quote one; 89 reports carried the sentence, some quoting none)
_PCT = r"\d+(\.\d+)?\s?(%|percent\b)"
TITLE_SHARE = re.compile(rf"(title|championship)[^\n]{{0,120}}?{_PCT}|{_PCT}[^\n]{{0,120}}?(title|championship)", re.I)


def quotes_title_share(text):
    return bool(TITLE_SHARE.search(text))


def check(report_path, sweep_path, deck=None):
    """deck (owner 2026-11-17, "Flag it and re-sweep"): with a deck checkout, a sweep measured on another engine fails
    the check, whatever the report quotes: its figures are not the live engine's band (sweep_record.stale)."""
    with open(report_path, encoding="utf-8") as f:
        text = f.read().replace("−", "-").replace("–", "-")
    with open(sweep_path, encoding="utf-8") as f:
        sw = json.load(f)
    problems = []
    if deck:
        s = SR.stale(sw, deck)
        if s["status"] == "STALE":
            problems.append(f"the sweep record is STALE: {s['why']}; quote a sweep made on the live engine")
            return False, problems
    # owed when the report quotes a title share, or names a FRAGILE constant (a half-quoted band is still a fault)
    if not quotes_title_share(text) and not any(k.split(".", 1)[-1] in text for k in sw.get("fragile", [])):
        return True, problems
    for key in sw.get("fragile", []):
        c = sw["constants"][key]
        name = key.split(".", 1)[-1]
        if name not in text:
            problems.append(f"{key} is FRAGILE but the report never names it")
            continue
        if not re.search(rf"{re.escape(name)}.{{0,400}}FRAGILE|FRAGILE.{{0,400}}{re.escape(name)}", text, re.S):
            problems.append(f"{key}: the report names it but not as FRAGILE within 400 characters")
        for v in c["variants"]:
            s = _signed(v["shift_mean"])
            if s not in text:
                problems.append(f"{key}: band figure {s} ({v['label']}) is not quoted")
    return not problems, problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", required=True)
    ap.add_argument("--sweep", required=True)
    ap.add_argument("--deck", default=DECK, help="deck checkout the sweep's engine is compared with ('' to skip)")
    a = ap.parse_args()
    ok, problems = check(a.report, a.sweep, deck=a.deck or None)
    with open(a.sweep, encoding="utf-8") as f:
        sw = json.load(f)
    with open(a.report, encoding="utf-8") as f:
        t = f.read()
    quoted = quotes_title_share(t) or any(k.split(".", 1)[-1] in t for k in sw.get("fragile", []))
    if ok and not quoted:
        print(f"BANDS CHECK: PASS — the report quotes no title share and names no FRAGILE constant; bands not owed; engine {sw.get('engine_commit', '?')}")
    elif ok:
        print(f"BANDS CHECK: PASS — {len(sw.get('fragile', []))} FRAGILE band(s) quoted "
              f"({', '.join(sw.get('fragile', [])) or 'none'}); engine {sw.get('engine_commit', '?')}")
    else:
        print("BANDS CHECK: FAIL")
        for p in problems:
            print("  " + p)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
