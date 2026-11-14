# After-report — morning prompt v3 (2026-10-27)

**Request (owner, 2026-10-27, RUNNER-ASK-v3.md pasted into the runner session):**

> "update this conversation's morning scheduled task ('Fantasy kit morning run (persistent runner, can push)', trig_01V43JtVvW6teWGmwt17dPVw) so its stored prompt is byte-identical to the attached text (morning_v3.txt). Change the prompt only: not the schedule, not the afternoon task. Then read the task back with get_trigger and confirm the stored prompt equals the file byte for byte (length 14,452 bytes)."

**What changed:** the morning task's stored prompt.

**Method:**
- Checked that the file is 14,452 bytes.
- Checked that main carries #214.
- Read the live prompt with get_trigger and pulled it out of the session transcript by script, not retyped.
- Diffed the live prompt against v2 and against v3.
- Applied the change with update_trigger, prompt field only.
- Read it back and compared with `cmp` and `sha256sum`.
- Afterwards, read the afternoon task fresh and compared it to `pm_new.txt`.

**Headline:**
- The stored morning prompt is now byte-identical to `morning_v3.txt`: 14,452 bytes, sha256 `f13041a46de69d5c…`.
- The change was exactly the five edits you listed.
- Schedule, name and enabled state are unchanged.
- The afternoon task is unchanged and still equals `pm_new.txt`.
- The first run on v3 is the morning task's next fire, 2026-10-28T12:01:54Z.

## Actions, in order (EVIDENCE: tool output this session)

| # | Time (UTC) | Action | Result |
|---|---|---|---|
| 1 | ~19:5x | `wc -c morning_v3.txt` | 14452. The file ends without a newline. |
| 2 | — | Checked that origin/main matches what v3 assumes | main head 6ddc2bb is "Merge pull request #214 … availability-fold". `scripts/availability_calibration.py` is absent from main. `scripts/morning.py` on main has the steps "tag outcomes" (l.79), "minutes line" (l.84), "season sweep" (l.105) and "next week forecasts" (l.112). |
| 3 | — | get_trigger on the morning task, then scripted compare | The live prompt was `cmp`-identical to `morning_new_v2.txt` ("live == v2"). The diff against v3 had exactly five hunks: lines 1, 47, 56, 72→72–73 and 74→75. These are your edits 1 (rules: "unattended" sentence), 2 (step 4), 3 (step 6), 4 (step 7, tag outcomes / minutes / sweep / forecasts) and 5 (step 7, Monday accuracy and fit). |
| 4 | 19:53:55.77 | update_trigger, morning task, `prompt` only | Accepted. Cron `CRON_TZ=America/Los_Angeles 0 5 * * *`, `enabled: true` and `next_run_at` 2026-10-28T12:01:54Z are as before. |
| 5 | — | get_trigger, then `cmp` against `morning_v3.txt` | "IDENTICAL". 14452 bytes. sha256 `f13041a46de69d5c…` for both. |
| 6 | 19:55 | get_trigger on the afternoon task, then `cmp` against `pm_new.txt` | "afternoon == pm_new.txt". `updated_at` is still 2026-10-26T19:28:32Z. `enabled: true`. Next run 2026-10-27T22:03Z. |

**Not done:**
- Neither task was fired.
- No change to the afternoon task.
- No repository change other than this report.
- PR #165 was not touched.

## Context from today's run (EVIDENCE)

This morning's run (commit a7d7283, 12:20Z) ran on v2. Its step 4 still called `availability_calibration.py`, which printed:

> AVAILABILITY CALIBRATION: INSUFFICIENT — median team games 3.5 < 15 …

At that time, the runner's local checkout still had the script; #214 merged to main later the same day. From tomorrow the script is gone from main, so under v2 that step would have failed. v3 removes it.

## Bounds

**Out of scope by design:**
- I did not review v3's new step-7 wording beyond the diff.
- I did not check that morning.py's new steps print the exact line prefixes v3 tells the runner to quote ("TAG OUTCOMES", "MINUTES LINE"). Their `pass_re` patterns in morning.py match those names; that is INFERENCE that the printed lines will too.

**In scope and unverified:**
- **Whether tomorrow's run executes v3 cleanly.** NOT-ATTEMPTED, because firing a task was not asked for. The 2026-10-28 run is the first test. Watch for the TAG OUTCOMES and MINUTES LINE step lines in the MORNING block, and for no AVAILABILITY CALIBRATION line.

## Decisions for the owner

None are required. One optional check: after tomorrow's run, confirm its report quotes the TAG OUTCOMES and MINUTES LINE step lines, and that the minutes line is labelled a candidate.

## Provenance

- Runner session `session_01BsJA4wttu98TKVNoh6HBz1`, 2026-10-27.
- Scratch read-backs (not committed; the get_trigger output is the record):
  - `/tmp/claude-0/-home-user-fantasy-basketball-2026-27/f7b74300-8501-5e41-b8c5-d2c75dd06ce4/scratchpad/trig/cur3_trig_01V43JtVvW6teWGmwt17dPVw.txt`
  - `/tmp/claude-0/-home-user-fantasy-basketball-2026-27/f7b74300-8501-5e41-b8c5-d2c75dd06ce4/scratchpad/trig/new3_trig_01V43JtVvW6teWGmwt17dPVw.txt`
- Re-verify with get_trigger on both task IDs, comparing `derived_state.prompt` to `morning_v3.txt` and `pm_new.txt`.
