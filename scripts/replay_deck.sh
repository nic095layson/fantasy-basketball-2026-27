#!/usr/bin/env bash
# replay_deck.sh <YYYY-MM-DD> — rebuild the Season Deck for one recorded real morning into a throwaway folder and
# print its SEASON DECK line. season_deck.py already refuses a page that cannot draw itself (render check), so the
# PASS line means: built from that morning's records AND opened in a headless browser with 6 tabs and 0 errors.
# Used by scripts/gates.py --replay through scripts/independent_audit/replay_gate.py (owner 2026-10-21).
set -u
d="$1"; here="$(cd "$(dirname "$0")" && pwd)"; out="$(mktemp -d)"
trap 'rm -rf "$out"' EXIT
python3 "$here/season_deck.py" --date "$d" --out "$out"
