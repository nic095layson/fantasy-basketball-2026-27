#!/bin/bash
# Basketball-Reference regular-season totals pages 2003-04 .. 2025-26 into an untrusted dir; manifest url/utc/code/bytes/sha256.
DL="$1"; UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
M=$DL/manifest.tsv; : > $M
for y in $(seq 2004 2026); do
  out=$DL/totals_$y.html; u="https://www.basketball-reference.com/leagues/NBA_${y}_totals.html"
  code=$(curl -sS -L -m 90 -A "$UA" "$u" -o "$out" -w "%{http_code}" 2>/dev/null)
  if [ "$code" != "200" ]; then sleep 30; code=$(curl -sS -L -m 90 -A "$UA" "$u" -o "$out" -w "%{http_code}" 2>/dev/null); fi
  printf "%s\t%s\t%s\t%s\t%s\n" "$u" "$(date -u +%FT%TZ)" "$code" "$(stat -c %s "$out")" "$(sha256sum "$out" | cut -c1-64)" >> $M
  echo "$y $code $(stat -c %s "$out")"; sleep 4
done
echo "== bref done $(date -u +%T)"
