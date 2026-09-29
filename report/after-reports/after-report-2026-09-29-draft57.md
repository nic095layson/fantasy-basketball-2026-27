# After-Report — draft_57: sixth live-human mock from the REAL slot 10, the first room on the concise card, and the roster-balance question

**Owner request (2026-09-29, verbatim):** "Here is the first, pick by pick,
live mock draft with this new tool layout." — the deck tool's pick-by-pick
feed and Yahoo's round-by-round recap (the authoritative record). Mid-analysis,
a second ask, with a screenshot of the card at pick 128: "I followed the card's
suggestion, but was also getting the 'Roster Imbalance' warning. In addition
to categorical strength, does the tool also account for if I am loading too
much towards one position category (and weak on the others?)" — answered in
§6, from the code.

**Room:** public Yahoo mock, 12 × 13, owner seat 10 (the real league slot;
random humans — a practice rep, not opponent intel; none of the eleven seat
names is a modeled league-mate). **Deck used:** v34 (rev `0dfbe77`, the
concise-card and YOUR PICK build published the same evening) — its data,
engine and judgment blocks are byte-identical to v33 (rev `a3b4d31`, pool sha
`6efb01cd772b`, 334 rows), so the room grades on the v33 pool as its own
pool; Porziņģis veto live. **Method:** the recap was resolved to pool names
by the deck's own resolver (156 of 156, no unresolved name) and the state
checked snake-consistent; the grade is the deck plane's machine-derived retro
(`yahoo-fantasy-basketball` `arena/results/m57_*.json`, debrief
`debrief_2026-09-29_mock57_slot10.md`, deck card replayed from the deck he
drafted against). Every figure below is read from those files; none is
eyeballed. Verification: this file passes `report/check_report.py`; receipts
in the section below.

Pull window: 2026-09-29 → 2026-09-29 (analysis run 2026-09-29 against the
9/29 re-derived pool and the 9/22 market file; not a roster pull — the 9/29
pull-log rows cover the window).

**Headline.** The first room on the concise card logged clean and drafted
to **rank 1 of 12** on every readout: ECW **5.271** cats/week (next seat
5.052), favored in **11 of 11** head-to-heads, board rank 1 by 13.5 z,
championship rate **35.23%** over 18,000 simulated seasons [EVIDENCE:
`m57_final.json`, `m57_arms.json`]. On the same re-derived lines the earlier
rooms from this seat read 39.8 / 23.7 / 29.3 / 38.3 / 25.5% (mocks 51–54,
56; `after-report-2026-09-29-final-check.md`), so this roster sits in the
middle of the set, not above it: the four off-card picks — Tatum at #10,
Kyrie at #39, Lillard at #58, McDaniels at #87 — are where the title odds
went. Following the card self-consistently scores **52.96%** (ECW 5.678)
[EVIDENCE: `m57_followcard_grade.json`], in line with the 45–57% the card
recovers in every live room on these lines. The owner took the 🎯 at **9 of
13** turns and a Top-5 row at 10 of 13; from round 9 on, **5 of 5** picks
were the 🎯 (the D54-1 rule: broken once in mock 56, three times in mock
54). The tool board finished **identical to Yahoo's recap** on the v34 page
(159 events, 0 drift, 0 page errors). Two new findings: the draft room shows
fewer positions than the pool for 29 of the 156 drafted men (§7), and the
survival chips beat the base rate here by the widest margin yet (§5).

## 1. Validation vs the Yahoo recap

| check | result |
|---|---|
| picks in the recap | 156; every "Last, First" line resolved to a pool name by the deck's own resolver (diacritics, suffixes and the dotted "P.J." included; zero unresolved, zero surname mismatches) |
| snake attribution | all 156 seats match the round parity; the owner's 13 picks sit at #10, #15, #34, #39, #58, #63, #82, #87, #106, #111, #130, #135, #154 |
| owner's roster | Tatum, Towns, Jalen Williams, Kyrie, Lillard, OG Anunoby, Poeltl, McDaniels, Hartenstein, Gillespie, PJ Washington, Vassell, Grimes — identical to the recap's "My Team" |
| poolless names | none — every pick in this room is a pool row |
| cast | seats 1–12: Darin, jordan, Kei, Nathan, Matan, Jeff, cnote, Kevin, Jake, **David (10)**, Alwin, Yoann |
| positions shown by the draft room vs the pool | **29 of 156 differ**, every one the pool listing MORE positions than the room (see §7) |
| state | `arena/data/states/draft_state_57.json`, md5 `de73d84f7f60ae858153f801f1319d59` |

