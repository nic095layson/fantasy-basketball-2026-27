#!/usr/bin/env python3
"""D-GP-3 record (owner 2026-10-22, "Weekly totals only"): checks the pinned Yahoo weekly totals of three older seasons
(data/source/flaim/history/<league>/matchups_weekNN.json, raw Flaim get_matchups responses pinned by
scripts/flaim_live.py --history) without trusting Yahoo's own verdicts:

  1. every week of the season is on disk, its header names the league and the week, scoring is categories;
  2. every matchup is final, with no games remaining, both teams inside the league's 12 and no team twice in a week;
  3. every side carries the same 11 categories in Yahoo's order (FGM/A, FG%, FTM/A, FT%, 3PTM, PTS, REB, AST, ST, BLK, TO);
  4. each of the nine scored categories is decided again from the totals (FG% and FT% from makes and attempts, TO lower
     wins) and must equal Yahoo's result on both sides, and the side's wins-losses-ties must equal Yahoo's categoryScore;
  5. each team's regular-season record summed from its matchups must equal Yahoo's standings file for that season.

It reads only the pinned files and writes verify_record.json beside itself. Exit 0 only when nothing failed."""
import json
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
ROOT = os.path.join(KIT, "data", "source", "flaim", "history")
SEASONS = {"454.l.115080": ("2024-25", 21), "428.l.39018": ("2023-24", 23), "418.l.131270": ("2022-23", 21)}
CATS = ["FGM/A", "FG%", "FTM/A", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]
SCORED = ["FG%", "FT%", "3PTM", "PTS", "REB", "AST", "ST", "BLK", "TO"]
WORD = {"win": "wins", "loss": "losses", "tie": "ties"}
FLIP = {"win": "loss", "loss": "win", "tie": "tie"}


def value(cats, k, fails, tag):
    if k in ("FG%", "FT%"):
        made, att = map(int, cats["FGM/A" if k == "FG%" else "FTM/A"]["value"].split("/"))
        if att and abs(float(cats[k]["value"]) - made / att) > 0.0005 + 1e-9:
            fails.append(f"{tag}: {k} shown {cats[k]['value']} is not {made}/{att} rounded")
        return Fraction(made, att) if att else Fraction(0)
    v = int(cats[k]["value"])
    return -v if k == "TO" else v


def check(root=ROOT):
    fails, seasons = [], {}
    for lk, (label, nweeks) in SEASONS.items():
        d = os.path.join(root, lk)
        files = sorted(f for f in os.listdir(d) if f.startswith("matchups_week"))
        if files != [f"matchups_week{w:02d}.json" for w in range(1, nweeks + 1)]:
            fails.append(f"{lk}: {len(files)} week files on disk, expected weeks 1-{nweeks}")
        per_week, n_m, n_cells, record, regular = [], 0, 0, {}, []
        for f in files:
            wk = int(f[13:15])
            data = json.load(open(os.path.join(d, f), encoding="utf-8"))
            if data.get("leagueKey") != lk or int(data.get("matchupWeek")) != wk or data.get("scoringType") != "categories":
                fails.append(f"{lk} {f}: header {data.get('leagueKey')} week {data.get('matchupWeek')} {data.get('scoringType')}")
            ms = data["matchups"]
            per_week.append(len(ms))
            is_regular = len(ms) == 6
            if is_regular:
                regular.append(wk)
            seen = []
            for m in ms:
                n_m += 1
                tag = f"{label} week {wk} matchup {m.get('matchupId')}"
                if m.get("status") != "final" or int(m.get("week")) != wk:
                    fails.append(f"{tag}: status {m.get('status')}, week {m.get('week')}")
                sides = {}
                for s in ("home", "away"):
                    t = m[s]
                    tid = int(t["teamId"])
                    seen.append(tid)
                    if not 1 <= tid <= 12 or t["teamKey"] != f"{lk}.t.{tid}":
                        fails.append(f"{tag} {s}: team {t['teamKey']}")
                    if t.get("gamesRemaining") not in (0, None):
                        fails.append(f"{tag} {s}: {t.get('gamesRemaining')} games remaining")
                    names = [c["displayName"] for c in t["categories"]]
                    if names != CATS:
                        fails.append(f"{tag} {s}: categories {names}")
                    sides[s] = (t, {c["displayName"]: c for c in t["categories"]}, {"wins": 0, "losses": 0, "ties": 0})
                (h, hc, hs), (a, ac, as_) = sides["home"], sides["away"]
                for k in SCORED:
                    n_cells += 1
                    hv, av = value(hc, k, fails, tag), value(ac, k, fails, tag)
                    r = "win" if hv > av else "loss" if hv < av else "tie"
                    if hc[k]["result"] != r or ac[k]["result"] != FLIP[r]:
                        fails.append(f"{tag} {k}: totals say {r}/{FLIP[r]}, Yahoo {hc[k]['result']}/{ac[k]['result']}")
                    hs[WORD[r]] += 1
                    as_[WORD[FLIP[r]]] += 1
                for t, _, sc in (sides["home"], sides["away"]):
                    if t["categoryScore"] != sc or t.get("points") != sc["wins"]:
                        fails.append(f"{tag} team {t['teamId']}: totals give {sc}, Yahoo {t['categoryScore']} (points {t.get('points')})")
                    if is_regular:
                        rec = record.setdefault(t["teamId"], [0, 0, 0])
                        rec[0] += t["categoryScore"]["wins"]
                        rec[1] += t["categoryScore"]["losses"]
                        rec[2] += t["categoryScore"]["ties"]
            if len(set(seen)) != len(seen):
                fails.append(f"{label} week {wk}: a team appears twice")
        standings = json.load(open(os.path.join(d, "standings.json"), encoding="utf-8"))["standings"]
        agree = 0
        for t in standings:
            got = record.get(t["teamId"])
            if got == [int(t["wins"]), int(t["losses"]), int(t["ties"])]:
                agree += 1
            else:
                fails.append(f"{label} team {t['teamId']}: standings {t['wins']}-{t['losses']}-{t['ties']}, summed matchups {got}")
        seasons[label] = {"league_key": lk, "weeks": len(files), "matchups": n_m, "category_results_recomputed": n_cells,
                          "matchups_per_week": per_week, "regular_season_weeks": [regular[0], regular[-1]] if regular else None,
                          "standings_records_agree": f"{agree}/{len(standings)}"}
    return {"seasons": seasons, "fails": fails, "verdict": "PASS" if not fails else "FAIL"}


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else ROOT
    rec = check(root)
    if root == ROOT:
        with open(os.path.join(HERE, "verify_record.json"), "w", encoding="utf-8") as f:
            json.dump(rec, f, indent=1, ensure_ascii=False)
            f.write("\n")
    for label, s in rec["seasons"].items():
        print(f"{label} ({s['league_key']}): {s['weeks']} weeks, {s['matchups']} matchups, "
              f"{s['category_results_recomputed']} category results recomputed, standings {s['standings_records_agree']}")
    print(f"HISTORY TOTALS: {rec['verdict']} — {len(rec['fails'])} failure(s)")
    for x in rec["fails"][:40]:
        print("  " + x)
    return 0 if not rec["fails"] else 1


if __name__ == "__main__":
    sys.exit(main())
