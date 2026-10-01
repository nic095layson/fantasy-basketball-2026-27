#!/usr/bin/env python3
"""Reproducibility gate for the derived layer (drift fix D4, 2026-09-29).

The 2026-09-29 validation found that every dated analysis in report/ read the
CURRENT pool when re-run, so a re-run of the 8/24 league projection or the
9/16 market statistics quietly produced different numbers from the ones the
committed report quotes. Each of those artifacts now ends with an input stamp
(report/derived.py) naming the files it read and the commit they came from.
This gate re-runs every registered artifact at its own pin into a temp dir
and compares the result with the committed file byte for byte — the
check_parity.py of the derived layer. Exit 0 only if every artifact
reproduces; exit 1 lists each file that differs (first lines of the diff).

Deliberately re-scoping an artifact to a newer pool is `<script> --live`
(or `--as-of <commit>`), which rewrites the file with a new stamp; commit it
and this gate follows the new pin. A registered artifact with no stamp fails
until it is regenerated with --as-of.

Usage: python3 report/check_derived.py [-v]     (-v: show each script's output)
"""
import difflib
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import derived  # noqa: E402

REGISTRY = [
    {"label": "2026-08-24 mock-draft league projection",
     "cmd": ["mock_draft_league_projection.py"], "out": "--out",
     "pin": "mock-draft-2026-08-24-analysis.md",
     "outputs": ["mock-draft-2026-08-24-analysis.md"]},
    {"label": "2026-09-15 market statistics (the 9/16 after-report's numbers)",
     "cmd": ["market/market_stats.py", "2026-09-15"], "out": "stdout",
     "pin": "market/market_stats-2026-09-15.txt",
     "outputs": ["market/market_stats-2026-09-15.txt"]},
    {"label": "2026-08-24 market build (Hashtag + Statdunk)",
     "cmd": ["market/build_market.py", "2026-08-24"], "out": "--out-dir",
     "pin": "market/unmatched-2026-08-24.md",
     "outputs": ["market/hashtag-2026-08-24.csv", "market/statdunk-2026-08-24.csv",
                 "market/unmatched-2026-08-24.md", "market/disagreements-2026-08-24.md"]},
    {"label": "2026-09-15 Yahoo intake (draft-analysis page)",
     "cmd": ["market/yahoo_market.py", "2026-09-15"], "out": "--out-dir",
     "pin": "market/unmatched-yahoo-2026-09-15.md",
     "outputs": ["market/yahoo-2026-09-15.csv", "market/consensus-2026-09-15.csv",
                 "market/unmatched-yahoo-2026-09-15.md", "market/disagreements-yahoo-2026-09-15.md"]},
    {"label": "2026-09-22 Yahoo 9-cat rankings page",
     "cmd": ["market/yahoo_market.py", "2026-09-22", "rankings"], "out": "--out-dir",
     "pin": "market/unmatched-yahoo-9cat-rankings-2026-09-22.md",
     "outputs": ["market/yahoo-9cat-rankings-2026-09-22.csv",
                 "market/unmatched-yahoo-9cat-rankings-2026-09-22.md"]},
    {"label": "2026-09-22 Yahoo intake (draft-analysis page)",
     "cmd": ["market/yahoo_market.py", "2026-09-22"], "out": "--out-dir",
     "pin": "market/unmatched-yahoo-2026-09-22.md",
     "outputs": ["market/yahoo-2026-09-22.csv", "market/consensus-2026-09-22.csv",
                 "market/unmatched-yahoo-2026-09-22.md", "market/disagreements-yahoo-2026-09-22.md"]},
    {"label": "2026-09-28 Yahoo 9-cat rankings page (top 250, official positions)",
     "cmd": ["market/yahoo_market.py", "2026-09-28", "rankings"], "out": "--out-dir",
     "pin": "market/unmatched-yahoo-9cat-rankings-2026-09-28.md",
     "outputs": ["market/yahoo-9cat-rankings-2026-09-28.csv",
                 "market/unmatched-yahoo-9cat-rankings-2026-09-28.md"]},
    {"label": "2026-09-29 expert consensus intake (owner upload, top 50)",
     "cmd": ["market/third_party_market.py", "experts", "2026-09-29"], "out": "--out-dir",
     "pin": "market/unmatched-experts-2026-09-29.md",
     "outputs": ["market/experts-2026-09-29.csv", "market/unmatched-experts-2026-09-29.md",
                 "market/disagreements-experts-2026-09-29.md"]},
    {"label": "2026-09-26 projected top 150 (owner paste; 2025-26 actual lines)",
     "cmd": ["market/third_party_market.py", "projected150", "2026-09-26"], "out": "--out-dir",
     "pin": "market/unmatched-projected150-2026-09-26.md",
     "outputs": ["market/projected150-2026-09-26.csv", "market/unmatched-projected150-2026-09-26.md",
                 "market/disagreements-projected150-2026-09-26.md"]},
    {"label": "2026-09-29 RotoBaller overall 9-cat projected rankings (owner upload, 250)",
     "cmd": ["market/third_party_market.py", "rotoballer", "2026-09-29"], "out": "--out-dir",
     "pin": "market/unmatched-rotoballer-2026-09-29.md",
     "outputs": ["market/rotoballer-2026-09-29.csv", "market/unmatched-rotoballer-2026-09-29.md",
                 "market/disagreements-rotoballer-2026-09-29.md"]},
    {"label": "2026-10-01 Yahoo intake (draft-analysis page, owner paste; the WO-4 price source)",
     "cmd": ["market/yahoo_market.py", "2026-10-01"], "out": "--out-dir",
     "pin": "market/unmatched-yahoo-2026-10-01.md",
     "outputs": ["market/yahoo-2026-10-01.csv", "market/consensus-2026-10-01.csv",
                 "market/unmatched-yahoo-2026-10-01.md", "market/disagreements-yahoo-2026-10-01.md"]},
    {"label": "2026-09-30 Hashtag projections + ADP pages (owner PDFs, read with pdfplumber)",
     "cmd": ["market/hashtag_pdf_market.py", "2026-09-30"], "out": "--out-dir",
     "pin": "market/unmatched-hashtag-2026-09-30.md",
     "outputs": ["market/hashtag-2026-09-30.csv", "market/hashtag-adp-2026-09-30.csv",
                 "market/unmatched-hashtag-2026-09-30.md"]},
    {"label": "2026-09-29 unnamed-outlet 9-cat top 144 with profiles + sleepers/breakouts/busts (owner paste)",
     "cmd": ["market/third_party_market.py", "profiles", "2026-09-29"], "out": "--out-dir",
     "pin": "market/unmatched-profiles-2026-09-29.md",
     "outputs": ["market/profiles-2026-09-29.csv", "market/profiles-tags-2026-09-29.csv",
                 "market/unmatched-profiles-2026-09-29.md", "market/disagreements-profiles-2026-09-29.md"]},
]


