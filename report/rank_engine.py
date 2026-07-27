#!/usr/bin/env python3
"""9-cat z-score ranking engine — implements PROMPT.md §4.2.

Reads projections-2026-27.csv (per-game projections + GP), computes impact-weighted
z-scores over an iterated top-180 draft pool, availability-adjusts by GP/82, and
writes top-200-2026-27.md. Update the CSV, re-run, done.
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
        r["z_adj"] = r["z_total"] * (r["gp"] / 82.0)
        # punt fits: rank shift if a category's z is dropped from everyone's sum
        r["punt_totals"] = {p: r["z_total"] - z[p] for p in PUNTS}

    board = sorted(rows, key=lambda r: -r["z_adj"])[:200]

    # punt best/worst by rank improvement under each punt
    for p in PUNTS:
        order = sorted(rows, key=lambda r: -(r["punt_totals"][p] * r["gp"] / 82.0))
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
        "by availability-adjusted value (z-total × GP/82). Punt column: build where the "
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
        "- **Unsigned free agents without a team are excluded** (Russell Westbrook",
        "  remains one as of 2026-07-27). LeBron James was added 2026-07-24 after",
        "  signing with PHI. Rows still labeled FA (James Harden, DeRozan, Draymond",
        "  Green, Kuminga \u2014 now just outside the top 200 \u2014 Cam Thomas, Ivey,",
        "  Sochan) were re-verified unsigned",
        "  2026-07-16..27; Harden relabeled FA 2026-07-27 (option declined 6/29,",
        "  CLE re-sign framework agreed but unsigned — consistent FA treatment).",
        "- Kawhi Leonard carries a 35-GP projection while his Toronto trade sits in",
        "  league-investigation limbo (probe fact-finding done, NBA reviewing as of",
        "  2026-07-24; suspension/void scenarios still live); his row is a placeholder.",
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
