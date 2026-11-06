# After-report — morning run 2026-10-29 (prompt v5)

**Request (owner, 2026-10-29):** "Create after report to feed into Main session for any corrections or updates."

**What was covered:**
- The run at T0 2026-10-29T12:04:06Z on season/daily.
  - Base 547edaf (merge of origin/main deccaf2: #224, #225).
  - Run commit 62cfdc6; report fix 7a7b458.
- The 10-28 morning records it is compared with: commit 2beeb16 and e0c81db.
- The kit code behind the two open items: `scripts/daily_brief.py`, `scripts/co_gm.py`.

**Method:**
- Read-only, from committed files and this session's step output (`morning_1029.log` in the runner's scratchpad).
- No simulator re-run and no code changed: root-causing is the main session's job and waits on the owner.
- Every EVIDENCE line below was re-read from the file named beside it on 2026-10-29 at ~14:30Z.

**Headline:**

| # | Item | Status | Needs |
|---|---|---|---|
| 1 | **Title 32.6% → 15.6% overnight.** Most likely cause: Haliburton moved from SG to IL, and the simulator's IL rule (D-IS-8) zeroes an IL player for the whole simulated season. | INFERENCE, strong; not measured | Main session: measure, then owner decision |
| 2 | **This morning's runner report was wrong on that point.** It said "Haliburton … already tagged Out on 10-28". The 10-28 *morning* brief had him Q and active. | EVIDENCE | Correction (done in the report file, line added) |
| 3 | **Team 5 renamed** "Giavaris Jamal Javarison-Lamar" → "ANONG NANGIANNIS?!". LEAGUE PAIRINGS and LEAGUE TABLE FAIL because they key on team name. | EVIDENCE | Main session: owner decision |
| 4 | Waiver gate (10-28 Finding A) works in production: Jalen Williams set aside. | EVIDENCE | Nothing |
| 5 | #225 is live: `status_feed.py` and `season_deck.py` both list `--phase`, so the 3 PM run takes the `_pm` path for the first time today. | EVIDENCE | Check the afternoon report |

## 1. Run results (EVIDENCE: step output and `report/briefs/morning_2026-10-29.json`)

| Step | Line |
|---|---|
| MORNING | PASS — 2026-10-29: 16 steps |
| LEAGUE LIVE | PASS — rosters from Flaim (Yahoo), pinned data/source/flaim/pull_2026-10-29.json; 1 not in the pool, not simulated: Matisse Thybulle |
| BOX PULL | PASS — 2026-10-28: 12 games, 320 player lines, 222 in the pool, 98 unpooled; two outlets |
| TAG OUTCOMES | PASS — 33 flagged: 3 no game, 7 played, 22 sat, 1 unresolved |
| SEASON LINES | PASS — 287 lines moved by 0.25+ |
| STATUS GATE | PASS — status_2026-10-29.json: 26 flagged rows |
| WEEK MATCHUP | PASS — vs Looking Cool Joker!; to date from Yahoo (rebuild agrees); 3 days, 0 missing; projected 7-2-0 |
| LEAGUE PAIRINGS | **FAIL (non-fatal)** — week 1: team 'Giavaris Jamal Javarison-Lamar' is not in the league state |
| LEAGUE TABLE | **FAIL (non-fatal)** — week_1.json has no yahoo_score for ['ANONG NANGIANNIS?!'] |
| SEASON DECK | PASS — 7 panes, 315 board rows, 26 status rows; 7 tabs, 0 page errors |
| MANAGER LOG | PASS — 12 lineups for 2026-10-28; profile 7 days; 73 moves on record |
| COMMIT CHECK | PASS (after 62cfdc6 and after 7a7b458) |

**Other results:**
- Calls: Flaim 31 of 31 returned data with no retries (session, league info, 12 rosters, matchups, available list, standings, 12 dated lineups, transactions). FantasyBot 1 of 1 (outlook).
- Deck: Version 42 (1793275736-dde7). The 499,167 built bytes are contained in the 499,713-byte live page.
- Pushed: 7a7b458; `ls-remote` equals HEAD. PR #165 is open and draft, and was not touched.

## 2. The title drop (item 1)

**The numbers (EVIDENCE):**

| Brief | Title (seed 2026 / 2027) | Playoffs | Base exp. cat wins/week |
|---|---|---|---|
| 10-28 (`git show e0c81db:report/briefs/brief_2026-10-28.json`) | 32.57 / 32.64 | 99.86 | 5.5695 |
| 10-29 (`report/briefs/brief_2026-10-29.json`) | 15.0 / 16.27 | 95.99 | 5.031 |

**What changed for seat 10 between the two league states (EVIDENCE, `data/league_state.json`):**

| | 2beeb16 (10-28 am) | 62cfdc6 (10-29 am) |
|---|---|---|
| Tyrese Haliburton | **SG (active)** | **IL** |
| Bobby Portis | not rostered | UTIL |
| Kawhi Leonard | IL | IL |

**The rule that turns an IL slot into a season-long zero (EVIDENCE):**
- `scripts/co_gm.py:50-54` `rosters(state, by, include_il=False)`: "an IL player counts as zero (absent from the simulation) until he is on the active roster". It drops every player whose `slot` is `"IL"`.
- `scripts/daily_brief.py:162` builds the simulator's rosters with that default, and `:219` passes them to `CG.run_league_sim`.

