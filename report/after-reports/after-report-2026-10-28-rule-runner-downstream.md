# RULES rule 11: runner changes travel downstream, and RUNNER-ASK-v5 verified applied — 2026-10-28

Pull window: 2026-10-28 → 2026-10-28 (no pull for the kit: two read-only `get_trigger` reads of the runner's scheduled tasks; no market pull).

**Method up front.** Owner 2026-10-28: "Pasted in runner, please verify that it was applied", then "add a RULE that, any changes, updates to the Main session that implicates or updates/upgrades the runner's tasks, have this main session push or integrate downstream to Runner session".
- The verification compares each stored prompt, as the read returned it, byte for byte with the file the paste-ask named.
- The comparison is read mechanically from this session's tool results, never retyped.

EVIDENCE marks what a read or run showed; INFERENCE marks what is derived.

## 1. RUNNER-ASK-v5 applied (EVIDENCE)

| task | updated (UTC) | stored bytes | sha256 (first 16) | equals the file |
|---|---|---|---|---|
| morning (trig_01V43JtVvW6teWGmwt17dPVw) | 2026-10-28 18:53:26 | 15,081 | 96b815327c685ad6 | yes (`morning_v5.txt`) |
| afternoon (trig_015cHK6ECUvXA9TX1UNTT53r) | 2026-10-28 18:53:25 | 5,370 | d7031f07cba4b75d | yes (`pm_v2.txt`) |

- The morning text carries the retry rule (step 3a) and the waiver-status report line (step 7).
- The afternoon text carries the retry rule (step 2a).
- Before the paste, both reads matched the earlier texts (morning v3 14,452 bytes; afternoon 5,062).

## 2. Rule 11 (EVIDENCE: the RULES.md diff)

- **What triggers it.** A main-session change that alters what the runner's tasks run, read, write, commit or report.
- **What the same session does before calling the work done:**
  - reads both stored prompts;
  - drafts each edit with its diff, byte count and sha256;
  - hands the owner one paste-ask with what changed and what the next runs should show;
  - after the paste, confirms byte equality by reading both back.
- **"Runner impact" line.** Every after-report carries one: none, code-only, or a prompt edit with its read-back state.
- **Why "push downstream" ends at a paste-ask** (EVIDENCE). The tasks take prompt edits only from the conversation they post into: `update_trigger` from this session was refused earlier, and the doctrine never routes a refused action through another session. So this session does everything up to the paste and verifies after it. Code reaches the runner without any paste, because each run merges main.

## 3. Bounds

**Out of scope by design.**
- **No gate enforces the "Runner impact" line yet.** `report/check_report.py` could require it; that is a build left to the owner's word.
- **The deck repo's `RULES.md` was not changed.** Its copy was identical to the kit's ("both repos carry this page") and now lacks rule 11. The deck repo is not in this session's GitHub scope.

**In scope and unverified.** Whether the next runs show what the paste-ask listed is checked on tomorrow's morning report (Watchlist).

## 4. Next steps (owner decisions)

1. Merge this PR (rule 11 on the kit).
2. Sync the deck's `RULES.md` copy, or leave the rule kit-only, since only the kit has a runner.
3. Optionally, make `check_report.py` require the "Runner impact" line.

Runner impact: none from this PR (RULES.md only). The prompt edit of today (v5) is read back as matching (§1).

## Watchlist

- **Tomorrow's morning report** (2026-10-29) shows the waiver scan's status line and names any retry.
- **The afternoon report** (2026-10-28 22:03Z) names any retry.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| RUNNER-ASK-v5 applied | **VERIFIED**, byte-equal | §1 |
| main-to-runner rule | **ADDED** as rule 11 (kit) | §2 |
| deck RULES.md copy | **OPEN**, owner decision | §3 |

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
