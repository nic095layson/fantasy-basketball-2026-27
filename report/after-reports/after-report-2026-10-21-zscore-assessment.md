# Z-scores and the Season tool: what decides what, the pasted claims checked, the measurements and the 2025-26 game logs — 2026-10-21 (night)

Pull window: 2026-10-21 → 2026-10-21. No league or market pull. Two attempts to read the G-score paper failed (§4), and one web search read the paper's listing. You then uploaded the paper (about 21:21Z). It is pinned at `data/source/papers/rosenof-2307.02188v5.pdf`, with its pdfplumber text and 17 page-cited quotes checked against that text (`.quotes.json`). Everything else is local: the pinned 10/21 Flaim league state, the 10/21 season pool, and the deck's `weekly_matchups_2025-26.csv`. Then, on your "Run it", one pull: Basketball-Reference's 2025-26 regular-season game logs for 169 players (169 pages, all HTTP 200, finished 21:45Z). The data in those logs runs 2025-10-21 → 2026-04-12; the weeks used are stated in §4.

**Owner's request** (2026-10-21, verbatim): "A thought for you to consider- if our computation model is heavily favoring zscores in projections for the Season tool, may we need to consider a pivot or adjustment?" This was followed by a pasted summary arguing that z-scores are not the most efficient way to win 9-category leagues. The summary cites Reddit, Medium and arXiv 2307.02188, and names G-scores, category-win-probability boards and Hashtag-style adjusted z-scores.

Your decisions on the assessment (clicked, about 21:05Z):
- direction: **"Measure first"**;
- adjustment, if one follows: **"Fit the weekly variance first"**.

Then, at about 21:20Z:
- D-ZS-1: **"Stress-test, then game logs"**;
- D-ZS-2: **"I'll paste/upload the paper"**, which you did.

Then, after the paper:
- D-ZS-1 step 2: **"Run it"** (the 2025-26 game-log pull);
- D-ZS-2: **"Build it"**: the G-score column beside z on the season board, the paper's Table 5 formula, no ranking change, test-first, on its own PR. It is not in this PR; see the decision sheet.

**What was analyzed.**
- Kit main `9b00fc1` and deck main `80eecdf`.
- `scripts/season_board.py`, `daily_brief.py`, `co_gm.py`, `week_matchup.py`.
- The deck's `arena/arena.py`.
- `data/league_settings.json`.
- The red-team sweep record `redteam-2026-10-19/sweep.json`.
- Basketball-Reference's 2025-26 game logs for the board's top 180 (169 found), checked against the deck's pinned ESPN 2025-26 per-game file.

**Method.** A question about method gets an assessment and options (`CLAUDE.md`); nothing was built. Each measurement's method was stated to you before it ran. Both measurement scripts were run twice with identical output.

**Headline.**
- **The Season tool is not one z-score model.**
  - Z-scores rank players: the board, the daily lineup, streaming, the waiver shortlist, and the week card's drop candidates.
  - The decisions that win weeks use head-to-head category-win probabilities built on weekly means and variances: the waiver swap value and the title odds.
- **The waiver shortlist hides nothing today.** On 10/21, scoring every pooled free agent (153) instead of the top 40 by z finds the same two positive swaps. Both sit inside the shortlist.
- **The weekly spread is the open issue.** Your team's actual week-to-week spread in per-game rates (2025-26, 17 weeks) was 1.53 to 2.46 times what the model's weekly variance implies, before allowing for unequal players. The cause is not yet split among five sources:
  - per-game variance;
  - unequal players;
  - schedule mix;
  - roster changes;
  - games-played errors.
  
  If the model's weekly spread is too narrow, its win probabilities are too confident.
