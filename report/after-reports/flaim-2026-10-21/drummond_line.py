#!/usr/bin/env python3
"""Andre Drummond's pool line (owner 2026-10-21: "Drummond, pull data from both sources to add a projection for him").

Why: the Flaim rosters of 10/21 carry him on Podz save the league's bench, and the intake halts on a rostered name with
no row in the deck pool (deck data/players.csv). The kit plane already had a line for him (2025-26 base, 60 GP / 19.5
mpg); the deck plane never did.

Method (stated to the owner before the run):
  - identity from Yahoo through Flaim (team, position, no status letter): data/source/flaim/players_andre-drummond_2026-10-21.json
  - the outside projection from FantasyBot (per game, as of 10/21): data/source/fantasybot/player_value_andre-drummond_2026-10-21.json
  - the 10/14 blend's own rule, by its own code (report/blend/tools: common.blend_cell and fmt; blend_lines.py A1-A3):
    A1 each of the nine categories the equal-weight mean of the kit line and FantasyBot's; A2 games, minutes and tags
    untouched; A3 FGA and FTA scaled by one factor so points = 2*FG%*FGA + 3PM + FT%*FTA (FantasyBot publishes no
    attempts). One outside projection is below the blend's three-reference floor (A4, MIN_REFS = 3): the owner's order.
  - the same line on both planes: the kit row replaced in report/projections-2026-27.csv, a new row appended to deck
    data/players.csv. The deck's arena/results/players_v69.csv is NOT touched: it is the Version 69 pool snapshot the
    mock regrades read (arena/mocks/live_retro.py POOLS["v69"]).

    python3 drummond_line.py [--write]
Prints 'DRUMMOND LINE: PASS — ...' (dry run unless --write) or exits 1."""
import argparse, csv, io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DECK = os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball")
sys.path.insert(0, os.path.join(KIT, "report", "blend", "tools"))
from common import CATS, STAT, KITCOL, fmt, blend_cell  # noqa: E402

NAME = "Andre Drummond"
KIT_CSV = os.path.join(KIT, "report", "projections-2026-27.csv")
DECK_CSV = os.path.join(DECK, "data", "players.csv")
FB = os.path.join(KIT, "data", "source", "fantasybot", "player_value_andre-drummond_2026-10-21.json")
FL = os.path.join(KIT, "data", "source", "flaim", "players_andre-drummond_2026-10-21.json")
FB_KEYS = {"fg_pct": ("fgPct", 0.01), "ft_pct": ("ftPct", 0.01), "tpm": ("tpm", 1), "pts": ("pts", 1), "reb": ("reb", 1),
           "ast": ("ast", 1), "stl": ("stl", 1), "blk": ("blk", 1), "tov": ("tov", 1)}
