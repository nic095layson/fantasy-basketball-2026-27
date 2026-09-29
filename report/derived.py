#!/usr/bin/env python3
"""Input provenance for the kit's derived artifacts (drift fix D4, 2026-09-29).

The 2026-09-29 validation found that every dated analysis in report/ read the
CURRENT pool when re-run, so its numbers moved as the pool grew (the 8/24
league projection: 65 category wins became 64; the 9/16 market statistics:
n=214 became n=225). Nothing recorded which pool a number came from. This
module gives every generating script two things:

  * a STAMP — one trailing line in each Markdown/text output naming every
    input file it read, the first 16 hex of that file's sha256, its row
    count, and either the commit the inputs came from or the generation
    date. CSV outputs carry no stamp (a comment line would break their
    readers — the deck build reads yahoo-*.csv); their sibling .md carries it.
  * an AS-OF mode — `--as-of <YYYY-MM-DD | commit-ish>` reads the inputs
    from git at that point instead of the working tree. A date resolves to
    the last commit on or before 23:59:59 UTC of that day (commit times in
    this repo mix +0000 and -0700 offsets, so the day boundary is stated in
    UTC). The stamp records the resolved commit, so the same command
    reproduces the same bytes on any later day.

A dated script re-run without --as-of first looks for the stamp in its own
committed output and pins to that commit, so `yahoo_market.py 2026-09-15`
reproduces the committed 9/15 files instead of re-scoping them to today's
pool. `--live` forces the working tree (the deliberate re-scope). The gate
report/check_derived.py re-runs every registered artifact at its own pin and
fails on any byte of difference — the check_parity.py of the derived layer.

One input can be pinned to a different commit than the rest
(`--pin FILE=COMMIT`, shown in the stamp as `(at <sha>)`): the 8/24 market
build read the 220-row pool and the 8/24 raw snapshots that landed in the
SAME commit that completed the pool to 234, so its pool pins to that
commit's parent.
"""
import atexit
import csv
import datetime
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

KIT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
_STAMP_RE = re.compile(r"^_Inputs: .*_$")
_PIN_RE = re.compile(r"as of commit ([0-9a-f]{7,40})")
_FILEPIN_RE = re.compile(r"(\S+) sha256 [0-9a-f]{16} \d+ (?:rows|lines) \(at ([0-9a-f]{7,40})\)")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _git(repo, *args):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout


def resolve(spec, repo=KIT):
    """Full commit sha for a date (end of that day, UTC) or a commit-ish."""
    if _DATE_RE.match(spec):
        sha = _git(repo, "rev-list", "-1", f"--until={spec} 23:59:59 +0000", "HEAD").strip()
        if not sha:
            raise SystemExit(f"derived: no commit on or before {spec}")
        return sha
    return _git(repo, "rev-parse", "--verify", f"{spec}^{{commit}}").strip()


def commit_date(sha, repo=KIT):
    return _git(repo, "log", "-1", "--format=%cs", sha).strip()


def pin_from(path):
    """(commit, {file: commit}) recorded in a committed output's stamp, or None."""
    if not os.path.exists(path):
        return None
    last = ""
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                last = line.strip()
    m = _PIN_RE.search(last) if _STAMP_RE.match(last) else None
    if not m:
        return None
    return m.group(1), {f: c for f, c in _FILEPIN_RE.findall(last)}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rows(path):
    """(count, unit): data rows for a CSV, lines otherwise."""
    if path.endswith(".csv"):
        with open(path, encoding="utf-8", newline="") as f:
            n = sum(1 for _ in csv.reader(f)) - 1
        return max(n, 0), "rows"
    with open(path, encoding="utf-8") as f:
        return sum(1 for _ in f), "lines"


