#!/usr/bin/env python3
"""Rotoworld (NBC Sports) 2026-27 Fantasy Basketball Draft Kit v2, uploaded by the owner on
2026-10-06 (PDF modified 2026-10-05). Read with pdfplumber page by page (parser output only;
pdf-extract law): the raw layer is rotoworld-raw-<date>.txt — every page's text, with the
two-column profile pages (7-19 guards, 21-33 forwards, 35-43 centers) cropped into a left and a
right column so a profile's lines stay together. The kit carries an offseason recap, 141 player
profiles (age, height, weight, the 2025-26 per-game line where the player has one, and prose:
2025-26 / What's Changed / Outlook) and four cheat sheets (points 200, 8-category 200,
9-category 200, dynasty 300). It carries no projected stat lines.

  --extract PDF                   write the raw text layer (once, at intake)
  <date> [--as-of|--live|--out-dir] parse the raw text deterministically into
    rotoworld-sheets-<date>.csv    one row per name across the four sheets (ranks per sheet, the
                                   9-cat sheet's position and team; the dynasty sheet's team where
                                   it differs)
    rotoworld-profiles-<date>.csv  141 rows: section, profile rank, player, team, age, ht, wt, the
                                   2025-26 line (blank for rookies and players who sat the year)
                                   and the three prose fields
    rotoworld-9cat-<date>.csv      the 9-cat sheet in the third-party intake's raw shape (Rank,
                                   Player, Pos, Team) with the other sheets' ranks, the profile
                                   rank, age and the 2025-26 line where a profile exists — the
                                   input of `third_party_market.py rotoworld <date>`
    rotoworld-parse-<date>.md      counts, invariants, the sheets' internal team disagreements,
                                   and the input stamp (drift fix D4)

Transcription invariants: each sheet's ranks contiguous 1..N; profile ranks contiguous within
each section; every profile carries an age line; a stat line parses in full or is absent. Exit 2
on any failure. The board is untouched: a ranking outlet is one line of evidence, never an edit
(owner decision 2026-08-21; fix F2).
Usage: python3 report/market/rotoworld_pdf_market.py --extract <pdf> [YYYY-MM-DD]
       python3 report/market/rotoworld_pdf_market.py [YYYY-MM-DD] [--as-of DATE|COMMIT | --live] [--out-dir DIR]
"""
import argparse
import csv
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import build_market as BM  # noqa: E402  norm(), _write_csv
import derived  # noqa: E402

DEFAULT_DATE = "2026-10-05"
PROFILE_PAGES = list(range(7, 20)) + list(range(21, 34)) + list(range(35, 44))
SHEETS = {"points": (45, 46), "cat8": (47, 48), "cat9": (49, 50), "dynasty": (51, 52, 53)}
TEAMS_FULL = ["Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", "Chicago Bulls",
              "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons",
              "Golden State Warriors", "Houston Rockets", "Indiana Pacers", "Los Angeles Clippers",
              "Los Angeles Lakers", "LA Clippers", "Memphis Grizzlies", "Miami Heat", "Milwaukee Bucks",
              "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks", "Oklahoma City Thunder",
              "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns", "Portland Trail Blazers",
              "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors", "Utah Jazz", "Washington Wizards"]
HDR = re.compile(r"^(\d+) (.+?) (" + "|".join(TEAMS_FULL) + r")\s*$")
PCT = r"(\.\d{3}|\d{1,3}(?:\.\d)?)"
STAT = re.compile(r"^(20\d\d-\d\d) ([A-Z0-9]{2,3}) (\d+) ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+) " + PCT +
                  r" ([\d.]+) ([\d.]+) " + PCT + r" ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+)\s*$")
AGE = re.compile(r"^Age: (\d+) HT: (\d-\d{1,2}) WT: (\d+)")
FOOT = re.compile(r"Fantasy Basketball Draft Kit \| \d+$|^\d+ \| 20\d\d-\d\d Fantasy Basketball Draft Kit$")
ROW = re.compile(r"(\d{1,3})\. (.+?) (G/F|F/C|G/C|G|F|C) \(?([A-Z]{2,3})\)?(?: C)?(?=\s|$)")
TEAM_FIX = {"NOR": "NOP"}      # the sheets' two spellings of New Orleans
MARKS = (("recap", "2025-26:"), ("changed", "What’s Changed:"), ("outlook", "Outlook:"))


