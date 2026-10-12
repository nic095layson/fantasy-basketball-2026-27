#!/usr/bin/env python3
"""WO-5 P6: write every re-derived line to BOTH planes in one pass, with assertions.

  wo5_apply.py <lines.json> --deck <data/players.csv> --kit <report/projections-2026-27.csv>
               [--out-dir DIR] [--record PATH] [--date 10/12]

<lines.json> is wo5_lines.py's output. For every row that has a method line ("new"):
  deck  fg_pct fga ft_pct fta tpm pts reb ast stl blk tov  <- the line; the note gains one dated entry
        ("<date>: WO-5 line — <base> base at <M> min[, <role>] (<outlets>)"), replaced in place on a re-run
  kit   fgp fga ftp fta tpm pts reb ast stl blk tov       <- the same values; mpg <- the line's minutes
Everything else on both files (names, teams, positions, games, tags, row order, headers) is left alone.
Without --out-dir the two files are rewritten in place; with it, copies are written there.

Assertions (any failure exits 1 and writes nothing):
  A1 headers and row counts unchanged on both planes; no row added, dropped or reordered
  A2 every non-stat column unchanged (deck: player/team/pos and the note up to the WO-5 entry;
     kit: name/team/pos/gp)
  A3 every row with a method line was written on every plane it sits on; every row without one is
     byte-identical
  A4 the two planes carry the same eleven values on every shared row with a method line
  A5 points identity: |pts - (2*FGA*FG% + 3PM + FTA*FT%)| <= 0.25 on every written row (rounding only)
  A6 sanity: percentages in (0, 1); counts >= 0; FGA <= 30; points <= 40; minutes in [4, 40]
  A7 no deck note carries "];" (the build's non-greedy PLAYERS match would stop there — D-1006-3)
A second run on its own output changes nothing (idempotent): the WO-5 note entry is replaced, not stacked."""
import argparse, csv, io, json, os, re, sys, unicodedata