- **Your title odds barely care.** The stress test raised the per-game variation to ×1.5 and ×2.0. The title share moved −0.36 and −0.61 points against a baseline of 23.77% / 24.20%, with the simulation's own noise at 0.54. ROBUST at every step (§4).
- **The G-score paper (your upload) supports the claim on its own terms.** In its simulated head-to-head leagues, a G-score drafter against a field of Z-score drafters won 21.4% of each-category seasons, against an 8.33% baseline (p. 6–7). Its 2022-23 table weights steals at 44% of their Z-score value and assists at 75% (p. 9). A G-score column needs each player's week-to-week variance, which the game-log pull you chose would supply. It is not built; it waits for your go.
- **The game logs are in (step 2), and they agree with the paper.** Over 22 weeks of 2025-26 and 157 of the board's top 180:
  - steals get the smallest weight, 0.47 of their z, against the paper's 44%;
  - the other eight run 0.55 to 0.73, in nearly the paper's order (§4, Measurement 3);
  - the per-game variation is 24% to 43% wider than the hand-set values (`arena.CV`). That is inside the ×1.5 the stress test found ROBUST for your title odds, and it explains part, not all, of the weekly spread gap above.
  - The figures came from the second parse; the first kept 1,183 header rows (§5).

## 1. Roster changes

None. No pool row, line, tag or roster changed.

## 2. What decides each Season-tool output (read from the code, 2026-10-21)

| output | mechanism | head-to-head aware | where |
|---|---|---|---|
| season board ranking | z-scores over an iterated top-156, availability-adjusted | no | `scripts/season_board.py:35` |
| daily lineup | z-sum value, filled by position | no | `scripts/daily_brief.py:141`, `:146` |
| streaming | z value per game x games left | no | `scripts/daily_brief.py:180` |
| waiver shortlist | top 40 pooled free agents by z value | no; it limits the next row | `scripts/co_gm.py:126-130` |
| waiver swap value | expected categories won per week: per-category win probability from weekly mean and variance (`_pcat`, normal model) | yes | `scripts/co_gm.py:116-123`; deck `arena.team_week_model` |
| title odds | simulated seasons of category-by-category weekly matchups; standings by category record | yes | deck `arena.simulate_seasons`, `arena/mocks/league_sim.py` |
| week card category leader | point estimates of week totals, no probability | partly | `scripts/week_matchup.py:24` (M5) |
| week card pickups | projected category wins gained; drop candidates by z value | partly | `scripts/week_matchup.py:25-27` (M6, M7) |

## 3. The pasted claims, checked

| claim | grade | evidence |
|---|---|---|
| z-scores are not the most efficient method for head-to-head 9-cat | SUPPORTED as the paper states it; "most efficient" goes beyond it | Primary source, your upload (`data/source/papers/rosenof-2307.02188v5.pdf`):<br>p. 4: "G-scores are the same as Z-scores except the denominators are modified to add period-to-period variance".<br>p. 6–7: G against a Z field won "21.4% of simulated Each Category seasons"; Table 6 aggregate "0.4% 0.5% 32.5% 21.4%".<br>The paper's own limits: p. 8, "choosing players via a static ranking list is fundamentally sub-optimal", and expected categories won "is not a perfect proxy".<br>The same author's later H-scoring paper (arXiv 2409.09884) reports a dynamic method beating static lists; that one was not read. |
| a 5-4 week is worth the same as 9-0 | wrong for this league's regular season; right for its playoffs | `data/league_settings.json` scoring_type "Head-to-Head - Categories"; the deck simulator builds standings from category records (`arena.py`: "Yahoo H2H-each-cat standings accumulate the CATEGORY record"); a playoff matchup is won with 5 or more categories |
| skewed categories let one elite blocker inflate his z | PARTIAL, plausible | standardizing over the top 156 limits it; the size on our board was not measured (did not check) |
| linear z-scores bury poor free-throw shooters | PARTIAL | volume-weighted FT% impact is the standard team contribution (`hoops.zscores`). Punting is a strategy question already tested in the draft rooms: it beat the plain card in 2 of 9 turns, averaging −0.32 (D75-2), and stayed advice-only. |
| better tools use category-win probability | supported; the kit already does this for swap values and title odds | `co_gm._pcat`, `arena.simulate_seasons` |

## 4. Measurements (your "Measure first")

**Measurement 1: does the z shortlist hide good swaps?** (`zscore-assessment-2026-10-21/waiver_shortlist_audit.py`, record `.json`)
- Inputs: the 10/21 league state from the pinned Flaim pull (`league_state_2026-10-21_flaim.json`, with Drummond) and the 10/21 season pool (`pool_season_2026-10-21.csv`).
- Both sets were scored by the brief's own `co_gm.waiver_pairs`, with the current variance.

