# After-report — 2026-10-01: the survival model against your own league (last season's pre-draft ranks, D40-2)

**Owner input (2026-10-01):** "Here are the Pre-draft yahoo rankings from LAST year" — Yahoo's
analyst column (Dan Titus, 10/16), 199 names with teams and positions.

**What this is.** The card's survival chips and the two-pick read price a player's chance of
still being on the board at your next turn from Yahoo's price alone, with parameters fit on
98 rows from two public mock rooms (2026-09-22). Your league is eleven named people, not
strangers. This report scores that model against the one draft those people actually ran:
last season's 156 picks (the room model of 8/04, re-verified 10/01) against the pre-draft
ranks the room displayed. Method and the decision rule were fixed before the numbers
(the plan gate in this session): rows are every ranked player still on the board at each of
your thirteen turns within 60 ranks of the pick, predicted to your next turn and observed;
league parameters would be proposed only if they beat the shipped ones by at least 0.01
Brier under leave-one-turn-out. Verification: `arena/mocks/league_survival.py` reproduces
`arena/results/league_survival_2025-26.json` from the two raw files; this file passes
`report/check_report.py`.

Pull window: 2026-10-01 → 2026-10-01 (owner upload; not a roster pull).

**Headline.** The shipped model holds in your league by the pre-stated rule (leave-one-turn-out
Brier 0.1417 for the best league fit against 0.1451 shipped, a gain of
0.0034, under the 0.01 bar) — but it is too pessimistic at every band: of the
481 rows it called quiet, 447 survived; of the 53 it called BUY NOW, 21 survived
(a two-in-five, not a one-in-ten); and of the 434 rows where the man sat 24 or more ranks below the
pick, 407 were still there at your next turn (94 percent). Your eleven draft close to
Yahoo's rank (median pick minus rank -1); the two who reach are Robby and Will. Nothing on the
card changes today; the decision sheet carries what could.

## 1. The inputs

[EVIDENCE: `arena/data/league_predraft_ranks_2025-26_raw_2026-10-01.txt` (md5 `a0416c192b65…`,
199 rows; the rank cell equals the row number on all 198 rows that carry one);
`arena/draft_boards.json` ["2025-26"], 156 picks with manager; `arena/results/league_survival_2025-26.json`]

