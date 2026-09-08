# After-Report — Data Pull 2026-09-02

**Pull window: 2026-09-01 → 2026-09-02 (1 day — the design case).**
Gate: `check_provenance.py` → `PROVENANCE GATE: PASS — all rows sourced;
verified 2026-07-13 .. 2026-09-02`, exit 0.

> **Headline.** The NBA closed the Clippers / Kawhi Leonard cap-circumvention
> investigation today. This is the event the Kawhi discount has been pricing
> for seven consecutive pulls. **No team labels moved** — the trade it unblocks
> is cleared but not confirmed executed. See §2 for why that distinction was
> held, and §4 for what it means for the next pull.

## 1. NBA roster changes

**Zero placements moved on either plane.** Board diff **0 entries / 0 exits /
0 moves ≥3** — and 0 rank moves of any size. `verify_rosters` **255/255, 0
mismatches, 0 unmatched**, dated 2026-09-02.

Sweep run: transactions aggregators (Spotrac, RealGM, HoopsRumors, NBA.com
offseason tracker via dated search), general transaction searches, an injury
sweep, the FA rows, every open item from the 9/1 after-report, and the
scripted JUDGMENT enumeration. Direct page fetches to every sports and news
domain re-tested this run were blocked by the environment egress policy
(ESPN, NBA.com, `pr.nba.com`, CBS Sports, CNN, Sportico, CP24, The Globe and
Mail) — claims rest on dated web-search results corroborated across
independent outlets.

### The one material event — and why no row moved

**NBA announces findings and penalties, 2026-09-02** `[CONFIRMED]`
(NBA Communications release; CNN 9/2, Deseret News 9/2, Sportico, CP24 9/2,
BlogTO 9/2, The Globe and Mail, Bleacher Report, Heavy — independent and
mutually consistent):

- Clippers forfeit **five first-round picks** (2029, 2030, 2031, 2032, 2033)
  and are **fined $30M**.
- **Steve Ballmer** and business-ops president **Gillian Zucker** suspended
  **one year**; basketball-ops president **Lawrence Frank** suspended **six
  months**.
- Findings: a pattern of off-court income routed to Leonard through Clippers
  corporate partners — **Aspiration, Boingo, Daktronics, Lockton**. The
  Daktronics channel, carried as *alleged* in yesterday's card, is now part
  of the league's own findings.
- **Leonard was NOT suspended and his contract was NOT voided.** He pays the
  league **$700,000**.
- Penalties are final and not appealable; the Clippers say they "vehemently
  reject" the findings.

This lifts the league hold on the **June 30 trade**: Leonard to Toronto for
**Brandon Ingram, Gradey Dick**, unprotected **2031** and **2033** firsts, a
**2027** first-round swap, and **2030** and **2033** seconds.

**Rows held, not moved.** The trade is *cleared*, not *confirmed executed*:

| evidence | says | weight |
|---|---|---|
| CP24, BlogTO, Globe and Mail, SI, Yahoo (all 9/2) | ruling "clears the way"; trade "will likely be unpaused" | outlet-level, consistent |
| two further searches | "not yet finalized as of the most recent reporting"; "agreed but frozen… has not yet been officially finalized" | outlet-level |
| one Threads post (`@theboxscoreph`) | "OFFICIAL: … has officially been completed" | **single aggregator social post** |

One aggregator social post is not two independent sources, and it is
contradicted by the outlet-level reporting in the same sweep. Under §3 a team
change needs the transaction to have *happened*. **Leonard stays LAC; Ingram
and Dick stay TOR.** What did change is their `note` cells, which said
`(league hold)` and now say `(league hold LIFTED 2026-09-02, awaiting
execution)` — three rows, note text only, zero team or stat edits. Leading
availability tags are untouched (Kawhi `inj-risk` → 0.78; Ingram and Dick
`trade-agreed` → 1.0).

Their kit-plane provenance rows were **re-verified today** against the ruling
coverage (source date and `verified_on` → 2026-09-02) without changing a team
value.

### Other window items, all checked and held

| item | finding | action |
|---|---|---|
| **Jalen Duren** | HoopsHype **2026-09-01**: DET and Duren **~$5M/yr apart** — five years at ~$35M per vs a $40M-plus ask. **Oct 1** is the last day to sign the $9.6M QO. | Card rebased; adj **held −0.08** |
| **Bennedict Mathurin** | LAC **formally withdrew** the $8.8M QO **8/29** (Keith Smith/Spotrac, RealGM, HoopsRumors); 2yr/$16M NOP complete | Card's stale "not formally withdrawn yet" line **removed**; adj held −0.15 |
| **Cam Thomas** | still unsigned, no dated event in window | hold |
| **Jaden Ivey** | still unsigned; dated waiver (CHI, **2026-03-30**, conduct detrimental) re-confirmed | hold; board header corrected (§3) |
| **Lonzo Ball** | still unsigned | hold |
| **Jeremy Sochan** | POR non-guaranteed camp deal, no change | hold |
| **Jalen Brunson** | no new wrist reporting in window | hold |
| **Cam Whitmore** | traded to CLE in the Watson/Strus/Mann multi-team deal, **waived**, cleared waivers, now a UFA | **CANNOT VERIFY closed** — he is on no pool row, so correctly absent |
| **Mark Williams** | **10th quiet pull** | hold — see §4 |

