# Post-mortem — 39 stale team values in projections-2026-27.csv, 2026-07-13

Incident: a client spot check of three Lakers-adjacent players (Grimes,
Hachimura, Sexton) found all three `Tm` values wrong. The full audit that
followed ([roster-audit-2026-07-13.md](roster-audit-2026-07-13.md)) corrected
**39 of 220 rows (17.7%)** — in a file authored the previous evening and
presented as research-backed. This document is the why, and the gates that
now make the failure mode mechanically impossible to repeat silently.

## The failure, precisely

Every one of the 39 wrong values described a move that was **already public
when the CSV was written** (commit `29f2276`, 2026-07-12 22:38). Nothing
"broke after authoring." The misses span every vintage:

- a January blockbuster (Trae Young → WAS, traded 1/9 — six months old);
- February-deadline secondary pieces (McCain, Hunter, Mathurin, Hendricks,
  the Dosunmu↔Dillingham swap, Coby White, CP3's retirement);
- late-June trades (O'Neale/Allen → CHA 6/26, Claxton deal agreed 6/22);
- ten days of July free agency (Grimes, Sexton, Hachimura, Smart, Powell,
  Simons, Vučević, Robinson, Harris, Collins, Bogdanović, Drummond…);
- a four-team trade completed **two days** before authoring (LaMelo, 7/10).

Two rows were wrong about 2025-26 itself (Sexton "CHA" — he finished the
season in Chicago; Drummond "LAC" — a *2021-22* team). That detail is the
tell for root cause (a) below.

## Root causes

**(a) Team values came from model memory, not research.** The wrong values
are exactly what a language model's training data would say: pre-2026 rosters,
in Drummond's case a years-old one. The 220-row CSV landed **24 minutes**
after the baseline commit (22:14 → 22:38) — there was no time in that window
for per-player verification, and none happened.

**(b) The research that DID happen was headline-scoped, and it shows.** The
baseline's offseason ledger is accurate — not one of its ~15 verified
headline claims was falsified by the audit (JJJ → UTA even resolved as
written). But a ledger of headlines is not roster verification: every CSV row
the ledger touched was right (Giannis, Herro, Ware, Kessler, Zubac, Harden,
Garland, AD…), and the stale rows are precisely the players outside the
ledger's beam. The CSV = memory ⊕ headline patches. Coverage failed, not
accuracy.

**(c) The repo's own gates were bound to the occasion, not the artifact.**
PROMPT.md §0 already said "never assert a player's team from memory" and §7
already required every top-150 affiliation verified within 14 days — but both
were written as instructions for *the October run*. The July session produced
a claims-bearing artifact (220 player-team pairings) on a path where no gate
fired. The rule existed; nothing bound it to the file.

**(d) No per-row provenance made staleness invisible.** A reader of the CSV
could not distinguish "verified 7/12" from "remembered from 2024." With no
source column, the file's freshness was unfalsifiable — until someone spot-
checked three rows by hand.

**(e) The generated board overclaimed.** Its header said projections were
"adjusted for **every** verified 2026 offseason move," converting partial
coverage into an implied full sweep. Classic theater-over-truth: exactly the
failure mode the project charter (and Operating Principle #1: never invent
data) exists to prevent.

**Aggravating factor:** authoring date was July 12 — day 12 of a live free
agency described *in the same repo* as "a live market." Snapshotting rosters
from memory during peak FA maximizes damage per unverified row.

## What worked (keep)

- **The spot-check-as-signal instinct.** Three errors in one cluster were
  treated as a systemic alarm, not a patch list — that call is what surfaced
  the other 36.
- **The offseason ledger's accuracy.** Verified-headline research held up
  100%; the method is sound where it was applied.
- **Tm-only scope discipline.** Fixing the label without touching stat lines
  kept the audit reviewable and the tier-diff honest (0 moves, by
  construction — the engine never reads the team column).

## Fixes shipped (the gates)

1. **`report/roster-provenance.csv`** — a source ledger with one row per
   player: team, source URL, source date, verification date. Seeded from the
   2026-07-13 audit, so all 220 rows start verified. A team claim without a
   source now has nowhere to live.
2. **`report/check_provenance.py`** — the mechanical gate. Fails (exit 1) on:
   any CSV row without a provenance row, any team mismatch between the two
   files (i.e., someone edited one without the other), empty sources,
   malformed dates, orphan rows. `--max-age-days N` adds a freshness gate.
3. **`rank_engine.py` now refuses to build an unverified board.** The gate
   runs before ranking; on failure there is no output artifact. The escape
   hatch (`--allow-stale`) prints the defect count into the board header
   itself — "**TEAM LABELS UNVERIFIED … Do not draft off this board**" — so
   the shortcut can never be silent. A clean run stamps the verification date
   span into the header. (Tested 2026-07-13: pass, mismatch-fail, and
   allow-stale paths all behave as described.)
4. **PROMPT.md §0.6 (new):** the data policy binds every claims-bearing
   artifact at the moment it is written — "interim file" is not an exemption.
5. **PROMPT.md §7 (new checklist line):** the October run must pass
   `check_provenance.py --max-age-days 14` over **all** rows, not just the
   top 150 — the cheap tail rows are where memory-sourced teams hide.
6. **README + Appendix B workflow updated:** every CSV team edit and its
   provenance edit travel together, in the same change.
7. **The board header overclaim is gone** — replaced by the provenance stamp,
   which claims exactly what is checked and nothing more.

## Residual risk (named, not hidden)

- The gate proves a team claim **has a dated source**; it cannot prove the
  source was read correctly. A fabricated provenance row would pass. The
  defense is procedural (§0.2 two-source rule for load-bearing facts) plus
  the audit trail the sidecar now leaves for spot checks.
- Freshness is enforced at board-build time, not continuously. Between now
  and October the file will silently age — by design; the header stamp and
  the §7 --max-age-days gate make the age visible and block a stale
  *deliverable*.
- GP and stat lines have no analogous per-row gate. Out of scope here
  (they're projections, not facts), but the October run's §4.4 sanity gate
  and Pass C injury ledger are the corresponding controls — e.g., VanVleet
  (missed all 2025-26) and Butler (out to ~Dec) carry GP values this audit
  deliberately did not touch.

## The lesson, portably

A ledger of headline moves is not roster verification, and a data policy
bound to "the run" instead of the artifact will be skipped by every session
that doesn't think of itself as "the run." Any committed file asserting
live-world facts carries per-row source + date, and a machine check — not a
checklist item — stands between it and the artifact people consume. Recorded
as lesson 10 in the cross-project ledger
(`yahoo-fantasy-basketball/LESSONS.md`).
