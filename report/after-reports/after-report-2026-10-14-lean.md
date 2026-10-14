# After-report — 2026-10-14 (lock day, pre-draft): the LEAN roster-balance line counted position tokens, not players — fixed on both engines, deck Version 70

**Owner request (2026-10-14, verbatim):** "Can you please adjust this where: System is saying I have 7G, but in reality that is 'G eligible' it is saying I am overloaded in a position when I am not. I hope it is not affecting the computation"; then "I just want to ensure, this is not changing your arithmetic computation right? The positional counting"; then "Publish fix now and grade Mock 82".

Pull window: 2026-10-14 → 2026-10-14 (a display fix on the deck page; no roster pull, no line, tag, price or placement change on either plane).

**Headline.** The ⚠ LEAN line under the card tallied position *tokens* — a PG,SG player counted as two guards — so the owner's six-man roster of four dual-eligible guards and two forwards read "7G vs 2F". It is a warning line only: the card's 🎯 ordering never reads positions, and the TARGET read uses the family counter that already counted each player once (the one printing "G (4) F (2) C (2)"). The line now counts players once per family on the page and on its Python twin (3 files, +35/−5 lines). Red-first: the new test reproduces the owner's exact "7G vs 2F" on the pre-fix engine (2 of 67 cases fail), then all 67 pass. The owner's roster rendered in Chromium: old page "⚠ LEAN: 7G vs 2F — flag for roster balance", new page no LEAN line, census "G (4)  F (2)  C (2)" on both. Chain green on the fixed page (parity EXACT 481 turns / 37 states; card 103, draft 67, gates 54; DOM 145/0); published as Version 70 (id 1792013103-d68e), byte-verified at offset 349.

## 1. Roster changes

None. No line, tag, placement or price changed on either plane; the pool sha256 is unchanged. The page's JavaScript and `scripts/hoops.py` changed in one place each, plus the dated note in the page's Logic paragraph.

## 2. What was wrong, and what was not

EVIDENCE: `fix.diff`; the page at `docs/draft-deck.html` (the LEAN line, `posCounts`), `scripts/hoops.py` (`pos_counts`); the TARGET read's `balCt` / `familiesOf` and the roster header's `famN`.

- The LEAN line summed `posCounts.PG + posCounts.SG` against `posCounts.SF + posCounts.PF`, where `posCounts` counts every position string a player carries. Derrick White (PG,SG), Devin Booker (PG,SG) and Tyrese Haliburton (PG,SG) each counted twice, Desmond Bane (SG,SF) once on each side: 7 against 2. The Python twin did the same.
- The 🎯 and the card's +/− cats-per-week numbers are the blend50 score (marginal weekly category wins against the room plus balanced value); positions do not enter it. The TARGET / BOARD LEAN read uses `familiesOf(p)` and `balCt`, which count a player once per family and compare against the startable floor; the roster header's `G (4) F (2) C (2)` is the same counter. Neither changed, and neither was wrong.
- The fix: `g` = players eligible at PG or SG, `f` = players eligible at SF or PF, each player once; threshold unchanged (|G − F| ≥ 4 at five or more players). On the owner's roster: 4 against 2, no line.

## 3. Verification

| check | result |
|---|---|
| red-first: the two new `test_draft.py` cases against the pre-fix engine (`test_draft_red.txt`) | 2 of 67 FAIL, the first printing "⚠ LEAN: 7G vs 2F" — the owner's exact line |
| the same suite after the fix (`test_draft_green.txt`) | all 67 cases passed |
| the owner's screenshot roster (picks #10 Haliburton, #15 Towns, #34 Booker, #39 White, #58 Okongwu, #63 Bane) fed into the real page in headless Chromium (`lean_demo.txt`, `events_screenshot.json`, `arena/mocks/lean_dom_check.mjs`) | old page: "⚠ LEAN: 7G vs 2F — flag for roster balance"; new page: no LEAN line; census "G (4)  F (2)  C (2)" on both |
| `check_parity.py` on the fixed page (`chainA.log`) | PARITY: EXACT MATCH — 481 owner turns across 37 committed states |
| `test_card.py` / `test_draft.py` / `test_gates.py` | all 103 / all 67 / all 54 |
| `full_dom_check.mjs` (`chainB.log`) | 145 assertions, 0 failed, 0 page errors |
| `identity_check.py` / `check_planes.py` | exit 0 / planes team 0 exclusion 0 drift 0 propagation 0 on 315 shared rows |
| publish | Version 70, id 1792013103-d68e, the built page (sha256 beb243ef57af) found whole in the served file at offset 349 (688,795 bytes served) |