### Two stale/garbled items refuted before they touched a row

- **"Hornets' Mark Williams to miss training camp with a foot injury."** The
  sweep surfaced this as if current. It is **2024-25 Charlotte-era reporting**
  — it names Charles Lee as the new coach and a 19-game season ended by a back
  injury. **Mark Williams is a Phoenix Sun on this board.** Not applied.
- **"New Orleans withdrew Mathurin's qualifying offer."** The same aggregator
  garble refuted on 8/26 and 9/1 resurfaced on 9/2. It was the **Clippers'**
  offer. Refuted a third time; the correction is now written into his card so
  future sweeps stop re-litigating it.

## 2. Significant fantasy analysis changes

**Kawhi Leonard: adj COLLAPSED −0.25 → −0.08.**

Yesterday this card was *widened* −0.20 → −0.25 on ESPN's "could run into
2027, no timetable." **That thesis was refuted one day later** and is
retracted in the card text rather than quietly dropped. The −0.25 explicitly
priced the **horizon** ("an unresolved trade that runs into the season means a
mid-season team-and-role change for TWO pool rows"). The horizon is gone: the
ruling is final, he is not suspended, his contract stands, and the trade is
cleared. What remains is last-mile execution plus role integration in Toronto
— hence −0.08 rather than 0. Penalties `[CONFIRMED]`; execution `[LIKELY]`;
magnitude `[SPECULATIVE]`.

**Jalen Duren: held −0.08, rationale rebased.** The 8/27 narrowing leaned on
Fischer's "on track for a four-year, $160M deal." The 9/1 reporting supersedes
that framing ($5M/yr apart). Held rather than re-widened because the Oct 1 QO
deadline *replaces* open-ended camp-timing risk with a dated forcing function,
and he is a Piston on every branch — extension or QO — so there is no team
risk to price.

**Bennedict Mathurin: held −0.15**, superseded QO sentence removed.

No projection edits, no line changes, no structural-knob changes. Board
unchanged (diff ran clean).

## 3. Two truth defects found and fixed

- **The deck's "Data." colophon was two weeks stale.** It still narrated the
  **8/18** pull, counted **254 rows** against a 255-row pool (three places),
  and stated *"Kawhi's Toronto trade is still ON HOLD"* — false as of today.
  `build_deck.py` auto-updates only the `Pool refreshed <date>` token; the
  prose is hand-authored and had drifted. Rewritten for this window. This is
  user-facing text on the published artifact, so it is a delivery defect, not
  cosmetics.
- **`rank_engine.py` header contradicted the deck's own evidence.** It called
  Ivey's FA label "a contract tracker plus the absence of any reported
  signing, not a dated news item… the weakest label on the board." The deck's
  JUDGMENT card has carried the dated 3/30 CHI waiver since **8/26**, and this
  sweep re-confirmed it. Header corrected per §4 (the board must not
  contradict itself). Note this stale claim was also repeated in the **9/1**
  after-report's watchlist.

## 4. Watchlist / open items

- **Kawhi + Ingram + Dick — the next pull very likely moves three rows.**
  Leonard LAC→TOR, Ingram TOR→LAC, Dick TOR→LAC, on trade execution. This is
  the highest-probability pending change on the board; it is *not* applied
  today. Ingram's Toronto line and Dick's role will both need a reprice once
  the deal processes, and Leonard's Toronto role likewise.
- **Duren — hard date now on the board: Oct 1.** Either an extension or the
  $9.6M QO. Re-check before then; this resolves inside the October refresh
  window.
- **Mark Williams — 10th quiet pull, and now diagnosed.** Every search hit
  resolves to 2025-26 (PHX: left-foot stress reaction, third metatarsal,
  walking boot in the OKC series) or stale Charlotte-era content. There is no
  current PHX camp reporting because camps have not opened. Carried on the §6
  October must-do list; his row keeps `inj-risk`.
- **Camp opens late September** — Kuminga's usage share and Mathurin's NOP
  role are the first reprice candidates, both explicitly labelled as such on
  their cards.
- **Cam Thomas / Jaden Ivey** — the two FA rows.
- **September trigger: still blocked on owner input.** §1.2 (consensus ADP)
  and §1.2b (projection datasets) are unchanged from 9/1 — D-S1 and D-S2 below.
  §1.4 and all §2 experiments remain held; **zero append-only bars consumed.**
- Carried: Sarr/Sharpe cross-plane severity mismatches · four deck-draftable
  names missing from the kit pool + owner decision D1 · PHI logjam · Brunson
  wrist (informational, no multiplier).
- **Closed this pull:** Whitmore CANNOT VERIFY (6 pulls) · Mathurin QO
  mechanism (fully resolved) · Kawhi investigation horizon (7 pulls).

## 5. Verification (adversarial pass)

- **C1 — the tempting error was the opposite of yesterday's.** On 9/1 the risk
  was applying a garbled item; today it was *under*-applying a real one. A
  single post saying "OFFICIALLY COMPLETED" against the biggest story of the
  window is exactly what a hurried pull would have taken. It was checked, found
  to be an aggregator social post, found contradicted by two outlet-level
  searches in the same sweep, and **did not move a team label**. The penalties,
  which *are* multiply sourced, were applied in full.
- **C2 — yesterday's own conclusion was refuted, and the retraction is written
  where it can be seen.** A −0.25 widening one day old is now −0.08. The card
  says so explicitly rather than presenting the new number as if it had always
  been there. A judgment layer that quietly overwrites its own reasoning is
  unauditable.
- **C3 — the D-S5 enumeration refinement was validated before being asked
  for.** Requiring an *unresolved* marker rather than any transaction word cut
  the flagged set from 18 to **8** with no loss: the 8 are exactly the
  genuinely-open subset identified by hand on 9/1, and resolved trades
  (Kuminga, DeRozan, Harden, Strus, Mann, Watson) correctly dropped out. That
  is evidence for D-S5, not just a proposal.
- **C4 — two gates fired on my own work and were obeyed, not bypassed.** The
  malformed-row gate rejected an unquoted comma in the new note cells (the
  class of defect added after the 8/26 truncation). Gate 4 rejected a
  "pool changed" assertion after an intermediate build had already recorded
  the new hash; fixed by restoring the manifest to the last *published* pool
  and rebuilding once. `--force` was not used, and `--allow-stale` was not used.
- **C5 — stale-prose sweep should be systematic, not incidental.** The
  colophon defect (§3) was found by grepping for a row count, not by any gate.
  Nothing checks hand-authored prose against the current pull. See D-S6.
- **Not claimed:** roster verification remains `fallback-partial` against an
  owner-authored ledger (egress policy). Every 9/2 claim here rests on dated
  search summaries across independent outlets, not on fetched article bodies —
  every direct fetch attempted today was blocked. The trade-execution question
  is the one place where that thinness actually bites, and it is the reason
  the rows were held rather than moved.

## 6. Decision sheet (owner disposes)

| # | decision | recommendation |
|---|---|---|
| **D-S1** | Upload the 2026-27 **projection/ranking datasets** (§1.2b) | unchanged from 9/1 — this is the input the September plan waits on |
| **D-S2** | Provide **September consensus ADP** (§1.2) — paste a table, or allow one ADP domain through egress | unchanged; a paste is enough |
| **D-S4** | **October Routine** — exists and is armed (`trig_0146xxp4wAt4uHQypXLxjNZ1`, 2026-10-12 14:00Z). Its one forced test run aborted mid-turn | do not recreate; decide between leaving it armed with a manual prompt in reserve, or one more forced test run |
| **D-S5** | Promote the JUDGMENT scan to `scripts/judgment_open_items.py` with the unresolved-marker refinement | **yes — now validated** (18 → 8, no loss). It is currently re-typed by hand every pull |
| **D-S6** | **New.** Add a build gate that fails when hand-authored deck prose contradicts the current pull — at minimum the colophon's row count vs the actual pool, and a staleness check on its narrated pull date | yes; §3 shows prose drifts silently while every computed surface stays correct |

## 7. Gates

`verify_rosters` **255/255, 0 mismatches, 0 unmatched**, dated 2026-09-02 ·
`check_provenance` exit **0** · `freshness --stamp` green with an explicit
`--pool-changes` assertion (note cells, 3 rows) · `build_deck.py` all gates
pass — 255 players, pull 2026-09-02, pool `9b2316a313de`, injection round-trip
byte-identical · `check_parity.py` **EXACT MATCH** (2295 z-cells, 64 name
fixtures, 72 df_hash vectors, 78 card orderings) · `test_draft.py` **53/53** ·
`test_gates.py` **12/12** · board diff **0/0/0**.
