# After-report — draft_79: the 10/14 early live room from slot 10, on deck Version 65

**Owner request (2026-10-14, verbatim):** the deck tool's LIVE feed, the owner's 13-man roster and Yahoo's round-by-round recap, pasted without comment while mock 78 was being graded (`draft79-2026-10-14/owner_message.txt`). Read as the standing request for these pastes: grade the room with the deck pipeline and report; no line, tag or price changes.

**Room:** public Yahoo mock, 12 × 13, owner seat 10 (random humans; a practice rep, not opponent intel; display names: 1 The Boss, 2 Stephen, 3 Ritznore, 4 kenneth, 5 Menelaos, 6 Dr. Endo, 7 Gabriel, 8 aiden, 9 JB, 10 David, 11 allan, 12 어진). **Deck used:** Version 65 (rev `dd6b719`, the dial pass; Porziņģis veto live). Replaying the owner's tool log through the v65 page reproduces all seven "off the card" lines of the paste character for character.

Pull window: 2026-10-14 → 2026-10-14 (analysis only; no roster pull; the planes are held for this morning's final pull by the owner's decision).

**Headline.** As drafted **25.65 percent** for the title on the real eight-team bracket, rank 1 of 12, playoffs 99.36 percent. Expected weekly category wins 5.245, rank 1 of 12, favored in 11 of 11 head-to-heads. Following the card's 🎯 from the same seat (the self-consistent chain) grades 46.18 percent. The owner took the 🎯 at 6 of 13 turns and stayed in the Top 5 at 10; the largest single swap is #10 Jamal Murray (33.04 percent, +7.39 points). The tool log is clean: the board the tool held equals Yahoo's recap at 156 of 156 picks.

## 1. Roster changes

None. No line, tag, placement or price changed on either plane; this is a grade of a practice room.

## 2. The team, graded

EVIDENCE: `arena/results/m79_final.json`, `m79_arms.json` (18,000 seasons per arm, seeds 11/23/47, the real eight-team bracket), pool tag v65 = `players_v65.csv` (data/players.csv at `dd6b719`, sha256 bd2b983876a8).

| arm | title % | playoffs % | rank |
|---|---|---|---|
| as drafted | 25.65 | 99.36 | 1 |
| follow the card's 🎯 at every turn (self-consistent chain: #10 Jamal Murray, #39 Dyson Daniels, #58 Kel'el Ware, #63 Michael Porter Jr., #82 Ty Jerome, #111 Reed Sheppard, #130 Miles Bridges) | 46.18 | 100.00 | 1 |
| single swap at #10: Jamal Murray | 33.04 | 99.87 | 1 |
| single swap at #63: Kel'el Ware | 32.96 | 99.91 | 1 |
| single swap at #15: Jamal Murray | 28.84 | 99.68 | 1 |
| single swap at #58: Kel'el Ware | 27.04 | 99.69 | 1 |
| single swap at #82: Ty Jerome | 26.98 | 99.56 | 1 |
| single swap at #135: Reed Sheppard | 26.76 | 99.51 | 1 |
| single swap at #34: Domantas Sabonis | 26.28 | 99.23 | 1 |
| single swap at #39: Kel'el Ware | 26.11 | 99.49 | 1 |
| single swap at #130: PJ Washington | 26.06 | 99.52 | 1 |
| single swap at #106: Josh Hart | 26.00 | 99.34 | 1 |

Category shape (weekly model, rank of 12): FG% 9, FT% 1, 3PTM 4, PTS 9, REB 8, AST 7, ST 8, BLK 4, TO 1.

For scale, the other live public rooms graded on this bracket: mock 67 17.51, mock 68 28.36, mock 73 34.17, mock 74 17.91, mock 75 29.39, mock 77 35.98, mock 78 19.48.

## 3. Pick by pick: the page's card, the owner, hindsight

