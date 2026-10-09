#!/usr/bin/env python3
"""ADP refresh (owner 2026-10-09): the WO-4 price file re-priced from Hashtag's projections page, whose ADP
column is Yahoo's ADP (owner verification 2026-10-09: "Hashtag compiles the most up-to-date ADP from Yahoo
system"). The page carries 200 names and Yahoo's paste 250, so the refreshed file keeps the paste's rows
(and its XRank, which the deck's mock bots read) and replaces the ADP of every name the page prices; a name
the page does not carry keeps the paste's ADP, and the sibling .md says which. Names the page prices that
the paste lacks are appended without an XRank.

  yahoo-<date>.csv       player,team,pos,xrank,adp — the deck's price file (scripts/market_prices.py reads
                         the newest yahoo-*.csv in this directory)
  adp-refresh-<date>.md  composition counts, the largest moves, the page names without an ADP, the stamp

Transcription invariants: every base row present exactly once; every ADP numeric; the re-priced count equals
the page's priced names found in the base. Exit 2 on any failure.
Usage: python3 report/market/adp_refresh.py [YYYY-MM-DD] [--as-of DATE|COMMIT | --live] [--out-dir DIR]
"""
import argparse
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import build_market as BM  # noqa: E402
import derived  # noqa: E402

COLS = ["player", "team", "pos", "xrank", "adp"]


def main():
    ap = derived.add_args(argparse.ArgumentParser(description="ADP refresh: the price file re-priced from Hashtag's Yahoo ADP column"))
    ap.add_argument("date", nargs="?", default="2026-10-09", help="page date (default 2026-10-09)")
    ap.add_argument("--out-dir", default=HERE)
    args = ap.parse_args()
    d, out = args.date, args.out_dir
    inp = derived.inputs_for(args, os.path.join(HERE, f"adp-refresh-{d}.md"))
    bases = sorted(f for f in inp.listdir("report/market")
                   if re.fullmatch(r"yahoo-\d{4}-\d{2}-\d{2}\.csv", f) and f < f"yahoo-{d}.csv")
    if not bases:
        sys.exit("no earlier yahoo-YYYY-MM-DD.csv to re-price")
    base_name = bases[-1]
    base_path = inp.path(f"report/market/{base_name}")
    page_path = inp.path(f"report/market/hashtag-{d}.csv")
    alias_index = {}
    for ours, variants in BM.ALIASES.items():
        for v in variants:
            alias_index[BM.norm(v)] = BM.norm(ours)
    canon = lambda n: alias_index.get(BM.norm(n), BM.norm(n))
    with open(base_path, encoding="utf-8") as f:
        base = list(csv.DictReader(f))
    with open(page_path, encoding="utf-8") as f:
        page = list(csv.DictReader(f))
    priced = {canon(r["player"]): r for r in page if r["adp"]}
    unpriced = [r for r in page if not r["adp"]]
    rows, moves, kept, problems = [], [], [], []
    seen = set()
    for r in base:
        k = canon(r["player"])
        if k in seen:
            problems.append(f"duplicate base row: {r['player']}")
        seen.add(k)
        new = dict(r)
        if k in priced:
            new["adp"] = priced[k]["adp"]
            if r["adp"]:
                moves.append((r["player"], float(r["adp"]), float(priced[k]["adp"])))
        else:
            kept.append(r["player"])
        rows.append({c: new.get(c, "") for c in COLS})
    appended = [r for k, r in priced.items() if k not in seen]
    for r in appended:
        rows.append({"player": r["player"], "team": r["team"], "pos": r["pos"], "xrank": "", "adp": r["adp"]})
    for r in rows:
        if r["adp"]:
            try:
                float(r["adp"])
            except ValueError:
                problems.append(f"non-numeric ADP: {r['player']} {r['adp']!r}")
    if len(rows) != len(base) + len(appended):
        problems.append("row count mismatch")
    n_repriced = sum(1 for r in base if canon(r["player"]) in priced)
    if n_repriced != len(moves) + sum(1 for r in base if canon(r["player"]) in priced and not r["adp"]):
        problems.append("re-priced count does not reconcile")
    print(f"base {base_name}: {len(base)} rows; page hashtag-{d}.csv: {len(page)} rows, {len(priced)} with an ADP; "
          f"re-priced {n_repriced}, kept the base ADP {len(kept)}, appended {len(appended)}")
    if problems:
        print(f"TRANSCRIPTION GATE: FAIL — {len(problems)} problem(s)")
        for p in problems:
            print(" ", p)
        sys.exit(2)
    print("TRANSCRIPTION GATE: PASS")
    BM._write_csv(os.path.join(out, f"yahoo-{d}.csv"), COLS, rows)
    deltas = [b - a for _, a, b in moves]
    L = [f"# ADP refresh — {d}: `{base_name}` re-priced from `hashtag-{d}.csv` (Yahoo ADP column)", "",
         f"Owner verification (2026-10-09): Hashtag's page carries the current Yahoo ADP. Base rows {len(base)}; the page prices "
         f"{len(priced)} of its {len(page)} names; re-priced {n_repriced}; {len(kept)} base rows keep the base ADP (outside the "
         f"page's top {len(page)}); {len(appended)} appended. XRank unchanged (the base paste's).", ""]
    if moves:
        L += [f"Moves among the {len(moves)} re-priced rows that had a base ADP: mean |diff| {sum(abs(x) for x in deltas) / len(deltas):.2f}, "
              f"largest |diff| {max(abs(x) for x in deltas):.1f}; {sum(abs(x) >= 5 for x in deltas)} of 5+ places.", "",
              "| player | base ADP | page ADP | diff |", "|---|---|---|---|"]
        for p, a, b in sorted(moves, key=lambda x: -abs(x[2] - x[1]))[:15]:
            L.append(f"| {p} | {a} | {b} | {b - a:+.1f} |")
    L += ["", "## Base rows keeping the base ADP (not on the page)", "", ", ".join(kept) or "none", "",
          "## Page names without an ADP", "", ", ".join(f"{r['player']} (R# {r['rank']})" for r in unpriced) or "none", ""]
    if appended:
        L += ["## Appended from the page (no base row)", "", ", ".join(r["player"] for r in appended), ""]
    L += [inp.stamp()]
    with open(os.path.join(out, f"adp-refresh-{d}.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(f"wrote yahoo-{d}.csv, adp-refresh-{d}.md")


if __name__ == "__main__":
    main()