## 2. The team, replayed

| readout | value | evidence |
|---|---|---|
| ECW (cats/week vs the average opponent) | **5.271**, rank 1 of 12 (next 5.052, Kei — seat 3) | `m57_final.json` |
| head-to-heads favored | 11 of 11 (per-opponent expected cats 4.70–5.94; thinnest vs Kei 4.70 and Kevin 4.76) | `m57_final.json` |
| season-shape H2H | wins 9 of 11 (cats won per opponent 3–8; the two losses are Kei 4 and Kevin 3) | `m57_final.json` |
| board rank (kept-total z-sum) | 1 (+13.52; next +6.30) | debrief |
| category ranks, weekly model | FG% 6 · **FT% 1** · **3PTM 3** · PTS 5 · **REB 3** · **AST 9** · **ST 3** · **BLK 8** · TO 4 | `m57_final.json` |
| championship rate, as drafted | **35.23%**, playoff 97.29%, rank 1 | `m57_arms.json` |
| follow-card arm (self-consistent) | **52.96%**, ECW 5.678; six swaps: #10 Haliburton, #34 Anthony Davis, #39 Derrick White, #58 Pritchard, #87 LaVine, #111 Cason Wallace | `m57_arms.json`, `m57_followcard_grade.json` |
| best single swaps | #10 Chet Holmgren 45.06%; #39 Derrick White 42.63%; #87 Miles Bridges 41.01%; #34 Anthony Davis 39.29%; #58 Payton Pritchard 37.56% | `m57_arms.json` |
| the two cheap card legs together | White at #39 and Bridges at #87: 47.21%, ECW 5.505 (+12.0 title points for two picks the card had at #1) | `m57_followcard_grade.json` |

The shape is the one the owner has been drafting toward: elite FT%, top-3
in threes, rebounds and steals, turnovers kept, with assists (9th) and
blocks (8th) conceded — the same categorical frame as mock 56's point-guard
build, this time with two centers (Poeltl, Hartenstein) instead of Mobley
and Turner, which is why rebounds are 3rd here and blocks are not.

## 3. Pick by pick — card vs owner vs hindsight

| pick | deck 🎯 (Top-5) | owner took | card rank · gap (blend) | hindsight best single swap (ΔECW vs final rosters) |
|---|---|---|---|---|
| #10 | Karl-Anthony Towns (Karl-Anthony Towns, Jalen Johnson, Tyrese Haliburton, Anthony Davis, Chet Holmgren) | Jayson Tatum | #16 · +0.049 | Chet Holmgren +0.172 |
| #15 | Karl-Anthony Towns (Karl-Anthony Towns, Jalen Johnson, Chet Holmgren, Jalen Williams, Anthony Davis) | Karl-Anthony Towns | #1 · +0.000 | Jalen Johnson +0.022 |
| #34 | Jalen Williams (Jalen Williams, Anthony Davis, Derrick White, Evan Mobley, Dyson Daniels) | Jalen Williams | #1 · +0.000 | Anthony Davis +0.064 |
| #39 | Derrick White (Derrick White, Desmond Bane, OG Anunoby, Franz Wagner, Kyrie Irving) | Kyrie Irving | #5 · +0.014 | Derrick White +0.149 |
| #58 | OG Anunoby (OG Anunoby, Payton Pritchard, Tyler Herro, Darius Garland, Jakob Poeltl) | Damian Lillard | #7 · +0.023 | Payton Pritchard +0.044 |
| #63 | OG Anunoby (OG Anunoby, Payton Pritchard, Jakob Poeltl, Ivica Zubac, De'Aaron Fox) | OG Anunoby | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #82 | Jakob Poeltl (Jakob Poeltl, Payton Pritchard, Miles Bridges, Jalen Suggs, Coby White) | Jakob Poeltl | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #87 | Miles Bridges (Miles Bridges, Jalen Suggs, Isaiah Hartenstein, Myles Turner, Zach LaVine) | Jaden McDaniels | #7 · +0.023 | Miles Bridges +0.093 |
| #106 | Isaiah Hartenstein (Isaiah Hartenstein, PJ Washington, Collin Gillespie, Devin Vassell, Quentin Grimes) | Isaiah Hartenstein | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #111 | Collin Gillespie (Collin Gillespie, Devin Vassell, PJ Washington, Cason Wallace, Fred VanVleet) | Collin Gillespie | #1 · +0.000 | Draymond Green +0.008 |
| #130 | PJ Washington (PJ Washington, Devin Vassell, Quentin Grimes, Herbert Jones, Malik Monk) | PJ Washington | #1 · +0.000 | none positive (the pick was hindsight-best) |
| #135 | Devin Vassell (Devin Vassell, Quentin Grimes, Herbert Jones, Malik Monk, Saddiq Bey) | Devin Vassell | #1 · +0.000 | Draymond Green +0.020 |
| #154 | Quentin Grimes (Quentin Grimes, Daniel Gafford, Malik Monk, Herbert Jones, Draymond Green) | Quentin Grimes | #1 · +0.000 | Draymond Green +0.013 |

