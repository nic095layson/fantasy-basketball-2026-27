# What Tuesday found, and whether the model got better — 2026-10-22

Pull window: 2026-10-21 → 2026-10-22. No league or market pull and no web search. This report reads only what is already committed: the day's after-reports, the morning runner's records, and the git history of both repositories.

**Your request** (2026-10-22, 05:25:46Z by the session transcript, `day-findings-2026-10-22/request.json`; verbatim): "Provide thorough, detailed report of findings from today, if data model has improved at all, in plain language please"

**What "today" means here** (stated to you before the work): Tuesday 2026-10-21, Pacific time. That is 07:00Z on 10/21 through this report, about 06:00Z on 10/22.
- 17 after-reports were committed in that window.
- Three more were committed on Monday evening, Pacific (the red-team audit, the corrections and the Council fixes). They are used only as background.
- Commit times are in `day-findings-2026-10-22/report_commit_times.txt`.

**How it was built.**
- **Sources:**
  - the 20 after-reports, read from their committed text;
  - both repositories' merge history since Monday 18:00 PT (`git_kit_first_parent.txt` and `git_deck_first_parent.txt`, beside this report);
  - the morning runner's commit `847748e` of 20:46 PT, found while checking this report (§3). Its records are pinned in `day-findings-2026-10-22/runner-2026-10-22/`.
- **Every number traced:** `day-findings-2026-10-22/trace.py` pulls every number out of this report and checks that each appears in a cited source. Counts this report makes itself are re-computed by the script from the same files.
- **What "the data model" means** (assumption A2, stated before the work): the inputs and rules that feed the board, the waiver scan, the week card and the title odds. Plumbing (checks, guards, the morning runner) is reported separately in §5.
- **Four labels** in §2:
  - **IN USE**: merged, and a morning run has used it;
  - **PARTLY IN USE**: it ran, but its input arrived incomplete;
  - **BUILT, NOT IN USE**: on main or on a draft, but nothing you see reads it yet;
  - **UNPROVEN**: no prediction has yet been checked against what happened.

**Headline, in plain language.**
- **Yes, the model improved, in what it is fed and in the rules it applies.** It is not yet in results you would notice.
  - **One hand-set guess was replaced by a measurement.** The per-game variation behind every head-to-head probability is now fitted from 10,332 rows of last season's game logs. The fitted values are 1.24–1.43 times the old hand-set ones.
  - **Four hand-set rules were corrected:** recovery and `out-*` players now count as zero in the simulator, Yahoo's "D" means doubtful (0.25), and six injury-tagged rows lost 6 games each. The first two merged late Monday night and were measured today.
  - **The pool now holds in-season pickups.** Andre Drummond is the first.
- **What it changed in decisions: very little.**
  - On the 10/21 records, one waiver swap stopped being positive: Holiday-for-Braun went from +0.0047 to −0.0042.
  - Your title odds moved by less than the sampling noise, and none of these changes moved a season-board rank.
  - The one larger move was on draft-day rosters. The recovery rule moved seat 10's draft-day title share from 21.1 % to 23.3 % and from 21.3 % to 24.1 %, on the two reference seeds.
- **Everything merged today has now run once, but on part of a day's games.**
  - The runner ran a morning at 20:43 PT on your pasted prompt, on main `af625a8` (§3).
  - At that hour only 8 of Tuesday's 11 games were final; the three West Coast games were not.
  - The run still passed, its records are dated 2026-10-22, and the live Season Deck showed that partial picture until the next run.
  - **Update, 05:54 PT 10/22:** the scheduled run rebuilt everything on all 11 games and republished. Its week card still shows the mid-game Yahoo figures as "to date", and my explanation of the 21-stat gap held for your side only (§3).
  - The same run was Yahoo-through-Flaim's first live morning:
    - Yahoo's matchup came back, so the week card's to-date column is Yahoo's;
    - only 4 of 12 rosters and no free-agent list arrived (a Yahoo sign-in refresh error), so rosters came from FantasyBot.
  - The runner's stored prompt is still the old one, and it has no Flaim step. The 05:53 PT scheduled run reads that stored text unless you store the new one.
- **Unproven, all of it.** No prediction has yet been scored against an outcome.
  - Week 1 ends 10/25 and is the first that can be scored: the pre-week card said 60.6 % to win; the week card projects 3–6–0.
  - The injury calibration says INSUFFICIENT until about 2026-11-17.
- **Newly connected tonight:** the title-odds simulation still runs on the draft-day player lines (`players_v69.csv`), not the in-season lines. In-season games, tags and pickups never reach it (§4).
- **Errors.** No arithmetic error anywhere, which is Monday night's pattern again. The mistakes were about what runs, what reads which file, which folder a command ran in, and pass lines that did not check. Most were caught before they reached you; seven reached you, a live page or a merged file (§6).

---

## 1. Roster changes and the day's merges

No roster, projection line or tag was changed by this report. The roster moves the day's reports recorded (`after-report-2026-10-21-flaim.md` §1, Yahoo through Flaim, single source) and tonight's run recorded (`runner-2026-10-22/morning_report_2026-10-22.md`) are not repeated here.

