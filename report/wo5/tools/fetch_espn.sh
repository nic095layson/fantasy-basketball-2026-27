#!/bin/bash
# ESPN preseason scoreboards 2026-09-28 .. 2026-10-12 and every listed game's summary (box score); manifest url/utc/code/bytes/sha256.
DL="$1"; M=$DL/manifest.tsv; : > $M
get() { local out=$1 u=$2; local code; code=$(curl -sS -m 60 "$u" -o "$out" -w "%{http_code}" 2>/dev/null)
  [ "$code" != "200" ] && { sleep 5; code=$(curl -sS -m 60 "$u" -o "$out" -w "%{http_code}" 2>/dev/null); }
  printf "%s\t%s\t%s\t%s\t%s\n" "$u" "$(date -u +%FT%TZ)" "$code" "$(stat -c %s "$out")" "$(sha256sum "$out" | cut -c1-64)" >> $M; echo "$code"; }
for d in $(seq 0 14); do
  dt=$(date -u -d "2026-09-28 + $d day" +%Y%m%d)
  get $DL/scoreboard_$dt.json "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates=$dt&seasontype=1" >/dev/null
  for id in $(python3 -I -c "import json,sys; d=json.load(open(sys.argv[1])); print(' '.join(e['id'] for e in d.get('events',[]) if e['status']['type']['name']=='STATUS_FINAL'))" $DL/scoreboard_$dt.json); do
    c=$(get $DL/summary_$id.json "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event=$id"); echo "$dt $id $c"; sleep 0.3
  done
done
echo "== espn done $(date -u +%T)"
