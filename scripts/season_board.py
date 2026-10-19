#!/usr/bin/env python3
"""The in-season board (in-season tool; Council 2026-10-19 decisions 8 and 10): report/rank_engine.py's own
functions (load, exclude_held, zscores, total, avail) run on data/season/projections_season.csv, written to
report/season/board_<date>.md and .json. The preseason board (report/top-200-2026-27.md) is never rewritten; on
an identity season file this board's order equals it.

    python3 scripts/season_board.py --date 2026-10-21 [--lines data/season/projections_season.csv] [--out report/season]
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(KIT, "report"))
import rank_engine as RE  # noqa: E402

LINES = os.path.join(KIT, "data", "season", "projections_season.csv")
OUT = os.path.join(KIT, "report", "season")
LABEL = {"fgp": "FG%", "ftp": "FT%", "tpm": "3PM", "pts": "PTS", "reb": "REB", "ast": "AST", "stl": "STL", "blk": "BLK", "tov": "TOV"}


def build(path):
    rows = RE.load(path)
    rows, held = RE.exclude_held(rows)
    z1 = RE.zscores(rows, rows)
    pool = sorted(rows, key=lambda r: -RE.total(z1[r["name"]]))[:RE.POOL_SIZE]
    z2 = RE.zscores(rows, pool)
    for r in rows:
        z = z2[r["name"]]
        r["z_total"] = RE.total(z)
        r["z_adj"] = r["z_total"] * RE.avail(r["gp"]) if r["z_total"] > 0 else r["z_total"]
        r["z"] = {LABEL[k]: round(z[k], 3) for k in LABEL if k in z}
    board = sorted(rows, key=lambda r: -r["z_adj"])
    return dict(board=board, n_held=len(held), held=sorted(r["name"] for r in held), n_rows=len(rows) + len(held))


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
    L += ["| # | player | team | pos | GP | value (adj) | z total | FG% | FT% | 3PM | PTS | REB | AST | STL | BLK | TOV |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(b["board"][:200], 1):
        L.append(f"| {i} | {r['name']} | {r['team']} | {r['pos']} | {int(r['gp'])} | {r['z_adj']:.2f} | {r['z_total']:.2f} | "
                 + " | ".join(f"{r['z'].get(c, 0):+.2f}" for c in ("FG%", "FT%", "3PM", "PTS", "REB", "AST", "STL", "BLK", "TOV")) + " |")
    return "\n".join(L) + "\n"


def write(lines_path, date, out_dir, movers):
    b = build(lines_path)
    os.makedirs(out_dir, exist_ok=True)
    md = os.path.join(out_dir, f"board_{date}.md"); js = os.path.join(out_dir, f"board_{date}.json")
    with open(md, "w", encoding="utf-8") as f:
        f.write(render(b, date, os.path.relpath(lines_path, KIT), movers))
    with open(js, "w", encoding="utf-8") as f:
        json.dump(dict(date=date, lines=os.path.relpath(lines_path, KIT), n_rows=b["n_rows"], held=b["held"],
                       board=[dict(rank=i, name=r["name"], team=r["team"], pos=r["pos"], gp=r["gp"], z_adj=round(r["z_adj"], 4),
                                   z_total=round(r["z_total"], 4), z=r["z"]) for i, r in enumerate(b["board"], 1)]), f, indent=1, ensure_ascii=False)
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
