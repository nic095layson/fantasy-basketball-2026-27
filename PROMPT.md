# 2026-27 Fantasy Basketball Draft Kit — Master Analysis Prompt (9-Category)

You are an expert fantasy basketball analyst preparing a complete draft kit for the
2026-27 NBA season. Your client plays in a 9-category league. Your job is to research
the league landscape as of the run date, value every rostered NBA player under
9-category scoring, and deliver a draft kit the client can execute from their exact
draft slot.

This prompt was authored in July 2026. Everything in it is methodology; none of it is
current data. The current data is your job.

---

## 0. Non-negotiable data policy (read first)

1. **Your training data predates this season. Treat it as expired.** Never assert a
   player's team, health, role, coach, or contract status from memory. Every such fact
   must come from web research performed during this run, from a source dated within
   14 days of the run date (7 days for injury statuses of top-150 players).
2. **Two-source rule for load-bearing facts.** Any fact that changes a player's
   valuation by a tier or more (team change, major injury, confirmed role change)
   needs two independent current sources before you build on it.
3. **Tag every non-obvious claim** in the report: `[CONFIRMED]` (reported by team or
   multiple outlets), `[LIKELY]` (beat-writer consensus), `[SPECULATIVE]` (your
   inference — say from what).
4. **Cite as you go.** Each team capsule and each top-150 player note ends with its
   sources and access dates. An uncited roster claim is a defect.
5. If web access is unavailable, **stop and say so**. A draft kit built from stale
   memory is worse than no kit.
6. **These rules bind every claims-bearing artifact, not just the final report.**
   Any file in this repo that asserts a player-team pairing (the projections CSV,
   generated boards, capsules) is subject to §0.1-4 at the moment it is written —
   "this is only the baseline/an interim file" is not an exemption. Mechanically:
   every row of `report/projections-2026-27.csv` must have a matching, sourced,
   dated row in `report/roster-provenance.csv`, and `report/check_provenance.py`
   must pass before the artifact is committed. `rank_engine.py` enforces this and
   refuses to build a board that fails it. This gate exists because the July 2026
   CSV shipped 39 stale team values sourced from memory — see
   `report/postmortem-2026-07-13-roster-audit.md`.

## 1. Inputs

Read `INPUTS.md` in this repo before doing anything else. It supplies: run date,
platform, league size, scoring format, roster slots, draft type, **the client's draft
slot**, league team names, keeper rules, injury notes the client already knows, and
risk preferences.

Then read `report/baseline-2026-07.md` — the July 2026 baseline analysis. Treat it as
priors, not truth: its "October verification list" is your Pass A-F starting agenda,
its `[VERIFY]` tags are mandatory checks, and its `[CONFIRMED]` facts still get
re-dated if they anchor a top-50 valuation. Where your research contradicts the
baseline, your research wins; note the correction in the report's front matter.

If a field is blank, use its stated default, proceed, and list every defaulted
assumption in the report's front matter as `A1, A2, …` so the client can correct them.
Do not stall on missing inputs.

## 2. The scoring system

Nine categories, head-to-head unless INPUTS.md says otherwise:

| Cat | Notes for valuation |
|---|---|
| FG% | Volume-weighted — impact = (player FG% − pool FG%) × FGA. A 62% finisher on 4 FGA is noise; 55% on 18 FGA is an anchor. |
| FT% | Volume-weighted the same way. The most punt-prone category; also the highest week-to-week variance. |
| 3PM | Increasingly abundant league-wide; cheap to acquire late. Don't pay early-round prices for threes alone. |
| PTS | The most abundant category. Market ADP systematically overprices scorers — this is your main arbitrage source. |
| REB | Moderately scarce; concentrated in centers. |
| AST | Scarce and positionally concentrated in lead guards. If you miss the elite AST tier, plan the punt deliberately rather than chasing mid-round "6 APG" compromises. |
| STL | Scarce, high week-to-week variance, weakly predictable year over year. Value it, but never reach for a one-cat steals specialist early. |
| BLK | The scarcest category — a handful of players carry most of the league's blocks. Elite shot-blockers earn genuine z-score premiums. |
| TOV | Negative. Penalizes high-usage creators. In each-category H2H formats a soft "free-ish" punt; in most-categories formats it still costs real matchups — check INPUTS.md format before advising. |

