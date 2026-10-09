"""sweep.tsv (the 24-game ESPN record) -> a markdown table, one row per player, built from the record, never typed."""
import csv, collections, sys
rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
by = collections.OrderedDict()
for r in rows: by.setdefault(r["player"], []).append(r)
out = ["| player | team | games (date: role, min) | lines (pts / reb / ast / stl / blk, FG) |", "|---|---|---|---|"]
for p, rs in by.items():
    rs.sort(key=lambda r: r["date"])
    g = []; l = []
    for r in rs:
        d = r["date"][5:].replace("-", "/").lstrip("0").replace("/0", "/")
        if r["role"] == "DNP":
            g.append(f"{d}: DNP ({r['reason'].lower()})")
        else:
            g.append(f"{d}: {'start' if r['role']=='S' else 'bench'}, {r['min']} min")
            l.append(f"{r['pts']} / {r['reb']} / {r['ast']} / {r['stl']} / {r['blk']}, {r['fg']}")
    out.append(f"| {p} | {rs[0]['team']} | {'; '.join(g)} | {'; '.join(l) if l else '—'} |")
print("\n".join(out))
