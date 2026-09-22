#!/usr/bin/env python3
"""Yahoo rankings intake + market consensus (work order §3-§4; owner ask 2026-09-16).

The owner pasted Yahoo's player rankings (XRank + ADP, as of 2026-09-15) into chat
on 2026-09-16 and asked to "consolidate and average into your internal database".
The paste is landed verbatim as yahoo-raw-YYYY-MM-DD.txt (the raw layer — for a
paste, the chat message is the origin and the committed transcription is the
auditable copy). This script:

  1. Parses the raw file under transcription invariants (I1-I5 below). The paste
     duplicates most name lines (a copy artifact the owner said to ignore); the
     parser requires the two copies to MATCH, turning the artifact into a
     redundancy check on the transcription.
  2. Writes yahoo-YYYY-MM-DD.csv  (player,team,pos,xrank,adp).
  3. Joins to the full projections pool via build_market.norm + aliases, under the
     work order's HARD unmatched gate (§3.3): every pool player matches Yahoo or
     is listed in _ACCEPTED_ABSENT_YH with a verified reason. Exit 3 otherwise.
  4. Writes consensus-YYYY-MM-DD.csv — the averaged consolidation the owner asked
     for: per pool player, mean of the available rank signals (our board rank,
     Yahoo XRank, Yahoo ADP), re-ranked. This is a MARKET-LENS artifact in the
     reference layer; the first-principles board (rank_engine over projections)
     is untouched, per the owner decision of 2026-08-21 (work order §1: "NOT a
     blend ... do not re-litigate"). If the owner wants the consensus to replace
     the board or feed marketRanks, that is the work order's gated step 5.
  5. Writes disagreements-yahoo-YYYY-MM-DD.md — §5.3 values/fades vs the fresh
     ADP, team-code mismatches (FLAGS ONLY: Yahoo is one outlet, so per fix F2 no
     pool row changes flow from it), availability disagreements, and coverage
     gaps both directions. Owner adjudicates.
  6. Appends/refreshes the yahoo row in provenance.csv.

Transcription invariants (any failure = exit 2, fix the raw file first):
  I1 every block parses: name [dup name == name], positions from {PG,SG,SF,PF,C},
     '·', team from the 30 NBA codes, 'XRank #N', optionally '·' + 'ADP x.y'
  I2 ADP-bearing rows form a strict PREFIX of the list, ADP non-decreasing
     (owner: the list is ordered best-to-worst)
  I3 after ADP stops, XRank strictly increasing
  I4 XRank values unique; gaps in 1..299 reported (expected coverage: the full
     1..299 plus one placeholder-tier 668)
  I5 no duplicate players

Second raw format (2026-09-22 paste — Yahoo's 9-cat RANKINGS page, rank only,
no ADP): three lines per player, "N" / name / "POS<tab>TEAM", with Yahoo's own
site codes (NOR, PHO, UTH — mapped to the pool's NOP, PHX, UTA). Detected by the
first non-empty line being a bare integer. Invariants: I1 (pos/team), I4 (unique
XRank, no gaps in 1..N), I5 (no duplicate players), I6 (rank N sits at position
N — the list is contiguous). XRank = the rank; ADP empty. For this format the
absence gate is MECHANICAL: an unmatched pool player is accepted only when no
Yahoo-only name shares (surname, first three letters) with him — otherwise the
pair is a possible spelling variant and trips the gate until an alias or an
accepted absence is recorded.

Two Yahoo pages can land for one date (2026-09-22): the draft-analysis page
(XRank + ADP, block format) is the CANONICAL file yahoo-YYYY-MM-DD.csv — the
deck's F8 price source and the consensus/disagreements input — while the
9-cat RANKINGS page (rank only) lands as reference under the
yahoo-9cat-rankings-* names (its own unmatched gate and provenance row, no
consensus). Run the rankings page with the `rankings` flag. The canonical
report carries a cross-page section (G) when both exist for the date.

From 2026-09-22 (MECHANICAL_FROM) the absence gate is mechanical for every
format; the 2026-09-15 run keeps its hand-verified list so it reproduces.

Usage: python3 report/market/yahoo_market.py [YYYY-MM-DD] [rankings]
"""
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_market as BM  # norm(), ALIASES, our_board(), _write_csv

TEAMS = {"ATL", "BOS", "BKN", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GSW",
         "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK",
         "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"}
POS = {"PG", "SG", "SF", "PF", "C"}
YAHOO_TEAM = {"NOR": "NOP", "PHO": "PHX", "UTH": "UTA"}  # Yahoo site codes -> pool codes
DRAFTABLE = 156          # 12 teams x 13 rounds: the universe the room drafts
PASTED_ON = {"2026-09-15": "2026-09-16"}  # paste date when it differs from the list date
MECHANICAL_FROM = "2026-09-22"  # absence gate mechanical (surname + first 3) from this list date on
XRANK_CAP = 300  # 668 is Yahoo's placeholder tier for expert-unranked names;
                 # capped at 300 (list depth + 1) when averaging, stored raw.

