# The box-score name mismatch, fixed in the three readers — 2026-10-22

Window: box-score records 2026-10-16, 10-19, 10-20, 10-21 (the four on `season/daily` `e7b69bb`); one live re-pull of 2026-10-21. No projection line, tag, roster or engine constant changed.

**Owner's request.** The opponent-side gap on the week card was assessed on 2026-10-22 (the whole gap was Darius Acuff Jr.'s 10/21 game, left unmatched by the box pull). Asked how to handle it, the owner chose "Fix both readers", 2026-10-22 ~14:40Z: box-score names also match with the Jr./II suffix dropped, and the week card matches box scores by its own spelling, covering Acuff, Mikel Brown Jr., Kelly Oubre Jr., Dereck Lively II and Cam Johnson; then rebuild the 10/21 records and season lines.

**What was analyzed.**
- Kit `main` `af625a8`; this branch `claude/box-name-suffix-fix`.
- The committed records of `season/daily` `e7b69bb` (the 14:44Z morning run).
- Deck `048efb6`, unchanged.

**Method.**
- Red-first: the seven new tests were run on `main`'s code first. Six failed (4 failures, 2 errors); the seventh, two pool names sharing a key, is a guard written to pass from the start, and it did. Then the fix was written. Logs are in `name-fix-2026-10-22/red_first.txt` and `green.txt`.
- Evidence on real data comes from `name-fix-2026-10-22/evidence.py`, run on the fixed code against `e7b69bb`'s records (writes `evidence.json`), plus one live re-pull of 10/21 (`repull_2026-10-21.json`).
- Fallback rule: a name matches its suffix-free key only when exactly one name shares that key. A shared key matches nothing, so nothing is guessed.

**Headline.**
- **The week card's rebuild now counts Acuff's 10/21 game.** On the committed records your side still equals Yahoo on all 11 stats. The opponent's gap shrinks to exactly Gui Santos's 10/21 line. Santos was dropped this morning after playing, and the rebuild reads today's roster. That second cause is outside this fix and is recorded below.
- **The box pull now matches Acuff, Mikel Brown Jr., Kelly Oubre Jr. and Labaron Philon Jr.** The live re-pull of 10/21 differs from the committed record only in those names' match (3 on that date). Zero stat cells differ.
- **Season lines:**
  - The kit-format lines (the kit board) gain the games of Acuff, Brown and Oubre.
  - The deck-format lines (the simulator) were already counting them, because the raw ESPN spelling matched. They keep doing so, which needed the change in `season_lines.py`. Without it, the box-pull change alone would have dropped them.
  - The deck-format line for Herbert Jones now receives his 10/21 game, as the kit-format line already did. ESPN's "Herbert Jones" is "Herb Jones" in the kit file and alias table, the same pattern as Cam Johnson.

---

## 1. The change

| File | Change |
|---|---|
| `scripts/box_pull.py` | `name_index` / `match_name`: the folded spelling first (with the alias table), then the suffix-free key when one name shares it. `resolve_names` uses them. |
| `scripts/week_matchup.py` | `played()` and `_recent_boxes()` take the card's names and read each box line under the spelling its source name (then its pool name) matches there; `build()` passes the card's pool names. Without names, behaviour is unchanged. |
| `scripts/season_lines.py` | `totals()` keeps each total's source spellings; `finder()` matches a plane row by either spelling, then by the suffix-free key when it names one total; both planes use it. |
| tests | 7 new: 2 in `test_box_pull.py`, 3 in `test_week_matchup.py`, 2 in `test_season_lines.py`. |

## 2. Evidence (all EVIDENCE: measured on the fixed code, records named)

**Tests.**
- New tests on `main`'s code: 6 of 7 fail (4 failures, 2 errors), the guard passes. With the fix, all 59 tests in the three files pass.
- Full suite: 342 tests, two runs, identical results. 340 pass, 1 is skipped, and 1 fails: `test_matchup_live.Record.test_todays_transcript_yields_todays_outlook`.
- That failure is pre-existing. It fails identically on `main` `af625a8` (335 tests). It reads today's live session transcript and expects a fixed opponent name from an earlier date. It is unrelated to this change and was left untouched.

**Re-match of the four committed records** (`evidence.json` → `reresolve`): 7 rows change, all from unmatched to matched:

| Date | ESPN name | Now matched to | Regular season |
|---|---|---|---|
| 10-16 | Labaron Philon Jr. | Labaron Philon | no |
| 10-16 | Kelly Oubre Jr. | Kelly Oubre | no |
| 10-16 | Darius Acuff Jr. | Darius Acuff | no |
| 10-20 | Labaron Philon Jr. | Labaron Philon | yes (did not play) |
| 10-21 | Mikel Brown Jr. | Mikel Brown | yes |
| 10-21 | Kelly Oubre Jr. | Kelly Oubre | yes |
| 10-21 | Darius Acuff Jr. | Darius Acuff | yes |

**Live re-pull of 10/21** (`repull_2026-10-21.json`):
- Same 301 players. 0 stat cells differ.
- Games and the reconciliation between the two box-score sources are identical.
- Name-match changes: Brown, Oubre, Acuff. Matched lines 204 → 207, unmatched 97 → 94.

**Week card, 2026-10-22, on the committed records:**
- Your rebuild equals Yahoo on all 11 stats.
- The opponent's rebuild differs from Yahoo by FGM 5, FGA 10, FTM 1, FTA 2, 3PM 1, PTS 12, REB 5, STL 1. That is exactly Gui Santos's 10/21 box line (5-10 FG, 1-2 FT, 1 3PM, 12 PTS, 5 REB, 0 AST, 1 STL, 0 BLK, 0 TO).
- Before the fix, the gap was that line plus Acuff's (10 stats).

**Season lines rebuilt on the re-matched records against the committed ones:**
- Kit-format file (325 rows): changes for Darius Acuff, Kelly Oubre and Mikel Brown only.
- Deck-format file (336 rows): changes for Herbert Jones only, and his new values equal the kit-format "Herb Jones" line exactly.

## 3. Bounds

**Out of scope by design:**
- The rebuild reads **today's** roster, so a player dropped after playing (Gui Santos) loses his games, and one added late would gain games he did not score for the team. A fix would read Yahoo's daily rosters (Flaim `as_of_date`) instead. That is a design choice for the owner and is not part of this PR.
- `scripts/availability_calibration.py` has the same name mismatch: it credits games by the box pull's spelling (kit file) to rostered names (Yahoo spelling). It is unchanged by this PR. Its verdict cannot be produced before about 11/17.

**In scope and unverified:**
- How much one 10/21 game moves the kit board for Acuff, Brown and Oubre beyond the line values above (board ranks were not recomputed).
- Cam Johnson has played no regular-season game in the records yet. His case is covered by the unit tests, not yet by a real line.

**Records on `season/daily` are not edited.** They pick the fix up on the first morning run after this PR merges.

## 4. Decisions for the owner

1. **Merge this PR?** It is a draft; gates are run on it before any merge (RULES 7).
2. **The today's-roster rule:** leave it, or have the rebuild read Yahoo's daily rosters.
3. **The availability calibration's name mismatch:** a one-file follow-up, or leave it until the verdict date.
