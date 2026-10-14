# After-report — draft_83: the 10/14 evening live room from slot 10, on the locked lines

**Owner request (2026-10-14, verbatim):** the deck tool's LIVE feed, the owner's 13-man roster and Yahoo's round-by-round recap, pasted with no other text (`draft83-2026-10-14/owner_message.txt`). Read as the standing request for these pastes: grade the room with the deck pipeline and report; no line, tag or price changes.

**Room:** public Yahoo mock, 12 × 13, owner seat 10 (random humans; a practice rep, not opponent intel; display names: 1 Itsel, 2 Sammy, 3 Girthquake, 4 De Ma Sh, 5 Zoran, 6 Anwar, 7 Yanique, 8 Jericho, 9 Marsel, 10 David, 11 Joshua, 12 Aaron). **Deck used:** the locked lines (pool tag v69 = data/players.csv at `af91b23`). The page was Version 69 or Version 70 — the log cannot tell which: Version 70 changed only the ⚠ LEAN warning line's count, which this paste does not carry, and the one "off the card" line of the paste is reproduced character for character by the current page.

Pull window: 2026-10-14 → 2026-10-14 (analysis only; no roster pull).

**Headline.** As drafted **29.69 percent** for the title on the real eight-team bracket, rank 1 of 12, playoffs 99.50 percent. Expected weekly category wins 5.316, rank 1 of 12, favored in 11 of 11 head-to-heads. Following the card's 🎯 from the same seat (the self-consistent chain) grades 30.57 percent. The owner took the 🎯 at 11 of 13 turns and stayed in the Top 5 at 13; the largest single swap is #34 Chet Holmgren (31.97 percent, +2.27 points). The tool log carried two Insert-at-# corrections (#6 Jayson Tatum, #92 Brandon Ingram), a double undo at the last round, and one refused repeat entry; the board the tool ended on equals Yahoo's recap at 156 of 156 picks. One display defect found: after the #6 insert moved Haliburton onto the owner's seat, the log line said "Haliburton is the 🎯" while the card at #10 had Tyrese Maxey as 🎯 and Haliburton #2 (D83-1).

## 1. Roster changes

None. No line, tag, placement or price changed on either plane; this is a grade of a practice room.

## 2. The team, graded