# Yahoo-specific spelling variants, verified against the raw (surname present,
# different name form). Extends the work order's shared alias set.
ALIASES = dict(BM.ALIASES)
ALIASES.update({
    "Ron Holland": {"Ronald Holland II"},   # yahoo uses the given name + suffix
})


def parse_raw(path):
    """Returns (rows, problems, fmt) with fmt in {"block", "rank"}."""
    lines = [l.strip() for l in open(path, encoding="utf-8")]
    nonblank = [l for l in lines if l]
    if nonblank and re.fullmatch(r"\d+", nonblank[0]):
        rows, problems = _parse_rank_list(nonblank)
        return rows, problems, "rank"
    blocks, cur = [], []
    for line in lines:
        if line:
            cur.append(line)
        elif cur:
            blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)
    rows, problems = _parse_blocks(blocks)
    return rows, problems, "block"


def _parse_rank_list(lines):
    rows, problems = [], []
    if len(lines) % 3:
        problems.append(f"rank-list: {len(lines)} non-blank lines is not a multiple of 3")
    for i in range(0, len(lines) - len(lines) % 3, 3):
        rk, name, posteam = lines[i], lines[i + 1], lines[i + 2]
        if not re.fullmatch(r"\d+", rk):
            problems.append(f"entry {i // 3 + 1}: rank line {rk!r} is not an integer")
            continue
        toks = posteam.split()
        if len(toks) != 2:
            problems.append(f"entry {rk} ({name!r}): expected 'POS<tab>TEAM', got {posteam!r}")
            continue
        pos, team = toks
        team = YAHOO_TEAM.get(team, team)
        if not _is_pos(pos):
            problems.append(f"entry {rk} ({name!r}): bad positions {pos!r}")
        if team not in TEAMS:
            problems.append(f"entry {rk} ({name!r}): bad team {team!r}")
        rows.append({"player": name, "team": team, "pos": pos.replace(" ", ""),
                     "xrank": int(rk), "adp": None})
    return rows, problems


def _parse_blocks(blocks):
    rows, problems = [], []
    for i, b in enumerate(blocks, 1):
        name = b[0]
        j = 1
        if j < len(b) and b[j] == name:
            j += 1                       # duplicated name line (copy artifact)
        elif j < len(b) and b[j] not in ("·",) and not _is_pos(b[j]):
            problems.append(f"block {i} ({name!r}): second line {b[j]!r} is neither "
                            "a matching duplicate name nor a position line")
            continue
        rest = [x for x in b[j:] if x != "·"]
        if len(rest) not in (3, 4):
            problems.append(f"block {i} ({name!r}): expected pos/team/xrank[/adp], "
                            f"got {rest!r}")
            continue
        pos, team, xr = rest[0], rest[1], rest[2]
        if not _is_pos(pos):
            problems.append(f"block {i} ({name!r}): bad positions {pos!r}")
        if team not in TEAMS:
            problems.append(f"block {i} ({name!r}): bad team {team!r}")
        m = re.fullmatch(r"XRank #(\d+)", xr)
        if not m:
            problems.append(f"block {i} ({name!r}): bad xrank {xr!r}")
            continue
        adp = None
        if len(rest) == 4:
            ma = re.fullmatch(r"ADP (\d+(?:\.\d+)?)", rest[3])
            if not ma:
                problems.append(f"block {i} ({name!r}): bad adp {rest[3]!r}")
                continue
            adp = float(ma.group(1))
        rows.append({"player": name, "team": team, "pos": pos.replace(" ", ""),
                     "xrank": int(m.group(1)), "adp": adp})
    return rows, problems


def _is_pos(s):
    return all(p.strip() in POS for p in s.split(","))


def check_invariants(rows, fmt="block"):
    problems = []
    depth = list_depth(rows, fmt)
    if fmt == "rank":
        for i, r in enumerate(rows, 1):
            if r["xrank"] != i:
                problems.append(f"I6: rank {r['xrank']} ({r['player']}) sits at position {i}")
    # I2: ADP prefix, non-decreasing
    seen_no_adp = False
    prev_adp = 0.0
    for r in rows:
        if r["adp"] is None:
            seen_no_adp = True
        else:
            if seen_no_adp:
                problems.append(f"I2: {r['player']} has ADP after the ADP section ended")
            if r["adp"] < prev_adp:
                problems.append(f"I2: ADP decreases at {r['player']} "
                                f"({prev_adp} -> {r['adp']})")
            prev_adp = r["adp"]
    # I3: XRank strictly increasing in the no-ADP tail
    tail = [r for r in rows if r["adp"] is None]
    for a, b in zip(tail, tail[1:]):
        if b["xrank"] <= a["xrank"]:
            problems.append(f"I3: tail XRank not increasing at {b['player']} "
                            f"({a['xrank']} -> {b['xrank']})")
    # I4: uniqueness + gap report
    xrs = [r["xrank"] for r in rows]
    dups = {x for x in xrs if xrs.count(x) > 1}
    if dups:
        problems.append(f"I4: duplicate XRank values {sorted(dups)}")
    in_range = {x for x in xrs if x <= depth}
    gaps = sorted(set(range(1, depth + 1)) - in_range)
    # I5: duplicate players
    names = [r["player"] for r in rows]
    pdups = {n for n in names if names.count(n) > 1}
    if pdups:
        problems.append(f"I5: duplicate players {sorted(pdups)}")
    return problems, gaps


