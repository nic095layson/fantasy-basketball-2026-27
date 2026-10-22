# De'Andre Hunter's eye tag cleared in the season tools (D-RR-1) — 2026-10-22

Pull window: 2026-10-22 → 2026-10-22. No league or market pull and no web search. The evidence behind the decision is the 10/22 risk-rows pull, pinned in `data/source/hunter-2026-10-22/`.

**Your decisions** (2026-10-22, clicked):
- **02:25Z, D-RR-1:** "Remove it (Recommended)".
- **03:37Z, the route:** "Deck PR + restamp (Recommended)".
- **03:41Z, the route again:** "Kit season override (Recommended)". You chose it after I corrected the deck option: the season tools read the deck's frozen lock file, `players_v69.csv`, not the live deck pool, so a deck change alone would not have reached them.

**What was analyzed.**
- Kit main at `af625a8`, and this branch.
- Deck `048efb6` (main), as the season scripts' sibling.

**Method, stated to you before the run** (03:43Z): the morning pipeline with no fetch, run twice on the same committed league state and the 10/22 box scores, at the brief's own settings (10,000 seasons × seeds 2026 and 2027). One run was on main; the other was main plus this change. A small record script, `hunter-override-2026-10-22/compare.py`, isolates the season pool and Hunter's figures.

**Headline.**
- **The tag is cleared where the season tools read it, and nowhere else.**
  - In the season pool, `data/season/pool_season.csv`, exactly 1 of 336 rows × 15 columns changes: Hunter's note.
  - Its leading tag goes from `inj-eye-risk` to `tag-cleared`.
  - The lock file, the draft page and the kit's own projections are untouched.
- **Today it changes nothing you would see** (measured: `compare.json`, and the two morning runs in §2).
  - Hunter is a free agent. His season value is −4.21, below zero.
  - The deck's rule never discounts a negative value for injury: `adj_value` returns `tv * av if tv > 0 else tv`.
  - So his adjusted value is −4.21 either way. He is free agent 60 of 155 either way, below the waiver shortlist's cut of −3.55.
  - The brief (sha256 6c921a1d8f9a) and the board (9955372e45a1) came out byte-identical before and after.
- **When it would matter.** If his season line rises above zero, the waiver scan prices him at full availability rather than ×0.78. If a team rosters him, the week tools count him at 0.88 of games rather than 0.75. The deck's title-odds simulation would still read the lock file's tag (§3).

## 1. What changed

No projection line, roster or engine constant changed. One tag changed, in the season pool only.

- **`data/tag_overrides.csv`** (new): one row, Hunter, `inj-eye-risk` to `tag-cleared`.
  - Its `decided` cell quotes your two clicks.
  - Its `receipt` cell names the evidence: February retinal repair with full recovery expected (ESPN and NBA.com, 2026-02-21); two preseason games; on neither ESPN's nor Basketball-Reference's injury list on 2026-10-22.
- **`scripts/season_lines.py`.** After the frozen snapshot and the pool additions, each override row replaces one player's leading note tag. The prose after the tag is kept, and a marker naming the file is added.
  - A row is refused, and nothing is written, when the player is not in the pool, when the pool's tag is no longer the one the row expects, when the replacement is not a single tag token, or when its `decided` cell is empty.
  - The day's record lists every override applied, and the PASS line counts them.
- **`scripts/redteam/check_constants.py`.** The registry check flagged the two new module names, `OVERRIDES` (a path) and `OVERRIDE_FIELDS` (a column list), as unregistered judgment constants. They go on its exempt list for the module, beside `ADDITIONS`. Registered constants stay 32 = 32.
- **Test first.** `scripts/test_tag_overrides.py` has 11 tests.
  - The first 10 failed 10 of 10 on main's code (`hunter-override-2026-10-22/red.txt`).
  - The 11th was added by the delivery check: an empty `decided` cell raised `IndexError` instead of the FAIL line. It failed on the first build before its one-line fix.
  - All 11 pass on this branch (`green.txt`).
  - It checks that the deck's own rules read the new tag as healthy: board availability 1.0, weekly 0.88. The old tag read 0.78 and 0.75.
  - The existing `test_season_lines.py` passes 12 of 12.

