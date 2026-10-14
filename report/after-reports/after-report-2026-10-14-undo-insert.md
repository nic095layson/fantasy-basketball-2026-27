# After-report — 2026-10-14: Undo and Insert-at-# integrity on the Version 68 page

**Owner request (2026-10-14, verbatim):** "Hi Claude, can you please test, validate integrity, that when using the “undo pick” and “insert at #” features are used, the arithmetic computation and correct team association is accurate?" Read as an assessment: test and report; nothing on the page changes (the publish freeze holds).

**What was analyzed:** the published Version 68 page (sha256 b83d1cdcc0e9, version id 1791993066-d8ff), driven in headless Chromium by `undo_insert_check.mjs`. **Method (stated to the owner before the run):** a PATH page reaches a final pick list through Undo and Insert-at-# (the owner's corrections); a clean ORACLE page is fed the same list in one feed; every derived value is compared — the picks and their seats (every seat also held to the snake formula), each team's roster, the nine z-total categories per team, the owner's category ranks, the next-pick clock, the available pool, the Top-5 card, the visible text of all five tabs — and the latest history line for each pick is held to the state. Each team's totals are re-computed independently in Python from the deck's own data (`hoops.py`).

Pull window: 2026-10-14 → 2026-10-14 (analysis only; no roster pull; no page change).

**Headline.** Undo and Insert-at-# keep the arithmetic and the team association exact. In 9 hand-built cases and 10 seeded full 156-pick drafts (90 inserts, 203 undos, 113 wrong picks logged and undone; each draft compared at a mid-draft checkpoint and at the end), every pick sat on the correct seat, and every roster, category total, rank, clock, pool and Top-5 card equalled the clean page. 2,916 team-by-category totals re-computed in Python agree within 4.1e-06 (the page bakes each player to six decimals). Three display quirks were found; none changes a number (§3).

## 1. Roster changes

None. No line, tag, placement, price or page byte changed; this is a test of the shipped page.

## 2. Results

EVIDENCE: `run_a_2026-10-14.json` (the hand cases and seeds 1–5), `run_b_2026-10-14.json` (seeds 6–10), the `_totals` dumps, `totals_oracle.py`.

| check | result |
|---|---|
| hand cases (A, B, C, D, E, E2, F, G, H): undo and re-log; an insert crossing the owner's seat (#12, moving #15 and #16 on and off YOUR seat); insert at #1; insert at the end; insert ahead of a standing UNKNOWN (renamed to its new number); undo after insert; refusals (past the end, already drafted, #0, an off-snake my: pick) change nothing; reload | 54 of 54 assertions pass |
| seats equal the snake formula, final list equals the intended draft, history's latest line per pick equals the state (random drafts) | 60 of 60 pass |
| the advice line at mid-draft checkpoints equals the clean page | 10 of 10 |
| every derived value equals the clean page (random drafts, checkpoints and ends) | 6 of 20 pass; the 14 that differ differ in no number (picks, seats, rosters, totals, ranks, clock, pool and Top-5 all equal) — only the punt advisor's wording (§3, Q3) |
| Python re-computation of every team's nine totals | 2,916 cells, largest gap 4.1e-06 (tolerance 6.5e-06: 13 players × half a sixth-decimal) |
| category ranks against Python | 11 rank cells differ by one place; each is an exact tie (largest gap between the two teams 2.2e-15), and the page and the clean page match on every one |
| page errors | 0 |

## 3. Three display quirks (no number changes)

