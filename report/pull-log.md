# Data Pull Log

One row per pull. The next pull's window starts at the previous row's date.
A pull that is not pushed to main did not happen — see DATA-PULL.md §0.

| date | window | rows edited | added | removed | after-report |
|---|---|---|---|---|---|
| 2026-07-13 | full verification (roster audit, all 220 rows) | 39 | 0 | 0 | ../postmortem-2026-07-13-roster-audit.md |
| 2026-07-24 | — | — | — | — | RAN BUT NEVER LANDED — no commit, no report, invisible to later sessions (LESSONS.md lesson 10) |
| 2026-07-27 | 07-13 → 07-27 | 4 | 2 | 2 | after-reports/after-report-2026-07-27.md |
| 2026-07-27 | validation sweep (post-pull) | 1 | 0 | 0 | after-reports/after-report-2026-07-27-validation.md |
| 2026-08-13 | 07-27 → 08-13 (17d) | 2 | 0 | 0 | after-reports/after-report-2026-08-13.md |
| 2026-08-18 | 08-13 → 08-18 (5d) | 0 (kit) / 3 (deck) | 0 | 0 | after-reports/after-report-2026-08-18.md |
| 2026-08-20 | 08-18 → 08-20 (2d) | 2 (kit) / 3 (deck) | 0 | 0 | after-reports/after-report-2026-08-20.md |
| 2026-08-21 | 08-20 → 08-21 (1d) | 2 (kit) / 1 (deck) | 0 | 0 | after-reports/after-report-2026-08-21.md |
| 2026-08-25 | 08-21 → 08-25 (4d) | 3 (kit) / 3 (deck) | 0 | 0 | after-reports/after-report-2026-08-25.md — recovered later-8/21 deck orphan + shipped Insert-#/RESYNC to live |
| 2026-08-26 | 08-25 → 08-26 (1d) | 2 (kit) / 2 (deck) | 0 | 0 | after-reports/after-report-2026-08-26.md — Mathurin LAC→NOP (MISSED by the first sweep, caught on owner challenge, applied same-pull); fixed a malformed pool row publishing a truncated note + gated the class (gates 10→12) |
| 2026-08-27 | 08-26 → 08-27 (1d) | 1 (kit) / 1 (deck) | 0 | 0 | after-reports/after-report-2026-08-27.md — Kuminga FA→MIN (found by the JUDGMENT-enumeration process fix, not the general sweep); adj collapsed −0.30→−0.05 on a sourced starter role, line held; Duren narrowed −0.15→−0.08 (on track ~4yr/$160M, still unsigned); fixed a board-header contradiction in rank_engine.py |
| 2026-09-01 | 08-27 → 09-01 (5d) | 0 (kit) / 0 (deck) | 0 | 0 | after-reports/after-report-2026-09-01.md — no roster changes; Kawhi widened −0.20→−0.25 (ESPN: inquiry could run into 2027, no timetable); Mathurin QO formally withdrawn by LAC 8/29 (watchlist closed); two garbled aggregator items refuted (Mathurin/Sochan). SEPTEMBER TRIGGER: §1.1/§1.3 executed; §1.2 ADP egress-blocked, §1.2b datasets not uploaded; §1.4 + all §2 experiments deliberately held, zero bars consumed; the self-firing Routine never existed |
| 2026-09-02 | 09-01 → 09-02 (1d) | 3 (kit provenance) / 3 (deck note cells) | 0 | 0 | after-reports/after-report-2026-09-02.md — **NBA closed the Clippers/Kawhi Leonard investigation 9/2**: 5 first-rounders (2029-2033) forfeited, $30M fine, Ballmer + Zucker suspended 1yr, Frank 6mo; Leonard NOT suspended, contract NOT voided, pays $700K. League hold on the Kawhi→TOR trade LIFTED. NO team labels moved — trade cleared but not confirmed executed (the only 'officially completed' claim was a single aggregator social post, contradicted by outlet reporting in the same sweep); Kawhi/Ingram/Dick note cells restated and kit provenance re-verified. Kawhi adj COLLAPSED −0.25→−0.08 (yesterday's 'into 2027' widening retracted); Duren held −0.08 on rebased 9/1 reporting ($5M apart, Oct 1 QO deadline); Mathurin held −0.15, stale QO line removed. Fixed two truth defects: the deck colophon was 2 weeks stale (narrated the 8/18 pull, said 254 rows vs 255, claimed the trade was 'still ON HOLD') and rank_engine's Ivey caveat contradicted the deck's own dated evidence. Whitmore CANNOT VERIFY closed (6 pulls). |
