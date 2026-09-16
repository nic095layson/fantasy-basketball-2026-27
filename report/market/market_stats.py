#!/usr/bin/env python3
"""Divergence statistics for the Yahoo-vs-board after-report (2026-09-16).

Reads ONLY committed artifacts (consensus-YYYY-MM-DD.csv, yahoo-YYYY-MM-DD.csv,
projections-2026-27.csv) and prints the numbers the after-report quotes:
rank correlations, gap medians, the band-limited value/fade category lean, and
the room-vs-experts split inside Yahoo's own data. Deterministic; rerun to
re-verify the report's §2/§3/§7 figures.

Usage: python3 report/market/market_stats.py [YYYY-MM-DD]   (default 2026-09-15)
"""
import csv
import os
import statistics as st
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.dirname(HERE)
sys.path.insert(0, REPORT)
sys.path.insert(0, HERE)

BAND = 140          # our-rank depth where Yahoo ADP (max ~125) can disagree
                    # meaningfully; deeper "fades" are ADP-truncation artifacts
GAP = 15            # §5.3 arbitrage threshold (picks)
XRANK_CAP = 300     # placeholder-tier cap, same as yahoo_market.py


def spearman(pairs):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0] * len(v)
        for p, i in enumerate(order):
            r[i] = p + 1
        return r
    a, b = ranks([p[0] for p in pairs]), ranks([p[1] for p in pairs])
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    sa = (sum((x - ma) ** 2 for x in a)) ** 0.5
    sb = (sum((y - mb) ** 2 for y in b)) ** 0.5
    return cov / (sa * sb)


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else "2026-09-15"
    cons = list(csv.DictReader(open(os.path.join(HERE, f"consensus-{d}.csv"))))
    yah = list(csv.DictReader(open(os.path.join(HERE, f"yahoo-{d}.csv"))))

    with_x = [r for r in cons if r["yahoo_xrank"]]
    with_a = [r for r in cons if r["yahoo_adp"]]
    px = [(float(r["our_rank"]), float(r["yahoo_xrank"])) for r in with_x]
    pa = [(float(r["our_rank"]), float(r["yahoo_adp"])) for r in with_a]
    print(f"matched w/ XRank: {len(with_x)} | rho(our, XRank) = {spearman(px):.4f}")
    print(f"matched w/ ADP  : {len(with_a)} | rho(our, ADP)   = {spearman(pa):.4f}")
    print(f"median |our-XRank| = {st.median(abs(a - b) for a, b in px):.0f} | "
          f"median |our-ADP| = {st.median(abs(a - b) for a, b in pa):.0f}")

    band = [r for r in with_a if float(r["our_rank"]) <= BAND]
    gb = [abs(float(r["our_rank"]) - float(r["yahoo_adp"])) for r in band]
    print(f"band (our_rank<={BAND}, ADP present): {len(band)} players | "
          f"median |our-ADP| = {st.median(gb):.0f} | gap>=25: "
          f"{sum(1 for g in gb if g >= 25)}")

    # band-limited values/fades and their 9-cat z lean on OUR board
    import rank_engine as RE
    rows = RE.load(os.path.join(REPORT, "projections-2026-27.csv"))
    z1 = RE.zscores(rows, rows)
    pool = sorted(rows, key=lambda r: -RE.total(z1[r["name"]]))[:RE.POOL_SIZE]
    Z = RE.zscores(rows, pool)
    cats = ["fgp", "ftp", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"]
    val = [r for r in band if float(r["our_rank"]) + GAP <= float(r["yahoo_adp"])]
    fad = [r for r in band if float(r["yahoo_adp"]) + GAP <= float(r["our_rank"])]

    def lean(rs):
        zz = [Z[r["player"]] for r in rs if r["player"] in Z]
        return {c: sum(z[c] for z in zz) / len(zz) for c in cats}

    lv, lf = lean(val), lean(fad)
    print(f"\nband values n={len(val)} / fades n={len(fad)} — mean z per cat:")
    for c in sorted(cats, key=lambda c: -(lv[c] - lf[c])):
        print(f"  {c:4s} value {lv[c]:+.2f}  fade {lf[c]:+.2f}  "
              f"diff {lv[c] - lf[c]:+.2f}")

    # room vs Yahoo's own experts (most negative ADP - capped XRank)
    split = sorted((float(r["adp"]) - min(float(r["xrank"]), XRANK_CAP),
                    r["player"], r["xrank"], r["adp"], r["team"])
                   for r in yah if r["adp"])
    print("\nroom vs experts, 12 biggest room reaches (ADP minus capped XRank):")
    for dd, p, x, a, t in split[:12]:
        print(f"  {dd:+7.1f}  {p} ({t})  XRank {x} / ADP {a}")


if __name__ == "__main__":
    main()