EVIDENCE: `m79_deckcard_v65.json` (the v65 page's own engine), `m79_hindsight.json` (every single-swap alternative scored by weekly category wins against the final rosters).

| pick | owner took | card rank | the page's 🎯 | hindsight's best alternative (Δ weekly cat wins) |
|---|---|---|---|---|
| #10 | Tyrese Haliburton | 9 | Jamal Murray | Jamal Murray (+0.219) |
| #15 | Kevin Durant | 1 | Kevin Durant | Jamal Murray (+0.098) |
| #34 | Chet Holmgren | 1 | Chet Holmgren | Domantas Sabonis (+0.002) |
| #39 | Derrick White | 1 | Derrick White | Kel'el Ware (+0.036) |
| #58 | Franz Wagner | 2 | Michael Porter Jr. | Kel'el Ware (+0.058) |
| #63 | Zach Edey | 44 | Kel'el Ware | Kel'el Ware (+0.236) |
| #82 | Payton Pritchard | 6 | Ty Jerome | Ty Jerome (+0.033) |
| #87 | Immanuel Quickley | 1 | Immanuel Quickley | Jabari Smith Jr. (-0.006) |
| #106 | Yaxel Lendeborg | 3 | Reed Sheppard | Josh Hart (+0.003) |
| #111 | Miles Bridges | 5 | Collin Gillespie | Collin Gillespie (-0.013) |
| #130 | Tre Jones | 5 | Reed Sheppard | PJ Washington (+0.045) |
| #135 | Saddiq Bey | 1 | Saddiq Bey | Reed Sheppard (+0.005) |
| #154 | Tari Eason | 1 | Tari Eason | Draymond Green (-0.019) |

The turns outside the Top 5: #10 Tyrese Haliburton (card #9, 🎯 Jamal Murray, taken #20 by seat 5), #63 Zach Edey (card #44, 🎯 Kel'el Ware, taken #66 by seat 7), #82 Payton Pritchard (card #6, 🎯 Ty Jerome, taken #85 by seat 12).

**The six players from the owner's question, in this room** (see `after-report-2026-10-13-draft78.md` §6): Jalen Williams went #44 to seat 5; Payton Pritchard went #82 to seat 10; OG Anunoby went #64 to seat 9; Chet Holmgren went #34 to seat 10; Anthony Davis went #28 to seat 4; Karl-Anthony Towns went #17 to seat 8. On the owner's card: #15 Chet Holmgren card #3; #34 Chet Holmgren card #1 (the 🎯); #63 OG Anunoby card #5. Holmgren at #34 was the card's 🎯 and the owner took him; Pritchard at #82 was the owner's pick at card #6, behind the 🎯 Ty Jerome.

## 4. Tool-state integrity

recap picks 156; seats 12 (David = 10); pool-less 0: []; feed vs recap: 156 of 156 agree on name and seat; differences []; feed picks still UNKNOWN at the end: []; owner picks: #10 Tyrese Haliburton, #15 Kevin Durant, #34 Chet Holmgren, #39 Derrick White, #58 Franz Wagner, #63 Zach Edey, #82 Payton Pritchard, #87 Immanuel Quickley, #106 Yaxel Lendeborg, #111 Miles Bridges, #130 Tre Jones, #135 Saddiq Bey, #154 Tari Eason. The owner's tool log as pinned in `arena/data/events/m79_tool_events.json` (161 events: 159 feeds, 2 of them raw texts that resolved to UNKNOWN ("Chetr" at #34, "Jrie" at #147), 2 numbered fixes, 1 halt ("Mitchell" after #132, Donovan Mitchell already drafted), 1 insert (Cason Wallace at #115, sent after #123), 1 undo (Daniel Gafford at #133, re-fed after Ajay Mitchell); 2 page resumes in the paste, replayed as one session) replayed through the v65 page in headless Chromium: 0 echo misses, 0 clock mismatches, 0 page errors, 156 picks; the final board equals Yahoo's recap at 156 of 156 and the seven "off the card" lines equal the paste's. The page's card on the recap board gives the same rank and 🎯 for all seven. The grading pipeline's Python port differs from the page record at 4 turns (#58: port 3, page 2, #87: port 2, page 1, #111: port 6, page 5, #130: port 4, page 5); the page record is the authority for what the card said.

## Watchlist

- #10 across the recent live rooms (page records): mock 72 Karl-Anthony Towns (card #1, 🎯 Karl-Anthony Towns); mock 73 Karl-Anthony Towns (card #1, 🎯 Karl-Anthony Towns); mock 74 Karl-Anthony Towns (card #1, 🎯 Karl-Anthony Towns); mock 75 Karl-Anthony Towns (card #1, 🎯 Karl-Anthony Towns); mock 77 Donovan Mitchell (card #4, 🎯 Jamal Murray); mock 78 Tyrese Haliburton (card #9, 🎯 Jamal Murray); mock 79 Tyrese Haliburton (card #9, 🎯 Jamal Murray). Haliburton at card #9 in the last two rooms; the 🎯 there is Jamal Murray on v65, where it was Towns before the 10/12 rebuild.
- The 10/14 lock paste (D-1013-1), the publish freeze during the draft (D-1013-5), no RESYNC during the draft (D-1013-2).

## Open-item receipts

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| (this room) | records only; no web research and no roster pull | the room's names resolve to the v65 pool 156 of 156; the lines are the ones merged in kit PR #109 |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the 10/13 pull (`after-report-2026-10-13.md`, receipts dated 10/13) | all HELD or unsigned on 2026-10-13 per those receipts; not re-queried here (did not check); this morning's final pull re-queries them |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 09a889d4baa5), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 28 of 28 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-13.csv`, Hashtag `hashtag-2026-10-12.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-13.csv`, `hashtag-2026-10-12.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Kel'el Ware | 24 of 28 | 26 | 77 | 51 | 51 | 63 | 61 | ft_pct .732 vs .714-.723 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Reed Sheppard | 23 of 28 | 63 | 180 | 56 | 118 | 126 | 129 | tpm 2.8 vs 2.2-2.6 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Ty Jerome | 23 of 28 | 39 | 117 | 48 | 60 | 101 | 65 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Yaxel Lendeborg | 11 of 28 | 70 | 143 | 93 | 121 | 137 | 91 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 9 of 28 | 79 | 183 | 100 | 126 | 148 | 155 | pts 12.7 vs 9.5-11.9; reb 4.1 vs 3.3-3.9; tpm 2.9 vs 2.1-2.7; tov 1.6 vs 1.1-1.4 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Saddiq Bey | 9 of 28 | 90 | 177 | 108 | 132 | 169 | 157 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Michael Porter Jr. | 7 of 28 | 32 | 60 | 55 | 62 | 70 | 57 | pts 24.5 vs 18.7-21.8; ast 3 vs 2.4-2.6; stl 0.7 vs 0.8-1; tpm 3.4 vs 2.9-3.1; tov 2.3 vs 1.9-2 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Dyson Daniels | 6 of 28 | 22 | 62 | 20 | 64 | 56 | 55 | reb 6.8 vs 5.8-6.4; ast 5.9 vs 4.7-5.5; tpm 0.3 vs 0.5-0.6 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 5 of 28 | 7 | 32 | 15 | 16 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Tari Eason | 5 of 28 | 98 | 151 | 132 | 147 | 147 | 139 | tpm 1.6 vs 1.3-1.4; fg_pct .427 vs .441-.450 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (24 mocks, value 6, market 18); Lauri Markkanen (15 mocks, value 21, market 37); VJ Edgecombe (13 mocks, value 58, market 75); Derrick White (12 mocks, value 29, market 45); Tyrese Maxey (7 mocks, value 5, market 9).


