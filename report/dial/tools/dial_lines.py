#!/usr/bin/env python3
"""Dial pass 2026-10-13 (D-1013-6, council 4–1): the clamped lines, computed, nothing written to either plane.

Selection (A7): every top-150 line whose cells outside the range of the three outside projections carry more than 0.5 z
net, either way, in the deck's own range-check frame on Version 64 (report/after-reports/usage-2026-10-13/
range_check_no_actual.json: the deck's scripts/range_check.py at f6fb476 with no last-season reference), plus
Philadelphia's other three (LeBron James, Joel Embiid, VJ Edgecombe) for the team budget.
Reference (A6): per category, [min, max] of Yahoo 10/13, Hashtag 10/12 and RotoBaller 9/29 as the deck's range check
loads them (range_check.references, newest file per outlet, RotoBaller percentages /100).
Target (A8): every cell of a selected line outside [min, max] moves to the nearest edge, rounded inward (one decimal on
counts, three on percentages) so the written value never leaves the range; cells inside stay; games, minutes, positions,
teams and tags are untouched.
Identity (A9): when points, threes, FG% or FT% moved, FGA and FTA scale by one common factor (their ratio kept) so that
points = 2*FG%*FGA + 3PM + FT%*FTA; when none of the four moved, FGA and FTA stay as they are.

  dial_lines.py --deck <data/players.csv> --kit <report/projections-2026-27.csv> --out <lines.json>"""
import argparse, csv, json, math, os, re, sys, unicodedata
KIT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
DECK = os.environ.get("DECK_REPO", "/home/user/yahoo-fantasy-basketball")
sys.path.insert(0, os.path.join(DECK, "scripts"))
import range_check  # noqa: E402  (the deck's own loader and name fold)
CATS = range_check.CATS                      # pts reb ast stl blk tpm tov fg_pct ft_pct
STAT = ["fg_pct", "fga", "ft_pct", "fta", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"]
KITCOL = {"fg_pct": "fgp", "ft_pct": "ftp"}
SEL_JSON = os.path.join(KIT, "report/after-reports/usage-2026-10-13/range_check_no_actual.json")
PHI = ["LeBron James", "Joel Embiid", "VJ Edgecombe"]
THRESH = 0.5
LABEL = {"pts": "pts", "reb": "reb", "ast": "ast", "stl": "stl", "blk": "blk", "tpm": "3PM", "tov": "TO", "fg_pct": "FG%", "ft_pct": "FT%"}


def inward(c, v, toward_hi):
    """Round v to the written precision without leaving the range: down when clamping to the max, up when to the min."""
    q = 1000 if c.endswith("pct") else 10
    return (math.floor(v * q + 1e-9) if toward_hi else math.ceil(v * q - 1e-9)) / q


def fmt(c, v):
    return f"{v:.3f}".lstrip("0") if c.endswith("pct") else f"{v:g}"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--deck", required=True); ap.add_argument("--kit", required=True)
    ap.add_argument("--out", required=True); a = ap.parse_args()
    rec = json.load(open(SEL_JSON, encoding="utf-8"))
    chosen = [(r["player"], r["net_z"]) for r in rec["rows"] if abs(r["net_z"]) > THRESH] + [(n, None) for n in PHI]
    refs, used = range_check.references(KIT, None)
    deck = {range_check.fold(r["player"]): r for r in csv.DictReader(open(a.deck, encoding="utf-8"))}
    kit = {range_check.fold(r["name"]): r for r in csv.DictReader(open(a.kit, encoding="utf-8"))}
    rows, problems = [], []
    for name, nz in chosen:
        k = range_check.fold(name); d = deck.get(k); kr = kit.get(k); ref = refs.get(k, {})
        if d is None or kr is None: problems.append(f"{name}: not on both planes"); continue
        if len(ref) != 3: problems.append(f"{name}: {len(ref)} references, need 3"); continue
        before = {c: float(d[c]) for c in STAT}
        twin = {c: float(kr[KITCOL.get(c, c)]) for c in STAT}
        if any(abs(before[c] - twin[c]) > 1e-9 for c in STAT): problems.append(f"{name}: planes differ before the pass"); continue
        new = dict(before); cells = []
        for c in CATS:
            vals = [ref[s][c] for s in sorted(ref)]; lo, hi = min(vals), max(vals); v = before[c]
            # 1e-9: RotoBaller's percentages arrive as x/100 and carry float noise (88.6/100 = 0.88599...)
            if v > hi + 1e-9: nv = inward(c, hi, True); side = "down"
            elif v < lo - 1e-9: nv = inward(c, lo, False); side = "up"
            else: continue
            if not (lo - 1e-9 <= nv <= hi + 1e-9): problems.append(f"{name} {c}: rounded edge {nv} left [{lo}, {hi}]")
            if abs(nv - v) < 1e-9: continue   # the edge rounds back onto the value already written
            new[c] = nv
            cells.append(dict(cat=c, before=v, lo=lo, hi=hi, after=nv, side=side,
                              sources={s: ref[s][c] for s in sorted(ref)}))
        shot = any(new[c] != before[c] for c in ("pts", "tpm", "fg_pct", "ft_pct"))
        factor = 1.0
        if shot:
            denom = 2 * new["fg_pct"] * before["fga"] + new["ft_pct"] * before["fta"]
            factor = (new["pts"] - new["tpm"]) / denom
            new["fga"] = round(before["fga"] * factor, 1); new["fta"] = round(before["fta"] * factor, 1)
        resid = lambda x: x["pts"] - (2 * x["fg_pct"] * x["fga"] + x["tpm"] + x["ft_pct"] * x["fta"])
        if shot and abs(resid(new)) > 0.25: problems.append(f"{name}: identity residual {resid(new):.3f} after the rescale")
        if new["fga"] > 30 or min(new.values()) < 0: problems.append(f"{name}: sanity {new}")
        moved = "; ".join(f"{LABEL[x['cat']]} {fmt(x['cat'], x['before'])} to {fmt(x['cat'], x['after'])}" for x in cells)
        note = (f"10/13: range clamp (D-1013-6, council 4-1) - {moved}"
                + (f"; FGA {before['fga']:g} to {new['fga']:g}, FTA {before['fta']:g} to {new['fta']:g} for the points identity" if shot else "")
                + " (inside Yahoo 10/13, Hashtag 10/12 and RotoBaller 9/29)")
        rows.append(dict(key=k, name=name, team=d["team"], net_z=nz, why="net z beyond the range over 0.5" if nz is not None else "Philadelphia's team budget",
                         before=before, new=new, cells=cells, shots_rescaled=shot, factor=round(factor, 4),
                         resid_before=round(resid(before), 3), resid_after=round(resid(new), 3), note=note, on_deck=True, on_kit=True))
    out = dict(script="dial_lines.py", selection=os.path.relpath(SEL_JSON, KIT), threshold=THRESH, references=used,
               rows=rows, problems=problems, n_rows=len(rows), n_cells=sum(len(r["cells"]) for r in rows),
               n_shots_rescaled=sum(r["shots_rescaled"] for r in rows))
    json.dump(out, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"DIAL LINES: {len(rows)} rows, {out['n_cells']} cells clamped, {out['n_shots_rescaled']} shot rescales; problems {len(problems)}")
    for p in problems: print("  PROBLEM", p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
