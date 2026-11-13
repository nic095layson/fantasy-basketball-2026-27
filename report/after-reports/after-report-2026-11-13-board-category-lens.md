# Board: stacked category filter, as on the Draft Deck (owner 2026-11-13)

Pull window: 2026-11-13 → 2026-11-13 (no pull: kit main 8dc596d; the records branch season/daily at 81d047d, read only, for one deck build in a throwaway copy).

**Owner's request, verbatim:** "One ask to implement to tool, please. On the "Board" tab, can you add the multi-category filter ability like on the Draft Deck tool? Thank you!"

**Method up front.** The Draft Deck's Best Available table (`docs/draft-deck.html` in the deck repository, `renderBest`) was read and its behaviour copied: header clicks stack up to 3 categories, the table ranks by their combined z, a re-click drills into one, chips with × remove, Reset clears, any other sort clears. The plan, with each of these choices, was shown before any file was written. Tests first, seen failing.

**Verdict: built. Clicking a category header on the Board now adds it to a category lens instead of sorting by that one column.**

Runner impact: code-only — the morning and afternoon decks pick it up from `season_deck.py`; no step, record or prompt changes.

Pool rows touched: none

## 1. What it does

| Action | Result |
|---|---|
| Click a category header | Adds it to the lens (up to 3); the table ranks by the combined z of the selected categories, highest first, and a "cats" column shows that sum |
| Click a selected header again | Ranks by that category alone, the combined sum breaking ties; a third click returns to the combined order |
| Click a fourth category | Blocked, with a note to remove one first (the Draft Deck's rule) |
| × on a chip | Removes that category |
| Reset, any other column header, or a change to the build switches | Clears the lens |

The combined value is the plain sum of the category z-scores shown in the table, with no availability discount. The # and z adj columns, the build strip and the simulator are unchanged. Search and "free agents only" still apply.

## 2. Checks

| Check | Result |
|---|---|
| New tests (3) seen failing first | No lens existed: no chips, single-column sort |
| New tests after | Pass: combined order and the cats column; drill and the 3-category cap; ×, Reset and another header clearing the lens |
| Board, punt and Full health tests | Pass unchanged |
| Deck on today's records | PASS, 0 page errors. Assists + steals ranks Dyson Daniels (5.14), Nikola Jokic (4.86), Luka Doncic (4.38) first; after My build, a blocks lens ranks Wembanyama, Kessler, Holmgren first with the fit column still shown |
| Full suite | 1,203 tests OK, 2 skipped (was 1,200) |

## 3. Bounds

Out of scope by design: the Draft Deck's other lenses (market rank, ΔECW), which the season Board has no equivalent of; the Trade Analyzer and Free Agents tabs.

In scope and unverified: the layout at phone width was not checked in a browser at that size (did not check).

## 4. Next steps (owner decisions)

1. Merge this PR, or not.

## 5. Provenance

Session of 2026-11-13 (session model B), branch `claude/market-data-workorder-mnfi2b`. Re-verify: `python3 -m unittest test_season_deck.BoardCategoryLens` in `scripts/`.