class Inputs:
    """Resolves input paths (working tree or a git commit) and records what
    was read for the stamp. `relpath` is always relative to the repo root."""

    def __init__(self, as_of=None, repo=KIT, script=None, pins=None):
        self.repo = repo
        self.commit = resolve(as_of, repo) if as_of else None
        self.pins = {f: resolve(c, repo) for f, c in (pins or {}).items()}  # per-file overrides
        if self.pins and not self.commit:
            raise SystemExit("derived: --pin needs --as-of")
        self.script = script or os.path.basename(sys.argv[0])
        self.read = []          # (label, sha256, count, unit, commit-or-None)
        self._tmp = None

    @property
    def mode(self):
        return f"as of commit {self.commit[:7]} ({commit_date(self.commit, self.repo)})" if self.commit \
            else f"working tree, generated {datetime.date.today().isoformat()}"

    def commit_for(self, relpath):
        return self.pins.get(relpath) or self.pins.get(os.path.basename(relpath)) or self.commit

    def _materialize(self, relpath):
        if self._tmp is None:
            self._tmp = tempfile.mkdtemp(prefix="derived-")
            atexit.register(shutil.rmtree, self._tmp, True)
        sha = self.commit_for(relpath)
        dst = os.path.join(self._tmp, relpath)
        if not os.path.exists(dst):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            blob = subprocess.run(["git", "-C", self.repo, "show", f"{sha}:{relpath}"],
                                  capture_output=True)
            if blob.returncode != 0:
                raise SystemExit(f"derived: {relpath} does not exist at {sha[:7]}")
            with open(dst, "wb") as f:
                f.write(blob.stdout)
        return dst

    def path(self, relpath):
        """Absolute path to read `relpath` from, recorded for the stamp."""
        p = self._materialize(relpath) if self.commit else os.path.join(self.repo, relpath)
        at = self.commit_for(relpath)
        self._record(os.path.basename(relpath), p, at if at != self.commit else None)
        return p

    def external(self, abspath, label):
        """A file outside this repo (the deck plane's pool): working tree only."""
        if self.commit:
            raise SystemExit(f"derived: {label} lives outside the kit; as-of mode cannot pin it")
        self._record(label, abspath, None)
        return abspath

    def listdir(self, reldir):
        """Names in `reldir` (working tree or the pinned commit's tree)."""
        if not self.commit:
            return os.listdir(os.path.join(self.repo, reldir))
        out = _git(self.repo, "ls-tree", "--name-only", f"{self.commit}:{reldir}")
        return out.split()

    def _record(self, label, p, at):
        if any(r[0] == label for r in self.read):
            return
        n, unit = rows(p)
        self.read.append((label, sha256(p), n, unit, at))

    def stamp(self):
        parts = [f"{label} sha256 {h[:16]} {n} {unit}" + (f" (at {at[:7]})" if at else "")
                 for label, h, n, unit, at in self.read]
        return "_Inputs: " + " · ".join(parts) + f" · {self.mode} · by {self.script}_"


def add_args(parser):
    """The shared CLI: --as-of / --live (mutually exclusive)."""
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--as-of", metavar="DATE|COMMIT",
                   help="read inputs from git at this date (end of day UTC) or commit")
    g.add_argument("--live", action="store_true",
                   help="read the working tree even when the committed output carries a pin")
    parser.add_argument("--pin", action="append", default=[], metavar="FILE=COMMIT",
                        help="with --as-of: read this one input from a different commit")
    return parser


def inputs_for(args, pin_source, repo=KIT, script=None):
    """Inputs per the CLI: explicit --as-of, else the committed output's own
    pin (unless --live), else the working tree. Prints the choice."""
    if args.as_of:
        pins = dict(p.split("=", 1) for p in args.pin)
        src, why = Inputs(args.as_of, repo, script, pins), f"--as-of {args.as_of}"
    elif not args.live and pin_from(pin_source):
        pin, pins = pin_from(pin_source)
        src, why = Inputs(pin, repo, script, pins), f"pin from {os.path.basename(pin_source)}"
    else:
        src, why = Inputs(None, repo, script), "working tree"
    print(f"inputs: {src.mode} [{why}]", file=sys.stderr)  # stderr: stdout may be the artifact
    return src
