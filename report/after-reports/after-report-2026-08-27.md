# After-report — data pull 2026-08-27

**Pull window: 2026-08-26 → 2026-08-27** (1 day — the design case).
**Gate status:** `PROVENANCE GATE: PASS — all rows sourced; verified 2026-07-13 .. 2026-08-27` (exit 0).
**Orphan check (step one, before any edit): CLEAN.** The live artifact manifest
was fetched first and matched git `HEAD` exactly — `built: 2026-08-26`, pool
255, `c971f5d75a72…`. Two surfaces in sync; no orphan to recover.

**Process fix from the 8/26 pull was executed and it worked.** That pull missed
a transaction because unresolved situations living in the JUDGMENT layer never
got targeted searches. This pull enumerated them **from the file, not from
memory** — a scripted scan of every JUDGMENT entry whose text describes an
unresolved situation returned **18 names**, each then searched individually.
That enumeration is what surfaced the Kuminga signing below; the general
date-phrased transaction sweep did **not** return it, exactly as last time.

**Sourcing note:** direct page fetches to sports domains remain blocked by the
environment egress policy (unchanged). Web *search* works, so every claim rests
on dated search results rather than fetched article bodies. Stated, not swallowed.

---

## 2. NBA Roster Changes

**One roster change in window.**

| player | change | date | sources | applied |
|---|---|---|---|---|
| **Jonathan Kuminga** | **FA → MIN** — two years / $13M with a player option | 2026-08-26 | ESPN/Shams (quoting agent Aaron Turner directly), NBA.com, NBC Sports Bay Area, NBC New York, Bleacher Report, OpenCourt (8/27) — **[CONFIRMED]**, six independent | **Yes**, both planes |

He chose Minnesota over the Lakers, Bulls and Trail Blazers, **turning down a
similar starting role at $12M+/yr over three years in LA** for a shorter deal
and more control of his future. He leaves the FA block; **two rows remain
labeled FA — Cam Thomas and Jaden Ivey.**

**Line HELD — and here the reasoning differs from Mathurin's yesterday.** This
signing *does* carry a named, sourced role mechanism, which §3 would normally
let me reprice on: Shams reports outright that Kuminga **"will be a starter
alongside Anthony Edwards, LaMelo Ball, Jaden McDaniels and Rudy Gobert."** But
the mechanism **confirms the line already on the row rather than moving it** —
that row was already priced starter-shaped (16.0 ppg on 13.0 FGA; kit 28 mpg /
66 GP). No source gives minutes or a games figure to reprice against, and
repricing toward a number nobody reported would be inventing precision. Held,
with the residual carried in the JUDGMENT adj instead.

**Everything else in the sweep held:**

