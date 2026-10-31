# The decision log, slice 1: two ledgers and a grader on the board's line (owner 2026-10-31)

Pull window: 2026-10-31 → 2026-10-31 (no pull: the records on season/daily ccc984f read only, the 10-30 afternoon being the newest; kit main 2af1046, deck main 55d8e3f).

**Method up front.** The owner asked for a log that keeps score between the kit's roster advice and the owner's actual moves, and said "conduct red team test, and if gates pass and data is valuable, build it". The red team ran first on the build prompt's grader; it failed one part and passed the rest; the grader was redesigned and slice 1 built. EVIDENCE marks what a run or read showed; INFERENCE marks what is derived. The three method parameters below are stated here, before any grade, and are registered as uncalibrated with the decision that settles them.

**Verdict: the ledgers hold 11 brief rows, 2 session rows and 4 owner moves from the records on disk; the grader runs on all of them and reports every one PENDING as of today (the first window closes 2026-11-17). The box-score sum the prompt proposed as the verdict is not usable inside a season; the verdict reads the season board's blended line instead.**

## 1. Red team of the build prompt (EVIDENCE: `decision-log-2026-10-31/noise.json`)

Parameters: the 12 box-score files on disk (2026-10-16 to 2026-10-29), the 10-30 season pool and the 10-30 season board; players with 5+ games (196 players, 1,088 game residuals). Per-game z per category on the pool's per-game mean and sd, percentages weighted by attempts.

