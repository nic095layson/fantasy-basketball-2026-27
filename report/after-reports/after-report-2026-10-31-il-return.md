# Title odds if IL players return: a scenario section beside the headline (owner go, 2026-10-31)

Pull window: 2026-10-31 → 2026-10-31 (no pull: the 10-31 morning records on season/daily 44841fe read only; kit main 0093486, deck main 55d8e3f, deck branch aa470f8).

**Method up front.** The owner's words: "keep main title odds with current roster as is, but take espn injury return as a variable title odds in a separate section. Players returning from injury aren't a sure fire and I want to keep caution in keeping them as a constant when in reality it is a variable." The headline keeps D-IS-8 untouched. A new section runs the same simulator with every IL player league-wide counted from the Yahoo week of ESPN's expected return, slipped 0, 2 and 4 weeks, and never (= the headline). Inputs: the 10-31 league state (as of 2026-10-31), the 10-31 ESPN pin, the 10-31 season pool, seeds 2026 and 2027 × 10,000 seasons, real schedule with week 1 final. Roster-room rule (assumption A1): on a return the team's lowest-value active player (the brief's own "weakest" rule) leaves for the rest of the season. EVIDENCE marks what a run or read showed; INFERENCE what is derived.

**Verdict: built and tested, nothing merged. On today's inputs the range is on time 29.9 · +2 wk 29.9 · +4 wk 29.6 · never 14.3 (± 0.5 each): whether the IL players come back moves the title odds by about 15 points; when they come back, inside a month, barely moves them. The roster-room rule is FRAGILE at +13.4 points and is the owner's call.**

## 1. Research answers (§4 of the build prompt)

| question | answer | basis |
|---|---|---|
| Engine path | **Option B, deck repo**: `league_sim.py` reads an optional `from_week` / `to_week` on a pick; the team's weekly model is rebuilt only where the active roster changes; playoffs on the final week's roster. The kit passes windows through `co_gm.run_league_sim(..., windows=)`. Option A (kit only) cannot work: the simulator builds one static model per team and the kit cannot express a week-indexed roster without it. This session can push to the deck repo (dry run, then the branch). Headline path byte-identical: with no window the draws are unchanged in order. | EVIDENCE: deck `arena/test_windows.py`; old vs new simulator on `draft_state_100`, 300 seasons, seed 7: teams block byte-identical; the 10-31 brief re-run with the new code: title, playoffs, waiver_top, lineup, streaming, absent_from_sim all identical, the only new key `il_return` |
| Return-date uncertainty (a) | ESPN revises its dates **only later**: 34 revisions across the 6 pins (10-28 to 10-31), 34 later, 0 earlier; median +2 days, mean +5.6, max +63 (one long injury re-dated). | EVIDENCE: the 6 `espn_injuries_*.json` pins |
| Return-date uncertainty (b) | 16 players had an ESPN return date on or before 10-30 in the first pin and a later game on file: first game 0.75 days after the date on average (median 0). **Every one was a short Out or Day-To-Day; no long-term IL return has happened yet**, so no distribution is fitted; the stated grid stands. | EVIDENCE: the pins against `data/actuals` 10-16 to 10-30 |
| Roster room | A returning IL player needs an active spot. Rule A1 above; with it off the returning player joins a 14-man active roster, which the 10-29 report already showed the simulator rewards heavily. Named as the owner's method choice, registered as `il_return.ROOM_RULE_ON`. | EVIDENCE: §3 sweep |
| Scope | All 12 teams' IL players return in every grid row (22 players today, 2 on most teams). Seat 10 only, on time: **34.1** against 29.9 all-teams, the +4.2 bias the prompt predicted; reported, not shipped. | EVIDENCE: `il_return_2026-10-31.json` |
| Edge cases | Day-To-Day on IL: ESPN's date as given (Sengun, Sheppard: this week). No ESPN row (Naji Marshall): never, named in the section. A date before the run's date: the run's week. A week past the regular season or outside the calendar: never. A player the pool lacks: absent, as the headline leaves him. | EVIDENCE: `test_il_return.Dates` (6 cases), the 10-31 section lines |

## 2. The scenario table on today's inputs (EVIDENCE: `il-return-2026-10-31/il_return_2026-10-31.json`)

| scenario | every IL player league-wide… | title (2026 / 2027) | mean | playoffs |
|---|---|---|---|---|
| never (the headline) | never returns (D-IS-8) | 14.25 / 14.30 | **14.3** | 96.9 |
| on time | returns the week of ESPN's date | 29.49 / 30.27 | **29.9** | 99.6 |
| late +2 wk | 2 weeks after | 29.99 / 29.74 | **29.9** | 99.6 |
| late +4 wk | 4 weeks after | 29.43 / 29.71 | **29.6** | 99.3 |
| seat 10 only, on time (not shipped) | only Haliburton and Leonard return | 33.95 / 34.18 | 34.1 | 99.9 |

- Sampling error ± 0.48 per figure (2 runs × 10,000); the two seeds agree within 0.8 on every row.
- **Two error bars.** Sampling ± 0.5. Structural: the standing sweep's bands apply to every title share here (TEAM_WEEK_SHOCK FRAGILE +2.7 / −4.2; weekly_availability FRAGILE −5.4 / +3.7 / +0.4 / −0.5), and the new rule's band below.
- INFERENCE on the flat grid: the title is decided in the playoffs, which every scenario plays with the full roster, and the slip only trades a few regular-season weeks in which the rivals' stars also return. "Whether" is the variable that matters; "when, within a month" is not.
- The brief's line reads: "**If IL players return** (scenario range, not a forecast; ESPN dates of 2026-10-31, all 12 teams, 22 IL players): on time 29.9% · +2 wk 29.9% · +4 wk 29.6% · never = headline 14.3%. Error ± 0.48 each. Returns are uncertain; the headline counts the current roster." followed by one line per team, seat 10 first (Haliburton 11-13 wk 4; Leonard 11-23 wk 6).

