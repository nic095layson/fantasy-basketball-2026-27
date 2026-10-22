#!/usr/bin/env python3
"""The in-season board (in-season tool; Council 2026-10-19 decisions 8 and 10): report/rank_engine.py's own
functions (load, exclude_held, zscores, total, avail) run on data/season/projections_season.csv, written to
report/season/board_<date>.md and .json. The preseason board (report/top-200-2026-27.md) is never rewritten; on
an identity season file this board's order equals it.

G-score comparison column (D-ZS-2, owner 2026-10-21): when data/season/gscore_tau.json exists, each row also carries
Rosenof's G-score (arXiv 2307.02188v5, data/source/papers/, Table 5) on the same projections and pool as the z:
counting G = (x - mu) / sqrt(sigma^2 + kappa * (tau / g)^2), TOV negated; FG%/FT% G = (a / mu_A)(r - mu_R) /
sqrt(sigma_R^2 + kappa * tau_R^2). tau, tau_R, kappa and g (games per counted week, which puts a weekly tau on the
per-game scale) come from the pinned file, written from the 2025-26 game logs by
report/after-reports/zscore-assessment-2026-10-21/gamelogs/gscore_weights.py --pin. The G total takes the same
availability factor as z. The board stays ranked by z; G is shown beside it, never used to order it. No file, no column.

    python3 scripts/season_board.py --date 2026-10-21 [--lines data/season/projections_season.csv] [--out report/season]
"""
import argparse
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(KIT, "report"))
import rank_engine as RE  # noqa: E402

LINES = os.path.join(KIT, "data", "season", "projections_season.csv")
OUT = os.path.join(KIT, "report", "season")
GSCORE = os.path.join(KIT, "data", "season", "gscore_tau.json")
LABEL = {"fgp": "FG%", "ftp": "FT%", "tpm": "3PM", "pts": "PTS", "reb": "REB", "ast": "AST", "stl": "STL", "blk": "BLK", "tov": "TOV"}


def load_pin(path):
    """The pinned G-score inputs, or None when the file is absent. A file missing a category is refused."""
    if not path or not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        pin = json.load(f)
    missing = [k for k in RE.COUNTING + ["tov"] if k not in pin.get("tau", {})] + \
        [k for k in ("fgp", "ftp") if k not in pin.get("tau_r", {})] + [k for k in ("kappa", "games_per_week") if k not in pin]
    if missing:
        raise ValueError(f"{os.path.relpath(path, KIT)} lacks {', '.join(missing)}")
    return pin


def gscores(rows, pool, pin):
    """{name: {cat: G}} by Table 5 of arXiv 2307.02188v5 over the pool (population SDs, as rank_engine.zscores)."""
    k, g = pin["kappa"], pin["games_per_week"]

    def mean_sd(vals):
        m = sum(vals) / len(vals)
        return m, math.sqrt(sum((v - m) ** 2 for v in vals) / len(vals))

    out = {r["name"]: {} for r in rows}
    for cat in RE.COUNTING + ["tov"]:
        m, sd = mean_sd([r[cat] for r in pool])
        den = math.sqrt(sd ** 2 + k * (pin["tau"][cat] / g) ** 2) or 1.0
        sign = -1.0 if cat == "tov" else 1.0
        for r in rows:
            out[r["name"]][cat] = sign * (r[cat] - m) / den
    for cat, att in (("fgp", "fga"), ("ftp", "fta")):
        mu_a = sum(r[att] for r in pool) / len(pool)
        mu_r = sum(r[cat] * r[att] for r in pool) / max(sum(r[att] for r in pool), 1e-9)
        _, sd_r = mean_sd([r[cat] for r in pool])
        den = math.sqrt(sd_r ** 2 + k * pin["tau_r"][cat] ** 2) or 1.0
        for r in rows:
            out[r["name"]][cat] = (r[att] / mu_a) * (r[cat] - mu_r) / den
    return out


def build(path, gscore_path=GSCORE):
    rows = RE.load(path)
    rows, held = RE.exclude_held(rows)
    z1 = RE.zscores(rows, rows)
    pool = sorted(rows, key=lambda r: -RE.total(z1[r["name"]]))[:RE.POOL_SIZE]
    z2 = RE.zscores(rows, pool)
    pin = load_pin(gscore_path)
    g2 = gscores(rows, pool, pin) if pin else None
    for r in rows:
        z = z2[r["name"]]
        r["z_total"] = RE.total(z)
        r["z_adj"] = r["z_total"] * RE.avail(r["gp"]) if r["z_total"] > 0 else r["z_total"]
        r["z"] = {LABEL[k]: round(z[k], 3) for k in LABEL if k in z}
        if g2:
            g = g2[r["name"]]
            r["g_total"] = sum(g.values())
            r["g_adj"] = r["g_total"] * RE.avail(r["gp"]) if r["g_total"] > 0 else r["g_total"]
            r["g"] = {LABEL[k]: round(g[k], 3) for k in LABEL if k in g}
    board = sorted(rows, key=lambda r: -r["z_adj"])
    if g2:
        for i, r in enumerate(sorted(rows, key=lambda r: -r["g_adj"]), 1):
            r["g_rank"] = i
    gmeta = dict(file=os.path.relpath(gscore_path, KIT), **pin) if pin else None
    return dict(board=board, n_held=len(held), held=sorted(r["name"] for r in held), n_rows=len(rows) + len(held), gscore=gmeta)