**Ruled out (EVIDENCE):**
- Yahoo record: 3-6, rank 11 in both days' pinned standings.
- The code merged from main (#224, #225) changed no engine file: `git diff --stat 848a4ef deccaf2 -- scripts` lists `season_deck.py`, `status_feed.py`, `redteam/attacks.json` and tests only.

**Smaller contributors (EVIDENCE, `data/season/season_lines_2026-10-29.json` movers):**
- Small mixed line moves on the roster, e.g. Ty Jerome pts 17.5→20.6, Derrick White 16.8→15.7, Kyrie Irving 22.7→21.5.
- Summed board z for seat 10's roster, IL included, went 11.53 → 9.12.

**INFERENCE:**
- Haliburton is board rank 9 (z_adj 4.05 on 10-29).
- Removing him from every remaining simulated week is the largest single change between the two runs and fits a drop of this size.
- Not measured. The test is two simulator runs: 10-29 inputs with Haliburton forced active, and 10-28 inputs with him on IL.

**Why it matters:**
- An IL slot is a lineup move a manager makes for one day's flexibility. Under D-IS-8 the title share reads it as "gone for the season".
- The brief's structural band covers only TEAM_WEEK_SHOCK and weekly_availability. D-IS-8 is not in the swept set, so the stated band (+2.7/−4.2, −5.4/+3.7) does not bound this effect.
- The same rule zeroes Kawhi on both days, and every rival's IL players.

## 3. Correction to this morning's runner report (item 2)

- **What it said** (`report/briefs/morning_report_2026-10-29.md`, at 62cfdc6): "Haliburton and Kawhi were already tagged Out on 10-28."
- **What is true (EVIDENCE):**
  - `git show 2beeb16:data/status/status_2026-10-28.json` has Haliburton `questionable`, 0.5.
  - The 10-28 brief's today list has him "Q", 0.5, in the SG slot.
  - The branch-tip copy of `status_2026-10-28.json` says `out` because the 10-28 3 PM run overwrote it. That is exactly the overwrite #225 now prevents.
- **Root cause of my error:** I read the branch tip's file, not the morning commit's. The 10-28 after-report's own method (compare against the morning commit) would have caught it.
- **Fixed:** a correction line is added to the morning report in the commit carrying this after-report.

## 4. Team rename (item 3)

**EVIDENCE:**
- Flaim `get_league_info` 2026-10-29 lists team 5 as "ANONG NANGIANNIS?!" (owner Kyle).
- `git show 2beeb16:data/league_state.json` named it "Giavaris Jamal Javarison-Lamar".
- `data/weeks/week_1.json` and `data/weeks/team_weeks.csv` carry the old name.
- `data/managers/profile.json` keys teams by Yahoo team key (`478.l.36464.t.5`), so the manager log was unaffected (PASS) and its 10-28 day file uses the new name.

**Effect:**
- league_pairings and league_table halt every morning until fixed.
- Did not check what the deck's League tab shows while LEAGUE TABLE fails (NOT-ATTEMPTED). SEASON DECK passed with 7 tabs, but whether the League pane is stale or empty is unverified.

## 5. Updates since the 10-28 after-report

| 10-28 finding | 10-29 state | Basis |
|---|---|---|
| A. Waiver scan proposed unclaimable / Out players | **Fixed in production.** "Status from Yahoo and ESPN." Set aside: Jalen Williams (Out, ESPN back 2027-03-02), Cason Wallace, Kevin Porter Jr., Justin Champagnie, Dylan Cardwell. The top pair's add (Cameron Johnson, O, ESPN back 10-30) is kept and flagged as the 10-28 owner rule says. | `report/briefs/brief_2026-10-29.md`, Waiver scan |
| B. Flaim 502 halted the manager log | Retry rule in v5. **Not yet exercised:** no retryable error today, 31/31 first try. | Run transcript |
| Afternoon overwrite of morning status files | #225 merged. Both `--help` checks list `--phase` (checked 2026-10-29 ~12:30Z). Today's 3 PM run is the first on the `_pm` path. | `python3 scripts/status_feed.py --help`, `season_deck.py --help` |

## Bounds

**Out of scope by design:**
- No simulator run, no code or tag change, no edit to league_pairings or league_table.
- No research on Haliburton's injury timeline.

**In scope and unverified:**
- The size of D-IS-8's share of the title drop: NOT-ATTEMPTED (needs two simulator runs; a dry run waits on the owner's go).
- The League tab's content under the LEAGUE TABLE failure: NOT-ATTEMPTED.
- Haliburton's expected return: NOT-ATTEMPTED. His status row carries no ESPN return date; `status_2026-10-29.json` has only the Yahoo "O" receipt.

## Decisions for the owner

**A. Title figure while a starter sits on IL**
1. **Have the main session measure D-IS-8's effect first (Recommended).** Two seeded runs, Haliburton active vs IL on the same day's inputs. Report the delta with its sampling error before deciding anything.
2. Treat IL players as returning on ESPN's expected date in the season sim. More realistic, but it changes an engine rule and needs the red-team pass.
3. Keep D-IS-8 and add a line to the brief whenever an IL move shifts the title by more than its error.

**B. Name-keyed league steps**
1. **Key league_pairings and league_table on Yahoo team key, as manager_log already does (Recommended).** Renames can't break them again.
2. One-time alias for team 5.
3. Accept the two daily FAILs.

## Provenance

- Runner session `session_01BsJA4wttu98TKVNoh6HBz1`, 2026-10-29.
- Sources:
  - `report/briefs/brief_2026-10-28.json` (e0c81db) and `brief_2026-10-29.json`
  - `data/league_state.json` at 2beeb16 and 62cfdc6
  - `data/status/status_2026-10-28.json` at 2beeb16 and 7a7b458
  - `data/season/season_lines_2026-10-29.json`
  - `scripts/co_gm.py:50-54, 273-281`
  - `scripts/daily_brief.py:159-232`
  - `data/managers/profile.json`
- Re-verify:
  - `git show 2beeb16:data/league_state.json`
  - `sed -n 50,55p scripts/co_gm.py`
  - `grep -n "rosters(state" scripts/daily_brief.py`
