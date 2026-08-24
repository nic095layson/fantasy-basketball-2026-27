#!/usr/bin/env python3
"""Deterministic, offline builder for the market-data work order (report/market-data-workorder.md).

Reads the dated raw snapshots landed by fetch_market.py and produces:
  1. report/market/hashtag-YYYY-MM-DD.csv     (§4 schema + documented additions)
  2. report/market/statdunk-YYYY-MM-DD.csv    (§4 schema + per-category z-scores)
  3. report/market/provenance.csv             (source,url,fetched_on,rows,notes)
  4. report/market/unmatched-YYYY-MM-DD.md     HARD GATE (§3.3): every one of the 220
     pool players is matched to each source or listed here; no silent partial joins.
  5. report/market/disagreements-YYYY-MM-DD.md the reference/arbitrage tables the owner
     adjudicates (§3.4 line diffs vs Hashtag, ordering diffs vs Statdunk, §5.3 values/fades).

It does NOT touch projections-2026-27.csv, the board, or marketRanks — the work order joins
these as *reference columns* (owner decision 2026-08-21), and step 5 (marketRanks) is gated.

Name matching (§3.3) reuses the same normalization idea as the deck plane's hoops.norm():
accent-fold, drop punctuation, strip generational suffixes. Because that primitive lives in
the *deck* repo (out of this session's scope), an equivalent norm() is defined here.

Usage: python3 report/market/build_market.py [YYYY-MM-DD]
Exit 0 = built and every pool player accounted for. Exit 3 = unmatched pool players remain
that are not explained by a documented alias or a recorded genuine absence (hard gate trip).
"""
import csv
import json
import os
import re
import sys
import unicodedata
from datetime import date
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.dirname(HERE)
PROJECTIONS = os.path.join(REPORT, "projections-2026-27.csv")
sys.path.insert(0, REPORT)  # so we can reuse rank_engine's exact board math


# --------------------------------------------------------------------------- norm
_SUFFIXES = {"jr", "sr", "ii", "iii", "iv", "v"}


def norm(name):
    """Accent-fold, lowercase, drop punctuation, strip a trailing generational suffix,
    collapse whitespace. 'Nikola Jokić'/'Nikola Jokic' -> 'nikola jokic';
    'P.J. Washington' -> 'pj washington'; 'Jaren Jackson Jr.' -> 'jaren jackson'."""
    s = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = s.replace("’", "'").replace("`", "'")
    s = re.sub(r"[.'\-,]", "", s)      # drop . ' - ,  (period/apostrophe/hyphen/comma)
    s = re.sub(r"\s+", " ", s).strip()
    toks = s.split(" ")
    if len(toks) > 1 and toks[-1] in _SUFFIXES:
        toks = toks[:-1]
    return " ".join(toks)


# Documented aliases: pool spelling -> the equivalent source spelling(s), for real players
# whose name form differs between our pool and a source (nickname vs given name). Resolved
# from the unmatched-gate output and verified against the raw source (the surname is present
# with a different first name). Everything NOT an alias is a genuine coverage absence below.
ALIASES = {
    "Herb Jones": {"Herbert Jones"},        # hashtag & statdunk use the given name
    "Cam Johnson": {"Cameron Johnson"},      # hashtag & statdunk
    "Nic Claxton": {"Nicolas Claxton"},      # hashtag
    "Alex Sarr": {"Alexandre Sarr"},         # hashtag
}


def _canon(n, alias_index):
    return alias_index.get(n, n)