## Watchlist

- The publish freeze during the draft (D-1013-5) and no RESYNC during the draft (D-1013-2) stand; this publish precedes the draft.
- `arena/mocks/lean_dom_check.mjs` stays as a harness for roster-balance questions: any pick list, any page.

## Open-item receipts

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| (this fix) | records only; no web research and no roster pull | display fix; the pool sha256 unchanged |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this fix (did not check) |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 e68a85a5305f), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 30 of 30 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-14.csv`, Hashtag `hashtag-2026-10-14.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-14.csv`, `hashtag-2026-10-14.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 29 of 30 | 44 | 111 | 63 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 22 of 30 | 32 | 67 | 58 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 12 of 30 | 107 | 138 | 182 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 12 of 30 | 101 | 182 | 100 | 125 | 148 | 155 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Brandin Podziemski | 11 of 30 | 93 | 146 | 74 | 102 | 114 | 132 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| John Collins | 11 of 30 | 73 | 117 | 105 | 72 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 9 of 30 | 92 | 179 | 89 | 117 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 8 of 30 | 6 | 32 | 15 | 24 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Jaden McDaniels | 6 of 30 | 62 | 90 | 42 | 67 | 86 | 59 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 5 of 30 | 114 | 139 | 122 | 130 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Immanuel Quickley | 5 of 30 | 67 | 94 | 65 | 73 | 79 | 84 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Keegan Murray | 5 of 30 | 83 | 142 | 82 | 94 | 102 | 85 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (18 mocks, value 9, market 18); Derrick White (15 mocks, value 27, market 45); Lauri Markkanen (14 mocks, value 21, market 37); Tyrese Haliburton (12 mocks, value 7, market 12); Tyler Herro (9 mocks, value 51, market 69); Tyrese Maxey (9 mocks, value 5, market 9); Kel'el Ware (8 mocks, value 57, market 77); Karl-Anthony Towns (6 mocks, value 12, market 15).


## Bounds

**Out of scope by design.**
- No change to the lean threshold or to any engine computation; no line, tag, price or placement change.
- The repeat-name check was not re-run: the lines are byte-identical to the lock's (30 of 30 mocks, 12 flagged on the same pool).

**In scope and unverified.**
- None: every claim above is a run on this page's bytes.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| (none new) | the fix was the owner's call ("Publish fix now") | applied |
| D-INT-1, D-INT-2, D-1014-*, D-1013-*, earlier | carried | carried |

## Provenance

- Deck: `scripts/hoops.py`, `docs/draft-deck.html`, `scripts/test_draft.py` (+2 cases), `arena/mocks/lean_dom_check.mjs` (new); page sha256 beb243ef57af; published 1792013103-d68e after a fresh read of 1792001219-01f3.
- This folder: `fix.diff`, `test_draft_red.txt`, `test_draft_green.txt`, `lean_demo.txt`, `events_screenshot.json`, `chainA.log`, `chainB.log`, `publish.json`, `rn_section.md`, this writer.
- No line, tag or placement changed on either plane.

## In plain language

**What was wrong.** The warning line under the card counted White, Booker and Haliburton twice each because each is listed at both PG and SG. It said 7 guards; you had 4. It was only that warning line.

**What was not wrong.** The card's recommendation and its numbers never look at positions, and the roster header's "G (4) F (2) C (2)" was already counting correctly. Nothing in the arithmetic changed.

**What was done.** The line now counts each player once. A new test fails on the old code with your exact "7G vs 2F" and passes on the new; your roster rendered in a real browser shows the line gone; every check in the chain passes; the page on your link is Version 70, byte-verified.