EVIDENCE: `arena/results/m83_final.json`, `m83_arms.json` (18,000 seasons per arm, seeds 11/23/47, the real eight-team bracket), pool tag v69 = `players_v69.csv` (data/players.csv at `af91b23`, the lock's pool). The grade runs on Yahoo's recap (the true board), not the tool's.

| arm | title % | playoffs % | rank |
|---|---|---|---|
| as drafted | 29.69 | 99.50 | 1 |
| follow the card's 🎯 at every turn (self-consistent chain: #10 Tyrese Maxey, #87 Immanuel Quickley) | 30.57 | 99.59 | 1 |
| single swap at #34: Chet Holmgren | 31.97 | 99.61 | 1 |
| single swap at #111: Myles Turner | 31.32 | 99.64 | 1 |
| single swap at #135: PJ Washington | 30.98 | 99.58 | 1 |
| single swap at #87: VJ Edgecombe | 30.76 | 99.59 | 1 |
| single swap at #82: VJ Edgecombe | 30.23 | 99.41 | 1 |
| single swap at #154: Bobby Portis | 30.18 | 99.52 | 1 |
| single swap at #130: PJ Washington | 30.07 | 99.52 | 1 |
| single swap at #58: Michael Porter Jr. | 29.94 | 99.53 | 1 |

Category shape (weekly model, rank of 12): FG% 8, FT% 1, 3PTM 3, PTS 10, REB 5, AST 7, ST 2, BLK 7, TO 2.

For scale, the other live public rooms graded on this bracket: mock 67 17.51, mock 68 28.36, mock 73 34.17, mock 74 17.91, mock 75 29.39, mock 77 35.98, mock 78 19.48, mock 79 25.65, mock 80 23.84, mock 81 25.23, mock 82 27.58.

## 3. Pick by pick: the page's card, the owner, hindsight

EVIDENCE: `m83_deckcard_v69.json` (the page's own engine on the true board before each owner turn), `m83_hindsight.json` (every single-swap alternative scored by weekly category wins against the final rosters).

| pick | owner took | card rank | the page's 🎯 | hindsight's best alternative (Δ weekly cat wins) |
|---|---|---|---|---|
| #10 | Tyrese Haliburton | 2 | Tyrese Maxey | Tyrese Maxey (-0.006) |
| #15 | Karl-Anthony Towns | 1 | Karl-Anthony Towns | Domantas Sabonis (-0.029) |
| #34 | Kawhi Leonard | 1 | Kawhi Leonard | Chet Holmgren (+0.061) |
| #39 | James Harden | 1 | James Harden | Onyeka Okongwu (-0.062) |
| #58 | OG Anunoby | 1 | OG Anunoby | Michael Porter Jr. (+0.027) |
| #63 | Kel'el Ware | 1 | Kel'el Ware | Rudy Gobert (-0.029) |
| #82 | Ty Jerome | 1 | Ty Jerome | VJ Edgecombe (+0.008) |
| #87 | Andrew Wiggins | 4 | VJ Edgecombe | VJ Edgecombe (+0.040) |
| #106 | Isaiah Hartenstein | 1 | Isaiah Hartenstein | Jakob Poeltl (-0.051) |
| #111 | Miles Bridges | 1 | Miles Bridges | Myles Turner (+0.033) |
| #130 | Yaxel Lendeborg | 1 | Yaxel Lendeborg | PJ Washington (+0.025) |
| #135 | Cameron Johnson | 1 | Cameron Johnson | PJ Washington (+0.046) |
| #154 | Devin Vassell | 1 | Devin Vassell | Bobby Portis (+0.027) |

The turns off the 🎯: #10 Tyrese Haliburton (card #2, 0.005 behind 🎯 Tyrese Maxey, taken #11 by seat 11), #87 Andrew Wiggins (card #4, 0.013 behind 🎯 VJ Edgecombe, taken #93 by seat 4).

## 4. Tool-state integrity

recap picks 156; seats 12 (David = 10); pool-less 0: []; feed vs recap: 156 of 156 agree on name and seat; differences []; feed picks still UNKNOWN at the end: []; owner picks: #10 Tyrese Haliburton, #15 Karl-Anthony Towns, #34 Kawhi Leonard, #39 James Harden, #58 OG Anunoby, #63 Kel'el Ware, #82 Ty Jerome, #87 Andrew Wiggins, #106 Isaiah Hartenstein, #111 Miles Bridges, #130 Yaxel Lendeborg, #135 Cameron Johnson, #154 Devin Vassell.

EVIDENCE: the owner's tool log as pinned in `arena/data/events/m83_tool_events.json` (161 events: 157 feeds, of them 1 refused repeat; 2 inserts; 2 undos; the closing "resumed: 156 picks logged" line carries no event) replayed through the current page in headless Chromium (`draft83-2026-10-14/replay_v70.json`): 0 echo misses, 0 clock mismatches, 0 page errors, 156 picks; the final state equals Yahoo's recap name and seat at all 156 picks.

| what happened in the room | the log line | what the tool did |
|---|---|---|
| a missed pick restored at #6 | "inserted Jayson Tatum at #6" (to seat 6) | the later picks shifted one place and re-seated by the snake; replay echo matched |
| a missed pick restored at #92 | "inserted Brandon Ingram at #92" (to seat 5) | the later picks shifted one place and re-seated by the snake; replay echo matched |
| "Lendeborg" typed again after #130 was logged | "skipped \"Lendeborg\": already off the board (no pick logged)" | refused; nothing logged, the board unchanged |
| the last round entered out of order (#154 Jimmy Butler logged to the owner's seat) | "undid: Maxime Raynaud (Seat 11)"; "undid: Jimmy Butler (Seat 10)" | both picks removed in reverse order, then #154 Devin Vassell (seat 10), #155 Jimmy Butler (seat 11), #156 Maxime Raynaud (seat 12) re-logged, as Yahoo's recap has them |

The resolver's choices on shared surnames ("assumed over" lines, 12): every one agrees with Yahoo's recap — yes. Injury-excluded namesakes skipped by rule: #24 LaMelo Ball (Lonzo Ball skipped), #84 Day'Ron Sharpe (Shaedon Sharpe skipped). Heads-up lines ("injury-excluded on this board", the pick logged as typed): #117 Jusuf Nurkic → seat 4, #154 Jimmy Butler → seat 10, #155 Jimmy Butler → seat 11; Butler went at #155 to seat 11.

**The shift line (D83-1).** After the Tatum insert, the paste and the replayed page both print: "⚠ #10 Tyrese Haliburton is YOUR pick after the shift — Tyrese Haliburton is the 🎯 (card as of now)". The page builds that line from the card as last rendered (`cardGapText`, `docs/draft-deck.html`); Haliburton was already logged and so was not on that card, the lookup found no row, and the fallback text — written for the case "the pick is the 🎯" — printed instead. The card on the true board at #10 (`m83_deckcard_v69.json`) had Tyrese Maxey as 🎯 and Haliburton #2, 0.005 behind. The line is a log message only; nothing the card computes reads it. Not fixed tonight (publish freeze, D-1013-5).

The grading pipeline's Python port differs from the page record at 0 turns; the page record is the authority for what the card said.

## Watchlist

- #10 across the recent live rooms (page records): mock 75 Karl-Anthony Towns (card #1, 🎯 Karl-Anthony Towns); mock 77 Donovan Mitchell (card #4, 🎯 Jamal Murray); mock 78 Tyrese Haliburton (card #9, 🎯 Jamal Murray); mock 79 Tyrese Haliburton (card #9, 🎯 Jamal Murray); mock 80 Tyrese Haliburton (card #2, 🎯 Tyrese Maxey); mock 81 Tyrese Haliburton (card #2, 🎯 Tyrese Maxey); mock 82 Tyrese Haliburton (card #1, 🎯 Tyrese Haliburton); mock 83 Tyrese Haliburton (card #2, 🎯 Tyrese Maxey).
- A missed pick in the first round (Tatum at #6) moved the owner's own pick: the tool caught it with Insert-at-#, and the shift line printed the wrong 🎯 claim (D83-1). In the real draft, check the pick counter against Yahoo's before the owner's turn.
- The publish freeze during the draft (D-1013-5) and no RESYNC during the draft (D-1013-2) stand.

## Open-item receipts

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| (this room) | records only; no web research and no roster pull | the room's names resolve to the lock pool 156 of 156 |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this grade (did not check) |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 beb243ef57af), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 32 of 32 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-14.csv`, Hashtag `hashtag-2026-10-14.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-14.csv`, `hashtag-2026-10-14.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 31 of 32 | 44 | 111 | 63 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 23 of 32 | 32 | 67 | 58 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 14 of 32 | 107 | 138 | 182 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 12 of 32 | 101 | 182 | 100 | 125 | 148 | 155 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| John Collins | 12 of 32 | 73 | 117 | 105 | 72 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Brandin Podziemski | 11 of 32 | 93 | 146 | 74 | 102 | 114 | 132 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 10 of 32 | 92 | 179 | 89 | 117 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 9 of 32 | 6 | 32 | 15 | 24 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 6 of 32 | 114 | 139 | 122 | 130 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Jaden McDaniels | 6 of 32 | 62 | 90 | 42 | 67 | 86 | 59 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Immanuel Quickley | 5 of 32 | 67 | 94 | 65 | 73 | 79 | 84 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Keegan Murray | 5 of 32 | 83 | 142 | 82 | 94 | 102 | 85 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (18 mocks, value 9, market 18); Derrick White (16 mocks, value 27, market 45); Lauri Markkanen (15 mocks, value 21, market 37); Tyrese Haliburton (13 mocks, value 7, market 12); Kel'el Ware (10 mocks, value 57, market 77); Tyrese Maxey (10 mocks, value 5, market 9); Tyler Herro (9 mocks, value 51, market 69); Karl-Anthony Towns (8 mocks, value 12, market 15).


## Bounds

**Out of scope by design.**
- No line, price or engine change; the D83-1 line is flagged, not fixed.
- No Yahoo standings comparison: no screenshot came with this paste.
- The punt test and the advice line were not re-run: no punt was declared and no advisor click is in the feed.
- This is a room of random humans, not the league's managers.

**In scope and unverified.**
- Which page, Version 69 or Version 70: `UNVERIFIABLE` from the paste (no LEAN line in it); the engines are identical, so no figure here depends on it.
- The card the owner saw at the moment of the #10 pick: the tool was one pick short then (Tatum not yet logged), so the screen showed the card for the tool's pick #9 with Tatum available. This report grades the card on the true board, as for every room with an insert; the on-screen card at that moment was not reconstructed (did not check).
- Whether the season arms' title share holds against the league's real managers: `UNVERIFIABLE` until the draft.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D83-1 | the shift line after an Insert-at-# says "X is the 🎯" when X is simply not on the current card: (a) leave it until after the draft (publish freeze) and read the card, not that line; (b) after the draft, make the line say the card rank on the board before the pick, or say nothing | (a), then (b) after the draft |
| D82-1, D-INT-1, D-INT-2, D-1014-*, D-1013-*, earlier | carried | carried |

## Provenance

- Inputs: the owner's paste (`draft83-2026-10-14/owner_message.txt`, verbatim); the current page `docs/draft-deck.html` (Version 70, deck main `0fdb485`); pool tag v69 (rev `af91b23`).
- Tools: `build_state.py`, the deck's `arena/mocks/live_retro.py` (mock 83 registered on tag v69: replay, final, hindsight, arms), `live_deckcard.py`, `live_replay_dom.mjs`, `scripts/repeat_market_check.py` (32 of 32 mocks, 12 flagged), `write_report.py`. Records in `arena/results/m83_*.json` and this folder.
- No line, tag or placement changed on either plane.

## In plain language

**How the room went.** About a 30 percent title share, 1 of 12 by title odds and 1 of 12 week to week, favored against 11 of the other 11. You followed the card at 11 of 13 picks and stayed in its Top 5 at all 13.

**The pick to learn from.** The best single change would have been #34: Chet Holmgren instead of Kawhi Leonard, worth about +2.3 title points. Following the 🎯 at every turn would have graded 30.6 percent, +0.9 points against as drafted.

**The tool.** Your corrections all worked: the two inserts (Tatum at #6, Ingram at #92), the double undo at the end, and the refused repeat of Lendeborg left the tool's board identical to Yahoo's, 156 of 156. One line misled: after the Tatum insert it said "Haliburton is the 🎯". At #10 the card actually had Tyrese Maxey first and Haliburton second, 0.005 behind — a near tie. That line is a message only and doesn't change the card; trust the card itself.

**Your decisions.** D83-1, that message; the default leaves it until after the draft.
