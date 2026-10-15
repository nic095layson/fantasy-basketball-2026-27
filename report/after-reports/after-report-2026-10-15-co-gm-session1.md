# After-report — 2026-10-15: Session 1 closed — what runs, what it was tested against, what it cannot see, and the P1 sheet

**Owner request:** Session 1 item 8: "Closing after-report for Session 1: what runs, what it was tested against, what it cannot see, the decision sheet for P1."

**Scope delivered:** items 1, 2, 4, 5, 6 and 7 are merged. **Item 3 is blocked:** `check_provenance.py --max-age-days 14` still fails with 320 stale rows, and `site.api.espn.com` still answers (56) CONNECT tunnel failed, response 403 at 2026-10-15T20:37:35Z.

**Method:** this report reads the merged records; each item's own after-report carries its evidence. No line, tag, team, price or placement changed in Session 1. Nothing was published.

Pull window: 2026-10-15 → 2026-10-15 (the session's records; no web research).

## 1. Roster changes

None to the pool. The league's rosters are in `data/league_state.json` (as of 2026-10-15).

## 2. What runs

| item | what runs | command | tested against (red first) | PR |
|---|---|---|---|---|
| 1 | Rules, the open ledger, one gate runner | `scripts/gates.py --report R ... ; --verify --report R` | a naive exit-code runner (4 of 9 red); later the stale-record case (red), fixed in item 4 | kit #126, deck #123 |
| 2 | League settings and schedule; the simulator at 17 weeks with a reseeded bracket; `league_sim --schedule` | `scripts/test_settings.py`, `scripts/test_schedule.py` | old constants (3 of 8 red); `--schedule` ignored (red); `league_sim --verify` = arena draw for draw | kit #127, deck #124 |
| 3 | **Blocked:** provenance re-dating | `report/check_provenance.py --max-age-days 14` | red (320 rows); the live source is denied | — |
| 4 | Status feed: Yahoo letters → tiers with dated receipts; ESPN attempted every run | `scripts/status_feed.py`; `--check` | module missing; the real gate driven red (Durant at 1.00 with no receipt) | kit #130 |
| 5 | League state from the owner's rosters page | `scripts/league_intake.py` | halt on a missing name (seen); the IL-only exception (2 red); 162 of 162 resolved | kit #129 |
| 6 | The daily brief | `scripts/daily_brief.py --date D` | lineup matching beats slot-order greedy (test); the streaming sort bug caught on the first run, fixed red-first | kit #131 |
| 7 | Weekly preview and the append-only calibration ledger | `scripts/weekly_preview.py --week N --record`; `--score N --won ...` | module missing; a second record of week 1 refused on the real ledger | kit #132 |

**Today's numbers:**
- Title odds on today's rosters and the real schedule: 22.0% (seeds 22.18% / 21.90%).
- Week 1: P(win) vs DEVIN ELEVEN DOUBLES is 0.606, recorded 2026-10-15T20:26:51Z.

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

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 beb243ef57af), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 33 of 33 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-14.csv`, Hashtag `hashtag-2026-10-14.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-14.csv`, `hashtag-2026-10-14.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 32 of 33 | 44 | 111 | 63 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 23 of 33 | 32 | 67 | 58 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 14 of 33 | 107 | 138 | 182 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 12 of 33 | 101 | 182 | 100 | 125 | 148 | 155 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| John Collins | 12 of 33 | 73 | 117 | 105 | 72 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Brandin Podziemski | 11 of 33 | 93 | 146 | 74 | 102 | 114 | 132 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 10 of 33 | 6 | 32 | 15 | 24 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 10 of 33 | 92 | 179 | 89 | 117 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Jaden McDaniels | 7 of 33 | 62 | 90 | 42 | 67 | 86 | 59 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 6 of 33 | 114 | 139 | 122 | 130 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Immanuel Quickley | 5 of 33 | 67 | 94 | 65 | 73 | 79 | 84 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Keegan Murray | 5 of 33 | 83 | 142 | 82 | 94 | 102 | 85 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (18 mocks, value 9, market 18); Derrick White (17 mocks, value 27, market 45); Lauri Markkanen (15 mocks, value 21, market 37); Tyrese Haliburton (13 mocks, value 7, market 12); Tyrese Maxey (11 mocks, value 5, market 9); Kel'el Ware (10 mocks, value 57, market 77); Tyler Herro (9 mocks, value 51, market 69); Karl-Anthony Towns (8 mocks, value 12, market 15); Miles Bridges (5 mocks, value 96, market 98).

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
- Item reports: `after-report-2026-10-15-co-gm-{rules,settings,league-state,status,daily-brief,weekly}.md`.

## In plain language

Session 1 is done except one item: re-checking the old roster records, which needs a network setting changed on your side. The tool now:
- knows your league's real rules and your real schedule;
- knows every team's roster;
- reads injury letters from your Yahoo page;
- writes a daily note: who plays, your lineup, the best pickup, your title odds;
- predicts each week before it starts and grades itself afterwards.

What it still can't do: see news you haven't pasted, model streaming or trades, or prove it's accurate until real games are played.