# Pool players verified absent from Yahoo's published list (2026-09-16 run:
# every surname grepped against the raw — 19 absent entirely; 'Wallace' present
# only as Cason Wallace/OKC, a different player). Auto-reason from team; the
# _ABSENT_NOTES override where the absence itself is information. Anything
# unmatched and not listed here trips the gate (exit 3).
_ACCEPTED_ABSENT_YH = [
    "Bogdan Bogdanovic", "Cam Thomas", "Jaden Ivey", "Gary Trent Jr",
    "Obi Toppin", "Rob Dillingham", "Kasparas Jakucionis", "Khris Middleton",
    "Nikola Jovic", "Gradey Dick", "Liam McNeeley", "Dalton Knecht",
    "Kris Murray", "Dailyn Swain", "Zuby Ejiofor", "Labaron Philon",
    "Jeremy Sochan", "Cam Whitmore", "Ebuka Okorie",
    "Jalen Wilson",
    # Keaton Wallace removed 2026-09-16: his pool row was deleted on the
    # owner-approved integration (two-year Maccabi Tel Aviv deal — see
    # after-report-2026-09-16-gap-research.md §3).
]
_ABSENT_NOTES = {
    "Gradey Dick": "absent despite the executed 9/14 trade to LAC — Yahoo's list "
                   "does not carry him at all; watch his camp role next pull",
    "Jeremy Sochan": "absent — consistent with the standing cut-watch flag",
    "Cam Whitmore": "absent — consistent with the waive-and-stretch watch item",
}


def list_depth(rows, fmt):
    """Coverage depth the gap check runs against: the list length for the
    rank-list page; the largest in-range XRank for the block page (299 on
    9/15, 296 on 9/22 — placeholder-tier ranks above XRANK_CAP do not count)."""
    if fmt == "rank":
        return len(rows)
    inr = [r["xrank"] for r in rows if r["xrank"] <= XRANK_CAP]
    return max(inr) if inr else 0


def _key3(name):
    """(surname, first three letters) — the deck plane's drift key (F8)."""
    t = BM.norm(name).split()
    return (t[-1], t[0][:3]) if t else (name, "")


def _previous_file(d):
    """The newest yahoo-YYYY-MM-DD.csv dated before d, or None."""
    cands = sorted(f for f in os.listdir(HERE)
                   if re.fullmatch(r"yahoo-\d{4}-\d{2}-\d{2}\.csv", f) and f[6:16] < d)
    return os.path.join(HERE, cands[-1]) if cands else None


def _load_csv(path):
    out = []
    for r in csv.DictReader(open(path, encoding="utf-8")):
        r["xrank"] = int(r["xrank"])
        r["adp"] = float(r["adp"]) if r.get("adp") not in (None, "") else None
        out.append(r)
    return out


