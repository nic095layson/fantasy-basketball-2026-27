#!/usr/bin/env python3
"""One gate runner → gates.json (plan 2026-10-15 §4 D3; RULES.md rule 7).

A gate PASSES only when it exits 0 AND prints its PASS line; an exit 0 with an empty log
is a FAIL (the 10/15 repeat-name near-miss, plan §1). The verdict file records each gate's
command, exit code and PASS line, plus the sha256 of every input it judged, so --verify
refuses a gates.json that is failing, missing, or older than the files it vouches for.

Default gates for an after-report (the three report gates the kit's after-report contract
names): kit report/check_report.py, deck judgment_open_items.py --check-report, deck
repeat_market_check.py --check-report. Item-specific checks are added with --gate.

    python3 scripts/gates.py --report report/after-reports/X.md \\
        [--gate 'NAME::kit|deck::PASS_REGEX::COMMAND' ...] [--input PATH ...] \\
        [--out gates.json] [--deck ../yahoo-fantasy-basketball]
    python3 scripts/gates.py --quote [--out gates.json]     # PR-body block
    python3 scripts/gates.py --verify [--out gates.json]    # exit 1 unless PASS and fresh

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


def run_all(specs, inputs, root):
    gates = [run_gate(s) for s in specs]
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


def verify(path, root):
    """(ok, problems): the record exists, every gate PASSED, every input is unchanged."""
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
    ap.add_argument("--quote", action="store_true")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    root = os.path.dirname(os.path.abspath(a.out))

    if a.verify:
        ok, problems = verify(a.out, root)
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
        specs = report_gates(report, deck) + specs
        inputs = [report] + inputs
    if not specs:
        print("no gates: pass --report and/or --gate")
        sys.exit(2)
    rec = run_all(specs, inputs, root)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1)
        f.write("\n")
    print(quote(rec))
    sys.exit(0 if rec["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
