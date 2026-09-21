#!/usr/bin/env python3
"""Seat-10 draft slate — one page, regenerated from the deck board + Yahoo ADP.

    python3 report/slate.py > report/seat-10-slate.md

Inputs: the deck pool (data/players.csv, 9-cat z over the draftable 156,
injury multipliers) for WHO, and the kit's Yahoo consensus file for WHEN
(P(still there at pick N) = Φ((ADP − N)/σ), σ = the mock-51 fit of pick − ADP
across 145 matched picks). Owner stances (2026-09-21) are constants below.
Regenerate after every ADP paste; the October paste makes the draft-night copy.
"""
import csv, datetime, math, os, re, sys, unicodedata

KIT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DECK = os.environ.get("DECK_REPO", os.path.join(KIT, "..", "yahoo-fantasy-basketball"))
sys.path.insert(0, os.path.join(DECK, "scripts"))
import hoops  # noqa: E402
hoops.DATA_PATH = os.path.join(DECK, "data", "players.csv")
ADP_FILE = os.environ.get("ADP_FILE", os.path.join(KIT, "report", "market", "consensus-2026-09-15.csv"))

SLOT, TEAMS, ROUNDS = 10, 12, 13
SIGMA = 16.6            # sd of (actual pick − Yahoo ADP), mock 51, n=145
NO_ADP = 175.0          # a player Yahoo does not rank: deep tail
LIKELY_MIN = 0.60       # "likely there"
FLIP_MIN = 0.35         # "coin flip"
REACH_MIN = 0.08        # "if he falls": REACH_MIN <= p < FLIP_MIN
ALIASES = {"cameron johnson": "cam johnson", "herbert jones": "herb jones"}  # kit/Yahoo spellings
# Owner stances, 2026-09-21 (kit after-report draft51-retro, decision sheet)
FADES = {"Brook Lopez": "owner: age, LAC situation — only if he is clearly the best left"}
AST_RULE = ("Assists are the acceptable casualty ONLY when the roster is winning confidently "
            "elsewhere: at your R6 pick (#63) read the category strip — if you rank top-4 in "
            "at least 5 of the other 8, stop paying for assists (no Lillard/Sheppard-class "
            "insurance reaches). If not, the punt is not earned yet; keep drafting value.")


def norm(n):
    s = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return " ".join(t for t in s.split() if t not in {"jr", "sr", "ii", "iii", "iv"})


def phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


players = [p for p in hoops.zscores(hoops.load_players()) if hoops.availability(p) > 0]
board = sorted(players, key=lambda p: -hoops.adj_value(p))
rank = {p["player"]: i + 1 for i, p in enumerate(board)}
# price per player: Yahoo ADP first (the room's price), Yahoo XRank next
# (Yahoo's own rank), the consensus average last — each LABELED, because the
# 9/15 file carries an ADP for 181 of the deck's 264 rows and an XRank for 222
adp = {}
with open(ADP_FILE, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        for col, label in (("yahoo_adp", "ADP"), ("yahoo_xrank", "XR"), ("consensus_avg", "cons")):
            try:
                adp[norm(r["player"])] = (float(r[col]), label)
                break
            except (TypeError, ValueError):
                continue


def adp_of(p):
    """(price, label) or None."""
    k = norm(p["player"])
    return adp.get(ALIASES.get(k, k))


def p_avail(p, n):
    a = adp_of(p)
    return phi(((a[0] if a is not None else NO_ADP) - n) / SIGMA)


def plus_cats(p):
    return [c for c, z in sorted(p["z"].items(), key=lambda kv: -kv[1]) if z >= 0.5][:3]


def tag(p):
    a = adp_of(p)
    price = f"{a[1]} {a[0]:.0f}" if a is not None else "no price"
    return f"{p['player']}{'▲' if hoops.availability(p) < 1 else ''} (#{rank[p['player']]}, {price})"


picks = [n + 1 for n in range(TEAMS * ROUNDS) if hoops.team_of_pick(n, TEAMS) == SLOT]
adp_date = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(ADP_FILE))
out = []
out.append(f"# Seat-10 slate — {'EXAMPLE, ' if 'consensus-2026-09-15' in ADP_FILE else ''}"
           f"board {datetime.date.today().isoformat()} · Yahoo ADP {adp_date.group(1) if adp_date else '?'}")
