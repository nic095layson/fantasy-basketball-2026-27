# Availability tiers 0.80 / 0.65: the simulator change, the registry, and the re-run sweep

Pull window: 2026-11-16 → 2026-11-16 (no pull: kit main efe4356, deck main c933f07; the records branch season/daily at b35ad98, read only; this morning's pinned sweep inputs re-run in scratch).

**Owner's order, verbatim (2026-11-16):** "Owner pick 2026-11-16 (“Fit with a floor”, floor “Band edge: 0.80 / 0.65”): set the simulator’s availability tiers to healthy 0.80 (was 0.88) and injury-risk 0.65 (was 0.75); minor-knock stays 0.79, out/recovery stay 0." Deck: the two return values and the tests that pin them, red first, a PR. Kit: the registry value and its band ("healthy 0.88 / 0.78 and risk 0.75 / 0.56 (old value / unfloored fit)"), `season_deck.py`'s `TIER` labels, the kit tests that pin 0.88 / 0.75, a re-run of `sweep.py` on today's records, this report and its gates, a PR. Merge order: deck first, then kit, on the owner's word.

**Method up front.** Stated to the owner before any run (plan table in the session): the sweep runs `scripts/redteam/sweep.py --season … --real-schedule …`, 6,000 seasons x seeds 2026 and 2027, on this morning's pinned inputs from season/daily `report/after-reports/redteam-2026-11-16-season/` (league state sha b84f453f, season pool dbe05f8d, schedule 11e5bece; the derived picks file a12ecf58 matches the 5 AM record), deck at the change commit 9a009af. Basis: the same inputs as the 5 AM sweep (deck c933f07), so the engine change is the only difference between the two records. Tests were edited first and seen failing on the old engine, then the code changed. Mid-run, one owner card: the stale attack list (section 4).

**Verdict: the change is built and green on both repositories. On today's rosters the owner's title share moves from 14.8% to 17.1% (sweep baselines, mean of two seeds: 14.95 / 14.60 → 17.70 / 16.55; the 10k references agree, 14.69 / 14.52 → 17.26 / 16.63, +2.3). This is a method change, not a league event. weekly_availability stays FRAGILE, now through its risk tier only. The 11 standing attacks were re-run on the new engine on the owner's word. All are CURRENT and every gate passes. Two decision findings: one swap verdict is now conditional (A-6), and the 11-12 drop order's top two swapped inside a near-tie (A-11), section 9.**

Runner impact: code-only — tomorrow's morning run sweeps and simulates on the new tiers once the deck PR is merged; the title watch names the registry change as a METHOD CHANGE (checked: `title_watch.registry_changes` on main vs this branch returns the one `arena.weekly_availability` row). No step, record schema or Runner prompt changes.

Pool rows touched: none

## 1. What changed

| Where | Before | After | Evidence |
|---|---|---|---|
| Deck `arena/arena.py` `weekly_availability` | healthy 0.88, risk 0.75 | healthy 0.80, risk 0.65 (mild 0.79, recovery 0, out 0 unchanged) | deck commit 9a009af |
| Deck `docs/draft-deck.html` `weeklyAvail` (the page twin) | 0.88 / 0.75 | 0.80 / 0.65 | `test_card.py` asserts the exact twin; blocking dependency |
| Deck `arena/patches.py` `avail` patch | matched the live tiers by `== 0.75 / == 0.88` | matches `== 0.65 / == 0.80` | blocking dependency: on the old keys every avail variant in this sweep would have run as a silent no-op |
| Kit `constants_registry.json` `weekly_availability` | value 0.88 / 0.75; band: no discount, risk 0.65, healthy 0.95, healthy 0.80 | value 0.80 / 0.65; band (one tier moved, the other at its live value): healthy 0.88, healthy 0.78, risk 0.75, risk 0.56 | `check_constants.py`: PASS, 53 registered = 53 live on deck 9a009af |
| Kit `season_deck.py` `TIER` | 0.88 Healthy, 0.75 Injury risk | adds 0.80 Healthy and 0.65 Injury risk; keeps 0.88 and 0.75 | weeks 1-4 accuracy records are keyed by the old values |

The fit the pick rests on (EVIDENCE, `report/fits/fit_week4.json` on season/daily, read 2026-11-16): healthy tier measured 0.7788 (2,877 of 3,694 team games, SE 0.0068), risk tier 0.5594 (245 of 438, SE 0.0237), minor knock 0.885 (23 of 26), weeks 1-4. Both live values sat outside 2 SE of the measurement. The new values are each floored at the band edge, above the fit: healthy 0.80 is 3.1 SE above 0.779, risk 0.65 is 3.8 SE above 0.559.

## 2. Tests

| Repository | Red on the old engine (tests edited first) | Green after the change |
|---|---|---|
| Deck | `test_patches` 1 failure; `test_card` 2 of 103 (MILD weekly values, page twin); `test_season_cv` engine fingerprint (models sha and 600-season champion counts), re-pinned with the old values kept in a comment | each `arena/test_*.py` module OK run alone; `test_card` 103 of 103; `test_draft` 67 of 67; `test_gates`: see section 6 |
| Kit | 3 pins: `test_tag_overrides` (healthy read 0.88), `test_fit_constants` (risk ratio 0.75 / 0.88), `test_weekly_preview` (band labels and P(win) range) | full suite: section 6 |

## 3. The sweep on today's rosters (`availability-tiers-2026-11-16/sweep.json`)

Baseline within 3 SE of its own 10k reference on both seeds (17.70 / 16.55 against 17.26 / 16.63); MC SE 0.54 points per seed; engine 9a009af; inputs sha as in the method line. The 5 AM record on the same inputs and the old engine is beside it (`sweep_before_0500.json`, from season/daily).

| Constant | Variant | 5 AM, old tiers | Now, new tiers | Tier now |
|---|---|---|---|---|
| — | baseline, 6k sweep (10k reference) | 14.95 / 14.60 (14.69 / 14.52) | 17.70 / 16.55 (17.26 / 16.63) | — |
| weekly_availability | healthy at the old 0.88 | (live) | +0.4 | ROBUST |
| weekly_availability | healthy at the unfloored fit (0.78) | — | +0.1 | ROBUST |
| weekly_availability | risk at the old 0.75 | (live) | -2.7 | FRAGILE |
| weekly_availability | risk at the unfloored fit (0.56) | — | +1.8 | SENSITIVE |
| TEAM_WEEK_SHOCK | no shock / doubled | +0.4 / -0.9 | +0.9 / -1.2 | SENSITIVE (was ROBUST) |
| PCT_MIX_INFL | binomial floor only / 1.30 | +0.5 / -0.3 | +1.1 / +0.1 | SENSITIVE (was ROBUST) |
| GAMES_PER_WEEK | 3.0 / 4.0 | -0.2 / +0.9 | -0.3 / +0.4 | ROBUST |
| BENCH_WEIGHT | 0.50 / 1.00 | 0.0 / 0.0 | 0.0 / 0.0 | ROBUST |

**weekly_availability is FRAGILE:** +0.4 (healthy at the old 0.88) / +0.1 (healthy at the unfloored fit (0.78)) / -2.7 (risk at the old 0.75) / +1.8 (risk at the unfloored fit (0.56)); headline title share 17.1% ± 0.5 (MC) within that band, -2.7 to +1.8 points. Sweep of 2026-11-16 on this morning's rosters and season pool, engine 9a009af.

Reading it:
- **The move is the risk tier.** The 5 AM sweep had already measured risk 0.65 alone at +2.8 and healthy 0.80 alone at -0.4; together they predict about +2.4, and the change measures +2.3 on the sweep baselines (14.78 → 17.13) and on the 10k references (14.61 → 16.95). EVIDENCE: both records.
- **Cross-check, passed exactly.** Two engine points appear in both records, once as a patch on the old engine and once on the new: healthy 0.80 / risk 0.75 gives 14.38 / 14.45 in both ("healthy players play 0.80 of games" at 5 AM, "risk at the old 0.75" now), and healthy 0.88 / risk 0.65 gives 17.67 / 17.40 in both ("harsher risk tier (0.65)", "healthy at the old 0.88"). Identical to the hundredth on both seeds, so the new code path and the re-keyed patch compute what the old engine computed at those values. EVIDENCE: `variants` in both records.
- **The healthy tier no longer matters much** (+0.4, +0.1). The title share now hangs on the risk tier: its old value is 2.7 points down, its unfloored fit 1.8 up.
- **Two constants moved from ROBUST to SENSITIVE**, TEAM_WEEK_SHOCK (-1.2) and PCT_MIX_INFL (+1.1). Neither was touched. INFERENCE: both sit about 1.5 SE (shift SE about 0.76 points if the runs are independent) from the 1-point line they crossed, so the new tier may be noise as much as the new availability mix. The Monday sweep will show which.

## 4. The standing attack list: STALE at first (owner card), then re-run (section 9)

`run_attacks.py --check` on deck 9a009af: every record is fingerprinted to the engine, so the change marked all 11 STALE. EVIDENCE: the check's output, 2026-11-16. A-1 (`rt_math.py`) and A-9 (the from-spec simulator `attacker.py`, `SPEC.md`) also hard-code 0.88 / 0.75, so re-running them unchanged would fail on the new engine.

Owner card (2026-11-16, verbatim pick): **"Report it, decide later (Recommended)"**: re-run A-7 and A-8 only, open the kit PR with the attack gate as a known FAIL, the rest on a decision sheet.

| Attack | Now | What was done |
|---|---|---|
| A-7 constants registry | **CURRENT** | `check_constants.py --json` re-written to its record (`redteam-2026-10-19/constants.json`), engine 9a009af |
| A-8 assumption sweep (draft configuration) | STALE | ATTEMPTED-FAILED: run on the draft configuration (draft_state_100, pool v69), the baseline came out 25.68 / 25.27, outside 3 SE of the deck's 10k reference (23.06 / 23.25, built on the old engine), so its tiers cannot be read; record not written. The reference is a deck file (`arena/results/m100_league_sim_10k_s{seed}_w17r_av0_scv.json`) and needs regenerating on the new engine |
| A-1, A-9 | STALE | not re-run (owner card); the spec and attacker hold 0.88 / 0.75 |
| A-2 to A-6, A-10, A-11 | STALE | not re-run (owner card) |

The season sweep the owner ordered (section 3) is a separate record. It does not refresh A-8, which is the draft-configuration sweep.

## 5. Bounds

Out of scope by design:
- Minor knock stays 0.79 (owner). It was derived 2026-10-13 as a share of the old 0.88-to-0.75 gap and now sits 0.01 below healthy (measured 0.885, n 26). Flagged, not changed.
- Decision robustness (red-team step 5) for today's week-5 advice under the new band. A-6 and A-11 cover the standing decisions (section 9); the 11-16 advice was not re-run.
- The board's ranking discount (`hoops.availability`: 1.0 / 0.85 / 0.78) is a separate constant and is not changed. The registry's D-PM-4 reconciliation note still applies.

In scope and unverified:
- The sweep ran once (two seeds) on one configuration (this morning's rosters, blend season pool). The minutes-switched pool that the morning run uses from 11-17 was not swept with the new tiers (NOT-ATTEMPTED). The Monday sweep will do it.
- The SENSITIVE tiers for TEAM_WEEK_SHOCK and PCT_MIX_INFL are within MC error of the boundary (section 3; INFERENCE).
- Found in verification, flagged and not changed: `fit_constants.availability_pool` pools the weekly accuracy records by the tier's value string, and `board_comparison` reads the live keys (`tier_keys()`, now "0.80" / "0.65"). From week 5 the next fit therefore splits healthy into a "0.88" row (weeks 1-4, n 3,694) and a "0.80" row (week 5 on), and compares only the second. The same happens to risk. Nothing crashes. The healthy and risk measurements restart at week-5 sample sizes (EVIDENCE: `scripts/fit_constants.py` lines 92-106 and 110-114, read 2026-11-16).
- Pre-existing in the deck, not caused here: `test_season_cv` fails under `unittest discover` on deck main as well (models sha a876b1a0 in the shared process vs 88073a51 alone). It passes run alone, and that is how it was verified. Flagged, not touched.

## 6. Gates

The gate records are `gates.json` in each repository, quoted in each PR body. The first run, before the attacks were re-run, had two known FAILs with one cause (the stale attack list; `check_claims` CL-6 falls with it, as on 2026-10-21, D-RT-STALE). After the re-run (section 9), every gate passes: kit check_report, claim receipts, redteam constants (53 = 53), redteam bands, redteam attacks (11 of 11 CURRENT), check_claims (7 of 7 as expected). The deck record adds the deck and kit tests that pin the tiers. Kit suite: 1,244 tests OK (2 skipped).

## 7. Decisions for the owner

1. **Merge the deck PR, then the kit PR, on your word.** Both gate records pass (section 6).
2. **A-6, Draymond Green for Braun (the 10-19 draft pickup):** now conditional on the games shock, negative on one seed with no shock (section 9). Record it as conditional, or re-test it at 10,000 seasons to separate it from noise.
3. **Minor knock at 0.79,** 0.01 below healthy. Keep it, or re-derive it on the new gap (0.80 - 0.15 x 0.15 / 0.22 ≈ 0.70)? The measurement (0.885, n 26) is thin.
4. **The fit's pooling across the tier change** (section 5). (a) Pool by tier name, so weeks 1-4 and week 5 on count together. The measured share is the players', not the assumption's, so this is a small change to `fit_constants.py`. (b) Leave it keyed by value, so each assumption gets a fresh measurement.

## 8. Provenance

Produced by one Claude Code session on 2026-11-16 (session model A), at the owner's order above. Records beside this report: `availability-tiers-2026-11-16/sweep.json`, `sweep.log`, `sweep_before_0500.json` (copied from season/daily `redteam-2026-11-16-season/sweep.json`). Section 9's records sit beside each attack's script (old ones as `*_pre-2026-11-16-tiers.json`); scratch work for A-10 and A-11 was a worktree of season/daily 0e21df1. Re-verify: `python3 scripts/redteam/run_attacks.py --check` (expect 11 CURRENT on the deck that carries 9a009af); `python3 scripts/redteam/check_constants.py` (expect 53 = 53 on the deck commit that carries 0.80 / 0.65); `python3 scripts/redteam/check_bands.py --report <this> --sweep report/after-reports/availability-tiers-2026-11-16/sweep.json`; `git show origin/season/daily:report/fits/fit_week4.json` for the fit.

## 9. The attacks re-run on the new engine (owner: "Re-run the stale attacks on the new engine")

Stated before the run: each attack re-runs on the same inputs as its current record, so only the engine changes. Those inputs are the draft state 100 and pool v69 (A-1 to A-6, A-8, A-9), the 11-12 evening records (season/daily 0e21df1) for A-10 and A-11, and each script's own seasons and seeds. Old records are kept beside the new ones as `*_pre-2026-11-16-tiers.json`, and each attack's history row in `scripts/redteam/attacks.json` says what changed. `run_attacks.py --check`: **PASS, 11 of 11 CURRENT** (engine files last changed 9a009af).

| Attack | Change needed | Result on the new engine |
|---|---|---|
| A-1 known-answer math | known-answer tiers 0.80 / 0.65 | z, availability, owner week FG% and PTS mean and variance equal to the last digit |
| A-2 line join | none | 0 line differences on 309 rows, as before |
| A-3 card vs simulator | none | every category at 50%; max gap 0.023 / 0.026 (was 0.036 / 0.038); rank agreement 0.972 / 0.979 |
| A-4 ties | none | 0.177 / 0.180 tied categories per matchup (was 0.175 / 0.176) |
| A-5 structural sensitivity | patch keys to 0.80 / 0.65 (on the old keys every tier variant was a silent no-op); tier variants = the new band; new reference | baseline 25.67 / 26.07 within 3 SE of 26.11 / 26.26; shock is the widest (+6.1 / +4.7 with no shock) |
| A-6 decision robustness | "no discount" lifts risk to 0.80 | **Jalen Johnson for Durant positive everywhere (smallest +0.18). Draymond Green for Braun is NOT: no shock gives -0.18 / +0.67** |
| A-7 constants | none | 53 = 53 |
| A-8 draft sweep | new reference (`_scv_t8065`, 25.52 / 25.68) | baseline within 3 SE; TEAM_WEEK_SHOCK FRAGILE +2.4 / -3.4; weekly_availability SENSITIVE (worst -1.5) |
| A-9 separate-attacker simulator | SPEC.md rules 4, 6, 7 and attacker.py to 0.65 / 0.65 / 0.80 | every exact section PASS; seasons max abs z 2.21; same-seed stream 12 of 12 |
| A-10 IL-return known answers | brief headline recomputed on the live engine (daily_brief's section-5 code path, 22.23 / 21.36) | 4 of 4 live checks PASS |
| A-11 drop order | the new band overlaid on the 11-12 registry | **top two swap inside a near-tie; rule's pick last 21 of 22** |

Known answers on the new references (EVIDENCE: deck commit 56b3a6b). `league_sim --verify` passes on all four new files. The new engine with the tiers patched back to 0.88 / 0.75 reproduces the four old reference files seat for seat. In A-5 and the season sweep, the engine points shared with the old records reproduce them to the hundredth.

**A-6 finding.** Under "no shared games shock", Draymond Green for Braun is -0.18 on seed 2026 and +0.67 on 2027. The mean is +0.25, against the difference's MC SE of 0.76. The old record's smallest value was +0.42. Per the red-team rule, a verdict that flips sign under a plausible constant is reported as conditional. INFERENCE: the 10-19 pickup's value now rests on the games shock being non-zero. A separate cross-check (`attacks/` scratch, 2026-11-16) found this swap's shipped-setting figure (26.32 / 27.82) equal to A-5's "healthy 0.78" variant on both seeds. Every other seat differs between the two runs, so it is a coincidence of shared random streams, not a shared computation.

**A-11 finding.** On the same 11-12 records (state, pool and schedule sha equal to the old record), the baseline order of the top two swaps:

| | Old engine | New engine |
|---|---|---|
| Queta + Cam Johnson / Champagnie + Queta (title %) | 28.10 / 27.93 | 29.42 / 29.51 |
| Best pair across 22 seed-runs | 18 / 3 / 1 | 11 / 9 / 2 (Queta + CJ / Champagnie + Queta / Champagnie + CJ) |
| Rule's pick last | 22 of 22 | 21 of 22 |

The top two were within 0.2 points before and are within 0.1 now, so on both engines they are a near-tie. The 11-12 conclusion that any of the three pairs beats the rule's pick still holds in 21 of 22 seed-runs. The decision itself is past: today's roster no longer carries Champagnie (season/daily `data/league_state.json`, as of 2026-11-16).

A-9 caveat: the three amended numbers in `attacker.py` were edited by this session, which had read `arena.py`. Independence for those three is not fresh. The rest of the attacker is the 10-21 separate attacker's. A-1 keeps its pre-existing recovery 0.60 (the engine has used 0.0 since 10-21). It is untested here because no recovery-tagged player is on the checked roster; flagged, not changed.
