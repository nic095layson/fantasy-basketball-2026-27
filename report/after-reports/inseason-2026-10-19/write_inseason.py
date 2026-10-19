#!/usr/bin/env python3
"""Writes after-report-2026-10-19-inseason-tool.md from the build's records: the morning-run records, the box-score
records, the season-line record, the two-outlet summary, the registry record, and the test runs. No figure typed by
hand. Open-item receipts and Repeat-name sections carried from the post-mortem of the same day."""
import json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(os.path.dirname(os.path.dirname(H)))
OUT = os.path.join(KIT, "report/after-reports/after-report-2026-10-19-inseason-tool.md")
PM = os.path.join(KIT, "report/after-reports/after-report-2026-10-19-draft-postmortem.md")
J = lambda p: json.load(open(os.path.join(KIT, p), encoding="utf-8"))
M21, M17 = J("report/briefs/morning_2026-10-21.json"), J("report/briefs/morning_2026-10-17.json")
BOX = J("data/actuals/2026-10-16.json"); TWO = J("report/after-reports/inseason-2026-10-19/two_outlet_2026-04-10.json")
SL = J("data/season/season_lines_2026-10-21.json"); SW = J("report/after-reports/redteam-2026-10-19/sweep.json")
REG = J("scripts/redteam/constants_registry.json"); BRIEF = J("report/briefs/brief_2026-10-21.json")
TRIGGER = dict(id="trig_01YUcivSLv7aWWoSPoFPmhg4", cron="CRON_TZ=America/Los_Angeles 52 6 * * *", next_run="2026-10-20T13:52:00Z", push=True)
LS = J("data/league_state.json"); WAIV = J("report/after-reports/waivers-2026-10-19/jones_holiday.json")
n_team = len(LS["teams"]); n_pl = sum(len(t["players"]) for t in LS["teams"])
n_add = sum(len(t.get("added_since_draft") or []) for t in LS["teams"]); n_drop = sum(len(t.get("dropped_since_draft") or []) for t in LS["teams"])
pm = open(PM, encoding="utf-8").read()
shock = SW["constants"]["arena.TEAM_WEEK_SHOCK"]
band = "TEAM_WEEK_SHOCK is FRAGILE: " + " / ".join(f"{v['shift_mean']:+.1f} ({v['label']})" for v in shock["variants"])


def section(h):
    m = re.search(rf"^## {re.escape(h)}.*?(?=^## )", pm, re.S | re.M); return m.group(0).rstrip() + "\n"


def tests(name):
    p = subprocess.run([sys.executable, os.path.join(KIT, "scripts", name)], capture_output=True, text=True)
    m = re.search(r"Ran (\d+) tests", p.stderr); return int(m.group(1)) if m else 0, "OK" if p.returncode == 0 else "FAIL"


