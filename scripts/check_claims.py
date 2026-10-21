#!/usr/bin/env python3
"""Claim-vs-reality check (GAUNTLET 2026-10-21; Council 4-1, Expansionist).

The defect: in one night, three statements the system made ABOUT ITSELF turned
out to have no live counterpart --- the self-audit's "the weekly in-season pull
keeps it green" (nothing writes that file), the scheduled tasks' "the kit is
this session's own repository" (a fresh session has none), and D-INT-1's "run
the re-dating pass" (no such pass was ever written). Each read as a settled
fact in a document the owner relies on. Prose cannot be tested; a registry of
the same claims can.

report/claims.json holds one row per claim: what is asserted, where it is
asserted, and a MECHANICAL check. This script runs them and prints a verdict
per row. Exit 1 if any row is FALSIFIED.

    python3 scripts/check_claims.py [--json]

NOT wired into scripts/gates.py --- deliberately (Council 2026-10-21, Executor:
no new gate surface inside 12 hours of a scheduled run). Wiring it is an owner
decision, D-CLAIM-1.

Bounds of the two checks, stated because a checker nobody distrusts is the
dangerous kind:
  writer_exists  resolves the path to the local variables assigned to it in
                 each referencing .py, then looks for those variables reaching
                 a write (open(v,"w"/"a"), json.dump(...,v), csv.writer(v),
                 .to_csv(v)). A writer that builds the path by some other
                 route --- an f-string, a glob, a shell command --- is NOT
                 seen, so SUPPORTED is strong and FALSIFIED is "no writer
                 found by this method", not proof none exists.
  invoked_by     plain substring of the script's basename in the caller's
                 source. A caller that builds the name dynamically is not
                 seen. Same asymmetry.
Both are validated on a known-answer SUPPORTED row so the detector is never
trusted while failing everything (adversarial-verify rule 9).
"""
import argparse
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
REGISTRY = os.path.join("report", "claims.json")
KINDS = ("writer_exists", "invoked_by")
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv"}

_WRITE_PATTERNS = (
    r"open\(\s*{v}\s*,\s*['\"][wa]",
    r"json\.dump\([^)]*?,\s*open\(\s*{v}\s*,\s*['\"][wa]",
    r"csv\.writer\(\s*{v}\b",
    r"\.to_csv\(\s*{v}\b",
    r"{v}\.write_text\(",
    r"shutil\.(?:copy|move)\([^)]*,\s*{v}\b",
)


def _py_files(root):
    for base, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for n in sorted(names):
            if n.endswith(".py"):
                yield os.path.join(base, n)


def _read(path):
    try:
        return io.open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def writer_exists(root, relpath):
    """Does any .py under root write relpath? Returns verdict + evidence."""
    base = os.path.basename(relpath)
    writers, readers = [], []
    for f in _py_files(root):
        src = _read(f)
        if base not in src:
            continue
        rel = os.path.relpath(f, root)
        # variables that hold this path in this file
        names = set(re.findall(
            r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=.*" + re.escape(base), src, re.M))
        # argparse defaults: add_argument("--out", default=...<base>) means the
        # path reaches the writer as a.out / args.out, never as a module-level
        # name. Missing this idiom made the detector fail its own known-answer
        # control on 2026-10-21 (gates.py writes gates.json exactly this way).
        for dest in re.findall(
                r"add_argument\(\s*['\"]--([A-Za-z0-9_-]+)['\"][^)]*?default="
                r"[^)]*?" + re.escape(base), src):
            d = dest.replace("-", "_")
            names.update(("a.%s" % d, "args.%s" % d, "opts.%s" % d))
        names.add(re.escape(base))
        wrote = False
        for v in names:
            vpat = v if v.startswith(re.escape(base)[:3]) else re.escape(v)
            for pat in _WRITE_PATTERNS:
                if re.search(pat.format(v=vpat), src):
                    wrote = True
                    break
            if wrote:
                break
        (writers if wrote else readers).append(rel)
    return {
        "kind": "writer_exists", "target": relpath,
        "verdict": "SUPPORTED" if writers else "FALSIFIED",
        "writers": sorted(writers), "readers": sorted(readers),
        "detail": ("written by " + ", ".join(sorted(writers))) if writers
        else ("no writer found; %d file(s) reference it, all read-only: %s"
              % (len(readers), ", ".join(sorted(readers)) or "none")),
    }


def invoked_by(root, script_basename, caller_relpath):
    """Is script_basename named in caller_relpath's source?"""
    caller = os.path.join(root, caller_relpath)
    src = _read(caller)
    if not src:
        return {"kind": "invoked_by", "target": script_basename,
                "caller": caller_relpath, "verdict": "FALSIFIED",
                "detail": "caller %s not readable" % caller_relpath}
    hit = script_basename in src
    return {
        "kind": "invoked_by", "target": script_basename,
        "caller": caller_relpath,
        "verdict": "SUPPORTED" if hit else "FALSIFIED",
        "detail": ("%s names %s" % (caller_relpath, script_basename)) if hit
        else ("%s never names %s" % (caller_relpath, script_basename)),
    }


def load_registry(root):
    path = os.path.join(root, REGISTRY)
    return json.load(io.open(path, encoding="utf-8"))["claims"]


def run(root):
    out = []
    for row in load_registry(root):
        c = row["check"]
        if c["kind"] == "writer_exists":
            res = writer_exists(root, c["path"])
        elif c["kind"] == "invoked_by":
            res = invoked_by(root, c["script"], c["caller"])
        else:
            res = {"kind": c["kind"], "verdict": "FALSIFIED",
                   "detail": "unknown check kind"}
        res.update(id=row["id"], claim=row["claim"],
                   asserted_in=row["asserted_in"],
                   expected=row.get("expected", "SUPPORTED"))
        res["as_expected"] = res["verdict"] == res["expected"]
        out.append(res)
    return out


def exit_code(results):
    return 1 if any(r["verdict"] == "FALSIFIED" for r in results) else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    res = run(KIT)
    if a.json:
        print(json.dumps(res, indent=1))
    else:
        bad = [r for r in res if r["verdict"] == "FALSIFIED"]
        print("CLAIM CHECK: %d claim(s), %d FALSIFIED"
              % (len(res), len(bad)))
        for r in res:
            print(" - [%s] %s :: %s" % (r["verdict"], r["id"], r["claim"]))
            print("     asserted in %s" % r["asserted_in"])
            print("     %s" % r["detail"])
        print("CLAIM CHECK: %s" % ("FAIL" if bad else "PASS"))
    return exit_code(res)


if __name__ == "__main__":
    sys.exit(main())