def fail(msg):
    print(f"rotoworld_pdf_market: {msg}", file=sys.stderr)
    sys.exit(2)


def derank(s):
    """The kit prints profile ranks with every digit doubled ('1199' is 19)."""
    return int(s[::2]) if len(s) % 2 == 0 and s[::2] == s[1::2] else int(s)


# --------------------------------------------------------------------------- extract (once)
def extract(pdf_path, date, out_dir):
    import pdfplumber
    raw = open(pdf_path, "rb").read()
    lines = [f"# Rotoworld 2026-27 Fantasy Basketball Draft Kit v2 — pdfplumber {pdfplumber.__version__} text layer",
             f"# PDF sha256 {hashlib.sha256(raw).hexdigest()} md5 {hashlib.md5(raw).hexdigest()} bytes {len(raw)}"]
    with pdfplumber.open(pdf_path) as pdf:
        meta = pdf.metadata or {}
        lines.append(f"# pages {len(pdf.pages)} CreationDate {meta.get('CreationDate')} ModDate {meta.get('ModDate')}")
        for i, p in enumerate(pdf.pages, 1):
            if i in PROFILE_PAGES:
                w, h = p.width, p.height
                for tag, box in (("L", (0, 0, w / 2, h)), ("R", (w / 2, 0, w, h))):
                    lines.append(f"=== page {i} col {tag} ===")
                    lines.append(p.crop(box).extract_text() or "")
            else:
                lines.append(f"=== page {i} ===")
                lines.append(p.extract_text() or "")
    path = os.path.join(out_dir, f"rotoworld-raw-{date}.txt")
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"wrote {path}: {len(pdf.pages)} pages")


# --------------------------------------------------------------------------- parse
def blocks(raw_text):
    """[(page, col or '', text)] in file order."""
    out, cur, buf = [], None, []
    for ln in raw_text.split("\n"):
        m = re.match(r"^=== page (\d+)(?: col ([LR]))? ===$", ln)
        if m:
            if cur:
                out.append((cur[0], cur[1], "\n".join(buf)))
            cur, buf = (int(m.group(1)), m.group(2) or ""), []
        elif cur:
            buf.append(ln)
    if cur:
        out.append((cur[0], cur[1], "\n".join(buf)))
    return out


def parse_sheets(blk):
    page_text = {p: t for p, c, t in blk if c == ""}
    out = {}
    for name, pages in SHEETS.items():
        rows = []
        for n in pages:
            t = re.sub(r"(G/F|F/C|G/C|G|F|C) I ND(?=\s|$)", r"\1 IND", page_text[n])   # a split team code
            t = re.sub(r"(G/F|F/C|G/C|G|F|C) ND(?=\s|$)", r"\1 IND", t)
            for ln in t.split("\n"):
                for m in ROW.finditer(ln):
                    if re.search(r"\d\. ", m.group(2)):
                        fail(f"{name} sheet page {n}: a row swallowed its neighbour — {m.group(0)!r}")
                    rows.append({"rank": int(m.group(1)), "player": m.group(2).strip(), "pos": m.group(3),
                                 "team": TEAM_FIX.get(m.group(4), m.group(4))})
        rows.sort(key=lambda r: r["rank"])
        ranks = [r["rank"] for r in rows]
        if ranks != list(range(1, len(rows) + 1)):
            fail(f"{name} sheet: ranks not contiguous 1..{len(rows)} (missing {sorted(set(range(1, max(ranks) + 1)) - set(ranks))[:10]})")
        out[name] = rows
    return out