## 3. Red team (EVIDENCE: `il-return-2026-10-31/room_rule_and_blend.json`, `rt_il_return.json`; attack A-10)

| constant | status | moved | effect on the on-time title |
|---|---|---|---|
| `il_return.SLIPS` (0 / 2 / 4 / never) | declared_band | it is the band: every row shown | 29.9, then 29.6, then 14.3 |
| `il_return.ROOM_RULE_ON` | declared_band | off (returning players join a 14-man roster) | **+13.4: 29.9 to 43.3** (and +4 wk 29.6 to 43.4). FRAGILE |
| `il_return.BLEND_WEIGHTS` (0.4 / 0.3 / 0.2 / 0.1) | uncalibrated, D-ILR-1 | never 0.5 gives −6.2; never 0.0 gives +1.6; uniform gives −2.4 | FRAGILE on the blend (28.3), so **the blend is not shown**; the record carries it |

- **ROOM_RULE_ON is FRAGILE: +13.4 (rule off); on-time 29.9 ± 0.5 within that band.** With the rule off the figure (43.3) is within a point of `include_il` (42.2): a 14th active player is worth more than the returning star's timing, as the 10-29 report found (+21 then on a 14-man roster).
- Known answers (A-10, PASS): never = the brief's headline to the digit (14.25 / 14.30); every IL player back in week 1 with the rule off = `include_il=True` exactly (identical windows, identical draws); back after the last week = the headline exactly; seat 10 monotonic within error (29.88 ≥ 29.86 ≥ 29.57 ≥ 14.28).
- Fingerprint: the engine files (hoops.py, arena.py) are at 95ebade; the window change lives in `league_sim.py` at deck aa470f8, which the fingerprint rule does not cover. Flagged, not changed here (scope-fence): the owner may want `league_sim.py` added to the engine files.
- Not done: a separate-attacker re-implementation of the window logic (NOT-ATTEMPTED, cost); the three exact identities above are the specification's boundary cases and stand in for it. Not load-bearing for the range, which rests on runs of the engine itself.

## 4. Tests (§7)

| test | result |
|---|---|
| headline byte-identity (same inputs and seeds, before vs after) | PASS: 10-31 brief re-run, every existing field identical; old vs new simulator identical on the deck's test state |
| week 1, rule off = include_il | PASS, exact |
| after the last week = headline | PASS, exact |
| seat 10 monotonic | PASS within error (the two late rows are flat, 0.02 and 0.3 apart) |
| two seeds | PASS: spread 0.05 to 0.78 on every row |
| suites | kit: every test file OK (test_il_return 8 new); deck: test_windows 4 new, test_schedule, test_season_cv, test_pool, test_patches OK |
| deck render | the Today tab's Odds card draws the four-row faded table under the tiles; the title tile reads 14.3% (the headline), unchanged |

## 5. Bands quoted

Every title share above carries the standing structural band (season sweep 2026-10-26, real schedule):
- **TEAM_WEEK_SHOCK is FRAGILE:** +2.7 (no shared games shock (0.0)) / -4.2 (shared games shock doubled (0.12)).
- **weekly_availability is FRAGILE:** -5.4 (no in-sim injury discount (risk 0.88 like healthy)) / +3.7 (harsher risk tier (0.65)) / +0.4 (healthy players play 0.95 of games) / -0.5 (healthy players play 0.80 of games).
- The section's own: **ROOM_RULE_ON is FRAGILE:** +13.4 (rule off).

## 6. Open decisions (the owner's; options, recommended first)

1. **Engine path**: (a) Recommended: the deck-repo window change (draft PR open), kit-only is not possible without it; (b) a kit-only approximation that scales a returning player's season availability by the share of weeks he plays, labelled an approximation (not built).
2. **Roster-room rule**: (a) Recommended: lowest-value active player leaves from the return week, as run; (b) rule off, the returning player joins the roster as a 14th man (+13.4, the simulator's known inflation); (c) a named drop list the owner supplies per team.
3. **The blended figure**: (a) Recommended: not shown (FRAGILE on its weights); (b) shown with its band beside it.
4. **When the section turns on**: (a) Recommended: a non-fatal morning step before the brief from the next merge, so the section appears daily; (b) on request only (the script exists, the brief draws the section whenever a record for the day exists); (c) after the first long-term return is observed so the grid can be checked against one real case.

Runner impact: none as built (no morning step added; option 4a would be code-only).

## 7. Bounds

- Out of scope by design: changing the headline, any line, tag, roster or engine constant; the mixed per-player draw inside one simulation (the windows are fixed per run; a mixed scenario would need a per-season random window).
- In scope and unverified: no long-term IL return has happened yet, so the grid's realism is unmeasured; the "team games" of the room rule's removed player are not tracked (he simply leaves). The deck-repo PR is open and unmerged; the kit PR's section draws only when a record exists, so nothing shows until the owner picks 4a or runs the script.

## Watchlist

- The first long-term IL return (Nurkic 11-04, Claxton 11-04, Knueppel 11-02, White 11-02 are the first ESPN dates): the date against the first box-score game, for the record.
- After the deck PR merges: the kit's `co_gm.run_league_sim` windows need the deck at or past aa470f8; before that a windowed run is refused by the old simulator's state reader (unknown pick keys are ignored, so it would silently count the player all season). The kit PR must merge after the deck PR.

## Open-item receipts

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward the same way the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (`after-report-2026-10-21-pickups-file.md` §1) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck 366d3ca (this PR changes no deck file), checked today, the same page the 10/22 day report replayed. Its table stands, carried here verbatim from the day report.

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
