#!/usr/bin/env python3
"""Writer for after-report-2026-10-15-co-gm-status.md — figures read from records (RULES.md rule 6)."""
import collections, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(KIT, "report", "after-reports", "after-report-2026-10-15-co-gm-status.md")
rd = lambda n: open(os.path.join(HERE, n), encoding="utf-8").read()
def counts(t):
    ran = int(re.search(r"Ran (\d+) tests?", t).group(1)); m = re.search(r"FAILED \((?:failures=(\d+))?(?:, )?(?:errors=(\d+))?\)", t)
    return ran, (int(m.group(1) or 0) + int(m.group(2) or 0)) if m else 0
rec = json.load(open(os.path.join(KIT, "data", "status", "status_2026-10-15.json"), encoding="utf-8"))
rows = rec["rows"]; tiers = collections.Counter(r["tier"] for r in rows)
mine = [r for r in rows if r["seat"] == 10]
first3 = [r for r in mine if r["player"] in ("Kevin Durant", "Kyrie Irving", "Miles Bridges")]
assert len(first3) == 3 and "ModuleNotFoundError" in rd("test_status_feed_red.txt")
g = counts(rd("test_status_feed_green.txt")); vr = counts(rd("test_gates_runner_verify_red.txt")); vg = counts(rd("test_gates_runner_verify_green.txt"))
red_gate = [l.strip() for l in rd("status_check_red.txt").splitlines() if l.strip().startswith("-")]
green_gate = rd("status_check_green.txt").splitlines()[0]
mine_rows = "\n".join(f"| {r['player']} | {r['slot']} | {r['yahoo_status']} | {r['tier']} | {r['availability']:.2f} | {r['receipts'][0]['captured']}, `{os.path.basename(r['receipts'][0]['file'])}` | not read ({r['espn']['detail'].split(':')[0]}) |" for r in mine)
rn = rd("rn_section.md").rstrip() + "\n"
text = f"""# After-report — 2026-10-15: Session 1 item 4 — the status feed: Yahoo letters into availability tiers with dated receipts; ESPN attempted and denied

**Owner request:** Session 1 item 4: "a daily script reading Yahoo status letters (owner paste or fetch) and the ESPN injury feed into availability tiers with dated receipts; gate: a Q/O-flagged row at availability 1.00 with no receipt fails the build. Record Durant, Irving, Miles Bridges first." The owner said "Proceed" on the Council's order: 5, then 4 (Yahoo half), then 6, then 7.

**What changed.**
- Kit: `scripts/status_feed.py`, `scripts/test_status_feed.py`, and `data/status/status_2026-10-15.json`.
- Kit: `scripts/gates.py --verify --report` and a new test, for a defect found during item 5 (below).
- No line, tag, team, price or placement changed. Nothing published.

**Method (stated to the owner before the run).**
- Tiers: Yahoo **O → out 0.00**, **Q → questionable 0.50**, no letter → healthy 1.00. An unknown letter is refused.
- Owner overrides (`data/status_overrides.json`) win and must carry a dated receipt.
- ESPN's injury feed is attempted on every run and its outcome recorded.

Pull window: 2026-10-15 → 2026-10-15 (Yahoo letters from the owner's rosters page captured 2026-10-15; ESPN attempted {rec['espn']['attempted']}, denied).

## 1. Roster changes

None.

## 2. The owner's flagged players, recorded first

| player | slot | Yahoo | tier | availability | receipt | ESPN |
|---|---|---|---|---|---|---|
{mine_rows}

League-wide: {len(rows)} flagged rows ({dict(tiers)}).

**ESPN (ATTEMPTED-FAILED):** `{rec['espn']['detail']}`. The environment's network policy denies `site.api.espn.com`. Until the owner allows it, availability rests on Yahoo's letters alone.

## 3. Red first, and the gate seen both ways

- **Tests:** `test_status_feed_red.txt` failed (ModuleNotFoundError). `test_status_feed_green.txt`: {g[0]} tests, {g[1]} failing.
- **The real gate, driven red:** today's file with Durant forced to 1.00 and his receipt removed returns `{red_gate[0] if red_gate else ''}` and exits 1 (`status_check_red.txt`).
- **Green on today's file:** `{green_gate}`.
- **Defect found during item 5 (item 1's tool):**
  - **What happened:** a command chain stopped before the item-5 gates ran, and `gates.py --verify` passed item 2's stale `gates.json`. The verifier never checked *which* report a record covered.
  - **Fix:** `--verify --report R` now refuses a record whose inputs do not include R.
  - **Tests:** `test_gates_runner_verify_red.txt` ({vr[0]} tests, {vr[1]} error); `test_gates_runner_verify_green.txt` ({vg[0]} tests, {vg[1]} failing).
  - **Item 5's own gates:** these were then run for real and passed before its merge.

## Watchlist

- The 0.50 tier for Q is a prior, not a measurement. Item 7's calibration ledger will grade it against games actually played.
- With the network closed, an injury reported after the owner's last paste is invisible until the next paste.

## Open-item receipts

| item | query run (2026-10-15) | dated finding |
|---|---|---|
| (this item) | Yahoo letters from the owner's page; ESPN injury feed attempted, denied by the environment | status file written; pool unchanged |
| Brandon Ingram, Kristaps Porzingis, Kawhi Leonard, Cam Thomas, Jaden Ivey, Jeremy Sochan, Lonzo Ball, Rob Dillingham, Bennedict Mathurin, Ryan Rollins | the lock report (`after-report-2026-10-14-lock.md`, receipts dated 10/14) | as recorded there; not re-queried (the network is blocked) |

{rn}
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
"""
open(OUT, "w", encoding="utf-8").write(text); print("wrote", os.path.relpath(OUT, KIT))
