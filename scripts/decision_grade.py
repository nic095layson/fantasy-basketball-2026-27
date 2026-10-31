#!/usr/bin/env python3
"""The decision log's grader (owner 2026-10-31; red team of the same day, slice 1).

For every recommendation in data/decisions/recommendations.jsonl and session.jsonl, and the owner's move that
matched it (data/decisions/moves.jsonl), the grade is the kit's own in-season value: each player's z_adj on the
season board (report/season/board_<date>.json, the lines the box scores have been blended into) at the window's
end, add minus drop. The window opens on the move date (an exact or add-match move) or the recommendation date and
runs WINDOW_DAYS. Box-score games and totals over the window (data/actuals/<date>.json) are reported beside the
verdict and never decide it: the red team measured per-game z noise at sd 3.65 against a 0.5 line, so a sum of
box scores cannot resolve a pair inside a season; the board's blended line can.

Verdict words, fixed before the first grade (method parameters, stated to the owner before the first grade):
  KIT RIGHT   add − drop  >  +LINE on the window-end board          KIT WRONG  < −LINE          TOO CLOSE between
  OWNER BETTER / KIT BETTER / TOO CLOSE on the owner's pair minus the kit's pair, same line, when the drop differs
  PENDING     the window has not elapsed as of the grading date, or either player has fewer than MIN_GAMES games
  HOLD        a hold row; not graded in slice 1 (the free-agent-set-aside comparison is slice 2)

Final verdicts append to report/decisions/grades.jsonl (one row per recommendation per window end, with each input
file's sha256, never rewritten); report/decisions/scorecard.md is regenerated from the ledger plus the pending rows.

    python3 scripts/decision_grade.py --as-of 2026-11-30 [--dry-run]
"""
import argparse
import csv
import datetime as dt
import glob
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import box_pull  # noqa: E402
import decision_log as DL  # noqa: E402

WINDOW_DAYS = 28    # the grading window, days from the move (or the recommendation)
LINE = 0.5          # the verdict line on z_adj, add minus drop (and owner's pair minus kit's pair)
MIN_GAMES = 10      # fewer games than this for either player in the window → PENDING, never a verdict
BOARDS = os.path.join(KIT, "report", "season")
ACTUALS = os.path.join(KIT, "data", "actuals")
OUTDIR = os.path.join(KIT, "report", "decisions")
GRADES = os.path.join(OUTDIR, "grades.jsonl")
SCORECARD = os.path.join(OUTDIR, "scorecard.md")
STATS = ("min", "pts", "reb", "ast", "stl", "blk", "tov", "tpm", "fgm", "fga", "ftm", "fta")


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def board_on(date, boards=BOARDS):
    """The newest board dated on or before `date`: (date, path) or (None, None)."""
    hits = sorted((os.path.basename(p)[6:16], p) for p in glob.glob(os.path.join(boards, "board_*.json"))
                  if os.path.basename(p)[6:16] <= date)
    return hits[-1] if hits else (None, None)


def board_values(path, aliases=None):
    """{board name: z_adj} and the name index (alias table + suffix-free keys) the ledgers' spellings resolve through."""
    b = json.load(open(path, encoding="utf-8"))
    vals = {r["name"]: r["z_adj"] for r in b["board"]}
    return vals, box_pull.name_index(list(vals), aliases if aliases is not None else box_pull.load_aliases())


def value(name, vals, index):
    hit = box_pull.match_name(name, index) if name else None
    return (vals.get(hit), hit) if hit else (None, None)


def games_in(name, start, end, actuals=ACTUALS, aliases=None):
    """(games played, team games, totals) for `name` over [start, end] from the box files on disk; a day with no file
    is not a game (the count is on the files, named in `days`)."""
    index = None
    played, team_games, tot, days, team = 0, 0, {k: 0.0 for k in STATS}, [], None
    for p in sorted(glob.glob(os.path.join(actuals, "*.json"))):
        d = os.path.basename(p)[:10]
        if not (start <= d <= end):
            continue
        try:
            a = json.load(open(p, encoding="utf-8"))
        except (OSError, ValueError):
            continue
        rows = a.get("players") or []
        days.append(d)
        if index is None:
            names = sorted({r["pool_name"] for r in rows if r.get("pool_name")})
            index = box_pull.name_index(names, aliases if aliases is not None else box_pull.load_aliases())
        hit = box_pull.match_name(name, index) if name else None
        mine = [r for r in rows if hit and r.get("pool_name") == hit]
        if mine:
            team = mine[0].get("team") or team
        if team and any(r.get("team") == team for r in rows):
            team_games += 1
        for r in mine:
            if not r.get("dnp") and (r.get("min") or 0) > 0:
                played += 1
                for k in STATS:
                    tot[k] += float(r.get(k) or 0)
    return played, team_games, {k: round(v, 1) for k, v in tot.items()}, days


