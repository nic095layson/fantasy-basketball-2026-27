# After-report — Pre-draft gap audit: how this league is actually played vs what the system models (2026-09-30)

**Owner request (2026-09-30, verbatim):** "Do you remember when I uploaded
Yahoo data of past season, rosters, real life draft history from past seasons
- you learned a lot about how fantasy basketball is ACTUALLY played. Do you
have any gaps or things you are unsure about going into the draft? If so, I
want you to research on the internet and have expertise understanding and
comprehension to master this fantasy basketball tool."

**What the system holds (read this session from the repos, not recalled):**
the league file `arena/results/league_intel_2025-26.md` (confirmed settings,
three seasons of standings and draft boards, the owner's 17 answers of
2026-08-04, the complete 12-manager map), the 2025-26 weekly scoreboard
(`arena/data/weekly_matchups_2025-26.csv`, 22 matchups reconciled to the
displayed 103-58-1), the room model and eleven manager profiles
(`arena/profiles.json`, E18), and the two prior gap-research reports
(2026-09-16, 2026-09-21), which were about missing players, not about the
league. This audit is the other kind: every place where the code's model of
the league, of Yahoo, or of the NBA calendar differs from what those files
and the public rules say.

**Scope.** Structural gaps only. Player news is the daily pull's job and is
not repeated here. Each gap was found by reading the engine, the arena and
the deck against the league files, then researched and classified: CLOSED
(two outlets, or a computed artifact validated against published facts),
OWNER-ONLY (a league setting only the settings page answers), ATTEMPTED
(searched, not resolved), or UNMODELED-KNOWN (registered before, still open
in code). **Nothing in the pool, the board, the deck or the arena was
changed**; every change is a decision below.

**Method.** WebSearch summaries for the Yahoo rules (sports.yahoo.com,
help.yahoo.com and rotowire.com are egress-blocked, so the summary is the
channel and every Yahoo claim names its help-page id); nba.com and
basketball-reference.com fetched directly. The schedule table is computed by
`report/schedule/build_schedule.py` from Basketball-Reference's seven month
pages (1,200 dated games, exactly 80 per team; the 30 NBA Cup knockout-window
games are not yet dated) and validated against seven facts Yahoo published
about this calendar — all seven matched (§3). Verification: this file passes
`report/check_report.py`; receipts in the section below.

Pull window: 2026-09-30 → 2026-09-30 (research run 2026-09-30; not a roster
pull — the 9/30 pull-log rows cover the window).

**Headline.** Three gaps matter for draft night, and none of them is player
news. **(1) Every championship probability the system has ever quoted is on
the wrong bracket.** The arena still plays a six-team playoff with byes for
the top two seeds (`arena/arena.py`, `PLAYOFF_TEAMS = 6`); this league sends
eight of twelve with no byes. The difference was measured on 2026-08-04 —
elite rosters lose four to six points of title odds under the real bracket —
and registered as E14 for adoption, but it never shipped. The card, the 🎯,
ΔECW and the advisor do not touch the bracket, so draft-night advice is
unaffected; the debrief headlines (mock 57's 35.23 percent) are overstated.
**(2) The 2026-27 fantasy calendar is new, and the system had no calendar at
all.** Yahoo runs two 14-day matchups this season — week 7 (Nov 30 to Dec 13,
the NBA Cup knockout window) and week 17 (Feb 15 to 28, All-Star) — so the
season has 23 game weeks instead of last season's 24, and this league's
playoff weeks 19 to 21 land on **March 8 to 28**, a week later than last
season's pattern. The per-team games table for that window is now computed
for all 30 teams: Dallas, Memphis and Phoenix play twelve, Cleveland nine.
**(3) The weekly model's flat 3.5 games per week is right on average (the real
seven-day-week mean is 3.47) and blind to everything else** — the two 14-day
weeks, the six-day week 1, and the playoff-window spread. Smaller closures:
the NBA Cup final on Dec 11 counts for neither the NBA standings nor Yahoo;
Yahoo's basketball position eligibility is editorial and rarely changes in
season, which makes the draft room's positions the season's positions and
turns D57-1 from a nicety into a should-do; a pre-draft ranking list can be
loaded from a CSV with a Chrome extension, the only insurance against a
dropped connection on the pick clock; and XRank and ADP are what the Mkt
column assumes they are.

