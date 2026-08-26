# After-report — draft_state_49: first full live-human mock (12 humans, pick-by-pick)

**Owner request (verbatim):** "Completed a full mock draft, pick by pick, with
other live humans. I have the JSON and the yahoo draft recap for you. Analyze
(names not recognized, Tim Hardaway Jr.), validate with Yahoo draft results,
and provide after-report of system operations integrity, post-draft analysis
of my roster vs. opponents."

**Analyzed:** `draft_state_49.json` (uploaded 2026-08-25; 12 teams, slot 8 =
David, size 13, declared punt AST, 156 picks) against the owner-pasted Yahoo
round-by-round recap (156 picks, 12 named seats). Engine:
`yahoo-fantasy-basketball` @ `4b8d375` (pool `eed45b60`, 254 rows, pull
2026-08-25). Draft-night engine behavior reconstructed from `427d19a` (the
commit live before tonight's #18 feed-grammar fix).

**Method:** Yahoo recap transcribed to a machine-readable table (mojibake
restored: Jokić, Dončić, Şengün, Porziņģis, Nurkić, Diabaté, Dëmin); each
recap name canonicalized through the engine's own `match_candidates`; all 156
picks diffed name-by-name and seat-by-seat against the state file; failure
inputs probed on both draft-night (`427d19a`) and current resolvers;
roster analysis computed independently and cross-checked against the engine's
own `resync → status → matrix` path (exact agreement). Scripts and raw output
committed beside this report (`mock-draft-2026-08-25-49-validation.csv`,
`validate_49.py`, `validate_49_out.txt`).

**Headline:** The system held up in its first real 12-human room. 151 of 156
picks verified correct against Yahoo, **zero wrong-player matches**, and both
failures were loud, recoverable UNKNOWNs: pick 81 (Day'Ron Sharpe — an
apostrophe-normalization gap; he IS in the pool) and pick 148 (Tim Hardaway
Jr. — the pool's only missing drafted player, 155/156 = 99.4% coverage).
Separately, picks 58–60 were entered in rotated order, so the state file has
three players on the wrong teams (entry-order error, not an engine failure).
On the board: **David's roster ranks #1 of 12** on the engine's z-metric in
both the 9-cat and punt-AST views, and is the H2H favorite against all 11
opponents.

---

## 1. System operations integrity

### F1 — Pick 81 UNKNOWN: Day'Ron Sharpe (seat 9, Yizan)

- **EVIDENCE** (`data/players.csv`, 2026-08-25): `Day'Ron Sharpe,BKN,C,…` —
  in the pool, no injury note, availability 1.0. The "~6 mo" injury from the
  8/25 pull is **Shaedon** Sharpe (`knee-recovery`, availability 0).
- **EVIDENCE** (resolver probe, both `427d19a` and current): `Day'Ron Sharpe`,
  `Day'Ron`, and `D Sharpe` all resolve; **every apostrophe-less spelling
  fails** — `Dayron Sharpe`, `DayRon Sharpe`, `Day-Ron Sharpe`, `Day Ron
  Sharpe` → NO MATCH → UNKNOWN. `fold()` strips accents but not apostrophes,
  so the folded pool name `day'ron sharpe` can never equal `dayron sharpe`.
- **EVIDENCE**: `Sharpe, Day'Ron` (Yahoo paste form) failed on the
  draft-night engine and resolves on the current one (tonight's #18
  Last-First fix).
- **INFERENCE** (raw inputs are not stored in the export): the typed input
  was an apostrophe-less or Last-First spelling. Cannot be confirmed —
  see Bounds.
- **Behavior grade:** correct-but-unforgiving. The failure was loud
  (`⚠ logged as UNKNOWN … fix with: draft fix 81 "Name"`) and did not
  cascade (pick 82 logged clean). It was never corrected mid-draft, so
  Day'Ron stayed "available" on the board for the final 75 picks. Whether
  any turn card actually recommended him: did not check (per-turn
  recommendations are not reconstructable from the export).

### F2 — Pick 148 UNKNOWN: Tim Hardaway Jr. (seat 4, Andy)

- **EVIDENCE**: `grep -i hardaway data/players.csv` → no row. Not a resolver
  failure — no spelling could have matched. This is the pool's **only**
  missing player among 156 real-room picks (99.4% coverage; the other 155
  all resolve).

### F3 — Picks 58–60 rotated in the state (not an engine failure)

| pick | Yahoo truth | state has | state's team | truth's team |
|---|---|---|---|---|
| 58 | Franz Wagner → John (seat 10) | Desmond Bane | John | Jay C. |
| 59 | Desmond Bane → Jay C. (seat 11) | Nickeil Alexander-Walker | Jay C. | Peter |
| 60 | Nickeil Alexander-Walker → Peter (seat 12) | Franz Wagner | Peter | John |

- **EVIDENCE**: validation CSV rows 58–60. The three names were entered one
  position out of order; the engine attributed each to the seat on the clock,
  as designed. Consequence: in the state file John, Jay C., and Peter each
  carry one wrong player. The roster analysis below uses the Yahoo truth.

### F4 — Bare `Sharpe` assumes the injury-excluded namesake

- **EVIDENCE** (CLI, current engine): `draft turn "Sharpe"` → `✓ Shaedon
  Sharpe (assumed over Day'Ron Sharpe)`. The namesake tiebreak uses raw
  value, not availability-adjusted value, so it defaults to a player who is
  availability-0 (out ~6 months) and whom no live room is drafting. Loud, but
  the wrong default.

### F5 — Yahoo's `Jimmy Butler III` suffix form does not resolve

- **EVIDENCE**: pool row is `Jimmy Butler`; query `Jimmy Butler III` → NO
  MATCH on both engine versions (a query longer than the pool name defeats
  the substring stage). No live impact — pick 136 logged correctly because a
  shorter form was typed — but a verbatim Yahoo paste would have failed.

### What held (the positive evidence)

- **154/156 Yahoo-form full names resolve 1:1** through the current resolver,
  including restored accents, apostrophes (Kel'el Ware, De'Aaron Fox),
  hyphens, and suffixes (validation section A).
- **Zero wrong-player matches in 156 picks** — the failure classes from
  draft_state_46/47/48 (surname collisions, missing pool players, feed
  grammar) all held: 3 Georges, 3 Murrays, 3 Mitchells, 3 Thompsons,
  2 Bridges, 2 Williams, 2 Porters drafted; every one attributed correctly.
- **Throughput** (measured 2026-08-25): full 156-name `resync` in 174 ms,
  `status` in 51 ms — far inside a live pick clock.
- **Cross-check**: the engine's own `resync → matrix` output reproduces this
  report's independent z-analysis exactly (T8 row `+5.3 +0.6 +1.0 +2.6 +2.3
  −3.4 +9.6 +4.4 +3.4`, ranks identical).

## 2. Post-draft: David's roster vs the field

Rosters built from the **Yahoo truth** (state's three rotated players
corrected; THJ absent from Andy's totals — a round-13 pick, negligible).
Values are projection z-scores over the 254-player pool (engine standard).

**David (slot 8):** KAT, Anthony Davis, Kyrie Irving, Jalen Williams, Jaren
Jackson Jr., Dyson Daniels, Payton Pritchard, Reed Sheppard, Jakob Poeltl,
Cameron Johnson, Brook Lopez, Christian Braun, Tari Eason.

### Standings (engine z-metric)

| rank | 9-cat composite | punt-AST composite (8 cats) |
|---|---|---|
| 1 | **David +25.8** | **David +29.2** |
| 2 | Peter +1.5 | Andy +5.5 |
| 3 | Brandon +1.4 | Peter +3.1 |
| 4 | Andy +1.2 | Team 3 −1.6 |
| … | … | … |
| 12 | seat 6 (??) −28.4 | seat 6 (??) −23.9 |

Honest framing: z-sum magnitude is a draft-quality score, not a win
probability — the H2H view is flatter and is the better predictor of weekly
matchups.

### Category profile (rank of 12)

ST **1st** (+9.6) · BLK **1st** (+4.4) · FG% **2nd** (+5.3) · 3PTM 3rd ·
PTS 3rd · REB 3rd · TO 3rd (+3.4, low-turnover build) · FT% **7th** (+0.6,
weakest kept cat) · AST 9th (declared punt — working as declared).

### H2H: categories David leads (of 9 / of 8 ex-AST)

Favorite vs **all 11**: 9/9 vs seat 6; 8/9 vs Jay C.; 7/9 vs Ethan, Team 3,
Andy, Scott, Chase, Yizan; 6/9 vs Brandon, Peter; **5/9 vs John — the
closest rival** (John takes FT%, AST, and contests 3PTM/PTS).

### Build coherence (vs the declared punt AST)

Coherent. The roster concentrates FG%/ST/BLK/TO — the classic punt-AST
frame — and AST landed 9th without a single pick spent chasing it. One
note: Kyrie (R3) carries meaningful AST value a punt-AST build doesn't
cash; his PTS/FT%/3PTM/TO still justify the slot on this board, and FT%
7/12 would be materially worse without him. Fine pick; the punt just
doesn't get full credit for it.

### Pick-by-pick vs the engine board (composite value order)

R1 KAT (board #6) fair · R2 AD (#5) fair · R3 Kyrie (#16) value ·
R4 J-Dub (#17) value · R5 JJJ (#22) value · R6 Dyson (#10) **value, +55** ·
R7 Pritchard (#37) value · R8 Sheppard (#55) value · R9 Poeltl (#49) value ·
R10 CamJ (#48) value · R11 Brook (#59) value · R12 Braun (#54) value ·
R13 Eason (#44) **value, +108**.

Caveat: late-round "value" margins partly measure the room drafting by
market/name while the engine ranks by 9-cat production — expected divergence
per the deck's own colophon. The signal that matters: **no reaches, zero
picks graded below fair**, and the R6 Dyson Daniels / R13 Tari Eason steals
are large even after discounting.

## 3. Bounds

**Out of scope by design:** converting z-standings to season win
probabilities; opponent tendency profiling from one draft; keeper/schedule
effects; September ADP recalibration (feature-frozen until then).

**In scope, unverified:**
- The raw text typed at picks 81 and 148 — **UNVERIFIABLE**: the export
  schema carries only `{player, slot}`; the deck's per-pick input memory
  lives in the drafting browser's localStorage and was not exported.
- Which deck version was live during the draft (pre- or post-#18) —
  **UNVERIFIABLE** from the state file; the export carries no build stamp.
  The probe covered both engines, so every conclusion above holds either way.
- Whether any live turn card recommended the phantom-available Day'Ron
  Sharpe after pick 81 — **NOT-ATTEMPTED**: reconstructable only by
  replaying all 75 subsequent turns; bounded impact either way (one
  late-round C on one opponent's roster).

## 4. Decision sheet (owner disposes; nothing below has been executed)

| tier | action | would be demoted if… |
|---|---|---|
| MUST ADD | **Tim Hardaway Jr. → pool** (MIA, SG/SF). A real room spent pick 148 on him; pool-completeness law says drafted players must exist. | he goes unsigned/unrostered before your real draft |
| HIGHLY RECOMMEND | **Apostrophe/hyphen-insensitive matching** (fold strips `'`/`-` from query AND pool names; both engines + parity fixtures). Kills the entire `Dayron Sharpe` failure class (also protects Kel'el, De'Aaron, D'Angelo-type names). | evidence the owner always types apostrophes correctly under the clock (draft_state_49 suggests otherwise) |
| HIGHLY RECOMMEND | **Namesake assumption prefers availability > 0** — bare `Sharpe` should assume Day'Ron (draftable), not Shaedon (out ~6 mo). | Shaedon returns to draftability |
| NICE TO HAVE | Suffix-tolerant fallback: on no-match, retry with trailing `Jr./III/II` stripped from the query (`Jimmy Butler III` → Jimmy Butler). | — |
| NICE TO HAVE | Deck nudge when an UNKNOWN persists ≥ 12 picks ("pick 81 still UNKNOWN — fix with 81- Name"), so phantom-availability windows stay short. | — |
| HOUSEKEEPING | If draft_state_49 feeds any later analysis, repair it first: `fix 58 "Franz Wagner"`, `fix 59 "Desmond Bane"`, `fix 60 "Nickeil Alexander-Walker"`, `fix 81 "Day'Ron Sharpe"` (148 needs THJ in the pool first). | — |

## 4a. Execution addendum (2026-08-25, post-approval)

The owner approved all four decision-sheet items ("1. Yes / 2. Can you have
it so typing in 'Dayron' will read? / 3. Yes / 4. Yes"). Executed, with
evidence, in `yahoo-fantasy-basketball` PR #21 (`claude/dayron-thj-resolver`):

- **THJ added** — pool 254 → 255; `rosters_official.json` MIA entry; roster
  verification re-authored: 255/255 checked, 0 unmatched. Projection is an
  authored estimate from in-pool comps (Klay Thompson, Gary Trent Jr.,
  Duncan Robinson) — owner may reprice.
- **Apostrophe-insensitive fold** — `Dayron Sharpe` AND bare `Dayron` now
  resolve to Day'Ron Sharpe (the owner's named acceptance test). Hyphens
  deliberately untouched: stripping them would make bare `Alexander`
  ambiguous (SGA vs Alexander-Walker).
- **Injury-aware namesake tiebreak** — bare `Sharpe` → Day'Ron, with
  `(Shaedon Sharpe skipped: injury-excluded)` printed.
- **Suffix retry** — `Jimmy Butler III` → Jimmy Butler.
- **Deck stale-UNKNOWN nudge** — strip names picks unfixed ≥ 12 picks.
- Validation at ship: test_draft **53/53** (5 new red-first cases),
  test_gates **10/10**, parity **EXACT** (64 fixtures), build safe-to-publish
  with a `--pool-changes` stamp, live deck republished.
- **`draft_state_49_fixed.json`** committed beside this report: picks 58–60
  de-rotated (JSON reorder — the CLI's double-log guard correctly refuses a
  3-cycle of already-logged names), 81 → Day'Ron Sharpe and 148 → Tim
  Hardaway Jr. via `draft fix`. Final: 156 picks, 0 UNKNOWN, 0 duplicates,
  all 5 repairs verified against the Yahoo recap.

## 5. Provenance

Produced 2026-08-25 by the Claude Code session working
`yahoo-fantasy-basketball` @ `4b8d375` (pool `eed45b60`, 254 rows) and this
repo. Inputs: owner-uploaded `draft_state_49.json`; owner-pasted Yahoo recap
(transcribed in `validate_49.py`, committed beside this report). Raw outputs:
`mock-draft-2026-08-25-49-validation.csv` (all 156 rows),
`validate_49_out.txt`. Re-verify volatile claims: rerun `validate_49.py`
against the engine repo; resolver probes reproduce with the form table in
`validate_49_probe.txt` (old engine = `git show ef9f193^:scripts/hoops.py`).
