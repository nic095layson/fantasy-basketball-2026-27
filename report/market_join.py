#!/usr/bin/env python3
"""Pass E market join + §5.3 arbitrage table.

Joins report/market/*.csv (external consensus feeds) to the 220-row pool and
writes market-2026-27.md: the ADP table PROMPT.md Pass E asks for, and the
values/fades arbitrage §5.3 defines.

WHAT THIS IS NOT: a blend. Owner decision 2026-08-21 (report/market-workorder.md
§1) is that these feeds are a sanity check and an arbitrage input, not an input
to the projections. The board stays built from first principles — its own header
says it is built from profiles/ledger/age-curve, "not scraped rankings." This
script therefore NEVER writes projections-2026-27.csv.

Both feeds are re-ranked with THIS repo's engine before any ordering is
compared, because their native ranks are not comparable: Hashtag ranks on its
own 9-cat z-sum, statdunk on points-league fantasy points.

HARD GATE (work order §3.3): a silent partial join is a defect. Any feed player
inside the top 150 that does not match a pool row is reported, and an ambiguous
name collision aborts with exit 2 rather than guessing.
"""
import csv
import os
import re
import sys
import unicodedata
from collections import defaultdict
from datetime import date

from rank_engine import avail, total, zscores

HERE = os.path.dirname(os.path.abspath(__file__))
MARKET = os.path.join(HERE, "market")
NUM = ["gp", "mpg", "fg_pct", "fga", "ft_pct", "fta", "tpm", "pts", "reb",
       "ast", "stl", "blk", "tov"]
KIT_MAP = {"fgp": "fg_pct", "ftp": "ft_pct"}
POOL_SIZE = 180
ARB = 15          # §5.3 threshold: 15+ picks
TOP_UNMATCHED = 150

# Confirmed nickname/full-name variants between the feeds and this pool.
# Found by the unmatched gate on 2026-08-21, each verified by surname+team
# before being added. Never add one without that check — a wrong alias merges
# two different players and is worse than an unmatched row.
NAME_ALIAS = {
    "cameron johnson": "cam johnson",     # feeds full, pool short
    "alexandre sarr": "alex sarr",
    "herbert jones": "herb jones",
    "nicolas claxton": "nic claxton",
}

TEAM_ALIAS = {"SA": "SAS", "NY": "NYK", "PHO": "PHX", "GS": "GSW", "NO": "NOP",
              "UTAH": "UTA", "WSH": "WAS", "BKN": "BRK", "CHO": "CHA"}


def team_norm(t):
    t = (t or "").strip().upper()
    return TEAM_ALIAS.get(t, t)


def norm(name):
    """Accent/punctuation-insensitive key. Mirrors hoops.norm()'s intent."""
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    s = s.lower().replace(".", "").replace("'", "").replace("-", " ")
    s = re.sub(r"\b(jr|sr|ii|iii|iv)\b", " ", s)
    s = " ".join(s.split())
    return NAME_ALIAS.get(s, s)


def load(path, rename=None):
    rows = []
    with open(path) as f:
        for r in csv.DictReader(f):
            if rename:
                for a, b in rename.items():
                    if a in r:
                        r[b] = r[a]
            name = (r.get("player") or r.get("name") or "").strip()
            if not name:
                continue
            try:
                d = {k: float(r[k]) for k in NUM}
            except (KeyError, ValueError):
                continue
            if d["gp"] <= 0 or d["fga"] <= 0:
                continue
            d.update(name=name, key=norm(name), team=team_norm(r.get("team")),
                     adp=r.get("adp"), raw=r)
            rows.append(d)
    return rows


def collide(rows, label):
    """Abort on an ambiguous key — never guess which player a row means."""
    seen = defaultdict(set)
    for r in rows:
        seen[r["key"]].add(r["name"])
    bad = {k: v for k, v in seen.items() if len(v) > 1}
    if bad:
        print("JOIN GATE: FAIL — ambiguous names in %s:" % label, file=sys.stderr)
        for k, v in bad.items():
            print("  %s -> %s" % (k, sorted(v)), file=sys.stderr)
        sys.exit(2)


