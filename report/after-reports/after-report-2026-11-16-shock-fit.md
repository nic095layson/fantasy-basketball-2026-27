# TEAM_WEEK_SHOCK 0.06 → 0.11: the Council on the shock fit, the change, and the re-run attacks

Pull window: 2026-11-16 → 2026-11-16 (no pull: kit main 7ba438d, deck main 944b98a; the records branch season/daily at b35ad98, read only; refits, sweeps and attacks in scratch and throwaway worktrees).

**Owner's order, verbatim (2026-11-16):** "Have council deliberate the shock fit and proceed."

**Method up front.** Two things were read before the Council deliberated:
- the shock fit's history (`report/fits/fit_week1..4.json` on season/daily);
- a week-4 refit on both tier settings, splitting the fit into the model's level (mean of actual / model over the counting categories) and the shock relative to that level.

The Council's verdict and the plan were shown to the owner before any file was written. The change was then carried like the tier change:
- deck tests first;
- new 10k references, checked against the old ones by patching the old value back;
- the registry and band;
- every standing attack re-run on its current record's inputs;
- one season sweep on the same 5 AM pinned inputs as the tier sweep (state a12ecf58, pool dbe05f8d, schedule 11e5bece), 6,000 seasons on seeds 2026 and 2027.

**Verdict: TEAM_WEEK_SHOCK is 0.11 (Council 4-1). On today's rosters the owner's title share moves from 17.1% to 16.5% (sweep baselines 17.70 / 16.55 → 16.78 / 16.15; 10k references 17.26 / 16.63 → 16.34 / 15.98). This is a method change, not a league event. Two findings for the owner: the model's weekly level runs 10% low since the tier change, and the card's category edges now run wider than the simulator's. Also corrected: a record from earlier today.**

Runner impact: code-only — the morning run's simulator and sweep use the new shock and the new references once both PRs merge; the title watch names the registry change as a method change. No step, record schema or Runner prompt changes.

Pool rows touched: none

## 1. The Council

| Vote | Verdict | Evidence (read 2026-11-16) |
|---|---|---|
| 4-1 | Set 0.11, the level-relative fit rounded. New band: 0.0 / 0.06 (old value) / 0.13 (fit + 2 SE) | Fit by week: 0.097 → 0.112 → 0.107 (weeks 2-4, 24 / 36 / 48 team-weeks), SE about 0.013. The live 0.06 sat 3.6 SE below. The raw fit on the new tiers is 0.118, but relative to the model's level it is 0.1067, against 0.1068 on the old tiers (the same week-4 inputs re-fitted both ways) |

Dissent (Contrarian): fix the model's level error (section 4) first, so the engine changes once, not twice. That vote flips if fixing the level is shown to move the level-relative shock.

## 2. What changed

| Where | Change |
|---|---|
| Deck `arena/arena.py` | `TEAM_WEEK_SHOCK = 0.11` (commit ecb60cb) |
| Deck `arena/test_season_cv.py` | The value pinned (seen failing first); the 600-season champion fingerprint re-pinned, with the 0.06 counts kept in a comment. The weekly-model hash does not move: the shock is drawn in the season, not in the model |
| Deck `arena/results/m100_league_sim_10k_s{2026,2027}_w17r_av0[_scv]_t8065_s11.json` | New references (`league_sim --verify`). The engine with 0.06 patched back reproduces the four `_t8065` files seat for seat. Seat 10 on the draft configuration: 26.11 / 26.26 to 22.90 / 22.98 |
| Kit `constants_registry.json` | Value 0.11; record with the fit and the vote; band 0.0 / 0.06 / 0.13 |
| Kit `sweep.py`, `rt_sensitivity.py`, `rt_decisions.py` | Reference to `_s11`; shock variants follow the new band; the A-6 shipped label is 0.11 |
| Kit A-9 `SPEC.md`, `attacker.py` | The shock 0.06 to 0.11, edited by this session, which had read the engine: independence for that one number is not fresh |
| Kit `rt_consistency.py` (A-3) | Repointed to the live references (correction, section 5) |
| Kit `test_weekly_preview.py` | The structural-band test now has 7 variants; its P(win) range is recomputed on the new band |

## 3. The sweep on today's rosters (`shock-fit-2026-11-16/sweep.json`)

Baseline within 3 SE of its own 10k reference on both seeds (16.78 / 16.15 against 16.34 / 15.98); MC SE 0.54 points per seed; engine 56230e9.

**weekly_availability is FRAGILE:** -0.8 (healthy at the old 0.88) / -0.3 (healthy at the unfloored fit (0.78)) / -2.6 (risk at the old 0.75) / +1.4 (risk at the unfloored fit (0.56)); headline title share 16.5% ± 0.5 (MC) within that band. Sweep of 2026-11-16, engine 56230e9.

| Constant | Variants | Tier |
|---|---|---|
| TEAM_WEEK_SHOCK | +1.6 (no shock) / +0.7 (old 0.06) / -1.1 (0.13) | SENSITIVE |
| PCT_MIX_INFL | +0.5 / -0.8 | ROBUST |
| GAMES_PER_WEEK | -0.4 / +0.4 | ROBUST |
| BENCH_WEIGHT | 0.0 / 0.0 | ROBUST |