def parse_profiles(blk):
    profiles, section, cur = [], None, None
    for page, col, text in blk:
        if page not in PROFILE_PAGES:
            continue
        for ln in text.split("\n"):
            ln = ln.strip()
            if not ln or FOOT.search(ln):
                continue
            if ln in ("GUARDS", "FORWARDS", "CENTERS", "GUARDS GUARDS", "FORWARDS FORWARDS", "CENTERS CENTERS"):
                section = ln.split()[0]
                continue
            m = HDR.match(ln)
            if m:
                cur = {"section": section, "profile_rank": derank(m.group(1)), "player": m.group(2), "team_name": m.group(3), "_prose": []}
                profiles.append(cur)
                continue
            if cur is None:
                continue
            m = AGE.match(ln)
            if m and "age" not in cur:
                cur.update(age=int(m.group(1)), ht=m.group(2), wt=int(m.group(3)))
                continue
            if ln.startswith("Year Team G MIN"):
                continue
            m = STAT.match(ln)
            if m and "g" not in cur:
                g = list(m.groups())
                pct = lambda v: v if v.startswith(".") else f"{float(v) / 100:.3f}"
                cur.update(year=g[0], team25=g[1], g=g[2], mpg=g[3], pts=g[4], fgm=g[5], fga=g[6], fgp=pct(g[7]),
                           ftm=g[8], fta=g[9], ftp=pct(g[10]), tpm=g[11], reb=g[12], ast=g[13], stl=g[14], blk=g[15], tov=g[16])
                continue
            cur["_prose"].append(ln)
    for p in profiles:
        text = " ".join(p.pop("_prose"))
        pos = {k: text.find(mark) for k, mark in MARKS}
        order = sorted(((i, k) for k, i in pos.items() if i >= 0))
        for j, (i, k) in enumerate(order):
            end = order[j + 1][0] if j + 1 < len(order) else len(text)
            p[k] = text[i + len(dict(MARKS)[k]):end].strip()
        for k, _ in MARKS:
            p.setdefault(k, "")
        if "age" not in p:
            fail(f"profile {p['player']} has no age line")
    for sec in ("GUARDS", "FORWARDS", "CENTERS"):
        rs = [p["profile_rank"] for p in profiles if p["section"] == sec]
        if rs != list(range(1, len(rs) + 1)):
            fail(f"{sec} profile ranks not contiguous: {rs}")
    return profiles


