#!/usr/bin/env python3
"""Six-way blend (owner 2026-10-14, council 4–1): write blend_lines.py's lines to BOTH planes in one pass, with assertions.
Modelled on report/dial/tools/dial_apply.py (same CSV handling); kit minutes and games left alone.

  blend_apply.py <lines.json> --deck <data/players.csv> --kit <report/projections-2026-27.csv> [--out-dir DIR] [--record PATH]

  deck  fg_pct fga ft_pct fta tpm pts reb ast stl blk tov  <- the blended line; the note gains one dated "six-way blend"
        entry (replaced in place on a re-run)
  kit   fgp fga ftp fta tpm pts reb ast stl blk tov       <- the same values; name, team, pos, gp, mpg untouched
Assertions (any failure exits 1 and writes nothing):
  A1 headers and row counts unchanged on both planes; no row added, dropped or reordered
  A2 every non-stat column unchanged (deck: player/team/pos and the note before the blend entry; kit: name/team/pos/gp/mpg)
  A3 every listed row written on every plane that carries it; every other row byte-identical
  A4 the two planes carry the same eleven values on every listed shared row
  A5 points identity |pts - (2*FGA*FG% + 3PM + FTA*FT%)| <= 0.25 on every listed row
  A6 sanity: percentages in (0, 1); counts >= 0; FGA <= 30; points <= 40
  A7 no deck note carries "];" (the build's PLAYERS regex trap, D-1006-3)
  A8 verified at the source: every one of the nine categories equals the equal-weight mean of the line before the blend
     and the outside projections, recomputed here from the pinned files (not taken from the lines file); and the three
     outside values the deck's own range_check.references loads (Yahoo, Hashtag, RotoBaller) agree with this loader's
  A9 the values that changed are the nine categories plus FGA and FTA, nothing else
A second run on its own output changes nothing (the "before" for A8 is read from the lines file's old line, which A8b
checks against the plane on a first run)."""
import argparse, csv, io, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CATS, STAT, KITCOL, MIN_REFS, KIT, canon, references, fmt, blend_cell, range_check  # noqa: E402
ENTRY = re.compile(r"(; |\. )?10/14: six-way blend \(.*$")
CHECK_RC = {"Yahoo": "Yahoo", "Hashtag": "Hashtag", "RotoBaller": "RotoBaller"}


def read(path):
    raw = open(path, encoding="utf-8", newline="").read()
    return raw, raw.splitlines()[0].split(","), list(csv.DictReader(io.StringIO(raw)))