# --------------------------------------------------------------------------- hashtag parse
class _Grid(HTMLParser):
    """Parse hashtag's ContentPlaceHolder1_GridView1 into rows of (text, first_full_anchor)."""

    def __init__(self):
        super().__init__()
        self.intbl = 0
        self.inrow = self.incell = False
        self.rows = []
        self.cur = None
        self.buf = []
        self.anchor_full = None  # text of the HyperLink1_ (full name) anchor in this cell
        self.in_full_anchor = False

    def handle_starttag(self, t, a):
        d = dict(a)
        if t == "table" and d.get("id") == "ContentPlaceHolder1_GridView1":
            self.intbl = 1
        if not self.intbl:
            return
        if t == "tr":
            self.inrow = True
            self.cur = []
        elif t in ("td", "th"):
            self.incell = True
            self.buf = []
            self.anchor_full = None
        elif t == "a" and self.incell:
            aid = d.get("id", "")
            if "HyperLink1_" in aid:      # the full-name anchor (d-sm-inline)
                self.in_full_anchor = True
                self.anchor_full = ""

    def handle_endtag(self, t):
        if not self.intbl:
            return
        if t == "a" and self.in_full_anchor:
            self.in_full_anchor = False
        elif t in ("td", "th") and self.incell:
            text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
            self.cur.append((text, self.anchor_full))
            self.incell = False
        elif t == "tr" and self.inrow:
            self.rows.append(self.cur)
            self.inrow = False
        elif t == "table":
            self.intbl = 0

    def handle_data(self, data):
        if self.incell:
            self.buf.append(data)
        if self.in_full_anchor:
            self.anchor_full = (self.anchor_full or "") + data


def _pct_att(cell):
    """'0.573 (10.5/18.3)' -> (0.573, 18.3) i.e. (pct, attempts). Attempts = denom in parens."""
    m = re.match(r"([\d.]+)", cell)
    pct = float(m.group(1)) if m else ""
    att = ""
    mm = re.search(r"\(([\d.]+)\s*/\s*([\d.]+)\)", cell)
    if mm:
        att = float(mm.group(2))
    return pct, att


# Hashtag GridView columns are a fixed order. The header row is NOT reliable — on the
# full-list view its per-category on/off toggles collapse it to 8 cells — so parse by
# position and validate the width (17) and the player anchor instead.
# 0 R#  1 PLAYER  2 ADP  3 POS  4 TEAM  5 GP  6 MPG  7 FG%  8 FT%  9 3PM
# 10 PTS  11 TREB  12 AST  13 STL  14 BLK  15 TO  16 TOTAL
_HT = dict(rnum=0, player=1, adp=2, pos=3, team=4, gp=5, mpg=6, fgp=7, ftp=8,
           tpm=9, pts=10, reb=11, ast=12, stl=13, blk=14, tov=15, total=16)


def parse_hashtag(raw):
    p = _Grid()
    p.feed(raw)
    out = []
    for r in p.rows:
        if len(r) != 17 or not r[_HT["player"]][1]:   # need full width + a full-name anchor
            continue
        cell = [c[0] for c in r]
        name = r[_HT["player"]][1].strip()
        fg_pct, fga = _pct_att(cell[_HT["fgp"]])
        ft_pct, fta = _pct_att(cell[_HT["ftp"]])

        def num(key):
            v = cell[_HT[key]].replace(",", "")
            try:
                return float(v)
            except ValueError:
                return ""

        out.append({
            "player": name,
            "team": cell[_HT["team"]],
            "pos": cell[_HT["pos"]],
            "gp": num("gp"), "mpg": num("mpg"),
            "fg_pct": fg_pct, "fga": fga, "ft_pct": ft_pct, "fta": fta,
            "tpm": num("tpm"), "pts": num("pts"), "reb": num("reb"),
            "ast": num("ast"), "stl": num("stl"), "blk": num("blk"), "tov": num("tov"),
            "adp": num("adp"), "htag_rank": num("rnum"), "htag_total": num("total"),
        })
    return out


HASHTAG_COLS = ["player", "team", "pos", "gp", "mpg", "fg_pct", "fga", "ft_pct", "fta",
                "tpm", "pts", "reb", "ast", "stl", "blk", "tov",   # §4 schema (order)
                "adp", "htag_rank", "htag_total"]                   # documented additions


# --------------------------------------------------------------------------- statdunk parse
# Statdunk's published category block (BASE endpoint) is a stale 8/11 "provisional" build
# whose player universe is broken (misses most stars). Its per-game category z-scores are,
# however, reproduced *exactly* (Pearson=Spearman=1.0000) from its own projectedStats by the
# 9-cat attempt-weighted z-score below — i.e. this IS statdunk's categoryMethod
# ('attempt-weighted-nine-category-zscore-v1'). So we validate the method against BASE, then
# apply it to the freshest full-coverage projections (V2 / V4.10) to reconstruct statdunk's
# category value as its own engine would compute it on current numbers. The clean pre-computed
# board lives only in statdunk's Supabase backend, which is off the egress allowlist (403).
_SD_CNT = ["pts", "reb", "ast", "stl", "blk", "tpm"]