---

## 1. Gap ledger

| # | gap | what the system does today | what is actually true | status |
|---|---|---|---|---|
| G1 | playoff bracket | arena: 6 teams, seeds 1 and 2 on byes, fixed bracket | 8 of 12 qualify, no byes, three 1-week rounds (owner, 2026-08-04; three seasons of standings) | UNMODELED-KNOWN — E14 registered 8/4, never shipped; D-G1 |
| G2 | fantasy calendar | none; every week is a 7-day week of 3.5 games per man | 23 Yahoo game weeks; week 1 Oct 20 to 25 (six days); weeks 7 and 17 are 14 days; the league's playoff weeks 19 to 21 are Mar 8 to 28 if the league keeps "playoffs start week 19" | CLOSED (Yahoo schedule analysis via search; validated against the schedule, §3); the league's start-week setting is OWNER-ONLY, D-G5 |
| G3 | per-team playoff-week schedule | none | computed for all 30 teams for weeks 18 to 23, with back-to-backs (§3, `report/schedule/`) | CLOSED (artifact); D-G2 |
| G4 | NBA Cup final | not modeled | the Dec 11 game sits outside the regular season; Yahoo excludes its stats; every team plays exactly two counted games in the Dec 4 to 11 window and the finalists a third that does not count | CLOSED (nba.com Cup FAQ fetched; Yahoo schedule analysis via search) |
| G5 | position eligibility source | pool positions come from the 9/28 rankings paste; 29 of 156 men drafted on 9/29 showed fewer positions in the draft room (D57-1) | Yahoo sets basketball eligibility editorially (box scores, outside trackers, its reporters); adding or changing eligibility is rare; commissioners can only add | CLOSED (Yahoo help SLN7057 via search — the primary page, one source); D-G3 |
| G6 | streaming and roster churn | not modeled; champ% is a no-streaming bound (E16) | unlimited moves, daily lineups, two IL+ slots; 16 to 87 moves per team per season; the last two champions made 16 and 50 moves | UNMODELED-KNOWN — §5; no change before the draft |
| G7 | regular-season standings tiebreak | none | winning percentage with ties at one half; ties broken by the last game week's percentage, then each earlier week (no total-categories tiebreak in category leagues) | CLOSED (Yahoo help SLN35744 via search) |
| G8 | playoff matchup tie | none | Yahoo default is "higher seed wins"; private commissioners may choose "best regular-season record vs opponent", which in basketball categories means the most category wins | OWNER-ONLY (which rule this league uses; Yahoo help SLN6539 via search) |
| G9 | lineup-change mode | "daily" (owner) | Yahoo has Daily-Today (adds and drops apply at once) and Daily-Tomorrow (11:59 PM PT deadline the night before); active-bench swaps lock at each player's tip-off under both | OWNER-ONLY (Yahoo help SLN22673 and SLN6775 via search) |
| G10 | clock insurance | none | Yahoo autopick fills from your pre-draft ranking, starters before bench, position-balanced; a Chrome extension imports a CSV into that list | CLOSED (Yahoo help SLN6163; Chrome Web Store listing); D-G4 |
| G11 | market column semantics | Mkt = Yahoo ADP, else XRank | XRank is Yahoo's editorial rank (six Yahoo analysts plus RotoWire); ADP averages Yahoo mock and real drafts | CLOSED [SINGLE-SOURCE: Yahoo's football explainer via search; the basketball construction is not separately confirmed] |
| G12 | NBA rest rules | games played priced per player | the Player Participation Policy is unchanged since 2023-24 (no resting healthy stars in national-TV or Cup games; 65-game award threshold); no 2026-27 change found | ATTEMPTED — nothing found in two search passes |
| G13 | playoff-tier objective (E9) | ΔECW is measured against all eleven rosters in the room | the title is three one-week matchups against playoff-tier teams; in three seasons the champions' record ranks were 2, 7 and 7, and the best record never won | UNMODELED-KNOWN; D-G6 |
| G14 | draft-night settings | Oct 14, 7:00 PM, slot 10; the owner has mentioned a 60-second clock | time zone and clock length are settings-page facts | OWNER-ONLY |

