# The season tools' per-game variation, fitted (D-ZS-3) — 2026-10-22

Pull window: 2026-10-21 → 2026-10-22. No league or market pull and no web search. Every figure below comes from committed files run on the merged deck.

**Your decisions.**
- **2026-10-21, D-ZS-3:** (a) **"Adopt the fitted values"**, then **"Season tools only"** (`after-report-2026-10-21-gscore-column.md`, decision sheet item 3).
- **2026-10-22, about 02:25Z, clicked:** **"#159 then #160, Season variance, #161 risk rows, #162 + deck #131"**. "Season variance" is deck PR #130 plus this kit PR, both to merge. Deck #130 merged at 048efb6; this PR merges on the same word once its gates pass.

**What was analyzed.**
- Kit main at `4106055`, plus this branch's wiring commit.
- Deck `048efb6` (main, after #131 and #130). It is the season scripts' sibling and the red team's engine.

**Method, stated to you before the run** (after the compaction, about 03:05Z):
- **Assumption sweep:** 6,000 seasons × seeds 2026 and 2027 on deck 048efb6. The baseline is asserted within 3 sampling errors of the deck's new 10,000-season reference (`m100_league_sim_10k_s{seed}_w17r_av0_scv.json`) before any tier is read.
- **Before/after:** the same 10,000 seasons × seeds 2026 and 2027 as the first run, on the league schedule and the committed `data/league_state.json`. Swaps are scored on the brief's own waiver shortlist: the top 40 free agents by z, 520 add/drop pairs.
- **Attack records** re-run on 048efb6: A-1, A-5, A-7, A-8, A-9.

**Headline.**
- **The season tools now run on the fitted variation.** That means the waiver swaps, the week preview, the title-odds simulation and the standing sweep. The draft engine and the draft page are unchanged: the page is sha256 6a5cefea4921 at both 80eecdf and 048efb6.
- **Waiver swaps: one positive swap instead of two.**
  - Expected categories per week for the current roster: 5.2996 before, 5.2251 after.
  - Portis-for-Braun stays positive: +0.0304 before, +0.0257 after.
  - Holiday-for-Braun goes from +0.0047 to −0.0042, below zero.
- **Title odds: no change beyond sampling noise.**
  - 24.48 / 23.72 before and 24.69 / 22.94 after (seed 2026 / seed 2027), at 10,000 seasons each.
  - The two seeds move in opposite directions (+0.21 and −0.78). The binomial sampling error is about 0.43 points per seed.
  - TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared shock) / −3.4 (shock doubled), on the 10/22 sweep; the title figure sits inside that band.
- **The red team's bands moved a little; the FRAGILE set did not.** TEAM_WEEK_SHOCK and weekly_availability are FRAGILE, PCT_MIX_INFL is SENSITIVE and the rest are ROBUST, as on 80eecdf (§3).

## 1. What changed

No player, pool row, tag, line or price changed. The roster is as committed in `data/league_state.json`.