def _price(r):
    return r["adp"] if r["adp"] is not None else r["xrank"]


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else "2026-09-15"
    rankings = "rankings" in sys.argv[2:]
    stem = "yahoo-9cat-rankings" if rankings else "yahoo"
    raw_path = os.path.join(HERE, f"{stem}-raw-{d}.txt")
    rows, problems, fmt = parse_raw(raw_path)
    inv, gaps = check_invariants(rows, fmt)
    problems += inv
    n_adp = sum(1 for r in rows if r["adp"] is not None)
    depth = list_depth(rows, fmt)
    print(f"format {fmt}: parsed {len(rows)} players ({n_adp} with ADP, {len(rows) - n_adp} "
          f"XRank-only); XRank gaps in 1..{depth}: {gaps if gaps else 'NONE'}")
    if problems:
        print(f"TRANSCRIPTION GATE: FAIL — {len(problems)} problem(s)")
        for p in problems:
            print(" ", p)
        sys.exit(2)
    if gaps:
        print("TRANSCRIPTION GATE: FAIL — XRank coverage has gaps; re-check the "
              "raw transcription at those ranks before proceeding")
        sys.exit(2)
    print("TRANSCRIPTION GATE: PASS (I1-I5" + (", I6)" if fmt == "rank" else ")"))

    BM._write_csv(os.path.join(HERE, f"{stem}-{d}.csv"),
                  ["player", "team", "pos", "xrank", "adp"], rows)

    # ---- join under the hard gate --------------------------------------------
    board = BM.our_board()
    alias_index = {}
    for canonical, variants in ALIASES.items():
        for v in variants:
            alias_index[BM.norm(v)] = BM.norm(canonical)
    yh_by = {}
    for r in rows:
        yh_by.setdefault(alias_index.get(BM.norm(r["player"]), BM.norm(r["player"])), r)

    matched, unmatched = [], []
    for name, b in board.items():
        key = alias_index.get(BM.norm(name), BM.norm(name))
        y = yh_by.get(key)
        if y is None:
            unmatched.append((b["rank"], name, b["row"]["team"]))
        matched.append({"name": name, "board": b, "yh": y})
    unmatched.sort()

    pool_keys = {alias_index.get(BM.norm(n), BM.norm(n)) for n in board}
    yahoo_only = [r for r in rows
                  if alias_index.get(BM.norm(r["player"]), BM.norm(r["player"]))
                  not in pool_keys]

    reasons = None
    if d >= MECHANICAL_FROM:
        # Mechanical absence check: a Yahoo-only name sharing (surname, first 3)
        # with an unmatched pool player is a possible spelling variant.
        spare = {}
        for r in yahoo_only:
            spare.setdefault(_key3(r["player"]), r["player"])
        reasons, trips = {}, []
        for rk, n, t in unmatched:
            hit = spare.get(_key3(n))
            if hit and n not in set(_ACCEPTED_ABSENT_YH):
                trips.append((rk, n, t, hit))
            elif t == "FA":
                reasons[n] = "unsigned FA — Yahoo's list carries no free agents"
            else:
                reasons[n] = _ABSENT_NOTES.get(
                    n, f"outside Yahoo's top {len(rows)} — surname absent from the raw "
                       "(mechanical check: no Yahoo-only name shares surname + first 3 letters)")
        print(f"JOIN: {len(board)} pool players | matched to yahoo="
              f"{len(board) - len(unmatched)} | unmatched={len(unmatched)} "
              f"(possible spelling variants {len(trips)}) | yahoo-only names={len(yahoo_only)}")
        if trips:
            print("HARD GATE TRIP — unmatched pool players that look like a Yahoo spelling "
                  "(add a verified alias, or record the absence with a reason):")
            for rk, n, t, hit in trips:
                print(f"  #{rk:<4} {n} ({t})  ~  {hit} (Yahoo)")
            sys.exit(3)
    else:
        trips = [n for _, n, _ in unmatched if n not in set(_ACCEPTED_ABSENT_YH)]
        print(f"JOIN: {len(board)} pool players | matched to yahoo="
              f"{len(board) - len(unmatched)} | unmatched={len(unmatched)} "
              f"(unexplained {len(trips)}) | yahoo-only names={len(yahoo_only)}")
        if trips:
            print("HARD GATE TRIP — unexplained unmatched pool players (add a verified "
                  "alias or record as a genuine absence):")
            for rk, n, t in unmatched:
                if n in trips:
                    print(f"  #{rk:<4} {n} ({t})")
            sys.exit(3)

    if rankings:
        _write_unmatched(d, unmatched, board, len(rows), reasons, stem)
        _refresh_provenance(d, len(rows), n_adp, fmt, stem)
        print(f"wrote {stem}-{d}.csv, unmatched-{stem}-{d}.md, provenance.csv (reference page: no consensus)")
        print("GATE PASS — every pool player matched or recorded as a genuine absence.")
        return

    # ---- consensus: the averaged consolidation (owner ask 2026-09-16) --------
    cons = []
    for m in matched:
        b, y = m["board"], m["yh"]
        signals = [float(b["rank"])]
        xr = adp = ""
        if y:
            xr = y["xrank"]
            signals.append(float(min(y["xrank"], XRANK_CAP)))
            if y["adp"] is not None:
                adp = y["adp"]
                signals.append(y["adp"])
        cons.append({"player": m["name"], "team": b["row"]["team"],
                     "pos": b["row"]["pos"], "our_rank": b["rank"],
                     "z_adj": round(b["z_adj"], 3), "yahoo_xrank": xr,
                     "yahoo_adp": adp, "n_signals": len(signals),
                     "consensus_avg": round(sum(signals) / len(signals), 2)})
    cons.sort(key=lambda r: (r["consensus_avg"], r["our_rank"]))
    for i, r in enumerate(cons, 1):
        r["consensus_rank"] = i
    BM._write_csv(os.path.join(HERE, f"consensus-{d}.csv"),
                  ["consensus_rank", "player", "team", "pos", "consensus_avg",
                   "our_rank", "yahoo_xrank", "yahoo_adp", "n_signals", "z_adj"],
                  cons)

    prev_path = _previous_file(d)
    prev = _load_csv(prev_path) if prev_path else None
    _write_unmatched(d, unmatched, board, len(rows), reasons, stem)
    rk_path = os.path.join(HERE, f"yahoo-9cat-rankings-{d}.csv")
    rk = _load_csv(rk_path) if os.path.exists(rk_path) else None
    _write_disagreements(d, matched, cons, yahoo_only, rows, fmt, prev,
                         os.path.basename(prev_path) if prev_path else None, alias_index, rk)
    _refresh_provenance(d, len(rows), n_adp, fmt, stem)
    print(f"wrote yahoo-{d}.csv, consensus-{d}.csv, unmatched-yahoo-{d}.md, "
          f"disagreements-yahoo-{d}.md, provenance.csv")
    print("GATE PASS — every pool player matched or recorded as a genuine absence.")