## 2. The bracket (G1): what it changes and what it does not

The league file measured this on 2026-08-04 by re-simulating four ledger
mocks under the real eight-team no-bye bracket on the same seeds
[EVIDENCE: `league_intel_2025-26.md` §4, `arena/mocks/format_delta.py`]:

| mock | owner champ%, 6-team with byes | owner champ%, 8-team no byes | owner playoff% |
|---|---|---|---|
| 21 | 26.91 | 20.92 | 91.4 to 97.7 |
| 25 | 29.19 | 22.86 | 94.3 to 98.3 |
| 27 | 9.76 | 9.42 | 62.5 to 80.6 |
| 30 | 2.12 | 3.31 | 31.1 to 59.5 |

The real format taxes elite rosters four to six points and hands weak rosters
equity; a .488 team qualified and won last season. The eight-team bracket
exists in code today only inside the calibration harness; the arena's season
simulator still reads six teams with byes, and that simulator is what every
retro harness (`live_retro.py` included) runs to produce the champ% in the
mock debriefs and in this repo's after-report headlines. Playoff% is the number most
understated: under the real cut, eight of twelve, a mid roster qualifies far
more often than the ledger says.

What the bracket does not touch: the deck's Top-5 order, the blend50 score,
ΔECW, the LAST CALL row and the advisor are weekly-model outputs, and the
survival chips are price-model outputs; none of them has a bracket in it. So the advice the owner followed in
mocks 54 to 57 is unaffected; the grades' title odds are the part that is
wrong. The port is small (the harness has the bracket) but it changes every
historical champ% and the ledger's comparability, which is why it was
deferred to a re-baseline; D-G1 proposes doing it before Oct 14 with the six
live-room retros re-run so the debriefs carry real-bracket numbers.

## 3. The 2026-27 calendar and the per-team schedule (G2 to G4)

**Yahoo's 2026-27 game weeks** [EVIDENCE: Yahoo's schedule analysis via
search summary; validated below]:

| week | dates | days | note |
|---|---|---|---|
| 1 | Oct 20 to 25 | 6 | opening night Tue Oct 20 |
| 2 to 6 | Oct 26 to Nov 29 | 7 each | Cup group play on Tuesdays and Fridays Oct 30 to Nov 27 (all count) |
| 7 | Nov 30 to Dec 13 | 14 | Cup knockout window: 29 games Nov 30 to Dec 3, quarterfinals Dec 4 and 5, semifinals Dec 8 and 9, final Dec 11 (does not count), 14 games Dec 12 and 13 |
| 8 to 16 | Dec 14 to Feb 14 | 7 each | |
| 17 | Feb 15 to 28 | 14 | All-Star weekend Feb 19 to 21 in Phoenix; break Feb 19 to 24 |
| 18 | Mar 1 to 7 | 7 | the league's last regular-season week |
| 19, 20, 21 | Mar 8 to 14, Mar 15 to 21, Mar 22 to 28 | 7 each | the league's quarterfinal, semifinal and final, if playoffs start week 19 (D-G5) |
| 22, 23 | Mar 29 to Apr 4, Apr 5 to 11 | 7 each | Yahoo's default playoffs are weeks 20 to 22; the NBA season ends Apr 11 |

