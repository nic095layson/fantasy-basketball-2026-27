# After-report — 2026-10-14 (the lock): Yahoo and Hashtag 10/14 re-blended into the lines, Kawhi and Davis back to 0.78, deck Version 69

**Owner input (2026-10-14, verbatim):** "Yahoo ADP and Projections 10/14:" — Yahoo's player list from the draft room, 350 rows; then, with the Hashtag projections page printed to PDF (`Hashtag_Projections_10.14.pdf`): "Take the Yahoo and Hashtag projections dated today, and synergize with kit's as you see fit and meaningful. Provide to me the final 180 kit rankings and lock"; and, during the work: "I'm sorry, but for Kawhi and Anthony Davis, revert their health multiplier to 0.78".

Pull window: 2026-10-14 → 2026-10-14 (owner inputs, WO-4 and the lock; not a roster pull — the morning pull report `after-report-2026-10-14.md` stands).
Gate: `check_provenance.py` → `PROVENANCE GATE: PASS — all rows sourced; verified 2026-07-13 .. 2026-10-07`, exit 0.

**Method (stated to the owner before any line moved).** A1: the six-way blend you approved this morning, taken again *from our own pre-blend lines* (re-blending already-blended lines would count our line twice), with Yahoo 10/14 and Hashtag 10/14 in place of Yahoo 10/13 and Hashtag 10/12; RotoBaller, FantasyPros and the Basketball Monster cards (all 10/13) unchanged; each of the nine categories the equal-weight mean, shot attempts rescaled so points add up. A2: games, minutes, tags and teams stay ours — Yahoo's games cuts are listed, not applied. A3: Luke Kornet keeps the line your lock call restored. Then your mid-work call: Kawhi Leonard and Anthony Davis back from the lighter tier to `inj-risk` (×0.78).

