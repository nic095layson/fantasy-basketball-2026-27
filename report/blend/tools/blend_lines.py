#!/usr/bin/env python3
"""Six-way blend (owner 2026-10-14: "tighten up and dial in all the numbers"; council 4–1): the blended lines, computed,
nothing written to either plane.

A1 weights: each of the nine categories becomes the equal-weight mean of our line and every outside projection on file
   (Yahoo 10/13, Hashtag 10/12, RotoBaller 10/13, FantasyPros 10/13, BBM cards 10/13): ours counts one of up to six.
A2 only the nine per-game categories blend; games, minutes, positions, teams and tags are untouched.
A3 FGA and FTA scale by one common factor so points = 2*FG%*FGA + 3PM + FT%*FTA. Rows whose factor falls outside
   [0.85, 1.15] are listed, not held: the first run held them and that left exactly the widest disagreements (Maluach
   3.0 points against 5.0-10.4 outside) half-blended (rebounds and blocks moved, points did not); minutes feed neither
   engine, so a larger shot factor is consistent with how the line is valued. Sanity bounds stay with the writer (A6).
A4 universe: every kit row with three or more outside projections (the deck twin follows on the shared rows).

  blend_lines.py --deck <data/players.csv> --kit <report/projections-2026-27.csv> --out <lines.json>"""
import argparse, csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CATS, STAT, KITCOL, MIN_REFS, SOURCES, canon, references, fmt, blend_cell  # noqa: E402
SHOOT = ["fg_pct", "fga", "ft_pct", "fta", "tpm", "pts"]
LO, HI = 0.85, 1.15


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--deck", required=True); ap.add_argument("--kit", required=True)
    ap.add_argument("--out", required=True); a = ap.parse_args()
    refs = references()
    kit = list(csv.DictReader(open(a.kit, encoding="utf-8")))
    deck = {canon(r["player"]): r for r in csv.DictReader(open(a.deck, encoding="utf-8"))}
    rows, held, problems = [], [], []
    for r in kit:
        k = canon(r["name"]); ref = refs.get(k, {})
        if len(ref) < MIN_REFS: continue
        ours = {c: float(r[KITCOL.get(c, c)]) for c in STAT}
        d = deck.get(k)
        if d and any(abs(float(d[c]) - ours[c]) > 1e-9 for c in STAT):
            problems.append(f"{r['name']}: the deck twin differs from the kit line before the blend")
        new = dict(ours)
        for c in CATS: new[c] = blend_cell(ours[c], ref, c)
        denom = 2 * ours["fga"] * new["fg_pct"] + ours["fta"] * new["ft_pct"]
        f = (new["pts"] - new["tpm"]) / denom if denom else 1.0
        rescaled = True
        if not (LO <= f <= HI): held.append(dict(name=r["name"], factor=round(f, 3)))
        new["fga"] = float(fmt("fga", ours["fga"] * f)); new["fta"] = float(fmt("fta", ours["fta"] * f))
        resid = new["pts"] - (2 * new["fga"] * new["fg_pct"] + new["tpm"] + new["fta"] * new["ft_pct"])
        if rescaled and abs(resid) > 0.25: problems.append(f"{r['name']}: identity residual {resid:.3f}")
        labels = [s for s, _, _, _ in SOURCES if s in ref]
        cells = [dict(cat=c, ours=ours[c], refs={s: ref[s][c] for s in labels}, new=new[c]) for c in CATS]
        note = (f"10/14: six-way blend (owner call 10/14, council 4–1) — each category the equal-weight mean of this line and "
                f"{len(labels)} outside projections ({', '.join(labels)}); games, minutes and tags unchanged"
)
        rows.append(dict(key=k, name=r["name"], on_deck=bool(d), n_refs=len(labels), sources=labels, old=ours, new=new,
                         cells=cells, shots_rescaled=rescaled, factor=round(f, 4), residual=round(resid, 4), note=note))
    out = dict(script="blend_lines.py", sources=[fn for _, fn, _, _ in SOURCES], min_refs=MIN_REFS, rows=rows, wide_factor=held,
               problems=problems)
    json.dump(out, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False, sort_keys=True)
    nval = sum(1 for x in rows for c in STAT if abs(x["new"][c] - x["old"][c]) > 1e-9)
    print(f"BLEND LINES: {len(rows)} rows ({sum(x['on_deck'] for x in rows)} on the deck), {nval} values change, "
          f"{len(held)} rows with a shot factor outside 0.85-1.15 (listed, not held), {len(problems)} problems")
    for p in problems[:20]: print("  PROBLEM " + p)
    for h in held: print(f"  wide factor {h['name']} {h['factor']}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