Last season's calendar (from the scoreboard file) had one 14-day week (week
17, Feb 9 to 22) and 24 game weeks, with this league's weeks 19 to 21 on
March 2 to 22. The Cup merge is new for 2026-27 and moves every week from 7
on by one. The nba.com fantasy calendar carries the same NBA dates (opening
night Oct 20, Cup group play Oct 30 to Nov 27, knockout Dec 4 to 11,
All-Star Feb 19 to 21, season end Apr 11) but does not describe Yahoo's
weeks; Yahoo's own week structure is a single channel here, so it was
validated mechanically instead: Yahoo published seven checkable facts about
this calendar, and the schedule table reproduces all seven — 29 games on Nov
30 to Dec 3 and 14 on Dec 12 and 13 (week 7's edges), Dallas and Phoenix at
twelve games in weeks 20 to 22, Minnesota's two-game week 20, Cleveland's
two-game week 21, and New Orleans' two-game week 22. Yahoo's sentence naming
Memphis as a third twelve-game team in weeks 20 to 22 is wrong by one:
Yahoo's own Memphis schedule listing gives eleven games for Mar 15 to Apr 4,
and so does the table. A calendar that put either merge anywhere else would
fail these checks.

**Games per team in the league's playoff window (weeks 19 to 21, Mar 8 to
28), with the surrounding weeks, computed from the dated schedule**
[EVIDENCE: `report/schedule/games-per-week-2026-27.csv`]:

| team | w18 | w19 QF | w20 SF | w21 F | w22 | w23 | **w19 to 21** | back-to-backs in w19 to 21 |
|---|---|---|---|---|---|---|---|---|
| DAL | 2 | 4 | 4 | 4 | 4 | 4 | **12** | 2 |
| MEM | 3 | 4 | 4 | 4 | 3 | 4 | **12** | 3 |
| PHO | 3 | 4 | 4 | 4 | 4 | 3 | **12** | 2 |
| ATL | 3 | 4 | 4 | 3 | 4 | 3 | 11 | 2 |
| BOS | 3 | 4 | 3 | 4 | 4 | 3 | 11 | 3 |
| CHO | 2 | 4 | 3 | 4 | 4 | 4 | 11 | 1 |
| DEN | 3 | 4 | 4 | 3 | 4 | 4 | 11 | 3 |
| DET | 3 | 4 | 3 | 4 | 4 | 4 | 11 | 2 |
| GSW | 4 | 4 | 3 | 4 | 4 | 4 | 11 | 3 |
| LAC | 3 | 4 | 3 | 4 | 4 | 4 | 11 | 2 |
| NOP | 4 | 4 | 4 | 3 | 2 | 4 | 11 | 2 |
| OKC | 3 | 4 | 3 | 4 | 3 | 4 | 11 | 2 |
| ORL | 3 | 3 | 4 | 4 | 3 | 4 | 11 | 2 |
| PHI | 4 | 3 | 4 | 4 | 3 | 3 | 11 | 3 |
| SAC | 3 | 4 | 4 | 3 | 4 | 4 | 11 | 2 |
| TOR | 3 | 3 | 4 | 4 | 3 | 4 | 11 | 3 |
| BRK | 4 | 3 | 4 | 3 | 4 | 4 | 10 | 1 |
| CHI | 4 | 3 | 3 | 4 | 4 | 4 | 10 | 1 |
| HOU | 4 | 3 | 3 | 4 | 4 | 3 | 10 | 3 |
| IND | 3 | 3 | 4 | 3 | 4 | 4 | 10 | 2 |
| LAL | 4 | 3 | 4 | 3 | 3 | 4 | 10 | 2 |
| MIA | 3 | 4 | 3 | 3 | 4 | 4 | 10 | 0 |
| MIL | 3 | 3 | 3 | 4 | 4 | 4 | 10 | 2 |
| MIN | 3 | 4 | 2 | 4 | 4 | 4 | 10 | 2 |
| NYK | 3 | 3 | 3 | 4 | 4 | 4 | 10 | 3 |
| POR | 4 | 3 | 4 | 3 | 4 | 3 | 10 | 3 |
| SAS | 3 | 3 | 4 | 3 | 4 | 4 | 10 | 2 |
| UTA | 4 | 3 | 3 | 4 | 3 | 4 | 10 | 2 |
| WAS | 4 | 3 | 3 | 4 | 3 | 4 | 10 | 1 |
| CLE | 3 | 4 | 3 | 2 | 4 | 4 | **9** | 1 |

