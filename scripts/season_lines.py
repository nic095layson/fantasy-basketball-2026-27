#!/usr/bin/env python3
"""Season lines: the pinned preseason line blended with the season's actuals (in-season tool; Council 2026-10-19
decision 8, 4-1; owner "proceed").

Rule, per player and category: a prior worth PRIOR_GAMES[c] games of the preseason line, plus every regular-season
game the player appeared in (data/actuals/<date>.json from box_pull.py; preseason and DNP lines excluded):

    counting cat   line = (k * pre + n * mean_actual) / (k + n)
    FG% / FT%      line = (k * pre_attempts * pre_pct + made) / (k * pre_attempts + attempts), attempts blended as counting

PRIOR_GAMES are derived, not tuned: k = n (1 - rho) / rho at n = SEASON_GAMES, rho the three-transition mean
year-over-year stability per category measured on 2022-23 through 2025-26 (after-report-2026-10-09-market.md,
"Year-over-year stability"; a category that carries less of itself across seasons earns a weaker prior). They are
judgment constants with a declared band (scripts/redteam/constants_registry.json, module season_lines) and a sweep.

The preseason line is never edited: report/projections-2026-27.csv (kit schema) and the deck's players_v69.csv
(deck schema) are read, and data/season/projections_season.csv and pool_season.csv are written beside a dated
movers record. The deck plane is the frozen snapshot followed by the kit's data/pool_additions.csv (in-season pickups
the draft pool never carried, deck schema; owner 2026-10-21, option (b)); a name already in the snapshot is refused.
Then the kit's data/tag_overrides.csv (owner 2026-10-22, D-RR-1, "Kit season override"): each row replaces one
player's leading note tag in the season pool, and is refused when the plane's tag is no longer the one it expects.
With no regular-season games and no overrides the outputs equal the inputs byte for byte (the snapshot, then the
additions' rows).

    python3 scripts/season_lines.py --date 2026-10-21 [--actuals data/actuals] [--out data/season] [--threshold 0.25]
Prints 'SEASON LINES: PASS — ...' and exits 0, or FAIL (an unreadable record) and exits 1.
"""
import argparse
import csv
import glob
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
DECK = os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball")
KIT_CSV = os.path.join(KIT, "report", "projections-2026-27.csv")
DECK_CSV = os.path.join(DECK, "arena", "results", "players_v69.csv")
ADDITIONS = os.path.join(KIT, "data", "pool_additions.csv")
OVERRIDES = os.path.join(KIT, "data", "tag_overrides.csv")
OVERRIDE_FIELDS = ["player", "tag_from", "tag_to", "decided", "receipt"]
ACTUALS = os.path.join(KIT, "data", "actuals")
OUT = os.path.join(KIT, "data", "season")
# Year-over-year Spearman rho, mean of the three transitions 2022-23..2025-26 (after-report-2026-10-09-market.md).
STABILITY = {"FG%": 0.714, "FT%": 0.634, "3PM": 0.872, "PTS": 0.848, "REB": 0.840, "AST": 0.847,
             "STL": 0.750, "BLK": 0.818, "TO": 0.823}
SEASON_GAMES = 65  # the games a full season of the stability sample carries (25+ game players; stated assumption)


def prior_games(rho, n=SEASON_GAMES):
    """Prior strength in games: rho = n / (n + k) solved for k."""
    return round(n * (1 - rho) / rho, 1)


PRIOR_GAMES = {c: prior_games(r) for c, r in STABILITY.items()}
# kit column -> (category, actuals total key); FGA/FTA blend as counting with the FG%/FT% priors
KIT_COLS = {"fga": ("FG%", "fga"), "fta": ("FT%", "fta"), "tpm": ("3PM", "tpm"), "pts": ("PTS", "pts"), "reb": ("REB", "reb"),
            "ast": ("AST", "ast"), "stl": ("STL", "stl"), "blk": ("BLK", "blk"), "tov": ("TO", "tov")}
DECK_COLS = dict(KIT_COLS)
DEC = {"fga": 1, "fta": 1, "tpm": 1, "pts": 1, "reb": 1, "ast": 1, "stl": 1, "blk": 1, "tov": 1}


def fold(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c) and c not in "'’`.").strip()


