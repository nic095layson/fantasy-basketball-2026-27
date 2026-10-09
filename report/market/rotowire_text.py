#!/usr/bin/env python3
"""RotoWire's expert-panel 9-cat rankings with role and health notes, pasted by the owner on 2026-10-09
(article dated 2026-10-09) and kept verbatim as rotowire-raw-<date>.txt. This script transcribes the
text deterministically into the third-party intake's raw CSV and names, per row, the health and role
words the note carries — leads for the next pull's two-outlet verification, never facts on their own
(fix F2: a single outlet changes no pool row).

  rotowire-raw-<date>.csv   Rank, Player, Pos (blank — the article prints none), Team (code), Round,
                            Flag (health: … / role: … keywords found in the note), Claim (the note verbatim)
  rotowire-parse-<date>.md  counts, the invariants, the flagged rows, the input stamp (drift fix D4)

Invariants: ranks contiguous 1..N; every numbered line parses (rank, name, team, note); every team
name maps to a kit code. Exit 2 on any failure.
Usage: python3 report/market/rotowire_text.py [YYYY-MM-DD] [--as-of DATE|COMMIT | --live] [--out-dir DIR]
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import build_market as BM  # noqa: E402
import derived  # noqa: E402

TEAMS = {"Atlanta Hawks": "ATL", "Boston Celtics": "BOS", "Brooklyn Nets": "BKN", "Charlotte Hornets": "CHA",
         "Chicago Bulls": "CHI", "Cleveland Cavaliers": "CLE", "Dallas Mavericks": "DAL", "Denver Nuggets": "DEN",
         "Detroit Pistons": "DET", "Golden State Warriors": "GSW", "Houston Rockets": "HOU", "Indiana Pacers": "IND",
         "Los Angeles Clippers": "LAC", "Los Angeles Lakers": "LAL", "Memphis Grizzlies": "MEM", "Miami Heat": "MIA",
         "Milwaukee Bucks": "MIL", "Minnesota Timberwolves": "MIN", "New Orleans Pelicans": "NOP", "New York Knicks": "NYK",
         "Oklahoma City Thunder": "OKC", "Orlando Magic": "ORL", "Philadelphia 76ers": "PHI", "Phoenix Suns": "PHX",
         "Portland Trail Blazers": "POR", "Sacramento Kings": "SAC", "San Antonio Spurs": "SAS", "Toronto Raptors": "TOR",
         "Utah Jazz": "UTA", "Washington Wizards": "WAS"}
HEALTH = ["achilles", "acl", "hamstring", "calf", "foot injury", "wrist", "ankle", "back issue", "injur", "health",
          "games played", "rest days", "not at", "training camp", "availability", "absences", "missed", "load management",
          "lost season", "out indefinitely", "out a chunk", "foul trouble", "age"]
ROLE = ["murky", "cloudy", "cloudiness", "logjam", "crowded", "minutes risk", "minutes projection", "role is modest",
        "trims the usage", "costs him shots", "fewer shots", "fewer possessions", "fewer minutes", "usage competition",
        "pecking order", "competing", "hard to project", "faller", "riser", "sixth man", "off the bench", "path to"]
LINE = re.compile(r"^(\d+)\.\s+(.+?),\s+([A-Z][A-Za-z0-9 ]+?)\s+—\s+(.*)$")
COLS = ["Rank", "Player", "Pos", "Team", "Round", "Flag", "Claim"]


def _hit(k, low):
    """whole-word match; a trailing 'injur' is a prefix (injury, injuries, injured)."""
    pat = r"\b" + re.escape(k) + (r"" if k.endswith("injur") else r"\b")
    return re.search(pat, low) is not None


def flags(note):
    low = note.lower()
    h = [k for k in HEALTH if _hit(k, low)]
    r = [k for k in ROLE if _hit(k, low)]
    return "; ".join(x for x in (("health: " + ", ".join(h)) if h else "", ("role: " + ", ".join(r)) if r else "") if x)


def main():
    ap = derived.add_args(argparse.ArgumentParser(description="RotoWire expert-panel rankings (owner paste) intake"))
    ap.add_argument("date", nargs="?", default="2026-10-09")
    ap.add_argument("--out-dir", default=HERE)
    args = ap.parse_args()
    d, out = args.date, args.out_dir
    inp = derived.inputs_for(args, os.path.join(HERE, f"rotowire-parse-{d}.md"))
    text = open(inp.path(f"report/market/rotowire-raw-{d}.txt"), encoding="utf-8").read()
    rows, problems, rnd = [], [], ""
    for line in text.splitlines():
        s = line.strip()
        m = re.match(r"^Round (\d+)$", s)
        if m:
            rnd = m.group(1)
            continue
        if not re.match(r"^\d+\.\s", s):
            continue
        m = LINE.match(s)
        if not m:
            problems.append(f"unparsed line: {s[:70]!r}")
            continue
        rank, name, team, note = int(m.group(1)), m.group(2).strip(), m.group(3).strip(), m.group(4).strip()
        code = TEAMS.get(team)
        if not code:
            problems.append(f"unknown team {team!r} on rank {rank}")
            continue
        rows.append({"Rank": rank, "Player": name, "Pos": "", "Team": code, "Round": rnd, "Flag": flags(note), "Claim": note})
    ranks = [r["Rank"] for r in rows]
    if ranks != list(range(1, len(ranks) + 1)):
        problems.append(f"ranks not contiguous 1..{len(ranks)}")
    print(f"rows {len(rows)}; flagged {sum(1 for r in rows if r['Flag'])} (health {sum(1 for r in rows if 'health:' in r['Flag'])}, "
          f"role {sum(1 for r in rows if 'role:' in r['Flag'])})")
    if problems:
        print(f"TRANSCRIPTION GATE: FAIL — {len(problems)} problem(s)")
        for p in problems:
            print(" ", p)
        sys.exit(2)
    print("TRANSCRIPTION GATE: PASS")
    BM._write_csv(os.path.join(out, f"rotowire-raw-{d}.csv"), COLS, rows)
    L = [f"# RotoWire expert-panel 9-cat rankings — {d}: transcription of the owner's paste", "",
         f"{len(rows)} rows, ranks contiguous, every line parsed, every team mapped to a kit code; the note is kept verbatim in "
         f"Claim and the health / role words it carries in Flag — leads for the next pull's two-outlet verification, never facts "
         f"on their own.", "",
         "## Rows carrying a health word", "", "| rank | player | team | flag |", "|---|---|---|---|"]
    for r in rows:
        if "health:" in r["Flag"]:
            L.append(f"| {r['Rank']} | {r['Player']} | {r['Team']} | {r['Flag']} |")
    L += ["", "## Rows carrying a role word only", "", "| rank | player | team | flag |", "|---|---|---|---|"]
    for r in rows:
        if r["Flag"] and "health:" not in r["Flag"]:
            L.append(f"| {r['Rank']} | {r['Player']} | {r['Team']} | {r['Flag']} |")
    L += ["", inp.stamp()]
    open(os.path.join(out, f"rotowire-parse-{d}.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"wrote rotowire-raw-{d}.csv, rotowire-parse-{d}.md")


if __name__ == "__main__":
    main()
