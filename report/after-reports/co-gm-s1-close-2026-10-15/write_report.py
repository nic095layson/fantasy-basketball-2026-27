#!/usr/bin/env python3
"""Writer for after-report-2026-10-15-co-gm-session1.md (Session 1 item 8) — figures read from records."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(KIT, "report", "after-reports", "after-report-2026-10-15-co-gm-session1.md")
rd = lambda n: open(os.path.join(HERE, n), encoding="utf-8").read()
stale = re.search(r"(\d+) row\(s\) over the limit", rd("check_provenance_still_red.txt")).group(1)
blocked = rd("espn_still_blocked.txt").splitlines()
brief = json.load(open(os.path.join(KIT, "report", "briefs", "brief_2026-10-21.json"), encoding="utf-8"))
cal = json.load(open(os.path.join(KIT, "report", "calibration.json"), encoding="utf-8"))["weeks"]["1"]
st = json.load(open(os.path.join(KIT, "data", "league_state.json"), encoding="utf-8"))
t = brief["title"]; m = (t["2026"] + t["2027"]) / 2
rn = rd("rn_section.md").rstrip() + "\n"
text = f"""# After-report — 2026-10-15: Session 1 closed — what runs, what it was tested against, what it cannot see, and the P1 sheet

**Owner request:** Session 1 item 8: "Closing after-report for Session 1: what runs, what it was tested against, what it cannot see, the decision sheet for P1."

**Scope delivered:** items 1, 2, 4, 5, 6 and 7 are merged. **Item 3 is blocked:** `check_provenance.py --max-age-days 14` still fails with {stale} stale rows, and `site.api.espn.com` still answers {blocked[0].split(':')[-1].strip()} at {blocked[-1]}.

**Method:** this report reads the merged records; each item's own after-report carries its evidence. No line, tag, team, price or placement changed in Session 1. Nothing was published.