| measure | value |
|---|---|
| pooled free agents (not rostered, availability above 0, not do-not-draft) | 153 |
| shortlist (top 40 by z value) | 40 |
| adds with a positive best swap, all 153 scored | 2 |
| of those, inside the shortlist | 2 |
| hidden by the shortlist | 0 |
| best: Bobby Portis for Christian Braun | +0.0231 categories a week (z-rank 5) |
| second: Julian Champagnie for Christian Braun | +0.0019 (z-rank 2) |
| your expected categories won per week now | 5.2595 |

**Measurement 2: is the model's weekly spread in the right range?** (`zscore-assessment-2026-10-21/weekly_spread_check.py`, record `.json`)
- Data: your 2025-26 regular-season weekly totals, weeks 1–18 except 17 (two calendar weeks): 17 weeks, 41.7 games played a week on average.
- Per counting category: the spread (coefficient of variation) of the per-game rate across weeks, against the model's implied spread CV / √gp, assuming equal players. Equal players gives the model's smallest possible spread, so the ratio is the most the model could be off.

| category | model's per-game variance (hand-set) | model's implied weekly rate spread | observed weekly rate spread | observed / model |
|---|---|---|---|---|
| PTS | 0.30 | 0.046 | 0.089 | 1.91 |
| REB | 0.35 | 0.054 | 0.129 | 2.38 |
| AST | 0.40 | 0.062 | 0.110 | 1.77 |
| 3PTM | 0.55 | 0.085 | 0.145 | 1.70 |
| ST | 0.70 | 0.108 | 0.166 | 1.53 |
| BLK | 0.75 | 0.116 | 0.286 | 2.46 |
| TO | 0.50 | 0.077 | 0.144 | 1.86 |

The observed spread contains five things:
- per-game noise, which `arena.CV` models;
- unequal players, which can only raise the model side;
- the week's schedule mix, i.e. which players' games make up the week (the model gives every player 3.5 games a week);
- roster changes during the season;
- games-played transcription error: the README says only week 1 has been checked against a screenshot.

So the result is that the model's weekly spread is narrower than observed, by at most these ratios. It is not a fitted `arena.CV`.

**Stress test (your "Stress-test, then game logs", step 1).** (`zscore-assessment-2026-10-21/sweep_cv_stress.json`, `.log`, `registry_cv_stress.json`)

Setup:
- the standing red-team sweep (`scripts/redteam/sweep.py`) on deck `80eecdf`;
- the 10/14 league draft rosters, pool v69;
- 6,000 seasons on each of seeds 2026 and 2027;
- the baseline lands within 3 standard errors of the 10k reference runs on both seeds.

Only the per-game variation (`arena.CV`) moved, through a scratch registry. The standing `sweep.json` and its gate are untouched.

| per-game variation | title share, seed 2026 / 2027 | mean shift | tier |
|---|---|---|---|
| as set (×1.0) | 23.77% / 24.20% | baseline | |
| ×1.2 | 22.88% / 24.20% | −0.45 | ROBUST |
| ×1.5 | 23.02% / 24.22% | −0.36 | ROBUST |
| ×2.0 | 23.23% / 23.52% | −0.61 | ROBUST |

The simulation's own noise is ±0.54 points. Up to ×2.0, which covers most of the gap measured above, the title odds stay within about one unit of that noise. The fit therefore matters for the size of swap values and for a G-score column, not for the title figure.

**The G-score paper (your upload).**
- *Before the upload:* WebFetch of arxiv.org failed (`getaddrinfo ENOTFOUND`, about 21:00Z), and `curl` to arxiv.org, export.arxiv.org and semanticscholar.org got no response (000).
- *The upload:* `data/source/papers/rosenof-2307.02188v5.pdf`, 17 pages, sha256 `e3b7151f84b7…`, read with pdfplumber page by page.
- *Definition (p. 4–5).* The G-score is the Z-score with each category's denominator widened from the spread of players' means (σ²) to σ² + κ·τ². Here τ² is the average week-to-week variance of a player's weekly line, and κ = 2N/(2N−1). The paper's simulation "approximated [κ] at 1" (p. 6).
- *Result (p. 6–7, Table 6), aggregate row:*
  - Z against a G field won 0.4% of most-categories seasons and 0.5% of each-category seasons;
  - G against a Z field won 32.5% and 21.4%;
  - the baseline is 1 in 12, or 8.33%.