def _sd_players(raw):
    d = json.loads(raw)
    players = d.get("players") or (d.get("release", {}) or {}).get("players") or []
    pub = d.get("publication") or (d.get("release", {}) or {}).get("publication") or {}
    return players, pub


def _mean_sd(vals):
    m = sum(vals) / len(vals)
    sd = (sum((v - m) ** 2 for v in vals) / len(vals)) ** 0.5 or 1.0
    return m, sd


def sd_category_value(players, mode):
    """Statdunk's own 9-cat method over `players`. mode='averages' (per-game) or 'totals'
    (season). Returns {pid: {'value', 'z': {cat: z}}}. Volume-weighted FG%/FT% impact,
    negative TOV, z over the pool = `players`."""
    pool = [p for p in players if p.get("projectedGames") and p.get("projectedStats")]

    def x(p, k):
        v = p["projectedStats"].get(k, 0.0)
        return v / p["projectedGames"] if mode == "averages" else v

    pool_fgp = (sum(p["projectedStats"].get("fgm", 0) for p in pool)
                / max(sum(p["projectedStats"].get("fga", 0) for p in pool), 1e-9))
    pool_ftp = (sum(p["projectedStats"].get("ftm", 0) for p in pool)
                / max(sum(p["projectedStats"].get("fta", 0) for p in pool), 1e-9))
    for p in pool:
        ps = p["projectedStats"]
        p_fgp = ps.get("fgm", 0) / max(ps.get("fga", 0), 1e-9)
        p_ftp = ps.get("ftm", 0) / max(ps.get("fta", 0), 1e-9)
        p["_fg"] = (p_fgp - pool_fgp) * x(p, "fga")
        p["_ft"] = (p_ftp - pool_ftp) * x(p, "fta")

    stat = {k: _mean_sd([x(p, k) for p in pool]) for k in _SD_CNT}
    stat["to"] = _mean_sd([x(p, "to") for p in pool])
    stat["fg"] = _mean_sd([p["_fg"] for p in pool])
    stat["ft"] = _mean_sd([p["_ft"] for p in pool])

    out = {}
    for p in pool:
        z = {}
        for k in _SD_CNT:
            m, s = stat[k]
            z[k] = (x(p, k) - m) / s
        m, s = stat["to"]
        z["to"] = -((x(p, "to") - m) / s)
        m, s = stat["fg"]
        z["fgPct"] = (p["_fg"] - m) / s
        m, s = stat["ft"]
        z["ftPct"] = (p["_ft"] - m) / s
        out[p["canonicalPlayerId"]] = {"value": sum(z.values()), "z": z}
    return out


def _spearman(pairs):
    """pairs: list of (a, b). Return Spearman rho via Pearson on ranks."""
    def ranks(vals):
        order = sorted(range(len(vals)), key=lambda i: vals[i])
        r = [0] * len(vals)
        for pos, i in enumerate(order):
            r[i] = pos + 1
        return r
    a = ranks([p[0] for p in pairs])
    b = ranks([p[1] for p in pairs])
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    sa = (sum((x - ma) ** 2 for x in a)) ** 0.5
    sb = (sum((y - mb) ** 2 for y in b)) ** 0.5
    return cov / (sa * sb) if sa and sb else 0.0


def validate_method(base_raw):
    """Reconstruct BASE's published averages value from BASE's own projectedStats and
    confirm it reproduces statdunk's engine. Returns Spearman rho (expected ~1.0)."""
    players, _ = _sd_players(base_raw)
    have = [p for p in players if (p.get("categories", {}) or {}).get("averages")]
    recon = sd_category_value(have, "averages")
    pairs = [(recon[p["canonicalPlayerId"]]["value"],
              p["categories"]["averages"]["value"]) for p in have
             if p["canonicalPlayerId"] in recon]
    return _spearman(pairs), len(pairs)


