#!/usr/bin/env python3
"""Pin the records behind the 2026-10-22 correction in §3 of after-report-2026-10-22-day-findings.md (owner
2026-10-22, "Add a correction": one dated paragraph saying the cause of the opponent-side week-card gap is Acuff's
dropped box score; the report's earlier text stays as it was).

Reads git objects only (the four 10/22 morning runs on season/daily and the name-fix commit of kit draft PR #168):
  - week_cards.json: each run's T0, Yahoo pin sha256 and the week card's Yahoo and rebuild to-date totals per side;
  - league_moves.json: every team's moves as each run recorded them (the opponent is MAXEY-MUM OVERDRIVE);
  - commits.txt: the runs' commit lines;
  - name_fix_week_card.json: the fixed code's week card on the 14:44Z records (evidence.json on the #168 branch);
  - acuff_spellings.json: Acuff's rows in the 10/21 box record and in the kit's projections file on main.
recon.py / recon.json beside this file are the lineup reconciliation made in the session at 14:33Z (lineups from
Flaim get_roster as_of_date, read from the session transcript, which is not committed; its rows carry them).

    python3 report/after-reports/day-findings-2026-10-22/correction-2026-10-22/pin.py
"""
import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
RUNS = ["51cf6b3", "2f2aea8", "21d815d", "e7b69bb"]  # 05:54 PT scheduled, 14:15Z on-demand, 14:31Z runner, 14:44Z on-demand
NAME_FIX = "97a1714"
MAIN = "af625a8"  # kit main, the base of #167 and #168


def show(commit, path):
    return subprocess.run(["git", "-C", KIT, "show", f"{commit}:{path}"], capture_output=True, text=True, check=True).stdout


def card(commit):
    wk = json.loads(show(commit, "report/briefs/week_matchup_2026-10-22.json"))
    morning = show(commit, "report/briefs/morning_2026-10-22.json")
    td = wk["to_date_source"]
    assert td["source"] == "yahoo", (commit, td["source"])
    return dict(t0=re.search(r"--since (\S+Z)", morning).group(1), yahoo_pull_sha256=wk["inputs"]["yahoo_pull"]["sha256"],
                opponent=wk["opponent"], to_date_days=wk["to_date_days"],
                yahoo={s: wk["totals"][s]["to_date"] for s in ("me", "opp")},
                rebuild={s: wk["totals"][s]["rebuild_to_date"] for s in ("me", "opp")},
                differences=td["differences"])


def main():
    cards = {c: card(c) for c in RUNS}
    json.dump(cards, open(os.path.join(HERE, "week_cards.json"), "w"), indent=1)
    json.dump({c: json.loads(show(c, "data/news/league_moves_2026-10-22.json")) for c in RUNS},
              open(os.path.join(HERE, "league_moves.json"), "w"), indent=1)
    log = subprocess.run(["git", "-C", KIT, "log", "--no-walk", "--format=%h %cI %s", *RUNS],
                         capture_output=True, text=True, check=True).stdout
    open(os.path.join(HERE, "commits.txt"), "w").write(log)
    # the two spellings: ESPN's in the 10/21 box record the 14:15Z run read, the kit's in the projections file on main
    box = json.loads(show("2f2aea8", "data/actuals/2026-10-21.json"))
    kit_rows = [l for l in show(MAIN, "report/projections-2026-27.csv").splitlines() if "acuff" in l.lower()]
    json.dump(dict(box_record="2f2aea8:data/actuals/2026-10-21.json",
                   box_rows=[p for p in box["players"] if "acuff" in p["name"].lower()],
                   kit_file=f"{MAIN}:report/projections-2026-27.csv", kit_rows=kit_rows),
              open(os.path.join(HERE, "acuff_spellings.json"), "w"), indent=1)
    ev = json.loads(show(NAME_FIX, "report/after-reports/name-fix-2026-10-22/evidence.json"))
    json.dump(dict(commit=NAME_FIX, records_from=ev["records_from"], week_card=ev["week_card"]),
              open(os.path.join(HERE, "name_fix_week_card.json"), "w"), indent=1)
    print("PIN: wrote week_cards.json, league_moves.json, commits.txt, acuff_spellings.json, name_fix_week_card.json")


if __name__ == "__main__":
    main()
