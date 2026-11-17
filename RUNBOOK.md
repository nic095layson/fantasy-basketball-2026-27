# Runbook: rebuilding the Runner

What to do when the session that carries the daily runs is lost, stuck or has to be replaced. Written 2026-11-17
(`report/after-reports/after-report-2026-11-17-gaps-and-fixes.md`, proposal F3). **This procedure has not been
rehearsed.** It is assembled from the stored prompts, the session records and the scripts as they stood on that date;
the first rebuild should correct it.

## What the Runner is

| part | value on 2026-11-17 |
|---|---|
| Session | one persistent cloud session, "Fantasy kit morning runner (persistent)", with the kit attached and the right to push `season/daily` |
| Morning run | scheduled task `trig_01V43JtVvW6teWGmwt17dPVw`, 4:40 AM Pacific daily, prompt in `report/runner/morning_prompt.txt` |
| Afternoon run | scheduled task `trig_015cHK6ECUvXA9TX1UNTT53r`, 3:00 PM Pacific daily, prompt in `report/runner/afternoon_prompt.txt` |
| Records | branch `season/daily`, draft pull request "Season: daily records" (never merged) |
| Page | the Season Deck, published by both runs to the address named in the prompts |
| Watchdogs | two fresh-session tasks, "Fantasy kit run watch: morning" (6:30 AM Pacific) and "afternoon" (3:45 PM Pacific); they run `scripts/run_watch.py` against `season/daily` and alert on a missing or failed run |

What it needs to work:
- the kit checkout with push rights to `season/daily`; the deck is cloned publicly beside it by the prompt's own step 1c;
- the Yahoo connector (Flaim), and FantasyBot as the fallback, connected on the account;
- the governance plugin: both prompts load plan-gate and adversarial-verify, and the turn gates stop a run that does not;
- the right to publish to the deck page.

Why a new session can take over without the old one's history: the scripts read the day's Yahoo responses from the
running session's own transcript, and only entries stamped at or after the run's start time (`--since <T0>`,
`scripts/flaim_live.py`, `scripts/league_live.py`). Every other input is a file on `season/daily`.

## Signs it is broken

- A run-watch alert, or no `report/briefs/morning_<date>.json` on `season/daily` by about 6:30 AM Pacific.
- The scheduled task's last run is not SUCCEEDED (the task list shows it). For a task bound to a session this says the
  message was delivered, not that the run finished: read the day's report on the branch.
- The session's context is close to its limit. On 2026-11-16 it stood at 775,056 of 1,000,000 tokens and was compacted
  automatically to about 300,000 overnight; the 2026-11-17 run passed, 24 steps. One run is the only evidence so far.

## Rebuild, in order

1. **Do not delete anything first.** Disable the two scheduled tasks (enabled off). Their prompts and history stay.
2. Create a new cloud session with the kit attached and `season/daily` as the branch it may push. Name it so it reads
   as the Runner.
3. In the new session, before any run: check that the governance plugin is present and its self-test passes (the
   handoff prompt of 2026-11-16, section 1, lists the five checks), and that the Flaim tools load (`get_user_session`
   shows the league ANTI MARTIN MARTIN CLUB, id `478.l.36464`). Never call `refresh_leagues`.
4. Create two scheduled tasks bound to the new session, with the schedules above and the prompts from
   `report/runner/`, word for word. Compare each stored prompt with its file (`sha256sum`).
5. Let the next scheduled run fire, or fire the afternoon task once by hand (it is the lighter one: rosters, status,
   deck). Read its report on `season/daily` and the run watch's line.
6. When one morning and one afternoon run have passed, delete the old scheduled tasks. Only the owner archives the old
   session.
7. Record the rebuild in `report/corrections-log.md` if it was caused by a statement that proved wrong, and update the
   ids in this file and in `report/runner/README.md`.

## What only the owner does

Merging anything, archiving a session, and any change to a stored prompt (made from the Runner's own conversation).
No session pushes to `season/daily` except the Runner, or another session on the owner's word.

## Cost and size, for the record

Usage on the Runner session from 2026-10-21 to 2026-11-17: about $660 as the session record meters it (not checked
against a bill). The Monday review can carry this figure forward.
