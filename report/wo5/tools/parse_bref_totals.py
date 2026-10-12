"""Basketball-Reference season totals pages (row=season: the first row per player id, the season total; row=split: each team row after it) (untrusted HTML; run with python3 -I) -> one CSV of player-season totals.
First row per player id is the season total (TOT / 2TM / 3TM listed first); 'League Average' dropped.
Columns: season, pid, player, team, g, gs, mp, fg, fga, fg3, ft, fta, trb, ast, stl, blk, tov, pts."""
import csv, glob, html as H, os, re, sys
DL, OUT = sys.argv[1], sys.argv[2]
STAT = {"g": ("games", "g"), "gs": ("games_started", "gs"), "mp": ("mp",), "fg": ("fg",), "fga": ("fga",), "fg3": ("fg3",),
        "ft": ("ft",), "fta": ("fta",), "trb": ("trb",), "ast": ("ast",), "stl": ("stl",), "blk": ("blk",), "tov": ("tov",), "pts": ("pts",)}
rows = []; probs = []
for f in sorted(glob.glob(os.path.join(DL, "totals_*.html"))):
    y = int(re.search(r"totals_(\d+)", f).group(1)); season = f"{y-1}-{str(y)[2:]}"
    t = open(f, encoding="utf-8", errors="replace").read()
    a = t.find('id="totals_stats"'); b = t.find('id="totals_stats_post"')
    assert a >= 0, f"{f}: no regular-season table"
    t = t[a:b] if b > a else t[a:]   # the regular-season table only; the playoffs table (totals_stats_post) follows it
    seen = set(); n = 0
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", t, re.S):
        m = re.search(r'<t[dh]([^>]*data-stat="(?:player|name_display)"[^>]*)>(.*?)</t[dh]>', row, re.S)
        if not m: continue
        am = re.search(r'data-append-csv="([^"]+)"', m.group(1))
        if not am: continue
        pid = am.group(1); name = H.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
        split = pid in seen
        seen.add(pid)
        cells = dict(re.findall(r'<t[dh][^>]*data-stat="([^"]+)"[^>]*>(.*?)</t[dh]>', row, re.S))
        clean = lambda v: H.unescape(re.sub(r"<[^>]+>", "", v)).strip()
        team = clean(cells.get("team_name_abbr", cells.get("team_id", "")))
        d = dict(season=season, pid=pid, player=name, team=team, row="split" if split else "season")
        for k, cands in STAT.items():
            v = next((clean(cells[c]) for c in cands if c in cells), "")
            try: d[k] = float(v) if v != "" else 0.0
            except ValueError: probs.append((season, name, k, v)); d[k] = 0.0
        rows.append(d); n += 1
    print(season, n, "players")
with open(OUT, "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("rows", len(rows), "problems", len(probs), probs[:5])