DECK_COLS = ["player", "team", "pos", "fg_pct", "fga", "ft_pct", "fta", "tpm", "pts", "reb", "ast", "stl", "blk", "tov", "note"]
NOTE = ("10/21: added in-season (owner 10/21: \"Drummond, pull data from both sources to add a projection for him\"): "
        "on Podz save the league's bench, {team} {pos}, no status letter (Yahoo via Flaim 10/21, "
        "data/source/flaim/players_andre-drummond_2026-10-21.json); the line is the 10/14 blend rule (each category the "
        "equal-weight mean, shots rescaled to the points identity) on the kit line (2025-26 base, {gp} GP / {mpg} mpg) and "
        "FantasyBot's 10/21 projection (data/source/fantasybot/player_value_andre-drummond_2026-10-21.json), one outside "
        "projection, below the blend's three-reference floor by the owner's order; games, minutes and tags as the kit line")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true"); a = ap.parse_args()
    fb = json.load(open(FB, encoding="utf-8"))["response"]["player"]
    proj = fb["nba"]["projected"]
    yahoo = [p for p in json.load(open(FL, encoding="utf-8"))["response"]["data"]["players"] if p["name"] == NAME]
    problems = []
    if len(yahoo) != 1: problems.append(f"Flaim record has {len(yahoo)} rows named {NAME}")
    y = yahoo[0] if yahoo else {}
    kit_rows = list(csv.DictReader(open(KIT_CSV, encoding="utf-8")))
    kit_fields = list(kit_rows[0].keys())
    hits = [i for i, r in enumerate(kit_rows) if r["name"] == NAME]
    if len(hits) != 1: problems.append(f"kit plane has {len(hits)} rows named {NAME}")
    k = kit_rows[hits[0]] if hits else {}
    deck_text = open(DECK_CSV, encoding="utf-8").read()
    deck_rows = list(csv.DictReader(io.StringIO(deck_text)))
    if any(r["player"] == NAME for r in deck_rows): problems.append(f"deck pool already has a row named {NAME}")
    if y and (y.get("team"), y.get("position")) != (k.get("team"), k.get("pos")):
        problems.append(f"Yahoo says {y.get('team')} {y.get('position')}, the kit line {k.get('team')} {k.get('pos')}")
    if fb.get("team") != k.get("team"): problems.append(f"FantasyBot team {fb.get('team')} vs kit {k.get('team')}")
    if y.get("status") or fb.get("injury") or fb.get("statusTag"): problems.append("a status is set; the line rule assumes none")
    if problems:
        for p in problems: print("  PROBLEM " + p)
        print("DRUMMOND LINE: FAIL"); sys.exit(1)

    ours = {c: float(k[KITCOL.get(c, c)]) for c in STAT}
    ref = {"FantasyBot 10/21": {c: proj[key] * scale for c, (key, scale) in FB_KEYS.items()}}
    new = dict(ours)
    for c in CATS: new[c] = blend_cell(ours[c], ref, c)                        # A1
    denom = 2 * ours["fga"] * new["fg_pct"] + ours["fta"] * new["ft_pct"]     # A3, as blend_lines.py
    f = (new["pts"] - new["tpm"]) / denom
    new["fga"] = float(fmt("fga", ours["fga"] * f)); new["fta"] = float(fmt("fta", ours["fta"] * f))
    resid = new["pts"] - (2 * new["fga"] * new["fg_pct"] + new["tpm"] + new["fta"] * new["ft_pct"])
    if abs(resid) > 0.25: print(f"  PROBLEM identity residual {resid:.3f}"); print("DRUMMOND LINE: FAIL"); sys.exit(1)

    rec = dict(name=NAME, kit_before=ours, fantasybot=ref["FantasyBot 10/21"], new=new, shot_factor=round(f, 4),
               identity_residual=round(resid, 4), kit_games=k["gp"], kit_minutes=k["mpg"],
               fantasybot_expected_games=fb["nba"].get("expectedGames"), fantasybot_minutes=proj.get("min"),
               yahoo=dict(team=y["team"], position=y["position"], league_team=y.get("league_team_name"),
                          status=y.get("status")))
    print(json.dumps({c: [ours[c], ref["FantasyBot 10/21"].get(c), new[c]] for c in STAT}))
    if a.write:
        for c in STAT: k[KITCOL.get(c, c)] = fmt(c, new[c])
        buf = io.StringIO(); w = csv.DictWriter(buf, fieldnames=kit_fields, lineterminator="\n"); w.writeheader(); w.writerows(kit_rows)
        open(KIT_CSV, "w", encoding="utf-8").write(buf.getvalue())
        row = dict(player=NAME, team=y["team"], pos=y["position"], note=NOTE.format(team=y["team"], pos=y["position"], gp=k["gp"], mpg=k["mpg"]))
        row.update({c: fmt(c, new[c]) for c in STAT})
        buf = io.StringIO(); csv.DictWriter(buf, fieldnames=DECK_COLS, lineterminator="\n").writerow(row)
        open(DECK_CSV, "w", encoding="utf-8").write(deck_text + ("" if deck_text.endswith("\n") else "\n") + buf.getvalue())
        json.dump(rec, open(os.path.join(HERE, "drummond_line_record.json"), "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(f"DRUMMOND LINE: PASS — {'written to both planes' if a.write else 'dry run, nothing written'}; shot factor {f:.4f}, "
          f"identity residual {resid:+.3f}; Yahoo {y['team']} {y['position']} on {y.get('league_team_name')}")


if __name__ == "__main__":
    main()
