# Prompt for the main session: the afternoon deck record names its own page

Paste everything below the line into the main session.

---

**Build order from David (owner pick 2026-11-05, decision A option 1 of `after-report-2026-11-05-runner-window.md`): put the phase in the Season Deck record's `out` path, so that an afternoon build's `deck_record_<date>_pm.json` names `report/season/deck_<date>_pm.html`. Add a test.**

Read first, on season/daily: `report/after-reports/after-report-2026-11-05-runner-window.md` (Finding 3 and the owner's picks at the bottom).

Governance: load plan-gate before your first edit and adversarial-verify before you report. Show David the compact plan (Goal · Method / parameters · Done when · If it breaks) before building. Build on a claude/ branch off main and open a PR. Do not merge it, and do not touch season/daily.

## The defect (EVIDENCE, code at season/daily 4232453, the same as main 6b30551 for these files)

- `scripts/season_deck.py:333`, inside `build(paths, date, phase=None)`:
  `record = dict(date=date, out=f"report/season/deck_{date}.html", …`. The phase is not in the path.
- The page and the record file themselves are named correctly in `main()`:
  - `:1225` `sfx = "_pm" if a.phase == "pm" else ""`
  - `:1235` `op = … f"deck_{a.date}{sfx}.html"`
  - `:1246` `rp = … f"deck_record_{a.date}{sfx}.json"`
- **Known answers.** All 8 afternoon records on season/daily (`deck_record_2026-10-29_pm.json` through `deck_record_2026-11-05_pm.json`) name the morning page; checked 2026-11-05, 8 of 8. Two examples:

  | Record | `out` today | `out` after the fix |
  |---|---|---|
  | `report/season/deck_record_2026-11-04_pm.json` | `report/season/deck_2026-11-04.html` | `report/season/deck_2026-11-04_pm.html` |
  | `report/season/deck_record_2026-11-05_pm.json` | `report/season/deck_2026-11-05.html` | `report/season/deck_2026-11-05_pm.html` |
  | any morning record | `report/season/deck_<date>.html` | unchanged |

## What to build

1. In `build()`, derive `out` from the phase that `build()` already receives (`phase == "pm"` → `_pm`). Keep the morning path byte-identical.
2. A test in `scripts/test_season_deck.py`. The afternoon build test near `:1485` already asserts that `deck_record_2026-10-21_pm.json` exists; extend it, or add a sibling, so it asserts that file's `out` ends with `deck_2026-10-21_pm.html`. Red first: show it fails on the current code.
3. Assert the morning record's `out` is unchanged (`deck_<date>.html`), for example in the test that reads `deck_record_2026-10-21.json` near `:430`.
4. Do not rewrite the 8 committed afternoon records on season/daily. They stay as they were written; the fix applies from the next afternoon run.

## Two adjacent observations. Flag them to David; do not build them without his word

- **The page footer has the same mislabel (EVIDENCE).** `season_deck.py:1211` builds the footer text `"Record: report/season/deck_record_"+D.date+".json"`, so an afternoon page points readers to the morning record. Same defect class, but on the page rather than in the record, and outside the pick as worded. Ask David whether it rides this PR.
- **The replay gate counts afternoon records as mornings (EVIDENCE for the mechanism and the listing; the gate itself not run).**
  - `scripts/gates.py:178` feeds `report/season/deck_record_*.json` to `independent_audit/replay_gate.py`.
  - `replay_gate.py:30` takes the first `YYYY-MM-DD` in the filename. `replay_deck.sh` then rebuilds that date's *morning* deck with no `--phase`.
  - The last 3 records by basename at 4232453 are `deck_record_2026-11-04_pm.json`, `deck_record_2026-11-05.json`, `deck_record_2026-11-05_pm.json`. So `--last 3` replays 2 distinct mornings (11-04, 11-05), with 11-05 twice, and never an afternoon build.
  - Report it to David as a finding with options. Do not change the gate under this order.

## Done when

- The new test fails on the old code and passes with the fix (red-first output shown).
- The full `scripts/test_season_deck.py` suite passes, plus the repo's usual gates (`python3 scripts/gates.py` as main runs it before a PR).
- A morning build's record is byte-identical to before for the same inputs. An afternoon build's record differs only in `out`.
- The PR is open and unmerged, with an after-report in `report/after-reports/`.

## If it breaks

- If `build()` is called somewhere with a phase that `main()` does not pass (another caller, a replay path), stop and report the call site rather than guessing the phase.
- If a reader of `out` turns up that relies on the morning path, name it and ask before changing behaviour. A grep at 4232453 found none outside `season_deck.py`.

## Report back

One bold outcome line, then:
- a before→after table of `out` for a morning and an afternoon build
- the red-first test output and the suite result
- the PR link
- David's answer, or your question to him, on each of the two adjacent observations

Commits use the neutral label "Claude (session model A)". No model names.