def _write_unmatched(d, unmatched, board, n_yahoo, reasons=None, stem="yahoo"):
    lines = [f"# Unmatched-name report vs Yahoo — {d} (HARD GATE, work order §3.3)", "",
             f"Pool players: {len(board)}; Yahoo list: {n_yahoo}. Every pool player "
             "below did NOT join to Yahoo after normalization and documented aliases; "
             "each is an accepted genuine absence, verified against the raw (surname "
             "truly absent, not a spelling variant). Silent partial joins are refused.", "",
             f"## Not matched to Yahoo ({len(unmatched)}) — all accepted absences", "",
             "| our board # | player | team | reason |", "|---|---|---|---|"]
    for rk, n, t in unmatched:
        if reasons is not None:
            reason = reasons[n]
        else:
            reason = _ABSENT_NOTES.get(
                n, "unsigned FA — Yahoo's list carries no free agents" if t == "FA"
                else "outside Yahoo's published list (deep tail / not rostered by Yahoo)")
        lines.append(f"| {rk} | {n} | {t} | {reason} |")
    lines.append("")
    open(os.path.join(HERE, f"unmatched-{stem}-{d}.md"), "w").write("\n".join(lines) + "\n")


def _write_disagreements(d, matched, cons, yahoo_only, rows, fmt="block", prev=None,
                         prev_name=None, alias_index=None, rankings_page=None):
    xr_only = fmt == "rank"
    plabel = "XRank" if xr_only else "ADP"
    val, fad = [], []
    for m in matched:
        y = m["yh"]
        if not y or (not xr_only and y["adp"] is None):
            continue
        r, adp = m["board"]["rank"], _price(y)
        if r + 15 <= adp:
            val.append((adp - r, m["name"], r, adp, BM._zprofile(m)))
        elif adp + 15 <= r:
            fad.append((r - adp, m["name"], r, adp, BM._zprofile(m)))
    val.sort(reverse=True)
    fad.sort(reverse=True)

    mism = [(m["board"]["rank"], m["name"], m["board"]["row"]["team"], m["yh"]["team"])
            for m in matched if m["yh"] and m["yh"]["team"] != m["board"]["row"]["team"]]
    mism.sort()

    avail = []
    for m in matched:
        y = m["yh"]
        gp = m["board"]["row"].get("gp")
        if y and isinstance(gp, (int, float)) and gp <= 40:
            avail.append((m["board"]["rank"], m["name"], gp, y["xrank"], y["adp"]))
    avail.sort(key=lambda x: (x[4] if x[4] is not None else x[3]))

    if xr_only:
        gaps_deep = [r for r in yahoo_only if r["xrank"] <= DRAFTABLE]
    else:
        gaps_deep = [r for r in yahoo_only if r["adp"] is not None and r["adp"] < 140]

    if xr_only:
        intro = [f"# Yahoo market consolidation — {d}", "",
                 f"Owner paste ({PASTED_ON.get(d, d)}): Yahoo's current 9-cat RANKINGS as of "
                 f"{d} — rank order only, no ADP column. Landed per the standing work order: "
                 f"Yahoo lands as reference data (`yahoo-{d}.csv`, XRank = the rank, ADP "
                 f"empty) and the average lands as the market-lens consensus board "
                 f"(`consensus-{d}.csv`) — mean of our board rank and Yahoo XRank, re-ranked "
                 "over all pool players. The first-principles board itself is UNCHANGED "
                 "(owner decision 2026-08-21: reference, not a blend). Downstream, the deck's "
                 "F8 price loader (yahoo-fantasy-basketball PR #36) prices by ADP where "
                 "Yahoo lists one, else XRank — this file prices every matched player by "
                 "XRank, labelled XR.", "",
                 "Yahoo is a single outlet: per fix F2, nothing here changes a pool row. Team "
                 "mismatches, Yahoo's own team changes since the previous paste, and coverage "
                 "gaps below are flags for the next pull's watchlist.", ""]
    else:
        intro = [f"# Yahoo market consolidation — {d}", "",
                 "Owner ask (2026-09-16): consolidate and average Yahoo's rankings into the "
                 "internal database. Consolidated per the standing work order: Yahoo lands as "
                 f"reference data (`yahoo-{d}.csv`) and the average lands as the market-lens "
                 f"consensus board (`consensus-{d}.csv`) — mean of the available rank signals "
                 "(our board rank, Yahoo XRank capped at 300, Yahoo ADP), re-ranked over all "
                 "pool players. The first-principles board itself is UNCHANGED (owner decision "
                 "2026-08-21: reference, not a blend; replacing marketRanks with real market "
                 "data remains the work order's gated step 5).", "",
                 "Yahoo is a single outlet: per fix F2, nothing here changes a pool row. Team "
                 "mismatches and coverage gaps below are flags for the next pull's watchlist.", ""]
    L = intro + ["---", "",
         f"## A. Consensus board top 30 (full file: consensus-{d}.csv)", "",
         "| cons # | player | avg | our # | XRank | ADP |", "|---|---|---|---|---|---|"]
    for r in cons[:30]:
        L.append(f"| {r['consensus_rank']} | {r['player']} | {r['consensus_avg']} | "
                 f"{r['our_rank']} | {r['yahoo_xrank']} | {r['yahoo_adp']} |")
    if xr_only:
        L += ["", "---", "",
              "## B. Market arbitrage vs Yahoo XRank (§5.3 / Pass E)",
              "**Values** = our rank 15+ picks ahead of Yahoo's rank; **Fades** = the reverse. "
              "z-lean = the two categories our board leans on most/least — the structural "
              "'why', for the owner to accept or reject.", "",
              f"**Read with care:** this paste is Yahoo's expert RANK, not the room's ADP. It "
              f"covers {len(rows)} names, so a player we rank inside {len(rows)} but absent "
              "from it appears in section E (coverage), not here.", ""]
    else:
        L += ["", "---", "",
              "## B. Market arbitrage vs fresh Yahoo ADP (§5.3 / Pass E)",
              "**Values** = our rank 15+ picks ahead of ADP; **Fades** = the reverse. "
              "z-lean = the two categories our board leans on most/least — the structural "
              "'why', for the owner to accept or reject.", "",
              "**Read the deep fades with care:** Yahoo publishes ADP only for its top "
              "189 rows (max 125.2), so a player we rank ≥ ~140 shows a mechanical 15+ "
              "'fade' merely by having an ADP at all. The real adjudication items are "
              "the fades among players we rank inside ~140; below that, read a fade as "
              "'the room drafts him at all', not as a precise gap.", ""]
    L += [f"### Values ({len(val)}) — we're higher than the room", "",
          f"| gap | player | our # | {plabel} | our z-lean |", "|---|---|---|---|---|"]
    for gap, name, r, adp, prof in val[:25]:
        L.append(f"| +{gap:.0f} | {name} | {r} | {adp:.0f} | {prof} |")
    L += ["", f"### Fades ({len(fad)}) — the room is higher than us", "",
          f"| gap | player | our # | {plabel} | our z-lean |", "|---|---|---|---|---|"]
    for gap, name, r, adp, prof in fad[:25]:
        L.append(f"| -{gap:.0f} | {name} | {r} | {adp:.0f} | {prof} |")
    L += ["", "---", "",
          f"## C. Team-code mismatches ({len(mism)}) — FLAGS ONLY (F2: single source)", "",
          "| our # | player | our team | yahoo team |", "|---|---|---|---|"]
    for rk, n, ours, ya in mism:
        L.append(f"| {rk} | {n} | {ours} | {ya} |")
    L += ["", "---", "",
          f"## D. Availability disagreements ({len(avail)}) — our GP ≤ 40, market "
          "still pricing them", "",
          "| our # | player | our GP | XRank | ADP |", "|---|---|---|---|---|"]
    for rk, n, gp, xr, adp in avail:
        L.append(f"| {rk} | {n} | {gp:.0f} | {xr} | {adp if adp is not None else '—'} |")
    L += ["", "---", "",
          f"## E. Coverage gaps — Yahoo names not in our pool ({len(yahoo_only)}; "
          + (f"{len(gaps_deep)} ranked inside the draftable {DRAFTABLE})" if xr_only
             else f"{len(gaps_deep)} carry an ADP inside 140)"),
          "Names the room is drafting that our database cannot price. Owner decides "
          "which enter the pool (each needs a sourced projection row).", "",
          "| player | team | pos | XRank | ADP |", "|---|---|---|---|---|"]
    for r in sorted(yahoo_only, key=lambda r: (r["adp"] is None,
                                               r["adp"] if r["adp"] is not None
                                               else r["xrank"])):
        L.append(f"| {r['player']} | {r['team']} | {r['pos']} | {r['xrank']} | "
                 f"{r['adp'] if r['adp'] is not None else '—'} |")
    if prev is not None:
        L += _moves_section(rows, prev, prev_name, alias_index or {})
    if rankings_page is not None:
        L += _cross_page_section(d, rows, rankings_page, matched, alias_index or {})
    L.append("")
    open(os.path.join(HERE, f"disagreements-yahoo-{d}.md"), "w").write("\n".join(L) + "\n")


