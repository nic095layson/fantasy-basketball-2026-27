# Prompt for the main session: show the waiver date and "you dropped him" beside waiver and streaming picks

Paste everything below the line into the main session.

---

**Build order from David (owner pick 2026-11-03, option 1 of the runner's after-report): show Yahoo's waiver date, and a "you dropped him on <date>" note, beside every waiver-scan and streaming pick. Display only.**

Read first, on season/daily: `report/after-reports/after-report-2026-11-03-waiver-readds.md` (the evidence and the owner's pick, §4). Your own 11-02 report says the own-drop fix was "not built, the owner's word". This pick supersedes that **only for the display**. Options 2 and 3 (re-ranking, minimum gain) were offered and not chosen. Do not build them.

Governance: load plan-gate before your first edit and adversarial-verify before you report. Show David the compact plan (Goal · Method / parameters · Done when · If it breaks) before building. Build on a claude/ branch off main and open a PR. Do not merge it, and do not touch season/daily.

## What the problem is (from the after-report, EVIDENCE)

- Across 7 briefs (10-28 to 11-03), 5 of 17 printed pairs re-added a player David had dropped hours earlier. All 5 were on Yahoo waivers that morning, so none could be added that day.
- `co_gm.free_agents()` (scripts/co_gm.py:191) takes candidates as "pool player not on a roster". Nothing in `scripts/*.py` reads `waiverDate`.
- `daily_brief.status_inputs()` (scripts/daily_brief.py:80) already loads the pin's `free_agents.freeAgents`, but uses it only for injury codes.

## What to build

1. **Waiver date.** For each scan pair's add, and each streaming row, look the player up in that day's pinned `data/source/flaim/pull_<date>.json` → `free_agents.freeAgents[]`. If `acquisitionState == "waivers"`, print "on waivers until <waiverDate>".
   - Yahoo gives a calendar date with no time. Print the date as given and never invent a clearance time.
   - If the player is missing from the 100-row list, print nothing. Missing means unknown, not free.
   - **Name-matching trap (checked 11-03):** the pin says "Bobby Portis Jr." while the brief and league_moves say "Bobby Portis". Match through the kit's existing Yahoo↔pool name mapping (the one `flaim_live`/`league_moves` already use), never by raw string. The 11-01 known answer below fails on a raw match.
2. **Own-drop note.** If David's seat dropped that player within the look-back window, add "you dropped him <date>".
   - **Source: `data/news/league_moves_<date>.json`** (seat 10 / KEL'EL YAXEL HALQUETA, `dropped`), for today and the prior days in the window.
   - Do not use `data/managers/transactions.json`. `manager_log.py` runs after `morning.py`, so at brief time it holds yesterday's pull and misses that morning's drops (11-03: tr.114 at 05:02Z and tr.115 at 06:11Z, run at 13:03Z).
   - **Window: proposed 3 days.** Basis: the league's waiverTime is 1 day (get_league_info) and the evidence's re-adds were 0–2 days old. This is a method parameter. State it to David in one line, as a clickable choice with 3 days recommended, before the first run.
3. **Where it shows:**
   - The brief's "## Waiver scan" pair lines and the "## Streaming" lines in `scripts/daily_brief.py` (~281–305). Reuse the pattern of the existing `add_status` suffix ("— O today …, check before claiming").
   - The deck's Free Agents tab and Today card wherever a scan pair or streaming row appears (`scripts/season_deck.py`; the status-beside-each-row code is at ~236 and ~825).
   - The record (`waiver_top[]`, `streaming[]` in the brief JSON), as new fields `add_waiver_date` and `add_own_drop_date` (null when none).
4. **Unchanged:** the ranking, the candidate list, d_ecw, the title runs, the status gate, the decision log's matching, and every engine constant. A pair on waivers stays exactly where it ranks today.

## Done when

- **Known answer, 11-03** (pins on season/daily): the brief rebuilt from `pull_2026-11-03.json` + `league_moves_2026-11-03.json` shows
  - pair 1, Julian Champagnie: "on waivers until 2026-11-04 · you dropped him 2026-11-03"
  - pair 3, Cameron Johnson: the same two notes
  - pair 2, Tobias Harris: no waiver note (his existing O / ESPN-date flag unchanged)
- **Known answer, 11-01:** Bobby Portis shows "on waivers until 2026-11-03 · you dropped him 2026-11-01".
- **Negative case:** a player on waivers whom another team dropped (Kris Dunn in the 11-01 pin, waiverDate 2026-11-02, dropped by Podz) gets the waiver date and **no** own-drop note.
- Tests in `scripts/test_daily_brief.py`, `test_waiver_status.py` and `test_season_deck.py` cover:
  - waivers + own drop
  - waivers only
  - free agent
  - a player missing from the list
  - no pin (no note, no crash)
  - a drop outside the window
- The whole suite and the gates pass.
- The deck renders 7 tabs with 0 page errors.
- A before→after diff of the 11-03 brief shows only the added notes. Ranks and numbers are byte-identical apart from those notes.

## If it breaks

- No pin for the day → no waiver notes and one line "waiver dates not read today". Never assume free.
- league_moves missing for a day in the window → the own-drop note covers only the days present, and the brief names the missing days.
- If a change would move any rank or number, stop. It is outside this build order; report it to David.

## Report back

One bold outcome line, then:
- a before→after table of the 11-03 lines
- tests and gates
- the PR link
- the window David chose

Commits use the neutral label "Claude (session model A)". No model names.
