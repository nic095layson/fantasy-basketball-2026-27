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

**Headline.** Items 1–6 are done. Item 7 is **[P3 HEADLINE]**.
- **#149 merged** (`32f12db`). It carries the band fix, the calibration instrument, the audit note and the script comments.
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
- **Today's run** (EVIDENCE, `gauntlet-2026-10-21/availability_calibration.json`):

  > AVAILABILITY CALIBRATION: INSUFFICIENT — median team games 0 < 15; 0 risk-tagged with games < 10; no realized ratio (no healthy or tagged player has team games on file) (population 155: healthy 136, mild 2, risk 17; regular-season team-games on file 0); first verdict expected near 2026-11-17. No value changed.

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

**What happened (EVIDENCE):** [P3 RESULTS]

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

- **[P3 WATCH]**
- **`--since` reaches the runner only through `main`.** This PR must merge before **2026-10-23 12:53Z**. Until then the prompt's fallback runs on any day whose pull is incomplete.
  - 10/21 and 10/22 are safe either way: the runner's transcript holds no earlier pull.
- **The runner's transcript grows daily.** Compaction is the session's own business. With the guard in place, old pulls in it are inert.
- **The first regular-season box scores** arrive with the 10/22 run (the season opens tonight). The calibration's sample starts then.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| kit #149 | **MERGED** | `32f12db` |
| band line, every FRAGILE constant | **DONE** (in #149) | red-first 50/50; both bands on the 10/20 page |
| calibration instrument | **BUILT**, INSUFFICIENT until about 11-17 | `availability_calibration.json` |
| audit second correction | **DONE** (in #149) | paragraph + inventory row 11 |
| old scripts | **LEFT**, commented (in #149) | two comments |
| A1 / #128 | **STANDS** | deck `80eecdf` |
| morning push | **[P3 RECEIPT]** | §3 |
| 7 risk rows | **PROPOSED**, none applied | §4, `seven_rows.json` |
| D-INT-1 | carried | provenance writer not built (owner's call) |

The flagged-name receipts are carried forward from the lock report. This build pulled nothing and researched no player, so they were not re-queried (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this build (did not check) |

## Repeat-name market check

[REPEAT-NAME]

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
4. **[P3 DECISION]**
5. **The old routine** (`trig_015cdR1nKmi2ZgqTcVZQBSgf`) is disabled, not deleted. Delete it once the runner has pushed for a week, or keep it as the fallback. *Recommended: keep it until 10/28.*

## Bounds

**Out of scope by design.**
- Any projection line, tag, roster or engine constant. That includes the 7 rows, which are proposed only.
- The board-rank effect of the 7-row proposals. Computing it is a dry run, and it waits for your go.
- Any deck change. The deck stays at `80eecdf`.
- FantasyBot calls. Today's quota was spent by the 12:54Z run.

**In scope and unverified.**
- **[P3 BOUNDS]**
- **The cause of the 12:54Z run's missing push: UNVERIFIABLE.** No tool here reads another session's transcript; `get_session` shows only status, tags and a summary. The run's session carried `config:no-git-repo`, which fits a session with no repo attached, but nothing shows the exact refusal.
- **The 7 rows' preseason notes** are as recorded in the pool on 10/21. They were not re-queried for this report (did not check). That is not load-bearing for the GP history, which comes from git; it bears only on the per-row proposals, which are yours to make.
- **Cardwell**, one of the tag-time comparison rows in the 10/14 report, has no row under that spelling in the kit file. Other spellings: did not check. Not load-bearing: three comparison rows remain.

## Provenance

- **Session:** Claude Code (cloud), 2026-10-21. The work ran from about 13:50Z to [END]Z, with one context compaction in the middle.
- **Governors, loaded with the Skill tool for this task:**
  - gauntlet, at the start;
  - plan-gate, at the start, with its full block shown to you before any merge. It was reloaded after the compaction, before the #149 merge;
  - scope-fence, at the `--since` guard, which it classified as a blocking dependency of item 7;
  - adversarial-verify, before delivery;
  - after-report, [AR].
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