Cross-check, exact: "shock at the old 0.06" gives 17.70 / 16.55, the tier sweep's baseline to the hundredth.

## 4. Finding: the model's weekly level runs 10% low since the tier change (flagged, not changed)

Weeks 1-4, every team-week, actual divided by modelled over the seven counting categories:

| Engine | Mean actual / model | SD | Shock fit | Shock relative to the level |
|---|---|---|---|---|
| Tiers 0.88 / 0.75 | 1.0006 | 0.119 | 0.1069 | 0.1068 |
| Tiers 0.80 / 0.65 (live) | 1.1027 | 0.131 | 0.1177 | 0.1067 |

EVIDENCE: the refit, the same `fit_constants` code on season/daily b35ad98, the engine patched both ways.

The tiers are right player by player (the 11-16 fit: healthy players play 77.9% of team games). Yet on 0.88 the team-week totals matched exactly, and on 0.80 they run 10% under.

INFERENCE, not tested: a player's missed games are partly filled by bench players in Yahoo's daily lineups, and the weekly model's daily-fill weights do not raise the bench enough when availability falls. The old 0.88 hid that.

The shock is unaffected (the last column). What it affects is the level of every team's counting-category means, and so how wide the simulated category edges are. The headline's direction is unclear (INFERENCE).

## 5. Correction to a record from earlier today

Section 9 of `after-report-2026-11-16-availability-tiers.md` reported A-3 (card vs simulator) on the new engine as max gap 0.023 / 0.026. `rt_consistency.py` reads the simulator side from a reference file by name, and that name still pointed at `_w17r_av0` (0.88 / 0.75, shock 0.06). So that record compared the new card with the old engine's seasons. It was caught here: two re-runs gave identical numbers although the engine had changed. A row is in `report/corrections-log.md`.

A-3 on matching references:

| Engine (card and seasons the same) | Max gap | Mean gap | Rank agreement |
|---|---|---|---|
| Tiers 0.80 / 0.65, shock 0.06 (`_t8065`) | 0.030 / 0.031 | 0.008 | 1.0 |
| Tiers 0.80 / 0.65, shock 0.11 (`_t8065_s11`, live) | 0.084 / 0.086 | 0.021 | 0.993 |

**Finding (flagged, not changed):** the card's expected category wins carry no shock term, so with the shock at 0.11 they state edges about 2.5 times wider than the seasons realize. The order of teams barely moves. The decision card and the waiver checks rank on that measure.

## 6. The attacks re-run (`run_attacks.py --check`: PASS, 11 of 11 CURRENT, engine files ecb60cb)

| Attack | Result |
|---|---|
| A-1, A-2 | Exact; unchanged |
| A-3 | Section 5 |
| A-4 | 0.162 / 0.162 tied categories per matchup (was 0.177 / 0.180) |
| A-5 | Baseline 23.28 / 22.38 within 3 SE of 22.90 / 22.98 |
| A-6 | Jalen Johnson for Durant positive everywhere (smallest +0.67). Draymond Green for Braun still conditional (no shock: -0.18 / +0.67); +0.47 / +1.75 at the shipped 0.11. The shock-0.06 row reproduces the previous shipped record to the hundredth |
| A-7 | 53 = 53 |
| A-8 (draft sweep) | Baseline within 3 SE of 22.53 / 22.55; TEAM_WEEK_SHOCK FRAGILE (+5.1 / +2.8 / -1.1) |
| A-9 | Every exact section PASS; seasons max abs z 1.74 |
| A-10 | 4 of 4 live checks PASS (brief headline recomputed on the live engine: `brief_headline_2026-11-12_t8065_s11.json`) |
| A-11 | Rule's pick last in 24 of 24 seed-runs; the top two still within 0.11 (25.88 / 25.77) |

Old records are kept beside the new ones as `*_pre-2026-11-16-shock.json`; each attack's history row in `scripts/redteam/attacks.json` says what changed.

## 7. Bounds

Out of scope by design: any change for the two findings (sections 4 and 5); the Monday fit record, which the morning run writes.

In scope and unverified: none.

## 8. Decisions for the owner

1. **Merge the deck PR, then the kit PR, on your word.**
2. **The 10% level error (section 4).**
   - (a) Test the backfill reading: measure, per team-week, how much of the counting totals came from players beyond the modelled starters, then decide a fix.
   - (b) Raise GAMES_PER_WEEK or the bench weight to absorb the gap. Cheaper, but it hides the cause.
   - (c) Leave it: the shock is unaffected and the order of teams barely moves.
3. **The card's missing shock term (section 5).**
   - (a) Add the shock's variance to the card's category edges, so the card and the seasons agree again.
   - (b) Leave the card as a ranking measure and say so on it.

## 9. Provenance

One Claude Code session on 2026-11-16 (session model A), on the owner's order above. Records beside this report: `shock-fit-2026-11-16/sweep.json` and `sweep.log`. Re-verify: `python3 scripts/redteam/run_attacks.py --check` (expect 11 CURRENT on a deck whose engine files last changed at ecb60cb); `python3 scripts/redteam/check_bands.py --report <this> --sweep report/after-reports/shock-fit-2026-11-16/sweep.json`.
