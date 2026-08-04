# After-report — data pull 2026-08-04

**Pull window: 2026-07-27 → 2026-08-04.** Gate:
`PROVENANCE GATE: PASS — all rows sourced; verified 2026-07-13 .. 2026-08-04`.
Two-run regeneration byte-identical. Executed as Tier-1 item R2 of the
2026-08-04 independent system review (`report/system-review-2026-08-04.md`),
on owner instruction; the window's research was performed by the review's
current-facts sweep (20 items, each with dated sources or CANNOT VERIFY).

## NBA Roster Changes

| Player | Change | Date | Source(s) |
|---|---|---|---|
| Draymond Green | FA → GSW (re-signed 1yr/$27.7M; official Thu 7/30) | 2026-07-30 | nba.com/news/draymond-green-warriors-free-agency-2026; hoopsrumors.com 2026-07 [CONFIRMED, 2 sources] |
| Jeremy Sochan | FA → POR (1yr/~$2.63M) | 2026-08-01 | hoopsrumors.com/2026/08/trail-blazers-jeremy-sochan-agree-to-one-year-deal.html; 740thefan.com 2026-08-01 [CONFIRMED, 2 sources] |

Stat lines unchanged for both (no sourced role mechanism this window;
Draymond returns to the same team/role, Sochan's POR role is unknown —
role-staleness flag on Sochan's row for the October per-36 rebuild, same
treatment as the 7/27 Dort/Risacher precedent).

FA rows re-verified unsigned 2026-08-04 (provenance `verified_on`
refreshed with this run's sources): Harden (CLE framework agreed,
structure talks — [LIKELY] imminent), DeRozan (MIA favorites, nothing
agreed), Cam Thomas, Ivey, Kuminga. Westbrook still unsigned/excluded
[CONFIRMED]. Header caveat corrected: Kuminga is an unrestricted FA (ATL
declined his $24.3M option late June) — the prior "rights" framing was
wrong.

## Significant Fantasy Analysis Changes

Board movement (scripted diff vs 7/27 board): **zero entries/exits, zero
moves ≥3 ranks** — the two edits were team labels only; the engine reads
stats+GP, so rank stability here is by construction, not evidence of
anything (postmortem lesson). Engine header updated in the same pull
(DATA-PULL §4): Draymond/Sochan out of the FA list, Kuminga UFA wording,
Westbrook date, Kawhi timeline now "resolution could drag into 2027 if
contested" (ESPN ~7/29-30) — worse than the prior "NBA reviewing 7/24"
framing; his 35-GP row remains a flagged placeholder.

Deck plane (DATA-PULL §0.5-6, §7): **already current** — the deck's own
8/4 refresh had Draymond GSW and Sochan POR before this pull, and
`data/freshness.json` reads 2026-08-04 on the (now-merged) main. The
published artifact was rebuilt/republished today by the deck session
(built 2026-08-04, pool 246, verified by fetch during the review). No
deck edits or republish needed this pull. Cross-plane label diff for the
two edited rows: both planes now agree.

## Watchlist / open items

- **Jimmy Butler GP 55 looks optimistic** — late-July: ~6 weeks from
  resuming running, will miss the start of 2026-27, team prepared for
  longer [LIKELY]. No hard date to overturn 55; re-check next pull, GP
  edit needs a sourced timeline.
- **Peyton Watson DEN label at sign-and-trade risk** (MIL/LAC pursuing,
  DEN payroll ~$246M) — label stands, watch.
- **Harden → CLE** signing believed imminent; relabel the moment official.
- **DeRozan/Beal → MIA** "favorites," nothing agreed — watch.
- **Kawhi**: investigation could run into 2027 (arbitration path);
  35-GP placeholder stands; Mathurin RFA still frozen by the same probe.
- **Kon Knueppel (#101) and Keyonte George (#170)**: market-riser
  candidates from the review's cross-check (both inside a dated
  2026-07-27 market top-50, MEDIUM confidence) — stale-role review, needs
  research + mechanism before any projection edit; queued for next pull.
- Duren RFA (QO path live), VanVleet 55 GP (no new fact) — carryover.
- CANNOT VERIFY (carryover): Mark Williams foot status, Trey Alexander
  SL injury severity.

**Note on the definition of done:** this session operates under a
branch-only rule for this repo, so the pull is committed and pushed to
`claude/fantasy-basketball-agent-578128` (PR #4) rather than direct to
`main`. DATA-PULL §0.1 is satisfied when PR #4 merges — until then the
pull is visible on the branch but not to `main`-pinned surfaces. Deck
plane §0.5-6 obligations are already met on the deck repo's `main`
(merged today, d4f7678).