def note_tag(note):
    """Leading tag of a deck note, the deck's own rule (scripts/hoops.py note_tag): everything from the first space or
    parenthesis onward is prose."""
    return re.split(r"[\s(]", (note or "").lower(), 1)[0]


def load_actuals(folder=ACTUALS):
    recs = []
    for p in sorted(glob.glob(os.path.join(folder, "*.json"))):
        with open(p, encoding="utf-8") as f:
            recs.append(json.load(f))
    return recs


def totals(records):
    """Per player (pool name, else the source name flagged unpooled): regular-season games appeared in and the
    summed box cells."""
    out = {}
    for rec in records:
        regular = {g["espn_id"] for g in rec.get("games", []) if g.get("season_type") == 2}
        for p in rec.get("players", []):
            if p.get("dnp") or p.get("game") not in regular:
                continue
            key = p.get("pool_name") or p["name"]
            t = out.setdefault(key, dict(games=0, min=0, pts=0, fgm=0, fga=0, tpm=0, tpa=0, ftm=0, fta=0, reb=0, ast=0,
                                         tov=0, stl=0, blk=0, unpooled=p.get("pool_name") is None))
            t["games"] += 1
            for k in ("min", "pts", "fgm", "fga", "tpm", "tpa", "ftm", "fta", "reb", "ast", "tov", "stl", "blk"):
                t[k] += p.get(k, 0)
    return out


def _blend_counting(pre, t, col, cat):
    k, n = PRIOR_GAMES[cat], t["games"]
    return (k * pre + t[col]) / (k + n)


def _blend_pct(pre_pct, pre_att, t, made, att, cat):
    k = PRIOR_GAMES[cat]
    denom = k * pre_att + t[att]
    return (k * pre_att * pre_pct + t[made]) / denom if denom > 0 else pre_pct


def _apply(row, t, pct_cols, cols):
    if not t or t["games"] <= 0:
        return row
    out = dict(row)
    fg_col, ft_col = pct_cols
    out[fg_col] = f"{_blend_pct(float(row[fg_col]), float(row['fga']), t, 'fgm', 'fga', 'FG%'):.3f}"
    out[ft_col] = f"{_blend_pct(float(row[ft_col]), float(row['fta']), t, 'ftm', 'fta', 'FT%'):.3f}"
    for col, (cat, key) in cols.items():
        out[col] = f"{_blend_counting(float(row[col]), t, key, cat):.{DEC[col]}f}"
    return out


def blend_kit(row, t):
    return _apply(row, t, ("fgp", "ftp"), KIT_COLS)


def blend_deck(row, t):
    return _apply(row, t, ("fg_pct", "ft_pct"), DECK_COLS)


def _read(path):
    with open(path, encoding="utf-8", newline="") as f:
        r = csv.DictReader(f); return list(r), r.fieldnames


def _write(path, rows, fields):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n"); w.writeheader(); w.writerows(rows)


def _with_additions(deck_rows, deck_fields, additions_csv):
    if not additions_csv or not os.path.exists(additions_csv):
        return deck_rows
    adds, fields = _read(additions_csv)
    if fields != deck_fields:
        raise ValueError(f"{additions_csv}: columns {fields} differ from the deck plane's {deck_fields}")
    have = {fold(r["player"]) for r in deck_rows}
    dup = [a["player"] for a in adds if fold(a["player"]) in have]
    if dup:
        raise ValueError(f"already in the deck plane, remove from {additions_csv}: {', '.join(dup)}")
    return deck_rows + adds


