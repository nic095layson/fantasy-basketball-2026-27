# The Runner's stored prompts (copies)

The two daily runs are scheduled tasks bound to one persistent session. Their prompts live in the scheduler, not in this
repository; these files are word-for-word copies, kept so a prompt can be read, compared and restored. **The scheduler's
copy is the live one.** A prompt is edited only from the Runner's own conversation, on the owner's word; when one is,
copy it here again in the same pull request or the next, with its new `updated_at`.

| file | scheduled task | schedule | scheduler `updated_at` | sha256 of the file |
|---|---|---|---|---|
| `morning_prompt.txt` | Fantasy kit morning run (persistent runner, can push), `trig_01V43JtVvW6teWGmwt17dPVw` | `CRON_TZ=America/Los_Angeles 40 4 * * *` | 2026-11-17T22:12:25Z | `5f0553d0d623abe92e5e66ab9927ffe683ebc3e140a8a89471d652270ddba4ea` |
| `afternoon_prompt.txt` | Fantasy kit afternoon roster + status check (persistent runner), `trig_015cHK6ECUvXA9TX1UNTT53r` | `CRON_TZ=America/Los_Angeles 0 15 * * *` | 2026-11-05T23:43:16Z | `f7186373b80423061310f5d9f6da57060989e6c5ad579d5c51280e338f6b8cea` |

Copied 2026-11-17 from the scheduler's own record (`get_trigger`), extracted mechanically from the copying session's
transcript, never retyped. Each file is the prompt followed by one newline. Check a copy with `sha256sum report/runner/*.txt`.

Refreshed 2026-11-23 (owner, Monday list; Council 4-1): the morning copy now matches the scheduler's record of that
day (`updated_at` 2026-11-17T22:12:25Z), extracted mechanically from the copying session's `get_trigger` result. The
only change from the 2026-11-17 copy is the owner's own edit of 2026-11-17: the minutes line is described as the
minutes ratios applied to points, rebounds and assists in the live season lines, and its step line is quoted as printed.
The afternoon copy is unchanged (scheduler `updated_at` 2026-11-05T23:43:16Z).