def _cross_page_section(d, rows, rk, matched, alias_index):
    """Section G: the same outlet's two pages on one date — the draft-analysis
    page's XRank/ADP (this file) vs the 9-cat RANKINGS page's rank — per player,
    with the biggest disagreements and where our board sits."""
    canon = lambda n: alias_index.get(BM.norm(n), BM.norm(n))
    rmap = {canon(r["player"]): r for r in rk}
    ours = {canon(m["name"]): m["board"]["rank"] for m in matched}
    both = []
    for r in rows:
        k = canon(r["player"])
        if k in rmap:
            both.append((r["player"], r["xrank"], r["adp"], rmap[k]["xrank"], ours.get(k)))
    diffs = [(b[1] - b[3], b) for b in both if b[1] <= XRANK_CAP]
    up = sorted(diffs, key=lambda x: -x[0])[:15]     # 9-cat page ranks him much higher than this page
    down = sorted(diffs, key=lambda x: x[0])[:15]    # 9-cat page ranks him much lower
    n_adp = [b for b in both if b[2] is not None]
    room_vs_9cat = sorted(((b[2] - b[3], b) for b in n_adp), key=lambda x: x[0])
    L = ["", "---", "",
         f"## G. Yahoo's two pages on {d}: this file (draft-analysis XRank + ADP) vs the 9-cat RANKINGS page",
         f"{len(both)} players on both pages. The 9-cat rankings page (reference file "
         f"`yahoo-9cat-rankings-{d}.csv`) is a different expert ordering from this page's XRank; the "
         "deck prices by ADP where present, else this page's XRank (F8). Differences here are Yahoo "
         "disagreeing with Yahoo — read them as the width of the expert band, not as a price.", "",
         "### 9-cat page ranks him higher than this page (top 15)", "",
         "| 9-cat rank | XRank here | ADP | player | our # |", "|---|---|---|---|---|"]
    for dlt, (n, xr, adp, rk9, our) in up:
        L.append(f"| {rk9} | {xr} | {adp if adp is not None else '—'} | {n} | {our if our else '—'} |")
    L += ["", "### 9-cat page ranks him lower than this page (top 15)", "",
          "| 9-cat rank | XRank here | ADP | player | our # |", "|---|---|---|---|---|"]
    for dlt, (n, xr, adp, rk9, our) in down:
        L.append(f"| {rk9} | {xr} | {adp if adp is not None else '—'} | {n} | {our if our else '—'} |")
    L += ["", "### The room vs the 9-cat page: biggest reaches (ADP well ahead of the 9-cat rank)", "",
          "| ADP | 9-cat rank | player | our # |", "|---|---|---|---|"]
    for dlt, (n, xr, adp, rk9, our) in room_vs_9cat[:12]:
        L.append(f"| {adp:.1f} | {rk9} | {n} | {our if our else '—'} |")
    L += ["", "### The room vs the 9-cat page: biggest fades (ADP well behind the 9-cat rank)", "",
          "| ADP | 9-cat rank | player | our # |", "|---|---|---|---|"]
    for dlt, (n, xr, adp, rk9, our) in room_vs_9cat[-12:][::-1]:
        L.append(f"| {adp:.1f} | {rk9} | {n} | {our if our else '—'} |")
    return L


