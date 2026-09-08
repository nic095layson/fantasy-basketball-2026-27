# DATA-PULL.md — Incremental Data Pull Protocol (Claude Code)

You are running a **routine data pull** for the 2026-27 fantasy basketball draft kit
in this repo. This is NOT the October full build (`PROMPT.md` governs that). A pull
is a **delta cross-check against the last committed state**: sweep the news since
the last pull, verify what changed, edit only the rows that changed, regenerate the
board, write a short after-report, and **commit and push everything**. On a normal
day most of the 220 rows are untouched and the after-report is a few lines. That is
the expected outcome, not a failure.

## 0. Definition of done — read first

**A pull that is not pushed to `main` did not happen.** On 2026-07-24 a pull was
run whose output never reached the repo; three days later the next session could
not see it and correctly treated the data as 14 days stale. The repo is the only
persistent layer — chat transcripts, local analysis, and delivered files that were
never committed are invisible to every future session.

A pull is complete only when ALL of the following are true:

1. Edited data files are committed to `main` and **pushed** (verify with
   `git log origin/main -1` after pushing — confirm your commit SHA is there).
2. The after-report exists at `report/after-reports/after-report-YYYY-MM-DD.md`
   and is in the same push.
3. `report/pull-log.md` has a new row for this pull (same push).
4. `python3 report/check_provenance.py` exits 0.
4b. `python3 report/check_report.py` exits 0 (fix F2, 2026-09-08 — the
   publication gate: structure, single-source labeling, pull-log row), AND
   the deck plane's `python3 scripts/judgment_open_items.py --check-report
   <after-report>` passes (fix F1 — every flagged open item carries a
   receipts row). Born from Ben Simmons shipping as a Clipper and a NOP–MEM
   trade shipping unswept in the same report.
5. The Draft Deck data plane (`yahoo-fantasy-basketball` → `data/players.csv`)
   received the same window's news under its own laws (role-reprice,
   pool-completeness, roster validation lock), landed on a pushed branch/PR.
6. The Draft Deck artifact was rebuilt and **republished to its existing URL**
   with `built` = today (§7) — or the after-report states exactly why not.
   On 2026-07-27 the owner found the deck serving a 3-day-old pool because a
   pull treated the repo push as the whole job. The artifact is a delivery
   surface of this system; a pull that leaves it stale is not done.

If the push fails, say so explicitly and stop — do not report the pull as done.

## 1. Establish the baseline (no consequential edits before this)

1. `git pull` first — work from current `main` only.
2. Read `report/pull-log.md` (create it from the template in §6 if missing). The
   **window start** = the end date of the last logged pull. If no log exists, use
   the newest `verified_on` in `report/roster-provenance.csv`.
3. Window end = today. State both dates at the top of your output:
   "Pull window: YYYY-MM-DD → YYYY-MM-DD."
4. Snapshot the current board for diffing:
   `cp report/top-200-2026-27.md /tmp/top-200-baseline.md`

If the window is longer than 7 days, say so and widen the sweep accordingly (more
searches, lower threshold for re-checking injury statuses). A 1-day window is the
design case and should be fast.

## 2. Delta sweep (research, window-bounded)

Web research only — training-data memory is expired for everything here (PROMPT.md
§0 binds this file too). Sweep for events **reported inside the window**:

- **Transactions:** trades, signings, waivers, buyouts, retirements, players
  leaving for or arriving from overseas leagues. Check a transactions aggregator
  (RealGM transactions, RotoWire news feed, HoopsRumors via search) plus 1-2
  general searches ("NBA trades <month> <year>", "NBA transactions this week").
- **Injuries/availability:** surgeries, setbacks, new timelines, holdouts, trade
  requests. One general sweep + targeted checks on any player whose row already
  carries a GP discount if news is likely (in-season: check daily injury reports).
- **Open items from the last after-report:** read the previous after-report's
  "watchlist / cannot verify / open" section and re-check each item. This is how
  multi-day stories (e.g. the Kawhi trade investigation) stay tracked without
  re-deriving them. **Mechanized 2026-09-08 (fix F1):** run the deck plane's
  `python3 scripts/judgment_open_items.py` — every flagged name gets a
  DEDICATED search and one row in the after-report's "Open-item receipts"
  table (§5). A flagged name with no receipt means the pull is incomplete;
  the 8/26 Mathurin miss recurred on 9/8 on the same player precisely because
  the hand-run checklist was skippable and nothing audited execution.
- **Team-shadow sweep (fix F3, 2026-09-08):** the script also prints the TEAM
  WATCH SET the open items imply (each flagged player's team plus
  counterparties named in their rationales). Run one team-shaped news query
  per team. A trade about a flagged player's cap room or depth chart may
  never name the player — the 9/8 four-player NOP–MEM deal existed to
  complete Mathurin's signing and no player-name query could catch it.
- **Zero-trade anomaly rule (fix F5, 2026-09-08):** a multi-day window in
  which the sweep finds zero league-wide trades is a sweep-failure signal,
  not a finding. Run one ledger-shaped query (RealGM month/season
  transactions page, HoopsRumors trades index) and cite it before writing
  "no trades in window."
- **Returner-vs-tag diff (fix F6, 2026-09-08):** the injury sweep diffs
  "returning player" coverage against `judgment_open_items.py --tags` BOTH
  directions — tagged-but-now-cleared AND returning-but-untagged. Grading
  the headline instead of the row is how Jamal Murray (ruptured Achilles,
  untagged, availability 1.0) shipped certified as "already correct.".
- **FA rows:** any row with team `FA` gets a quick status check (signed? overseas?
  retired?).

Source rules (unchanged from PROMPT.md §0): every claim needs a dated source from
this run; **two independent sources for anything that moves a player a tier or
more** (team change, major injury, role change); tag claims `[CONFIRMED]` /
`[LIKELY]` / `[SPECULATIVE]`. If you cannot verify something, write CANNOT VERIFY
and move on — never guess, never fill from memory.

**Publication gate (fix F2, 2026-09-08): row impact no longer scopes
verification.** Any named transaction/team/injury fact that enters the
after-report, the deck colophon, or a PR body needs two independent sources
— or an explicit `[SINGLE-SOURCE]` label so the reader can apply their own
discount. `report/check_report.py` enforces the checkable core of this on
the after-report's tables. Ben Simmons shipped as a Clipper (he signed with
Sacramento) because he wasn't a pool row and nothing gated what got
*published*; it was the fifth documented search-summary garble. Also treat a
summarizer's "as of <date>" framing as the summarizer's date, not the
article's, unless the article's own date is visible.

## 3. Apply the delta — edit rows, never rebuild

**Forbidden: regenerating the projections CSV from scratch, re-deriving all 220
projections, or re-verifying rows with no news.** Rows without news in the window
are left byte-identical. Only these edits are allowed, and a CSV team edit and its
provenance edit always travel in the same change (the gate enforces this):

- **Team change** → update `team` in `report/projections-2026-27.csv` AND the
  matching row in `report/roster-provenance.csv` (new source_url, source_date,
  verified_on = today). Stats stay unless there is a sourced role mechanism.
- **Player leaves the pool** (retired, signed overseas, out for the season with no
  stash value) → delete the row from BOTH files; say so in the after-report.
- **Player enters the pool** (unsigned FA signs, missed-by-the-pool player becomes
  relevant) → add rows to BOTH files. Base rates for the projection come from a
  stats source fetched this run (Basketball-Reference), scaled for role/age, and
  the projection is labeled **[ESTIMATED]** with its mechanism.
- **Projection change** → only with a named mechanism (minutes, role, health, age,
  system — PROMPT.md §4.4), and any ±20% swing gets its mechanism sentence in the
  after-report. Label direction vs magnitude honestly ([LIKELY] direction,
  [SPECULATIVE] magnitude is a normal label).

## 4. Rebuild and diff (computed, never eyeballed)

```
python3 report/check_provenance.py        # must pass before ranking
python3 report/rank_engine.py             # regenerates top-200-2026-27.md
```

Then diff `/tmp/top-200-baseline.md` against the new board **with a script**:
entries/exits from the top 200, and every move of ≥3 ranks with old → new. If the
engine's hard-coded header caveats are contradicted by a change you made (e.g. a
player it says is excluded now has a row), fix the header text in `rank_engine.py`
in the same pull — the board must not contradict itself.

## 5. After-report — required every pull, short by design

Write `report/after-reports/after-report-YYYY-MM-DD.md` with exactly these
sections (a quiet day yields a ~10-line file; that is a valid report):

1. **Header** — pull date, window, gate status (`check_provenance` output line).
2. **NBA Roster Changes** — every transaction applied, one row each: player,
   change, date, source link(s). If none: "No roster changes in window — sweep
   ran, sources checked: <list the feeds/searches>." Never write "no changes"
   without having run the sweep.
3. **Significant Fantasy Analysis Changes** — projection edits with mechanisms
   and labels; board movement from the §4 diff (entries/exits, moves ≥3); anything
   that changes draft strategy (punt fits, tier breaks). If none: "Board
   unchanged (diff ran clean)."
4. **Watchlist / open items** — flagged-not-edited situations, CANNOT VERIFY
   items, and unresolved stories to re-check next pull. The next pull reads this
   section (§2).
5. **Open-item receipts** (fix F1, 2026-09-08) — one table row per name the
   deck plane's `judgment_open_items.py` flags: player → query run → dated
   finding. `judgment_open_items.py --check-report` must pass against this
   file. A quiet finding is a valid receipt; a missing row is not.

## 6. Log, commit, push

Append one row to `report/pull-log.md`:

```
| date | window | rows edited | added | removed | after-report |
|---|---|---|---|---|---|
| YYYY-MM-DD | MM-DD → MM-DD | N | N | N | after-reports/after-report-YYYY-MM-DD.md |
```

Commit everything from §3-§6 in one commit:
`Data pull YYYY-MM-DD: <one-line summary, or "no changes — verified quiet">`
Push, then run `git log origin/main -1` and confirm the SHA. Report the SHA in
your final message. Quiet days still commit — the pull-log row and after-report
ARE the record that the check happened; without them the next pull cannot date
its window and staleness becomes invisible again.

## 7. Deck sync + republish (the other data plane)

The published **Draft Deck** artifact renders from `yahoo-fantasy-basketball`'s
`data/players.csv` (the deck pool, `scripts/hoops.py` math), NOT from
this repo's CSVs. The two planes share news, not files — a pull that updates
only this repo leaves the deck lying about freshness. After §6:

1. In `yahoo-fantasy-basketball`: apply the window's news to
   `data/players.csv` under its laws — role-reprice for new-team roles,
   pool-completeness (`MUST_HAVE`), availability tags (`out-*` / `recovery` /
   `risk`), players who leave the NBA leave the pool. Update the
   `data/rosters_official.json` evidence entries for every placement you
   changed (dated sources).
2. `python3 scripts/verify_rosters.py` — zero mismatches, dated today.
3. `python3 scripts/hoops.py freshness --stamp --note "<window summary>"`.
4. Re-author the deck's `JUDGMENT` layer (in `docs/draft-deck.html`) from this
   window's research — date it today; stale rationales are defects.
   **Authoring contract (2026-09-08):** a card describing an OPEN situation
   must include at least one marker phrase from `judgment_open_items.py`'s
   lexicon — the enumerator is lexicon-based, and on its first run the
   freshly re-authored Kawhi and Mathurin cards both silently dropped off
   the flagged list because their new phrasing evaded it. Re-run the script
   after re-authoring and confirm every still-open situation is flagged.
   Also rewrite the colophon's "Data." paragraph for this window —
   `build_deck.py` gate 6 (fix F4/D-S6) refuses a build whose colophon
   contradicts the pool count or narrates the wrong pull.
5. `python3 scripts/build_deck.py` — all gates must pass; never hand-edit the
   injection anchors.
6. Republish `docs/draft-deck.html` to the **existing** artifact URL (do not
   mint a new one) and confirm the page header reads "fresh today".
7. Commit and push (that repo's branch/PR rules apply).

## 8. Failure modes

- Web access unavailable → stop and say so. No pull from memory.
- A source conflicts with the repo → the fresher sourced fact wins; flag the
  discrepancy in the after-report.
- Gate fails → fix the provenance/CSV pairing; never ship with `--allow-stale`.
- Anything surprising (a row that shouldn't exist, a diff you can't explain) →
  stop and diagnose before patching; put the finding in the after-report.
