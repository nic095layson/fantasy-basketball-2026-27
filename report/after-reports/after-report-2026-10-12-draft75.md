# After-report — draft_75: the fifteenth live-human room from the real slot 10, the first on deck v59 — the card followed at 10 of 13 turns; the punt test

**Owner requests (2026-10-12, verbatim):** "How do you set punt box? If the system sees a clear path to punt and dominate other cats, I give it authority to do so" (with the decision card's screenshot: "Losing AST to most of the room, 2 picks running … Punting them works: you'd be winning 7 of the other 8 categories (need 6). Your call — set the punt box if you agree."), then "Here is this draft, which triggered the Punt question, for you to review. After analysing this draft, please conduct your tests and let me know your findings." — the deck tool's pick-by-pick feed (LIVE mode) and Yahoo's recap. Graded as mock 75, the standing live-room protocol; the punt test is §10.

**Room:** public Yahoo mock, 12 × 13, owner seat 10 (random humans — a practice rep, not opponent intel; display names 1 Ray, 2 Peter, 3 Wayne, 4 Julien, 5 Josh, 6 KeVsTeR, 7 Matus, 8 cihan, 9 LeonEs, 10 David, 11 Orlando, 12 David are not the league's; seat 12 is a second "David", so the owner is identified by seat). **Deck used:** v59 (rev `f918062`, live at the standing URL from 17:03 UTC — the 10/12 ADP refresh: the 10/12 Yahoo prices baked, pool and values identical to v58; Porziņģis veto live). The page's own echo code re-emitted the owner's 3 "off the card" lines identically in the replay (#58 Anunoby rank 2, 0.002 behind Payton Pritchard; #87 Sharpe rank 3, 0.004 behind Isaiah Hartenstein; #111 Hachimura rank 67, 0.318 behind Devin Vassell); v58 replays the same lines (the card-gap arithmetic is price-blind), so the version is fixed by the publish time (A1). **Method:** the recap resolved to pool names by the tracker's own resolver (`hoops.py draft resync`, 156 of 156); the tool log replayed through the real page in headless Chromium and reconciled against the recap; the grade is the deck plane's machine-derived retro (`arena/results/m{M}_*.json`, debrief `debrief_{DATE}_mock{M}_slot10.md`; title odds on the league's real eight-team bracket). Every figure below is read from those files. Verification: this file passes `report/check_report.py` and the deck's `judgment_open_items.py --check-report` and `repeat_market_check.py --check-report`.

Pull window: 2026-10-12 → 2026-10-12 (analysis only, the fourth report of the day; no roster pull).

**Headline.** As drafted **29.39 percent** on the real bracket (rank 2 of 12), expected weekly category wins 5.486, rank 2 of 12 (next 5.508), favored in 10 of 11 head-to-heads; the card's 🎯 taken at 10 of 13 turns, a Top-5 row at 12 of 13 (off the card: #58 OG Anunoby (card #2), #87 Day'Ron Sharpe (card #3), #111 Rui Hachimura (card #67)); the self-consistent follow-card chain from the same seat grades 35.79 percent. Category shape: REB, ST, BLK, TO in the top three of the weekly model, PTS ninth or lower. Hindsight's best single swap is Aaron Gordon at #111 (+0.159 a week). The tool log (158 events, one halt, one UNKNOWN fixed in place) replayed on the real page with zero drift; positions matched the pool on 156 of 156 picks. **The punt test:** at the 9 clear-path turns on record (the veto on): the punt-steered follow-card arm beat the plain follow-card arm at 4 of 9 turns, mean -0.32 title points; the registered bar (+2.0 points on 2 of 3 seeds) met at 2 of 9 — the bar did not hold; against the room as drafted the punt-steered card was worse at 4 of the 9 turns, level at 3, better at 2 (this room's #111 the one clear gain).

## 1. Roster changes

None — a public practice room; no pull, no row moved on either plane.

## 2. The team, replayed

| arm | ECW (rank; next) | favored | title odds (rank) |
|---|---|---|---|
| as drafted (the card's 🎯 at 10 of 13 turns) | 5.486 (rank 2; next 5.508) | 10 of 11 | 29.39% (rank 2) |
| follow-card, self-consistent (arms stage) | 5.678 (rank 1; next 5.480) | 11 of 11 | 35.79% (rank 1) |
| 🎯 at #58: Payton Pritchard for OG Anunoby (card #2; Payton Pritchard went #63) | 5.486 (rank 2; next 5.508) | 10 of 11 | 29.39% (rank 2) |
| 🎯 at #87: Isaiah Hartenstein for Day'Ron Sharpe (card #3; Isaiah Hartenstein went #106) | 5.486 (rank 2; next 5.508) | 10 of 11 | 29.39% (rank 2) |
| 🎯 at #111: Devin Vassell for Rui Hachimura (card #67; Devin Vassell went #135) | 5.486 (rank 2; next 5.508) | 10 of 11 | 29.39% (rank 2) |
| advice at #34: Derrick White for Anthony Davis (the 'now' man; Derrick White went #39) | 5.486 (rank 2; next 5.508) | 10 of 11 | 29.39% (rank 2) |
| advice at #58: OG Anunoby for Payton Pritchard (the 'now' man; OG Anunoby went #58) | 5.486 (rank 2; next 5.508) | 10 of 11 | 29.39% (rank 2) |
| the 2 advice 'now' men together (#34 White, #58 Anunoby) | 5.486 (rank 2; next 5.508) | 10 of 11 | 29.39% (rank 2) |
| hindsight single swap Jalen Johnson at #10 | 5.489 (rank 2; next 5.504) | 10 of 11 | 30.63% (rank 2) |
| hindsight single swap Tyler Herro at #58 | 5.486 (rank 2; next 5.500) | 10 of 11 | 29.96% (rank 2) |
| hindsight single swap Tyler Herro at #63 | 5.495 (rank 2; next 5.509) | 10 of 11 | 29.23% (rank 2) |
| hindsight single swap Zach LaVine at #87 | 5.514 (rank 1; next 5.508) | 10 of 11 | 29.52% (rank 2) |
| hindsight single swap Aaron Gordon at #111 | 5.645 (rank 1; next 5.505) | 10 of 11 | 34.64% (rank 1) |

Category ranks (weekly model): FG% 5 · FT% 5 · 3PTM 5 · PTS 9 · REB 3 · AST 6 · ST 3 · BLK 3 · TO 1.

## 3. Pick by pick — card vs owner vs hindsight

| pick | deck 🎯 (Top-5) | owner took | card rank · gap (blend) | hindsight best single swap (ΔECW vs final rosters) |
|---|---|---|---|---|
| #10 | Karl-Anthony Towns (Karl-Anthony Towns, Tyrese Maxey, Jalen Johnson, Tyrese Haliburton, Anthony Davis) | Karl-Anthony Towns | #1 · +0.000 | Jalen Johnson +0.003 |
| #15 | Tyrese Haliburton (Tyrese Haliburton, Donovan Mitchell, Jalen Williams, Jamal Murray, Derrick White) | Tyrese Haliburton | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #34 | Anthony Davis (Anthony Davis, Derrick White, Dyson Daniels, Desmond Bane, OG Anunoby) | Anthony Davis | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #39 | Derrick White (Derrick White, Desmond Bane, OG Anunoby, Dyson Daniels, Payton Pritchard) | Derrick White | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #58 | Payton Pritchard (Payton Pritchard, OG Anunoby, Tyler Herro, Darius Garland, Cameron Boozer) | OG Anunoby | #2 · +0.002 | Tyler Herro +0.000 |
| #63 | Payton Pritchard (Payton Pritchard, Tyler Herro, De'Aaron Fox, Cameron Boozer, Coby White) | Payton Pritchard | #1 · +0.000 | Tyler Herro +0.009 |
| #82 | Coby White (Coby White, Josh Hart, Jalen Suggs, Zach LaVine, Isaiah Hartenstein) | Coby White | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #87 | Isaiah Hartenstein (Isaiah Hartenstein, Jalen Suggs, Day'Ron Sharpe, Zach LaVine, Yaxel Lendeborg) | Day'Ron Sharpe | #3 · +0.004 | Zach LaVine +0.028 |
| #106 | Isaiah Hartenstein (Isaiah Hartenstein, Yaxel Lendeborg, PJ Washington, Sandro Mamukelashvili, Herbert Jones) | Isaiah Hartenstein | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #111 | Devin Vassell (Devin Vassell, Sandro Mamukelashvili, Herbert Jones, Collin Gillespie, Aaron Gordon) | Rui Hachimura | #67 · +0.318 | Aaron Gordon +0.159 |
| #130 | Yaxel Lendeborg (Yaxel Lendeborg, Herbert Jones, Collin Gillespie, Devin Vassell, Sandro Mamukelashvili) | Yaxel Lendeborg | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #135 | Devin Vassell (Devin Vassell, Herbert Jones, Fred VanVleet, Sandro Mamukelashvili, Collin Gillespie) | Devin Vassell | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #154 | Draymond Green (Draymond Green, Saddiq Bey, Herbert Jones, Jerami Grant, Kyle Filipowski) | Draymond Green | #1 · +0.000 | none positive (the pick was hindsight-best) |

[EVIDENCE: `m75_replay.json`, `m75_deckcard_v58.json`, `m75_hindsight.json`; card ranks are the deck's own JS replayed on the v59 page; the live echoes at #58 (0.002 behind Pritchard, rank #2), #87 (0.004 behind Hartenstein, rank #3), #111 (0.318 behind Vassell, rank #67) match the replay]

Advice line (page reading): fired at #34 (Derrick White now, Desmond Bane next turn (81% to survive): +0.022 cats/wk over the pair); #58 (OG Anunoby now, Payton Pritchard next turn (78% to survive): +0.035 cats/wk over the pair). Note: at #58 the owner took the pair exactly as the line said (Anunoby then, Pritchard at #63, who survived to that turn as the line's 78 percent said he probably would).

## 4. Tool-state integrity — the deck's board vs the recap, on the v59 page

| check | result |
|---|---|
| picks differing from the recap | **0 of 156**; owner's roster identical; nothing missing, nothing extra |
| events replayed | 158 (158 feeds incl. 12 shared-token feeds resolved by the 'assumed over' / 'skipped' rule and 1 heads-up feed; 1 halt; 0 undos; 0 inserts; 1 UNKNOWN feed) |
| the halt | the feed "Jalen" after pick #30 halted on Jalen Johnson (already drafted) with the fuller-name hint (Jalen Williams, Jalen Duren, Jalen Green); the owner resent the full name and the log continued with nothing lost |
| the UNKNOWN | "Mavion" at #119 found no match; the next feed (119- Davion Mitchell) fixed it in place, as designed (mock 54 lesson) |
| the empty resync | 1 "RESYNC refused: paste is empty" — the Rebuild button pressed with nothing pasted; the board was untouched, as designed |
| page reloads | 2 "resumed" markers (at 143 and 156 picks): the state persisted across both reloads, nothing re-fed |
| the page's own off-card echoes | re-emitted at #58, #87, #111 identical to the owner's paste (rank, three-decimal gap, 🎯); identical on the v58 page too |
| echo lines asserted / clock text / page errors | 158 of 158 / 0 mismatches / 0 errors |

[EVIDENCE: `arena/results/m75_tool_vs_truth.json`, `arena/data/events/m75_tool_events.json`; harness `live_replay_dom.mjs` on `page_v59.html` (and `page_v58.html`, `scratchpad m75/m75_replay_dom_v58.json`)]

## 5. Survival chips

Survival (`m75_survival.json`): this room 49 rows, predicted 0.499 vs realized 0.633, Brier 0.185; BUY NOW 0 of 5 survived, TOSS-UP 7 of 13, quiet 24 of 31. Pooled 51–75: 1268 rows, Brier 0.233.

Target-wait (`target_wait_2026-10-12b.json`, mocks 56–75): deep (mkt − pick ≥ 24) — 🎯s passed on 48, still there at the next owner turn 32, at the turn after 9 of 43; mid (12–23) — 🎯s passed on 15, still there at the next owner turn 7, at the turn after 1 of 14; near (< 12) — 🎯s passed on 32, still there at the next owner turn 12, at the turn after 0 of 30.

## 6. The draft room's positions vs the pool

0 of 156 positions differ, teams 0 of 156 [EVIDENCE: `scratchpad m75/positions_check.json`; the recap as pasted].

## 7. Where this human room took the preseason standouts

The standing comparison. The deck rank is the v58/v59 board (identical values), the ADP the 10/12 Yahoo file (Hashtag's column, the prices baked into the v59 page).

| player | deck rank (v59) | Yahoo ADP 10/12 | this room (humans) | mock 74, public, 10/12 | mock 73, public, 10/09 |
|---|---|---|---|---|---|
| Yaxel Lendeborg | 82 | 114.5 | #130 (David (seat 10)) | #106 (you) | #106 (you) |
| Ty Jerome | 101 | 110.2 | #91 (KeVsTeR (seat 6)) | #85 | #83 |
| Sandro Mamukelashvili | 81 | 119.1 | #151 (Matus (seat 7)) | #121 | #130 (you) |
| Ryan Rollins | 70 | 74.5 | #70 (Wayne (seat 3)) | #67 | #69 |
| Darryn Peterson | 140 | 103.3 | #127 (Matus (seat 7)) | #124 | #97 |
| Kel'el Ware | 80 | 76.2 | #81 (LeonEs (seat 9)) | #79 | #64 |
| Cameron Boozer | 48 | 55.4 | #65 (cihan (seat 8)) | #59 | #71 |
| Aday Mara | 315 | 107.7 | undrafted | undrafted | undrafted |
| Jalen Williams | 16 | 40.4 | #31 (Matus (seat 7)) | #34 (you) | #31 |
| Tyrese Haliburton | 7 | 13.5 | #15 (David (seat 10)) | #14 | #12 |
| Damian Lillard | 88 | 69.3 | #53 (Josh (seat 5)) | #63 (you) | #55 |
| Deni Avdija | 77 | 40.3 | #35 (Orlando (seat 11)) | #36 | #50 |

Late card: 0 unpriced rows across the owner's three turns in rounds 11–13. Repeat-name audit (`m75_repeat_names_audit.json`): the #1 changes at 12 of 13 turns under other rooms' rosters (10 of 13 against an empty roster); Gafford on the Top-5 at 0, Braun 0, Poeltl 0.

## 8. Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 ca032b2697c5), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 25 of 25 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-06.csv`, Hashtag `hashtag-2026-10-12.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-09-29.csv`. Cells: our per-game line against `yahoo-proj-2026-10-06.csv`, `hashtag-2026-10-12.csv`, `rotoballer-2026-09-29.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 5 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| PJ Washington | 20 of 25 | 87 | 155 | 178 | 144 | 141 | 121 | ast 2.4 vs 1.9-2; tov 1.5 vs 1.7-1.8; fg_pct .470 vs .448-.451; ft_pct .750 vs .698-.703 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Payton Pritchard | 19 of 25 | 37 | 85 | 33 | 90 | 92 | 72 | stl 1 vs 0.7-0.8; tpm 3.8 vs 3-3.2; tov 2 vs 1.3-1.3; ft_pct .850 vs .873-.875 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 18 of 25 | 28 | 64 | 60 | 56 | 43 | 44 | pts 18.5 vs 16.4-17; ast 2.3 vs 2.1-2.1; ft_pct .805 vs .813-.819 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Sandro Mamukelashvili | 17 of 25 | 81 | 169 | 138 | 105 | 153 | 120 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Daniel Gafford | 11 of 25 | 90 | 180 | 188 | 181 | 161 | 155 | pts 10.5 vs 9.1-9.8; reb 7.5 vs 5.8-6.5; ast 1.5 vs 1.1-1.2; blk 1.7 vs 1.2-1.4; fg_pct .700 vs .648-.689; ft_pct .700 vs .671-.687 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Jalen Suggs | 11 of 25 | 59 | 105 | 89 | 54 | 84 | 99 | pts 17 vs 14.1-15.1; ast 4 vs 4.8-5 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Yaxel Lendeborg | 11 of 25 | 82 | 141 | 94 | 121 | 137 | 98 | reb 7.5 vs 5.5-6.9; tpm 0.9 vs 1.2-1.3; fg_pct .520 vs .447-.498; ft_pct .740 vs .765-.828 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Isaiah Hartenstein | 9 of 25 | 75 | 104 | 141 | 92 | 100 | 102 | pts 11.5 vs 9.1-10.5; reb 11 vs 9.2-10.3; fg_pct .585 vs .597-.611; ft_pct .680 vs .642-.656 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 7 of 25 | 89 | 138 | 122 | 131 | 125 | 123 | pts 16.8 vs 13.4-15.1; tov 1.5 vs 1-1.2; fg_pct .465 vs .432-.443 | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Zach LaVine | 7 of 25 | 56 | 99 | 162 | 68 | 77 | 118 | pts 22.5 vs 17-21.1; reb 4.5 vs 3.1-3.6; ast 4 vs 2.8-3.4; tov 2.6 vs 2-2.4 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Josh Hart | 6 of 25 | 67 | 95 | 68 | 84 | 91 | 94 | pts 13.5 vs 11.9-12.2; tpm 1 vs 1.2-1.5; fg_pct .520 vs .498-.503; ft_pct .780 vs .751-.759 | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Anthony Davis | 5 of 25 | 5 | 42 | 36 | 26 | 28 | 31 | pts 24 vs 19.8-22; reb 11.8 vs 9.8-10.6; ast 3.4 vs 2.8-3.1; blk 2.1 vs 1.7-1.9; tpm 0.9 vs 0.5-0.6 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Coby White | 5 of 25 | 58 | 89 | 106 | 86 | 76 | 77 | ft_pct .900 vs .843-.864 | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Dyson Daniels | 5 of 25 | 11 | 62 | 20 | 64 | 56 | 53 | pts 14.5 vs 11.3-11.8; stl 3 vs 2-2.4; tpm 1.1 vs 0.5-0.6; fg_pct .495 vs .501-.513 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Herbert Jones | 5 of 25 | 74 | 182 | 147 | 169 | 134 | >250 | — | LINE QUESTIONED: all 4 outside ranks sit 25+ places below ours; re-derive at the next projection pass (two dated outlets) |
| Saddiq Bey | 5 of 25 | 95 | 175 | 109 | 132 | 169 | 143 | blk 0.4 vs 0.1-0.1; tpm 2.4 vs 1.8-2; tov 1.5 vs 0.8-0.9 | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Karl-Anthony Towns (20 mocks, value 6, market 15); Jalen Williams (16 mocks, value 16, market 40); Derrick White (14 mocks, value 24, market 45); Jalen Johnson (6 mocks, value 13, market 11); Mikal Bridges (6 mocks, value 61, market 84).

What this room changed (the check re-run with mock 75 registered on the v59 page, `arena/results/repeat_market_check_2026-10-12_m75.json`; the previous run, with mock 74 registered, on 24 mocks is `repeat_market_check_2026-10-12_m74.json`): 25 of 25 mocks replayed; 16 flagged against 14. Newly across the five-mock bar: Anthony Davis (the 🎯 in 5 mocks, value 5 against market 42), Coby White (the 🎯 in 5 mocks, value 58 against market 89). LINE QUESTIONED lines: PJ Washington, Daniel Gafford, Devin Vassell, Herbert Jones (unchanged). Every flagged line sits inside the owed WO-5 top-150 re-derivation, where the D-RN-3 range check requires a mechanism for each outlier cell.

## 9. The off-card turns, read one by one

- **#58 OG Anunoby** (card #2, 0.002 behind Payton Pritchard, who went #63 to David (seat 10)): the 🎯 alone +0.00 title points (a zero by construction: the owner took Pritchard at the next turn, so the pairwise swap returns the same thirteen men); hindsight's best single swap here is Tyler Herro +0.000 a week. This was the advice line's own pair (OG Anunoby now, Payton Pritchard next turn (78% to survive): +0.035 cats/wk over the pair), taken as advised.
- **#87 Day'Ron Sharpe** (card #3, 0.004 behind Isaiah Hartenstein, who went #106 to David (seat 10)): the 🎯 alone +0.00 title points (a zero by construction: the owner took Hartenstein at the next turn, so the pairwise swap returns the same thirteen men); hindsight's best single swap here is Zach LaVine +0.028 a week.
- **#111 Rui Hachimura** (card #67, 0.318 behind Devin Vassell, who went #135 to David (seat 10)): the 🎯 alone +0.00 title points (a zero by construction: the owner took Vassell at the next turn, so the pairwise swap returns the same thirteen men); hindsight's best single swap here is Aaron Gordon +0.159 a week.

## 10. The punt test

**The question.** The card at this room's late turns read "Losing AST to most of the room, 2 picks running … Punting them works: you'd be winning 7 of the other 8 categories (need 6). Your call — set the punt box if you agree." The owner asked how the box is set and offered the system authority to set it when it sees a clear path. The box is set before pick 1 by the setup chips, or mid-draft only by Export, edit `"punt"`, Import; the one-click Adopt/FULL TILT/Retarget buttons sit behind `PUNT_BUTTONS` (off since 9/22, D51R-3). A declared punt steers the council shortlist, the Fit lens and the coherence strip; the 🎯 ranking is punt-blind by measured design.

**Pre-registration.** The instrument and its bar were registered on 9/28 (`arena/mocks/punt_arms.py`, D54-3): at a turn, three arms on the room as it happened — as drafted; follow the card's #1 from that turn (blend50 over balanced value + ΔECW on all nine categories, strict pairwise swaps); the same follow-card with the card punt-steered (value and ΔECW over the kept categories only) — 6,000 CRN seasons × seeds 11/23/47, the league's real bracket, the veto on. **Bar:** the steered arm beats the unsteered arm by 2.0 title points or more on 2 of 3 seeds. The turns under test are every owner turn on record where the shipped advisor's clear-path rule was true (`punt_advice_effect.py` re-run over all 32 committed states on the v59 engine, 352 owner turns, `arena/results/punt_advice_effect_2026-10-12.json`): 11 turns, of which 9 are in registered live rooms (the mock-42 parity fixture of 2026-08-13 (slot 7, not a slot-10 room) and a mock-69 turn whose lean had not yet held two picks are listed, not run).

| room | turn | punt the advisor named | kept path | as drafted | follow the card | follow the card, punt-steered | steered minus plain | steered minus as drafted | what each arm took | seeds at the bar | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mock 56 | #135 | AST, PTS, REB | 5/6 | 43.66% | 43.66% | 41.15% | -2.51 | -2.51 | plain: as drafted; steered: #135 Cason Wallace | 0 of 3 | fail |
| mock 59 | #135 | PTS, AST | 5/7 | 20.38% | 20.69% | 19.68% | -1.02 | -0.70 | plain: #135 Saddiq Bey; steered: #135 Herbert Jones | 0 of 3 | fail |
| mock 65 | #63 | REB, PTS | 5/7 | 23.19% | 23.19% | 16.91% | -6.28 | -6.28 | plain: as drafted; steered: #63 Cason Wallace, #82 Herbert Jones, #87 Mikal Bridges, #106 Reed Sheppard, #111 Fred VanVleet, #135 Daniel Gafford | 0 of 3 | fail |
| mock 68 | #135 | AST | 6/8 | 28.36% | 25.66% | 28.71% | +3.04 | +0.35 | plain: #135 Fred VanVleet; steered: #135 Saddiq Bey | 3 of 3 | PASS |
| mock 74 | #135 | AST, PTS | 5/7 | 17.91% | 19.03% | 17.91% | -1.12 | +0.00 | plain: #135 Saddiq Bey; steered: as drafted | 0 of 3 | fail |
| mock 74 | #154 | AST, PTS | 5/7 | 17.91% | 17.91% | 17.91% | +0.00 | +0.00 | plain: as drafted; steered: as drafted | 0 of 3 | fail |
| mock 75 | #111 | PTS | 6/8 | 29.39% | 33.29% | 35.83% | +2.54 | +6.44 | plain: #111 Sandro Mamukelashvili, #154 Saddiq Bey; steered: #111 Fred VanVleet, #135 Sandro Mamukelashvili | 2 of 3 | PASS |
| mock 75 | #135 | AST, PTS | 6/7 | 29.39% | 27.54% | 28.18% | +0.64 | -1.21 | plain: #154 Saddiq Bey; steered: #135 Sandro Mamukelashvili | 0 of 3 | fail |
| mock 75 | #154 | AST, PTS | 6/7 | 29.39% | 27.54% | 29.39% | +1.85 | +0.00 | plain: #154 Saddiq Bey; steered: as drafted | 1 of 3 | fail |

Across the 9 turns: the steered arm better than the plain card at 4, mean -0.32 title points, the bar met at 2; against the room as drafted the steered arm is better at 2 of 9, mean -0.44. The 9/28 record at mock 54 #63 (assists punted from the sixth round, the veto on) reads 46.29 plain against 38.54 steered. Per-seed figures are in each `m<mock>_punt_arms_from<pick>_veto.json`.

**Reading.** The bar did not hold: met at 2 of 9 turns; the steered arm's mean -0.32 title points against the plain card and -0.44 against the room as drafted, better than the room at 2 of 9 and worse at 4. The aggregate rule (a majority of turns at the bar and a positive mean) was written into this report's generator while the first two runs were in, both failing. The turns at the bar read differently from each other: mock 68 #135 (punt AST): the steered card ends +0.35 against the room as drafted; it sidestepped the plain card's pick (#135 Fred VanVleet) rather than buying anything the room did not already have; mock 75 #111 (punt PTS): +6.44 against the room as drafted, the steered card taking #111 Fred VanVleet, #135 Sandro Mamukelashvili where the plain card took #111 Sandro Mamukelashvili, #154 Saddiq Bey; the one turn on record where the punt path bought title equity. 8 of the 9 turns fall in rounds 10 to 13, when the kept categories are already set and the punt only narrows the late card; the earlier one (mock 65 #63 (round 6) at -6.28) is the worst result on the table. This is the same direction as the 7/30 gap study (every punt policy −4.9 to −11.2 points), the 7/27 pivot gate and the mock-54 arms. The authority the owner offered would, on this record, lower the odds at more turns than it raised them; the advisor stays advice-only (D75-2 a) unless the owner prefers the one-click Adopt (D75-2 c), which keeps the decision in the owner's hand at the turn.

[EVIDENCE: `arena/results/punt_advice_effect_2026-10-12.json`; `arena/results/m<mock>_punt_arms_from<pick>_veto.json` for each row; `arena/mocks/punt_arms.py` (the bar in its docstring, registered 2026-09-28); `m54_punt_arms_veto.json` (2026-09-28)]

## Watchlist

- The 3 off-card turns: #58 OG Anunoby (card #2), #87 Day'Ron Sharpe (card #3), #111 Rui Hachimura (card #67). The card's man alone at each, with every other pick as drafted: #58 +0.00, #87 +0.00, #111 +0.00 title points (each a zero by construction: the owner took the card's man at the following turn, so the pairwise swap only reorders two of the owner's own picks); the whole follow-card chain +6.40.
- The preseason standouts (§7): the owed WO-5 pass re-derives their lines; the next human room then prices them on the new values.
- The survival chips against humans (D62-2: leave, log).
- The punt advisor: advice-only unless D75-2 says otherwise; the clear-path rule fires in the last four rounds on this record.

## Open-item receipts

| item | query run (2026-10-12) | dated finding |
|---|---|---|
| (this analysis) | machine replay only — no web research in this report | pull receipts for the window live in `after-report-2026-10-12.md` (the morning's pull), same day |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the day's pull, same day (after-report-2026-10-12.md, receipts dated 10/12) | all HELD or unsigned on 2026-10-12; nothing changed since |

## Bounds

- A1: the room ran on the v59 page (live from 17:03 UTC; the paste arrived after 18:20 UTC); the three echoes replay identically on v58, so the echoes cannot tell the two apart and the version is fixed by the publish time; the grade (values, pool) is identical on either.
- The punt test steers the card by the E20 ordering (value and ΔECW over the kept categories) at a fixed roster the room produced; it does not re-draft the whole room around a punt declared at pick 1, which no live room on record has done since the buttons came off. A pre-draft punt is a different experiment.
- Grades are on the v58/v59 lines; the owed WO-5 refresh will move them.
- A public room is a practice rep against strangers: the title odds are against the league's real bracket with these twelve rosters, not a forecast of the league.
- Hindsight is single-swap on current lines: an upper bound on what a different pick was worth, not a strategy.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D75-1 | The first human room on v59 grades 29.39 percent with the card followed at 10 of 13 turns (off the card: #58 OG Anunoby (card #2), #87 Day'Ron Sharpe (card #3), #111 Rui Hachimura (card #67)); the follow-card chain grades 35.79 percent. Log it? | log it; no card change |
| D75-2 | Punt authority (the owner's offer: let the system set the box when it sees a clear path). The test (§10): at the 9 clear-path turns on record (the veto on): the punt-steered follow-card arm beat the plain follow-card arm at 4 of 9 turns, mean -0.32 title points; the registered bar (+2.0 points on 2 of 3 seeds) met at 2 of 9. Options: (a) advice-only stays — the card says "Punting them works" and the owner sets the box by the setup chips or Export/Import; (b) auto-adopt — the rule writes the box when it fires (two turns held, 70 percent of the kept categories winnable) and the 🎯 steers on the kept categories from then on; (c) `PUNT_BUTTONS = true` — the Adopt button returns beside the advisor's sentence, one click, the owner decides | (a) — the bar did not hold; (c) on request |
| D74-1, D-1012-2, D-1012-1, D-1011-4, D-1011-1..3, D-1010-2, D-1010-1, D-RN-6, D73-1, D72-1, D71-1, D70-1, D69-1, D68-1..3, D61-4, D-RN-1..5, D67-1..6, D66-1, D-V4-1, D-CAST-1..4, D62-1..3, D-1008-1..3, D-1009-1..13 and earlier | carried | carried |

## Provenance

- Inputs: the owner's paste (the deck tool's LIVE feed and Yahoo's recap, 2026-10-12), pinned as `scratchpad m75/paste.txt`; the recap resolved by `hoops.py draft resync` to `arena/data/states/draft_state_75.json` (md5 `2dbbc53780830fdb7055c9f844a1af00`); the tool events pinned as `arena/data/events/m75_tool_events.json`; the pool is rev `f918062`'s data/players.csv, whose values equal `arena/results/m74_players_v58.csv` (tag v58).
- Every figure from `arena/results/m75_*.json`, `target_wait_2026-10-12b.json`, `punt_advice_effect_2026-10-12.json` and the `m<mock>_punt_arms_from<pick>_veto.json` files; the arms use 18,000 CRN seasons (seeds 11/23/47) on the real eight-team bracket; the deck card, the DOM replays and the audit ran the v59 page's own engine (and the v58 page's for the version check); §7's prices from `report/market/yahoo-2026-10-12.csv` and the deck board snapshot of the 10/12 pull.
- Not verified: nothing here rests on web research.

## In plain language

**What this was.** A live room against twelve strangers on today's page. It grades 29.4 percent on the real bracket, second of twelve, second in expected weekly category wins, and you took the card's name at 10 of 13 turns and a Top-5 name at 12.

**What the card left on the table.** Hindsight's best single swap is Aaron Gordon at #111, worth about 0.16 categories a week. The advice line spoke at 2 turn(s).

**Following the card.** Following it all the way grades 35.8 percent against 29.4 as drafted.

**The tool.** The log replayed on the real page with zero drift: one halt (the bare "Jalen" with three Jalens left, resent as the full name), one typo ("Mavion") fixed in place by the next feed, one empty Resync press that refused to touch the board, two page reloads that resumed where they were, 12 shared-surname feeds resolved as the page said, and the 3 off-card lines you saw are the page's own, re-emitted to the third decimal.

**The punt test.** I ran the registered test at every turn on record where the card said "Punting them works" (9 turns in 6 rooms, including this one at #111, #135 and #154). Declaring the punt beat not declaring it at 4 of 9 turns, by -0.32 title points on average, and cleared the registered bar at 2 of 9. Against the room as drafted the punt-steered card was better at 2 of 9 turns and worse at 4. The one turn where it clearly paid was this room at #111 (+6.44 title points had the card punted points there and taken VanVleet over Mamukelashvili); the other pass, mock 68, only avoided a bad plain-card pick. On the record, the authority you offered would lower the odds at more turns than it would raise them, mainly because the clear path shows up in the last four rounds, when there is little left to build with. So the card keeps saying it in words and the box stays yours; if you want it one click away, say so and the Adopt button comes back (D75-2 c).

**Your decisions.** D75-1 log the room (default yes). D75-2 the punt authority (default a, with c on request). Everything earlier is carried.
