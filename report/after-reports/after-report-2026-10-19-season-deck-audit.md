# After-report — Season Deck audit: rostered players shown as free agents; Waivers tab removed; Trade Analyzer and Free-Agent Adder split; Status tab removed

Pull window: 2026-10-19 → 2026-10-19 — no pull; a fix to the deck's rendering join and its tabs.

**Owner request (2026-10-19 evening, verbatim):** "Please Audit season deck, as there are rostered players listed on the available free agent list (Jaren Jackson Jr, Cameron Johnson). Additionally, Let's remove the \"Waivers\" tab, as this would be the same is the Free Agents tab. Let's separate Trade Analyzer and Free-Agent Adder"

**Owner follow-up (same evening, verbatim):** "Thank you, and please proceed with removing the "Status" tab as well"

**Headline.** EVIDENCE: the deck joined the league rosters (the paste's spelling) to the season board (the kit's spelling) by exact string, so 8 rostered players were marked free agents: the two you named and six more. The join now runs the kit's own resolver (fold, alias table, unique suffix-free name) and halts the build on any unresolved or doubled name. All 165 rostered players resolve (161 on the board, 4 held off it); free agents on the board fell from 160 to 152. The brief's engine-graded waiver scan never had this fault: it uses the roster's spelling end to end, and its three suggested adds are all genuinely unrostered (verified). The Waivers tab is gone; the Trade Analyzer and the Free-Agent Adder are separate tabs; on your follow-up the Status tab is gone too, leaving 6 tabs. The audit went out as Season Deck Version 3 and the Status removal as Version 5 (Version 4 still carried two unused style rules), each byte-verified. Full kit suite 131 of 131, twice.

## 1. Roster changes

None. The deck proposes; nothing changed on either plane.

## 2. The audit, with its evidence

- **Cause.** `season_deck.py` matched `data/league_state.json` names to `report/season/board_<date>.json` names exactly. The league state carries the deck pool's spelling ("Jaren Jackson Jr.", "Cameron Johnson"); the season board carries the kit's ("Jaren Jackson Jr", "Cam Johnson"). Same root as the 10/13 repeat-name fix, a different join.
- **The eight misjoined players** (paste spelling → board row):

| rostered as | board row |
|---|---|
| Cameron Johnson | Cam Johnson |
| Darius Acuff Jr. | Darius Acuff |
| Jabari Smith Jr. | Jabari Smith Jr |
| Jaime Jaquez Jr. | Jaime Jaquez Jr |
| Jaren Jackson Jr. | Jaren Jackson Jr |
| Kevin Porter Jr. | Kevin Porter Jr |
| Michael Porter Jr. | Michael Porter Jr |
| Wendell Carter Jr. | Wendell Carter Jr |