Under Yahoo's default window (weeks 20 to 22) the twelve-game teams are
Dallas and Phoenix, and Cleveland and New Orleans sit at nine; the CSV
carries both sums. If the league's settings page shows playoffs on weeks 21
to 23 instead (the "last three weeks" reading of a 23-week calendar), the
table's w21 to w23 columns are the ones to read.

**What the spread is worth.** With daily lineups the ten active slots start
99 to 100 percent of a healthy man's games (the daily-fill instrument,
calibrated on this league), so a team's extra game is an extra started game
for each of its men that week. A twelve-game team's player brings four
starts in every playoff round; a ten-game team's brings three in two of
them — one third less of his counting stats in those rounds — and
Cleveland's men bring two in the final. That is a tiebreak, not a ranking term: the Top-5 order is
validated as is, and two positional re-orderings measured on 2026-08-05 (E22)
both failed their bars, so D-G2 proposes a display-only hint on the card from
round 8, the same way LEAN and LINEUP CAP name a trap without moving the
order. Before the draft the schedule enters as the round-8-to-13 tiebreak
among near-equal candidates; it never overrides a value gap.

**The two 14-day weeks** are in-season items, not draft items, and they are
not double weeks: the Cup gap and the All-Star break eat most of the extra
days. Week 17 runs three to five games per team (twenty teams at four, seven
at five, three at three; mean 4.13), and week 7 runs four or five counted
games (the dated 2.87 per team plus the two knockout-window games). The
weekly model, which treats every matchup as seven days of 3.5 games,
understates those two matchups by roughly 18 and 39 percent. D-G7 defers
that to the in-season advisor. **Week 1** is six days: Boston, Cleveland, Denver,
Phoenix and Portland play two games, Philadelphia four, everyone else three
— the first matchup's swing, and nothing to draft around.

## 4. The weekly model against the real schedule (calibration check)

The deck's `teamWeekModel` gives every man 3.5 games a week times his
availability (0.88 healthy, 0.75 risk, 0.60 recovery, from `weeklyAvail`).
Over the 450 seven-day regular weeks of the real schedule (weeks 2 to 18,
minus the two 14-day weeks; 30 teams) the mean is **3.471 games per
team-week, sd 0.593**: 20 two-game weeks, 201 three-game, 226 four-game and
3 five-game [EVIDENCE: `build_schedule.py` output]. The constant is right to
one percent; no re-fit. The distribution is the part the model does not
carry: a four-game week is the modal week, and the two-game weeks (20 of
450) are where a single matchup swings.

The league's own scoreboard adds an outside check. The owner's team and its
opponents logged **42.5 player-games per seven-day week** (mean of 40
team-weeks in 2025-26, sd 5.6, range 21 to 49; weeks 1 and 17 excluded as
short and long) [EVIDENCE: `arena/data/weekly_matchups_2025-26.csv`]. A
thirteen-man roster on the model's healthy line would start about 13 × 3.5
× 0.88 ≈ 40 games; the observed 42.5 sits above that. INFERENCE: the gap of
roughly three player-games a week is streaming's footprint — managers with
unlimited moves add players who play that night — and is the same E16 term
the champ% bound omits. It is small per week and cumulative over eighteen.

## 5. Streaming, IL+ and the late rounds (G6)

