# After-report — 2026-10-07, third report: did the late-card problem touch the live tool (no, measured), the first WO-5 step (Castle and Barrett re-derived on both planes), and the mock bots' late-round value axis shipped by experiment (V4)

**Owner request (2026-10-07 evening, verbatim):** "Did this bug in the system also affect the Live Draft tool? Or Just mock against 11 personalities? Implement all fixes. Can you please remind me the differences between integration, integrity, validation, and all the other tests that I've requested?"

**Method:** the live-tool question is answered from the deck-card records of the ten human rooms (every owner turn's Top-5 as the page showed it at the time, `arena/results/m5x_deckcard_*.json`), scored against the v47 price set; the lines follow the WO-5 method on the 10/01 work order; the bot change follows the pre-registered experiment (`castsim_design_2026-10-07.md`, amendments 4 and 5). Every figure is read from a file named in Provenance. Verification: this file passes `report/check_report.py` and the deck's `judgment_open_items.py --check-report`; the gates table is §5.

Pull window: 2026-10-07 → 2026-10-07 (the third report of the day; no roster pull — the morning's `after-report-2026-10-07.md` is the pull, `after-report-2026-10-07-cast.md` the cast rooms and D-CAST-1/3/4).

**Headline.** The late-card problem did not reach the live tool in practice: across the ten human rooms (mocks 51–54, 56–61; 20 recorded deck cards incl. re-plays on later pages), the card's Top-5 in rounds 11–13 carried an unpriced row 0 times in 60 owner turns, had an unpriced #1 0 times, and you took an unpriced man 0 times and an unsigned man 0 times. The symptom appeared only in cast rooms (mock 55 at #154, then 62–65), because the value-leaning bots drain the priced value men before round 13 and leave the unpriced tail for a price-blind card; in human rooms the humans take the market names and leave priced value (Vassell, Washington, Grimes, Gillespie) for the late card. Both fixes shipped in v48 apply to every surface — the live tool and MOCK run the same page and engine — and the live room's DOM drive passes on it. This evening's two further fixes: **D-CAST-2, first step** — Castle and Barrett re-derived on both planes from their 2025-26 lines (deck value rank Castle 248 → 171, Barrett 236 → 193; kit board Castle 98 → 179, Barrett outside the top 200 before and after); and **V4** — the mock bots' value axis is Yahoo's XRank from round 7, shipped because the pre-registered N=30 run passed every term (mean pick gap to the humans 9.29 against 12.07, consensus names left undrafted 7.2 against 10.43 per room, personality guard Spearman 1). Deck v49 built, every gate green (§5), published.

## 1. Roster changes

No team label, tag or placement moved. Two lines were re-derived on both planes (the first WO-5 step, on the owner's 'implement all fixes').

| plane | row | line before (pts / reb / ast / stl / blk / 3PM / FG% on FGA / FT% on FTA / TO) | line after | mechanism | outlets |
|---|---|---|---|---|---|
| both | Stephon Castle (SAS) | deck 16.5 / 4.0 / 4.8 / 1.0 / 0.4 / 1.2 / .440 on 14.5 / .730 on 4.6 / 2.4; kit 18.5 / 5.0 / 6.0 / 1.2 / 0.4 / 1.5 / .460 on 14.5 / .780 on 4.5 / 2.6 at 32 min | 16.7 / 5.3 / 7.4 / 1.1 / 0.3 / 1.2 / .463 on 12.0 / .732 on 5.6 / 3.2 at 30 min (identical on both planes) | 2025-26 per-game at last season's 30.0 minutes; FG%/FT% shrunk one-third toward career (.447 / .729); no minutes claim — the Spurs have not played a preseason game yet (first 10/8) and Harper's push for a starting role is live | Basketball-Reference season table (read 2026-10-07); role context FantasyAlarm preview and ESPN (Mike Wright) via the same preview — not a line-moving claim |
| both | RJ Barrett (TOR) | 20.5 / 6.2 / 5.2 / 0.9 / 0.3 / 1.6 / .465 on 15.5 / .630 on 5.0 / 2.7 (the 2024-25-based line, identical on both planes) | 19.1 / 5.2 / 3.3 / 0.7 / 0.3 / 1.7 / .476 on 14.2 / .711 on 4.9 / 1.7 at 30 min | 2025-26 per-game at 30 minutes as the starter the row already carries; FG%/FT% shrunk one-third toward career (.447 / .700) | Basketball-Reference season table (read 2026-10-07); starter role 9/30 per SI Raptors and Yardbarker (on the row) |

Board effects. Kit (`rank_engine.py`): Castle 98 → 179 — the July kit line had him above his own 2025-26 production (18.5 pts on .780 FT; he shot .734 with 3.2 turnovers), so the honest line costs him on the kit; 94 other rows move by at most 3 places. Deck (value rank over the 319 draftable): Castle 248 → 171, Barrett 236 → 193; 78 rows move, none other by three or more. The two planes now agree on both men (planes gate: differing lines 171 → 170; Barrett's line was already identical). What this says about the owner's instinct: Castle is a 53rd-pick market price on a 9-cat production rank near 170 on both engines — the market is paying for role growth, which the preseason box scores will or will not confirm (watchlist).

## 2. Did it reach the live tool? — the record, room by room

Each recorded deck card of the human rooms (the Top-5 the page showed at every owner turn, on the page the room was drafted on; later re-plays on newer pages included), rounds 11–13 only; 'unpriced' = no Yahoo price on the v47 price set.

| room | page | late owner turns | unpriced rows in the Top-5 (of 15) | unpriced #1 | unpriced men taken | unsigned men taken |
|---|---|---|---|---|---|---|
| mock 51 | refit | 3 | 0 | 0 | 0 | 0 |
| mock 51 | v22 | 3 | 0 | 0 | 0 | 0 |
| mock 51 | v23 | 3 | 0 | 0 | 0 | 0 |
| mock 51 | v33 | 3 | 0 | 0 | 0 | 0 |
| mock 52 | refit | 3 | 0 | 0 | 0 | 0 |
| mock 52 | tuned | 3 | 0 | 0 | 0 | 0 |
| mock 52 | v23 | 3 | 0 | 0 | 0 | 0 |
| mock 52 | v33 | 3 | 0 | 0 | 0 | 0 |
| mock 53 | v25 | 3 | 0 | 0 | 0 | 0 |
| mock 53 | v33 | 3 | 0 | 0 | 0 | 0 |
| mock 54 | v28 | 3 | 0 | 0 | 0 | 0 |
| mock 54 | v33 | 3 | 0 | 0 | 0 | 0 |
| mock 56 | v31 | 3 | 0 | 0 | 0 | 0 |
| mock 56 | v33 | 3 | 0 | 0 | 0 | 0 |
| mock 57 | v33 | 3 | 0 | 0 | 0 | 0 |
| mock 58 | v35 | 3 | 0 | 0 | 0 | 0 |
| mock 59 | v37 | 3 | 0 | 0 | 0 | 0 |
| mock 59 | v39 | 3 | 0 | 0 | 0 | 0 |
| mock 60 | v42 | 3 | 0 | 0 | 0 | 0 |
| mock 61 | v44 | 3 | 0 | 0 | 0 | 0 |

Zero in every column, every room. In the cast rooms the same engine showed Thomas and Goodwin at #154 in all four of 62–65 (and two unpriced rows at #154 in mock 55). The mechanism is the room, not the tool: the value-leaning bots take the priced value men earlier than humans do, so the price-blind round-13 card was left with the unpriced tail. The rule shipped in v48 (priced rows only from round 11) is on for every room, and in the human rooms it changes nothing (there were no unpriced rows to remove).

## 3. V4 — the bots' late-round value axis, shipped by the pre-registered rule

Amendment 4 (written before the run): the XRank value axis from round 7 only, rounds 1–6 on the shipped formula; same metrics, seeds and ship rule as the first run. Result:

| variant | M1 mean abs pick gap | players scored | M2 consensus names left undrafted per room | M3 guard (Spearman vs V0 / mean abs change) | never drafted by the cast (of the human-reference set) |
|---|---|---|---|---|---|
| V0 (shipped before) | 12.07 | 147 | 10.43 of 143 | 1 / 0 | 12: Stephon Castle, Khaman Maluach, Maxime Raynaud, Kyshawn George, Kevin Porter Jr., Paul Reed, Jaime Jaquez Jr., RJ Barrett, Jimmy Butler, Dillon Brooks, Anthony Black, Jeremiah Fears |
| V4 | 9.29 | 153 | 7.2 of 143 | 1 / 0 | 6: Cameron Johnson, Kevin Porter Jr., Jaime Jaquez Jr., Jimmy Butler, Wendell Carter Jr., Darius Acuff Jr. |

V4 improves both fidelity metrics and leaves the personality guard at 1.0 by construction (rounds 1–6 unchanged), so it ships: `BOT_XRANK_FROM = 7` in the page's `managerScores`, the build bakes `PLAYERS[].xr` from the kit's Yahoo file (246 of 335 rows), red-first in `scripts/test_card.py` (three cases failed on the unchanged engine and build, 99 of 99 pass after). The cast now drafts Castle, Barrett and Brooks; the six human-reference names it still never takes are Cameron Johnson, Kevin Porter Jr., Jaime Jaquez Jr., Jimmy Butler, Wendell Carter Jr. and Darius Acuff Jr. The bots' first six rounds are untouched, so the eleven personalities measured by E18 are as they were.

## 4. The tests, in one table — what each one is for

| name the owner has used | what it actually checks | runs where | fails when |
|---|---|---|---|
| **unit / red-first** (`test_card.py`, `test_draft.py`, `test_gates.py`) | one function or rule at a time, on fixtures; a new rule's cases are written first and must FAIL on the unchanged code, then pass | deck, every build | the engine or the build no longer does what a rule says |
| **parity** (`check_parity.py`) | the deck's JavaScript and the kit-style Python engine compute the same numbers: z-scores, values, hashes, survival, clock reads, and the card's ordering at every owner turn of every committed room | deck, every build (~8 min) | the two engines disagree anywhere, so a grading in Python would not match what the page shows |
| **integration** (`full_dom_check.mjs`) | the whole page driven in a real browser through a recorded room: feed parsing, the card, the chips, the history, the seating — 130 assertions | deck, every build | something works in isolation but not when wired together on the page |
| **integrity / gates** (`build_deck.py` gates 1–7, `check_planes.py`) | the data is fit to publish: rosters verified today, the pool stamp matches the pool, the judgment layer is dated, the colophon prose matches the build, the two planes match on team, exclusion class, spelling and propagation | deck build | the data or its description drifted, even if every function is correct |
| **validation / calibration** (`live_retro.py`, `live_survival.py`, `target_wait.py`, the arms) | the system against outcomes: how the card's picks grade on the real bracket, whether the survival chips are calibrated, whether 🎯s passed on were still there | deck, after each room | the model is internally consistent but wrong about the world |
| **provenance / derived** (`check_provenance.py`, `check_derived.py`, `check_report.py`, `judgment_open_items.py --check-report`) | every team label has a dated source; every parsed market artifact reproduces byte-for-byte from its pinned inputs; every transaction row in a report names two outlets; every flagged judgment card has a receipt | kit, every report | a claim is on the page or in a report without the evidence that put it there |
| **experiment** (pre-registered: `castsim_design_*.md`, the pair experiment) | a proposed behavior change against a bar written down before the run; ships only if it passes | deck, on demand | the change would help by one measure but fail the guard that protects another |

## 5. Gates

| gate | result |
|---|---|
| deck build (gates 1–7) | safe to publish; gate 7 waivers ×3 (D-CAST-1, unchanged), team 0, exclusion 0, drift 0, propagation 0; differing lines 171 to 170 (Castle's planes now match) |
| roster lock | direct-complete, 334 of 335 rows on an official roster (Broome allowed, as in the morning) |
| scripts/test_card.py | 99 of 99 (four V4 cases added; 3 of 99 failed on the unchanged engine and build, all pass after) |
| scripts/test_gates.py / test_draft.py | all 37 cases passed / all 65 cases passed |
| scripts/check_parity.py | EXACT MATCH — 286 owner turns across 22 committed states, 335 pool rows, 3015 z-score cells, survival and clock reads bit-identical |
| arena/mocks/full_dom_check.mjs (state 54, a live human room) | 130/130 assertions, no page errors (`full_dom_check_2026-10-07_v49.json`) |
| D-CAST-3 follow-up experiment (V4) | pre-registered (amendment 4), run at N=30, passed every term, shipped (amendment 5) |
| kit rank_engine.py | board regenerated; Castle 98 to 179, 94 rows moved; provenance gate PASS |
| kit check_derived.py / check_provenance.py | 17 of 17 reproduce / PASS |
| kit check_report.py / deck judgment_open_items.py --check-report | PASS on this file (run after it was written; the PR records the run) |

## Watchlist

- Castle's minutes: the Spurs' first two preseason games (10/8 vs Atlanta, then the next) settle the Fox–Castle–Harper split; the line is re-checked then (WO-5 proper).
- WO-5 proper starts when every team has played twice: the remaining top-150 lines by the same method, Rotoworld's 25 divergences (D-RW-1) and the Hashtag rows 25+ places from the kit.
- The first live human room on v49 is the out-of-sample test for both the round-11 card rule and the new bots (which only MOCK rooms exercise).

## Open-item receipts

| item | query run (2026-10-07) | dated finding |
|---|---|---|
| (this analysis) | two web searches for Castle's and Barrett's preseason role (no Spurs preseason game played yet; no Raptors recap of 10/3 found); Basketball-Reference season tables read 2026-10-07; no other web research | pull receipts for the window live in `after-report-2026-10-07.md` (the morning's pull, same day) |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (after-report-2026-10-07.md, ten receipts dated 10/7) | all HELD or unsigned on 2026-10-07; the four unsigned stay out (D-CAST-1); nothing changed this evening |

## Bounds

- The live-tool measurement is on the price set of 10/6 applied to rooms drafted on earlier pages; the earliest rooms (51–54) were drafted before any Yahoo price was baked, so 'unpriced' there means 'unpriced today'. The conclusion does not depend on it: no late Top-5 row in any human room is a man Yahoo does not list today.
- The two lines use last season's minutes and a one-third career shrinkage stated as the convention; the WO-5 work order names the method but not the weight.
- V4 is measured against ten human rooms from one seat; the first six rounds are unchanged by construction, so the guard is passed by construction and the fidelity gain is entirely in rounds 7–13.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-CAST-2a | Castle and Barrett re-derived at last season's minutes (applied). Re-check Castle's minutes after the Spurs' first two preseason games and move the line only on two dated outlets? | yes |
| D-CAST-2b | Proceed with WO-5 proper (the remaining top-150 lines, same method, both planes) as soon as every team has played twice? | yes |
| D-V4-1 | The bots' round-7+ XRank value axis shipped by the pre-registered rule (applied). Keep it, with the next MOCK rooms as its out-of-sample check? | yes |
| D-CAST-1, D-CAST-3, D-CAST-4, D-C64-1, D62-1..3 and earlier | carried | carried |

## Provenance

- The live-tool table: `arena/results/m51–m61_deckcard_*.json` (the page's own Top-5 at each owner turn, replayed on the page each room was drafted on) scored against the v47 page's `PLAYERS[].mkt`.
- Lines: `arena/results/dcast_lastseason_2026-10-07.json` and the Basketball-Reference season tables read 2026-10-07 (the derivation script and its dry-run output are in the session scratchpad; the identical line is asserted on both planes); board diffs computed from the regenerated `top-200-2026-27.md` against the v48 regeneration and from the v48 and v49 pages' value ranks.
- V4: `arena/results/castsim_design_2026-10-07.md` (amendments 4 and 5) and `castsim_n30_v4_2026-10-07.json`.
- Not verified by web research: the two searches found no 2026-27 preseason box score for either man; no line rests on a search summary.

## In plain language

**Your question.** Did the late-card problem affect the live draft tool, or only the practice rooms against the eleven? I checked the record rather than reasoning about it: every card the tool showed you in your ten human rooms, rounds 11 through 13. It never put a man Yahoo does not list in the top five, never put one at #1, and you never took one. The problem showed up only against the bots, because the bots take the priced value players earlier than humans do and leave the unpriced tail for the last round. The fixes already shipped apply everywhere, since the live tool and the practice mode are the same page.

**What was implemented.** Two more fixes. Castle's and Barrett's lines were rebuilt on both planes from what they actually did last season, which raises both of them on the deck and lowers Castle on the kit; the two planes now agree on both men, and both land around 170 to 190 in 9-cat production, which is why neither engine will draft Castle at Yahoo's 53. And the bots were changed by experiment: from round 7 they weigh Yahoo's own rankings as their value axis, which closed a third of their gap to your human rooms and left the eleven personalities exactly as they were in the early rounds; they now draft Castle, Barrett and Brooks.

**What stayed open.** Castle's minutes depend on the Fox–Castle–Harper split, and the Spurs have not played a preseason game yet; the line is re-checked after their first two. The full projection refresh starts when every team has played twice.

**The tests.** Unit tests check one rule at a time and are written to fail first. Parity checks that the page's JavaScript and the Python engine agree to the digit. Integration drives the whole page in a real browser through a recorded room. Integrity gates check the data is fit to publish and that the two planes agree. Validation checks the system against outcomes: how the picks grade, whether the chips are calibrated. Provenance checks that every claim carries its source. Experiments test a proposed change against a bar written down before the run. Section 4 has the table.
