#!/bin/bash
# Range resolution to a fixed point: lines -> candidate files -> range check -> range.json -> lines ... (max 6 rounds)
set -e
W=$1; cd $W
B="python3 tools/wo5_lines.py bref_totals_all_rows.csv $DECK_CSV $KIT_CSV"
A="python3 tools/wo5_apply.py"; DK="--deck $DECK_CSV --kit $KIT_CSV"
rm -rf iter; mkdir iter
$B iter/lines_0.json --minutes minutes_overrides.csv > iter/lines_0.log
$A iter/lines_0.json $DK --out-dir iter/c0 > iter/apply_0.log
prev=""
for i in 1 2 3 4 5 6; do
  j=$((i-1))
  python3 tools/wo5_range.py iter/c$j/players.csv iter/lines_$j.json iter/range_$i.json $prev | tee iter/range_$i.log
  $B iter/lines_$i.json --minutes minutes_overrides.csv --range iter/range_$i.json > iter/lines_$i.log
  $A iter/lines_$i.json $DK --out-dir iter/c$i > iter/apply_$i.log
  if [ -n "$prev" ] && cmp -s iter/c$i/players.csv iter/c$j/players.csv && cmp -s iter/c$i/projections-2026-27.csv iter/c$j/projections-2026-27.csv; then
    echo "fixed point at round $i"; echo $i > iter/FINAL; exit 0; fi
  prev="--prev iter/range_$i.json"
done
echo "no fixed point in 6 rounds"; exit 1