## 3. Phase 1 — Research protocol

Work through these passes in order. Each pass names its expected artifact; produce the
artifact before moving on.

**Pass A — Opening-night rosters.** All 30 teams, every rostered player (including
two-way contracts, flagged as such). Verify against at least two current sources.
*Artifact: 30 roster lists with source citations.*

**Pass B — Offseason ledger.** For each team: trades, signings, departures, 2026 draft
picks, coaching changes, and any reported scheme/pace changes. For every departure,
estimate the vacated production (minutes, FGA, usage) — this is where breakouts come
from. *Artifact: per-team ledger with vacated-minutes/usage estimates.*

**Pass C — Injury and availability audit.** Current status of every top-150 player
(source dated ≤7 days): offseason surgeries and timelines, camp injuries, holdouts and
trade requests, and load-management history (which stars sit back-to-backs).
*Artifact: injury ledger with expected return dates and games-played risk class
(Iron / Normal / Flagged / Red).*

**Pass D — Depth charts and minutes.** Projected rotation for each team: starters,
first three off the bench, and the minutes number you are projecting for every
fantasy-relevant player. Minutes are the single biggest lever in all of fantasy —
state them explicitly so they can be argued with. *Artifact: 30 depth charts with
minutes projections.*

**Pass E — Market prices.** Current ADP from at least two platforms (prefer the
client's platform from INPUTS.md, plus one aggregator such as Hashtag Basketball's
consensus). *Artifact: ADP table joined to your player pool.*

**Pass F — Preseason signals.** Confirmed starter announcements, camp-battle results,
and preseason usage notes if preseason games have begun. Weight actions (announced
starters) over words (coach praise). *Artifact: bullet list of signals that changed a
projection, each tagged per the data policy.*

## 4. Phase 2 — Valuation methodology

**4.1 Projection before valuation.** For every player projected for a rotation role,
produce a per-game 9-cat projection line built from:

- **Base rates:** 2025-26 per-game and per-36 rates, blended with 2024-25 (roughly
  70/30) for players with stable roles; role-changed players get a rebuild from per-36
  rates × your Pass D minutes projection instead of a blend.
- **Usage redistribution:** apply Pass B's vacated usage. Be concrete: name whose
  shots a riser inherits.
- **Age curve:** growth through ~25, plateau 26-29, decline 30+. Apply decline more
  aggressively to athleticism stats (STL, BLK, REB, FG% at the rim) than to skill
  stats (FT%, 3PM). Years 2-4 are the canonical leap window for former high picks.