def render(b, date, lines_rel, movers):
    L = [f"# In-season board — {date}", "",
         f"*Built by `scripts/season_board.py` from `{lines_rel}` (the preseason line blended with the season's actuals by "
         f"`season_lines.py`), with `report/rank_engine.py`'s functions: per-game z-scores over an iterated top-{RE.POOL_SIZE} "
         f"pool, FG%/FT% impact-weighted, TOV negative, availability-adjusted (GP/82 + (1−GP/82)×{RE.STREAM_R}); "
         f"{b['n_held']} rows held off the board at the exclusion class. The preseason board `report/top-200-2026-27.md` is unchanged.*", ""]
    if movers:
        L += ["**Lines that moved this run** (preseason → season, by the blend; see the dated `season_lines_*.json`):", ""]
        L += [f"- {m['name']} ({m['games']} games): " + ", ".join(f"{LABEL.get(c, c)} {x} → {y}" for c, (x, y) in m["moved"].items()) for m in movers[:40]]
        L.append("")
    gs = b.get("gscore")
    if gs:
        L += [f"*G column (comparison only; the board is ranked by z): Rosenof's G-score, arXiv 2307.02188v5 Table 5, on the "
              f"same lines and pool as the z, with week-to-week variance from `{gs['file']}` (κ {gs['kappa']:.3f}, "
              f"{gs['games_per_week']} games per counted week), availability-adjusted like z. G # is the rank G alone would give.*", ""]
    head = "| # | player | team | pos | GP | value (adj) | z total |" + (" G (adj) | G # |" if gs else "") + " FG% | FT% | 3PM | PTS | REB | AST | STL | BLK | TOV |"
    L += [head, "|" + "---|" * (head.count("|") - 1)]
    for i, r in enumerate(b["board"][:200], 1):
        L.append(f"| {i} | {r['name']} | {r['team']} | {r['pos']} | {int(r['gp'])} | {r['z_adj']:.2f} | {r['z_total']:.2f} | "
                 + (f"{r['g_adj']:.2f} | {r['g_rank']} | " if gs else "")
                 + " | ".join(f"{r['z'].get(c, 0):+.2f}" for c in ("FG%", "FT%", "3PM", "PTS", "REB", "AST", "STL", "BLK", "TOV")) + " |")
    return "\n".join(L) + "\n"


def write(lines_path, date, out_dir, movers, gscore_path=GSCORE):
    b = build(lines_path, gscore_path)
    os.makedirs(out_dir, exist_ok=True)
    md = os.path.join(out_dir, f"board_{date}.md"); js = os.path.join(out_dir, f"board_{date}.json")
    with open(md, "w", encoding="utf-8") as f:
        f.write(render(b, date, os.path.relpath(lines_path, KIT), movers))
    rows = []
    for i, r in enumerate(b["board"], 1):
        row = dict(rank=i, name=r["name"], team=r["team"], pos=r["pos"], gp=r["gp"], z_adj=round(r["z_adj"], 4),
                   z_total=round(r["z_total"], 4), z=r["z"])
        if b["gscore"]:
            row.update(g_adj=round(r["g_adj"], 4), g_total=round(r["g_total"], 4), g_rank=r["g_rank"], g=r["g"])
        rows.append(row)
    rec = dict(date=date, lines=os.path.relpath(lines_path, KIT), n_rows=b["n_rows"], held=b["held"])
    if b["gscore"]:
        rec["gscore"] = b["gscore"]
    rec["board"] = rows
    with open(js, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False)
        f.write("\n")
    return md, js


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", required=True); ap.add_argument("--lines", default=LINES); ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    movers = []
    rec = os.path.join(os.path.dirname(a.lines), f"season_lines_{a.date}.json")
    if os.path.exists(rec):
        with open(rec, encoding="utf-8") as f:
            movers = json.load(f).get("movers", [])
    md, js = write(a.lines, a.date, a.out, movers)
    print(f"SEASON BOARD: PASS — {a.date}: {os.path.relpath(md, KIT)} ({len(movers)} movers listed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
