# OPEN — disputed results and unanswered owner questions

Re-read after every compaction (RULES.md rule 8). An item leaves this file only by an owner
decision or a record that settles it, named in the line that closes it. Mirrored in the deck
repo's `OPEN.md`; this kit copy is the master.

## DISPUTED (never cite as a finding)

| id | result | disputed by | record |
|---|---|---|---|
| X-1 | The 20-season usage backtest (window 2006-07 onward, set by the data file's extent) and the WO-5b new-team-usage candidate built from it | owner, 2026-10-13 | `report/after-reports/after-report-2026-10-13-scope-fence.md` §4 R3–R6 |
| X-2 | "Projection confidence 97.8%" as a measure of accuracy — it measures agreement with the consensus the lines were blended toward | its author, 2026-10-14 | `after-report-2026-10-14-integrity.md` line 122; plan §1 self-reporting |
| X-4 | The league grade "22.50% title share" (2026-10-14) as the current figure — it ran 18 regular weeks and a fixed bracket; superseded by the 17-week reseeded re-run (`after-report-2026-10-15-co-gm-settings.md`) | the settings page, 2026-10-15 | `scripts/test_settings.py` red log |
| X-3 | Mock and league grades as independent evidence — the grader is the engine that built the card (circular) | plan 2026-10-15 §1, L6 | `report/plans/co-gm-self-audit-2026-10-15.md` §2 L6 |

## OPEN owner decisions (default if silent in brackets)

| id | question | default | record |
|---|---|---|---|
| D-S1-2 | Model weeks 7 and 17 (Yahoo's two 14-day matchups) as double-length in the simulator | not modelled; flagged | `after-report-2026-10-15-co-gm-settings.md` |
| D-SA-6 | SessionStart governor hook: P1, or pull into Session 1 if under an hour | P1 | plan §7 |
| D-LD-2 | Waiver move: Draymond Green for Christian Braun now / watch week 1 / Portis for Braun / stand pat | watch week 1 | `after-report-2026-10-14-league-draft.md` |
| D-LD-1, D83-1, D82-1 | Draft-page log/shift/resolver defects | P2 per D-SA-1 | plan §6 |
| D-1013-2 | RESYNC hardening | P2 per D-SA-2 | plan §7 |
| D-1009-2 | Availability discount zero at replacement level | P1 (B4) | plan §4 |
| D-INT-1 | Provenance re-dating pass (318 July rows) | Session 1 item 3 | `after-report-2026-10-14-integrity.md` |
| D-INT-2 | Commit the two lagging tools as standing versions | after the draft | `after-report-2026-10-14-integrity.md` |
| D-SF-1..4 | Scope-fence follow-ups (analysis-session prompt, lessons entry, Hashtag parse, usage dry run) | (a)/(b)/(b)/(a) | `after-report-2026-10-13-scope-fence.md` |

## Owner inputs requested, not yet received

| asked | what | for |
|---|---|---|
| 2026-10-15 | Standings and current scoreboard (none exist before 10/20; rosters RECEIVED 2026-10-15, pinned `data/source/`) | Session 1 item 5 |
| 2026-10-15 | Reseeding semantics (assumed: best remaining seed v worst) | `data/league_settings.json` |
| 2026-10-15 | The other ten teams' weekly pairings (only the owner's 17 opponents were supplied; the sim pairs the rest at random) | `league_sim.py --schedule` |
