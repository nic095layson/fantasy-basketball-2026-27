"""F3: the morning of 10/22 pins Yahoo's 10/20 and 10/21 lineups in pull_2026-10-22.json; the afternoon check runs
league live for the same date on a pull with no dated lineup (the e7b69bb run's own pull); the week card of 10/23
then gathers the week's lineups. Run once per tree: python3 afternoon.py <kit tree> <records tree> <lineups json> <workdir>"""
import json, os, subprocess, sys
kit, records, lineups, work = sys.argv[1:5]
os.makedirs(work, exist_ok=True)
run_pull = os.path.join(records, "data", "source", "flaim", "pull_2026-10-22.json")
morning = json.load(open(run_pull, encoding="utf-8"))
morning["daily"] = json.load(open(lineups, encoding="utf-8"))
with open(os.path.join(work, "pull_2026-10-22.json"), "w", encoding="utf-8") as f:
    json.dump(morning, f)
p = subprocess.run([sys.executable, os.path.join(kit, "scripts", "league_live.py"), "--as-of", "2026-10-22", "--source", "flaim",
                    "--pull", run_pull, "--out", os.path.join(work, "league_state.json"), "--pin-dir", work,
                    "--flaim-pin-dir", work], capture_output=True, text=True)
print("afternoon:", [l for l in p.stdout.splitlines() if l.startswith("LEAGUE LIVE")])
sys.path.insert(0, os.path.join(kit, "scripts"))
import week_matchup as WM
got = WM.week_lineups(os.path.join(work, "pull_2026-10-23.json"), "2026-10-20", "2026-10-23")
print("week card 10/23 reads:", {t: sorted(d) for t, d in got.items()}, "=", sum(len(d) for d in got.values()), "lineups")
