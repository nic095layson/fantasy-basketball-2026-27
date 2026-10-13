# After-report — draft_77: the 10/13 late live room from slot 10, on deck Version 65 — the highest grade since September; Yahoo's projected standings beside ours

**Owner request (2026-10-13, verbatim):** "Here is a live mock for your analysis, as well as Yahoo system projections:" — the deck tool's LIVE feed, the owner's 13-man roster, Yahoo's round-by-round recap, and a screenshot of Yahoo's 2026-27 projected standings for the room.

**Room:** public Yahoo mock, 12 × 13, owner seat 10 (random humans; a practice rep, not opponent intel; display names: 1 charlie, 2 Swish Kebabs, 3 nactarum, 4 Tim, 5 Marko, 6 adrian mullins, 7 Isaac, 8 Carlos, 9 itsANDYdotcom, 10 David, 11 J, 12 Roy). **Deck used:** Version 65 (rev `dd6b719`, the dial pass; Porziņģis veto live). The page's own engine re-emits all six "off the card" echoes with the same rank, gap and 🎯.

Pull window: 2026-10-13 → 2026-10-13 (analysis only; no roster pull; the planes are held for tomorrow's final pull by the owner's decision).

**Headline.** As drafted **35.98 percent** for the title on the real eight-team bracket, rank 1 of 12, playoffs 99.91 percent: the highest as-drafted grade of any room since mock 58 (the best since then was mock 73's 34.17); 5 late-September rooms graded higher on earlier pools and projections: 51 (42.79), 52 (37.95), 54 (38.62), 56 (43.66), 58 (36.75). Expected weekly category wins 5.506, rank 1 of 12, favored in 11 of 11 head-to-heads. The card's 🎯 was taken at 7 of 13 turns and the pick sat in the Top 5 at 12 of 13; the self-consistent follow-card chain from the same seat grades 38.04 percent. The one costly turn was #39: Walker Kessler, card #9, where Donovan Clingan (taken the next pick) grades 40.14. Yahoo's projected standings put this roster second of 12 on season totals; on the same totals it is favored head to head against 10 of 11 teams, losing only to seat 9, whose edge is games played, not per-game production.

## 1. Roster changes

None. No line, tag, placement or price changed on either plane; this is a grade of a practice room.

## 2. The team, graded

EVIDENCE: `arena/results/m77_final.json`, `m77_arms.json` (18,000 seasons per arm, seeds 11/23/47, the real eight-team bracket), pool tag v65 = `players_v65.csv` (data/players.csv at `dd6b719`, sha256 bd2b983876a8).

| arm | title % | playoffs % | rank |
|---|---|---|---|
| as drafted | 35.98 | 99.91 | 1 |
| follow the card's 🎯 at every turn (self-consistent chain: #10 Jamal Murray, #15 Chet Holmgren, #39 Dyson Daniels) | 38.04 | 99.93 | 1 |
| single swap at #39: Donovan Clingan | 40.14 | 99.96 | 1 |
| single swap at #130: PJ Washington | 39.39 | 99.94 | 1 |
| single swap at #111: Myles Turner | 38.83 | 99.95 | 1 |
| single swap at #15: Chet Holmgren | 37.90 | 99.93 | 1 |
| single swap at #34: Lauri Markkanen | 37.83 | 99.93 | 1 |
| single swap at #10: Jamal Murray | 37.64 | 99.97 | 1 |
| single swap at #87: Jabari Smith Jr. | 36.49 | 99.92 | 1 |
| single swap at #106: Myles Turner | 36.33 | 99.92 | 1 |

Category shape (weekly model, rank of 12): FG% 4, FT% 1, 3PTM 3, PTS 5, REB 4, AST 10, ST 2, BLK 7, TO 2. Assists are the one weak category (tenth); free throws first, steals and turnovers second.

## 3. Pick by pick: the page's card, the owner, hindsight

EVIDENCE: `m77_deckcard_v65.json` (the v65 page's own engine), `m77_hindsight.json` (every single-swap alternative scored by weekly category wins against the final rosters).

| pick | owner took | card rank | the page's 🎯 | hindsight's best alternative (Δ weekly cat wins) |
|---|---|---|---|---|
| #10 | Donovan Mitchell | 4 | Jamal Murray | Jamal Murray (+0.080) |
| #15 | Scottie Barnes | 2 | Chet Holmgren | Chet Holmgren (+0.054) |
| #34 | Kawhi Leonard | 2 | Lauri Markkanen | Lauri Markkanen (+0.070) |
| #39 | Walker Kessler | 9 | Kel'el Ware | Donovan Clingan (+0.101) |
| #58 | Michael Porter Jr. | 1 | Michael Porter Jr. | Naz Reid (-0.084) |
| #63 | Kel'el Ware | 1 | Kel'el Ware | Rudy Gobert (-0.200) |
| #82 | Ty Jerome | 1 | Ty Jerome | Jabari Smith Jr. (-0.005) |
| #87 | VJ Edgecombe | 1 | VJ Edgecombe | Jabari Smith Jr. (+0.023) |
| #106 | Yaxel Lendeborg | 2 | Reed Sheppard | Myles Turner (+0.010) |
| #111 | Ayo Dosunmu | 1 | Ayo Dosunmu | Myles Turner (+0.070) |
| #130 | Tre Jones | 5 | Saddiq Bey | PJ Washington (+0.058) |
| #135 | Saddiq Bey | 1 | Saddiq Bey | Bobby Portis (-0.028) |
| #154 | Devin Vassell | 1 | Devin Vassell | Bobby Portis (-0.006) |

The off-card turns: #10 Donovan Mitchell (card #4, 🎯 Jamal Murray); #15 Scottie Barnes (card #2, 🎯 Chet Holmgren); #34 Kawhi Leonard (card #2, 🎯 Lauri Markkanen); #39 Walker Kessler (card #9, 🎯 Kel'el Ware); #106 Yaxel Lendeborg (card #2, 🎯 Reed Sheppard); #130 Tre Jones (card #5, 🎯 Saddiq Bey). 5 of the six were within 0.010 of the 🎯 or at round 9 and later; #39 Kessler was the one wide miss (0.032 behind, card #9) and the one that cost: the 🎯 Ware lasted to the owner's #63 anyway, but the swap the grade rewards is Clingan, gone at #40.

## 4. Yahoo's projected standings against ours

EVIDENCE: `yahoo_standings_2026-10-13.csv` (the screenshot transcribed; recomputing roto points from its 12 rows reproduces Yahoo's printed order, the 6.5 tie included), `yahoo_compare.json` (each roster summed on Yahoo's per-player file of 10/13), `m77_final.json`.

| view | where this roster lands |
|---|---|
| Yahoo, season-total roto points | 2 of 12 (behind itsANDYdotcom) |
| Yahoo totals, head to head category by category | favored against 10 of 11; loses only to itsANDYdotcom (2-7) |
| the deck, weekly category model | rank 1 of 12, favored against 11 of 11; closest is seat 9 |

Both views name the same rival: seat 9 (itsANDYdotcom). Yahoo's edge for seat 9 is volume: summed from Yahoo's own per-player file, seat 9 carries 943 projected games against this roster's 890. Per player-game this roster leads in points (16.71 to 16.12), blocks and turnovers, is within 0.06 in rebounds, and trails slightly in threes, assists and steals. A season-total ranking rewards games; a weekly head-to-head with a fixed lineup rewards them only partly, which is why the deck ranks this roster first and Yahoo second. Summing Yahoo's 10/13 per-player file comes within 3.2 percent of the screenshot's points for every team but does not equal it, so the screenshot rests on a slightly newer Yahoo projection than the file on hand.

## 5. Tool-state integrity

recap picks 156; seats 12 (David = 10); pool-less 0: []; feed vs recap: 156 of 156 agree on name and seat; differences []; owner picks: #10 Donovan Mitchell, #15 Scottie Barnes, #34 Kawhi Leonard, #39 Walker Kessler, #58 Michael Porter Jr., #63 Kel'el Ware, #82 Ty Jerome, #87 VJ Edgecombe, #106 Yaxel Lendeborg, #111 Ayo Dosunmu, #130 Tre Jones, #135 Saddiq Bey, #154 Devin Vassell. The page's own engine reproduces all six echoes (rank, gap and 🎯). The grading pipeline's Python port, which keeps the pre-v24 name tie-break per its docstring, differs from the page by one place at 2 turns (#39: port 8, page 9, #111: port 2, page 1); the page record is the authority for what the card said. The as-drafted grade and the single swaps do not depend on card order; the follow-card chain's swaps at #10 and #15 are the page's 🎯, and at #39 the chain took Dyson Daniels because the 🎯 Ware was the owner's own later pick.

## Watchlist

- Walker Kessler: the one wide off-card turn (card #9 at #39); he carries the availability discount for his health tag. The card had Ware first, who lasted to #63.
- Seat 9's projected games lead on Yahoo; not a line question, a reminder that Yahoo's standings are season totals.
- The 10/14 lock paste (D-1013-1), the publish freeze during the draft (D-1013-5), no RESYNC during the draft (D-1013-2).

## Open-item receipts

| item | query run (2026-10-13) | dated finding |
|---|---|---|
| (this room) | records only; no web research and no roster pull | the room's names resolve to the v65 pool 156 of 156; the lines are the ones merged in kit PR #109 |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (`after-report-2026-10-13.md`, receipts dated 10/13) | all HELD or unsigned on 2026-10-13 per those receipts; not re-queried here (did not check) |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 09a889d4baa5), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 26 of 26 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-13.csv`, Hashtag `hashtag-2026-10-12.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-13.csv`, `hashtag-2026-10-12.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Kel'el Ware | 22 of 26 | 26 | 77 | 51 | 51 | 63 | 61 | ft_pct .732 vs .714-.723 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Reed Sheppard | 21 of 26 | 63 | 180 | 56 | 118 | 126 | 129 | tpm 2.8 vs 2.2-2.6 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Ty Jerome | 21 of 26 | 39 | 117 | 48 | 60 | 101 | 65 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Yaxel Lendeborg | 11 of 26 | 70 | 143 | 93 | 121 | 137 | 91 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Saddiq Bey | 8 of 26 | 90 | 177 | 108 | 132 | 169 | 157 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 7 of 26 | 79 | 183 | 100 | 126 | 148 | 155 | pts 12.7 vs 9.5-11.9; reb 4.1 vs 3.3-3.9; tpm 2.9 vs 2.1-2.7; tov 1.6 vs 1.1-1.4 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Dyson Daniels | 6 of 26 | 22 | 62 | 20 | 64 | 56 | 55 | reb 6.8 vs 5.8-6.4; ast 5.9 vs 4.7-5.5; tpm 0.3 vs 0.5-0.6 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Michael Porter Jr. | 6 of 26 | 32 | 60 | 55 | 62 | 70 | 57 | pts 24.5 vs 18.7-21.8; ast 3 vs 2.4-2.6; stl 0.7 vs 0.8-1; tpm 3.4 vs 2.9-3.1; tov 2.3 vs 1.9-2 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (22 mocks, value 6, market 18); Lauri Markkanen (15 mocks, value 21, market 37); VJ Edgecombe (13 mocks, value 58, market 75); Derrick White (10 mocks, value 29, market 45); Tyrese Maxey (7 mocks, value 5, market 9).


## Bounds

**Out of scope by design.**
- No line, price or engine change: the owner holds every decision until tomorrow morning's final pull.
- The punt test and the advice line were not re-run: no punt was declared and the advice line did not fire in the feed.
- This is a room of random humans, not the league's managers.

**In scope and unverified.**
- The exact Yahoo projection behind the screenshot: `UNVERIFIABLE` from here; the 10/13 per-player file on hand sums to within 3.2 percent of it but not exactly.
- Whether the season arms' title share holds against the league's real managers: `UNVERIFIABLE` until the draft.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-1013-10..14 | carried as set this evening; the owner's hold until tomorrow's final pull | hold |
| D-1013-1..9, D-C2, D-SF-1..4 and earlier | carried | carried |

## Provenance

- Inputs: the owner's paste (`draft77-2026-10-13/owner_message.txt`, verbatim) and the screenshot (`yahoo_standings_screenshot.webp`, transcribed to `yahoo_standings_2026-10-13.csv`); deck rev `dd6b719` (Version 65, page sha256 09a889d4baa5).
- Tools: `build_state.py` (state and feed check), the deck's `arena/mocks/live_retro.py` (mock 77 registered: replay, final, hindsight, arms) and `live_deckcard.py` (the page's engine), `scripts/repeat_market_check.py` (26 mocks), `yahoo_compare.py`, `write_report.py` (this file's writer). Records in `arena/results/m77_*.json` and this folder.
- No line, tag or placement changed; both planes' hashes equal before and after (e821ec1ddc67 kit, bd2b983876a8 deck).

## In plain language

**How the room went.** Your best practice room since late September: about a 36 percent title share, first of 12, and favored against every other team week to week. You followed the card at 7 of 13 picks and stayed inside its Top 5 at 12.

**The one pick to learn from.** At #39 you took Kessler, ninth on the card. Ware was the card's pick and lasted to you at #63, but Clingan, gone one pick later, would have been worth about 4 more title points. Everything else was within a hair of the card.

**Yahoo's view.** Yahoo ranks you second, behind seat 9. That is a season-total view, and seat 9 is projected for 53 more games; player for player you are level or ahead in most categories. On Yahoo's own numbers you beat 10 of the 11 teams category by category.

**Your decisions.** Nothing new; everything holds until tomorrow morning's final pull.
