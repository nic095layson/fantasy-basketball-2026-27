#!/usr/bin/env python3
"""One gate runner → gates.json (plan 2026-10-15 §4 D3; RULES.md rule 7).

A gate PASSES only when it exits 0 AND prints its PASS line; an exit 0 with an empty log
is a FAIL (the 10/15 repeat-name near-miss, plan §1). The verdict file records each gate's
command, exit code and PASS line, plus the sha256 of every input it judged, so --verify
refuses a gates.json that is failing, missing, or older than the files it vouches for.

Default gates for an after-report (the three report gates the kit's after-report contract
names): kit report/check_report.py, deck judgment_open_items.py --check-report, deck
repeat_market_check.py --check-report. Item-specific checks are added with --gate. The claim
registry (scripts/check_claims.py --gate, D-CLAIM-1) runs last on every invocation unless
--no-claims. Every gate's verdict is also appended to the run-ledger (scripts/run_ledger.py).

    python3 scripts/gates.py --report report/after-reports/X.md \\
        [--gate 'NAME::kit|deck::PASS_REGEX::COMMAND' ...] [--input PATH ...] [--redteam SWEEP_JSON] \\
        [--out gates.json] [--deck ../yahoo-fantasy-basketball]
    python3 scripts/gates.py --quote [--out gates.json]     # PR-body block
    python3 scripts/gates.py --verify [--report R] [--out gates.json]  # exit 1 unless PASS, fresh, covering R

Exit codes: 0 PASS, 1 FAIL, 2 usage error.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_ledger  # noqa: E402

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK_DEFAULT = os.environ.get("DECK_REPO") or os.path.join(KIT, "..", "yahoo-fantasy-basketball")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def run_gate(spec):
    """Run one gate; PASS iff exit 0 and a line matches spec['pass_re']."""
    p = subprocess.run(spec["cmd"], cwd=spec["cwd"], capture_output=True, text=True)
    lines = (p.stdout + "\n" + p.stderr).splitlines()
    rx = re.compile(spec["pass_re"])
    hits = [ln.strip() for ln in lines if rx.search(ln)]
    pass_line = hits[-1] if hits else ""
    verdict = "PASS" if p.returncode == 0 and pass_line else "FAIL"
    why = "" if verdict == "PASS" else (
        f"exit {p.returncode}" if p.returncode != 0 else "exit 0 but no PASS line")
    return {"name": spec["name"], "cmd": " ".join(shlex.quote(c) for c in spec["cmd"]),
            "cwd": os.path.relpath(spec["cwd"], KIT) if os.path.isabs(spec["cwd"]) else spec["cwd"],
            "pass_re": spec["pass_re"], "exit": p.returncode, "pass_line": pass_line,
            "verdict": verdict, "why": why,
            "tail": [ln for ln in lines if ln.strip()][-3:]}


def run_all(specs, inputs, root, ledger=None):
    """Run every gate in order. With `ledger` (the run-ledger path; main passes run_ledger.LEDGER), each gate's
    verdict is appended as it finishes, so a later gate in the same run (check_claims) can read it."""
    gates = []
    for s in specs:
        g = run_gate(s)
        gates.append(g)
        if ledger:
            run_ledger.safe_record(g["name"], g["verdict"], g["pass_line"] or g["why"], ledger=ledger)
    rec = {
        "ran_at_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "inputs": {os.path.relpath(p, root): sha256(p) for p in inputs},
        "gates": gates,
        "verdict": "PASS" if gates and all(g["verdict"] == "PASS" for g in gates) else "FAIL",
    }
    try:
        rec["base_commit"] = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                                            capture_output=True, text=True).stdout.strip()
    except OSError:
        rec["base_commit"] = ""
    return rec


def verify(path, root, report=None):
    """(ok, problems): the record exists, every gate PASSED, every input is unchanged, and (with
    `report`) the record judged that report — a stale gates.json from an earlier item is refused."""
    try:
        with open(path, encoding="utf-8") as f:
            rec = json.load(f)
    except (OSError, ValueError) as e:
        return False, [f"no readable gates.json at {path}: {e}"]
    problems = []
    if rec.get("verdict") != "PASS":
        problems.append(f"verdict is {rec.get('verdict')!r}")
    if not rec.get("gates"):
        problems.append("no gates recorded")
    for g in rec.get("gates", []):
        if g.get("verdict") != "PASS" or g.get("exit") != 0 or not g.get("pass_line"):
            problems.append(f"gate {g.get('name')}: {g.get('why') or g.get('verdict')}")
    for rel, digest in rec.get("inputs", {}).items():
        p = os.path.join(root, rel)
        if not os.path.exists(p):
            problems.append(f"input {rel} missing")
        elif sha256(p) != digest:
            problems.append(f"input {rel} changed since the gates ran")
    if report is not None:
        rel = os.path.relpath(os.path.abspath(report), root)
        if rel not in rec.get("inputs", {}):
            problems.append(f"gates.json does not cover {rel}")
    return not problems, problems


def quote(rec):
    out = [f"gates.json — ran {rec.get('ran_at_utc')} on base {rec.get('base_commit', '')[:7]}"]
    for g in rec["gates"]:
        out.append(f"- {g['verdict']} · {g['name']} · exit {g['exit']} · "
                   f"{g['pass_line'] or '(no PASS line: ' + g['why'] + ')'}")
    for rel, d in rec.get("inputs", {}).items():
        out.append(f"- input {rel} sha256 {d[:12]}")
    out.append(f"verdict: {rec['verdict']}")
    return "\n".join(out)


def report_gates(report, deck):
    py = sys.executable
    return [
        {"name": "kit check_report", "cwd": KIT, "pass_re": r"^REPORT GATE: PASS",
         "cmd": [py, "report/check_report.py", report]},
        {"name": "deck judgment_open_items --check-report", "cwd": deck,
         "pass_re": r"^receipts check PASS", "cmd": [py, "scripts/judgment_open_items.py",
                                                       "--check-report", report]},
        {"name": "deck repeat_market_check --check-report", "cwd": deck,
         "pass_re": r"^REPEAT-NAME CHECK: PASS", "cmd": [py, "scripts/repeat_market_check.py",
                                                          "--check-report", report]},
    ]


def redteam_gates(report, sweep, deck):
    """The three standing red-team gates (post-mortem 2026-10-19 D-PM-1; scripts/redteam/): the constants
    registry against the live engine, the report quoting every FRAGILE band of the sweep record, and the attack
    list's records present and on the live engine."""
    py = sys.executable
    rt = os.path.join(KIT, "scripts", "redteam")
    return [
        {"name": "redteam constants", "cwd": KIT, "pass_re": r"^CONSTANTS CHECK: PASS",
         "cmd": [py, os.path.join(rt, "check_constants.py"), "--deck", deck]},
        {"name": "redteam bands", "cwd": KIT, "pass_re": r"^BANDS CHECK: PASS",
         "cmd": [py, os.path.join(rt, "check_bands.py"), "--report", report, "--sweep", sweep]},
        {"name": "redteam attacks", "cwd": KIT, "pass_re": r"^ATTACKS CHECK: PASS",
         "cmd": [py, os.path.join(rt, "run_attacks.py"), "--check", "--deck", deck]},
    ]


