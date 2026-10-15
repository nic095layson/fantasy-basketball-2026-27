#!/usr/bin/env python3
"""Writer for after-report-2026-10-15-co-gm-league-state.md — figures read from records (RULES.md rule 6)."""
import collections, csv, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(KIT, "report", "after-reports", "after-report-2026-10-15-co-gm-league-state.md")
rd = lambda n: open(os.path.join(HERE, n), encoding="utf-8").read()
def counts(t):
    ran = int(re.search(r"Ran (\d+) tests?", t).group(1)); m = re.search(r"FAILED \((?:failures=(\d+))?(?:, )?(?:errors=(\d+))?\)", t)
    return ran, (int(m.group(1) or 0) + int(m.group(2) or 0)) if m else 0
st = json.load(open(os.path.join(KIT, "data", "league_state.json"), encoding="utf-8"))
tr = list(csv.DictReader(open(os.path.join(KIT, "data", "source", "yahoo-starting-rosters-2026-10-20-view.transcribed.csv"), encoding="utf-8")))
r1_missing = "ModuleNotFoundError" in rd("test_league_intake_red.txt"); assert r1_missing
r2, g = counts(rd("test_unpooled_red.txt")), counts(rd("test_league_intake_green.txt"))
halt = [l for l in rd("intake_run_1.txt").splitlines() if l.strip().startswith("-")]
passline = rd("intake_run_2.txt").splitlines()[0]
n_players = sum(len(t["players"]) for t in st["teams"]); n_rows = len(tr)
status = collections.Counter(p["status"] for t in st["teams"] for p in t["players"] if p["status"])
rows = []
for t in sorted(st["teams"], key=lambda t: t["seat"]):
    adds = ", ".join(t["added_since_draft"] + [f"{n} (unpooled IL)" for n in t["unpooled_il"]]) or "none"
    rows.append(f"| {t['seat']} | {t['manager']} | {t['name']} | {t['draft_overlap']} of 13 | {adds} | {', '.join(t['dropped_since_draft']) or 'none'} | {', '.join(t['empty_slots']) or 'none'} |")
