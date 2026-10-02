# After-report — draft_60: the ninth live-human room from the REAL slot 10, the fourth on the concise card, the first with the re-numbered history and the advice line live — the card followed at eleven of thirteen turns

**Owner request (2026-10-02, verbatim):** "Here is a live pick by pick mock draft
for your analysis:" — the deck tool's pick-by-pick feed and Yahoo's round-by-round
recap, pasted after the Friday-morning pull.

**Room:** public Yahoo mock, 12 × 13, owner seat 10 (the real league slot; random
humans — a practice rep, not opponent intel; none of the eleven seat names is a
modeled league-mate). **Deck used:** v42 (rev `6ae36ab`, the Friday-morning
second-pull build; pool sha `75a4994b4a59`, 334 rows; Porziņģis veto live; the
D59-1 re-numbered history and the D59-2 advice line live) — or v41, which carries
every value byte-identical (the second pull changed notes only), so the grade is
the same; proved by replay: the owner's own echoes at #15 ("0.015 behind 🎯 Jalen
Williams") and #106 ("0.405 behind 🎯 PJ Washington") reproduce on the page's own
engine as 0.015 and 0.405. **Method:** the recap was resolved to pool names by the
tracker's own resolver (156 of 156) and the state checked snake-consistent; the
grade is the deck plane's machine-derived retro (`yahoo-fantasy-basketball`
`arena/results/m60_*.json`, debrief `debrief_2026-10-02_mock60_slot10.md`, deck
card replayed from the v42 page, title odds on the league's real eight-team
bracket). Every figure below is read from those files; none is eyeballed.
Verification: this file passes `report/check_report.py`; receipts below.

Pull window: 2026-10-02 → 2026-10-02 (analysis run 2026-10-02 against the v42 pool
and the 10/01 market file; not a roster pull — the two 10/02 pull-log rows cover
the window).

**Headline.** Rank 1 of 12 in expected weekly category wins (5.419 against 4.935 for seat 8, aesses9), favored in all 11 head-to-heads; title odds **33.02 percent on the league's real bracket** (rank 1 of 12) — back to first from the real seat after mock 59's second, with the card followed at 11 of 13 turns, the most of the nine live rooms. The two deviations read differently. Durant at #15 (card #6, 0.015 behind Jalen Williams, who waited to #34 as the survival read said he would) sits 5th of 296 legal picks in hindsight: the best alternative, Chet Holmgren, is worth +0.073 categories a week (35.98 percent). Murray-Boyles at #106 (card #87, 0.405 behind PJ Washington, with the round-9+ reminder on the echo) is the room's one real cost: 57 of 212 legal picks grade better, Gafford by +0.181 a week and +6.47 points of title odds (39.49 percent). Following the card's chain self-consistently grades 43.14 percent (Jamal Murray at #15, Anthony Davis at #34, Payton Pritchard at #63, Zach LaVine at #82, Mikal Bridges at #87, Daniel Gafford at #106). The D59-2 advice line fired once, at #15 — "Jamal Murray now, Derrick White next turn (82% to survive)" — and the owner took a third path that still landed Williams and White; that arm grades 32.31 percent. The survival chips posted their best out-of-sample Brier yet (0.175 against a 0.236 base rate); the draft room's positions matched the pool on all 156 picks for the first time; the tool log, including the insert D59-1 was built for, replayed on the real page with zero drift.

## 1. Validation vs the Yahoo recap

| check | result |
|---|---|
| picks in the recap | 156; all 156 "Last, First" lines resolved to a pool name by the tracker's resolver (diacritics, suffixes, "P.J." included); no UNKNOWN |
| snake attribution | all 156 seats match the round parity; the owner's 13 picks sit at #10, #15, #34, #39, #58, #63, #82, #87, #106, #111, #130, #135, #154 |
| owner's roster | Towns, Durant, Jalen Williams, Derrick White, Dyson Daniels, Herro, Mikal Bridges, Josh Hart, Murray-Boyles, Mamukelashvili, PJ Washington, Lendeborg, Vassell — identical to the recap's "My Team" |
| cast | seats 1–12: Gabriel, Tim, Rien, Edward, Joseph, Devin, Pharmacie, aesses9, jose, **David (10)**, Steven, shiny |
| positions shown by the draft room vs the pool | **0 of 156 differ** — the first room since the 10/01 position sync (D-ADP-3) where the room and the pool match on every drafted man (see §7) |
| state | `arena/data/states/draft_state_60.json`, md5 `9023d2d25d41be108230a1a90f77c3fc` |