- *Weights (p. 9, Table 8, 2022-23).* Each category's G-score as a fraction of its Z-score:

| steals | FG% | FT% | turnovers | points | blocks | rebounds | threes | assists |
|---|---|---|---|---|---|---|---|---|
| 44% | 56% | 58% | 62% | 65% | 68% | 69% | 72% | 75% |

- *What a G-score column here would need:* each player's week-to-week variance (τ) per category, from weekly lines. Season totals don't give it. The 2025-26 game logs you chose as step 2 would, aggregated to Yahoo weeks. Both sources answered HTTP 200 from here at about 21:30Z: Basketball-Reference game logs and the ESPN athlete game-log API. Measured in Measurement 3 below; the column itself is not in this PR.

**Measurement 3: the 2025-26 game logs (your "Run it", D-ZS-1 step 2).** (`zscore-assessment-2026-10-21/gamelogs/`: `pull_gamelogs.py`, `pull_manifest.json`, `gamelogs_2025-26.csv`, `q_ids.json`, `gscore_weights.py`, record `gscore_weights_2025-26.json`)

Method, stated to you before the run:
- **Players (Q).** The 10/21 season board's top 180, the pool its z-scores use. 169 have a 2025-26 Basketball-Reference id. The other 11 are not in that season's per-game table: Haliburton, Irving, Lillard, VanVleet, Boozer, Wilson, Lendeborg, Dybantsa, Peterson, Acuff, Wagler. Sensitivity: the top 156.
- **Weeks.** Monday to Sunday from 2025-10-27. The two All-Star-break weeks (2026-02-09 to 02-22) are left out, as are weeks the logs do not wholly cover: 22 weeks, 2025-10-27 to the week of 2026-04-06. Games of 10/21–10/26 fall before the first counted week. A player's week counts if he played, and he needs 10 or more counted weeks: 157 players (134 of the top 156).
- **Formula.** The paper's Table 5 on 2025-26 alone: σ is the spread of players' weekly means and τ the week-to-week spread (root-mean-square over players). FG% and FT% follow Table 5b exactly: the spread of players' shooting rates, and the weekly attempts-weighted rate gap. The league rate weights each player by his attempts (a_q read as μ_A(q)). That reading is INFERENCE: it matches the appendix's derivation, Σ μ_A(q)·μ_R(q) / Σ μ_A(q) = μ_R (p. 12), where the parser text is partly garbled. The weight is w = σ / √(σ² + κτ²), the paper's Table 8 column "G-score as fraction of Z-score", with κ = 26/25 from the league's 13 non-IL roster spots (`data/league_settings.json`).
- **Second outlet.** Each player's per-game means against the deck's pinned ESPN 2025-26 per-game file.

| category | σ² ours | σ² paper | τ² ours | τ² paper | weight ours (top 156) | paper, 2022-23 |
|---|---|---|---|---|---|---|
| ST | 1.20 | 1.01 | 4.10 | 4.2 | **0.47** (0.47) | 44% |
| FT% | 0.0079 | 0.009 | 0.0175 | 0.018 | **0.55** (0.56) | 58% |
| TO | 5.35 | 5.45 | 9.12 | 8.85 | **0.60** (0.59) | 62% |
| BLK | 1.80 | 2.35 | 2.77 | 2.7 | **0.62** (0.62) | 68% |
| PTS | 303.10 | 325.52 | 422.11 | 448.32 | **0.64** (0.63) | 65% |
| FG% | 0.0046 | 0.003 | 0.0061 | 0.007 | **0.65** (0.65) | 56% |
| REB | 45.78 | 52.01 | 55.18 | 57.55 | **0.67** (0.66) | 69% |
| 3PTM | 8.60 | 9.52 | 9.29 | 9.04 | **0.69** (0.69) | 72% |
| AST | 37.13 | 41.57 | 30.42 | 31.55 | **0.73** (0.73) | 75% |

