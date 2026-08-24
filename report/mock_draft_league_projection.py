#!/usr/bin/env python3
"""League projection for the 2026-08-24 live Yahoo mock draft (David = slot 4).

Reads the reconstructed draft (mock-draft-2026-08-24-results.csv) and the kit pool,
values every rostered player with the committed 9-cat engine (rank_engine.py over
projections-2026-27.csv), and writes mock-draft-2026-08-24-analysis.md:
  - power ranking (round-robin matchup record, category wins, summed availability-adjusted z)
  - a 12x9 category-rank matrix (who wins each category)
  - David's category profile, the punt reality, and his head-to-head vs each opponent.

Method notes (stated in the report too): team category totals sum each roster's full
per-game lines (all 13 picks — depth counts); FG%/FT% are volume-weighted (Σmakes/Σatt);
TOV is lower-is-better. The power ranking's Σz uses availability-adjusted value; the
category matrix uses raw per-game production. Projections are the kit's own; 14 deep
players carry [ESTIMATED] Hashtag-sourced lines (see the board header).

Usage: python3 report/mock_draft_league_projection.py
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "market"))
import rank_engine as RE  # noqa: E402
import build_market as bm  # noqa: E402 (reuse norm + aliases)

norm = bm.norm
ALIAS = {norm(v): norm(k) for k, vs in bm.ALIASES.items() for v in vs}
def canon(n): return ALIAS.get(n, n)

CNT = ["pts", "reb", "ast", "stl", "blk", "tpm"]
CATS = ["pts", "reb", "ast", "stl", "blk", "tpm", "fgp", "ftp", "tov"]  # tov: lower better
LAB = {"pts": "PTS", "reb": "REB", "ast": "AST", "stl": "STL", "blk": "BLK",
       "tpm": "3PM", "fgp": "FG%", "ftp": "FT%", "tov": "TOV"}


def player_values():
    rows = RE.load(os.path.join(HERE, "projections-2026-27.csv"))
    z1 = RE.zscores(rows, rows)
    pool = sorted(rows, key=lambda r: -RE.total(z1[r["name"]]))[:RE.POOL_SIZE]
    z2 = RE.zscores(rows, pool)
    P = {}
    for r in rows:
        zt = RE.total(z2[r["name"]])
        av = RE.avail(r["gp"])
        P[canon(norm(r["name"]))] = {"row": r, "z_adj": zt * av if zt > 0 else zt}
    return P


def team_cats(keys, P):
    fgm = fga = ftm = fta = tov = zsum = 0.0
    tot = {c: 0.0 for c in CNT}
    for k in keys:
        p = P.get(k)
        if not p:
            continue
        r = p["row"]
        zsum += p["z_adj"]
        for c in CNT:
            tot[c] += float(r[c])
        tov += float(r["tov"])
        fga += float(r["fga"]); fta += float(r["fta"])
        fgm += float(r["fgp"]) * float(r["fga"]); ftm += float(r["ftp"]) * float(r["fta"])
    out = dict(tot)
    out.update({"tov": tov, "fgp": fgm / fga if fga else 0, "ftp": ftm / fta if fta else 0,
                "zsum": zsum})
    return out


def main():
    P = player_values()
    drafted = list(csv.DictReader(open(os.path.join(HERE, "mock-draft-2026-08-24-results.csv"))))
    TEAMS, SLOT = {}, {}
    for d in drafted:
        TEAMS.setdefault(d["drafted_by"], []).append(canon(norm(d["player"])))
        SLOT[d["drafted_by"]] = int(d["slot"])
    teams = sorted(TEAMS)
    TC = {t: team_cats(TEAMS[t], P) for t in teams}

    def better(a, b, c):
        return (TC[a][c] < TC[b][c]) if c == "tov" else (TC[a][c] > TC[b][c])

    rank = {c: {t: i + 1 for i, t in enumerate(
        sorted(teams, key=lambda t: TC[t][c], reverse=(c != "tov")))} for c in CATS}

    rec = {t: [0, 0, 0] for t in teams}
    catwins = {t: 0 for t in teams}
    h2h = {t: {} for t in teams}
    for i, a in enumerate(teams):
        for b in teams[i + 1:]:
            wa = sum(1 for c in CATS if better(a, b, c))
            wb = sum(1 for c in CATS if better(b, a, c))
            catwins[a] += wa; catwins[b] += wb
            h2h[a][b] = wa; h2h[b][a] = wb
            if wa > wb:
                rec[a][0] += 1; rec[b][1] += 1
            elif wb > wa:
                rec[b][0] += 1; rec[a][1] += 1
            else:
                rec[a][2] += 1; rec[b][2] += 1

    standings = sorted(teams, key=lambda t: (rec[t][0], catwins[t], TC[t]["zsum"]), reverse=True)

    L = ["# Live mock-draft league projection — 2026-08-24", "",
         "12-team, 9-cat H2H. **David = slot 4.** Every rostered player valued with the committed "
         "engine (`rank_engine.py` over `projections-2026-27.csv`, pool now complete at 234). "
         "Round-robin: each pair compared across all 9 categories; a matchup is won by taking 5+. "
         "Team category totals sum each roster's full per-game lines (depth counts); FG%/FT% are "
         "volume-weighted; TOV is lower-is-better. Power ranking's Σz is availability-adjusted "
         "value. Projections are the kit's own (14 deep players carry [ESTIMATED] lines).", "",
         "## Power ranking", "",
         "| # | Manager | slot | matchups (W-L-T) | cat wins | Σ z-adj |",
         "|---|---|---|---|---|---|"]
    for i, t in enumerate(standings, 1):
        w, l, tt = rec[t]
        me = " **← YOU**" if t == "David" else ""
        L.append(f"| {i} | {t}{me} | {SLOT[t]} | {w}-{l}-{tt} | {catwins[t]} | {TC[t]['zsum']:+.1f} |")

    L += ["", "## Category-rank matrix (1 = best of 12)", "",
          "| Manager | " + " | ".join(LAB[c] for c in CATS) + " |",
          "|" + "---|" * (len(CATS) + 1)]
    for t in standings:
        cells = " | ".join(str(rank[c][t]) for c in CATS)
        me = " **←**" if t == "David" else ""
        L.append(f"| {t}{me} | {cells} |")

    d = TC["David"]
    strong = [LAB[c] for c in CATS if rank[c]["David"] <= 4]
    weak = [LAB[c] for c in CATS if rank[c]["David"] >= 9]
    L += ["", "## David's team (slot 4)", "",
          f"**Projected finish: #{standings.index('David') + 1} of 12.**  "
          f"Strengths (top-4): {', '.join(strong)}.  Weaknesses (bottom-4): {', '.join(weak)}.", "",
          "| Category | league rank | team per-game total |", "|---|---|---|"]
    for c in CATS:
        val = f"{d[c]:.3f}" if c in ("fgp", "ftp") else f"{d[c]:.1f}"
        L.append(f"| {LAB[c]} | {rank[c]['David']}/12 | {val} |")

    L += ["", "### Head-to-head vs each opponent", "",
          "| Opponent | cats W-L | result | categories David wins |", "|---|---|---|---|"]
    for b in [t for t in standings if t != "David"]:
        wa = h2h["David"][b]
        res = "**W**" if wa >= 5 else "L"
        won = ",".join(LAB[c] for c in CATS if better("David", b, c))
        L.append(f"| {b} | {wa}-{9 - wa} | {res} | {won} |")

    out = os.path.join(HERE, "mock-draft-2026-08-24-analysis.md")
    open(out, "w").write("\n".join(L) + "\n")
    print("wrote", out)
    print(f"David finish: #{standings.index('David') + 1}; record {rec['David']}; "
          f"strong {strong}; weak {weak}")


if __name__ == "__main__":
    main()
