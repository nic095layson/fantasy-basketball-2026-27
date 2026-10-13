# After-report — the 10/13 live mock: the RESYNC wipe reproduced, the page identified, the card against the practice page, and the Yahoo question

**Owner request (2026-10-13, verbatim):** "I just completed a live mock draft and experienced a critical system failure when using the RESYNC feature. This draft and the card's suggestions look wildly different than how we've been practicing for months. I am scared that we deviated significantly with this re-deveration and I want to work with you extensively today to ensure we have a championship caliber system ahead of tomorrow's draft. Did you find major statistical drift from the yahoo intake today?" With a screenshot, the page's pick-by-pick history, the roster and Yahoo's round-by-round results (all in `live-mock-2026-10-13/owner_message.txt` and `owner_screenshot.png`).

**Method:** an assessment, not a fix — nothing on either plane changed for it. (1) RESYNC: the page's own code read, then the failure reproduced in headless Chromium on the Version 63 page bytes (sha256 `1ec428cd372a`, the deck's `d9916ce`): a 141-pick board built from Yahoo's recap, then the owner's history text pasted into RESYNC exactly as it stood; plus the natural retry, Yahoo's recap pasted as-is, the recap as a semicolon list, and the console restore with a reload. (2) Page identity and the card: the deck's own card replayer (`arena/mocks/live_deckcard.py`; the page's data and engine blocks run under node, the extraction the parity gate pins) at the 13 slot-10 turns of the room rebuilt from Yahoo's recap, on Versions 58, 59 (the practice page), 60 (WO-5), 62 (the minutes-and-games pass), 63, and the unpublished 64 (today's Yahoo re-price). (3) Lines against Yahoo: each page's value rank (neutral weights, the replayer's own value order) against Yahoo's projected-line Rank and ADP in `report/market/yahoo-proj-2026-10-13.csv`. (4) The drift question: Yahoo's 10/06 and 10/13 projection files compared field by field. Verification: the seven UNKNOWN lines the reproduction printed are byte-identical to the owner's; the eight "off the card" echoes in the owner's history reproduce to the digit on Versions 62 and 63; every comparison was saved as a script, re-run from this folder and matched its first output byte for byte; the card replays and value ranks were run twice and matched.

Pull window: 2026-10-13 → 2026-10-13 (analysis only; no roster pull; no line, board, tag or page changed by this report).

**Headline.** No statistical drift came from Yahoo: its 10/13 projections are identical to its 10/06 projections on all 249 shared names, in games and in all nine categories; only Yahoo's ranks, prices and injury letters moved, and that re-price was not on the page you drafted on. Replayed on your room, it changes no 🎯 at any of your 13 turns. The card *did* change a great deal, and your read is right: your practice page and today's page agree on the 🎯 at **0 of 13** turns, and their Top 5s share 1.5 names on average. That change is the two line passes you approved — WO-5 on 10/12 (it alone changed the 🎯 at 12 of the 13 turns) and the minutes-and-games pass on 10/13 (which changed 6 of the 13 again) — and its direction is *toward* Yahoo's own projections, not away: on Yahoo's top 150 our order now agrees with Yahoo's projected-line rank at ρ 0.827, up from 0.781, with 53 players 25+ places apart against 69. The RESYNC failure is a page defect, reproduced exactly: the box expects a semicolon list of names, you pasted the page's own history, its six semicolons cut it into seven pieces that are not names, and RESYNC wipes the board before it checks anything. Your board was correct at the moment of the wipe (141 of 141 picks match Yahoo's recap). The 141-pick board is still saved in your browser unless RESYNC ran again, and a tested console snippet restores it.

## 1. Roster changes

None — analysis only; no row moved on either plane.

## 2. The RESYNC wipe, reproduced

**What the page did (EVIDENCE, your history, lines 162–171 of `owner_message.txt`).** `RESYNC refused: paste is empty — nothing cleared, the board is untouched.` then `RESYNC: cleared 141 pick(s); rebuilt 7 from the paste. Prior board saved in this browser (draftdeck.v1:preresync).`, seven `⚠ (R1) #1..#7: UNKNOWN (...)` lines, and `— resumed: 7 picks logged —` after a reload. The screenshot shows the result: `Pick #8 · R1/13 Seat 8 on the clock … 318 available`, `⚠ 7 UNKNOWN open: #1, #2, #3, #4, #5, #6, #7`, and a card reading "Take Nikola Jokic — top of the 9-cat value board". That card is the wiped board talking, not the lines: with seven unknown picks the page believes it is pick #8 of round 1.

**Why (EVIDENCE, the page's `runResync`, deck `docs/draft-deck.html` lines 2348–2369 at `d9916ce`).** The Resync box is a one-line text input whose placeholder asks for "the FULL pick list in draft order (semicolons)". Pressing Enter or "Rebuild board" splits the paste on `;` only, refuses only an empty paste, saves the current board under `draftdeck.v1:preresync`, sets the picks to empty, and rebuilds positionally from whatever the paste parsed. Nothing checks that the pieces are players, nothing asks before wiping, and nothing on the page reads the saved board back.

**Why your paste gave exactly seven pieces (EVIDENCE, `parse_inputs.py`).** The history text you pasted (lines 6–162 of your message, 157 lines) contains six semicolons, all written by the page itself: the header line ("156 picks; you are Team 10"), the three insert echoes ("→ Seat 2; #23–#26 → …" and the same for Amen Thompson and Murray-Boyles) and two resolver notes ("(only Miles left; …)", "(only Davion left; …)"). Six cuts make seven pieces; none is a player name, so each became an UNKNOWN pick at #1–#7. A line break pasted into a one-line box becomes a space; your seven UNKNOWN lines show three spaces at each break.

**The reproduction (EVIDENCE, `repro_resync.mjs` → `repro_v63.json`, `repro_double.mjs` → `repro_double_v63.json`; Version 63 bytes; no page errors).**

| step | what was pasted | result on the page |
|---|---|---|
| A | Yahoo's first 141 picks as a semicolon list | 141 picks, 0 UNKNOWN; your 12 picks on seat 10 |
| B | your history text, verbatim, Enter pressed | `RESYNC: cleared 141 pick(s); rebuilt 7 from the paste.` — 7 UNKNOWN; the seven UNKNOWN lines **byte-identical** to yours; the saved board holds the 141 picks |
| C | (reload) | the page resumes the wiped board: `— resumed: 7 picks logged —`, as you saw |
| D | console restore (below), then reload | 141 picks back, identical to step A; strip reads `Pick #142 · R12/13 Seat 3 on the clock your next: #154` |
| E | after a wipe, the same paste again (the natural retry) | board 7, saved board now **7** — the 141-pick board is gone for good |
| F | Yahoo's round-by-round results pasted as-is | `RESYNC: cleared 141 pick(s); rebuilt 1 from the paste.` — the recap format wipes the board too |
| G | the recap turned into "First Last; …" | 156 picks; 1 UNKNOWN (#147 Brice Sensabaugh, not in the 335-row pool); your 13 picks on seat 10 |

**The board was right before the wipe (EVIDENCE, `board_sync.py`).** All 141 picks in your history, with the three late inserts and the #141 "Mamy" fix applied, match Yahoo's recap by name and by seat: 0 differences. RESYNC replaced a correct board.

**Recovery (EVIDENCE, step D).** In a desktop browser on the deck page, open the developer console and run:

```js
const d = JSON.parse(localStorage.getItem("draftdeck.v1"));
d.state = JSON.parse(localStorage.getItem("draftdeck.v1:preresync"));
localStorage.setItem("draftdeck.v1", JSON.stringify(d));
location.reload();
```

It works only while the saved board is the one you want: one RESYNC overwrites it (step E). Your history ends at `— resumed: 7 picks logged —` with no second RESYNC, so your browser should still hold this room's 141 picks (INFERENCE — did not check; only your browser holds it). The room itself needs no restore: Yahoo's recap gives all 156 picks (`draft_state_m76.json`).

**What RESYNC accepts.** Only a semicolon list of names in draft order (step A). The page's own history (B) and Yahoo's recap (F) both wipe the board. Until D-1013-2 is decided, the safe tools in a live draft are "N- Name" for a wrong pick and Insert-at-# for a missed one; neither clears the board.

## 3. Which page you drafted on

**Versions 62 or 63 — identical for this room (EVIDENCE, `echo_check.txt`).** Your header reads "Data pull: 2026-10-13 · fresh today · 335 players", which only the pages published on 10/13 carry (Versions 61–63). Replayed at your turns, Versions 62 and 63 reproduce all 12 logged turns: the eight "off the card" echoes in rank, gap and 🎯 (Mitchell #6, 0.015 behind Maxey; Kessler #4, 0.013 behind Ware; Wagner #5, 0.010 behind Ware; Edey #40, 0.154 behind Ware; Mikal Bridges #5, 0.019 behind Edgecombe; Peterson #15, 0.064 behind Sheppard; Lendeborg #4, 0.010 behind Gillespie; Gordon #17, 0.150 behind Holiday) and the four turns where you took the 🎯 (Durant, Kawhi, Edgecombe, Holiday). Versions 58 and 59 reproduce 0 of 12. The unpublished Version 64 reproduces 11 of 12 (Gordon at #130 reads #16, 0.106 behind Holiday).

Your history shows five reloads during the draft (`— resumed:` after 15, 17, 47, 71 and 94 picks); the board survived each one. Version 63 replaced Version 62 during the day, so a reload across that publish would have switched versions mid-draft; in this room it would have changed nothing, because the two give identical cards at all 13 turns. Tomorrow it could matter (D-1013-5).

## 4. The card against the practice page — all 13 turns

EVIDENCE: `card_compare.txt`, from the replays `card_v59.json` … `card_v64.json`. The practice page is Version 59 (A1: the last page before WO-5, the one mock 75 was drafted on, with the same 10/12 prices as today's page, so only the lines differ).

| pick | you took | 🎯 practice page (v59) | 🎯 after WO-5 (v60) | 🎯 the page you drafted on (v62/v63) | 🎯 with 10/13 prices (v64) | your pick's card rank, practice / drafted-on |
|---|---|---|---|---|---|---|
| #10 | Donovan Mitchell | Karl-Anthony Towns | Tyrese Maxey | Tyrese Maxey | Tyrese Maxey | #10 / #6 |
| #15 | Kevin Durant | Chet Holmgren | Kevin Durant | Kevin Durant | Kevin Durant | #5 / #1 |
| #34 | Kawhi Leonard | Anthony Davis | Kawhi Leonard | Kawhi Leonard | Kawhi Leonard | #20 / #1 |
| #39 | Walker Kessler | Derrick White | Derrick White | Kel'el Ware | Kel'el Ware | #15 / #4 |
| #58 | Franz Wagner | OG Anunoby | Ryan Rollins | Kel'el Ware | Kel'el Ware | #3 / #5 |
| #63 | Zach Edey | Payton Pritchard | Ryan Rollins | Kel'el Ware | Kel'el Ware | #66 / #40 |
| #82 | Mikal Bridges | Payton Pritchard | VJ Edgecombe | VJ Edgecombe | VJ Edgecombe | #6 / #5 |
| #87 | VJ Edgecombe | Coby White | VJ Edgecombe | VJ Edgecombe | VJ Edgecombe | #19 / #1 |
| #106 | Darryn Peterson | Sandro Mamukelashvili | Reed Sheppard | Reed Sheppard | Reed Sheppard | #37 / #15 |
| #111 | Yaxel Lendeborg | Sandro Mamukelashvili | Collin Gillespie | Collin Gillespie | Collin Gillespie | #4 / #4 |
| #130 | Aaron Gordon | Sandro Mamukelashvili | Collin Gillespie | Jrue Holiday | Jrue Holiday | #8 / #17 |
| #135 | Jrue Holiday | PJ Washington | Reed Sheppard | Jrue Holiday | Jrue Holiday | #16 / #1 |
| #154 | Fred VanVleet | Saddiq Bey | Grayson Allen | Reed Sheppard | Reed Sheppard | #5 / #8 (no live card: the board was wiped) |

| pages compared | same 🎯 at your 13 turns | Top-5 overlap |
|---|---|---|
| practice (v59) vs WO-5 (v60) | 1 of 13 | — |
| WO-5 (v60) vs minutes-and-games (v62) | 7 of 13 | — |
| practice (v59) vs drafted-on (v63) | **0 of 13** | 1.54 of 5 on average (2, 2, 2, 2, 3, 1, 1, 1, 1, 2, 0, 1, 2) |
| v62 vs v63 | 13 of 13 | — |
| drafted-on (v63) vs 10/13 prices (v64) | 13 of 13 | 5 of 5 at every turn |

**What differs between the pages (EVIDENCE, `page_diff.txt`).** The card's engine code is byte-identical on Versions 58 through 64, and so is the owner veto (Porziņģis). Between the practice page and the page you drafted on, all 335 prices are identical, one availability tag differs (Raynaud's, added 10/13), and the values differ on 318 of 335 rows: the line passes. So the 0-of-13 is the lines.

**Version 59 stands for the week of practice (EVIDENCE, `practice_span.txt`).** Replayed on this room, the practice pages of 10/06 (Version 44), 10/08 (50), 10/09 (54) and 10/12 (59) named the same 🎯 at 11 to 13 of your 13 turns among themselves — Towns at #10, Holmgren at #15, Davis at #34, Anunoby at #58, Pritchard at #63 and #82, Mamukelashvili at #106 and #111. The page you drafted on shares the 🎯 with none of them at any turn (0 of 13 against each).

The replays hold the room fixed: every page sees the same picks before each of your turns, so the differences are the pages' own. On a practice page you might have picked differently and the room would have gone differently; the table does not model that.

## 5. Did the Yahoo intake drift anything?

**No (EVIDENCE, `drift_check.py` on the two pinned files).** Yahoo's 10/06 file has 250 names, the 10/13 file 300; 249 are on both. On those 249, games played and all nine per-game categories changed on **0** names. What moved is Yahoo's market and opinion: XRank on 217 names (largest move 63 places), ADP on 176 (largest 5.8 picks), Yahoo's own projected-line Rank on 107 (largest 4 places, a re-sort as 51 new names entered the list) and injury letters on 57. The re-price makes these the page's prices (294 of 335 rows priced, from 246). Prices do not enter the card's score; from round 11 they decide which rows the card may show (priced rows only), which is the one change the re-price makes in this room — Gordon at #130 reads #16, 0.106 behind Holiday, instead of #17, 0.150. The 🎯 is unchanged at all 13 turns and every Top 5 is identical (§4).

## 6. Our lines against Yahoo's own projections

The fear behind the question is that the re-derivation pulled the board away from the rest of the world. Measured against Yahoo's own projections, it did the opposite (EVIDENCE, `rank_agreement.txt`; 148 of Yahoo's top 150 joined — Herb Jones and Morez Johnson Jr. did not join by name):

| Yahoo's projection top 150 | practice (v59) | WO-5 (v60) | drafted-on (v63) |
|---|---|---|---|
| ρ, our value order vs Yahoo's projected-line Rank | 0.781 | 0.813 | 0.827 |
| mean distance between the two ranks, places | 32.6 | 30.7 | 29.7 |
| players 25+ places apart | 69 | 59 | 53 |
| ρ, our value order vs Yahoo ADP (142 priced) | 0.810 | 0.780 | 0.787 |

On Yahoo's top 60 the distance fell from 18.2 to 13.3 places and the 25+ gaps from 16 to 9; ρ rose from 0.651 to 0.691 (0.721 after WO-5 alone). Against ADP, the room's draft prices, agreement fell a little (0.810 to 0.787): the new board values some players above where the market drafts them. Ware is this room's example: value 27, ADP 76.4, the card's 🎯 at #39, #58 and #63, taken at #68.

**The names the card pushed in your room (EVIDENCE, `pushed_vs_yahoo.txt`).** Value rank on the page, Yahoo's projected-line Rank, Yahoo ADP, where the player went:

| today's 🎯s | our value rank | Yahoo Rank | ADP | went | our line minus Yahoo's (0.5+) |
|---|---|---|---|---|---|
| Tyrese Maxey | 4 | 4 | 9.7 | #12 | pts +2.1, ast +0.8 |
| Kawhi Leonard | 6 | 15 | 34.2 | #34 | pts +3.5 |
| Kevin Durant | 10 | 27 | 16.0 | #15 | pts +1.3, ast +0.5 |
| Kel'el Ware | 27 | 51 | 76.4 | #68 | pts +0.5, reb +2.1 |
| VJ Edgecombe | 56 | 31 | 74.7 | #87 | reb −0.5 |
| Reed Sheppard | 62 | 56 | 120.6 | undrafted | within 0.5 |
| Collin Gillespie | 79 | 100 | 123.2 | #133 | pts +0.8 |
| Jrue Holiday | 88 | 161 | 115.2 | #135 | pts +4.4, reb +0.6, ast +1.7, tpm +0.7, tov +1.0 |

| practice 🎯s | value rank on v59 | Yahoo Rank | ADP | went |
|---|---|---|---|---|
| Anthony Davis | 5 | 36 | 42.6 | #38 |
| Karl-Anthony Towns | 6 | 13 | 15.6 | #17 |
| Chet Holmgren | 10 | 19 | 30.6 | #20 |
| Derrick White | 24 | 25 | 45.1 | #43 |
| OG Anunoby | 28 | 60 | 67.7 | #70 |
| Payton Pritchard | 37 | 32 | 82.4 | #85 |
| Coby White | 58 | 106 | 90.5 | #90 |
| Sandro Mamukelashvili | 81 | 137 | 119.1 | #141 |
| PJ Washington | 87 | 178 | 116.6 | #140 |
| Saddiq Bey | 95 | 108 | 119.8 | undrafted |

Today's 🎯s sit a median 13 places above Yahoo's projected rank; the practice page's sat a median 22 above. The one large outlier today is Jrue Holiday (88 against Yahoo's 161; already LINE QUESTIONED on the repeat-name check), then Ware (27 against 51), Gillespie (79 against 100) and Durant (10 against 27).

**Why the practice card was different (EVIDENCE, earlier reports).** The 10/12 Towns report found the practice card's #10 pick rested on Towns' 2024-25 line ("on his 2025-26 line … the card's #1 at #10 is Maxey", `after-report-2026-10-12-towns-haliburton.md`), and the WO-5 report records that most star lines were then "older estimates — for the stars, mostly shaped like 2024-25", with 131 players and 435 cells outside every outside projection (23 and 25 after WO-5) and 49 top-200 lines more than a point off their own shooting (0 after) (`after-report-2026-10-12-wo5.md`). The method behind today's lines beat last-season-only in 7 of 7 seasons in the 2019-20 to 2025-26 backtest (composite error 0.3924 against 0.406 for last season alone and 0.4176 for career averages; 1,528 player-seasons of players with 20+ minutes the season before; `scope-fence-2026-10-13/out/modern/modern_history_20mpg.json`). The WO-5 report also records the honest limit: the out-of-sample test behind the 82% board-order confidence ran on the old ordering and was never re-run on the new one (§13 there).

## Watchlist

- Tomorrow's draft: RESYNC as it stands wipes the board on any non-empty paste (§2) until D-1013-2 is decided.
- The four names this room put furthest above Yahoo's own projection: Holiday, Ware, Gillespie, Durant (§6).
- The 10/14 lock paste (D-1013-1) and the publish freeze (D-1013-5).

## Open-item receipts

| item | query run (2026-10-13) | dated finding |
|---|---|---|
| (this analysis) | machine replay only — no web research in this report | pull receipts for the window live in `after-report-2026-10-13.md` (the morning's pull), same day |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (`after-report-2026-10-13.md`, receipts dated 10/13) | all HELD or unsigned on 2026-10-13; nothing changed since |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 a88d83f4e2f8), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 25 of 25 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-13.csv`, Hashtag `hashtag-2026-10-12.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-13.csv`, `hashtag-2026-10-12.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 5 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 20 of 25 | 38 | 117 | 48 | 60 | 101 | 71 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Kel'el Ware | 19 of 25 | 27 | 77 | 51 | 51 | 63 | 65 | ft_pct .732 vs .714-.723 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 19 of 25 | 62 | 180 | 56 | 118 | 126 | 129 | tpm 2.8 vs 2.2-2.6 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Lauri Markkanen | 16 of 25 | 11 | 37 | 18 | 31 | 41 | 29 | pts 26.4 vs 20.2-23.8; ast 2.1 vs 1.8-1.9; fg_pct .471 vs .452-.463 | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Jrue Holiday | 14 of 25 | 88 | 148 | 161 | 129 | 128 | 145 | pts 16.4 vs 12-12.8; reb 4.6 vs 4-4.2; ast 6.1 vs 4.4-4.6; tpm 2.6 vs 1.9-2; tov 2.8 vs 1.8-2.1; ft_pct .822 vs .855-.867 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Yaxel Lendeborg | 11 of 25 | 70 | 143 | 93 | 121 | 137 | 98 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Ryan Rollins | 9 of 25 | 28 | 74 | 58 | 63 | 78 | 83 | stl 1.7 vs 1.3-1.5 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Kawhi Leonard | 6 of 25 | 6 | 32 | 15 | 16 | 15 | 20 | pts 27.8 vs 23.7-24.3; tpm 2.6 vs 2.2-2.3 | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (21 mocks, value 7, market 18); VJ Edgecombe (12 mocks, value 56, market 75); Tyrese Maxey (7 mocks, value 4, market 9); Derrick White (6 mocks, value 30, market 45).

This is the check on the page as it now stands (Version 64, prices only against Version 63: values identical on 335 of 335 rows, `page_diff.txt`), run by the Yahoo re-price chain; the page you drafted on carried the same eight flags in the morning's pull (`after-report-2026-10-13.md`).

## Bounds

**Out of scope by design.**
- No fix was built: the RESYNC hardening and any line change are proposals on the decision sheet.
- No title odds: this room is not graded (offered as D-1013-4).
- The card replays hold the room fixed (§4); they do not model the room you would have had on another page.

**In scope and unverified.**
- Whether your browser still holds the 141-pick board — `UNVERIFIABLE` from here: the browser's storage is reachable only on your machine. Nothing here depends on it: the room comes from Yahoo's recap.
- The console restore inside claude.ai's artifact viewer — `UNVERIFIABLE` from here: it was tested on the page file in headless Chromium, not in your browser. If the deck page sits in a frame, the console must be switched to that frame first; in the wrong frame the snippet stops with an error ("Cannot set properties of null") before it writes anything. This weakens D-1013-2 (b) as a fallback and is part of why (a) adds an Undo button inside the page.
- The screenshot clock's time zone — `NOT-ATTEMPTED`; not load-bearing, because Versions 62 and 63 give identical cards at all 13 turns.
- Two of Yahoo's top 150 did not join by name (§6) — `ATTEMPTED-FAILED` (name folding); a 148-name sample, not 150.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-1013-2 | RESYNC before tomorrow's draft. Options: (a) harden it — show what the paste would do and ask before any wipe; refuse a paste whose pieces do not all resolve to players, or that is the page's own history; keep every replaced board with an Undo button; red-first browser test with your exact paste, the recap pasted as-is and a clean list; the full chain; publish; (b) no code change — the draft-day rule: never paste the history or the recap into Resync, fix a pick with "N- Name" or Insert-at-#, and if a wipe happens run the console restore (§2) before anything else; (c) hide the Resync button for the draft | (b); I recommend (a) with (b) as the procedure either way |
| D-1013-3 | The lines for tomorrow. Options: (a) keep today's lines (WO-5 + minutes-and-games, approved 10/12 and 10/13) and practice on them today; (b) go back to the practice page's lines (Version 59) with today's prices; (c) keep today's lines and, before the lock, re-check the four furthest above Yahoo's projection (Holiday, Ware, Gillespie, Durant) with two dated outlets each, moving a line only where both support it — a line edit, so it needs your go | (a); I recommend (a) |
| D-1013-4 | Grade this room as mock 76 (title odds as drafted, the card-follow chain, the tool log) on the page you drafted on | not graded (offered only) |
| D-1013-5 | No publish while you draft: the version on the page at your first pick stays until your last, so a reload cannot switch versions mid-draft | (a) freeze |
| D-1013-1, D-C2, D-SF-1..4, D-1011-4 and earlier | carried | carried |

## Provenance

- Inputs: the owner's message and screenshot (`live-mock-2026-10-13/owner_message.txt`, `owner_screenshot.png`); the deck pages from git (`b39838c` v58, `85d778d` v59, `7428778` v60, `81032d7` v62, `d9916ce` v63) and the unpublished Version 64 build (working tree, sha256 `a88d83f4e2f8`); the deck's `data/players.csv` at `85d778d` and `d9916ce`; `report/market/yahoo-proj-2026-10-06.csv` and `yahoo-proj-2026-10-13.csv`.
- Scripts (all in `live-mock-2026-10-13/`): `parse_inputs.py` (paste, echo lines, recap), `build_state.py` (the room as a deck state), `repro_resync.mjs` and `repro_double.mjs` (`env -u TMPDIR node <script> <page.html> <out.json>`), `replay_card.py` (the deck's `live_deckcard.py` with the state path, the punt timeline and three outputs added: the echo gap, the 🎯 row and the Top 10), `valranks.py`, `echo_check.py`, `card_compare.py`, `practice_span.py`, `page_diff.py`, `board_sync.py`, `pushed_vs_yahoo.py`, `rank_agreement.py`, `drift_check.py`. Outputs beside them.
- `repro_v63.json` step E ran on the restored board, so it does not test the retry; `repro_double_v63.json` is the retry test quoted in §2.
- Not verified: nothing here rests on web research.

## In plain language

**Did Yahoo change anything?** No. Yahoo's projections today are the same numbers it had on 10/06, for every one of the 249 players on both lists. Only its rankings and draft prices moved, and those were not even on the page you drafted on.

**Why the card felt so different.** Because it is different. Your practice page and today's page never named the same 🎯 at any of your 13 turns. That is not Yahoo. It is the two projection refreshes you approved on 10/12 and 10/13, which replaced lines that were mostly two seasons old with last season's production. The new numbers sit closer to Yahoo's own projections than the old ones did, not further away. Holiday is the one name today's card pushed that Yahoo's projection strongly disagrees with.

**What broke.** The Resync box wants a list of names separated by semicolons. You pasted the pick log, and the log happens to contain six semicolons of its own, so the box saw seven "names" that are not players. It then erased your 141 correct picks before checking anything, which is why the card started recommending Jokić again. Your old board is still saved in your browser, and the four-line console snippet in §2 brings it back, as long as Resync is not run again first.

**Your decisions.** D-1013-2: harden Resync before tomorrow (default: no change, just never paste the log; I recommend hardening). D-1013-3: keep today's lines (default and my recommendation), revert to the practice lines, or keep them and re-check four names. D-1013-4: grade this room, if you want it. D-1013-5: no publishing while you draft (default yes).
