# After-report — draft_80: the 10/14 afternoon live room from slot 10, on deck Version 68

**Owner request (2026-10-14, verbatim):** "Thank you. First live mock for today:" followed by the deck tool's LIVE feed, the owner's 13-man roster and Yahoo's round-by-round recap (`draft80-2026-10-14/owner_message.txt`). Read as the standing request for these pastes: grade the room with the deck pipeline and report; no line, tag or price changes (Version 68 is the lock page).

**Room:** public Yahoo mock, 12 × 13, owner seat 10 (random humans; a practice rep, not opponent intel; display names: 1 DMT, 2 Justin, 3 Smitty, 4 James, 5 Zed, 6 Anteo, 7 Braden, 8 Gary, 9 harris, 10 David, 11 reyan, 12 The_DON). **Deck used:** Version 68 (rev `cb1a922`, the final morning pull and the owner's three lock calls; Porziņģis veto live). Replaying the owner's tool log through the Version 68 page reproduces all five "off the card" lines of the paste character for character; through Version 67 one differs (page: "⚠ off the card: Yaxel Lendeborg ranks #4 (0.017 behind 🎯 Myles Turner) — round-9+ rule (D54-1): take the 🎯"), so the room was drafted on Version 68.

Pull window: 2026-10-14 → 2026-10-14 (analysis only; no roster pull; Version 68 is the locked page).

**Headline.** As drafted **23.84 percent** for the title on the real eight-team bracket, rank 1 of 12, playoffs 98.38 percent. Expected weekly category wins 5.054, rank 1 of 12, favored in 11 of 11 head-to-heads. Following the card's 🎯 from the same seat (the self-consistent chain) grades 31.75 percent. The owner took the 🎯 at 8 of 13 turns and stayed in the Top 5 at 13; the largest single swap is #111 Myles Turner (27.45 percent, +3.61 points). The tool log is clean: the board the tool held equals Yahoo's recap at 156 of 156 picks, after three typed names were fixed by number (one of them four picks later).

## 1. Roster changes

None. No line, tag, placement or price changed on either plane; this is a grade of a practice room.

## 2. The team, graded

EVIDENCE: `arena/results/m80_final.json`, `m80_arms.json` (18,000 seasons per arm, seeds 11/23/47, the real eight-team bracket), pool tag v68 = `players_v68.csv` (data/players.csv at `cb1a922`, sha256 30246ac015fe).

| arm | title % | playoffs % | rank |
|---|---|---|---|
| as drafted | 23.84 | 98.38 | 1 |
| follow the card's 🎯 at every turn (self-consistent chain: #10 Tyrese Maxey, #15 Jalen Johnson, #111 Myles Turner, #130 Reed Sheppard) | 31.75 | 99.72 | 1 |
| single swap at #111: Myles Turner | 27.45 | 99.37 | 1 |
| single swap at #135: Draymond Green | 27.35 | 99.26 | 1 |
| single swap at #130: Draymond Green | 26.52 | 99.10 | 1 |
| single swap at #15: Jalen Johnson | 26.30 | 98.91 | 1 |
| single swap at #10: Tyrese Maxey | 26.20 | 98.93 | 1 |
| single swap at #106: Myles Turner | 25.79 | 99.04 | 1 |
| single swap at #58: Michael Porter Jr. | 25.31 | 98.65 | 1 |
| single swap at #154: Bobby Portis | 25.14 | 98.71 | 1 |
| single swap at #34: Domantas Sabonis | 25.12 | 98.66 | 1 |

Category shape (weekly model, rank of 12): FG% 8, FT% 1, 3PTM 2, PTS 11, REB 7, AST 12, ST 2, BLK 9, TO 1.

For scale, the other live public rooms graded on this bracket: mock 67 17.51, mock 68 28.36, mock 73 34.17, mock 74 17.91, mock 75 29.39, mock 77 35.98, mock 78 19.48, mock 79 25.65.

## 3. Pick by pick: the page's card, the owner, hindsight

EVIDENCE: `m80_deckcard_v68.json` (the Version 68 page's own engine), `m80_hindsight.json` (every single-swap alternative scored by weekly category wins against the final rosters).

| pick | owner took | card rank | the page's 🎯 | hindsight's best alternative (Δ weekly cat wins) |
|---|---|---|---|---|
| #10 | Tyrese Haliburton | 2 | Tyrese Maxey | Tyrese Maxey (+0.075) |
| #15 | Karl-Anthony Towns | 2 | Kawhi Leonard | Jalen Johnson (+0.097) |
| #34 | Kawhi Leonard | 1 | Kawhi Leonard | Domantas Sabonis (+0.085) |
| #39 | Derrick White | 1 | Derrick White | Donovan Clingan (-0.020) |
| #58 | OG Anunoby | 1 | OG Anunoby | Michael Porter Jr. (+0.062) |
| #63 | Kel'el Ware | 1 | Kel'el Ware | Tyler Herro (-0.004) |
| #82 | VJ Edgecombe | 2 | Ty Jerome | Myles Turner (-0.001) |
| #87 | Ty Jerome | 1 | Ty Jerome | Myles Turner (-0.011) |
| #106 | Miles Bridges | 1 | Miles Bridges | Myles Turner (+0.068) |
| #111 | Yaxel Lendeborg | 4 | Isaiah Hartenstein | Myles Turner (+0.142) |
| #130 | Cameron Johnson | 2 | Reed Sheppard | Draymond Green (+0.121) |
| #135 | Christian Braun | 1 | Christian Braun | Draymond Green (+0.151) |
| #154 | Tari Eason | 1 | Tari Eason | Bobby Portis (+0.059) |

The turns off the 🎯: #10 Tyrese Haliburton (card #2, 🎯 Tyrese Maxey, taken #11 by seat 11), #15 Karl-Anthony Towns (card #2, 🎯 Kawhi Leonard, taken #34 by seat 10), #82 VJ Edgecombe (card #2, 🎯 Ty Jerome, taken #87 by seat 10), #111 Yaxel Lendeborg (card #4, 🎯 Isaiah Hartenstein, taken #112 by seat 9), #130 Cameron Johnson (card #2, 🎯 Reed Sheppard, taken #146 by seat 2).

## 4. Tool-state integrity

recap picks 156; seats 12 (David = 10); pool-less 0: []; feed vs recap: 156 of 156 agree on name and seat; differences []; feed picks still UNKNOWN at the end: []; owner picks: #10 Tyrese Haliburton, #15 Karl-Anthony Towns, #34 Kawhi Leonard, #39 Derrick White, #58 OG Anunoby, #63 Kel'el Ware, #82 VJ Edgecombe, #87 Ty Jerome, #106 Miles Bridges, #111 Yaxel Lendeborg, #130 Cameron Johnson, #135 Christian Braun, #154 Tari Eason. The owner's tool log as pinned in `arena/data/events/m80_tool_events.json` (159 events: 159 feeds, 3 of them raw texts that resolved to UNKNOWN ("Toung" at #13, "Borles" at #93, "KPH" at #133), 3 numbered fixes (#13 Trae Young, #93 Collin Murray-Boyles, #133 Kevin Porter Jr.; #133 sent after #137, four picks late), 0 halts, 0 inserts, 0 undos; 2 page resumes in the paste, replayed as one session) replayed through the Version 68 page in headless Chromium: 0 echo misses, 0 clock mismatches, 0 page errors, 156 picks; the final board equals Yahoo's recap at 156 of 156 and the five "off the card" lines equal the paste's. The late fix: in the tool's final board #133 is Kevin Porter Jr. on Seat 12; Yahoo's recap has Kevin Porter Jr. at #133 for seat 12 (The_DON). The grading pipeline's Python port differs from the page record at 1 turns (#135: port 2, page 1); the page record is the authority for what the card said.

## 5. The Undo / Insert-at-# check of this morning, on this room

The owner's question of 2026-10-14 ("when using the undo pick and insert at # features ... the arithmetic computation and correct team association is accurate?") was answered from a separate harness (`report/after-reports/undo-insert-2026-10-14/`). This room used neither feature; its three numbered fixes are the nearest live case, and they behaved as the harness predicts: each landed on its own pick number and seat, the late one included, and the final board equals Yahoo's recap at 156 of 156.

## Watchlist

- #10 across the recent live rooms (page records): mock 73 Karl-Anthony Towns (card #1, 🎯 Karl-Anthony Towns); mock 74 Karl-Anthony Towns (card #1, 🎯 Karl-Anthony Towns); mock 75 Karl-Anthony Towns (card #1, 🎯 Karl-Anthony Towns); mock 77 Donovan Mitchell (card #4, 🎯 Jamal Murray); mock 78 Tyrese Haliburton (card #9, 🎯 Jamal Murray); mock 79 Tyrese Haliburton (card #9, 🎯 Jamal Murray); mock 80 Tyrese Haliburton (card #2, 🎯 Tyrese Maxey). On Version 68 Haliburton is card #2 at #10 (🎯 Tyrese Maxey); on Version 65 he was card #9.
- The publish freeze during the draft (D-1013-5) and no RESYNC during the draft (D-1013-2) stand.

## Open-item receipts

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| (this room) | records only; no web research and no roster pull | the room's names resolve to the Version 68 pool 156 of 156 |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | this morning's final pull (`after-report-2026-10-14.md`, receipts dated 10/14) | as recorded there (HELD, or unsigned); not re-queried for this grade (did not check) |

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

**Out of scope by design.**
- No line, price or engine change: Version 68 is the lock page and the publish freeze holds.
- No Yahoo standings comparison: no screenshot came with this paste.
- The punt test and the advice line were not re-run: no punt was declared and no advisor click is in the feed.
- This is a room of random humans, not the league's managers.

**In scope and unverified.**
- The raw text the owner typed for picks the tool resolved by surname ("assumed over" lines) is not in the paste; the pinned events feed the resolved names. The echoes and the final board match, so the state is the same; the typed strings are `UNVERIFIABLE`.
- Whether the season arms' title share holds against the league's real managers: `UNVERIFIABLE` until the draft.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| (none new) | this room raises no decision | — |
| D-1014-1..3, D-1014-8, D-1013-1..14 and earlier | carried as set in the 10/14 reports | carried |

## Provenance

- Inputs: the owner's paste (`draft80-2026-10-14/owner_message.txt`, verbatim); deck rev `cb1a922` (Version 68, page sha256 b83d1cdcc0e9, published 1791993066-d8ff).
- Tools: `build_state.py` (state, feed check and the replay events), the deck's `arena/mocks/live_retro.py` (mock 80 registered on tag v68: replay, final, hindsight, arms), `live_deckcard.py` (the page's engine), `live_replay_dom.mjs` (the tool log through the Version 68 and Version 67 pages), `scripts/repeat_market_check.py`, `write_report.py` (this file's writer). Records in `arena/results/m80_*.json` and this folder.
- No line, tag or placement changed on either plane.

## In plain language

**How the room went.** About a 24 percent title share, 1 of 12 by title odds and 1 of 12 week to week, favored against 11 of the other 11. You followed the card at 8 of 13 picks and stayed in its Top 5 at 13.

**The pick to learn from.** The best single change would have been #111: Myles Turner instead of Yaxel Lendeborg, worth about 3.6 title points.

**The tool.** Clean on the final page: three typos fixed by number (one four picks after the fact), one page reload, and the tool's board matched Yahoo's at every pick.

**Your decisions.** Nothing new.