From the three ingested seasons: moves per team ran 16 to 87 a season; the
champions made 28 (2023-24, record rank 2), 16 (2024-25, rank 7) and 50
(2025-26, rank 7); the owner made 84 and 64 in the last two seasons and had
the best record in 2025-26 [EVIDENCE: `league_intel_2025-26.md` §2, §10,
§11]. Streaming is common, is not required to win, and is how the bracket's
one-week matchups get played in practice: daily lineups, unlimited moves, and
two IL+ slots that accept day-to-day and game-time-decision designations
(owner, answer 6) mean a hurt man parks without costing a roster spot and a
churn slot is refilled the same day.

That lowers the true cost of a missed game below what a no-streaming model
charges. The kit already carries a credit for it — availability is games ÷ 82
plus a fifth of the missed share, the streaming-credit law of 2026-07-27 —
and the deck's 0.78 multiplier on risk-tagged men was calibrated on real
2025-26 games in a simulator with no streaming. Both point the right way;
neither knows about the IL+ slots. For draft night the consequence is
already the deck's behavior from round 11: the last two or three roster
spots are churn spots, so they buy upside and category specialists, not
floor. No change is proposed before the draft; an in-season model needs the
streaming term itself (E16, deferred with D-G7).

## 6. Yahoo rules the tool has right, and the ones only the settings page can answer (G7 to G11, G14)

- **Scoring.** Each category is one game per week; the standings use wins
  plus half of ties over games played (Yahoo help SLN35744, SLN6212). The
  scoreboard file reconciles to the displayed 103-58-1 under exactly that
  rule, and the arena's ECW counts ties at a half. Right.
- **Standings tiebreak.** Last game week's winning percentage, then each
  earlier week — not total categories won. Unmodeled and irrelevant to the
  draft; noted so nobody adds a "total cats" tiebreak by assumption.
- **Playoff tie.** Yahoo's default is higher seed wins; a private commissioner
  can set "best regular-season record vs opponent", which in basketball
  categories is the most category wins (Yahoo help SLN6539). The champion won
  three rounds 5-4 last season; a 4-4-1 round would have gone to the seed or
  to the head-to-head record depending on this setting. Owner-only.
- **Lineup mode.** Daily-Today applies adds and drops at once; Daily-Tomorrow
  sets an 11:59 PM PT deadline the night before; under both, a man locks at
  his own tip-off (Yahoo help SLN22673, SLN6775). Owner-only; it changes
  in-season streaming agility, not the draft.
- **Autopick and pre-rank.** If the clock runs out or the connection drops,
  Yahoo autopicks from the manager's pre-draft ranking (starters before bench,
  position-balanced), falling back to Yahoo's default ranking (Yahoo help
  SLN6163). A Chrome extension ("Custom Player Rankings Import Tool") loads
  a CSV into that list; the do-not-draft list is separate and manual. Today
  the fallback would be XRank, not the board — D-G4.
- **XRank and ADP.** XRank blends six Yahoo analysts with RotoWire; ADP is
  the average pick across Yahoo mock and real drafts (Yahoo's football
  explainer; the basketball construction is presumed the same). The Mkt
  column's "ADP, else XRank" is the right pairing: ADP is what the room
  does, XRank is what the room is shown.
