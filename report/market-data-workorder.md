# Work order: external market data → Pass E (opened 2026-08-21)

**Status: EXECUTED 2026-08-21** (later same day) — see
`report/after-reports/after-report-2026-08-21-market.md` §1 and §4. The fresh
session picked up the network change exactly as predicted: statdunk,
hashtagbasketball AND basketball-reference all return 200 (verified by the §0
curl check, not assumed). Both feeds are landed under `report/market/`,
`report/market_join.py` produces the Pass E + §5.3 output at
`report/market-2026-27.md`, and the §3 unmatched-name gate is implemented and
caught 19 real defects. **Steps 1-4 of §3 are done; step 5 (`marketRanks`) is
deliberately NOT started** — it is the next session's job, driven red first.
**D1 is moot, not answered:** basketball-reference is reachable again, so pool
additions no longer need deck-plane projections as a base rate; four of the five
carried names were added from B-Ref lines fetched during the run.

Original status when opened: **BLOCKED on session start, not on information.** The owner reconfigured the
cloud environment's network access to Custom on 2026-08-21 and added the domains
below. Environment config is read once at session start, so the session that
requested the change could not use it. **A fresh session picks it up.**

This file exists because LESSONS.md lesson 10 is the house rule: the repo is the
only persistent layer, and a chat transcript is invisible to the next session.

## 0. First thing: verify the channel, do not assume it

```
for d in statdunk.com hashtagbasketball.com www.basketball-reference.com \
         site.api.espn.com www.nba.com; do
  printf "%-32s " "$d"; curl -sS -o /dev/null -w "%{http_code}" --max-time 20 "https://$d/"; echo
done
```

`000` or `EGRESS_BLOCKED` means still blocked — say so plainly and stop, do not
work around it. Four consecutive pulls (8/13, 8/18, 8/20, 8/21) reported this
channel as degraded; do not report it as fixed without running the check.

**Also verify artifact access specifically.** The deck lives at
`claude.ai/code/artifact/190e2c13-a19c-4239-8085-73230ef4eae0` and Claude reads
it through `*.frame.claudeusercontent.com`. If that domain was omitted from the
allowlist, artifact reads fail — which silently kills the **pre-republish orphan
check** (LESSONS.md lesson 21), the check that caught the 8/10 orphaned build.
Fetch the artifact before the first republish and confirm it still returns the
build-manifest. If it does not, tell the owner to add that domain before
republishing anything.

## 1. What the owner asked for

Two preliminary category-ranking sources, to be synthesized into the player data
and refined through October:

- https://statdunk.com/projections/categories?sport=nba&sort=val
- https://hashtagbasketball.com/fantasy-basketball-projections

**Owner decisions already taken (2026-08-21), do not re-litigate:**

1. **Access route: allowlist the domains.** Done.
2. **Use: Pass E sanity-check + arbitrage table, NOT a blend.** The board stays
   built from first principles. PROMPT.md §4.2 and the board's own header say it
   is built from profiles/ledger/age-curve, "not scraped rankings," and
   consensus is "consulted only as a sanity reference." Blending would be a
   method change requiring that header text to change in the same pass — the
   owner declined that. Join them as reference columns and surface
   disagreements for adjudication.

Note PROMPT.md **Pass E** already names "Hashtag Basketball's consensus" as the
intended aggregator, and **§5.3 Market arbitrage** already defines the output
(values = our rank 15+ picks ahead of ADP; fades = the reverse). This is a
designed-but-never-populated input, not a new idea.

## 2. The finding that reframes the job

The deck's `Mkt` column is **not** real market data. `marketRanks()` in
`docs/draft-deck.html`, mirrored by `arena.market_ranks()` in `arena/arena.py`,
computes it **from our own z-scores** with a points/3PM reweight (`MKT_W`) plus
seven hand-typed rookie pins (`MKT_PIN`).

Measured on the committed 2026-08-21 pool (238 live players):

```
Spearman rho(Mkt, our val board)   0.8842
rho with MKT_PIN removed           0.9028
median |Mkt - val| gap             17 ranks
players with |gap| >= 25           91 of 238
```

