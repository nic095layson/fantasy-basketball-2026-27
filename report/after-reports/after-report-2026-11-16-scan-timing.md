# Pickup scan prices a same-day swap (owner pick 2026-11-16, "Price both timings")

Pull window: 2026-11-16 → 2026-11-16 (no pull: kit main fa2f001; the records branch season/daily read only, re-run in a throwaway worktree with the 11-16 statuses and Yahoo's live tags of 9 AM Pacific).

**Owner's words, verbatim:** "Spencer has 11/16, 11/18, 11/19 and 11/21 games... which is 4 games this week. Please ensure that system and your calculations are all operating with robust integrity." Pick on the card that followed: "Price both timings (Recommended)".

**Method up front.** The week card's pickup scan (`week_matchup.scan_this_week`) priced every free agent as "the drop plays today, the add counts from tomorrow", so a free agent whose team plays today never had today's game counted, though the league counts a same-day add made before tip (OWNER-PLAYBOOK, 11-14). The rule was stated to the owner before the build; tests were written first and seen failing.

**Verdict: built. When the add's team plays today, the scan also prices the same-day swap (drop and add before tip) and keeps the better timing for each drop, labelled on the row and on the deck.**

Runner impact: code-only — the morning and afternoon week cards pick it up from `week_matchup.py`; no step, record or prompt changes.

Pool rows touched: none

## 1. What changed

| Part | Rule |
|---|---|
| Same-day pricing | Only when the add's team plays today: the drop loses today's game, the add counts from today; the drop-alone share is priced with the same timing |
| Choice | Per drop, the better timing is kept; a tie keeps tonight's game; the other timing's change and starts ride on the row (`other_timing`) |
| Row fields | `timing` ("after tonight" or "same day"), `games` = starts under that timing, `games_left` counted to match |
| Deck | The games cell reads "4 · today" or "3 · from tomorrow", with the other timing beneath ("3 if after tonight") |

## 2. Checks

| Check | Result |
|---|---|
| New tests seen failing first | Card 3, deck 1 |
| Two earlier tests pinned the old rule ("t0 is before the swap", a today-only free agent scoring 0) | Updated to the owner's rule; each now asserts the after-tonight figure on the row as well |
| Week 5 on the 11-16 records | Cam Spencer 4 starts (same day), Robert Williams III 4 (same day), Kris Dunn 3 and Andre Drummond 4 (after tonight: neither team plays today) |
| Independent re-computation in scratch | Williams same day for Hezonja +0.424, P(5+) 93.1%; Spencer +0.215, 90.1%: the same figures as the hand table given to the owner before the build |
| New finding from the scan | With same-day pricing the best drop for Williams and Spencer is PJ Washington (Dallas has no game today), not Hezonja: Williams +0.457 (93.3%), Spencer +0.227 (90.4%) |

## 3. Bounds

Out of scope by design: the waiver pairs of the brief and the decision card (season pricing, no timing); Yahoo's waiver-claim delay for players on waivers (the scan's pool is the free agents Yahoo lists; a waiver player's same-day figure assumes an immediate add).

In scope and unverified: tip-off times are not in the schedule file, so "before tip" relies on the owner acting before both teams' games start.