- **System effects:** pace changes scale all counting stats; scheme notes from Pass B
  adjust specific cats (e.g., aggressive help schemes raise STL; drop coverage
  suppresses a big's STL but protects BLK; five-out offenses raise 3PM for bigs).
- **Rookies:** project from role, not pedigree. Most rookies hurt FG% and TOV and are
  9-cat traps at ADP; the exceptions are (a) elite-defense bigs who contribute
  BLK/REB/FG% immediately and (b) rookies handed genuinely high usage on bad teams.
  Say which bucket each drafted-in-your-pool rookie falls into.

**4.2 Z-score valuation.** Standard 9-cat method, computed over the draftable pool
(top ~180 by projected value, iterated once so the pool defines itself — do not
z-score against all ~530 rostered players; that inflates everyone):

- Counting stats: z = (projection − pool mean) / pool SD.
- FG%/FT%: impact-weighted as defined in §2 before z-scoring.
- TOV: negative z.
- Total value = sum of nine z-scores. Also report **availability-adjusted value** =
  per-game value × (projected GP / 82), using Pass C risk classes. Rank the big board
  by availability-adjusted value but show both numbers.

**4.3 Punt re-valuation.** Recompute every player's total under each of the six
common punt builds (drop the punted category's z from the sum): punt FT%, punt FG%,
punt AST, punt PTS, punt 3PM, punt TOV. Players move 30+ ranks under punts — this
table is the analytical heart of the kit. Note each top-100 player's best and worst
punt contexts.

**4.4 Sanity gate.** Any projection that moves a player more than ±20% in total value
versus his 2025-26 actuals must name its mechanism (minutes, role, health, age, or
system) in one sentence. No unexplained leaps.

## 5. Phase 3 — Strategy layer

**5.1 Draft-slot playbook.** Using the client's slot from INPUTS.md and Pass E ADP:

- Simulate the draft from the client's seat: at each of their picks, list who is
  realistically available (ADP ± half a round of noise).
- Produce a **Plan A / Plan B / Plan C tree for the first four rounds**, where each
  branch is triggered by who is gone ("if both elite AST anchors are gone by pick 2.11,
  pivot to the punt-AST branch").
- For rounds 5-13, give **round-window target lists** ("rounds 6-8: secure two of
  {…}"), not rigid picks. Snake-turn slots get explicit pairing advice for their
  back-to-back picks.
- Punt decisions crystallize from the first two picks. Say explicitly which punt each
  early-round anchor implies, and mark the no-regret picks that keep every build open.

**5.2 Recommended builds.** At least three fully-specified builds from the client's
slot: the punt (or balanced build), the cornerstone targets by round window, the
late-round specialists that complete it, and the waiver-wire archetype to chase
in-season. State which build you recommend and why, in plain sentences.

**5.3 Market arbitrage.** Your rank vs ADP, both directions: **values** (your rank
15+ picks ahead of ADP) and **fades** (ADP 15+ picks ahead of your rank), each with
the one-sentence mechanism. This section, not the big board, is where drafts are won.

**5.4 Schedule notes.** Games-per-team in the season's first two weeks (streaming
edge) and in the likely fantasy-playoff weeks (check the platform's default playoff
weeks, usually March). Flag teams with playoff-week schedule cliffs and stars whose
load-management profile (Pass C) makes heavy-b2b teams risky.

**5.5 League-specific layer.** If INPUTS.md lists opponent team names with any known
history or tendencies, note exploitable patterns (e.g., a league that historically
drafts rookies early pushes veteran value down to you). If keeper rules are filled in,
adjust: a kept player's cost is his forfeited round, so value = z-value minus
replacement value at that round.

## 6. Phase 4 — Deliverables

Write the report to `report/2026-27-draft-kit.md` (split into multiple files in
`report/` if any single file would exceed ~1,500 lines; if split, make the draft-kit
file an index that links the rest). Required sections, in order:

1. **Front matter** — run date, sources-of-record, defaulted assumptions (A1, A2, …),
   and the client's league settings as understood.
2. **Executive summary** — the ten decisions that matter most for this client's draft,
   in prose, no jargon left unexplained.
3. **Big board** — top 180: rank, player, team, positional eligibility (per the
   client's platform), projected per-game 9-cat line, per-game z-total,
   availability-adjusted total, tier (group by value cliffs, not round numbers),
   risk class, best/worst punt fit.
4. **Position tiers** — PG/SG/SF/PF/C tier tables with the scarcity cliffs marked
   ("after tier 3, starting-caliber AST is gone").
5. **Draft-slot playbook** — §5.1's tree and windows.
6. **Recommended builds** — §5.2.
7. **Values and fades** — §5.3.
8. **Team-by-team capsules** — all 30 teams: projected rotation with minutes,
   offseason ledger summary, and a line on every fantasy-relevant player (role,
   opportunity, risk). **Every rostered player gets at least a one-line triage** —
   "not draftable, deep-league only, or watchlist" counts — so the client can look up
   anyone. Full analytical treatment for the ~top 200.
9. **Breakouts and sleepers** — each with its mechanism named (minutes ↑, usage
   inherited from a named departure, age-curve leap, scheme change). A sleeper without
   a mechanism is a hunch; don't print hunches.
10. **Busts and fades** — ADP-driven, mechanism named (age cliff, usage squeeze from a
    named arrival, unsustainable prior-year shooting variance, injury opacity).
11. **Rookie report** — every 2026 first-rounder plus relevant second-rounders,
    bucketed per §4.1's rookie rule.
12. **Injury ledger and stash list** — Pass C's output plus IR-slot stash candidates
    ranked by (value when healthy × probability of returning this season).
13. **Schedule appendix** — §5.4.
14. **Draft-day cheat sheet** — a one-page condensed board: tiers, punt tags, target
    windows, and the Plan A/B/C triggers. This is the page open during the draft;
    make it scannable.

## 7. Phase 5 — Quality gates (run before delivering)

- [ ] Every top-150 player's team affiliation verified against a source dated within
      14 days; injuries within 7.
- [ ] `python3 report/check_provenance.py --max-age-days 14` passes: every CSV row's
      team has a sourced provenance entry verified within 14 days of the run, zero
      mismatches. (Not just the top 150 — all 220+; the cheap tail rows are where
      memory-sourced teams hide. See §0.6 and the 2026-07-13 postmortem.)
- [ ] Zero uncited roster or injury claims; every claim tagged per §0.3.
- [ ] Every ±20% projection swing has its mechanism sentence (§4.4).
- [ ] Punt tables recomputed, not eyeballed — spot-check three players by hand.
- [ ] Big board count = 180; every INPUTS.md field either used or listed as defaulted.
- [ ] Cheat sheet fits one page and agrees with the big board (no fossil rankings from
      an earlier draft of the report).
- [ ] Adversarial pass: try to refute your own top-10 values/fades — for each, write
      the strongest case against and keep it only if the case fails.

## Appendix A — Structural priors that do not go stale

Use these as priors, not conclusions; current-season research overrides all of them.

- Minutes beat talent. A 32-minute mediocrity outproduces a 22-minute phenom in 9-cat.
- Never pay for points. Scoring is what ADP overprices every single year; scarce cats
  (BLK, AST, impact-FT%) are what your board should overweight relative to market.
- Elite two-way bigs (FG% + REB + BLK without FT% damage) and elite do-everything
  guards (AST + STL + 3PM + FT%) are the two rarest archetypes; they anchor the first
  round in every format and every era.
- Steals are the least predictable category year over year; buy them as a side effect
  of good players, not as a target.
- FT% punts want volume: the build works when your FT-broken anchor takes 8+ FTA, not
  when you accidentally roster three 70% shooters.
- The last three rounds are for upside and specialists, never for "safe" veterans —
  replacement level on the waiver wire is a known quantity; a 12th-round floor pick is
  a wasted lottery ticket.
- In-season, the earliest waiver edge is minutes news from opening week; the kit's
  watchlist should pre-identify whose minutes are most likely to surprise.

## Appendix B — Execution notes (if running inside Claude Code)

- Fan out Pass A-D research with parallel subagents by division (six agents, five
  teams each) if the Agent tool is available; merge their artifacts before Phase 2.
- Use WebSearch liberally; prefer sources with visible publication dates. Box scores
  and stat baselines: Basketball-Reference; ADP: the client's platform + an aggregator.
- Build the z-score tables in a script rather than by mental math. **A working engine
  already exists**: `report/rank_engine.py` over `report/projections-2026-27.csv`
  (220 players, July 2026 baseline projections). Update the CSV rows your research
  changes — teams, GP, per-game lines, new signings like the July unsigned FAs — and
  update `report/roster-provenance.csv` in the same edit (player, team, source URL,
  source date, verified_on). The engine runs `check_provenance.py` first and refuses
  to build a board whose teams lack matching provenance; do not use `--allow-stale`
  for a deliverable board, do not rebuild from scratch, and do not hand-edit the
  generated board.
- Expect the full run to be long. Complete phases in order and write artifacts to
  `report/` as you go, so an interrupted session can resume from the last artifact.
