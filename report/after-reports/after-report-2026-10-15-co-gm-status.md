# After-report — 2026-10-15: Session 1 item 4 — the status feed: Yahoo letters into availability tiers with dated receipts; ESPN attempted and denied

**Owner request:** Session 1 item 4: "a daily script reading Yahoo status letters (owner paste or fetch) and the ESPN injury feed into availability tiers with dated receipts; gate: a Q/O-flagged row at availability 1.00 with no receipt fails the build. Record Durant, Irving, Miles Bridges first." The owner said "Proceed" on the Council's order: 5, then 4 (Yahoo half), then 6, then 7.

**What changed.**
- Kit: `scripts/status_feed.py`, `scripts/test_status_feed.py`, and `data/status/status_2026-10-15.json`.
- Kit: `scripts/gates.py --verify --report` and a new test, for a defect found during item 5 (below).
- No line, tag, team, price or placement changed. Nothing published.

**Method (stated to the owner before the run).**
- Tiers: Yahoo **O → out 0.00**, **Q → questionable 0.50**, no letter → healthy 1.00. An unknown letter is refused.
- Owner overrides (`data/status_overrides.json`) win and must carry a dated receipt.
- ESPN's injury feed is attempted on every run and its outcome recorded.

Pull window: 2026-10-15 → 2026-10-15 (Yahoo letters from the owner's rosters page captured 2026-10-15; ESPN attempted 2026-10-15T19:49:25Z, denied).

## 1. Roster changes

None.

## 2. The owner's flagged players, recorded first

| player | slot | Yahoo | tier | availability | receipt | ESPN |
|---|---|---|---|---|---|---|
| Kevin Durant | SG | Q | questionable | 0.50 | 2026-10-15, `yahoo-starting-rosters-2026-10-20-view.pdf` | not read (URLError) |
| Kyrie Irving | Util | Q | questionable | 0.50 | 2026-10-15, `yahoo-starting-rosters-2026-10-20-view.pdf` | not read (URLError) |
| Max Strus | IL | O | out | 0.00 | 2026-10-15, `yahoo-starting-rosters-2026-10-20-view.pdf` | not read (URLError) |
| Miles Bridges | PF | Q | questionable | 0.50 | 2026-10-15, `yahoo-starting-rosters-2026-10-20-view.pdf` | not read (URLError) |

League-wide: 53 flagged rows ({'questionable': 46, 'out': 7}).

**ESPN (ATTEMPTED-FAILED):** `URLError: <urlopen error Tunnel connection failed: 403 Forbidden>`. The environment's network policy denies `site.api.espn.com`. Until the owner allows it, availability rests on Yahoo's letters alone.

## 3. Red first, and the gate seen both ways

- **Tests:** `test_status_feed_red.txt` failed (ModuleNotFoundError). `test_status_feed_green.txt`: 7 tests, 0 failing.
- **The real gate, driven red:** today's file with Durant forced to 1.00 and his receipt removed returns `- Kevin Durant: Yahoo Q at availability 1.00 with no dated receipt` and exits 1 (`status_check_red.txt`).
- **Green on today's file:** `STATUS GATE: PASS — status_2026-10-15.json: 53 flagged row(s), each tiered with a dated receipt`.
- **Defect found during item 5 (item 1's tool):**
  - **What happened:** a command chain stopped before the item-5 gates ran, and `gates.py --verify` passed item 2's stale `gates.json`. The verifier never checked *which* report a record covered.
  - **Fix:** `--verify --report R` now refuses a record whose inputs do not include R.
  - **Tests:** `test_gates_runner_verify_red.txt` (10 tests, 1 error); `test_gates_runner_verify_green.txt` (10 tests, 0 failing).
  - **Item 5's own gates:** these were then run for real and passed before its merge.

## Watchlist

- The 0.50 tier for Q is a prior, not a measurement. Item 7's calibration ledger will grade it against games actually played.
- With the network closed, an injury reported after the owner's last paste is invisible until the next paste.

## Open-item receipts

| item | query run (2026-10-15) | dated finding |
|---|---|---|
| (this item) | Yahoo letters from the owner's page; ESPN injury feed attempted, denied by the environment | status file written; pool unchanged |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried (the network is blocked) |

## Repeat-name market check

Rule (owner, 2026-10-08, D-RN-1): the card's 🎯 in 5+ of the graded mocks, replayed on this page (sha256 beb243ef57af), with 25+ places between the value rank and the market rank the card prints (or no Yahoo price), gets an outside-source check at every refresh. Replays: 33 of 33 mocks. Outside ranks: Yahoo Rank `yahoo-proj-2026-10-14.csv`, Hashtag `hashtag-2026-10-14.csv`, Rotoworld `rotoworld-9cat-2026-10-05.csv`, RotoBaller `rotoballer-2026-10-13.csv`. Cells: our per-game line against `yahoo-proj-2026-10-14.csv`, `hashtag-2026-10-14.csv`, `rotoballer-2026-10-13.csv` (outside all three; tolerance .005 on percentages, 5% with a 0.1 floor on counting stats). Spellings resolved through the kit's alias table (`build_market.py`, 6 players).

| player | 🎯 in mocks | value rank | market rank | Yahoo Rank | Hashtag | Rotoworld | RotoBaller | cells outside all three projections | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ty Jerome | 32 of 33 | 44 | 111 | 63 | 60 | 101 | 65 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| OG Anunoby | 23 of 33 | 32 | 67 | 58 | 56 | 43 | 45 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Cameron Johnson | 14 of 33 | 107 | 138 | 182 | 93 | 129 | 107 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Collin Gillespie | 12 of 33 | 101 | 182 | 100 | 125 | 148 | 155 | none | SOURCES SPLIT: 2 of 4 sit 25+ places on one side; the line holds |
| John Collins | 12 of 33 | 73 | 117 | 105 | 72 | 104 | 109 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Brandin Podziemski | 11 of 33 | 93 | 146 | 74 | 102 | 114 | 132 | none | SOURCES SPLIT: 1 of 4 sit 25+ places on one side; the line holds |
| Kawhi Leonard | 10 of 33 | 6 | 32 | 15 | 24 | 15 | 20 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Reed Sheppard | 10 of 33 | 92 | 179 | 89 | 117 | 126 | 129 | none | SOURCES SPLIT: 3 of 4 sit 25+ places on one side; the line holds |
| Jaden McDaniels | 7 of 33 | 62 | 90 | 42 | 67 | 86 | 59 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Devin Vassell | 6 of 33 | 114 | 139 | 122 | 130 | 125 | 125 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Immanuel Quickley | 5 of 33 | 67 | 94 | 65 | 73 | 79 | 84 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |
| Keegan Murray | 5 of 33 | 83 | 142 | 82 | 94 | 102 | 85 | none | SOURCES SPLIT: 0 of 4 sit 25+ places on one side; the line holds |

Near misses (the 🎯 in 5+ mocks, under 25 places): Jamal Murray (18 mocks, value 9, market 18); Derrick White (17 mocks, value 27, market 45); Lauri Markkanen (15 mocks, value 21, market 37); Tyrese Haliburton (13 mocks, value 7, market 12); Tyrese Maxey (11 mocks, value 5, market 9); Kel'el Ware (10 mocks, value 57, market 77); Tyler Herro (9 mocks, value 51, market 69); Karl-Anthony Towns (8 mocks, value 12, market 15); Miles Bridges (5 mocks, value 96, market 98).

The section above is carried from item 1's run today; the page is unchanged, and the gate replays it.

## Bounds

**Out of scope by design.**
- Changing any season-long injury tag on the pool.
- Fetching Yahoo directly, which needs a login.

**In scope and unverified.**
- The ESPN half: ATTEMPTED-FAILED (network policy).
- The Q tier's value: a stated prior.

**What this cannot see.**
- News after the owner's last paste.
- Minutes restrictions.
- Rest days that carry no letter.

## Decision sheet (owner disposes)

| id | decision question | default if silent |
|---|---|---|
| D-S1-6 | Allow `site.api.espn.com` in the environment's network settings (unblocks item 3 and ESPN here) | Yahoo letters only |
| D-S1-7 | The Q tier: 0.50, or a different value | 0.50 until calibration says otherwise |
| D-S1-8 | Daily paste of the Yahoo rosters page before the brief, or only when news breaks | daily on game days |
| earlier rows | carried in `OPEN.md` | carried |

## Provenance

This folder: `test_status_feed_red.txt`, `test_status_feed_green.txt`, `status_run.txt`, `status_check_green.txt`, `status_check_red.txt`, `test_gates_runner_verify_red.txt`, `test_gates_runner_verify_green.txt`, `rn_section.md`, this writer.

## In plain language

The tool now reads the little Q and O letters next to players on your Yahoo page. Questionable players count as a coin flip and players marked out count as zero, and each comes with a record of where and when it was seen.

- Durant, Irving and Bridges are questionable; Strus is out.
- If a flagged player is ever treated as fully healthy with no source, the check fails.
- ESPN's injury feed is still blocked by the network setting.
