# A-9 specification — the weekly H2H category simulator

You are re-implementing a fantasy-basketball simulator **from this document alone**. Do not
read any other file in either repository except `fixture.json` beside this one. In particular
you may not open `arena.py`, `hoops.py`, `co_gm.py`, `weekly_preview.py`, `draft-deck.html`, any
`check_parity*`, or any existing result JSON. If something below is ambiguous, choose the
most natural reading, and **list every such choice** in your output. Do not guess what some
other code does.

League: 12 teams, 9 categories, head-to-head weekly, Yahoo "H2H each category".

## 0. Data

`fixture.json` has:
- `rosters`: `{seat: [player, ...]}` for 12 seats. Each player has `player` (name), `positions`
  (list drawn from PG, SG, SF, PF, C), `note` (free text), `z_sum` (a number), and per-game
  `fg_pct, fga, ft_pct, fta, tpm, pts, reb, ast, stl, blk, tov`.
- `notes`: every distinct note string in the player pool.
- `hash_vectors`: `[name, k, salt]` triples.

Categories, in this order: `FG%, FT%, 3PTM, PTS, REB, AST, ST, BLK, TO`. The counting
categories map to columns as follows: 3PTM→tpm, PTS→pts, REB→reb, AST→ast, ST→stl, BLK→blk,
TO→tov. For TO, **lower is better**. For every other category, higher is better.

## 1. Note tag and weekly availability

The **tag** of a note is the note lowercased and cut at the first whitespace character or
`(`. Everything from there on is prose for humans and must be ignored. An empty note gives an
empty tag.

`a` is a player's expected share of a full week's games. It is decided from the tag alone,
with the first matching rule winning:

1. the tag starts with `out-` (season-ending, unsigned, retired or overseas): **0.0**, the
   player is excluded. This tier order mirrors the ranking engine's availability rule.
2. the tag contains `mild`: **0.79**
3. the tag ends with `-recovery`: **0.0**
4. the tag ends with `-risk`, or equals `risk` or `inj-risk`: **0.75**
5. the tag contains `recovery`: **0.0**
6. the tag contains `risk`: **0.75**
7. anything else: **0.88**

The order is deliberate: a risk tag followed by a parenthetical mentioning recovery is a
risk, because the parenthetical is not part of the tag.

## 2. Deterministic hash

`h(s, k, salt)` returns a float in [0, 1). It must be bit-exact. Work in unsigned 32-bit
arithmetic, where `imul(a, b) = (a*b) mod 2^32`, `^` is XOR, and `>>` is a logical shift:

```
h = 2166136261 ^ imul(k, 2654435761) ^ imul(salt, 2246822519)
for each UTF-16 code unit c of s (little-endian pairs; non-ASCII names hash by code unit):
    h = h ^ c
    h = imul(h, 16777619)
h = h ^ (h >> 15);  h = imul(h, 2246822507)
h = h ^ (h >> 13);  h = imul(h, 3266489909)
h = h ^ (h >> 16)
return h / 4294967296
```

## 3. Daily-fill start rate (per roster)

Lineups are set daily. Ten slots per day, in this order: PG, SG, G (PG or SG), SF, PF, F (SF or
PF), C, C, Util, Util. A Util slot takes anyone.

For one roster, simulate `K = 32` trial weeks, `k = 0..31`. For each player in each trial:
- Draw the games this week from `u = h(name, k, 1)`: 2 if `u < 0.08`, 3 if `u < 0.63`, 4 if
  `u < 0.98`, else 5.
- Draw that many distinct days from 0..6, **without replacement**. Day weights are
  `W = (1.3, 0.7, 1.4, 0.8, 1.5, 0.9, 1.4)`. For game `j = 0, 1, ...`, compute
  `r = h(name, k, 10 + j) × (sum of W over the days still available)`. Walk the available days
  in ascending order, accumulating their weights, and pick the first day where `r < cumulative`.
  If none qualifies, take the last available day. Remove the picked day.
