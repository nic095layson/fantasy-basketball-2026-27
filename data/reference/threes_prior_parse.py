import sys, re, csv, hashlib, json, html
src, out_csv, out_manifest = sys.argv[1:4]
raw = open(src, 'rb').read(); h = raw.decode('utf-8', 'replace')
rows = {}; bad = []
for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', h, re.S):
    m = re.search(r'data-append-csv="([^"]+)"[^>]*data-stat="name_display"[^>]*><a[^>]*>([^<]+)</a>', tr)
    if not m: continue
    def cell(k):                                   # league leaders are printed inside <strong>, team codes inside <a>
        m2 = re.search(r'data-stat="%s"[^>]*>(.*?)</td>' % k, tr, re.S)
        return re.sub(r'<[^>]+>', '', m2.group(1)).strip() if m2 else ''
    pid, name = m.group(1), html.unescape(m.group(2))
    if pid in rows: continue                      # the first row per player is his season total (the combined row when traded)
    try: rows[pid] = dict(player=name, bref_id=pid, team=cell('team_name_abbr'), games=int(cell('games')), fg3=int(cell('fg3') or 0), fg3a=int(cell('fg3a') or 0))
    except ValueError: bad.append(name); continue
with open(out_csv, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['player', 'bref_id', 'team', 'games', 'fg3', 'fg3a'], lineterminator='\n'); w.writeheader()
    for r in sorted(rows.values(), key=lambda r: r['player']): w.writerow(r)
json.dump(dict(source='https://www.basketball-reference.com/leagues/NBA_2026_totals.html', title=re.findall(r'<title>([^<]*)', h)[0],
               fetched_utc=sys.argv[4], html_sha256=hashlib.sha256(raw).hexdigest(), html_bytes=len(raw), players=len(rows),
               rule='first table row per bref_id (the combined row for a traded player); games, fg3, fg3a as printed',
               csv_sha256=hashlib.sha256(open(out_csv, 'rb').read()).hexdigest()), open(out_manifest, 'w'), indent=1)
print(len(rows), 'unparsed', bad, rows.get('whitede01'), rows.get('champju02'))
