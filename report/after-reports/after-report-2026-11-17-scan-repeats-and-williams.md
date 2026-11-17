# The waiver scan's repeated names, Ziaire Williams, and two scan fixes (2026-11-17)

Pull window: 2026-11-17 → 2026-11-17 (no pull: kit main 80b2be4, deck main 3551a15, the records branch season/daily at e971a0f, read only; 38 simulator runs and two replays in throwaway worktrees; one live Flaim lookup of one player at 19:54 UTC).

**Owner's requests, verbatim (2026-11-17).** "Assess the waiver scan's repeated names now, and expand your report on Ziaire Williams". Then, on the card: "Both fixes (Recommended)" for the scan, and "Score the post-return roster (Recommended)" for Williams.

**Method up front.** Each choice was stated to the owner before the run that used it.

- The scan: the 28 briefs from 2026-10-20 to 2026-11-17 (`waiver_top`) and the scan's code. A listed pick is graded on the 7 days after it was listed, on box scores to 11-16; the session's window.
- Williams: three lines for him and nobody else: the kit's, his season to date (10-20 to 11-16, 11 games), his last 14 days (11-03 to 11-16, 6 games). 10,000 seasons × seeds 2026 and 2027; title and reach-the-final shares (the owner's pick of the same day: "Quote both"). Two worlds: injured players never return (the brief's), and both of the owner's stars active from week 6 (11-23), the session's assumption from ESPN's earliest dates of 11-22 and 11-23. An earlier run of the day had Haliburton back in week 5; section 3 shows both.
- The gate rule was replayed on every pinned ESPN feed from 10-28 to 11-12 before it was kept, against the box scores, and against one alternative.
- Known answers: the no-move baseline reproduced the morning brief (14.09 against 14.1); the earlier return baseline reproduced (20.48 against 20.5); the counts of the reading lines on the 26 briefs with picks match the assessment's counts made a different way (18 inside sampling error, 14 at or below zero, 37 clear).

**Verdict. The repeats are mostly an honest list of replacement-level veterans, with two real defects, both now fixed in this pull request: an Out player whose return date keeps moving stayed in the scan (Tobias Harris, 17 listings, no game), and a list headed "Best 3" whose title figure mostly describes the owner's drop. Ziaire Williams is a steals specialist whose swap is negative on the kit's line and positive on his own season line; no row is a verdict.**

Runner impact: code-only (the morning brief's waiver gate reads the pinned ESPN feeds of the seven days before; an Out whose absence is no longer short is set aside and named; the waiver section gains reading lines and one record key, `waiver_read`; the deck's free-agent status reads the same rule). No prompt, step or pass line changes. Meant to land Monday 2026-11-23 after that morning's grading (RULES.md rule 12: the gate change alters which free agents the scan can list), unless the owner says otherwise for this pull request.

Pool rows touched: none

## 1. The repeated names

EVIDENCE: `scan-repeats-2026-11-17/slots.json` (every listed pick) and `scan_assess.py`.

| finding | EVIDENCE |
|---|---|
| Five names took 55 of 69 listed picks | Tobias Harris 17, Julian Champagnie 16, Bobby Portis 9, Cameron Johnson 9, Jrue Holiday 4; 16 distinct names in all |
| Harris: 17 listings, no game | No box-score row for him from 10-16 to 11-16. First pick on 5 mornings (11-05 to 11-08, 11-13). ESPN's return date read 10-31, 11-06, 11-09, 11-11, 11-19, then 12-03 on 11-17 |
| A large title figure belongs to the drop | 23 picks showed more than +2 points; 20 of them dropped Karlo Matkovic (9), Ziaire Williams (5), Noah Clowney (3) or Mario Hezonja (3) |
| The picks are often inside the noise | 18 of 69 title changes between 0 and the sampling error (about 0.7), 14 at or below zero; the list is ranked by weekly category wins and the title run is a check |
| The picks are sometimes tied | On 16 mornings every pick named one drop; on 5 of them the adds were within sampling error of each other |
| The first pick was middling | Over the next 7 days (22 mornings to 11-10): no game on 5; on the other 17 the median was the 64th percentile of free players with 2+ games at 18+ minutes, 3 in the top quarter, none the best |
| The scan re-lists what the owner just dropped | 26 of 69 picks named a player he had dropped in the previous 7 days; Champagnie was added and dropped three times |
| Only one of the five lines was wrong | Portis: line 13.3 points and 6.8 rebounds, actual 7 and 6 in 20 minutes over 14 games. Champagnie (10.0 against 10), Johnson (13.0 against 13) and Holiday (12.2 against 13) played to their lines |

Why, from the code (`scripts/co_gm.py`): the candidates are the 40 best free players by the kit's line (`free_agents`), which moves slowly; the pairs are ranked by expected weekly category wins (`waiver_pairs`); an Out player ESPN expects back within `SHORT_OUT_DAYS` (7) stays in at full season value (`fa_status`), asked afresh each morning; nothing remembers the owner's own moves.

INFERENCE: that several repeats were the scan disagreeing with a streamer the owner had just added. On Matkovic the box scores bear it out (5 points in 19 minutes after the add); on Williams they do not.

## 2. Ziaire Williams

| | EVIDENCE |
|---|---|
| Availability | Free agent in the league (Flaim `get_players`, 2026-11-17 19:54 UTC); 12% rostered on Yahoo; a free agent, not on waivers, in the morning pull |
| Role | Started his first 4 games (24 to 31 minutes); no game logged from 10-28 to 11-01; six of seven since off the bench (15 to 23 minutes), one start on 11-09 (28) |
| Season to date, 11 games | 10.5 points, 2.5 rebounds, 2.1 assists, 1.5 steals, 1.8 threes, 0.5 turnovers, 42 of 74 from the field (57%); a steal in 10 of 11 games |
| Kit's line | 10.2 points, 1.2 steals, 0.8 turnovers, 46% from the field |
| Schedule | Lakers: 2 games left in week 5 from 11-18, 3 in week 6. Boston and Denver: 3 and 3 |
| History | Scottie's Thotties 10-26 to 11-04; the owner 11-05 to 11-08 |
| League limits | Yahoo `maxWeeklyAdds` 4 (Flaim `get_league_info`, same time); the feed shows one owner add in week 5 (Cam Spencer, 11-16) |

The owner's category win rates in the simulator (never-return world): assists 26%, steals 29%, rebounds 37%, points 39%, FG% 43%, threes 47%, turnovers 49%, blocks 50%, FT% 54%. Williams for Neemias Queta moves steals by +6 to +10, threes +6, FT% +4, rebounds -9, blocks -9. Williams for Cameron Johnson moves steals by +2 to +6 and rebounds -3.

## 3. The swaps, on three lines

Title / final, change from the baseline of the row's world. EVIDENCE: `zw.json`, `zw2.json`, `zw_lines.json`.

| world, baseline title / final | swap | kit's line | season to date | last 14 days |
|---|---|---|---|---|
| never return, 14.1 / 27.1 | Williams for Queta | -0.8 / -1.3 | +1.2 / +1.3 | +2.0 / +2.2 |
| never return | Williams for Cameron Johnson | -1.1 / -1.1 | +1.3 / +1.8 | +1.8 / +2.3 |
| returns, Haliburton from week 5, 20.5 / 37.0 | Williams for Queta from week 6 | -1.3 / -1.8 | +1.0 / +1.4 | +1.8 / +2.2 |
| returns, both from week 6; the owner's plan (Johnson and Spencer out), 20.4 / 36.7 | Williams in PJ Washington's spot | -1.3 / -1.3 | +1.7 / +2.4 | +2.0 / +2.7 |
| the same | Williams in Queta's spot | -1.2 / -1.8 | +1.1 / +1.5 | +1.6 / +2.0 |
| the same | no Williams; Johnson and Washington out, Spencer kept | +0.8 / +1.1 | the same | the same |

Two error bars. Sampling: about ±0.7 on a difference. Structural: the choice of line moves every Williams row by 2 to 3 points and flips its sign. The kit's line is the regressed estimate: at 11 games the blend still leans on the pre-season number for about 70% of FG% and 66% of steals (`season_lines.PRIOR_GAMES` 26.0 and 21.7).

**weekly_availability is FRAGILE:** -0.8 (healthy at the old 0.88) / -0.3 (healthy at the unfloored fit (0.78)) / -2.6 (risk at the old 0.75) / +1.4 (risk at the unfloored fit (0.56)); headline title share 14.1% ± 0.5 (MC) within that band. Sweep of 2026-11-16, made on the lines before the minutes switch; no sweep has run on the switched lines with the new constants.

What holds on every line: Queta is the costlier drop (rebounds and blocks), and Washington is the spot where Williams helps most or hurts least. The one row that does not depend on Williams's line is the last: keeping Cam Spencer over PJ Washington adds 8 points of assists win rate, the owner's weakest category, for about 6 each of rebounds and blocks; at +0.8 it is just outside the sampling error.

The session's read, against its own earlier framing: the audit of the same day listed Williams beside Anthony Black and Christian Braun as a pickup dropped too soon. He is the weakest of those cases. His standing on the audit's scale came from efficiency on low minutes, and his role has shrunk, not grown.

## 4. The two fixes

| fix | what changed | checks |
|---|---|---|
| A short Out is a short absence | `co_gm.fa_status` takes the pinned ESPN feeds of the 7 days before (`espn_history`). An Out counts as short only when the first day of the unbroken run of Out listings (`out_since`) to the return date is within `SHORT_OUT_DAYS` too. The same 7; no new constant. With no feeds on disk it reads as before. The brief's set-aside line names such a player with "out since <day>, so not a short absence" | `scripts/test_waiver_status.py` SlidingReturn, 8 tests, red before the change (8 errors); `test_daily_brief.py` LongOutWording |
| The list says what it can tell apart | `daily_brief.scan_read`: the sampling error of a title change is printed in the heading; a pair at or below zero is marked "no title gain", one inside the error "inside sampling error"; when every pair names one drop the note says the figures describe that roster spot; when the adds are within the error of each other it says the scan cannot rank them. "Best 3" becomes "Top 3 by weekly category wins". Display only: no pair is reordered | `test_daily_brief.py` ScanRead, 4 tests |

The gate rule on the real records (`rule_replay.py`, `rule_replay.txt`): on 384 mornings-and-players that today's rule kept in the scan as a short Out (10-28 to 11-12), the player played by the quoted date on 122 (32%).

| rule | kept in the scan | of those, played by the date | set aside | of those, played by the date |
|---|---|---|---|---|
| today's | 384 | 122 (32%) | 0 | 0 |
| built: the whole absence within 7 days | 237 | 87 (37%) | 147 | 35 (24%) |
| tried and rejected: the return date has not been pushed back | 237 | 70 (30%) | 147 | 52 (35%) |

- Harris is kept on 10-28 to 10-30 (return quoted 10-31) and set aside on every morning from 10-31.
- The cost: 35 set-aside listings where the player did come back on the quoted date, over 12 players (Nic Claxton and Keegan Murray among them). They are named each morning in the set-aside line with ESPN's date, and they return to the scan the day their status clears.
- A pushed-back date, the rule first expected to matter, does not separate the two groups at all (35% against a base of 32%).
- On 2026-11-17 the rule moves Maxime Raynaud and Dominick Barlow out of the 40 candidates and Javonte Green and Collin Sexton in; the three listed pairs are unchanged.

The reading lines on the 26 briefs with picks: "one shared drop" on 16 mornings, "cannot rank them" on 5, 18 pairs marked inside sampling error, 14 marked no title gain.

## 5. Decisions for the owner (nothing changes without a pick)

1. This pull request: merge on Monday 2026-11-23 after grading (rule 12), merge now as his exception, or keep as a draft.
2. Williams: his call. Section 3 is conditional on the line.
3. The last spot after the returns: the plan (Johnson and Spencer out) against keeping Spencer over Washington. One more run would say whether +0.8 holds on other seeds.
4. `SHORT_OUT_DAYS` itself is graded on 2026-11-25 (D-WS-2). The replay's 32% belongs with that decision.

## 6. Bounds

Out of scope by design: no line, roster or pool row was changed; no trade was scored (owner veto 2026-10-20); the deck's cards and the decision card still show the pairs without the reading lines; the scan's ranking and its 40-candidate width are untouched; the scan still has no memory of the owner's own drops.

In scope and unverified:
- Current reporting on Williams's role, and why he has no game from 10-28 to 11-01: did not check. The advice rests on league data and box scores.
- Only Williams's line was varied. NOT-ATTEMPTED: the recent form of Queta, Johnson or Washington, each of whom has played below his kit line.
- The week-6 return date is an assumption from ESPN's earliest dates, which section 4 shows hold about a third of the time.
- What a free-agent add costs against the owner's budget: did not check.
- The transaction feed was not re-read after the morning, so the count of week-5 adds is as of the morning.
- The replay's "played by the quoted date" is by date, not by game; the feeds begin 10-28, so a run that began earlier reads as starting then.
- The earlier feeds the deck now reads for the same rule are not pinned in the deck's input record.
- The sweep quoted in section 3 predates the minutes switch.

## 7. Provenance

Session of 2026-11-17 (session model A), the Main session; branch `claude/new-session-koi1jp`. Records: kit main 80b2be4, deck main 3551a15, season/daily e971a0f. Re-verify: `python3 scripts/test_waiver_status.py`; `python3 scripts/test_daily_brief.py`; from a checkout of the records branch with this branch's scripts, `SEASON_POOL=data/season/pool_season.csv python3 <kit>/report/after-reports/scan-repeats-2026-11-17/rule_replay.py`. One correction logged with this report: the sampling error for comparing two picks.
