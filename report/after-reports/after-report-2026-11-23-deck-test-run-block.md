# The deck test file runs every test when run on its own (2026-11-23)

Pull window: 2026-11-23 → 2026-11-23 (no pull: kit main 1c6eaa0, deck main 3551a15; no records read).

**Owner's request, verbatim (2026-11-23).** On the Monday ranked list's card of small fixes: "For the remaining 3 decisions on this card, invoke Council to deliberate and proceed with their vote." The Council voted 4-1 to build all three; this pull request is the first (the test file), the other two ship together as one documents pull request.

**Method up front.** Stated to the owner before the change: move `scripts/test_season_deck.py`'s `if __name__ == "__main__": unittest.main()` block from line 1750 to the end of the file, with a guard test that fails when any class or function follows it. No test is changed.

**Verdict. Run as a script, the file now runs 254 tests, OK, the same as the module form every gate uses (it ran 178 with 5 errors before).**

Runner impact: none (the Runner and every gate run the module form).

Pool rows touched: none

## 1. Checks

| run | before | after |
|---|---|---|
| `python3 scripts/test_season_deck.py` | 178 tests, 5 errors (NameError: accuracy_record) | 254 tests, OK (255 with the guard) |
| `python3 -m unittest discover -s scripts -p test_season_deck.py` | 254 OK | 254 OK (255 with the guard) |
| guard `RunBlockLast` against the old layout | fails (run block at line 1750, last definition at 3038) | passes |

The full suite and gates: below, from gates.py.

## 2. Provenance

Session of 2026-11-23 (session model B, continuing the Main session; branch `claude/deck-test-run-block`). Re-verify: `python3 scripts/test_season_deck.py`.
