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
| 2026-08-26 | 08-25 → 08-26 (1d) | 0 (kit) / 1 repaired (deck) | 0 | 0 | after-reports/after-report-2026-08-26.md — no roster changes; caught+fixed a malformed pool row publishing a truncated note, gated the class (gates 10→12) |
