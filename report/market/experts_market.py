#!/usr/bin/env python3
"""Expert-consensus intake (owner upload 2026-09-29): a top-N "consensus combination of
experts' individual rankings" for 9-cat, landed as a REFERENCE source next to the Yahoo,
Hashtag and Statdunk snapshots. The board stays first-principles (owner decision
2026-08-21; fix F2: a single outlet never changes a pool row).

Reads experts-raw-<date>.csv verbatim as uploaded (columns Rank, Player, Pos, Team,
vs '25, Fantrax ADP, '25-26 FPPG, Avg rank; a UTF-8 BOM is tolerated), joins every row
to the pool under the work order's HARD unmatched gate (§3.3: every expert name matches a
pool row or is a recorded, reasoned absence — exit 3 otherwise), and writes:
  experts-<date>.csv              expert rank / avg rank / Fantrax ADP joined to our board rank,
                                  availability-adjusted z and the newest Yahoo XRank/ADP on file
  unmatched-experts-<date>.md     the gate report
  disagreements-experts-<date>.md rank agreement (Spearman), top-50 coverage, and the two
                                  disagreement tables (we are higher / the experts are higher)
  provenance.csv                  one row merged by (source, fetched_on)
Drift fix D4 applies: --as-of / --live / --out-dir, and the .md outputs end with the input
stamp; report/check_derived.py reproduces the committed intake at its pin.

Usage: python3 report/market/experts_market.py [YYYY-MM-DD] [--as-of DATE|COMMIT | --live] [--out-dir DIR]
"""
import argparse
import csv
import os
import re
import statistics as st
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = HERE
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import build_market as BM  # noqa: E402  norm(), ALIASES, our_board(), _write_csv, _merge_provenance, _zprofile
import derived  # noqa: E402
from market_stats import spearman  # noqa: E402

GAP = 10  # places: the disagreement threshold for the two tables
# Expert names verified absent from the pool (none on the 2026-09-29 upload).
_ACCEPTED_ABSENT = {}