## 2. The team, replayed

[EVIDENCE: `m60_final.json`, `m60_arms.json`, `m60_followcard_grade.json`,
the debrief's headline table]

| roster | ECW (cats/week vs the average opponent) | head-to-heads favored | championship rate, 18,000 seasons, real 8-team bracket | playoff rate | swaps |
|---|---|---|---|---|---|
| as drafted | 5.419, rank 1 (next 4.935) | 11 of 11 | **33.02%** (rank 1) | 99.83% | none |
| follow-card, self-consistent (arms stage) | 5.676, rank 1 (next 4.933) | 11 of 11 | **43.14%** (rank 1) | 99.98% | Jamal Murray at #15, Anthony Davis at #34, Payton Pritchard at #63, Zach LaVine at #82, Mikal Bridges at #87, Daniel Gafford at #106 |
| card at #15 only (Jalen Williams up, Durant to #34) | 5.419, rank 1 (next 4.935) | 11 of 11 | **33.02%** (rank 1) | 99.83% | Jalen Williams at #15 |
| card at #106 only (PJ Washington up, Murray-Boyles to #130) | 5.419, rank 1 (next 4.935) | 11 of 11 | **33.02%** (rank 1) | 99.83% | PJ Washington at #106 |
| advice line at #15 (Jamal Murray now; Derrick White came at #39 as drafted) | 5.411, rank 1 (next 4.939) | 11 of 11 | **32.31%** (rank 1) | 99.74% | Jamal Murray at #15 |
| hindsight single swap Chet Holmgren at #15 | 5.493, rank 1 (next 4.926) | 11 of 11 | **35.98%** (rank 1) | 99.89% | Chet Holmgren at #15 |
| hindsight single swap Anthony Davis at #34 | 5.495, rank 1 (next 4.934) | 11 of 11 | **36.63%** (rank 1) | 99.91% | Anthony Davis at #34 |
| hindsight single swap Anthony Davis at #39 | 5.419, rank 1 (next 4.939) | 11 of 11 | **35.09%** (rank 1) | 99.82% | Anthony Davis at #39 |
| hindsight single swap Zach LaVine at #82 | 5.423, rank 1 (next 4.937) | 11 of 11 | **33.91%** (rank 1) | 99.85% | Zach LaVine at #82 |
| hindsight single swap Isaiah Hartenstein at #87 | 5.456, rank 1 (next 4.926) | 11 of 11 | **34.77%** (rank 1) | 99.88% | Isaiah Hartenstein at #87 |
| hindsight single swap Daniel Gafford at #106 | 5.600, rank 1 (next 4.927) | 11 of 11 | **39.49%** (rank 1) | 99.97% | Daniel Gafford at #106 |
| hindsight single swap Kyle Filipowski at #135 | 5.429, rank 1 (next 4.935) | 11 of 11 | **33.36%** (rank 1) | 99.84% | Kyle Filipowski at #135 |
| hindsight single swap Kyle Filipowski at #154 | 5.438, rank 1 (next 4.931) | 11 of 11 | **34.04%** (rank 1) | 99.83% | Kyle Filipowski at #154 |

| category rank, as drafted | |
|---|---|
| weekly model | FG% 4 · FT% 6 · 3PTM 1 · PTS 4 · REB 5 · AST 9 · ST 1 · BLK 5 · TO 2 |
| 13-man z-sum | FG% 4 · FT% 5 · 3PTM 4 · PTS 6 · REB 8 · AST 10 · ST 1 · BLK 6 · TO 2 |

The shape is the most balanced of the nine rooms from this seat: threes and
steals 1st, turnovers 2nd, nothing worse than 9th (assists) in the weekly model,
and 11 of 11 head-to-heads favored — the earlier rank-1 rooms conceded assists
outright. Hindsight's single-swap ledger finds nothing at five turns and small
change at five more; its one large entry is Gafford at #106 (+0.181 a week,
+6.47 title points). The follow-the-card chain (Jamal Murray at #15, Anthony Davis at #34, Payton Pritchard at #63, Zach LaVine at #82, Mikal Bridges at #87, Daniel Gafford at #106) adds
+10.12 points, most of it from the same slot and from Anthony Davis at #34 (the
chain's pick once Jamal Murray is on the roster at #15). The two off-card turns
as plain reorders (Williams up to #15, Washington up to #106) grade identically to
as-drafted by construction: the same thirteen men.

## 3. Pick by pick — card vs owner vs hindsight

| pick | deck 🎯 (Top-5) | owner took | card rank · gap (blend) | hindsight best single swap (ΔECW vs final rosters) |
|---|---|---|---|---|
| #10 | Karl-Anthony Towns (Karl-Anthony Towns, Tyrese Maxey, Tyrese Haliburton, Anthony Davis, Chet Holmgren) | Karl-Anthony Towns | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #15 | Jalen Williams (Jalen Williams, Jamal Murray, Donovan Mitchell, Derrick White, James Harden) | Kevin Durant | #6 · +0.015 | Chet Holmgren +0.073 |
| #34 | Jalen Williams (Jalen Williams, Dyson Daniels, Derrick White, Anthony Davis, OG Anunoby) | Jalen Williams | #1 · +0.000 | Anthony Davis +0.076 |
| #39 | Derrick White (Derrick White, Desmond Bane, Dyson Daniels, Kyrie Irving, OG Anunoby) | Derrick White | #1 · +0.000 | Anthony Davis +0.000 |
| #58 | Dyson Daniels (Dyson Daniels, OG Anunoby, Payton Pritchard, Tyler Herro, De'Aaron Fox) | Dyson Daniels | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #63 | Tyler Herro (Tyler Herro, Payton Pritchard, OG Anunoby, Michael Porter Jr., De'Aaron Fox) | Tyler Herro | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #82 | Mikal Bridges (Mikal Bridges, Jalen Suggs, Zach LaVine, Josh Hart, Isaiah Hartenstein) | Mikal Bridges | #1 · +0.000 | Zach LaVine +0.003 |
| #87 | Josh Hart (Josh Hart, Isaiah Hartenstein, Day'Ron Sharpe, Yaxel Lendeborg, Jalen Suggs) | Josh Hart | #1 · +0.000 | Isaiah Hartenstein +0.036 |
| #106 | PJ Washington (PJ Washington, Yaxel Lendeborg, Sandro Mamukelashvili, Daniel Gafford, Aaron Gordon) | Collin Murray-Boyles | #87 · +0.405 | Daniel Gafford +0.181 |
| #111 | Sandro Mamukelashvili (Sandro Mamukelashvili, PJ Washington, Yaxel Lendeborg, Aaron Gordon, Daniel Gafford) | Sandro Mamukelashvili | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #130 | PJ Washington (PJ Washington, Yaxel Lendeborg, Collin Gillespie, Devin Vassell, Saddiq Bey) | PJ Washington | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #135 | Yaxel Lendeborg (Yaxel Lendeborg, Saddiq Bey, Devin Vassell, Cason Wallace, Fred VanVleet) | Yaxel Lendeborg | #1 · +0.000 | Kyle Filipowski +0.009 |
| #154 | Devin Vassell (Devin Vassell, Fred VanVleet, Jerami Grant, Christian Braun, Kyle Filipowski) | Devin Vassell | #1 · +0.000 | Kyle Filipowski +0.018 |

🎯 taken 11 of 13; Top-5 row 11 of 13

[EVIDENCE: `m60_replay.json`, `m60_deckcard_v42.json`, `m60_hindsight.json`;
card ranks are the deck's own JS replayed on the v42 page; the live echoes at #15
(0.015 behind Jalen Williams, rank #6) and #106 (0.405 behind PJ Washington, rank
#87) match the replay's 0.015 and 0.405]

Reading: the card was followed at eleven of thirteen turns, and at ten of
them hindsight has nothing or next to nothing to add (none at #10, #58, #63,
#111, #130; +0.003 at #82; +0.009 and +0.018 at #135 and #154; +0.036 at #87;
+0.000 at #39); the eleventh, #34, is Anthony Davis at +0.076 — the card's own
#4 row at that turn, the one swap the follow-card chain makes once Murray is on
the roster. The two deviations split. At #15 the owner took Durant over the
🎯 Jalen Williams by 0.015 — and then took Williams at #34, so the roster lost
nothing to the swap; hindsight's 5th-of-296 for Durant says the pick itself was
sound (Holmgren +0.073 is the best alternative, and he went #25 to seat 1).
At #106 the owner took Murray-Boyles, card #87 and 0.405 behind PJ Washington,
after the echo's round-9+ reminder — and then took Washington at #130, so again
the 🎯 was not lost; what was lost is the slot: 57 of 212 legal picks grade
better than Murray-Boyles there, Gafford (+0.181, went #127) the best of
them, and that one turn is +6.47 points of title odds. The D59-4 pattern
(Derrick White the 🎯 at #39 and passed on in three rooms) broke here: the
owner took White at #39, hindsight-best to within 0.0001.

Four turns carry a port-versus-page note (D59-5): the retro's Python card port
breaks exact blend ties by name order while the page breaks them by ΔECW, so the
port ranks Durant #5 at #15 where the page said #6 (Harden tied at 0.972), and
names Lendeborg the 🎯 at #106 and #130 and VanVleet at #154 where the page said
Washington, Washington and Vassell (three-way and two-way ties at 0.988, 0.990
and 0.994). The table above reads the page; the owner's echoes agree with the
page; the follow-card chain in §2 reads the port. One room, four tie turns: the
harness item is now worth doing (D60-1).

## 4. Tool-state integrity — the deck's board vs the recap, on the v42 page

The owner's tool log was rebuilt as an event list (156 events: 155 feeds, fourteen
of them the shared token wherever the echo said "assumed over" or "only X left" —
Johnson, Barnes, Mitchell, Murray twice, Ball, Williams, Wagner, Brown, Allen,
Sharpe, Wiggins, Collins, Sheppard; one Insert-at-# correction — Derik Queen at #95
after Claxton and Morant had been logged at #95–#96; no UNKNOWN feed, no halt, no
undo) and replayed through the real v42 page in headless Chromium [EVIDENCE:
`m60_tool_vs_truth.json`, `arena/data/events/m60_tool_events.json`]:

| finding | detail |
|---|---|
| positions differing from the recap | **0 of 156**; owner's roster identical; nothing missing, nothing extra |
| echo lines asserted | 156 of 156 (each feed's resolved name, the fourteen shared-token resolutions, the insert) |
| clock text under the feed title | correct after all 156 events |
| page errors | 0 |
| the Insert-at-# correction, live (D59-1's first live use) | the echo put Derik Queen at #95 for Seat 2 and moved the two later picks to #96–#97 with their seats recomputed; the history re-rendered Claxton as #96 for Seat 1 and Morant as #97 for Seat 1 from the state, exactly as the owner's log shows; the final board matches the recap pick for pick |
| the resume marker | the owner's log shows "— resumed: 47 picks logged —" after #47 (a page reload; the state persisted); the harness has no reload op, so the replay ran as one continuous session — the final state is identical either way |
| the injury-excluded guards | "Mark Williams skipped: injury-excluded" at #34 and "Shaedon Sharpe skipped" at #89 resolved the shared token past the excluded man; "heads-up: Jimmy Butler is injury-excluded on this board" at #152 logged the opponent's pick verbatim with the warning |

Fifth clean public room in a row on the concise card's page family (mocks 56–60
drifted none). D59-1 did on this room what the mock-59 report asked for: the two
picks that moved after the insert read with their new numbers and seats, and
nothing was logged under another seat.

## 5. Survival chips — seventh out-of-sample room for the refit

[EVIDENCE: `m60_survival.json`; the debrief's survival table]

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 60 (out of sample) | 50 | 0.491 | 0.620 | **0.175** | 0.236 |
| pooled with every earlier scored room (51 to 59) | 503 | 0.426 | 0.666 | 0.280 | 0.236 |

By chip in this room: BUY NOW 7 rows, mean predicted 0.111, 2 survived; TOSS-UP 13 rows, 0.307, 5 survived; quiet rows 30, 0.660, 24 survived; survivors called at two percent or less: none.

Seventh straight out-of-sample room under the base rate for the price-only
refit (0.178, 0.189, 0.183, 0.175 in the last four), and the best so far. By
chip the pattern is the one your league's own draft showed (D-LS-2): BUY NOW
rows survive more often than their probabilities say, TOSS-UP rows about as
often, quiet rows a little less. The pooled row still carries the pre-refit
rooms and is a history, not a grade. In this room the model said Jalen Williams
would wait at #15 (0.73) and PJ Washington would wait at #106 (0.55); both did.

## 6. The punt advisor, replayed

[EVIDENCE: `m60_advisor.json`, 23 pre- and post-pick moments across the owner's
turns; `m60_final.json` for the finish]

The room-relative advisor (D51R-3) never spoke in this room: at none of the 23
moments did a lean clear the two-turn hysteresis, so the strip carried no ADVISE
read at any owner turn. The pre-2026-09-21 advisor's z-sum leans surfaced
rebounds at #106–#111 and assists at #135–#154 without a button. The owner
declared no punt. The finish is the most balanced of the nine rooms: no category
worse than 9th weekly (assists), steals and threes 1st, turnovers 2nd. Advice
only, box left empty by design; a roster that concedes nothing is what the
advisor's silence means.

## 7. The draft room's positions now match the pool — 0 of 156

Mocks 57, 58 and 59 showed 28 or 29 of the drafted men with fewer positions in
the draft room than the pool carried. On 10/01 both planes took their positions
from Yahoo's draft-analysis paste (D-ADP-3, the owner's "yes"); this is the first
room since, and the room's display matches the pool on all 156 drafted men
[EVIDENCE: `scratchpad m60/positions_check.json`; the recap as pasted]. The
owner's roster reads the same in the room and on the deck (Jalen Williams SF,PF;
PJ Washington PF,C; Lendeborg PF). D-G3 (set positions from the draft room) is
answered by this room; it is on the sheet as D60-4 to close.

## 8. Repeat names on the card — the audit, re-run on this room

Same instrument as mocks 56–59 (`repeat_names_audit.mjs`, nine other rooms'
owner rosters substituted in at each turn, an empty roster, value-only and
ΔECW-only orders; the watch list Poeltl, Gafford, Brook Lopez, Cameron Johnson,
Braun, Eason) [EVIDENCE: `m60_repeat_names_audit.json`]:

| readout | mock 60 | mock 59 | mock 58 |
|---|---|---|---|
| owner turns where the #1 changes under at least one other room's roster | **12 of 13** | 10 of 13 | 10 of 13 |
| owner turns where the #1 changes under an empty roster | **12 of 13** | 10 of 13 | 8 of 13 |
| watch names on this room's Top-5 | Gafford at two turns (#106 4th, #111 5th), Braun at one (#154 4th); Poeltl, Lopez, Cameron Johnson and Eason at none | Poeltl at three turns, Braun at one | — |

The #1 depended on the roster at twelve of thirteen turns (only #10, the first
pick, is roster-blind by construction), and the empty-roster #1 from #58 on reads
Jarrett Allen, Allen, LaVine, LaVine, Gafford, Gafford, Braun, Braun, Braun while
the card said Daniels, Herro, Bridges, Hart, Washington, Mamukelashvili,
Washington, Lendeborg, Vassell — nine of nine decided by the roster as it stood.
The value-only #1 was Anthony Davis at four early turns and Fred VanVleet at the
last five; the card never put either first. Poeltl, the mock-59 question, was not
on the Top-5 at any turn here (card rank 89 at #10, drifting down as the room
priced centers), which is the audit showing the card reading this room rather
than repeating last room's names.

## 9. The two off-card turns, and the advice line's first live room

[EVIDENCE: `m60_advice_reads.json` (the advice line on the page's own Top-5
rows, pair_decision twin), `m60_pairarms.json`, `target_wait_2026-10-02.json`,
`m60_followcard_grade.json`]

**The advice line's first live room (D59-2, shipped v40 as advice only).** It
fired at exactly one turn, #15: on the page's rows (Williams, Jamal Murray,
Mitchell, White, Harden) it read "Jamal Murray now, Derrick White next turn (82%
to survive): +0.039 cats/wk over the pair", because Williams was 73 percent to
survive to #34 and Murray 5 percent to survive to #18. At every other turn it
stayed silent for the right reason: the 🎯 was under the 0.60 wait floor at
eight turns, the best pair at four. The owner neither took the 🎯 nor the
advice: Durant, rank 6, 1 percent to survive. What followed was the advice's
logic by another route — Williams came at #34 (the deck said he would), White at
#39 — and the roster the advice would have built (Murray at #15, White at #39,
everything else as drafted) grades a hair under as drafted, 32.31 percent against 33.02 as drafted. The
pre-registered pair rule, replayed as the marker across this room, moved the 🎯
at two turns (#15 to Murray, #82 held Bridges and took LaVine at #87) and
finished at the same ECW and title odds as the blend chain (5.676,
43.14 percent) — the experiment's advice-only verdict holds on its first
out-of-sample room: no loss, no gain.

**A wording defect, found here.** The twin's sentence names the highest-ΔECW
partner as the "next turn" man, whatever his survival: on the port's row order
(Durant 5th by name-order tie-break) the same turn read "Jamal Murray now, Kevin
Durant next turn (1% to survive)". The page's rows happened to produce a sensible
partner (White, 82%); the port's did not. The sentence should name the first
partner the model expects to be there — a wording change in both twins,
red-first (D60-3).

**Does the 🎯 wait? — the instrument, with this room added.** Across mocks 56–60
the 🎯s passed on with a market rank 24 or more slots below the pick were still
there at the owner's next turn 6 of 7 times (this room added Williams at #15,
+26, and Washington at #106, +42 — both there), and two turns on 2 of 7;
near-price 🎯s (under 12 slots) 5 of 10 and 0 of 9. The card's
survival read is the number to trust on a deep 🎯; this room followed it twice
and was right twice.

## Watchlist

- **D60-1, the port's tie-break**: four turns in one room now; align the retro's
  card port with the page's ΔECW rule and re-run mocks 56–60's chains.
- **D60-2, #106**: Murray-Boyles at card #87 after the reminder — the room's one
  measurable cost (+6.47 title points). His line is a WO-5 item.
- **D60-3, the advice line's partner wording**: both twins, red-first, next deck
  build.
- **D-G3 / D60-4**: positions matched the room 156 of 156; close it.
- **The D59-4 pattern** (White passed at #39) broke: taken, hindsight-best.
- Carried: D-1002-1 (Knueppel), D-1002-3 (camp first-unit signals), D58-2
  (UPSIDE chip), D58-3 (ceiling experiment), D58-4 (team-stack ⚠), D59-3 (Yang
  Hansen's row — not drafted here), the league settings screenshot (D-G5), the
  preseason projection refresh (WO-5, after two games per team).

## Open-item receipts

| item | query run (2026-10-02) | dated finding |
|---|---|---|
| (this analysis) | machine replay only — no web research in this report | pull receipts for the window live in `after-report-2026-10-02.md` and `after-report-2026-10-02-morning.md` |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the Friday-morning pull's dedicated queries, same day (after-report-2026-10-02-morning.md) | all HELD on 2026-10-02; Ingram (#73, seat 1) and Mathurin (#142, seat 3) were drafted by opponents in this room; nothing here changes a card |
| Jalen Duren | the Friday-morning pull (after-report-2026-10-02-morning.md) | re-signed 10/1, card retired; drafted #32 by seat 8 here |

## Bounds

- Championship figures are on the real eight-team bracket (E14); the arms use
  18,000 CRN seasons on three seeds (seed set 2 for the pair-arms replay:
  33.68 / 43.89 / 43.89 percent as drafted / blend chain / pair chain).
- The room was drafted on v42 or v41 and graded on v42's lines; every value is
  identical between the two. A different line set grades every room differently.
- The follow-the-card chain is the retro's Python port of the card; at four tie
  turns its 🎯 differs from the page's (§3). The page's reads are in §3 and §9.
- The advice line's reads are the Python twin of pairDecision on the page's
  rows, not a capture of the rendered sentence; the two are bit-identical by the
  card suite's fixtures, and the "next turn" wording defect is in both.
- The resume after #47 was replayed as one continuous session (no reload op in
  the harness); the final state is identical either way.
- The target-wait table pools five rooms of random public opponents; it says how
  the public prices the card's deep names, not how the eleven league-mates will.
- The advisor's silence is the replay's read of the engine at each owner turn;
  the owner's screen at the time is not recorded. No punt was declared (A1).

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D60-1 | `live_retro.py`'s card port breaks exact blend ties by name order (its pre-D51R-4 rule); the page breaks them by ΔECW. Four turns in this room (#15 rank, the 🎯 at #106, #130, #154). Align the port with the page's rule for rooms drafted on v33 or later, keep the old rule by pool tag for the earlier rooms, and re-run mocks 56 to 60's chains (D59-5, re-put with the evidence)? | yes — next harness change, red-first, before the next live room |
| D60-2 | Murray-Boyles at #106: card #87, 0.405 behind, after the round-9+ reminder; hindsight +0.181 a week, +6.47 title points (Gafford). Is there a reason about Murray-Boyles the card is missing (a Toronto role the line does not carry) that belongs on his row, or was it a conviction pick the card should simply log? | no card change; review his line at the WO-5 refresh with the preseason box scores, and log the pick as a conviction pick |
| D60-3 | The advice line's sentence names the highest-ΔECW partner as the "next turn" man regardless of his survival (on the port's rows at #15: "Kevin Durant next turn (1% to survive)"). Name the first partner the model expects to be there (survival ≥ 0.60, else the expected-value partner) in both twins, red-first? | yes — wording only, next deck build |
| D60-4 | D-G3 (set both planes' positions from the draft room): this room's display matched the pool on all 156 drafted men after the 10/01 sync (D-ADP-3). Close D-G3? | close; keep syncing from each Yahoo draft-analysis paste |
| D-1002-1 | Knueppel's tag | carried: hold until ruled out of the opener |
| D-1002-3 | camp first-unit signals (Lendeborg, Isaiah Jackson over Lopez) | carried: hold for WO-5 |
| D58-2 | UPSIDE chip from round 9 | carried: at the final pre-draft refresh |
| D58-3 | the ceiling experiment | carried: design doc first |
| D58-4 | NBA-team stack ⚠ at three or more | carried: next deck build, red-first |

## Provenance

- Inputs: the owner's tool log and Yahoo recap (this session, 2026-10-02),
  transcribed verbatim into `arena/data/events/m60_tool_events.json` and the
  recap into the state by the tracker's resolver (`hoops.py draft resync`).
- Every number is read from `arena/results/m60_*.json` and the debrief; the arms
  use 18,000 CRN seasons (seeds 11/23/47) on the real eight-team bracket; the
  audit, the deck card, the advisor and the tool replay ran the v42 page's own
  engine under node and headless Chromium.
- Not verified: nothing here rests on web research.

## In plain language

**What this was.** Your ninth practice draft from the real seat, on the deck as
it stood this morning. I rebuilt the room from Yahoo's recap, replayed your tool
log through the real page, and graded the roster the way every room has been
graded: expected weekly category wins against the eleven other rosters, then
18,000 simulated seasons on the league's real eight-team bracket.

**How it went.** First of twelve. The roster is favored against every one of the
other eleven and wins the title in about one simulated season in three
(33.02 percent), with a 99.8 percent playoff rate. It is also the most
balanced team you have drafted from this seat: first in threes and steals,
second in turnovers, nothing worse than ninth.

**What you did with the card.** You took the card's top name at eleven of
thirteen turns, the most of any room. The two exceptions:

- **#15, Durant.** The card had Jalen Williams first by a hair, and said he would
  probably still be there at your next turn. You took Durant, and Williams was
  still there at #34. Nothing lost. In hindsight Durant was the fifth-best of
  296 legal picks at that spot.
- **#106, Murray-Boyles.** The card had PJ Washington first by a wide margin and
  the echo reminded you of the round-9 rule. You took Murray-Boyles, and
  Washington was still there at #130, so you got him too. The cost is the slot
  itself: 57 of the 212 players available graded better there, and the best of
  them, Gafford, is worth about +6.5 points of title odds. That one pick is
  the only measurable cost in the room.

**The new advice line.** This was its first live room. It spoke once, at #15,
and said to take Jamal Murray now and Derrick White next turn, because Williams
would wait and Murray would not. You took neither path and still ended up with
Williams and White. Following its advice would have graded 32.31 percent.
One defect surfaced: the sentence can name a partner who is almost certainly
gone. It is on your sheet to reword.

**The tool itself.** Your 156 feeds and the one insert replayed on the real page
with zero mismatches, and the insert re-numbered the two picks after it exactly
as the mock-59 report asked. The draft room's positions matched the deck on all
156 players for the first time. The survival chips had their best room yet.

**Your decisions.** D60-1 fix the retro's tie-break (default yes). D60-2
Murray-Boyles: a note, or a conviction pick (default: review his line after the
preseason games). D60-3 reword the advice line's partner (default yes). D60-4
close the positions item (default close).
