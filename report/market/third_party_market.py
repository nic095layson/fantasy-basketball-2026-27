#!/usr/bin/env python3
"""Third-party ranking intake (2026-09-29): an owner-supplied ranking file lands as a
REFERENCE source next to the Yahoo, Hashtag and Statdunk snapshots. The board stays
first-principles (owner decision 2026-08-21; fix F2: a single outlet never changes a pool row).

Sources (SOURCES below): `experts` — a top-50 consensus of experts' individual 9-cat
rankings (upload, Fantrax ADP column); `projected150` — a projected top 150 dated
2026-09-26 with each player's ACTUAL 2025-26 per-game line, a VALUE score and Yahoo
ADP / pre-rank snapshots (transcribed from the owner's paste of the article; the prose was
read in-session, not stored); `rotoballer` — RotoBaller's overall 9-cat PROJECTED
rankings, 250 rows with a projected 2026-27 per-game line, a positional rank and a tier.

For each source the raw file is kept verbatim (BOM tolerated) and every row is joined to
the pool under the work order's hard gate (§3.3): a source name with no pool row is
recorded as a pool-completeness item; one that looks like a spelling variant of a pool
name (surname + first three letters, the mechanical check from yahoo_market.py) trips the
gate (exit 3) until an alias or an accepted absence is recorded. Outputs:
  <source>-<date>.csv              joined rows: source rank, our board rank, availability-
                                   adjusted z, the newest Yahoo XRank / ADP on file, the
                                   source's extra columns and its stat line when it has one
  unmatched-<source>-<date>.md     the gate report
  disagreements-<source>-<date>.md rank agreement (Spearman), coverage, the two disagreement
                                   tables, team mismatches vs the kit, and — when the source
                                   carries a stat line — the kit projection against it, row by
                                   row where the gap crosses a threshold (re-derivation
                                   candidates, never automatic edits)
  provenance.csv                   one row merged by (source, fetched_on)
Drift fix D4 applies: --as-of / --live / --out-dir; the .md outputs end with the input stamp;
report/check_derived.py reproduces each committed intake at its pin.

Usage: python3 report/market/third_party_market.py <source> [YYYY-MM-DD] [--as-of DATE|COMMIT | --live] [--out-dir DIR]
"""
import argparse
import csv
import os
import re
import statistics as st
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = HERE
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import build_market as BM  # noqa: E402  norm(), ALIASES, our_board(), _write_csv, _merge_provenance, _zprofile
import derived  # noqa: E402
from market_stats import spearman  # noqa: E402

