#!/usr/bin/env python3
"""GP reconstruction test (owner 2026-10-22 "Test, then weekly"): rebuild each team-week's games played (Yahoo's
"Games Played" tracker) from the week-start roster and the players' 2025-26 game logs, and score it against the 44
known values in the deck's arena/data/weekly_matchups_2025-26.csv.

Method, stated to the owner before the run (2026-10-22):
  roster   the Flaim get_roster snapshot on the matchup week's first day (rosters/), held for the whole week
           (in-week adds, drops and IL returns are invisible: Yahoo transactions reach back only 30 days)
  IL       a player in an IL or IL+ slot on that day counts for nothing all week
  played   a player played on a day when his Basketball-Reference regular-season log has a row for it (a row needs
           a points cell, so did-not-play rows are out); a name with no 2025-26 game counts none
  lineup   each day, the players who played fill the ten active slots (PG SG G SF PF F C C Util Util) by their Yahoo
           eligibility, as many as can be seated (a maximum matching): a perfect daily manager, bench included
  GP       the sum over the week's days of the players seated
  verdict  PASS when, over all 44 team-weeks, mean |reconstructed - known| <= 1.5 and |mean (reconstructed - known)|
           <= 0.75; otherwise FAIL. No parameter is fit to the 44 values.
  also     reported, not part of the verdict: the same two figures without week 17 (14 days on one snapshot), the
           owner's rows against the opponents', and each row's uncapped roster games (the ceiling's ceiling)
Writes reconstruction_2025-26.json beside itself."""
import csv, datetime as dt, glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TRUTH = os.path.join(KIT, "..", "yahoo-fantasy-basketball", "arena", "data", "weekly_matchups_2025-26.csv")
PRIOR = os.path.join(HERE, "..", "zscore-assessment-2026-10-21", "gamelogs", "gamelogs_2025-26.csv")
EXTRA = os.path.join(HERE, "gamelogs_extra_2025-26.csv")
SLOTS = ["PG", "SG", "G", "SF", "PF", "F", "C", "C", "Util", "Util"]
TAKES = {"PG": {"PG"}, "SG": {"SG"}, "G": {"PG", "SG"}, "SF": {"SF"}, "PF": {"PF"}, "F": {"SF", "PF"}, "C": {"C"},
         "Util": {"PG", "SG", "SF", "PF", "C"}}
IL = {"IL", "IL+"}
MAE_BAR, BIAS_BAR = 1.5, 0.75
sys.path.insert(0, HERE)
from extract_rosters import TEAM, week_start  # noqa: E402


def week_end(dates):
    m, d = (int(x) for x in dates.split("-")[1].split("/"))
    return dt.date(2025 if m >= 10 else 2026, m, d)


def seat(eligibilities, slots=SLOTS):
    """Most players seatable: eligibilities is one set of positions per player; returns the matching size."""
    owner = [None] * len(slots)

    def place(i, seen):
        for s, name in enumerate(slots):
            if s in seen or not (TAKES[name] & eligibilities[i]):
                continue
            seen.add(s)
            if owner[s] is None or place(owner[s], seen):
                owner[s] = i
                return True
        return False
    return sum(1 for i in range(len(eligibilities)) if place(i, set()))


def load_days():
    man = json.load(open(os.path.join(HERE, "logs_manifest.json"), encoding="utf-8"))
    days = {}
    for path in (PRIOR, EXTRA):
        for r in csv.DictReader(open(path, encoding="utf-8")):
            days.setdefault(r["bref_id"], set()).add(r["date"])
    return man, days


def team_week(roster, start, end, ids, days):
    active = [p for p in roster["players"] if p["selectedPosition"] not in IL]
    elig = {p["name"]: set(p["position"].split(",")) for p in active}
    gp = uncapped = unseated = 0
    d = start
    while d <= end:
        iso = d.isoformat()
        playing = [n for n in elig if iso in days.get(ids.get(n), ())]
        s = seat([elig[n] for n in playing])
        gp += s; uncapped += len(playing); unseated += len(playing) - s
        d += dt.timedelta(days=1)
    return dict(gp=gp, uncapped=uncapped, unseated=unseated, active=len(active), il=len(roster["players"]) - len(active))


def summary(rows):
    e = [r["error"] for r in rows]
    return dict(n=len(e), mae=round(sum(abs(x) for x in e) / len(e), 3), bias=round(sum(e) / len(e), 3))


def main():
    man, days = load_days()
    ids = man["resolved"]
    rows = []
    for r in csv.DictReader(open(TRUTH, encoding="utf-8")):
        start, end, tid = week_start(r["dates"]), week_end(r["dates"]), TEAM[r["manager"]]
        roster = json.load(open(os.path.join(HERE, "rosters", f"t{tid:02d}_{start.isoformat()}.json"), encoding="utf-8"))
        tw = team_week(roster, start, end, ids, days)
        rows.append(dict(week=int(r["week"]), manager=r["manager"], team_id=tid, start=start.isoformat(), end=end.isoformat(),
                         days=(end - start).days + 1, known=int(r["gp"]), reconstructed=tw["gp"],
                         error=tw["gp"] - int(r["gp"]), uncapped=tw["uncapped"], unseated=tw["unseated"],
                         active=tw["active"], il=tw["il"]))
    allr = summary(rows)
    verdict = "PASS" if allr["mae"] <= MAE_BAR and abs(allr["bias"]) <= BIAS_BAR else "FAIL"
    rec = dict(method="reconstruct.py docstring (stated to the owner before the run)", bar=dict(mae=MAE_BAR, bias=BIAS_BAR),
               verdict=verdict, all=allr, without_week17=summary([r for r in rows if r["week"] != 17]),
               owner_rows=summary([r for r in rows if r["manager"] == "David"]),
               opponent_rows=summary([r for r in rows if r["manager"] != "David"]),
               worst=sorted(rows, key=lambda r: -abs(r["error"]))[:5], rows=rows)
    with open(os.path.join(HERE, "reconstruction_2025-26.json"), "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1); f.write("\n")
    print(f"RECONSTRUCTION: {verdict} — {allr['n']} team-weeks, MAE {allr['mae']} (bar {MAE_BAR}), bias {allr['bias']:+} (bar ±{BIAS_BAR})")
    for k in ("without_week17", "owner_rows", "opponent_rows"):
        print(f"  {k}: MAE {rec[k]['mae']}, bias {rec[k]['bias']:+} (n {rec[k]['n']})")
    print("  worst: " + "; ".join(f"wk{r['week']} {r['manager']} {r['reconstructed']} vs {r['known']}" for r in rec["worst"]))


if __name__ == "__main__":
    main()
