#!/usr/bin/env python3
"""The 7 risk-tagged kit rows at healthy-level GP (D-PM-4 look, GAUNTLET 2026-10-21). Read-only: changes no line or tag.

  1. the rows: the pool population of the 10/21 D-PM-4 record (proceed-2026-10-21/dpm4.json) whose tier is risk and
     whose kit availability is at or above the healthy median
  2. each row's kit GP across every commit of report/projections-2026-27.csv, plus three rows tagged since 10/10 (the
     D-1010-2 convention: tag + kit GP -6) for comparison
  3. the commit that first put each row's risk tag on the deck's data/players.csv

    python3 report/after-reports/gauntlet-2026-10-21/seven_rows.py   (writes seven_rows.json beside this file)
"""
import csv
import io
import json
import os
import subprocess
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
DECK = os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball")
PROJ = "report/projections-2026-27.csv"
COMPARE = ["Isaiah Stewart", "Maxime Raynaud", "Coby White"]


def norm(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if c.isalnum()).lower().replace("jr", "").replace("iii", "")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=True).stdout


def main():
    d = json.load(open(os.path.join(KIT, "report/after-reports/proceed-2026-10-21/dpm4.json"), encoding="utf-8"))
    pop = d["populations"]["pool"]
    med = pop["kit_healthy_median"]
    seven = sorted([p for p in pop["players"] if p["tier"] == "risk" and p["kit"] >= med], key=lambda p: -p["kit"])
    names = [p["player"] for p in seven] + COMPARE
    want = {norm(n): n for n in names}
    hist = {n: [] for n in names}
    for line in git(KIT, "log", "--reverse", "--format=%h %ad", "--date=short", "--", PROJ).splitlines():
        h, day = line.split()
        seen = {want[norm(r["name"])]: r["gp"] for r in csv.DictReader(io.StringIO(git(KIT, "show", f"{h}:{PROJ}")))
                if norm(r["name"]) in want}
        for n in names:
            if not hist[n] or hist[n][-1]["gp"] != seen.get(n):
                hist[n].append(dict(commit=h, date=day, gp=seen.get(n)))
    pool = {r["player"]: r for r in csv.DictReader(open(os.path.join(KIT, "data/season/pool_season.csv"), encoding="utf-8"))}
    rows = []
    for p in seven + [dict(player=n) for n in COMPARE]:
        n = p["player"]
        tag = (pool.get(n, {}).get("note") or "").split(" ")[0].rstrip(";")
        first = git(DECK, "log", "--reverse", "--format=%h %ad", "--date=short", "-G", f"^\"?{n}\"?,.*{tag}",
                    "--", "data/players.csv").splitlines() if tag.startswith("inj-") else []
        rows.append(dict(player=n, seven=n not in COMPARE, tag=tag, gp_history=hist[n],
                         tag_first_on_deck=first[0] if first else None,
                         kit=p.get("kit"), kit_rel=p.get("kit_rel"), active=p.get("active")))
    out = dict(source="proceed-2026-10-21/dpm4.json pool population; kit file history; deck data/players.csv history",
               kit_head=git(KIT, "rev-parse", "--short", "HEAD").strip(), deck_head=git(DECK, "rev-parse", "--short", "HEAD").strip(),
               healthy_median=med, n_seven=len(seven), rows=rows)
    with open(os.path.join(HERE, "seven_rows.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    for r in rows:
        gp = " then ".join(f"{e['gp']} ({e['date']})" for e in r["gp_history"])
        print(f"{'*' if r['seven'] else ' '} {r['player']}: {r['tag']} first on deck {r['tag_first_on_deck']}; kit GP {gp}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
