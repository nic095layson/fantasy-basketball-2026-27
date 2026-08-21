#!/usr/bin/env python3
"""9-cat z-score ranking engine — implements PROMPT.md §4.2.

Reads projections-2026-27.csv (per-game projections + GP), computes impact-weighted
z-scores over an iterated top-180 draft pool, availability-adjusts with a
streaming-credit model (GP/82 plus 0.20 credit on missed games; negatives never
shrunk by absence), and writes top-200-2026-27.md. Update the CSV, re-run, done.
"""
import csv
import math
import os
import sys
from datetime import date

from check_provenance import check as check_provenance

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTING = ["tpm", "pts", "reb", "ast", "stl", "blk"]
PUNTS = ["fgp", "ftp", "tpm", "pts", "ast", "tov"]  # the six common punt builds
POOL_SIZE = 180
# Streaming credit (method change 2026-07-27): in weekly H2H with open roster
# moves, a missed game is partly replaceable, so availability-adjusted value
# uses GP/82 + (1-GP/82)*STREAM_R for positive-value players. STREAM_R is
# anchored to the deck plane's arena-calibrated 0.78 risk multiplier (solve
# a + (1-a)*r = 0.78 at the risk-class GP centroid a~=0.72), the law whose
# own rationale is that missed games are partly replaceable via streaming.
# Negative per-game values are NEVER shrunk by absence (matches
# scripts/hoops.py adj_value: a 15-GP rehab season must not outrank playable
# players — the linear model had DiVincenzo #93 on exactly that artifact).
# Derivation + full board diff: report/method-change-2026-07-27-availability.md
STREAM_R = 0.20


def avail(gp):
    a = gp / 82.0
    return a + (1 - a) * STREAM_R


def load(path):
    with open(path) as f:
        rows = [r for r in csv.DictReader(f)]
    for r in rows:
        for k in r:
            if k not in ("name", "team", "pos"):
                r[k] = float(r[k])
    return rows


def zscores(rows, pool):
    """Return {name: {cat: z}} using pool means/SDs. %s are impact-weighted."""
    def mean_sd(vals):
        m = sum(vals) / len(vals)
        sd = math.sqrt(sum((v - m) ** 2 for v in vals) / len(vals)) or 1.0
        return m, sd

    # volume-weighted pool percentages
    pool_fgp = sum(r["fgp"] * r["fga"] for r in pool) / max(sum(r["fga"] for r in pool), 1e-9)
    pool_ftp = sum(r["ftp"] * r["fta"] for r in pool) / max(sum(r["fta"] for r in pool), 1e-9)
    for r in rows:
        r["fg_imp"] = (r["fgp"] - pool_fgp) * r["fga"]
        r["ft_imp"] = (r["ftp"] - pool_ftp) * r["fta"]

    stats = {}
    for cat in COUNTING + ["fg_imp", "ft_imp", "tov"]:
        stats[cat] = mean_sd([r[cat] for r in pool])

    out = {}
    for r in rows:
        z = {}
        for cat in COUNTING:
            m, sd = stats[cat]
            z[cat] = (r[cat] - m) / sd
        m, sd = stats["fg_imp"]
        z["fgp"] = (r["fg_imp"] - m) / sd
        m, sd = stats["ft_imp"]
        z["ftp"] = (r["ft_imp"] - m) / sd
        m, sd = stats["tov"]
        z["tov"] = -((r["tov"] - m) / sd)
        out[r["name"]] = z
    return out


def total(z):
    return sum(z.values())