- **Cam Thomas, Jaden Ivey, Lonzo Ball** — all re-verified **still unsigned**
  ([CONFIRMED] by HoopsRumors' late-August "several longtime players remain free
  agents" plus the absence of any reported signing). Ivey's label still rests on
  a tracker plus absence, not a dated news item — **weakest label on the board**,
  sixth pull running.
- **Kawhi Leonard — 6th consecutive hold.** Nothing in window; freshest
  reporting remains 8/10 (resolution expected within six weeks) and 8/17 (ESPN's
  no-direct-funneling finding, publicly disputed by the league). Silver expected
  to announce before the season. A resolution still moves **two** pool rows via
  the Ingram return.
- **DeMar DeRozan, Draymond Green, Paul George** — a general date-phrased sweep
  surfaced items on all three ("Kings waive DeRozan", "Wizards in conversations
  with free agent DeRozan", "Draymond returns to GSW", "PG waives trade bonus").
  All three were checked against our rows and are **pre-window content the
  aggregators are still serving**: DeRozan is already DEN (signed 8/21, line
  repriced), Draymond already GSW, George already BOS. No action — logged
  because "the search returned something" is not the same as "something changed."

## 3. Significant Fantasy Analysis Changes

**Kit board unchanged (diff ran clean).** `rank_engine.py` regenerated; the
scripted diff against the pre-pull snapshot returned **0 entries, 0 exits, 0
moves ≥3 ranks**. Expected: a team label does not enter the kit's stat-based
value math. **No projection edits.**

**Kuminga's JUDGMENT adj COLLAPSED −0.30 → −0.05.** The old discount was priced
almost entirely for destination-and-role unknowns, and both resolved in one
report. This is a *collapse*, not a rebase — and deliberately unlike Mathurin's
−0.15 the day before, which only **held** its magnitude because one risk
(RFA route) was replaced by another (rotation-role risk on rotation money).
Kuminga's low AAV is **not** the market calling him a bench piece: he declined
more money and years elsewhere for the same role. What survives is usage-share
risk only — Edwards and LaMelo dominate this offense, so a third/fourth option
on a contender is a narrower band than his Golden State volume. Direction
[LIKELY], magnitude [SPECULATIVE].

**Duren's adj NARROWED −0.15 → −0.08.** Still unsigned, but the framing the
discount was priced on — both sides dug in, DET refusing the number, the $9.6M
qualifying offer openly weighed — no longer matches the reporting. Jake Fischer,
carried 8/25–8/27 by HoopsHype, Yahoo Sports, RotoBaller, Yardbarker and
ClutchPoints, has the sides **on track for four years upwards of $160M**, DET in
the $35–38M AAV range against his ~$287M ask. Fischer verbatim: *"I talked with
someone today who still believes he's on track for a four-year, $160 million
deal."* **Not narrowed to zero** — nothing is signed and RFAs have about a month
left. What survives is camp-timing risk; the QO-year scenario and its role
uncertainty are receding. He stays in Detroit on every live branch, so there is
no team risk to price. Direction [LIKELY], magnitude [SPECULATIVE].

**Board-header contradiction caught and fixed in the same pull (§4 requires
it).** `rank_engine.py` hard-codes header caveats, and one of them read *"The
THREE rows still labeled FA — Kuminga, Cam Thomas, Jaden Ivey — were re-verified
unsigned 2026-08-25."* The Kuminga edit made the board contradict itself. The
header now records his departure and Mathurin's LAC→NOP move from yesterday
(which was never added to it), and reads **TWO** rows still FA. Verified in the
regenerated file.

**Checked, not assumed: Kuminga is absent from the top 200 both before and
after, and that is correct.** The engine has **no FA filter** — line 128 takes
the top 200 by `z_adj` from all 235 rows — so his exclusion is value, not
labeling: .720 FT%, 1.0 3PM, 0.8 STL, 0.5 BLK is a mediocre 9-cat profile behind
decent counting stats. Worth stating because "signed a starting job" and "rises
on a 9-cat board" are different claims, and only the first happened.

## 4. Watchlist / open items

- **Jalen Duren — closest to resolving.** Signing (or a QO acceptance) should
  land inside the next pull or two; either collapses the −0.08 or re-widens it.
- **Kuminga usage share — first reprice candidate.** If camp reporting gives
  minutes or names him ahead of / behind McDaniels in the pecking order, the held
  line moves.
- **Bennedict Mathurin (NOP)** — carried from 8/26; still the other reprice
  candidate at camp. Note his **$8.8M qualifying offer had not been formally
  withdrawn** as of yesterday's reporting (Fischer); administrative only, no
  fantasy row moves on it, and it was **not separately re-searched this pull**.
- **Cam Thomas / Jaden Ivey** — the two remaining FA rows. Ivey's label is the
  weakest on the board (tracker + absence, no dated news item), sixth pull.
- **Kawhi Leonard — 6th hold**, moves two rows on resolution.
- **Mark Williams' foot — 8th quiet pull.** Flagged repeatedly as an October
  must-do rather than a watchlist line; it has now outlived the usefulness of
  being carried as "quiet."
- Carried unchanged: Whitmore (**CANNOT VERIFY**, 5th pull, plus the standing
  CLE-vs-WAS row discrepancy) · Sarr and Sharpe cross-plane severity mismatches ·
  the four deck-draftable names missing from the kit pool + open owner decision
  D1 · PHI logjam.

## 5. Verification (adversarial pass)

**What the refutation pass actually caught this run:**

- **C1 — the sweep.** Full pass, and the reason is the process fix, not luck.
  The general date-phrased search returned **stale aggregator content** (trackers
  current through 8/19) and would have produced a false "quiet day" for the
  second pull running. The JUDGMENT enumeration is what found Kuminga. **Keep it
  and keep it scripted** — enumerating from the file is the part that worked;
  enumerating from memory is what failed on 8/26.
- **C2 — the roster lock fired correctly and was not bypassed.** The freshness
  stamp **refused** on first attempt because `roster_verification.json` still
  carried 8/26: in fallback-partial mode the artifact inherits the evidence
  file's own date, by design, so that nothing self-certifies. Resolved the
  sanctioned way — re-dated `rosters_official.json` to 2026-08-27 (the deliberate
  act meaning "I checked today", which I had), re-ran `verify_rosters`, then
  stamped. **`--force` was available and not used.**
- **C3 — a wrong number caught before it shipped.** The first stamp attempt
  asserted "256/256 rows verified." The pool is **255** — Kuminga was already a
  row and only changed team. Corrected before the successful stamp; no build
  ever carried it.
- **C4 — the board-header contradiction** (§3) was found by grepping the
  regenerated board for the edited name rather than trusting the clean rank diff.
  A 0/0/0 diff says the *rankings* did not move; it says nothing about prose the
  engine hard-codes. Worth keeping as a habit.
- **Not claimed:** no independent live roster source was reachable (egress
  policy), so verification remains `fallback-partial` against an
  owner-authored ledger. That is a real bound, unchanged since 8/09.

## 6. Gates

`verify_rosters` **255/255, 0 mismatches, 0 unmatched**, dated 2026-08-27 ·
`check_provenance` exit **0** · `freshness --stamp` green with the pool-changes
assertion · `build_deck` green, injection round-trip OK, pool `c1b911fd64f8` ·
`check_parity` **EXACT MATCH** (255 rows, 2295 z-cells, 64 name fixtures, 72
df_hash vectors, 78 card orderings) · `test_draft` **53/53** · `test_gates`
**12/12**.

Deck **republished to the existing artifact URL**, verified serving
`"Jonathan Kuminga","t":"MIN"`, `built: 2026-08-27`, JUDGMENT `date: 2026-08-27`,
Kuminga adj `-0.05`, Duren adj `-0.08`.
