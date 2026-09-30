#!/usr/bin/env python3
"""2026-27 NBA schedule -> games per team per Yahoo fantasy week (gap audit G2/G3, 2026-09-30).

Reads Basketball-Reference's seven month pages for the 2026-27 season
(https://www.basketball-reference.com/leagues/NBA_2027_games-<month>.html),
buckets every dated game into Yahoo's 2026-27 fantasy weeks, and writes:

  games-2026-27.csv           one row per dated game (date, visitor, home, note)
  games-per-week-2026-27.csv  one row per team: games in each of the 23 Yahoo
                              weeks, dated total, undated knockout-window games,
                              back-to-backs, and the two playoff-window sums

Yahoo's 2026-27 calendar (Yahoo's schedule analysis, 2026-09; validated
mechanically in after-report-2026-09-30-gap-audit.md §3): week 1 is Tue Oct 20
to Sun Oct 25; every later week runs Mon-Sun except two 14-day matchups — week 7
(Nov 30-Dec 13, the NBA Cup knockout window) and week 17 (Feb 15-28, All-Star).
23 game weeks; the season ends Sun Apr 11, 2027. The owner's league plays 18
regular weeks and three 1-week playoff rounds in weeks 19-21 (Mar 8-28) —
confirm on the settings page (D-G5). Yahoo's default playoffs are weeks 20-22.

The NBA Cup knockout window (Dec 4-11) is undated until group play ends on
Nov 27: every team plays exactly two counted games in it (nba.com Cup FAQ), and
the two finalists a third — the Dec 11 championship — that counts for neither
the NBA standings nor Yahoo. The per-week file therefore carries week 7 as the
dated games plus an explicit `undated_knockout` column of 2 for every team.

Usage:
  python3 build_schedule.py                 # fetch the seven pages live
  python3 build_schedule.py --cache DIR     # read <month>.html from DIR instead
"""
import argparse
import csv
import datetime as dt
import os
import re
import ssl
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
MONTHS = ["october", "november", "december", "january", "february", "march", "april"]
URL = "https://www.basketball-reference.com/leagues/NBA_2027_games-{m}.html"
SEASON_LABEL = "2026-27"

# Yahoo 2026-27 fantasy calendar (see module docstring).
WEEK1 = (dt.date(2026, 10, 20), dt.date(2026, 10, 25))
FIRST_MONDAY = dt.date(2026, 10, 26)
SEASON_END = dt.date(2027, 4, 11)
FOURTEEN_DAY_STARTS = {dt.date(2026, 11, 30), dt.date(2027, 2, 15)}
OWNER_PLAYOFF_WEEKS = (19, 20, 21)   # league setting per owner (2026-08-04); D-G5
YAHOO_DEFAULT_PLAYOFF_WEEKS = (20, 21, 22)
UNDATED_KNOCKOUT_GAMES = 2           # per team, Dec 4-11 (nba.com Cup FAQ)


def weeks():
    out = [(1, WEEK1[0], WEEK1[1])]
    s, n = FIRST_MONDAY, 2
    while s <= SEASON_END:
        e = s + dt.timedelta(days=13 if s in FOURTEEN_DAY_STARTS else 6)
        out.append((n, s, e))
        s, n = e + dt.timedelta(days=1), n + 1
    return out


def fetch(month, cache):
    if cache:
        with open(os.path.join(cache, f"{month}.html"), encoding="utf-8", errors="ignore") as f:
            return f.read()
    ctx = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE") or os.environ.get("CURL_CA_BUNDLE") or None)
    req = urllib.request.Request(URL.format(m=month), headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
        return r.read().decode("utf-8", errors="ignore")


ROW = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
DATE = re.compile(r'data-stat="date_game"[^>]*csk="(\d{8})')
VIS = re.compile(r'data-stat="visitor_team_name"[^>]*><a href="/teams/([A-Z]{3})/2027\.html"')
HOME = re.compile(r'data-stat="home_team_name"[^>]*><a href="/teams/([A-Z]{3})/2027\.html"')
NOTE = re.compile(r'data-stat="game_remarks"[^>]*>([^<]*)')


def parse(html):
    games = []
    for row in ROW.findall(html):
        d = DATE.search(row)
        if not d:
            continue
        v, h = VIS.search(row), HOME.search(row)
        if not (v and h):
            continue
        note = NOTE.search(row)
        games.append((d.group(1), v.group(1), h.group(1), note.group(1).strip() if note else ""))
    return games


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", help="directory holding <month>.html copies of the seven pages")
    ap.add_argument("--out", default=HERE)
    a = ap.parse_args()

    games = []
    for m in MONTHS:
        games.extend(parse(fetch(m, a.cache)))
    games.sort()
    if not games:
        sys.exit("no games parsed")

    W = weeks()

    def wk(date_str):
        d = dt.date(int(date_str[:4]), int(date_str[4:6]), int(date_str[6:]))
        for n, s, e in W:
            if s <= d <= e:
                return n
        return None

    teams = sorted({g[1] for g in games} | {g[2] for g in games})
    counts = {t: {n: 0 for n, _, _ in W} for t in teams}
    dates = {t: [] for t in teams}
    for d, v, h, _ in games:
        n = wk(d)
        for t in (v, h):
            counts[t][n] += 1
            dates[t].append(dt.date(int(d[:4]), int(d[4:6]), int(d[6:])))

    with open(os.path.join(a.out, f"games-{SEASON_LABEL}.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "yahoo_week", "visitor", "home", "note"])
        for d, v, h, note in games:
            w.writerow([f"{d[:4]}-{d[4:6]}-{d[6:]}", wk(d), v, h, note])

    with open(os.path.join(a.out, f"games-per-week-{SEASON_LABEL}.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["team"] + [f"w{n}" for n, _, _ in W]
                   + ["dated_total", "undated_knockout", "b2b_total",
                      "b2b_w19_21", "po_w19_21", "po_w20_22"])
        for t in teams:
            ds = sorted(dates[t])
            pairs = [(x, y) for x, y in zip(ds, ds[1:]) if (y - x).days == 1]
            b2b_po = sum(1 for _, y in pairs if wk(y.strftime("%Y%m%d")) in OWNER_PLAYOFF_WEEKS)
            w.writerow([t] + [counts[t][n] for n, _, _ in W]
                       + [len(ds), UNDATED_KNOCKOUT_GAMES, len(pairs), b2b_po,
                          sum(counts[t][n] for n in OWNER_PLAYOFF_WEEKS),
                          sum(counts[t][n] for n in YAHOO_DEFAULT_PLAYOFF_WEEKS)])

    print(f"games dated: {len(games)}  teams: {len(teams)}  weeks: {len(W)}")
    for n, s, e in W:
        print(f"  week {n:2}: {s} to {e}  ({(e - s).days + 1} days)  mean games/team {sum(counts[t][n] for t in teams) / len(teams):.2f}")
    sev = [counts[t][n] for t in teams for n in range(2, 19) if n not in (7, 17)]
    print(f"7-day regular weeks (2-18 minus 7 and 17): mean {sum(sev) / len(sev):.3f} games per team-week over {len(sev)} team-weeks")


if __name__ == "__main__":
    main()