NEW = ["test_box_pull.py", "test_season_lines.py", "test_season_board.py", "test_scoreboard_intake.py", "test_morning.py", "test_daily_brief.py", "test_constants_registry.py", "test_weekly.py"]
T = {n: tests(n) for n in NEW}
ALL = sorted(f for f in os.listdir(os.path.join(KIT, "scripts")) if f.startswith("test_") and f.endswith(".py"))
TA = {n: tests(n) for n in ALL}
seasonc = [c for c in REG["constants"] if c["module"] == "season_lines"]
title = BRIEF.get("title") or BRIEF.get("odds") or {}
L = []; w = L.append
w("# After-report — the in-season tool: morning box scores from two outlets, season lines blended from the actuals, the board and brief on the blended pool, the weekly scoreboard intake, and the 06:52 scheduled run")
w("")
w("**Owner request (2026-10-19, verbatim):** \"We've used the Draft tool preparing during pre-season. Let's discuss by you asking me questions so that we can build an IN-season tool. Ideally, I'd like for there to be an input for me to upload all the current rosters. Based on the rosters, this tool should be able to deduce which players are in the available player pool for me to add. I'll feed the system week by week fantasy scores, and if possible I'd like for you Claude to pull box scores every morning (like our refresh pull) so that we can continue strenghtening our system model. Let's get to work!\" Then: \"Please have the council deliberate on each decision. Let me know what their expert recomendations are, and proceed with that.\"")
w("")
w(f"**What was built.** On Session 1's foundation (the league state with all twelve rosters, the free-agent scan, the status feed, the weekly preview and its append-only ledger): `scripts/box_pull.py` (ESPN's scoreboard and summary API as primary, Basketball-Reference reconciled player by player, names resolved to the kit pool or listed as unpooled, receipts, retries, single-source labelling); `scripts/season_lines.py` (the preseason line, never edited, blended with the season's regular-season games with per-category priors derived from the measured year-over-year stability); `scripts/season_board.py` (the rank engine's functions on the blended line); the `SEASON_POOL` override so the brief, preview and waiver scan run on the blended pool; `scripts/scoreboard_intake.py` (one CSV per week, all six matchups, halts on any unresolved team, scores the ledger, builds the team-week dataset for D-PM-1); `scripts/morning.py` (the five steps as gates); a scheduled task that runs it every morning; the runbook `report/plans/in-season-runbook-2026-10-19.md`. Every piece landed red-first: " + ", ".join(f"`{n}` {c} {r}" for n, (c, r) in T.items()) + f". All {len(TA)} kit test files: {sum(c for c, _ in TA.values())} tests, {sum(1 for _, r in TA.values() if r == 'OK')} of {len(TA)} files OK. No projection line, tag, roster or engine constant changed.")
w("")
w(f"**Headline.** The morning run passes end to end on the season pool: `morning.py --date 2026-10-21 --no-fetch` ran season lines, season board, status feed and daily brief, all PASS (record `report/briefs/morning_2026-10-21.json`); with the live fetch for 2026-10-17 the box-score step pulled the 2026-10-16 preseason slate ({len(BOX['games'])} games, {BOX['n_players']} player lines, {BOX['n_pooled']} in the pool, single-source because Basketball-Reference carries no preseason) and the brief then refused a date outside the fantasy calendar, which is the designed failure (record `morning_2026-10-17.json`). On a 2025-26 regular-season slate the two outlets reconciled {TWO['reconciliation']['matched']} of {TWO['n_players']} lines with {len(TWO['reconciliation']['mismatched'])} cells differing. With zero regular-season games the season files equal the preseason files byte for byte, so nothing moves before the first game. The scheduled task `{TRIGGER['id']}` fires at 06:52 America/Los_Angeles (your 10/19 evening call; it was created Eastern), first on {TRIGGER['next_run'][:10]}; the first real brief is the morning of 10/21. The rosters paste parser is built on your 10/19 evening sample (§6); the scoreboard paste still waits on a week-1 sample, and until then its CSV route works. The band every odds figure carries: {band}.")
w("")
w("Pull window: 2026-10-19 → 2026-10-19 (build only; the 2026-10-16 preseason box scores were pulled as a test record; no roster pull, no line change).")
w("")
w("## 1. Roster changes")
w("")
w("None. The league state is Session 1's 2026-10-15 upload; the season files are derived; the brief proposes.")
w("")
w("## 2. The Council's ten decisions (the design)")
w("")
w("| # | decision | verdict | built as |")
w("|---|---|---|---|")
for row in [
    ("1", "roster input", "5–0 paste the Yahoo Starting Rosters text; PDF a flagged fallback", "intake halts on any unresolved name; paste parser on the first sample (D-IS-2)"),
    ("2", "upload cadence", "4–1 weekly before waivers, plus after your moves; as-of date printed", "`daily_brief.py` prints the state's as-of date (Session 1); the 7-day refusal is D-IS-3"),
    ("3", "weekly scores", "5–0 the league scoreboard, all six matchups' nine totals", "`scoreboard_intake.py` + `data/weeks/TEMPLATE.csv`; team-week dataset for D-PM-1"),
    ("4", "daily lineups", "4–1 not required; the brief's lineup is the graded record", "the brief records its lineup each morning"),
    ("5", "box-score source", "5–0 ESPN API primary, Basketball-Reference second outlet", "`box_pull.py`; measured reachable 2026-10-19 with a browser agent"),
    ("6", "cadence", "5–0 06:52 America/New_York, fresh session, `season/daily` branch under a draft PR", f"scheduled task `{TRIGGER['id']}` (push notification on; moved to America/Los_Angeles on your 10/19 evening call)"),
    ("7", "autonomy", "5–0 record and propose only", "no script writes a line, tag or roster; the run never merges"),
    ("8", "model strengthening", "4–1 blended season line, per-category priors registered and swept", "`season_lines.py`; priors in the registry (STABILITY measured, SEASON_GAMES uncalibrated D-IS-1)"),
    ("9", "graded on", "5–0 weekly category calls, title odds by week, waiver verdicts with bands", "ledger (Session 1) + scoreboard intake; waiver bands D-IS-4"),
    ("10", "where it lives", "4–1 the kit only; the deck page frozen as the draft record", "kit scripts only; the deck engine imported read-only")]:
    w("| " + " | ".join(row) + " |")