## Bounds

**Out of scope by design.**
- No line, price or engine change: the owner holds every decision until this morning's final pull.
- No Yahoo standings comparison: no screenshot came with this paste.
- The punt test and the advice line were not re-run: no punt was declared and no advisor click is in the feed.
- This is a room of random humans, not the league's managers.

**In scope and unverified.**
- The raw text the owner typed for picks the tool resolved by surname ("assumed over" lines) is not in the paste; the pinned events feed the resolved names. The echoes and the final board match, so the state is the same; the typed strings are `UNVERIFIABLE`.
- Whether the season arms' title share holds against the league's real managers: `UNVERIFIABLE` until the draft.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-1013-10..14 | carried as set; the owner's hold until this morning's final pull | hold |
| D-1013-1..9, D-C2, D-SF-1..4 and earlier | carried | carried |

## Provenance

- Inputs: the owner's paste (`draft79-2026-10-14/owner_message.txt`, verbatim); deck rev `dd6b719` (Version 65, page sha256 09a889d4baa5).
- Tools: `build_state.py` (state and feed check), the deck's `arena/mocks/live_retro.py` (mock 79 registered: replay, final, hindsight, arms), `live_deckcard.py` (the page's engine), `live_replay_dom.mjs` (the tool log through the real page), `scripts/repeat_market_check.py` (28 mocks), `write_report.py` (this file's writer). Records in `arena/results/m79_*.json` and this folder.
- No line, tag or placement changed; both planes' hashes equal before and after (e821ec1ddc67 kit, bd2b983876a8 deck).

## In plain language

**How the room went.** About a 26 percent title share, 1 of 12 by title odds and 1 of 12 week to week, favored against 11 of the other 11. You followed the card at 6 of 13 picks and stayed in its Top 5 at 10.

**The pick to learn from.** The best single change would have been #10: Jamal Murray instead of Tyrese Haliburton, worth about 7 title points.

**The tool.** Clean: two typos fixed, one halt handled, one insert and one undo, and the tool's board matched Yahoo's at every pick.

**Your decisions.** Nothing new; everything holds until this morning's final pull.
