#!/usr/bin/env python3
"""Every fact the next-level proposal (after-report-2026-10-22-next-level.md) cites from a record, written by script so
no count is retyped. Inputs: this kit checkout (main), the season/daily records at e7b69bb (the 14:44Z morning run of
10/22: the brief, the calibration ledger, the week card, data/weeks), the deck at 048efb6 (the league simulator) and the
pinned Flaim samples beside this file (pin.py).

    python3 report/after-reports/next-level-2026-10-22/facts.py --records <kit worktree at e7b69bb> --deck <deck at 048efb6>

Writes facts.json beside itself.
"""
import argparse
import collections
import csv
import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
RECORDS_COMMIT, DECK_COMMIT, DATE = "e7b69bb", "048efb6", "2026-10-22"


def head(path):
    return subprocess.run(["git", "-C", path, "rev-parse", "--short=7", "HEAD"], capture_output=True, text=True,
                          check=True).stdout.strip()


def grep(path, pattern):
    """(line number, line) of every line matching pattern: the receipt for a claim about code."""
    with open(path, encoding="utf-8") as f:
        return [(i, ln.rstrip("\n")) for i, ln in enumerate(f, 1) if re.search(pattern, ln)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", required=True)
    ap.add_argument("--deck", required=True)
    a = ap.parse_args()
    assert head(a.records) == RECORDS_COMMIT, f"records at {head(a.records)}, not {RECORDS_COMMIT}"
    assert head(a.deck) == DECK_COMMIT, f"deck at {head(a.deck)}, not {DECK_COMMIT}"
    R = lambda *p: os.path.join(a.records, *p)  # noqa: E731
    out = dict(records_commit=RECORDS_COMMIT, deck_commit=DECK_COMMIT, kit_commit=head(KIT))

    # the NBA schedule by Yahoo week: games per NBA team, and the league's own weeks (settings: 17 regular, 18-20 playoffs)
    weeks, dates = collections.defaultdict(collections.Counter), collections.defaultdict(set)
    with open(os.path.join(KIT, "report", "schedule", "games-2026-27.csv"), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        w = int(r["yahoo_week"])
        weeks[w][r["visitor"]] += 1
        weeks[w][r["home"]] += 1
        dates[w].add(r["date"])
    out["schedule"] = dict(games=len(rows), weeks={w: dict(first=min(dates[w]), last=max(dates[w]),
                                                           teams_by_games=dict(sorted(collections.Counter(weeks[w].values()).items())))
                                                   for w in sorted(weeks) if w <= 20})

    settings = json.load(open(os.path.join(KIT, "data", "league_settings.json"), encoding="utf-8"))
    out["settings"] = {k: settings[k]["value"] for k in ("max_acquisitions_per_week", "roster_positions", "playoffs",
                                                          "regular_season_weeks", "waivers", "lineup_deadline")}
    out["league_schedule_scope"] = json.load(open(os.path.join(KIT, "data", "league_schedule.json"), encoding="utf-8"))["_source"]["scope"]

    # the red-team registry: every judgment constant with its status and the decision that would calibrate it
    reg = json.load(open(os.path.join(KIT, "scripts", "redteam", "constants_registry.json"), encoding="utf-8"))["constants"]
    out["registry"] = dict(counts=dict(collections.Counter(c["status"] for c in reg)),
                           open=[dict(name=c["name"], status=c["status"], decision=c.get("decision", ""))
                                 for c in reg if c["status"] in ("uncalibrated", "declared_band")])

    # the morning records: what the brief keeps, what the ledger holds, what the scoreboard intake has
    brief = json.load(open(R("report", "briefs", f"brief_{DATE}.json"), encoding="utf-8"))
    out["brief"] = dict(keys=sorted(brief), title=brief["title"], playoffs=brief["playoffs"], seasons=brief["seasons"],
                        lines=brief["lines"], streaming=brief["streaming"], waiver_pairs_scored=brief["waiver_pairs_scored"])
    cal = json.load(open(R("report", "calibration.json"), encoding="utf-8"))
    out["calibration"] = {w: dict(recorded_at=v.get("recorded_at"), scored=("won" in v or "brier" in v))
                          for w, v in cal["weeks"].items()}
    out["data_weeks"] = sorted(os.listdir(R("data", "weeks")))
    wm = json.load(open(R("report", "briefs", f"week_matchup_{DATE}.json"), encoding="utf-8"))
    out["week_card"] = dict(keys=sorted(wm), pickups=len(wm.get("pickups") or []))

    # the owner's roster in the morning pull (Flaim get_roster, team 11), by Yahoo slot
    pull = json.load(open(R("data", "source", "flaim", f"pull_{DATE}.json"), encoding="utf-8"))
    mine = pull["rosters"]["478.l.36464.t.11"]["players"]
    out["owner_roster"] = dict(players=len(mine), slots=dict(collections.Counter(p.get("selectedPosition") for p in mine)),
                               roster_spots=len(settings["roster_positions"]["value"]))

    # Yahoo's week-2 gamesRemaining (pinned at 16:19Z) against each roster's NBA games that week (morning pull, schedule
    # file through the kit's Basketball-Reference -> Yahoo code map): is Yahoo's count all rostered players' games?
    os.environ["DECK_REPO"] = a.deck
    import sys
    sys.path.insert(0, os.path.join(KIT, "scripts"))
    import co_gm  # noqa: E402
    g2 = collections.Counter()
    for r in rows:
        if r["yahoo_week"] == "2":
            for t in (r["visitor"], r["home"]):
                g2[co_gm.TEAM_CODE.get(t, t)] += 1
    y2 = {s["teamName"]: s["gamesRemaining"] for x in json.load(open(os.path.join(HERE, "flaim_samples.json"), encoding="utf-8"))
          ["matchups_week2"]["matchups"] for s in (x["home"], x["away"])}
    out["week2_games_check"] = {r["teamName"]: dict(
        yahoo=y2.get(r["teamName"]),
        all_rostered=sum(g2.get(p.get("team"), 0) for p in r["players"]),
        non_il=sum(g2.get(p.get("team"), 0) for p in r["players"] if p.get("selectedPosition") not in ("IL", "IL+")),
        active_slots=sum(g2.get(p.get("team"), 0) for p in r["players"] if p.get("selectedPosition") not in ("IL", "IL+", "BN")),
        unknown_codes=sorted({p.get("team") for p in r["players"] if p.get("team") not in g2}))
        for r in pull["rosters"].values()}
    chk = out["week2_games_check"]
    out["week2_games_definitions"] = {d: sorted(t for t, v in chk.items() if v[d] == v["yahoo"])
                                      for d in ("all_rostered", "non_il", "active_slots")}

    # the code receipts: which lines the title simulation runs on, and what the simulator takes as input
    out["receipts"] = dict(
        co_gm_lines_tag=grep(os.path.join(KIT, "scripts", "co_gm.py"), r'^LINES_TAG\s*='),
        co_gm_sim_call=grep(os.path.join(KIT, "scripts", "co_gm.py"), r'league_sim\.py'),
        league_sim_argv=grep(os.path.join(a.deck, "arena", "mocks", "league_sim.py"), r'sys\.argv'),
        league_sim_data_path=grep(os.path.join(a.deck, "arena", "mocks", "league_sim.py"), r'DATA_PATH'),
        league_sim_team_record=grep(os.path.join(a.deck, "arena", "mocks", "league_sim.py"), r'out\["teams"\]\[i\] = dict'),
        week_matchup_m5=grep(os.path.join(KIT, "scripts", "week_matchup.py"), r'M5 leader'),
        week_matchup_m6=grep(os.path.join(KIT, "scripts", "week_matchup.py"), r'M6 drop'),
        co_gm_free_agents=grep(os.path.join(KIT, "scripts", "co_gm.py"), r'^def free_agents|^def streaming'),
        scoreboard_input=grep(os.path.join(KIT, "scripts", "scoreboard_intake.py"), r'The owner fills it'),
        team_week_games=grep(os.path.join(a.deck, "arena", "arena.py"), r'^\s+g = 3\.5 \* a'),
        pcat=grep(os.path.join(KIT, "scripts", "co_gm.py"), r'^def _pcat|^def pwins'),
        fa_tab_sort=grep(os.path.join(KIT, "scripts", "season_deck.py"), r'free agents by z, descending'),
        morning_steps=grep(os.path.join(KIT, "scripts", "morning.py"), r'week_matchup\.py|weekly_preview|scoreboard_intake'),
    )

    # the pinned Flaim samples (pin.py)
    fs = json.load(open(os.path.join(HERE, "flaim_samples.json"), encoding="utf-8"))
    st = fs["standings"]["standings"]
    tx = fs["transactions"]
    m2 = fs["matchups_week2"]
    out["flaim"] = dict(
        standings=dict(teams=len(st), faab=sorted({t["faabBalance"] for t in st}), records=sorted({(t["wins"], t["losses"], t["ties"]) for t in st}),
                       fields=sorted(st[0])),
        transactions=dict(rows=tx["count"], first=tx["transactions"][-1]["date"], last=tx["transactions"][0]["date"],
                          ids=[tx["transactions"][-1]["transaction_id"], tx["transactions"][0]["transaction_id"]],
                          faab_bid_reported=sum(1 for t in tx["transactions"] if t["faab_bid"] is not None),
                          limitations=tx["limitations"], by_team=dict(collections.Counter(t["team_ids"][0].rsplit(".", 1)[-1] for t in tx["transactions"]))),
        matchups_week2=dict(week=m2["matchupWeek"], current_week=m2["currentWeek"], matchups=len(m2["matchups"]),
                            status=sorted({x["status"] for x in m2["matchups"]}),
                            games_remaining={s["teamName"]: s["gamesRemaining"] for x in m2["matchups"] for s in (x["home"], x["away"])},
                            pairs=[(x["home"]["teamName"], x["away"]["teamName"]) for x in m2["matchups"]]),
    )
    with open(os.path.join(HERE, "facts.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"FACTS: PASS — records {RECORDS_COMMIT}, deck {DECK_COMMIT}, kit {out['kit_commit']}")


if __name__ == "__main__":
    main()