def claims_gate():
    """D-CLAIM-1 (b), owner "build council's fixes" 2026-10-21: the claim registry as a gate — it passes only when
    every claim's verdict equals its recorded `expected`, so a known-false claim does not block, a CHANGE does. Runs
    last, so its ledger_pass claims can read the rows this run's earlier gates just wrote."""
    return {"name": "kit check_claims --gate", "cwd": KIT, "pass_re": r"^CLAIM GATE: PASS",
            "cmd": [sys.executable, os.path.join(KIT, "scripts", "check_claims.py"), "--gate"]}


def audit_gates(report, replay=False, last=3):
    """Independent-audit adoption (owner 2026-10-21; library skill claude-core-skills independent-audit):
    claim receipts on the report — ADVISORY, it lists 'it runs / it changes nothing' sentences with no receipt and
    never fails the build (precision 3 of 7 on the kit's own 10/19–10/21 reports, below the 0.5 gate bar) — and,
    with replay=True (`--replay`), the Season Deck rebuilt and render-checked on the last `last` real mornings that
    produced a deck. Replayed on the real 10/21 records, the code before #152 and before #154 both FAIL."""
    ia = os.path.join(KIT, "scripts", "independent_audit")
    specs = [{"name": "claim receipts", "cwd": KIT, "pass_re": r"^CLAIM RECEIPTS: (PASS|ADVISORY)",
              "cmd": [sys.executable, os.path.join(ia, "claim_receipts.py"), report]}]
    if replay:
        specs.append({"name": "deck replay", "cwd": KIT, "pass_re": r"^REPLAY: PASS",
                      "cmd": [sys.executable, os.path.join(ia, "replay_gate.py"), "--last", str(last),
                              "--inputs", os.path.join(KIT, "report", "season", "deck_record_*.json"),
                              "--cmd", f"bash {os.path.join(KIT, 'scripts', 'replay_deck.sh')} {{input_date}}",
                              "--pass-re", r"^SEASON DECK: PASS"]})
    return specs