Card 🎯 = what the v34 deck showed (blend50 #1; no urgent TARGET pin fired
at any turn — `tgOnPin` false at all 13). "Gap" is the blend distance from
the 🎯 to the man taken. Hindsight scores every legal single swap against
the FINAL rosters (pairwise when the alternative was drafted later), so a
positive number is an upper bound on what a different pick was worth
[EVIDENCE: `m57_replay.json`, `m57_deckcard_v33.json`, `m57_hindsight.json`].

- **#10 Tatum is the costliest turn of the room.** The card ranked him #16
  (blend 0.9475, the 0.78 availability tag on `inj-achilles-risk` doing the
  work) and 17 of 302 legal alternatives beat him in hindsight — Holmgren,
  who went #22, by +0.172 cats/week, worth +9.8 title points on his own.
  The card's 🎯, Towns, has no pairwise form because the owner took him
  himself at #15; the follow-card chain swaps #10 to Haliburton (0.78 tag,
  went #13) instead.
- **#39 Kyrie over Derrick White (card #1) cost +0.149**, the second-largest
  single gap, 7 alternatives better; White went #51 to Kei. **#87 McDaniels
  over Miles Bridges (card #1) cost +0.093**, 8 alternatives better; Bridges
  went #99 to Kei. Both were within 0.023 on the blend and both were the
  card's #1 by a margin the deck showed; both are the D54-1 lesson again —
  the round-4 and round-8 versions of it.
- **#58 Lillard over Anunoby (card #1)** cost +0.044 by hindsight (Pritchard
  the best alternative); the owner then took Anunoby at #63, where he was
  hindsight-best — so the pair of picks cost only the Pritchard gap.
- **Four turns were hindsight-best as taken:** #63 Anunoby, #82 Poeltl,
  #106 Hartenstein, #130 PJ Washington. The late-round rule held: #111,
  #135 and #154 were the 🎯 and trail only Draymond Green (went #155) by
  0.008–0.020.
- **#82 is D51R-2 vindicated live.** Poeltl and Pritchard tied on the blend
  to four decimals (0.9979); the deck broke the tie by ΔECW (Poeltl 0.941 vs
  0.917) and showed Poeltl 🎯, the owner took him, and Poeltl was
  hindsight-best while Pritchard graded −0.066. The Python replay port, which
  still breaks exact ties by name, lists Pritchard first (see Bounds).

## 4. Tool-state integrity — the deck's board vs the recap, on the v34 page

