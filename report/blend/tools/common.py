"""Shared loader for the six-way blend (owner 2026-10-14, council 4–1): the five outside projections, keyed the kit's way."""
import ast, csv, os, sys
KIT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
DECK = os.environ.get("DECK_REPO", "/home/user/yahoo-fantasy-basketball")
sys.path.insert(0, os.path.join(DECK, "scripts"))
import range_check  # noqa: E402  (the deck's own name fold)
fold = range_check.fold
CATS = ["pts", "reb", "ast", "stl", "blk", "tpm", "tov", "fg_pct", "ft_pct"]
STAT = ["fg_pct", "fga", "ft_pct", "fta", "tpm", "pts", "reb", "ast", "stl", "blk", "tov"]
KITCOL = {"fg_pct": "fgp", "ft_pct": "ftp"}
MIN_REFS = 3
# label, pinned file, column prefix, percentage scale
SOURCES = [("Yahoo", "yahoo-proj-2026-10-13.csv", "", 1.0), ("Hashtag", "hashtag-2026-10-12.csv", "", 1.0),
           ("RotoBaller", "rotoballer-2026-10-13.csv", "src_", 100.0), ("FantasyPros", "fantasypros-2026-10-13.csv", "src_", 100.0),
           ("BBM cards", "cards-2026-10-13.csv", "src_", 100.0)]
# 2026-10-14 lock (owner: "Take the Yahoo and Hashtag projections dated today, and synergize with kit's"): BLEND_SET=lock
# swaps in the two outlets' 10/14 files; the other three outlets and the method are unchanged. Unset, the set above stands
# (Version 67's blend reproduces).
LOCK = os.environ.get("BLEND_SET") == "lock"
if LOCK:
    SOURCES = [("Yahoo", "yahoo-proj-2026-10-14.csv", "", 1.0), ("Hashtag", "hashtag-2026-10-14.csv", "", 1.0)] + SOURCES[2:]


def aliases():
    tree = ast.parse(open(os.path.join(KIT, "report", "market", "build_market.py"), encoding="utf-8").read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "ALIASES" for t in node.targets):
            return {fold(v): fold(k) for k, vs in ast.literal_eval(node.value).items() for v in vs}
    return {}


AL = aliases()


def canon(s):
    return AL.get(fold(s), fold(s))


def references():
    refs = {}
    for label, fn, pre, scale in SOURCES:
        for r in csv.DictReader(open(os.path.join(KIT, "report", "market", fn), encoding="utf-8-sig")):
            try:
                d = {c: float(r[pre + c]) / (scale if c.endswith("pct") else 1.0) for c in CATS}
            except (KeyError, TypeError, ValueError):
                continue
            refs.setdefault(canon(r["player"]), {})[label] = d
    return refs


def fmt(c, v):
    return f"{v:.3f}" if c.endswith("pct") else f"{v:.1f}"


def blend_cell(ours, ref, c):
    """Equal-weight mean of our value and every outside projection's value, rounded the planes' way."""
    vals = [ours] + [ref[s][c] for s in ref]
    return float(fmt(c, sum(vals) / len(vals)))