- **Steals get the smallest weight,** as in the paper. That was the pre-set sanity check: had steals not been lowest, I would have stopped before any build.
- **Same order as the paper,** with FG% the exception: 0.65 against 56%. The reason is in the σ² column: shooting rates spread more across our top 180 in 2025-26 (0.0046) than across the paper's 2022-23 pool (0.003). The paper's other σ² and τ² sit close to ours, which checks that the script follows its definitions.
- **The top 156 gives the same weights** within 0.01.
- **Games per counted player-week:** 3.01 (SD 0.91, 3,067 player-weeks).
- **Checked against the data, not memory.**
  - 2025-10-27 is a Monday.
  - The logs hold no game from 2026-02-13 to 02-18, so both excluded weeks are All-Star-break weeks.
  - A separate recomputation of the steals weight (different week arithmetic, same definitions) gives σ 1.0971, τ 2.0249, w 0.4692, equal to the record.

**Per-game variation fit (`arena.CV`).** Pooled over Q's players with 20+ games, √(Σ n·var / Σ n·mean²) per category:

| category | hand-set `arena.CV` | fitted, 2025-26 | fitted / hand-set |
|---|---|---|---|
| PTS | 0.3 | 0.395 | ×1.32 |
| REB | 0.35 | 0.445 | ×1.27 |
| AST | 0.4 | 0.496 | ×1.24 |
| 3PTM | 0.55 | 0.717 | ×1.3 |
| ST | 0.7 | 0.945 | ×1.35 |
| BLK | 0.75 | 1.072 | ×1.43 |
| TO | 0.5 | 0.668 | ×1.34 |

- **EVIDENCE.** The hand-set per-game variation is 24% to 43% below 2025-26's.
- **INFERENCE.** In Measurement 2's equal-player bound, per-game noise alone at these values accounts for a ratio of about ×1.24 to ×1.43. The observed gap was ×1.53 to ×2.46. The rest belongs to the other four causes named there (schedule mix the largest candidate).
- **The stress test covers it.** ×1.5 was ROBUST for your title odds. Under the fitted values, swap values would move toward zero, since a wider variance pulls each category's win probability toward 50%. That is INFERENCE from the formula; not measured.
- **Nothing was changed** (D-ZS-3 below).

**Second-outlet check.** 169 of 169 players agree with ESPN: games played exact, and nine per-game stats within 0.15.
- The checker was tested on two planted faults, an extra game and 10 points removed from one of 64 games, and caught both.
- Its resolution: a single-game error smaller than about 0.15 × games played (about 10 points over 65 games) would pass.

**Pull receipts.**
- 169 pages, all HTTP 200, paced 3.5 seconds apart.
- The raw pages are kept outside the repo, with each page's sha256 in `pull_manifest.json`. The ID page's sha256 is in `q_ids.json`.
- 10,332 game rows.

**Structural bands, carried for the gate.** This report quotes no simulator figure. The standing sweep's bands are carried verbatim:
- TEAM_WEEK_SHOCK is FRAGILE: +2.7 (no shock) / −3.6 (shock doubled).
- weekly_availability is FRAGILE: −2.7 (no in-sim injury discount) / +0.5 (harsher risk tier 0.65) / −1.5 (healthy plays 0.95) / +1.0 (healthy plays 0.80).

## 5. Errors and surprises, stated plainly

- **The first parse of the game logs kept 1,183 header rows.** Basketball-Reference repeats its column headers inside the game-log table, about seven times a player. The parser's comment said it skipped them, but its test didn't catch them: it checked the date and points cells, and a header row holds "Date" and "PTS" there.
  - Found when the first weights run stopped on the date "Date". No figure came from that parse.
  - Fixed in the parser: a game row needs an ISO date. The CSV was rebuilt from the same saved pages (`pull_gamelogs.py --reparse`), each page checked against its manifest sha256: 10,332 rows.
  - Planting the same fault in the ESPN check fails it (games played 66 against 65).