So the "market" the deck prices against is ~0.9-correlated with our own board
**by construction**. The only exogenous information in it is seven hand-entered
rookie ranks. It structurally cannot tell you the room disagrees with you.

This matters because `Mkt` is load-bearing, not cosmetic:

- it is the **default lens** on the Best-available board (`value="mkt" selected`)
- it drives the mock-draft AI personas (`rank = adp_w·marketRank + val_w·valueRank`)
- it drives `archetypeRead`'s "can likely wait a round" advice
- it drives `survPhi(MKT_RANK.get(name), pickN)` — the will-he-last-until-my-
  next-pick model

Real consensus data can replace a circular proxy in the single most load-bearing
"will he be there" calculation on the live-draft surface. That is a bigger prize
than a static comparison table, from the same data.

## 3. Sequencing — data first, integration second

`marketRanks` is mirrored across JS and Python and locked by `check_parity.py`
(72 df_hash vectors, 78 card orderings, 6 committed states). LESSONS.md lesson
19 is explicit that the newest code is the least-audited and that every fix
lands with a test that FAILED first. **Do not write the integration against a
schema you have not seen.**

1. Fetch both sources. Land them raw and dated under `report/market/`.
2. Normalize to the schema in §4 and commit that too, with provenance.
3. Join to the 220-row pool. **Name matching is the real risk** — this pool has
   18 shared surnames (Johnson ×4; Williams, Thompson, Murray, George ×3; …).
   An unmatched-name report is a **hard gate**, not a warning: refuse to
   proceed on silent partial joins. `hoops.norm()` already does accent/punct
   normalization and is the right primitive to reuse.
4. Produce the disagreement table: biggest per-game line differences vs
   Hashtag, biggest ordering differences vs Statdunk value. Owner adjudicates.
5. ONLY THEN consider `marketRanks`. Any change there is a cross-language
   change: update the JS, `arena.market_ranks`, and the `check_parity.py`
   fixtures together, driven red first.

## 4. Schema to normalize into

`report/market/hashtag-YYYY-MM-DD.csv`
```
player,team,pos,gp,mpg,fg_pct,fga,ft_pct,fta,tpm,pts,reb,ast,stl,blk,tov
```

`report/market/statdunk-YYYY-MM-DD.csv`
```
player,team,pos,rank,value[,per-category values if the page exposes them]
```

Both carry a companion row in `report/market/provenance.csv`:
`source,url,fetched_on,rows,notes`.

If a source's live columns differ from the above, **adjust the normalizer and
say so in the after-report** — do not silently drop columns to make it fit.

## 5. Repo state at the time this was written

- Both repos on branch `claude/fantasy-basketball-data-pull-687jyp`.
- Kit `8c9062b`, deck `b6afce4`. `origin/main` still at 8/18 on both
  (`161d1dd` / `a14d6a3`) — the PRs are open and unmerged.
- Open PRs, each carrying the 8/20 AND 8/21 pulls:
  kit nic095layson/fantasy-basketball-2026-27#7, deck
  nic095layson/yahoo-fantasy-basketball#12.
- Deck artifact live at `built: 2026-08-21`, pool `8bbd5bf918b1…`.
- Latest after-report: `report/after-reports/after-report-2026-08-21.md`.

## 6. Carried open items (from the 8/21 after-report §4)

- **Cam Whitmore** — Cleveland reportedly weighing a waive-and-stretch; his
  medical clearance from a DVT is unverified across two pulls. If waived and
  unsigned by October, delete the row rather than discount it again.
- **Mark Williams** — FIFTH consecutive quiet pull; the 58-GP discount has
  stood unexamined since 7/27. Treat as an October must-do.
- **Alex Sarr** — cross-plane severity mismatch: deck `inj-foot-risk` (×0.78)
  vs kit 72 GP. Same June 2026 surgery, different severity.
- **D1 (open owner decision)** — does a committed, gate-verified projection on
  the deck plane count as a sourced base rate for the kit? Answering yes closes
  the Peyton Watson gap (starting SF, $88M, missing from the kit for four
  pulls) and probably two or three of the other four missing names.