STAT_KEYS = ["pts", "tpm", "reb", "ast", "stl", "blk", "tov", "fg_pct", "ft_pct"]
THRESH = {"pts": 4.0, "tpm": 1.0, "reb": 2.0, "ast": 2.0, "stl": 0.5, "blk": 0.5, "tov": 1.0, "fg_pct": 4.0, "ft_pct": 5.0}
LAB = {"pts": "PTS", "tpm": "3PM", "reb": "REB", "ast": "AST", "stl": "STL", "blk": "BLK", "tov": "TOV", "fg_pct": "FG%", "ft_pct": "FT%"}
SOURCES = {
    "experts": dict(default_date="2026-09-29", raw="experts-raw-{d}.csv", gap=10,
                    cols=dict(rank="Rank", player="Player", team="Team", pos="Pos"),
                    extra={"avg_rank": "Avg rank", "fantrax_adp": "Fantrax ADP", "vs_25": "vs '25"}, stats=None,
                    title="the expert consensus (top 50)",
                    url="(owner upload — consensus of experts' individual 9-cat rankings; Fantrax ADP column)",
                    notes="Top-{n} expert consensus uploaded by the owner on {d} and kept verbatim as experts-raw-{d}.csv "
                          "(Rank, Player, Pos, Team, vs '25, Fantrax ADP, '25-26 FPPG (empty), Avg rank). Joined under the "
                          "hard gate by third_party_market.py ({m} matched, {u} without a pool row); reference layer only — "
                          "no board row changes (fix F2)."),
    "projected150": dict(default_date="2026-09-26", raw="projected150-raw-{d}.csv", gap=15,
                         cols=dict(rank="rank", player="player", team="team"),
                         extra={"value": "value", "gp_2025_26": "gp", "yahoo_adp_0926": "yahoo_adp_0926", "yahoo_prerank_0926": "yahoo_prerank_0926"},
                         stats=dict(kind="actual 2025-26 line", map={k: k for k in STAT_KEYS}),
                         title="the projected top 150 (2026-09-26)",
                         url="(owner paste of an article — 'Projected Top 150 for 2026-27', corrected 2025-26 production; Yahoo ADP and pre-rank snapshots dated 2026-09-26)",
                         notes="Projected top {n} dated {d} pasted by the owner on 2026-09-29; the structured fields (rank, team, 2025-26 GP "
                               "and per-game line, VALUE, Yahoo ADP and pre-rank) transcribed to projected150-raw-{d}.csv under "
                               "invariants (ranks contiguous, stats in range); the prose was read in-session and not stored. Joined "
                               "under the hard gate by third_party_market.py ({m} matched, {u} without a pool row); reference only."),
    "rotoworld": dict(default_date="2026-10-05", raw="rotoworld-9cat-{d}.csv", gap=20,
                      cols=dict(rank="Rank", player="Player", team="Team", pos="Pos"),
                      extra={"points_rank": "Points_Rank", "cat8_rank": "Cat8_Rank", "dynasty_rank": "Dynasty_Rank", "profile": "Profile", "age": "Age"},
                      stats=dict(kind="actual 2025-26 line (the kit's profile table; blank where the name has no profile or sat the season)",
                                 map={"pts": "PTS", "tpm": "3PM", "reb": "REB", "ast": "AST", "stl": "STL", "blk": "BLK", "tov": "TO", "fg_pct": "FG%", "ft_pct": "FT%"}),
                      team_map={"NOR": "NOP"},
                      title="Rotoworld's 2026-27 draft kit v2, the 9-category cheat sheet (200)",
                      url="(owner upload — Rotoworld / NBC Sports 2026-27 Fantasy Basketball Draft Kit v2, PDF modified 2026-10-05, read with pdfplumber by rotoworld_pdf_market.py)",
                      notes="Rotoworld draft kit v2 (PDF modified {d}, uploaded by the owner on 2026-10-06): the 9-category cheat sheet, {n} rows, "
                            "parsed from the raw text layer by rotoworld_pdf_market.py into rotoworld-9cat-{d}.csv with the points, 8-cat and "
                            "dynasty ranks, the profile rank and the profile's 2025-26 line (actuals, not projections). Joined under the hard gate "
                            "by third_party_market.py ({m} matched, {u} without a pool row); reference layer only — no board row changes (fix F2)."),
    "rotoballer": dict(default_date="2026-09-29", raw="rotoballer-raw-{d}.csv", gap=20,
                       cols=dict(rank="Rank", player="Player", team="Team", pos="Pos"),
                       extra={"pos_rank": "P-Rank", "tier": "Tier"},
                       stats=dict(kind="RotoBaller 2026-27 projection", map={"pts": "PTS", "tpm": "3PM", "reb": "REB", "ast": "AST", "stl": "STL", "blk": "BLK", "tov": "TO", "fg_pct": "FG%", "ft_pct": "FT%"}),
                       team_map={"GS": "GSW", "NO": "NOP", "NY": "NYK", "SA": "SAS", "WSH": "WAS"},
                       title="RotoBaller's overall 9-cat projected rankings (250)",
                       url="(owner upload — RotoBaller NBA overall 9-cat projected rankings CSV)",
                       notes="RotoBaller overall 9-cat projected rankings, {n} rows, uploaded by the owner on {d} and kept verbatim as "
                             "rotoballer-raw-{d}.csv (Rank, Player, Pos, Team, P-Rank, projected PTS/REB/AST/STL/BLK/3PM/FG%/FT%/TO, "
                             "Tier). Joined under the hard gate by third_party_market.py ({m} matched, {u} without a pool row); "
                             "reference only — no board row changes (fix F2)."),
    "profiles": dict(default_date="2026-09-29", raw="profiles-raw-{d}.csv", gap=20,
                     cols=dict(rank="Rank", player="Player", team="Team", pos="Pos"),
                     extra={"printed_rank": "Printed", "profile": "Profile", "claim": "Claim"}, stats=None,
                     tags="profiles-tags-raw-{d}.csv",
                     team_map={"Nuggets": "DEN", "Denver": "DEN", "Spurs": "SAS", "Thunder": "OKC", "Lakers": "LAL", "Pistons": "DET",
                               "Timberwolves": "MIN", "Celtics": "BOS", "Hawks": "ATL", "Clippers": "LAC", "Heat": "MIA", "Raptors": "TOR",
                               "Pacers": "IND", "76ers": "PHI", "Mavericks": "DAL", "Cavaliers": "CLE", "Rockets": "HOU", "Knicks": "NYK",
                               "Bulls": "CHI", "Wizards": "WAS", "Warriors": "GSW", "Pelicans": "NOP", "Pelican": "NOP", "Suns": "PHX",
                               "Trail Blazers": "POR", "Blazers": "POR", "Jazz": "UTA", "Kings": "SAC", "Magic": "ORL", "Hornets": "CHA",
                               "Bucks": "MIL", "Grizzlies": "MEM", "Nets": "BKN"},
                     title="an unnamed outlet's 9-cat top 144 with profiles (owner paste, 2026-09-29)",
                     url="(owner paste of an article — outlet not named; a 9-cat top 144 with prose profiles on the top 50, and its companion sleepers / breakouts / busts piece)",
                     notes="A 9-cat top 144 pasted by the owner on {d} (outlet not named; teams given as nicknames, mapped to codes; "
                           "the list numbers 126 twice, so Rank is the list position 1..145 and Printed keeps the article's number) "
                           "transcribed to profiles-raw-{d}.csv with a Profile flag and a short Claim in the analyst's own words for the "
                           "50 profiled players; the companion sleepers / breakouts / busts lists transcribed to profiles-tags-raw-{d}.csv "
                           "(38 rows). The prose was read in-session and not stored. Joined under the hard gate by third_party_market.py "
                           "({m} matched, {u} without a pool row); reference only — no board row changes (fix F2; a single unnamed outlet)."),
}
# Source names verified absent from the pool (a reason each). Anything else without a pool
# row is listed as a pool-completeness item; a possible spelling variant trips the gate.
_ACCEPTED_ABSENT = {}


