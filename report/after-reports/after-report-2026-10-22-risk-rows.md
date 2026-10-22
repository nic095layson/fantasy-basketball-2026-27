# The seven risk-tagged rows at healthy-level GP — 2026-10-22

Pull window: 2026-10-21 → 2026-10-22. No league or market pull. One web check for De'Andre Hunter. Four pages were fetched and pinned in `data/source/hunter-2026-10-22/`, with each page's sha256 in its `manifest.json`:
- the ESPN and NBA.com stories of 2026-02-21;
- ESPN's live injury feed, at 00:18Z;
- Basketball-Reference's injury list, at 00:29Z.

**Owner's decisions** (2026-10-22, about 00:05Z, clicked):
- On the GAUNTLET report's decision 2 (`after-report-2026-10-21-gauntlet.md` §4): **"Per row (Recommended)"**. The option read: "Use the per-row proposal table in the report's §4. Each approved row then goes through a line change, kit rerun, board diff and gates."
- For the two rows that table left as "−6, or keep": **"Murphy 70 to 64"** and **"Wells 72 to 66"**.
- For De'Andre Hunter: **"Keep GP, research tag (Recommended)"**. The option read: "Games stay 70. I check two dated outlets on his eye and bring a tag proposal; no tag change without your word."
- On the evening status routine (decision 5): **"Disable it"**. Done at 00:00:23Z, before its 00:23Z run.

**What was analyzed.**
- Kit at `2b5bd1f` (main): `report/projections-2026-27.csv`, `report/rank_engine.py`, `scripts/season_lines.py`, `scripts/season_board.py`.
- Deck `80eecdf` (main), as the season scripts' sibling.

**Method, stated to you before the run.**
- **The change.** The D-1010-2 convention, "tag + kit GP −6", on six rows, by a script that asserts each old value first: `risk-rows-2026-10-22/apply_gp.py`.
- **The reruns.** The kit rank engine regenerates the preseason board.
- **The season tools.** `season_lines.py` and `season_board.py` run for 2026-10-21 in two scratch copies that differ only in the projections file: `risk-rows-2026-10-22/season_diff.py`.

