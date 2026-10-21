# After-report — Trending-players early-warning: how to build it (research only)

**Owner's request (2026-10-20):** "4, research more - then provide a report on how to
computationally build." Item 4 of the FantasyBot proposals: a breakout early-warning that
crosses platform-wide add/drop trends against the kit's engine. This report designs the build;
nothing was built and no projection line, tag or roster changed.

**Analyzed:** one live `get_trending_players` call (sport=nba, type=add, limit=15,
lookback=24h), made 2026-10-20 and pinned at `data/source/fantasybot/trending_sample_2026-10-20.json`
(sha in git); crossed against `data/league_state.json` (FantasyBot pull, as-of 2026-10-20) and the
season pool (`SEASON_POOL=data/season/pool_season.csv`, lines v69). Method: mechanical name fold
(`verify_rosters.norm`), kit 9-cat z summed over CATS.

**Headline.** The tool is rich enough to build from today (per-player: platform add count,
current per-game line, minutes, games this week, back-to-backs, status). But the obvious screen —
"trending AND positive kit z" — would have fired on **zero of 15** names today, because 10 of 15
are already rostered in this league and the 5 free ones carry season z from −2.36 to −5.81
(EVIDENCE: the cross below, run 2026-10-20). The right design is a **staleness detector**: flag
trenders whose *live per-game line or minutes exceed our projection* — the market saying our line
is old — and route hits to the WO-5 review queue as leads, never as auto-adds.

## 1. What the tool returns (EVIDENCE, live call 2026-10-20)

Per player: `count` (adds across fantasy platforms, e.g. Leonard Miller 23,823 in 24h),
`perGame` (pts/reb/ast/stl/blk/3pm/tov/fg%/ft%/min — current season), `gamesThisWeek` /
`gamesLeftThisWeek`, `backToBacks`, `status` (e.g. "Day-to-day (right groin)"), plus
FantasyBot's own `boardRank` and `categoryValuePerGame` — the last two are **not used**
(owner rule 2026-10-20: their grades evaluate nothing; the kit's engine does the evaluating).
`type` takes "add" or "drop"; `lookback_hours` 1–168.

## 2. The cross, run today (record: command output 2026-10-20)

| trender | adds 24h | FA here | kit season z |
|---|---|---|---|
| Leonard Miller | 23,823 | Y | **not in pool** |
| Isaiah Jackson | 22,519 | n | −4.54 |
| Jalen Smith | 17,958 | n | −3.69 |
| Rui Hachimura | 17,549 | n | −2.62 |
| Davion Mitchell | 16,011 | n | −3.15 |
| Khaman Maluach | 12,618 | n | −4.17 |
| Cason Wallace | 12,609 | n | −0.50 |
| Derrick Jones | 10,071 | Y | −3.48 |
| Keaton Wagler | 8,096 | n | −3.01 |
| Mitchell Robinson | 7,734 | n | −2.13 |
| Precious Achiuwa | 6,760 | Y | −4.10 |
| Alex Caruso | 5,139 | Y | −2.36 |
| Jeremiah Fears | 5,000 | n | −3.83 |
| Nique Clifford | 4,860 | Y | −5.81 |
| Cedric Coward | 4,830 | n | −1.98 |

Three findings (EVIDENCE, one 24h sample — rates stay rates):
1. **This league is fast**: 10/15 trenders already rostered. The edge is not "hear about
   breakouts" but "hear about them before the 2 of 12 managers who move fastest".
2. **Season z is the wrong screen**: a breakout's season z lags by construction (July baseline,
   season GP). A screen demanding z > 0 fires on 0/15 today and would nearly always fire on 0.
3. **Pool coverage is a real failure mode**: the #1 trender (Leonard Miller, 23,823 adds) is not
   in the 335-player pool at all. A naive join silently drops exactly the names the tool exists
   to surface.

## 3. The computational build (proposed, not built)

**Script** `scripts/trend_watch.py`, morning step (non-fatal), +2 FantasyBot calls/day
(adds + drops, limit 25, lookback 24h), responses read mechanically from the session transcript
like league_live/matchup_live; raw pinned under `data/source/fantasybot/trending_<date>.json`.

**Signal, per trending ADD, in order:**
1. Resolve via `norm` + the kit aliases. **Not in pool → always surfaces** ("out-of-pool trender,
   N adds") as a WO-5 lead — never silently dropped (finding 3).
2. Drop if rostered in this league and not mine (nothing to do) unless on MY team (hold signal).
3. For FAs here, compute the **staleness gap**: FantasyBot `perGame.min` minus our projected
   minutes, and live per-game vs our per-game in the counting cats. Flag when minutes gap ≥ +6
   or any two counting cats exceed ours by ≥ 25% (both thresholds are stated defaults for the
   owner to re-tune — D-SD-1 class, INFERENCE not measurement).
4. Rank flagged names by platform adds × staleness; emit `data/news/trend_watch_<date>.json`,
   a brief line ("Market moving, our line may be stale: ...") and a small deck note on the FA pane.
5. **Never a pool edit**: every hit is a WO-5 queue lead with its receipt (adds count, live line,
   our line, gap), owner decides.

**Drops side** (1 call): trending drops that are rostered by rivals = early signal of who may hit
waivers; joins the rival-vulnerability picture; display only.

**Cost:** +2 calls/morning (shared daily limit; today's usage ran ~30 calls without hitting it —
EVIDENCE for today only, the limit itself is UNVERIFIABLE from here: no documented number found in
the tool's descriptions, and the service only reveals it by refusing).

**Validation plan (red-first):** fixture-based tests for the resolver (out-of-pool surfacing,
alias fold, rostered-drop), threshold tests on a synthetic stale line, and a two-week paper run
in the morning report before any deck card ships — grade: of the names it flags, how many get
added by a rival within 72h (the "would it have beaten the league" measure).

## 4. Verdict

**HIGHLY RECOMMEND** building the staleness-detector form (steps 1–5): ~2 calls/day, no engine
change, feeds the existing WO-5 review instead of creating a new decision path. Demoted from
MUST ADD because today's sample shows the league already absorbs most trends — the measured
two-week paper run decides whether it earns a deck card. **NOT NEEDED**: the naive "trending +
positive z" screen (0/15 today) and any use of FantasyBot's boardRank/categoryValuePerGame.

## 5. Bounds

*Out of scope by design:* drops-side analysis beyond the sketch; MLB/NFL/NHL; sizing the add
counts against Yahoo-only adds (different platform mix). *In scope, unverified:* one 24h sample
only — day-to-day variance of the trending list NOT-ATTEMPTED (one more call tomorrow settles
it); the shared daily call limit's actual number UNVERIFIABLE as above; whether `perGame` is
current-season-to-date or a blend — ATTEMPTED (compared Miller's 6.0 pts/12.6 min against a
box-score-shaped line; consistent with season-to-date) but not confirmed against a second source,
so treated as INFERENCE.

## 6. Decision sheet

- **D-TW-1:** build `trend_watch.py` as designed (go / adjust thresholds / not now).
- **D-TW-2:** if built, paper-run two weeks before the deck card (recommended) or ship the card
  immediately.
- **D-TW-3:** include the drops-side rival signal (1 extra call) or adds only.

## 7. Provenance

Produced 2026-10-20 (owner-local) in session session_01QjgeRdpDaWgSJmGKRG8fTU from one live
`get_trending_players` call (raw pinned beside this report's data path) and the session's own
cross (command + output in the session transcript). Re-verify: rerun the cross against
`data/source/fantasybot/trending_sample_2026-10-20.json` and today's `data/league_state.json`.
