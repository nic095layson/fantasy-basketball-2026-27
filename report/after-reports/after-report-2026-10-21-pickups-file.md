# In-season pickups file: Andre Drummond joins the pool on the kit side; seven stale roster rows researched — 2026-10-21 (late evening)

Pull window: 2026-10-14 → 2026-10-21. What was read:
- Web searches only, for the roster-drift research: 12 queries, one or two per name. Records are in `pickups-file-2026-10-21/roster_drift_2026-10-21.json`.
- ESPN's 30-roster feed of 10/21, already on disk from this afternoon (`flaim-2026-10-21/roster_verification_2026-10-21_accidental.json`).

There was no league pull and no Flaim or FantasyBot call. `data/league_state.json` is untouched.

**Owner's request** (2026-10-21 at about 20:10Z, three clicked options):
1. Drummond: "(b) Kit-side pickups file". In-season player rows live in the kit, read by the roster intake and the season lines. Drummond's row moves there, deck #129 closes, the draft page stays frozen, and future pickups use the same file. This unblocks tomorrow's run.
2. Roster drift: "Research and report only". Two dated outlets per name, for Tony Bradley, Kevin Porter Jr., Ochai Agbaji, Jeremy Sochan, Dalton Knecht, Johni Broome and Bruce Brown. No pool change.
3. #156: "Global merges #156 now". That is the Global Operations session's job; this session does nothing on it.

Nothing was merged. Merging stays the owner's word.

