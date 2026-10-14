# After-report — draft_82: the 10/14 late live room from slot 10, on the lock page (Version 69)

**Owner request (2026-10-14, verbatim):** the deck tool's LIVE feed, the owner's 13-man roster and Yahoo's round-by-round recap, pasted during the integrity audit (`draft82-2026-10-14/owner_message.txt`), then "Publish fix now and grade Mock 82". Read as the standing request for these pastes: grade the room with the deck pipeline and report; no line, tag or price changes.

**Room:** public Yahoo mock, 12 × 13, owner seat 10 (random humans; a practice rep, not opponent intel; display names: 1 Raymund, 2 Nahuel, 3 456, 4 Jason, 5 Ralph, 6 will, 7 Ahmad, 8 T, 9 sailhan, 10 David, 11 Marcvelous3, 12 Runckler). **Deck used:** the lock page, published as Version 69 (rev `af91b23`, page sha256 e68a85a5305f; the six-way blend re-taken on Yahoo and Hashtag 10/14, Kawhi and Davis at 0.78). Replaying the owner's tool log through that page reproduces all three "off the card" lines of the paste character for character; through the Version 68 page the echoes differ (page: "⚠ off the card: Payton Pritchard ranks #5 (0.015 behind 🎯 John Collins)"; page: "⚠ off the card: Yaxel Lendeborg ranks #4 (0.014 behind 🎯 Neemias Queta) — round-9+ rule (D54-1): take the 🎯"; page: "⚠ off the card: Nic Claxton ranks #6 (0.036 behind 🎯 Neemias Queta) — round-9+ rule (D54-1): take the 🎯"), so the room was drafted on the lock page — the first live room on the locked lines.

Pull window: 2026-10-14 → 2026-10-14 (analysis only; no roster pull).

**Headline.** As drafted **27.58 percent** for the title on the real eight-team bracket, rank 1 of 12, playoffs 98.75 percent. Expected weekly category wins 5.124, rank 1 of 12, favored in 11 of 11 head-to-heads. Following the card's 🎯 from the same seat (the self-consistent chain) grades 28.05 percent. The owner took the 🎯 at 10 of 13 turns and stayed in the Top 5 at 12; the largest single swap is #106 Derik Queen (29.72 percent, +2.14 points). The tool log: 156 feeds, no fix, no resume; the board the tool held equals Yahoo's recap at 155 of 156 picks — at #124 the tool resolved an ambiguous entry to Draymond Green (assumed over Jalen Green, AJ Green) while Yahoo's recap has Jalen Green there (seat 4 either way). Neither Green appeared on the owner's card after #124. The miss had a cost the other way: with Draymond marked taken, the card could not offer him afterwards, and hindsight ranks him the best alternative at #154 (+0.057 weekly cats) — he went undrafted in the room. The same log through the LEAN-fix page (Version 70) gives the same 🎯 at all 13 of the owner's turns.

## 1. Roster changes

None. No line, tag, placement or price changed on either plane; this is a grade of a practice room.

## 2. The team, graded

