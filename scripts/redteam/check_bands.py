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
import re
import sys


def _signed(x):
    return f"{x:+.1f}"


def check(report_path, sweep_path):
    with open(report_path, encoding="utf-8") as f:
        text = f.read().replace("−", "-").replace("–", "-")
    with open(sweep_path, encoding="utf-8") as f:
        sw = json.load(f)
    problems = []
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
    a = ap.parse_args()
    ok, problems = check(a.report, a.sweep)
    with open(a.sweep, encoding="utf-8") as f:
        sw = json.load(f)
    if ok:
        print(f"BANDS CHECK: PASS — {len(sw.get('fragile', []))} FRAGILE band(s) quoted "
              f"({', '.join(sw.get('fragile', [])) or 'none'}); engine {sw.get('engine_commit', '?')}")
    else:
        print("BANDS CHECK: FAIL")
        for p in problems:
            print("  " + p)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