def main():
    global OUT
    ap = derived.add_args(argparse.ArgumentParser(description="expert-consensus intake under the hard unmatched gate"))
    ap.add_argument("date", nargs="?", default="2026-09-29")
    ap.add_argument("--out-dir", default=HERE)
    args = ap.parse_args()
    d = args.date
    OUT = args.out_dir
    BM.OUT = OUT
    inp = derived.inputs_for(args, os.path.join(HERE, f"unmatched-experts-{d}.md"))
    raw = list(csv.DictReader(open(inp.path(f"report/market/experts-raw-{d}.csv"), encoding="utf-8-sig")))
    if not raw or "Player" not in raw[0] or "Avg rank" not in raw[0]:
        sys.exit("experts_market: unexpected columns in the raw upload")
    board = BM.our_board(inp.path("report/projections-2026-27.csv"))
    # newest Yahoo consensus file on or before the intake date, for the reference columns
    cands = sorted(f for f in inp.listdir("report/market")
                   if re.fullmatch(r"consensus-\d{4}-\d{2}-\d{2}\.csv", f) and f[10:20] <= d)
    yah, yah_name = {}, None
    if cands:
        yah_name = cands[-1]
        yah = {BM.norm(r["player"]): r for r in csv.DictReader(open(inp.path(f"report/market/{yah_name}"), encoding="utf-8"))}

    alias_index = {BM.norm(v): BM.norm(k) for k, vs in BM.ALIASES.items() for v in vs}
    by_key = {alias_index.get(BM.norm(n), BM.norm(n)): (n, b) for n, b in board.items()}
    rows, unmatched = [], []
    for r in raw:
        key = alias_index.get(BM.norm(r["Player"]), BM.norm(r["Player"]))
        hit = by_key.get(key)
        if hit is None:
            unmatched.append((int(r["Rank"]), r["Player"], r.get("Team", "")))
            continue
        n, b = hit
        y = yah.get(BM.norm(n), {})
        rows.append({"expert_rank": int(r["Rank"]), "player": n, "team": b["row"]["team"], "pos": b["row"]["pos"],
                     "avg_rank": r["Avg rank"], "fantrax_adp": r["Fantrax ADP"], "vs_25": r.get("vs '25", ""),
                     "our_rank": b["rank"], "z_adj": round(b["z_adj"], 3),
                     "yahoo_xrank": y.get("yahoo_xrank", ""), "yahoo_adp": y.get("yahoo_adp", ""),
                     "expert_name": r["Player"]})
    trips = [u for u in unmatched if u[1] not in _ACCEPTED_ABSENT]
    print(f"JOIN: {len(raw)} expert rows | matched to pool={len(rows)} | unmatched={len(unmatched)} (unexplained {len(trips)})")
    if trips:
        print("HARD GATE TRIP — expert names with no pool row (add a verified alias or record the absence):")
        for rk, n, t in trips:
            print(f"  #{rk:<4} {n} ({t})")
        sys.exit(3)

    BM._write_csv(os.path.join(OUT, f"experts-{d}.csv"),
                  ["expert_rank", "player", "team", "pos", "avg_rank", "fantrax_adp", "vs_25", "our_rank", "z_adj",
                   "yahoo_xrank", "yahoo_adp", "expert_name"], rows)
    stamp = inp.stamp()
    # ---- gate report
    L = [f"# Unmatched-name report vs the expert consensus — {d} (HARD GATE, work order §3.3)", "",
         f"Expert rows: {len(raw)}; pool players: {len(board)}. Every expert name below did NOT join to a pool row "
         "after normalization and documented aliases; each is an accepted genuine absence with a reason. "
         "Silent partial joins are refused.", "",
         f"## Not matched to the pool ({len(unmatched)})", "",
         "| expert # | name | team | reason |", "|---|---|---|---|"]
    for rk, n, t in unmatched:
        L.append(f"| {rk} | {n} | {t} | {_ACCEPTED_ABSENT.get(n, '')} |")
    L += ["", stamp]
    open(os.path.join(OUT, f"unmatched-experts-{d}.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")

    # ---- disagreements
    n_exp = len(rows)
    pairs = [(float(r["our_rank"]), float(r["avg_rank"])) for r in rows]
    rho = spearman(pairs)
    pa = [(float(r["our_rank"]), float(r["fantrax_adp"])) for r in rows if r["fantrax_adp"]]
    rho_adp = spearman(pa) if len(pa) > 2 else float("nan")
    py = [(float(r["our_rank"]), float(r["yahoo_xrank"])) for r in rows if r["yahoo_xrank"]]
    rho_y = spearman(py) if len(py) > 2 else float("nan")
    ours_top = sorted(board.values(), key=lambda b: b["rank"])[:n_exp]
    ours_top_names = {b["row"]["name"] for b in ours_top}
    in_both = [r for r in rows if r["player"] in ours_top_names]
    ours_only = [b["row"]["name"] for b in ours_top if b["row"]["name"] not in {r["player"] for r in rows}]
    med = st.median(abs(a - b) for a, b in pairs)
    higher = sorted([r for r in rows if r["our_rank"] + GAP <= r["expert_rank"]], key=lambda r: r["our_rank"] - r["expert_rank"])
    lower = sorted([r for r in rows if r["expert_rank"] + GAP <= r["our_rank"]], key=lambda r: -(r["our_rank"] - r["expert_rank"]))
    prof = lambda name: BM._zprofile({"name": name})
    fmt = lambda v: v if v not in ("", None) else "—"
    D = [f"# Expert consensus vs the board — {d}", "",
         f"Source: the owner's upload of a top-{len(raw)} consensus of experts' individual 9-cat rankings "
         f"(`experts-raw-{d}.csv`, kept verbatim; Fantrax ADP column carried through). Reference layer only: "
         "the board is first-principles and no row changes because of this file (owner decision 2026-08-21; fix F2).", "",
         "## A. Agreement", "",
         "| measure | value |", "|---|---|",
         f"| expert rows joined | {n_exp} of {len(raw)} |",
         f"| Spearman rho, our rank vs expert average rank | {rho:.3f} |",
         f"| Spearman rho, our rank vs Fantrax ADP | {rho_adp:.3f} ({len(pa)} rows) |",
         f"| Spearman rho, our rank vs Yahoo XRank ({yah_name or 'no Yahoo file'}) | {rho_y:.3f} ({len(py)} rows) |",
         f"| median absolute gap, our rank vs expert rank | {med:.0f} places |",
         f"| experts' top {n_exp} inside our top {n_exp} | {len(in_both)} of {n_exp} |",
         f"| our top {n_exp} the experts leave outside their {n_exp} | {len(ours_only)}: {', '.join(ours_only)} |", "",
         f"## B. We are higher by {GAP}+ places ({len(higher)}) — the board's values against the experts", "",
         "| gap | player | our # | expert # (avg) | Fantrax ADP | Yahoo XRank / ADP | our board z-lean |", "|---|---|---|---|---|---|---|"]
    for r in higher:
        D.append(f"| +{r['expert_rank'] - r['our_rank']} | {r['player']} | {r['our_rank']} | {r['expert_rank']} ({r['avg_rank']}) | {fmt(r['fantrax_adp'])} | {fmt(r['yahoo_xrank'])} / {fmt(r['yahoo_adp'])} | {prof(r['player'])} |")
    D += ["", f"## C. The experts are higher by {GAP}+ places ({len(lower)}) — the board's fades against the experts", "",
          "| gap | player | our # | expert # (avg) | Fantrax ADP | Yahoo XRank / ADP | our board z-lean |", "|---|---|---|---|---|---|---|"]
    for r in lower:
        D.append(f"| -{r['our_rank'] - r['expert_rank']} | {r['player']} | {r['our_rank']} | {r['expert_rank']} ({r['avg_rank']}) | {fmt(r['fantrax_adp'])} | {fmt(r['yahoo_xrank'])} / {fmt(r['yahoo_adp'])} | {prof(r['player'])} |")
    D += ["", "## D. Every row", "",
          "| expert # | avg | Fantrax ADP | player | team | our # | Yahoo XRank / ADP |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        D.append(f"| {r['expert_rank']} | {r['avg_rank']} | {fmt(r['fantrax_adp'])} | {r['player']} | {r['team']} | {r['our_rank']} | {fmt(r['yahoo_xrank'])} / {fmt(r['yahoo_adp'])} |")
    D += ["", stamp]
    open(os.path.join(OUT, f"disagreements-experts-{d}.md"), "w", encoding="utf-8").write("\n".join(D) + "\n")

    BM._merge_provenance([{"source": "experts", "url": "(owner upload — consensus of experts' individual 9-cat rankings; Fantrax ADP column)",
                           "fetched_on": d, "rows": len(raw),
                           "notes": f"Top-{len(raw)} expert consensus uploaded by the owner on {d} and kept verbatim as experts-raw-{d}.csv "
                                    "(Rank, Player, Pos, Team, vs '25, Fantrax ADP, '25-26 FPPG (empty), Avg rank). Joined to the pool "
                                    f"under the hard gate by experts_market.py ({len(rows)} matched, {len(unmatched)} absent); reference "
                                    "layer only — no board row changes (fix F2)."}])
    print(f"wrote experts-{d}.csv, unmatched-experts-{d}.md, disagreements-experts-{d}.md, provenance.csv")
    print(f"rho(our, expert avg) = {rho:.3f} | rho(our, Fantrax ADP) = {rho_adp:.3f} | rho(our, Yahoo XRank) = {rho_y:.3f} | "
          f"in both top-{n_exp}: {len(in_both)}")
    print("GATE PASS — every expert name matched or recorded as a genuine absence.")


if __name__ == "__main__":
    main()