def _key3(n):
    t = BM.norm(n).split()
    return (t[-1], t[0][:3]) if t else ("", "")


def main():
    global OUT
    ap = derived.add_args(argparse.ArgumentParser(description="third-party ranking intake under the hard unmatched gate"))
    ap.add_argument("source", choices=sorted(SOURCES))
    ap.add_argument("date", nargs="?")
    ap.add_argument("--out-dir", default=HERE)
    args = ap.parse_args()
    S = SOURCES[args.source]
    src, d = args.source, args.date or S["default_date"]
    OUT = args.out_dir
    BM.OUT = OUT
    inp = derived.inputs_for(args, os.path.join(HERE, f"unmatched-{src}-{d}.md"))
    raw = list(csv.DictReader(open(inp.path(f"report/market/{S['raw'].format(d=d)}"), encoding="utf-8-sig")))
    C = S["cols"]
    if not raw or C["player"] not in raw[0] or C["rank"] not in raw[0]:
        sys.exit(f"third_party_market: unexpected columns in {S['raw'].format(d=d)}: {list(raw[0].keys()) if raw else 'empty'}")
    board = BM.our_board(inp.path("report/projections-2026-27.csv"))
    files = inp.listdir("report/market")
    yr = sorted(f for f in files if re.fullmatch(r"yahoo-9cat-rankings-\d{4}-\d{2}-\d{2}\.csv", f))
    yc = sorted(f for f in files if re.fullmatch(r"consensus-\d{4}-\d{2}-\d{2}\.csv", f))
    xr = {BM.norm(r["player"]): r for r in csv.DictReader(open(inp.path(f"report/market/{yr[-1]}"), encoding="utf-8"))} if yr else {}
    adp = {BM.norm(r["player"]): r for r in csv.DictReader(open(inp.path(f"report/market/{yc[-1]}"), encoding="utf-8"))} if yc else {}

    alias_index = {BM.norm(v): BM.norm(k) for k, vs in BM.ALIASES.items() for v in vs}
    key = lambda n: alias_index.get(BM.norm(n), BM.norm(n))
    by_key = {key(n): (n, b) for n, b in board.items()}
    pool3 = {}
    for n in board:
        pool3.setdefault(_key3(n), []).append(n)
    tmap = S.get("team_map", {})
    rows, absent, trips = [], [], []
    for r in raw:
        name = r[C["player"]].strip()
        hit = by_key.get(key(name))
        team_src = tmap.get(r.get(C.get("team", ""), ""), r.get(C.get("team", ""), "")) if C.get("team") else ""
        if hit is None:
            if name in _ACCEPTED_ABSENT:
                absent.append((int(r[C["rank"]]), name, team_src, _ACCEPTED_ABSENT[name]))
            elif pool3.get(_key3(name)):
                trips.append((int(r[C["rank"]]), name, team_src, pool3[_key3(name)]))
            else:
                absent.append((int(r[C["rank"]]), name, team_src, "no pool row (pool-completeness item; verify the name against the raw before adding a sourced row)"))
            continue
        n, b = hit
        y, a = xr.get(BM.norm(n), {}), adp.get(BM.norm(n), {})
        row = {"src_rank": int(r[C["rank"]]), "player": n, "team_src": team_src, "team_kit": b["row"]["team"],
               "our_rank": b["rank"], "z_adj": round(b["z_adj"], 3),
               "yahoo_xrank": y.get("xrank", ""), "yahoo_adp": a.get("yahoo_adp", ""), "src_name": name}
        for k, c in S["extra"].items():
            row[k] = r.get(c, "")
        if S["stats"]:
            for k, c in S["stats"]["map"].items():
                row[f"src_{k}"] = r.get(c, "")
        rows.append(row)
    # Companion tag lists (sleepers / breakouts / busts) — joined under the same gate; a tag name
    # outside the ranking keeps an empty source rank.
    tag_rows, tag_absent = [], []
    if S.get("tags"):
        traw = list(csv.DictReader(open(inp.path(f"report/market/{S['tags'].format(d=d)}"), encoding="utf-8-sig")))
        srank = {r["player"]: r["src_rank"] for r in rows}
        for r in traw:
            name = r["Player"].strip()
            hit = by_key.get(key(name))
            team_src = tmap.get(r.get("Team", ""), r.get("Team", ""))
            if hit is None:
                if pool3.get(_key3(name)):
                    trips.append((0, name, team_src, pool3[_key3(name)]))
                else:
                    tag_absent.append((r["Section"], name, team_src, "no pool row (pool-completeness item; verify the name against the raw before adding a sourced row)"))
                continue
            n, b = hit
            y, a = xr.get(BM.norm(n), {}), adp.get(BM.norm(n), {})
            tag_rows.append({"section": r["Section"], "tier": r["Tier"], "player": n, "team_src": team_src, "team_kit": b["row"]["team"],
                             "our_rank": b["rank"], "z_adj": round(b["z_adj"], 3), "src_rank": srank.get(n, ""),
                             "yahoo_xrank": y.get("xrank", ""), "yahoo_adp": a.get("yahoo_adp", ""), "claim": r.get("Claim", ""), "src_name": name})
    print(f"JOIN ({src} {d}): {len(raw)} source rows | matched to pool={len(rows)} | no pool row={len(absent)} | possible spelling variants={len(trips)}"
          + (f" | tag rows {len(tag_rows)} matched, {len(tag_absent)} without a pool row" if S.get("tags") else ""))
    if trips:
        print("HARD GATE TRIP — source names that look like a pool spelling (add a verified alias, or record the absence with a reason):")
        for rk, n, t, hits in trips:
            print(f"  #{rk:<4} {n} ({t})  ~  {', '.join(hits)}")
        sys.exit(3)

    cols = ["src_rank", "player", "team_src", "team_kit", "our_rank", "z_adj", "yahoo_xrank", "yahoo_adp"] + list(S["extra"]) + \
           ([f"src_{k}" for k in S["stats"]["map"]] if S["stats"] else []) + ["src_name"]
    BM._write_csv(os.path.join(OUT, f"{src}-{d}.csv"), cols, rows)
    if S.get("tags"):
        BM._write_csv(os.path.join(OUT, f"{src}-tags-{d}.csv"),
                      ["section", "tier", "player", "team_src", "team_kit", "our_rank", "z_adj", "src_rank", "yahoo_xrank", "yahoo_adp", "claim", "src_name"], tag_rows)
    stamp = inp.stamp()
    n_src, n_pool = len(raw), len(board)

    # ---- gate report
    L = [f"# Unmatched-name report vs {S['title']} — {d} (HARD GATE, work order §3.3)", "",
         f"Source rows: {n_src}; pool players: {n_pool}; joined: {len(rows)}. Every source name below has no pool row after "
         "normalization and documented aliases and shares no surname + first-three-letters key with any pool name "
         "(the mechanical variant check); each is a pool-completeness item or an accepted absence. Silent partial joins are refused.", "",
         f"## Source names without a pool row ({len(absent)})", "",
         "| source # | name | team | reason |", "|---|---|---|---|"]
    for rk, n, t, why in absent:
        L.append(f"| {rk} | {n} | {t} | {why} |")
    if S.get("tags"):
        L += ["", f"## Tag-list names without a pool row ({len(tag_absent)})", "",
              "| section | name | team | reason |", "|---|---|---|---|"]
        for sec, n, t, why in tag_absent:
            L.append(f"| {sec} | {n} | {t} | {why} |")
    L += ["", stamp]
    open(os.path.join(OUT, f"unmatched-{src}-{d}.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")

    # ---- disagreements
    pairs = [(float(r["our_rank"]), float(r["src_rank"])) for r in rows]
    rho = spearman(pairs)
    py = [(float(r["our_rank"]), float(r["yahoo_xrank"])) for r in rows if r["yahoo_xrank"]]
    rho_y = spearman(py) if len(py) > 2 else float("nan")
    ps = [(float(r["src_rank"]), float(r["yahoo_xrank"])) for r in rows if r["yahoo_xrank"]]
    rho_sy = spearman(ps) if len(ps) > 2 else float("nan")
    N = len(raw)
    ours_top = [b["row"]["name"] for b in sorted(board.values(), key=lambda b: b["rank"])[:N]]
    src_names = {r["player"] for r in rows}
    in_both = sum(1 for n in ours_top if n in src_names)
    ours_only = [n for n in ours_top if n not in src_names]
    med = st.median(abs(a - b) for a, b in pairs)
    GAP = S["gap"]
    higher = sorted([r for r in rows if r["our_rank"] + GAP <= r["src_rank"]], key=lambda r: r["our_rank"] - r["src_rank"])
    lower = sorted([r for r in rows if r["src_rank"] + GAP <= r["our_rank"]], key=lambda r: -(r["our_rank"] - r["src_rank"]))
    mism = [r for r in rows if r["team_src"] and r["team_src"] != r["team_kit"]]
    fmt = lambda v: v if v not in ("", None) else "—"
    prof = lambda name: BM._zprofile({"name": name})
    D = [f"# {S['title'][0].upper() + S['title'][1:]} vs the board — {d}", "",
         f"Source: {S['url']}; raw kept verbatim as `{S['raw'].format(d=d)}`. Reference layer only: the board is first-principles "
         "and no row changes because of this file (owner decision 2026-08-21; fix F2).", "",
         "## A. Agreement", "",
         "| measure | value |", "|---|---|",
         f"| source rows joined | {len(rows)} of {n_src} |",
         f"| Spearman rho, our rank vs source rank | {rho:.3f} |",
         f"| Spearman rho, our rank vs Yahoo XRank ({yr[-1] if yr else 'no file'}), same rows | {rho_y:.3f} ({len(py)} rows) |",
         f"| Spearman rho, source rank vs Yahoo XRank, same rows | {rho_sy:.3f} ({len(ps)} rows) |",
         f"| median absolute gap, our rank vs source rank | {med:.0f} places |",
         f"| source's top {N} inside our top {N} | {in_both} of {N} |",
         f"| our top-{N} names the source leaves out | {len(ours_only)}: {', '.join(ours_only[:40])}{'…' if len(ours_only) > 40 else ''} |", "",
         f"## B. We are higher by {GAP}+ places ({len(higher)}) — the board's values against the source", "",
         "| gap | player | our # | source # | Yahoo XRank / ADP | our board z-lean |", "|---|---|---|---|---|---|"]
    for r in higher:
        D.append(f"| +{r['src_rank'] - r['our_rank']} | {r['player']} | {r['our_rank']} | {r['src_rank']} | {fmt(r['yahoo_xrank'])} / {fmt(r['yahoo_adp'])} | {prof(r['player'])} |")
    D += ["", f"## C. The source is higher by {GAP}+ places ({len(lower)}) — the board's fades against the source", "",
          "| gap | player | our # | source # | Yahoo XRank / ADP | our board z-lean |", "|---|---|---|---|---|---|"]
    for r in lower:
        D.append(f"| -{r['our_rank'] - r['src_rank']} | {r['player']} | {r['our_rank']} | {r['src_rank']} | {fmt(r['yahoo_xrank'])} / {fmt(r['yahoo_adp'])} | {prof(r['player'])} |")
    D += ["", f"## D. Team mismatches vs the kit ({len(mism)})", "",
          "| source # | player | source says | kit says (verified ledger) |", "|---|---|---|---|"]
    for r in mism:
        D.append(f"| {r['src_rank']} | {r['player']} | {r['team_src']} | {r['team_kit']} |")
    if S["stats"]:
        kit = {key(r["name"]): r for r in csv.DictReader(open(inp.path("report/projections-2026-27.csv"), encoding="utf-8"))}
        flagged = []
        for r in rows:
            k = kit.get(key(r["player"]))
            if not k or not r.get("src_pts"):
                continue
            kv = {"pts": float(k["pts"]), "tpm": float(k["tpm"]), "reb": float(k["reb"]), "ast": float(k["ast"]), "stl": float(k["stl"]),
                  "blk": float(k["blk"]), "tov": float(k["tov"]), "fg_pct": 100 * float(k["fgp"]), "ft_pct": 100 * float(k["ftp"])}
            sv = {c: float(r[f"src_{c}"]) for c in STAT_KEYS if r.get(f"src_{c}") not in ("", None)}
            hits = [(c, kv[c] - sv[c]) for c in STAT_KEYS if c in sv and abs(kv[c] - sv[c]) >= THRESH[c]]
            if hits:
                flagged.append((r["our_rank"], r["player"], r["src_rank"], hits, kv, sv))
        flagged.sort()
        D += ["", f"## E. The kit's projection line against the source's {S['stats']['kind']} ({len(flagged)} rows cross a threshold)", "",
              "Kit minus source, per game; a row is listed when any category crosses the threshold "
              + ", ".join(f"{LAB[c]} {THRESH[c]:g}" for c in STAT_KEYS) + ". These are re-derivation candidates, never automatic edits: "
              + ("a projection is supposed to differ from last season where the role changed." if "actual" in S["stats"]["kind"] else "two projections disagreeing is a question for the role research, not an answer."), "",
              "| our # | player | source # | categories crossing the threshold (kit vs source) |", "|---|---|---|---|"]
        for our, name, srk, hits, kv, sv in flagged:
            cells = "; ".join(f"{LAB[c]} {kv[c]:.1f} vs {sv[c]:.1f} ({dlt:+.1f})" for c, dlt in hits)
            D.append(f"| {our} | {name} | {srk} | {cells} |")
    D += ["", "## F. Every row", "",
          "| source # | player | team | our # | Yahoo XRank / ADP | " + " | ".join(S["extra"]) + " |",
          "|" + "---|" * (5 + len(S["extra"]))]
    for r in rows:
        D.append(f"| {r['src_rank']} | {r['player']} | {r['team_src'] or '—'} | {r['our_rank']} | {fmt(r['yahoo_xrank'])} / {fmt(r['yahoo_adp'])} | "
                 + " | ".join(fmt(r[k]) for k in S["extra"]) + " |")
    if S.get("tags"):
        D += ["", f"## G. The source's sleepers / breakouts / busts against the board ({len(tag_rows)} names)", "",
              "Our # is the board's first-principles rank; the source # is the same article's ranking (empty when the name sits "
              "outside its top 144). The board z-lean is the row's own profile, not a reaction to the tag.", "",
              "| section | tier | player | our # | source # | Yahoo XRank / ADP | our board z-lean | the source's reason |", "|---|---|---|---|---|---|---|---|"]
        for r in tag_rows:
            D.append(f"| {r['section']} | {r['tier']} | {r['player']} | {r['our_rank']} | {fmt(r['src_rank'])} | {fmt(r['yahoo_xrank'])} / {fmt(r['yahoo_adp'])} | {prof(r['player'])} | {r['claim']} |")
    D += ["", stamp]
    open(os.path.join(OUT, f"disagreements-{src}-{d}.md"), "w", encoding="utf-8").write("\n".join(D) + "\n")
    BM._merge_provenance([{"source": src, "url": S["url"], "fetched_on": d, "rows": n_src,
                           "notes": S["notes"].format(n=n_src, d=d, m=len(rows), u=len(absent))}])
    print(f"wrote {src}-{d}.csv, unmatched-{src}-{d}.md, disagreements-{src}-{d}.md, provenance.csv")
    print(f"rho(our, source) = {rho:.3f} | rho(our, Yahoo XRank) = {rho_y:.3f} | rho(source, Yahoo XRank) = {rho_sy:.3f} | "
          f"in both top-{N}: {in_both} | team mismatches: {len(mism)}" + (f" | stat rows flagged: {len(flagged)}" if S["stats"] else ""))
    print("GATE PASS — every source name matched or recorded.")


if __name__ == "__main__":
    main()
