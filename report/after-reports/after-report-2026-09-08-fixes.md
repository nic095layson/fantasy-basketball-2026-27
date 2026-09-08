# After-Report — Fix Adoption + Full System Audit, 2026-09-08

**Scope:** owner directive — *"Implement all fixes. Afterwards, conduct
validation, integrity and full system audit test. Provide after report. If
all checks green, merge."* This report covers the implementation and the
audit; the merge record is appended by the pull requests themselves.

**Method up front:** every fix was implemented, then **exercised to failure
and to success** — a gate that has never been seen red is untested by
definition (the house rule that produced `test_gates.py`). Two of the checks
below found real defects **in the fixes themselves** during this audit, both
fixed before adoption; they are reported, not smoothed over.

## 1. What was implemented

| fix | where | what it does |
|---|---|---|
| **F1** receipts contract | deck `scripts/judgment_open_items.py` (new, 200 lines) + kit `DATA-PULL.md` §2/§5 | Enumerates open JUDGMENT items by unresolved-marker lexicon (the refinement validated 9/2: 18→8, zero loss vs hand triage); prints a ready-to-fill **Open-item receipts** table; `--check-report` fails any report whose player column lacks a receipt for a flagged name. A flagged name with no receipt = the pull is incomplete |
| **F2** publication gate | kit `report/check_report.py` (new, 160 lines) + `DATA-PULL.md` §0.4b/§2 | Row impact no longer scopes verification: any transaction-asserting table row in an after-report needs **two outlets or an explicit `[SINGLE-SOURCE]` label**. Also checks report structure and the pull-log row. Scoped by table header so evidence/receipts/decision tables don't false-positive |
| **F3** team-shadow sweep | in F1's script + `DATA-PULL.md` §2 | Prints the **team watch set** the open items imply (flagged players' teams + counterparties named in their cards); one team-shaped query each per pull. Current set: CHI, DET, LAC, MEM, NOP, NYK, POR — a set that contains **both teams of the trade this pull missed** |
| **F4** colophon truth gate | deck `build_deck.py` **gate 6** + 3 new `test_gates.py` cases | Build refuses when the hand-authored "Data." paragraph contradicts the pool count (any `N rows`, `N/N`, `N-player pool` token) or narrates the wrong pull (`This refresh (M/D` ≠ freshness date). The colophon drifted silently on two consecutive pulls |
| **F5** zero-trade anomaly rule | `DATA-PULL.md` §2 | A multi-day window with zero league-wide trades found is a **sweep-failure signal**: one ledger-shaped query (RealGM/HoopsRumors index) is mandatory, cited, before writing "no trades in window" |
| **F6** returner-vs-tag diff | F1's script `--tags` + `DATA-PULL.md` §2 | Prints the availability-tag inventory (7 excluded, 31 risk-tagged); the injury sweep diffs returning-player coverage against it **both directions** — returning-but-untagged is how Jamal Murray shipped unpriced |

Plus the **authoring contract** (`DATA-PULL.md` §7.4): a JUDGMENT card
describing an open situation must carry a marker phrase from the lexicon,
and the enumerator is re-run after re-authoring.

## 2. Defects found IN the fixes during this audit (both fixed pre-adoption)

1. **The enumerator lost two open items on its first run.** The freshly
   re-authored Kawhi and Mathurin cards described open situations in
   phrasings the lexicon didn't cover, and both silently dropped off the
   flagged list (8 → 6). Lexicon extended (`not formally executed`,
   `yet to be finalized`, `expected to be finalized`, `reprice checkpoint`);
   the authoring contract exists because of this. Re-run: **8 flagged,
   matching the hand triage exactly.**
2. **The receipts check had a hole.** On its first behavioral test, deleting
   a player's receipt cell passed anyway — the name survived inside the
   *query* column's text. Tightened to require the name in the **player
   column** (first cell). Re-test: broken report now fails naming the
   missing player; the real report passes.

A third, smaller catch: gate 6 correctly refused a `test_gates.py` scenario
whose colophon lied about its mutated pool — the test now keeps its colophon
truthful, which is the discipline the gate enforces.

## 3. Full system audit — all green

| check | result |
|---|---|
| deck `verify_rosters` | **255/255, 0 mismatches, 0 unmatched**, dated 2026-09-08, `fallback-partial` (egress bound, stated) |
| deck `build_deck.py` — **all six gates, live file** | green: 255 players, pull 2026-09-08, pool `c98cf4f39840`, injection round-trip byte-identical |
| deck `check_parity` | **EXACT MATCH** — 2295 z-cells, 64 name fixtures, 72 df_hash vectors bit-identical, 78 card orderings |
| deck `test_gates.py` | **15/15** (12 prior + 3 new gate-6 cases, each run to refusal and acceptance) |
| deck `test_draft.py` | **53/53** |
| `judgment_open_items.py` | 8 flagged (= hand triage); `--tags` inventory 7 excluded / 31 risk; `--check-report` **PASS** on the real report, **FAIL** on the mutated one |
| kit `check_provenance` | exit **0** (verified 2026-07-13 .. 2026-09-02) |
| kit `check_report.py` | **PASS** on the amended 9/8 report; **FAIL** (as designed) on the label-stripped copy |
| kit `rank_engine` determinism | run twice — **byte-identical** apart from the generation-date line |
| cross-plane spot state | Murray: deck `inj-achilles-risk` 0.78 / kit GP 62 ✓ · Hawkins: deck MEM, kit no row ✓ · Mathurin: NOP both planes, deck −0.10 ✓ |
| artifact | republished at `built: 2026-09-08`, built through the six-gate pipeline |

## 4. Verification (adversarial pass)

- **C1 — every gate was seen red before being trusted**: gate 6 refused a
  wrong count and a wrong narrated pull in `test_gates.py`; `check_report`
  refused the label-stripped report; the receipts check refused the
  deleted-cell report — after being fixed to (§2.2).
- **C2 — the fixes were tested against the failures that motivated them**:
  the team watch set contains NOP and MEM (the missed trade's two teams);
  the `--tags` diff names Murray's exact failure mode; the publication gate
  fires on exactly the class of row Simmons shipped in.
- **C3 — scope**: no engine, projection, or structural-knob change anywhere
  in this adoption; the September feature freeze is untouched (this work is
  owner-explicit + truth/reporting). Board unchanged by the audit
  (deterministic re-run only).
- **Bounds**: `check_report`'s outlet lexicon is a list, not intelligence —
  a fabricated outlet name would count; the gate raises the cost of a
  garble shipping, it cannot verify truth. The receipts check verifies a
  receipt EXISTS, not that its query was well-chosen. Both stated rather
  than oversold.

## 5. Owner decisions closed / remaining

- **D-S9 (adopt fixes): CLOSED — adopted**, this report.
- **D-S6/F4: CLOSED — shipped** as gate 6.
- **D-S5: CLOSED — shipped** as `judgment_open_items.py`.
- **D-S7 (merge the stack): executing now** per the owner's directive;
  merge results recorded on the PRs.
- Remaining: **D-S1** (projection datasets), **D-S2** (consensus ADP),
  **D-S4** (October Routine de-risk), **D-S8** (Sabonis tag overrule).