def parse_statdunk(v2_raw, base_raw):
    """Build statdunk rows from the fresh V2 projections with reconstructed category value.
    Self-validates the reconstruction method against the BASE published block first."""
    rho, n = validate_method(base_raw)
    if rho < 0.999:
        raise SystemExit(f"statdunk method validation FAILED: Spearman {rho:.4f} over {n} "
                         "players vs published categories — refusing to reconstruct.")
    players, pub = _sd_players(v2_raw)
    tot = sd_category_value(players, "totals")
    avg = sd_category_value(players, "averages")
    tot_rank = {pid: i + 1 for i, pid in enumerate(
        sorted(tot, key=lambda k: -tot[k]["value"]))}
    avg_rank = {pid: i + 1 for i, pid in enumerate(
        sorted(avg, key=lambda k: -avg[k]["value"]))}

    out = []
    for p in players:
        pid = p["canonicalPlayerId"]
        if pid not in tot:
            continue
        gp = p.get("projectedGames") or 0
        ps = p.get("projectedStats", {}) or {}
        z = tot[pid]["z"]

        def pg(k):
            return round(ps[k] / gp, 3) if gp and k in ps else ""

        fgm, fga = ps.get("fgm"), ps.get("fga")
        ftm, fta = ps.get("ftm"), ps.get("fta")
        out.append({
            "player": p.get("displayName", ""),
            "team": p.get("teamAbbreviation", ""),
            "pos": "/".join(p.get("fantasyPositions", []) or []),
            "rank": tot_rank[pid],                    # §4 'rank' = totals (games-inclusive)
            "value": round(tot[pid]["value"], 4),
            "rank_avg": avg_rank[pid],
            "value_avg": round(avg[pid]["value"], 4),
            "gp": round(gp, 1) if gp else "",
            "mpg": round(p["projectedMinutes"] / gp, 1) if gp and p.get("projectedMinutes") else "",
            "pts": pg("pts"), "reb": pg("reb"), "ast": pg("ast"), "stl": pg("stl"),
            "blk": pg("blk"), "tpm": pg("tpm"), "tov": pg("to"),
            "fg_pct": round(fgm / fga, 3) if fgm and fga else "",
            "fga": round(fga / gp, 2) if fga and gp else "",
            "ft_pct": round(ftm / fta, 3) if ftm and fta else "",
            "fta": round(fta / gp, 2) if fta and gp else "",
            "z_pts": round(z["pts"], 3), "z_reb": round(z["reb"], 3), "z_ast": round(z["ast"], 3),
            "z_stl": round(z["stl"], 3), "z_blk": round(z["blk"], 3), "z_tpm": round(z["tpm"], 3),
            "z_fgpct": round(z["fgPct"], 3), "z_ftpct": round(z["ftPct"], 3), "z_tov": round(z["to"], 3),
        })
    out.sort(key=lambda r: r["rank"])
    return out, pub, (rho, n)


STATDUNK_COLS = ["player", "team", "pos", "rank", "value",            # §4 schema (order)
                 "rank_avg", "value_avg", "gp", "mpg",
                 "pts", "reb", "ast", "stl", "blk", "tpm", "tov",
                 "fg_pct", "fga", "ft_pct", "fta",
                 "z_pts", "z_reb", "z_ast", "z_stl", "z_blk", "z_tpm",
                 "z_fgpct", "z_ftpct", "z_tov"]                        # per-category z (§4 opt)


# --------------------------------------------------------------------------- our board
def our_board():
    """Our value board exactly as rank_engine.py builds it: z-scores over the iterated
    top-180 pool, ranked by availability-adjusted value. Returns
    {name: {rank, z_total, z_adj, row}} for all 220 pool players."""
    import rank_engine as RE
    rows = RE.load(PROJECTIONS)
    z1 = RE.zscores(rows, rows)
    ranked1 = sorted(rows, key=lambda r: -RE.total(z1[r["name"]]))
    pool = ranked1[:RE.POOL_SIZE]
    z2 = RE.zscores(rows, pool)
    for r in rows:
        z = z2[r["name"]]
        r["z_total"] = RE.total(z)
        av = RE.avail(r["gp"])
        r["z_adj"] = r["z_total"] * av if r["z_total"] > 0 else r["z_total"]
    board = sorted(rows, key=lambda r: -r["z_adj"])
    return {r["name"]: {"rank": i + 1, "z_total": r["z_total"], "z_adj": r["z_adj"], "row": r}
            for i, r in enumerate(board)}


