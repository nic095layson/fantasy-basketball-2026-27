#!/bin/bash
# Dial pass 2026-10-13: the deck's full chain on the rebuilt page (Version 65 candidate), one harness at a time.
cd /home/user/yahoo-fantasy-basketball
O=/home/user/fantasy-basketball-2026-27/report/dial/out
echo "== page $(sha256sum docs/draft-deck.html | cut -c1-12) $(wc -c < docs/draft-deck.html) bytes"
echo "== parity $(date -u +%T)"; timeout 1800 python3 scripts/check_parity.py 2>&1 | tail -4; echo "exit ${PIPESTATUS[0]}"
echo "== test_card $(date -u +%T)"; timeout 1800 python3 scripts/test_card.py 2>&1 | tail -2; echo "exit ${PIPESTATUS[0]}"
echo "== test_draft $(date -u +%T)"; timeout 1800 python3 scripts/test_draft.py 2>&1 | tail -2; echo "exit ${PIPESTATUS[0]}"
echo "== test_gates $(date -u +%T)"; timeout 2400 python3 scripts/test_gates.py 2>&1 | tail -3; echo "exit ${PIPESTATUS[0]}"
echo "== full_dom_check $(date -u +%T)"; env -u TMPDIR timeout 1800 node arena/mocks/full_dom_check.mjs docs/draft-deck.html arena/data/states/draft_state_54.json arena/results/full_dom_check_2026-10-13_v65.json 2>&1 | tail -4; echo "exit ${PIPESTATUS[0]}"
echo "== repeat_market_check $(date -u +%T)"; env -u TMPDIR timeout 1800 python3 scripts/repeat_market_check.py --json arena/results/repeat_market_check_2026-10-13_v65.json > $O/rn_section_v65.md 2>&1; echo "exit $?"; head -3 $O/rn_section_v65.md
echo "== identity_check $(date -u +%T)"; timeout 600 python3 scripts/identity_check.py --json $O/identity_v65.json 2>&1 | head -3; echo "exit ${PIPESTATUS[0]}"
echo "== range_check (D-RN-3, with last season) $(date -u +%T)"; timeout 600 python3 scripts/range_check.py --json $O/range_check_v65.json > $O/range_check_v65.txt 2>&1; echo "exit $?"; head -1 $O/range_check_v65.txt
echo "== done $(date -u +%T)"