def verdict_word(gap, line=LINE):
    return "KIT RIGHT" if gap > line else "KIT WRONG" if gap < -line else "TOO CLOSE"


def owner_word(diff, line=LINE):
    return "OWNER BETTER" if diff > line else "KIT BETTER" if diff < -line else "TOO CLOSE"


def grade(rec, moves, as_of, boards=BOARDS, actuals=ACTUALS, window=WINDOW_DAYS, line=LINE, min_games=MIN_GAMES, aliases=None):
    """One grade row for a recommendation as of `as_of` (ISO date). Never raises on a missing input: the row says
    what is missing and stays PENDING."""
    row = {"rec": rec["id"], "source": rec.get("source"), "kind": rec.get("kind"), "rec_date": rec["date"],
           "kit_add": rec.get("add"), "kit_drop": rec.get("drop"), "d_title_at_rec": (rec.get("basis") or {}).get("d_title"),
           "as_of": as_of, "window_days": window, "line": line, "min_games": min_games, "inputs": {}}
    if rec.get("kind") == "hold":
        row.update(verdict="HOLD", note="hold rows are not graded in slice 1")
        return row
    mv = next((m for m in moves if m.get("matches") == rec["id"] and m.get("match_kind") in ("exact", "add_match_drop_differs")), None)
    start = mv["date"] if mv else rec["date"]
    end = (dt.date.fromisoformat(start) + dt.timedelta(days=window)).isoformat()
    row.update(window=[start, end], move=mv and {"id": mv["id"], "added": mv["added"], "dropped": mv["dropped"], "match_kind": mv["match_kind"]})
    elapsed = as_of >= end
    bdate, bpath = board_on(min(end, as_of), boards)
    sdate, spath = board_on(start, boards)
    if not bpath:
        row.update(verdict="PENDING", note=f"no season board on or before {min(end, as_of)}")
        return row
    row["inputs"]["board_end"] = {"date": bdate, "file": os.path.relpath(bpath, KIT), "sha256": sha(bpath)}
    if spath:
        row["inputs"]["board_start"] = {"date": sdate, "file": os.path.relpath(spath, KIT), "sha256": sha(spath)}
    aliases = aliases if aliases is not None else box_pull.load_aliases()
    vals, index = board_values(bpath, aliases)
    svals, sindex = board_values(spath, aliases) if spath else ({}, ({}, {}))
    owner_drop = (mv["dropped"][0] if mv and mv.get("dropped") else None) if mv and mv["match_kind"] == "add_match_drop_differs" else None
    players = {"kit_add": rec.get("add"), "kit_drop": rec.get("drop"), "owner_drop": owner_drop}
    pv, missing, games = {}, [], {}
    for role, name in players.items():
        if not name:
            continue
        v, hit = value(name, vals, index)
        v0, _ = value(name, svals, sindex) if spath else (None, None)
        g, tg, tot, days = games_in(name, start, min(end, as_of), actuals, aliases)
        pv[role] = {"name": name, "board_name": hit, "z_adj_end": v, "z_adj_start": v0}
        games[role] = {"name": name, "games": g, "team_games": tg, "totals": tot}
        if v is None:
            missing.append(name)
    row.update(values=pv, games=games, box_days=len(days) if players.get("kit_add") else 0)
    if missing:
        row.update(verdict="PENDING", note=f"not on the {bdate} board: {', '.join(missing)}")
        return row
    gap_end = pv["kit_add"]["z_adj_end"] - pv["kit_drop"]["z_adj_end"]
    gap_start = (pv["kit_add"]["z_adj_start"] - pv["kit_drop"]["z_adj_start"]
                 if pv["kit_add"]["z_adj_start"] is not None and pv["kit_drop"]["z_adj_start"] is not None else None)
    row.update(kit_gap_end=round(gap_end, 3), kit_gap_start=None if gap_start is None else round(gap_start, 3))
    if owner_drop:
        og = pv["kit_add"]["z_adj_end"] - pv["owner_drop"]["z_adj_end"]
        row.update(owner_gap_end=round(og, 3), owner_minus_kit=round(og - gap_end, 3))
    short = [g["name"] for g in games.values() if g["games"] < min_games]
    if not elapsed:
        row.update(verdict="PENDING", note=f"window open until {end}; as of {as_of} the gap is {gap_end:+.2f}")
    elif short:
        row.update(verdict="PENDING", note=f"fewer than {min_games} games in the window: {', '.join(short)}")
    else:
        row["verdict"] = verdict_word(gap_end, line)
        if owner_drop:
            row["owner_verdict"] = owner_word(row["owner_minus_kit"], line)
    return row


