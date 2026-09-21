# After-Report — draft_51: first live-human mock from the REAL slot 10

**Owner request (2026-09-21, verbatim):** "I am now beginning to practice mock
drafts with other live humans with my 10 seat… please analyze. Additionally, I
broke the tool — I input player names that were not in the data base, and it
stuck on 'YOUR PICK'." Two inputs: the deck tool's pick-by-pick feed (with
errors), then Yahoo's direct draft recap — the authoritative record.

**Room:** public Yahoo mock, 12 × 13, owner seat 10 (matches the real league
slot; opponents are random humans, NOT the league cast — practice rep, not
opponent intel). **Method:** the recap was reconciled against the tool feed
pick-by-pick; the 12 rosters were replayed against the CURRENT post-integration
kit lines (`rank_engine` z-scores, `avail(gp)` weighting, attempt-weighted
percentages — the draft_50 method on the kit plane, because the deck plane
still carries pre-2026-09-16 lines for several names). Verification: this file
passes `report/check_report.py`; every figure below is computed, none eyeballed.

Pull window: 2026-09-15 → 2026-09-15 (analysis run 2026-09-21; not a roster
pull — market/roster state unchanged since the 9/16 integration).

**Headline.** The slot-10 pair plan executed on first contact: picks 10/15/34/39
landed our board's **#8, #6, #7, #9** (Edwards, Towns, Davis, Daniels) — four
of the top nine, with Davis at 34 and Daniels at 39 costing nothing. The replay
projects **winning weeks against 9 of 11 opponents** (draft_50 from slot 5:
8 of 11) on a clean punt-AST shape: STL 1st, TOV 2nd, 3PM 3rd, AST 12th. The
tool failures all trace to ONE root cause — two live-drafted players (Tre
Jones, Julian Champagnie) are absent from the deck's 255-row pool — which
produced a silently WRONG logged pick (#134), a blocked pick (#152), and the
owner's stuck "YOUR PICK" (#154). And one correction of this system's own
record: the deck has carried Butler's `acl-recovery-jan26` tag all along — the
9/16 claim that the deck owed him a tag was wrong; the kit was the stale plane.

---

## 1. Validation vs the Yahoo recap

156/156 picks accounted for. The tool's logged state differs from reality in
exactly three places, all sharing one root cause:

| pick | tool logged | reality (recap) | mechanism |
|---|---|---|---|
| #134 | Herbert Jones, seat 11 | **Tre Jones**, andrew | input "Jones" silently resolved to an in-pool surname-mate because Tre Jones has no pool row |
| #152 | UNKNOWN gap | **Herbert Jones**, Akis | the real Herbert pick was refused — "already off the board" — because #134 had wrongly consumed him |
| #154 | UNKNOWN, unfixable | **Julian Champagnie**, OWNER | no pool row; the owner's own pick could not log — the stuck "YOUR PICK" |

Everything else reconciles exactly, including the two mid-draft insertions
(Garland at #55, Harper at #94 — both recomputed correctly against the recap)
and both disambiguation HALTs (Murray, Mitchell), which worked as designed.

## 2. Tool defect report

- **T1 (root cause, data): pool coverage.** Tre Jones (CHI — Yahoo XRank 173,
  drafted #134 by a live room) and Julian Champagnie (SAS — kit row added
  2026-09-16, deck never synced) are absent from the deck pool. Real rooms
  draft deeper than ADP: the no-ADP Yahoo tail needs a pool-candidate review.
- **T2 (design): opponent picks must never require pool membership.** The
  resolver's failure mode was not the refusal — it was the silent wrong
  "assumed over" substitution at #134. An opponent's pick should log verbatim
  with a not-in-pool marker; only OWNER-side recommendations need pool data.
  (Contrast: "Markenan" → UNKNOWN and "Champagnie" → no-match behaved
  honestly; the dangerous case is a bare surname with in-pool holders.)
- **T3 (cosmetic):** "#140: Jimmy Butler → Seat 5 (Jimmy Butler skipped:
  injury-excluded)" — the tool correctly LOGGED a live human drafting an
  excluded player, with a self-contradicting annotation. Message wording fix.
- **T4 (observation): the punt advisor retargeted four times** (AST+FT% →
  FT%+TO → TO+FG% → TO+AST). Its final call was half right: the replay shows
  AST genuinely punted (12th) but TO as the roster's SECOND-BEST category —
  "punt TO" was noise. Advisor stability is worth a look in the sync pass.
- **Correction to this system's record:** the deck pool carries
  `Jimmy Butler … acl-recovery-jan26 (return ~2027)` (verified by grep,
  2026-09-21). The 9/16 integration report's watchlist claim that the next
  deck session "owes Butler his recovery tag" was WRONG — the deck knew; the
  kit was stale until 9/16. What remains real is the severity mismatch: deck
  availability 0.0 vs kit GP 20 (board #68) — decision D-I1, now concrete.

## 3. The team, replayed on current kit lines

Category ranks (1 = best of 12), availability-weighted:

| FG% | FT% | 3PM | PTS | REB | AST | ST | BLK | TO |
|---|---|---|---|---|---|---|---|---|
| 4 | 5 | **3** | 7 | 5 | 12 | **1** | 4 | **2** |

Head-to-head, all nine categories: **9 wins of 11** (6-3, 7-2, 7-2, 5-4, 5-4,
7-2, 7-2, 7-2, 6-3), losses 4-5 to Bonani (Jokić room) and dnd (Cade + Embiid
+ Garland) — both assist-rich builds beating the punt where it lives. The
shape is a **natural punt-AST**: eight categories at median or better, six in
the top five, with the two engine signatures (STL first, TO second) exactly
where the market analysis said our drafting edge lives.

## 4. Value audit — pick vs current board rank

| pick | player | our # | read |
|---|---|---|---|
| 10 | Anthony Edwards | 8 | plan |
| 15 | Karl-Anthony Towns | 6 | plan |
| 34 | Anthony Davis | 7 | +27 vs board; ADP 24.9 lasted |
| 39 | Dyson Daniels | 9 | the market-analysis gift, secured |
| 58 | OG Anunoby | 44 | value |
| 63 | Damian Lillard | 93 | reach −30 (AST insurance for the punt build it then didn't need) |
| 82 | Reed Sheppard | 107 | reach −25 on CURRENT line — the deck tool still showed his pre-downgrade rank |
| 87 | Kristaps Porziņģis | 52 | +35, round-8 steal |
| 106 | Cam Johnson | 61 | +45 |
| 111 | Jakob Poeltl | 128 | slight reach, C depth |
| 130 | Tari Eason | 65 | +65, the stocks engine |
| 135 | Christian Braun | 83 | +52 |
| 154 | Julian Champagnie | 173 | fine for R13 |

Ten of thirteen picks at or above board value. The two true reaches (Lillard,
Sheppard) share a diagnosis: both were AST/guard insurance priced off stale
deck lines — Sheppard's bench downgrade and the punt-AST shape both live only
on the kit plane right now. INFERENCE: with synced lines the tool would have
steered those two picks toward Porziņģis-class bigs or wings earlier.

## 5. What this run answers and asks

**D50-1 context:** no punt was pre-declared here; the advisor adapted
mid-draft and the roster settled into punt-AST organically from value picks —
evidence the slot-10 seat drafts best value-first, letting the punt emerge.
**Draft_state_51 storage is deliberately deferred:** committing it now with
two pool-unresolvable names would break the deck's parity harness (which
auto-ingests committed states); it stores cleanly the moment the pool adds
land. The full pick list is preserved in this report and in Yahoo's recap.

## Watchlist

Deck-sync items now urgent (more live mocks coming): pool adds, line
reconciliation, resolver fix — §Decision sheet. Standing items unchanged
(preseason data drop, camp roles, Wagler/WAS-center/Daniels-minutes watches).

## Open-item receipts

| check | receipt |
|---|---|
| Recap-vs-feed reconciliation | 156/156 mapped; 3 corrections (#134, #152, #154), all one root cause |
| Replay coverage | 155/156 names resolved against kit 240-pool; only Tre Jones unmatched (opponent-side; andrew projects 2-7 regardless) |
| Category/H2H figures | computed 2026-09-21, availability-weighted per the draft_50 method, kit plane |
| Butler deck-tag verification | `data/players.csv` on deck main grepped 2026-09-21: `acl-recovery-jan26` present |
| Publication gate | `report/check_report.py` PASS on this file |

## Bounds

**Out of scope by design:** opponent-intel conclusions (random public room,
not the league cast); any repo edit beyond this report (the deck sync is a
proposed work order, not done); deck-plane replay (its lines are pre-9/16 for
five names — the kit replay is the honest current read).

**In scope and unverified:** Tre Jones's stat line is absent from both planes,
so andrew's totals omit one deep pick (bounded: he projects 2-7 with margin);
per-game rates carry no weekly schedule grain (season-shape projection, not
week simulation — same bound as draft_50).

## Decision sheet (owner disposes)

- **D51-1 — the deck-sync work order** (recommended before your next live
  mock): pool adds (Champagnie, Tre Jones, and a review of the no-ADP Yahoo
  tail for other room-draftable names), kit-to-deck line reconciliation
  (Sheppard, Vučević, Keyonte George, Randle — plus the six 9/16 kit adds),
  resolver change (opponent picks log verbatim when not in pool — T2), the
  T3 annotation fix, then rebuild, parity, artifact republish, and canonical
  storage of draft_state_51.
- **D-I1, now concrete:** Butler — deck 0.0 ("return ~2027") vs kit GP 20
  (board #68). Pick a severity; the sync pass applies it to both planes.
- **D51-2 —** want the punt-AST variant of the slot-10 pick slate built
  alongside the balanced one once preseason data lands? This mock suggests
  the seat drifts there naturally.

## Provenance

Produced 2026-09-21 by the operating session
(`https://claude.ai/code/session_01QjgeRdpDaWgSJmGKRG8fTU`) on branch
`claude/draft-51-mock-analysis`. Inputs: the owner's tool feed and Yahoo recap
(2026-09-21, verbatim in chat); kit board at the 9/16 integration state; deck
pool at main (Butler grep). Replay script inline in session; method identical
to `after-report-2026-09-08-draft50.md` on the kit plane.
