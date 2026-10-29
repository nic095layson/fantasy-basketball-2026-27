# Red-team follow-ups F1–F3 (owner picks, 2026-10-29)

Pull window: 2026-10-28 → 2026-10-28 (no pull: the 10-28 afternoon records on season/daily 2f80fb0, read only; kit main 848a4ef, deck main 55d8e3f).

**Method up front.** The owner picked all three follow-ups from the 10-28 system audit (PR #224): "Run it on today's pairs", "Re-run and fingerprint", "Pin the morning copies". F1 is an assessment only. F2 and F3 are code. The method parameters below were stated to the owner before each run. EVIDENCE marks what a run or read showed; INFERENCE marks what is derived.

**Verdict: F1 — Cameron Johnson for Gillespie holds under all 12 variants, and Tobias Harris for Queta is negative except with no shared-games shock. F2 — 7 of 9 attacks are CURRENT; A-3 cannot be stamped as it stands (owner decision). F3 — fixed from the next run on; it needs a Runner prompt edit (pm_v4).**

## 1. F1: today's waiver pairs under every sweep variant (EVIDENCE: f1_decisions.json)

Parameters, stated before the run:
- **Base roster:** the league state after the 10-28 afternoon run (Portis added, Haliburton on IL, which the simulator leaves out, as it does every IL player).
- **Pairs:** the brief's own selection (status gate, then `waiver_pairs`, top 3 distinct adds) re-run on that state with the 10-28 status pins. The 10-28 brief's pairs were scored before the Portis add (its third pair was Portis for Washington).
- **Variants:** baseline plus the 12 declared bands in the registry.
- **Sims:** seeds 2026 and 2027 (the brief's) × 10,000 seasons, season pool, real schedule; each pair is paired with the base on the same seed.
- **Missing player:** Mo Bamba (Looking Cool Joker!) is not in season/daily's pool_season.csv yet (pooled 10-28 after the 5 AM build), so he is left out, as the simulator handles any unpooled player.
- **Harness check:** the same code reproduces the 10-28 brief's base on that morning's state: 32.57 / 32.64 against 32.6 published (sanity.py).

The three pairs: Cameron Johnson (DEN, **D** on Yahoo) for Collin Gillespie, +0.027 cats/week; Darryn Peterson (UTA) for Gillespie, +0.010; Tobias Harris (SAS, **O**, ESPN expects him back within 7 days) for Neemias Queta, +0.007. 5 of 520 pairs are positive. Set aside as Out: Jalen Williams, Cason Wallace, Kevin Porter Jr., Justin Champagnie, Dylan Cardwell.

Title Δ in points, the mean of the two seeds:

| variant | base title | C. Johnson for Gillespie | D. Peterson for Gillespie | T. Harris for Queta |
|---|---|---|---|---|
| baseline | 21.9 | **+1.06** | +0.13 | **−1.25** |
| BENCH_WEIGHT 0.50 / 1.00 | 21.9 | +1.06 | +0.13 | −1.25 |
| PCT_MIX_INFL 1.0 | 22.1 | +1.62 | +0.57 | −1.12 |
| PCT_MIX_INFL 1.30 | 21.1 | +1.28 | +0.64 | −0.90 |
| TEAM_WEEK_SHOCK 0.0 | 22.5 | +1.96 | +1.64 | **+0.45** |
| TEAM_WEEK_SHOCK 0.12 | 19.0 | +0.74 | +0.23 | −0.15 |
| availability: no injury discount | 16.0 | +1.17 | +0.50 | −0.97 |
| availability: risk tier 0.65 | 25.7 | +1.21 | +0.28 | −1.03 |
| availability: healthy 0.95 | 22.7 | +0.72 | +0.66 | −0.70 |
| availability: healthy 0.80 | 20.3 | +0.75 | +0.48 | −0.57 |
| GAMES_PER_WEEK 3.0 | 21.1 | +1.08 | +0.51 | −0.54 |
| GAMES_PER_WEEK 4.0 | 22.3 | +1.16 | +0.44 | −1.60 |
| **verdict** | | **HOLDS** (13 of 13 positive) | **HOLDS in direction**, but at baseline +0.13 sits inside the seed spread (+0.1 / +0.2) | **FLIPS** (negative except at shock 0.0) |

- INFERENCE: Johnson for Gillespie is the robust pick, conditional on his **D** status. Harris for Queta ranks positive on cats/week, but the season simulator scores it negative under 11 of 12 variants. The cats/week ranking and the title share disagree on it, so it is not a move.
- EVIDENCE: the base title share went from 32.6% (10-28 brief) to 21.9% on the post-afternoon roster. The harness reproduces 32.6 on the morning roster, so the drop comes from the roster change. INFERENCE: most of it is Haliburton moving to IL, which the simulator scores as gone for the season. Read 21.9 as the "out all season" floor, not a forecast of his return.
- This is not registered as a standing attack: it was an assessment only. Registering it is an option in §5.

## 2. F2: attacks re-run on today's engine (EVIDENCE)

Correction to the 10-28 audit: it named A-1 to A-4 as the unfingerprinted attacks. The checker's list was A-2, A-3, A-4 and A-6. A-1 already carried 048efb6, whose engine files are unchanged.

| attack | re-run on deck 55d8e3f | result vs the 10-19 record | status now |
|---|---|---|---|
| A-1 category math | yes | z and availability diffs 0.0, board identical; kit rows 325 to 327 (Brazile, Bamba) | CURRENT (55d8e3f) |
| A-2 kit/deck join | yes, now writes `engine_commit` | 0 line differences; Brazile and Bamba kit-only (not in the frozen v69 deck pool) | CURRENT |
| A-3 card vs simulator | yes | **does not hold as pinned**: max gap 0.044 to 0.221, ρ 0.99 to 0.93 | UNFINGERPRINTED (owner decision) |
| A-4 integer ties | yes, now writes `engine_commit` | tied categories per matchup 0.174 to 0.175 (2026); per-category rates within 0.001 | CURRENT |

**Why A-3 moved.** The script compares a card computed on the live engine with reference sims pinned, by design (decision 5 (a), 10-21), to the old 0.60-recovery engine (files of 10-15). After deck #127/#128 those are two different engines, so stamping today's fingerprint would call a stale comparison CURRENT. The same attack against today's references (`_w17r_av0`, made 10-20 on the live engine): max gap 0.036 / 0.038, ρ title 0.993 / 0.986, which holds (`rt_consistency_av0.json`). A-3 is left as it was until the owner picks (§5).

Attack check after: `ATTACKS CHECK: PASS — 9 attacks on engine 55d8e3f; CURRENT 7, UNFINGERPRINTED 2` (A-3, A-6).

## 3. F3: the 3 PM run stops overwriting the morning's pinned files (EVIDENCE)

| file | before | after |
|---|---|---|
| status | 3 PM rewrote `status_<date>.json` | 3 PM writes `status_<date>_pm.json` (`status_feed --phase pm`) |
| ESPN pin | 3 PM rewrote `espn_injuries_<date>.json` | 3 PM writes `espn_injuries_<date>_pm.json` |
| league state in the morning record | `data/league_state.json` (rewritten at 3 PM) | `data/news/league_state_am_<date>.json`, league_live's morning copy, byte-identical to the state the morning built (checked 10-27 and 10-28) |
| 3 PM deck | read the overwritten files | reads the `_pm` files and the live state; no `_pm` status file halts the 3 PM page, and the morning page stands |

- Tests: 4 new, red first (4 of 4 failed before the change), now pass. test_season_deck 126 OK. test_status_feed, test_daily_brief, test_morning and test_redteam_attacks OK. One test_season_deck run showed a single failure that did not recur in two re-runs; its output was not kept.
- Behavioral check (a scratch copy of season/daily with this diff, date 10-28): `status_feed --phase pm` wrote the `_pm` files and left `status_2026-10-28.json` byte-identical. Both deck builds PASS. All 6 league_state, status and ESPN inputs in the two records re-check from the paths they name. With the `_pm` file removed, the 3 PM build FAILs with "status record missing".
- `tag_outcomes` reads `status_<date>.json`, which its docstring calls the file "built that morning". Until now it was getting the 3 PM overwrite; it now gets the morning file its spec names.
- Bounds: records already made (10-26 to 10-28) are unchanged. Their league_state bytes survive in the morning copies (10-27, 10-28). Their morning status bytes survive only in git history.

Runner impact: prompt edit — the afternoon task's status step moves to `--phase pm` behind a `--help` guard (pm_v4, RUNNER-ASK-v7, rule 11). Until it is pasted, the merged code makes the 3 PM deck halt (morning page stands).

## 4. Bands quoted

Every title share above carries the standing structural band (season sweep 2026-10-26, real schedule):
- **TEAM_WEEK_SHOCK is FRAGILE:** +2.7 (no shared games shock (0.0)) / -4.2 (shared games shock doubled (0.12)).
- **weekly_availability is FRAGILE:** -5.4 (no in-sim injury discount (risk 0.88 like healthy)) / +3.7 (harsher risk tier (0.65)) / +0.4 (healthy players play 0.95 of games) / -0.5 (healthy players play 0.80 of games).

## 5. Bounds and open decisions

**Out of scope by design.** No projection line, tag, roster or constant changed. No claim is made for Johnson's or Harris's health beyond the pinned status codes.

**In scope and unverified.** The 10-29 morning's own pairs (its 12:02Z run) may differ: a new status, Bamba pooled. A-6 is still the draft-day record.

Open decisions for the owner: A-3's reference (repoint to the live `_w17r_av0` sims, or retire it as a historical record); whether F1 becomes a standing attack; PR merge order (paste pm_v4 first).

## Watchlist

- 10-29 22:03Z afternoon run: the first one on pm_v4, if pasted; expect `status_2026-10-29_pm.json` and "SEASON DECK: PASS … (afternoon refresh)".
- Cameron Johnson's D status before any claim.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| F1 decision robustness in-season | **ASSESSED** (one day) | §1, f1_decisions.json |
| F2 unfingerprinted attacks | **CLOSED** for A-1, A-2, A-4; **OPEN** A-3 (owner), A-6 | §2 |
| F3 afternoon overwrites morning-pinned files | **FIXED** in code; Runner paste pending | §3, RUNNER-ASK-v7 |
| F4 week-1 bias and generous tiers | **WATCH**, the week-4 fit | 10-28 audit §3 |

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