out.append("")
out.append(f"Who = the deck's 9-cat board (#rank; ▲ = injury multiplier ×0.78). When = the room's price turned into "
           f"now/next = chance he is still there at this pick / at your following pick (σ {SIGMA} picks, the "
           f"mock-51 fit). Price = Yahoo ADP where Yahoo lists one, else XR = Yahoo XRank, else cons = consensus average. "
           f"A high NEXT number means you can wait on him; a low one means it is now or never. "
           f"Three bands per pick: likely (≥60%), coin flip (35–60%), if he falls (<35%). The live card decides on the night.")
out.append("")
out.append("## Identity and rules")
out.append("- Value first; let the punt emerge (the slot-10 pair plan executed in mock 51: board #8/#6/#7/#9 at 10/15/34/39).")
out.append(f"- {AST_RULE}")
out.append("- From round 7 on, take the card's #1 unless you can say why not out loud (mock 51: the two costly picks were both deviations from a correct card).")
out.append("- Late center: " + "; ".join(f"**{k}** faded — {v}" for k, v in FADES.items()) + ".")
out.append("- Injury-multiplier players (▲, ×0.78) are priced in; take them at price, never as a reach.")
out.append("")
out.append("## Pick by pick")
for i, n in enumerate(picks):
    rnd = (n - 1) // TEAMS + 1
    n2 = picks[i + 1] if i + 1 < len(picks) else None
    pool = [p for p in board if p["player"] not in FADES]
    def fmt(p):
        nxt = f"/{p_avail(p, n2):.0%}" if n2 else ""
        return f"{tag(p)} {p_avail(p, n):.0%}{nxt}" + (f" +{'/'.join(plus_cats(p))}" if plus_cats(p) else "")
    likely = [p for p in pool if p_avail(p, n) >= LIKELY_MIN][:5]
    flip = [p for p in pool if FLIP_MIN <= p_avail(p, n) < LIKELY_MIN][:3]
    falls = [p for p in pool if REACH_MIN <= p_avail(p, n) < FLIP_MIN][:3]
    parts = []
    if likely: parts.append("likely: " + ", ".join(fmt(p) for p in likely))
    if flip: parts.append("coin flip: " + ", ".join(fmt(p) for p in flip))
    if falls: parts.append("if he falls: " + ", ".join(f"{tag(p)} {p_avail(p, n):.0%}" for p in falls))
    out.append(f"- **#{n} (R{rnd})** — " + " · ".join(parts))
out.append("")
out.append("## Late-center shortlist (your #130 / #135 / #154)")
early_c = [p for p in board if "C" in hoops.positions_of(p) and p["player"] not in FADES and rank[p["player"]] <= 90 and p_avail(p, 130) >= 0.5]
if len(early_c) < 2:
    out.append(f"- The shelf after the fade is thin ({len(early_c)} top-90 center{'s' if len(early_c) != 1 else ''} likely left at #130): "
               "secure your second center by #111 — the Poeltl / Porziņģis / Turner band above.")
cs = [p for p in board if "C" in hoops.positions_of(p) and p["player"] not in FADES and p_avail(p, 130) >= 0.5][:6]
out.append("- " + ", ".join(f"{tag(p)} {p_avail(p, 130):.0%}@130 {p_avail(p, 154):.0%}@154" + (f" +{'/'.join(plus_cats(p))}" if plus_cats(p) else "") for p in cs))
for k, v in FADES.items():
    p = next((q for q in board if q["player"] == k), None)
    if p:
        out.append(f"- ~~{tag(p)}~~ {p_avail(p, 130):.0%}@130 — {v}")
out.append("")
out.append("## Two reminders from mock 51")
out.append("- #82 Sheppard over Turner cost ~7 points of title odds; Turner was still there at #87 and went #102.")
out.append("- The 13th pick is a real pick: a center who starts beat a wing who never did by ~8 points.")
missing = [p["player"] for p in board[:120] if adp_of(p) is None]
xr = [p["player"] for p in board[:120] if adp_of(p) is not None and adp_of(p)[1] != "ADP"]
out.append("")
out.append(f"_Price source, top-120 board: Yahoo ADP for {120 - len(xr) - len(missing)}; XRank/consensus fallback for {len(xr)}"
           + (f" ({', '.join(xr[:12])}{'…' if len(xr) > 12 else ''})" if xr else "")
           + (f"; no price for {len(missing)} ({', '.join(missing)})" if missing else "") + "._")
print("\n".join(out))