def board(rows):
    """Rank with this repo's engine so all three are comparable."""
    for r in rows:
        r["fgp"], r["ftp"] = r["fg_pct"], r["ft_pct"]
    z1 = zscores(rows, rows)
    pool = sorted(rows, key=lambda r: -total(z1[r["name"]]))[:POOL_SIZE]
    z2 = zscores(rows, pool)
    for r in rows:
        r["_v"] = total(z2[r["name"]]) * avail(r["gp"])
    ranked = sorted(rows, key=lambda r: -r["_v"])
    return {r["key"]: i + 1 for i, r in enumerate(ranked)}


def main():
    kit = load(os.path.join(HERE, "projections-2026-27.csv"),
               rename={"fgp": "fg_pct", "ftp": "ft_pct"})
    ht = load(os.path.join(MARKET, "hashtag-2026-08-21.csv"))
    sd = load(os.path.join(MARKET, "statdunk-2026-08-21.csv"))
    for rows, label in ((kit, "pool"), (ht, "hashtag"), (sd, "statdunk")):
        collide(rows, label)

    bk, bh, bs = board(kit), board(ht), board(sd)
    kit_by_key = {r["key"]: r for r in kit}
    ht_by_key = {r["key"]: r for r in ht}
    sd_by_key = {r["key"]: r for r in sd}

    # ---- hard gate: unmatched feed players inside the top 150 ------------
    unmatched = []
    for by_key, ranks, label in ((ht_by_key, bh, "hashtag"),
                                 (sd_by_key, bs, "statdunk")):
        for key, r in by_key.items():
            if key not in kit_by_key and ranks[key] <= TOP_UNMATCHED:
                unmatched.append((ranks[key], r["name"], r["team"], label))
    unmatched.sort()

    # Near-miss detector. An unmatched feed player who shares a surname AND a
    # team with a pool row is almost certainly the same person under a
    # different first-name form. These are REPORTED for confirmation, never
    # auto-joined: a wrong merge is worse than a missing row.
    pool_by_surteam = defaultdict(list)
    for r in kit:
        parts = r["key"].split()
        if parts:
            pool_by_surteam[(parts[-1], r["team"])].append(r["name"])
    near = []
    for rank, name, team, label in unmatched:
        parts = norm(name).split()
        if not parts:
            continue
        hit = pool_by_surteam.get((parts[-1], team))
        if hit:
            near.append((name, team, label, hit))

    # ---- Pass E: ADP joined to the pool ----------------------------------
    joined = []
    for key, r in kit_by_key.items():
        adp = ht_by_key.get(key, {}).get("adp")
        try:
            adp = float(adp)
        except (TypeError, ValueError):
            adp = None
        joined.append(dict(name=r["name"], team=r["team"], kit=bk[key],
                           ht=bh.get(key), sd=bs.get(key), adp=adp))
    joined.sort(key=lambda d: d["kit"])
    with_adp = [d for d in joined if d["adp"] is not None]

    values = sorted((d for d in with_adp if d["adp"] - d["kit"] >= ARB),
                    key=lambda d: -(d["adp"] - d["kit"]))
    fades = sorted((d for d in with_adp if d["kit"] - d["adp"] >= ARB),
                   key=lambda d: -(d["kit"] - d["adp"]))

    # ---- line-level disagreement vs each feed ----------------------------
    def line_gaps(feed_by_key, label):
        out = []
        for key, r in kit_by_key.items():
            f = feed_by_key.get(key)
            if not f:
                continue
            dp, dg = f["pts"] - r["pts"], f["gp"] - r["gp"]
            out.append((abs(dp) / max(r["pts"], 1) + abs(dg) / 82.0,
                        r["name"], r["pts"], f["pts"], r["gp"], f["gp"], label))
        out.sort(reverse=True)
        return out

    ht_gaps = line_gaps(ht_by_key, "hashtag")
    sd_gaps = line_gaps(sd_by_key, "statdunk")

    conflicts = [(r["name"], r["team"], lbl, f[r["key"]]["team"])
                 for r in kit for lbl, f in (("hashtag", ht_by_key), ("statdunk", sd_by_key))
                 if r["key"] in f and f[r["key"]]["team"] and r["team"] != "FA"
                 and f[r["key"]]["team"] != r["team"]]

    def arb_tbl(rs):
        o = ["| Player | Tm | our rank | ADP | edge |", "|---|---|---:|---:|---:|"]
        for d in rs[:25]:
            o.append("| %s | %s | %d | %.1f | %+.0f |"
                     % (d["name"], d["team"], d["kit"], d["adp"], d["adp"] - d["kit"]))
        return "\n".join(o)

    def gap_tbl(gs):
        o = ["| Player | our pts | feed pts | our GP | feed GP |",
             "|---|---:|---:|---:|---:|"]
        for _, n, kp, fp, kg, fg in [g[:6] for g in gs[:15]]:
            o.append("| %s | %.1f | %.1f | %.0f | %.0f |" % (n, kp, fp, kg, fg))
        return "\n".join(o)

    md = """# Pass E — market join and §5.3 arbitrage — %s

*Generated by `market_join.py` from `report/market/`. **Not a draft board and
not a blend.** Owner decision 2026-08-21: these feeds are a sanity check and an
arbitrage input; the board stays built from first principles. Nothing here
writes `projections-2026-27.csv`.*

**Method.** Both feeds are re-ranked with this repo's own engine before any
ordering is compared — their published ranks are not comparable to each other
(Hashtag ranks on a 9-cat z-sum, statdunk on points-league fantasy points).
ADP comes from Hashtag, the aggregator PROMPT.md Pass E already names.

**Coverage.** pool %d · hashtag %d · statdunk %d · %d pool rows carry an ADP.

**Join gate.** No ambiguous names in any source. %d feed players ranked inside
the top %d are absent from the pool (listed at the bottom) — reported, not
silently dropped.

## §5.3 Values — we are 15+ picks higher than the market

The market is letting these fall. Each still needs its one-sentence mechanism
before it is actionable; that adjudication is the owner's, per the work order.

%s

## §5.3 Fades — the market is 15+ picks higher than us

%s

## Biggest per-game line disagreements vs Hashtag

%s

## Biggest per-game line disagreements vs statdunk

Note statdunk's GP is an expected-games figure with injury risk priced in —
the same meaning as this repo's `gp` column — so a GP gap here is a real
disagreement about availability, not a units mismatch. Hashtag's GP is a
rounder healthy-baseline number and its gaps read high by construction.

%s

## Team-label disagreements (%d)

A feed disagreeing about a player's team is a roster-verification signal and
outranks any valuation question.

%s

## Probable alias misses needing confirmation (%d)

Unmatched feed players who share a surname AND a team with a pool row. Almost
certainly the same person under a different first-name form. Reported, never
auto-joined — confirm, then add to `NAME_ALIAS` in `market_join.py`.

%s

## Ranked top-%d by a feed, absent from the pool (%d)

Pool-completeness candidates. Presence here is not sufficient reason to add a
row: DATA-PULL.md §3 still requires a sourced team placement and base rates
fetched during the run.

| feed rank | Player | Tm | source |
|---:|---|---|---|
%s
""" % (date.today().isoformat(), len(kit), len(ht), len(sd), len(with_adp),
       len(unmatched), TOP_UNMATCHED,
       arb_tbl(values), arb_tbl(fades), gap_tbl(ht_gaps), gap_tbl(sd_gaps),
       len(conflicts),
       "\n".join("- **%s** — pool says `%s`, %s says `%s`" % c for c in conflicts) or "- none",
       len(near),
       "\n".join("- **%s** (%s, %s) \u2248 pool row `%s`" % (n, t, l, "`, `".join(h))
                 for n, t, l, h in near) or "- none",
       TOP_UNMATCHED, len(unmatched),
       "\n".join("| %d | %s | %s | %s |" % u for u in unmatched[:30]))

    out = os.path.join(HERE, "market-2026-27.md")
    with open(out, "w") as f:
        f.write(md)
    print("wrote", out)
    print("  join gate: PASS (no ambiguous names) · %d unmatched in top %d"
          % (len(unmatched), TOP_UNMATCHED))
    print("  %d pool rows carry ADP · %d values · %d fades"
          % (len(with_adp), len(values), len(fades)))
    print("  team conflicts:", len(conflicts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
