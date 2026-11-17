# The Runner's stored prompts (copies)

The two daily runs are scheduled tasks bound to one persistent session. Their prompts live in the scheduler, not in this
repository; these files are word-for-word copies, kept so a prompt can be read, compared and restored. **The scheduler's
copy is the live one.** A prompt is edited only from the Runner's own conversation, on the owner's word; when one is,
copy it here again in the same pull request or the next, with its new `updated_at`.

| file | scheduled task | schedule | scheduler `updated_at` | sha256 of the file |
|---|---|---|---|---|
| `morning_prompt.txt` | Fantasy kit morning run (persistent runner, can push), `trig_01V43JtVvW6teWGmwt17dPVw` | `CRON_TZ=America/Los_Angeles 40 4 * * *` | 2026-11-13T18:12:39Z | `8d77f41ea462659cdffc0ab45c681992333a5a9e91be633842145391f6c98d88` |
| `afternoon_prompt.txt` | Fantasy kit afternoon roster + status check (persistent runner), `trig_015cHK6ECUvXA9TX1UNTT53r` | `CRON_TZ=America/Los_Angeles 0 15 * * *` | 2026-11-05T23:43:16Z | `f7186373b80423061310f5d9f6da57060989e6c5ad579d5c51280e338f6b8cea` |

Copied 2026-11-17 from the scheduler's own record (`get_trigger`), extracted mechanically from the copying session's
transcript, never retyped. Each file is the prompt followed by one newline. Check a copy with `sha256sum report/runner/*.txt`.

Known stale wording, recorded and not changed here (a prompt edit is the Runner's and the owner's): the morning prompt
calls the minutes line "the minutes-trend CANDIDATE line; nothing live reads it" and tells the report "the minutes line
is a candidate: never present its numbers as the projection". Since kit #274 (2026-11-16) the minutes ratio is applied
to points, rebounds and assists in the live season lines.