The value: `arena.SEASON_CV` (deck #130), fitted to the 2025-26 game logs of the board's top 180 with 20+ games (`zscore-assessment-2026-10-21/gamelogs/gscore_weights_2025-26.json`, `cv_fit`). The fit is one season, 2025-26; no multi-season window is involved, so no era check applies.

| category | draft engine `arena.CV` (hand-set) | season tools `arena.SEASON_CV` (fitted) | ratio |
|---|---|---|---|
| PTS | 0.30 | 0.395 | 1.32 |
| REB | 0.35 | 0.445 | 1.27 |
| AST | 0.40 | 0.496 | 1.24 |
| 3PTM | 0.55 | 0.717 | 1.30 |
| ST | 0.70 | 0.945 | 1.35 |
| BLK | 0.75 | 1.072 | 1.43 |
| TO | 0.50 | 0.668 | 1.34 |

The kit's wiring (this PR):
- `co_gm.waiver_pairs` builds every team-week model with `arena.SEASON_CV`.
- `co_gm.run_league_sim` passes `--season-cv` to the deck's `league_sim.py`.
- `weekly_preview.py` builds its models with `arena.SEASON_CV`.
- `scripts/redteam/sweep.py`:
  - reads the `_scv` reference;
  - runs `simulate_seasons(..., cv=arena.SEASON_CV)`;
  - its per-game-variance patch now scales `SEASON_CV`.
- The registry (`scripts/redteam/constants_registry.json`):
  - `arena.CV` goes from `declared_band` to `uncalibrated`, scoped to the draft engine only and frozen with the draft page. No decision is needed, per your "Season tools only".
  - `arena.SEASON_CV` is new, `measured`, with the fit as its record.
- **Test first.** `scripts/test_season_cv.py` failed on the unwired code with 4 failures and 1 error (`season-cv-2026-10-21/red.txt`) and passes 5 of 5 on this branch (`green.txt`).

## 2. What it moves in the brief

From `season-cv-2026-10-21/compare.json`. "Before" runs the same code with `SEASON_CV` set to the draft engine's `CV`, so only the variation differs.

| add | drop | before (expected categories per week) | after |
|---|---|---|---|
| Bobby Portis | Christian Braun | +0.0304 | +0.0257 |
| Jrue Holiday | Christian Braun | +0.0047 | −0.0042 |
| Aaron Nesmith | Christian Braun | −0.0039 | −0.0103 |
| Nikola Vucevic | Christian Braun | −0.0129 | −0.0096 |
| Anthony Black | Christian Braun | −0.0145 | −0.0355 |

The table shows the top five before, with their after values.
- Positive swaps: two before (Portis, Holiday) and one after (Portis).
- Every one of the top five drops Braun, before and after.

| | title, seed 2026 | title, seed 2027 | playoffs, 2026 / 2027 | categories per week, 2026 / 2027 |
|---|---|---|---|---|
| before (`CV`) | 24.48 | 23.72 | 99.61 / 99.68 | 5.311 / 5.313 |
| after (`SEASON_CV`) | 24.69 | 22.94 | 99.27 / 99.39 | 5.235 / 5.237 |

**Read the title rows with both error bars:**
- the sampling error is about 0.43 points per seed;
- the structural bands are in §3; TEAM_WEEK_SHOCK alone spans +2.3 / −3.4.

Two more instruments, on the deck's draft-day state rather than the league state, point the same small way:
- the 10,000-season reference: 23.27 / 24.07 on 80eecdf, 23.06 / 23.25 on 048efb6;
- the sweep's own baseline: 23.77 / 24.20 on 80eecdf, 23.18 / 23.30 on 048efb6.

Across all three instruments the seed-level changes run from +0.21 to −0.90. More game-to-game variation makes every team's week noisier, which narrows the favorite's edge slightly. That last sentence is INFERENCE; the figures are EVIDENCE.

## 3. The red team on the new engine

**Sweep** (`redteam-2026-10-19/sweep.json`):
- engine 048efb6; 6,000 seasons × seeds 2026 / 2027; sampling error 0.535 points;
- baseline 23.18 / 23.30, against the reference 23.06 / 23.25, within 3 SE on both seeds.

| constant | variant | 80eecdf (`CV`) | 048efb6 (`SEASON_CV`) | tier now |
|---|---|---|---|---|
| TEAM_WEEK_SHOCK | no shared games shock (0.0) | +2.71 | +2.29 | FRAGILE |
| TEAM_WEEK_SHOCK | shared games shock doubled (0.12) | −3.62 | −3.35 | FRAGILE |
| weekly_availability | no in-sim injury discount | −2.68 | −2.00 | FRAGILE |
| weekly_availability | harsher risk tier (0.65) | +0.47 | +0.75 | ROBUST |
| weekly_availability | healthy players play 0.95 of games | −1.54 | −1.46 | SENSITIVE |
| weekly_availability | healthy players play 0.80 of games | +1.01 | +0.95 | ROBUST |
| PCT_MIX_INFL | binomial floor only (1.0) | +0.99 | +0.82 | ROBUST |
| PCT_MIX_INFL | inflation 1.30 | −1.06 | −1.28 | SENSITIVE |
| GAMES_PER_WEEK | 3.0 games per healthy week | −0.95 | −0.69 | ROBUST |
| GAMES_PER_WEEK | 4.0 games per healthy week | +0.29 | +0.63 | ROBUST |
| BENCH_WEIGHT | 0.50 and 1.00 | 0.00 | 0.00 | ROBUST |

`arena.CV`'s own band (×0.8 / ×1.2: +0.11 / −0.45, ROBUST on 80eecdf) leaves the sweep. The value the season tools use is now measured, not hand-set, and the draft engine's copy is frozen. The fitted values are 1.24–1.43 times the old ones, just beyond that band's ×1.2 edge. §2's title rows are the measured effect of the whole move.

**Attacks**, all re-run on 048efb6:

| attack | record | result |
|---|---|---|
| A-1 known-answer re-implementation | `postmortem-2026-10-19/rt_math.json` | engine 048efb6, z and availability differences 0.0 |
| A-5 sensitivity | `postmortem-2026-10-19/rt_sensitivity.json` | re-run; figures identical to the 80eecdf record (`git diff` changes only the engine line) |
| A-7 constants registry | `redteam-2026-10-19/constants.json` | PASS: 32 registered = 32 live; declared_band 5, measured 7, settings 7, structural 4, uncalibrated 9 |
| A-8 assumption sweep | `redteam-2026-10-19/sweep.json` | the table above |
| A-9 simulator re-implementation | `redteam-sim-2026-10-21/rt_sim.json` | PASS, deck head 048efb6 |
| freshness | `season-cv-2026-10-21/attacks.json` | 9 attacks: CURRENT 5, UNFINGERPRINTED 4, STALE 0 |

## 4. Errors and surprises, stated plainly

- **The before/after reproduced byte for byte.** `compare.json` written on 10/21 (kit 384a610, deck PR branch) and again today (kit 4106055, deck 048efb6) is identical. So the merges in between changed nothing these figures read. Two runs agreeing is the reproducibility check.
- **A-1 first reproduced the old record.** `rt_math.py` hard-codes `/home/user/yahoo-fantasy-basketball` and ignores `DECK_REPO`. That sibling still sat at 80eecdf.
  - After `git pull --ff-only` there, it re-ran: engine 048efb6, differences 0.0.
  - The hard-coded path is a script defect, flagged and not fixed here (out of scope).
- **The sweep record's registry hash is one edit old.** `sweep.json` records `registry_sha256` 7654a2cdd8ae, the registry as the sweep read it. Afterwards one string changed: `SEASON_CV`'s record now names this report (`-2026-10-22-`) instead of the planned `-2026-10-21-` name. No value, status or band changed. The committed registry hashes to ad58a6a1eb2b, and no gate compares the two.
- **The sweep's first launch did nothing** (`time: command not found` under an environment prefix). It was relaunched without `time`.
- **Between deck #130's merge and this PR, kit main's constants and attacks checks fail.** The registry still says `CV` is `declared_band` and lacks `SEASON_CV`, and four records carry 80eecdf. This PR closes that window. The 6:00 PT morning run does not run those checks.
- **#161's and #162's reports quote the 80eecdf bands** (+2.7 / −3.6 and so on). They were right on the sweep of their day and are not re-gated; reports quoting bands from today on quote 048efb6's.

## Watchlist

- **The draft engine keeps the hand-set `arena.CV`**, now registered `uncalibrated` with the page frozen.
- **D-PM-4 is untouched:** the board's and the simulator's injury tiers still differ (`after-report-2026-10-21-council-fixes.md`).
- **The fit is one season.** If 2026-27's game logs show different spreads, `SEASON_CV` is re-fit from them. The record names the file, so the next fit is one command (`zscore-assessment-2026-10-21/gamelogs/`).

## Open-item receipts

| item | status | receipt |
|---|---|---|
| D-ZS-3 season variation (your "Adopt the fitted values", "Season tools only", "Season variance") | **DONE**: deck #130 merged (048efb6); this kit PR merges on your word | §1–§3 |
| Hunter's tag (D-RR-1) | **OPEN**: you chose "Remove it"; the route is the open question (the deck's frozen-pool stamp) | `after-report-2026-10-22-risk-rows.md` §4 |
| older seasons' weekly totals (D-GP-3, "Weekly totals only") | **DONE on a draft PR**, not merged; merging is your call | `after-report-2026-10-22-flaim-history-totals.md` |

