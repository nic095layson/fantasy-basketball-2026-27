# The week preview carries a structural band and names the moves since its rosters (owner pick 2026-11-09, "Band + staleness")

Pull window: 2026-11-08 → 2026-11-09 (no pull: data/league_state.json, data/season/pool_season.csv and report/schedule at e0fb268 (11-08 morning), data/news/league_moves_2026-11-09.json at 85556cc, on season/daily, read only in a scratch worktree removed after; kit main 8f252a2, deck main e14cc42).

**Method up front.** The owner picked option 1 of the D1 after-report (`after-report-2026-11-09-week4-preview-gap.md` §3). Method parameters, stated before the build:
- **Band.** The preview re-runs its own matchup (`weekly_preview.preview`: the season pool, seeds 2026/2027, 10,000 matchups per seed) under each declared-band variant in the constants registry for `arena.weekly_availability` (4 variants) and `arena.TEAM_WEEK_SHOCK` (2), one at a time. Patches go through the deck's `arena/patches.py`, as the sweep applies them, and each patched attribute is restored after its run. The preview prints the P(win) range and each variant beside the seed spread.
- **Staleness.** On Mondays, a new non-fatal morning step adds one line to the week's preview naming the two teams' moves recorded after the preview's rosters date, from the `league_moves_*` records, the rosters day's afternoon record included. The forecast lines are never changed: they are the pre-registered ledger entry, and the band is not written to the ledger.

EVIDENCE marks what a run or read showed; INFERENCE what is derived.

**Verdict: built and tested. Re-rendered on its own 11-08 inputs, the week-4 preview reproduces 41.0% and now reads "Structural band: P(win) 37.5% to 44.2%". The 11-09 note names seat 3's IL moves (Dončić, Markkanen) and says the forecast does not include them.**

## 1. What changed (EVIDENCE: the diff, the suite)

- `scripts/weekly_preview.py`:
  - `structural_band()`, `moves_since()`, `stale_note()`.
  - `render_preview()` prints the band line ("The ± above is the seed spread only").
  - `main()`: adds the band to every preview (`--no-band` skips it), and `--stale-note DATE` adds the moves line. The ledger record leaves the band out.
- `scripts/morning.py` — Mondays: a "preview staleness" step (`weekly_preview.py --week <current> --stale-note <date>`), non-fatal, after the decision grades.
- Tests:
  - `test_weekly_preview.StructuralBand`: 6 variants, the engine restored, the band rendered.
  - `test_weekly_preview.Staleness`: moves after the rosters' date for the two seats only; the note added once with the numbers untouched.
  - `test_morning.PreviewStaleness`: Monday only.

Red first (EVIDENCE): 3 errors (`AttributeError: … no attribute 'structural_band' / 'moves_since' / 'stale_note'`) and 1 failure (no band line). One expected value in my own fixture was corrected before the code was written: the 0.80 / 0.95 healthy variants give 0.38 / 0.53, not 0.40 / 0.58.

## 2. The known answer (EVIDENCE: scratch worktree at e0fb268, the 11-09 moves record copied in)

| | before | after |
|---|---|---|
| Week-4 preview, P(win) line | 41.0% (±0.7 points) | 41.0% (±0.7 points), unchanged |
| Band | none | **37.5% to 44.2%**: no shock 38.6%; shock doubled 43.9%; risk like healthy 41.0%; harsher risk 41.0%; healthy 0.95 37.5%; healthy 0.80 44.2% |
| Moves since the rosters (11-09 step) | none | SNOWTIME WHITE WALKERS: added Jake LaRavia, Jaxson Hayes; dropped Luguentz Dort, Maxime Raynaud; to IL Lauri Markkanen, Luka Doncic; off IL Josh Hart. The forecast does not include them; the week card does. |

Cross-check: the no-shock variant (38.6%) equals the D1 decomposition's independent no-shock run on the same inputs (0.386).

INFERENCE: the band (6.7 points wide) is about 10 times the seed spread (±0.7). The two "risk" variants do not move this matchup, because neither roster carried a risk-tier player on 11-08.

## 3. Bands quoted

The standing structural band for any title figure is the season sweep of 2026-11-02 (deck e14cc42): **weekly_availability is FRAGILE:** -2.6 (no in-sim injury discount (risk 0.88 like healthy)) / +2.2 (harsher risk tier (0.65)) / -0.2 (healthy players play 0.95 of games) / +0.0 (healthy players play 0.80 of games), mean of the two seeds. The weekly band above is the preview's own and is measured on P(win), not title share.

Runner impact: code-only. The Sunday step's command is unchanged and the preview simply gains the band; Monday gains one non-fatal step inside `morning.py`. No prompt edit.

## 4. Bounds

- Out of scope by design: the week card's own band; the calibration ledger's schema.
- In scope and unverified: the first live Sunday and Monday runs after merge. A run takes about 1.4 s for the seven previews (EVIDENCE: the scratch run).
## Watchlist

- 2026-11-09: week 3 on the accuracy card, the candidate's second graded week under D-ML-1.
- 2026-11-16: the week-5 confidence re-run; re-run `backtest.py` on about 20 games per player.

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