- **NBA Cup final.** Outside the regular season for the NBA (nba.com FAQ:
  "All Emirates NBA Cup games will count toward the regular-season standings
  except the Championship") and excluded by Yahoo. Every team gets two
  counted games in the Dec 4 to 11 window (the 22 non-qualifiers on off
  nights); the finalists play a third that counts for nothing.
- **Position eligibility.** Yahoo's basketball help page (SLN7057) says
  eligibility is set from box scores, past performance, outside trackers and
  its reporters, that changes are rare, and that commissioners can add but
  not remove positions. There is no games-at-a-position threshold as in
  baseball. So the eligibility the draft room shows on Oct 14 is, for nearly
  every man, the eligibility he carries through March — which is why the
  pool should carry the room's set, not the rankings article's (D-G3).

## 7. What three seasons of your league taught the system, and what is still unsure

Learned and in the code: the bracket decides the title (champions' record
ranks 2, 7, 7; the best record has never won), the room reaches past value
early (eight or nine of eleven opponents; the owner's +24.3 reach index was
the room's best and produced the best record), the weekly variance of a
strong team (observed sd 1.56 cats a week against the model's 1.40), the
fixed rotation of opponents (seven twice, four once; the simulator shuffles,
which is acceptable), loyalty pairs at chance league-wide with a few named
exceptions, and the owner's own profile (value-first, risk-tolerant at the
right price, no IL+ stash drafting).

Still unsure, in the order it matters for Oct 14:

1. Whether the 2026-27 league renewed with playoffs starting week 19 (Mar 8)
   — the 23-week calendar makes "last three weeks" a different window (weeks
   21 to 23, Mar 22 to Apr 11). One screenshot of the settings page answers
   this and G8, G9 and G14 together (D-G5).
2. Which positions the draft room will show for the 29 D57-1 names and the
   rest of the pool (D-G3).
3. The dates of the 30 knockout-window games (known after Nov 27; week 7's
   counts are complete in number, two per team, and incomplete in dates).
4. The two 14-day weeks in the weekly model (in-season, D-G7).
5. The playoff-tier objective, E9 (D-G6).

## Watchlist

- **League settings page** (owner): playoff start week and number of rounds
  for 2026-27, the playoff tiebreak rule, Daily-Today or Daily-Tomorrow, the
  pick clock, the draft's time zone.
- **Draft-room positions**: the Yahoo player list's eligibility for the pool
  before the final pre-draft build (D57-1, D-G3).
- **Cup knockout dates** (Nov 28): re-run `build_schedule.py`; week 7 fills
  in, nothing else moves.
- **Fresh Yahoo ADP paste** in early October (carried from 9/29).
- **Duren's qualifying-offer deadline** 11:59 PM Thursday Oct 1 (carried
  from the 9/30 report).

## Open-item receipts

| item | query run (2026-09-30) | dated finding |
|---|---|---|
| Yahoo 2026-27 game weeks | WebSearch on Yahoo's schedule analysis and RotoWire's schedule-impact piece (both domains egress-blocked for fetch; summaries only) | week 1 Oct 20 to 25; week 7 Nov 30 to Dec 13 and week 17 Feb 15 to 28 are 14 days; 23 weeks; default playoffs weeks 20 to 22 (Mar 15 to Apr 4); the seven published facts in §3 |
| NBA calendar | nba.com fantasy calendar article fetched; nba.com Cup group-play page fetched | opening night Oct 20; group play Oct 30 to Nov 27; quarterfinals Dec 4 and 5, semifinals Dec 8 and 9, final Dec 11 at Hinkle Fieldhouse; All-Star Feb 19 to 21; season ends Apr 11 |
| Cup final and standings | nba.com Cup FAQ fetched | "All Emirates NBA Cup games will count toward the regular-season standings except the Championship"; the 22 non-qualifiers play two regular-season games on off nights |
| schedule | Basketball-Reference NBA_2027 month pages, seven fetched | 1,200 dated games, 80 per team, 60 marked "NBA Cup"; nothing dated Dec 4 to 11 |
| Memphis cross-check | WebSearch on Memphis' Mar 15 to Apr 4 games | Yahoo's Memphis listing: Mar 15, 17, 18, 20, 22, 24, 25, 28, 30, Apr 2, 4 — eleven, matching the table |
| position eligibility | WebSearch restricted to help.yahoo.com | SLN7057: editorial eligibility, changes rare, commissioners add only |
| tiebreaks | WebSearch on Yahoo help | SLN35744 regular season (last week's percentage, then earlier weeks); SLN6539 playoffs (higher seed default; record-vs-opponent option, category wins in basketball) |
| lineup mode | WebSearch on Yahoo help | SLN22673 and SLN6775: Daily-Today immediate, Daily-Tomorrow 11:59 PM PT deadline; locks at tip-off under both |
| pre-rank and autopick | WebSearch on Yahoo help and the Chrome Web Store | SLN6163: autopick fills from the pre-rank, starters first, position-balanced; the extension imports a CSV |
| XRank and ADP | WebSearch | Yahoo football explainer: XRank six Yahoo analysts plus RotoWire; ADP from Yahoo mock and real drafts [SINGLE-SOURCE for basketball] |
| rest rules | WebSearch twice (ESPN, nba.com, Yahoo summaries) | Player Participation Policy unchanged; no 2026-27 change found |

## Bounds

- Yahoo's week structure was read through a search summary (the page is
  egress-blocked); the mechanical validation in §3 is what makes it
  EVIDENCE rather than a quoted claim. If Yahoo ever re-cuts a week, the
  seven checks fail loudly on a re-run.
- The playoff window assumes the league's 2026-27 setting is still
  "playoffs start week 19" (A1). Under a different setting the table's other
  columns apply; nothing else in the report changes.
- The 30 knockout-window games are undated; week 7 is complete in number,
  not in dates.
- The streaming footprint in §4 is an inference from two numbers, not a fit.
- XRank's construction is sourced from Yahoo's football explainer, not a
  basketball page.
- No claim here rests on a direct read of a blocked sports domain.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D-G1 | Ship E14: port the eight-team no-bye bracket from `format_delta.py` into `arena.py` and re-run the six live-room retros so the debriefs and the ledger's live rooms carry real-bracket champ% and playoff%; older ledger mocks keep their dual report | yes, before Oct 14, as a deck-plane PR that restates the retro numbers |
| D-G2 | Keep `report/schedule/` in the kit ritual (re-run on Nov 28 for the knockout dates) and add a display-only playoff-games hint to the card rows from round 8 (the man's team's games in weeks 19 to 21), no ordering change | kit artifact lands with this report; the card hint follows D-G5, red-first, with the E22 bars as the regression check |
| D-G3 | Make D57-1 required: set both planes' positions from the Yahoo draft room's display before Oct 14 (the mock-57 recap already holds the room's set for 156 men; the owner pastes the room's player list for the rest) | yes, at the final pre-draft refresh |
| D-G4 | Export a Yahoo pre-rank CSV from the deck's balanced-value order, with the veto list as the do-not-draft entries, for the Chrome import extension, so a dropped connection autopicks from the board rather than from XRank | yes, at the final pre-draft build |
| D-G5 | Owner: confirm on the league settings page that 2026-27 playoffs start week 19 with three one-week rounds (Mar 8 to 28), plus the playoff tiebreak, lineup mode, clock and time zone — one screenshot | the report assumes weeks 19 to 21 = Mar 8 to 28 |
| D-G6 | E9: measure ΔECW against the projected top-eight rosters instead of all eleven, under a pre-registered bar and a re-baseline | after the draft |
| D-G7 | Weekly model: carry the two 14-day matchups (weeks 7 and 17) and the schedule's game counts for the in-season advisor | after the draft |

## Provenance

- Inputs: the two repos at kit main d278646 and deck main 6426a59 (the
  league file, the scoreboard CSV, the profiles, `arena.py`,
  `format_delta.py`, the deck's engine block); eleven dated WebSearch
  summaries and four direct fetches (nba.com ×3, Basketball-Reference ×7
  pages) on 2026-09-30.
- Every number in §3 and §4 is the output of `report/schedule/build_schedule.py`
  (two runs, byte-identical) or of a one-off read of the scoreboard CSV; the
  bracket numbers in §2 are copied from the league file's measured table.
- Not verified: nothing here rests on a direct read of a blocked sports
  domain; the Yahoo help pages are cited by id from search summaries.
