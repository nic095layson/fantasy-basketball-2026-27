#!/usr/bin/env python3
"""Hashtag Basketball pages printed to PDF by the owner (2026-10-01): the projections page
("Fantasy Basketball Projections", Top 200, rest-of-season per-game lines with FG/FT makes and
attempts and a TOTAL z-score; positions and ADP from Yahoo) and the ADP page ("Fantasy Basketball
ADP Data": Yahoo, ESPN and Fantrax ADP with a blend, 418 rows). The PDFs were read with pdfplumber
page by page (parser output only); the page texts are the raw layer, kept verbatim as
hashtag-raw-<date>.txt and hashtag-adp-raw-<date>.txt. This script parses them deterministically:

  hashtag-<date>.csv          200 rows: rank, move (Hashtag's rank movement glyph count), player,
                              flag ("inj" when the page carries its injury glyph), adp, pos, team,
                              gp, mpg, fg_pct, fgm, fga, ft_pct, ftm, fta, tpm, pts, reb, ast,
                              stl, blk, tov, total
  hashtag-adp-<date>.csv      418 rows: player, team, per-platform pos/adp/order (yahoo, espn,
                              fantrax) and the blend; a row whose platform groups cannot be told
                              apart keeps them under unknown* columns
  unmatched-hashtag-<date>.md the join of the projection rows to the pool (build_market.norm +
                              ALIASES), the Yahoo-ADP cross-check against the kit's newest Yahoo
                              paste, and the input stamp (drift fix D4)

Transcription invariants: projection ranks contiguous 1..N; every projection line parses; blend
orders contiguous 1..M. Exit 2 on any failure. The hard gate of the other intakes (a Hashtag-only
name that looks like a spelling variant of a pool-only name — surname + first three letters) exits 3.
The board is untouched: a projection outlet is one line of evidence for D-WO1-1, never an edit.
Usage: python3 report/market/hashtag_pdf_market.py [YYYY-MM-DD] [--as-of DATE|COMMIT | --live] [--out-dir DIR]
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

TEAMS = {"ATL", "BOS", "BKN", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GS", "HOU", "IND", "LAC",
         "LAL", "MEM", "MIA", "MIL", "MIN", "NO", "NY", "OKC", "ORL", "PHI", "PHO", "POR", "SA",
         "SAC", "TOR", "UTA", "WAS", "FA"}
ORDER = ["PG", "SG", "SF", "PF", "C"]
PROJ_RE = re.compile(
    r"^(\d+) (?:[] (\d+) )?(.+?)\s+(\d+\.\d)?\s*([A-Z,]+) ([A-Z]{2,3}) (\d+) (\d+\.\d) "
    r"(0\.\d{3}|1\.000) \(([\d.]+)/([\d.]+)\) (0\.\d{3}|1\.000) \(([\d.]+)/([\d.]+)\) ([\d.]+) ([\d.]+) "
    r"([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+) (-?[\d.]+)$")
PROJ_COLS = ["rank", "move", "player", "flag", "adp", "pos", "team", "gp", "mpg", "fg_pct", "fgm", "fga",
             "ft_pct", "ftm", "fta", "tpm", "pts", "reb", "ast", "stl", "blk", "tov", "total"]
ADP_COLS = ["player", "team", "yahoo_pos", "yahoo_adp", "yahoo_order", "espn_pos", "espn_adp", "espn_order",
            "fantrax_pos", "fantrax_adp", "fantrax_order", "blend_adp", "blend_order",
            "unknown1_pos", "unknown1_adp", "unknown1_order", "unknown2_pos", "unknown2_adp", "unknown2_order",
            "unknownA_pos", "unknownA_adp", "unknownA_order", "unknownB_pos", "unknownB_adp", "unknownB_order"]


def _clean(s):
    return "".join(c for c in s if ord(c) < 0xE000).strip()


def parse_projections(path):
    rows, problems = [], []
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not re.match(r"^\d+ ", line):
            continue
        m = PROJ_RE.match(line.strip())
        if not m:
            problems.append(f"unparsed projection line: {line[:80]!r}")
            continue
        g = m.groups()
        rows.append({"rank": int(g[0]), "move": g[1] or "", "player": _clean(g[2]),
                     "flag": "inj" if "" in g[2] else "", "adp": g[3] or "", "pos": g[4], "team": g[5],
                     "gp": int(g[6]), "mpg": g[7], "fg_pct": g[8], "fgm": g[9], "fga": g[10], "ft_pct": g[11],
                     "ftm": g[12], "fta": g[13], "tpm": g[14], "pts": g[15], "reb": g[16], "ast": g[17],
                     "stl": g[18], "blk": g[19], "tov": g[20], "total": g[21]})
    ranks = [r["rank"] for r in rows]
    if ranks != list(range(1, len(ranks) + 1)):
        problems.append(f"projection ranks not contiguous 1..{len(ranks)}")
    return rows, problems


def parse_adp(path, yahoo_adp):
    """yahoo_adp: {norm(name): adp float} from the kit's newest Yahoo paste, to label a row's
    Yahoo group when the page shows fewer than three platform groups."""
    rows, problems, ambiguous = [], [], []
    for line in open(path, encoding="utf-8"):
        toks = line.strip().split()
        if len(toks) < 4:
            continue
        ti = next((i for i, t in enumerate(toks) if t in TEAMS and i > 0), None)
        if ti is None:
            continue
        rest = toks[ti + 1:]
        if len(rest) < 2 or not re.fullmatch(r"-?\d+(\.\d+)?", rest[-1]) or not re.fullmatch(r"-?\d+(\.\d+)?", rest[-2]):
            continue
        name = _clean(" ".join(toks[:ti]))
        try:
            blend_adp, blend_order = float(rest[-2]), int(rest[-1])
        except ValueError:
            problems.append(f"blend cell unreadable: {line[:80]!r}")
            continue
        body, groups, cur, i = rest[:-2], [], None, 0
        ok = True
        while i < len(body):
            t = body[i]
            if t in ORDER:
                if cur is None or (cur["pos"] and ORDER.index(t) <= ORDER.index(cur["pos"][-1])):
                    cur = {"pos": [], "adp": None, "order": None}
                    groups.append(cur)
                cur["pos"].append(t)
                i += 1
            else:
                if cur is None:
                    cur = {"pos": [], "adp": None, "order": None}
                    groups.append(cur)
                try:
                    cur["adp"], cur["order"] = float(t), int(body[i + 1])
                except (ValueError, IndexError):
                    ok = False
                    break
                i += 2
                cur = None
        if not ok:
            problems.append(f"platform cells unreadable: {line[:80]!r}")
            continue
        rec = {"player": name, "team": toks[ti], "blend_adp": blend_adp, "blend_order": blend_order}
        plats = ["yahoo", "espn", "fantrax"]
        if len(groups) == 3:
            assign = dict(zip(plats, groups))
        else:
            yadp = yahoo_adp.get(BM.norm(name))
            cand = [g for g in groups if yadp is not None and g["adp"] is not None and abs(g["adp"] - yadp) <= 0.3]
            assign = {}
            if len(groups) == 1:
                assign["yahoo" if cand else "unknown1"] = groups[0]
            elif len(groups) == 2:
                if cand:
                    assign["yahoo"] = cand[0]
                    assign["unknown2"] = [g for g in groups if g is not cand[0]][0]
                else:
                    assign["unknownA"], assign["unknownB"] = groups
            ambiguous.append((name, len(groups), bool(cand)))
        for p, g in assign.items():
            rec[p + "_pos"] = ",".join(g["pos"])
            rec[p + "_adp"] = g["adp"] if g["adp"] is not None else ""
            rec[p + "_order"] = g["order"] if g["order"] is not None else ""
        rows.append(rec)
    orders = sorted(r["blend_order"] for r in rows)
    if orders != list(range(1, len(orders) + 1)):
        problems.append(f"blend orders not contiguous 1..{len(orders)}")
    return rows, problems, ambiguous


def main():
    ap = derived.add_args(argparse.ArgumentParser(description="Hashtag PDF pages (projections + ADP) intake"))
    ap.add_argument("date", nargs="?", default="2026-09-30", help="page date (default 2026-09-30)")
    ap.add_argument("--out-dir", default=HERE)
    args = ap.parse_args()
    d, out = args.date, args.out_dir
    inp = derived.inputs_for(args, os.path.join(HERE, f"unmatched-hashtag-{d}.md"))
    proj_raw = inp.path(f"report/market/hashtag-raw-{d}.txt")
    # 2026-10-07: the ADP page is optional — the 10/6 upload was the projections page alone.
    # The existence test goes through the Inputs object so it holds in both modes (the
    # working tree and a pinned commit, where a missing file is a SystemExit, not an OSError).
    adp_raw = (inp.path(f"report/market/hashtag-adp-raw-{d}.txt")
               if f"hashtag-adp-raw-{d}.txt" in inp.listdir("report/market") else None)
    pool_path = inp.path("report/projections-2026-27.csv")
    yfiles = sorted(f for f in inp.listdir("report/market") if re.fullmatch(r"yahoo-\d{4}-\d{2}-\d{2}\.csv", f))
    ypath = inp.path(f"report/market/{yfiles[-1]}") if yfiles else None
    yahoo = {}
    if ypath:
        with open(ypath, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                yahoo[BM.norm(r["player"])] = r
    yahoo_adp = {k: float(v["adp"]) for k, v in yahoo.items() if v.get("adp")}

    proj, p1 = parse_projections(proj_raw)
    adp, p2, ambiguous = parse_adp(adp_raw, yahoo_adp) if adp_raw else ([], [], [])
    problems = p1 + p2
    print(f"projections: {len(proj)} rows ({sum(1 for r in proj if r['adp'])} with ADP, "
          f"{sum(1 for r in proj if r['flag'])} injury-flagged); ADP page: {len(adp)} rows "
          f"({sum(1 for r in adp if r.get('yahoo_adp') not in (None, ''))} Yahoo, "
          f"{sum(1 for r in adp if r.get('espn_adp') not in (None, ''))} ESPN, "
          f"{sum(1 for r in adp if r.get('fantrax_adp') not in (None, ''))} Fantrax; {len(ambiguous)} with fewer than three platform groups)")
    if problems:
        print(f"TRANSCRIPTION GATE: FAIL — {len(problems)} problem(s)")
        for p in problems:
            print(" ", p)
        sys.exit(2)
    print("TRANSCRIPTION GATE: PASS")
    BM._write_csv(os.path.join(out, f"hashtag-{d}.csv"), PROJ_COLS, proj)
    if adp_raw:
        BM._write_csv(os.path.join(out, f"hashtag-adp-{d}.csv"), ADP_COLS, adp)

    # ---- join the projection rows to the pool (names only; the lines are evidence, not edits)
    alias_index = {}
    for ours, variants in BM.ALIASES.items():
        for v in variants:
            alias_index[BM.norm(v)] = BM.norm(ours)
    canon = lambda n: alias_index.get(BM.norm(n), BM.norm(n))
    pool = {}
    with open(pool_path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            pool[BM.norm(r["name"])] = r
    hkeys = {canon(r["player"]): r for r in proj}
    matched = [k for k in hkeys if k in pool]
    hashtag_only = [hkeys[k] for k in hkeys if k not in pool]
    pool_only = [pool[k] for k in pool if k not in hkeys]
    key3 = lambda n: (n.split()[-1], n.split()[0][:3]) if n.split() else (n, n)
    pool_keys = {key3(k) for k in {BM.norm(r["name"]) for r in pool_only}}
    variants = [r for r in hashtag_only if key3(canon(r["player"])) in pool_keys]
    # ---- Yahoo ADP cross-check (the page's Yahoo column vs the newest paste)
    comp, diffs, posdiff = 0, [], []
    for r in adp:
        k = BM.norm(r["player"])
        if k in yahoo and yahoo[k].get("adp") and r.get("yahoo_adp") not in (None, ""):
            comp += 1
            dlt = round(float(r["yahoo_adp"]) - float(yahoo[k]["adp"]), 1)
            if abs(dlt) > 0.05:
                diffs.append((r["player"], float(yahoo[k]["adp"]), float(r["yahoo_adp"]), dlt))
        if k in yahoo and r.get("yahoo_pos"):
            a = ",".join(sorted(r["yahoo_pos"].split(",")))
            b = ",".join(sorted(yahoo[k]["pos"].replace(" ", "").split(",")))
            if a != b:
                posdiff.append((r["player"], yahoo[k]["pos"], r["yahoo_pos"]))
    L = [f"# Hashtag PDF pages — {d}: projections (top {len(proj)}) and ADP ({len(adp) if adp_raw else 'page not supplied'}{' rows' if adp_raw else ''})", "",
         f"Projection rows joined to the pool by name: {len(matched)} of {len(proj)} have a pool row; "
         f"{len(hashtag_only)} Hashtag-only; {len(pool_only)} pool rows are outside Hashtag's top {len(proj)} "
         "(a top-200 page carries no absence gate — the count is informational).", "",
         "## Hashtag names with no pool row", "", "| rank | player | team | Hashtag ADP |", "|---|---|---|---|"]
    for r in hashtag_only:
        L.append(f"| {r['rank']} | {r['player']} | {r['team']} | {r['adp'] or '—'} |")
    L += ["", f"## Yahoo ADP cross-check against `{os.path.basename(ypath) if ypath else 'n/a'}`", "",
          f"{comp} comparable rows; {len(diffs)} differ; largest |diff| "
          f"{max((abs(x[3]) for x in diffs), default=0.0)}; positions differing: {len(posdiff)}.", ""]
    if diffs:
        L += ["| player | paste ADP | page ADP | diff |", "|---|---|---|---|"]
        for p, a, b, dl in sorted(diffs, key=lambda x: -abs(x[3]))[:12]:
            L.append(f"| {p} | {a} | {b} | {dl:+.1f} |")
    if ambiguous:
        L += ["", "## ADP rows with fewer than three platform groups", "",
              "| player | groups | Yahoo group identified by the paste |", "|---|---|---|"]
        for n, g, c in ambiguous:
            L.append(f"| {n} | {g} | {'yes' if c else 'no'} |")
    L += ["", inp.stamp()]
    with open(os.path.join(out, f"unmatched-hashtag-{d}.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(f"wrote hashtag-{d}.csv, {'hashtag-adp-' + d + '.csv, ' if adp_raw else ''}unmatched-hashtag-{d}.md")
    if variants:
        print(f"GATE FAIL — {len(variants)} Hashtag-only name(s) look like spelling variants of pool-only names: "
              + ", ".join(r["player"] for r in variants))
        sys.exit(3)
    print(f"GATE PASS — {len(hashtag_only)} Hashtag-only name(s), none a spelling variant of a pool-only name")


if __name__ == "__main__":
    main()