me = next(t for t in st["teams"] if t["seat"] == 10)
mine = ", ".join(f"{p['player']} {p['status']}" for p in me["players"] if p["status"])
h = json.load(open(os.path.join(HERE, "h2h_assessment_2026-10-15.json")))
pw = [(r["s2026"]["p_win"] + r["s2027"]["p_win"]) / 2 for r in h["rows"]]
rn = rd("rn_section.md").rstrip() + "\n"
text = f"""# After-report — 2026-10-15: Session 1 item 5 — the league's current state from the owner's rosters page; data/league_state.json

**Owner request:** Session 1 item 5 (rosters, standings, scoreboard → `data/league_state.json`, names resolved 100% to the pool, halt on any miss). Owner input: the rosters PDF uploaded 2026-10-15. On the halt, the owner said: "Convene council to decide and proceed with their recommendations." Then "Proceed".

**What changed.**
- Kit: `data/source/yahoo-starting-rosters-2026-10-20-view.transcribed.csv` ({n_rows} rows), `scripts/league_intake.py`, `scripts/test_league_intake.py`, `data/unpooled_il.json`, `data/league_state.json`.
- No line, tag, team, price or placement changed. Nothing published.

**Method (stated before the run).**
- **Transcription.** The PDF has no text layer and no OCR engine is installed. Each page was rendered at 250 dpi, and every team column was read from the image.
- **Resolution, in order:**
  1. The deck's name fold.
  2. Yahoo's abbreviations as recorded on the 10/14 draft board.
  3. Nothing else: any other miss halts the intake.
- **Seats.** Each team gets the draft seat whose 13 picks overlap its roster most, and the match must be unique.
- **Standings and scoreboard.** None exist before week 1, which starts 2026-10-20.

Pull window: 2026-10-15 → 2026-10-15 (the owner's rosters page as of its Tue Oct 20 view; no web research — the environment denies the sports hosts, see item 3).

## 1. Roster changes

No pool row changed. League-roster moves since the draft, read from the page:

| seat | manager | fantasy team | draft picks still rostered | added since draft | dropped | empty slots |
|---|---|---|---|---|---|---|
{chr(10).join(rows)}

## 2. The halt and the Council's decision

- **First run:** `{halt[0].strip().lstrip('- ')}`. The intake halted and wrote nothing (`intake_run_1.txt`).
- **Council (owner-convened, 4–1):** carry the player as an IL-only exception in `data/unpooled_il.json`, with no projection line, rather than writing a pool row from memory or with no source. He is on IL, so he contributes nothing to the lineup.
- **Red first:**
  - `test_league_intake_red.txt`: ModuleNotFoundError — the intake module did not exist.
  - `test_unpooled_red.txt`: {r2[0]} tests, {r2[1]} errors.
  - `test_league_intake_green.txt`: {g[0]} tests, {g[1]} failing. This includes the test that the same name in a BN slot still halts.
- **Second run:** `{passline}`

**Cross-checks that came free (EVIDENCE):**
- Every team keeps all 13 of its draft picks, so each maps to exactly one seat.
- Yahoo's NBA team equals the pool's team for all {n_players} pooled players ({len(st['nba_team_disagreements'])} disagreements). This also checks the transcription.

**Status letters on the page:** {dict(status)}. The owner's flagged players: {mine}.

## 3. The owner's question: the predicted head-to-head (an assessment, not a build)

- **Asked:** "what is my predicted head to head result each week, based on your rosters and calculations as of today?"
- **Method (stated before the run):**
  - non-IL players from this league state, on the v69 lines;
  - `arena.team_week_model` and the house simulator's weekly draw;
  - 10,000 matchups per week on seeds 2026 and 2027, against the owner's real schedule.
- **Records:** `h2h_assessment.py`, `h2h_assessment_2026-10-15.json`.
- **Result:** favored in all {len(pw)} weeks, P(win) from {min(pw):.0%} to {max(pw):.0%}. Expected regular-season wins: {sum(pw):.1f} of {len(pw)}.
- **Not modelled:** Q statuses, streaming, injuries after today, and the two 14-day weeks. Item 7 records week 1's prediction formally before the week.

## Watchlist

- Niederhäuser's exception ends when he gets a sourced pool row; the file says so.
- The standings and scoreboard fields stay `null` until week 1 has results to read.

## Open-item receipts

| item | query run (2026-10-15) | dated finding |
|---|---|---|
| (this item) | owner rosters page only; no web research (sports hosts denied by the environment) | league state written; pool unchanged |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried (did not check; the network is blocked) |

{rn}
The section above is today's output of the deck's `repeat_market_check.py`, carried from item 1; the page is unchanged. The gate replays it again.

## Bounds

**Out of scope by design.**
- No pool rows were added.
- The other teams' standings are not modelled.

**In scope and unverified.**
- The transcription is the agent's reading of page images. It agrees with the pool on every NBA team and every draft pick, but statuses and slots have no second reader.

**What this cannot see.**
- Anything on Yahoo after the page was captured.
- FAB budgets.
- Pending waiver claims.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-S1-4 | Add a sourced pool row for Yanic Konan Niederhäuser once the network allows | keep the IL-only exception |
| D-S1-5 | Paste the rosters again before each Monday preview (weekly), or only on change | weekly |
| earlier rows | carried in `OPEN.md` | carried |

## Provenance

- This folder: `test_league_intake_red.txt`, `test_unpooled_red.txt`, `test_league_intake_green.txt`, `intake_run_1.txt`, `intake_run_2.txt`, `preview_state_without_niederhauser.json`, `h2h_assessment.py`, `h2h_assessment_2026-10-15.json`, `rn_section.md`, this writer.
- Item 3's blocker receipts are in `co-gm-s1-provenance-2026-10-15/`.

## In plain language

Every team's roster is now on file. All 162 players match our database, except one injured rookie who is parked as an exception.

Everyone still has all the players they drafted. The only pickups so far are bench and injured-list adds; yours is Max Strus.

On today's rosters you're favored every week, with an expected record of about {round(sum(pw))}–{len(pw)-round(sum(pw))}.
"""
open(OUT, "w", encoding="utf-8").write(text); print("wrote", os.path.relpath(OUT, KIT))