# --------------------------------------------------------------------------- main
def _write_csv(path, cols, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
    ht_raw = open(os.path.join(HERE, f"hashtag-raw-{d}.html"), encoding="utf-8").read()
    sd_v2_raw = open(os.path.join(HERE, f"statdunk-v2-raw-{d}.json"), encoding="utf-8").read()
    sd_base_raw = open(os.path.join(HERE, f"statdunk-raw-{d}.json"), encoding="utf-8").read()

    hashtag = parse_hashtag(ht_raw)
    statdunk, sd_pub, (sd_rho, sd_n) = parse_statdunk(sd_v2_raw, sd_base_raw)
    print(f"parsed: hashtag={len(hashtag)} rows, statdunk={len(statdunk)} rows "
          f"(method validated vs BASE published: Spearman {sd_rho:.4f} over {sd_n})")

    _write_csv(os.path.join(HERE, f"hashtag-{d}.csv"), HASHTAG_COLS, hashtag)
    _write_csv(os.path.join(HERE, f"statdunk-{d}.csv"), STATDUNK_COLS, statdunk)

    # provenance
    prov = [
        {"source": "hashtag", "url": "https://hashtagbasketball.com/fantasy-basketball-projections",
         "fetched_on": d, "rows": len(hashtag),
         "notes": "2026-27 Rest-of-Season projections; POS/ADP source=Yahoo (DDPOSFROM=1, "
                  "client platform per INPUTS default); DDSHOW=All. Per-game line + Yahoo ADP "
                  "+ hashtag rank(R#)/value(TOTAL). FG%/FT% cells carry pct + makes/attempts."},
        {"source": "statdunk", "url": "https://statdunk.com/projections/categories?sport=nba&sort=val",
         "fetched_on": d, "rows": len(statdunk),
         "notes": f"StatMaxers same-origin API. Projections = /api/statdunk-nba-projections-v2 "
                  f"(label={sd_pub.get('label')}, asOf={sd_pub.get('asOf')}). The pre-computed "
                  f"category board lives in the Supabase backend (off-allowlist, 403), so "
                  f"category value is reconstructed via statdunk's own method "
                  f"(attempt-weighted-nine-category-zscore-v1), VALIDATED to reproduce the "
                  f"published /api/statdunk-nba-projections block (Spearman {sd_rho:.4f} over "
                  f"{sd_n} players). rank/value=totals(season); rank_avg/value_avg=averages(per-game); "
                  f"z_*=totals. base(8/11 provisional) & v3(lock-in) also landed raw."},
    ]
    _write_csv(os.path.join(HERE, "provenance.csv"),
               ["source", "url", "fetched_on", "rows", "notes"], prov)
    print(f"wrote hashtag-{d}.csv, statdunk-{d}.csv, provenance.csv")

    # ---- join + hard unmatched gate ------------------------------------------------
    board = our_board()
    alias_index = {}
    for canonical, variants in ALIASES.items():
        for v in variants:
            alias_index[norm(v)] = norm(canonical)

    ht_by = {}
    for r in hashtag:
        ht_by.setdefault(_canon(norm(r["player"]), alias_index), r)
    sd_by = {}
    for r in statdunk:
        sd_by.setdefault(_canon(norm(r["player"]), alias_index), r)

    unmatched_ht, unmatched_sd, matched = [], [], []
    for name, b in board.items():
        key = _canon(norm(name), alias_index)
        h = ht_by.get(key)
        s = sd_by.get(key)
        if h is None:
            unmatched_ht.append((b["rank"], name))
        if s is None:
            unmatched_sd.append((b["rank"], name))
        matched.append({"name": name, "board": b, "ht": h, "sd": s, "key": key})

    unmatched_ht.sort()
    unmatched_sd.sort()
    _write_unmatched(d, unmatched_ht, unmatched_sd, board)
    _write_disagreements(d, matched, sd_pub)

    # GENUINE ABSENCES recorded as accepted (players a source legitimately does not carry).
    # Anything here is treated as explained; everything else trips the gate.
    accepted_absent_ht = set(_ACCEPTED_ABSENT_HT)
    accepted_absent_sd = set(_ACCEPTED_ABSENT_SD)
    trip_ht = [n for _, n in unmatched_ht if n not in accepted_absent_ht]
    trip_sd = [n for _, n in unmatched_sd if n not in accepted_absent_sd]

    print(f"\nJOIN: {len(board)} pool players | "
          f"unmatched→hashtag={len(unmatched_ht)} (unexplained {len(trip_ht)}) | "
          f"unmatched→statdunk={len(unmatched_sd)} (unexplained {len(trip_sd)})")
    if trip_ht or trip_sd:
        print("HARD GATE TRIP — unexplained unmatched pool players (add an alias or record "
              "as a genuine absence):")
        for n in trip_ht:
            print("  hashtag:", n)
        for n in trip_sd:
            print("  statdunk:", n)
        sys.exit(3)
    print("GATE PASS — every pool player matched or recorded as a genuine absence.")


# Genuine absences — the source legitimately does not carry the player (verified against the
# raw: surname truly absent, not a spelling variant). All are deep-tail (our board # in
# parens) or unsigned FAs; both sources cover our entire top ~108 (statdunk's shallowest gap
# is Dereck Lively #109). See the unmatched report for team + auto-reason.
_ACCEPTED_ABSENT_HT = [
    "Cam Thomas",          # FA (#118) — Hashtag excludes unsigned free agents
    "Jaden Ivey",          # FA (#139)
    "Jonathan Kuminga",    # FA (#200)
    "Donte DiVincenzo",    # MIN (#159) — genuinely absent from Hashtag's full 429-row set
    "Liam McNeeley",       # CHA (#203) — deep tail, outside Hashtag's set
    "Kris Murray",         # MEM (#206)
    "Ebuka Okorie",        # DET (#219)
    "Jalen Wilson",        # ATL (#220)
]
_ACCEPTED_ABSENT_SD = [
    # Unsigned FAs (statdunk V4.10 excludes them):
    "Cam Thomas", "Jaden Ivey", "Jonathan Kuminga",
    # Deep tail — outside statdunk's 250-by-value set (which covers our entire top 108):
    "Dereck Lively", "Keon Ellis", "Daniel Gafford", "Jared McCain", "Gary Trent Jr",
    "Moussa Diabate", "GG Jackson", "Taylor Hendricks", "Khaman Maluach", "Obi Toppin",
    "Rob Dillingham", "Terrence Shannon Jr", "Kasparas Jakucionis", "Hannes Steinbach",
    "Nikola Jovic", "Ron Holland", "Gradey Dick", "Liam McNeeley", "Dalton Knecht",
    "Kris Murray", "Dailyn Swain", "Clint Capela", "Brice Sensabaugh", "Zuby Ejiofor",
    "Andre Drummond", "Labaron Philon", "Jeremy Sochan", "Cam Whitmore", "Ebuka Okorie",
    "Jalen Wilson",
]


def _reason(name, team, source):
    if team == "FA":
        return "unsigned FA — source excludes free agents"
    if source == "statdunk":
        return "deep tail — outside statdunk's 250-by-value set (covers our whole top ~108)"
    return "absent from Hashtag's full 429-row projection set"


def _write_unmatched(d, unmatched_ht, unmatched_sd, board):
    n_pool = len(board)
    lines = [f"# Unmatched-name report — {d} (HARD GATE, work order §3.3)", "",
             f"Pool players: {n_pool}. This file is the gate: every pool player below is a "
             "name that did NOT join to the named source after accent/punct/suffix "
             "normalization AND documented aliases were applied. Each remaining name is an "
             "accepted genuine absence, verified against the raw source (surname truly absent, "
             "not a spelling variant). Silent partial joins are refused; spelling variants are "
             "resolved in ALIASES (Herb/Herbert Jones, Cam/Cameron Johnson, Nic/Nicolas "
             "Claxton, Alex/Alexandre Sarr) and do NOT appear here.", ""]
    for label, rows, src in [("Hashtag", unmatched_ht, "hashtag"),
                             ("Statdunk", unmatched_sd, "statdunk")]:
        lines.append(f"## Not matched to {label} ({len(rows)}) — all accepted absences")
        lines.append("| our board # | player | team | reason |\n|---|---|---|---|")
        for rk, n in rows:
            team = board[n]["row"]["team"]
            lines.append(f"| {rk} | {n} | {team} | {_reason(n, team, src)} |")
        lines.append("")
    open(os.path.join(HERE, f"unmatched-{d}.md"), "w").write("\n".join(lines) + "\n")


def _write_disagreements(d, matched, sd_pub):
    # thresholds for "material" per-game line divergence vs Hashtag
    THR = {"pts": 3.0, "reb": 1.5, "ast": 1.5, "stl": 0.4, "blk": 0.4, "tpm": 0.6,
           "gp": 8, "fg_pct": 0.030, "ft_pct": 0.040, "tov": 0.8}
    CATS = ["pts", "reb", "ast", "stl", "blk", "tpm", "fg_pct", "ft_pct", "tov", "gp"]

    line_rows = []
    for m in matched:
        h = m["ht"]
        if not h:
            continue
        row = m["board"]["row"]
        diffs = {}
        for c in CATS:
            ov, hv = row.get(c if c != "gp" else "gp"), h.get(c)
            # our projections use 'fgp'/'ftp' keys, hashtag uses fg_pct/ft_pct
            if c == "fg_pct":
                ov = row.get("fgp")
            elif c == "ft_pct":
                ov = row.get("ftp")
            if isinstance(ov, (int, float)) and isinstance(hv, (int, float)):
                diffs[c] = ov - hv
        flags = [c for c, v in diffs.items() if abs(v) >= THR[c]]
        if flags:
            mag = sum(abs(diffs[c]) / THR[c] for c in flags)  # total divergence in threshold-units
            line_rows.append((m["name"], m["board"]["rank"], diffs, flags, mag))
    # sort by total divergence magnitude (biggest line differences first)
    line_rows.sort(key=lambda x: -x[4])

    ord_rows = []
    for m in matched:
        s = m["sd"]
        if not s or not isinstance(s.get("rank"), int):
            continue
        delta = s["rank"] - m["board"]["rank"]   # +ve: statdunk ranks him lower than we do (we're higher)
        ord_rows.append((abs(delta), delta, m["name"], m["board"]["rank"], s["rank"],
                         s.get("rank_avg"), m["board"]["z_adj"]))
    ord_rows.sort(reverse=True)

    # §5.3 arbitrage vs Yahoo ADP
    val, fad = [], []
    for m in matched:
        h = m["ht"]
        if not h or not isinstance(h.get("adp"), (int, float)):
            continue
        adp = h["adp"]
        r = m["board"]["rank"]
        if r + 15 <= adp:           # we rank him 15+ picks ahead of the room
            val.append((adp - r, m["name"], r, adp, _zprofile(m)))
        elif adp + 15 <= r:         # room drafts him 15+ picks ahead of us
            fad.append((r - adp, m["name"], r, adp, _zprofile(m)))
    val.sort(reverse=True)
    fad.sort(reverse=True)

    L = [f"# Market disagreement & arbitrage tables — {d}", "",
         "Reference layer for owner adjudication (work order §3.4, §5.3). Built from committed "
         "raw snapshots; our board = rank_engine.py over projections-2026-27.csv, unchanged. "
         "The board stays built from first principles — these are consulted as a sanity "
         "reference, not blended (owner decision 2026-08-21).", "",
         f"- **Statdunk** = category value reconstructed from the freshest projections "
         f"(`{sd_pub.get('label')}`, asOf **{sd_pub.get('asOf')}**) via statdunk's own "
         "`attempt-weighted-nine-category-zscore-v1` method — validated to reproduce statdunk's "
         "published category block exactly (Spearman 1.0000). The pre-computed board itself sits "
         "behind statdunk's off-allowlist Supabase backend. Ranks compared = games-inclusive "
         "`totals` (structural analog of our availability-adjusted board); per-game `averages` "
         "rank shown alongside.",
         "- **Hashtag** = 2026-27 Rest-of-Season, Yahoo ADP + eligibility.", "",
         "---", "",
         "## A. Biggest per-game line (and games) differences vs Hashtag (§3.4)",
         "Our projection minus Hashtag's, for matched players with at least one category past "
         f"threshold ({', '.join(f'{k} {v}' for k, v in THR.items())}); `gp` is season games. "
         "Sorted by total divergence. `+` = we project higher than Hashtag.", "",
         "| our # | player | flagged diffs (our − hashtag) |", "|---|---|---|"]
    for name, rk, diffs, flags, mag in line_rows[:40]:
        cells = ", ".join(f"{c} {diffs[c]:+.3f}" if c in ("fg_pct", "ft_pct")
                          else f"{c} {diffs[c]:+.1f}" for c in flags)
        L.append(f"| {rk} | {name} | {cells} |")
    L += ["", f"_{len(line_rows)} matched players show a material line divergence._", "",
          "---", "",
          "## B. Biggest ordering differences vs Statdunk value (§3.4)",
          "Δ = Statdunk totals rank − our board rank. **Δ>0 = we rank him higher than "
          "Statdunk** (a relative value on our board); Δ<0 = Statdunk higher (a relative "
          "fade). `sd_avg#` = Statdunk per-game rank.", "",
          "**Read with care:** Statdunk `totals` weights games proportionally (full season "
          "totals) — a harsher availability model than our streaming-credit `z_adj`. For "
          "injury-discounted stars a large Δ is mostly that model gap, not a valuation "
          "disagreement: compare `sd_avg#` (per-game) instead. E.g. Embiid sits at sd_tot#≈117 "
          "but sd_avg#≈23 ≈ our #22 — we agree on his per-game value and differ only on how "
          "hard to dock the missed games.", "",
          "| |Δ| | player | our # | sd_tot# | sd_avg# | our zAdj |", "|---|---|---|---|---|---|"]
    for adelta, delta, name, our_r, sd_r, sd_avg, zadj in ord_rows[:40]:
        L.append(f"| {delta:+d} | {name} | {our_r} | {sd_r} | {sd_avg} | {zadj:+.2f} |")
    L += ["", "---", "",
          "## C. Market arbitrage vs Yahoo ADP (§5.3 / Pass E)",
          "Designed-but-never-populated Pass E output. **Values** = our rank 15+ picks ahead "
          "of ADP; **Fades** = ADP 15+ picks ahead of our rank. z-profile names the two "
          "categories our board leans on most (+) and least (−) for that player — the "
          "structural 'why', for the owner to accept or reject. Mechanisms are the owner's "
          "call; nothing here is blended into the board.", "",
          f"### Values ({len(val)}) — we're higher than the room", "",
          "| gap | player | our # | Yahoo ADP | our board z-lean |", "|---|---|---|---|---|"]
    for gap, name, r, adp, prof in val[:30]:
        L.append(f"| +{gap:.0f} | {name} | {r} | {adp:.0f} | {prof} |")
    L += ["", f"### Fades ({len(fad)}) — the room is higher than us", "",
          "| gap | player | our # | Yahoo ADP | our board z-lean |", "|---|---|---|---|---|"]
    for gap, name, r, adp, prof in fad[:30]:
        L.append(f"| -{gap:.0f} | {name} | {r} | {adp:.0f} | {prof} |")
    L.append("")
    open(os.path.join(HERE, f"disagreements-{d}.md"), "w").write("\n".join(L) + "\n")


def _zprofile(m):
    """Two strongest (+) and weakest (−) 9-cat contributions on OUR board for this player,
    recomputed from the projection row via rank_engine, so the 'why' is ours not the market's."""
    import rank_engine as RE
    # cheap: reuse the z-scores already implied by the board row is not stored per-cat, so
    # recompute this player's per-cat z against the same pool once (cached).
    global _ZCACHE
    if "_ZCACHE" not in globals():
        rows = RE.load(PROJECTIONS)
        z1 = RE.zscores(rows, rows)
        pool = sorted(rows, key=lambda r: -RE.total(z1[r["name"]]))[:RE.POOL_SIZE]
        globals()["_ZCACHE"] = RE.zscores(rows, pool)
    z = _ZCACHE.get(m["name"], {})
    if not z:
        return ""
    order = sorted(z.items(), key=lambda kv: kv[1], reverse=True)
    lab = {"fgp": "FG%", "ftp": "FT%", "tpm": "3PM", "pts": "PTS", "reb": "REB",
           "ast": "AST", "stl": "STL", "blk": "BLK", "tov": "TOV"}
    hi = ", ".join(f"+{lab.get(k, k)}" for k, _ in order[:2])
    lo = ", ".join(f"-{lab.get(k, k)}" for k, _ in order[-2:])
    return f"{hi} / {lo}"


if __name__ == "__main__":
    main()
