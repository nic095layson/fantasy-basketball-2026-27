#!/usr/bin/env python3
"""Season tools before/after the six GP changes (owner 2026-10-22). Two scratch copies of this checkout, identical
except report/projections-2026-27.csv (BEFORE takes it from --base, AFTER from the working tree), each with a deck
sibling at --deck; in each, season_lines.py and season_board.py run for --date. Compares every season output and the
board's rows. Writes season_diff.json beside itself.

    python3 report/after-reports/risk-rows-2026-10-22/season_diff.py --date 2026-10-21 [--base origin/main] [--deck PATH]"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUTS = ["data/season/projections_season.csv", "data/season/pool_season.csv"]


def board_rows(path):
    rows = {}
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^\| (\d+) \| ([^|]+?) \| [^|]* \| [^|]* \| (\d+) \| ([-+]?[\d.]+) \| ([-+]?[\d.]+) \|", line)
        if m:
            rows[m.group(2)] = dict(rank=int(m.group(1)), gp=int(m.group(3)), value_adj=float(m.group(4)), z_total=float(m.group(5)))
    return rows


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--date", required=True); ap.add_argument("--base", default="origin/main")
    ap.add_argument("--deck", default=os.path.abspath(os.path.join(KIT, "..", "yahoo-fantasy-basketball"))); a = ap.parse_args()
    tmp = tempfile.mkdtemp(prefix="season_diff_"); res = {}
    try:
        for v in ("before", "after"):
            dst = os.path.join(tmp, v, "fantasy-basketball-2026-27")
            shutil.copytree(KIT, dst, ignore=shutil.ignore_patterns(".git"))
            os.symlink(os.path.realpath(a.deck), os.path.join(tmp, v, "yahoo-fantasy-basketball"))
            if v == "before":
                csv = subprocess.run(["git", "-C", KIT, "show", f"{a.base}:report/projections-2026-27.csv"], capture_output=True, check=True).stdout
                open(os.path.join(dst, "report", "projections-2026-27.csv"), "wb").write(csv)
            lines = subprocess.run([sys.executable, "scripts/season_lines.py", "--date", a.date], cwd=dst, capture_output=True, text=True)
            board = subprocess.run([sys.executable, "scripts/season_board.py", "--date", a.date], cwd=dst, capture_output=True, text=True)
            assert lines.returncode == 0 and board.returncode == 0, (lines.stdout[-500:], board.stdout[-500:])
            res[v] = dict(dir=dst, lines=lines.stdout.strip().splitlines()[-1], board=board.stdout.strip().splitlines()[-1],
                          rows=board_rows(os.path.join(dst, "report", "season", f"board_{a.date}.md")))
        files = {}
        for f in OUTS:
            b = open(os.path.join(res["before"]["dir"], f), encoding="utf-8").read().splitlines()
            af = open(os.path.join(res["after"]["dir"], f), encoding="utf-8").read().splitlines()
            files[f] = dict(identical=b == af, lines_changed=sum(1 for x, y in zip(b, af) if x != y) + abs(len(b) - len(af)))
        rb, ra = res["before"]["rows"], res["after"]["rows"]
        moved = [dict(player=n, before=rb.get(n), after=ra.get(n)) for n in sorted(set(rb) | set(ra), key=lambda n: (ra.get(n) or rb[n])["rank"]) if rb.get(n) != ra.get(n)]
        rec = dict(date=a.date, base=a.base, base_commit=subprocess.run(["git", "-C", KIT, "rev-parse", a.base], capture_output=True, text=True).stdout.strip(),
                   deck_commit=subprocess.run(["git", "-C", a.deck, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip(),
                   files=files, board_rows=len(ra), board_changed=moved,
                   rank_changes=[m["player"] for m in moved if m["before"] and m["after"] and m["before"]["rank"] != m["after"]["rank"]],
                   lines_pass=[res[v]["lines"] for v in ("before", "after")], board_pass=[res[v]["board"] for v in ("before", "after")])
        json.dump(rec, open(os.path.join(HERE, "season_diff.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        for f, d in files.items():
            print(f"{f}: {'identical' if d['identical'] else str(d['lines_changed']) + ' lines differ'}")
        for m in moved:
            print(f"{m['player']}: {m['before']} -> {m['after']}")
        print(f"SEASON DIFF: {len(moved)} board rows changed, rank changes {len(rec['rank_changes'])}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