**What merged on Tuesday, Pacific time** (from `git_kit_first_parent.txt` and `git_deck_first_parent.txt`):

| repo | PRs merged | source |
|---|---|---|
| kit, 10/21 PT | #149, #151, #152, #153, #150, #154, #157, #155, #158, #156, #159, #160, #161, #162, #163 (15) | `git_kit_first_parent.txt` |
| deck, 10/21 PT | #131, #130 (2) | `git_deck_first_parent.txt` |
| kit, Monday night | #146 (18:36 PT), #147 (19:16 PT), #148 (22:26 PT) | `git_kit_first_parent.txt` |
| deck, Monday night | #126 (18:36 PT), #127 (22:27 PT), #128 (23:14 PT) | `git_deck_first_parent.txt` |

Still open, waiting on your word (`open_prs.json`, read tonight):
- kit #164 (older seasons' totals) and kit #166 (Hunter), both drafts. Both add to `OPEN.md` and `report/pull-log.md`, so whichever merges second needs main merged into it first, keeping both sides.
- kit #165, "Season: daily records", the runner's draft for tonight's records (§3).
- The old drafts: kit #3 and #4, and deck #5.

**Monday night, the background.**
- **The red-team audit:** the arithmetic is clean, 1,800 of 1,800 cells by an independent implementation, and "the system is reliable at computing and unreliable at knowing what actually runs" (redteam-audit headline).
- **The corrections:** three defects were one pattern, "statements the system makes about itself, with no live counterpart", and a claim-against-reality checker was built (corrections headline).
- **The Council fixes** built that checker into a gate, added the run ledger, and set recovery to 0.0. A separate attacker rebuilt the simulator from its specification and agreed on every deterministic number (council-fixes headline).
- Today's work started from there.

**The 20 reports, by commit time** (from `report_commit_times.txt`):

