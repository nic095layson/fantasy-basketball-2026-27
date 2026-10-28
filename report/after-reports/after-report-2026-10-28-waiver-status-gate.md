# The waiver scan's status gate, and the Flaim retry rule — 2026-10-28

Pull window: 2026-10-28 → 2026-10-28 (no pull for the kit: the pinned Flaim pulls of 10-21..10-28 on season/daily at 4559da0; read-only Flaim reads this session — get_players and two get_free_agents inventory pages for availability, one dated get_roster for team 5 at 2026-10-27; ESPN's injury feed read 16:15Z; one web search; no market pull).

**Method up front.** Owner 2026-10-28: diagnose and fix two findings from the runner's 10-28 report (`after-report-2026-10-28-morning-run-v3.md`), its EVIDENCE re-verified and its INFERENCE tested. Phase 1 read-only; options to the owner; the owner picked "Status gate (Recommended)" for A and "Retry once (Recommended)" for B. Parameters stated to the owner before the build: Out = Yahoo O or NA, or ESPN "Out"; Yahoo's letter wins where the player is on the pinned list, ESPN's feed covers the rest; D, Q, P and ESPN Day-To-Day stay in the waiver scan at full season value, flagged; streaming scales this week's games by the tier, ESPN Day-To-Day = 0.50; no source read = the scan halts; names resolved with `league_intake.resolve`; retry once on a retryable error after its retry_after, at most 60 s, never parallel. EVIDENCE marks what a run or read showed; INFERENCE what is derived.

## 1. Finding A, re-verified (EVIDENCE)

- Reproduced from the pinned 10-28 inputs: `daily_brief.py:168` built `fa = CG.free_agents(P, state)` (`co_gm.py:133-137`: unrostered pool players with `hoops.availability(p) > 0`, not vetoed, top 40 by board value). Jalen Williams's note leads "10/7:", so his tag is empty and `hoops.availability` returns 1.0 (`hoops.py:411`). He was in the 40 and the brief's top add: +0.1442 cats/week, title 37.34 (+4.73).
- The morning 10-27 pull (`a7d7283`) shows him `status: "O"` on MAXEY-MUM OVERDRIVE; transaction tr.85 dropped him 2026-10-27 14:58:46Z; the afternoon pull replaced that file, so today's copy of `pull_2026-10-27.json` no longer shows the O. The runner's line holds for the morning pin.
- REFUTED as framed: absent from the pinned available list does not mean unclaimable. A live read-only `get_free_agents` inventory page shows him **on waivers, clearing 2026-10-29**, 69% rostered across Yahoo. The pinned list (Yahoo's ranked mode, top 100 by rostered rate) omitted him although Jalen Smith (47%), dropped in the same move, is on it; 5 of the 6 candidates off the ranked list are claimable (Williams on waivers; Aldama, Merrill, Konchar, Hendricks free agents); Steinbach is not in the first 200 inventory rows (not checked further). Unrostered in the league is claimable; the defect was the status, not the claim.
- Of the 10-28 brief's 40 candidates, 9 carried a Yahoo letter (O ×5, D, NA, P, Q) the scan never read.
- My own 10-27 answer that Portis was not on Yahoo's top-100 list was wrong: Yahoo spells him "Bobby Portis Jr."; through the kit's resolver he is on every pinned list.
- Jalen Williams's status: ESPN reported 2026-10-26 a dislocated left ankle and fractured fibula needing surgery, timelines after the operation, return "in doubt for the remainder of the season"; ESPN's injury feed lists him Out (entry 2026-10-26T22:07Z). Season-ending is plausible, not confirmed.

**Blast radius.** The brief's waiver pairs and streaming list read the same `fa` (affected; fixed here). The deck's Today pickups come from `week_matchup`'s scan, which already reads Yahoo's list and status (`week_matchup.py:704`; not affected). The deck's Free Agents tab lists every unrostered board row (`season_deck.py:699`; affected, not fixed: §5). The Trade Analyzer and the form view use the FA flag as a filter only.

**Audit, every morning brief since 10-20** (scripted from the pinned pulls; 39 rows over 9 days: 25 clean, 10 with a status letter, 1 not on the list, 3 with no list pinned — 10-20 and 10-22 have none):

| date | slot | add | title Δ shown | Yahoo that day |
|---|---|---|---|---|
| 10-23 | waiver #2 | Tobias Harris | +0.1 | O |
| 10-23 | waiver #3 | Aaron Nesmith | 0.0 | Q |
| 10-24 | waiver #2 | Tobias Harris | −1.38 | Q |
| 10-25 | waiver #3 | Tobias Harris | +4.45 | O |
| 10-27 | waiver #2 | Cameron Johnson | +0.7 | Q (waivers) |
| 10-27 | waiver #3 | Tobias Harris | −0.32 | O |
| 10-27 | stream | Tobias Harris | — | O |
| 10-28 | waiver #1 | Jalen Williams | +4.73 | not on the ranked list (ESPN Out; on waivers) |
| 10-28 | waiver #2 | Cameron Johnson | −0.16 | D |
| 10-28 | stream | Yves Missi | — | O |
| 10-28 | stream | Aaron Nesmith | — | P |

## 2. Finding B, re-verified (EVIDENCE)

- The 502's shape (`"retryable": true, "retry_after": 60`) rests on the runner's report: its log is in its own container and the pinned pull records no failed call (ATTEMPTED-FAILED: path not present here).
- `manager_log.py:262-265` halts when fewer than 12 lineups for the day are pinned; `pinned_lineups` (`:118-127`) unions every pin, later wins; `flaim_live.take` keys a dated lineup by the date the response carries (`flaim_live.py:69-70`). A read-only `get_roster` for team 5 at 2026-10-27, made today, returned the full lineup (14 players with slots): Yahoo still serves it a day later, so a back-fill would complete the day with no code change. The owner did not pick the back-fill.
- The runner's call count holds: 30 Flaim calls (session, league info, 12 rosters, matchups, available list, standings, 12 dated lineups, transactions) plus 1 FantasyBot. Its reading that a `get_standings` beside a dated `get_roster` complied with the one-at-a-time rule (which names `get_roster`) is mine too; what it sent was not checked (its transcript is not here).

## 3. What was built (EVIDENCE)

- `co_gm.fa_status(P, yahoo, espn)`: per unrostered pool player, the day's status (Yahoo letter where listed, else ESPN), or `StatusMissing` when neither source exists. `co_gm.free_agents(P, state, status, n)` returns `(fa, set_aside)`: Out and untiered codes are set aside and named; the 40 are filled after the gate. `co_gm.streaming` ranks on expected games (games left × tier). `ESPN_TIERS = {"Out": 0.00, "Day-To-Day": 0.50}`.
- `status_feed.py` pins ESPN's feed as `data/status/espn_injuries_<date>.json` (one row per player) whenever it reads it.
- `daily_brief.py`: reads the two pins, gates the scan and streaming, flags a pair whose add carries D/Q/P ("check before claiming"), lists what was set aside, and on no source prints `WAIVER SCAN: HALT` and shows no pairs or streaming. The footer no longer says ESPN injuries are network-denied (the feed has read `ok` since 10-26).
- Red first: `test_waiver_status` (15) errored or failed on main's code (1 failure, 14 errors) and passes; `test_season_cv` adopted the new signature. Kit suite: 659 tests OK (2 skipped). Three dated after-report scripts (`zscore-assessment-2026-10-21`, `hunter-override-2026-10-22`, `season-cv-2026-10-21`) call the old signature; they reproduce at their own commits and were not edited.

## 4. The 10-28 brief before and after (EVIDENCE: two re-runs from the pinned 10-28 inputs, scratch worktrees at 4559da0)

The before run reproduces the recorded brief exactly. The after run used ESPN's feed as read at 16:15Z (10-28 has no ESPN pin; the morning would have read it near 12:05Z).

| | before (as recorded) | after |
|---|---|---|
| top pairs | Jalen Williams for Gillespie +0.144, title 37.34 (+4.73); Cameron Johnson for Gillespie 32.45 (−0.16); Bobby Portis for Washington 31.48 (−1.13) | Cameron Johnson for Gillespie 32.45 (−0.16), flagged D; Bobby Portis for Washington 31.48 (−1.13) |
| positive pairs | 10 of 520 | 2 of 520 |
| set aside | — | Jalen Williams (ESPN Out), Cason Wallace, Tobias Harris, Justin Champagnie, Yves Missi, Dylan Cardwell (Yahoo O), Kevin Porter Jr. (NA), Santi Aldama (ESPN Out) |
| streaming | Mamukelashvili, Melton, Missi, Nesmith, LaRavia | Mamukelashvili, Melton, Nesmith (P: 2.25 expected games), LaRavia, Horford |
| title (no move) | 32.6% ± 0.6 | 32.6% ± 0.6 |

The gate changes no engine constant and no simulator input: the title with no move is the same 32.6% ± 0.6 (avg of 2 runs × 10,000 seasons), and the surviving pairs' figures are unchanged. Every title share above carries the standing structural band (season sweep of 2026-10-26, current rosters, season pool, real schedule): TEAM_WEEK_SHOCK is FRAGILE: +2.7 (no shared games shock (0.0)) / -4.2 (shared games shock doubled (0.12)); weekly_availability is FRAGILE: -5.4 (no in-sim injury discount (risk 0.88 like healthy)) / +3.7 (harsher risk tier (0.65)) / +0.4 (healthy players play 0.95 of games) / -0.5 (healthy players play 0.80 of games).

## 5. B: the retry rule, drafted for the runner (not applied)

Morning prompt v3 → v4 (`morning_v4.txt`, 14,764 bytes), step 3a, one sentence replaced:
- before: "…if it returns YAHOO_AUTH_UNAVAILABLE, wait about 30 seconds (a Monitor until-loop, not a foreground sleep) and retry that same call once; only a failed retry counts as a failure."
- after: "…retry that same call once. If it returns an error marked retryable (for example a Cloudflare 502 or 503 with "retryable": true), wait its retry_after seconds, at most 60 (the same Monitor until-loop), and retry that same call once. Never retry in parallel and never more than once per call; only a failed retry counts as a failure, and the report names each retry and its result."

Afternoon prompt (`pm_new.txt` → `pm_v2.txt`, 5,370 bytes), step 2a, the same two sentences after "…and retry that same call once." Both drafts start from the texts verified byte-identical to the stored tasks; applying them is the owner's go in the runner conversation, which the tasks post into.

## 6. Bounds

**Out of scope by design.** No projection line, injury tag, roster or engine constant changed. The deck's Free Agents tab still lists every unrostered board row with no status (§1, blast radius); a follow-up on the owner's word. The 10-27 manager-log day for team 5 stays unlogged (back-fill not picked; it would work, §2). **In scope and unverified.** `ESPN_TIERS` (Out 0.00, Day-To-Day 0.50) and the Yahoo letter tiers it sits beside (`status_feed.TIERS`, D-S1-7, D-IS-6/7/10) are stated defaults, not registered in `constants_registry.json` (whose checker covers arena, hoops, season_lines, minutes_line only): new decision D-WS-1, whether to register them. Why Yahoo's ranked list omitted Jalen Williams is not explained (ATTEMPTED-FAILED: the ranked and inventory responses carry no reason). A letter tiers the next game, not the season: an Out for one game (Tobias Harris, calf) is set aside the same as a season-long Out until the letter clears (INFERENCE from the rule as picked).

## 7. Next steps (owner decisions)

1. Merge this PR; the gate runs from tomorrow's morning brief (status_feed pins ESPN first, then the brief reads it).
2. Apply `morning_v4.txt` and `pm_v2.txt` in the runner conversation (one sentence each).
3. D-WS-1: register the status tiers in the constants registry, or leave them as stated defaults.
4. The deck's Free Agents tab: show the day's status beside unrostered rows, or leave it.

## Watchlist

- **Tomorrow's brief:** a "Status from Yahoo and ESPN" line under the waiver scan, and no add whose Yahoo letter is O or NA.
- **data/status/espn_injuries_2026-10-29.json** exists after the status feed step.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| waiver scan recommends Out players (finding A) | **FIXED** in the brief; deck Free Agents tab open | §1, §3, §4 |
| Flaim 502 halts the manager log (finding B) | **DRAFTED**, prompt edit awaits the owner | §2, §5 |
| status tiers unregistered (D-WS-1) | **OPEN**, owner decision | §6 |

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward the same way the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (`after-report-2026-10-21-pickups-file.md` §1) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck e0722cf (this change's deck commit), checked today, the same page the 10/22 day report replayed. Its table stands, carried here verbatim from the day report.

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
