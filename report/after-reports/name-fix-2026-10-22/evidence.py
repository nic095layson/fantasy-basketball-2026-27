#!/usr/bin/env python3
"""Evidence for the name-mismatch fix (owner 2026-10-22, "Fix both readers"), run on the fixed code against the
season/daily records of commit e7b69bb (the 14:44Z morning run). Writes evidence.json beside this file.

  1. re-resolve: box_pull.resolve_names over every committed box-score record; every pool name that changes.
  2. week card: week_matchup.build for 2026-10-22 on the committed records; the to-date rebuild against Yahoo's
     totals for both teams.
  3. season lines: season_lines.run on the re-resolved records; every kit-plane and deck-plane row that differs
     from the committed lines.

    DECK_REPO=... python3 report/after-reports/name-fix-2026-10-22/evidence.py <records-dir: a season/daily checkout>
"""
import csv, glob, json, os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(KIT, "scripts"))
import box_pull as BP, season_lines as SL, week_matchup as WM  # noqa: E402

REC = sys.argv[1]
out = {"records_from": REC}

# 1 re-resolve
pool, aliases = BP.load_pool_names(), BP.load_aliases()
changes, reresolved = [], []
for f in sorted(glob.glob(os.path.join(REC, "data", "actuals", "*.json"))):
    rec = json.load(open(f, encoding="utf-8"))
    new = BP.resolve_names(rec["players"], pool, aliases)
    for a, b in zip(rec["players"], new):
        if a.get("pool_name") != b["pool_name"]:
            changes.append(dict(date=rec["date"], name=a["name"], before=a.get("pool_name"), after=b["pool_name"],
                                dnp=bool(a.get("dnp")), regular=any(g["espn_id"] == a.get("game") and g.get("season_type") == 2 for g in rec["games"])))
    reresolved.append(dict(rec, players=new))
out["reresolve"] = dict(records=len(reresolved), lines=sum(len(r["players"]) for r in reresolved), changes=changes)

# 2 week card on the committed records (the card reads box lines under its own spelling)
os.environ["SEASON_POOL"] = os.path.join(REC, "data", "season", "pool_season.csv")
paths = dict(state=os.path.join(REC, "data", "league_state.json"), schedule=os.path.join(REC, "data", "league_schedule.json"),
             games=os.path.join(REC, "report", "schedule", "games-2026-27.csv"), actuals=os.path.join(REC, "data", "actuals"),
             status=os.path.join(REC, "data", "status"), yahoo_pull=os.path.join(REC, "data", "source", "flaim", "pull_2026-10-22.json"))
card = WM.build("2026-10-22", paths)
src = card["to_date_source"]
out["week_card"] = dict(source=src["source"], rebuild_agrees=src["rebuild_agrees"], differences=src["differences"],
                        rebuild=dict(me=card["totals"]["me"]["rebuild_to_date"], opp=card["totals"]["opp"]["rebuild_to_date"]),
                        yahoo=dict(me=card["totals"]["me"]["to_date"], opp=card["totals"]["opp"]["to_date"]))

# 3 season lines on the re-resolved records, against the committed lines
def rows(path, key):
    return {r[key]: r for r in csv.DictReader(open(path, encoding="utf-8"))}
with tempfile.TemporaryDirectory() as d:
    SL.run(date="2026-10-22", actuals=reresolved, out_dir=d, additions_csv=os.path.join(REC, "data", "pool_additions.csv"))
    diff = {}
    for fname, key in (("projections_season.csv", "name"), ("pool_season.csv", "player")):
        old, new = rows(os.path.join(REC, "data", "season", fname), key), rows(os.path.join(d, fname), key)
        diff[fname] = dict(rows=len(new), same_names=sorted(old) == sorted(new),
                           changed={n: {c: [old[n][c], new[n][c]] for c in new[n] if old[n].get(c) != new[n][c]}
                                    for n in new if n in old and old[n] != new[n]})
out["season_lines"] = diff
json.dump(out, open(os.path.join(HERE, "evidence.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(json.dumps(dict(reresolve=out["reresolve"]["changes"], card=dict((k, out["week_card"][k]) for k in ("source", "rebuild_agrees", "differences")),
                      season={f: dict(rows=v["rows"], same_names=v["same_names"], changed=sorted(v["changed"])) for f, v in diff.items()}), indent=1))