Pull window: 2026-10-15 → 2026-10-15 (the session's records; no web research).

## 1. Roster changes

None to the pool. The league's rosters are in `data/league_state.json` (as of {st['as_of']}).

## 2. What runs

| item | what runs | command | tested against (red first) | PR |
|---|---|---|---|---|
| 1 | Rules, the open ledger, one gate runner | `scripts/gates.py --report R ... ; --verify --report R` | a naive exit-code runner (4 of 9 red); later the stale-record case (red), fixed in item 4 | kit #126, deck #123 |
| 2 | League settings and schedule; the simulator at 17 weeks with a reseeded bracket; `league_sim --schedule` | `scripts/test_settings.py`, `scripts/test_schedule.py` | old constants (3 of 8 red); `--schedule` ignored (red); `league_sim --verify` = arena draw for draw | kit #127, deck #124 |
| 3 | **Blocked:** provenance re-dating | `report/check_provenance.py --max-age-days 14` | red ({stale} rows); the live source is denied | — |
| 4 | Status feed: Yahoo letters → tiers with dated receipts; ESPN attempted every run | `scripts/status_feed.py`; `--check` | module missing; the real gate driven red (Durant at 1.00 with no receipt) | kit #130 |
| 5 | League state from the owner's rosters page | `scripts/league_intake.py` | halt on a missing name (seen); the IL-only exception (2 red); 162 of 162 resolved | kit #129 |
| 6 | The daily brief | `scripts/daily_brief.py --date D` | lineup matching beats slot-order greedy (test); the streaming sort bug caught on the first run, fixed red-first | kit #131 |
| 7 | Weekly preview and the append-only calibration ledger | `scripts/weekly_preview.py --week N --record`; `--score N --won ...` | module missing; a second record of week 1 refused on the real ledger | kit #132 |

**Today's numbers:**
- Title odds on today's rosters and the real schedule: {m:.1f}% (seeds {t['2026']:.2f}% / {t['2027']:.2f}%).
- Week 1: P(win) vs {cal['opponent_team']} is {cal['p_win']:.3f}, recorded {cal['recorded_at']}.

## 3. What it cannot see

- **News between the owner's pastes.** Yahoo is read from the owner's uploads, because Yahoo needs a login, and ESPN and the other sports hosts are denied by the environment.
- **In-season dynamics in the odds:** streaming, waivers, trades and IL moves (plan B3, P1).
- **Q/O statuses in the weekly and season model.** Only the daily lineup uses them (D-S1-11).
- **The two 14-day matchups (weeks 7, 17)** are modelled as one week (D-S1-2).
- **The other ten teams' real pairings.** Only the owner's opponents are known.
- **Calibration.** The model has never been graded against real games. The ledger starts that after week 1.
- **Every grade here is the house model's own (X-3).** The independent graders are P1 (D4).

## 4. Process notes (what this session caught in itself)

- **A stale `gates.json` once passed `--verify`:** a broken command chain left an earlier item's record in place. It was caught before merge and the tool was fixed red-first.
- **A carried repeat-name section said "30 of 30 mocks" when the replay ran 33.** It was regenerated from the run.
- **The streaming list sorted on a clamped value.** It was caught on the first run and fixed red-first.
- **Each PR was merged only after its gates passed, on the owner's "Merge".** The first merge attempt, before that word, was blocked by the permission system and not worked around.

## Watchlist

- Week 1 is scored on 10/26 from the owner's scoreboard paste.
- The 10/21 brief should be re-run that morning on a fresh paste.

## Open-item receipts

| item | query run (2026-10-15) | dated finding |
|---|---|---|
| (Session 1) | records only; the sports hosts are denied | — |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried (network blocked) |

{rn}
The section above is carried from item 1's run today; the page is unchanged, and the gate replays it.

## Bounds

**Out of scope by design.** Everything in plan §6's P1 and P2 lists.

**In scope and unverified.**
- Item 3, blocked by the network (ATTEMPTED-FAILED; receipts in `co-gm-s1-provenance-2026-10-15/` and this folder).

## Decision sheet for P1 (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-S1-6 | Allow `site.api.espn.com` in the environment's network settings. This unblocks item 3 and the ESPN injury feed. | Yahoo pastes only; item 3 stays open |
| D-S1-11 | Apply status tiers inside the weekly and season model (with B3, in-season dynamics) | P1, first |
| D-S1-2 | Model weeks 7 and 17 as double-length | P1, with B3 |
| D-S1-3 | Send the full league schedule (all 12 teams) | random pairings for the other ten |
| D-S1-7 | The Q tier (0.50) | until calibration says otherwise |
| D-S1-4 | Sourced pool row for Niederhäuser | keep the IL-only exception |
| D-LD-2 | Green for Braun: the waiver scan's best pair (one-seed +2.57 title points) | watch week 1; the brief re-scores it daily |
| D-SA-6 | SessionStart governor hook and the merge-refusal stop hook (D1) | P1 |
| D4 / X-3 | Independent graders (consensus lines, actuals) | P1 |
| B4, B5, A1, A4, A5 | The rest of plan §6's P1 list | P1 |

## Provenance

- This folder: `check_provenance_still_red.txt`, `espn_still_blocked.txt`, `rn_section.md`, this writer.
- Item reports: `after-report-2026-10-15-co-gm-{{rules,settings,league-state,status,daily-brief,weekly}}.md`.

## In plain language

Session 1 is done except one item: re-checking the old roster records, which needs a network setting changed on your side. The tool now:
- knows your league's real rules and your real schedule;
- knows every team's roster;
- reads injury letters from your Yahoo page;
- writes a daily note: who plays, your lineup, the best pickup, your title odds;
- predicts each week before it starts and grades itself afterwards.

What it still can't do: see news you haven't pasted, model streaming or trades, or prove it's accurate until real games are played.
"""
open(OUT, "w", encoding="utf-8").write(text); print("wrote", os.path.relpath(OUT, KIT))