This change touched no pool row. The flagged-name receipts are carried forward from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21 (`after-report-2026-10-21-pickups-file.md` §1). The rest were not re-queried for this change (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this change (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (§1, `roster_drift_2026-10-21.json`) |

## Repeat-name market check

This change did not touch the draft-room deck page. Deck #131 changed a data README, and #130 changed the arena engine, `league_sim.py`, their test, README and records (`git diff --stat 80eecdf 048efb6`). `docs/draft-deck.html` is sha256 6a5cefea4921 at 048efb6, the same page the GAUNTLET report replayed on 10/21. Its table stands, carried here verbatim.

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

**Structural bands** (the 10/22 sweep, engine 048efb6):
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared shock) / −3.4 (shock doubled); the title figures of §2 sit inside that band.
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy plays 0.95) / +0.9 (healthy plays 0.80).

## Decision sheet

| ID | Question | Default if you say nothing | Where |
|---|---|---|---|
| D-ZS-3 | Season variation: decided 10/21 ("Adopt the fitted values", "Season tools only"); merged on your 10/22 "Season variance". The row leaves OPEN.md with this PR | closed | this report |

No new decision is opened here.

## Bounds

**Out of scope by design:**
- the draft engine and the draft page (frozen; `arena.CV` stays);
- the season board's z-scores and the G column, into which per-game variation does not enter;
- D-PM-4's injury tiers;
- `rt_math.py`'s hard-coded deck path (flagged in §4).