EVIDENCE: `arena/results/m82_final.json`, `m82_arms.json` (18,000 seasons per arm, seeds 11/23/47, the real eight-team bracket), pool tag v69 = `players_v69.csv` (data/players.csv at `af91b23`, the lock's pool, sha256 d1d74587c5db). The grade runs on Yahoo's recap (the true board), not the tool's.

| arm | title % | playoffs % | rank |
|---|---|---|---|
| as drafted | 27.58 | 98.75 | 1 |
| follow the card's 🎯 at every turn (self-consistent chain: #87 John Collins, #106 Brandin Podziemski, #111 Neemias Queta) | 28.05 | 99.04 | 1 |
| single swap at #106: Derik Queen | 29.72 | 99.15 | 1 |
| single swap at #58: Matas Buzelis | 29.09 | 99.28 | 1 |
| single swap at #154: Draymond Green | 28.96 | 99.11 | 1 |
| single swap at #10: Jalen Johnson | 28.68 | 98.95 | 1 |
| single swap at #34: Walker Kessler | 28.31 | 99.00 | 1 |
| single swap at #130: PJ Washington | 28.14 | 99.02 | 1 |
| single swap at #135: PJ Washington | 28.14 | 98.84 | 1 |
| single swap at #87: Josh Hart | 28.11 | 98.90 | 1 |
| single swap at #111: Jakob Poeltl | 27.86 | 98.88 | 1 |
| single swap at #63: Ivica Zubac | 27.12 | 98.47 | 1 |
| single swap at #82: Josh Hart | 26.91 | 98.71 | 1 |

Category shape (weekly model, rank of 12): FG% 7, FT% 2, 3PTM 2, PTS 12, REB 8, AST 6, ST 3, BLK 6, TO 1.

For scale, the other live public rooms graded on this bracket: mock 67 17.51, mock 68 28.36, mock 73 34.17, mock 74 17.91, mock 75 29.39, mock 77 35.98, mock 78 19.48, mock 79 25.65, mock 80 23.84, mock 81 25.23.

## 3. Pick by pick: the page's card, the owner, hindsight

EVIDENCE: `m82_deckcard_v69.json` (the lock page's own engine), `m82_hindsight.json` (every single-swap alternative scored by weekly category wins against the final rosters).

| pick | owner took | card rank | the page's 🎯 | hindsight's best alternative (Δ weekly cat wins) |
|---|---|---|---|---|
| #10 | Tyrese Haliburton | 1 | Tyrese Haliburton | Jalen Johnson (+0.070) |
| #15 | Karl-Anthony Towns | 1 | Karl-Anthony Towns | Kevin Durant (-0.012) |
| #34 | Lauri Markkanen | 1 | Lauri Markkanen | Walker Kessler (+0.014) |
| #39 | Derrick White | 1 | Derrick White | Onyeka Okongwu (-0.027) |
| #58 | Dyson Daniels | 1 | Dyson Daniels | Matas Buzelis (+0.058) |
| #63 | Kel'el Ware | 1 | Kel'el Ware | Ivica Zubac (+0.004) |
| #82 | Ty Jerome | 1 | Ty Jerome | Josh Hart (+0.002) |
| #87 | Payton Pritchard | 5 | John Collins | Josh Hart (+0.030) |
| #106 | Yaxel Lendeborg | 3 | Neemias Queta | Derik Queen (+0.072) |
| #111 | Nic Claxton | 8 | Neemias Queta | Jakob Poeltl (+0.013) |
| #130 | Reed Sheppard | 1 | Reed Sheppard | PJ Washington (+0.059) |
| #135 | Cameron Johnson | 1 | Cameron Johnson | PJ Washington (+0.037) |
| #154 | Tobias Harris | 1 | Tobias Harris | Draymond Green (+0.057) |

The turns off the 🎯: #87 Payton Pritchard (card #5, 🎯 John Collins, taken #103 by seat 7), #106 Yaxel Lendeborg (card #3, 🎯 Neemias Queta, taken #112 by seat 9), #111 Nic Claxton (card #8, 🎯 Neemias Queta, taken #112 by seat 9).

## 4. Tool-state integrity

recap picks 156; seats 12 (David = 10); pool-less 0: []; feed vs recap: 155 of 156 agree on name and seat; differences [(124, ('Draymond Green', 4), 'Jalen Green', 4)]; feed picks still UNKNOWN at the end: []; owner picks: #10 Tyrese Haliburton, #15 Karl-Anthony Towns, #34 Lauri Markkanen, #39 Derrick White, #58 Dyson Daniels, #63 Kel'el Ware, #82 Ty Jerome, #87 Payton Pritchard, #106 Yaxel Lendeborg, #111 Nic Claxton, #130 Reed Sheppard, #135 Cameron Johnson, #154 Tobias Harris; events 156: feeds 156, numbered fixes 0. The owner's tool log as pinned in `arena/data/events/m82_tool_events.json` (156 events: 156 feeds, 0 UNKNOWN, 0 numbered fixes, 0 halts, 0 inserts, 0 undos; 0 page resumes) replayed through the lock page in headless Chromium: 0 echo misses, 0 clock mismatches, 0 page errors, 156 picks; the three "off the card" lines equal the paste's. **The one divergence from the true board:** at #124 the paste's line reads "Draymond Green → Seat 4 (assumed over Jalen Green, AJ Green)" — the resolver picked Draymond from an ambiguous entry — while Yahoo's recap has Jalen Green at #124 for seat 4 (Jason); Jalen Green was in fact gone and Draymond (taken by nobody; Yahoo's recap does not list him) stayed on the tool's available list. Neither Green reached the owner's card at #130, #135 or #154. The miss had a cost the other way: with Draymond marked taken, the card could not offer him afterwards, and hindsight ranks him the best alternative at #154 (+0.057 weekly cats) — he went undrafted in the room. The resolver's rule (a bare surname resolves to the best available namesake) did what it says; the typed text is not in the paste. The grading pipeline's Python port differs from the page record at 0 turns; the page record is the authority for what the card said.

## 5. The same room on the LEAN-fix page (Version 70)

EVIDENCE: `draft82-2026-10-14/replay_fixed.json` (the owner's tool log through the page carrying the roster-balance fix, in headless Chromium: 0 echo misses, 0 page errors, 156 picks).

The fix changes one warning line's count, not the engine; on this room the fixed page gives the same 🎯 at all 13 of the owner's turns, and prints 3 "off the card" lines to the paste's 3 — identical.

## Watchlist

- #10 across the recent live rooms (page records): mock 75 Karl-Anthony Towns (card #1, 🎯 Karl-Anthony Towns); mock 77 Donovan Mitchell (card #4, 🎯 Jamal Murray); mock 78 Tyrese Haliburton (card #9, 🎯 Jamal Murray); mock 79 Tyrese Haliburton (card #9, 🎯 Jamal Murray); mock 80 Tyrese Haliburton (card #2, 🎯 Tyrese Maxey); mock 81 Tyrese Haliburton (card #2, 🎯 Tyrese Maxey); mock 82 Tyrese Haliburton (card #1, 🎯 Tyrese Haliburton). On the lock page Haliburton is card #1 at #10 (🎯 Tyrese Haliburton).
- The ambiguous-surname resolution (#124): a bare surname with several namesakes resolves to the best available one by rule; in a live room, typing the first name too ("Jalen Green") removes the ambiguity. No rule change proposed tonight.
- The publish freeze during the draft (D-1013-5) and no RESYNC during the draft (D-1013-2) stand.

## Open-item receipts

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| (this room) | records only; no web research and no roster pull | the room's names resolve to the lock pool 156 of 156 |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this grade (did not check) |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 beb243ef57af), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 31 of 31 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-14.csv`, Hashtag `hashtag-2026-10-14.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-14.csv`, `hashtag-2026-10-14.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 30 of 31 | 44 | 111 | 63 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 22 of 31 | 32 | 67 | 58 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 13 of 31 | 107 | 138 | 182 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 12 of 31 | 101 | 182 | 100 | 125 | 148 | 155 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| John Collins | 12 of 31 | 73 | 117 | 105 | 72 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Brandin Podziemski | 11 of 31 | 93 | 146 | 74 | 102 | 114 | 132 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 10 of 31 | 92 | 179 | 89 | 117 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 8 of 31 | 6 | 32 | 15 | 24 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Jaden McDaniels | 6 of 31 | 62 | 90 | 42 | 67 | 86 | 59 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 5 of 31 | 114 | 139 | 122 | 130 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Immanuel Quickley | 5 of 31 | 67 | 94 | 65 | 73 | 79 | 84 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Keegan Murray | 5 of 31 | 83 | 142 | 82 | 94 | 102 | 85 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (18 mocks, value 9, market 18); Derrick White (16 mocks, value 27, market 45); Lauri Markkanen (15 mocks, value 21, market 37); Tyrese Haliburton (13 mocks, value 7, market 12); Kel'el Ware (9 mocks, value 57, market 77); Tyler Herro (9 mocks, value 51, market 69); Tyrese Maxey (9 mocks, value 5, market 9); Karl-Anthony Towns (7 mocks, value 12, market 15).


## Bounds

**Out of scope by design.**
- No line, price or engine change.
- No Yahoo standings comparison: no screenshot came with this paste.
- The punt test and the advice line were not re-run: no punt was declared and no advisor click is in the feed.
- This is a room of random humans, not the league's managers.

**In scope and unverified.**
- The raw text the owner typed for picks the tool resolved by surname ("assumed over" lines, #124 among them) is not in the paste; the pinned events feed the resolved names: `UNVERIFIABLE`.
- Whether the season arms' title share holds against the league's real managers: `UNVERIFIABLE` until the draft.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D82-1 | the bare-surname resolver after a live miss (#124, Green): (a) keep the rule, type first names in the real draft; (b) halt on any surname with 2+ available namesakes (the pre-9/29 behaviour, which buried the owner mid-draft at "George") | (a) |
| D-INT-1, D-INT-2, D-1014-*, D-1013-*, earlier | carried | carried |

## Provenance

- Inputs: the owner's paste (`draft82-2026-10-14/owner_message.txt`, verbatim); the lock page (deck rev `af91b23`, sha256 e68a85a5305f, published as Version 69, id 1792001219-01f3); the Version 68 page (rev `cb1a922`); the LEAN-fix page (Version 70).
- Tools: `build_state.py`, the deck's `arena/mocks/live_retro.py` (mock 82 registered on tag v69: replay, final, hindsight, arms), `live_deckcard.py`, `live_replay_dom.mjs` (three pages), `scripts/repeat_market_check.py` (31 of 31 mocks, 12 flagged), `write_report.py`. Records in `arena/results/m82_*.json` and this folder.
- No line, tag or placement changed on either plane.

## In plain language

**How the room went.** About a 28 percent title share, 1 of 12 by title odds and 1 of 12 week to week, favored against 11 of the other 11. You followed the card at 10 of 13 picks and stayed in its Top 5 at 12. This was the first live room on the locked lines.

**The pick to learn from.** The best single change would have been #106: Derik Queen instead of Yaxel Lendeborg, worth about 2.1 title points. Following the 🎯 at every turn would have graded 28.1 percent, +0.5 points against as drafted.

**The tool.** One thing to know for tonight: at #124 you logged a "Green" and the tool chose Draymond, but the room had taken Jalen Green. It did not put a wrong name on your card, but it hid one: Draymond Green stayed marked as taken, so the card could not offer him, and hindsight likes him at #154. In the real draft, type the first name when a surname is shared. The roster-balance line fix (Version 70) changes nothing on this room's card.

**Your decisions.** D82-1, the surname rule; the default keeps it and relies on first names.