def main():
    # Provenance gate (PROMPT.md §0.6): refuse to build a board whose team
    # labels lack a matching, sourced row in roster-provenance.csv. The 39
    # stale teams shipped on 2026-07-12 entered through exactly this gap
    # (postmortem-2026-07-13-roster-audit.md). --allow-stale skips the hard
    # stop but stamps the defect into the board header.
    problems, newest, oldest = check_provenance()
    if problems and "--allow-stale" not in sys.argv:
        print(f"PROVENANCE GATE: FAIL ({len(problems)} problem(s)) — board not generated")
        for p in problems:
            print(" -", p)
        print("Fix roster-provenance.csv (or rerun with --allow-stale to "
              "generate a board stamped as unverified).")
        sys.exit(1)
    if oldest is None:
        verification_note = "**TEAM LABELS UNVERIFIED — no provenance dates.**"
    elif problems:
        verification_note = (f"**TEAM LABELS UNVERIFIED — generated with "
                             f"--allow-stale over {len(problems)} provenance "
                             f"problem(s). Do not draft off this board.**")
    else:
        span = oldest.isoformat() if oldest == newest else f"{oldest} – {newest}"
        verification_note = (f"Team labels verified against sourced provenance "
                             f"(`roster-provenance.csv`), verification dated {span}.")

    rows = load(os.path.join(HERE, "projections-2026-27.csv"))

    # Pass 1: pool = everyone; Pass 2: pool = top 180 by pass-1 value (per spec §4.2)
    z1 = zscores(rows, rows)
    ranked1 = sorted(rows, key=lambda r: -total(z1[r["name"]]))
    pool = ranked1[:POOL_SIZE]
    z2 = zscores(rows, pool)

    for r in rows:
        z = z2[r["name"]]
        r["z_total"] = total(z)
        av = avail(r["gp"])
        r["z_adj"] = r["z_total"] * av if r["z_total"] > 0 else r["z_total"]
        # punt fits: rank shift if a category's z is dropped from everyone's sum
        r["punt_totals"] = {p: r["z_total"] - z[p] for p in PUNTS}

    board = sorted(rows, key=lambda r: -r["z_adj"])[:200]

    # punt best/worst by rank improvement under each punt
    for p in PUNTS:
        order = sorted(rows, key=lambda r: -(r["punt_totals"][p] * avail(r["gp"])
                                             if r["punt_totals"][p] > 0
                                             else r["punt_totals"][p]))
        pr = {r["name"]: i for i, r in enumerate(order)}
        base = {r["name"]: i for i, r in enumerate(sorted(rows, key=lambda r: -r["z_adj"]))}
        for r in rows:
            r.setdefault("punt_shift", {})[p] = base[r["name"]] - pr[r["name"]]

    label = {"fgp": "FG%", "ftp": "FT%", "tpm": "3PM", "pts": "PTS", "ast": "AST", "tov": "TOV"}
    tiers = [(3, 1), (12, 2), (24, 3), (40, 4), (60, 5), (85, 6), (115, 7), (150, 8), (200, 9)]

    def tier(rank):
        return next(t for cut, t in tiers if rank <= cut)

    lines = [
        "# 2026-27 Top 200 — 9-Cat Big Board (baseline edition)",
        "",
        f"*Generated {date.today().isoformat()} by `rank_engine.py` from "
        "`projections-2026-27.csv`. Method: PROMPT.md §4.2 — per-game z-scores over an "
        "iterated top-180 pool, FG%/FT% impact-weighted by volume, TOV negative, ranked "
        "by availability-adjusted value: z-total × (GP/82 + (1−GP/82)×0.20) — the "
        "streaming-credit availability model; negatives never shrunk by absence. "
        "Punt column: build where the "
        "player gains the most ranks / loses the most.*",
        "",
        "**Basis and caveats (read before drafting off this):**",
        "",
        "- Projections are the analyst's own per-player estimates (2025-26 statistical",
        "  profiles + offseason ledger + age curve — see `baseline-2026-07.md`), not",
        "  scraped rankings. Consensus boards were consulted only as a sanity reference.",
        f"- {verification_note}",
        "- **This is a balanced board.** Where it diverges from market ADP, that is the",
        "  method speaking, not a bug: STL-scarce profiles rank high (Dyson Daniels'",
        "  steals are worth more z than the market pays), and FT%-broken stars rank low",
        "  (Giannis is a top-8 pick *inside punt-FT%* — see his punt column — and priced",
        "  here for the build-agnostic drafter).",
        "- **Unsigned free agents without a team are excluded.** Russell Westbrook",
        "  announced his retirement 2026-08-12 after 18 seasons and is out of the",
        "  pool for good. LeBron James was added 2026-07-24 after signing with PHI;",
        "  Draymond Green (GSW, agreed 7/28) and Jeremy Sochan (POR, non-guaranteed",
        "  camp deal ~8/1) were relabeled to teams in the 2026-08-13 pull.",
        "  **James Harden LEFT the FA block on 2026-08-20**, agreeing to a",
        "  three-year / $97M deal to stay in Cleveland with a 2028-29 player",
        "  option and a trade kicker; he is relabeled CLE and his line is",
        "  unchanged because it was already priced as a Cavalier. (Note for",
        "  the record: the 8/20 reporting this board relayed as \u201cat most two",
        "  guaranteed years\u201d was wrong \u2014 the deal is three years.) The FOUR",
        "  rows still labeled FA \u2014 DeRozan, Kuminga, Cam Thomas, Jaden Ivey",
        "  \u2014 were re-verified unsigned 2026-08-21. Ivey's status rests on a",
        "  contract tracker plus the absence of any reported signing, not on",
        "  a dated news item; treat it as the weakest label on the board.",
        "  **DeMar DeRozan left the FA block later the same day**, agreeing to",
        "  one year / $3.9M with Denver (reported 2026-08-21, after that",
        "  morning's pull). He is relabeled DEN and repriced DOWN to a bench-",
        "  veteran line: minimum-scale money at 37, behind Jokic and Murray.",
        "  THREE rows remain FA \u2014 Kuminga, Cam Thomas, Jaden Ivey.",
        "- Kawhi Leonard carries a 35-GP projection while his Toronto trade sits in",
        "  league-investigation limbo. On 2026-08-17 ESPN reported the probe found",
        "  no evidence that Clippers ownership funneled money to him, the league",
        "  publicly disputed that report, and the inquiry narrowed to whether the",
        "  team's sponsor introductions themselves broke the rules. The trade is",
        "  still on hold, he is still a Clipper, and a mid-September Board of",
        "  Governors meeting is the next checkpoint; his row is a placeholder.",
        "- **Four carried pool gaps closed 2026-08-21.** Peyton Watson (CLE),",
        "  Deandre Ayton (WAS), Cedric Coward (MEM) and Al Horford (GSW) were",
        "  draftable names missing from this pool since 7/27. The blocker was",
        "  never judgment \u2014 DATA-PULL \u00a73 requires base rates from a stats",
        "  source fetched during the run, and Basketball-Reference had been",
        "  egress-blocked for four straight pulls. The owner's 2026-08-21",
        "  network change opened it; the four rows are built from B-Ref",
        "  2025-26 per-game lines fetched this run, scaled for role and age,",
        "  and are [ESTIMATED]. Each was cross-checked against two external",
        "  projection feeds (report/market/). D'Angelo Russell stays OUT: his",
        "  2026-27 team is contested across sources this run, and a contested",
        "  team label is exactly what this board refuses to ship.",
        "- **Availability model changed 2026-07-27**: missed games are partly",
        "  replaceable in weekly H2H, so the GP discount carries a 0.20 streaming",
        "  credit (anchored to the deck plane's arena-calibrated 0.78 risk law),",
        "  and negative per-game values are never shrunk by absence. Injury-",
        "  discounted stars rise a tier (Kawhi, Embiid); rehab-season rows fall",
        "  to the tail where they belong. Derivation and full diff:",
        "  report/method-change-2026-07-27-availability.md.",
        "- October's job: update rows in the CSV as news lands, re-run this script,",
        "  and the board regenerates. Do not hand-edit the table below.",
        "",
        "| # | Player | Tm | Pos | GP | Line (pts/reb/ast/stl/blk/3pm) | FG%/FT% | zPG | zAdj | Tier | Punt +/− |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(board, 1):
        best = max(PUNTS, key=lambda p: r["punt_shift"][p])
        worst = min(PUNTS, key=lambda p: r["punt_shift"][p])
        line = (f"{r['pts']:.1f}/{r['reb']:.1f}/{r['ast']:.1f}/"
                f"{r['stl']:.1f}/{r['blk']:.1f}/{r['tpm']:.1f}")
        pct = f"{r['fgp']:.3f}/{r['ftp']:.3f}"
        lines.append(
            f"| {i} | {r['name']} | {r['team']} | {r['pos']} | {int(r['gp'])} | {line} | {pct} "
            f"| {r['z_total']:+.2f} | {r['z_adj']:+.2f} | {tier(i)} "
            f"| +{label[best]} / −{label[worst]} |"
        )

    out = os.path.join(HERE, "top-200-2026-27.md")
    with open(out, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {out}: {len(board)} players from {len(rows)} projected")
    print("top 12:", ", ".join(r["name"] for r in board[:12]))


if __name__ == "__main__":
    main()