def write(rows, header, eol):
    buf = io.StringIO(); w = csv.DictWriter(buf, fieldnames=header, lineterminator=eol); w.writeheader(); w.writerows(rows)
    return buf.getvalue()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("lines"); ap.add_argument("--deck", required=True)
    ap.add_argument("--kit", required=True); ap.add_argument("--out-dir"); ap.add_argument("--record"); a = ap.parse_args()
    L = {r["key"]: r for r in json.load(open(a.lines, encoding="utf-8"))["rows"]}
    draw, dhead, deck = read(a.deck); kraw, khead, kit = read(a.kit)
    d0 = [dict(r) for r in deck]; k0 = [dict(r) for r in kit]
    rec, fails = [], []
    for r in deck:
        x = L.get(canon(r["player"]))
        if not x: continue
        before = {c: r[c] for c in STAT}
        for c in STAT: r[c] = fmt(c, x["new"][c])
        base = ENTRY.sub("", r["note"])
        sep = ". " if base.rstrip().endswith("]") else "; "
        r["note"] = (base + sep if base else "") + x["note"]
        rec.append(dict(plane="deck", player=r["player"], key=x["key"], before=before, after={c: r[c] for c in STAT},
                        changed=sorted(c for c in STAT if before[c] != r[c])))
    for r in kit:
        x = L.get(canon(r["name"]))
        if not x: continue
        before = {c: r[KITCOL.get(c, c)] for c in STAT}
        for c in STAT: r[KITCOL.get(c, c)] = fmt(c, x["new"][c])
        after = {c: r[KITCOL.get(c, c)] for c in STAT}
        rec.append(dict(plane="kit", player=r["name"], key=x["key"], before=before, after=after,
                        changed=sorted(c for c in STAT if before[c] != after[c])))
    # A1
    if dhead != draw.splitlines()[0].split(",") or khead != kraw.splitlines()[0].split(","): fails.append("A1 header")
    if len(deck) != len(d0) or len(kit) != len(k0): fails.append("A1 row count changed")
    # A2 / A3
    for r, r0 in zip(deck, d0):
        if (r["player"], r["team"], r["pos"]) != (r0["player"], r0["team"], r0["pos"]): fails.append(f"A2 deck identity {r0['player']}")
        if not r["note"].startswith(ENTRY.sub("", r0["note"])): fails.append(f"A2 deck note prefix {r0['player']}")
        if canon(r["player"]) not in L and r != r0: fails.append(f"A3 deck row without a line changed: {r0['player']}")
    for r, r0 in zip(kit, k0):
        if (r["name"], r["team"], r["pos"], r["gp"], r["mpg"]) != (r0["name"], r0["team"], r0["pos"], r0["gp"], r0["mpg"]): fails.append(f"A2 kit identity {r0['name']}")
        if canon(r["name"]) not in L and r != r0: fails.append(f"A3 kit row without a line changed: {r0['name']}")
    wrote = {(x["plane"], x["key"]) for x in rec}
    for k, x in L.items():
        if ("kit", k) not in wrote: fails.append(f"A3 kit row not written: {x['name']}")
        if x["on_deck"] and ("deck", k) not in wrote: fails.append(f"A3 deck row not written: {x['name']}")
    # A4
    kd = {canon(r["name"]): r for r in kit}
    for r in deck:
        k = canon(r["player"])
        if k in L:
            for c in STAT:
                if r[c] != kd[k][KITCOL.get(c, c)]: fails.append(f"A4 planes differ {r['player']} {c}")
    # A7
    for r in deck:
        if "];" in r["note"]: fails.append(f"A7 note carries '];': {r['player']}")
    refs = references()
    rc_refs, _ = range_check.references(KIT, None)
    byk = {(x["plane"], x["key"]): x for x in rec}
    for r in kit:
        k = canon(r["name"]); x = L.get(k)
        if not x: continue
        v = {c: float(r[KITCOL.get(c, c)]) for c in STAT}; b = {c: float(byk[("kit", k)]["before"][c]) for c in STAT}
        old = {c: float(x["old"][c]) for c in STAT}
        # A8b: on a first run the plane's line before the write is the lines file's old line
        if any(abs(b[c] - old[c]) > 1e-9 for c in STAT) and any(abs(b[c] - v[c]) > 1e-9 for c in STAT):
            fails.append(f"A8 {r['name']}: the plane's line before the write is not the lines file's old line")
        # A5
        resid = v["pts"] - (2 * v["fga"] * v["fg_pct"] + v["tpm"] + v["fta"] * v["ft_pct"])
        if abs(resid) > 0.25: fails.append(f"A5 identity {r['name']} residual {resid:.3f}")
        # A6
        if not (0 < v["fg_pct"] < 1 and 0 < v["ft_pct"] < 1): fails.append(f"A6 pct {r['name']}")
        if min(v.values()) < 0 or v["fga"] > 30 or v["pts"] > 40: fails.append(f"A6 range {r['name']}")
        # A8: recomputed from the pinned files
        ref = refs.get(k, {})
        if len(ref) < MIN_REFS: fails.append(f"A8 {r['name']} has {len(ref)} references"); continue
        for c in CATS:
            want = blend_cell(old[c], ref, c)
            if abs(v[c] - want) > 1e-9: fails.append(f"A8 {r['name']} {c} {v[c]} != six-way mean {want}")
        for s, rs in CHECK_RC.items():
            if s in ref and rs in rc_refs.get(k, {}):
                for c in CATS:
                    if abs(ref[s][c] - rc_refs[k][rs][c]) > 1e-6: fails.append(f"A8b {r['name']} {s} {c}: loaders disagree")
        # A9
        got = {c for c in STAT if abs(v[c] - old[c]) > 1e-9}
        if not got <= set(CATS) | {"fga", "fta"}: fails.append(f"A9 {r['name']} changed {sorted(got)}")
    if fails:
        print("BLEND APPLY: FAIL"); [print("  " + f) for f in fails[:40]]; sys.exit(1)
    eol = lambda raw: "\r\n" if "\r\n" in raw else "\n"
    dout, kout = write(deck, dhead, eol(draw)), write(kit, khead, eol(kraw))
    od = a.out_dir
    dp = os.path.join(od, "players.csv") if od else a.deck; kp = os.path.join(od, "projections-2026-27.csv") if od else a.kit
    if od: os.makedirs(od, exist_ok=True)
    open(dp, "w", encoding="utf-8", newline="").write(dout); open(kp, "w", encoding="utf-8", newline="").write(kout)
    nd = sum(1 for x in rec if x["plane"] == "deck" and x["changed"]); nk = sum(1 for x in rec if x["plane"] == "kit" and x["changed"])
    vals = sum(len(x["changed"]) for x in rec)
    if a.record:
        json.dump(dict(script="blend_apply.py", lines=os.path.basename(a.lines), deck_rows_changed=nd, kit_rows_changed=nk,
                       values_changed=vals, rows=rec), open(a.record, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"BLEND APPLY: PASS — deck {nd} rows changed, kit {nk} rows changed, {vals} values changed; files "
          f"{'changed' if (dout != draw or kout != kraw) else 'unchanged'} (deck {dout != draw}, kit {kout != kraw})")


if __name__ == "__main__":
    main()