STAT = ["fg_pct", "fga", "ft_pct", "fta", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"]
KITCOL = {"fg_pct": "fgp", "ft_pct": "ftp"}
ALIASES = {"herb jones": "herbert jones", "cam johnson": "cameron johnson", "nic claxton": "nicolas claxton",
           "alex sarr": "alexandre sarr", "ron holland": "ronald holland"}
MARK = "WO-5 line"


def norm(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[.'`,’-]", "", s); s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = " ".join(t for t in s.split() if t not in {"jr", "sr", "ii", "iii", "iv"})
    return ALIASES.get(s, s)


def fmt(c, v):
    return f"{v:.3f}" if c.endswith("pct") else f"{v:.1f}"


def read(path):
    raw = open(path, encoding="utf-8", newline="").read()
    rows = list(csv.DictReader(io.StringIO(raw)))
    header = raw.splitlines()[0].split(",")
    return raw, header, rows


def write(rows, header, eol):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=header, lineterminator=eol)
    w.writeheader(); w.writerows(rows)
    return buf.getvalue()


def note_entry(date, rec):
    m = rec["meta"]; src = rec.get("minutes_source", "")
    role = ""
    if src.startswith("override: "):
        mech = src[len("override: "):]
        role = ", " + mech.split(" -> ")[0].replace(";", ",")
    g = rec.get("range") or {}; extra = ""
    if g.get("factor", 1.0) != 1.0:
        extra += ", minutes to the outside lines' range"
    if g.get("pct"):
        extra += ", " + "/".join({"fg_pct": "FG%", "ft_pct": "FT%"}[c] for c in sorted(g["pct"])) + " to the range"
    if g.get("cnt"):
        extra += ", " + "/".join(sorted(g["cnt"])) + " to the range"
    src = "Yahoo, Hashtag, RotoBaller" if extra else "Basketball-Reference"
    if m["base"].startswith("rookie"):
        return f"{date}: {MARK} — rookie translation held{extra} ({src})"
    return f"{date}: {MARK} — {m['base']} base at {m['minutes']:.1f} min{role}{extra} ({'Basketball-Reference; ' + src if extra else src})"


def strip_entry(note):
    """The note without an earlier WO-5 entry (so a re-run replaces it)."""
    return re.sub(r"(; |\. )?\d{1,2}/\d{1,2}: " + re.escape(MARK) + r" — .*$", "", note)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("lines"); ap.add_argument("--deck", required=True)
    ap.add_argument("--kit", required=True); ap.add_argument("--out-dir"); ap.add_argument("--record")
    ap.add_argument("--date", default="10/12")
    a = ap.parse_args()
    L = {r["key"]: r for r in json.load(open(a.lines, encoding="utf-8"))["rows"] if r.get("new")}
    draw, dhead, deck = read(a.deck); kraw, khead, kit = read(a.kit)
    d0 = [dict(r) for r in deck]; k0 = [dict(r) for r in kit]
    rec = []; fails = []
    for r in deck:
        k = norm(r["player"]); x = L.get(k)
        if not x: continue
        before = {c: r[c] for c in STAT}
        for c in STAT: r[c] = fmt(c, x["new"][c])
        base = strip_entry(r["note"])
        # a note ending in "]" joins with ". ", never "; " — "];" inside the JSON ends the build's non-greedy
        # PLAYERS match early and fails the injection round-trip (the D-1006-3 trap)
        sep = ". " if base.rstrip().endswith("]") else "; "
        r["note"] = (base + sep if base else "") + note_entry(a.date, x)
        rec.append(dict(plane="deck", player=r["player"], key=k, before=before, after={c: r[c] for c in STAT},
                        changed=sorted(c for c in STAT if before[c] != r[c])))
    for r in kit:
        k = norm(r["name"]); x = L.get(k)
        if not x: continue
        before = {c: r[KITCOL.get(c, c)] for c in STAT}; before["mpg"] = r["mpg"]
        for c in STAT: r[KITCOL.get(c, c)] = fmt(c, x["new"][c])
        r["mpg"] = f"{x['meta']['minutes']:.1f}"
        after = {c: r[KITCOL.get(c, c)] for c in STAT}; after["mpg"] = r["mpg"]
        rec.append(dict(plane="kit", player=r["name"], key=k, before=before, after=after,
                        changed=sorted(c for c in after if before[c] != after[c])))
    # A1
    if len(deck) != len(d0) or len(kit) != len(k0): fails.append("A1 row count changed")
    # A2 / A3
    for r, r0 in zip(deck, d0):
        if (r["player"], r["team"], r["pos"]) != (r0["player"], r0["team"], r0["pos"]): fails.append(f"A2 deck identity {r0['player']}")
        if not r["note"].startswith(strip_entry(r0["note"])): fails.append(f"A2 deck note prefix {r0['player']}")
        if norm(r["player"]) not in L and r != r0: fails.append(f"A3 deck row without a line changed: {r0['player']}")
    for r, r0 in zip(kit, k0):
        if (r["name"], r["team"], r["pos"], r["gp"]) != (r0["name"], r0["team"], r0["pos"], r0["gp"]): fails.append(f"A2 kit identity {r0['name']}")
        if norm(r["name"]) not in L and r != r0: fails.append(f"A3 kit row without a line changed: {r0['name']}")
    wrote = {(x["plane"], x["key"]) for x in rec}
    for k, x in L.items():
        if x.get("on_deck") and ("deck", k) not in wrote: fails.append(f"A3 deck row not written: {x['name']}")
        if x.get("on_kit") and ("kit", k) not in wrote: fails.append(f"A3 kit row not written: {x['name']}")
    # A4
    kd = {norm(r["name"]): r for r in kit}
    for r in deck:
        k = norm(r["player"])
        if k in L and k in kd:
            for c in STAT:
                if r[c] != kd[k][KITCOL.get(c, c)]: fails.append(f"A4 planes differ {r['player']} {c} {r[c]} vs {kd[k][KITCOL.get(c, c)]}")
    # A7: no note may carry "];" (the build's PLAYERS regex trap, D-1006-3)
    for r in deck:
        if "];" in r["note"]: fails.append(f"A7 note carries '];': {r['player']}")
    # A5 / A6
    for r in deck:
        if norm(r["player"]) not in L: continue
        v = {c: float(r[c]) for c in STAT}
        imp = 2 * v["fga"] * v["fg_pct"] + v["tpm"] + v["fta"] * v["ft_pct"]
        if abs(v["pts"] - imp) > 0.25: fails.append(f"A5 identity {r['player']} {v['pts']} vs {imp:.2f}")
        if not (0 < v["fg_pct"] < 1 and 0 <= v["ft_pct"] < 1): fails.append(f"A6 pct {r['player']}")
        if min(v[c] for c in STAT) < 0 or v["fga"] > 30 or v["pts"] > 40: fails.append(f"A6 range {r['player']}")
    for r in kit:
        if norm(r["name"]) in L and not (4 <= float(r["mpg"]) <= 40): fails.append(f"A6 minutes {r['name']} {r['mpg']}")
    if fails:
        print("WO-5 APPLY: FAIL"); [print("  " + f) for f in fails[:40]]; sys.exit(1)
    eol = lambda raw: "\r\n" if "\r\n" in raw else "\n"
    dout, kout = write(deck, dhead, eol(draw)), write(kit, khead, eol(kraw))
    od = a.out_dir
    dp = os.path.join(od, "players.csv") if od else a.deck; kp = os.path.join(od, "projections-2026-27.csv") if od else a.kit
    if od: os.makedirs(od, exist_ok=True)
    dch = dout != draw; kch = kout != kraw
    open(dp, "w", encoding="utf-8", newline="").write(dout); open(kp, "w", encoding="utf-8", newline="").write(kout)
    nd = sum(1 for x in rec if x["plane"] == "deck" and x["changed"]); nk = sum(1 for x in rec if x["plane"] == "kit" and x["changed"])
    vals = sum(len(x["changed"]) for x in rec)
    if a.record:
        json.dump(dict(script="wo5_apply.py", lines=os.path.basename(a.lines), date=a.date, deck_rows_written=sum(1 for x in rec if x["plane"] == "deck"),
                       kit_rows_written=sum(1 for x in rec if x["plane"] == "kit"), deck_rows_changed=nd, kit_rows_changed=nk,
                       values_changed=vals, rows=rec), open(a.record, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"WO-5 APPLY: PASS — deck {sum(1 for x in rec if x['plane'] == 'deck')} rows written ({nd} with a changed value), "
          f"kit {sum(1 for x in rec if x['plane'] == 'kit')} rows written ({nk} changed); {vals} values changed; "
          f"files {'changed' if dch or kch else 'unchanged'} (deck {dch}, kit {kch})")


if __name__ == "__main__":
    main()
