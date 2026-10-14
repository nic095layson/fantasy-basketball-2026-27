# After-report — draft_81: the 10/14 evening live room from slot 10, on deck Version 68

**Owner request (2026-10-14, verbatim):** the deck tool's LIVE feed, the owner's 13-man roster and Yahoo's round-by-round recap, pasted three times during the lock work (`draft81-2026-10-14/owner_message.txt`), with "I was trying to run Mock draft as 'Queue Later'" and then "Grade mock 81 now". Read as the standing request for these pastes: grade the room with the deck pipeline and report; no line, tag or price changes (the lock is published as Version 69).

**Room:** public Yahoo mock, 12 × 13, owner seat 10 (random humans; a practice rep, not opponent intel; display names: 1 Deniz, 2 george, 3 Smitty, 4 Dave, 5 Jermaine, 6 Bishal, 7 bugs, 8 Pavlos, 9 Chris, 10 David, 11 Peter, 12 Mert). **Deck used:** Version 68 (rev `cb1a922`, the final morning pull and the owner's three lock calls; the lock page was not yet published when this room ran). Replaying the owner's tool log through the Version 68 page reproduces all four "off the card" lines of the paste character for character; through Version 67 one differs (page: "⚠ off the card: Sandro Mamukelashvili ranks #6 (0.032 behind 🎯 Reed Sheppard) — round-9+ rule (D54-1): take the 🎯"), so the room was drafted on Version 68.

Pull window: 2026-10-14 → 2026-10-14 (analysis only; no roster pull; Version 69, the lock, is the published page).

**Headline.** As drafted **25.23 percent** for the title on the real eight-team bracket, rank 1 of 12, playoffs 98.67 percent. Expected weekly category wins 5.125, rank 1 of 12, favored in 11 of 11 head-to-heads. Following the card's 🎯 from the same seat (the self-consistent chain) grades 28.54 percent. The owner took the 🎯 at 9 of 13 turns and stayed in the Top 5 at 13; the largest single swap is #135 Draymond Green (27.15 percent, +1.92 points). The tool log is clean: the board the tool held equals Yahoo's recap at 156 of 156 picks, after one typed name was fixed by number. The same log replayed through the lock page (Version 69) changes the 🎯 at 2 of the owner's 13 turns (#82: Version 68 VJ Edgecombe, lock Mikal Bridges; #154: Version 68 Devin Vassell, lock Christian Braun).

## 1. Roster changes

None. No line, tag, placement or price changed on either plane; this is a grade of a practice room.

## 2. The team, graded

EVIDENCE: `arena/results/m81_final.json`, `m81_arms.json` (18,000 seasons per arm, seeds 11/23/47, the real eight-team bracket), pool tag v68 = `players_v68.csv` (data/players.csv at `cb1a922`, sha256 30246ac015fe). The grade is on the Version 68 pool, the page the room was drafted on; the lock's 54 re-blended lines are not in it (see §5).

| arm | title % | playoffs % | rank |
|---|---|---|---|
| as drafted | 25.23 | 98.67 | 1 |
| follow the card's 🎯 at every turn (self-consistent chain: #10 Tyrese Maxey, #63 Kel'el Ware, #87 Immanuel Quickley, #111 Jakob Poeltl, #130 Reed Sheppard) | 28.54 | 99.46 | 1 |
| single swap at #135: Draymond Green | 27.15 | 98.97 | 1 |
| single swap at #87: Isaiah Hartenstein | 26.77 | 99.00 | 1 |
| single swap at #111: Nic Claxton | 26.73 | 98.94 | 1 |
| single swap at #130: PJ Washington | 26.61 | 98.90 | 1 |
| single swap at #58: Dyson Daniels | 26.54 | 98.68 | 1 |
| single swap at #15: Donovan Mitchell | 26.43 | 98.94 | 1 |
| single swap at #106: Isaiah Hartenstein | 26.31 | 98.68 | 1 |
| single swap at #10: Tyrese Maxey | 26.21 | 98.79 | 1 |
| single swap at #34: James Harden | 25.68 | 98.66 | 1 |
| single swap at #63: Michael Porter Jr. | 25.16 | 98.72 | 1 |

Category shape (weekly model, rank of 12): FG% 7, FT% 1, 3PTM 1, PTS 9, REB 8, AST 10, ST 6, BLK 8, TO 1.

For scale, the other live public rooms graded on this bracket: mock 67 17.51, mock 68 28.36, mock 73 34.17, mock 74 17.91, mock 75 29.39, mock 77 35.98, mock 78 19.48, mock 79 25.65, mock 80 23.84.

## 3. Pick by pick: the page's card, the owner, hindsight

EVIDENCE: `m81_deckcard_v68.json` (the Version 68 page's own engine), `m81_hindsight.json` (every single-swap alternative scored by weekly category wins against the final rosters).

| pick | owner took | card rank | the page's 🎯 | hindsight's best alternative (Δ weekly cat wins) |
|---|---|---|---|---|
| #10 | Tyrese Haliburton | 2 | Tyrese Maxey | Tyrese Maxey (+0.025) |
| #15 | Karl-Anthony Towns | 1 | Karl-Anthony Towns | Donovan Mitchell (+0.003) |
| #34 | Kawhi Leonard | 1 | Kawhi Leonard | James Harden (+0.003) |
| #39 | Derrick White | 1 | Derrick White | Walker Kessler (-0.012) |
| #58 | OG Anunoby | 1 | OG Anunoby | Dyson Daniels (+0.011) |
| #63 | Tyler Herro | 1 | Tyler Herro | Michael Porter Jr. (+0.007) |
| #82 | VJ Edgecombe | 1 | VJ Edgecombe | Josh Hart (-0.013) |
| #87 | Neemias Queta | 4 | Andrew Wiggins | Isaiah Hartenstein (+0.052) |
| #106 | Miles Bridges | 1 | Miles Bridges | Isaiah Hartenstein (+0.010) |
| #111 | Yaxel Lendeborg | 2 | Jakob Poeltl | Nic Claxton (+0.056) |
| #130 | Sandro Mamukelashvili | 5 | Reed Sheppard | PJ Washington (+0.045) |
| #135 | Cameron Johnson | 1 | Cameron Johnson | Draymond Green (+0.056) |
| #154 | Devin Vassell | 1 | Devin Vassell | Tari Eason (-0.008) |

The turns off the 🎯: #10 Tyrese Haliburton (card #2, 🎯 Tyrese Maxey, taken #11 by seat 11), #87 Neemias Queta (card #4, 🎯 Andrew Wiggins, taken #98 by seat 2), #111 Yaxel Lendeborg (card #2, 🎯 Jakob Poeltl, taken #118 by seat 3), #130 Sandro Mamukelashvili (card #5, 🎯 Reed Sheppard, taken #139 by seat 6).

## 4. Tool-state integrity

recap picks 156; seats 12 (David = 10); pool-less 0: []; feed vs recap: 156 of 156 agree on name and seat; differences []; feed picks still UNKNOWN at the end: []; owner picks: #10 Tyrese Haliburton, #15 Karl-Anthony Towns, #34 Kawhi Leonard, #39 Derrick White, #58 OG Anunoby, #63 Tyler Herro, #82 VJ Edgecombe, #87 Neemias Queta, #106 Miles Bridges, #111 Yaxel Lendeborg, #130 Sandro Mamukelashvili, #135 Cameron Johnson, #154 Devin Vassell. The owner's tool log as pinned in `arena/data/events/m81_tool_events.json` (157 events: 157 feeds, 1 of them a raw text that resolved to UNKNOWN ("Giannas" at #5), 1 numbered fix (#5 Giannis Antetokounmpo), 0 halts, 0 inserts, 0 undos; 1 page resume in the paste, after 15 picks, replayed as one session) replayed through the Version 68 page in headless Chromium: 0 echo misses, 0 clock mismatches, 0 page errors, 156 picks; the final board equals Yahoo's recap at 156 of 156 and the four "off the card" lines equal the paste's. The grading pipeline's Python port differs from the page record at 1 turns (#135: port 2, page 1); the page record is the authority for what the card said.

## 5. The same room on the lock page (Version 69)

EVIDENCE: `draft81-2026-10-14/replay_lock.json` (the owner's tool log through the published lock page, sha256 e68a85a5305f, in headless Chromium: 0 echo misses, 0 page errors, 156 picks).

The lock re-blended 54 lines after this room was drafted. On the lock page the same 156 picks give a different 🎯 at 2 of the owner's 13 turns: #82 Version 68 🎯 VJ Edgecombe, lock 🎯 Mikal Bridges; #154 Version 68 🎯 Devin Vassell, lock 🎯 Christian Braun. The lock page prints 6 "off the card" lines to the paste's 4: the 4 not in the paste are "⚠ off the card: VJ Edgecombe ranks #2 (0.000 behind 🎯 Mikal Bridges)"; "⚠ off the card: Neemias Queta ranks #6 (0.030 behind 🎯 Andrew Wiggins)"; "⚠ off the card: Sandro Mamukelashvili ranks #6 (0.027 behind 🎯 Reed Sheppard) — round-9+ rule (D54-1): take the 🎯"; "⚠ off the card: Devin Vassell ranks #2 (0.004 behind 🎯 Christian Braun) — round-9+ rule (D54-1): take the 🎯". Nothing here changes the lock; it records where the practice room's page and the draft page differ at the owner's seat, on the owner's own picks.

## Watchlist

- #10 across the recent live rooms (page records): mock 73 Karl-Anthony Towns (card #1, 🎯 Karl-Anthony Towns); mock 74 Karl-Anthony Towns (card #1, 🎯 Karl-Anthony Towns); mock 75 Karl-Anthony Towns (card #1, 🎯 Karl-Anthony Towns); mock 77 Donovan Mitchell (card #4, 🎯 Jamal Murray); mock 78 Tyrese Haliburton (card #9, 🎯 Jamal Murray); mock 79 Tyrese Haliburton (card #9, 🎯 Jamal Murray); mock 80 Tyrese Haliburton (card #2, 🎯 Tyrese Maxey); mock 81 Tyrese Haliburton (card #2, 🎯 Tyrese Maxey). Haliburton at #10 is the owner's stated plan (`after-report-2026-10-14-haliburton-plan.md`); on Version 68 he is card #2 there, 0.005 behind the 🎯.
- The publish freeze during the draft (D-1013-5) and no RESYNC during the draft (D-1013-2) stand.

## Open-item receipts

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| (this room) | records only; no web research and no roster pull | the room's names resolve to the Version 68 pool 156 of 156 |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there (held; Thomas, Ivey, Sochan, Dillingham absent from Yahoo's 350); not re-queried for this grade (did not check) |

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
- No line, price or engine change: the lock is published and the publish freeze holds.
- No Yahoo standings comparison: no screenshot came with this paste.
- The punt test and the advice line were not re-run: no punt was declared and no advisor click is in the feed.
- The grade runs on the Version 68 pool the room was drafted on, not the lock's lines; §5 shows only what the lock page's card would have said, not a re-grade.
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

- Inputs: the owner's paste (`draft81-2026-10-14/owner_message.txt`, verbatim); deck rev `cb1a922` (Version 68, page sha256 b83d1cdcc0e9, published 1791993066-d8ff); the lock page at deck `origin/main` after PR #118 (sha256 e68a85a5305f, published as Version 69, id 1792001219-01f3).
- Tools: `build_state.py` (state, feed check and the replay events), the deck's `arena/mocks/live_retro.py` (mock 81 registered on tag v68: replay, final, hindsight, arms), `live_deckcard.py` (the page's engine), `live_replay_dom.mjs` (the tool log through the Version 68, Version 67 and lock pages), `scripts/repeat_market_check.py` (30 of 30 mocks, 12 flagged), `write_report.py` (this file's writer). Records in `arena/results/m81_*.json` and this folder.
- No line, tag or placement changed on either plane.

## In plain language

**How the room went.** About a 25 percent title share, 1 of 12 by title odds and 1 of 12 week to week, favored against 11 of the other 11. You followed the card at 9 of 13 picks and stayed in its Top 5 at 13.

**The pick to learn from.** The best single change would have been #135: Draymond Green instead of Cameron Johnson, worth about 1.9 title points. Following the 🎯 at every turn would have graded 28.5 percent, 3.3 points more than as drafted.

**The tool.** Clean: one typo fixed by number, one page reload, and the tool's board matched Yahoo's at every pick. The room ran on Version 68; on the lock page the card would have pointed elsewhere at 2 of your 13 turns (#82 Mikal Bridges, #154 Christian Braun).

**Your decisions.** Nothing new.