def _moves_section(rows, prev, prev_name, alias_index):
    """Section F: what Yahoo itself changed between the previous paste and this one —
    XRank moves (XRank on BOTH sides; a previous placeholder-tier XRank > XRANK_CAP
    means Yahoo's experts had not ranked him, listed separately with his old ADP),
    team changes in Yahoo's own data, and names that entered or left the draftable
    range of the expert list."""
    canon = lambda n: alias_index.get(BM.norm(n), BM.norm(n))
    pmap = {canon(r["player"]): r for r in prev}
    nmap = {canon(r["player"]): r for r in rows}
    both = [k for k in nmap if k in pmap]
    ranked_before = [k for k in both if pmap[k]["xrank"] <= XRANK_CAP]
    moves = [(pmap[k]["xrank"] - nmap[k]["xrank"], nmap[k]["player"], pmap[k]["xrank"],
              nmap[k]["xrank"], pmap[k]["adp"]) for k in ranked_before]
    inside = [m for m in moves if min(m[2], m[3]) <= 150]
    risers = sorted([m for m in inside if m[0] >= 10], reverse=True)[:20]
    fallers = sorted([m for m in inside if m[0] <= -10])[:20]
    newly = sorted((nmap[k]["xrank"], nmap[k]["player"], pmap[k]["adp"])
                   for k in both if pmap[k]["xrank"] > XRANK_CAP)
    teams = sorted((nmap[k]["xrank"], nmap[k]["player"], pmap[k]["team"], nmap[k]["team"])
                   for k in both if pmap[k]["team"] != nmap[k]["team"])
    entered = sorted((r["xrank"], r["player"], r["team"]) for k, r in nmap.items()
                     if k not in pmap and r["xrank"] <= DRAFTABLE)
    left = sorted((r["xrank"], r["player"], r["team"], r["adp"]) for k, r in pmap.items()
                  if k not in nmap and r["xrank"] <= DRAFTABLE)
    fmt_adp = lambda a: f"{a:.0f}" if a is not None else "—"
    L = ["", "---", "",
         f"## F. What Yahoo changed since `{prev_name}`",
         f"Same-outlet comparison ({len(both)} names in both files, {len(ranked_before)} "
         "expert-ranked in both). Moves are XRank vs XRank — the previous file's ADP is "
         "shown for reference only, because this paste carries none. A rank move is Yahoo "
         "re-pricing a player; a team change here is Yahoo's own roster data moving between "
         "the two pastes — still ONE outlet, so it flags a transaction to verify at the next "
         "pull, never a row edit.", "",
         f"### Risers ({len(risers)} shown; XRank move ≥ 10 places, inside 150 on either side)", "",
         "| move | player | XRank before | XRank after | ADP before |", "|---|---|---|---|---|"]
    for mv, n, a, b, adp in risers:
        L.append(f"| +{mv} | {n} | {a} | {b} | {fmt_adp(adp)} |")
    L += ["", f"### Fallers ({len(fallers)} shown)", "",
          "| move | player | XRank before | XRank after | ADP before |", "|---|---|---|---|---|"]
    for mv, n, a, b, adp in fallers:
        L.append(f"| {mv} | {n} | {a} | {b} | {fmt_adp(adp)} |")
    L += ["", f"### Newly expert-ranked ({len(newly)}) — placeholder tier before, ranked now", "",
          "| XRank now | player | ADP before |", "|---|---|---|"]
    for xr, n, adp in newly:
        L.append(f"| {xr} | {n} | {fmt_adp(adp)} |")
    L += ["", f"### Yahoo team changes ({len(teams)}) — transaction flags for the next pull", "",
          "| XRank | player | before | after |", "|---|---|---|---|"]
    for xr, n, a, b in teams:
        L.append(f"| {xr} | {n} | {a} | {b} |")
    L += ["", f"### Entered Yahoo's list inside the draftable {DRAFTABLE} ({len(entered)})", "",
          "| XRank | player | team |", "|---|---|---|"]
    for xr, n, t in entered:
        L.append(f"| {xr} | {n} | {t} |")
    L += ["", f"### Left Yahoo's list from inside the draftable {DRAFTABLE} ({len(left)})", "",
          "| XRank before | player | team | ADP before |", "|---|---|---|---|"]
    for xr, n, t, adp in left:
        L.append(f"| {xr} | {n} | {t} | {fmt_adp(adp)} |")
    return L