**What was analyzed.**
- Kit main `cec4eae` (#155 merged). The branch `claude/market-data-workorder-mnfi2b` was restarted from it.
- Deck main `80eecdf`, and deck PR #129 `10226ce`, whose row this file carries.
- Live PR state read at about 20:20Z: #156 open (draft, `36cdae1`); #155 and #157 merged.

**Method.** Each choice was stated to the owner before the run that used it.
- **Drummond's row** is copied byte for byte from deck #129's `data/players.csv`, never retyped. `cmp` against `git show 10226ce:data/players.csv` (header plus his row): equal.
- **Duplicates.** A name in both the deck pool and the additions file is refused with an error, never carried twice. The intake matches with the deck's name fold (`verify_rosters.norm`); the season lines use their own `fold`.
- **Research window.** 2026-10-14, the Version 68 lock, to today. Two dated outlets per name, with ESPN's 10/21 roster feed as a mechanical second record.

**Headline.**
- The real 10/21 Flaim pull now builds all twelve teams with Drummond on Podz save the league's bench. It does this against deck **main**, which has no Drummond row. Before this change the same pull halted on his name.
- The season lines now write his row into `pool_season.csv`, which the brief and the week card read. Like every pool row, it is blended with his regular-season games: one so far, on 10/20.
- **The verification found a regression, and it is fixed.**
  - With Drummond in the league state, the daily brief failed. The brief is a fatal morning step, so the whole morning would have failed and skipped the week card and the deck.
  - The cause: the deck's season simulator runs only on its frozen `v69` pool and stops on any rostered name it lacks (`league_sim.py:35`).
  - Without this PR, tomorrow's intake halts on Drummond (non-fatal) and the morning passes on the old state. Merged unfixed, the PR would have made tomorrow worse.
  - The fix, kit-side and test-first: the simulator leaves out a rostered player its frozen pool lacks, as it already leaves out IL players (D-IS-8). The brief names him under the title odds.
  - The full offline morning now passes all six steps with Drummond in the state.
- The added row moves no other player's z-score in any category (largest change 0.0). Drummond lands at #227 in the deck engine's order.
- All seven drift names have moved since the lock:
  - Bradley was claimed by Utah;
  - the other six were waived and are on no NBA roster in ESPN's 10/21 feed.
- Two of the seven touch the league:
  - Kevin Porter Jr. is rostered by a rival;
  - Bruce Brown is on Yahoo's free-agent list.
  
  Yahoo marks both `NA`, which the matchup scores at 0.00.
- 315 of 315 tests pass, twice. Gates: see §3.

## 1. Roster changes (research and report only — no pool row changed)

All seven differ from the deck pool, which is frozen at the lock. The ESPN column is the feed of 10/21 (`site.api.espn.com`, all 30 rosters).

| player | pool team | ESPN 10/21 | what the outlets report (dates as the search index gives them) | outlets | league |
|---|---|---|---|---|---|
| Tony Bradley | NYK | UTA | waived by the Knicks (Thu 10/15), claimed off waivers by Utah, non-guaranteed (10/17–10/18) | Deseret News (URL dated 2026-10-17), RotoBaller, ESPN feed | not rostered, not on Yahoo's list of 100 |
| Kevin Porter Jr. | MIL | on no roster | waived by Milwaukee (Mon 10/19) to reach 15; no claim or signing found in a second search | Yardbarker (Hoops Rumors), Bleacher Report, Eurohoops (10/19), ESPN feed | **rostered**: MAXEY-MUM OVERDRIVE, PG slot, Yahoo `NA` |
| Ochai Agbaji | NYK | on no roster | waived by the Knicks with Bradley and Eubanks (Thu 10/15) | BVM Sports (URL dated 2026-10-15), Yardbarker, ESPN feed | not rostered |
| Jeremy Sochan | POR | on no roster | waived by Portland (Sat 10/17); no claim found | RotoBaller, Yardbarker, Eurohoops (10/17), ESPN feed | not rostered |
| Dalton Knecht | LAL | on no roster | waived by the Lakers (Mon 10/19) after failed trade talks; no claim or signing found | TSN, Yardbarker (Hoops Rumors), ESPN feed | not rostered |
| Johni Broome | MIL | on no roster | waived by Milwaukee (~10/17) with Nance and Stephens; Wisconsin Herd expected, not reported done | Yardbarker (Hoops Rumors), BVM Sports, ESPN feed | not rostered |
| Bruce Brown | NYK | on no roster | waived by the Knicks (Sat 10/17, reported 10/18), Wiseman kept; no claim found | TSN, RotoBaller (10/18), Eurohoops, ESPN feed | **on Yahoo's free-agent list** (#100 of 100), Yahoo `NA` |

**About the dates.** The outlet pages could not be read: WebFetch of rotoballer.com, eurohoops.net, yardbarker.com and urbanmilwaukee.com failed at about 20:20Z with `getaddrinfo ENOTFOUND`, the environment's DNS. Titles, URLs and dates are therefore the search index's. A date marked "URL dated" sits in the outlet's own address; the others come from the search summary. The ESPN column is a mechanical record and does not depend on any summary. For Porter Jr. and Knecht, only one outlet's summary carries the date. Both are listed as waived on ESPN's 10/21 feed regardless.

**What the drift means today.** Assessment only; nothing was changed.
- **The two league-relevant names already score zero.** Yahoo marks Porter Jr. and Brown `NA`, and `status_feed.TIERS` scores `NA` at 0.00. On today's 100-player list Brown is one of the 10 "out". The rival's Porter Jr. contributes nothing to the week card.
- **The deck pool's team field is stale for all seven.** Bradley is the only one with a new team. If he were picked up, the week card would count Knicks games for him: it schedules by the pool's team field, so it would use NYK, not UTA. He is unrostered and not on Yahoo's list of 100 today.
- **The draft page is frozen by design** (option (b)), so these rows stay as they were at the lock. Correcting a frozen row is a different question from adding a missing one; it is on the decision sheet (D-RD-1).

## 2. What was built

1. **`data/pool_additions.csv`.** It uses the deck's schema and holds one row, Andre Drummond's, copied from deck #129 together with its note. This is where in-season players the draft pool never carried now live.
2. **`league_intake.load_pool(pool_path, additions_path)`** (`scripts/league_intake.py`).
   - Returns the deck pool's rows, then the additions.
   - A missing additions file means the deck pool alone.
   - An addition whose folded name the deck pool already carries raises an error naming it.
   - `main()` uses it, and halts with "LEAGUE INTAKE: HALT — pool additions: …" on a duplicate.
   - The record's `sources.pool` now reads `deck data/players.csv + kit data/pool_additions.csv`.
3. **`league_live.py`.** It uses `league_intake.load_pool()`, where it used to read the deck pool directly at line 252. On a duplicate it halts and leaves `league_state.json` untouched.
4. **`season_lines.py`.**
   - New `ADDITIONS` constant and a `run(…, additions_csv=None)` parameter.
   - The deck plane is the frozen snapshot followed by the additions. The columns must match, and a name already in the snapshot is refused.
   - `main()` passes the kit's file and fails loudly on a refusal.
   - The record's `inputs` gains `additions`.
   - The docstring states the rule. The zero-games identity now covers the snapshot followed by the additions' rows.
5. **`scripts/redteam/check_constants.py`.** `season_lines.ADDITIONS` joins the path names the constants check ignores, beside `KIT_CSV` and `DECK_CSV`. The registry's drift check caught it as "live constant not registered" on the first suite run (§4).
6. **`co_gm.run_league_sim` and the brief.** Added after the verification pass found the regression (§4).
   - The simulator bridge reads the names in the deck simulator's frozen pool (`sim_pool_names`). It leaves a rostered player missing from that pool out of the simulated rosters and returns his name in `absent_from_sim`. It is the IL rule (D-IS-8) applied to a player the simulator cannot play.
   - The brief records `absent_from_sim` and adds one line under the title odds: "Andre Drummond: left out of the season simulation (not in its frozen v69 pool; the rule for IL players, D-IS-8); the waiver scan still counts him."
   - The brief's lineup, waiver scan, streaming and the week card are unchanged. They read the season pool, which carries him.
7. **Tests.** Nine new; one changed.
   - `test_league_intake.PoolAdditions` (4 new):
     - additions follow the deck rows;
     - a name in both files is refused;
     - no file means the deck pool alone;
     - every addition equals its twin on the kit's own projection list (`report/projections-2026-27.csv`), so both lists carry the same line.
   - `test_season_lines.Run` (3 new):
     - additions follow the snapshot;
     - a name already in the snapshot is refused and nothing is written. This test was written after the code, green from the start;
     - the command-line run reads the kit's file and Drummond reaches `pool_season.csv`.
   - `test_daily_brief.SimulatorPool` (2 new):
     - a rostered player the simulator's pool lacks is left out and named, where the bridge used to raise `CalledProcessError`;
     - the brief's caveat line names him.
     
     Both failed first (`red_simulator.txt`).
   - `test_league_live`: the real-pull test is now unconditional. The halt branch written for the blocked deck row is gone, and it asserts the PASS: 12 teams, Flaim, rival slots beyond BN/IL, Porter `NA`, Drummond on Podz save the league's bench.

**Not changed, flagged.**
- `transactions.py` reads the deck pool plus every rostered name (`pool_names = deck pool | owners`, line 107). A rostered pickup like Drummond is covered, but an unrostered addition would not be listed. None exists today (D-TX-1).
- `report/slate.py` is the draft-era tool and reads the deck pool on purpose.

## 3. Evidence

| check | result | record |
|---|---|---|
| red before the change (kit `cec4eae` plus the new tests, deck main `80eecdf`) | 5 errors, 2 failures in 8 tests: no `load_pool` or `ADDITIONS`; `run()` refuses `additions_csv`; the CLI pool lacks Drummond; the real pull ends "LEAGUE INTAKE: HALT — 1 name(s) not in the pool … Andre Drummond (Podz save the league, BN, NYK, status -)" | `pickups-file-2026-10-21/red.txt` |
| green after | 9 of 9 (the 8, plus the refusal test written after the code) | `pickups-file-2026-10-21/green.txt` |
| deck main has no Drummond row | `git show HEAD:data/players.csv \| grep -c "^Andre Drummond,"` gives 0 at `80eecdf` | this session |
| additions row equals deck #129 | `cmp` of `data/pool_additions.csv` against #129's header plus row: equal | this session |
| additions equal the kit plane | 13 of 13 fields equal (`test_every_addition_equals_its_kit_plane_twin`) | suite |
| z-score side effect | v69 snapshot, without and then with the additions: largest change in any other player's z is 0.0 in all nine categories; top-156 set identical; snapshot order identical; Drummond #227, total value −4.458 | `pickups-file-2026-10-21/zscore_effect.json` |
| full suite | 315 of 315, twice (main's 306 plus 9) | this session |
| end to end with Drummond in the state, first run (kit copy outside the repo, deck main, `morning.py --no-fetch --seasons 200`) | **MORNING: FAIL** at "daily brief": `league_sim.py` exit 1, `AssertionError: ['Andre Drummond']`; week matchup and season deck SKIPPED. Control with the committed 10/20 state (no Drummond): brief writes | this session |
| simulator fix, red before | 2 errors: `CalledProcessError` from `league_sim.py`; no `sim_absent_line` | `pickups-file-2026-10-21/red_simulator.txt` |
| end to end after the fix (same kit copy, `--seasons 2000`) | **MORNING: PASS**, 6 steps: season lines, board, status feed, brief, week matchup (3-6-0, as this afternoon's real card), season deck (6 tabs, 0 page errors). The brief's `absent_from_sim` is ["Andre Drummond"], named under the title odds. Deck tree clean afterwards | `pickups-file-2026-10-21/morning_e2e_with_drummond_2026-10-21.json`, `brief_e2e_with_drummond_2026-10-21.md` |
| Drummond's season line, both planes | blended with his 10/20 game (24 min, 12 pts, 14 reb): FG% .470 to .462, FGA 5.0 to 5.3, FT% .622 to .612, PTS 5.8 to 6.3, REB 7.9 to 8.4. Deck plane equals kit plane in 11 of 11 cells | scratch run of `season_lines.py` |
| gates | 7 of 7 PASS (`gates.py --report` this file `--redteam` the 10/19 sweep), deck on main `80eecdf` | `gates.json` |

**Structural bands, carried for the gate.** This report quotes no simulator figure. The standing sweep's bands are carried verbatim:
- TEAM_WEEK_SHOCK is FRAGILE: +2.7 (no shock) / −3.6 (shock doubled).
- weekly_availability is FRAGILE: −2.7 (no in-sim injury discount) / +0.5 (harsher risk tier 0.65) / −1.5 (healthy plays 0.95) / +1.0 (healthy plays 0.80).

## 4. Errors and surprises, stated plainly

- **The build, as first written, would have broken tomorrow's morning.**
  - What caught it: the adversarial pass ran the whole morning chain, not only the scripts this PR touched.
  - What failed: the daily brief, a fatal step. It shells out to the deck's season simulator, which loads only its frozen `players_v69.csv` and asserts that every rostered name is in it.
  - Why 313 passing tests missed it: the suite's brief tests read the committed 10/20 state, which has no Drummond.
  - The fix is in §2 item 6. I did not know of this reader when I wrote the plan. My plan listed four kit readers of the deck pool, and this one reads the deck's own frozen snapshot through a subprocess.
- **Drummond's season line is not his additions row.** It is that row blended with his one regular-season game (10/20). That is the season lines' rule for every pool row. The box-score pull had already matched his name through the kit's projection list.

- **The constants check failed the first suite run.** The message was "season_lines.ADDITIONS: live constant not registered". It is the red team's drift check doing its job: every new upper-case name in `season_lines` must be registered or listed as a path. `ADDITIONS` is a path, so it went beside `KIT_CSV` and `DECK_CSV`. The second and third runs passed 313 of 313; that was before the simulator fix, which brought it to 315.
- **The outlet pages could not be fetched** (`ENOTFOUND` on four hosts). The drift table rests on the search index's records plus ESPN's feed, and is labelled as such in §1.
- **Kevin Porter Jr. is rostered by a rival.** I did not know this before the research; it came from the pinned 10/21 pull. Yahoo already marks him `NA`.
- **One test was not red first.** `test_an_addition_already_in_the_snapshot_is_refused` was written after the code it tests. It is stated in the test's comment.

## Watchlist

- **Tomorrow's 05:53 PT run** reads the stored prompt. The runner session holds "2 decisions open" on it.
  - With this PR merged before then, the intake finds Drummond in the additions file.
  - Without it, the intake halts on him again and the last league state stands.
- **Playwright in the runner.** Since #156 is not merged, a container without it still only skips the deck render step. Once #156 merges, a container without it fails the whole morning (owner: Global merges #156).
- **The next pickup** the intake meets without a pool row halts it, as Drummond did. The fix now is one row in `data/pool_additions.csv`, sourced like Drummond's, with no deck rebuild.
- **Drummond and the title odds.** The season simulator leaves him out, as it leaves out IL players. Podz save the league is simulated without its bench center, who is #227 by the deck engine's value with a total of −4.458. Without this PR the brief's simulation lacks him too, because it runs on the 10/20 state. Any later pickup in the additions file is left out the same way, and the brief names it.
- **Kevin Porter Jr.** If he signs with a team, Yahoo's `NA` should lift, and his pool line (MIL) would then be scored on the pool's team schedule.
- **Attack records.** This PR changes no deck commit, so the records stay CURRENT on `80eecdf`.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| D-DR-1, Drummond's row | **BUILT as (b)**; deck PR #129 to be closed | §2, §3 |
| roster drift, seven names | **RESEARCHED**, no pool change | §1, `roster_drift_2026-10-21.json` |
| #156 | **Global Operations' job** (owner 20:10Z); open at `36cdae1` when read at about 20:20Z | `list_pull_requests` |
| runner prompt | **NOT STORED** by this session; only the runner's conversation can store it | carried from `after-report-2026-10-21-merge-check.md` |

The flagged-name receipts are carried forward from the lock report, except Jeremy Sochan's, which this build re-queried (§1). The rest were not re-queried for this build (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this build (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (§1, `roster_drift_2026-10-21.json`) |

## Repeat-name market check

This build did not change the draft-room deck page, which is still deck `80eecdf` (checked with `git -C ../yahoo-fantasy-basketball log -1`, clean tree, 2026-10-21), page sha256 6a5cefea4921. The GAUNTLET report replayed it today. Its table stands, carried here verbatim.

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

1. **Merge this PR before 12:53Z on 10/22** (05:53 PT). The intake needs it to read Drummond tomorrow.
   - Default if you're silent: not merged, and tomorrow's intake halts on him as it did today.
2. **D-RD-1, the seven stale deck rows.**
   - **(a)** Record only: Yahoo's `NA` already zeroes the two in the league.
   - **(b)** A kit-side corrections file for team or status on frozen deck rows, read where the additions file is read. This is a build, on your go.
   - **(c)** Rebuild the draft page with today's rosters. This is the deck routine, and it needs today's 6 unmatched names and 1 mismatch reconciled first.
   - Recommendation: (a), until a drifted player is rostered or picked up with a real team. Bradley is the only one with a new team, and he is unrostered.
   - Default: (a).
3. **D-SIM-1, the season simulator and in-season pickups.**
   - **(a)** Leave them out of the simulation, as built here, named in the brief.
   - **(b)** A deck change, so `league_sim.py` also reads the kit's additions file. A deck commit marks the four attack records STALE until `run_attacks.py` re-runs, and the deck merge is yours.
   - Recommendation: (a) while the additions are bench-level players. Revisit when one would start for his team.
   - Default: (a).
4. **D-TX-1, `transactions.py`.** Read the additions file too, so an unrostered addition's transactions are listed. Today every addition is rostered, so nothing is missed.
   - Default: not built.
5. **Carried.** The runner prompt is the runner conversation's to store (decision 3 of the merge-check report). Global Operations merges #29 and #156.

## Bounds

**Out of scope by design.**
- The draft page and the deck pool: frozen by option (b).
- Any line, tag or status tier.
- The other players the morning runner lists as "unpooled with games". None of them is rostered, so the intake does not halt on them.
- #156 and #29.

**In scope and unverified.**
- How much leaving Drummond out of the season simulation moves the title odds: UNVERIFIABLE with the simulator as it is. It cannot play a name missing from its frozen pool. That is the measurement D-SIM-1 (b) would make possible.
- The outlet pages: ATTEMPTED-FAILED (`ENOTFOUND` on four hosts at about 20:20Z). The dates are the search index's.
- Whether Porter Jr., Sochan, Knecht or Brown signed anywhere between their last report and now: one follow-up search each found nothing. ESPN's feed shows them on no roster at its read this afternoon. A signing after that read did not check.
- Broome's Wisconsin Herd assignment: reported as expected, not as done.
- **Two duplicate checks, two folds.** The intake's refusal uses the deck's fold (`verify_rosters.norm`, which drops suffixes such as "Jr."); the season lines use their own `fold`, which keeps them. A suffix-variant duplicate ("Kevin Porter" added while the pool has "Kevin Porter Jr.") is therefore refused by the intake and accepted by the season lines. The intake runs first each morning and halts on it. Not exercised: no such row exists.
- **A waiver candidate the simulator cannot play.** If an unrostered addition were ever a waiver candidate, the title check for that add would run without him. The brief's record marks such a pair (`absent_from_sim` on the pair), but the brief's text does not. Not exercised: today every addition is rostered.

## Provenance

- **Produced by** the kit session `session_01QjgeRdpDaWgSJmGKRG8fTU` on 2026-10-21, about 20:05–20:40Z, on branch `claude/market-data-workorder-mnfi2b` restarted from `cec4eae`.
- **Governors.** plan-gate was loaded with the Skill tool after the compaction, and its full block was emitted before the first write. adversarial-verify runs before the PR.
- **Sources.**
  - Deck PR #129 (`10226ce`).
  - ESPN's 10/21 roster feed, on disk since this afternoon.
  - WebSearch (standard), 12 queries, listed in the record.
  - The pinned Flaim pull of 10/21.
- **Re-verify.**
  - `python3 -m unittest test_league_intake test_season_lines test_league_live test_daily_brief`, run from `scripts/`.
  - The morning chain: copy the kit outside the repo, put a league state with Drummond in its `data/`, and run `morning.py --no-fetch` there with `DECK_REPO` pointed at the deck.
  - `python3 report/after-reports/pickups-file-2026-10-21/zscore_effect.py`.
  - `python3 scripts/gates.py --verify --report report/after-reports/after-report-2026-10-21-pickups-file.md`.

## In plain language

**Drummond.** Kevin's team picked up Andre Drummond. Our player list was frozen on draft day, so every morning the tool stopped at his name. You chose to keep a small list of new players in the kit instead of rebuilding the draft page. That list now exists, holds Drummond, and the morning tool and the season lines both read it. Today's real league data now loads all twelve teams. Adding him changed nobody else's numbers. The next pickup is one line in that file.

**What my check caught.** Before handing this over, I ran the whole morning routine with Drummond on Kevin's team, and it failed at the daily brief. The brief's season simulator only knows the players from draft day. I changed the brief to leave such a player out of the season simulation, the way injured-list players are already left out, and to say so in the brief. The whole morning now passes. Without this fix, merging would have broken tomorrow morning.

**The seven names.** Six were cut by their teams since draft day, and Tony Bradley moved from the Knicks to the Jazz. Two of them matter in the league:
- one rival rosters Kevin Porter Jr.;
- Bruce Brown sits on the waiver list.

Yahoo already marks both as not active, so the tool already counts them as zero. Nothing in the player list was changed, as you asked.

**What I need from you.** Your word to merge this PR before tomorrow's 5:53 am Pacific run.
