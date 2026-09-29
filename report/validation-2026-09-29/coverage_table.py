#!/usr/bin/env python3
"""Build the control-coverage table of the 2026-09-29 validation report from the
harness result file (arena/results/full_dom_check_2026-09-29.json in the deck
repo, copied here as full_dom_check_2026-09-29.json). Every row is read from the
recorded assertions — nothing is typed from memory.

    python3 report/validation-2026-09-29/coverage_table.py [result.json]
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "full_dom_check_2026-09-29.json")
d = json.load(open(path, encoding="utf-8"))
res = {a["id"]: a for a in d["all"]}

# control -> the assertion ids that exercise it (ids are the harness's own)
CONTROLS = [
    ("Teams / Rounds / Your slot inputs (echo)", ["S1.echo-default", "S1.echo-updates-on-input"]),
    ("Start draft — invalid config refused", ["S1.invalid-teams", "S1.invalid-rounds", "S1.invalid-slot", "S1.invalid-start-stays-on-setup"]),
    ("Start draft — LIVE", ["S2.start-log", "S2.feed-title-live", "S2.advance-hidden", "S2.strip-pick1", "S2.countdown-pick1", "S2.placeholder-pick1"]),
    ("Start draft — MOCK (cast seated, AI advances to your pick)", ["S4.start-log", "S4.auto-advance-to-owner", "S4.cast-seated"]),
    ("LIVE / MOCK mode buttons", ["S1.mode-mock-pressed", "S1.mode-live-pressed"]),
    ("Punt chips (9) at setup", ["S1.punt-chips-9", "S1.punt-chip-toggles-on", "S1.punt-chip-toggles-off", "S3.start-log-punt", "S3.strip-punt"]),
    ("⟳ Daily sweep panel", ["S1.sweep-panel-opens", "S1.sweep-panel-names-last-sweep", "S1.sweep-panel-closes"]),
    ("Import draft_state.json (chooser, invalid JSON, missing keys, valid)", ["S1.import-button-opens-chooser", "S1.import-invalid-json", "S1.import-missing-keys", "S1.import-valid-enters-draft"]),
    ("Export draft_state.json (download)", ["S1.export-download", "S1.export-logged", "S2.export-24", "S4.export-has-cast"]),
    ("Copy state JSON (clipboard)", ["S2.copy-state"]),
    ("Reset draft (two-click confirm)", ["S1.reset-armed", "S1.reset-clears", "S1.reset-remembers-slot"]),
    ("Pick feed — Log button and Enter", ["S2.enter-key-logs", "S2.replay-complete"]),
    ("Pick feed — numbered correction (24- Name)", ["S2.numbered-fix", "S2.numbered-fix-restore"]),
    ("Pick feed — live hint under the box (D54-1)", ["S2.hint-late-rule-from-round-9"]),
    ("Undo last pick", ["S2.undo", "S2.relog-after-undo", "S4.undo-x19-back-to-owner-turn", "S4.undo-owner-pick"]),
    ("Insert at #… (toggle, empty input, insert)", ["S2.insert-bar-opens", "S2.insert-empty-warns", "S2.insert-empty-warn-visible-after-next-render", "S2.insert-shifts"]),
    ("Resync (toggle, empty paste, rebuild)", ["S2.resync-bar-opens", "S2.resync-empty-refused", "S2.resync-empty-refusal-visible-after-next-render", "S2.resync-rebuilds"]),
    ("Advance AI picks (MOCK)", ["S4.advance-button"]),
    ("Stage pick / Draft them buttons on the card", ["S4.take-label", "S4.draft-them-auto-advances", "S4.mock-complete"]),
    ("TARGET / BOARD LEAN button on the card", ["S2.target-button-click"]),
    ("Tabs (Best available, Draft board, Rosters, Matrix, Head-to-head)", ["S2.tab-best", "S2.tab-boardtab", "S2.tab-rosters", "S2.tab-matrix", "S2.tab-vs"]),
    ("Best available — Pos filter", ["S2.filter-pos-C"]),
    ("Best available — Find box and Enter (drafted lookup)", ["S2.filter-search", "S2.search-enter-drafted"]),
    ("Best available — Show N", ["S2.show-12"]),
    ("Best available — Lens select (val / ΔECW / fit / mkt)", ["S2.lens-val-sorted", "S2.lens-decw-sorted", "S2.lens-fit-header", "S2.lens-mkt-sorted"]),
    ("Best available — category header clicks, 3-cat cap, drill, × chip", ["S2.cat-lens-PTS", "S2.cat-lens-3", "S2.cat-lens-cap", "S2.cat-lens-drill", "S2.cat-chip-remove"]),
    ("Best available — Reset", ["S2.best-reset"]),
    ("Best available — row click stages the pick", ["S2.row-click-stages"]),
    ("Best available — ⛔ DO NOT DRAFT marker", ["S2.veto-row-marked"]),
    ("Head-to-head opponent select", ["S2.vs-options", "S2.vs-table"]),
    ("Tooltip (data-tip hover)", ["S2.tooltip"]),
    ("Draft-complete state (strip, countdown, placeholder, card)", ["S1.draft-complete-strip", "S1.draft-complete-countdown", "S1.draft-complete-placeholder", "S1.draft-complete-card", "S1.draft-complete-roster-13", "S2.final-strip", "S2.final-card", "S2.final-roster-13", "S4.complete-log"]),
]
NUMBERS = [
    ("Status strip: pick #, round, seat on the clock, your next, roster n/13, N available (= availablePool)", ["S2.strip-pick1", "S2.strip-at-24", "S2.strip-at-48", "S2.strip-at-72", "S2.strip-at-96", "S2.strip-at-120", "S2.strip-at-144"]),
    ("Decision card top-5 = rankCard(decwScores) over the owner pool, every owner turn", ["S2.card-matches-engine-all-turns", "S2.owner-turns-13"]),
    ("Exactly one 🎯 on the card; veto never on the card", ["S2.veto-never-on-card"]),
    ("Draft board grid: 13 rounds × 12 seats, snake placement", ["S2.grid-head", "S2.grid-rows", "S2.grid-snake"]),
    ("Rosters tab: 12 rosters, kept-cat value = Σ totalValue", ["S2.rosters-12", "S3.rosters-kept-excludes-punt"]),
    ("Matrix: every cell = categoryRanks totals, Kept column, rank note; punted column struck", ["S2.matrix", "S3.matrix-punted-struck"]),
    ("Head-to-head: You/Them = rosterTotals, lead flags, W–L note, consistent with the matrix; punted label", ["S2.vs-table", "S3.vs-punted-label"]),
    ("Mkt column = marketRanks over the baked Yahoo prices", ["S2.mkt-column-matches-marketRanks"]),
    ("Lens orderings monotone (val, ΔECW, fit, mkt, cat lens, drill)", ["S2.lens-val-sorted", "S2.lens-decw-sorted", "S2.lens-fit-header", "S2.lens-mkt-sorted", "S2.cat-lens-PTS", "S2.cat-lens-drill"]),
    ("Your roster list and my-pick logging at all 13 owner turns", [f"S2.turn#{k}" for k in (10, 15, 34, 39, 58, 63, 82, 87, 106, 111, 130, 135, 154)]),
    ("MOCK: typed my: pick logs, D54-1 gap warning, input memory across Undo", ["S4.typed-pick-logs-and-advances", "S4.gap-warn-on-off-card-pick", "S4.undo-x19-back-to-owner-turn"]),
]

def row(label, ids):
    got = [res.get(i) for i in ids]
    missing = [i for i, g in zip(ids, got) if g is None]
    fails = [i for i, g in zip(ids, got) if g is not None and not g["ok"]]
    n = len([g for g in got if g is not None])
    verdict = "PASS" if not fails and not missing else ("FAIL" if fails else "NOT RUN")
    detail = "; ".join(f"{i}: {json.dumps(res[i]['detail'], ensure_ascii=False)[:110]}" for i in fails)
    if missing: detail += (" " if detail else "") + "not recorded: " + ", ".join(missing)
    return f"| {label} | {n} | {verdict} | {detail} |"

print(f"Harness run: {d['at']} on `{d['deck']}` — {d['assertions']} assertions, {d['failed']} failed, {len(d['pageErrors'])} page errors, crash: {bool(d.get('harnessCrash'))}.")
print()
print("| control | assertions | verdict | failing assertion (detail) |")
print("|---|---|---|---|")
for label, ids in CONTROLS: print(row(label, ids))
print()
print("| displayed number / computation | assertions | verdict | failing assertion (detail) |")
print("|---|---|---|---|")
for label, ids in NUMBERS: print(row(label, ids))
covered = {i for _, ids in CONTROLS + NUMBERS for i in ids}
rest = [a["id"] for a in d["all"] if a["id"] not in covered]
print()
print(f"Assertions not in either table ({len(rest)}): " + ", ".join(f"{i} {'PASS' if res[i]['ok'] else 'FAIL'}" for i in rest))
lv = d["notes"].get("live", {})
print(f"Live replay notes: substitutions {lv.get('substitutions')} (a mock-54 opponent name already taken by the card's earlier pick, replaced by the cheapest available), TARGET button present at {lv.get('targetSeen')} of 13 owner turns, LAST CALL rows {lv.get('lastCallSeen')}; clipboard grant: {d['notes'].get('clipboardGrant')}; copy path: {d['notes'].get('copyPath')}.")
