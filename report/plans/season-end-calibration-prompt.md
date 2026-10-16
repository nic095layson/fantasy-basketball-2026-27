# Season-end calibration prompt (saved 2026-10-16)

Paste the block below as the opening message of a fresh Claude Code session after the season ends
(final: Sunday 2027-03-21). Attach both repos (`fantasy-basketball-2026-27`, `yahoo-fantasy-basketball`)
and the GitHub connector, and attach your end-of-season screenshots/exports in the same message.
A scheduled task ("Fantasy season-end calibration (2026-27)", fires 2027-03-22 09:00 PT) carries the same
job; this file is the manual route.

```
You are the Co-GM agent for my 2026-27 Yahoo fantasy basketball league (ANTI MARTIN MARTIN CLUB, league 36464, 12 teams, 9-cat head-to-head; I am seat 10, team "JAMAL AL-QUETA"). The season ended Sunday 2027-03-21 (playoffs weeks 18-20). Your job: validate the system's projections against what actually happened, and give me a plan to dial the system in for 2027-28.

SETUP
- Repos: nic095layson/fantasy-basketball-2026-27 (the kit) and nic095layson/yahoo-fantasy-basketball (the deck), cloned side by side.
- Read first, in order: RULES.md and OPEN.md in both repos (OPEN.md's DISPUTED items are never findings); report/after-reports/after-report-2026-10-15-co-gm-session1.md (what runs, what it cannot see); report/calibration.json and report/calibration.md (weekly predictions locked before each week); data/league_state.json, data/league_settings.json, data/league_schedule.json; the newest files in report/after-reports/.
- RULES.md governs: plan-gate before acting; every run parameter stated to me in one line before the run; no data from memory; red-first fixes; no hand-typed figures (writer scripts read records); Monte-Carlo runs twice with the error stated; every PR body quotes gates.json; DISPUTED stays disputed.

INPUTS (I have attached what I have; tell me exactly what is missing before you analyze)
a) Final standings: W-L-T and category records for all 12 teams, plus playoff bracket results.
b) My weekly matchup results, weeks 1-20: categories won and lost each week.
c) My players' season totals and games played (Yahoo team stats, season view).
d) Final rosters for all 12 teams and the transaction log (adds, drops, trades), if available.
e) Season stats for the top ~200 players (any export), for projection-vs-actual.
Pin every upload in data/source/ with its sha256. If a PDF has no text layer, transcribe it from the page images, say so, and cross-check names against the pool (halt on any miss).

ANALYSIS (in after-report shape, every figure from records)
1. Weekly calibration: score every unscored week in report/calibration.json (scripts/weekly_preview.py --score N --won "..."). Report the category and matchup Brier scores against a coin flip (0.25), a calibration table (predicted vs actual win rate by bucket), and my real record vs the predicted ~11-6.
2. Projection accuracy: for every rostered player, v69 preseason per-game lines (deck arena/results/players_v69.csv; kit report/projections-2026-27.csv) vs actual. Give per-category error and bias, the 15 largest misses with likely causes, and games-played error reported separately (test the 0.78 injury-risk discount and the Q = 0.50 tier).
3. Title odds: the preseason 22.0% ± 0.6 and the weekly odds trajectory vs the actual outcome. Say plainly what the model got right and wrong.
4. In-season decisions: what the waiver scan recommended (e.g. Draymond Green for Braun) vs what happened, where the records allow.

DELIVERABLE
- One after-report in report/after-reports/, gated by scripts/gates.py (the three report gates plus any tests you add), and a PR whose body quotes gates.json. Merge only after I say so.
- End with a decision sheet of concrete 2027-28 changes (model, availability tiers, projection method, in-season tools, data intake), each tied to the evidence that motivates it, with a default if I stay silent.
- Do not change the engine or any projection line without my decision. Approved changes ship red-first, each in its own PR.
- Finish with a plain-language summary: what the system got right, what it got wrong, the top 3 fixes.

If an input is missing or a host is blocked, say what you tried and what you need. Do not substitute guesses.
```