- **Q1 — the history box after Undo then Insert.** Insert re-numbers the history from the state; lines for picks that were undone are re-rendered too, with whoever now holds that number. Reproduction (`repro_history.mjs`, 12 picks, Undo 3, three different players logged, a missed pick inserted at #2): the history shows "✓ (R1) #11: Josh Giddey → Seat 11" just before "↶ undid: …" lines for other players, and "· #11 Josh Giddey is no longer your pick after the shift" twice. The state equals a clean feed of the same picks.
- **Q2 — the advice line after the last pick.** When the draft completes the card renderer returns before it clears the advice line (`docs/draft-deck.html`: the `draftDone()` return in the card renderer comes before `alBox.classList.add("hidden")`), so the last "Take …" sentence stays on screen. Any draft, not only corrections.
- **Q3 — the punt advisor's "2 picks running".** Its counter counts owner turns the page rendered (`st.leanSeen`, ticked when the pick count differs from `st.leanSeenAt`), so the same picks entered one at a time and in one batch word it differently (measured: every one of the differing comparisons above). From the code (INFERENCE, not measured): undoing back across an owner turn, or an insert, can count a turn twice, so the message can arrive a turn early. Advice only; no button writes the punt box.

## Watchlist

- The publish freeze during the draft (D-1013-5) and no RESYNC during the draft (D-1013-2) stand; Q1–Q3 are carried to after the draft.

## Open-item receipts

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| (this test) | records only; no web research and no roster pull | the page tested is the published Version 68, byte-identical (sha256 b83d1cdcc0e9) |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | this morning's final pull (`after-report-2026-10-14.md`, receipts dated 10/14) | as recorded there; not re-queried for this test (did not check) |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 b83d1cdcc0e9), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 29 of 29 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-13.csv`, Hashtag `hashtag-2026-10-12.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-13.csv`, `hashtag-2026-10-12.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 29 of 29 | 41 | 117 | 48 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 20 of 29 | 90 | 180 | 56 | 118 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 12 of 29 | 34 | 65 | 60 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 9 of 29 | 105 | 138 | 181 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| John Collins | 9 of 29 | 72 | 118 | 102 | 71 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 9 of 29 | 6 | 32 | 15 | 16 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 8 of 29 | 100 | 183 | 100 | 126 | 148 | 155 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 5 of 29 | 114 | 141 | 120 | 131 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (19 mocks, value 9, market 18); Lauri Markkanen (16 mocks, value 20, market 37); Derrick White (13 mocks, value 27, market 45); Tyrese Haliburton (12 mocks, value 7, market 12); Tyrese Maxey (8 mocks, value 5, market 9); Kel'el Ware (7 mocks, value 57, market 77); VJ Edgecombe (6 mocks, value 61, market 75).


## Bounds

**Out of scope by design.** Mock mode (the owner's draft is LIVE); RESYNC (covered 10/13); any fix (freeze).

**In scope and unverified.** Q3's double count is read from the code and not reproduced (`NOT-ATTEMPTED`; not load-bearing: it moves advice wording, no number).

## Decision sheet (owner disposes)

| id | decision | options | recommendation |
|---|---|---|---|
| D-1014-9 | Q1, the history box after Undo then Insert | (a) leave through the draft; fix after (relabel skips lines whose pick was undone); (b) fix now (breaks the freeze) | (a) |
| D-1014-10 | Q2, the stale advice line after the last pick | (a) leave; clear it in the draft-complete branch after the draft; (b) fix now | (a) |
| D-1014-11 | Q3, the punt advisor counter | (a) leave; key the counter to the owner's pick number after the draft; (b) fix now | (a) |

## Provenance

- `undo_insert_check.mjs` (the harness; runs A and B, two processes), `totals_oracle.py`, `repro_history.mjs`, this writer; records beside them. The trial run (`trial_2026-10-14.json`) found the harness's own two faults (an open insert bar compared to a closed one; the stale advice line at draft end) before the full runs.

## In plain language

Undo and Insert-at-# are safe to use in the draft. Across 9 hand-built cases and 10 full practice drafts with 90 inserts and 203 undos, every pick landed on the right team and every total, rank and recommendation matched a clean entry of the same picks. Three display quirks, none of which changes a number: the history box can look muddled after an undo followed by an insert; the last advice sentence stays up after the final pick; and the punt advisor's "2 picks running" can be off by a turn. Trust the Rosters tab, the board and the card — they are always rebuilt from the actual picks.