- **Second symptom, same cause.** The trade picker's opponent lists were built from the same names, so these players were silently missing from their teams' lists (Jaren Jackson Jr. from Looking Cool Joker!). Rosters are now embedded in board spelling, with held players listed separately as off the board.
- **Other consumers checked.** The daily brief, its waiver scan, and the Jones/Holiday analysis all run on the deck pool, whose names are the roster's own: 165 of 165 rostered names resolve there exactly, and the three adds the brief suggested are not rostered. No other output carried the fault.
- **Fix, red first.** Four tests in `scripts/test_season_deck.py` (spelling variants resolve; rosters embedded in board spelling; an unresolvable rostered name halts; two names on one row halts) failed on the old join, then passed. The halt also caught a fixture defect: a rostered "Bench Guy" with no board row, which the old join ignored silently.
- **Independent cross-check.** A looser matcher (surname plus first initial, suffix-free) over the 152 remaining free agents found 5 look-alikes. Each is a different person whose rostered namesake is correctly owned: Jalen Smith / Jabari Smith Jr., Jaylin / Jalen Williams, Javonte / Jalen Green, Aaron / Andrew Wiggins, Kris / Keegan Murray.
- **Tabs.** Waivers removed. Trade Analyzer (my players out, an opponent's in) and Free-Agent Adder (my players dropped, free agents added, searchable) are separate tabs sharing one arithmetic function. Chromium at 1200px light and 400px dark: 0 px overflow, 0 script errors; searching "Jaren" or "Cam Johnson" in the Free-Agent Adder returns nothing; Looking Cool Joker!'s trade list shows Jaren Jackson Jr. Holiday-for-Washington reads ABOUT EVEN at net −0.09 on the page and in python.
- **Status tab removed.** It listed the 24 flagged rostered players with Yahoo letter, tier, availability and the dated receipt. The status feed still runs every morning: the letters still show on the Today tab's games table for your players, and tiers and availability still drive the lineup and the brief. What leaves the page is the other teams' letters and the receipt text; both stay in `data/status/status_<date>.json`. `test_panes_present` now also asserts the Status, Waivers and old Moves panes are absent (red on the pre-removal build, green after). A tab remembered as Status in a browser falls back to Today. Chromium on Version 5's bytes at 1200px light and 400px dark: tabs Today / Trade Analyzer / Free Agents / Board / Movers / Week, 0 px overflow, 0 script errors.
- **A miss of mine, fixed here.** PR #135 added the deck as the morning runner's sixth step but ran only the deck's own tests. Two tests in `scripts/test_morning.py` still expected five steps with the brief last, so #135 merged with them failing. Both now expect six steps; the full suite is 131 of 131 on two runs.
- **Odds band.** The deck's odds keep the standing sweep's band: arena.TEAM_WEEK_SHOCK is FRAGILE: +3.4 / -2.3 title points (engine 259c630).

## Watchlist

- The resolver halts the morning build if a future roster paste brings a name it cannot place. That fails the morning run loudly rather than mislabeling a player; the fix then is one alias row in `report/market/build_market.py`.
- The simulator-graded waiver pairs that the Waivers tab showed remain in the daily brief and the morning report.

## Open-item receipts

Carried from the post-mortem report of the same day (no pull today; the rows are that report's):

Carried verbatim from the 10/14 league report (gated there on 10/15); not re-queried for this post-mortem (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| (this draft) | records only; no web research and no roster pull | Yahoo's 156 names resolve to the lock pool 156 of 156; Yahoo's NBA team agrees with the pool's at all 156 |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this grade (did not check) |

## Repeat-name market check

Carried from the post-mortem report of the same day (no refresh today):

Carried verbatim from the 10/14 league report; the same 33 rooms, not replayed again here (did not check).

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 beb243ef57af), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 33 of 33 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-14.csv`, Hashtag `hashtag-2026-10-14.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-14.csv`, `hashtag-2026-10-14.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 32 of 33 | 44 | 111 | 63 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 23 of 33 | 32 | 67 | 58 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 14 of 33 | 107 | 138 | 182 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 12 of 33 | 101 | 182 | 100 | 125 | 148 | 155 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| John Collins | 12 of 33 | 73 | 117 | 105 | 72 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Brandin Podziemski | 11 of 33 | 93 | 146 | 74 | 102 | 114 | 132 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 10 of 33 | 6 | 32 | 15 | 24 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 10 of 33 | 92 | 179 | 89 | 117 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Jaden McDaniels | 7 of 33 | 62 | 90 | 42 | 67 | 86 | 59 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 6 of 33 | 114 | 139 | 122 | 130 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Immanuel Quickley | 5 of 33 | 67 | 94 | 65 | 73 | 79 | 84 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Keegan Murray | 5 of 33 | 83 | 142 | 82 | 94 | 102 | 85 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (18 mocks, value 9, market 18); Derrick White (17 mocks, value 27, market 45); Lauri Markkanen (15 mocks, value 21, market 37); Tyrese Haliburton (13 mocks, value 7, market 12); Tyrese Maxey (11 mocks, value 5, market 9); Kel'el Ware (10 mocks, value 57, market 77); Tyler Herro (9 mocks, value 51, market 69); Karl-Anthony Towns (8 mocks, value 12, market 15); Miles Bridges (5 mocks, value 96, market 98).

## Bounds

**Out of scope by design.** The board, lines, rosters, and engine are unchanged. The Free-Agent Adder remains a z-sum screen, not the simulator.

**In scope and unverified.** None: every consumer of the roster join named above was checked.

## Decision sheet (owner disposes)

| id | decision | recommended |
|---|---|---|
| D-SDA-1 | the brief's simulator-graded pickups (the old Waivers content): (a) leave them in the brief and the morning report only; (b) show them as a small card atop the Free-Agent Adder tab | (a) |

## Provenance

- Session: Claude Code (claude.ai/code), 2026-10-19 evening, kit branch `claude/market-data-workorder-mnfi2b` on main 17b320b. Records: `report/season/deck_record_2026-10-21.json` (join block), evidence in `season-deck-audit-2026-10-19/`. Re-verify: `python3 scripts/season_deck.py --date 2026-10-21`, then read the join block; `python3 -m unittest scripts.test_season_deck`.

## In plain language

The league paste spells a few names differently from our board (a period after Jr., Cameron versus Cam), and the deck compared them letter for letter, so eight rostered players looked free. It now uses the same name matcher the rest of the kit uses and refuses to build if any rostered name cannot be placed. Your morning brief's pickup suggestions were never affected. Waivers and Status are gone, and trades and free-agent pickups each have their own tab. Injury letters for your players still show on the Today tab.