- **One check ran in the wrong folder.** While checking the G-column change end to end, my copy command failed (`rsync` is not installed here). The commands after it were joined with `;`, so the morning chain ran in this checkout instead of the copy.
  - It rewrote eleven 10/21 records (season lines, board, status, brief, deck page) and wrote one new file.
  - All were restored from this branch's commit, and the new file deleted, before anything was committed. `git status` afterwards shows only this update's files. The deck repo was untouched.
  - The run was then repeated in a proper copy.
- **I changed the percentage method before the run.** The weights script as first written measured FG% and FT% on the impact quantity the kit's z uses (makes − league rate × attempts). That is not the paper's Table 5b. Re-reading Table 5 from the pinned text before the run, I switched to 5b exactly. No figure came from the first version.

- **I first described the spread gap too narrowly.** I said it showed that the hand-set variance was too small. Checking it found a cause the model omits: the schedule mix (one week your big man plays four games, another week two), on top of per-game noise. The record and this report now say the gap is not attributable to `arena.CV` alone.
- **A label in the standing registry says "variance" but means CV.** Its `arena.CV` variants are labeled "per-game variance ×0.8 / ×1.2", but the sweep multiplies the per-game variation (CV, the standard-deviation scale), not the variance. Flagged, not changed; the scratch registry here labels its variants "per-game CV". Not fixing it now is deliberate (scope).
- **The paste's "5-4 = 9-0" claim does not hold for your regular season.** It is true in the playoffs, where a matchup is won with 5 or more categories.

## Watchlist

- **The win probabilities may be too confident** until the weekly spread is fitted. That affects the brief's swap values and the title odds, not the z-ranked board.
- **The waiver shortlist** hid nothing on 10/21. The result is one day under the current variance; a wider variance can change which marginal swaps rate positive.

## Open-item receipts

| item | status | receipt |
|---|---|---|
| z-score question (owner 10/21) | **ASSESSED**; measured on your "Measure first" | §2–§4 |
| G-score board | **NOT BUILT**: the paper's formula could not be read here (§4) | WebFetch and curl records |

The flagged-name receipts are carried forward from the lock report, except Jeremy Sochan's, which the pickups build re-queried on 10/21 (`after-report-2026-10-21-pickups-file.md` §1). The rest were not re-queried for this build (did not check).