**In scope and unverified:**
- Whether 2025-26's spreads hold for 2026-27. That is an assumption (the fit is one season, named in §1); did not check. A re-fit on this season's logs is meaningful only once they hold enough games per player.
- The figures on later days' league states. Today's run is the committed state; the morning run uses the new value from its next run once this merges.

## Provenance

- **Produced by** session `session_01QjgeRdpDaWgSJmGKRG8fTU` on 2026-10-22, about 03:00–03:30Z. The code commit was written 10/21 23:16Z on an earlier base and cherry-picked onto 4106055.
- **Governors.** plan-gate was loaded at about 03:05Z after a context compaction, and its full block was emitted before the first change. adversarial-verify is loaded before the delivery.
- **Re-verify:**
  - `python3 report/after-reports/season-cv-2026-10-21/compare.py` rewrites `compare.json`; expect no diff.
  - `python3 scripts/redteam/check_constants.py --deck ../yahoo-fantasy-basketball --json /tmp/c.json`
  - `python3 scripts/redteam/run_attacks.py --check --deck ../yahoo-fantasy-basketball`
  - `SEASON_POOL=1 python3 -m unittest scripts/test_season_cv.py`

## In plain language

Last night you chose to give the in-season tools a more realistic sense of how much a player's nightly numbers bounce around. We measured that from last season's game logs, and it is 24–43% bigger than the guess the tools were using. Your draft page is untouched.

What it changes for you: the waiver scan now finds one worthwhile swap instead of two. Portis for Braun still helps a little. Holiday for Braun now comes out slightly negative, so it drops off. Your title odds barely move: one simulation run went up a fifth of a point and the other went down about three-quarters, which is within the normal wobble of the simulation. Nothing about your roster or anyone's projections changed.
