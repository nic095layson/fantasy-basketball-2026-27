# After-Report — draft_state_50 Live Mock: Validation + Roster Analysis

**Artifact:** `arena/data/states/draft_state_50.json` (deck plane).
**Room:** 12 teams × 13 rounds, snake; owner at **slot 5**; human cast named
for all 11 opponent seats. **Declared build: punt FT% + 3PTM + PTS.**
**Method:** the state was validated mechanically against the live pool, then
replayed through the deck engine (`hoops.py` z-scores, availability
multipliers, punt-aware `adj_value`); every number below is computed from
that replay, none is eyeballed.

## 1. System operations integrity — ALL GREEN, zero interventions

| check | result |
|---|---|
| picks recorded | **156/156** — a complete draft |
| name resolution | **156/156 resolve exactly** against the 255-row pool — zero unresolved, zero fuzzy repairs needed |
| duplicates | none |
| snake-order integrity | **0 violations** across all 13 rounds |
| excluded players drafted | **none** — no `out-*`/`*-recovery` row was draftable or drafted |
| risk-tagged players drafted | 24, all legitimately draftable at availability 0.78 |
| deep-pool coverage | Kon Knueppel, Cameron Boozer, AJ Dybantsa, Darryn Peterson, Yaxel Lendeborg, Collin Gillespie, Ajay Mitchell, Jusuf Nurkic — all resolved as pool rows |

This is the **first uploaded draft state in the series to arrive fully clean**:
draft_state_46 surfaced nine missing pool names, draft_state_48 was the
critical name-resolution failure, draft_state_49 needed state repair. The
resolver hardening (PR #21), pool-completeness passes, and the malformed-row
gate have now carried a 156-pick live human room end to end with **zero
defects**. That is the system-ops verdict.

One timing note, stated for the record: this room drafted against the deck as
built before today's amendments. **Jamal Murray went at pick 26, pre-tag** —
on the current board he carries `inj-achilles-risk` (0.78) and prices ~a round
later. Not a defect (the tag postdates the draft); noted so the pick-26 cost
is read against the board that existed at draft time.

## 2. The build executed — completely

Availability-weighted category ranks (1 = best of 12):

| | FG% | FT% | 3PTM | PTS | REB | AST | ST | BLK | TO |
|---|---|---|---|---|---|---|---|---|---|
| **Owner (slot 5)** | **1** | 12 | 12 | 10 | **2** | 5 | **3** | **2** | 6 |

Dead last in both fully punted counting cats, 10th in the third — and
**first in FG%, second in REB and BLK, third in ST** with above-median AST
and TO. A three-cat punt only works if the six live cats are genuinely
elite, and this one is: owner leads the league median in **all six**
(FG% .51 vs .48, REB 82.4 vs 78.5, AST 52.1 vs 51.2, ST 14.7 vs 13.8, BLK
12.0 vs 8.9, TO 25.8 vs 26.2 fewer-is-better).

## 3. Head-to-head projection, all 11 opponents

| opponent | all-9 | live-6 |
|---|---|---|
| Cayas (11) | **7–2** | 6–0 |
| JCo (9) | **6–3** | 6–0 |
| Hegi (2) · Noah (4) · John (6) · Martin (7) · Robby (8) | **5–4** | 5–1 |
| Kevin (10) | **5–4** | 4–2 |
| Oblena (1) · Kyle (3) · Will (12) | 4–5 | 4–2 |

Projected winning weeks against **8 of 11** opponents, and the three losses
are not structural — the live-cat margins say they're coin flips or one-move
fixes:

- **vs Oblena:** the two live losses are BLK **−0.5%** and TO **−2.6%**.
  One shot-blocker swing flips the week.
- **vs Kyle:** ST −7.0% and TO −1.3% — Kyle is the league's #1 steals team;
  everything else is a win, REB by +19%.
- **vs Will:** REB −3.0% and AST −6.3% against the league's #1 REB team;
  FG%/ST/BLK/TO are all owner wins.

**The team's one soft live cat is TO (6th)** — and it's the swing cat in two
of the three losing matchups. That's the in-season streaming lever.

## 4. Punt-fit audit — where the draft fought its own build

Engine `adj_value` under punt(FT%, 3PTM, PTS), rank among the full pool:

| pick | player | punt-board rank |
|---|---|---|
| 20 | Giannis | **4** |
| 29 | Chet Holmgren | **11** |
| 92 | Jalen Duren | **14** |
| 116 | Rudy Gobert | **15** |
| 125 | Ausar Thompson | **21** |
| 77 | Zion | 37 |
| 101 | Cason Wallace | 45 |
| 68 | Myles Turner | 48 |
| 149 | Alex Caruso | 66 |
| 53 | Reed Sheppard | 89 |
| **5** | **Jayson Tatum** | **92** |
| 140 | Ayo Dosunmu | 123 |
| **44** | **Trae Young** | **219** |

Rounds 2–10 are a punt-drafting clinic — five picks from the punt board's
top 21. The two outliers:

- **Tatum at pick 5 (punt rank 92).** His value concentration is exactly
  the three punted cats. If the punt was chosen *after* pick 1, this is the
  ordinary cost of committing mid-draft and Tatum still contributes ST/REB;
  if the punt was pre-declared, slot 5 had Jokić-class fits available. Worth
  knowing which it was, because it changes nothing now but everything for
  the October room.
- **Trae Young at pick 44 (punt rank 219).** He is why AST sits 5th rather
  than 9th — but he actively fights all three punted cats and drags FG%/TO.
  The engine's read: the AST insurance cost ~a full round of punt value.
  **Daniel Gafford (never drafted, in the pool) was on the board at every
  one of the owner's last five turns** and is a top-4 punt-board leftover;
  a Gafford-class big over Dosunmu (punt rank 123) at pick 140 was the
  cleanest available upgrade the build left behind.

## 5. Verification

Computed, not estimated: name resolution, snake order, duplicates, and
availability checks are mechanical; category totals are
availability-weighted per-game sums with attempt-weighted percentages;
head-to-heads compare those totals per category. **Bounds:** per-game rates
carry no weekly schedule grain (games-played volume differences between
weeks are not modeled), and availability multipliers are season-level, so
these are season-shape projections, not week simulations. The punt-board
ranks come from the deck's own `adj_value` — the same engine the owner
drafts with, which is the point of the audit.

## 6. Owner decisions

| # | decision |
|---|---|
| **D50-1** | Was the FT%/3PTM/PTS punt declared before pick 1 or adopted mid-draft? (Reads on Tatum-at-5 and shapes October seat strategy) |
| **D50-2** | TO is the swing cat in two of three losing matchups — want a low-TO streaming shortlist built from the pool for in-season use? |