def parse_gate(text, deck):
    parts = text.split("::", 3)
    if len(parts) != 4 or parts[1] not in ("kit", "deck"):
        raise ValueError(f"--gate wants 'NAME::kit|deck::PASS_REGEX::COMMAND', got {text!r}")
    name, where, rx, cmd = parts
    return {"name": name, "cwd": KIT if where == "kit" else deck, "pass_re": rx,
            "cmd": shlex.split(cmd)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report")
    ap.add_argument("--gate", action="append", default=[])
    ap.add_argument("--input", action="append", default=[])
    ap.add_argument("--out", default=os.path.join(KIT, "gates.json"))
    ap.add_argument("--deck", default=DECK_DEFAULT)
    ap.add_argument("--redteam", metavar="SWEEP_JSON",
                    help="add the three red-team gates (constants, bands vs this sweep record, attacks)")
    ap.add_argument("--replay", action="store_true",
                    help="also rebuild and render-check the Season Deck on the last 3 real mornings (independent-audit, 2026-10-21)")
    ap.add_argument("--no-claims", action="store_true",
                    help="omit the claim-registry gate (it is on by default, D-CLAIM-1)")
    ap.add_argument("--ledger", default=run_ledger.LEDGER,
                    help="run-ledger to append each gate's verdict to ('' to skip)")
    ap.add_argument("--quote", action="store_true")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    root = os.path.dirname(os.path.abspath(a.out))

    if a.verify:
        ok, problems = verify(a.out, root, report=a.report)
        print("GATES VERIFY: PASS — gates.json is PASS and its inputs are unchanged" if ok
              else "GATES VERIFY: FAIL\n  " + "\n  ".join(problems))
        sys.exit(0 if ok else 1)
    if a.quote:
        with open(a.out, encoding="utf-8") as f:
            print(quote(json.load(f)))
        sys.exit(0)

    deck = os.path.abspath(a.deck)
    try:
        specs = [parse_gate(g, deck) for g in a.gate]
    except ValueError as e:
        print(e)
        sys.exit(2)
    inputs = [os.path.abspath(p) for p in a.input]
    if a.report:
        report = os.path.abspath(a.report)
        specs = report_gates(report, deck) + audit_gates(report, replay=a.replay) + specs
        inputs = [report] + inputs
    if a.redteam:
        if not a.report:
            print("--redteam needs --report (the bands check reads the report)")
            sys.exit(2)
        sweep = os.path.abspath(a.redteam)
        specs = specs + redteam_gates(report, sweep, deck)
        inputs = inputs + [sweep]
    if not specs:
        print("no gates: pass --report and/or --gate")
        sys.exit(2)
    if not a.no_claims:
        specs = specs + [claims_gate()]
    rec = run_all(specs, inputs, root, ledger=a.ledger or None)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1)
        f.write("\n")
    print(quote(rec))
    sys.exit(0 if rec["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