The owner's tool log was rebuilt as an event list (159 events: 154 direct
feeds, the shared token wherever the echo said "assumed over" or "only X
left"; the two raw UNKNOWN texts "Gianis" and "Giffey" with their `6-
Giannis Antetokounmpo` and `19- Josh Giddey` fixes; the duplicate "OG" feed
the deck skipped) and replayed through the real v34 page in headless
Chromium [EVIDENCE: `m57_tool_vs_truth.json`,
`arena/data/events/m57_tool_events.json`]:

| finding | detail |
|---|---|
| positions differing from the recap | **0 of 156**; owner's roster identical |
| echo lines asserted | 159 of 159 (each feed's resolved name, both UNKNOWNs, both fixes, the skip) |
| clock text under the feed title | correct after all 159 events |
| page errors | 0 |
| the D54 UNKNOWN mechanics, live | #19 "Giffey" was left open, #20 Trae Young was fed on top of it, the status strip kept naming #19 until `19- Josh Giddey` landed — no drift; #6 "Gianis" was fixed before the next feed |
| off-card echoes reproduced | #10 Tatum (card #16, 0.049 behind 🎯 Towns), #39 Kyrie (#5, 0.014 behind 🎯 Derrick White), #58 Lillard (#7, 0.023 behind 🎯 Anunoby), #87 McDaniels (#7, 0.023 behind 🎯 Miles Bridges) |

Second clean public room in a row (mock 54 drifted 13 positions; mocks 56
and 57 drifted none). The concise card and the YOUR PICK banner changed nothing in
the resolver or the state, and this replay is the first live-room evidence
that the v34 page logs a full room identically to v31/v32.

## 5. Survival chips — fourth out-of-sample room for the refit

Fourth room out of sample for the price-only refit (D51R-1R, 2026-09-22),
and the first in which it beats the constant base rate by a wide margin
[EVIDENCE: `m57_survival.json`, `scratchpad/m57/survival_refit_pool.json`]:

| room | rows | mean predicted | realized | Brier | constant-base-rate Brier |
|---|---|---|---|---|---|
| mock 57 (out of sample) | 51 | 0.518 | 0.608 | **0.178** | 0.238 |
| refit-era rooms pooled (53–57) | 255 | 0.539 | 0.698 | 0.196 | 0.211 |

- This room: BUY NOW 6 rows, 5 gone by the next turn; TOSS-UP 12 rows, 7
  gone; quiet 33 rows, 25 still there (76% vs 64% predicted). No survivor
  was called at 2% or less.
- The refit-era pool now beats its base rate by 0.015 over 255 rows (0.009
  after mock 56). The debrief's "every earlier scored room" pool (354 rows,
  Brier 0.324) mixes in mocks 51 and 52, whose deck cards carry the
  pre-refit model, and is not a reading of the refit.
- Read BUY NOW as it was read: about five in six here, two in three across
  the pool.

## 6. Does the tool account for positional loading? (owner's question)

Short answer: **yes in the marginal-value half of the score, no as a
penalty on the ranking, and loudly in the flags** — and on this roster the
model's answer is that the forward stack costs you almost nothing, which is
why the card kept sending forwards while the warnings fired. From the code
[EVIDENCE: `docs/draft-deck.html` engine and app blocks, rev `0dfbe77`]:

| layer | what it does with positions | evidence |
|---|---|---|
| Top-5 order (blend50) | 50% ΔECW percentile + 50% balanced-value percentile. No positional-balance term. Two reordering fixes for the position cap were measured on 2026-08-05 (E22/E22b) and both failed their registered bars, so the card keeps the validated order and NAMES the trap instead | engine `decwScores`; app block comment above the LINEUP CAP line |
| ΔECW (the marginal cats/week figure) | runs your roster plus the candidate through the weekly model, which sets a Yahoo lineup EVERY DAY (PG, SG, G, SF, PF, F, C, C, Util, Util) over 32 simulated weeks of 2–5 games per man and counts only started games; a man who cannot get into the lineup on his game days adds nothing that day | engine `teamWeekModel` calling `dailyFillWeights` (Instrument v2, 2026-08-05) |
| the structural TARGET read | premium-shelf scarcity first, then roster balance (a family below its floor once you hold 4+), can move the 🎯 only under the D51R-4 gate (no availability multiplier, within 0.05 cats/week of #1); it never fired in this room (no urgent pin at any of the 13 turns) | engine `archetypeRead`; `m57_deckcard_v33.json` `tgOnPin` false at every turn |
| ⚠ LEAN flag | fires from 5 players on when guard listings and forward listings differ by 4 or more, counting EVERY eligibility a man carries | app block `posCounts` |
| ⚠ LINEUP CAP flag | fires when 4 or more of the 5 card rows share a family whose start ceiling you already hold (C = 4 via C·C·Util·Util; G and F = 5) | app block, the E22 comment |
| ⚠ FEASIBILITY flag | open lineup slots vs picks left | app block `unfilledSlots` |

What the numbers said at pick 128 (the screenshot): "9F vs 5G" counts
Tatum, Jalen Williams, Anunoby and McDaniels twice each (SF and PF), Towns
once (PF), and Williams once more as a guard (the pool lists him SG as well —
§7); the LINEUP CAP line fired because four of the five card rows were
forward-eligible and you already held five forwards. The card still put PJ
Washington first by +0.007 cats/week over Vassell because the daily-fill
model finds the stack nearly free: on your final 13, every man starts
99–100% of his game days — Grimes, the thirteenth, 99.0% — and the same
holds for the 11-man roster at #128 with either Washington or Vassell added
[EVIDENCE: `fill_check.log`, the deck's own `dailyFillWeights` run on the
state]. The reason is arithmetic, not optimism: each man plays 3–4 of 7
days, so on a typical day about half the roster has a game and ten lineup
slots absorb six forwards through SF, PF, F and the two Utils. That
instrument was calibrated on the owner's league (99.4% of a 13-man
roster's played games start), so its indifference to a forward stack is a
measurement, not an oversight.

So the honest reading of the two lines together: the flags tell you the
roster SHAPE the ranking will not fix for you, and the ranking tells you the
shape is not costing categories. Where it would bite — six forwards who all
play the same night, or a real league week with two off-days — the model
under-counts it slightly, and the flag is the reminder to check the
schedule. What positional loading is NOT doing is hurting your category
profile: the categories this roster concedes (assists 9th of 12, blocks 8th)
come from the men chosen, not from the slots they fill, and the advisor read
in the screenshot ("Losing AST to most of the room … Don't punt them: you'd be
winning only 4 of the other 8, need 6") is the same weekly model saying so.

## 7. Two Yahoo position displays disagree — 29 of 156 drafted men

The pool's positions were set on 9/28 to Yahoo's official eligibility from
the 9-cat rankings page paste (D-M1; `yahoo-9cat-rankings-raw-2026-09-28.txt`
lists, for example, Anthony Edwards "PG,SF,SG" and Scottie Barnes
"C,PF,SF,SG"). The draft room's recap on 9/29 shows Edwards "PG,SG" and
Barnes "SF,PF,C". Across the 156 drafted men, 29 differ and in every case the
pool carries a superset of what the room showed: 11 extra SF listings, 11
SG, 5 PF, 2 PG [EVIDENCE: `scratchpad/m57/checks.json`; the recap as
pasted]. On the owner's roster: Jalen Williams (room SF,PF; pool adds SG),
McDaniels (room SF; pool adds PF), PJ Washington (room PF,C; pool adds SF).

Where it matters in the deck: `positionsOf` feeds the daily lineup fill, the
LEAN count, the family reads, the LINEUP CAP line and the Best-available
position filter. On this roster the start rates are unchanged with the
room's narrower set for those three men (all 1.000; `fill_check2.log`), and
the LEAN flag would still have fired (8F vs 4G). It is a data-quality item,
not a ranking defect: the draft room is the display the league software
applies, and the pool should carry it. Decision D57-1 below.

## 8. Repeat names on the card — the audit, re-run on this room

Same instrument as mock 56 (`repeat_names_audit.mjs`, six other rooms'
owner rosters substituted in at each turn, an empty roster, value-only and
ΔECW-only orders) [EVIDENCE: `m57_repeat_names_audit.json`]:

| readout | mock 57 | mock 56 |
|---|---|---|
| owner turns where the #1 changes under at least one other room's roster | **10 of 13** | 9 of 13 |
| owner turns where the #1 changes under an empty roster | **11 of 13** | 11 of 13 |
| the mock-56 repeat names (Brook Lopez, Cameron Johnson, Braun, Eason) on this room's Top-5 | at no turn | on the Top-5 at 7, 3, 5 and 4 turns |

The late-round #1 is a function of THIS roster: from #106 on the empty-roster
#1 is Daniel Gafford at every turn while the card said Hartenstein,
Gillespie, PJ Washington, Vassell and Grimes — five different names, each
the best marginal add to the roster as it stood. The names the owner
flagged after mock 56 left the card once their lines were re-derived
(D-M4), as `after-report-2026-09-29-final-check.md` predicted; PJ Washington
and Grimes were on that report's follow-the-card list for this seat, and
here they were the 🎯 at #130 and #154.

## 9. What this run answers and asks

- **Answers:** the v34 page (concise card, YOUR PICK banner) logged a full
  public room identically to the recap — the layout change touched nothing
  the resolver or the state use, and the D54 UNKNOWN mechanics worked live
  twice; the seat-10 process held from round 9 on (5 of 5 on the 🎯); the
  four off-card picks are where the title odds went (35.2% as drafted vs
  53.0% following the card), and three of the four were guards or a wing
  taken over the card's forward or guard by 0.014–0.049 on the blend; the
  roster-balance flags are display-only by measurement and the model finds
  the forward stack free on this roster (§6); D-R3 (a fresh seat-10 mock on
  the re-derived lines) is closed by this room.
- **Asks:** the 29 position discrepancies between Yahoo's two displays
  (D57-1); Tatum at #10 on the Achilles tag (D57-2); whether the
  point-guard preference is a standing override the card should not be
  asked to price (D57-3); the survival chips' re-fit trigger (D57-4).

## Watchlist

- Tatum (#10, `inj-achilles-risk`, 0.78): the card's #16 and the room's
  costliest turn by hindsight; no return date reported — the tag, not the
  line, decides his rank.
- Kyrie (#39, 0.78) and Lillard (#58): the owner's guard overrides; the
  card's #1s at those turns (White, Anunoby) graded +0.149 and +0.044 by
  hindsight.
- Positions: 29 of 156 drafted men carry extra eligibility in the pool vs
  the draft room; re-check against the room display at the next Yahoo
  paste (D57-1).
- Survival chips: refit beat the base rate here by 0.060; pooled margin
  0.015 over 255 rows — the re-fit trigger stays "a room that misses by more
  than 0.03".
- Yahoo market paste: seven days old; early-October paste before 10/14.
- Duren: qualifying-offer deadline Thursday 10/1 (standing).

## Open-item receipts

| item | query run (2026-09-29) | dated finding |
|---|---|---|
| (this analysis) | machine replay only — no web research in this report | pull receipts for the window live in `after-report-2026-09-29.md` §8 |

## Bounds

- Random public room: the field's weakness is in every denominator; the
  championship rate is not a league forecast. None of the eleven seat names
  is a modeled league-mate.
- Hindsight is single-swap on current lines: an upper bound on a pick's
  cost, not a strategy.
- The championship and ECW figures use the same projection lines the card
  ranks by; they cannot certify those lines. This report carries no
  line-independent evidence.
- The Python replay port breaks exact blend ties by name while the deck
  breaks them by ΔECW: at #82 the port lists Pritchard first and the deck
  showed Poeltl 🎯 (the tool log carries no off-card note there, so the
  deck's order is the one the owner saw); the table in §3 follows the deck.
- The follow-card chain at #10 swaps to Haliburton rather than the card's
  Towns because Towns was the owner's own next pick (no pairwise form); its
  52.96% therefore rests partly on a 0.78-availability man at #10.
- Which of Yahoo's two position displays the league software applies to
  lineups this season is not verified from a Yahoo page (sports.yahoo.com
  is blocked from this session); §7 rests on the two pastes the owner
  supplied, dated 9/28 and 9/29.
- The typed texts behind the "assumed over" / "only X left" echoes are
  reconstructed as the shared token; the replay's 159 of 159 echo matches
  show each resolves to the same man, but the literal keystrokes are not
  recorded.
- Grimes at #154 is the one roster spot the daily-fill model does not start
  every game day (99.0%); every other start rate in §6 is 1.000 to three
  decimals.

## Decision sheet (owner disposes)

| id | question | default if silent |
|---|---|---|
| D57-1 | Positions: the draft room (9/29 recap) shows fewer positions than the pool for 29 of 156 drafted men, the pool having copied Yahoo's 9/28 rankings-page paste. Sync those rows (and check all 334 at the next paste taken from the draft room, not the rankings page)? | sync the 29 at the next pull under the D-M1 rule (the platform's own listing, no second outlet); note the source display in the pull-log |
| D57-2 | Tatum at #10 on the Achilles tag: the card had him #16 and hindsight ranks the pick 18th of 302; keep the 0.78 availability tier for a player with no announced return date, or set availability to 0 until a return date is reported? | keep 0.78 — the card already priced it (#16); the pick was the owner's override |
| D57-3 | The guard overrides (#39 Kyrie over White, #58 Lillard over Anunoby): 0.149 + 0.044 cats/week by hindsight, 7.4 and 2.3 title points singly. Treat "strong PGs" as a standing preference the card is not asked to price, or add a guard-family lens to the card? | preference stands; no card change — the card shows the gap under the feed and that is the mechanism |
| D57-4 | Survival chips: this room beat the base rate by 0.060 and the refit-era pool by 0.015 over 255 rows; keep them on with the same re-fit trigger? | keep on; re-fit only if a room misses by more than 0.03 |

## Provenance

- Inputs: the owner's tool log and Yahoo recap (this session, 2026-09-29),
  transcribed verbatim into `arena/data/events/m57_tool_events.json` and the
  recap into the state by the deck's resolver.
- Every number is read from `arena/results/m57_*.json` and the debrief; the
  arms use 18,000 CRN seasons (seeds 11/23/47); the audit and the start-rate
  checks ran the deck's own engine under node against `docs/draft-deck.html`
  (main, v34 — engine identical to v33).
- Not verified: nothing here rests on web research.
