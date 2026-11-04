# The turn gate treats a scheduled run as a turn of its own (owner pick 2026-11-03, decision A option 1)

Pull window: 2026-11-04 → 2026-11-04 (no pull: hook code only; kit main 37b936e, whose `hooks/` equal season/daily's; this session's own transcript read for the row shape).

**Method up front.** Build order from the owner (`prompt-2026-11-04-main-turn-gate-scheduled.md`, from Finding 1 of `after-report-2026-11-03-runner-window.md` on season/daily): every turn-gate caller judged "everything after the owner's latest message", and a scheduled run never moves that index, so a scheduled run and the owner's previous turn were judged as one span (a false block observed 2026-11-03 23:06Z; a false pass by the same logic). The boundary is matched on the notification header form only; the build order's trap (the fixed paragraph "A scheduled trigger is a stored prompt" in every notification read) was re-checked on this session's transcript before the build. Fixtures were written and run against the old code first. EVIDENCE marks what a run or read showed; INFERENCE what is derived.

**Verdict: `turngate.turn_start` starts a turn at the owner's latest message or the latest scheduled-trigger notification, whichever is later; the Stop gate (F1) and the pre-tool gates (F2, F3) use it; a scheduled run can no longer merge on an earlier owner word; the four fixtures and a fifth for the merge stance pass, three of them red on the old code; every hook selftest passes; the library is not patched and now differs from the kit.**

## 1. The row shape (EVIDENCE: this session's transcript, 2026-11-04)

| check | result |
|---|---|
| ReadNotifications results in the transcript | 75 |
| header regex `^--- Notification .*· origin: scheduled trigger` (multiline) | 13 (the scheduled tasks) |
| plain substring "scheduled trigger" | 75 (every result: the trap) |
| row shape of a scheduled one | `type` user; `message.content` a list with a `tool_result` whose `content` is a string starting "[SYSTEM NOTIFICATION" |
| `turn_start` on this transcript | equals `owner_index` (the last scheduled notification, 2026-11-02 20:01Z, precedes the owner's latest message) |

## 2. What was built (EVIDENCE: the diff, the selftests)

| change | where |
|---|---|
| `SCHEDULED_HEADER`, `scheduled_index(rows)`, `turn_start(rows)` = max(owner index, last scheduled notification row) | `hooks/turngate.py` |
| F1 (Stop gate) judges the span after `turn_start` | `hooks/governance-enforce.py` |
| F2/F3 use `turn_start`; a merge inside a scheduled run is denied ("a scheduled run never merges"), since it carries no owner word | `hooks/turn-gates-pretool.py` |
| `governance-trigger.py` unchanged (decision stated to the owner before the build): it runs only on an owner prompt, a scheduled run has none, and classifying a stored prompt's body would let stored text steer the governance cue | none |
| Fixtures S1 to S5 with a `notif()` builder in the real row shape | `hooks/selftest-turn-gates.py` |

The governor list, the outward-action list and the prompt classifier are unchanged.

## 3. Red first, then green (EVIDENCE: `python3 hooks/selftest-turn-gates.py`, old code then new)

| fixture | old code | new code |
|---|---|---|
| S1 replay of 2026-11-03 23:06Z (owner push before plan-gate; scheduled run loads both) | BLOCK (wrong) | ALLOW |
| S2 crafted skip (owner turn governed; scheduled run commits with no governor) | ALLOW (wrong) | BLOCK |
| S3 GitHub-only notification, no boundary | BLOCK | BLOCK |
| S4 explanatory paragraph, no scheduled header, no boundary | BLOCK | BLOCK |
| S5 a scheduled run merges on the owner's earlier "merge" | ALLOW (wrong) | DENY |

S3 and S4 pass on both by design: they guard against a boundary placed where none belongs (were one placed, the governed span after the notification would ALLOW).

| selftest | result |
|---|---|
| `selftest-turn-gates.py` | 44 passed, 0 failed (39 before + 5) |
| `selftest-governance-classify.py` | 45 passed, 0 failed |
| `selftest-reminders.sh` | 8 passed, 0 failed |
| `selftest-receipt-law.sh` | 15 passed, 0 failed |

## 4. The library

The hooks were ported from `nic095layson/claude-core-skills` (commits 4e883f9, 1d3a40e, 9dbbc3d). That repository is not attached to this session, so this is the kit-only path: **the kit's `hooks/turngate.py`, `governance-enforce.py`, `turn-gates-pretool.py` and `selftest-turn-gates.py` now differ from the library, and the library needs the same patch.** The library was not updated.

## 5. Bands quoted

No title share or model figure is touched or quoted. The standing structural band for any title figure is the season sweep of 2026-11-02 (deck e14cc42): **weekly_availability is FRAGILE:** -2.6 (no in-sim injury discount (risk 0.88 like healthy)) / +2.2 (harsher risk tier (0.65)) / -0.2 (healthy players play 0.95 of games) / +0.0 (healthy players play 0.80 of games).

Runner impact: code-only (the governance hooks, no prompt change). The runner's scheduled runs are now judged on their own: a run that loads plan-gate before its first commit and adversarial-verify before it ends passes, whatever the owner's previous turn did; a run that skips them is blocked; a run never merges.

## 6. Bounds and open items

- Out of scope by design: the prompt classifier; the library patch (not attached).
- In scope and unverified: the first live scheduled run after merge (the 05:00 Pacific morning run).

## Watchlist

- The next morning run after merge: its Stop gate verdict depends only on that run's own governor loads.

## Open-item receipts

This report touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward the same way the 10/22 day report carries them (`after-report-2026-10-22-day-findings.md`, Open-item receipts): from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21. None was re-queried for this report (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this report (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (`after-report-2026-10-21-pickups-file.md` §1) |

## Repeat-name market check

This report did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck 366d3ca (this PR changes no deck file), checked today, the same page the 10/22 day report replayed. Its table stands, carried here verbatim from the day report.

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 6a5cefea4921), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 33 of 33 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-14.csv`, Hashtag `hashtag-2026-10-14.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-14.csv`, `hashtag-2026-10-14.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 32 of 33 | 44 | 111 | 63 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 23 of 33 | 32 | 67 | 58 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 14 of 33 | 107 | 138 | 182 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 12 of 33 | 101 | 182 | 100 | 125 | 148 | 155 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| John Collins | 11 of 33 | 73 | 117 | 105 | 72 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 10 of 33 | 6 | 32 | 15 | 24 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 10 of 33 | 92 | 179 | 89 | 117 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Brandin Podziemski | 9 of 33 | 93 | 146 | 74 | 102 | 114 | 132 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 7 of 33 | 114 | 139 | 122 | 130 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Jaden McDaniels | 7 of 33 | 62 | 90 | 42 | 67 | 86 | 59 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Immanuel Quickley | 5 of 33 | 67 | 94 | 65 | 73 | 79 | 84 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Keegan Murray | 5 of 33 | 83 | 142 | 82 | 94 | 102 | 85 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (18 mocks, value 9, market 18); Derrick White (17 mocks, value 27, market 45); Lauri Markkanen (15 mocks, value 21, market 37); Tyrese Haliburton (13 mocks, value 7, market 12); Tyrese Maxey (11 mocks, value 5, market 9); Kel'el Ware (10 mocks, value 57, market 77); Tyler Herro (9 mocks, value 51, market 69); Karl-Anthony Towns (8 mocks, value 12, market 15); Miles Bridges (5 mocks, value 96, market 98).
