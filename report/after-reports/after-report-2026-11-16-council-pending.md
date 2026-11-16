# Council on the three pending decisions of the availability-tiers change, and what was carried out

Pull window: 2026-11-16 → 2026-11-16 (no pull: kit main a2aa86f, deck main 944b98a; the records branch season/daily at b35ad98, read only, refit in a throwaway worktree).

**Owner's order, verbatim (2026-11-16):** "Have council deliberate pending decisions and proceed with their vote."

**Method up front.** The facts each decision needed were read before the Council deliberated, and are the evidence column below. The Council ran five roles (Contrarian, First Principles, Expansionist, Outsider, Executor) and voted per decision. The plan (goal, method, done-when, branch rule) was shown to the owner before any file was written. The one build was tested first (a new test, seen failing), then checked on the season/daily records: refit week 4 and compare with the committed `fit_week4.json`.

**Verdict: three decisions taken. One builds: the weekly availability fit now pools each tier across its value change. Two are recorded: the A-6 swap verdict is conditional, and minor knock stays 0.79.**

Runner impact: code-only — the Monday fit (`scoreboard_intake` → `fit_constants.run`) keys each tier by its live value and pools the weeks recorded under the tier's earlier value. No step, prompt or schedule changes.

Pool rows touched: none

## 1. The three decisions

| Decision | Vote | Verdict | Evidence (read 2026-11-16) |
|---|---|---|---|
| A-6: Draymond Green for Braun, conditional under no shock | 4-1 | Record as conditional; no 10k re-test | The difference's MC SE is 0.76 at 6,000 seasons and about 0.59 at 10,000, so a re-test cannot resolve the +0.25 mean. The swap is no live decision: Draymond Green is on another team's roster and Braun was dropped by the owner (season/daily `data/league_state.json`, as of 2026-11-16) |
| Minor knock at 0.79, now 0.01 below healthy | 5-0 | Keep 0.79 | The one measurement is 0.885 (n 26, weeks 1-4, `fit_week4.json`). Re-deriving on the new gap (about 0.70) would sit 2.9 SE below it. Mild-tagged players today: Kyrie Irving (owner's roster) and Damian Lillard |
| Fit pooling across the tier change | 4-1 | Pool by tier, keyed and judged by the live value, per-value counts kept | Keyed by value, the next fit would have split healthy into a "0.88" row (n 3,694) and a "0.80" row, and compared only the second |

Dissents. On A-6, the Expansionist voted to re-test because it costs about a minute; that vote flips if the swap becomes a live decision again. On pooling, the Contrarian holds that pooling could hide a change in who carries a tag; that vote flips if a tag's definition changes. The `pooled_from` counts are kept so such a change stays visible.

## 2. What changed

| Where | Change |
|---|---|
| `scripts/fit_constants.py` | `availability_pool(weeks, live=None)`. With `live` (the live keys from `tier_keys()`), a tier's rows under an earlier value pool with its live-value rows, keyed and judged by the live value, with `pooled_from` holding team games per recorded value. `VALUE_TIER` lists every value each tier has carried. `run()` passes `live`. Without `live`, the pool is by value as before |
| `scripts/test_fit_constants.py` | Two tests: pooling across a value change (seen failing first), and the by-value pool without `live` |
| `scripts/redteam/attacks.json` | A-6 history: the conditional verdict and the vote |
| `scripts/redteam/constants_registry.json` | weekly_availability record: mild kept at 0.79 and why. The value is unchanged |

## 3. Checks

| Check | Result |
|---|---|
| New test before the code | ERROR (no `live` argument), then OK. One assertion in the new test was my own arithmetic slip: 0.80 against a pooled 0.852 at n 1,609 is about 5.8 SE away, so "within 2 SE" is False. I corrected the test, not the code |
| Week-4 refit on season/daily b35ad98 (throwaway worktree) | Measured shares identical to `fit_week4.json`: healthy 0.7788 (n 3,694, `pooled_from` 0.88), risk 0.5594 (n 438, `pooled_from` 0.75), out 0.0583, mild 0.8846. They are now judged against the live 0.80 / 0.65 |
| Board comparison in the refit | risk 0.718, simulator ratio 0.8125 (was 0.8523); mild 1.136, simulator 0.9875 (was 0.8977), now within 2 SE of the simulator. The simulator ratios moved because of the merged tier change |
| Kit suite | 1,254 tests OK (2 skipped) |
| Constants registry / standing attacks | 53 = 53; 11 of 11 CURRENT |

## 4. Bounds

Out of scope by design: any value change (none was voted); a re-test of the A-6 swap; re-running the Monday fit into `report/fits/` on the records branch, which is the morning run's job.

In scope and unverified: none.

Limit of the pooling, stated rather than guarded: `VALUE_TIER` maps a recorded value to its tier. A future value not in the table still pools correctly (checked: healthy at a hypothetical 0.82 pools the 0.88 rows under "0.82"). If a tier is ever set to a value another tier holds (for example healthy to 0.79, minor knock's value), the two tiers' rows cannot be told apart by value. That change would need a tier name in the accuracy card's rows.

Found in the refit, flagged and not acted on: the week-4 TEAM_WEEK_SHOCK fit moves from 0.1069 to 0.1177 on the same inputs. This branch with the engine patched back to 0.88 / 0.75 reproduces 0.10689 exactly, so the move is the merged tier change, not this edit. The fit compares the realized weekly swing with the model's own variance, and the lower availability lowers the model's game counts. The next Monday fit will show it. It is a proposal only and changes nothing live.

## 5. Decisions for the owner

1. **Merge the kit PR on your word.** No deck change.
2. **TEAM_WEEK_SHOCK.** The fit now reads 0.118 against the live 0.06 (section 4). The decision is yours when the fit makes its weekly proposal; nothing here changes it.

## 6. Provenance

One Claude Code session on 2026-11-16 (session model A), on the owner's order above. The Council's deliberation stayed internal; its condensed verdict was shown to the owner before the build. Re-verify: `python3 -m unittest scripts.test_fit_constants`; the refit with `FC.run(4, <records>/data/weeks, <records>/report/accuracy, <records>/report/accuracy.json, <out>)` on season/daily.
