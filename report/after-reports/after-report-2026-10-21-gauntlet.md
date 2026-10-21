# GAUNTLET fixes: the season page's bands, a calibration instrument, the 7 risk rows, the audit's second correction, and a morning runner that can push — 2026-10-21

Pull window: 2026-10-21 → 2026-10-21 (build and measurement only; no roster pull, no box scores, no projection line or tag changed).

**Owner's request.** "Implement gauntlet fixes for all these", 2026-10-21. GAUNTLET is the full governed sequence. "These" were the open items from the proceed-with-all decision sheet and the 13:41Z check-in:
1. merge kit #149;
2. the season page's band line reads every FRAGILE constant;
3. D-PM-4 risk/mild, two parts:
   - calibrate against realized games (option d, with a check date);
   - look at the 7 risk-tagged kit rows that carry healthy-level GP;
4. a dated correction note on the red-team audit report;
5. the old scripts on the old references (recommended: leave, plus a note);
6. the A1 reading (deck #128's merge);
7. the morning run could not push its records.

**What was analyzed.**
- Kit `main`, first `f7db616` and then `32f12db` (after #149). The kit branch is `claude/market-data-workorder-mnfi2b`.
- Deck `main` `80eecdf`, unchanged by this work.
- The code read for each item: `scripts/season_deck.py`, `scripts/league_live.py`, `scripts/matchup_live.py`, `scripts/morning.py`, `hooks/govclass.py` and `hooks/governance-enforce.py`.
- The morning routine's stored prompt (`trig_015cdR1nKmi2ZgqTcVZQBSgf`).
- The git history of `report/projections-2026-27.csv` (41 commits) and of the deck's `data/players.csv`.

**Method choices, stated to you in the plan before the runs that used them:**
- M1. The season page quotes every FRAGILE constant in the sweep record, with a fallback to the record's tiers.
- M2. The calibration instrument is defined as follows:
  - **Season:** regular season only (`season_type` 2). Preseason and DNPs never count.
  - **Population:** rostered, non-IL players. Their tier is today's pool tag.
  - **Share:** games played ÷ the games the player's team has played.
  - **Threshold:** INSUFFICIENT until the median team has played 15 games and at least 10 risk-tagged players have games. That puts the first possible verdict near **2026-11-17**.
  - **Cadence:** the morning run prints its line daily.
- M3. The 7 rows are read from git records. A GP or tag is proposed for each, and no line or tag is changed.
- M4. The old scripts stay as they are, with a comment.
- M5. A1 is settled: #128 stands.
- M6. A dedicated persistent runner session.
  - It has the kit attached, `season/daily` as its push branch, and runs on the same model as the routine.
  - A new schedule at the same time fires into it.
  - The old routine is disabled, not deleted.
  - A catch-up run happens today with FantasyBot skipped, because today's quota is spent.
- Added mid-task, said to you before it was built: a `--since` guard on the two transcript readers. It is a blocking dependency of M6 (§3).

**Headline.** Items 1–6 are done. Item 7 is **fixed for scheduled runs**, and it surfaced one new flag.
- **#149 merged** (`32f12db`). It carries the band fix, the calibration instrument, the audit note and the script comments.
- **The morning runner pushed.** A scheduled fire into the new persistent runner committed `8ba6534` to `season/daily` (5 run-ledger rows) and opened draft PR #150.
  - The **"Run now" path does not use the runner.** A force-run spawned a fresh no-repo session, which pushed nothing, like this morning's run.
  - **The runner's deck step failed** on a latent 10/20 bug: `season_deck.py` crashes whenever there is no matchup pull that day. It is flagged with a one-line patch (decision 4), not fixed.
- **The 7 risk rows** got their GP in July, before their tags existed. The tag-time convention (−6 GP) began on 10/11 and never reached them. One proposal per row is in §4; nothing was changed.
- **A hazard found in my own design, fixed before it could fire:**
  - A persistent session keeps every day's FantasyBot pulls in one transcript.
  - On a day the pull failed, the kit would therefore have published yesterday's rosters dated today.
  - Shown live on this session's transcript: a run dated 2099-01-01 PASSed on the 10/20 pull.
  - The `--since` guard closes it. It is red-first, and it needs this PR on `main` before **10/23 12:53Z**.

---

## 1. Roster changes and the merges

No roster moved and no projection line or tag changed.

| PR | state | commit | note |
|---|---|---|---|
| kit #149 (proceed with all + owner fixes) | **MERGED** | `32f12db` | squash, pinned to head `a65e5d1`; main's tree equals the branch head's (checked) |
| kit branch | restarted from main | `8317a68` | merge commit with main as first parent, tree = main; fast-forward push, no force |

## 2. Items 2, 3a, 4, 5, 6

**Item 2: the season page quotes every FRAGILE band** (in #149, `a65e5d1`).
- `season_deck.py` now builds `bands` from every constant the sweep record tiers FRAGILE, and the page prints all of them. Before, it hardcoded `TEAM_WEEK_SHOCK`.
- The red-first test is `test_every_fragile_band_is_on_the_page`:
  - its fixture holds two FRAGILE constants and one SENSITIVE one;
  - it went red on `KeyError 'bands'`, then green at 50/50.
- EVIDENCE: on the real 10/20 page, run in node, both bands print, with engine `80eecdf`.

**Item 3a: the calibration instrument** (`scripts/availability_calibration.py`, in #149).
- **What it reports:** the realized risk÷healthy and mild÷healthy ratios, set beside the three instruments.
- **Tests:** a known-answer test, a preseason/DNP test, a threshold test, and a test that zero thresholds cannot turn nothing-measured into a verdict. Red-first, 4/4.
- **Two runs today, both EVIDENCE, both INSUFFICIENT.** My run on `main`, which does not yet hold the 10/20 box scores, is `gauntlet-2026-10-21/availability_calibration.json`:

  > AVAILABILITY CALIBRATION: INSUFFICIENT — median team games 0 < 15; 0 risk-tagged with games < 10; no realized ratio (no healthy or tagged player has team games on file) (population 155: healthy 136, mild 2, risk 17; regular-season team-games on file 0); first verdict expected near 2026-11-17. No value changed.

- The runner's run, with the 10/20 box scores (3 regular-season games, all `season_type` 2; I re-checked the committed file), is `report/briefs/availability_calibration_2026-10-21.json` on `season/daily`:

  > INSUFFICIENT — median team games 1 < 15; 5 risk-tagged with games < 10 … regular-season team-games on file 6

  **Correction to my own plan:** the regular season opened on **10/20**, not tonight.
- The three instruments it will be measured against are unchanged from 10/21:

  | instrument | risk ÷ healthy | mild ÷ healthy |
  |---|---|---|
  | deck board | 0.78 | 0.85 |
  | simulator | 0.852 | 0.898 |
  | kit board, mean over the active rosters | 0.906 | 0.807 |

- The new runner's prompt runs it daily (§3).
- This report quotes no title share. The structural bands that any title share carries are unchanged from the proceed report: sweep on `80eecdf`, `redteam-2026-10-19/sweep.json`.
  - **TEAM_WEEK_SHOCK is FRAGILE:** +2.7 (no shock) / −3.6 (shock doubled).
  - **weekly_availability is FRAGILE:** −2.7 (no in-sim injury discount) / +0.5 (harsher risk tier 0.65) / −1.5 (healthy plays 0.95) / +1.0 (healthy plays 0.80).

**Item 4: the audit's second correction** (in #149).
- A dated **SECOND CORRECTION** paragraph sits in `after-report-2026-10-21-redteam-audit.md`, right after its "two separate factors" passage.
- Inventory row 11 points to it.

**Item 5: the old scripts.**
- `rt_consistency.py` and `retro_redteam.py` each gained a two-line comment: pinned by design to the 0.60-recovery `_w17r` references; the live engine's references are the `_av0` files.
- Their behaviour is unchanged.

**Item 6: A1.** Deck #128 stands as merged. Nothing was reverted.

## 3. Item 7: a morning run that can push

**The cause stays unverified.** I could not read the 12:54Z run's transcript, because no transcript tool is available here. That run published the deck and pushed nothing. Its session carried `config:no-git-repo`. The routine creates sessions with no source repository (`sources: []`), and `update_trigger` cannot add one.

**What was built:**
- **The guard: `--since` on `league_live.py`, `matchup_live.py` and `morning.py`** (`67f6e71`).
  - **The hazard:**
    - `league_live` keeps the latest `get_league_team` per team in the transcript, and `matchup_live` keeps the last outlook.
    - A fresh session holds only today's pull.
    - A persistent session holds every day's pulls.
    - So a skipped or partial pull (the shared limit reached after 6 teams, say) would pass yesterday's rosters off as today's, or mix two days, stamped with today's date.
  - **The fix:** with `--since T0`, only transcript entries stamped at or after T0 count.
    - The comparison is between parsed instants, not strings; a test pins the sub-second case.
    - Entries with no readable stamp do not count.
    - An unreadable `--since` halts.
    - Without `--since`, behaviour is unchanged, and two tests pin that.
  - **Red-first:** 9 new tests went red on the missing option. The kit suite then passed 237/237, twice.
  - **Live check on this session's transcript** (EVIDENCE):
    - Without `--since`, a run dated 2099-01-01 printed `LEAGUE LIVE: PASS` on the pull made 2026-10-20 23:05Z, and `MATCHUP LIVE: PASS — week 1, games left 30 mine / 37`.
    - With `--since` set to now, both printed HALT and wrote nothing.
- **The runner prompt** (`gauntlet-2026-10-21/morning_runner_prompt.md`, the exact text the schedule carries). It is the old prompt plus:
  - T0, passed as `--since`;
  - a fallback for "no `--since` on main and today's pull incomplete": `box_pull` + `transactions` + `morning.py --no-fetch`, so no transcript reader runs;
  - repo-present handling, and a stash for leftovers;
  - the calibration line;
  - the run report written to `report/briefs/morning_report_<date>.md` and committed;
  - the governor loads that this repo's hooks expect;
  - FantasyBot tools found by name suffix. The probe showed they carry a UUID prefix in the runner.
- **The runner session.** `session_01BsJA4wttu98TKVNoh6HBz1`: the kit attached, outcome branch `season/daily`, model as the routine.
  - Its setup probe made no call, no write and no push.
  - EVIDENCE (the session's own summary, read through `get_session`): the repo at `08ac2db` on `season/daily`, and the FantasyBot tools present under a UUID prefix.
- **The schedule.** `trig_01V43JtVvW6teWGmwt17dPVw`, `CRON_TZ=America/Los_Angeles 53 5 * * *`, bound to the runner (`persist_session: true`).
  - Its `connectors` parameter was refused ("not available for this organization"), so it stores no connector. The runner session carries FantasyBot itself.
- **The old routine** `trig_015cdR1nKmi2ZgqTcVZQBSgf` is **disabled** (`enabled: false`), kept with its history.

**What happened (EVIDENCE):**
1. **The force-run went to a fresh session.** `fire_trigger` at 14:48:51Z did not deliver into the bound runner, though `persistent_session_id` stayed set on the schedule (re-read after the fire).
   - Instead it created `session_01WHG3uFwfGQVamoQnSDX4xf`, with origin `force_run_trigger` and tag `config:no-git-repo`: the shape of this morning's failing run.
   - It ran 14:48:51Z–14:52:31Z and pushed nothing; `season/daily` stayed `08ac2db`.
   - It also published no deck (see item 3). What else it did is UNVERIFIABLE: its record carries no summary, and no tool here reads its transcript.
2. **The scheduled one-shot landed in the runner.** It was a one-shot bound to the runner (`trig_011MxfEaVsbDxdVBX5HomF2v`, 14:56:00Z, the same binding as the daily schedule).
   - It was delivered into `session_01BsJA4wttu98TKVNoh6HBz1`: status RUNNING at 14:56:43Z, a re-provisioned container (worker epoch 2) with the repo present.
   - The schedule's own record agrees: last run in session `…01BsJA4wttu98TKVNoh6HBz1`, then `enabled: false`, `ended_reason: run_once_fired`.
   - At 14:59:56Z it pushed `8ba6534` to `season/daily`.
     - It was a fast-forward: `08ac2db` is an ancestor of `32f12db`, the commit's parent. No force.
     - 14 files.
     - 5 run-ledger rows: season lines, season board, status feed and daily brief PASS; season deck FAIL.
   - At 15:00:05Z it opened **draft PR #150, "Season: daily records"**.
   - Its own report is committed as `report/briefs/morning_report_2026-10-21.md`:
     - T0 was 14:56:43Z;
     - step 4 took the no-fetch fallback, because `main` has no `--since` and step 3 was skipped;
     - the kit was already attached;
     - FantasyBot tools were present under the prefix `mcp__fc659f00-…__`, and 0 of 14 calls were made, as instructed.
   - I re-checked its box-score and calibration claims against the committed files (above).
3. **Its MORNING verdict is FAIL, at "season deck".**
   - The error: `FileNotFoundError` on `data/news/matchup_live_2026-10-21.json`, at `scripts/season_deck.py:142`.
   - The deck was not built or published by this run.
   - The live page is still the 12:54Z publish. EVIDENCE: the page's embedded `generated_utc` is `2026-10-21T12:58:50Z`, read at about 15:10Z, so neither later session published.
   - **Reproduced twice** (EVIDENCE), with the identical `FileNotFoundError`:
     - `season_deck.py --date 2026-10-21` in a scratch worktree of `8ba6534`;
     - the same run with `season_deck.py` as it stood at `f7db616`, before today's band edit.
   - **The cause predates today:**
     - `matchup_live` is optional when loaded (line 90, `os.path.exists`), but the provenance record hashes every input path unconditionally (line 142).
     - The two lines date from 10/20 (`ec803bb`) and 10/19 (`b285fb3`).
     - So the deck step fails on any morning when `matchup live` halts, with or without today's changes. My fallback merely made today such a morning.

**Assessment of item 7.**
- **Pushing works.** It goes through the scheduler into a session that has the repo attached (EVIDENCE: `8ba6534`, PR #150).
- **The daily 05:53 cron** uses the same schedule kind and the same binding as the one-shot that landed. INFERENCE: it lands the same way. First observation: 2026-10-22 12:53Z.

## 4. Item 3b: the 7 risk-tagged rows at healthy-level GP

**Method.**
- **The rows:** those the 10/21 D-PM-4 record (`proceed-2026-10-21/dpm4.json`, pool population) places in the risk tier, with kit availability at or above the healthy median (0.8634, the `avail` of GP 68).
- **Their history:** each row's kit GP across all 41 commits of `report/projections-2026-27.csv`, and the first deck commit carrying each tag.
- **Record:** `gauntlet-2026-10-21/seven_rows.py` writes `seven_rows.json`. Two runs gave identical output.

| player | team | tag | first tagged (deck) | kit GP, and since when | rostered | latest preseason note on file |
|---|---|---|---|---|---|---|
| Alex Sarr | WAS | inj-foot-risk (June surgery) | 2026-07-23 `bd3dd89` | 72 since 2026-07-12 | yes | held out of the 10/8 opener, started 10/10 (20 min) |
| Jaylen Wells | MEM | inj-toe-risk (surgery) | 2026-07-23 `64fe8c7` | 72 since 2026-07-12 | no | started 10/5, 10/7, 10/9 |
| Keegan Murray | SAC | inj-ankle-risk (May scope) | 2026-07-23 `64fe8c7` | 72 since 2026-07-12 | yes | missed two preseason games, 8 min on 10/10 |
| Zach Edey | MEM | inj-ankle-risk (bone stress surgery) | 2026-07-23 `bd3dd89` | 70 since 2026-07-12 | yes | held out 10/5, 10 min on 10/7; "tag kept by convention for the first season back" |
| Trey Murphy III | NOP | inj-shoulder-risk (season ended early) | 2026-07-23 `64fe8c7` | 70 since 2026-07-12 | yes | started 10/6 and 10/8 |
| De'Andre Hunter | SAC | inj-eye-risk (retinal surgery Feb) | 2026-07-23 `bb85c1c` | 70 since 2026-07-12 | no | started 10/8, bench 10/10 |
| Jaren Jackson Jr. | UTA | inj-knee-risk (PVNS surgery) | 2026-07-23 `bb85c1c` | 68 since 2026-07-12 | yes | started 10/4 and 10/6; "the tag stays for the first season back" |

**For comparison: rows tagged since the convention began.** The D-1010-2 default is "tag + kit GP −6".

| player | tag first on deck | kit GP history |
|---|---|---|
| Isaiah Stewart | 2026-10-11 | 70, then 64 on 2026-10-11 |
| Maxime Raynaud | 2026-10-13 | 72, then 66 on 2026-10-13 |
| Coby White | 2026-10-14 | 68, then 62 on 2026-10-14 |

**Assessment.**
- **EVIDENCE:** all 7 tags arrived on 2026-07-23 ("injury-law application", "risk tags"), eleven days after the kit's GP baseline of 07-12. No commit since has touched their GP. Every later pass left it alone, and the 10/14 blend notes say "games, minutes and tags unchanged".
- **INFERENCE:** the −6 convention was born on 10/10–10/11 for new tags. Nothing in the record applied it, or decided not to apply it, to tags that already existed. So these 7 rows are a gap between two rules, not a decision.
- **The effect of each option on the kit's discount is arithmetic, not a board run.** `avail` falls by 6/82 × 0.8 = 0.0585 for any row moved by −6, which would put every one of the 7 below the healthy median. The board ranks that would follow were **not computed**; that is a dry run, and it waits for your go.
- **The deck board already discounts all 7 at ×0.78.** Only the kit board is affected.

**Proposal per row** (none applied):

| player | proposed | basis |
|---|---|---|
| Alex Sarr | GP 72 to 66 | absent in preseason; the convention |
| Keegan Murray | GP 72 to 66 | two preseason absences; the convention |
| Zach Edey | GP 70 to 64 | the note keeps the tag for the first season back; the convention |
| Jaren Jackson Jr. | GP 68 to 62 | the same "first season back" note; the convention |
| Trey Murphy III | GP 70 to 64, or keep | no preseason absence on file; the convention says −6, the preseason says healthy |
| Jaylen Wells | GP 72 to 66, or keep | no absence on file; not rostered |
| De'Andre Hunter | keep GP, review the tag | an eye surgery in February and every preseason game played; the tag may be the question, not the GP |

## 5. Every gate, pass or fail

| gate | result |
|---|---|
| kit suite (`SEASON_POOL=1 … unittest`) | 237/237, twice (226 before the guard, 11 new) |
| guard red-first | 9 red on the missing option, then green |
| live guard check | without `--since` PASS on the 10/20 pull; with it HALT in both readers |
| seven_rows.py | two runs identical |
| calibration | INSUFFICIENT, exit 0 |
| report gates, red-team gates, claims | in `gates.json` (this report) |

## Watchlist

- **Never use "Run now" on the new schedule.** A force-run spawns a fresh no-repo session that cannot push (§3). For a catch-up, use a one-shot schedule bound to the runner, as done here.
- **The deck step fails on any day without a matchup pull** (decision 4). On 10/22, the deck builds only if the FantasyBot pull returns the outlook.
- **The first cron fire into the runner is 2026-10-22 12:53Z.** Check `git ls-remote origin refs/heads/season/daily` after about 13:05Z.
- **The runner's own commits carry its own attribution trailer.** That comes from the runner's harness, not from this prompt.
- **`--since` reaches the runner only through `main`.** This PR must merge before **2026-10-23 12:53Z**. Until then the prompt's fallback runs on any day whose pull is incomplete.
  - 10/21 and 10/22 are safe either way: the runner's transcript holds no earlier pull.
- **The runner's transcript grows daily.** Compaction is the session's own business. With the guard in place, old pulls in it are inert.
- **The regular season opened 10/20** (3 games on file). The calibration's sample has started: 6 team-games and 5 risk players measured.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| kit #149 | **MERGED** | `32f12db` |
| band line, every FRAGILE constant | **DONE** (in #149) | red-first 50/50; both bands on the 10/20 page |
| calibration instrument | **BUILT**, INSUFFICIENT until about 11-17 | `availability_calibration.json` |
| audit second correction | **DONE** (in #149) | paragraph + inventory row 11 |
| old scripts | **LEFT**, commented (in #149) | two comments |
| A1 / #128 | **STANDS** | deck `80eecdf` |
| morning push | **DONE** for scheduled runs; deck step FAIL (latent bug, flagged) | `8ba6534` on `season/daily`, PR #150 |
| 7 risk rows | **PROPOSED**, none applied | §4, `seven_rows.json` |
| D-INT-1 | carried | provenance writer not built (owner's call) |

The flagged-name receipts are carried forward from the lock report. This build pulled nothing and researched no player, so they were not re-queried (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this build (did not check) |

## Repeat-name market check

Re-run fresh on deck `80eecdf` (this build changed no deck page): 33 of 33 mocks replayed.

**The result is identical to the proceed report.** The page hash is the same (`6a5cefea4921`), and the flagged table and near-miss line are equal line for line (EVIDENCE: `diff` on the two sections with the hash masked; record `gauntlet-2026-10-21/repeat_name.json`).

The tool's output, pasted:

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


## Decision sheet

1. **Merge this kit PR before 2026-10-23 12:53Z.** Merging is your word.
   - It carries the `--since` guard, this report and the runner prompt's record.
   - Until it merges, the runner's fallback runs on any day the pull is incomplete. The fallback publishes everything except that day's rosters and matchup.
2. **The 7 risk rows** (§4). Options:
   - (a) apply the −6 convention to all seven;
   - (b) keep all seven as they are;
   - (c) per row, as in §4's proposal table.
   - *Recommended: (c).*
   - Any row you approve takes the usual path: line change, then kit rerun, board diff, gates. That run is where the rank effect is first measured.
3. **The calibration check date.** 2026-11-17, with thresholds of 15 team games and 10 risk-tagged players with games. Keep it, or name another.
   - Until then every morning line says INSUFFICIENT.
   - Which number to adopt once it is MEASURED stays D-PM-4, yours.
4. **The deck's missing-input crash** (flagged, not fixed; it predates today).
   - **The bug:** `season_deck.py:142` hashes every input path, including the optional `matchup_live`, so a morning with no matchup pull publishes no deck.
   - **The proposed patch** (one line plus a red-first test):
     - hash only the inputs that exist, and record a missing one as `sha256: null`;
     - the test builds the deck with no `matchup_live` file.
   - Options: (a) build it now, ahead of the 10/22 run; (b) leave it.
   - *Recommended: (a).* Tomorrow's FantasyBot pull is not guaranteed, because the limit is shared.
5. **The evening status check** (`trig_0192N7Asy7SSSJF33j1NM4ZL`, 17:23 PT daily, enabled). Flagged, not touched: it was not in item 7.
   - It has the same fresh-session, no-repo shape as the old morning routine. It pulls FantasyBot, rebuilds the deck, and pushes to `season/daily`.
   - Its last run, 10/21 00:23:36Z–00:23:52Z, lasted 16 seconds. Whether it pushed or published anything: did not check.
   - Options: (a) disable it; (b) move it into the runner as a second bound schedule, with its own prompt adapted the same way; (c) leave it.
   - Its 14 FantasyBot calls come from the same shared daily limit as the morning pull.
6. **The old routine** (`trig_015cdR1nKmi2ZgqTcVZQBSgf`) is disabled, not deleted. Delete it once the runner has pushed for a week, or keep it as the fallback. *Recommended: keep it until 10/28.*

## Bounds

**Out of scope by design.**
- Any projection line, tag, roster or engine constant. That includes the 7 rows, which are proposed only.
- The board-rank effect of the 7-row proposals. Computing it is a dry run, and it waits for your go.
- Any deck change. The deck stays at `80eecdf`.
- FantasyBot calls. Today's quota was spent by the 12:54Z run.

**In scope and unverified.**
- **Whether the daily cron fire lands in the runner:** UNVERIFIABLE until 2026-10-22 12:53Z.
  - EVIDENCE: a one-shot through the same scheduler, with the same binding, landed.
  - EVIDENCE: a force-run did not.
  - The branch rule, if the cron does not land: re-enable the old routine and disable the new one. The records then go unpushed, as before.
- **Whether the runner keeps its repo and FantasyBot tools across later re-provisions.** Seen once (worker epoch 2, repo present, tools present); not proven for every day.
- **The cause of the 12:54Z run's missing push: UNVERIFIABLE.** No tool here reads another session's transcript; `get_session` shows only status, tags and a summary. The run's session carried `config:no-git-repo`, which fits a session with no repo attached, but nothing shows the exact refusal.
- **The 7 rows' preseason notes** are as recorded in the pool on 10/21. They were not re-queried for this report (did not check). That is not load-bearing for the GP history, which comes from git; it bears only on the per-row proposals, which are yours to make.
- **Cardwell**, one of the tag-time comparison rows in the 10/14 report, has no row under that spelling in the kit file. Other spellings: did not check. Not load-bearing: three comparison rows remain.

## Provenance

- **Session:** Claude Code (cloud), 2026-10-21. The work ran from about 13:50Z to 15:15Z, with one context compaction in the middle.
- **Governors, loaded with the Skill tool for this task:**
  - gauntlet, at the start;
  - plan-gate, at the start, with its full block shown to you before any merge. It was reloaded after the compaction, before the #149 merge;
  - scope-fence, at the `--since` guard, which it classified as a blocking dependency of item 7;
  - adversarial-verify, before delivery;
  - after-report, **late**: it loaded after this report's draft was written, before it was finalized. The draft's structure came from the house format, not from the loaded skill.
- **Records:** `report/after-reports/gauntlet-2026-10-21/`:
  - `morning_runner_prompt.md`, the schedule's exact text;
  - `seven_rows.py` and `seven_rows.json`;
  - `availability_calibration.json`;
  - `repeat_name.json` and `repeat_name.out`.
- **Re-verify:**
  - `python3 report/after-reports/gauntlet-2026-10-21/seven_rows.py`;
  - `python3 scripts/availability_calibration.py`;
  - `SEASON_POOL=1 python3 -m unittest discover -s scripts -p 'test_*.py'` (expect 237 OK);
  - `git ls-remote origin refs/heads/season/daily` after 12:53Z daily.