- 154 of 156 picks match a ranked name (diacritics, dots and suffixes folded: Jokić, Dončić,
  P.J. Washington Jr., Bobby Portis Jr.). The two that do not are outside the top 199, not
  spelling: Nikola Jović (pick #139, Kyle); Jayson Tatum (pick #155, Cayas).
- Your turns last year (seat 4): #4, #21, #28, #45, #52, #69, #76, #93, #100, #117, #124, #141, #148.
- Rows scored: 719 (window 60 ranks); 365 in a 30-rank sensitivity window.

## 2. The model against the league

[EVIDENCE: `league_survival_2025-26.json` → `main`, `narrow`]

| statistic (60-rank window) | value |
|---|---|
| realized survival to your next turn | 0.821 |
| Brier, shipped parameters (k 0.30, floor 8) | 0.1450 |
| Brier, constant base rate | 0.1472 |
| Brier, best grid point (k 0.2, floor 16) | 0.1397 |
| leave-one-turn-out: best league fit / shipped | 0.1417 / 0.1451 |

Calibration of the shipped model on your league:

| predicted band | rows | mean predicted | realized |
|---|---|---|---|
| [0,0.2) | 53 | 0.09 | 0.40 |
| [0.2,0.4) | 69 | 0.31 | 0.52 |
| [0.4,0.6) | 116 | 0.51 | 0.74 |
| [0.6,0.8) | 240 | 0.71 | 0.88 |
| [0.8,1.0) | 241 | 0.89 | 0.98 |

Every band realizes above its prediction. In the public rooms the same bands read 0.33, 0.48,
0.57 (mock 51: 0.571), 0.88 and 1.00; your league sits higher still in the low bands. The
30-rank window — the rows nearest the pick, where the chips fire — is the honest caveat: there
the shipped model's Brier (0.2337) is worse than the constant base rate (0.2158),
so near the pick the price-only model's confidence is not earned in this room; the best grid
point there (k 0.5, floor 4) gains little (0.2281). The chips' words
are the right reading for this league: BUY NOW is "two in five survive here", TOSS-UP is a coin
flip, quiet is "nineteen in twenty".

## 3. How your eleven draft

[EVIDENCE: `league_survival_2025-26.json` → `league_profile`]

Pick minus pre-draft rank over the 154 matched picks: mean -3.6, median -1;
reaches of 24 or more slots 17, falls of 24 or more 11. By manager:

| manager | picks | mean pick − rank | reaches 24+ |
|---|---|---|---|
| Cayas | 12 | -2.1 | 2 |
| David | 13 | +4.3 | 1 |
| Hegi | 13 | -8.2 | 1 |
| JCo | 13 | -5.0 | 2 |
| John | 13 | -7.1 | 2 |
| Kevin | 13 | +8.6 | 0 |
| Kyle | 12 | +5.5 | 0 |
| Martin | 13 | -1.2 | 1 |
| Noah | 13 | -6.5 | 1 |
| Oblena | 13 | -1.0 | 2 |
| Robby | 13 | -16.5 | 3 |
| Will | 13 | -13.2 | 2 |

Positive means the manager takes men after their rank (lets value fall to them); negative
means reaching. You (+4.3) and Kevin (+8.6) take value as it falls; Robby
(-16.5) and Will (-13.2) reach. This is the shape the arena's eleven profiles
(E18, built 8/04 from the same draft) already encode; nothing re-derives.

## 4. What it means for the card

- The two-pick read's wait guard (row 1 must be at least 0.60 to survive) is conservative
  for this league: rows the model rates 0.60 to 0.80 survived 88% of the time here.
- The deep-🎯 pattern of mocks 56–59 would be more reliable in your league than in the public
  rooms: a man 24+ ranks below the pick waited 94 percent of the time at your seat last year.
- One season, one seat, 719 rows that share thirteen turns: the bands are evidence about
  direction, not a new fit. The rule I set before looking said "keep", and the numbers agree.

## Watchlist

- Mock 60 on v40: the advice-line reads it produces, judged against these bands.
- After 10/5 (WO-5): re-score this file on the refreshed lines (nothing here depends on lines,
  only on ranks and picks, so the answer should not move).
- Carried: D40-1 (marker switch), D40-3 (undo of an insert), D-ADP-1/2, the league settings
  screenshot.

## Open-item receipts

| item | query run (2026-10-01) | dated finding |
|---|---|---|
| (this intake) | machine joins only — no web research | the 10/01 daily pull's receipts cover the window |
| Jalen Duren, Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the daily pull's dedicated queries, same day (after-report-2026-10-01.md) | all HELD on 2026-10-01; this report edits no pool row |

## Bounds

- The rank column is an analyst rank the room displayed, not an ADP; this season's chips
  price off ADP where Yahoo lists one. The comparison is like for like in kind (the number the
  room sees), not in source.
- Rows at one seat in one season are not independent across the thirteen turns; the
  leave-one-turn-out figure is the honest one and it is what the rule used.
- Managers can change; the profiles are last season's.

## Decision sheet (owner disposes)

| id | decision | default if silent |
|---|---|---|
| D-LS-1 | Keep the shipped survival parameters (k 0.30, floor 8). The league fit gains 0.0034 Brier, under the 0.01 bar set in advance. | keep |
| D-LS-2 | Show the league-realized bands on the chip tooltip ("in your league last year: BUY NOW rows survived two in five, quiet rows nineteen in twenty") so the words match the room you draft in. Display only; red-first; deck v41. | yes, with the next deck build |
| D-LS-3 | Lower the two-pick read's wait guard from 0.60 toward 0.50 for this league, where 0.6–0.8 rows survived 88%. A ranking-adjacent change: pre-registered replay first, same bar as D59-2. | not before mock 60 |

## Provenance

Every number is read from `arena/results/league_survival_2025-26.json` (written by
`arena/mocks/league_survival.py` from the two raw files named in §1); no web research.