def final(row):
    return row.get("verdict") not in (None, "PENDING", "HOLD")


def scorecard(rows, ledger_rows, as_of):
    """The Markdown scorecard: the running tally over the ledger's final rows, then every recommendation."""
    fin = [r for r in ledger_rows]
    kit = [r for r in fin if r.get("verdict") in ("KIT RIGHT", "KIT WRONG", "TOO CLOSE")]
    own = [r for r in fin if r.get("owner_verdict")]
    L = [f"# Decision scorecard — as of {as_of}", "",
         f"Method: z_adj on the season board at the window's end, add minus drop; window {WINDOW_DAYS} days; verdict line ±{LINE}; "
         f"fewer than {MIN_GAMES} games for either player → PENDING. Box-score games and totals are shown beside each verdict and never decide it.", "",
         "| scorer | graded | KIT RIGHT | KIT WRONG | TOO CLOSE | OWNER BETTER | KIT BETTER | owner TOO CLOSE |", "|---|---|---|---|---|---|---|---|",
         f"| kit vs its own drop | {len(kit)} | {sum(r['verdict'] == 'KIT RIGHT' for r in kit)} | {sum(r['verdict'] == 'KIT WRONG' for r in kit)} | "
         f"{sum(r['verdict'] == 'TOO CLOSE' for r in kit)} | {sum(r['owner_verdict'] == 'OWNER BETTER' for r in own)} | "
         f"{sum(r['owner_verdict'] == 'KIT BETTER' for r in own)} | {sum(r['owner_verdict'] == 'TOO CLOSE' for r in own)} |", "",
         "| rec | source | kit said | owner did | window | kit gap (end) | owner − kit | games add / drop | verdict |", "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        mv = r.get("move")
        did = f"+{', '.join(mv['added'])} −{', '.join(mv['dropped']) or '-'}" if mv else "no matching move"
        g = r.get("games") or {}
        gs = f"{g.get('kit_add', {}).get('games', '-')} / {g.get('kit_drop', {}).get('games', '-')}" if g else "-"
        kg = "-" if r.get("kit_gap_end") is None else f"{r['kit_gap_end']:+.2f}"
        ok = "-" if r.get("owner_minus_kit") is None else f"{r['owner_minus_kit']:+.2f}"
        said = f"+{r.get('kit_add')} −{r.get('kit_drop')}" if r.get("kind") != "hold" and r.get("kit_add") else "hold"
        v = r.get("verdict", "") + (f" / {r['owner_verdict']}" if r.get("owner_verdict") else "")
        w = " to ".join(r.get("window") or []) or "-"
        L.append(f"| {r['rec']} | {r['source']} | {said} | {did} | {w} | {kg} | {ok} | {gs} | {v}{(' (' + r['note'] + ')') if r.get('note') else ''} |")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--as-of", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true", help="print every grade; write nothing")
    ap.add_argument("--dir", default=DL.DIR); ap.add_argument("--boards", default=BOARDS); ap.add_argument("--actuals", default=ACTUALS)
    ap.add_argument("--out", default=OUTDIR)
    a = ap.parse_args(argv)
    recs = DL.recommendations(os.path.join(a.dir, "recommendations.jsonl"), os.path.join(a.dir, "session.jsonl"))
    moves = DL.read(os.path.join(a.dir, "moves.jsonl"))
    rows = [grade(r, moves, a.as_of, a.boards, a.actuals) for r in recs]
    grades_path, card_path = os.path.join(a.out, "grades.jsonl"), os.path.join(a.out, "scorecard.md")
    ledger = DL.read(grades_path)
    have = {(g["rec"], tuple(g.get("window") or [])) for g in ledger}
    new = [r for r in rows if final(r) and (r["rec"], tuple(r["window"])) not in have]
    for r in rows:
        print(f"  {r['rec']:<18} {r.get('verdict', ''):<12} {r.get('kit_add') or '-'} for {r.get('kit_drop') or '-'}"
              f"  gap {r.get('kit_gap_end') if r.get('kit_gap_end') is not None else '-'}  {r.get('note', '')}")
    if a.dry_run:
        print(f"DECISION GRADE: DRY RUN {len(rows)} rows, {len(new)} final (not written)")
        return 0
    os.makedirs(a.out, exist_ok=True)
    for r in new:
        r["graded_at"] = DL.now()
    with open(grades_path, "a", encoding="utf-8") as f:
        for r in new:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(card_path, "w", encoding="utf-8") as f:
        f.write(scorecard(rows, ledger + new, a.as_of))
    print(f"DECISION GRADE: PASS {len(rows)} rows, {len(new)} new final, {sum(r.get('verdict') == 'PENDING' for r in rows)} pending; "
          f"wrote {os.path.relpath(card_path, KIT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