| source report | committed (PT) | window |
|---|---|---|
| corrections | 10-20 18:36 | Monday night, background |
| redteam-audit | 10-20 19:16 | Monday night, background |
| council-fixes | 10-20 22:26 | Monday night, background |
| proceed | 10-21 07:39 | today |
| gauntlet | 10-21 08:39 | today |
| deck-patch | 10-21 08:47 | today |
| board-test | 10-21 09:22 | today |
| deck-render | 10-21 09:42 | today |
| week-matchup | 10-21 10:28 | today |
| independent-audit | 10-21 10:43 | today |
| flaim | 10-21 11:27 | today |
| merge-check | 10-21 12:38 | today |
| pickups-file | 10-21 13:51 | today |
| zscore-assessment | 10-21 14:18 | today |
| gscore-column | 10-21 15:27 | today |
| risk-rows | 10-21 17:36 | today |
| gp-reconstruction | 10-21 18:10 | today |
| season-cv | 10-21 20:24 | today |
| flaim-history-totals | 10-21 20:32 | today (draft #164) |
| hunter-override | 10-21 21:11 | today (draft #166) |

## 2. Did the data model improve? Item by item

| change | what it fixes | label | what it changed (measured) | source report |
|---|---|---|---|---|
| Per-game variation fitted from game logs (`arena.SEASON_CV`; deck #130, kit #163, merged 20:06 and 20:25 PT) | the hand-set variation behind every head-to-head win probability | IN USE (first run 20:43 PT) | on the 10/21 records: expected categories per week 5.2996 before, 5.2251 after; Portis-for-Braun +0.0304 before, +0.0257 after; Holiday-for-Braun +0.0047 before, −0.0042 after; title 24.48 / 23.72 before, 24.69 / 22.94 after, inside the binomial error of about 0.43 per seed | season-cv §headline |
| Recovery players count 0.0 in the simulator (deck #127, Monday 22:27 PT) | the simulator priced them at 0.60 while the board excluded them | IN USE | draft-day title share 21.10 / 21.33 before, 23.27 / 24.07 after; in-season numbers unchanged, because all recovery players are on IL | proceed §3; council-fixes §headline |
| `out-*` players count 0.0 in the simulator (deck #128, Monday 23:14 PT) | they fell through to the healthy 0.88, against the function's own comment | IN USE | no current number: no `out-*` player is on a league roster | proceed §2 |
| Six injury-tagged rows lose 6 games (#161, 19:56 PT) | seven rows got their games in July, before their tags, and the −6 rule never reached them | IN USE | preseason board 8 of 200 rows change, all small; season board ranks unchanged; `pool_season.csv` byte-identical | risk-rows §headline; gauntlet §4 |
| In-season pickups file, `data/pool_additions.csv` (#158, 14:01 PT) | the morning intake halted on any player the frozen pool lacked | IN USE | Drummond reaches the pool; no other player's z moves (largest change 0.0); he ranks #227 | pickups-file §2–§3 |
| Week card on the real schedule (#155, 12:59 PT) | the pre-week card gives every player 3.5 games | IN USE | week 1 projected 3–6–0; the opponent has 41 player-games against your 35; tonight's run still projects 3-6-0 | week-matchup §headline, §4; `runner-2026-10-22/morning_report_2026-10-22.md` |
| Yahoo's "D" means doubtful, 0.25 (in #155) | an unknown letter halted the Flaim intake | PARTLY IN USE | Stewart scored at 0.25 on the 10/21 list (87 scored + 10 out + 0 unknown + 3 not projected); tonight the Flaim rosters arrived 4 of 12, so the letters came from FantasyBot | merge-check §2–§3; `morning_report_2026-10-22.md` |
| Yahoo's own week totals, free-agent list, rosters and letters through Flaim (A–D, in #155) | rebuilt figures and FantasyBot rosters stood in for Yahoo's | PARTLY IN USE | on the 10/21 pull, Yahoo's totals equal the box-score rebuild on all 11 stats; tonight the matchup came back but 4 of 12 rosters and no free-agent list did; the stored prompt has no Flaim step | flaim §headline; `morning_report_2026-10-22.md`; `stored_prompt_read.json` |
| G-score column (#160) | z-scores treat a volatile category like a steady one | BUILT, NOT IN USE (comparison only, by design) | rank correlation 0.98 with z; 44 of 156 move 10 or more places; Dyson Daniels 34 to 64, Paolo Banchero 122 to 94 | gscore-column §headline |
| Hunter's tag cleared in the season tools (draft #166) | an old eye-surgery tag on a healthy player | BUILT, NOT IN USE | 1 of 336 rows changes; nothing you would see today, because his value is −4.21, below zero | hunter-override §headline |
| Real games behind 2025-26's weeks (#162) | Yahoo's "Games Played" counter was assumed to be real games | BUILT, NOT IN USE | 41 of 44 team-weeks reproduce Yahoo's totals exactly; the counter equals real games in only 3 of 44 | gp-reconstruction §headline |
| Older seasons' weekly totals (draft #164) | one season of weekly data | BUILT, NOT IN USE | 65 weeks, 372 matchups; 3,348 of 3,348 category results and 36 of 36 standings records reproduce | flaim-history-totals §1–§2 |
| Injury calibration (#149) | the injury discounts were never checked against games played | UNPROVEN | INSUFFICIENT until about 2026-11-17; tonight's line says the same | gauntlet §headline; `morning_report_2026-10-22.md` |

**Verdict, item by item.**
- **Improved and in use:** the fitted variation, the recovery and `out-*` rules, the six game counts, the pickups file and the week card. That is 6 of the 13 rows.
- **Partly in use:** Yahoo through Flaim and its "D" letter. They ran live for the first time tonight, with an incomplete pull.
- **Built, not yet in use:** Hunter's override, the real-games series, the older seasons, and the G-score column (by design).
- **Unproven: all of it.** None of these changes has yet been checked against a real outcome.
  - The model now has better inputs and fewer known-wrong rules.
  - Whether its predictions are better can first be measured when week 1 ends (10/25), and when the calibration has enough games (about 11/17).

**What the measurements say about the model's foundations** (zscore-assessment §headline, §4):
- **Z-scores rank players; they do not decide swaps or title odds.**
  - The board, the lineup, streaming and the waiver shortlist rank by z.
  - The waiver swap value and the title odds use head-to-head category-win probabilities.
  - Scoring every pooled free agent (153) instead of the top 40 found the same two positive swaps, so the shortlist hides nothing.
- **Your title odds barely care about the variation's size.** At ×1.5 and ×2.0 the title share moved −0.36 and −0.61 points, against noise of 0.54: ROBUST at every step.
- **The paper you uploaded agrees with the logs.**
  - In its simulated leagues, a G-score drafter won 21.4 % against an 8.33 % baseline.
  - Fitted on our logs, steals get the smallest weight, 0.47 of their z, against the paper's 44 %.

## 3. Tonight's run: everything merged today, on part of a day

The runner's commit `847748e`, "Morning run 2026-10-22", landed on `season/daily` at 20:46 PT on 10/21. EVIDENCE, from its records pinned in `runner-2026-10-22/`:
- **When and on what.**
  - T0 was 2026-10-22T03:43:33Z, which is 20:43 PT on 10/21.
  - It merged main `af625a8` into `season/daily`, so it ran every change in §2 marked IN USE.
  - It was dated 2026-10-22 because `morning.py` takes the container's UTC date. The runner said so itself in its report.
- **Box scores for 10/21.**
  - ESPN listed 11 events and 8 final (`box_2026-10-21_sources.json`). The schedule has 11 games that day (`schedule_2026-10-21.csv`).
  - The three missing are the West Coast games: GSW at LAL, PHO at POR, SAC at LAC.
  - The step still printed `BOX PULL: PASS — 2026-10-21: 8 games`.
- **The week card's to-date column was Yahoo's.** It differs from the box-score rebuild on 21 stats, and Yahoo is higher on every one (`week_card_to_date.json`).
  - **INFERENCE:** Yahoo's live totals included the three West Coast games then in progress, and the rebuild did not.
    - Both teams roster players in those games (`west_coast_players.json`): yours, Miles Bridges (PHX) and Yaxel Lendeborg (GSW), active; theirs, Darius Acuff Jr. (SAC) and Gui Santos (GSW).
    - On the 10/21 morning pull, with every game final, the two agreed on all 11 stats (flaim §headline).
  - The card's line reads "to date 2 day(s), 0 missing", so nothing on it says a day was unfinished.
- **Flaim.**
  - 4 of 12 roster calls returned data; the others failed on "Yahoo token refresh is already in progress", plus one 502.
  - `get_free_agents` and `get_league_info` failed the same way. `get_matchups` returned.
  - So rosters came from FantasyBot (14 of 14 calls), and the pickup scan had no Yahoo list.
- **What it showed:**
  - title 23.8 % ± 0.6 (2 runs × 10,000), with the bands in § Bounds;
  - no positive waiver pair of 520 ("stand pat"); on the 10/21 records, Portis-for-Braun was the one positive pair (season-cv §headline);
  - 152 season lines moved by 0.25 or more;
  - calibration INSUFFICIENT;
  - deck render 6 tabs, 0 page errors, published as version 1792640745-5b2e.
- **The stored prompt is unchanged.** `updated_at` is 2026-10-21T14:48:41Z, read tonight, and its step 3 is "FantasyBot pull" with no Flaim step (`stored_prompt_read.json`). So tonight's run used your pasted text. The 05:53 PT scheduled run reads the stored text.

**What this means (INFERENCE, as first written on the evening of 10/21).**
- The live Season Deck, the brief and the season lines now rest on 8 of Tuesday's 11 games.
- The 05:53 PT run will also be dated 2026-10-22 (the same UTC rule). It should re-pull 10/21 with all games final and rewrite these records. Watch that its box line says 11 games (Watchlist).

**Update, 2026-10-22 05:54 PT: the scheduled run (`51cf6b3`), pinned in `runner-2026-10-22/*_0554PT.*`.** EVIDENCE:
- **The partial day is replaced.**
  - ESPN listed 11 events and 11 final; the box record holds 11 games from two outlets (`box_2026-10-21_sources_0554PT.json`).
  - The deck was republished as version 1792673766-2b1d, render 6 tabs, 0 page errors. This session's render check of the live page agrees.
- **The week card still shows the 03:43Z Yahoo figures as "to date".**
  - The stored prompt made no Flaim call, so the card read the same Yahoo pin as the evening run. Both runs record the same sha256, 4900ea890f89.
  - The card says "rebuild differs on 13 stat(s)", but nothing on it says the Yahoo figures were read mid-game.
- **The inference above held for your side only.** Against the complete rebuild, the 13 differences split 6 and 7 (`week_card_to_date_0554PT.json`):
  - **Your side:** the rebuild is higher on all 6 (PTS 210 against Yahoo's 203). That is what unfinished games at 03:43Z predict.
  - **The opponent's side:** Yahoo's mid-game figure is higher than the complete rebuild on all 7 (FGA 149 against 139).
    - Unfinished games cannot explain that.
    - The rebuild undercounts the opponent for some other reason; the card's method M2 (current roster, ten-slot rule) is the first candidate.
    - Not diagnosed here.

**Correction, 2026-10-22, after the 14:15Z on-demand run: the opponent-side gap was one dropped box score, not the card's method.** EVIDENCE, pinned in `correction-2026-10-22/`:
- **The cause.** ESPN's box score names the opponent's player "Darius Acuff Jr."; the kit's file names him "Darius Acuff". The box pull matched names by spelling and the alias table only, so his 10/21 line was left unmatched (`recon.json`), and the week card's rebuild never counted it.
  - His line: 5-24 FG, 2-5 FT, 0 3PM, 12 PTS, 3 REB, 3 AST, 3 STL, 0 BLK, 4 TO.
- **It is the whole gap.** The 05:54 PT rebuild of the opponent plus that line equals Yahoo's complete totals from the 14:15Z Flaim pull on all 11 stats: FGA 139 + 24 = 163 (`week_cards.json`).
  - The 14:15Z run's own card (`2f2aea8`) differs from Yahoo on 9 of the 11 stats, the ones where his line is not zero. Your side agrees on all 11.
- **The card's method (M2) was not the cause; the "first candidate" named above was wrong.**
  - Yahoo's daily lineups for both teams on 10/20 and 10/21 (Flaim, by date), summed over the box scores with names matched suffix-free, give Yahoo's totals on all 11 stats for each side (`recon.json`).
  - No benched or IL player of either team played on those days, so the ten-slot rule had nothing to choose.
- **A second effect came later, and that one is M2's.**
  - The opponent dropped Gui Santos after his 10/21 game. The drop first shows in the 14:44Z run (`e7b69bb`), not in the 14:31Z one (`21d815d`) (`league_moves.json`).
  - The card rebuilds from today's roster, so his line (5-10 FG, 12 PTS, 5 REB) falls out. With the name fix applied to the 14:44Z records, the opponent's gap is exactly that line (`name_fix_week_card.json`).
  - Whether the card should read Yahoo's daily rosters instead is a separate decision for you.
- **The fix** for the names is kit draft PR #168, not merged (`pr_168.json`). This answers the opponent-side item left open in § Bounds; the text above it is left as first written.

## 4. Gaps found, still open

1. **The title odds run on draft-day lines.**
   - **EVIDENCE**, read tonight from the code on main:
     - `scripts/co_gm.py` lines 162–177 hand the deck's `league_sim.py` the tag `v69`;
     - `league_sim.py` line 33 loads `arena/results/players_v69.csv`, the frozen lock file.
   - So the title-odds simulation never sees an in-season line, an in-season tag or a pickup. It does get the fitted variation, through a flag (season-cv §headline).
   - Two reports recorded this for one player each: Drummond is left out (pickups-file §2 item 6), and Hunter's old tag stays (hunter-override §3).
   - One report said the opposite. The risk-rows report says `pool_season.csv` is read by "the title-odds simulation" (risk-rows §headline). That is wrong.
     - Its conclusion still holds, because the lock file did not change either.
     - The waiver scan, the week card and the brief's lineup do read the season pool.
   - How much this moves your title odds today is not measured. It grows as season lines move away from preseason lines.
   - Decision D-DAY-1.
2. **The box pull passes on an unfinished day.**
   - It records ESPN's "final" count (8 of 11 tonight), but its PASS line and the week card's "0 missing" do not use it (§3).
   - A run before the last game ends builds every season line on part of a day, and nothing says so.
   - Decision D-DAY-2.
3. **Records are dated by the container's UTC date.** An evening run on Pacific Tuesday writes Wednesday's records (§3). Decision D-DAY-3.
4. **Three injury discounts disagree (D-PM-4).**
   - For a risk-tagged player: the deck board ×0.78, the simulator ×0.852, the kit board ×0.918 on average.
   - Which one is right needs realized games. The first possible verdict is about 2026-11-17 (proceed §4; gauntlet M2).
5. **The weekly model gives every player 3.5 games.**
   - That flat figure sits behind the pre-week card and the waiver swap value (week-matchup §4; zscore-assessment §2).
   - The real week 1 is 41 games against 35. That is why the pre-week card said 60.6 % and the week card projects 3–6–0.
   - Changing it touches the title odds: a separate work order on your go (week-matchup decision 5).
6. **The model's weekly spread is too narrow.**
   - Your team's real week-to-week spread in 2025-26 was 1.53 to 2.46 times what the model implies.
   - The fitted variation explains part of that, not all. Schedule mix, unequal players, roster changes and games-played errors are not yet split out.
   - A spread that is too narrow makes win probabilities too confident (zscore-assessment §headline).
7. **Yahoo's games counter is not real games.**
   - It matches in only 3 of 44 team-weeks, off by −7 to +8, and you decided not to fit on it (D-GP-2).
   - So the games and shock model stays hand-set, and TEAM_WEEK_SHOCK stays FRAGILE (§ Bounds).
8. **The runner's stored prompt.** It can be changed only inside the runner's own conversation; you are doing it there (stored-prompt read, §3).
9. **The 2021-22 league was a 10-team points league.** Any multi-season analysis needs the era and format check first (flaim §3).

## 5. Plumbing: what got sturdier

None of this changes a number. It changes whether the numbers you see are the ones the tools computed.

| what | why it matters | source report |
|---|---|---|
| `--since` guard on the transcript readers (#151) | a persistent runner could have published yesterday's rosters dated today; a run dated 2099-01-01 passed on the 10/20 pull before the guard; tonight's run used it | gauntlet §headline; `morning_report_2026-10-22.md` |
| Persistent morning runner that pushes | it committed `8ba6534` and opened #150 on 10/21, and `847748e` tonight; the old routine is disabled | gauntlet §headline; `commit.txt` |
| Deck builds with an optional input missing (#152) | any morning without a matchup pull crashed the deck step | deck-patch §2 |
| Movers rows fixed, and a render check before any page is written (#154) | the live Season Deck lost its tabs on 10/21; tonight's page rendered 6 tabs, 0 page errors | board-test §3; deck-render §headline; `morning_report_2026-10-22.md` |
| Board test no longer reads live data (#153) | it would have failed on every in-season record | board-test §2 |
| Morning preflight, claim-receipts lint, deck replay (#156) | the run checks its preconditions first (tonight: 4 checks, PASS); the lint is advisory (precision 3 of 7) | independent-audit §headline, §3 |
| Attack records current on the live engine | 5 CURRENT, 0 STALE on 048efb6; arithmetic re-implementation differences 0.0 | season-cv §3 |

## 6. Errors and mis-truths, stated plainly

Taken from each report's own errors section, plus four found while writing this one (marked "this report"). One incident told in two reports is listed once.

| # | what was said or done | what was true | caught by | source report |
|---|---|---|---|---|
| **A** | **Claims about what runs, or what reads what** | | | |
| A1 | "The recovery change changes nothing either way" (said to you) | it moved seat 10's draft-day title share 21.1 % to 23.3 % and 21.3 % to 24.1 % | decomposing a surprise | proceed §3 |
| A2 | The red-team audit's correction: "the board" applies the injury tier and the games factor together | no board does; the deck board is tier only and the kit board games only; a finding had been withdrawn for a false reason (Monday's 13th error) | reading the code | proceed §4 |
| A3 | `SEASON DECK: PASS` and the publish step's six-tab check, on a page that could not draw its tabs | the check read the text, not a render; the live page lost its tabs | your question | board-test §3 |
| A4 | The pickups plan listed four readers of the deck pool | a fifth, the simulator's frozen-snapshot reader, would have failed the next morning's brief | running the whole morning | pickups-file §4 |
| A5 | Preflight made playwright fatal | that would have stopped a whole morning over one step; removed the same evening | the merge check | independent-audit §3 |
| A6 | Hunter: the deck route "reaches the season tools"; the override "reaches the title odds" (shown to you as options) | neither is true; both corrected before the build | re-reading the readers | hunter-override §4 |
| A7 | "`pool_season.csv`, which … the title-odds simulation read" | the simulation reads `players_v69.csv` | this report, §4 | risk-rows §headline |
| A8 | Deck README (#131), schema line: `gp` is "player-games actually played" | its own 10/22 correction, lower in the same file, says it is not; the line was not amended | this report | deck `weekly_matchups_2025-26_README.md` |
| A9 | `BOX PULL: PASS — 8 games`; week card "0 missing" | ESPN listed 11 events, 8 final; the live deck and brief rest on part of a day | this report, §3 | `runner-2026-10-22/box_2026-10-21_sources.json` |
| **B** | **Checkers broken before the data** | | | |
| B1 | Games cross-check read column `g` | the column is `gp`; it failed 222 of 222, then 222 of 222 matched | a check that fails everything | gp-reconstruction §4 |
| B2 | Game-log parser said it skipped repeated headers | it kept 1,183 header rows; no figure came from that parse | the first weights run | zscore-assessment §5 |
| B3 | First preflight spec looked for `hoops.py` at the deck root | it failed a correctly set-up kit; fixed, with a pass control | its own test | independent-audit §2 |
| B4 | Board test compared the season board to the preseason board | true only until the first regular-season game | merging #150 | board-test §2 |
| B5 | `rt_math.py` hard-codes the deck path and ignores `DECK_REPO` | it first reproduced the old record; flagged, not fixed | a stale engine line | season-cv §4 |
| **C** | **Commands with side effects, or run in the wrong place** | | | |
| C1 | Prompt text passed through an unquoted heredoc | it started a real morning run at 18:10Z; stopped and restored | the hung command | flaim §4 |
| C2 | An end-to-end check meant for a copy (`rsync` missing, commands joined with `;`) | it ran in the main checkout and rewrote eleven records; restored before any commit | `git status` | zscore-assessment §5; gscore-column §4 |
| C3 | First gate run with the deck checkout on another branch | attack records read STALE; 2 of 7 failed; with the deck on main, 7 of 7 pass | the gate | merge-check §4 |
| C4 | Pool exercise first ran on the 10/20 state | 86 instead of 87 scored; only the second run is quoted | re-reading the input | merge-check §4 |
| C5 | Sweep's first launch | did nothing (`time: command not found`) | no output | season-cv §4 |
| C6 | Hunter's "after" run, started in parallel | exited 1 with an empty log; rerun alone passed; cause not found | the exit code | hunter-override §4 |
| **D** | **Predictions that missed, caught at the phase boundary** | | | |
| D1 | Seat 10's reference to move less than a point | it moved +2.2 and +2.7 | the run | proceed §3 |
| D2 | The games test to overcount | it undercounted, bias −3.25 | the run | gp-reconstruction §4 |
| D3 | 35 ledger rows after the merge | 43 | counting | board-test §2 |
| D4 | The weekly spread gap "shows the variance is too small" | schedule mix also drives it | checking the cause | zscore-assessment §5 |
| D5 | Hunter's override would show today | nothing visible moved today: brief and board byte-identical before and after (`compare.json`) | the before/after run | hunter-override §4 |
| **S** | **Slips** | | | |
| S1 | Season-CV report: "the 6:00 PT morning run" | the run is at 05:53 PT (12:53Z) | this report | season-cv §4 |
| S2 | "Jaren Jackson Jr." in the GAUNTLET report | the projections file spells it without the period; the first lookup missed him | the script | risk-rows §5 |
| S3 | Drummond's first method line: attempts stay the kit's | the blend's rule rescales them; corrected before the run | re-reading the rule | merge-check §4 |

**Arithmetic: none found.** The checks behind that:
- Monday's spec-only re-implementation agreed on 1,800 of 1,800 cells (redteam-audit §1).
- The simulator's separate attacker agreed bit-for-bit on 2,174 deterministic numbers (council-fixes §headline).
- On tonight's engine, `048efb6`, the known-answer differences are 0.0 and the simulator re-implementation passes (season-cv §3).
- The older-season checker failed a planted wrong turnover total before it passed the real files (flaim-history-totals §2).

**The pattern.** It is Monday night's pattern again: the maths is clean, and the misses are about whether something runs, which file it reads, where a command runs, and pass lines that report success without checking the thing that matters (A3, A9).
- **Most were caught before they reached you.** They were caught by running the whole morning chain, by a check that fails everything, by a planted wrong answer, or by a second run.
- **Seven reached you, a live page or a merged file:**
  - A1, said to you;
  - A6, your options, corrected before the build;
  - A3, the live page on Tuesday morning;
  - A9, the live page tonight;
  - A7, A8 and S1, merged text, corrected only here.

## Watchlist

- **The 05:53 PT run (12:53Z) reads the stored prompt, which has no Flaim step,** unless you store the new one first. It will also be dated 2026-10-22. Check that:
  - its box line says 11 games for 10/21;
  - it rewrites tonight's partial records and republishes the deck.
  - *Observed at 05:54 PT:* both happened (`51cf6b3`, §3 update). The week card's to-date column still reads the 03:43Z Yahoo pin.
- **Week 1 ends 10/25.** It is the first chance to score a prediction: the pre-week 60.6 % against the week card's 3–6–0.
- **Attack records** are CURRENT on 048efb6. Any deck commit marks them STALE until the attacks are re-run.
- **#164 and #166:** the second to merge needs main merged in first.
- **The calibration's first possible verdict** is about 2026-11-17.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| Hunter's tag (D-RR-1) | **BUILT on draft PR #166**; merging is yours | `after-report-2026-10-22-hunter-override.md` |
| older seasons' weekly totals (D-GP-3) | **DONE on draft PR #164**, not merged | `after-report-2026-10-22-flaim-history-totals.md` |
| the runner's stored prompt | **OPEN**: still the 10/21 14:48:41Z text, read tonight; changeable only inside the runner's own conversation | `runner-2026-10-22/stored_prompt_read.json` |
| title odds on draft-day lines | **OPEN, newly connected** (D-DAY-1) | §4 item 1 |
| box pull on an unfinished day | **OPEN, new** (D-DAY-2) | §3; §4 item 2 |

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21 (`after-report-2026-10-21-pickups-file.md` §1). The rest were not re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (§1, `roster_drift_2026-10-21.json`) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck 048efb6, the page the GAUNTLET report replayed on 10/21. Its table stands, carried here verbatim.

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

| ID | Question | Default if you say nothing | Where |
|---|---|---|---|
| D-DAY-1 | Title odds on draft-day lines: (a) leave it, and say so in the brief under the title odds; (b) measure it: how far today's season pool sits from `players_v69.csv`, line by line, with no change; (c) a deck work order so `league_sim.py` reads the season pool, which re-stamps the attack records and needs the sweep re-run. Recommendation: (b) first, because it is cheap and tells you whether (c) is worth it | nothing changes; the title odds keep reading the lock file | §4 item 1 |
| D-DAY-2 | The box pull on an unfinished day: (a) leave it, since a run at 05:53 PT normally finds every game final; (b) the box pull prints "N of M final" and the week card names an unfinished day, red-first, a kit build on your go; (c) as (b), and the season lines skip a day until every game is final. Recommendation: (b) | nothing changes; an evening run builds on part of a day, unlabelled | §3; §4 item 2 |
| D-DAY-3 | Record dates: (a) leave the container's UTC date; (b) `morning.py` defaults to the Pacific date the league runs on, a kit build on your go. Recommendation: (b) | an evening run keeps writing tomorrow's date | §3; §4 item 3 |
| D-DAY-4 | `rt_math.py`'s hard-coded deck path: a one-line fix to honour `DECK_REPO`, on your word | not fixed; anyone re-running A-1 must keep the sibling checkout on the live deck | §6 B5 |
| D-DAY-5 | Deck README schema line (A8): one line amended to match its own correction, on your word. It is a deck commit, so the attack records read STALE until re-run | not changed; the correction note below it stands | §6 A8 |
| carried | merge #164 and #166; store the runner's prompt; the 3.5 games (week-matchup decision 5); old drafts kit #3 and #4 and deck #5; delete the old routine after 10/28 | as each report states | the cited reports |

## Bounds

**Out of scope by design:**
- No engine run, no re-measurement and no fix. This is a report on records.
- A1–S3 are listed, not re-litigated. Each report's own text is the record.

**In scope and unverified:**
- **How much the draft-day lines move today's title odds** (§4 item 1). NOT-ATTEMPTED: measuring it is decision D-DAY-1 (b). The finding itself does not depend on the size.
- **Why Yahoo exceeds the rebuild on 21 stats tonight** (§3). Labelled INFERENCE: three games not final.
  - Comparing tonight's Yahoo figures game by game was not attempted.
  - Tested by the 05:54 PT run, against a complete rebuild: it holds for your side (6 of 6) and fails for the opponent's (7 of 7 still lower in the rebuild).
  - So the opponent-side gap has another cause, not diagnosed (NOT-ATTEMPTED). A fresh Yahoo pull with every game final would separate the two.
- **Whether every report's errors section is complete.** Each report wrote its own; this report adds four it found (A7, A8, A9, S1). A full re-audit was not attempted.
- **How tight the trace is.**
  - `trace.py` finds each number in *a* cited source, not necessarily in the one named beside it. A distinctive figure (5.2996, #165) is effectively pinned; a small number like 3 is not.
  - The counts this report makes itself are bound to their computed values.
  - Five planted wrong figures all failed it (`plants.txt`). The first version caught only 2 of 4, so the binding checks were added and the plants re-run.

**Bands.**
- Title shares quoted above from 10/21 reports (21.1 %, 23.3 %, 23.77 %, 24.20 %) were made on engine 80eecdf and quoted with that sweep's bands in their own reports.
- The standing sweep record is now on engine 048efb6: 6,000 seasons × seeds 2026 and 2027, sampling error 0.535, baseline 23.18 / 23.30 against the reference 23.06 / 23.25.
- Its bands, which also go with tonight's 23.8 % ± 0.6:
  - TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared shock) / −3.4 (shock doubled).
  - weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy plays 0.95) / +0.9 (healthy plays 0.80).
  - PCT_MIX_INFL is SENSITIVE: −1.28 at inflation 1.30. The rest are ROBUST (season-cv §3).

## Provenance

- **Produced by** session `session_01QjgeRdpDaWgSJmGKRG8fTU` on 2026-10-22, from your 05:25Z request, on branch `claude/day-report-2026-10-22` from main `af625a8`.
- **Governors.**
  - plan-gate was loaded with the Skill tool after the compaction, before the first write. Its block was stated before the work: the window, the 20 sources and five criteria.
  - The runner's commit was added as a source mid-work, when the check of this report found it (§3).
  - adversarial-verify is loaded before delivery.
- **Records beside this report**, in `report/after-reports/day-findings-2026-10-22/`:
  - `git_kit_first_parent.txt`, `git_deck_first_parent.txt` and `report_commit_times.txt`, with the commands that wrote them in `commands.txt`;
  - `open_prs.json` (both repos' open PRs, read tonight) and `request.json` (your request's time, from the session transcript);
  - `runner-2026-10-22/`: the morning report, the week card's to-date block, the box record's sources block, the 10/21 schedule rows, the commit line and the stored-prompt read;
  - `trace.py`, which writes `trace.json`.
- **Re-verify:**
  - `python3 report/after-reports/day-findings-2026-10-22/trace.py` (exit 0: every number in this report found in a cited source);
  - `python3 scripts/gates.py --verify --report report/after-reports/after-report-2026-10-22-day-findings.md`.

## In plain language

**Did the model get better today?** Yes, but quietly.
- **What it's fed got better.** It used to guess how much a player's nightly numbers bounce around. Now it measures that from last season's real games, and the real bounce is a quarter to almost half again bigger than the guess.
- **Four rules that were simply wrong are fixed:**
  - injured and out players now count as zero;
  - Yahoo's "doubtful" is understood;
  - six injured players lost a few projected games;
  - mid-season pickups like Drummond can be added without breaking the morning.

**Did your decisions change?** Barely.
- One waiver idea, Holiday for Braun, stopped being worth it.
- Your title odds moved less than the dice-roll noise, and nobody moved on the season board.
- That's mostly good news: the fixes didn't turn up a hidden problem with the team you have.

**Something to know about tonight.** The morning tool ran at 8:43 pm Tuesday, from the instructions you pasted, instead of waiting for 5:53 am. It ran everything merged today, and it passed. But at that hour three of Tuesday's eleven games, the West Coast ones, weren't finished. So the Season Deck you can open right now is built on part of Tuesday, and nothing on it says so. The 5:53 am run should replace it with the full day. I'd like your OK to make the tool say when a day isn't finished.

**The Yahoo connection** got its first live try tonight. The weekly scoreboard came through. Most rosters and the free-agent list didn't, because Yahoo's sign-in was refreshing, so the tool used FantasyBot instead, as designed. The 5:53 am run follows the saved instructions, which don't include Yahoo, until you save the new ones in the runner's own chat.

**The bigger gap I connected tonight.** The title-odds number still uses draft-day player projections. Nothing that happens in the season, whether games, injuries or pickups, reaches it yet. I'd suggest measuring how far apart the two sets of projections already are before deciding whether to rewire it.

**Is it actually more accurate?** We don't know yet, and nobody can until results come in.
- The first real test is Sunday, when week 1 ends. The old card said you were a 60.6 % favourite; the new one, using the real schedule, projects a 3–6 loss.
- The injury numbers get their first test in mid-November.

**Mistakes.** None of today's mistakes was a maths mistake. They were about which file a tool reads, whether a check really checks, and which folder a command ran in. Most were caught before they reached you. Seven weren't:
- one thing I told you was wrong ("nothing either way");
- two of my option descriptions for Hunter were wrong (fixed before building);
- the live page lost its tabs Tuesday morning;
- tonight's page rests on part of a day;
- three sentences in merged files were wrong, and are corrected here.
