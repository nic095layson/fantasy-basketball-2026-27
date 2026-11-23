# Playbook: the Braun and Queta lesson (2026-11-23)

Pull window: 2026-11-23 → 2026-11-23 (no pull: kit main 8f4b0c8, the records branch season/daily read only; documents only).

**Owner's request, verbatim (2026-11-23).** "Yes, add it to the playbook and lessons ledger to improve system recommendations and guidance in the future", after he wrote: "I really messed up with dropping Braun. Cautious tale for moving forward. I personally think Queta is a solid center, but the Kit and even Yahoo say otherwise (ranked ~180 player)".

**Method up front.** Stated to the owner before the change: his words quoted as written in OWNER-PLAYBOOK.md section 3, with a marked session reading built from the records; the lessons-ledger entry goes to the deck's LESSONS.md in its own pull request.

**Verdict. The playbook carries his lesson verbatim, with the record behind it: the Braun drop of 2026-10-24, the kit's own three graded-wrong Braun drop calls, and the category lines of both players on the 2026-11-23 board.**

Runner impact: none.

Pool rows touched: none

## 1. Evidence used (all read 2026-11-23)

| fact | record |
|---|---|
| Braun dropped 2026-10-24 with Anthony Black, for Collin Gillespie | `data/decisions/moves.jsonl` M-2026-10-24-01 |
| The briefs named Braun as the drop 10-20, 10-21 (Portis) and 10-22 (Champagnie); graded KIT WRONG, -3.29 / -3.27 / -1.70 | `report/decisions/scorecard.md` |
| Braun #56 (z_adj +0.65: STL +1.14, TOV +1.15, FG% +0.66); Queta #129 (-1.59: FG% +1.56, BLK +1.11, REB +0.94, TOV +0.89; 3PM -1.52, STL -1.55, FT% -1.13, PTS -1.01, AST -0.88) | `report/season/board_2026-11-23.json` |
| Team-level scan: Gillespie for Wiggins +1.1 title, for Queta +0.5; Cam Johnson +0.8 / +0.1 (±0.7) | the session's package scans of 2026-11-23 |

The owner's "~180" is Yahoo's rank, not checked here; the kit's board has Queta at #129.

## 2. Provenance

Session of 2026-11-23 (session model B, continuing the Main session; branch `claude/playbook-braun-lesson`).