def _refresh_provenance(d, n, n_adp, fmt="block", stem="yahoo"):
    path = os.path.join(HERE, "provenance.csv")
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    rows = [r for r in rows if not (r["source"] == stem and f"as of {d} " in r["notes"])]
    pasted = PASTED_ON.get(d, d)
    if fmt == "rank":
        notes = (f"Yahoo 9-cat player RANKINGS page as of {d} per the owner, pasted into chat "
                 f"{pasted} and transcribed verbatim to {stem}-raw-{d}.txt (rank / name / "
                 f"pos+team, Yahoo site codes NOR/PHO/UTH mapped to NOP/PHX/UTA). XRank = the "
                 f"rank (1..{n}, contiguous); NO ADP in this paste. Parsed under invariants "
                 f"I1, I4-I6 by yahoo_market.py; absence gate mechanical (surname + first 3).")
    else:
        notes = (f"Yahoo player rankings as of {d} per the owner, pasted into chat "
                 f"{pasted} and transcribed verbatim to {stem}-raw-{d}.txt (duplicate "
                 f"name lines are a copy artifact, used as a transcription check). "
                 f"XRank = Yahoo expert rank (668 = placeholder tier, capped at 300 "
                 f"for averaging); ADP on the top {n_adp} rows only, non-decreasing "
                 f"(list ordered best-to-worst per owner). Parsed under invariants "
                 f"I1-I5 by yahoo_market.py.")
    rows.append({"source": stem,
                 "url": "(owner paste — no direct fetch; sports egress blocked)",
                 "fetched_on": pasted, "rows": n, "notes": notes})
    BM._write_csv(path, ["source", "url", "fetched_on", "rows", "notes"], rows)


if __name__ == "__main__":
    main()