**Headline.** The lock moved little, and only where today's outlets moved. Hashtag's page changed on 4 rows since 10/12; Yahoo revised 58 projection lines overnight. Re-blended, 54 lines move on both planes (Rui Hachimura +1.3 points, De'Andre Hunter −1.0, Jonathan Kuminga +0.9 the largest), and Obi Toppin is newly blended now that three outlets project him. The kit's final top 180 holds the same 180 players as this morning; 116 change place, by 2.59 places on average and 10+ for 7. Kawhi and Davis are back at ×0.78 on the draft page. The deck is Version 69, priced on Yahoo's lock paste (302 of 335 rows), every gate green, published and byte-verified.

## 1. Roster changes

None. Single-source flags only (F2; Yahoo is one outlet): Yahoo lists Lonzo Ball at CLE with the NA letter (the pool holds him unsigned) and Tyus Jones at DEN (not a pool row). No pool row changed team, entered or left.

## 2. What landed

- Kit, market: `yahoo-raw-2026-10-14.txt` (the paste, verbatim) and its outputs (`yahoo-2026-10-14.csv` the price file, `yahoo-proj-2026-10-14.csv`, consensus, unmatched, disagreements); `hashtag-raw-2026-10-14.txt` (the PDF's page text, pdfplumber, 10 pages, 238 lines) and `hashtag-2026-10-14.csv`, `unmatched-hashtag-2026-10-14.md`; both registered (derived 29 of 29).
- Kit, parser: `yahoo_market.py` reads the headerless draft-room copy, and its name resolver no longer joins a second Yahoo row on another team to a pool row a same-team Yahoo row already holds (the paste's third "J. Green", Lonzo Ball as "L. Ball" and Tyus Jones as "T. Jones"); a new check fails the run if two Yahoo rows land on one player (red-first: 3 problems with the rule off, 0 with it on).
- Kit, lines: `report/projections-2026-27.csv` (54 lines), `report/top-200-2026-27.md` (regenerated); `blend/tools/common.py` (`BLEND_SET=lock` selects the 10/14 files; unset, Version 67's sources stand), `blend/out/lines_blend_lock_2026-10-14.json`, `lines_blend_lock_apply_2026-10-14.json` (Kornet held), `apply_record_lock_2026-10-14.json`.
- This folder: `preblend.py` (the starting point), `revert_mild.py` (Kawhi, Davis), `board_diff.py`, `final_180.py` and **`final-180-kit-2026-10-14.md`**, `blend_lock.log`, `chain.log`, `rn_section.txt`, `publish.json`, this writer.
- Deck: `data/players.csv` (54 lines, two tags, 238 notes), `data/freshness.json`, `data/market-snapshot.csv`, `docs/draft-deck.html` (Version 69).

## 3. Today's two outlets

**Yahoo (the lock paste).** 350 rows, 186 with ADP; Q on 86, O on 14, NA on 6. Against the 10/13 paste: XRank identical on all 300 shared names; ADP moved on 130 by at most 1.0 (mean 0.24); Anfernee Simons lost his ADP (110.4; now priced by XRank 201, market rank 119 to 210). Projections revised on 58 names — games on 23 (Brandon Ingram 68 to 55; Kyle Filipowski 75 to 65; Kon Knueppel 79 to 70; Maxime Raynaud 74 to 65; Kyle Kuzma 71 to 65; Jusuf Nurkic 55 to 50, …), points per game by 1.5+ on Maxime Raynaud 12.2 to 8.8, Scotty Pippen Jr. 12.3 to 10.3, Kyle Kuzma 14.8 to 12.8, Jaylen Wells 13.8 to 12.2, Coby White 18.9 to 20.4, Damian Lillard 18.7 to 20.3, DeMar DeRozan 14.3 to 16.0, Kyrie Irving 21.4 to 23.6, Keyonte George 17.7 to 20.3, Gui Santos 7.3 to 10.1, Zach LaVine 17.0 to 20.0, Jonathan Kuminga 11.6 to 16.0, Rui Hachimura 11.4 to 18.6.

**Hashtag.** The 10/14 page (Updated: 14 October 2026) carries the same 200 names as 10/12; 4 rows differ: Kawhi Leonard (points 23.7 to 24.7, GP 58 to 50); Kristaps Porzingis (points 16.5 to 16.5, GP 42 to 30); Brandin Podziemski (points 14.5 to 15.1, GP 78 to 78); De'Andre Hunter (points 18.6 to 14.8, GP 65 to 65).

## 4. The lock re-blend

- **Starting point** (`preblend.py`): on all 241 rows of this morning's blend, today's kit and deck lines equal the blend's output (Kornet equals his restored pre-blend line) — nothing else touched a blended line since; each returned to its pre-blend line. PREBLEND: PASS.
- **Control**: the unchanged sources on that starting point reproduce this morning's blend on 241 of 241 rows, value for value — the tool and the starting point are the ones Version 67 used.
- **Lock run** (`BLEND_SET=lock`): 242 rows reach three or more outside lines (Toppin newly: Yahoo, Hashtag, FantasyPros); Kornet held; 24 rows with a shot factor outside 0.85–1.15, listed not held (the morning's rule); 0 problems. `blend_apply.py` PASS on A1–A9 (both planes in one pass; every category recomputed from the pinned files) — deck 238 rows, kit 241 rows rewritten against the pre-blend start; a second run changes nothing.
- **Against this morning's lines**: 54 rows move on each plane (the same rows on both, suffix spellings aside). The largest:

| player | points | rebounds | assists | threes | steals | FG% | FT% |
|---|---|---|---|---|---|---|---|
| Rui Hachimura | +1.3 | +0.4 | +0.2 | +0.1 |  | -0.009 | +0.004 |
| De'Andre Hunter | -1.0 | -0.2 | -0.1 | -0.1 | -0.1 | -0.005 |  |
| Jonathan Kuminga | +0.9 | +0.2 |  |  |  | +0.001 | +0.008 |
| Zach LaVine | +0.5 | +0.1 | +0.1 | +0.1 |  |  |  |
| Gui Santos | +0.5 | +0.3 | +0.2 |  |  |  | -0.001 |
| Kyrie Irving | +0.4 |  | +0.1 |  |  |  |  |
| Keyonte George | +0.4 | +0.1 |  |  |  | +0.004 | +0.001 |
| Scotty Pippen Jr. | -0.4 | -0.1 | -0.1 | -0.1 |  |  | -0.002 |
| Brandin Podziemski | +0.3 | +0.1 | +0.1 |  | +0.1 |  |  |
| Jaylen Wells | -0.3 | -0.1 |  | -0.1 |  |  | +0.001 |
| Damian Lillard | +0.3 | +0.1 | +0.1 |  |  |  |  |
| DeMar DeRozan | +0.3 | +0.1 | +0.1 |  |  |  |  |
| Brandon Ingram | -0.3 | -0.1 | -0.1 |  |  |  |  |
| Jakob Poeltl | +0.3 | +0.1 | +0.1 |  |  | -0.001 | +0.001 |

Games stayed ours (A2). Yahoo's games cuts — Ingram 55, Raynaud 65, Kuzma 65, Knueppel 70, Filipowski 65 — and Hashtag's (Kawhi 58 to 50, Porziņģis 42 to 30) are not applied; Ingram and Raynaud already carry risk tags, Porziņģis is on the DO NOT DRAFT list.

## 5. Kawhi Leonard and Anthony Davis back to ×0.78

Version 66 moved both from `inj-risk` to `inj-risk-mild` (×0.85) as a deck tag only — the kit's games were not touched (kit GP 60 and 55 throughout). `revert_mild.py` puts the leading tag back to `inj-risk` with the dated reason inside it; asserted: exactly those two rows change, only their notes, `hoops.availability` = 0.78 for both; a second run changes nothing. Kyrie Irving and Damian Lillard stay on the lighter tier. The kit board is not affected (the kit models health through games).

## 6. The kit board — the final 180

`rank_engine.py` on the lock lines: 200 players from 313 projected; provenance PASS; `test_rank_engine.py` OK. The top 180 holds the same 180 players as this morning's board (none in, none out). 116 change place; mean move 2.59 places; 10+ for 7:

| player | this morning | the lock |
|---|---|---|
| Rui Hachimura | 168 | 145 |
| Egor Demin | 152 | 136 |
| Ivica Zubac | 78 | 64 |
| Brandin Podziemski | 107 | 94 |
| Tari Eason | 118 | 131 |
| Coby White | 103 | 92 |
| Scotty Pippen Jr. | 136 | 147 |
| Matas Buzelis | 80 | 74 |
| Cason Wallace | 91 | 85 |
| Zach LaVine | 109 | 104 |
| Cedric Coward | 112 | 117 |
| Draymond Green | 151 | 156 |

The full table is `lock-2026-10-14/final-180-kit-2026-10-14.md` (rank, team, positions, games, line, percentages, value, move).

## 7. Deck build and publish

- `hoops.py freshness --stamp --pool-changes` (the lock); colophon: a lock paragraph at the head of the Data section, the Kawhi/Davis sentence of 10/13 marked as reverted, the Market sentence on the 10/14 paste.
- `build_deck.py`: planes: 315 shared · kit-only 10 · deck-only 20 · team 0 · exclusion 0 · drift 0 · propagation 0; market: yahoo-2026-10-14.csv — priced 302/335 rows, 0 days old; built 335 players, pool d1d74587c5db, injection round-trip OK, no waiver, "safe to publish" (first build passed).
- Chain on the built page (sha256 e68a85a5305f): `check_parity.py` PARITY: EXACT MATCH; `test_card.py` CARD: all 103 cases passed; `test_draft.py` all 65; `test_gates.py` all 54; `full_dom_check.mjs` 145 assertions, 0 failed, 0 page errors, pass true; `repeat_market_check.py` 29 of 29 mocks replayed; 12 FLAGGED, 8 near miss(es); `identity_check.py` POINTS IDENTITY: 0 player(s), 0 line(s) more than 1 from their own shooting (200 deck and 200 kit lines checked); `range_check.py` RANGE CHECK: 4 player(s) with 4 cell(s) outside every reference (147 of the top 150 checkable).
- Published to the standing URL (https://claude.ai/code/artifact/190e2c13-a19c-4239-8085-73230ef4eae0) after a fresh read of Version 68 (id 1791993066-d8ff): Version 69, id 1792001219-01f3; the served file carries the built page byte-for-byte at offset 349. (The service numbers this publish Version 69: this afternoon's price-only build, which the session's commits had called Version 69, was never published — the lock superseded it — and the lock build is labelled ‘Version 70’ in the deck commit messages. The test chain ran in two passes: the first stopped at the session's 30-minute background limit after parity, card and draft tests passed; the remaining checks ran on the same bytes, sha256 e68a85a5305f.)

## 8. Gates (2026-10-14, the lock)

| gate | evidence |
|---|---|
| `market/yahoo_market.py 2026-10-14 --as-of 7438f8c` | TRANSCRIPTION GATE PASS (I1–I7); 350 parsed, 186 with ADP; I7 306 of 350; JOIN 306 matched, 19 accepted absences; GATE PASS |
| `market/hashtag_pdf_market.py 2026-10-14 --as-of 03a8704` | 200 rows, TRANSCRIPTION GATE PASS; 1 Hashtag-only name, none a spelling variant; GATE PASS |
| `report/check_derived.py` | DERIVED: all 29 dated artifacts reproduce byte-for-byte from their pinned inputs |
| `preblend.py` / control / `blend_lines.py` (lock) / `blend_apply.py` ×2 | PASS / 241 of 241 identical / 0 problems / PASS, second run no change |
| `revert_mild.py` ×2 | 2 rows, both at 0.78 / 0 rows |
| `rank_engine.py`, `check_provenance.py`, `test_rank_engine.py` | 200 from 313; PASS; OK |
| `build_deck.py` (deck) | gates 1–7 + F8 pass, no waiver, 302/335 priced |
| `check_parity.py` / `test_card.py` / `test_draft.py` / `test_gates.py` (deck) | PARITY: EXACT MATCH / CARD: all 103 cases passed / all 65 / all 54; exit 0 each |
| `full_dom_check.mjs` (deck) | 145 assertions, 0 failed, 0 page errors, pass true |
| `repeat_market_check.py` (deck) | 29 of 29 mocks replayed; 12 FLAGGED, 8 near miss(es) |
| `identity_check.py` / `range_check.py` (deck) | POINTS IDENTITY: 0 player(s), 0 line(s) more than 1 from their own shooting (200 deck and 200 kit lines checked) / RANGE CHECK: 4 player(s) with 4 cell(s) outside every reference (147 of the top 150 checkable) |
| `report/check_report.py`, deck `--check-report` gates | run on this file after writing (PR body) |
| artifact publish | Version 69, id 1792001219-01f3, byte-verified at offset 349 |

## Watchlist

- Yahoo's and Hashtag's games cuts (§4) — not applied; the draft page's tags carry health.
- Anfernee Simons lost his Yahoo ADP (market rank 210 now).
- Lonzo Ball listed by Yahoo at CLE with NA (one outlet; the pool holds him unsigned).

## Open-item receipts

| player | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the morning pull, same day (`after-report-2026-10-14.md`, receipts dated 10/14) | all held as of this morning; today's pastes add letters and games only — Ingram O (Yahoo ADP 73.5, GP 55); Porzingis Q (Yahoo ADP 104.6, GP 55); Leonard unlettered (Yahoo ADP 34.2, GP 59); Mathurin unlettered (Yahoo ADP 115.9, GP 65); Rollins unlettered (Yahoo ADP 74.0, GP 69); Hashtag 10/14 has Kawhi at 50 games and Porziņģis at 30; Thomas, Ivey, Sochan, Dillingham absent from Yahoo's 350; Lonzo Ball listed at CLE with NA (one outlet, no row change) |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 e68a85a5305f), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 29 of 29 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-14.csv`, Hashtag `hashtag-2026-10-14.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-14.csv`, `hashtag-2026-10-14.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 29 of 29 | 44 | 111 | 63 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 21 of 29 | 32 | 67 | 58 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 12 of 29 | 101 | 182 | 100 | 125 | 148 | 155 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| Brandin Podziemski | 11 of 29 | 93 | 146 | 74 | 102 | 114 | 132 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 11 of 29 | 107 | 138 | 182 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| John Collins | 11 of 29 | 73 | 117 | 105 | 72 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 8 of 29 | 92 | 179 | 89 | 117 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 7 of 29 | 6 | 32 | 15 | 24 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Jaden McDaniels | 6 of 29 | 62 | 90 | 42 | 67 | 86 | 59 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 5 of 29 | 114 | 139 | 122 | 130 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Immanuel Quickley | 5 of 29 | 67 | 94 | 65 | 73 | 79 | 84 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Keegan Murray | 5 of 29 | 83 | 142 | 82 | 94 | 102 | 85 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (18 mocks, value 9, market 18); Derrick White (14 mocks, value 27, market 45); Lauri Markkanen (14 mocks, value 21, market 37); Tyrese Haliburton (12 mocks, value 7, market 12); Kel'el Ware (8 mocks, value 57, market 77); Tyler Herro (8 mocks, value 51, market 69); Tyrese Maxey (8 mocks, value 5, market 9); Karl-Anthony Towns (5 mocks, value 12, market 15).

## Bounds

- Out of scope by design: games and minutes (A2) — the outlets' games are listed, not blended; teams and placements; the deck's other injury tags.
- The blend's five outside lines: only Yahoo's and Hashtag's are today's; RotoBaller, FantasyPros and the cards are 10/13 (no newer files were supplied).
- The Haliburton plan research (separate report) was run on Version 68's lines; the lock moves its names by 1–5 places on the kit board (Towns 13 to 14, Derrick White 25 to 26, Wagner 35 to 38, Anunoby 34 to 31, Jerome 43 to 47) — its turn lists stand as scouting, not re-run.
- Did not check: the card's 🎯 at your turns in past rooms on Version 69 (a re-grade); not load-bearing for publishing the lock.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-1014-3 | the lock paste | applied — Version 69 is priced on it |
| D-1014-12 | re-blend on today's Yahoo and Hashtag | applied at your call ("synergize … and lock") |
| D-1014-13 | the outlets' games cuts (Ingram 55, Raynaud 65, Kuzma 65, Knueppel 70, Filipowski 65; Kawhi 50 on Hashtag) — (a) games stay ours; (b) apply | (a) |
| D-1014-15 | Kawhi Leonard and Anthony Davis back to ×0.78 | applied at your call |
| D-1014-1..11, D-1013-*, earlier | carried | carried |

## Provenance

- Inputs: the owner's Yahoo paste and Hashtag PDF (chat, 2026-10-14), the pinned 10/13 RotoBaller, FantasyPros and cards files, this morning's blend record `blend/out/lines_blend_2026-10-14.json`, the kit at 7bf829d and the deck at main 85ad6ea (Version 68).
- Commits: kit 8380ff7, 023372a, 7438f8c (Yahoo raw and parser), 03a8704 (Hashtag raw), the lock commit; deck af91b23 (Version 69) and the merge of main 462fa1b.
- Re-verify: `BLEND_SET=lock python3 report/blend/tools/blend_lines.py --deck <pre>/players.csv --kit <pre>/projections-2026-27.csv --out x.json` after `preblend.py`; `python3 report/check_derived.py`; read the standing URL and compare at offset 349.

## In plain language

**What I did.** I took Yahoo's and Hashtag's projections from today and folded them into our lines exactly the way you approved this morning — every category is the average of our line and the five outside lines, with today's Yahoo and Hashtag replacing yesterday's. I started from our own lines, not this morning's already-averaged ones, so nothing got counted twice; and I checked that running the old sources through the same steps gives back this morning's lines exactly.

**What moved.** Not much, because Yahoo and Hashtag barely moved: 54 players' lines changed, mostly by a few tenths. Hachimura (+1.3 points), Kuminga (+0.9), LaVine, Santos and Kyrie went up; Hunter (−1.0), Pippen Jr. and Wells went down. Games, minutes and injury tags stayed ours; Kornet kept his restored line.

**Kawhi and Davis** are back at the full 0.78 injury discount on the draft page, as you asked. Kyrie and Lillard stay at 0.85.

**Your final 180.** Same 180 players as this morning; 116 shifted a few places, seven by ten or more (Hachimura 168 to 145 the biggest). The full list is in `final-180-kit-2026-10-14.md`.

**Locked.** The draft page is Version 69, priced on your 10/14 Yahoo paste, every check passed on the exact bytes that are published.