**Headline.**
- **Six rows changed, nothing else.** `git diff` on the projections file shows exactly six lines, each in the GP column only. `apply_gp.py --check` passes; Hunter stays at 70.
- **Preseason board: 8 of 200 rows change, all small.**
  - Trey Murphy III stays #17 (zAdj 2.97 to 2.78).
  - Jaren Jackson Jr slips 42 to 43, and Zach Edey 50 to 52.
  - Three players move up one place as those two pass them.
  - Keegan Murray (#82) and Alex Sarr (#89) change only their GP cell, because the engine never shrinks a negative per-game value for absence.
  - Jaylen Wells is not on the top 200 before or after.
- **Season tools: no rank changes.**
  - The 10/21 season board changes five rows, GP and value only. Murphy's value is 3.00 to 2.80, Jackson Jr's 1.31 to 1.22, Edey's 0.93 to 0.87; Murray and Sarr change GP only. Every rank is unchanged.
  - `pool_season.csv`, which the brief, the week preview, the waiver scan and the title-odds simulation read, is **byte-identical**. None of those changes.
- **Hunter: the evidence points to removing his tag.** That is your decision (§4).

## 1. What changed

| player | team | tag (deck) | kit GP | basis |
|---|---|---|---|---|
| Alex Sarr | WAS | inj-foot-risk | 72 to 66 | the report's proposal; absent in preseason |
| Keegan Murray | SAC | inj-ankle-risk | 72 to 66 | the report's proposal; two preseason absences |
| Zach Edey | MEM | inj-ankle-risk | 70 to 64 | the report's proposal; "first season back" note |
| Jaren Jackson Jr | UTA | inj-knee-risk | 68 to 62 | the report's proposal; "first season back" note |
| Trey Murphy III | NOP | inj-shoulder-risk | 70 to 64 | your pick of the two options |
| Jaylen Wells | MEM | inj-toe-risk | 72 to 66 | your pick of the two options |
| De'Andre Hunter | SAC | inj-eye-risk | 70, unchanged | your call: keep GP, research the tag (§4) |

Every old value matched the GAUNTLET report's table, and the script would have stopped if any had moved. The projections file spells the Jazz forward "Jaren Jackson Jr", without the period the report used; the script uses the file's spelling.

## 2. The preseason board

`risk-rows-2026-10-22/board_diff.json`, from `board_diff.py`, compares `report/top-200-2026-27.md` at main `2b5bd1f` with the regenerated board.

| player | rank | GP | zAdj |
|---|---|---|---|
| Trey Murphy III | 17, unchanged | 70 to 64 | 2.97 to 2.78 |
| Paul George | 43 to 42 | 60 | 1.29, unchanged |
| Jaren Jackson Jr | 42 to 43 | 68 to 62 | 1.32 to 1.23 |
| Jalen Brunson | 51 to 50 | 72 | 0.91, unchanged |
| Tyler Herro | 52 to 51 | 70 | 0.89, unchanged |
| Zach Edey | 50 to 52 | 70 to 64 | 0.93 to 0.87 |
| Keegan Murray | 82, unchanged | 72 to 66 | −0.04, unchanged |
| Alex Sarr | 89, unchanged | 72 to 66 | −0.54, unchanged |

- **Gates on the regenerated files.**
  - `rank_engine.py` exited 0.
  - `check_provenance.py`: PROVENANCE GATE PASS.
  - `check_derived.py`: all 29 dated artifacts reproduce byte for byte.
- **Why each row's availability fell by the same amount.** The arithmetic predicted in the GAUNTLET report holds: 6/82 × 0.8 = 0.0585 of availability. The value falls only for the three rows with positive per-game value.

## 3. The season tools

`risk-rows-2026-10-22/season_diff.json`, from `season_diff.py --date 2026-10-21`. It ran twice, and the record was byte-identical (md5 1ce55695…).
- **`data/season/projections_season.csv`:** six lines differ, the six GP cells.
- **`data/season/pool_season.csv`:** identical. This is the deck-schema pool that `co_gm.py` reads for the brief, the week preview, the waiver scan and the title-odds simulation. Those carry the deck's own ×0.78 discount on all seven rows, as the GAUNTLET report noted, and nothing here touches them.
- **The 10/21 season board:** five rows change and no rank changes.

| player | rank | GP | value (adj) |
|---|---|---|---|
| Trey Murphy III | 16 | 70 to 64 | 3.00 to 2.80 |
| Jaren Jackson Jr | 44 | 68 to 62 | 1.31 to 1.22 |
| Zach Edey | 51 | 70 to 64 | 0.93 to 0.87 |
| Keegan Murray | 83 | 72 to 66 | −0.04, unchanged |
| Alex Sarr | 91 | 72 to 66 | −0.55, unchanged |

Jaylen Wells is in the season projections but below the board's listed rows. His GP cell changes in the projections file and nowhere visible.

## 4. De'Andre Hunter's tag

**What I checked** (2026-10-22, about 00:10–00:30Z):
- Three web searches.
- Four pages, fetched and pinned:
  - the ESPN story, `espn_story_47990846_2026-02-21.html` (sha256 f0e587ae…);
  - the NBA.com story, `nbacom_story_2026-02-21.html` (sha256 817c5b3a…);
  - ESPN's live NBA injury feed, `espn_injuries_2026-10-22T0018Z.json` (sha256 47e4b4c9…);
  - Basketball-Reference's injury list, `bref_injuries_2026-10-22T0029Z.html` (sha256 e4da8337…).
- The box-score notes already on the deck's row.

| what | source | date | finding |
|---|---|---|---|
| the injury and surgery | ESPN story; NBA.com story (both pinned) | 2026-02-21 | hurt Feb. 6 at the Clippers; retinal detachment repaired; "expected to make a full recovery" (both) |
| his preseason | ESPN box scores, on the deck row's notes | 2026-10-08, 2026-10-10 | started 10/8 (18 min); off the bench 10/10 (19 min) |
| today's injury report | ESPN injury feed; Basketball-Reference injury list (both pinned) | 2026-10-22 00:18Z and 00:29Z | ESPN: 73 entries across 26 teams. Basketball-Reference: 69 rows. Both list the same four Kings (Simmons, Monk, Cardwell, Raynaud); **Hunter is on neither** |

- **Three more pages appeared in the search results but could not be read.**
  - A Rotowire note, which the search summary dated 2026-09-28 and described as the GM calling him healthy (WebFetch: ENOTFOUND; curl: HTTP 000).
  - An SI piece from early October (WebFetch: ENOTFOUND; curl: HTTP 000).
  - NBC Sports Bay Area's February story (curl: HTTP 000).
  - None is cited; the manifest lists all three as unreachable.
- **EVIDENCE:** a February surgery with a full recovery expected (two outlets); two preseason games played; absent from two outlets' injury lists today.
- **INFERENCE:** the tag no longer describes a current risk. An eye repair is not the kind of soft-tissue or bone injury the "first season back" convention was written for.

**Proposal** (D-RR-1, not applied):
- **(a)** Remove the `inj-eye-risk` tag on the deck plane. His deck value then loses the ×0.78 discount, a deck PR with the usual chain. Kit GP stays 70.
- **(b)** Keep the tag by convention.
- *Recommended: (a).*

## 5. Errors and surprises, stated plainly

- **The "before" season board did not match main's committed 10/21 board byte for byte.** The single difference is Andre Drummond's movers line: committed "PTS 6.0 → 6.5, REB 7.8 → 8.3"; rerun "PTS 5.8 → 6.3, REB 7.9 → 8.4, FT% 0.622 → 0.612".
  - #155 changed Drummond's kit line after the 10/21 morning run wrote that board.
  - So I compared before and after on identical inputs (both reruns) rather than against the committed file.
- **The GAUNTLET report spelled one name differently from the projections file:** "Jaren Jackson Jr." versus "Jaren Jackson Jr". My first lookup missed him; the script uses the file's spelling.

## Watchlist

- **The six rows' tags stay on the deck.** Only the kit GP changed. The deck still discounts all seven at ×0.78.
- **D-PM-4 is untouched.** The board and the simulator still carry different injury-tier tables (`after-report-2026-10-21-council-fixes.md`). This change moves the kit board's input, not that gap.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| the 7 risk-tagged rows (GAUNTLET decision 2) | **DONE** for six rows by your per-row decision; Hunter kept at 70 | §1–§3 |
| Hunter's tag (D-RR-1) | **OPEN**: proposal (a) remove / (b) keep; your call | §4 |
| evening status routine (GAUNTLET decision 5) | **DONE**: disabled 2026-10-22 00:00:23Z on your word | the routine's record |
| calibration date 11/17, old routine (decisions 3 and 6) | **OPEN**, defaults stand (keep 11/17; keep the old routine until 10/28) | `after-report-2026-10-21-gauntlet.md` decision sheet |

The flagged-name receipts are carried forward from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21 (`after-report-2026-10-21-pickups-file.md` §1). The rest were not re-queried for this change (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this change (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (§1, `roster_drift_2026-10-21.json`) |

## Repeat-name market check

This change did not touch the draft-room deck page, which is still deck `80eecdf` (checked with `git -C ../yahoo-fantasy-basketball log -1`, clean tree, 2026-10-21), page sha256 6a5cefea4921. The GAUNTLET report replayed it today. Its table stands, carried here verbatim.

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 6a5cefea4921), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 33 of 33 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-14.csv`, Hashtag `hashtag-2026-10-14.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-14.csv`, `hashtag-2026-10-14.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 32 of 33 | 44 | 111 | 63 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 23 of 33 | 32 | 67 | 58 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 14 of 33 | 107 | 138 | 182 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 12 of 33 | 101 | 182 | 100 | 125 | 148 | 155 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| John Collins | 11 of 33 | 73 | 117 | 105 | 72 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 10 of 33 | 6 | 32 | 15 | 24 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 10 of 33 | 92 | 179 | 89 | 117 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Brandin Podziemski | 9 of 33 | 93 | 146 | 74 | 102 | 114 | 132 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 7 of 33 | 114 | 139 | 122 | 130 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Jaden McDaniels | 7 of 33 | 62 | 90 | 42 | 67 | 86 | 59 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Immanuel Quickley | 5 of 33 | 67 | 94 | 65 | 73 | 79 | 84 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Keegan Murray | 5 of 33 | 83 | 142 | 82 | 94 | 102 | 85 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (18 mocks, value 9, market 18); Derrick White (17 mocks, value 27, market 45); Lauri Markkanen (15 mocks, value 21, market 37); Tyrese Haliburton (13 mocks, value 7, market 12); Tyrese Maxey (11 mocks, value 5, market 9); Kel'el Ware (10 mocks, value 57, market 77); Tyler Herro (9 mocks, value 51, market 69); Karl-Anthony Towns (8 mocks, value 12, market 15); Miles Bridges (5 mocks, value 96, market 98).

**Structural bands, carried for the gate.** This report quotes no simulator figure. The standing sweep's bands are carried verbatim:
- TEAM_WEEK_SHOCK is FRAGILE: +2.7 (no shock) / −3.6 (shock doubled).
- weekly_availability is FRAGILE: −2.7 (no in-sim injury discount) / +0.5 (harsher risk tier 0.65) / −1.5 (healthy plays 0.95) / +1.0 (healthy plays 0.80).

## Decision sheet

1. **Hunter's tag (D-RR-1):**
   - (a) remove `inj-eye-risk` on the deck, which drops his ×0.78 there;
   - (b) keep it.
   - *Recommended: (a).*
2. **Calibration date** (GAUNTLET decision 3): 2026-11-17 stands unless you name another.
3. **The old morning routine** (decision 6): kept disabled until 10/28, then deleted, unless you say otherwise.

## Bounds

**Out of scope by design.**
- The deck's tags and its ×0.78 discount (Hunter's is proposed, not changed).
- The simulator's injury tiers (D-PM-4).
- Any GP other than the six rows.

**In scope and unverified.**
- The ranks the change gives on later days' season boards. Today's run is 10/21's inputs. The morning run regenerates the board daily once this merges; did not check later dates.
- Rotowire's 2026-09-28 note, SI's early-October piece and NBC Sports Bay Area's February story on Hunter: ATTEMPTED-FAILED (all unreachable from this session); not cited.

## Provenance

- **Produced by** session `session_01QjgeRdpDaWgSJmGKRG8fTU` on 2026-10-22, about 00:05–00:30Z.
- **Governors.**
  - plan-gate was loaded for this batch, and its full block was emitted before the first change.
  - adversarial-verify was loaded before delivery. Its pass found that the Hunter evidence rested on one outlet (ESPN) for both claims. NBA.com and Basketball-Reference were then fetched, and both agree. It also checked mechanically:
    - that only the GP column changed;
    - that every table cell here matches the two records;
    - that the availability step of 0.0585 holds at all three GP levels.
- **Re-verify.**
  - `python3 report/after-reports/risk-rows-2026-10-22/apply_gp.py --check`
  - `python3 report/after-reports/risk-rows-2026-10-22/board_diff.py`
  - `python3 report/after-reports/risk-rows-2026-10-22/season_diff.py --date 2026-10-21`
  - `cd report && python3 rank_engine.py && python3 check_provenance.py && python3 check_derived.py`

## In plain language

Six players with old injury tags were still projected for a full, healthy season of games. You chose to trim six games from each, as we already do for newly tagged players. On the draft-style board, Murphy, Jackson Jr. and Edey lose a little value, and two of them slip a place or two. On the season board nobody changes rank. Your lineup advice, waiver swaps and title odds don't change at all, because they read a different pool that already discounts these players.

For De'Andre Hunter, ESPN and NBA.com both reported in February that his eye surgery was expected to fully heal. He played both preseason games. He isn't on ESPN's or Basketball-Reference's injury list today. I suggest removing his risk tag, but nothing changes until you say so.