## 2. What it moves

From `hunter-override-2026-10-22/compare.json`, run twice with identical results. Settings: the 10/22 box scores, the committed `data/league_state.json`, and the brief's own waiver shortlist (`co_gm.free_agents`, top 40 by adjusted value).

| Hunter, season pool | without the override | with it |
|---|---|---|
| leading tag | inj-eye-risk | tag-cleared |
| board availability | 0.78 | 1.0 |
| weekly availability (team-week model) | 0.75 | 0.88 |
| adjusted value | −4.21 | −4.21 |
| free-agent rank | 60 of 155 | 60 of 155 |
| in the waiver shortlist (cut −3.55) | no | no |
| on a roster | no | no |

**The morning run, both ways** (`morning.py --no-fetch`, 2026-10-22): MORNING: PASS, 7 steps, on both.
- The brief and the season board are byte-identical.
- The week-matchup record and the Season Deck differ only in their input pins (the pool file's sha256), the run timestamps and the season-lines record's two new fields.
- The availability calibration reads the same pool, so Hunter's tier there becomes healthy. It changes no value; it is a record.

## 3. What it does not reach

- **The deck's title-odds simulation.** `league_sim.py` loads `players_<tag>.csv` from the deck itself and takes only the tag name from the kit, so it still sees `inj-eye-risk`. It matters only if Hunter is rostered; today he is not. Reaching it would take the full deck chain you set aside (a new lock file, the kit moved to it, the red-team sweep re-run).
- **The draft page and the deck pool** (`data/players.csv`, `docs/draft-deck.html`): untouched, as you chose.
- **The kit's preseason board and season board.** They read the kit plane, where Hunter's games stayed at 70 on 10/22. Byte-identical.

## 4. Errors and surprises, stated plainly

- **My first two route descriptions were wrong.**
  - The deck option said removing the tag on the deck would reach the season tools. It would not have: they read the frozen lock file. I found this before building anything and put the options back to you.
  - The override option said it would reach the title odds. It does not (§3). I corrected that in chat before the build started.
- **The override has no visible effect today**, because Hunter's value is below zero. I found this from the before/after run, not before it. The build is still what you chose, and it starts to matter the day his line or his roster status changes.
- **The delivery check found one unhandled input.** An override with an empty `decided` cell crashed with `IndexError`. It now fails with the named FAIL line, and a test covers it (§1).
- **The first "after" run exited 1 with an empty log.** It was started in parallel with the "before" run. Re-run alone, it passed all 7 steps. I did not find the cause (ATTEMPTED-FAILED: the log was empty and the run wrote no record), so I report it rather than explain it.

## Watchlist

- **Hunter's season line.** If his blended line rises above zero value, the waiver scan will price him at full availability. That is the first point where this change shows.
- **The title-odds simulation** keeps the lock file's tag (§3). If he is rostered, the simulation and the week tools will disagree on his games (0.75 against 0.88). The brief does not say so today.
- **D-PM-4 is untouched:** the board's and the simulator's injury tiers still differ.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| Hunter's tag (D-RR-1; your "Remove it", then "Kit season override") | **BUILT on this draft PR**; merging is yours | §1–§3 |
| older seasons' weekly totals (D-GP-3) | **DONE on draft PR #164**, not merged | `after-report-2026-10-22-flaim-history-totals.md` |
| the runner's stored prompt | **OPEN**: changeable only inside the runner's own conversation; you are doing it there | this session's chat, 03:45Z |

This change touched no pool row of the frozen snapshot. The flagged-name receipts are carried forward from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21 (`after-report-2026-10-21-pickups-file.md` §1). The rest were not re-queried for this change (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this change (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (§1, `roster_drift_2026-10-21.json`) |

## Repeat-name market check

This change did not touch the draft-room deck page: `docs/draft-deck.html` is sha256 6a5cefea4921 at deck 048efb6, the page the GAUNTLET report replayed on 10/21. Its table stands, carried here verbatim.

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 6a5cefea4921), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 33 of 33 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-14.csv`, Hashtag `hashtag-2026-10-14.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-14.csv`, `hashtag-2026-10-14.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 32 of 33 | 44 | 111 | 63 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 23 of 33 | 32 | 67 | 58 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 14 of 33 | 107 | 138 | 182 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 12 of 33 | 101 | 182 | 100 | 125 | 148 | 155 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| John Collins | 11 of 33 | 73 | 117 | 105 | 72 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 10 of 33 | 6 | 32 | 15 | 24 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 10 of 33 | 92 | 179 | 89 | 117 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Brandin Podziemski | 9 of 33 | 93 | 146 | 74 | 102 | 114 | 132 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 7 of 33 | 114 | 139 | 122 | 130 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Jaden McDaniels | 7 of 33 | 62 | 90 | 42 | 67 | 86 | 59 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Immanuel Quickley | 5 of 33 | 67 | 94 | 65 | 73 | 79 | 84 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Keegan Murray | 5 of 33 | 83 | 142 | 82 | 94 | 102 | 85 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (18 mocks, value 9, market 18); Derrick White (17 mocks, value 27, market 45); Lauri Markkanen (15 mocks, value 21, market 37); Tyrese Haliburton (13 mocks, value 7, market 12); Tyrese Maxey (11 mocks, value 5, market 9); Kel'el Ware (10 mocks, value 57, market 77); Tyler Herro (9 mocks, value 51, market 69); Karl-Anthony Towns (8 mocks, value 12, market 15); Miles Bridges (5 mocks, value 96, market 98).

## Decision sheet

| ID | Question | Default if you say nothing | Where |
|---|---|---|---|
| D-RR-1 | Merge the season override? It is decided ("Remove it", then "Kit season override") and built on this draft PR; it changes nothing visible today (measured, §2: `compare.json`) | not merged; Hunter keeps ×0.78 in the season tools | this report |

## Bounds

**Out of scope by design:**
- the deck's title-odds simulation (§3);
- the draft page and the deck pool;
- D-PM-4's injury tiers;
- any other player's tag.

**In scope and unverified:** none. Every figure above comes from the two morning runs and `compare.py`, which was run twice.

**Red-team bands** (the standing sweep record, engine 048efb6; no title share is quoted in this report):
- TEAM_WEEK_SHOCK is FRAGILE: +2.3 (no shared shock) / −3.4 (shock doubled).
- weekly_availability is FRAGILE: −2.0 (no in-sim injury discount) / +0.8 (harsher risk tier 0.65) / −1.5 (healthy plays 0.95) / +0.9 (healthy plays 0.80).

## Provenance

- **Produced by** session `session_01QjgeRdpDaWgSJmGKRG8fTU` on 2026-10-22, about 03:45–04:15Z.
- **Governors.** plan-gate was loaded for your route clicks, and the plan was stated before the first change. adversarial-verify is loaded before the delivery.
- **Re-verify:**
  - `python3 scripts/test_tag_overrides.py` (11 tests)
  - `python3 report/after-reports/hunter-override-2026-10-22/compare.py`
  - `python3 scripts/season_lines.py --date 2026-10-22 --out /tmp/s` (its PASS line ends "1 tag override(s)")

## In plain language

You decided Hunter's old eye-surgery tag should go: he's healthy, played in preseason, and isn't on any injury list. The in-season tools now treat him as healthy, through a small kit file, and the frozen draft-day files stay as they were.

Right now that changes nothing you'd see: I ran the morning both ways, and the brief came out byte-identical (EVIDENCE, §2). Hunter is a free agent whose projected stats come out below average, and the tools never discount a below-average player further for injury. So he ranks the same either way, outside the waiver list, and your brief came out identical. It starts to matter if his numbers climb or somebody picks him up. One limit remains: the title-odds simulation still reads the old tag, which would only matter if he were on a roster. Merging is your call.