| item | query run (2026-10-14) | dated finding |
|---|---|---|
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report, same day (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried for this build (did not check) |
| Jeremy Sochan | 2026-10-21: "Jeremy Sochan Trail Blazers waived October 2026", then "Jeremy Sochan clears waivers signs" (the second returned February 2026 items only) | waived by Portland Sat 2026-10-17, non-guaranteed camp deal; no claiming team found; on no NBA roster in ESPN's 10/21 feed (§1, `roster_drift_2026-10-21.json`) |

## Repeat-name market check

This build did not change the draft-room deck page, which is still deck `80eecdf` (checked with `git -C ../yahoo-fantasy-basketball log -1`, clean tree, 2026-10-21), page sha256 6a5cefea4921. The GAUNTLET report replayed it today. Its table stands, carried here verbatim.

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

1. **D-ZS-1: the weekly-variance fit.** Done: step 1 (ROBUST up to ×2.0) and step 2 (you said "Run it"; Measurement 3). It closes here.
2. **D-ZS-2: G-score comparison column.** You said "Build it".
   - Comparison only: the paper's Table 5 on the board's own projections and pool, τ from Measurement 3, beside z on the season board. No ranking changes.
   - It is built test-first as a separate change for its own PR, and is not in this one. How it ships is yours to choose, because this session may push only to its one branch.
3. **D-ZS-3 (new): the per-game variation fit.** The hand-set `arena.CV` is 24% to 43% below 2025-26 (Measurement 3).
   - (a) Set `arena.CV` to the fitted values. This is a deck engine change: red-first, the standing sweep and title odds re-run and restated, the registry status moved from declared band to measured.
   - (b) Keep the hand-set values, record the fit, and widen the registry's sweep band for `arena.CV` to cover ×1.24 to ×1.43.
   - (c) Leave it.
   - Recommendation (a), on its own deck PR. The values are measured on the very players the tool scores, and the title odds are insensitive in that range, so the change mostly corrects swap sizes.
   - Default if silent: (c), flagged here.
3. **Unchanged:** z-scores keep ranking the board, lineup and streaming until a fit or a G-score comparison shows a difference.

## Bounds

**Out of scope by design.**
- Any change to a line, tag, constant or tool.
- The draft-room deck page.
- The Reddit and Medium posts in the paste (did not check). Nothing here rests on them.

**In scope and unverified.**
- How the five sources split the observed spread: UNVERIFIABLE with this file, which holds one team's totals with no weekly rosters.
- How the title odds respond to a wider variance: measured (the stress test above).
- The skew effect on the board: did not check.
- The G-score formula: read from your upload (above), and recomputed on 2025-26 for our pool (Measurement 3).
- That 2025-26's week-to-week variance carries into 2026-27 (an assumption): UNVERIFIABLE until this season's weeks accrue.
- The per-game variation fit counts players with 20+ games; the weights count players with 10+ counted weeks. Both cuts were stated before the run.
- The paper's later companion (H-scoring, arXiv 2409.09884): did not check.

## Provenance

- **Produced by** session `session_01QjgeRdpDaWgSJmGKRG8fTU` on 2026-10-21, about 20:55–22:00Z.
- **Governors.** plan-gate was loaded for the question, and its block was emitted before the reading and before each measurement. adversarial-verify was loaded before delivery and found the schedule-mix omission in §5. After a context compaction during the game-log pull, plan-gate was loaded again and its block emitted before the weights ran; adversarial-verify was loaded again before this update was delivered.
- **Sources.**
  - The code at the commits above.
  - `data/league_settings.json`.
  - The deck's `weekly_matchups_2025-26.csv` and its README.
  - The search index listing of arXiv 2307.02188 ([v5 page](https://arxiv.org/html/2307.02188v5)).
  - The paper itself, uploaded by you and pinned with page-cited quotes.
  - The stress-test record.
- **Re-verify.**
  - `python3 report/after-reports/zscore-assessment-2026-10-21/waiver_shortlist_audit.py`
  - `python3 report/after-reports/zscore-assessment-2026-10-21/weekly_spread_check.py`
  - `python3 scripts/redteam/sweep.py --registry report/after-reports/zscore-assessment-2026-10-21/registry_cv_stress.json --out <file>`
  - `python3 report/after-reports/zscore-assessment-2026-10-21/gamelogs/gscore_weights.py` (two runs, byte-identical record)
  - `python3 report/after-reports/zscore-assessment-2026-10-21/gamelogs/pull_gamelogs.py <dir of saved pages> --reparse`. This needs the pages; without them, a fresh fetch writes a new manifest to compare sha256s against.

## In plain language

The tool uses z-scores to rank players, but when it judges a waiver swap or your title chances, it plays out head-to-head weeks category by category. That's what the article recommends, and we already do it.

I checked whether ranking by z-score made the waiver scan miss a good pickup today. It didn't: scoring all 153 free agents found the same two small gains.

The bigger finding is how swingy real weeks are. Last season your team's weeks varied more than the model assumes: about twice as much, at most. Part of that is schedule luck the model ignores. If the model underestimates swings, it's a bit overconfident about who wins a category. That's the fit you picked, and the next step is choosing its data.

Then I made the model's weekly swings twice as wild and re-ran your title odds. They barely moved: from about 24% to about 23.4%, which is inside the simulation's own noise. So your title chances don't hinge on this setting.

The paper you uploaded backs the G-score idea on its own terms. In its simulated leagues, a G-score drafter beat a room of z-score drafters far more often than chance: 21.4% of seasons won, where 8.3% is chance. It counts steals at less than half their usual weight, because steals swing so much week to week. To build a G-score column for our players I need each player's week-to-week swings. That comes from last season's game logs, the step you chose next, which waits for your word.

Then I pulled last season's game logs for the board's top players and measured how much each category swings week to week, exactly as the paper defines it. The answer matches the paper closely. Steals swing the most against how much players differ, so a G-score would count them at about half (0.47); assists swing the least (0.73). The same data shows the model's per-game swings are set about a quarter to two-fifths too low in every category. The title odds don't care at that size, so whether to adopt the fitted values is a separate choice for you (D-ZS-3). The G-score column you said to build is done as its own change, kept out of this one; how it ships is your call.
