# The kit-row games rule is a registered constant (2026-11-23)

Pull window: 2026-11-23 → 2026-11-23 (no pull: kit main 1c6eaa0, deck main 3551a15, the records branch season/daily at 0e053c4b, read only).

**Owner's request, verbatim (2026-11-23).** Card pick "Register median-games rule (Recommended)", on the Monday ranked list's finding that kit #298 gives a copied kit row "gp = the kit file's median", "a stated judgment rule, not fitted", which the constants registry did not carry.

**Method up front.** Stated to the owner before the change: name the rule as a module constant in `scripts/season_lines.py` (`KIT_ROW_GP_QUANTILE = 0.5`, the median, read by `kit_rows_for_rostered`), register it as uncalibrated with a decision id, tests first. No value changes: 0.5 gives the same median as before.

**Verdict. The constants check now sees the rule: 54 registered = 54 live (was 53), uncalibrated 25; every copied row keeps the same games played.**

Runner impact: code-only (no record, step or prompt changes; a kit row's gp is unchanged at 0.5).

Pool rows touched: none

## 1. Checks

| check | before the registry row | after |
|---|---|---|
| `scripts/redteam/check_constants.py` with the constant named | FAIL: "season_lines.KIT_ROW_GP_QUANTILE: live constant not registered (value 0.5)" | PASS, 54 = 54 |
| `scripts/test_season_lines.py` (new test: the registry carries it as uncalibrated, and gp follows the quantile: 0.5 gives 65 on gp 40/60/70/80, 0 gives 40, 1 gives 80, 0.25 gives 55) | 1 error | 22 tests OK |

The full suite and gates: below, from gates.py. Decision D-KR-1: compare the copied rows' gp with the games those players actually play, at week 10.

## 2. Bounds

Out of scope by design: the rule's value; the other two Monday picks (gates for Runner-built changes, the test-file run block) ship in their own pull requests.

## 3. Provenance

Session of 2026-11-23 (session model B, continuing the Main session; branch `claude/register-kit-row-gp`). Re-verify: `python3 scripts/redteam/check_constants.py`.