| attack | question | result | status |
|---|---|---|---|
| inputs on file | is every record the log needs written daily? | briefs, league moves, box scores and the season board exist for every day since 10-20 (10-16 and 10-19 box files too) | PASS |
| join | does a mechanical join find the owner's move from a recommendation? | the 4 seat-10 moves on disk resolve to exact / add_match_drop_differs / drop_match_add_differs / unrelated with no hand input (`moves.jsonl`) | PASS |
| box-sum verdict | can a ±0.5 z line on summed box-score z resolve a pair in 28 days? | per-game z noise sd **6.19**; a weekly sum (3.5 games) has sd 11.6; about 600 games per player to put 0.5 z at two standard errors | **FAIL** |
| scale agreement | does the box-score scale say the same thing as the board? | corr(mean per-game z, board z_adj) **0.81** over 194 players | PASS (the board's line is the right scale) |
| recorded-at-time | can a row be written after the result? | brief rows refuse a repeated day; session rows are never edited (a correction supersedes); moves rows carry the record file | PASS |

- The session's first inline pass quoted a noise sd of 3.65; that pass was not pinned and its scale is not recoverable, so the pinned record above (6.19) is the figure this report rests on. Both say the same thing: a box-score sum cannot be the verdict.
- INFERENCE: the per-game noise is dominated by the percentage categories on low-attempt nights (a 0-for-3 night is a large negative impact z), which is the same reason the kit's lines blend games into a season line instead of reading them raw.

## 2. What was built (EVIDENCE: the suite, every file OK; `decision_grade.py --dry-run` on the records)

| piece | file | what it does |
|---|---|---|
| recommendations ledger | `data/decisions/recommendations.jsonl` | the brief's top waiver pair, one row per day, `kind: hold` when no pair is positive; appended by the morning run; a repeated day is refused |
| session ledger | `data/decisions/session.jsonl` | advice given in chat, written by the session in the same turn; a separate file so a session's branch and the Runner's branch never append to the same ledger (the only writer of each file is one branch) |
| moves ledger | `data/decisions/moves.jsonl` | every seat-10 move the league-moves records show (both phases), joined to the newest recommendation in its horizon; a move the afternoon and the next morning both see is one row |
| grader | `scripts/decision_grade.py` | per recommendation: window = 28 days from the matched move (or the recommendation); grade = add's z_adj minus drop's on the newest season board at the window's end; owner's pair against the kit's when the drop differs; box-score games and totals beside, never inside, the verdict; final rows append to `report/decisions/grades.jsonl` with input sha256s; `scorecard.md` regenerated |
| morning wiring | `scripts/morning.py` | "decision log" right after the brief every day; "decision grades" on Mondays; both non-fatal |
| registry | `scripts/redteam/constants_registry.json` | WINDOW_DAYS 28, LINE 0.5, MIN_GAMES 10 as uncalibrated, decision D-DL-1 |
| tests | `scripts/test_decision_log.py` (12), `test_morning.DecisionLog` (1) | red-first: duplicate day refused, the join's five answers, pm/am repeat is one row, games change the totals and never the verdict, open window and under-10 games stay PENDING, the same window is never graded twice |

Method parameters (D-DL-1, the owner's to change before the first grade lands on 2026-11-17, a Tuesday, so the Monday 2026-11-23 run writes it):

| parameter | value | basis |
|---|---|---|
| window | 28 days from the move | the prompt's default: long enough that a 3-game start does not decide it, short enough that the role at the time still applies (INFERENCE, not fitted) |
| verdict line | ±0.5 z_adj on the window-end board | the prompt's line, moved from the box-score scale to the board's; the board's z_adj already carries the availability factor |
| game minimum | 10 games each, else PENDING | so a verdict never rests on a player who did not play; reported, never excusing |

## 3. The ledgers today (EVIDENCE: `data/decisions/*.jsonl`; dry run as of 2026-10-31)

| rec | source | kit said | owner did | board gap now (add − drop, z_adj) | status |
|---|---|---|---|---|---|
| R-2026-10-20-01, -21-01 | brief | Bobby Portis for Christian Braun | no matching move | −0.44 | PENDING to 11-17 / 11-18 |
| R-2026-10-22-01 | brief | Julian Champagnie for Christian Braun | 10-24: Gillespie in, Black and Braun out (drop match); 10-26: Champagnie in, Clowney out (add match, drop differs) | −0.02 | PENDING to 11-23 |
| R-2026-10-23-01, -24-01, -26-01 | brief | hold | | | HOLD (slice 2) |
| R-2026-10-25-01 | brief | Bobby Portis for Noah Clowney | 10-25: Clowney in (unrelated) | +3.65 | PENDING to 11-22 |
| R-2026-10-27-01 | brief | Bobby Portis for Collin Gillespie | 10-28 pm: Portis in, nobody out (add match) | +0.02 | PENDING to 11-25 |
| R-2026-10-28-01 | brief | Jalen Williams for Collin Gillespie | no matching move | +2.51 | PENDING to 11-25 |
| R-2026-10-29-01, R-2026-10-30-01 | brief | Cameron Johnson for Collin Gillespie | not yet on disk (see bounds) | +0.21 | PENDING to 11-26 / 11-27 |
| S-2026-10-29-01 | session | Jalen Smith for Collin Gillespie (+0.65 title) | the owner did not act | −0.87 | PENDING to 11-26 |
| S-2026-10-30-01 | session | Cameron Johnson for Collin Gillespie (+1.15 title) | Johnson in, Champagnie out (owner's word; the record lands with the 10-31 pull) | +0.21 | PENDING to 11-27 |

- **A finding the log made on its first day:** the simulator put Johnson for Gillespie at +1.15 title points, and the board puts the same pair at +0.21 z_adj. The two scales measure different things (a title share under the roster's needs, against a player's own line), and the grader reads the board. INFERENCE: a pair the simulator likes for roster fit can grade TOO CLOSE on the board; the season-end review should read both columns, and slice 2's matchup-replay grade is the one that speaks the simulator's language.
- The brief rows and the 4 moves rows are flagged `backfilled` (written today from the records on disk, not by the runs that made them); from the next morning run the ledgers are written by the run.
- Every row's `made_at` for a back-filled brief is today's time; the brief's own date is the row's `date`, which is what the window and the join use.

Runner impact: code-only (two new morning.py steps, both non-fatal; no prompt changes: the afternoon's moves are picked up by the next morning's step).

## 4. Bounds and open decisions

- Out of scope by design: the deck's Decisions tab and the matchup-replay grade (slice 2, after 10+ rows); grading hold rows (the free-agent-set-aside comparison); any feedback from the log into the engine this season.
- In scope and unverified: the 10-31 moves row for Johnson-in, Champagnie-out waits for the 10-31 morning record (the records branch ends at the 10-30 afternoon as of this report); the morning step will write it. No real grade has run (the first window closes 2026-11-17), so the grader's final-row path is exercised by its tests only.
- The three parameters are the owner's (D-DL-1); the default stands until changed, and a change before 2026-11-23 regrades nothing.

## Watchlist

- 2026-11-02 (Monday): the first "decision grades" step runs; expect 13 rows, all PENDING or HOLD, and `report/decisions/scorecard.md` on the records branch.
- 2026-11-23 (Monday): the first final grades (R-2026-10-20-01, -21-01, -25-01, -22-01).
- Every session that gives add/drop advice appends a session row in the same turn and quotes its id.

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
