# The week card's adds honour Yahoo's waiver date (2026-11-18)

Pull window: 2026-11-18 → 2026-11-18 (no pull: kit main ecc2837, deck main 3551a15, the records branch season/daily at 2a61d547, read only; the week card and the deck page rebuilt in a throwaway worktree).

**Owner's request, verbatim (2026-11-18).** "Fix the Caruso waiver timing", after the session's report that this morning's "best adds this week" priced Alex Caruso as playing the same day while Yahoo's list had him on waivers until 2026-11-19.

**Method up front.** Stated to the owner before the change: the week card reads Yahoo's waiver date from the morning pull (the field the brief's waiver note already reads, `acquisitionState` "waivers" with `waiverDate`). A waiver player gets no "same day" timing unless the date is today or earlier; when it falls after tomorrow, a new timing, "after waivers", keeps the drop playing until that day and counts the add from it. Assumed and stated: a claim processes the morning of the waiver date, in time for that day's games (the league's `waiverTime` is 1 day, Flaim `get_league_info` 2026-11-17).

**Verdict. On this morning's records Caruso moves from "same day, 3 games, +0.271 expected categories" to "after tonight, 2 games, +0.219", and drops from second to below the five best adds; no free agent's figure changes.**

Runner impact: code-only (the week-matchup record's add rows gain `waiver_date`; the timing can read "after waivers"; the deck's games column says "from <date>" for it). No prompt, step or pass line changes.

Pool rows touched: none

## 1. On this morning's records

| add | before | after |
|---|---|---|
| Alex Caruso (on waivers until 2026-11-19) | same day, 3 games, +0.271 | after tonight, 2 games, +0.219 |
| Andre Drummond | after tonight, 3, +0.315 | unchanged |
| Tre Jones | same day, 3, +0.271 | unchanged |
| Kris Dunn | after tonight, 2, +0.262 | unchanged |
| Nic Claxton | same day, 2, +0.243 | unchanged |

EVIDENCE: `scripts/week_matchup.py --date 2026-11-18` re-run on season/daily 2a61d547; five rows carry a waiver date (Caruso, De'Anthony Melton, Cameron Johnson, Jaylen Wells, Ja'Kobe Walter, all 2026-11-19). The only other key that changed is the free-agent notice's copy of the top add, which gains `waiver_date` (null for Drummond). The deck page rebuilt from it: SEASON DECK PASS, 0 page errors; Caruso's row reads "2 · from tomorrow" beside the existing "on waivers until 2026-11-19" chip.

## 2. Checks

`scripts/test_week_matchup.py`: three new tests (a waiver player clearing tomorrow, after tomorrow and today; the drop keeps his games until the add clears; the waiver date read only for a waiver player). On the code before the change: 1 failure and 2 errors; after: all pass. The full suite and gates: below, from gates.py.

## 3. Bounds

Out of scope by design: the package scan (`package_scan.py`) still counts every move from tomorrow, which a one-day waiver period already matches; the waiver scan in the brief ranks for the season and prints the waiver date as before.

In scope and unverified:
- The claim-processing assumption: NOT-ATTEMPTED against Yahoo's own record of a processed claim; if claims process after that day's games, a waiver add counts one day later than priced.
- A real "after waivers" row (a date after tomorrow) has not occurred on the records; covered by the fixture test.

## 4. Decisions for the owner

1. This pull request: merge (the Runner's next week card uses it) or keep it as a draft.

## 5. Provenance

Session of 2026-11-18 (session model B), the Main session; branch `claude/waiver-timing`. Re-verify: `python3 scripts/test_week_matchup.py`; re-run `scripts/week_matchup.py --date 2026-11-18` on season/daily 2a61d547 with this branch's script.