def main():
    ap = derived.add_args(argparse.ArgumentParser(description="Rotoworld draft kit PDF intake"))
    ap.add_argument("date", nargs="?", default=DEFAULT_DATE)
    ap.add_argument("--extract", metavar="PDF", help="write the raw text layer from the PDF (once, at intake)")
    ap.add_argument("--out-dir", default=HERE)
    args = ap.parse_args()
    d, out = args.date, args.out_dir
    if args.extract:
        extract(args.extract, d, out)
        return
    inp = derived.inputs_for(args, os.path.join(HERE, f"rotoworld-parse-{d}.md"))
    raw = open(inp.path(f"report/market/rotoworld-raw-{d}.txt"), encoding="utf-8").read()
    blk = blocks(raw)
    sheets = parse_sheets(blk)
    profiles = parse_profiles(blk)
    pcols = ["section", "profile_rank", "player", "team_name", "age", "ht", "wt", "year", "team25", "g", "mpg", "pts", "fgm",
             "fga", "fgp", "ftm", "fta", "ftp", "tpm", "reb", "ast", "stl", "blk", "tov", "recap", "changed", "outlook"]
    BM._write_csv(os.path.join(out, f"rotoworld-profiles-{d}.csv"), pcols, [{c: p.get(c, "") for c in pcols} for p in profiles])

    # one row per name across the sheets, keyed by the planes gate's normalisation
    union, order = {}, []
    for name in ("cat9", "points", "cat8", "dynasty"):
        for r in sheets[name]:
            k = BM.norm(r["player"])
            if k not in union:
                union[k] = {"player": r["player"], "pos": r["pos"], "team": r["team"], "points_rank": "", "cat8_rank": "",
                            "cat9_rank": "", "dynasty_rank": "", "team_dynasty": ""}
                order.append(k)
            union[k][f"{name}_rank"] = r["rank"]
            if name == "dynasty" and r["team"] != union[k]["team"]:
                union[k]["team_dynasty"] = r["team"]
    srows = sorted((union[k] for k in order), key=lambda r: (r["cat9_rank"] or 999, r["points_rank"] or 999, r["dynasty_rank"] or 999))
    BM._write_csv(os.path.join(out, f"rotoworld-sheets-{d}.csv"),
                  ["player", "pos", "team", "cat9_rank", "cat8_rank", "points_rank", "dynasty_rank", "team_dynasty"], srows)

    # the 9-cat sheet in the third-party raw shape, with the profile's 2025-26 line where one exists
    prof = {BM.norm(p["player"]): p for p in profiles}
    nine = []
    for r in sheets["cat9"]:
        p = prof.get(BM.norm(r["player"]), {})
        u = union[BM.norm(r["player"])]
        pct = lambda v: f"{100 * float(v):.1f}" if v else ""
        nine.append({"Rank": r["rank"], "Player": r["player"], "Pos": r["pos"], "Team": r["team"],
                     "Points_Rank": u["points_rank"], "Cat8_Rank": u["cat8_rank"], "Dynasty_Rank": u["dynasty_rank"],
                     "Profile": f"{p['section'][0]}{p['profile_rank']}" if p else "", "Age": p.get("age", ""),
                     "PTS": p.get("pts", ""), "3PM": p.get("tpm", ""), "REB": p.get("reb", ""), "AST": p.get("ast", ""),
                     "STL": p.get("stl", ""), "BLK": p.get("blk", ""), "TO": p.get("tov", ""),
                     "FG%": pct(p.get("fgp", "")), "FT%": pct(p.get("ftp", ""))})
    BM._write_csv(os.path.join(out, f"rotoworld-9cat-{d}.csv"),
                  ["Rank", "Player", "Pos", "Team", "Points_Rank", "Cat8_Rank", "Dynasty_Rank", "Profile", "Age",
                   "PTS", "3PM", "REB", "AST", "STL", "BLK", "TO", "FG%", "FT%"], nine)

    with_line = sum(1 for p in profiles if p.get("g"))
    no_line = [f"{p['player']} ({p['section'][0]}{p['profile_rank']})" for p in profiles if not p.get("g")]
    prof_not_on_9 = [p["player"] for p in profiles if BM.norm(p["player"]) not in {BM.norm(r["player"]) for r in sheets["cat9"]}]
    nine_no_prof = sum(1 for r in nine if not r["Profile"])
    dyn_team = [(u["player"], u["team"], u["team_dynasty"]) for u in srows if u["team_dynasty"]]
    L = [f"# Rotoworld draft kit v2 — parse report, {d}", "",
         "Source: the owner's upload of 2026-10-06 (Rotoworld / NBC Sports 2026-27 Fantasy Basketball Draft Kit v2; the PDF's "
         "modification date is 2026-10-05). Raw layer `rotoworld-raw-" + d + ".txt` (pdfplumber text, profile pages cropped into "
         "two columns). The kit carries no projected stat lines: the profiles' lines are 2025-26 actuals.", "",
         "| measure | value |", "|---|---|",
         f"| cheat sheets parsed | points {len(sheets['points'])}, 8-cat {len(sheets['cat8'])}, 9-cat {len(sheets['cat9'])}, dynasty {len(sheets['dynasty'])} (ranks contiguous in each) |",
         f"| distinct names across the four sheets | {len(srows)} |",
         f"| profiles parsed | {len(profiles)} (guards {sum(1 for p in profiles if p['section'] == 'GUARDS')}, forwards {sum(1 for p in profiles if p['section'] == 'FORWARDS')}, centers {sum(1 for p in profiles if p['section'] == 'CENTERS')}) |",
         f"| profiles with a 2025-26 line | {with_line}; without one (rookies, players who sat the season): {len(no_line)} — {', '.join(no_line)} |",
         f"| 9-cat names without a profile | {nine_no_prof} of {len(nine)} |",
         f"| profiled names outside the 9-cat 200 | {len(prof_not_on_9)}: {', '.join(prof_not_on_9) or '—'} |",
         f"| dynasty sheet's team differs from the 9-cat/points/8-cat team | {len(dyn_team)}: " + ", ".join(f"{n} ({t} vs dynasty {td})" for n, t, td in dyn_team) + " |",
         "", inp.stamp()]
    open(os.path.join(out, f"rotoworld-parse-{d}.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"wrote rotoworld-sheets-{d}.csv ({len(srows)} names), rotoworld-profiles-{d}.csv ({len(profiles)}), "
          f"rotoworld-9cat-{d}.csv ({len(nine)}), rotoworld-parse-{d}.md")


if __name__ == "__main__":
    main()