def _diff_head(committed, produced, n=8):
    a = committed.decode("utf-8", "replace").splitlines()
    b = produced.decode("utf-8", "replace").splitlines()
    return list(difflib.unified_diff(a, b, "committed", "reproduced", lineterm="", n=0))[:n]


def check(verbose=False):
    failures = 0
    for e in REGISTRY:
        pin = derived.pin_from(os.path.join(HERE, e["pin"]))
        if not pin:
            print(f"FAIL  {e['label']}: no input stamp in {e['pin']} — regenerate with --as-of and commit")
            failures += 1
            continue
        commit, pins = pin
        tmp = tempfile.mkdtemp(prefix="check-derived-")
        argv = [sys.executable, os.path.join(HERE, e["cmd"][0]), *e["cmd"][1:], "--as-of", commit]
        for f, c in pins.items():
            argv += ["--pin", f"{f}={c}"]
        produced = {}
        if e["out"] == "--out":
            target = os.path.join(tmp, os.path.basename(e["outputs"][0]))
            argv += ["--out", target]
        elif e["out"] == "--out-dir":
            argv += ["--out-dir", tmp]
        r = subprocess.run(argv, capture_output=True)
        if verbose:
            sys.stdout.write(r.stdout.decode("utf-8", "replace"))
            sys.stdout.write(r.stderr.decode("utf-8", "replace"))
        if r.returncode != 0:
            print(f"FAIL  {e['label']}: exit {r.returncode}")
            print("      " + r.stdout.decode("utf-8", "replace").strip().splitlines()[-1] if r.stdout.strip() else "")
            print("      " + r.stderr.decode("utf-8", "replace").strip().splitlines()[-1] if r.stderr.strip() else "")
            failures += 1
            continue
        for rel in e["outputs"]:
            committed = open(os.path.join(HERE, rel), "rb").read()
            if e["out"] == "stdout":
                got = r.stdout
            else:
                p = os.path.join(tmp, os.path.basename(rel))
                got = open(p, "rb").read() if os.path.exists(p) else None
            produced[rel] = (committed == got, committed, got)
        bad = [rel for rel, (ok, _, _) in produced.items() if not ok]
        pinned = ", ".join([commit[:7]] + [f"{f}@{c[:7]}" for f, c in pins.items()])
        if bad:
            failures += 1
            print(f"FAIL  {e['label']} (pin {pinned}): {len(bad)}/{len(e['outputs'])} differ")
            for rel in bad:
                _, c, g = produced[rel]
                print(f"      {rel}: " + ("not produced" if g is None else f"{len(c)} vs {len(g)} bytes"))
                if g is not None:
                    for line in _diff_head(c, g):
                        print("        " + line[:160])
        else:
            print(f"PASS  {e['label']} (pin {pinned}; {len(e['outputs'])} file{'s' if len(e['outputs']) != 1 else ''} identical)")
    return failures


def main():
    failures = check(verbose="-v" in sys.argv[1:])
    if failures:
        print(f"DERIVED: FAIL — {failures} of {len(REGISTRY)} artifacts do not reproduce from their pinned inputs")
        sys.exit(1)
    print(f"DERIVED: all {len(REGISTRY)} dated artifacts reproduce byte-for-byte from their pinned inputs")


if __name__ == "__main__":
    main()
