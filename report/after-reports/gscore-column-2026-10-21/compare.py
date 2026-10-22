#!/usr/bin/env python3
"""D-ZS-2 record (owner 2026-10-21 "Build it"): the season board's G column against its z order on the 10/21 lines.
Reads data/season/projections_season.csv and data/season/gscore_tau.json through scripts/season_board.py; writes
compare.json beside itself. Comparison only: nothing here orders the board.

  agreement  Spearman rank correlation of G rank and z rank over the z top 156 (12 teams x 13 non-IL spots) and 180
  movers     the largest G-minus-z rank differences inside the z top 156
  weights    each category's effective G/z ratio on the board: sigma / sqrt(sigma^2 + kappa (tau/g)^2) for counting
             categories; for FG%/FT% the median of G/z over the pool, which also carries Table 5b's definition
  defn       FG%/FT% with tau_R = 0 (the paper's Z) against the kit's z: the part of the percentage change that is
             definition, not week-to-week variance
  g = 3.5    the same comparison with 3.5 games a week (the arena's figure) in place of the logs' 3.0065
"""
import copy, json, os, statistics, sys
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(KIT, "scripts"))
import season_board as SB  # noqa: E402
import rank_engine as RE  # noqa: E402

LINES = os.path.join(KIT, "data", "season", "projections_season.csv")


def spearman(a, b):
    n = len(a); ra = {x: i for i, x in enumerate(sorted(a, key=a.get))}; rb = {x: i for i, x in enumerate(sorted(b, key=b.get))}
    return 1 - 6 * sum((ra[k] - rb[k]) ** 2 for k in a) / (n * (n * n - 1))


def compare(b, top):
    rows = b["board"][:top]
    z = {r["name"]: i for i, r in enumerate(b["board"], 1)}
    g = {r["name"]: r["g_rank"] for r in b["board"]}
    names = [r["name"] for r in rows]
    diff = sorted(((g[n] - z[n], n) for n in names), key=lambda t: (-abs(t[0]), t[1]))
    return dict(top=top, spearman=round(spearman({n: z[n] for n in names}, {n: g[n] for n in names}), 4),
                moved_10_plus=sum(1 for d, _ in diff if abs(d) >= 10), same_top_12=len(set(names[:12]) & {n for n in names if g[n] <= 12}),
                largest=[dict(name=n, z_rank=z[n], g_rank=g[n]) for d, n in diff[:12]])


def main():
    pin = SB.load_pin(SB.GSCORE)
    b = SB.build(LINES)
    rows, _ = RE.exclude_held(RE.load(LINES))
    z1 = RE.zscores(rows, rows)
    pool = sorted(rows, key=lambda r: -RE.total(z1[r["name"]]))[:RE.POOL_SIZE]
    z2, g2 = RE.zscores(rows, pool), SB.gscores(rows, pool, pin)
    k, gw = pin["kappa"], pin["games_per_week"]
    weights = {}
    for cat in RE.COUNTING + ["tov"]:
        sd = statistics.pstdev([r[cat] for r in pool])
        weights[cat] = round(sd / (sd ** 2 + k * (pin["tau"][cat] / gw) ** 2) ** 0.5, 4)
    zero = dict(pin, tau_r={c: 0.0 for c in pin["tau_r"]})
    g0 = SB.gscores(rows, pool, zero)
    defn = {}
    for cat in ("fgp", "ftp"):
        ratio = [g2[r["name"]][cat] / z2[r["name"]][cat] for r in pool if abs(z2[r["name"]][cat]) > 0.25]
        weights[cat] = round(statistics.median(ratio), 4)
        defn[cat] = dict(paper_Z_over_kit_z_median=round(statistics.median(g0[r["name"]][cat] / z2[r["name"]][cat] for r in pool if abs(z2[r["name"]][cat]) > 0.25), 4),
                         G_over_paper_Z=round(statistics.median(g2[r["name"]][cat] / g0[r["name"]][cat] for r in pool if abs(g0[r["name"]][cat]) > 0.25), 4))
    alt = copy.deepcopy(pin); alt["games_per_week"] = 3.5
    tmp = os.path.join(HERE, "_tmp_pin.json")
    json.dump(alt, open(tmp, "w"))
    try:
        b35 = SB.build(LINES, gscore_path=tmp)
    finally:
        os.remove(tmp)
    rank = {r["name"]: r["g_rank"] for r in b["board"]}; rank35 = {r["name"]: r["g_rank"] for r in b35["board"]}
    top156 = [r["name"] for r in b["board"][:156]]
    rec = dict(lines=os.path.relpath(LINES, KIT), pin=os.path.relpath(SB.GSCORE, KIT), board_rows=len(b["board"]),
               order_unchanged=[r["name"] for r in b["board"]] == [r["name"] for r in SB.build(LINES, gscore_path=None)["board"]],
               agreement=[compare(b, 156), compare(b, 180)], effective_weight=weights, percentage_definition=defn,
               g_3_5=dict(spearman_with_3_0065=round(spearman({n: rank[n] for n in top156}, {n: rank35[n] for n in top156}), 4),
                          max_rank_change=max(abs(rank[n] - rank35[n]) for n in top156)))
    with open(os.path.join(HERE, "compare.json"), "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False); f.write("\n")
    print(json.dumps(rec, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