- The player **plays** on the picked day `d` if `h(name, k, 20 + d) < a`, where `a` comes from
  §1. Count each played game.

Then, for each day, order the players who play that day by `z_sum` descending, ties by name
ascending. Each player in turn claims a slot:
- the first still-open **specific** slot (any slot except Util) whose eligible positions
  intersect his positions;
- otherwise, the first still-open Util slot;
- otherwise, nothing.

A claim counts one **start**.

A player's weight `w` is `starts / played` over the 32 trials, or **1.0** if he never played.

## 4. Team weekly model

For one roster, with each player's `w` from §3 and `a` from §1, and `g = 3.5·a`,
`gvar = 3.5·a·(1−a)`:
- For each counting category with column `x`:
  - `mu += w · x · g`
  - `var += w · ((x · CV)² · g + x² · gvar)`
  - with per-game CV: PTS 0.30, REB 0.35, AST 0.40, 3PTM 0.55, ST 0.70, BLK 0.75, TO 0.50.
- `FGM = Σ w·fg_pct·fga·g`, `FGA = Σ w·fga·g`. Then `p = FGM / FGA`, using FGA = 1 if it
  is 0. `mu[FG%] = p` and `var[FG%] = 1.15² · max(p(1−p), 1e-4) / FGA`, using FGA = 1 if it
  is 0. FT% is built the same way from ft_pct and fta.

## 5. Head-to-head category probability

For team models `m` and `o`, category `c`: `d = (mu_m − mu_o) / sqrt(var_m + var_o)`. If the
square root is 0, use 1e-9. `P = Φ(d)`, the standard normal CDF, computed as
`0.5·(1 + erf(d/√2))`. For TO, the probability is `1 − P`.

`pwins(m, opponents)` is the sum over opponents and over the 9 categories of that
probability, divided by the number of opponents: expected categories won per week against
an average opponent.

## 6. Season Monte Carlo (stochastic; compared within sampling error, not exactly)

Fixed per team: the §4 models, and `σ_c = sqrt(var_c)`, using 1e-6 where that is 0.

One season:
- **17 regular weeks.** Each week, shuffle the 12 teams uniformly and pair them as
  positions (0,1), (2,3), …, (10,11).
- **A matchup (a, b).** Draw a shared games shock for each team, `s_a, s_b ~ Normal(1, 0.06)`.
  For each category `c`:
  - the mean is `mu_c` multiplied by the team's shock if `c` is a counting category, and is
    not multiplied for FG% and FT%;
  - draw `X_a ~ Normal(mean_a, σ_a,c)` and `X_b ~ Normal(mean_b, σ_b,c)`;
  - `a` wins the category if `X_a > X_b`, or `X_a < X_b` for TO.

  `wins_a` is the count, 0–9.
- **Standings** add up category records. Team `a` gets `wins_a`, team `b` gets `9 − wins_a`.
- **Seeding** sorts by record, highest first, breaking ties uniformly at random. The top 8
  make the playoffs.
- **Playoffs.** One matchup per round. Quarterfinals: seed 1 v 8, 4 v 5, 2 v 7, 3 v 6.
  A matchup is won with 5 or more categories, otherwise the opponent advances. The four
  winners are **reseeded** by original seed: best v worst, second v third, higher seed listed
  first. Then the final.

Report each team's title share and playoff share.

## 7. What to output

Write `attacker_out.json` with:
- `availability`: `{note: a}` for every string in `notes`
- `hash`: a list of `[name, k, salt, value]` for every hash vector
- `weights`: `{seat: {player: w}}`
- `models`: `{seat: {category: [mu, var]}}`
- `pcat`: `{"<seatA>|<seatB>": {category: probability}}` for every ordered pair A ≠ B
- `pwins`: `{seat: value}`, each seat against the other 11
- `season`: `{"seasons": N, "seed": <your seed>, "title": {seat: share}, "playoffs": {seat: share}}`
  with N = 20000
- `choices`: a list of every interpretation you had to make, one string each

Use full float precision. Do not round.