def _with_tag_overrides(deck_rows, overrides_csv):
    """The deck plane with each override's leading tag swapped in; the prose after the tag is kept. Returns the rows
    and the overrides applied."""
    if not overrides_csv or not os.path.exists(overrides_csv):
        return deck_rows, []
    overrides, fields = _read(overrides_csv)
    if fields != OVERRIDE_FIELDS:
        raise ValueError(f"{overrides_csv}: columns {fields}, expected {OVERRIDE_FIELDS}")
    at = {fold(r["player"]): i for i, r in enumerate(deck_rows)}
    rows, applied = list(deck_rows), []
    for o in overrides:
        i = at.get(fold(o["player"]))
        if i is None:
            raise ValueError(f"{overrides_csv}: {o['player']} is not in the deck plane")
        tag, want, new = note_tag(rows[i]["note"]), o["tag_from"].strip().lower(), o["tag_to"].strip()
        if tag != want:
            raise ValueError(f"{overrides_csv}: {o['player']}'s leading tag is now '{tag}', the override expects '{want}'")
        if not new or note_tag(new) != new.lower():
            raise ValueError(f"{overrides_csv}: {o['player']}: tag_to '{new}' must be one tag token")
        if not o["decided"].strip():
            raise ValueError(f"{overrides_csv}: {o['player']}: an override needs its decided cell (date and decision)")
        rows[i] = dict(rows[i], note=new + f" [kit tag override {o['decided'].split()[0]}; data/tag_overrides.csv]"
                       + rows[i]["note"][len(tag):])
        applied.append(dict(player=rows[i]["player"], tag_from=tag, tag_to=new))
    return rows, applied


def run(date, actuals, kit_csv=KIT_CSV, deck_csv=DECK_CSV, out_dir=OUT, threshold=0.25, additions_csv=None,
        overrides_csv=None):
    tot = totals(actuals)
    by_fold = {fold(k): v for k, v in tot.items()}
    kit_rows, kit_fields = _read(kit_csv); deck_rows, deck_fields = _read(deck_csv)
    deck_rows = _with_additions(deck_rows, deck_fields, additions_csv)
    deck_rows, overridden = _with_tag_overrides(deck_rows, overrides_csv)
    movers, n_games = [], 0
    out_kit = []
    for r in kit_rows:
        t = by_fold.get(fold(r["name"]))
        b = blend_kit(r, t); out_kit.append(b)
        if t:
            n_games += 1
            moved = {c: (r[c], b[c]) for c in list(KIT_COLS) + ["fgp", "ftp"] if r[c] != b[c]}
            big = [c for c, (x, y) in moved.items() if abs(float(y) - float(x)) >= (0.01 if c in ("fgp", "ftp") else threshold)]
            if big:
                movers.append(dict(name=r["name"], games=t["games"], moved={c: moved[c] for c in big}))
    out_deck = [blend_deck(r, by_fold.get(fold(r["player"]))) for r in deck_rows]
    os.makedirs(out_dir, exist_ok=True)
    _write(os.path.join(out_dir, "projections_season.csv"), out_kit, kit_fields)
    _write(os.path.join(out_dir, "pool_season.csv"), out_deck, deck_fields)
    rec = dict(date=date, records=len(actuals), players_with_games=n_games, prior_games=PRIOR_GAMES, season_games=SEASON_GAMES,
               threshold=threshold, movers=sorted(movers, key=lambda m: -m["games"]),
               unpooled_with_games=sorted(k for k, v in tot.items() if v["unpooled"]), tag_overrides=overridden,
               inputs=dict(kit=os.path.relpath(kit_csv, KIT), deck=deck_csv,
                           additions=os.path.relpath(additions_csv, KIT) if additions_csv and os.path.exists(additions_csv) else None,
                           overrides=os.path.relpath(overrides_csv, KIT) if overrides_csv and os.path.exists(overrides_csv) else None))
    with open(os.path.join(out_dir, f"season_lines_{date}.json"), "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1, ensure_ascii=False); f.write("\n")
    return rec


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", required=True)
    ap.add_argument("--actuals", default=ACTUALS)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--threshold", type=float, default=0.25)
    a = ap.parse_args()
    try:
        recs = load_actuals(a.actuals)
    except ValueError as e:
        print(f"SEASON LINES: FAIL — unreadable actuals record: {e}"); return 1
    try:
        rec = run(a.date, recs, out_dir=a.out, threshold=a.threshold, additions_csv=ADDITIONS, overrides_csv=OVERRIDES)
    except ValueError as e:
        print(f"SEASON LINES: FAIL — pool additions or tag overrides: {e}"); return 1
    print(f"SEASON LINES: PASS — {a.date}: {rec['records']} box-score records, {rec['players_with_games']} pool players with "
          f"regular-season games, {len(rec['movers'])} lines moved by {a.threshold}+ (priors in games: "
          + ", ".join(f"{c} {k}" for c, k in PRIOR_GAMES.items()) + f"); {len(rec['unpooled_with_games'])} unpooled players with games; {len(rec['tag_overrides'])} tag override(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
