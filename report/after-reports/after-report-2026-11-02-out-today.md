# Out-today banner on the Today tab, with the best bench swap (owner request 2026-11-02)

Pull window: 2026-11-02 → 2026-11-02 (no pull: the records on season/daily 00e71b6 read only, the 3 PM run's status file among them; kit main 2831565, deck main e14cc42).

**Method up front.** The owner saw Kyrie Irving Out on the afternoon page and asked for a flag at the top of the Today tab with the best bench player for his spot. The 3 PM status file reads Kyrie `O`, availability 0.0; the 5 AM file read `Q`, 0.5 (EVIDENCE: `status_2026-11-02_pm.json`, `status_2026-11-02.json`). Method stated to the owner before the build: the swap is chosen by the brief's own daily-fill value, the season-board z total, which reproduces the 5 AM lineup and bench exactly (EVIDENCE: `co_gm.daily_lineup` on board z totals with the 5 AM status gives the brief's 10 slots and 3 bench names, checked in this session). EVIDENCE marks what a run or read showed; INFERENCE what is derived.

**Verdict: the Today tab now opens with an "Out today" card naming each starter whose status reads Out and the best bench swap for his slot; on today's afternoon records it reads "Kyrie Irving (Util) is Out today, start Julian Champagnie at Util"; the morning records show no card; 3 red-first tests green, the deck suite green (167); nothing merged.**

## 1. What was built (EVIDENCE: the diff, the suite)

| change | where | test |
|---|---|---|
| `out_today(brief, avail, positions, values)`: each lineup slot whose availability today is 0, by the build's own status file (the 3 PM one in the afternoon build), with the highest-value bench player who has a game today, is not Out and is eligible for that slot (`co_gm.SLOTS`); if none fits, the lineup re-filled by `co_gm.daily_lineup` instead; two Outs never get the same swap | `season_deck.py` | `OutToday.test_the_swap_is_the_best_bench_player_with_a_game_who_fits_the_slot` (a higher-value bench player with no game is never the swap; a slot nobody fits gives the re-fill; Q is not Out) |
| The build passes it to the page as `out_today`; the Today pane renders it first, above every other card, with a note naming the status file (3 PM or 5 AM) and the value rule | `season_deck.py` | `OutToday.test_the_banner_is_the_first_thing_on_the_today_tab`, `OutToday.test_no_banner_when_no_starter_is_out` (browser read-back, 0 errors) |

Read-only: the card names a swap; it changes no lineup, roster, line, tag or constant. The 5 AM lineup card below it is unchanged.

## 2. Re-runs on the 11-02 records (EVIDENCE: two builds in scratch)

| build | top of the Today tab |
|---|---|
| afternoon (`--phase pm`, status 3 PM: Kyrie `O`) | "Out today · Kyrie Irving (Util) is Out today — start Julian Champagnie at Util"; SEASON DECK: PASS, 0 page errors |
| morning (status 5 AM: Kyrie `Q`) | no card; the brief's "Q, check before lock" line stands; SEASON DECK: PASS, 0 page errors |

Why Champagnie (EVIDENCE: board 11-02): the three bench players with a game today are Julian Champagnie (z total -1.17), Cameron Johnson (-1.44) and PJ Washington (-2.04); Util takes any of them, so the highest value goes in. INFERENCE: re-running the whole daily-fill rule with Kyrie Out also brings Champagnie in, with other starters shuffled between guard slots; the card names the one swap to make in Yahoo instead.

## 3. Bands quoted

No title share is quoted in this report. The standing structural band for any title figure on the deck is the season sweep of 2026-11-02 (deck e14cc42): **weekly_availability is FRAGILE:** -2.6 (no in-sim injury discount (risk 0.88 like healthy)) / +2.2 (harsher risk tier (0.65)) / -0.2 (healthy players play 0.95 of games) / +0.0 (healthy players play 0.80 of games), mean of the two seeds, as the 11-02 brief quotes it.

Runner impact: none. The morning and afternoon "season deck" steps pick the card up on their next build after merge; no new step, no prompt change.

## 4. Bounds and open items

- Out of scope by design: Questionable players (the brief's own "check before lock" line covers them); bench players added after the 5 AM run in an afternoon build (the swap pool is the brief's bench, as the lineup card above it is the 5 AM one); games already started.
- In scope and unverified: the first live render (the next afternoon run after merge that sees a starter Out).

## Watchlist

- Next afternoon run with a starter Out: the card appears on the published page above the matchup board.

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