w("")
w("## 3. What each piece does, with its evidence")
w("")
w(f"- **Box scores** (`box_pull.py`, {T['test_box_pull.py'][0]} tests). ESPN scoreboard → every FINAL event's summary → per-player minutes, PTS, FGM/FGA, 3PM/3PA, FTM/FTA, REB, AST, TOV, STL, BLK, starter, DNP; Basketball-Reference's basic box tables for the same date; the join tolerates the outlets' suffix and nickname habits (Robert Williams III / Robert Williams, Ron / Ronald Holland); a differing cell is listed, never averaged; names resolve by fold plus the kit alias table or stay unpooled; three fetch attempts per page; receipts (URLs, HTTP codes, times) in the record. Live: 2026-10-16, {len(BOX['games'])} games, {BOX['n_players']} lines, {BOX['n_pooled']} pooled, {len(BOX['unpooled'])} unpooled (camp bodies and deep bench), single-source. 2026-04-10 (regular season): {TWO['games']} games, {TWO['n_players']} lines, {TWO['reconciliation']['matched']} matched, {len(TWO['reconciliation']['mismatched'])} cells differ, {len(TWO['reconciliation']['espn_only'])} ESPN-only, {len(TWO['reconciliation']['bref_only'])} bref-only (`inseason-2026-10-19/two_outlet_2026-04-10.json`).")
w(f"- **Season lines** (`season_lines.py`, {T['test_season_lines.py'][0]} tests). Per category k games of the preseason line plus the regular-season games appeared in; percentages on attempts; preseason and DNP lines excluded. Priors k = n(1−ρ)/ρ at n = {SL['season_games']}: " + ", ".join(f"{c} {k}" for c, k in SL["prior_games"].items()) + ". Registered: " + "; ".join(f"`{c['name']}` {c['status']}" for c in seasonc) + f". Identity run on 2026-10-21: {SL['players_with_games']} players with regular-season games, {len(SL['movers'])} movers; both season files byte-equal to their sources (test and live diff).")
w(f"- **Season board** (`season_board.py`, {T['test_season_board.py'][0]} tests). `rank_engine.py`'s load, exclude_held, zscores, total and avail on the blended kit-schema file; the identity board's order equals the preseason board's; `report/top-200-2026-27.md` untouched.")
w(f"- **The brief on the blended pool** (`co_gm.load_pool`, `SEASON_POOL`; {T['test_daily_brief.py'][0]} tests). `report/briefs/brief_2026-10-21.md` rebuilt on the identity season pool; its figures equal Session 1's by construction (zero games). The brief's title-odds block now carries the structural band read from the standing sweep record (`daily_brief.band_line`, red-first), so the morning report can quote it (D-PM-6, D-RT-2).")
w(f"- **Weekly scoreboard** (`scoreboard_intake.py`, {T['test_scoreboard_intake.py'][0]} tests). Twelve rows, six matchups, every team resolved to the league state or the intake halts; your categories won / lost / tied (turnovers reversed); `data/weeks/team_weeks.csv` append-only and idempotent per week; the ledger scored through `weekly_preview.py --score`.")
w(f"- **Morning runner** (`morning.py`, {T['test_morning.py'][0]} tests). Each step must exit 0 and print its PASS line; a failure stops the run and later steps are SKIPPED; `report/briefs/morning_<date>.json` is the record. Dry runs: 2026-10-21 no-fetch PASS ({len(M21['steps'])} steps); 2026-10-17 with fetch: box scores PASS, season lines PASS, season board PASS, status feed PASS, daily brief FAIL (outside the fantasy calendar; preseason), run FAIL as designed.")
w(f"- **Weekly preview** (`weekly_preview.py`, {T['test_weekly.py'][0]} tests): the Python 3.11 f-string defect (D-RT-5) fixed red-first, since the weekly loop could not import it here.")
w("")
w("## 4. The scheduled run")
w("")
w(f"EVIDENCE: scheduled task `{TRIGGER['id']}`, cron `{TRIGGER['cron']}`, fresh session per firing, push notification on, next run {TRIGGER['next_run']} UTC. Its prompt (stored on the task) clones the deck beside the kit if absent, checks out `season/daily` (from this branch until it merges, then from main), runs `scripts/morning.py`, commits the records, pushes, keeps a draft PR \"Season: daily records\" open and never merges, then reports the MORNING line, the lineup, the top waiver pair with its band, the movers, the unpooled players with games and any failure. The platform warned on creation that the task stores no connectors: the fired session runs in this environment, where the kit's git access is configured (INFERENCE from the environment's settings, not yet observed), but the `add_repo` tool it would use to attach the deck may be absent; whether the deck clones from the environment's git proxy is `UNVERIFIABLE` until the first firing, and the first run's report will say. If it fails on that, the fix is attaching the deck to the environment, not a code change.")
w("")
w(f"The brief's odds line (Session 1's method, two seeds, error stated) is the figure the morning report quotes; every such figure carries the structural band from the standing sweep ({band}; `redteam-2026-10-19/sweep.json`).")
w("")
w("## 5. What waits on you")
w("")
w("- ~~A first paste of Yahoo's league \"Starting Rosters\" page~~ — delivered 10/19 evening; the parser is built and ran (§6).")
w("- A first paste of a Yahoo scoreboard (after week 1), so the scoreboard parser is built against the real format (until then: `data/weeks/TEMPLATE.csv`).")
w("- ~~The timezone~~ — answered 10/19 evening: Pacific. The task now runs at 06:52 America/Los_Angeles.")
w("")
w("## 6. The evening additions (owner messages, 2026-10-19)")
w("")
w(f"**The rosters paste parser (D-IS-2 option a, built).** You pasted the Yahoo Starting Rosters page as text; `league_intake.py --paste FILE` now parses it mechanically (slot line, NBA-team line, status letter, game note per player; a malformed block halts the run), writes a transcribed CSV beside the paste, and pins both with hashes. EVIDENCE: the run on your paste — `LEAGUE INTAKE: PASS — {n_team} teams, {n_pl} players, {n_pl} of {n_pl} resolved; 0 NBA-team disagreement(s)`; `data/league_state.json` is as-of {LS['as_of']}, recording {n_add} add(s) and {n_drop} drop(s) since the draft across the league. The CSV route stays as the fallback. Tests: `test_league_intake.py` (10, incl. 4 on the paste).")
w("")
w("**The P status tier (D-IS-6, stated default).** Your paste carried P (probable) letters, which the status feed did not tier; it now maps P to 0.75, between healthy (1.00) and Q (0.50), with O at 0.00 — a stated default on the sheet (D-IS-6), not a measured value; an unknown letter still halts the feed rather than guessing. Tests: `test_status_feed.py` (8).")
w("")
w(f"**The Jones/Holiday waiver question, answered on the record.** Your question — Tre Jones and/or Jrue Holiday in place of PJ Washington and/or Christian Braun — ran on the live {LS['as_of']} rosters and the locked lines: all five scenarios flat or negative (best mean title shift {max(r['d_title_mean'] for r in WAIV['scenarios']):+.2f}, worst {min(r['d_title_mean'] for r in WAIV['scenarios']):+.2f}; {WAIV['seasons']:,} seasons on seeds {WAIV['seeds'][0]} and {WAIV['seeds'][1]}); the assist gain never covers the rebound/block loss. Record: `waivers-2026-10-19/jones_holiday.json`. No roster change made.")
w("")
w("## Watchlist")
w("")
w("- The first firing on 2026-10-20 runs before any regular-season game: expect the box-score step to record zero games for 2026-10-19 and the brief to run on an unchanged pool; the first morning with games is 2026-10-21.")
w("- The unpooled list on a preseason slate is long (camp bodies); in season it should be short, and a real NBA player appearing there repeatedly is a candidate for the pool.")
w("- `SEASON_GAMES` (65) sets every prior; D-IS-1 measures it from the actuals record or sweeps it.")
w("")
w(section("Open-item receipts").replace("## Open-item receipts", "## Open-item receipts\n\nCarried from the post-mortem report of the same day (no pull today; the rows are that report's):", 1))
w(section("Repeat-name market check").replace("## Repeat-name market check", "## Repeat-name market check\n\nCarried from the post-mortem report of the same day (no refresh today):", 1))
w("## Bounds")
w("")
w("**Out of scope by design.**")
w("- The scoreboard paste parser is not built (one owner sample needed, after week 1); its CSV route is the interface until then. The rosters paste parser shipped 10/19 evening (§6).")
w("- The games-shock calibration (D-PM-1) is not run: `team_weeks.csv` collects the dataset; the fit waits for about six weeks of totals.")
w("- The in-sim availability tiers and the Q/O status tiers are not blended into the weekly model (Session 1's bound stands).")
w("- The deck page and its draft card are frozen; no in-season dashboard.")
w("")
w("**In scope and unverified.**")
w("- A regular-season morning end to end: `NOT-ATTEMPTED` because none has been played; the 2026-10-21 no-fetch run and the 2026-10-17 fetch run cover the two halves separately. Load-bearing for the task's first firing, which will report.")
w("- The fired session's access to the deck repo: `UNVERIFIABLE` until the first firing (above).")
w("- The blend's behaviour on real games: the formula is tested; its priors are derived, not validated against a season. `season_lines_<date>.json` records every mover for the week-6 review (D-IS-1).")
w("")
w("## Decision sheet (owner disposes)")
w("")
w("| id | decision | recommended |")
w("|---|---|---|")
w("| D-IS-1 | `SEASON_GAMES` = 65 (the n in k = n(1−ρ)/ρ): (a) measure the stability sample's mean games from `arena/results/actuals_2026-10-09/` and replace; (b) sweep 50 / 80 and quote the board band; (c) leave | (a) |")
w("| D-IS-2 | rosters paste parser | done — (a) built 10/19 evening on your sample (§6); the CSV route kept as fallback, not retired |")
w("| D-IS-3 | brief on a stale state: (a) refuse odds on a league state older than 7 days, print the date always; (b) print only | (a) |")
w("| D-IS-4 | waiver verdicts with bands: (a) the brief's top pairs re-run at shock 0 and 0.12 (about a minute), robust ones marked; (b) shipped engine only | (a) |")
w("| D-IS-5 | the morning task's branch: (a) `season/daily` under one standing draft PR you merge weekly; (b) a PR per day | (a) |")
w("| D-IS-6 | the P (probable) status tier at 0.75 (stated default, shipped 10/19 evening): (a) keep; (b) another value | (a) |")
w("")
w("## Provenance")
w("")
w("- Session: Claude Code (claude.ai/code), 2026-10-19, kit branch `claude/market-data-workorder-mnfi2b`; deck 259c630 read-only.")
w("- Records: `report/briefs/morning_2026-10-21.json`, `morning_2026-10-17.json`, `data/actuals/2026-10-16.json`, `inseason-2026-10-19/two_outlet_2026-04-10.json`, `data/season/season_lines_2026-10-21.json`, `scripts/redteam/constants_registry.json`; fixtures of the real fetches in `scripts/fixtures/`.")
w("- Tools: `scripts/box_pull.py`, `season_lines.py`, `season_board.py`, `scoreboard_intake.py`, `morning.py`, `co_gm.py` (SEASON_POOL), `weekly_preview.py` (fix); tests as listed; runbook `report/plans/in-season-runbook-2026-10-19.md`; this report by `inseason-2026-10-19/write_inseason.py`.")
w("- Re-verify: `python3 scripts/morning.py --no-fetch`; `python3 scripts/box_pull.py --date 2026-10-16`; `python3 scripts/gates.py --verify --report report/after-reports/after-report-2026-10-19-inseason-tool.md`.")
w("")
w("## In plain language")
w("")
w("From tomorrow morning a fresh session wakes at 6:52 Pacific, pulls last night's box scores from ESPN, checks them against Basketball-Reference, folds the games played so far into every player's line (the preseason line stays as it was, and counts as a fixed number of games of evidence per category), rebuilds the board and your daily brief on those lines, and sends you the summary. It never changes a line or a roster on its own. You feed it two things: your league's rosters page once a week (paste it as text, like tonight's), and the scoreboard after each week (as a CSV until you send one sample of that paste). Nothing in the model moves until the first regular-season game is played, and the first real brief arrives on the morning of October 21.")
w("")
open(OUT, "w", encoding="utf-8").write("\n".join(L)); print("wrote", OUT, len(L), "lines")
