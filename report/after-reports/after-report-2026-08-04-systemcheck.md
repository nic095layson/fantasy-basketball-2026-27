# After-report — full-system calibration, validation & integrity check, 2026-08-04 (evening)

Run after today's changes: the independent system review, the deck PR #3
merge + LESSONS reconciliation, the Routine repairs, the kit data pull, and
the ingestion of the owner's 2025-26 weekly category dataset. Method: every
check below was executed this run (commands + outputs, not recalled);
calibration is **measure-only** — the deck plane is under feature freeze and
the refit is the September session's registered work.

## 1. Integrity (is anything broken, missing, or self-contradicting?)

| Check | Result |
|---|---|
| Kit provenance gate (structural) | PASS — 220/220 rows sourced, span 2026-07-13..2026-08-04 |
| Kit CSV ↔ provenance row match | 220/220, 1:1, no orphans/duplicates |
| Kit engine header vs CSV state | CONSISTENT — FA set {Harden, DeRozan, Kuminga, Cam Thomas, Ivey} matches; Draymond=GSW, Sochan=POR, Westbrook absent |
| Kit git state | Clean tree; branch synced at `d4ddbd3` (PR #4) |
| Deck main ↔ PR #3 branch | 0 unmerged commits — fork fully resolved |
| Deck LESSONS numbering | 6 headers (9-A, 10, 11, 12, 13, 14), no collisions |
| Deck plan laws | E9b row present; §6 "October final refresh" present; bar-registry law present |
| Deck LEDGER | Stale second tally gone; single quotable-tally rule in place |
| Deck roster validation (`verify_rosters.py`) | 246/246 checked, 30 teams, 0 mismatches (fallback-partial — ESPN direct still proxy-blocked) |
| Weekly dataset | 44 rows / 22 matchups, arithmetic 22/22; season-record reproduction (103-58-1) holds |
| **Cross-plane label gate (R9 prototype, first run)** | **197 shared names, 0 team mismatches** |
| Co-GM raw surface | `raw.../main/LESSONS.md` serves lessons 13–14; weekly CSV serves 45 lines — chat plane sees today's work |
| Published deck artifact | Fetched: built 2026-08-04, pool 246, verification fallback-partial, footer narrative current (Sochan POR, Draymond GSW, Kawhi ON HOLD) — publish ↔ repo coherent |

## 2. Validation (do outputs match independent reality?)

- Kit engine two-run regeneration: **byte-identical** (determinism law
  holds); regenerated board matches the committed board exactly.
- Board invariants: negatives-never-shrunk — 0 violations in 200 rows;
  positive-GP<82 adjustment — 1 flag investigated and **cleared** (Dejounte
  Murray, zPG +0.01: true zAdj ≈ +0.008 rounds to +0.01 at 2-decimal
  display; a print-precision artifact, not a law breach).
- Weekly dataset external validation: every matchup's category score
  recomputed from raw totals matches the recorded scoreboard result
  (22/22), and the owner's summed regular-season rows independently
  reproduce the displayed 103-58-1 record including the single tie
  (week 1 TO 68–68).
- Pull accounting: pull-log row (2 edited / 0 added / 0 removed) matches
  the actual commit diff (2 CSV team cells; 7 provenance refreshes noted
  separately in the after-report — no banner-arithmetic recurrence).

## 3. Calibration readout (measure-only; no dials turned)

From the owner's 18 regular-season weeks (16 schedule-normal, excluding the
21-game short week and the 56-game All-Star double week):

- **Games model:** observed 43.0 games/week mean, sd 3.7 (normal weeks)
  vs the arena's implied 3.5 × 13 = 45.5. The model runs ~6% hot on weekly
  games and understates schedule-structure variance (full-range 21–56).
  [EVIDENCE: computed this run]
- **Weekly category variability (owner team, CV):** BLK .273 and STL .189
  noisiest; FT% .031 and FG% .048 steadiest; 3PM/REB/AST/TOV cluster
  .149–.155; PTS .096. The hand-set constants' *ordering* (STL/BLK most
  volatile, percentages least) is directionally consistent with reality;
  magnitude comparison requires the September decomposition (team-week CV
  ≠ per-player-game CV — GP variance is bundled in these numbers).
- **Non-circular refit targets now on record:** owner's per-category win
  rates across 19 matchups — STL 14/19, FT% 13/19, TOV 13/19, 3PM 12/19,
  FG%/PTS/AST/BLK 11/19, REB 9/19. The refit model must reproduce these
  without being tuned on them.
- Bracket datum: champion won QF/SF/F all 5-4 with a 78-82-2 regular
  season; owner (best record, 103-58-1) exited the QF 2-7 with ST lost by
  1, PTS by 10, REB by 9. Feeds E14's re-baseline; no model change today.

## 4. Known-open items (unchanged by this check, honestly restated)

- Kit freshness gate at `--max-age-days 14`: 207/220 rows over the limit
  (verified 7/13–7/27; only news-touched rows refresh under the pull
  protocol). This is by design until the October full re-verification —
  not a defect today, but the October gate will require all 220.
- Deck tooltip truth fixes (review F6: punt-aware claim, retired 🎯
  composite description) confirmed still present in the fetched artifact —
  queued R14, ships with the next deck rebuild.
- ESPN direct roster verification remains proxy-blocked (fallback-partial
  is the operating mode); arena evidence backfill (R8) remains September
  work; E18 sim-side numbers remain `[UNREPRODUCIBLE]` until then.

## 5. Verdict

**All integrity and validation checks pass; zero new defects found; one
false positive investigated and cleared.** Both repos, both scheduled
Routines, the published artifact, and the chat surface are mutually
coherent for the first time in the system's recorded history (the
cross-plane gate's first run: 197 shared names, 0 mismatches). The weekly
dataset is validated to scoreboard ground truth and is now the standing
calibration bench for the September refit, with its success criteria
(per-category win rates, games distribution) recorded here before any
tuning happens — pre-registered, per house law.
